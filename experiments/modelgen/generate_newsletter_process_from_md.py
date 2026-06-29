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

# BPMN element dimensions for diagram placement (width, height)
ELEM_SIZE = {
    "Activity": (100, 55),
    "StartEvent": (50, 50),
    "EndEvent": (50, 50),
    "Gateway": (60, 60),
    "ExclusiveGateway": (60, 60),
    "ParallelGateway": (60, 60),
    "InclusiveGateway": (60, 60),
    "DataObject": (70, 50),
    "Lane": (0, 0),  # computed dynamically
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

    # Find parent "Process Architecture" package
    c.execute("SELECT Package_ID FROM t_package WHERE Name='Process Architecture' AND Parent_ID=1")
    parent_row = c.fetchone()
    if not parent_row:
        print("FAIL: 'Process Architecture' package not found under Model")
        sys.exit(1)
    parent_pkg_id = parent_row[0]

    # Find or create "Newsletter Process Architecture" as a sub-package
    c.execute("SELECT Package_ID FROM t_package WHERE Name='Newsletter Process Architecture' AND Parent_ID=?",
              (parent_pkg_id,))
    row = c.fetchone()
    if row:
        pkg_id = row[0]
        print(f"Found sub-package 'Newsletter Process Architecture' (ID {pkg_id}) under Process Architecture")
    else:
        c.execute("SELECT MAX(Package_ID) FROM t_package")
        max_pkg = c.fetchone()[0] or 0
        pkg_id = max_pkg + 1
        c.execute("INSERT INTO t_package (Package_ID, Name, Parent_ID) VALUES (?, ?, ?)",
                  (pkg_id, "Newsletter Process Architecture", parent_pkg_id))
        conn.commit()
        print(f"Created sub-package 'Newsletter Process Architecture' (ID {pkg_id}) under Process Architecture")

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
    dia_id = None
    if collab_eid and collab_eid in object_ids:
        collab_oid = object_ids[collab_eid]
        if diag_guid:
            c.execute("SELECT Diagram_ID FROM t_diagram WHERE ea_guid=?", (diag_guid,))
            diag_row = c.fetchone()
        else:
            diag_row = None

        pdata = ("HideRel=0;ShowTags=0;ShowReqs=0;ShowCons=0;OpParams=1;ShowSN=0;ScalePI=0;"
                 "PPgs.cx=0;PPgs.cy=0;PSize=9;ShowIcons=1;SuppCN=0;HideProps=0;HideParents=0;"
                 "UseAlias=0;HideAtts=0;HideOps=0;HideStereo=0;HideEStereo=0;ShowRec=1;"
                 "ShowRes=0;ShowShape=1;FormName=;")
        styleex = ("ExcludeRTF=0;DocAll=0;HideQuals=0;AttPkg=1;ShowTests=0;ShowMaint=0;"
                   "SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;KanbanActive=0;"
                   "MatrixLineWidth=1;MatrixLineClr=0;MatrixLocked=0;"
                   "TConnectorNotation=UML 2.1;TExplicitNavigability=0;"
                   "AdvancedElementProps=1;AdvancedFeatureProps=1;AdvancedConnectorProps=1;"
                   "m_bElementClassifier=1;SPT=1;MDGDgm=BPMN2.0::Collaboration;STBLDgm=;"
                   "ShowNotes=0;VisibleAttributeDetail=0;ShowOpRetType=1;"
                   "SuppressBrackets=0;SuppConnectorLabels=0;PrintPageHeadFoot=0;"
                   "ShowAsList=0;SuppressedCompartments=;Theme=:119;")
        swimlanes = "locked=false;orientation=0;width=0;inbar=false;names=false;color=-1;bold=false;fcol=0;tcol=-1;ofCol=-1;ufCol=-1;hl=1;ufh=0;hh=0;cls=0;bw=0;hli=0;bro=0;"

        if diag_row:
            dia_id = diag_row[0]
            c.execute("""UPDATE t_diagram SET Name=?, ParentID=?, Author=?, PDATA=?, StyleEx=?,
                Swimlanes=?, cx=?, cy=? WHERE Diagram_ID=?""",
                      ("Newsletter Process Architecture", collab_oid,
                       "generator", pdata, styleex, swimlanes, 1100, 240, dia_id))
        else:
            c.execute("SELECT MAX(Diagram_ID) FROM t_diagram")
            max_diag = c.fetchone()[0] or 0
            dia_id = max_diag + 1
            diag_guid = "{" + __import__("uuid").uuid4().hex.upper() + "}"
            c.execute("""INSERT INTO t_diagram 
                (Diagram_ID, Name, ParentID, Package_ID, Diagram_Type, ea_guid,
                 Author, PDATA, StyleEx, Swimlanes, cx, cy, CreatedDate, ModifiedDate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (dia_id, "Newsletter Process Architecture", collab_oid, pkg_id,
                  "BusinessProcess", diag_guid, "generator", pdata, styleex,
                  swimlanes, 1100, 240))

    # Add BPMN2.0:: stereotype t_xref for all elements
    for eid, oid in object_ids.items():
        raw_label = elements[eid]["label"]
        stereo = LABEL_TO_STEREO.get(raw_label, raw_label)
        ea_guid_val = elem_guid_map.get(eid)
        if ea_guid_val and stereo:
            c.execute("DELETE FROM t_xref WHERE Client=? AND Name='Stereotypes' AND Type='element property'",
                      (ea_guid_val,))
            xref_id = "{" + _uuid.uuid4().hex.upper() + "}"
            c.execute("""INSERT INTO t_xref 
                (XrefID, Name, Type, Visibility, Partition, Description, Client)
                VALUES (?, 'Stereotypes', 'element property', 'Public', '', ?, ?)
            """, (xref_id, f"@STEREO;Name={stereo};FQName=BPMN2.0::{stereo};@ENDSTEREO;", ea_guid_val))

    # Place elements on the diagram with a grid layout (two lanes)
    if dia_id:
        c.execute("DELETE FROM t_diagramobjects WHERE Diagram_ID=?", (dia_id,))
        c.execute("SELECT MAX(Instance_ID) FROM t_diagramobjects")
        next_iid = (c.fetchone()[0] or 0) + 1

        def elem_dim(stereo):
            w, h = ELEM_SIZE.get(stereo, (100, 55))
            return w, h

        # Define per-eid positions (left, top, right, bottom)
        lane_y_top = 0
        lane_y_bot = 120

        pos = {
            # EAxpertise Lane
            "eaxpertise": (0, 0, 2200, 130),
            # Main flow row
            "startnewsletter":  (30, 30, 80, 80),
            "checkcadence":     (140, 30, 240, 85),
            "6weekselapsed":    (300, 20, 360, 80),
            "browseavailablearticles": (430, 30, 530, 85),
            "selectarticles":   (600, 30, 700, 85),
            "selectedarticles": (770, 30, 840, 80),
            "composenewsletter": (910, 30, 1010, 85),
            "newsletterdraft":  (1080, 30, 1150, 80),
            "submitforreview":  (1220, 30, 1320, 85),
            "reviewapproved":   (1390, 20, 1450, 80),
            "approvednewsletter": (1520, 30, 1590, 80),
            "sendnewsletter":   (1660, 30, 1760, 85),
            "contactlist":      (1830, 30, 1900, 80),
            "sentnewsletter":   (1970, 30, 2040, 80),
            "newslettersent":   (2110, 30, 2160, 80),
            # News Source Lane
            "newssource":       (0, 350, 1200, 480),
            "scheduledscrape":  (30, 380, 80, 430),
            "fetchurllist":     (150, 380, 250, 435),
            "urllist":          (320, 380, 390, 430),
            "scrapearticles":   (460, 380, 560, 435),
            "extractheadingsandsummaries": (630, 380, 730, 435),
            "articlepool":      (800, 380, 870, 430),
            "storenewarticles": (940, 380, 1040, 435),
            "scrapecomplete":   (1110, 380, 1160, 430),
        }

        # Draw order: Lanes first, then flow elements in process order
        draw_order = [
            "eaxpertise", "newssource",
            "startnewsletter", "checkcadence", "6weekselapsed",
            "browseavailablearticles", "selectarticles", "selectedarticles",
            "composenewsletter", "newsletterdraft", "submitforreview",
            "reviewapproved", "approvednewsletter", "sendnewsletter", "contactlist",
            "sentnewsletter", "newslettersent",
            "scheduledscrape", "fetchurllist", "urllist",
            "scrapearticles", "extractheadingsandsummaries", "articlepool",
            "storenewarticles", "scrapecomplete",
        ]

        seq = 0
        for eid in draw_order:
            if eid not in object_ids:
                continue
            oid = object_ids[eid]
            if eid not in pos:
                continue
            l, t, r, b = pos[eid]
            duid = _uuid.uuid4().hex[:8].upper()
            style = f"DUID={duid};HideIcon=0;"
            c.execute("""INSERT INTO t_diagramobjects 
                (Diagram_ID, Object_ID, RectTop, RectLeft, RectRight, RectBottom,
                 Sequence, ObjectStyle, Instance_ID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (dia_id, oid, t, l, r, b, seq, style, next_iid))
            seq += 1
            next_iid += 1

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
