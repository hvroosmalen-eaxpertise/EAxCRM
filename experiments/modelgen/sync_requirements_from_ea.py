"""Read Requirements from EAxCRM.qea and write them as Markdown.

Usage:
    python sync_requirements_from_ea.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-Requirements.md]
"""
import sys, os, argparse, sqlite3, re, textwrap


DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-Requirements.md"


def safe_id(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def main():
    parser = argparse.ArgumentParser(description="Sync requirements from EA to Markdown")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    conn = sqlite3.connect(args.qea)
    c = conn.cursor()

    # Find the EAxCRM Requirements package
    c.execute("SELECT Package_ID FROM t_package WHERE Name='EAxCRM Requirements'")
    row = c.fetchone()
    if not row:
        print("FAIL: 'EAxCRM Requirements' package not found in QEA file")
        sys.exit(1)
    pkg_id = row[0]

    # Read all Requirement elements in the package
    c.execute(
        "SELECT Object_ID, Name, IFNULL(Note, ''), ea_guid FROM t_object "
        "WHERE Package_ID=? AND Object_Type='Requirement' ORDER BY Object_ID",
        (pkg_id,)
    )
    elements = c.fetchall()
    print(f"Found {len(elements)} requirements")

    obj_info = {}
    for el in elements:
        oid, name, notes, guid = el
        obj_info[oid] = {"name": name, "guid": guid, "id": safe_id(name)}

    # Read connector hierarchy (Aggregation = parent-child)
    oid_list = [str(e[0]) for e in elements]
    c.execute(f"""
        SELECT Start_Object_ID, End_Object_ID
        FROM t_connector
        WHERE Start_Object_ID IN ({','.join(oid_list)})
          AND End_Object_ID IN ({','.join(oid_list)})
        ORDER BY Connector_ID
    """)
    connectors = c.fetchall()
    conn.close()

    # Build parent mapping: {child_id: [parent_ids]}
    parents_of = {}
    for src_id, tgt_id in connectors:
        # Aggregation: child (src) -> parent (tgt)
        parents_of.setdefault(src_id, []).append(tgt_id)

    # Build markdown
    lines = []
    lines.append("# EAxCRM \u2014 Requirements")
    lines.append("")
    lines.append("**Model ID**: r-eacrm")
    lines.append("**Purpose**: Requirements for the EAxCRM system")
    lines.append("**Version**: 1.0")
    lines.append("")

    # Topological sort: children before parents (leaf requirements first)
    # Simple approach: output children before their parents
    # First find top-level (no parent) vs child requirements
    all_child_ids = set()
    for child_id, parent_ids in parents_of.items():
        all_child_ids.update(parent_ids)

    def requirement_sort_key(el):
        oid, name, notes, guid = el
        has_parents = oid in parents_of
        num_children = sum(1 for c in parents_of if oid in parents_of.get(c, []))
        # Top-level requirements (no parent) come first
        # Within same level, sort by number of children (more = more important = first)
        # Then by name alphabetically
        return (0 if not has_parents else 1, -num_children, name.lower())

    sorted_elements = sorted(elements, key=requirement_sort_key)

    for el in sorted_elements:
        oid, name, notes, guid = el
        rid = obj_info[oid]["id"]

        lines.append(f"### Requirement\u2014{rid}")
        lines.append(f"- Name: {name}")
        if notes.strip():
            notes_clean = " ".join(notes.strip().split())
            lines.append(f"- Description: {notes_clean}")
        lines.append(f"- GUID: {guid}")
        if oid in parents_of:
            parent_ids = parents_of[oid]
            parent_names = []
            for pid in parent_ids:
                if pid in obj_info:
                    parent_names.append(obj_info[pid]["id"])
                else:
                    parent_names.append("(unknown)")
            lines.append(f"- Parents:" + (" (none)" if not parent_names else ""))
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


if __name__ == "__main__":
    main()
