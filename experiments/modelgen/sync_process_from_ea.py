"""Read BPMN 2.0 process model from EAxCRM.qea and write it as Markdown.

Reads CollaborationModel elements from the Process Architecture package,
including Pools, Lanes, flow elements (Tasks, Events, Gateways),
and SequenceFlow/MessageFlow connectors.

Usage:
    python sync_process_from_ea.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-ProcessModel.md]
"""
import sys, os, argparse, re
import win32com.client


DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-ProcessModel.md"

# Element types considered as flow elements within a Pool/Lane
BPMN_FLOW_TYPES = {
    "Activity", "Event", "Decision", "Gateway", "Object", "Note"
}

# Map EA Object_Type to readable BPMN category
BPMN_TYPE_LABEL = {
    "Activity": "Activity",
    "Event": "Event",
    "Decision": "Gateway",
    "Gateway": "Gateway",
    "Object": "DataObject",
    "Note": "Annotation",
}


def safe_id(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def get_tagged_value(el, tag_name):
    """Return the value of a tagged value by name, or empty string."""
    for t_idx in range(el.TaggedValues.Count):
        tv = el.TaggedValues.GetAt(t_idx)
        if tv.Name == tag_name:
            return tv.Value or ""
    return ""


def collect_tagged_values(el):
    """Return dict of all tagged values."""
    tags = {}
    for t_idx in range(el.TaggedValues.Count):
        tv = el.TaggedValues.GetAt(t_idx)
        tags[tv.Name] = tv.Value or ""
    return tags


def find_package(root, *names):
    """Navigate package hierarchy by names. Returns package or None."""
    pkg = root
    for name in names:
        found = None
        for i in range(pkg.Packages.Count):
            sp = pkg.Packages.GetAt(i)
            if sp.Name == name:
                found = sp
                break
        if not found:
            return None
        pkg = found
    return pkg


def main():
    parser = argparse.ArgumentParser(description="Sync BPMN process model from EA to Markdown")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    repo = win32com.client.Dispatch("EA.Repository")
    before_pids = get_ea_pids()
    try:
        repo.OpenFile(args.qea)
        root = repo.Models.GetAt(0)

        proc_pkg = find_package(root, "Process Architecture")
        if not proc_pkg:
            print("FAIL: 'Process Architecture' package not found")
            sys.exit(1)

        proc_pkg.Elements.Refresh()
        print(f"Process Architecture: {proc_pkg.Elements.Count} element(s)")

        # Collect all CollaborationModel elements
        collaborations = []
        for i in range(proc_pkg.Elements.Count):
            el = proc_pkg.Elements.GetAt(i)
            if el.Stereotype == "CollaborationModel":
                collaborations.append(el)
                print(f"  CollaborationModel: {el.Name} ({el.ElementGUID})")

        # Build element lookup for all elements in this package
        elem_by_id = {}
        for i in range(proc_pkg.Elements.Count):
            el = proc_pkg.Elements.GetAt(i)
            elem_by_id[el.ElementID] = el

        # Build parent→children mapping (via ParentID)
        children_of = {}  # parent_id → [child_element]
        for el in elem_by_id.values():
            pid = el.ParentID
            if pid and pid != 0 and pid in elem_by_id:
                children_of.setdefault(pid, []).append(el)

        # Build markdown
        lines = []
        lines.append("# EAxCRM — Process Architecture")
        lines.append("")
        lines.append("**Model ID**: pa-eacrm")
        lines.append("**Purpose**: BPMN 2.0 process model for the EAxCRM system")
        lines.append("**Version**: 1.0")
        lines.append("")

        for collab in collaborations:
            cid = safe_id(collab.Name)
            lines.append(f"## BPMN Collaboration—{cid}")
            lines.append(f"- Name: {collab.Name}")
            tags = collect_tagged_values(collab)
            if tags.get("documentation"):
                lines.append(f"- Documentation: {tags['documentation']}")
            if tags.get("isClosed") == "true":
                lines.append(f"- Is Closed: true")
            lines.append(f"- GUID: {collab.ElementGUID}")
            lines.append("")

            # Find immediate children (Pools and Processes)
            pool_children = children_of.get(collab.ElementID, [])
            # Also find elements in the same package that aren't children of another
            # (they may be linked via diagram rather than ParentID)
            free_elements = [
                el for el in elem_by_id.values()
                if el.ElementID != collab.ElementID
                and (el.ParentID == 0 or el.ParentID not in elem_by_id)
            ]

            def write_element_hierarchy(el, depth=0):
                """Recursively write an element and its children."""
                indent = "  " * depth
                prefix = "#" * (3 + depth)
                eid = safe_id(el.Name)
                stereo = el.Stereotype or el.Type
                # Build a display label
                label = stereo if stereo else el.Type
                lines.append(f"{prefix} {label}—{eid}")
                lines.append(f"{indent}- Name: {el.Name}")
                lines.append(f"{indent}- Type: {el.Stereotype or el.Type}")
                lines.append(f"{indent}- GUID: {el.ElementGUID}")

                notes = (el.Notes or "").strip()
                if notes:
                    lines.append(f"{indent}- Description: {notes[:500]}")

                # Tagged values
                tags = collect_tagged_values(el)
                for k, v in sorted(tags.items()):
                    if v and v not in ("<memo>", "") and k not in ("documentation",):
                        lines.append(f"{indent}- {k}: {v}")

                # Attributes (if any)
                if el.Attributes.Count > 0:
                    for a_idx in range(el.Attributes.Count):
                        a = el.Attributes.GetAt(a_idx)
                        lines.append(f"{indent}- {a.Name}: {a.Type}")

                lines.append("")

                # Recurse into children
                for child in children_of.get(el.ElementID, []):
                    write_element_hierarchy(child, depth + 1)

            # Write Pool/Process children
            for child in pool_children:
                write_element_hierarchy(child, 0)

            # Write free elements as top-level flow elements
            for child in free_elements:
                write_element_hierarchy(child, 0)

            # Process connectors
            connectors = []
            for el in elem_by_id.values():
                el.Connectors.Refresh()
                for j in range(el.Connectors.Count):
                    c = el.Connectors.GetAt(j)
                    stereo = c.Stereotype or ""
                    if stereo in ("SequenceFlow", "MessageFlow", "Association"):
                        src = elem_by_id.get(c.ClientID)
                        tgt = elem_by_id.get(c.SupplierID)
                        if src and tgt:
                            connectors.append({
                                "type": stereo,
                                "source": src.Name,
                                "target": tgt.Name,
                                "name": c.Name or "",
                                "guid": c.ConnectorGUID or "",
                            })

            if connectors:
                lines.append("### Sequence Flows")
                lines.append("")
                for c in connectors:
                    cond = f" [{c['name']}]" if c['name'] else ""
                    lines.append(f"- {c['source']} → {c['target']}{cond}")
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

    after_pids = get_ea_pids()
    new_pids = after_pids - before_pids
    if new_pids:
        for pid in new_pids:
            try:
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True, timeout=5)
            except:
                pass


def get_ea_pids():
    import subprocess
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-Process -Name EA | Select-Object -ExpandProperty Id"],
            capture_output=True, text=True, timeout=10
        )
        return set(int(pid) for pid in result.stdout.strip().split() if pid.isdigit())
    except:
        return set()


if __name__ == "__main__":
    main()
