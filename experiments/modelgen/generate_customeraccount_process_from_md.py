"""Generate the BPMN "Manage Customer Account" process in EAxCRM.qea from Markdown using COM API.

Usage:
    python generate_customeraccount_process_from_md.py

Supports SequenceFlow, MessageFlow, DataInputAssociation, DataOutputAssociation
(the current MD only uses SequenceFlow + Data*Association -- single lane, no
cross-participant MessageFlows).
Idempotent: uses GUID map for re-runs. Preserves manual diagram layout.
"""
import sys, os, argparse, re, json, subprocess, win32com.client, pythoncom
import diagram_utils
import ea_session

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-CustomerAccountProcess.md"
GUID_MAP_FILE = os.path.join(SCRIPT_DIR, "customeraccount_guid_map.json")

LABEL_TO_STEREO = {
    "BPMN Collaboration": "CollaborationModel",
    "Lane": "Lane",
    "Activity": "Activity",
    "StartEvent": "StartEvent",
    "EndEvent": "EndEvent",
    "IntermediateEvent": "IntermediateEvent",
    "Gateway": "Gateway",
    "ExclusiveGateway": "ExclusiveGateway",
    "ParallelGateway": "ParallelGateway",
    "InclusiveGateway": "InclusiveGateway",
    "ComplexGateway": "ComplexGateway",
    "EventBasedGateway": "EventBasedGateway",
    "DataObject": "DataObject",
    "DataStore": "DataStore",
    "TextAnnotation": "TextAnnotation",
}

OBJECT_TYPE_MAP = {
    "Activity": "Activity",
    "StartEvent": "Event",
    "EndEvent": "Event",
    "IntermediateEvent": "Event",
    "Gateway": "Decision",
    "ExclusiveGateway": "Decision",
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
        "eventDefinition": "Event Type",
        "triggerType": "Trigger",
    },
    "EndEvent": {
        "eventDefinition": "Event Type",
        "triggerType": "Result",
    },
    "IntermediateEvent": {
        "eventDefinition": "Event Type",
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
        "dataInOut": "Data In/Out",
    },
}

CONNECTOR_TYPES = {
    "SequenceFlow": "ControlFlow",
    "MessageFlow": "ControlFlow",
    "DataOutputAssociation": "Dependency",
    "DataInputAssociation": "Dependency",
}

CONNECTOR_STEREOTYPE_EX = {
    "SequenceFlow": "BPMN2.0::SequenceFlow",
    "MessageFlow": "BPMN2.0::MessageFlow",
    "DataOutputAssociation": "BPMN2.0::DataOutputAssociation",
    "DataInputAssociation": "BPMN2.0::DataInputAssociation",
}

CONNECTOR_STEREOTYPES_SHORT = {
    "SequenceFlow": "SequenceFlow",
    "MessageFlow": "MessageFlow",
    "DataOutputAssociation": "DataOutputAssociation",
    "DataInputAssociation": "DataInputAssociation",
}


def safe_id(name):
    return re.sub(r"[^a-zA-Z0-9]", "", name)


def parse_md(path):
    elements = {}
    connectors = {"SequenceFlow": [], "MessageFlow": [], "DataOutputAssociation": [], "DataInputAssociation": []}
    current = None
    section = None
    fields = {}
    label = ""
    parent_eid = None

    section_map = {
        "Sequence Flows": "SequenceFlow",
        "Message Flows": "MessageFlow",
        "Data Output Associations": "DataOutputAssociation",
        "Data Input Associations": "DataInputAssociation",
    }

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip()
        stripped = line.strip()

        if stripped.startswith("## "):
            section = "header"
            parts_after = stripped[3:].strip()
            sep = None
            for s in ("—", "–"):
                if s in parts_after:
                    sep = s
                    break
            if sep:
                if current and label:
                    elements[safe_id(current)] = {"label": label, "fields": dict(fields)}
                label, eid_part = parts_after.split(sep, 1)
                label = label.strip()
                eid_part = eid_part.strip()
                current = eid_part
                fields = {}
                parent_eid = safe_id(current)
            continue

        if stripped.startswith("### "):
            if current and label:
                elements[safe_id(current)] = {
                    "label": label,
                    "fields": dict(fields),
                }
            parts_after = stripped[4:].strip()
            if parts_after in section_map:
                section = section_map[parts_after]
                current = None
                continue
            sep_char = None
            for s in ("—", "–"):
                if s in parts_after:
                    sep_char = s
                    break
            if sep_char:
                label, eid_part = parts_after.split(sep_char, 1)
                label = label.strip()
                eid_part = eid_part.strip()
            else:
                label = parts_after
                eid_part = parts_after
            current = eid_part
            fields = {}
            parent_eid = safe_id(current)
            section = None
            continue

        if current and stripped.startswith("- "):
            key_val = stripped[2:].strip()
            colon_pos = key_val.find(": ")
            if colon_pos > 0:
                key = key_val[:colon_pos].strip()
                val = key_val[colon_pos + 2:].strip()
                fields[key] = val

        if section and section in connectors and stripped.startswith("- "):
            line_flow = stripped[2:].strip()
            m = re.match(r"(.+?)\s*[->→➡]\s*(.+?)(\s*\[(.+?)\])?$", line_flow)
            if m:
                src = safe_id(m.group(1).strip())
                tgt = safe_id(m.group(2).strip())
                cond = (m.group(4) or "").strip()
                connectors[section].append({"source": src, "target": tgt, "condition": cond})

    if current and label:
        elements[safe_id(current)] = {
            "label": label,
            "fields": dict(fields),
        }

    return elements, connectors


def set_tagged_values(elem, stereo, fields):
    tag_defs = BPMN_TAGGED_VALUES.get(stereo, {})
    if not tag_defs:
        return
    label_to_prop = {v: k for k, v in tag_defs.items()}
    for field_key, field_val in fields.items():
        prop_key = label_to_prop.get(field_key)
        if prop_key and field_val:
            tv = elem.TaggedValues.AddNew(prop_key, field_val)
            tv.Update()


def main():
    pythoncom.CoInitialize()
    parser = argparse.ArgumentParser(description="Generate Manage Customer Account process in EA")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    elements, connectors = parse_md(args.md)
    total_conns = sum(len(v) for v in connectors.values())
    print(f"Parsed {len(elements)} elements, {total_conns} connectors ({', '.join(f'{k}: {len(v)}' for k, v in connectors.items() if v)})")

    LANE_IDS = {eid for eid, edata in elements.items() if edata.get("label") == "Lane"}
    if not LANE_IDS:
        LANE_IDS = {"EAxpertise"}
    print(f"  Lane IDs: {LANE_IDS}")

    # elem_types for type-appropriate BPMN sizing (Gateway diamonds, DataObject,
    # StartEvent/EndEvent circles) via diagram_utils.BPMN_ELEMENT_SIZES.
    elem_types = {eid: data["label"] for eid, data in elements.items()
                  if data.get("label") and data["label"] != "Lane"}

    guid_map = {}
    if os.path.exists(GUID_MAP_FILE):
        with open(GUID_MAP_FILE, "r") as f:
            guid_map = json.load(f)

    elem_guid_map = guid_map.get("elements", {})

    before_pids = ea_session.get_ea_pids()

    app = win32com.client.DispatchEx("EA.App")
    repo = app.Repository
    repo.OpenFile(args.qea)
    print(f"Connected: {repo.ConnectionString}")

    try:
        try:
            repo.ActivateTechnology("BPMN2.0")
            print("  Activated BPMN2.0 MDG technology")
        except Exception as e:
            print(f"  Note: ActivateTechnology failed: {e}")

        root = ea_session.get_model_root(repo)
        proc_arch = None
        for i in range(root.Packages.Count):
            p = root.Packages.GetAt(i)
            if p.Name == "Process Architecture":
                proc_arch = p
                break
        if not proc_arch:
            proc_arch = root.Packages.AddNew("Process Architecture", "Package")
            proc_arch.Update()
            root.Update()

        proc_arch.Elements.Refresh()

        # CollaborationModel
        collab_name = "Manage Customer Account"
        collab_elem = None
        collab_guid = guid_map.get("_collaboration_model", "")
        if collab_guid:
            try:
                collab_elem = repo.GetElementByGuid(collab_guid)
            except:
                collab_elem = None

        if not collab_elem:
            for i in range(proc_arch.Elements.Count):
                e = proc_arch.Elements.GetAt(i)
                if e.Name == collab_name:
                    collab_elem = e
                    break

        proc_arch.Elements.Refresh()
        pkg_elems_by_name = {}
        for i in range(proc_arch.Elements.Count):
            e = proc_arch.Elements.GetAt(i)
            pkg_elems_by_name[e.Name] = e

        created_count = 0
        updated_count = 0
        object_ids = {}

        def create_element(eid, parent_elem):
            nonlocal created_count, updated_count
            elem_data = elements[eid]
            name = elem_data["fields"].get("Name", eid)
            raw_label = elem_data["label"]
            stereo = LABEL_TO_STEREO.get(raw_label, raw_label)
            obj_type = OBJECT_TYPE_MAP.get(stereo, "Class")
            notes = elem_data["fields"].get("Description", "")

            guid = elem_guid_map.get(eid, "")
            existing = None
            if guid:
                try:
                    existing = repo.GetElementByGuid(guid)
                except:
                    pass
            if not existing:
                md_guid = elem_data["fields"].get("GUID", "")
                if md_guid:
                    try:
                        existing = repo.GetElementByGuid(md_guid)
                    except:
                        pass
            if not existing:
                existing = pkg_elems_by_name.get(name)

            if existing:
                existing.Name = name
                existing.StereotypeEx = f"BPMN2.0::{stereo}"
                existing.Notes = notes
                if parent_elem:
                    existing.ParentID = parent_elem.ElementID
                existing.Update()
                elem_guid_map[eid] = existing.ElementGUID
                object_ids[eid] = existing.ElementID
                updated_count += 1
                pkg_elems_by_name[existing.Name] = existing
                return existing
            else:
                new_elem = proc_arch.Elements.AddNew(name, obj_type)
                new_elem.StereotypeEx = f"BPMN2.0::{stereo}"
                new_elem.Notes = notes
                if parent_elem:
                    new_elem.ParentID = parent_elem.ElementID
                new_elem.Update()
                elem_guid_map[eid] = new_elem.ElementGUID
                object_ids[eid] = new_elem.ElementID
                pkg_elems_by_name[new_elem.Name] = new_elem
                created_count += 1
                return new_elem

        collab_eid = None
        for eid, elem_data in elements.items():
            if elem_data["label"] == "BPMN Collaboration":
                collab_eid = eid
                break

        if collab_eid:
            collab_elem = create_element(collab_eid, None)

        if collab_elem:
            for eid, elem_data in elements.items():
                if eid not in object_ids and elem_data.get("label") == "Lane":
                    create_element(eid, collab_elem)
            for eid, elem_data in elements.items():
                if eid in object_ids:
                    continue
                lane = diagram_utils.get_lane_from_fields(elem_data.get("fields", {}))
                if lane and lane in object_ids:
                    parent = repo.GetElementByID(object_ids[lane])
                else:
                    parent = collab_elem
                create_element(eid, parent)
            for eid in elements:
                if eid not in object_ids:
                    create_element(eid, collab_elem)

        for eid, elem_data in elements.items():
            if elem_data.get("label") == "Lane" or eid == collab_eid:
                continue
            lane = diagram_utils.get_lane_from_fields(elem_data.get("fields", {}))
            if lane and lane in object_ids:
                oid = object_ids.get(eid)
                if oid:
                    try:
                        ea_elem = repo.GetElementByID(oid)
                        lane_oid = object_ids[lane]
                        if ea_elem and ea_elem.ParentID != lane_oid:
                            ea_elem.ParentID = lane_oid
                            ea_elem.Update()
                    except:
                        pass

        for eid, elem_oid in object_ids.items():
            elem_data = elements[eid]
            raw_label = elem_data["label"]
            stereo = LABEL_TO_STEREO.get(raw_label, raw_label)
            try:
                ea_elem = repo.GetElementByID(elem_oid)
            except:
                try:
                    guid = elem_guid_map.get(eid, "")
                    if guid:
                        ea_elem = repo.GetElementByGuid(guid)
                    else:
                        continue
                except:
                    continue
            if ea_elem:
                set_tagged_values(ea_elem, stereo, elem_data["fields"])

        print(f"Created {created_count} new element(s), updated {updated_count}")

        conn_counts = {}
        for conn_type, conn_list in connectors.items():
            if not conn_list:
                continue
            count = 0
            for flow in conn_list:
                src_oid = object_ids.get(flow["source"])
                tgt_oid = object_ids.get(flow["target"])
                if not src_oid or not tgt_oid:
                    continue

                try:
                    src_elem = repo.GetElementByID(src_oid)
                    tgt_elem = repo.GetElementByID(tgt_oid)
                except:
                    continue
                if not src_elem or not tgt_elem:
                    continue

                uml_type = CONNECTOR_TYPES[conn_type]
                stereo_ex = CONNECTOR_STEREOTYPE_EX[conn_type]

                short_stereo = CONNECTOR_STEREOTYPES_SHORT.get(conn_type, conn_type)
                exists = False
                src_elem.Connectors.Refresh()
                for i in range(src_elem.Connectors.Count):
                    conn = src_elem.Connectors.GetAt(i)
                    if conn.SupplierID != tgt_elem.ElementID:
                        continue
                    cstereo = conn.StereotypeEx or conn.Stereotype or ""
                    if cstereo in (stereo_ex, short_stereo):
                        exists = True
                        if cstereo == short_stereo:
                            conn.StereotypeEx = stereo_ex
                        if flow["condition"]:
                            conn.Name = flow["condition"]
                        conn.Update()
                        break

                if not exists:
                    new_conn = src_elem.Connectors.AddNew("", uml_type)
                    new_conn.SupplierID = tgt_elem.ElementID
                    new_conn.Direction = "Unidirectional"
                    new_conn.StereotypeEx = stereo_ex
                    if flow["condition"]:
                        new_conn.Name = flow["condition"]
                    new_conn.Update()
                    count += 1

            conn_counts[conn_type] = count

        for ctype, cnt in conn_counts.items():
            if cnt:
                print(f"  Created {cnt} new {ctype}(s)")

        # Diagram
        diag = None
        diag_guid_key = "_diagram_customeraccount"
        existing_diag_guid = guid_map.get(diag_guid_key)
        if existing_diag_guid:
            try:
                diag = repo.GetDiagramByGuid(existing_diag_guid)
            except:
                diag = None

        if not diag:
            if collab_eid:
                md_diag_guid = elements[collab_eid]["fields"].get("Diagram GUID", "")
                if md_diag_guid:
                    try:
                        diag = repo.GetDiagramByGuid(md_diag_guid)
                    except:
                        pass

        if not diag and collab_elem:
            collab_elem.Diagrams.Refresh()
            for i in range(collab_elem.Diagrams.Count):
                d = collab_elem.Diagrams.GetAt(i)
                if d.Name == "Manage Customer Account":
                    diag = d
                    break

        if not diag and collab_elem:
            diag = collab_elem.Diagrams.AddNew("Manage Customer Account", "BusinessProcess")
            diag.Update()
            collab_elem.Update()
            guid_map[diag_guid_key] = diag.DiagramGUID
            print("  Created new diagram under CollaborationModel")

        if diag:
            diag.Stereotype = "Collaboration"
            diag.StereotypeEx = "BPMN2.0::Collaboration"
            diag.Update()
            # SQLite fallback for the diagram-property stereotype xref only --
            # matches the documented exception in the ea-diagram-creator skill
            # ("BPMN Diagram Stereotype needs 3 things"), not a general SQLite
            # write. All element/connector writes above are COM API only.
            import sqlite3 as _sqlite3
            import uuid as _uuid
            _qea_path = args.qea
            _dg_guid = diag.DiagramGUID
            if _dg_guid:
                _db = _sqlite3.connect(_qea_path)
                _c = _db.cursor()
                _c.execute("SELECT COUNT(*) FROM t_xref WHERE Client=? AND Type='Stereotypes' AND Visibility='diagram property'",
                          (_dg_guid,))
                if _c.fetchone()[0] == 0:
                    _xref_id = f"{{{str(_uuid.uuid4())}}}"
                    _c.execute(
                        "INSERT INTO t_xref (XrefID, Client, Type, Visibility, Namespace, Description) "
                        "VALUES (?, ?, 'Stereotypes', 'diagram property', 'BPMN2_0', ?)",
                        (_xref_id, _dg_guid,
                         "@STEREO;Name=Collaboration;FQName=BPMN2.0::Collaboration;@ENDSTEREO;")
                    )
                    _db.commit()
                    print(f"  Added BPMN stereotype xref for diagram")
                _db.close()

        if diag:
            diag.DiagramObjects.Refresh()
            existing_count = diag.DiagramObjects.Count
            if existing_count > 0:
                print(f"  Diagram has {existing_count} objects, preserving positions")
                placed = diagram_utils.get_placed_ids(diag)
                new_ids = [eid for eid, oid in object_ids.items()
                           if eid not in LANE_IDS and oid not in placed]
                if new_ids:
                    new_by_lane = {}
                    for eid in new_ids:
                        lane = diagram_utils.get_lane_from_fields(elements[eid].get("fields", {}))
                        if lane and lane in LANE_IDS:
                            new_by_lane.setdefault(lane, []).append(eid)
                    if new_by_lane:
                        lane_config = [{"id": lid} for lid in sorted(LANE_IDS)]
                        lane_bounds = diagram_utils.compute_bpmn_lane_positions(lane_config)
                        all_by_lane = {}
                        for eid, edata in elements.items():
                            if edata.get("label") == "Lane":
                                continue
                            lane = diagram_utils.get_lane_from_fields(edata.get("fields", {}))
                            if lane and lane in LANE_IDS:
                                all_by_lane.setdefault(lane, []).append(eid)
                        for lane_id, eids in new_by_lane.items():
                            combined = all_by_lane.get(lane_id, [])
                            all_epos = diagram_utils.compute_bpmn_element_positions(
                                {lane_id: combined}, lane_bounds, elem_types=elem_types)
                            new_positions = {eid: all_epos[eid] for eid in eids if eid in all_epos}
                            added = diagram_utils.add_missing_elements(diag, list(new_positions.keys()),
                                                                       object_ids, new_positions)
                            if added:
                                print(f"  Added {added} new element(s) to existing diagram")
            else:
                print("  Placing elements on diagram (first time)")
                lane_config = [{"id": lid} for lid in sorted(LANE_IDS)]
                lane_bounds = diagram_utils.compute_bpmn_lane_positions(lane_config)
                elements_by_lane = {}
                unassigned = []
                for eid, edata in elements.items():
                    if edata.get("label") == "Lane":
                        continue
                    lane = diagram_utils.get_lane_from_fields(edata.get("fields", {}))
                    if lane and lane in lane_bounds:
                        elements_by_lane.setdefault(lane, []).append(eid)
                    else:
                        unassigned.append(eid)
                if unassigned:
                    print(f"  Warning: {len(unassigned)} element(s) have no Lane field")
                positions = dict(lane_bounds)
                elem_pos = diagram_utils.compute_bpmn_element_positions(elements_by_lane, lane_bounds, elem_types=elem_types)
                positions.update(elem_pos)
                all_ids = list(lane_bounds.keys()) + [
                    eid for eid in elements
                    if diagram_utils.get_lane_from_fields(elements[eid].get("fields", {})) in lane_bounds]
                count = diagram_utils.create_diagram_objects(diag, all_ids, object_ids, positions)
                if count:
                    diag.Update()
                    print(f"  Placed {count} elements on diagram")

        # Set Orthogonal Rounded line style for all connector links on this diagram
        try:
            diag.DiagramLinks.Refresh()
            link_count = diag.DiagramLinks.Count
            for i in range(link_count):
                dl = diag.DiagramLinks.GetAt(i)
                dl.LineStyle = 9  # Orthogonal Rounded
                dl.Update()
            if link_count:
                print(f"  Set Orthogonal Rounded linestyle on {link_count} connector(s)")
        except Exception as e:
            print(f"  [linestyle] Failed: {e}")

        if collab_elem:
            guid_map["_collaboration_model"] = collab_elem.ElementGUID
        if diag:
            guid_map[diag_guid_key] = diag.DiagramGUID
        guid_map["elements"] = elem_guid_map
        with open(GUID_MAP_FILE, "w") as f:
            json.dump(guid_map, f, indent=2)

    finally:
        try:
            repo.RefreshModelView(0)
            repo.RefreshOpenDiagrams(True)
        except Exception as e:
            print(f"  [refresh] RefreshModelView(0) failed: {e}")
        try:
            repo.CloseFile()
        except:
            pass
        pythoncom.CoUninitialize()

    killed = ea_session.kill_new_ea_processes(before_pids)
    if killed:
        print(f"  Cleaned up {len(killed)} zombie EA process(es)")

    print("Done.")


if __name__ == "__main__":
    main()
