"""Generate BPMN newsletter process model in EAxCRM.qea from Markdown using COM API.

Usage:
    python generate_newsletter_process_from_md.py

Idempotent: uses GUID map for re-runs. Only creates new elements/connectors/diagrams
on first run. Updates existing ones on subsequent runs. Preserves manual diagram layout.
"""
import sys, os, argparse, re, json, subprocess, win32com.client, pythoncom
import diagram_utils

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-NewsletterProcess.md"
GUID_MAP_FILE = os.path.join(SCRIPT_DIR, "newsletter_guid_map.json")

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

def parse_md(path):
    elements = {}
    sequence_flows = []
    current = None
    section = None
    fields = {}
    label = ""
    parent_eid = None  # most recent ### element, used as parent for #### children

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip()
        stripped = line.strip()

        if stripped.startswith("### Sequence Flows"):
            section = "flows"
            continue
        if stripped.startswith("## "):
            section = "header"
            # Capture CollaborationModel (## Type—id)
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

        if section != "flows" and stripped.startswith("#### "):
            if current and label:
                elements[safe_id(current)] = {
                    "label": label,
                    "fields": dict(fields),
                }
            parts = stripped[5:].strip()
            sep_char = None
            for s in ("—", "–"):
                if s in parts:
                    sep_char = s
                    break
            if sep_char:
                label, eid_part = parts.split(sep_char, 1)
                label = label.strip()
                eid_part = eid_part.strip()
            else:
                label = parts
                eid_part = parts
            current = eid_part
            fields = {}
            if parent_eid:
                fields["Parent"] = parent_eid
            continue
        if stripped.startswith("### "):
            if current and label:
                elements[safe_id(current)] = {
                    "label": label,
                    "fields": dict(fields),
                }
            parts_after = stripped[4:].strip()
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
            continue

        if current and stripped.startswith("- "):
            key_val = stripped[2:].strip()
            colon_pos = key_val.find(": ")
            if colon_pos > 0:
                key = key_val[:colon_pos].strip()
                val = key_val[colon_pos + 2:].strip()
                fields[key] = val

        if section == "flows" and stripped.startswith("- "):
            line_flow = stripped[2:].strip()
            m = re.match(r"(.+?)\s*[→➡]\s*(.+?)(\s*\[(.+?)\])?$", line_flow)
            if m:
                src = safe_id(m.group(1).strip())
                tgt = safe_id(m.group(2).strip())
                cond = (m.group(4) or "").strip()
                sequence_flows.append({"source": src, "target": tgt, "condition": cond})

    if current and label:
        elements[safe_id(current)] = {
            "label": label,
            "fields": dict(fields),
        }

    return elements, sequence_flows


def get_or_create_package(parent_pkg, name):
    for i in range(parent_pkg.Packages.Count):
        p = parent_pkg.Packages.GetAt(i)
        if p.Name == name:
            return p
    new_pkg = parent_pkg.Packages.AddNew(name, "Package")
    new_pkg.Update()
    parent_pkg.Update()
    return new_pkg


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


def kill_new_ea_processes(before_pids):
    killed = []
    try:
        import psutil
        current = set(p.info["pid"] for p in psutil.process_iter(["pid", "name"]) if p.info["name"] and "EA" in p.info["name"])
        new_pids = current - before_pids
        for pid in new_pids:
            try:
                p = psutil.Process(pid)
                p.kill()
                killed.append(pid)
            except:
                pass
    except ImportError:
        pass
    return killed


def main():
    pythoncom.CoInitialize()
    parser = argparse.ArgumentParser(description="Generate newsletter process model in EA")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    elements, sequence_flows = parse_md(args.md)
    print(f"Parsed {len(elements)} elements, {len(sequence_flows)} sequence flows")
    elem_types = {eid: data["label"] for eid, data in elements.items()
                  if data.get("label") and data["label"] != "Lane"}

    guid_map = {}
    if os.path.exists(GUID_MAP_FILE):
        with open(GUID_MAP_FILE, "r") as f:
            guid_map = json.load(f)

    elem_guid_map = guid_map.get("elements", {})

    repo = win32com.client.Dispatch("EA.Repository")
    repo.OpenFile(args.qea)
    print(f"Connected: {repo.ConnectionString}")

    before_pids = set()
    try:
        import psutil
        before_pids = set(p.info["pid"] for p in psutil.process_iter(["pid", "name"]) if p.info["name"] and "EA" in p.info["name"])
    except ImportError:
        pass

    try:
        try:
            repo.ActivateTechnology("BPMN2.0")
            print("  Activated BPMN2.0 MDG technology")
        except Exception as e:
            print(f"  Note: ActivateTechnology failed: {e}")

        root = repo.Models.GetAt(0)
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

        # Find the CollaborationModel element (existing or create)
        collab_name = "EAxCRM Newsletter Process Architecture"
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

        # Build a name-index of all existing elements in the package (for idempotent fallback)
        proc_arch.Elements.Refresh()
        pkg_elems_by_name = {}
        for i in range(proc_arch.Elements.Count):
            e = proc_arch.Elements.GetAt(i)
            pkg_elems_by_name[e.Name] = e
            # Seed GUID map from any element that matches an existing MD GUID
            for eid, elem_data in elements.items():
                md_guid = elem_data["fields"].get("GUID", "")
                if md_guid and e.ElementGUID == md_guid and md_guid not in guid_map:
                    if "_collaboration_model" not in guid_map and elem_data["label"] == "BPMN Collaboration":
                        guid_map["_collaboration_model"] = e.ElementGUID

        # Create/update elements using DFS traversal
        created_count = 0
        updated_count = 0
        object_ids = {}
        errors = []

        def create_element(eid, parent_elem):
            nonlocal created_count, updated_count
            elem_data = elements[eid]
            name = elem_data["fields"].get("Name", eid)
            raw_label = elem_data["label"]
            stereo = LABEL_TO_STEREO.get(raw_label, raw_label)
            obj_type = OBJECT_TYPE_MAP.get(stereo, "Class")
            notes = elem_data["fields"].get("Description", "")

            # Look up existing by GUID from map, then by MD GUID, then by name
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
                # Capture GUID/ID BEFORE Refresh() (Reference may break after Refresh)
                elem_guid = new_elem.ElementGUID
                elem_id = new_elem.ElementID
                elem_nm = new_elem.Name
                print(f"  [DEBUG] Created '{name}' -> ID={elem_id}, GUID={elem_guid}")
                proc_arch.Elements.Refresh()
                # Use captured values instead of potentially stale reference
                elem_guid_map[eid] = elem_guid
                object_ids[eid] = elem_id
                pkg_elems_by_name[elem_nm] = new_elem  # Keep ref for later updates
                created_count += 1
                return new_elem

        # Root = CollaborationModel
        collab_eid = None
        for eid, elem_data in elements.items():
            if elem_data["label"] == "BPMN Collaboration":
                collab_eid = eid
                break

        if collab_eid:
            collab_elem = create_element(collab_eid, None)

        # Lane-aware parent assignment: lanes under CM, elements under their lane
        if collab_elem:
            # First pass: create all Lane elements under CM
            print("  [DEBUG] FIRST PASS: creating lanes")
            for eid, elem_data in elements.items():
                if eid not in object_ids and elem_data.get("label") == "Lane":
                    create_element(eid, collab_elem)
            print(f"  [DEBUG] After first pass: {len(object_ids)} elements in object_ids")
            # Second pass: non-Lane elements, assign to correct lane parent
            print("  [DEBUG] SECOND PASS: creating non-lane elements")
            pass2_count = 0
            for eid, elem_data in elements.items():
                if eid in object_ids:
                    continue
                pass2_count += 1
                lane = diagram_utils.get_lane_from_fields(elem_data.get("fields", {}))
                if lane and lane in object_ids:
                    parent = repo.GetElementByID(object_ids[lane])
                else:
                    parent = collab_elem
                create_element(eid, parent)
            print(f"  [DEBUG] After second pass: {len(object_ids)} elements in object_ids")
            # Third pass: any missed elements (no Lane field)
            print("  [DEBUG] THIRD PASS: checking for missed elements")
            pass3_count = 0
            for eid in elements:
                if eid not in object_ids:
                    pass3_count += 1
                    create_element(eid, collab_elem)
            print(f"  [DEBUG] After third pass: {len(object_ids)} elements, {pass3_count} created in third pass")

        # Update parentage for all elements on re-runs (so lanes parent their children)
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
                            print(f"  [DEBUG] Fixed parentage: {eid} → lane {lane}")
                    except:
                        pass

        # Set tagged values (must be done after elements exist)
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

        # Create connectors (sequence flows)
        conn_count = 0
        for flow in sequence_flows:
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

            # Check if connector already exists (by either short or long stereotype)
            exists = False
            src_elem.Connectors.Refresh()
            for i in range(src_elem.Connectors.Count):
                conn = src_elem.Connectors.GetAt(i)
                if conn.SupplierID == tgt_elem.ElementID and conn.Stereotype in ("SequenceFlow", "BPMN2.0::SequenceFlow"):
                    exists = True
                    # Upgrade short-form stereotype to full BPMN2.0:: form
                    if conn.Stereotype == "SequenceFlow" and conn.StereotypeEx != "BPMN2.0::SequenceFlow":
                        conn.StereotypeEx = "BPMN2.0::SequenceFlow"
                    if flow["condition"]:
                        conn.Name = flow["condition"]
                    conn.Update()
                    break

            if not exists:
                new_conn = src_elem.Connectors.AddNew("", "SequenceFlow")
                new_conn.SupplierID = tgt_elem.ElementID
                new_conn.Direction = "Unidirectional"
                new_conn.StereotypeEx = "BPMN2.0::SequenceFlow"
                if flow["condition"]:
                    new_conn.Name = flow["condition"]
                new_conn.Update()
                conn_count += 1

        print(f"Created {conn_count} new connector(s)")

        # Diagram
        diag = None
        diag_guid_key = "_diagram_newsletter"
        existing_diag_guid = guid_map.get(diag_guid_key)
        if existing_diag_guid:
            try:
                diag = repo.GetDiagramByGuid(existing_diag_guid)
            except:
                diag = None

        if not diag:
            # Fallback: read diagram GUID from MD CollaborationModel fields
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
                if d.Name == "Newsletter Process Architecture":
                    diag = d
                    break

        if not diag and collab_elem:
            diag = collab_elem.Diagrams.AddNew("Newsletter Process Architecture", "BusinessProcess")
            diag.Update()
            collab_elem.Update()
            guid_map[diag_guid_key] = diag.DiagramGUID
            print("  Created new diagram under CollaborationModel")

        # Set diagram stereotype for BPMN2.0 rendering
        if diag:
            diag.Stereotype = "Collaboration"
            diag.StereotypeEx = "BPMN2.0::Collaboration"
            diag.Update()
            # Ensure t_xref for diagram stereotype (COM API may not persist it)
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

        # Place diagram objects — BPMN lane layout
        if diag:
            # Derive lane info from elements dict (case-preserved)
            lane_ids = {eid for eid, edata in elements.items() if edata.get("label") == "Lane"}
            lane_order = sorted(lane_ids)
            lanes_config = [{"id": lid} for lid in lane_order]

            diag.DiagramObjects.Refresh()
            existing_count = diag.DiagramObjects.Count
            if existing_count > 0:
                print(f"  Diagram has {existing_count} objects, preserving positions")
                # Add new elements not yet placed on the diagram
                placed = diagram_utils.get_placed_ids(diag)
                new_ids = [eid for eid, oid in object_ids.items()
                           if eid not in lane_ids and oid not in placed]
                if new_ids:
                    print(f"  [DEBUG] {len(new_ids)} new element(s) need diagram placement")
                    # Group new elements by lane
                    new_by_lane = {}
                    for eid in new_ids:
                        lane = diagram_utils.get_lane_from_fields(elements[eid].get("fields", {}))
                        if lane and lane in lane_ids:
                            new_by_lane.setdefault(lane, []).append(eid)
                    if new_by_lane:
                        lane_bounds = diagram_utils.compute_bpmn_lane_positions(lanes_config)
                        # Find existing elements already in each lane for append offset
                        all_by_lane = {}
                        for eid, edata in elements.items():
                            if edata.get("label") == "Lane":
                                continue
                            lane = diagram_utils.get_lane_from_fields(edata.get("fields", {}))
                            if lane and lane in lane_ids:
                                all_by_lane.setdefault(lane, []).append(eid)
                        # Sort by process flow order so new elements get correct positions
                        for lane_id in all_by_lane:
                            all_by_lane[lane_id] = diagram_utils.sort_by_flow_order(
                                all_by_lane[lane_id], sequence_flows)
                        new_positions = {}
                        for lane_id, eids in new_by_lane.items():
                            combined = all_by_lane.get(lane_id, [])
                            all_epos = diagram_utils.compute_bpmn_element_positions(
                                 {lane_id: combined}, lane_bounds, elem_types=elem_types)
                            for eid in eids:
                                if eid in all_epos:
                                    new_positions[eid] = all_epos[eid]
                        added = diagram_utils.add_missing_elements(diag, new_ids, object_ids, new_positions)
                        if added:
                            print(f"  Added {added} new element(s) to existing diagram")
            else:
                print("  Placing elements on diagram (first time)")
                lane_bounds = diagram_utils.compute_bpmn_lane_positions(lanes_config)
                # Group non-lane elements by lane
                elements_by_lane = {}
                unassigned = []
                for eid, edata in elements.items():
                    if edata.get("label") == "Lane":
                        continue
                    lane = diagram_utils.get_lane_from_fields(edata.get("fields", {}))
                    if lane and lane in lane_ids and lane in lane_bounds:
                        elements_by_lane.setdefault(lane, []).append(eid)
                    else:
                        unassigned.append(eid)
                if unassigned:
                    print(f"  Warning: {len(unassigned)} element(s) have no Lane field")
                # Sort elements within each lane by process flow order
                for lane_id in elements_by_lane:
                    elements_by_lane[lane_id] = diagram_utils.sort_by_flow_order(
                        elements_by_lane[lane_id], sequence_flows)
                # Compute positions
                positions = dict(lane_bounds)
                elem_pos = diagram_utils.compute_bpmn_element_positions(elements_by_lane, lane_bounds, elem_types=elem_types)
                positions.update(elem_pos)
                all_ids = list(lane_ids) + [
                    eid for eid in elements
                    if eid not in lane_ids
                    and diagram_utils.get_lane_from_fields(elements[eid].get("fields", {})) in lane_ids]
                count = diagram_utils.create_diagram_objects(diag, all_ids, object_ids, positions)
                if count:
                    diag.Update()
                    print(f"  Placed {count} elements on diagram")

        # Save GUID map
        guid_map["_collaboration_model"] = collab_elem.ElementGUID if collab_elem else ""
        if diag:
            guid_map[diag_guid_key] = diag.DiagramGUID
        guid_map["elements"] = elem_guid_map
        with open(GUID_MAP_FILE, "w") as f:
            json.dump(guid_map, f, indent=2)

    finally:
        try:
            repo.RefreshModelView(0)  # Full model tree refresh
            repo.RefreshOpenDiagrams(True)
        except Exception as e:
            print(f"  [refresh] RefreshModelView(0) failed: {e}")
        try:
            repo.CloseFile()
        except:
            pass
        pythoncom.CoUninitialize()

    killed = kill_new_ea_processes(before_pids)
    if killed:
        print(f"  Cleaned up {len(killed)} zombie EA process(es)")

    print("Done.")


if __name__ == "__main__":
    main()
