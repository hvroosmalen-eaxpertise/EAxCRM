"""Generate ArchiMate model in EAxCRM.qea from Markdown model file.

Usage:
    python generate_archimate.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-Archimate.md]

Idempotent: stores a JSON mapping of MD-GUID -> EA-GUID after first run.
Re-run to update names, descriptions, or add new elements/relations.
"""
import sys, os, argparse, json, subprocess, time
import diagram_utils


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-Archimate.md"
GUID_MAP_PATH = os.path.join(SCRIPT_DIR, "archimate_guid_map.json")

ARCHIMATE_ELEMENT_STEREOTYPES = {
    "BusinessActor": "ArchiMate3::ArchiMate_BusinessActor",
    "BusinessRole": "ArchiMate3::ArchiMate_BusinessRole",
    "BusinessFunction": "ArchiMate3::ArchiMate_BusinessFunction",
    "BusinessProcess": "ArchiMate3::ArchiMate_BusinessProcess",
    "BusinessObject": "ArchiMate3::ArchiMate_BusinessObject",
    "BusinessService": "ArchiMate3::ArchiMate_BusinessService",
    "ApplicationComponent": "ArchiMate3::ArchiMate_ApplicationComponent",
    "ApplicationCollaboration": "ArchiMate3::ArchiMate_ApplicationCollaboration",
    "ApplicationInterface": "ArchiMate3::ArchiMate_ApplicationInterface",
    "ApplicationService": "ArchiMate3::ArchiMate_ApplicationService",
    "ApplicationFunction": "ArchiMate3::ArchiMate_ApplicationFunction",
    "DataObject": "ArchiMate3::ArchiMate_DataObject",
    "Node": "ArchiMate3::ArchiMate_Node",
    "Device": "ArchiMate3::ArchiMate_Device",
    "SystemSoftware": "ArchiMate3::ArchiMate_SystemSoftware",
    "TechnologyService": "ArchiMate3::ArchiMate_TechnologyService",
    "Artifact": "ArchiMate3::ArchiMate_Artifact",
    "Grouping": "ArchiMate3::ArchiMate_Grouping",
    "Location": "ArchiMate3::ArchiMate_Location",
}

ARCHIMATE_RELATION_STEREOTYPES = {
    "Composition": "ArchiMate3::ArchiMate_Composition",
    "Aggregation": "ArchiMate3::ArchiMate_Aggregation",
    "Assignment": "ArchiMate3::ArchiMate_Assignment",
    "Realization": "ArchiMate3::ArchiMate_Realization",
    "Association": "ArchiMate3::ArchiMate_Association",
    "Triggering": "ArchiMate3::ArchiMate_Triggering",
    "Flow": "ArchiMate3::ArchiMate_Flow",
    "Serving": "ArchiMate3::ArchiMate_Serving",
    "Access": "ArchiMate3::ArchiMate_Access",
    "Influence": "ArchiMate3::ArchiMate_Influence",
}

# Short stereotype name (for t_connector.Stereotype) — no longer used via SQLite
# but kept for reference: {k: v.split("::")[-1] for k, v in ARCHIMATE_RELATION_STEREOTYPES.items()}

# Base Object_Type for each ArchiMate element type (Sparx EA base UML type)
ELEMENT_BASE_TYPE = {
    "BusinessActor": "Class",
    "BusinessRole": "Class",
    "BusinessFunction": "Activity",
    "BusinessProcess": "Activity",
    "BusinessObject": "Class",
    "BusinessService": "Class",
    "ApplicationComponent": "Component",
    "ApplicationCollaboration": "Class",
    "ApplicationInterface": "Interface",
    "ApplicationService": "Activity",
    "ApplicationFunction": "Class",
    "DataObject": "Class",
    "Node": "Node",
    "Device": "Device",
    "SystemSoftware": "Class",
    "TechnologyService": "Class",
    "Artifact": "Class",
    "Grouping": "Class",
    "Location": "Class",
}

# Base Connector_Type for each ArchiMate relationship type
CONNECTOR_BASE_TYPE = {
    "Composition": "Aggregation",
    "Aggregation": "Aggregation",
    "Assignment": "Association",
    "Realization": "Realisation",
    "Association": "Association",
    "Triggering": "Association",
    "Flow": "Association",
    "Serving": "Association",
    "Access": "Association",
    "Influence": "Association",
}


def load_guid_map():
    if os.path.exists(GUID_MAP_PATH):
        with open(GUID_MAP_PATH) as f:
            return json.load(f)
    return {}


def save_guid_map(mapping):
    with open(GUID_MAP_PATH, "w") as f:
        json.dump(mapping, f, indent=2)


def parse_md(path):
    """Parse the Markdown model file into elements and relations."""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    elements = []
    relations = []
    current = None
    section = None

    for line in lines:
        line = line.rstrip()

        if line.strip() == "## Elements":
            section = "elements"
            continue
        if line.strip() == "## Relationships":
            section = "relationships"
            continue

        if line.startswith("### "):
            if current is not None:
                if current["kind"] == "element":
                    elements.append(current)
                else:
                    relations.append(current)

            remainder = line[4:].strip()
            import re
            m = re.match(r'(\w+)\s*[—\-]+\s*(\S+)', remainder)
            if not m:
                continue
            typ, id_ = m.group(1), m.group(2)

            current = {
                "kind": "element" if section == "elements" else "relation",
                "type": typ.strip(),
                "id": id_.strip(),
                "name": "",
                "description": "",
                "guid": "",
                "layer": "",
                "source": "",
                "target": "",
            }
            continue

        if current is None:
            continue

        if line.startswith("- "):
            kv = line[2:].strip()
            if ": " in kv:
                key, value = kv.split(": ", 1)
                value = value.strip()
                if key == "Name":
                    current["name"] = value
                elif key == "Description":
                    current["description"] = value
                elif key in ("GUID", "Guid", "guid"):
                    current["guid"] = value
                elif key == "Layer":
                    current["layer"] = value
                elif key == "Source":
                    current["source"] = value
                elif key == "Target":
                    current["target"] = value

    if current is not None:
        if current["kind"] == "element":
            elements.append(current)
        else:
            relations.append(current)

    for el in elements:
        el["sparx_stereotype"] = ARCHIMATE_ELEMENT_STEREOTYPES.get(el["type"], "")
    for rel in relations:
        rel["sparx_stereotype"] = ARCHIMATE_RELATION_STEREOTYPES.get(rel["type"], "")

    return elements, relations


def get_or_create_package(parent, name):
    for i in range(parent.Packages.Count):
        p = parent.Packages.GetAt(i)
        if p.Name == name:
            return p
    pkg = parent.Packages.AddNew(name, "Package")
    pkg.Update()
    parent.Update()
    return pkg


def sync_elements(repo, pkg, elements, guid_map):
    """Create or update elements. Uses md_guid -> ea_guid mapping for idempotency."""
    # Build name lookup from package elements (for idempotent fallback)
    pkg.Elements.Refresh()
    pkg_elems_by_name = {}
    for j in range(pkg.Elements.Count):
        e = pkg.Elements.GetAt(j)
        pkg_elems_by_name[e.Name] = e

    for el in elements:
        md_guid = el["guid"]
        if not md_guid:
            print(f"  SKIP '{el['id']}': no GUID in MD")
            continue

        # 1) Lookup EA GUID from map
        ea_guid = guid_map.get(md_guid)
        existing = None
        if ea_guid:
            try:
                existing = repo.GetElementByGuid(ea_guid)
            except:
                pass

        # 2) Name-based fallback — scan package for element with same name
        if not existing:
            existing = pkg_elems_by_name.get(el["name"])

        base_type = ELEMENT_BASE_TYPE.get(el["type"], "Class")

        if existing:
            existing.Name = el["name"]
            existing.Notes = el["description"]
            existing.StereotypeEx = el["sparx_stereotype"]
            existing.Update()
            guid_map[md_guid] = existing.ElementGUID
            print(f"  Updated: '{el['name']}' ({el['type']})")
        else:
            new_elem = pkg.Elements.AddNew(el["name"], base_type)
            new_elem.StereotypeEx = el["sparx_stereotype"]
            new_elem.Notes = el["description"]
            new_elem.Update()

            pkg.Elements.Refresh()
            for j in range(pkg.Elements.Count):
                e = pkg.Elements.GetAt(j)
                if e.ElementID == new_elem.ElementID:
                    guid_map[md_guid] = e.ElementGUID
                    pkg_elems_by_name[e.Name] = e
                    break

            print(f"  Created: '{el['name']}' ({el['type']})")


def sync_relations(repo, relations, elements, guid_map):
    """Create or update connectors via COM API."""
    elem_by_id = {e["id"]: e for e in elements}

    for rel in relations:
        src = elem_by_id.get(rel["source"])
        tgt = elem_by_id.get(rel["target"])
        if not src or not tgt:
            print(f"  SKIP rel '{rel['id']}': source/target element not found")
            continue
        if not rel["sparx_stereotype"]:
            print(f"  SKIP rel '{rel['id']}': unknown type '{rel['type']}'")
            continue

        src_ea_guid = guid_map.get(src["guid"])
        tgt_ea_guid = guid_map.get(tgt["guid"])
        if not src_ea_guid or not tgt_ea_guid:
            print(f"  SKIP rel '{rel['id']}': source/target not yet in EA")
            continue

        full_stereo = rel["sparx_stereotype"]
        base_type = CONNECTOR_BASE_TYPE.get(rel["type"], "Association")

        src_elem = repo.GetElementByGuid(src_ea_guid)
        tgt_elem = repo.GetElementByGuid(tgt_ea_guid)
        if not src_elem or not tgt_elem:
            print(f"  SKIP rel '{rel['id']}': source/target element not found in repo")
            continue

        # Check if connector already exists between these two elements
        exists = False
        for i in range(src_elem.Connectors.Count):
            conn = src_elem.Connectors.GetAt(i)
            if conn.SupplierID == tgt_elem.ElementID and conn.StereotypeEx == full_stereo:
                exists = True
                break

        if exists:
            print(f"  Exists rel: '{rel['id']}' ({rel['type']})")
        else:
            new_conn = src_elem.Connectors.AddNew("", base_type)
            new_conn.SupplierID = tgt_elem.ElementID
            new_conn.StereotypeEx = full_stereo
            new_conn.Direction = "Source -> Destination"
            new_conn.Update()
            print(f"  Created rel: '{rel['id']}' ({rel['type']})")


def get_ea_pids():
    """Return set of PIDs for all currently running EA.exe processes."""
    try:
        out = subprocess.check_output(
            ["powershell", "-command",
             "Get-Process -Name 'EA' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"],
            text=True, timeout=10
        )
        return set(int(pid.strip()) for pid in out.strip().splitlines() if pid.strip())
    except:
        return set()


def kill_new_ea_processes(before_pids):
    """Kill EA.exe processes that started after before_pids was captured."""
    after_pids = get_ea_pids()
    new_pids = after_pids - before_pids
    for pid in new_pids:
        try:
            subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                           capture_output=True, timeout=5)
        except:
            pass
    return new_pids


def main():
    parser = argparse.ArgumentParser(description="Generate ArchiMate model in EAxCRM.qea")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    elements, relations = parse_md(args.md)
    print(f"Parsed {len(elements)} elements, {len(relations)} relationships")

    guid_map = load_guid_map()
    print(f"Loaded {len(guid_map)} GUID mappings")

    try:
        import win32com.client
    except ImportError:
        print("FAIL: win32com not installed. Run: pip install pywin32")
        sys.exit(1)

    # Record EA processes before we start (only kill our own later)
    before_pids = get_ea_pids()

    repo = win32com.client.Dispatch("EA.Repository")
    repo.OpenFile(args.qea)
    print(f"Connected: {repo.ConnectionString}")

    # Activate ArchiMate MDG technology
    try:
        repo.ActivateTechnology("ArchiMate3")
        print("  Activated ArchiMate3 MDG technology")
    except Exception as e:
        print(f"  Note: ActivateTechnology failed: {e}")

    root = repo.Models.GetAt(0)
    app_arch = None
    for i in range(root.Packages.Count):
        p = root.Packages.GetAt(i)
        if p.Name == "Application Architecture":
            app_arch = p
            break
    if not app_arch:
        app_arch = root.Packages.AddNew("Application Architecture", "Package")
        app_arch.Update()
        root.Update()
    eax_pkg = get_or_create_package(app_arch, "EAxCRM")

    try:
        # Phase 1: Elements
        print("\n--- Elements ---")
        sync_elements(repo, eax_pkg, elements, guid_map)
        save_guid_map(guid_map)

        # Phase 2: Relationships
        print("\n--- Relationships ---")
        sync_relations(repo, relations, elements, guid_map)

        # Build object_ids: el["id"] -> numeric EA ElementID
        object_ids = {}
        for el in elements:
            ea_guid = guid_map.get(el["guid"])
            if not ea_guid:
                continue
            try:
                ea_elem = repo.GetElementByGuid(ea_guid)
            except:
                continue
            if ea_elem:
                object_ids[el["id"]] = ea_elem.ElementID

        # Phase 3: Diagram
        diag_guid_key = "_diagram_eax_archimate"
        existing_diag_guid = guid_map.get(diag_guid_key)

        print("\n--- Diagram ---")

        # Look up diagram by GUID (for idempotent preservation)
        diag = None
        if existing_diag_guid:
            try:
                diag = repo.GetDiagramByGuid(existing_diag_guid)
            except:
                diag = None

        if not diag:
            for i in range(eax_pkg.Diagrams.Count):
                d = eax_pkg.Diagrams.GetAt(i)
                if d.Name == "EAxCRM ArchiMate":
                    diag = d
                    break

        if not diag:
            diag = eax_pkg.Diagrams.AddNew("EAxCRM ArchiMate", "Application Layer")
            diag.Update()
            eax_pkg.Update()
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)
            print("  Created diagram — element layout will be auto-generated")

            eid_list = [el["id"] for el in elements]
            positions = diagram_utils.compute_diagonal_positions(eid_list,
                per_row=8, step=200, row_gap=200, elem_width=180, elem_height=100)
            count = diagram_utils.create_diagram_objects(diag, eid_list, object_ids, positions)
            print(f"  Placed {count} elements on diagram")
        else:
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)
            placed = diagram_utils.get_placed_ids(diag)
            new_els = [el for el in elements if object_ids.get(el["id"]) not in placed]
            if new_els:
                new_ids = [el["id"] for el in new_els]
                new_positions = diagram_utils.compute_diagonal_positions(new_ids,
                    start_index=len(placed), per_row=8, step=200, row_gap=200,
                    elem_width=180, elem_height=100)
                added = diagram_utils.add_missing_elements(diag, new_ids, object_ids, new_positions)
                print(f"  Added {added} new element(s) to existing diagram")
            else:
                print("  Diagram already has all elements — preserving manual layout")

        diag.StereotypeEx = "ArchiMate3::ArchiMate_ArchimateDiagram"
        diag.Update()
        print("  Set diagram stereotype to ArchiMate_ArchimateDiagram")
    finally:
        try:
            repo.CloseFile()
        except:
            pass

    killed = kill_new_ea_processes(before_pids)
    if killed:
        print(f"  Cleaned up {len(killed)} zombie EA process(es)")

    print("\nDone. Open EAxCRM.qea in Sparx EA to view.")


if __name__ == "__main__":
    main()
