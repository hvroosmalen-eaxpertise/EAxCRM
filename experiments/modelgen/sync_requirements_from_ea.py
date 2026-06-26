"""Read Requirements from EAxCRM.qea (via COM API) and write them as Markdown.

Usage:
    python sync_requirements_from_ea.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-Requirements.md]
"""
import sys, os, argparse, re


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


def get_ea_pids():
    """Return set of EA process IDs currently running."""
    import subprocess
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq EA.exe", "/FO", "CSV"],
            capture_output=True, text=True, timeout=10
        )
        pids = set()
        for line in result.stdout.strip().split("\n")[1:]:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                try:
                    pids.add(int(parts[1].strip('"')))
                except ValueError:
                    pass
        return pids
    except:
        return set()


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

    before_pids = get_ea_pids()

    repo = win32com.client.Dispatch("EA.Repository")
    repo.OpenFile(args.qea)
    print(f"Connected: {repo.ConnectionString}")

    root = repo.Models.GetAt(0)
    pkg = find_package(root, "EAxCRM Requirements")
    if not pkg:
        print("FAIL: 'EAxCRM Requirements' package not found")
        repo.CloseFile()
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
        for el in elements:
            el.Connectors.Refresh()
            for j in range(el.Connectors.Count):
                conn = el.Connectors.GetAt(j)
                if conn.Type == "Aggregation" and conn.ClientID == el.ElementID:
                    if conn.SupplierID in elem_by_id:
                        parents_of.setdefault(el.ElementID, []).append(conn.SupplierID)

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

            lines.append(f"### Requirement\u2014{rid}")
            lines.append(f"- Name: {el.Name}")
            aid = (el.Alias or "").strip()
            lines.append(f"- ID: {aid}")
            if notes:
                notes_clean = " ".join(notes.split())
                lines.append(f"- Description: {notes_clean}")
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
    after_pids = get_ea_pids()
    new_pids = after_pids - before_pids
    if new_pids:
        import subprocess
        for pid in new_pids:
            try:
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True, timeout=5)
            except:
                pass


if __name__ == "__main__":
    main()
