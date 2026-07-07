"""Shared diagram layout utilities for EA COM API generators."""

# Type-appropriate dimensions for BPMN elements (width, height in pixels).
# EA renders each BPMN type as its native visual shape within these bounds.
# These match the Sales Process diagram's convention: right/bottom are always
# set on diagram objects (EA does not auto-size via COM API).
BPMN_ELEMENT_SIZES = {
    "Activity": (110, 60),
    "Task": (110, 60),
    "StartEvent": (30, 30),
    "EndEvent": (30, 30),
    "IntermediateEvent": (30, 30),
    "Gateway": (42, 42),
    "Decision": (42, 42),
    "ExclusiveGateway": (42, 42),
    "ParallelGateway": (42, 42),
    "InclusiveGateway": (42, 42),
    "ComplexGateway": (42, 42),
    "EventBasedGateway": (42, 42),
    "DataObject": (35, 50),
    "DataStore": (35, 50),
    "TextAnnotation": (80, 50),
    "Artifact": (35, 50),
}

# Type-appropriate default box sizes for non-BPMN diagrams (ArchiMate, UML
# data model, Requirements), keyed by Sparx EA base Object_Type (see
# ELEMENT_BASE_TYPE in generate_archimate.py).
#
# CONFIRMED (2026-07-02): EA's COM API does NOT auto-size a DiagramObject --
# leaving right/bottom unset produces a permanent 0x0 invisible object. This
# holds regardless of the diagram's Type/Stereotype/StereotypeEx -- verified
# against a diagram the user built by hand in EA's GUI ("EAxCRM Test", Type
# actually 'Logical', Stereotype/StereotypeEx both empty) where a manually
# drag-and-dropped ApplicationComponent still got a real size (90x70). Auto-
# sizing is triggered by EA's interactive drag-and-drop UI action, a
# different code path that DiagramObjects.AddNew()+Update() never runs.
# Explicit, type-appropriate bounds are required for every non-BPMN element
# placed via COM. "Class" and "Component" below are EA's actual observed
# native defaults (BusinessActor1/BusinessObject1/ApplicationComponent1,
# dragged fresh from the ArchiMate3 toolbox and left unresized -- all came
# back 90x70, suggesting this EA installation's native default is uniformly
# 90x70 regardless of ArchiMate stereotype). Activity/Interface/Node/Device/
# Requirement are not yet confirmed -- default to the same 90x70 until
# verified otherwise.
DEFAULT_ELEMENT_SIZES = {
    "Class": (90, 70),
    "Activity": (90, 70),
    "Component": (90, 70),
    "Interface": (90, 70),
    "Node": (90, 70),
    "Device": (90, 70),
    "Requirement": (90, 70),
}
DEFAULT_ELEMENT_SIZE = (90, 70)

# EA DiagramObject coordinate conventions:
#   - Origin (0,0) at top-left corner of the diagram
#   - left, right: standard X (left < right, increases rightward)
#   - top, bottom: Y values are ALWAYS negative below origin
#     Moving downward from {0,0} goes to {0, -100}, {0, -200}, etc.
#     So top > bottom (closer to zero = higher on page), e.g. Top=-30, Bottom=-200
#     Height = |top - bottom|
# Position tuples returned by layout functions use screen convention:
#   (left, visual_top, right, visual_bottom) with visual_top < visual_bottom (positive Y down)
# These are NEGATED at COM API assignment time for EA's negative-Y convention.


def compute_bpmn_lane_positions(lanes, lane_height=500, lane_width=1000, gap=250):
    positions = {}
    y = 30
    for lane in lanes:
        lid = lane.get("id")
        positions[lid] = (0, y, lane_width, y + lane_height)
        y += lane_height + gap
    return positions


def compute_bpmn_element_positions(elements_by_lane, lane_bounds,
                                    elem_width=180, elem_height=70,
                                    h_gap=30, v_gap=30,
                                    elem_types=None):
    positions = {}
    for lane_id, eids in elements_by_lane.items():
        bounds = lane_bounds.get(lane_id, (0, 0, 1000, 500))
        lane_left = bounds[0] + 20
        lane_top = bounds[1] + 40
        lane_right = bounds[2] - 20
        cell_w = elem_width + h_gap
        per_row = max(1, int((lane_right - lane_left) / cell_w))
        for idx, eid in enumerate(eids):
            col = idx % per_row
            row = idx // per_row
            if elem_types:
                t = elem_types.get(eid, "Activity")
                ew, eh = BPMN_ELEMENT_SIZES.get(t, (elem_width, elem_height))
            else:
                ew, eh = elem_width, elem_height
            x = lane_left + col * cell_w + (cell_w - ew) / 2
            y = lane_top + row * (elem_height + v_gap) + (elem_height - eh) / 2
            positions[eid] = (x, y, round(x + ew), round(y + eh))
    return positions


def compute_diagonal_positions(element_ids, start_index=0, per_row=8, step=200,
                                row_gap=200, elem_width=180, elem_height=120):
    """Legacy fallback layout. Prefer compute_grid_positions() for non-BPMN
    diagrams -- this one is kept only for callers that still depend on the
    diagonal-staircase look for a brand new, empty diagram.
    """
    positions = {}
    for offset, eid in enumerate(element_ids):
        idx = start_index + offset
        diag_pos = idx % per_row
        row = idx // per_row
        x = 20 + diag_pos * step
        y = 20 + diag_pos * step + row * (elem_height + row_gap)
        positions[eid] = (x, y, x + elem_width, y + elem_height)
    return positions


def get_diagram_extent(diag):
    """Return (max_right, max_bottom) of all currently placed diagram objects,
    in visual (positive-down) coordinates. (0, 0) if the diagram is empty.
    """
    diag.DiagramObjects.Refresh()
    max_right = 0
    max_bottom = 0
    for i in range(diag.DiagramObjects.Count):
        dobj = diag.DiagramObjects.GetAt(i)
        max_right = max(max_right, dobj.right)
        max_bottom = max(max_bottom, -dobj.bottom)
    return max_right, max_bottom


def compute_uml_class_height(attr_count, header_height=30, row_height=16,
                              min_height=70, padding=6):
    """Height for a UML Class box that shows an attribute compartment (e.g.
    data model entities with real EA Attributes added via sync_attributes()).

    Unlike ArchiMate elements (BusinessActor/BusinessObject/Component), which
    render as plain icon boxes with no attribute list and were confirmed to
    default to a fixed 90x70 regardless of instance, a UML Class's box grows
    with its attribute count -- a single fixed height would clip entities
    with many attributes or waste space on ones with few. This formula is an
    approximation (header + one row per attribute + padding), not an
    EA-confirmed constant like DEFAULT_ELEMENT_SIZES -- recalibrate against a
    real toolbox-dragged Class with a matching attribute count if it looks off.
    """
    return max(min_height, header_height + attr_count * row_height + padding)


def compute_uml_class_width(name, attr_labels, char_width=5.5, min_width=120, padding=10):
    """Width for a UML Class box, based on the longest label that has to fit
    (the class name itself, or an "attrname: type" attribute line) -- a fixed
    width works for the class name alone but clips long attribute/type names
    (e.g. "renewal_notice_sent: boolean").

    attr_labels: list of "name: type" strings (or any label text) that will
    be shown in the attribute compartment.
    char_width: rough average pixel width per character at EA's default
    diagram font/zoom -- an approximation, not a measured font metric.
    """
    longest = max([len(name)] + [len(l) for l in attr_labels], default=0)
    return max(min_width, longest * char_width + padding)


def compute_grid_positions(element_ids, elem_types=None, type_sizes=None,
                            sizes=None, default_size=DEFAULT_ELEMENT_SIZE,
                            start_x=20, start_y=20, per_row=8,
                            cell_width=180, cell_height=100,
                            h_gap=20, v_gap=20):
    """Tight, non-compounding row-major grid for non-BPMN diagrams (ArchiMate,
    UML data model, Requirements).

    Each element gets a box sized in one of two ways:
    - sizes={eid: (w, h)}: an explicit, per-element size (e.g. a UML Class
      whose height depends on its own attribute count -- see
      compute_uml_class_height). Takes precedence when present for that eid.
    - elem_types={eid: type} + type_sizes={type: (w, h)}: one size per
      element *type* (e.g. DEFAULT_ELEMENT_SIZES), for elements that render
      as a uniform icon box regardless of instance (ArchiMate elements).

    Either way, the box is centered within a uniform grid cell so differently
    -sized elements still line up -- same approach as the BPMN lane grid
    (compute_bpmn_element_positions). cell_height must be >= the tallest box
    that will be placed, or boxes in the same row will overlap. Row/column
    advance linearly (no compounding), so the layout stays compact and close
    to (start_x, start_y) instead of drifting far away as more elements are
    added.

    Explicit sizing is required here: EA's COM API does not auto-size a
    DiagramObject left with right/bottom unset (confirmed via a full live
    run -- produces a permanent 0x0 invisible object).
    """
    positions = {}
    sizes = sizes or {}
    type_sizes = type_sizes or {}
    cw = cell_width + h_gap
    ch = cell_height + v_gap
    for idx, eid in enumerate(element_ids):
        col = idx % per_row
        row = idx // per_row
        if eid in sizes:
            ew, eh = sizes[eid]
        else:
            t = (elem_types or {}).get(eid)
            ew, eh = type_sizes.get(t, default_size)
        x = start_x + col * cw + (cell_width - ew) / 2
        y = start_y + row * ch + (cell_height - eh) / 2
        positions[eid] = (x, y, x + ew, y + eh)
    return positions


def repair_zero_size_objects(diag, repo, type_sizes=None, default_size=DEFAULT_ELEMENT_SIZE,
                              get_elem_type=None, get_elem_size=None):
    """Fix any already-placed diagram objects that ended up 0x0 (e.g. from a
    prior position-only placement bug). Keeps each object's existing left/top
    (its position is fine) and only sets a proper right/bottom.

    get_elem_type: callable(element) -> Object_Type string. Defaults to
    element.Type via the COM API.
    get_elem_size: optional callable(element) -> (w, h), takes precedence
    over type_sizes/default_size when it returns a value (e.g. for UML
    Classes whose height depends on their own attribute count).
    """
    type_sizes = type_sizes or {}
    get_elem_type = get_elem_type or (lambda e: e.Type)
    diag.DiagramObjects.Refresh()
    fixed = 0
    for i in range(diag.DiagramObjects.Count):
        dobj = diag.DiagramObjects.GetAt(i)
        if dobj.right != 0 or dobj.bottom != 0:
            continue
        elem = repo.GetElementByID(dobj.ElementID)
        if not elem:
            continue
        size = get_elem_size(elem) if get_elem_size else None
        if size is None:
            t = get_elem_type(elem)
            size = type_sizes.get(t, default_size)
        ew, eh = size
        dobj.right = int(dobj.left) + ew
        dobj.bottom = int(dobj.top) - eh
        dobj.Update()
        fixed += 1
    if fixed:
        diag.Update()
    return fixed


def get_placed_ids(diag):
    diag.DiagramObjects.Refresh()
    placed = set()
    for i in range(diag.DiagramObjects.Count):
        dobj = diag.DiagramObjects.GetAt(i)
        placed.add(dobj.ElementID)
    return placed


def set_diagram_link_style(diag, line_style):
    """Set LineStyle on every DiagramLink on a diagram (see the LineStyle enum
    table in the ea-model-common skill -- e.g. 8 = Orthogonal Square,
    9 = Orthogonal Rounded). Idempotent -- safe to call on every run.
    """
    diag.DiagramLinks.Refresh()
    count = 0
    for i in range(diag.DiagramLinks.Count):
        dl = diag.DiagramLinks.GetAt(i)
        if dl.LineStyle != line_style:
            dl.LineStyle = line_style
            dl.Update()
            count += 1
    return count


def _place_diagram_object(diag, oid, pos):
    """pos is either (left, top) -- position only, EA auto-sizes the box --
    or (left, top, right, bottom) -- explicit size, only for BPMN diagrams
    where EA needs an exact type-appropriate box (see BPMN_ELEMENT_SIZES).
    """
    dobj = diag.DiagramObjects.AddNew("", "")
    dobj.ElementID = oid
    if len(pos) == 4:
        l, vt, r, vb = pos
        dobj.left = int(l)
        dobj.top = int(-vt)
        dobj.right = int(r)
        dobj.bottom = int(-vb)
    else:
        l, vt = pos
        dobj.left = int(l)
        dobj.top = int(-vt)
    dobj.Update()
    return dobj


def add_missing_elements(diag, element_ids, object_ids, positions):
    placed = get_placed_ids(diag)
    added = 0
    for eid in element_ids:
        oid = object_ids.get(eid)
        if oid is None or oid in placed:
            continue
        pos = positions.get(eid)
        if pos is None:
            continue
        _place_diagram_object(diag, oid, pos)
        added += 1
    if added:
        diag.Update()
    return added


def create_diagram_objects(diag, element_ids, object_ids, positions):
    diag.DiagramObjects.Refresh()
    count = 0
    for eid in element_ids:
        oid = object_ids.get(eid)
        if oid is None:
            continue
        pos = positions.get(eid)
        if pos is None:
            continue
        _place_diagram_object(diag, oid, pos)
        count += 1
    if count:
        diag.Update()
    return count


def get_lane_from_fields(fields):
    if fields is None:
        return None
    lane = fields.get("Lane") or fields.get("lane")
    if lane:
        return lane
    # Fallback: #### nesting stores parent eid in "Parent" field
    return fields.get("Parent") or None


def sort_by_flow_order(lane_element_ids, sequence_flows):
    """Sort BPMN element IDs by process flow order (DFS pre-order traversal).

    Starts from elements that participate in the flow (have outgoing edges)
    and have no incoming edges. Follows sequence flows forward. Elements not
    in the flow graph (e.g. DataObjects) are appended at the end. Cycles are
    handled naturally since visited elements are skipped.
    """
    adj = {}
    incoming = {}
    for eid in lane_element_ids:
        adj[eid] = []
        incoming[eid] = []
    for flow in sequence_flows:
        src, tgt = flow["source"], flow["target"]
        if src in adj and tgt in adj:
            adj[src].append(tgt)
            incoming[tgt].append(src)

    visited = set()
    result = []

    def dfs(eid):
        if eid in visited:
            return
        visited.add(eid)
        result.append(eid)
        for neighbor in adj.get(eid, []):
            dfs(neighbor)

    # Start from flow participants with no incoming edges:
    # only elements that have outgoing edges (adj non-empty) are flow participants
    for eid in lane_element_ids:
        if not incoming[eid] and adj[eid]:
            dfs(eid)

    # Append remaining elements not in the flow graph (DataObjects, etc.)
    for eid in lane_element_ids:
        if eid not in visited:
            result.append(eid)

    return result


def find_longest_path(adj, start_nodes):
    """Find the longest acyclic path in a directed graph via DFS.

    adj: {node: [neighbor, ...]}
    start_nodes: list of nodes with no incoming edges (and at least one outgoing)
    Returns list of node IDs in longest path, in traversal order.
    """
    best = []

    def dfs(node, path, visited):
        nonlocal best
        if len(path) > len(best):
            best = list(path)
        for n in adj.get(node, []):
            if n not in visited:
                visited.add(n)
                dfs(n, path + [n], visited)
                visited.remove(n)

    for s in start_nodes:
        dfs(s, [s], {s})

    return best


def compute_bpmn_flow_layout(elements_by_lane, lane_bounds, sequence_flows,
                             elem_types, h_gap=60, v_gap=30):
    """BPMN flow layout: longest path in straight line, side branches below.

    elements_by_lane: {lane_id: [eid, ...]}
    lane_bounds: {lane_id: (left, top, right, bottom)}
    sequence_flows: [{"source": eid, "target": eid}, ...]
    elem_types: {eid: label_string}

    Returns: (positions dict {eid: (l,t,r,b)}, updated_lane_bounds)
    """
    elem_to_lane = {}
    for lid, eids in elements_by_lane.items():
        for eid in eids:
            elem_to_lane[eid] = lid

    lane_adj = {}
    lane_inc = {}
    for lid in elements_by_lane:
        lane_adj[lid] = {}
        lane_inc[lid] = {}
        for eid in elements_by_lane[lid]:
            lane_adj[lid][eid] = []
            lane_inc[lid][eid] = []

    for fl in sequence_flows:
        s, t = fl["source"], fl["target"]
        sl = elem_to_lane.get(s)
        tl = elem_to_lane.get(t)
        if sl and sl == tl:
            lane_adj[sl][s].append(t)
            lane_inc[sl][t].append(s)

    # Find longest path and compute needed width per lane
    longest_paths = {}
    max_width = {}
    for lid, eids in elements_by_lane.items():
        adj = lane_adj[lid]
        inc = lane_inc[lid]
        starts = [e for e in eids if not inc.get(e, []) and adj.get(e, [])]
        lp = find_longest_path(adj, starts)
        longest_paths[lid] = lp
        if lp:
            tw = 0
            for i, e in enumerate(lp):
                t = elem_types.get(e, "Activity")
                ew, _ = BPMN_ELEMENT_SIZES.get(t, (110, 60))
                tw += ew
                if i > 0:
                    tw += h_gap
            max_width[lid] = tw + 90
        else:
            max_width[lid] = 0

    # Expand all lanes to the width of the widest one
    all_widths = [max_width.get(lid, 0) for lid in lane_bounds]
    overall_max = max(all_widths) if all_widths else 0
    updated_bounds = dict(lane_bounds)
    for lid, b in lane_bounds.items():
        nw = max(max_width.get(lid, 0), overall_max)
        cw = b[2] - b[0]
        if nw > cw:
            updated_bounds[lid] = (b[0], b[1], b[0] + nw, b[3])

    # Place elements
    pos = {}
    row_h = 70

    for lid, eids in elements_by_lane.items():
        b = updated_bounds[lid]
        ll = b[0] + 70
        lt = b[1] + 40
        adj = lane_adj[lid]
        inc = lane_inc[lid]
        lp = longest_paths[lid]

        flow_set = {e for e in eids if adj.get(e, []) or inc.get(e, [])}
        data_objs = [e for e in eids if e not in flow_set]

        if not lp:
            xp = ll
            for e in eids:
                t = elem_types.get(e, "Activity")
                ew, eh = BPMN_ELEMENT_SIZES.get(t, (110, 60))
                pos[e] = (xp, lt, xp + ew, lt + eh)
                xp += ew + h_gap
            continue

        # Row 0: longest path
        max_h = 0
        for e in lp:
            t = elem_types.get(e, "Activity")
            _, eh = BPMN_ELEMENT_SIZES.get(t, (110, 60))
            max_h = max(max_h, eh)

        xp = ll
        for e in lp:
            t = elem_types.get(e, "Activity")
            ew, eh = BPMN_ELEMENT_SIZES.get(t, (110, 60))
            yp = lt + (max_h - eh) / 2
            pos[e] = (xp, yp, xp + ew, yp + eh)
            xp += ew + h_gap

        # Row 1: remaining flow elements (side branches)
        remaining = [e for e in eids if e not in lp and e in flow_set]
        if remaining:
            yp = lt + row_h + v_gap
            xp = ll
            max_rh = max((BPMN_ELEMENT_SIZES.get(elem_types.get(e, "Activity"), (110, 60))[1] for e in remaining), default=0)
            for e in remaining:
                t = elem_types.get(e, "Activity")
                ew, eh = BPMN_ELEMENT_SIZES.get(t, (110, 60))
                preds = inc.get(e, [])
                placed = False
                for p in preds:
                    if p in pos:
                        pos[e] = (pos[p][0], yp + (max_rh - eh) / 2, pos[p][0] + ew, yp + (max_rh - eh) / 2 + eh)
                        placed = True
                        break
                if not placed:
                    pos[e] = (xp, yp + (max_rh - eh) / 2, xp + ew, yp + (max_rh - eh) / 2 + eh)
                    xp += ew + h_gap

        # Row 2: DataObjects
        if data_objs:
            yp = lt + 2 * (row_h + v_gap)
            xp = ll
            for e in data_objs:
                t = elem_types.get(e, "Activity")
                ew, eh = BPMN_ELEMENT_SIZES.get(t, (35, 50))
                pos[e] = (xp, yp, xp + ew, yp + eh)
                xp += ew + h_gap

    return pos, updated_bounds
