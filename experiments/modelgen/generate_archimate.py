"""Generate ArchiMate model in EAxCRM.qea from Markdown model file.

Usage:
    python generate_archimate.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-Archimate.md]

Idempotent: stores a JSON mapping of MD-GUID -> EA-GUID after first run.
Re-run to update names, descriptions, or add new elements/relations.
"""
import sys, os, argparse, json, uuid, sqlite3, subprocess, time


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
    for el in elements:
        md_guid = el["guid"]
        if not md_guid:
            print(f"  SKIP '{el['id']}': no GUID in MD")
            continue

        # Lookup EA GUID from map, then try to find element
        ea_guid = guid_map.get(md_guid)
        existing = None
        if ea_guid:
            try:
                existing = repo.GetElementByGuid(ea_guid)
            except:
                pass

        base_type = ELEMENT_BASE_TYPE.get(el["type"], "Class")

        if existing:
            existing.Name = el["name"]
            existing.Notes = el["description"]
            existing.StereotypeEx = el["sparx_stereotype"]
            existing.Update()
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
            if conn.SupplierID == tgt_elem.ElementID:
                exists = True
                break

        if exists:
            print(f"  Exists rel: '{rel['id']}' ({rel['type']})")
        else:
            new_conn = src_elem.Connectors.AddNew(rel["id"], base_type)
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

    # Phase 1: Elements — requires COM API
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
        print("\n--- Elements ---")
        sync_elements(repo, eax_pkg, elements, guid_map)
        save_guid_map(guid_map)
    finally:
        try:
            repo.CloseFile()
        except:
            pass
        kill_new_ea_processes(before_pids)
        time.sleep(0.5)

    # Phase 1b: Fix element Object_Type + Stereotype via SQLite
    # COM API's AddNew doesn't always set the right base type or fill t_object.Stereotype
    db_fix = sqlite3.connect(args.qea)
    try:
        t_object_fixes = 0
        t_xref_fixes = 0
        for el in elements:
            ea_guid = guid_map.get(el["guid"])
            if not ea_guid:
                continue
            base_type = ELEMENT_BASE_TYPE.get(el["type"], "Class")
            full_stereo = ARCHIMATE_ELEMENT_STEREOTYPES.get(el["type"], "")
            short_stereo = full_stereo.split("::")[-1]

            # Fix Object_Type + Stereotype in t_object (short form, e.g. ArchiMate_Artifact)
            # EA stores the short form in t_object.Stereotype; the full ArchiMate3:: prefix
            # goes only in t_xref.Description as the FQName.
            c = db_fix.execute(
                "UPDATE t_object SET Object_Type=?, Stereotype=?"
                " WHERE ea_guid=? AND (Object_Type!=? OR Stereotype IS NULL OR Stereotype!=?)",
                (base_type, short_stereo, ea_guid, base_type, short_stereo)
            )
            t_object_fixes += c.rowcount

            # Ensure t_xref entry for stereotype (COM API StereotypeEx often leaves Description NULL)
            existing_xref = db_fix.execute(
                "SELECT XrefID FROM t_xref WHERE Client=? AND Type='Stereotypes' AND Visibility='element property'",
                (ea_guid,)
            ).fetchone()
            desc = f"@STEREO;Name={short_stereo};FQName={full_stereo};@ENDSTEREO;"
            if existing_xref:
                db_fix.execute(
                    "UPDATE t_xref SET Description=? WHERE XrefID=?",
                    (desc, existing_xref[0])
                )
                t_xref_fixes += 1
            else:
                xref_id = "{" + str(uuid.uuid4()).upper() + "}"
                db_fix.execute(
                    "INSERT INTO t_xref (XrefID, Type, Visibility, Namespace, "
                    "Partition, Description, Client, Supplier) "
                    "VALUES (?, 'Stereotypes', 'element property', "
                    "'Public', '0', ?, ?, '<none>')",
                    (xref_id, desc, ea_guid)
                )
                t_xref_fixes += 1

        db_fix.commit()
        if t_object_fixes:
            print(f"  Fixed Object_Type/Stereotype for {t_object_fixes} elements")
        if t_xref_fixes:
            print(f"  Fixed t_xref for {t_xref_fixes} elements")
    finally:
        db_fix.close()

    # Phase 2: Relationships — COM API
    repo_rel = win32com.client.Dispatch("EA.Repository")
    repo_rel.OpenFile(args.qea)
    try:
        print("\n--- Relationships ---")
        sync_relations(repo_rel, relations, elements, guid_map)
    finally:
        # CloseFile can hang; use Exit() as a fallback
        try:
            repo_rel.CloseFile()
        except:
            pass
        kill_new_ea_processes(before_pids)
        time.sleep(0.5)

    # Phase 3: Diagram — COM API for objects, then SQLite for diagram type/stereotype
    diag_guid_key = "_diagram_eax_archimate"
    existing_diag_guid = guid_map.get(diag_guid_key)

    repo2 = win32com.client.Dispatch("EA.Repository")
    repo2.OpenFile(args.qea)
    try:
        root2 = repo2.Models.GetAt(0)
        app_arch2 = None
        for i in range(root2.Packages.Count):
            p = root2.Packages.GetAt(i)
            if p.Name == "Application Architecture":
                app_arch2 = p
                break
        if not app_arch2:
            app_arch2 = root2.Packages.AddNew("Application Architecture", "Package")
            app_arch2.Update()
            root2.Update()
        eax_pkg2 = get_or_create_package(app_arch2, "EAxCRM")
        print("\n--- Diagram ---")

        # Look up diagram by GUID (for idempotent preservation)
        diag = None
        if existing_diag_guid:
            try:
                diag = repo2.GetDiagramByGuid(existing_diag_guid)
            except:
                diag = None

        if not diag:
            for i in range(eax_pkg2.Diagrams.Count):
                d = eax_pkg2.Diagrams.GetAt(i)
                if d.Name == "EAxCRM ArchiMate":
                    diag = d
                    break

        if not diag:
            diag = eax_pkg2.Diagrams.AddNew("EAxCRM ArchiMate", "ArchiMate3::ArchiMate_ArchimateDiagram")
            diag.Update()
            eax_pkg2.Update()
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)
            print("  Created diagram — element layout will be auto-generated")

            # Place elements with grid layout
            LAYER_Y = {"Business": 20, "Application": 340, "Technology": 660, "Composite": 980}
            W, H = 180, 100
            GAP = 30
            layer_counters = {}
            added = 0

            for el in elements:
                ea_guid = guid_map.get(el["guid"])
                if not ea_guid:
                    continue
                try:
                    ea_elem = repo2.GetElementByGuid(ea_guid)
                except:
                    continue
                if not ea_elem:
                    continue

                layer = el.get("layer", "Business")
                y = LAYER_Y.get(layer, 20)
                idx = layer_counters.get(layer, 0)
                x = idx * (W + GAP) + 20
                layer_counters[layer] = idx + 1

                dobj = diag.DiagramObjects.AddNew("", "")
                dobj.ElementID = ea_elem.ElementID
                dobj.left = x
                dobj.top = y
                dobj.right = x + W
                dobj.bottom = y + H
                dobj.Update()
                added += 1

            diag.Update()
            print(f"  Placed {added} elements in diagram")
        else:
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)
            print("  Diagram already exists — preserving manual layout")
    finally:
        try:
            repo2.CloseFile()
        except:
            pass
        kill_new_ea_processes(before_pids)
        time.sleep(0.5)

    # Set diagram type, stereotype, and t_xref via SQLite
    db2 = sqlite3.connect(args.qea)
    try:
        drow = db2.execute(
            "SELECT ea_guid FROM t_diagram WHERE Name='EAxCRM ArchiMate'"
        ).fetchone()
        if drow:
            dguid = drow[0]
            db2.execute(
                "UPDATE t_diagram SET Diagram_Type='ArchiMateBusiness', "
                "Stereotype='ArchiMate_ArchimateDiagram' "
                "WHERE Name='EAxCRM ArchiMate'"
            )
            # Remove previous diagram xrefs for this diagram
            db2.execute(
                "DELETE FROM t_xref WHERE Type='Stereotypes' "
                "AND Visibility='diagram property' AND Client=?",
                (dguid,)
            )
            xref_id = "{" + str(uuid.uuid4()).upper() + "}"
            desc = "@STEREO;Name=ArchiMate_ArchimateDiagram;" \
                   "FQName=ArchiMate3::ArchiMate_ArchimateDiagram;@ENDSTEREO;"
            db2.execute(
                "INSERT INTO t_xref (XrefID, Type, Visibility, Namespace, "
                "Partition, Description, Client, Supplier) "
                "VALUES (?, 'Stereotypes', 'diagram property', "
                "'Public', '0', ?, ?, '<none>')",
                (xref_id, desc, dguid)
            )
            db2.commit()
            print("  Updated diagram type to ArchiMateBusiness + stereotype")
    finally:
        db2.close()

    killed = kill_new_ea_processes(before_pids)
    if killed:
        print(f"  Cleaned up {len(killed)} zombie EA process(es)")

    print("\nDone. Open EAxCRM.qea in Sparx EA to view.")


if __name__ == "__main__":
    main()
