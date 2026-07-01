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
    positions = {}
    for offset, eid in enumerate(element_ids):
        idx = start_index + offset
        diag_pos = idx % per_row
        row = idx // per_row
        x = 20 + diag_pos * step
        y = 20 + diag_pos * step + row * (per_row * step + row_gap - step)
        positions[eid] = (x, y, x + elem_width, y + elem_height)
    return positions


def get_placed_ids(diag):
    diag.DiagramObjects.Refresh()
    placed = set()
    for i in range(diag.DiagramObjects.Count):
        dobj = diag.DiagramObjects.GetAt(i)
        placed.add(dobj.ElementID)
    return placed


def _place_diagram_object(diag, oid, pos):
    l, vt, r, vb = pos
    dobj = diag.DiagramObjects.AddNew("", "")
    dobj.ElementID = oid
    dobj.left = int(l)
    dobj.top = int(-vt)
    dobj.right = int(r)
    dobj.bottom = int(-vb)
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
