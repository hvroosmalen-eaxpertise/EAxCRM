"""Generate ArchiMate model in EAxCRM.qea from Markdown model file.

Usage:
    python generate_archimate.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-Archimate.md]

Idempotent: stores a JSON mapping of MD-GUID -> EA-GUID after first run.
Re-run to update names, descriptions, or add new elements/relations.
"""
import sys, os, argparse, json, uuid, sqlite3


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

# Short stereotype name (for t_connector.Stereotype)
SHORT_STEREOTYPE = {k: v.split("::")[-1] for k, v in ARCHIMATE_RELATION_STEREOTYPES.items()}

# Base Object_Type for each ArchiMate element type (Sparx EA base UML type)
ELEMENT_BASE_TYPE = {
    "BusinessActor": "Class",
    "BusinessRole": "Class",
    "BusinessFunction": "Class",
    "BusinessProcess": "Class",
    "BusinessObject": "Class",
    "BusinessService": "Class",
    "ApplicationComponent": "Component",
    "ApplicationCollaboration": "Class",
    "ApplicationInterface": "Interface",
    "ApplicationService": "Class",
    "ApplicationFunction": "Class",
    "DataObject": "Class",
    "Node": "Node",
    "Device": "Device",
    "SystemSoftware": "Class",
    "TechnologyService": "Class",
    "Artifact": "Artifact",
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


def sync_relations(db, relations, elements, guid_map):
    """Create or update connectors via direct SQLite."""
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

        short_stereo = SHORT_STEREOTYPE.get(rel["type"])
        base_type = CONNECTOR_BASE_TYPE.get(rel["type"], "Association")

        # Resolve element IDs from GUID map
        src_row = db.execute(
            "SELECT Object_ID FROM t_object WHERE ea_guid=?", (src_ea_guid,)
        ).fetchone()
        tgt_row = db.execute(
            "SELECT Object_ID FROM t_object WHERE ea_guid=?", (tgt_ea_guid,)
        ).fetchone()
        if not src_row or not tgt_row:
            print(f"  SKIP rel '{rel['id']}': source/target object not in DB")
            continue
        src_id, tgt_id = src_row[0], tgt_row[0]

        # Check existing via SQLite
        existing = db.execute(
            "SELECT Connector_ID FROM t_connector WHERE Start_Object_ID=? AND End_Object_ID=? AND Stereotype=?",
            (src_id, tgt_id, short_stereo)
        ).fetchone()

        if existing:
            print(f"  Exists rel: '{rel['id']}' ({rel['type']})")
        else:
            cguid = "{" + str(uuid.uuid4()).upper() + "}"
            db.execute(
                "INSERT INTO t_connector (Start_Object_ID, End_Object_ID, "
                "Connector_Type, Stereotype, Name, Direction, ea_guid) "
                "VALUES (?, ?, ?, ?, '', 'Source -> Destination', ?)",
                (src_id, tgt_id, base_type, short_stereo, cguid)
            )

            # t_xref entry for MDG recognition
            xref_id = "{" + str(uuid.uuid4()).upper() + "}"
            desc = f"@STEREO;Name={short_stereo};FQName={rel['sparx_stereotype']};@ENDSTEREO;"
            db.execute(
                "INSERT INTO t_xref (XrefID, Type, Visibility, Namespace, "
                "Partition, Description, Client, Supplier) "
                "VALUES (?, 'Stereotypes', 'connector property', "
                "'Public', '0', ?, ?, '<none>')",
                (xref_id, desc, cguid)
            )
            db.commit()
            print(f"  Created rel: '{rel['id']}' ({rel['type']})")


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

    # Phase 1b: Fix element Object_Type via SQLite (cases where AddNew type differs)
    db_fix = sqlite3.connect(args.qea)
    try:
        for el in elements:
            ea_guid = guid_map.get(el["guid"])
            if not ea_guid:
                continue
            base_type = ELEMENT_BASE_TYPE.get(el["type"], "Class")
            db_fix.execute(
                "UPDATE t_object SET Object_Type=? WHERE ea_guid=? AND Object_Type!=?",
                (base_type, ea_guid, base_type)
            )
        db_fix.commit()
        updated = db_fix.total_changes
        if updated:
            print(f"  Fixed Object_Type for {updated} elements")
    finally:
        db_fix.close()

    # Phase 2: Relationships — direct SQLite (COM API hangs on CloseFile)
    db = sqlite3.connect(args.qea)
    try:
        print("\n--- Relationships ---")
        sync_relations(db, relations, elements, guid_map)
    finally:
        db.close()

    # Phase 3: Diagram — COM API for objects, auto-layout, then SQLite for diagram type/stereotype
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
        diag = None
        for i in range(eax_pkg2.Diagrams.Count):
            d = eax_pkg2.Diagrams.GetAt(i)
            if d.Name == "EAxCRM ArchiMate":
                diag = d
                break
        if not diag:
            diag = eax_pkg2.Diagrams.AddNew("EAxCRM ArchiMate", "ArchiMate3::ArchiMate_ArchimateDiagram")
            diag.Update()
            eax_pkg2.Update()
            print("  Created diagram")
        else:
            print("  Diagram already exists")

        # Clear existing objects
        for i in range(diag.DiagramObjects.Count - 1, -1, -1):
            diag.DiagramObjects.Delete(i)
        diag.Update()

        # Simple grid layout by layer
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

        print(f"  Added {added} elements to diagram")
    finally:
        try:
            repo2.CloseFile()
        except:
            pass

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

    print("\nDone. Open EAxCRM.qea in Sparx EA to view.")


if __name__ == "__main__":
    main()
