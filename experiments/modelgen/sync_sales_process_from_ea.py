"""Read Sales BPMN process model from EAxCRM.qea and write as Markdown (flat format).

Usage:
    python sync_sales_process_from_ea.py
"""
import sys, os, argparse, re, sqlite3

DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-SalesProcess.md"

BPMN_TYPE_LABEL = {
    "Activity": "Activity",
    "Event": "Event",
    "Decision": "Gateway",
    "Gateway": "Gateway",
    "Object": "DataObject",
    "Artifact": "Artifact",
    "ActivityPartition": "Lane",
}

PACKAGE_NAME = "Sales Process Architecture"
MODEL_ID = "sp-eacrm"
PURPOSE = "BPMN 2.0 sales process model for the EAxCRM system"

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
    "StartEvent": {
        "eventType": "Event Type",
        "triggerType": "Trigger",
    },
    "EndEvent": {
        "eventType": "Event Type",
        "triggerType": "Result",
    },
    "IntermediateEvent": {
        "eventType": "Event Type",
        "triggerType": "Trigger",
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
    return re.sub(r"[^a-zA-Z0-9]", "", name)

def main():
    parser = argparse.ArgumentParser(description=f"Sync {PACKAGE_NAME} from EA to Markdown")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    conn = sqlite3.connect(args.qea)
    c = conn.cursor()

    c.execute("SELECT Package_ID FROM t_package WHERE Name='Process Architecture' AND Parent_ID=1")
    parent_row = c.fetchone()
    if not parent_row:
        print("FAIL: 'Process Architecture' package not found under Model")
        sys.exit(1)
    parent_pkg_id = parent_row[0]

    pkg_id = None
    c.execute("SELECT Package_ID FROM t_package WHERE Name=? AND Parent_ID=?", (PACKAGE_NAME, parent_pkg_id))
    row = c.fetchone()
    if row:
        pkg_id = row[0]
        print(f"Found sub-package '{PACKAGE_NAME}' (ID {pkg_id})")
        c.execute(
            "SELECT Object_ID, Name, Object_Type, IFNULL(Stereotype, ''), "
            "IFNULL(ParentID, 0), IFNULL(Note, ''), IFNULL(ea_guid, '') "
            "FROM t_object WHERE Package_ID=? ORDER BY Name", (pkg_id,)
        )
    else:
        c.execute(
            "SELECT Object_ID, Name, Object_Type, IFNULL(Stereotype, ''), "
            "IFNULL(ParentID, 0), IFNULL(Note, ''), IFNULL(ea_guid, '') "
            "FROM t_object WHERE Package_ID=? AND Stereotype='CollaborationModel' AND Name LIKE '%Sales%'",
            (parent_pkg_id,)
        )
        cm_row = c.fetchone()
        if not cm_row:
            print(f"FAIL: No sales CollaborationModel found in Process Architecture package")
            sys.exit(1)
        cm_oid = cm_row[0]
        pkg_id = parent_pkg_id
        print(f"Found CollaborationModel '{cm_row[1]}' (OID {cm_oid}) in Process Architecture package")

        all_oids = [cm_oid]
        cursor = 0
        while cursor < len(all_oids):
            c.execute("SELECT Object_ID FROM t_object WHERE ParentID=?", (all_oids[cursor],))
            for (oid,) in c.fetchall():
                if oid not in all_oids:
                    all_oids.append(oid)
            cursor += 1

        oid_list = ",".join(str(oid) for oid in all_oids)
        c.execute(
            f"SELECT Object_ID, Name, Object_Type, IFNULL(Stereotype, ''), "
            f"IFNULL(ParentID, 0), IFNULL(Note, ''), IFNULL(ea_guid, '') "
            f"FROM t_object WHERE Object_ID IN ({oid_list})"
        )

    elements = c.fetchall()
    print(f"Found {len(elements)} elements")

    elem_by_id = {}
    cols = ["oid", "name", "type", "stereo", "parent", "notes", "guid"]
    for e in elements:
        elem_by_id[e[0]] = dict(zip(cols, e))

    # Read tagged values
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

    # Read diagram
    c.execute(
        "SELECT Diagram_ID, Name, ParentID, IFNULL(ea_guid, '') "
        "FROM t_diagram WHERE Package_ID=?", (pkg_id,)
    )
    diagram_by_parent = {}
    for d_id, d_name, d_parent, d_guid in c.fetchall():
        diagram_by_parent[d_parent] = {"name": d_name, "guid": d_guid}

    # Read connectors
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

    # Build children mapping
    children_of = {}
    parent_of = {}
    for info in elem_by_id.values():
        pid = info["parent"]
        parent_of[info["oid"]] = pid
        if pid and pid != 0 and pid in elem_by_id:
            children_of.setdefault(pid, []).append(info["oid"])
    for pid in children_of:
        children_of[pid].sort(key=lambda oid: elem_by_id[oid]["name"].lower())

    # Identify lane IDs and their safe_ids for Lane field output
    lane_info = {}  # oid -> {name, safe_id}
    for info in elem_by_id.values():
        if info["type"] == "ActivityPartition":
            lane_info[info["oid"]] = {"name": info["name"], "safe_id": safe_id(info["name"])}

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

        # Flatten: write all non-CM, non-Lane descendants at ### level
        # with - Lane: field based on their lane ancestor
        def find_lane_ancestor(oid):
            pid = parent_of.get(oid)
            while pid and pid in elem_by_id:
                if pid in lane_info:
                    return lane_info[pid]["safe_id"]
                pid = parent_of.get(pid)
            return None

        # Collect all descendants of CM that are not CM and not Lanes
        non_lane_oids = set()
        lane_oids = set()
        for info in elem_by_id.values():
            oid = info["oid"]
            if oid == cid:
                continue
            if info["type"] == "ActivityPartition":
                lane_oids.add(oid)
            else:
                non_lane_oids.add(oid)

        # Write lanes first (at ### level), then non-lane elements
        ordered_oids = sorted(lane_oids, key=lambda o: elem_by_id[o]["name"].lower())
        ordered_oids += sorted(non_lane_oids, key=lambda o: elem_by_id[o]["name"].lower())

        # Generate unique element IDs — detect collisions and disambiguate with type suffix
        eid_by_oid = {}
        eid_count = {}
        for oid in ordered_oids:
            info = elem_by_id[oid]
            eid = safe_id(info["name"])
            eid_count[eid] = eid_count.get(eid, 0) + 1
        for oid in ordered_oids:
            info = elem_by_id[oid]
            eid = safe_id(info["name"])
            label = BPMN_TYPE_LABEL.get(info["type"], info["type"])
            if stereo_label := (info["stereo"] if info["stereo"] != info["type"] else None):
                label = stereo_label
            if eid_count[eid] > 1:
                eid_by_oid[oid] = eid + "_" + safe_id(label)
            else:
                eid_by_oid[oid] = eid

        for oid in ordered_oids:
            info = elem_by_id[oid]
            eid = eid_by_oid[oid]
            stereo = info["stereo"] or info["type"]
            label = BPMN_TYPE_LABEL.get(info["type"], info["type"])
            if stereo and stereo != info["type"]:
                label = stereo

            lines.append(f"### {label}—{eid}")
            lines.append(f"- Name: {info['name']}")
            lines.append(f"- Type: {info['type']}")
            if info["stereo"]:
                lines.append(f"- Stereotype: {info['stereo']}")
            lines.append(f"- GUID: {info['guid']}")

            # Lane field for non-lane elements
            if oid not in lane_oids:
                lane_ref = find_lane_ancestor(oid)
                if lane_ref:
                    lines.append(f"- Lane: {lane_ref}")

            tags_meta = BPMN_TAGGED_VALUES.get(info["stereo"], {})
            if not tags_meta:
                tags_meta = BPMN_TAGGED_VALUES.get(info["type"], {})
            elem_tvs = tv_by_elem.get(oid, {})
            for k, label_text in sorted(tags_meta.items()):
                v = elem_tvs.get(k, "")
                if v and v not in ("<memo>", ""):
                    lines.append(f"- {label_text}: {v}")

            notes = info["notes"].strip()
            if notes:
                lines.append(f"- Description: {notes[:500]}")
            lines.append("")

    # Connectors — group by type
    def add_connector_section(stereo_filter, heading_label):
        filtered = [c for c in connectors if c[2] == stereo_filter]
        if not filtered:
            return
        lines.append(f"### {heading_label}")
        lines.append("")
        seen = set()
        for src_id, tgt_id, stereo, name, notes, guid in filtered:
            key = (src_id, tgt_id, name.strip())
            if key in seen:
                continue
            seen.add(key)
            src_eid = eid_by_oid.get(src_id, safe_id(elem_by_id.get(src_id, {}).get("name", f"ID:{src_id}")))
            tgt_eid = eid_by_oid.get(tgt_id, safe_id(elem_by_id.get(tgt_id, {}).get("name", f"ID:{tgt_id}")))
            cond = f" [{name}]" if name.strip() else ""
            lines.append(f"- {src_eid} → {tgt_eid}{cond}")
        lines.append("")

    add_connector_section("SequenceFlow", "Sequence Flows")
    add_connector_section("MessageFlow", "Message Flows")
    add_connector_section("DataInputAssociation", "Data Input Associations")
    add_connector_section("DataOutputAssociation", "Data Output Associations")

    output = "\n".join(lines) + "\n"
    with open(args.md, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Written {len(lines)} lines to {args.md}")
    print("Done.")

if __name__ == "__main__":
    main()
