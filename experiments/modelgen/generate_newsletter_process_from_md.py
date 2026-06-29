"""
Generate Newsletter BPMN process model from Markdown into EAxCRM.qea.

Usage:
    python generate_newsletter_process_from_md.py

Creates elements, connectors, and diagram for the Newsletter Process
Architecture in a dedicated package.
"""
import sys, os, re, json, uuid as _uuid, sqlite3
from xml.etree import ElementTree as ET

DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-NewsletterProcess.md"
GUID_MAP_FILE = os.path.join(os.path.dirname(__file__), "newsletter_guid_map.json")

BPMN_TYPE_LABEL = {
    "Activity": "Activity",
    "Event": "Event",
    "Decision": "Gateway",
    "Gateway": "Gateway",
    "Object": "DataObject",
    "Artifact": "DataObject",
    "ActivityPartition": "Lane",
}

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
    "CallActivity": {
        "calledElement": "Called Element",
        "isACalledActivity": "Is Called Activity",
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
    "IntermediateEvent": {
        "eventType": "Event Type",
        "triggerType": "Trigger",
    },
    "IntermediateCatchEvent": {
        "eventType": "Event Type",
        "triggerType": "Trigger",
    },
    "IntermediateThrowEvent": {
        "eventType": "Event Type",
        "triggerType": "Result",
    },
    "BoundaryEvent": {
        "eventType": "Event Type",
        "triggerType": "Trigger",
        "cancelActivity": "Cancel Activity",
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
    "InclusiveGateway": {
        "gatewayType": "Gateway Type",
    },
    "ComplexGateway": {
        "gatewayType": "Gateway Type",
    },
    "EventBasedGateway": {
        "gatewayType": "Gateway Type",
        "instantiate": "Instantiate",
        "eventGatewayType": "Event Gateway Type",
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
    "DataStore": {
        "capacity": "Capacity",
        "dataStoreRef": "Data Store Ref",
        "isUnlimited": "Is Unlimited",
    },
    "TextAnnotation": {
        "textFormat": "Text Format",
    },
}

# Object_Type mapping per BPMN type
OBJECT_TYPE_MAP = {
    "Activity": "Activity",
    "StartEvent": "Event",
    "EndEvent": "Event",
    "IntermediateEvent": "Event",
    "ExclusiveGateway": "Decision",
    "Gateway": "Decision",
    "ParallelGateway": "Gateway",
    "InclusiveGateway": "Gateway",
    "ComplexGateway": "Gateway",
    "EventBasedGateway": "Gateway",
    "Lane": "ActivityPartition",
    "Pool": "ActivityPartition",
    "CollaborationModel": "Activity",
    "DataObject": "Artifact",
    "DataStore": "Artifact",
    "TextAnnotation": "Artifact",
}

# Map MD header labels → EA Stereotype values
LABEL_TO_STEREO = {
    "BPMN Collaboration": "CollaborationModel",
}


def safe_id(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def parse_md(filepath):
    """Parse the newsletter process MD file into structured data."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    elements = {}  # safe_id → element dict
    current = None
    parent_stack = []  # (prefix, safe_id) for nesting tracking
    sequence_flows = []

    for line in lines:
        # Detect element headers like "### Lane—eaxpertise" or "#### Activity—checkcadence"
        m = re.match(r"^(#+)\s+(.+?)—(.+)$", line)
        if m:
            prefix, label, eid = m.group(1), m.group(2), m.group(3)
            depth = len(prefix) - 2  # ## = 0, ### = 1, #### = 2, etc.

            new_elem = {"label": label, "id": eid, "depth": depth,
                        "fields": {}, "children": []}
            elements[eid] = new_elem
            current = eid

            # Update parent stack
            while parent_stack and parent_stack[-1][0] >= depth:
                parent_stack.pop()
            if parent_stack:
                parent_stack[-1][2]["children"].append(eid)
            parent_stack.append((depth, eid, new_elem))
            continue

        if current is None:
            continue

        # Parse key-value fields
        kv = re.match(r"^\s*-\s*(.+?):\s*(.*)$", line)
        if kv:
            key = kv.group(1).strip()
            val = kv.group(2).strip()
            elements[current]["fields"][key] = val

    # Parse sequence flows
    in_flows = False
    for line in lines:
        if line.strip() == "### Sequence Flows":
            in_flows = True
            continue
        if in_flows and line.startswith("## "):
            break
        if in_flows:
            fm = re.match(r"^\s*-\s*(.+?)\s*→\s*(.+?)(?:\s+\[(.+)\])?\s*$", line)
            if fm:
                src = safe_id(fm.group(1))
                tgt = safe_id(fm.group(2))
                cond = fm.group(3) or ""
                sequence_flows.append({"source": src, "target": tgt, "condition": cond})

    return elements, sequence_flows


def main():
    conn = sqlite3.connect(DEFAULT_QEA)
    c = conn.cursor()

    # Find "Newsletter Process Architecture" package or create it
    c.execute("SELECT Package_ID FROM t_package WHERE Name='Newsletter Process Architecture'")
    row = c.fetchone()
    if row:
        pkg_id = row[0]
        print(f"Found package 'Newsletter Process Architecture' (ID {pkg_id})")
    else:
        # Create package under root
        c.execute("SELECT MAX(Package_ID) FROM t_package")
        max_pkg = c.fetchone()[0] or 0
        pkg_id = max_pkg + 1
        c.execute("INSERT INTO t_package (Package_ID, Name, Parent_ID) VALUES (?, ?, 0)",
                  (pkg_id, "Newsletter Process Architecture"))
        conn.commit()
        print(f"Created package 'Newsletter Process Architecture' (ID {pkg_id})")

    # Parse MD
    elements, sequence_flows = parse_md(DEFAULT_MD)
    print(f"Parsed {len(elements)} elements, {len(sequence_flows)} sequence flows")

    # Load GUID map
    guid_map = {}
    if os.path.exists(GUID_MAP_FILE):
        with open(GUID_MAP_FILE, "r") as f:
            guid_map = json.load(f)
    collab_guid = guid_map.get("_collaboration_model", "")
    diag_guid = guid_map.get("_diagram", "")
    elem_guid_map = guid_map.get("elements", {})

    # Get next available Object_ID
    c.execute("SELECT MAX(Object_ID) FROM t_object")
    next_oid = (c.fetchone()[0] or 0) + 1

    created = 0
    updated = 0

    # Find the CollaborationModel element
    collab_eid = None
    for eid, elem in elements.items():
        if elem["fields"].get("Name", "").startswith("EAxCRM Newsletter"):
            collab_eid = eid
            break

    # Create/update elements using DFS traversal so parent-child hierarchy is correct
    object_ids = {}

    def create_element(eid, parent_oid):
        nonlocal created, updated, next_oid
        elem = elements[eid]
        name = elem["fields"].get("Name", eid)
        raw_label = elem["label"]
        stereo = LABEL_TO_STEREO.get(raw_label, raw_label)
        obj_type = OBJECT_TYPE_MAP.get(stereo, "Class")
        notes = elem["fields"].get("Description", "")

        guid = elem_guid_map.get(eid, "")
        if guid:
            c.execute("SELECT Object_ID FROM t_object WHERE ea_guid=?", (guid,))
            row = c.fetchone()
        else:
            row = None

        if row:
            oid = row[0]
            c.execute("UPDATE t_object SET Name=?, Object_Type=?, Stereotype=?, Note=? WHERE Object_ID=?",
                      (name, obj_type, stereo, notes, oid))
            c.execute("DELETE FROM t_objectproperties WHERE Object_ID=?", (oid,))
            updated += 1
        else:
            guid = "{" + __import__("uuid").uuid4().hex.upper() + "}"
            oid = next_oid
            next_oid += 1
            c.execute("""INSERT INTO t_object 
                (Object_ID, Name, Object_Type, Stereotype, Note, Package_ID, ParentID, ea_guid, 
                 CreatedDate, ModifiedDate, Author, Status, Visibility)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'generator', 'Proposed', 'Public')
            """, (oid, name, obj_type, stereo, notes, pkg_id, parent_oid, guid))
            elem_guid_map[eid] = guid
            created += 1

        object_ids[eid] = oid

        # Set tagged values
        tags_meta = BPMN_TAGGED_VALUES.get(stereo, {})
        if not tags_meta:
            tags_meta = BPMN_TAGGED_VALUES.get(obj_type, {})
        label_to_key = {v: k for k, v in tags_meta.items()}
        for field_key, field_val in elem["fields"].items():
            prop_key = label_to_key.get(field_key)
            if prop_key and field_val:
                c.execute("INSERT INTO t_objectproperties (Object_ID, Property, Value) VALUES (?, ?, ?)",
                          (oid, prop_key, field_val))

        # Recurse into children
        for child_eid in elem.get("children", []):
            create_element(child_eid, oid)

    # Find root elements (depth 0, no parent) and process them in parse order
    root_eids = [eid for eid in elements if elements[eid]["depth"] == 0]
    for eid in root_eids:
        create_element(eid, 0)

    # Create diagram
    if collab_eid and collab_eid in object_ids:
        collab_oid = object_ids[collab_eid]
        if diag_guid:
            c.execute("SELECT Diagram_ID FROM t_diagram WHERE ea_guid=?", (diag_guid,))
            diag_row = c.fetchone()
        else:
            diag_row = None

        if diag_row:
            c.execute("UPDATE t_diagram SET Name=?, ParentID=? WHERE Diagram_ID=?",
                      ("Newsletter Process Architecture", collab_oid, diag_row[0]))
        else:
            c.execute("SELECT MAX(Diagram_ID) FROM t_diagram")
            max_diag = c.fetchone()[0] or 0
            diag_id = max_diag + 1
            diag_guid = "{" + __import__("uuid").uuid4().hex.upper() + "}"
            c.execute("""INSERT INTO t_diagram 
                (Diagram_ID, Name, ParentID, Package_ID, Diagram_Type, ea_guid, CreatedDate, ModifiedDate)
                VALUES (?, ?, ?, ?, 'BusinessProcess', ?, datetime('now'), datetime('now'))
            """, (diag_id, "Newsletter Process Architecture", collab_oid, pkg_id, diag_guid))

    # Create connectors (sequence flows)
    conn_count = 0
    c.execute("SELECT MAX(Connector_ID) FROM t_connector")
    next_cid = (c.fetchone()[0] or 0) + 1

    for flow in sequence_flows:
        src_oid = object_ids.get(flow["source"])
        tgt_oid = object_ids.get(flow["target"])
        if src_oid and tgt_oid:
            # Check if this connector already exists
            c.execute("""SELECT Connector_ID FROM t_connector 
                WHERE Start_Object_ID=? AND End_Object_ID=? AND Stereotype='SequenceFlow'""",
                      (src_oid, tgt_oid))
            if not c.fetchone():
                conn_guid = "{" + _uuid.uuid4().hex.upper() + "}"
                c.execute("""INSERT INTO t_connector 
                    (Connector_ID, Start_Object_ID, End_Object_ID, Name, Stereotype, 
                     Connector_Type, Direction, Notes, ea_guid)
                    VALUES (?, ?, ?, ?, ?, 'SequenceFlow', 'Unidirectional', ?, ?)
                """, (next_cid, src_oid, tgt_oid, flow["condition"],
                      "SequenceFlow", flow["condition"], conn_guid))
                next_cid += 1
                conn_count += 1

    conn.commit()
    conn.close()

    # Save GUID map
    guid_map["_collaboration_model"] = collab_guid or ""
    guid_map["_diagram"] = diag_guid or ""
    guid_map["elements"] = elem_guid_map
    with open(GUID_MAP_FILE, "w") as f:
        json.dump(guid_map, f, indent=2)

    print(f"Created {created} new element(s), updated {updated}")
    print(f"Created {conn_count} new connector(s)")
    print("Done.")


if __name__ == "__main__":
    main()
