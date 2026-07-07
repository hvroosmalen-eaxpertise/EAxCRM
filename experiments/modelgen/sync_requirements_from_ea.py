"""Read Requirements from EAxCRM.qea (via COM API) and write them as Markdown.

Usage:
    python sync_requirements_from_ea.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-Requirements.md]
"""
import sys, os, argparse, re
import ea_session
from changelog import ChangeLog, compute_md_diff

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-Requirements.md"


def safe_id(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def find_package(parent, name):
    """Recursively find a package by name."""
    for i in range(parent.Packages.Count):
        p = parent.Packages.GetAt(i)
        if p.Name == name:
            return p
        found = find_package(p, name)
        if found:
            return found
    return None


def main():
    parser = argparse.ArgumentParser(description="Sync requirements from EA to Markdown")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    try:
        import win32com.client
    except ImportError:
        print("FAIL: win32com not installed. Run: pip install pywin32")
        sys.exit(1)

    before_pids = ea_session.get_ea_pids()

    app = win32com.client.DispatchEx("EA.App")
    repo = app.Repository
    repo.OpenFile(args.qea)
    print(f"Connected: {repo.ConnectionString}")

    root = ea_session.get_model_root(repo)
    pkg = find_package(root, "EAxCRM Requirements")
    if not pkg:
        print("FAIL: 'EAxCRM Requirements' package not found")
        repo.CloseFile()
        ea_session.kill_new_ea_processes(before_pids)
        sys.exit(1)

    try:
        # Read all Requirement elements in the package
        elements = []
        pkg.Elements.Refresh()
        for i in range(pkg.Elements.Count):
            el = pkg.Elements.GetAt(i)
            if el.Type == "Requirement":
                elements.append(el)

        print(f"Found {len(elements)} requirements")

        # Build element lookup by ElementID
        elem_by_id = {}
        for el in elements:
            elem_by_id[el.ElementID] = el

        # Build element lookup by safe_id(name) for parent references
        elem_by_safeid = {}
        for el in elements:
            rid = safe_id(el.Name)
            elem_by_safeid[rid] = el

        # Build parent mapping from Aggregation connectors
        parents_of = {}
        # Build entity mapping from Realisation connectors
        entities_of = {}  # req ElementID → [entity names]

        # Find entity elements (in Data Architecture → EAxCRM Data Model)
        dm_pkg = None
        for i in range(root.Packages.Count):
            p = root.Packages.GetAt(i)
            if p.Name == "Data Architecture":
                for j in range(p.Packages.Count):
                    sp = p.Packages.GetAt(j)
                    if sp.Name == "EAxCRM Data Model":
                        dm_pkg = sp
                        break
                break

        entity_id_to_name = {}
        if dm_pkg:
            dm_pkg.Elements.Refresh()
            for i in range(dm_pkg.Elements.Count):
                el = dm_pkg.Elements.GetAt(i)
                entity_id_to_name[el.ElementID] = el.Name

        for el in elements:
            el.Connectors.Refresh()
            for j in range(el.Connectors.Count):
                conn = el.Connectors.GetAt(j)
                if conn.Type == "Aggregation" and conn.ClientID == el.ElementID:
                    if conn.SupplierID in elem_by_id:
                        parents_of.setdefault(el.ElementID, []).append(conn.SupplierID)
                elif conn.Type == "Realisation" and conn.SupplierID == el.ElementID:
                    # Requirement is the target of a Realisation connector from an entity
                    ent_name = entity_id_to_name.get(conn.ClientID)
                    if ent_name:
                        entities_of.setdefault(el.ElementID, []).append(ent_name)

        # Sort: top-level (no parents) before children
        def sort_key(el):
            has_parents = el.ElementID in parents_of
            # Count how many other elements have this element as parent (children count)
            num_children = sum(1 for c in parents_of if el.ElementID in parents_of.get(c, []))
            return (0 if not has_parents else 1, -num_children, el.Name.lower())

        sorted_elements = sorted(elements, key=sort_key)

        # Build markdown
        lines = []
        lines.append("# EAxCRM \u2014 Requirements")
        lines.append("")
        lines.append("**Model ID**: r-eacrm")
        lines.append("**Purpose**: Requirements for the EAxCRM system")
        lines.append("**Version**: 1.0")
        lines.append("")

        for el in sorted_elements:
            rid = safe_id(el.Name)
            notes = (el.Notes or "").strip()
            # Notes may contain "Rationale:" / "Test Cases:" sections appended
            # after the description (see build_notes() in the generator) —
            # those are sourced from Tagged Values below, so strip them here
            # to avoid duplicating them into the Description field.
            notes = re.split(r"\n\nRationale:", notes)[0].strip()

            el.TaggedValues.Refresh()
            rationale = ""
            test_cases = []
            for i in range(el.TaggedValues.Count):
                tv = el.TaggedValues.GetAt(i)
                if tv.Name == "Rationale":
                    rationale = (tv.Value or "").strip()
                elif tv.Name == "TestCases":
                    test_cases = [t for t in (tv.Value or "").split("\n") if t.strip()]

            lines.append(f"### Requirement\u2014{rid}")
            lines.append(f"- Name: {el.Name}")
            aid = (el.Alias or "").strip()
            lines.append(f"- ID: {aid}")
            if notes:
                notes_clean = " ".join(notes.split())
                lines.append(f"- Description: {notes_clean}")
            if rationale:
                lines.append(f"- Rationale: {' '.join(rationale.split())}")
            if test_cases:
                lines.append("- Test Cases:")
                for tc in test_cases:
                    lines.append(f"  - {tc.strip()}")
            entity_names = entities_of.get(el.ElementID)
            if entity_names:
                lines.append(f"- Entities: {', '.join(sorted(entity_names))}")
            lines.append(f"- Status: {el.Status or 'Proposed'}")
            lines.append(f"- Version: {el.Version or '1.0'}")
            lines.append(f"- GUID: {el.ElementGUID}")

            if el.ElementID in parents_of:
                parent_names = []
                for pid in parents_of[el.ElementID]:
                    parent = elem_by_id[pid]
                    parent_names.append(safe_id(parent.Name))
                lines.append("- Parents:" + (" (none)" if not parent_names else ""))
                for p in parent_names:
                    lines.append(f"  - {p}")
            else:
                lines.append("- Parents:")
                lines.append("  - (none \u2014 top-level)")
            lines.append("")

        output = "\n".join(lines) + "\n"

        # Read existing content and compute diff
        old_content = ""
        if os.path.exists(args.md):
            with open(args.md, "r", encoding="utf-8") as f:
                old_content = f.read()

        diff = compute_md_diff(old_content, output)
        clog = ChangeLog(os.path.join(SCRIPT_DIR, "requirements_changelog.md"))
        clog.checkpoint("Sync from EA")
        try:
            clog.log_diff(diff)
        finally:
            clog.close()

        with open(args.md, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Written {len(lines)} lines to {args.md}")
        print("Done.")

    finally:
        try:
            repo.CloseFile()
        except:
            pass

    # Kill zombie EA processes created by this script
    killed = ea_session.kill_new_ea_processes(before_pids)
    if killed:
        print(f"  Cleaned up {len(killed)} zombie EA process(es)")


if __name__ == "__main__":
    main()
