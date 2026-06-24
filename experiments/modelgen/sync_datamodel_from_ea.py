"""Read UML data model from EAxCRM.qea and write it as Markdown.

Reverse of generate_uml_datamodel.py:
  generate:  MD → EA (creates/updates elements, attributes, relationships)
  sync:      EA → MD (reads current EA state, writes MD file)

Usage:
    python sync_datamodel_from_ea.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-DataModel.md]
"""
import sys, os, argparse, sqlite3, re


DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-DataModel.md"

SPARX_TO_MD_TYPE = {
    "int": "int",
    "string": "string",
    "memo": "text",
    "datetime": "datetime",
    "date": "date",
    "boolean": "boolean",
    "float": "float",
}


def md_type(raw_type, length):
    raw = raw_type.lower().strip()
    mapped = SPARX_TO_MD_TYPE.get(raw, raw)
    if mapped == "string" and length and length > 0:
        return f"string({length})"
    return mapped


def safe_id(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def main():
    parser = argparse.ArgumentParser(description="Sync data model from EA to Markdown")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    conn = sqlite3.connect(args.qea)
    c = conn.cursor()

    # Find the EAxCRM Data Model package
    c.execute("SELECT Package_ID FROM t_package WHERE Name='EAxCRM Data Model'")
    row = c.fetchone()
    if not row:
        print("FAIL: 'EAxCRM Data Model' package not found in QEA file")
        sys.exit(1)
    pkg_id = row[0]

    # Read all Class elements in the package
    c.execute(
        "SELECT Object_ID, Name, IFNULL(Note, ''), ea_guid FROM t_object "
        "WHERE Package_ID=? AND Object_Type='Class' ORDER BY Name",
        (pkg_id,)
    )
    elements = c.fetchall()
    print(f"Found {len(elements)} elements")

    # Build lookup: Object_ID -> {name, guid}
    obj_info = {e[0]: {"name": e[1], "guid": e[3]} for e in elements}

    # Read attributes per element
    attrs_by_obj = {}
    for el in elements:
        oid = el[0]
        c.execute(
            "SELECT Name, Type, Length, IFNULL(Stereotype, ''), IFNULL(Notes, '') "
            "FROM t_attribute WHERE Object_ID=? ORDER BY ID",
            (oid,)
        )
        attrs_by_obj[oid] = c.fetchall()

    # Read connectors between elements in this package
    oid_list = [str(e[0]) for e in elements]
    c.execute(f"""
        SELECT Start_Object_ID, End_Object_ID,
               IFNULL(SourceCard, '*'), IFNULL(DestCard, '1'),
               IFNULL(Notes, ''), IFNULL(ea_guid, '')
        FROM t_connector
        WHERE Start_Object_ID IN ({','.join(oid_list)})
          AND End_Object_ID IN ({','.join(oid_list)})
        ORDER BY Connector_ID
    """)
    connectors = c.fetchall()
    conn.close()

    # Build markdown
    lines = []
    lines.append("# EAxCRM — Data Model")
    lines.append("")
    lines.append("**Model ID**: dm-eacrm")
    lines.append("**Purpose**: Logical data model for the EAxCRM Django application")
    lines.append("**Version**: 1.0")
    lines.append("")
    lines.append("## Entities")
    lines.append("")

    for el in elements:
        oid, name, notes, guid = el
        eid = safe_id(name)
        lines.append(f"### Class—{eid}")
        lines.append(f"- Name: {name}")
        if notes.strip():
            lines.append(f"- Description: {notes.strip()}")
        lines.append(f"- GUID: {guid}")
        lines.append("- Attributes:")

        attrs = attrs_by_obj.get(oid, [])
        if attrs:
            for a in attrs:
                aname, atype, alen, aster, anotes = a
                tstr = md_type(atype, alen)
                parts = [f"  - {aname}: {tstr}"]
                if aster:
                    parts[-1] += f" <<{aster}>>"
                if anotes:
                    parts[-1] += f" — {anotes}"
                lines.append(parts[-1])
        else:
            lines.append("  - (none)")
        lines.append("")

    lines.append("## Relationships")
    lines.append("")

    seen_rel_ids = set()
    for src_id, tgt_id, src_card, dst_card, notes, guid in connectors:
        src_info = obj_info.get(src_id)
        tgt_info = obj_info.get(tgt_id)
        if not src_info or not tgt_info:
            continue

        src_name = src_info["name"]
        tgt_name = tgt_info["name"]
        src_sid = safe_id(src_name)
        tgt_sid = safe_id(tgt_name)

        rel_id = f"r-{src_sid}-{tgt_sid}"
        if rel_id in seen_rel_ids:
            continue
        seen_rel_ids.add(rel_id)

        lines.append(f"### Association—{rel_id}")
        lines.append(f"- Source: {src_sid} ({src_card})")
        lines.append(f"- Target: {tgt_sid} ({dst_card})")
        if notes.strip():
            lines.append(f"- Description: {notes.strip()}")
        if not guid.strip():
            import uuid
            guid = "{" + str(uuid.uuid4()).upper() + "}"
        lines.append(f"- GUID: {guid}")
        lines.append("")

    output = "\n".join(lines) + "\n"

    with open(args.md, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Written {len(lines)} lines to {args.md}")
    print("Done.")


if __name__ == "__main__":
    main()
