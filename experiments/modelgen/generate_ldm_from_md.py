"""Generate the logical data model (LDM) in EAxCRM.qea from Markdown.

Usage:
    python generate_ldm_from_md.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-DataModel.md]

Idempotent: stores a GUID mapping after first run.
Re-run to update names, descriptions, attribute types, or add new entities/relations.

'LDM' distinguishes this UML-class-based logical model from the physical
data model (PDM), which uses <<table>>-stereotyped classes and lives
under experiments/pdm/.
"""
import sys, os, argparse, json, re
import diagram_utils
import ea_session
from changelog import ChangeLog

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-DataModel.md"
GUID_MAP_PATH = os.path.join(SCRIPT_DIR, "ldm_guid_map.json")

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
    """Parse the Markdown model file into entities, relationships, and enumerations."""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    entities = []
    relations = []
    enumerations = []
    current = None
    section = None
    in_attrs = False
    in_literals = False

    def flush():
        if current is None:
            return
        if current["kind"] == "entity":
            entities.append(current)
        elif current["kind"] == "enumeration":
            enumerations.append(current)
        else:
            relations.append(current)

    for line in lines:
        line = line.rstrip()

        if line.strip() == "## Entities":
            section = "entities"
            in_attrs = False
            in_literals = False
            continue
        if line.strip() == "## Relationships":
            section = "relationships"
            in_attrs = False
            in_literals = False
            continue

        if line.startswith("### "):
            flush()
            in_attrs = False
            in_literals = False

            remainder = line[4:].strip()
            m = re.match(r"(\w+)\s*[—\-]+\s*(\S+)", remainder)
            if not m:
                current = None
                continue
            typ, id_ = m.group(1), m.group(2)

            if typ.strip() == "Enumeration":
                kind = "enumeration"
            else:
                kind = "entity" if section == "entities" else "relation"

            current = {
                "kind": kind,
                "type": typ.strip(),
                "id": id_.strip(),
                "name": "",
                "description": "",
                "guid": "",
                "attributes": [],
                "literals": [],
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

        if line.strip() == "- Literals:":
            in_literals = True
            continue

        if in_literals:
            if line.startswith("  - ") or line.startswith("\t- "):
                current["literals"].append(line.lstrip(" \t-").strip())
                continue
            else:
                in_literals = False

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
            if in_attrs or in_literals:
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

    flush()

    # Resolve attributes typed against a locally-defined Enumeration: keep the
    # enum's own name as sparx_type (rather than the SPARX_TYPE_MAP "string"
    # fallback for an unrecognized primitive) so the generator can classify it.
    enum_names = {e["name"] for e in enumerations}
    for ent in entities:
        for attr in ent["attributes"]:
            if attr["type"] in enum_names:
                attr["sparx_type"] = attr["type"]
                attr["length"] = None
                attr["is_enum"] = True
            else:
                attr["is_enum"] = False

    return entities, relations, enumerations


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
    """Update or create a single attribute on an EA element.

    Note: EA's Attribute Automation object doesn't expose a settable/readable
    `Classifier` property over dynamic COM dispatch here (AttributeError on
    access) -- enum-typed attributes are represented purely via `Type` holding
    the Enumeration's name (e.g. "ContactRole"), matched back by name on the
    EA->MD sync side rather than resolved through a classifier link.
    """
    ea_attr.Name = attr_def["name"]
    ea_attr.Type = attr_def["sparx_type"]
    if attr_def.get("is_enum"):
        if ea_attr.Length:
            ea_attr.Length = 0
    else:
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


def sync_attributes(ea_elem, attr_defs, clog=None, entity_name=""):
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
            if clog:
                clog.log("deleted", a.Name, a.Name, "Attribute", changes={"entity": entity_name})

    ea_elem.Update()


def load_guid_map():
    if os.path.exists(GUID_MAP_PATH):
        with open(GUID_MAP_PATH) as f:
            return json.load(f)
    return {}


def save_guid_map(mapping):
    with open(GUID_MAP_PATH, "w") as f:
        json.dump(mapping, f, indent=2)


def main():
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="Generate UML data model in EAxCRM.qea")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    parser.add_argument("--state-dir", default=SCRIPT_DIR,
                         help="Directory for the changelog and GUID-map files (default: script dir). "
                              "Override in tests so runs against a sandboxed --qea don't touch the real ones.")
    args = parser.parse_args()

    global GUID_MAP_PATH
    GUID_MAP_PATH = os.path.join(args.state_dir, "ldm_guid_map.json")

    entities, relations, enumerations = parse_md(args.md)
    print(f"Parsed {len(entities)} entities, {len(relations)} relationships, {len(enumerations)} enumerations")
    clog = ChangeLog(os.path.join(args.state_dir, "ldm_changelog.md"))
    clog.checkpoint("Parsed MD")

    guid_map = load_guid_map()
    print(f"Loaded {len(guid_map)} GUID mappings")

    try:
        import win32com.client
    except ImportError:
        print("FAIL: win32com not installed. Run: pip install pywin32")
        sys.exit(1)

    before_pids = ea_session.get_ea_pids()

    app = win32com.client.DispatchEx("EA.App")
    repo = app.Repository
    repo.OpenFile(args.qea)
    print(f"Connected: {repo.ConnectionString}")

    root = ea_session.get_model_root(repo)
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
        # Phase 0: Enumerations (must exist before Phase 1 so Class attributes
        # can be classified against them)
        print("\n--- Enumerations ---")
        enum_elemid_by_name = {}
        for enum in enumerations:
            md_guid = enum["guid"]
            ea_guid = guid_map.get(md_guid) if md_guid else None
            existing = None
            if ea_guid:
                try:
                    existing = repo.GetElementByGuid(ea_guid)
                except Exception:
                    pass
            if not existing and md_guid:
                try:
                    existing = repo.GetElementByGuid(md_guid)
                except Exception:
                    pass
            if not existing:
                dm_pkg.Elements.Refresh()
                for j in range(dm_pkg.Elements.Count):
                    e = dm_pkg.Elements.GetAt(j)
                    if e.Name == enum["name"]:
                        existing = e
                        break

            if existing:
                target = existing
                target.Name = enum["name"]
                target.Notes = enum["description"]
                target.Update()
                if md_guid:
                    guid_map[md_guid] = target.ElementGUID
                clog.log("updated", enum["id"], enum["name"], "Enumeration", target.ElementGUID)
            else:
                target = dm_pkg.Elements.AddNew(enum["name"], "Enumeration")
                target.Notes = enum["description"]
                target.Update()
                if md_guid:
                    guid_map[md_guid] = target.ElementGUID
                clog.log("created", enum["id"], enum["name"], "Enumeration", target.ElementGUID)

            # EA's own convention for enumeration literals (see the built-in
            # "Enumeration Name" template element): each literal is an
            # Attribute with Type="int" and Stereotype="enum" -- matched here
            # so hand-authored and generated Enumerations look identical.
            existing_lits = {}
            target.Attributes.Refresh()
            for i in range(target.Attributes.Count):
                a = target.Attributes.GetAt(i)
                existing_lits[a.Name] = a
            lit_names = set(enum["literals"])
            for lit in enum["literals"]:
                a = existing_lits.get(lit)
                if not a:
                    a = target.Attributes.AddNew(lit, "int")
                a.Type = "int"
                a.Stereotype = "enum"
                a.Update()
            for i in range(target.Attributes.Count - 1, -1, -1):
                a = target.Attributes.GetAt(i)
                if a.Name not in lit_names:
                    target.Attributes.Delete(i)
            target.Update()

            enum_elemid_by_name[enum["name"]] = target.ElementID
            print(f"    Synced {len(enum['literals'])} literals for {enum['name']}")

        save_guid_map(guid_map)

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
        # Enums are also valid relationship endpoints (e.g. contact -> contactrole
        # for the has_role association). Seed them first so Phase 2 can resolve
        # both Class -> Class and Class -> Enum relationships.
        for enum in enumerations:
            entity_by_id[enum["id"]] = enum
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
                old_name = existing.Name
                old_notes = existing.Notes
                existing.Name = ent["name"]
                existing.Notes = ent["description"]
                existing.Update()
                changes = {}
                if old_name != ent["name"]:
                    changes["Name"] = (old_name, ent["name"])
                if old_notes != ent["description"]:
                    changes["Notes"] = (old_notes, ent["description"])
                clog.log("updated", ent["id"], ent["name"], "Class", existing.ElementGUID,
                         changes=(changes or None))
                guid_map[md_guid] = existing.ElementGUID
                sync_attributes(existing, ent["attributes"], clog=clog, entity_name=ent["name"])
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
                clog.log("created", ent["id"], ent["name"], "Class", new_elem.ElementGUID)
                sync_attributes(new_elem, ent["attributes"], clog=clog, entity_name=ent["name"],
                                 enum_elemid_by_name=enum_elemid_by_name)
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

            # Check if connector already exists. Must also check ClientID, not
            # just SupplierID -- src_elem.Connectors includes connectors where
            # src_elem is the *target* too (e.g. every "X -> Customer" relation
            # shows up in Customer's own Connectors collection). A self-
            # referential relation (src_elem is tgt_elem, e.g. Customer ->
            # Customer) would otherwise spuriously match the first unrelated
            # incoming connector and overwrite its Name/Notes (found + fixed
            # 2026-07-06, corrupted r-contact-customer's "belongs_to" when
            # adding r-customer-customer's "merged_into").
            exists = False
            for i in range(src_elem.Connectors.Count):
                conn = src_elem.Connectors.GetAt(i)
                if conn.ClientID == src_elem.ElementID and conn.SupplierID == tgt_elem.ElementID:
                    exists = True
                    conn.Name = rel.get("name", "")
                    conn.Notes = rel.get("description", "")
                    conn.Update()
                    clog.log("updated", rel["id"], f"{src['name']} -> {tgt['name']}", "Association", conn.ConnectorGUID)
                    break

            if not exists:
                new_conn = src_elem.Connectors.AddNew("", "Association")
                new_conn.SupplierID = tgt_elem.ElementID
                new_conn.Direction = "Source -> Destination"
                new_conn.Name = rel.get("name", "")
                new_conn.Notes = rel.get("description", "")
                new_conn.Update()
                clog.log("created", rel["id"], f"{src['name']} -> {tgt['name']}", "Association", new_conn.ConnectorGUID)

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
                if conn.ClientID == src_elem.ElementID and conn.SupplierID == tgt_elem.ElementID:
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

        # UML Class boxes show an attribute compartment (unlike ArchiMate
        # elements, which are plain icon boxes) -- both height and width must
        # scale with each entity's own attributes, not a fixed size for all.
        def entity_size(ent):
            labels = [f"{a['name']}: {a['sparx_type']}" for a in ent["attributes"]]
            w = diagram_utils.compute_uml_class_width(ent["name"], labels)
            h = diagram_utils.compute_uml_class_height(len(ent["attributes"]))
            return (w, h)

        entity_sizes = {ent["id"]: entity_size(ent) for ent in entities}
        # Grid cell must be at least as large as the biggest entity in this
        # batch, or rows/columns would overlap.
        max_entity_width = max((w for w, _ in entity_sizes.values()), default=160)
        max_entity_height = max((h for _, h in entity_sizes.values()), default=70)

        if not diag:
            diag = dm_pkg.Diagrams.AddNew("EAxCRM Data Model", "Logical")
            diag.Update()
            dm_pkg.Update()
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)
            print("  Created diagram — placing all entities")

            eid_list = [ent["id"] for ent in entities]
            positions = diagram_utils.compute_grid_positions(eid_list,
                sizes=entity_sizes, per_row=8, cell_width=max_entity_width + 20,
                cell_height=max_entity_height + 20, h_gap=20, v_gap=20)
            count = diagram_utils.create_diagram_objects(diag, eid_list, object_ids, positions)
            print(f"  Placed {count} entities on diagram")
        else:
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)

            placed = diagram_utils.get_placed_ids(diag)
            new_ents = [ent for ent in entities if object_ids.get(ent["id"]) not in placed]
            if new_ents:
                new_ids = [ent["id"] for ent in new_ents]
                # Anchor new entities just below the diagram's actual current
                # content instead of a blind index continuation.
                _, max_bottom = diagram_utils.get_diagram_extent(diag)
                new_positions = diagram_utils.compute_grid_positions(new_ids,
                    sizes=entity_sizes, start_x=20, start_y=max_bottom + 40,
                    per_row=8, cell_width=max_entity_width + 20,
                    cell_height=max_entity_height + 20, h_gap=20, v_gap=20)
                added = diagram_utils.add_missing_elements(diag, new_ids, object_ids, new_positions)
                print(f"  Added {added} new entit(ies) to existing diagram")
            else:
                print("  Diagram already has all entities — preserving manual layout")

        styled = diagram_utils.set_diagram_link_style(diag, 8)  # Orthogonal Square
        if styled:
            print(f"  Set Orthogonal Square line style on {styled} connector(s)")

        clog.checkpoint("Diagram complete")
        clog.close()

    finally:
        spawned_pids = ea_session.get_ea_pids() - before_pids
        with ea_session.hang_guard(spawned_pids):
            try:
                repo.RefreshModelView(0)  # Full model tree refresh
                repo.RefreshOpenDiagrams(True)
            except Exception as e:
                print(f"  [refresh] RefreshModelView(0) failed: {e}")
            try:
                repo.CloseFile()
            except:
                pass
        killed = ea_session.kill_new_ea_processes(before_pids)
        if killed:
            print(f"  Cleaned up {len(killed)} zombie EA process(es)")

    print("\nDone. Open EAxCRM.qea in Sparx EA to view.")


if __name__ == "__main__":
    main()
