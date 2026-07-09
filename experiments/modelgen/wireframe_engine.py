"""Shared wireframe engine: parse_md, generate(), sync_to_md() -- mirrors
bpmn_engine.py's split, but for EA Wireframe diagrams. Unlike BPMN/ArchiMate/
Data Model, a wireframe's positions ARE its content (explicit per-control
bounds authored in the MD, no flow-layout algorithm), and each Screen gets
its own diagram (as the Screen element's own child diagram, double-click-
able like BPMN's CollaborationModel) plus one shared sitemap overview.
"""
import json
import os
import re

import diagram_utils
import ea_session
from changelog import ChangeLog, compute_md_diff
from wireframe_config import (
    CONTROL_TYPE_TO_STEREO,
    DIAGRAM_NATIVE_TYPE,
    DIAGRAM_STYLEEX_EXTRA,
    DIAGRAM_STYLEEX_MDGDGM,
    NAVIGATION_CONNECTOR_TYPE,
    SCREEN_BASE_TYPE,
    SCREEN_STEREOTYPE,
    WIREFRAME_TAGGED_VALUES,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# parse_md(): MD -> in-memory structures
# ---------------------------------------------------------------------------

def parse_bounds(text):
    """'20, 60, 300, 24' -> (x, y, w, h) ints."""
    parts = [p.strip() for p in text.split(",")]
    x, y, w, h = (int(float(p)) for p in parts)
    return x, y, w, h


def parse_md(md_path):
    with open(md_path, encoding="utf-8") as f:
        lines = f.readlines()

    flow_fields = {}
    screens = {}
    controls = {}
    navigation = []

    section = None
    current = None
    current_kind = None
    current_eid = None

    def flush():
        if current_kind == "screen" and current_eid:
            screens[current_eid] = current
        elif current_kind == "control" and current_eid:
            controls[current_eid] = current

    for raw in lines:
        stripped = raw.rstrip("\n").strip()

        m_flow = re.match(r"^##\s+Flow[—-]+(\S+)", stripped)
        m_screen = re.match(r"^###\s+Screen[—-]+(\S+)", stripped)
        m_control = re.match(r"^####\s+Control[—-]+(\S+)", stripped)

        if m_flow:
            flush()
            section, current, current_kind, current_eid = "flow", flow_fields, "flow", None
            continue
        if m_screen:
            flush()
            section, current, current_kind, current_eid = "screen", {}, "screen", m_screen.group(1)
            continue
        if m_control:
            flush()
            section, current, current_kind, current_eid = "control", {}, "control", m_control.group(1)
            continue
        if stripped == "## Navigation":
            flush()
            section, current, current_kind, current_eid = "navigation", None, None, None
            continue

        if section == "navigation":
            m_nav = re.match(r"^-\s*(\S+)\s*(?:->|→)\s*(\S+)\s*(?:\[(.+?)\])?\s*$", stripped)
            if m_nav:
                navigation.append({
                    "source": m_nav.group(1),
                    "target": m_nav.group(2),
                    "trigger": (m_nav.group(3) or "").strip(),
                })
            continue

        if current is not None and stripped.startswith("- "):
            kv = stripped[2:]
            if ": " in kv:
                key, value = kv.split(": ", 1)
                current[key.strip()] = value.strip()

    flush()
    return flow_fields, screens, controls, navigation


# ---------------------------------------------------------------------------
# Tagged values
# ---------------------------------------------------------------------------

def set_tagged_values(elem, control_type, fields):
    """Set only the tagged values allow-listed for this control type (see
    WIREFRAME_TAGGED_VALUES) -- idempotent: updates an existing TaggedValue
    in place rather than adding a duplicate on re-run.
    """
    allowed = WIREFRAME_TAGGED_VALUES.get(control_type, set())
    if not allowed:
        return
    elem.TaggedValues.Refresh()
    existing = {}
    for i in range(elem.TaggedValues.Count):
        tv = elem.TaggedValues.GetAt(i)
        existing[tv.Name] = tv
    for key, value in fields.items():
        if key not in allowed or not value:
            continue
        if key in existing:
            if existing[key].Value != value:
                existing[key].Value = value
                existing[key].Update()
        else:
            tv = elem.TaggedValues.AddNew(key, value)
            tv.Update()


# ---------------------------------------------------------------------------
# Diagram Type/Toolbox (see issue #5's StyleEx/MDGDgm mechanism)
# ---------------------------------------------------------------------------

def ensure_diagram_toolbox(diag, is_new, label=""):
    """COM-only toolbox fix -- no SQLite, ever, per the 2026-07-06 hard rule
    (see ea-model-common skill). Diagram.Type is read-only via COM once a
    diagram already exists, and Diagram.StyleEx's MDGDgm key (the real
    toolbox selector, not Stereotype/StereotypeEx) won't be overwritten by
    COM once already non-empty -- so the only thing COM can reliably do is
    set both correctly at diagram-creation time, before anything else
    touches them.

    is_new=True (diagram just created this run via Diagrams.AddNew, native
    Type already passed in): set Stereotype/StereotypeEx blank and StyleEx's
    MDGDgm token via plain COM -- this persists, since the field starts
    empty.

    is_new=False (a pre-existing diagram found via GUID/name lookup): COM
    can only *read* Type/StyleEx to check them, never correct them if
    wrong. Log a warning naming the diagram rather than attempting a fix --
    correcting an already-wrong existing diagram needs either a manual fix
    in EA's GUI or an explicit, user-approved recreate-the-diagram pass.
    """
    mdgdgm_token = f"MDGDgm={DIAGRAM_STYLEEX_MDGDGM};"
    if is_new:
        diag.Stereotype = ""
        diag.StereotypeEx = ""
        diag.StyleEx = mdgdgm_token + DIAGRAM_STYLEEX_EXTRA
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


def _get_or_create_package(parent, name):
    for i in range(parent.Packages.Count):
        p = parent.Packages.GetAt(i)
        if p.Name == name:
            return p
    pkg = parent.Packages.AddNew(name, "Package")
    pkg.Update()
    parent.Update()
    return pkg


# ---------------------------------------------------------------------------
# generate(): MD -> EA
# ---------------------------------------------------------------------------

def generate(config, qea_path=None, md_path=None):
    qea_path = qea_path or config.default_qea
    md_path = md_path or config.default_md
    guid_map_file = os.path.join(SCRIPT_DIR, config.guid_map_file)

    flow_fields, screens, controls, navigation = parse_md(md_path)
    print(f"Parsed {len(screens)} screen(s), {len(controls)} control(s), "
          f"{len(navigation)} navigation link(s)")

    guid_map = {}
    if os.path.exists(guid_map_file):
        with open(guid_map_file) as f:
            guid_map = json.load(f)
    elem_guid_map = guid_map.get("elements", {})
    diag_guid_map = guid_map.get("diagrams", {})

    clog = None
    if config.changelog_file:
        clog = ChangeLog(config.changelog_file)
        clog.checkpoint("Parsed MD", run_id=config.model_id)

    with ea_session.ea_repository(qea_path, technology="Wireframing") as repo:
        root = ea_session.get_model_root(repo)
        ui_pkg = _get_or_create_package(root, config.parent_package_name)
        flow_pkg = _get_or_create_package(ui_pkg, config.package_name)
        flow_pkg.Elements.Refresh()

        pkg_elems_by_name = {}
        for i in range(flow_pkg.Elements.Count):
            e = flow_pkg.Elements.GetAt(i)
            pkg_elems_by_name[e.Name] = e

        object_ids = {}          # eid (screen or control) -> ElementID
        screen_object_ids = {}   # screen eid -> ElementID

        # --- Pass 1: Screens ---
        for eid, data in screens.items():
            name = data.get("Name", eid)
            desc = data.get("Description", "")
            ea_guid = elem_guid_map.get(eid)
            existing = None
            if ea_guid:
                try:
                    existing = repo.GetElementByGuid(ea_guid)
                except Exception:
                    existing = None
            if not existing:
                existing = pkg_elems_by_name.get(name)

            if existing:
                old_name, old_notes = existing.Name, existing.Notes
                existing.Name = name
                existing.Notes = desc
                existing.StereotypeEx = f"Wireframing::{SCREEN_STEREOTYPE}"
                existing.Update()
                changes = {}
                if old_name != name:
                    changes["Name"] = (old_name, name)
                if old_notes != desc:
                    changes["Notes"] = (old_notes, desc)
                if clog:
                    clog.log("updated", eid, name, "Screen", existing.ElementGUID, changes=(changes or None))
                elem_guid_map[eid] = existing.ElementGUID
                object_ids[eid] = existing.ElementID
                screen_object_ids[eid] = existing.ElementID
            else:
                new_elem = flow_pkg.Elements.AddNew(name, SCREEN_BASE_TYPE)
                new_elem.StereotypeEx = f"Wireframing::{SCREEN_STEREOTYPE}"
                new_elem.Notes = desc
                new_elem.Update()
                if clog:
                    clog.log("created", eid, name, "Screen", new_elem.ElementGUID)
                elem_guid_map[eid] = new_elem.ElementGUID
                object_ids[eid] = new_elem.ElementID
                screen_object_ids[eid] = new_elem.ElementID

        flow_pkg.Elements.Refresh()

        # --- Lint: warn on Buttons with no Description ---
        # A wireframe Button's Description is its onclick contract — what it
        # does, what it navigates to, which fields it writes. Missing one is
        # a real documentation gap (not a hard error) since the Notes pane
        # is where staff look for behavioural intent. Non-fatal — sync
        # continues regardless. See ea-wireframe-creator skill.
        buttons_missing_desc = []
        for eid, data in controls.items():
            if data.get("Type", "") == "Button" and not data.get("Description", "").strip():
                buttons_missing_desc.append((eid, data.get("Name", eid), data.get("Screen", "?")))
        for _eid, bname, bscreen in buttons_missing_desc:
            print(f"  [lint] Button '{bname}' on screen '{bscreen}' has no Description "
                  f"— add one so its click contract is documented in EA.")
        if buttons_missing_desc:
            print(f"  [lint] Wireframe lint: {len(buttons_missing_desc)} Button(s) missing Description.")

        # --- Pass 2: Controls (parented under their Screen, or -- via an
        # optional "- Parent:" field -- under another already-created
        # Control, e.g. a nested Frame/browser-chrome element containing
        # further Controls). Multi-pass resolution so MD declaration order
        # doesn't matter: keep sweeping the remaining controls until no more
        # progress can be made, rather than assuming a fixed one-level
        # Screen->Control hierarchy (found in the wild 2026-07-06 when the
        # user nested a Frame inside a Screen by hand in EA's GUI).
        remaining = dict(controls)
        made_progress = True
        while remaining and made_progress:
            made_progress = False
            for eid in list(remaining.keys()):
                data = remaining[eid]
                name = data.get("Name", eid)
                ctype = data.get("Type", "")
                screen_eid = data.get("Screen", "")
                parent_ref = data.get("Parent") or screen_eid
                desc = data.get("Description", "")
                stereo_info = CONTROL_TYPE_TO_STEREO.get(ctype)
                if not stereo_info:
                    print(f"  SKIP control '{eid}': unknown Type '{ctype}'")
                    del remaining[eid]
                    continue
                parent_oid = object_ids.get(parent_ref)
                if parent_oid is None:
                    continue  # parent not created yet -- retry next sweep

                stereo_name, base_type = stereo_info
                ea_guid = elem_guid_map.get(eid)
                existing = None
                if ea_guid:
                    try:
                        existing = repo.GetElementByGuid(ea_guid)
                    except Exception:
                        existing = None

                # Defense in depth: fall back to a name match among the
                # resolved parent's own children (mirrors Pass 1's screen
                # lookup) before creating a new element. Guards against
                # duplicating a control the guid map doesn't (yet) track --
                # e.g. anything added directly in EA's GUI between syncs --
                # even though sync_to_md now persists newly-discovered
                # GUIDs immediately, closing the main way this happened.
                if not existing:
                    try:
                        parent_elem = repo.GetElementByID(parent_oid)
                        parent_elem.Elements.Refresh()
                        for k in range(parent_elem.Elements.Count):
                            sib = parent_elem.Elements.GetAt(k)
                            if sib.Name == name:
                                existing = sib
                                break
                    except Exception:
                        pass

                if existing:
                    old_name, old_notes = existing.Name, existing.Notes
                    existing.Name = name
                    existing.Notes = desc
                    existing.StereotypeEx = f"Wireframing::{stereo_name}"
                    existing.ParentID = parent_oid
                    existing.Update()
                    set_tagged_values(existing, ctype, data)
                    changes = {}
                    if old_name != name:
                        changes["Name"] = (old_name, name)
                    if old_notes != desc:
                        changes["Notes"] = (old_notes, desc)
                    if clog:
                        clog.log("updated", eid, name, ctype, existing.ElementGUID, changes=(changes or None))
                    elem_guid_map[eid] = existing.ElementGUID
                    object_ids[eid] = existing.ElementID
                else:
                    new_elem = flow_pkg.Elements.AddNew(name, base_type)
                    new_elem.StereotypeEx = f"Wireframing::{stereo_name}"
                    new_elem.Notes = desc
                    new_elem.ParentID = parent_oid
                    new_elem.Update()
                    set_tagged_values(new_elem, ctype, data)
                    if clog:
                        clog.log("created", eid, name, ctype, new_elem.ElementGUID)
                    elem_guid_map[eid] = new_elem.ElementGUID
                    object_ids[eid] = new_elem.ElementID

                del remaining[eid]
                made_progress = True

        for eid, data in remaining.items():
            print(f"  SKIP control '{eid}': parent '{data.get('Parent') or data.get('Screen')}' never resolved (unknown reference or dependency cycle)")

        guid_map["elements"] = elem_guid_map
        with open(guid_map_file, "w") as f:
            json.dump(guid_map, f, indent=2)

        # --- Pass 3: Navigation connectors (labeled Association, Screen -> Screen) ---
        for nav in navigation:
            src_oid = screen_object_ids.get(nav["source"])
            tgt_oid = screen_object_ids.get(nav["target"])
            if src_oid is None or tgt_oid is None:
                print(f"  SKIP navigation '{nav['source']} -> {nav['target']}': unknown screen")
                continue
            src_elem = repo.GetElementByID(src_oid)
            tgt_elem = repo.GetElementByID(tgt_oid)
            src_elem.Connectors.Refresh()
            exists = False
            for i in range(src_elem.Connectors.Count):
                c = src_elem.Connectors.GetAt(i)
                if c.ClientID == src_elem.ElementID and c.SupplierID == tgt_elem.ElementID:
                    exists = True
                    if c.Name != nav["trigger"]:
                        c.Name = nav["trigger"]
                        c.Update()
                    break
            if not exists:
                new_conn = src_elem.Connectors.AddNew("", NAVIGATION_CONNECTOR_TYPE)
                new_conn.SupplierID = tgt_elem.ElementID
                new_conn.Name = nav["trigger"]
                new_conn.Direction = "Source -> Destination"
                new_conn.Update()
                if clog:
                    clog.log("created", "", f"{src_elem.Name} -> {tgt_elem.Name}", "Navigation",
                              new_conn.ConnectorGUID, changes={"trigger": nav["trigger"]})

        # --- Pass 4: One diagram per screen, explicit bounds ---
        for eid in screens:
            oid = screen_object_ids.get(eid)
            if oid is None:
                continue
            elem = repo.GetElementByID(oid)
            data = screens[eid]
            diag_name = data.get("Diagram Name", data.get("Name", eid))

            diag = None
            is_new_diag = False
            existing_diag_guid = diag_guid_map.get(eid)
            if existing_diag_guid:
                try:
                    diag = repo.GetDiagramByGuid(existing_diag_guid)
                except Exception:
                    diag = None
            if not diag:
                elem.Diagrams.Refresh()
                for i in range(elem.Diagrams.Count):
                    d = elem.Diagrams.GetAt(i)
                    if d.Name == diag_name:
                        diag = d
                        break
            if not diag:
                diag = elem.Diagrams.AddNew(diag_name, DIAGRAM_NATIVE_TYPE)
                diag.Update()
                elem.Update()
                is_new_diag = True
                print(f"  Created diagram '{diag_name}'")
            diag_guid_map[eid] = diag.DiagramGUID

            screen_control_ids = [ceid for ceid, cdata in controls.items() if cdata.get("Screen") == eid]
            positions = {}
            for ceid in screen_control_ids:
                bounds = controls[ceid].get("Bounds", "")
                if not bounds:
                    continue
                x, y, w, h = parse_bounds(bounds)
                positions[ceid] = (x, y, x + w, y + h)

            placed = diagram_utils.get_placed_ids(diag)
            new_ids = [ceid for ceid in screen_control_ids if object_ids.get(ceid) not in placed]
            if new_ids:
                added = diagram_utils.add_missing_elements(diag, new_ids, object_ids, positions)
                print(f"    Added {added} control(s) to '{diag_name}'")

            # A wireframe's positions ARE its content -- unlike BPMN/
            # ArchiMate (add-only, preserve manual layout), re-running
            # should push MD bounds changes through for already-placed
            # controls too, not just add new ones.
            oid_to_ceid = {object_ids[ceid]: ceid for ceid in screen_control_ids if ceid in object_ids}
            diag.DiagramObjects.Refresh()
            for i in range(diag.DiagramObjects.Count):
                dobj = diag.DiagramObjects.GetAt(i)
                ceid = oid_to_ceid.get(dobj.ElementID)
                if ceid is None or ceid not in positions:
                    continue
                l, vt, r, vb = positions[ceid]
                current_bounds = (int(dobj.left), int(-dobj.top), int(dobj.right), int(-dobj.bottom))
                new_bounds = (int(l), int(vt), int(r), int(vb))
                if current_bounds != new_bounds:
                    dobj.left, dobj.top = new_bounds[0], -new_bounds[1]
                    dobj.right, dobj.bottom = new_bounds[2], -new_bounds[3]
                    dobj.Update()

            ensure_diagram_toolbox(diag, is_new_diag, label=diag_name)

        # --- Pass 5: Sitemap diagram (all screens + navigation, overview) ---
        sitemap_name = config.sitemap_diagram_name
        sitemap = None
        is_new_sitemap = False
        sitemap_guid = diag_guid_map.get(config.diag_guid_key_sitemap)
        if sitemap_guid:
            try:
                sitemap = repo.GetDiagramByGuid(sitemap_guid)
            except Exception:
                sitemap = None
        if not sitemap:
            flow_pkg.Diagrams.Refresh()
            for i in range(flow_pkg.Diagrams.Count):
                d = flow_pkg.Diagrams.GetAt(i)
                if d.Name == sitemap_name:
                    sitemap = d
                    break
        if not sitemap:
            sitemap = flow_pkg.Diagrams.AddNew(sitemap_name, DIAGRAM_NATIVE_TYPE)
            sitemap.Update()
            flow_pkg.Update()
            is_new_sitemap = True
            print(f"  Created sitemap diagram '{sitemap_name}'")
        diag_guid_map[config.diag_guid_key_sitemap] = sitemap.DiagramGUID

        screen_ids_list = list(screens.keys())
        placed = diagram_utils.get_placed_ids(sitemap)
        new_screen_ids = [eid for eid in screen_ids_list if object_ids.get(eid) not in placed]
        if new_screen_ids:
            positions = diagram_utils.compute_grid_positions(
                new_screen_ids, per_row=4, cell_width=180, cell_height=100, h_gap=40, v_gap=60)
            added = diagram_utils.add_missing_elements(sitemap, new_screen_ids, object_ids, positions)
            print(f"  Added {added} screen(s) to sitemap")

        ensure_diagram_toolbox(sitemap, is_new_sitemap, label=sitemap_name)

        guid_map["diagrams"] = diag_guid_map
        with open(guid_map_file, "w") as f:
            json.dump(guid_map, f, indent=2)

        if clog:
            clog.checkpoint("Diagram complete", run_id=config.model_id)
            clog.close()

    print("Done.")


# ---------------------------------------------------------------------------
# sync_to_md(): EA -> MD
# ---------------------------------------------------------------------------

def _render_md(config, screens, controls, navigation):
    lines = [
        f"# EAxCRM — {config.header_name}",
        "",
        f"**Model ID**: {config.model_id}",
        f"**Purpose**: {config.purpose}",
        "",
        f"## Flow—{config.flow_id}",
        f"- Name: {config.name}",
        f"- Sitemap Diagram Name: {config.sitemap_diagram_name}",
        "",
    ]

    controls_by_screen = {}
    for ceid, cdata in controls.items():
        controls_by_screen.setdefault(cdata.get("screen", ""), []).append((ceid, cdata))

    for eid, sdata in screens.items():
        lines.append(f"### Screen—{eid}")
        lines.append(f"- Name: {sdata['name']}")
        lines.append("- Type: Screen")
        lines.append(f"- Stereotype: {SCREEN_STEREOTYPE}")
        lines.append(f"- GUID: {sdata['guid']}")
        if sdata.get("diagram_name"):
            lines.append(f"- Diagram Name: {sdata['diagram_name']}")
        if sdata.get("diagram_guid"):
            lines.append(f"- Diagram GUID: {sdata['diagram_guid']}")
        if sdata.get("description"):
            lines.append(f"- Description: {sdata['description']}")
        lines.append("")

        control_structural_keys = {"name", "guid", "type", "description", "parent_id", "screen", "bounds", "parent"}
        for ceid, cdata in controls_by_screen.get(eid, []):
            lines.append(f"#### Control—{ceid}")
            lines.append(f"- Name: {cdata['name']}")
            lines.append(f"- Type: {cdata['type']}")
            lines.append(f"- Screen: {eid}")
            if cdata.get("parent"):
                # Direct parent is another Control (e.g. a nested Frame),
                # not the Screen itself -- omitted in the common case where
                # a control's direct parent IS its Screen.
                lines.append(f"- Parent: {cdata['parent']}")
            if cdata.get("bounds"):
                lines.append(f"- Bounds: {cdata['bounds']}")
            if cdata.get("description"):
                lines.append(f"- Description: {cdata['description']}")
            # Tagged values (State, Items, Enabled, ...) -- anything read
            # back that isn't one of the structural fields above.
            for key, value in cdata.items():
                if key not in control_structural_keys:
                    lines.append(f"- {key}: {value}")
            lines.append(f"- GUID: {cdata['guid']}")
            lines.append("")

    lines.append("## Navigation")
    lines.append("")
    for nav in navigation:
        trigger = f" [{nav['trigger']}]" if nav.get("trigger") else ""
        lines.append(f"- {nav['source']} → {nav['target']}{trigger}")
    lines.append("")

    return "\n".join(lines) + "\n"


def sync_to_md(config, qea_path=None, md_path=None):
    qea_path = qea_path or config.default_qea
    md_path = md_path or config.default_md
    guid_map_file = os.path.join(SCRIPT_DIR, config.guid_map_file)

    guid_map = {}
    if os.path.exists(guid_map_file):
        with open(guid_map_file) as f:
            guid_map = json.load(f)
    elem_guid_map = guid_map.get("elements", {})
    diag_guid_map = guid_map.get("diagrams", {})
    reverse_elem = {v: k for k, v in elem_guid_map.items()}

    control_stereo_lookup = {s: t for t, (s, _) in CONTROL_TYPE_TO_STEREO.items()}

    with ea_session.ea_repository(qea_path, technology="Wireframing") as repo:
        root = ea_session.get_model_root(repo)
        ui_pkg = None
        for i in range(root.Packages.Count):
            p = root.Packages.GetAt(i)
            if p.Name == config.parent_package_name:
                ui_pkg = p
                break
        if not ui_pkg:
            raise RuntimeError(f"'{config.parent_package_name}' package not found under Model")
        flow_pkg = None
        for i in range(ui_pkg.Packages.Count):
            p = ui_pkg.Packages.GetAt(i)
            if p.Name == config.package_name:
                flow_pkg = p
                break
        if not flow_pkg:
            raise RuntimeError(f"'{config.package_name}' package not found under {config.parent_package_name}")

        flow_pkg.Elements.Refresh()
        screens, controls, screen_by_oid, control_elems = {}, {}, {}, {}

        # Only top-level Screens appear in flow_pkg.Elements -- Controls have
        # ParentID set to their Screen (or another Control -- see
        # walk_controls below), so (same containment gotcha as BPMN Lane
        # children -- see "Refresh() Stale-Proxy Bug" in the skill) they
        # disappear from the package's own flat Elements collection entirely
        # and only show up under their parent's own child .Elements
        # collection, to arbitrary depth.
        screen_elems = []
        for i in range(flow_pkg.Elements.Count):
            elem = flow_pkg.Elements.GetAt(i)
            stereo = (elem.StereotypeEx or elem.Stereotype or "").split("::")[-1]
            if elem.Type == SCREEN_BASE_TYPE or stereo == SCREEN_STEREOTYPE:
                screen_elems.append(elem)

        # Controls can themselves have children nested under them -- e.g. a
        # "Frame" (nested browser-chrome Screen/WireframeWebsite element,
        # found in the wild 2026-07-06) containing further Controls. Walk
        # to arbitrary depth rather than assuming a fixed one-level
        # Screen->Control hierarchy, or nested content silently disappears
        # from the sync the same way a flat one-level scan silently missed
        # every Control the first time.
        def walk_controls(parent_elem, parent_eid, screen_eid):
            parent_elem.Elements.Refresh()
            for j in range(parent_elem.Elements.Count):
                celem = parent_elem.Elements.GetAt(j)
                cstereo = (celem.StereotypeEx or celem.Stereotype or "").split("::")[-1]
                ceid = reverse_elem.get(celem.ElementGUID, celem.Name.replace(" ", ""))
                ctype = control_stereo_lookup.get(cstereo, cstereo)
                cdata = {
                    "name": celem.Name, "guid": celem.ElementGUID,
                    "type": ctype,
                    "description": celem.Notes or "", "parent_id": celem.ParentID,
                    "screen": screen_eid,
                }
                if parent_eid != screen_eid:
                    cdata["parent"] = parent_eid
                allowed_tags = WIREFRAME_TAGGED_VALUES.get(ctype, set())
                if allowed_tags:
                    celem.TaggedValues.Refresh()
                    for k in range(celem.TaggedValues.Count):
                        tv = celem.TaggedValues.GetAt(k)
                        if tv.Name in allowed_tags and tv.Value:
                            cdata[tv.Name] = tv.Value
                controls[ceid] = cdata
                control_elems[celem.ElementID] = ceid
                walk_controls(celem, ceid, screen_eid)

        for elem in screen_elems:
            eid = reverse_elem.get(elem.ElementGUID, elem.Name.replace(" ", ""))
            diag_guid = diag_guid_map.get(eid, "")
            diag_name = ""
            if diag_guid:
                try:
                    diag_name = repo.GetDiagramByGuid(diag_guid).Name
                except Exception:
                    pass
            screens[eid] = {
                "name": elem.Name, "guid": elem.ElementGUID,
                "description": elem.Notes or "",
                "diagram_name": diag_name, "diagram_guid": diag_guid,
            }
            screen_by_oid[elem.ElementID] = eid
            walk_controls(elem, eid, eid)

        # Bounds: read from each screen's own diagram
        for screen_eid, sdata in screens.items():
            if not sdata["diagram_guid"]:
                continue
            try:
                diag = repo.GetDiagramByGuid(sdata["diagram_guid"])
            except Exception:
                continue
            diag.DiagramObjects.Refresh()
            for i in range(diag.DiagramObjects.Count):
                dobj = diag.DiagramObjects.GetAt(i)
                ceid = control_elems.get(dobj.ElementID)
                if not ceid:
                    continue
                x = int(dobj.left)
                y = int(-dobj.top)
                w = int(dobj.right) - x
                h = int(-dobj.bottom) - y
                controls[ceid]["bounds"] = f"{x}, {y}, {w}, {h}"

        # Navigation: connectors between Screen elements
        navigation = []
        seen_conn_ids = set()
        for screen_eid, sdata in screens.items():
            elem = repo.GetElementByGuid(sdata["guid"])
            elem.Connectors.Refresh()
            for i in range(elem.Connectors.Count):
                c = elem.Connectors.GetAt(i)
                if c.ConnectorID in seen_conn_ids or c.ClientID != elem.ElementID:
                    continue
                tgt_eid = screen_by_oid.get(c.SupplierID)
                if tgt_eid:
                    navigation.append({"source": screen_eid, "target": tgt_eid, "trigger": c.Name or ""})
                    seen_conn_ids.add(c.ConnectorID)

        # Persist any newly-discovered element GUIDs back into the guid map.
        # Without this, an element found only via reverse_elem's name-derived
        # fallback (anything the user created directly in EA's GUI, not
        # through generate()) is untracked on the next generate() run --
        # Pass 2's control creation has no name-based fallback (unlike
        # Pass 1's screens), so it silently creates a brand-new DUPLICATE
        # element instead of recognizing the existing one. Found the hard
        # way 2026-07-06: a user-added Frame + Cancel button synced fine but
        # got duplicated on the very next generate(), leaving the originals
        # orphaned with stale positions once bounds were later changed.
        for eid, sdata in screens.items():
            elem_guid_map[eid] = sdata["guid"]
        for eid, cdata in controls.items():
            elem_guid_map[eid] = cdata["guid"]
        guid_map["elements"] = elem_guid_map
        with open(guid_map_file, "w") as f:
            json.dump(guid_map, f, indent=2)

        new_content = _render_md(config, screens, controls, navigation)

    old_content = ""
    if os.path.exists(md_path):
        with open(md_path, encoding="utf-8") as f:
            old_content = f.read()

    diff = compute_md_diff(old_content, new_content)
    if config.changelog_file:
        clog = ChangeLog(config.changelog_file)
        clog.checkpoint("Sync from EA", run_id=config.model_id)
        clog.log_diff(diff, run_id=config.model_id)
        clog.close()

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Written {new_content.count(chr(10))} lines to {md_path}")
