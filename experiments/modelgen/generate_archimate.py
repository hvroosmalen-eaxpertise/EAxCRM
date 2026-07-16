"""Generate ArchiMate model in EAxCRM.qea from Markdown model file.

Usage:
    python generate_archimate.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-Archimate.md]

Idempotent: stores a JSON mapping of MD-GUID -> EA-GUID after first run.
Re-run to update names, descriptions, or add new elements/relations.
"""
import sys, os, argparse, json, time
import diagram_utils
import ea_session
from changelog import ChangeLog

# stdout block-buffers when redirected/piped (e.g. to a log file), so nothing
# shows up until the buffer fills or the process exits. Force line buffering
# so progress is visible in real time if a COM call stalls.
sys.stdout.reconfigure(line_buffering=True)


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


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

# ArchiMate3 MDG diagram stereotypes (from MDGTechnologies/ArchiMate3.xml's
# <DiagramProfile> block) -- there are only 5, each single-layer, each
# applying to the native EA diagram Type "Logical" (NOT "Application Layer"
# -- that string is only the human-readable *alias* of the "Application"
# stereotype, not a real Diagram_Type value; using it directly as the Type
# silently created an unrecognized diagram type with no toolbox at all,
# github.com issue #5). "Application" is used here since that's what this
# diagram's (broken) Type string was already trying to say. There is no
# combined/multi-layer diagram stereotype in this MDG -- Business/Technology/
# Motivation/Implementation shapes remain reachable via the toolbox's "more
# tools" picker even though "Application" is the default page.
#
# NOTE: unlike the BPMN fix (verified against a diagram the user built
# correctly by hand in EA's GUI), this ArchiMate fix is applied BY ANALOGY
# only -- there is no user-verified ArchiMate reference diagram yet. The
# StyleEx tab caption still reads generic/lowercase after this fix, unlike
# BPMN's, which changed to a bold "Business Process" caption once fixed. If
# the toolbox still doesn't show, get a real reference the same way the BPMN
# one was obtained: have the user manually create + correctly type an
# ArchiMate diagram in EA's GUI, then read back its t_diagram.StyleEx.
DIAGRAM_NATIVE_TYPE = "Logical"
DIAGRAM_STYLEEX_MDGDGM = "ArchiMate3::Application"


def ensure_diagram_toolbox(diag, is_new, label=""):
    """Set an ArchiMate3 diagram Type/toolbox so EA shows the matching
    toolbox (github issue #5 -- an unrecognized Diagram_Type meant no
    ArchiMate toolbox ever showed by default, forcing manual selection).

    COM-only, no SQLite (2026-07-06 hard rule -- see ea-model-common skill;
    an earlier version of this function patched Diagram_Type/StyleEx via
    direct SQL, which is no longer allowed in shipped generate/sync code).

    - Diagram.Type: read-only once the diagram exists ("can not be set") --
      COM can only set it correctly at Diagrams.AddNew() time.
    - Diagram.StyleEx's "MDGDgm=<Technology>::<Name>;" key is the real
      toolbox selector (Stereotype/StereotypeEx do not drive it -- both
      ruled out empirically). It DOES persist via plain COM when the field
      starts empty, but COM silently refuses to overwrite an already-present
      MDGDgm value on an existing diagram.

    is_new=True: diagram was just created this run with the correct native
    Type already passed to AddNew() -- set Stereotype/StereotypeEx blank and
    StyleEx's MDGDgm token via COM; this persists since the field is empty.

    is_new=False: a pre-existing diagram found via GUID/name lookup -- COM
    can only *read* Type/StyleEx to check them, never correct them if
    wrong. Log a warning naming the diagram rather than attempting a fix --
    that needs a manual fix in EA's GUI or an explicit, user-approved
    recreate-the-diagram pass.
    """
    mdgdgm_token = f"MDGDgm={DIAGRAM_STYLEEX_MDGDGM};"
    if is_new:
        diag.Stereotype = ""
        diag.StereotypeEx = ""
        diag.StyleEx = mdgdgm_token
        diag.Update()
        return

    current_type = diag.Type
    current_style = diag.StyleEx or ""
    problems = []
    if current_type != DIAGRAM_NATIVE_TYPE:
        problems.append(f"Diagram_Type is {current_type!r}, expected {DIAGRAM_NATIVE_TYPE!r}")
    if mdgdgm_token not in current_style:
        problems.append(f"StyleEx is missing {mdgdgm_token!r}")
    if problems:
        print(f"  WARNING: '{label}' diagram toolbox may be wrong -- {'; '.join(problems)}. "
              f"COM can't correct an existing diagram's Type/StyleEx (see ea-model-common skill) -- "
              f"fix manually in EA's GUI, or ask to have this diagram recreated.")


# Base Connector_Type (t_connector.Connector_Type) for each ArchiMate
# relationship type. Aligned to ArchiMate 3 categories per the spec's
# Relationship Summary Table and the Sparx ArchiMate3 MDG:
#   Structural  -> Association (Composition/Aggregation/Assignment; the
#                  filled/open diamond is rendered by the MDG stereotype,
#                  NOT the UML base type) / Realisation
#   Dependency  -> Dependency (Serving/Access/Influence) / Association (the
#                  "unspecified" Association relation stays Association)
#   Dynamic     -> ControlFlow (both Triggering and Flow -- distinguished by
#                  stereotype, not by base type)
CONNECTOR_BASE_TYPE = {
    "Composition": "Association",
    "Aggregation": "Association",
    "Assignment": "Association",
    "Realization": "Realisation",
    "Association": "Association",
    "Triggering": "ControlFlow",
    "Flow": "ControlFlow",
    "Serving": "Dependency",
    "Access": "Dependency",
    "Influence": "Dependency",
}


def _rel_key(rel):
    """Key into guid_map for a relation. Prefer the MD GUID when populated;
    fall back to a prefixed rel-id so freshly-authored MDs (with placeholder
    ``GUID: {}``) still get idempotent tracking after their first successful
    run."""
    g = (rel.get("guid") or "").strip()
    if g and g != "{}":
        return g
    return "rel:" + rel["id"]


def _normalize_stereotype(s):
    """Normalize an EA StereotypeEx/Stereotype value to the short form. EA
    persists stereotypes as either ``Profile::Name`` or ``Name`` depending on
    how the connector was created; comparing without normalization silently
    duplicates connectors on re-run."""
    if not s:
        return ""
    return s.split("::")[-1]


def set_connector_tag(conn, prop, value):
    """Set a Tagged Value on ``conn`` (which MUST already have been
    ``Update()``d at least once so it has a real ``ConnectorID``).

    ``Connector.TaggedValues.AddNew(prop, value)`` called BEFORE the
    connector's first ``Update()`` lands the tag row in ``t_connectortag``
    with ``ElementID = 0`` -- orphaned, invisible to
    ``Connector.TaggedValues`` on subsequent reads, and impossible to look
    up by connector id later. Silent failure per issue #17 #6. This helper
    exists to keep call sites from doing that by accident.

    Idempotent: updates in place if a tag with ``prop`` already exists.
    """
    if not conn.ConnectorID:
        raise RuntimeError(
            "set_connector_tag called on a connector without a ConnectorID "
            "-- did you forget to call conn.Update() first? Tag would be "
            "orphaned with ElementID=0. (issue #17 #6)"
        )
    conn.TaggedValues.Refresh()
    for i in range(conn.TaggedValues.Count):
        tv = conn.TaggedValues.GetAt(i)
        if tv.Name == prop:
            if tv.Value != value:
                tv.Value = value
                tv.Update()
            return
    new_tv = conn.TaggedValues.AddNew(prop, value)
    new_tv.Update()
    conn.TaggedValues.Refresh()


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
                "direction": "",
                "access_mode": "",
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
                elif key == "Direction":
                    current["direction"] = value
                elif key == "AccessMode":
                    current["access_mode"] = value

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


def sync_elements(repo, pkg, elements, guid_map, clog):
    """Create or update elements. Uses md_guid -> ea_guid mapping for idempotency."""
    # Build name lookup from package elements (for idempotent fallback)
    pkg.Elements.Refresh()
    pkg_elems_by_name = {}
    for j in range(pkg.Elements.Count):
        e = pkg.Elements.GetAt(j)
        pkg_elems_by_name[e.Name] = e

    for idx, el in enumerate(elements):
        t0 = time.time()
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
            old_name = existing.Name
            old_notes = existing.Notes
            existing.Name = el["name"]
            existing.Notes = el["description"]
            existing.StereotypeEx = el["sparx_stereotype"]
            existing.Update()
            guid_map[md_guid] = existing.ElementGUID
            changes = {}
            if old_name != el["name"]:
                changes["Name"] = (old_name, el["name"])
            if old_notes != el["description"]:
                changes["Notes"] = (old_notes, el["description"])
            clog.log("updated", el["id"], el["name"], el["type"], existing.ElementGUID,
                     changes=(changes or None))
            log(f"  [{idx + 1}/{len(elements)}] Updated: '{el['name']}' ({el['type']}) [{time.time() - t0:.2f}s]")
        else:
            new_elem = pkg.Elements.AddNew(el["name"], base_type)
            new_elem.StereotypeEx = el["sparx_stereotype"]
            new_elem.Notes = el["description"]
            new_elem.Update()
            clog.log("created", el["id"], el["name"], el["type"], new_elem.ElementGUID)

            pkg.Elements.Refresh()
            for j in range(pkg.Elements.Count):
                e = pkg.Elements.GetAt(j)
                if e.ElementID == new_elem.ElementID:
                    guid_map[md_guid] = e.ElementGUID
                    pkg_elems_by_name[e.Name] = e
                    break

            log(f"  [{idx + 1}/{len(elements)}] Created: '{el['name']}' ({el['type']}) [{time.time() - t0:.2f}s]")


def sync_relations(repo, relations, elements, guid_map, clog):
    """Create or update connectors via COM API."""
    elem_by_id = {e["id"]: e for e in elements}

    for idx, rel in enumerate(relations):
        t0 = time.time()
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

        # Identity of an ArchiMate connector is
        # (ClientID, SupplierID, base_type, normalized_stereotype) -- multiple
        # connectors between the same pair are legal as long as they differ
        # in type/stereotype (e.g. a Serving alongside a Triggering). Github
        # issue #17.
        #
        # Tier 1: GUID-based lookup via archimate_guid_map.json. Authoritative
        # once we've created (or previously adopted) this rel -- doesn't
        # depend on ``src_elem.Connectors`` being fresh. Verify the resolved
        # connector still points at the expected pair, in case the underlying
        # connector was manually retargeted in EA.
        #
        # Tier 2: structural scan by the full 4-tuple, used only when Tier 1
        # misses (legacy connectors created before we stored GUIDs).
        # ``Connectors.Refresh()`` first so connectors added earlier in this
        # same run are visible; without it Sparx returns a stale snapshot and
        # silently duplicates on re-run.
        norm_stereo = _normalize_stereotype(full_stereo)
        rel_key = _rel_key(rel)

        conn = None
        stored_ea_guid = guid_map.get(rel_key)
        if stored_ea_guid:
            try:
                candidate = repo.GetConnectorByGuid(stored_ea_guid)
            except:
                candidate = None
            if (candidate
                    and candidate.ClientID == src_elem.ElementID
                    and candidate.SupplierID == tgt_elem.ElementID):
                conn = candidate

        if conn is None:
            src_elem.Connectors.Refresh()
            for i in range(src_elem.Connectors.Count):
                c = src_elem.Connectors.GetAt(i)
                if c.ClientID != src_elem.ElementID:
                    continue
                if c.SupplierID != tgt_elem.ElementID:
                    continue
                if c.Type != base_type:
                    continue
                c_stereo = _normalize_stereotype(c.StereotypeEx or c.Stereotype or "")
                if c_stereo != norm_stereo:
                    continue
                conn = c
                break

        # Direction: MD may override the default for Access/Flow/Triggering
        # per issue #17 #6. Fall back to "Source -> Destination" so behavior
        # for pre-#6 MD entries (no Direction field) is unchanged.
        md_direction = rel.get("direction") or "Source -> Destination"
        md_access_mode = rel.get("access_mode") or ""

        if conn is not None:
            guid_map[rel_key] = conn.ConnectorGUID
            # Update-path: apply MD Direction if it differs. TaggedValue
            # updates go through set_connector_tag (safe: connector already
            # has a ConnectorID here).
            if conn.Direction != md_direction:
                conn.Direction = md_direction
                conn.Update()
            if md_access_mode:
                set_connector_tag(conn, "AccessMode", md_access_mode)
            clog.log("updated", rel["id"], rel["type"], rel["type"], conn.ConnectorGUID)
            log(f"  [{idx + 1}/{len(relations)}] Exists rel: '{rel['id']}' ({rel['type']}) [{time.time() - t0:.2f}s]")
        else:
            new_conn = src_elem.Connectors.AddNew("", base_type)
            new_conn.SupplierID = tgt_elem.ElementID
            new_conn.StereotypeEx = full_stereo
            new_conn.Direction = md_direction
            new_conn.Update()
            # CRITICAL: AccessMode tag MUST be set AFTER Update() so the tag
            # binds to a real ConnectorID -- see set_connector_tag docstring
            # and issue #17 #6.
            if md_access_mode:
                set_connector_tag(new_conn, "AccessMode", md_access_mode)
            guid_map[rel_key] = new_conn.ConnectorGUID
            clog.log("created", rel["id"], rel["type"], rel["type"], new_conn.ConnectorGUID,
                     changes={"source": rel["source"], "target": rel["target"]})
            log(f"  [{idx + 1}/{len(relations)}] Created rel: '{rel['id']}' ({rel['type']}) [{time.time() - t0:.2f}s]")


def main():
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="Generate ArchiMate model in EAxCRM.qea")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    parser.add_argument("--state-dir", default=SCRIPT_DIR,
                         help="Directory for the changelog and GUID-map files (default: script dir). "
                              "Override in tests so runs against a sandboxed --qea don't touch the real ones.")
    args = parser.parse_args()

    global GUID_MAP_PATH
    GUID_MAP_PATH = os.path.join(args.state_dir, "archimate_guid_map.json")

    elements, relations = parse_md(args.md)
    print(f"Parsed {len(elements)} elements, {len(relations)} relationships")

    clog = ChangeLog(os.path.join(args.state_dir, "archimate_changelog.md"))
    clog.checkpoint("Parsed MD")

    guid_map = load_guid_map()
    print(f"Loaded {len(guid_map)} GUID mappings")

    try:
        import win32com.client
    except ImportError:
        print("FAIL: win32com not installed. Run: pip install pywin32")
        sys.exit(1)

    log("Opening EA session...")
    with ea_session.ea_repository(args.qea, technology="ArchiMate3") as repo:
        log("EA session open, resolving model root...")
        root = ea_session.get_model_root(repo)
        log("Model root resolved, locating Application Architecture package...")
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
        log("Package resolved.")

        # Phase 1: Elements
        log(f"--- Elements ({len(elements)}) ---")
        sync_elements(repo, eax_pkg, elements, guid_map, clog)
        save_guid_map(guid_map)
        log("--- Elements done ---")

        # Phase 2: Relationships
        log(f"--- Relationships ({len(relations)}) ---")
        sync_relations(repo, relations, elements, guid_map, clog)
        save_guid_map(guid_map)
        log("--- Relationships done ---")

        # Build object_ids: el["id"] -> numeric EA ElementID
        log("Resolving diagram object IDs...")
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

        log("--- Diagram ---")

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

        elem_types = {el["id"]: ELEMENT_BASE_TYPE.get(el["type"], "Class") for el in elements}

        is_new_diag = False
        if not diag:
            diag = eax_pkg.Diagrams.AddNew("EAxCRM ArchiMate", DIAGRAM_NATIVE_TYPE)
            diag.Update()
            eax_pkg.Update()
            is_new_diag = True
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)
            print("  Created diagram — element layout will be auto-generated")

            eid_list = [el["id"] for el in elements]
            positions = diagram_utils.compute_grid_positions(eid_list,
                elem_types=elem_types, type_sizes=diagram_utils.DEFAULT_ELEMENT_SIZES,
                per_row=8, cell_width=180, cell_height=100, h_gap=20, v_gap=20)
            count = diagram_utils.create_diagram_objects(diag, eid_list, object_ids, positions)
            print(f"  Placed {count} elements on diagram")
        else:
            guid_map[diag_guid_key] = diag.DiagramGUID
            save_guid_map(guid_map)

            placed = diagram_utils.get_placed_ids(diag)
            new_els = [el for el in elements if object_ids.get(el["id"]) not in placed]
            if new_els:
                new_ids = [el["id"] for el in new_els]
                # Anchor new elements just below the diagram's actual current
                # content (not a blind index continuation) so they land next
                # to the rest of the diagram instead of far away.
                _, max_bottom = diagram_utils.get_diagram_extent(diag)
                new_positions = diagram_utils.compute_grid_positions(new_ids,
                    elem_types=elem_types, type_sizes=diagram_utils.DEFAULT_ELEMENT_SIZES,
                    start_x=20, start_y=max_bottom + 40, per_row=8,
                    cell_width=180, cell_height=100, h_gap=20, v_gap=20)
                added = diagram_utils.add_missing_elements(diag, new_ids, object_ids, new_positions)
                print(f"  Added {added} new element(s) to existing diagram")
            else:
                print("  Diagram already has all elements — preserving manual layout")

        ensure_diagram_toolbox(diag, is_new_diag, label="EAxCRM ArchiMate")
        print(f"  Diagram toolbox: {DIAGRAM_STYLEEX_MDGDGM}")

    clog.checkpoint("Diagram complete")
    clog.close()

    print("\nDone. Open EAxCRM.qea in Sparx EA to view.")


if __name__ == "__main__":
    main()
