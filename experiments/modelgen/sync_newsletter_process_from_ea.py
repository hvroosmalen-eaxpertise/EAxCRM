"""Read Newsletter BPMN process model from EAxCRM.qea and write as Markdown.

Usage:
    python sync_newsletter_process_from_ea.py
"""
import sys, os, argparse, re, sqlite3

DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-NewsletterProcess.md"

BPMN_TYPE_LABEL = {
    "Activity": "Activity",
    "Event": "Event",
    "Decision": "Gateway",
    "Gateway": "Gateway",
    "Object": "DataObject",
    "Artifact": "Artifact",
    "ActivityPartition": "Lane",
}

PACKAGE_NAME = "Newsletter Process Architecture"
MODEL_ID = "nlp-eacrm"
PURPOSE = "BPMN 2.0 newsletter process model for the EAxCRM system"

BPMN_TAGGED_VALUES = {
    "Activity": {
        "taskType": "Task Type",
        "loopCharacteristics": "Loop",
        "completionQuantity": "Completion Quantity",
        "startQuantity": "Start Quantity",
        "isForCompensation": "Is For Compensation",
        "isACalledActivity": "Is Called Activity",
        "calledElement": "Called Element",
    },
    "SubProcess": {
        "loopCharacteristics": "Loop",
        "completionQuantity": "Completion Quantity",
        "startQuantity": "Start Quantity",
        "isForCompensation": "Is For Compensation",
        "adHoc": "Ad Hoc",
        "adhocOrdering": "Ad Hoc Ordering",
        "adhocCompletionCondition": "Ad Hoc Completion Condition",
    },
    "Event": {
        "eventType": "Event Type",
        "triggerType": "Trigger",
    },
    "StartEvent": {
        "eventType": "Event Type",
        "triggerType": "Trigger",
    },
    "EndEvent": {
        "eventType": "Event Type",
        "triggerType": "Result",
    },
    "Gateway": {
        "gatewayType": "Gateway Type",
    },
    "ExclusiveGateway": {
        "gatewayType": "Gateway Type",
    },
    "ParallelGateway": {
        "gatewayType": "Gateway Type",
    },
    "Lane": {
        "partitionElement": "Partition Element",
    },
    "Pool": {
        "processRef": "Process Ref",
    },
    "CollaborationModel": {
        "isClosed": "Is Closed",
        "mainPool": "Main Pool",
        "correlationKeys": "Correlation Keys",
        "choreographyRef": "Choreography Ref",
    },
    "DataObject": {
        "dataObjectRef": "Data Object Ref",
        "isCollection": "Is Collection",
    },
}

def safe_id(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())

def main():
    parser = argparse.ArgumentParser(description=f"Sync {PACKAGE_NAME} from EA to Markdown")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    conn = sqlite3.connect(args.qea)
    c = conn.cursor()

    c.execute("SELECT Package_ID FROM t_package WHERE Name=?", (PACKAGE_NAME,))
    row = c.fetchone()
    if not row:
        print(f"FAIL: '{PACKAGE_NAME}' package not found")
        sys.exit(1)
    pkg_id = row[0]

    c.execute(
        "SELECT Object_ID, Name, Object_Type, IFNULL(Stereotype, ''), "
        "IFNULL(ParentID, 0), IFNULL(Note, ''), IFNULL(ea_guid, '') "
        "FROM t_object WHERE Package_ID=? ORDER BY Name",
        (pkg_id,)
    )
    elements = c.fetchall()
    print(f"Found {len(elements)} elements")

    elem_by_id = {}
    cols = ["oid", "name", "type", "stereo", "parent", "notes", "guid"]
    for e in elements:
        elem_by_id[e[0]] = dict(zip(cols, e))

    oid_list = [str(e[0]) for e in elements]
    tv_by_elem = {}
    c.execute(f"""
        SELECT Object_ID, Property, Value
        FROM t_objectproperties
        WHERE Object_ID IN ({','.join(oid_list)})
    """)
    for tv_oid, prop, val in c.fetchall():
        if val and val.strip():
            tv_by_elem.setdefault(tv_oid, {})[prop] = val.strip()

    c.execute(
        "SELECT Diagram_ID, Name, ParentID, IFNULL(ea_guid, '') "
        "FROM t_diagram WHERE Package_ID=?",
        (pkg_id,)
    )
    diagram_by_parent = {}
    for d_id, d_name, d_parent, d_guid in c.fetchall():
        diagram_by_parent[d_parent] = {"name": d_name, "guid": d_guid}

    c.execute(f"""
        SELECT Start_Object_ID, End_Object_ID,
               IFNULL(Stereotype, ''), IFNULL(Name, ''), IFNULL(Notes, ''),
               IFNULL(ea_guid, '')
        FROM t_connector
        WHERE Start_Object_ID IN ({','.join(oid_list)})
          AND End_Object_ID IN ({','.join(oid_list)})
        ORDER BY Connector_ID
    """)
    connectors = c.fetchall()
    print(f"  {len(connectors)} connector(s)")
    conn.close()

    children_of = {}
    for info in elem_by_id.values():
        pid = info["parent"]
        if pid and pid != 0 and pid in elem_by_id:
            children_of.setdefault(pid, []).append(info["oid"])
    for pid in children_of:
        children_of[pid].sort(key=lambda oid: elem_by_id[oid]["name"].lower())

    def sort_topological(oid_list):
        lane_ids = [oid for oid in oid_list if elem_by_id[oid]["type"] == "ActivityPartition"]
        other_ids = [oid for oid in oid_list if oid not in lane_ids]
        lane_ids.sort(key=lambda oid: elem_by_id[oid]["name"].lower())
        other_ids.sort(key=lambda oid: elem_by_id[oid]["name"].lower())
        return lane_ids + other_ids

    lines = []
    header_name = PACKAGE_NAME
    lines.append(f"# EAxCRM — {header_name}")
    lines.append("")
    lines.append(f"**Model ID**: {MODEL_ID}")
    lines.append(f"**Purpose**: {PURPOSE}")
    lines.append("**Version**: 1.0")
    lines.append("")

    collab_ids = [info["oid"] for info in elem_by_id.values()
                  if info["stereo"] == "CollaborationModel"]

    for cid in collab_ids:
        col = elem_by_id[cid]
        ccid = safe_id(col["name"])
        notes = col["notes"].strip()

        lines.append(f"## BPMN Collaboration—{ccid}")
        lines.append(f"- Name: {col['name']}")
        lines.append(f"- GUID: {col['guid']}")
        dia = diagram_by_parent.get(cid)
        if dia:
            lines.append(f"- Diagram Name: {dia['name']}")
            lines.append(f"- Diagram GUID: {dia['guid']}")
        for k, label in sorted(BPMN_TAGGED_VALUES.get("CollaborationModel", {}).items()):
            v = tv_by_elem.get(cid, {}).get(k, "")
            if v and v not in ("<memo>", ""):
                lines.append(f"- {label}: {v}")
        if notes:
            lines.append(f"- Description: {notes[:500]}")
        lines.append("")

        def write_element(oid, depth=0):
            info = elem_by_id[oid]
            indent = "  " * depth
            prefix = "#" * (3 + depth)
            eid = safe_id(info["name"])
            stereo = info["stereo"] or info["type"]
            label = BPMN_TYPE_LABEL.get(info["type"], info["type"])
            if stereo and stereo != info["type"]:
                label = stereo

            lines.append(f"{prefix} {label}—{eid}")
            lines.append(f"{indent}- Name: {info['name']}")
            lines.append(f"{indent}- Type: {info['type']}")
            if info["stereo"]:
                lines.append(f"{indent}- Stereotype: {info['stereo']}")
            lines.append(f"{indent}- GUID: {info['guid']}")

            tags_meta = BPMN_TAGGED_VALUES.get(info["stereo"], {})
            if not tags_meta:
                tags_meta = BPMN_TAGGED_VALUES.get(info["type"], {})
            elem_tvs = tv_by_elem.get(oid, {})
            for k, label_text in sorted(tags_meta.items()):
                v = elem_tvs.get(k, "")
                if v and v not in ("<memo>", ""):
                    lines.append(f"{indent}- {label_text}: {v}")

            notes = info["notes"].strip()
            if notes:
                lines.append(f"{indent}- Description: {notes[:500]}")
            lines.append("")

            for child_oid in children_of.get(oid, []):
                write_element(child_oid, depth + 1)

        top_children = sort_topological(children_of.get(cid, []))
        for child_oid in top_children:
            write_element(child_oid, 0)

        free_ids = [info["oid"] for info in elem_by_id.values()
                    if info["oid"] != cid
                    and (info["parent"] == 0 or info["parent"] not in elem_by_id)]
        for child_oid in sorted(free_ids, key=lambda o: elem_by_id[o]["name"].lower()):
            write_element(child_oid, 0)

    flow_connectors = [c for c in connectors if c[2] in ("SequenceFlow", "MessageFlow")]
    if flow_connectors:
        lines.append("### Sequence Flows")
        lines.append("")
        for src_id, tgt_id, stereo, name, notes, guid in flow_connectors:
            src_name = elem_by_id.get(src_id, {}).get("name", f"ID:{src_id}")
            tgt_name = elem_by_id.get(tgt_id, {}).get("name", f"ID:{tgt_id}")
            cond = f" [{name}]" if name.strip() else ""
            lines.append(f"- {src_name} → {tgt_name}{cond}")
        lines.append("")

    output = "\n".join(lines) + "\n"
    with open(args.md, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Written {len(lines)} lines to {args.md}")
    print("Done.")

if __name__ == "__main__":
    main()
