"""Read UML data model from EAxCRM.qea and write it as Markdown.

Reverse of generate_uml_datamodel.py:
  generate:  MD → EA (creates/updates elements, attributes, relationships)
  sync:      EA → MD (reads current EA state, writes MD file)

COM-only via ``ea_session.sql_rows`` (Repository.SQLQuery). Never uses
sqlite3 directly -- see ``ea-model-common`` HARD RULE, and the sibling
sync_archimate_from_ea.py for the pattern this retrofit follows
(step 3/3 of the #17 #7 push).

Usage:
    python sync_datamodel_from_ea.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-DataModel.md]
"""
import sys, os, argparse, re
import ea_session
from changelog import ChangeLog, compute_md_diff


DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-DataModel.md"

SPARX_TO_MD_TYPE = {
    "int": "int",
    "string": "string",
    "memo": "string",
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
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="Sync data model from EA to Markdown")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    with ea_session.ea_repository(args.qea) as repo:
        # Find the EAxCRM Data Model package. Silent-failure trap: bad SQL
        # returns [] just like a legitimate not-found; assert non-empty and
        # fail loud since a missing package is a hard error, not "0 elements".
        rows = ea_session.sql_rows(repo, """
            SELECT Package_ID FROM t_package WHERE Name = 'EAxCRM Data Model'
        """)
        if not rows:
            print("FAIL: 'EAxCRM Data Model' package not found in EA repository")
            sys.exit(1)
        pkg_id = int(rows[0]["Package_ID"])

        # Read all Class + Enumeration elements in the package. Values from
        # sql_rows are always strings; cast Object_ID for int-key lookups.
        elem_rows = ea_session.sql_rows(repo, f"""
            SELECT Object_ID, Name, Object_Type,
                   IFNULL(Note, '') AS Note, ea_guid
            FROM t_object
            WHERE Package_ID = {pkg_id} AND Object_Type IN ('Class', 'Enumeration')
            ORDER BY Name
        """)
        all_elements = [
            (int(r["Object_ID"]), r["Name"], r["Object_Type"], r["Note"], r["ea_guid"])
            for r in elem_rows
        ]
        elements = [e for e in all_elements if e[2] == "Class"]
        enum_elements = [e for e in all_elements if e[2] == "Enumeration"]
        print(f"Found {len(elements)} elements, {len(enum_elements)} enumerations")

        # Build lookup: Object_ID -> {name, type, guid}
        obj_info = {e[0]: {"name": e[1], "type": e[2], "guid": e[4]} for e in all_elements}
        # Attribute.Type is stored/read case-sensitively as authored (e.g. "ContactRole"),
        # but isn't linked back to the Enumeration element via Classifier (see
        # generate_uml_datamodel.py's sync_attribute docstring) -- match by name instead.
        enum_name_by_lower = {e[1].lower(): e[1] for e in enum_elements}

        # Read attributes/literals in a single wide query, then bucket by
        # Object_ID in Python -- avoids an N+1 query loop AND avoids the
        # silent-failure trap where a typo in a per-element query would
        # return "0 attributes for every element" with no exception.
        if all_elements:
            oid_all_list = ",".join(str(e[0]) for e in all_elements)
            attr_rows = ea_session.sql_rows(repo, f"""
                SELECT Object_ID, Name, Type, Length,
                       IFNULL(Stereotype, '') AS Stereotype,
                       IFNULL(Notes, '') AS Notes, ID
                FROM t_attribute
                WHERE Object_ID IN ({oid_all_list})
                ORDER BY Object_ID, ID
            """)
            attrs_by_obj = {}
            for r in attr_rows:
                oid = int(r["Object_ID"])
                # Length may arrive as empty string when null; coerce to
                # int/0 to match sqlite3 behavior the downstream md_type()
                # expects.
                length_str = r["Length"]
                length = int(length_str) if length_str.strip() else 0
                attrs_by_obj.setdefault(oid, []).append(
                    (r["Name"], r["Type"], length, r["Stereotype"], r["Notes"])
                )
        else:
            attrs_by_obj = {}

        # Read connectors between elements in this package. Empty element
        # list would produce a syntactically-invalid "IN ()" clause; guard.
        if elements:
            oid_list = ",".join(str(e[0]) for e in elements)
            conn_rows = ea_session.sql_rows(repo, f"""
                SELECT Start_Object_ID, End_Object_ID,
                       IFNULL(SourceCard, '*') AS SourceCard,
                       IFNULL(DestCard, '1') AS DestCard,
                       IFNULL(Notes, '') AS Notes,
                       IFNULL(ea_guid, '') AS ea_guid,
                       IFNULL(Name, '') AS Name
                FROM t_connector
                WHERE Start_Object_ID IN ({oid_list})
                  AND End_Object_ID IN ({oid_list})
                ORDER BY Connector_ID
            """)
            connectors = [
                (int(r["Start_Object_ID"]), int(r["End_Object_ID"]),
                 r["SourceCard"], r["DestCard"], r["Notes"], r["ea_guid"], r["Name"])
                for r in conn_rows
            ]
        else:
            connectors = []

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
        oid, name, _typ, notes, guid = el
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
                enum_ref = enum_name_by_lower.get(atype.lower().strip())
                tstr = enum_ref if enum_ref else md_type(atype, alen)
                parts = [f"  - {aname}: {tstr}"]
                if aster:
                    parts[-1] += f" <<{aster}>>"
                if anotes:
                    parts[-1] += f" — {anotes}"
                lines.append(parts[-1])
        else:
            lines.append("  - (none)")
        lines.append("")

    for el in enum_elements:
        oid, name, _typ, notes, guid = el
        eid = safe_id(name)
        lines.append(f"### Enumeration—{eid}")
        lines.append(f"- Name: {name}")
        if notes.strip():
            lines.append(f"- Description: {notes.strip()}")
        lines.append(f"- GUID: {guid}")
        lines.append("- Literals:")

        literals = attrs_by_obj.get(oid, [])
        if literals:
            for lit in literals:
                lines.append(f"  - {lit[0]}")
        else:
            lines.append("  - (none)")
        lines.append("")

    lines.append("## Relationships")
    lines.append("")

    seen_rel_ids = set()
    for src_id, tgt_id, src_card, dst_card, notes, guid, conn_name in connectors:
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
        if conn_name.strip():
            lines.append(f"- Name: {conn_name.strip()}")
        if notes.strip():
            lines.append(f"- Description: {notes.strip()}")
        if not guid.strip():
            import uuid
            guid = "{" + str(uuid.uuid4()).upper() + "}"
        lines.append(f"- GUID: {guid}")
        lines.append("")

    new_content = "\n".join(lines) + "\n"

    # Changelog: diff against previous MD
    old_content = ""
    if os.path.exists(args.md):
        with open(args.md, "r", encoding="utf-8") as f:
            old_content = f.read()

    diff = compute_md_diff(old_content, new_content)
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    clog = ChangeLog(os.path.join(SCRIPT_DIR, "uml_datamodel_changelog.md"))
    clog.checkpoint("Sync from EA")
    try:
        clog.log_diff(diff)
    finally:
        clog.close()

    with open(args.md, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Written {len(lines)} lines to {args.md}")
    print("Done.")


if __name__ == "__main__":
    main()
