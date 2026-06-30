"""Generate BPMN newsletter process model in EAxCRM.qea from Markdown using COM API.

Usage:
    python generate_newsletter_process_from_md.py

Idempotent: uses GUID map for re-runs. Only creates new elements/connectors/diagrams
on first run. Updates existing ones on subsequent runs. Preserves manual diagram layout.
"""
import sys, os, argparse, re, json, subprocess, win32com.client, pythoncom

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

ELEM_SIZE = {
    "Activity": (100, 55),
    "StartEvent": (50, 50),
    "EndEvent": (50, 50),
    "Gateway": (60, 60),
    "DataObject": (30, 50),
    "Lane": (400, 120),
}

def safe_id(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())

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
                proc_arch.Elements.Refresh()
                # Find the actual ElementID after refresh
                for i in range(proc_arch.Elements.Count):
                    e = proc_arch.Elements.GetAt(i)
                    if e.ElementGUID == new_elem.ElementGUID:
                        elem_guid_map[eid] = e.ElementGUID
                        object_ids[eid] = e.ElementID
                        pkg_elems_by_name[e.Name] = e
                        break
                created_count += 1
                return new_elem

        # DFS: parents before children
        children_of = {}
        for eid, elem_data in elements.items():
            parent_text = elem_data["fields"].get("Parent", "")
            if parent_text:
                pid = safe_id(parent_text)
                if pid in elements:
                    children_of.setdefault(pid, []).append(eid)

        # Root = CollaborationModel
        collab_eid = None
        for eid, elem_data in elements.items():
            if elem_data["label"] == "BPMN Collaboration":
                collab_eid = eid
                break

        if collab_eid:
            collab_elem = create_element(collab_eid, None)
            if collab_elem:
                # DFS create children
                def dfs(parent_eid, parent_elem):
                    for child_eid in children_of.get(parent_eid, []):
                        child_elem = create_element(child_eid, parent_elem)
                        if child_elem:
                            dfs(child_eid, child_elem)
                dfs(collab_eid, collab_elem)

        # Handle free elements (no parent relationship in MD)
        for eid in elements:
            if eid not in object_ids:
                create_element(eid, collab_elem if collab_elem else None)

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

        if not diag:
            for i in range(proc_arch.Diagrams.Count):
                d = proc_arch.Diagrams.GetAt(i)
                if d.Name == "Newsletter Process Architecture":
                    diag = d
                    break

        if not diag:
            diag = proc_arch.Diagrams.AddNew("Newsletter Process Architecture", "BusinessProcess")
            diag.Update()
            proc_arch.Update()
            guid_map[diag_guid_key] = diag.DiagramGUID
            print("  Created new diagram")

        # Set diagram stereotype for BPMN2.0 rendering
        if diag:
            diag.StereotypeEx = "BPMN2.0::Collaboration"
            diag.Update()

        # Place diagram objects only if this is a fresh diagram (no objects yet)
        if diag:
            diag.DiagramObjects.Refresh()
            existing_count = diag.DiagramObjects.Count
            if existing_count > 0:
                print(f"  Diagram has {existing_count} objects, preserving manual layout")
            else:
                print("  Placing elements on diagram (first time)")
                lane_y_top = 0
                lane_y_bot = 120

                pos = {
                    "eaxpertise": (0, 0, 2200, 130),
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

                for eid in draw_order:
                    dobj_oid = object_ids.get(eid)
                    if not dobj_oid or eid not in pos:
                        continue
                    l, t, r, b = pos[eid]
                    dobj = diag.DiagramObjects.AddNew("", "")
                    dobj.ElementID = dobj_oid
                    dobj.left = l
                    dobj.top = t
                    dobj.right = r
                    dobj.bottom = b
                    dobj.Update()
                    diag.DiagramObjects.Refresh()

                diag.Update()
                print(f"  Placed {len(draw_order)} elements on diagram")

        # Save GUID map
        guid_map["_collaboration_model"] = collab_elem.ElementGUID if collab_elem else ""
        if diag:
            guid_map[diag_guid_key] = diag.DiagramGUID
        guid_map["elements"] = elem_guid_map
        with open(GUID_MAP_FILE, "w") as f:
            json.dump(guid_map, f, indent=2)

    finally:
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
