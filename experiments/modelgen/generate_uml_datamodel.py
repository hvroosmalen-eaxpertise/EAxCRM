"""Generate UML data model in EAxCRM.qea from Markdown model file.

Usage:
    python generate_uml_datamodel.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-DataModel.md]

Idempotent: stores a GUID mapping after first run.
Re-run to update names, descriptions, attribute types, or add new entities/relations.
"""
import sys, os, argparse, json, subprocess, re
import diagram_utils

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-DataModel.md"
GUID_MAP_PATH = os.path.join(SCRIPT_DIR, "uml_datamodel_guid_map.json")

SPARX_TYPE_MAP = {
    "int": "int",
    "string": "string",
    "text": "string",
    "datetime": "datetime",
    "date": "date",
    "boolean": "boolean",
    "float": "float",
}


def parse_type_str(raw):
    """Parse 'string(200)' -> ('string', 200) or 'int' -> ('int', None)."""
    raw = raw.strip()
    m = re.match(r"(\w+)\((\d+)\)$", raw)
    if m:
        return m.group(1), int(m.group(2))
    return raw, None


def parse_md(path):
    """Parse the Markdown model file into entities and relationships."""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    entities = []
    relations = []
    current = None
    section = None
    in_attrs = False

    for line in lines:
        line = line.rstrip()

        if line.strip() == "## Entities":
            section = "entities"
            in_attrs = False
            continue
        if line.strip() == "## Relationships":
            section = "relationships"
            in_attrs = False
            continue

        if line.startswith("### "):
            if current is not None:
                if current["kind"] == "entity":
                    entities.append(current)
                else:
                    relations.append(current)
            in_attrs = False

            remainder = line[4:].strip()
            m = re.match(r"(\w+)\s*[—\-]+\s*(\S+)", remainder)
            if not m:
                continue
            typ, id_ = m.group(1), m.group(2)

            current = {
                "kind": "entity" if section == "entities" else "relation",
                "type": typ.strip(),
                "id": id_.strip(),
                "name": "",
                "description": "",
                "guid": "",
                "attributes": [],
                "source": "",
                "target": "",
                "source_multi": "",
                "target_multi": "",
            }
            continue

        if current is None:
            continue

        if line.strip() == "- Attributes:":
            in_attrs = True
            continue

        if in_attrs:
            if line.startswith("  - ") or line.startswith("\t- "):
                attr_text = line.lstrip(" \t-").strip()
                m = re.match(r"(\w[\w_]*)\s*:\s*(.+)", attr_text)
                if m:
                    attr_name = m.group(1)
                    rest = m.group(2)
                    stereo = ""
                    desc = ""
                    type_part = rest
                    sm = re.match(r"(.*?)\s*<<(.+?)>>", rest)
                    if sm:
                        type_part = sm.group(1).strip()
                        stereo = sm.group(2).strip()
                    dm = re.match(r"(.*?)\s*[—\-]+\s*(.+)", rest)
                    if dm:
                        if not sm:
                            type_part = dm.group(1).strip()
                        desc = dm.group(2).strip()
                    sparx_type, length = parse_type_str(type_part)
                    current["attributes"].append({
                        "name": attr_name,
                        "type": sparx_type,
                        "sparx_type": SPARX_TYPE_MAP.get(sparx_type, "string"),
                        "length": length,
                        "stereotype": stereo,
                        "description": desc,
                    })
                continue
            else:
                in_attrs = False

        if line.startswith("- "):
            if in_attrs:
                continue
            kv = line[2:].strip()
            if ": " in kv:
                key, value = kv.split(": ", 1)
                value = value.strip()
                if key == "Name":
                    current["name"] = value
                elif key == "Description":
                    current["description"] = value
                elif key == "Name":
                    current["name"] = value
                elif key in ("GUID", "Guid", "guid"):
                    current["guid"] = value
                elif key == "Source":
                    sm = re.match(r"(\S+)\s*\((.+)\)", value)
                    if sm:
                        current["source"] = sm.group(1).strip()
                        current["source_multi"] = sm.group(2).strip()
                    else:
                        current["source"] = value.strip()
                elif key == "Target":
                    sm = re.match(r"(\S+)\s*\((.+)\)", value)
                    if sm:
                        current["target"] = sm.group(1).strip()
                        current["target_multi"] = sm.group(2).strip()
                    else:
                        current["target"] = value.strip()

    if current is not None:
        if current["kind"] == "entity":
            entities.append(current)
        else:
            relations.append(current)

    return entities, relations


def get_or_create_package(parent, name):
    for i in range(parent.Packages.Count):
        p = parent.Packages.GetAt(i)
        if p.Name == name:
            return p
    pkg = parent.Packages.AddNew(name, "Package")
    pkg.Update()
    parent.Update()
    return pkg


def sync_attribute(ea_attr, attr_def):
    """Update or create a single attribute on an EA element."""
    ea_attr.Name = attr_def["name"]
    ea_attr.Type = attr_def["sparx_type"]
    if attr_def["length"]:
        ea_attr.Length = attr_def["length"]
    elif ea_attr.Length:
        ea_attr.Length = 0
    if attr_def["stereotype"]:
        ea_attr.Stereotype = attr_def["stereotype"]
    elif ea_attr.Stereotype:
        ea_attr.Stereotype = ""
    if attr_def.get("description"):
        ea_attr.Notes = attr_def["description"]
    elif ea_attr.Notes:
        ea_attr.Notes = ""
    ea_attr.Update()


def sync_attributes(ea_elem, attr_defs):
    """Sync attributes on an EA element. Adds new, updates existing, deletes orphans."""
    existing = {}
    for i in range(ea_elem.Attributes.Count):
        a = ea_elem.Attributes.GetAt(i)
        existing[a.Name] = a

    md_names = set()
    for ad in attr_defs:
        md_names.add(ad["name"])
        if ad["name"] in existing:
            sync_attribute(existing[ad["name"]], ad)
        else:
            new_a = ea_elem.Attributes.AddNew(ad["name"], ad["sparx_type"])
            sync_attribute(new_a, ad)

    # Iterate in reverse index order so deletions don't shift indices
    for i in range(ea_elem.Attributes.Count - 1, -1, -1):
        a = ea_elem.Attributes.GetAt(i)
        if a.Name not in md_names:
            ea_elem.Attributes.Delete(i)
            print(f"    Deleted attribute '{a.Name}'")

    ea_elem.Update()


def load_guid_map():
    if os.path.exists(GUID_MAP_PATH):
        with open(GUID_MAP_PATH) as f:
            return json.load(f)
    return {}


def save_guid_map(mapping):
    with open(GUID_MAP_PATH, "w") as f:
        json.dump(mapping, f, indent=2)


def get_ea_pids():
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
    parser = argparse.ArgumentParser(description="Generate UML data model in EAxCRM.qea")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    entities, relations = parse_md(args.md)
    print(f"Parsed {len(entities)} entities, {len(relations)} relationships")

    guid_map = load_guid_map()
    print(f"Loaded {len(guid_map)} GUID mappings")

    try:
        import win32com.client
    except ImportError:
        print("FAIL: win32com not installed. Run: pip install pywin32")
        sys.exit(1)

    before_pids = get_ea_pids()

    repo = win32com.client.Dispatch("EA.Repository")
    repo.OpenFile(args.qea)
    print(f"Connected: {repo.ConnectionString}")

    root = repo.Models.GetAt(0)
    data_arch = None
    for i in range(root.Packages.Count):
        p = root.Packages.GetAt(i)
        if p.Name == "Data Architecture":
            data_arch = p
            break
    if not data_arch:
        data_arch = root.Packages.AddNew("Data Architecture", "Package")
        data_arch.Update()
        root.Update()
    dm_pkg = get_or_create_package(data_arch, "EAxCRM Data Model")

    try:
        # Phase 1: Entities
        print("\n--- Entities ---")

        # Build name lookup from package elements (for idempotent fallback)
        dm_pkg.Elements.Refresh()
        pkg_elements_by_name = {}
        for j in range(dm_pkg.Elements.Count):
            e = dm_pkg.Elements.GetAt(j)
            pkg_elements_by_name[e.Name] = e
            # Seed GUID map from any element that matches an existing MD GUID
            for ent in entities:
                if ent["guid"] and e.ElementGUID == ent["guid"] and ent["guid"] not in guid_map:
                    guid_map[ent["guid"]] = e.ElementGUID

        entity_by_id = {}
        for ent in entities:
            entity_by_id[ent["id"]] = ent
            md_guid = ent["guid"]
            if not md_guid:
                print(f"  SKIP '{ent['id']}': no GUID")
                continue

            # 1) Look up by EA GUID from map
            ea_guid = guid_map.get(md_guid)
            existing = None
            if ea_guid:
                try:
                    existing = repo.GetElementByGuid(ea_guid)
                except:
                    pass

            # 2) Look up by MD GUID directly (matches EA GUID when MD was seeded from EA)
            if not existing:
                try:
                    existing = repo.GetElementByGuid(md_guid)
                except:
                    pass

            # 3) Name-based fallback — scan package for element with same name
            if not existing:
                existing = pkg_elements_by_name.get(ent["name"])

            if existing:
                existing.Name = ent["name"]
                existing.Notes = ent["description"]
                existing.Update()
                print(f"  Updated: '{ent['name']}'")
                guid_map[md_guid] = existing.ElementGUID
                sync_attributes(existing, ent["attributes"])
                print(f"    Synced {len(ent['attributes'])} attributes")
            else:
                new_elem = dm_pkg.Elements.AddNew(ent["name"], "Class")
                new_elem.Notes = ent["description"]
                new_elem.Update()
                dm_pkg.Elements.Refresh()
                # Refresh the name lookup
                for j in range(dm_pkg.Elements.Count):
                    e = dm_pkg.Elements.GetAt(j)
                    if e.ElementID == new_elem.ElementID:
                        guid_map[md_guid] = e.ElementGUID
                        pkg_elements_by_name[e.Name] = e
                        break
                print(f"  Created: '{ent['name']}'")
                sync_attributes(new_elem, ent["attributes"])
                print(f"    Added {len(ent['attributes'])} attributes")

        save_guid_map(guid_map)

        # Phase 2: Relationships (via COM API — creation only, cardinality via SQLite)
        print("\n--- Relationships ---")
        for rel in relations:
            src = entity_by_id.get(rel["source"])
            tgt = entity_by_id.get(rel["target"])
            if not src or not tgt:
                print(f"  SKIP rel '{rel['id']}': source/target entity not found")
                continue

            src_ea_guid = guid_map.get(src["guid"])
            tgt_ea_guid = guid_map.get(tgt["guid"])
            if not src_ea_guid or not tgt_ea_guid:
                print(f"  SKIP rel '{rel['id']}': source/target not yet in EA")
                continue

            src_elem = repo.GetElementByGuid(src_ea_guid)
            tgt_elem = repo.GetElementByGuid(tgt_ea_guid)
            if not src_elem or not tgt_elem:
                print(f"  SKIP rel '{rel['id']}': source/target element not found in repo")
                continue

            # Check if connector already exists
            exists = False
            for i in range(src_elem.Connectors.Count):
                conn = src_elem.Connectors.GetAt(i)
                if conn.SupplierID == tgt_elem.ElementID:
                    exists = True
                    conn.Name = rel.get("name", "")
                    conn.Notes = rel.get("description", "")
                    conn.Update()
                    print(f"  Updated rel: '{rel['id']}'")
                    break

            if not exists:
                new_conn = src_elem.Connectors.AddNew("", "Association")
                new_conn.SupplierID = tgt_elem.ElementID
                new_conn.Direction = "Source -> Destination"
                new_conn.Name = rel.get("name", "")
                new_conn.Notes = rel.get("description", "")
                new_conn.Update()
                print(f"  Created rel: '{rel['id']}'")

        # Phase 2b: Delete orphan connectors via COM API (database-independent)
        print("\n--- Relationship Orphan Cleanup (COM API) ---")
        # Build set of expected (source_EA_guid, target_EA_guid) pairs from MD
        md_pairs = set()
        for rel in relations:
            src = entity_by_id.get(rel["source"])
            tgt = entity_by_id.get(rel["target"])
            if src and tgt:
                sg = guid_map.get(src["guid"])
                tg = guid_map.get(tgt["guid"])
                if sg and tg:
                    md_pairs.add((sg, tg))

        # Only consider connectors where both ends are data-model entities
        dm_guids = set(v for k, v in guid_map.items() if not k.startswith('_'))

        orphan_count = 0
        for ent in entities:
            ea_guid_val = guid_map.get(ent["guid"])
            if not ea_guid_val:
                continue
            try:
                ea_elem = repo.GetElementByGuid(ea_guid_val)
            except:
                continue
            if not ea_elem:
                continue

            # First pass: collect all candidate orphan connector IDs
            candidates = set()
            for i in range(ea_elem.Connectors.Count):
                conn = ea_elem.Connectors.GetAt(i)
                # Use ClientID/SupplierID for actual source/target (not the element being iterated)
                try:
                    src_e = repo.GetElementByID(conn.ClientID)
                    tgt_e = repo.GetElementByID(conn.SupplierID)
                except:
                    continue
                if not src_e or not tgt_e:
                    continue
                src_guid = src_e.ElementGUID
                tgt_guid = tgt_e.ElementGUID
                # Only consider connectors where BOTH ends are data-model elements
                if src_guid not in dm_guids or tgt_guid not in dm_guids:
                    continue
                in_md = (src_guid, tgt_guid) in md_pairs or (tgt_guid, src_guid) in md_pairs
                if in_md:
                    continue
                candidates.add(conn.ConnectorID)

            # Second pass: delete orphans from their source element's collection
            for cid in candidates:
                try:
                    conn = repo.GetConnectorByID(cid)
                except:
                    continue
                if not conn:
                    continue
                try:
                    src_elem = repo.GetElementByID(conn.ClientID)
                except:
                    continue
                if not src_elem:
                    continue
                for j in range(src_elem.Connectors.Count - 1, -1, -1):
                    if src_elem.Connectors.GetAt(j).ConnectorID == cid:
                        src_elem.Connectors.Delete(j)
                        orphan_count += 1
                        break

        if orphan_count:
            print(f"  Deleted {orphan_count} orphan connector(s)")
        else:
            print("  No orphan connectors to remove")

        # Phase 2c: Set cardinality via COM API
        print("\n--- Relationship Cardinality ---")
        cardinality_ok = 0
        for rel in relations:
            src = entity_by_id.get(rel["source"])
            tgt = entity_by_id.get(rel["target"])
            if not src or not tgt:
                continue
            sg = guid_map.get(src["guid"])
            tg = guid_map.get(tgt["guid"])
            if not sg or not tg:
                continue
            src_elem = repo.GetElementByGuid(sg)
            tgt_elem = repo.GetElementByGuid(tg)
            if not src_elem or not tgt_elem:
                continue
            src_multi = rel.get("source_multi", "")
            tgt_multi = rel.get("target_multi", "")
            for i in range(src_elem.Connectors.Count):
                conn = src_elem.Connectors.GetAt(i)
                if conn.SupplierID == tgt_elem.ElementID:
                    try:
                        conn.ClientEnd.Cardinality = src_multi
                        conn.SupplierEnd.Cardinality = tgt_multi
                        conn.Update()
                        cardinality_ok += 1
                    except:
                        pass
                    break
        print(f"  Set cardinality on {cardinality_ok} connector(s)")

        # Build object_ids dict: entity id → EA ElementID
        object_ids = {}
        for ent in entities:
            ea_guid = guid_map.get(ent["guid"])
            if ea_guid:
                try:
                    ea_elem = repo.GetElementByGuid(ea_guid)
                    if ea_elem:
                        object_ids[ent["id"]] = ea_elem.ElementID
                except:
                    pass

        # Phase 3: Diagram
        print("\n--- Diagram ---")
        diag_guid_key = "_diagram_eax_datamodel"
        existing_diag_guid = guid_map.get(diag_guid_key)

        diag = None
        if existing_diag_guid:
            try:
                diag = repo.GetDiagramByGuid(existing_diag_guid)
            except:
                diag = None

        if not diag:
            for i in range(dm_pkg.Diagrams.Count):
                d = dm_pkg.Diagrams.GetAt(i)
                if d.Name == "EAxCRM Data Model":
                    diag = d
                    break

        if not diag:
            diag = dm_pkg.Diagrams.AddNew("EAxCRM Data Model", "Logical")
            diag.Update()
            dm_pkg.Update()
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)
            print("  Created diagram — placing all entities")

            eid_list = [ent["id"] for ent in entities]
            positions = diagram_utils.compute_diagonal_positions(eid_list,
                per_row=8, step=200, row_gap=200, elem_width=200, elem_height=120)
            count = diagram_utils.create_diagram_objects(diag, eid_list, object_ids, positions)
            print(f"  Placed {count} entities on diagram")
        else:
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)

            placed = diagram_utils.get_placed_ids(diag)
            new_ents = [ent for ent in entities if object_ids.get(ent["id"]) not in placed]
            if new_ents:
                new_ids = [ent["id"] for ent in new_ents]
                new_positions = diagram_utils.compute_diagonal_positions(new_ids,
                    start_index=len(placed), per_row=8, step=200, row_gap=200,
                    elem_width=200, elem_height=120)
                added = diagram_utils.add_missing_elements(diag, new_ids, object_ids, new_positions)
                print(f"  Added {added} new entit(ies) to existing diagram")
            else:
                print("  Diagram already has all entities — preserving manual layout")

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

    killed = kill_new_ea_processes(before_pids)
    if killed:
        print(f"  Cleaned up {len(killed)} zombie EA process(es)")

    print("\nDone. Open EAxCRM.qea in Sparx EA to view.")


if __name__ == "__main__":
    main()
