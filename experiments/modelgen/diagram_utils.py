"""Shared diagram layout utilities for EA COM API generators."""


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
                                    h_gap=30, v_gap=30):
    positions = {}
    for lane_id, eids in elements_by_lane.items():
        bounds = lane_bounds.get(lane_id, (0, 0, 1000, 500))
        lane_left = bounds[0] + 20
        lane_top = bounds[1] + 40
        lane_right = bounds[2] - 20
        per_row = max(1, int((lane_right - lane_left) / (elem_width + h_gap)))
        for idx, eid in enumerate(eids):
            col = idx % per_row
            row = idx // per_row
            x = lane_left + col * (elem_width + h_gap)
            y = lane_top + row * (elem_height + v_gap)
            positions[eid] = (x, y, x + elem_width, y + elem_height)
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
        l, t, r, b = pos
        dobj = diag.DiagramObjects.AddNew("", "")
        dobj.ElementID = oid
        dobj.left = l
        dobj.top = t
        dobj.right = r
        dobj.bottom = b
        dobj.Update()
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
        l, t, r, b = pos
        dobj = diag.DiagramObjects.AddNew("", "")
        dobj.ElementID = oid
        dobj.left = l
        dobj.top = t
        dobj.right = r
        dobj.bottom = b
        dobj.Update()
        count += 1
    if count:
        diag.Update()
    return count


def get_lane_from_fields(fields):
    if fields is None:
        return None
    return fields.get("Lane") or fields.get("lane") or None
