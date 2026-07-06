"""Shared BPMN generate/sync engine, parameterized by bpmn_config.ProcessConfig.

Ports the logic previously duplicated across generate_*_process_from_md.py /
sync_*_process_from_ea.py. Two format families exist, both preserved exactly:

- flat (Customer Account, Sales): "### Label—eid" elements with an explicit
  "- Lane:" field; MD sequence/message/data-association connector sections
  keyed by heading text; sync side writes one heading per connector category.
- hierarchical (Newsletter): "#### Label—eid" elements nested under their
  "### Lane—" header, lane membership derived from nesting (fields["Parent"]),
  no explicit "- Lane:" field; sync side writes a recursive, indented MD tree
  and combines Sequence/MessageFlow into one "### Sequence Flows" section.
"""
import os
import re
import json
import sqlite3

import ea_session
from bpmn_config import (
    LABEL_TO_STEREO, OBJECT_TYPE_MAP, BPMN_TAGGED_VALUES,
    CONNECTOR_TYPES, CONNECTOR_STEREOTYPE_EX, CONNECTOR_STEREOTYPES_SHORT,
    BPMN_TYPE_LABEL, BPMN_ELEMENT_SIZES,
)
from diagram_utils import get_placed_ids, add_missing_elements, create_diagram_objects

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORY_HEADING = {
    "SequenceFlow": "Sequence Flows",
    "MessageFlow": "Message Flows",
    "DataInputAssociation": "Data Input Associations",
    "DataOutputAssociation": "Data Output Associations",
}


def safe_id(name):
    return re.sub(r"[^a-zA-Z0-9]", "", name)


# ---------------------------------------------------------------------------
# MD parsing (generate side)
# ---------------------------------------------------------------------------

def _parse_md_flat(path, categories):
    elements = {}
    connectors = {cat: [] for cat in categories}
    current = None
    section = None
    fields = {}
    label = ""

    section_map = {CATEGORY_HEADING[cat]: cat for cat in categories}

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip()
        stripped = line.strip()

        if stripped.startswith("## "):
            section = "header"
            parts_after = stripped[3:].strip()
            sep = None
            for s in ("—", "–"):
                if s in parts_after:
                    sep = s
                    break
            if sep:
                if current and label:
                    elements[safe_id(current)] = {"label": label, "fields": dict(fields)}
                label, eid_part = parts_after.split(sep, 1)
                label = label.strip()
                eid_part = eid_part.strip()
                current = eid_part
                fields = {}
            continue

        if stripped.startswith("### "):
            if current and label:
                elements[safe_id(current)] = {"label": label, "fields": dict(fields)}
            parts_after = stripped[4:].strip()
            if parts_after in section_map:
                section = section_map[parts_after]
                current = None
                continue
            sep_char = None
            for s in ("—", "–"):
                if s in parts_after:
                    sep_char = s
                    break
            if sep_char:
                label, eid_part = parts_after.split(sep_char, 1)
                label = label.strip()
                eid_part = eid_part.strip()
            else:
                label = parts_after
                eid_part = parts_after
            current = eid_part
            fields = {}
            section = None
            continue

        if current and stripped.startswith("- "):
            key_val = stripped[2:].strip()
            colon_pos = key_val.find(": ")
            if colon_pos > 0:
                key = key_val[:colon_pos].strip()
                val = key_val[colon_pos + 2:].strip()
                fields[key] = val

        if section and section in connectors and stripped.startswith("- "):
            line_flow = stripped[2:].strip()
            m = re.match(r"(.+?)\s*[->→➡]\s*(.+?)(\s*\[(.+?)\])?$", line_flow)
            if m:
                src = safe_id(m.group(1).strip())
                tgt = safe_id(m.group(2).strip())
                cond = (m.group(4) or "").strip()
                connectors[section].append({"source": src, "target": tgt, "condition": cond})

    if current and label:
        elements[safe_id(current)] = {"label": label, "fields": dict(fields)}

    return elements, connectors


def _parse_md_hierarchical(path, categories):
    elements = {}
    sequence_flows = []
    current = None
    section = None
    fields = {}
    label = ""
    parent_eid = None  # most recent ### element, used as parent for #### children

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip()
        stripped = line.strip()

        if stripped.startswith("### Sequence Flows"):
            section = "flows"
            continue
        if stripped.startswith("## "):
            section = "header"
            parts_after = stripped[3:].strip()
            sep = None
            for s in ("—", "–"):
                if s in parts_after:
                    sep = s
                    break
            if sep:
                if current and label:
                    elements[safe_id(current)] = {"label": label, "fields": dict(fields)}
                label, eid_part = parts_after.split(sep, 1)
                label = label.strip()
                eid_part = eid_part.strip()
                current = eid_part
                fields = {}
                parent_eid = safe_id(current)
            continue

        if section != "flows" and stripped.startswith("#### "):
            if current and label:
                elements[safe_id(current)] = {"label": label, "fields": dict(fields)}
            parts = stripped[5:].strip()
            sep_char = None
            for s in ("—", "–"):
                if s in parts:
                    sep_char = s
                    break
            if sep_char:
                label, eid_part = parts.split(sep_char, 1)
                label = label.strip()
                eid_part = eid_part.strip()
            else:
                label = parts
                eid_part = parts
            current = eid_part
            fields = {}
            if parent_eid:
                fields["Parent"] = parent_eid
            continue
        if stripped.startswith("### "):
            if current and label:
                elements[safe_id(current)] = {"label": label, "fields": dict(fields)}
            parts_after = stripped[4:].strip()
            sep_char = None
            for s in ("—", "–"):
                if s in parts_after:
                    sep_char = s
                    break
            if sep_char:
                label, eid_part = parts_after.split(sep_char, 1)
                label = label.strip()
                eid_part = eid_part.strip()
            else:
                label = parts_after
                eid_part = parts_after
            current = eid_part
            fields = {}
            parent_eid = safe_id(current)
            continue

        if current and stripped.startswith("- "):
            key_val = stripped[2:].strip()
            colon_pos = key_val.find(": ")
            if colon_pos > 0:
                key = key_val[:colon_pos].strip()
                val = key_val[colon_pos + 2:].strip()
                fields[key] = val

        if section == "flows" and stripped.startswith("- "):
            line_flow = stripped[2:].strip()
            m = re.match(r"(.+?)\s*[→➡]\s*(.+?)(\s*\[(.+?)\])?$", line_flow)
            if m:
                src = safe_id(m.group(1).strip())
                tgt = safe_id(m.group(2).strip())
                cond = (m.group(4) or "").strip()
                sequence_flows.append({"source": src, "target": tgt, "condition": cond})

    if current and label:
        elements[safe_id(current)] = {"label": label, "fields": dict(fields)}

    # Normalize to the same {category: [...]} shape the flat format returns.
    connectors = {cat: [] for cat in categories}
    connectors["SequenceFlow"] = sequence_flows
    return elements, connectors


def parse_md(config, md_path=None):
    path = md_path or config.default_md
    if config.hierarchical_format:
        return _parse_md_hierarchical(path, config.generate_connector_categories)
    return _parse_md_flat(path, config.generate_connector_categories)


# ---------------------------------------------------------------------------
# Lane / Pool field helpers + BPMN-only layout (moved from diagram_utils.py)
# ---------------------------------------------------------------------------

def get_lane_from_fields(fields):
    if fields is None:
        return None
    lane = fields.get("Lane") or fields.get("lane")
    if lane:
        return lane
    # Fallback: #### nesting (hierarchical format) stores parent eid in "Parent"
    return fields.get("Parent") or None


def get_pool_from_lane_fields(fields):
    """Parallel to get_lane_from_fields, read off a ### Lane-- entry's own
    fields. No Parent-style fallback -- Pool is new, no legacy data to match."""
    if fields is None:
        return None
    return fields.get("Pool") or fields.get("pool") or None


def sort_by_flow_order(lane_element_ids, sequence_flows):
    """Sort BPMN element IDs by process flow order (DFS pre-order traversal)."""
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

    for eid in lane_element_ids:
        if not incoming[eid] and adj[eid]:
            dfs(eid)

    for eid in lane_element_ids:
        if eid not in visited:
            result.append(eid)

    return result


def find_longest_path(adj, start_nodes):
    """Find the longest acyclic path in a directed graph via DFS."""
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


def compute_bpmn_lane_positions(lanes, lane_height=500, lane_width=1000, gap=250, pools=None):
    """Returns (lane_positions, pool_positions). pool_positions is {} when
    `pools` is not given, so callers never need a shape check.

    pools: optional {pool_id: [lane_id, ...]}. Lanes sharing a pool stack
    together inside a pool bounding box (header band + lane stack); lanes
    absent from `pools` lay out exactly as they did before pool support
    existed (flat vertical stack).
    """
    positions = {}
    pool_positions = {}
    pools = pools or {}
    lane_to_pool = {}
    for pid, lids in pools.items():
        for lid in lids:
            lane_to_pool[lid] = pid

    pool_header = 40
    pool_inner_gap = 20
    y = 30
    placed_pools = set()
    for lane in lanes:
        lid = lane.get("id")
        if lid in positions:
            continue
        pid = lane_to_pool.get(lid)
        if pid is not None:
            if pid in placed_pools:
                continue
            placed_pools.add(pid)
            pool_lane_ids = pools.get(pid, [lid])
            pool_start_y = y
            inner_y = y + pool_header
            for plid in pool_lane_ids:
                positions[plid] = (0, inner_y, lane_width, inner_y + lane_height)
                inner_y += lane_height + pool_inner_gap
            pool_end_y = inner_y - pool_inner_gap
            pool_positions[pid] = (0, pool_start_y, lane_width, pool_end_y)
            y = pool_end_y + gap
        else:
            positions[lid] = (0, y, lane_width, y + lane_height)
            y += lane_height + gap
    return positions, pool_positions


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


def _place_component_row(pos, comp, comp_adj, comp_inc, elem_types, ll, row_y, h_gap, v_gap,
                          preferred_cx=None):
    """Place one connected component (one independent StartEvent-rooted flow)
    as its own row: longest path in a straight line starting at `ll`
    (the lane's left column), with gateway forks/chained/merge-point branches
    stacked below it -- same logic as before, just scoped to one component
    and one row's local `row_y` instead of the whole lane's `lt`.

    preferred_cx: optional {eid: x} -- if the row's leading element (the
    first element on its own longest path) has an entry here, the row starts
    so that element is *centered* on that X instead of starting flush at
    `ll`. Used to align a message-flow-receiving element with its
    already-placed cross-lane sender (see compute_bpmn_flow_layout).
    """
    row_h = 70
    starts = [e for e in comp if not comp_inc.get(e, []) and comp_adj.get(e, [])]
    lp = find_longest_path(comp_adj, starts) if starts else []

    if lp and preferred_cx and lp[0] in preferred_cx:
        lead_t = elem_types.get(lp[0], "Activity")
        lead_ew, _ = BPMN_ELEMENT_SIZES.get(lead_t, (110, 60))
        ll = preferred_cx[lp[0]] - lead_ew / 2

    if not lp:
        # No zero-incoming-degree entry point (e.g. a pure cycle) -- place
        # the whole component in a single flat row, best effort.
        xp = ll
        for e in comp:
            t = elem_types.get(e, "Activity")
            ew, eh = BPMN_ELEMENT_SIZES.get(t, (110, 60))
            pos[e] = (xp, row_y, xp + ew, row_y + eh)
            xp += ew + h_gap
        return

    max_h = max((BPMN_ELEMENT_SIZES.get(elem_types.get(e, "Activity"), (110, 60))[1] for e in lp), default=60)
    xp = ll
    for e in lp:
        t = elem_types.get(e, "Activity")
        ew, eh = BPMN_ELEMENT_SIZES.get(t, (110, 60))
        yp = row_y + (max_h - eh) / 2
        pos[e] = (xp, yp, xp + ew, yp + eh)
        xp += ew + h_gap

    remaining = [e for e in comp if e not in lp]
    if not remaining:
        return
    lp_set = set(lp)

    # Pass 1: elements whose predecessor is on this row's main path (a
    # gateway fork) stack in one column under that predecessor, below this
    # row -- multiple siblings from the same fork stack under each other
    # instead of spreading out horizontally. Placed first since Pass 2/3
    # below may chain off these positions.
    groups = {}
    unresolved = []
    for e in remaining:
        anchor = next((p for p in comp_inc.get(e, []) if p in lp_set), None)
        if anchor is not None:
            groups.setdefault(anchor, []).append(e)
        else:
            unresolved.append(e)

    lp_index = {eid: i for i, eid in enumerate(lp)}
    for anchor, group_eids in groups.items():
        sizes = [BPMN_ELEMENT_SIZES.get(elem_types.get(e, "Activity"), (110, 60)) for e in group_eids]
        # Center the stack under the gateway's main-path successor (the
        # activity the flow continues to), not the gateway itself -- a
        # gateway diamond is narrow, so centering under it looks cramped
        # next to a wider activity box.
        idx = lp_index.get(anchor)
        if idx is not None and idx + 1 < len(lp):
            successor = lp[idx + 1]
            target_cx = (pos[successor][0] + pos[successor][2]) / 2
        else:
            target_cx = (pos[anchor][0] + pos[anchor][2]) / 2
        y = row_y + row_h + v_gap
        for e, (ew, eh) in zip(group_eids, sizes):
            ex = target_cx - ew / 2
            pos[e] = (ex, y, ex + ew, y + eh)
            y += eh + v_gap

    # Pass 2: any element that is BOTH the sole successor of its predecessor
    # AND that predecessor's only child continues that predecessor's row
    # horizontally (same vertical center, immediately to its right) instead
    # of dropping to a new row below it -- a branch, once dropped down by
    # Pass 1, keeps flowing left-to-right after its first activity, exactly
    # like the main row does. Applied repeatedly (not just one hop) so an
    # entire multi-element chain flows rightward, not just a lone Event.
    # Restricted to elements with exactly one predecessor total -- a genuine
    # merge point (2+ predecessors) must go through Pass 3's merge-point
    # handling instead, even if one specific incoming edge would otherwise
    # qualify.
    inline_events = set()
    changed = True
    while changed:
        changed = False
        for e in unresolved:
            if e in inline_events or e in pos:
                continue
            preds = comp_inc.get(e, [])
            if len(preds) != 1:
                continue
            p = preds[0]
            if p in pos and len(comp_adj.get(p, [])) == 1:
                t = elem_types.get(e, "Activity")
                ew, eh = BPMN_ELEMENT_SIZES.get(t, (110, 60))
                p_cy = (pos[p][1] + pos[p][3]) / 2
                px = pos[p][2] + h_gap
                pos[e] = (px, p_cy - eh / 2, px + ew, p_cy + eh / 2)
                inline_events.add(e)
                changed = True

    # Pass 3: anything still unplaced -- chained off another branch element,
    # or a merge point (multiple predecessors) -- stacks below its
    # predecessor(s)' actual position, or falls back to a fresh slot.
    # next_y_for_pred tracks each predecessor's next free slot so a
    # second/third child doesn't land on top of the first.
    xp2 = ll
    next_y_for_pred = {}
    for e in unresolved:
        if e in inline_events:
            continue
        t = elem_types.get(e, "Activity")
        ew, eh = BPMN_ELEMENT_SIZES.get(t, (110, 60))
        preds_placed = [p for p in comp_inc.get(e, []) if p in pos]
        placed = False
        if preds_placed:
            # A merge point must clear ALL of its placed predecessors'
            # bottoms, not just the first one found -- using only the first
            # can land exactly on top of a sibling that shares that same
            # predecessor and already claimed the "first predecessor's
            # bottom + gap" slot.
            anchor_p = preds_placed[0]
            py = max(next_y_for_pred.get(p, pos[p][3] + v_gap) for p in preds_placed)
            pos[e] = (pos[anchor_p][0], py, pos[anchor_p][0] + ew, py + eh)
            next_y_for_pred[anchor_p] = py + eh + v_gap
            placed = True
        if not placed:
            # Recomputed fresh each time (not a one-time snapshot), since
            # this same pass places chained elements that can extend deeper
            # during the pass itself.
            placed_bottoms = [pos[x][3] for x in remaining if x in pos]
            fallback_y = max([row_y + row_h + v_gap] + [b + v_gap for b in placed_bottoms])
            pos[e] = (xp2, fallback_y, xp2 + ew, fallback_y + eh)
            xp2 += ew + h_gap

    # Correction pass: a merge point can be visited (and placed) by the
    # DFS-ordered loop above before ALL of its predecessors are placed --
    # DFS fully explores one branch before backtracking to a sibling branch,
    # so a later predecessor's placement doesn't retroactively fix an
    # earlier, incomplete resolution. Re-clear against the complete set now
    # that everything in this component has been placed.
    for e in unresolved:
        if e in inline_events or e not in pos:
            continue
        preds = comp_inc.get(e, [])
        if len(preds) < 2:
            continue
        preds_placed = [p for p in preds if p in pos and p != e]
        if not preds_placed:
            continue
        needed_y = max(pos[p][3] for p in preds_placed) + v_gap
        if needed_y > pos[e][1]:
            l, t, r, b = pos[e]
            pos[e] = (l, needed_y, r, needed_y + (b - t))


def compute_bpmn_flow_layout(elements_by_lane, lane_bounds, sequence_flows,
                              elem_types, h_gap=60, v_gap=30, message_flows=None,
                              data_associations=None):
    """BPMN flow layout. Each independent StartEvent-rooted flow (a connected
    component of the lane's sequence-flow graph) becomes its own row,
    starting at the lane's left column and flowing rightward -- stacked
    vertically, one row per component, in lane order. Gateway forks within a
    single flow still stack near the fork point (not restarted at the left
    column -- they're an alternate path within one flow, not a new one).
    DataObjects/DataStores (no sequence-flow edges) always get their own
    row, below all flow rows in the lane -- lanes are fixed, non-overlapping
    vertical bands, so a DataObject can never actually move outside its own
    lane's row/band regardless of which lane its connected activity is in.

    message_flows (optional): a MessageFlow normally crosses to an element in
    another lane/pool -- when given (or when data_associations is given),
    lanes are processed top-to-bottom (rather than input order) and a
    component whose leading element is the source or target of a cross-lane
    MessageFlow to/from an already-placed element is horizontally centered
    on that partner's X, so the connector ends up a clean vertical line
    (top/bottom-center on both ends) instead of a long diagonal. Only the
    row's leading element is aligned this way -- a message received
    mid-chain doesn't reposition the row.

    data_associations (optional): DataInputAssociation/DataOutputAssociation
    edges -- a DataObject/DataStore stays in its own dedicated row (below the
    flow rows, in its own lane, as above), but is horizontally centered on
    its connected activity's X (wherever that activity ended up, even in
    another lane), so the connector is a straight line with no bends instead
    of an arbitrary diagonal. Placed in a pass after ALL lanes' flow elements
    are placed (not interleaved per-lane), so the connected activity's
    position is always known regardless of lane processing order.

    Returns (positions dict {eid: (l,t,r,b)}, updated_lane_bounds)
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

    # Cross-lane MessageFlow partners, keyed by the OTHER element -- used to
    # align a component's leading element with an already-placed partner.
    msg_partners = {}
    if message_flows:
        for fl in message_flows:
            s, t = fl["source"], fl["target"]
            sl, tl = elem_to_lane.get(s), elem_to_lane.get(t)
            if sl and tl and sl != tl:
                msg_partners.setdefault(s, []).append(t)
                msg_partners.setdefault(t, []).append(s)

    pos = {}
    row_h = 70
    updated_bounds = dict(lane_bounds)

    lane_order = sorted(elements_by_lane.keys(), key=lambda lid: lane_bounds[lid][1]) \
        if (message_flows or data_associations) else list(elements_by_lane.keys())

    pending_data_objs = {}  # lid -> (data_objs, flow_bottom) -- placed after all lanes' flow elements
    for lid in lane_order:
        eids = elements_by_lane[lid]
        adj = lane_adj[lid]
        inc = lane_inc[lid]
        b = lane_bounds[lid]
        ll = b[0] + 70
        lt = b[1] + 40

        flow_set = {e for e in eids if adj.get(e, []) or inc.get(e, [])}
        data_objs = [e for e in eids if e not in flow_set]

        if flow_set:
            # Connected components of the flow graph (undirected: a fork and
            # its branches, or a merge and its inputs, are one component even
            # though the edges are directed) -- each becomes its own row.
            undirected = {e: set(adj.get(e, [])) | set(inc.get(e, [])) for e in flow_set}
            visited = set()
            components = []
            for e in eids:  # preserve MD order for deterministic row order
                if e in flow_set and e not in visited:
                    comp = []
                    stack = [e]
                    visited.add(e)
                    while stack:
                        cur = stack.pop()
                        comp.append(cur)
                        for nb in undirected.get(cur, []):
                            if nb not in visited:
                                visited.add(nb)
                                stack.append(nb)
                    components.append(comp)

            row_y = lt
            for comp in components:
                comp_set = set(comp)
                comp_adj = {e: [t for t in adj.get(e, []) if t in comp_set] for e in comp}
                comp_inc = {e: [s for s in inc.get(e, []) if s in comp_set] for e in comp}
                preferred_cx = None
                if msg_partners:
                    preferred_cx = {}
                    for e in comp:
                        for partner in msg_partners.get(e, []):
                            if partner in pos:
                                pl, pt, pr, pb = pos[partner]
                                preferred_cx[e] = (pl + pr) / 2
                                break
                _place_component_row(pos, comp, comp_adj, comp_inc, elem_types, ll, row_y, h_gap, v_gap,
                                      preferred_cx=preferred_cx)
                row_bottom = max([pos[e][3] for e in comp if e in pos], default=row_y + row_h)
                row_y = row_bottom + v_gap * 2  # extra gap between independent flows

        if data_objs:
            # Deferred: placed in a pass below, after every lane's flow
            # elements are placed, so a DataObject's connected activity is
            # always known regardless of lane processing order (its activity
            # may be in a lane not yet processed at this point).
            flow_bottoms = [pos[e][3] for e in eids if e in flow_set and e in pos]
            flow_bottom = max(flow_bottoms, default=lt + row_h)
            pending_data_objs[lid] = (data_objs, flow_bottom, ll)

    # DataObjects/DataStores: own row below the flow rows in their own lane
    # (never move outside that lane's band), horizontally centered on their
    # connected activity's X when known (even if that activity is in another
    # lane) so the connector is a straight line instead of an arbitrary
    # diagonal -- explicit user rule: "positioned above or below the
    # activity they are connected to, which can exist in another lane/pool.
    # The connector preferably has no bends."
    data_partner = {}
    if data_associations:
        all_data_objs = {e for objs, _, _ in pending_data_objs.values() for e in objs}
        for fl in data_associations:
            s, t = fl["source"], fl["target"]
            if s in all_data_objs and t not in all_data_objs:
                data_partner.setdefault(s, []).append(t)
            elif t in all_data_objs and s not in all_data_objs:
                data_partner.setdefault(t, []).append(s)
    for lid, (data_objs, flow_bottom, ll) in pending_data_objs.items():
        yp = flow_bottom + v_gap
        xp = ll
        for e in data_objs:
            t = elem_types.get(e, "Activity")
            ew, eh = BPMN_ELEMENT_SIZES.get(t, (35, 50))
            cx = None
            for partner in data_partner.get(e, []):
                if partner in pos:
                    pl, pt, pr, pb = pos[partner]
                    cx = (pl + pr) / 2
                    break
            # Prefer the aligned X, but never place further left than the
            # packing pointer -- two DataObjects connected to the same (or
            # nearby) activity would otherwise land exactly on top of each
            # other, since each is computed independently. Cascades them
            # rightward instead when their preferred slots collide.
            left = max(cx - ew / 2, xp) if cx is not None else xp
            pos[e] = (left, yp, left + ew, yp + eh)
            xp = left + ew + h_gap

    # Widen every lane to the widest lane's actual content width, so all
    # lanes share a uniform right edge (computed from real placements now,
    # not a single longest-path estimate -- there can be multiple rows).
    lane_rights = {}
    for lid, eids in elements_by_lane.items():
        rights = [pos[e][2] for e in eids if e in pos]
        lane_rights[lid] = (max(rights) - lane_bounds[lid][0] + 20) if rights else 0
    overall_max_w = max(lane_rights.values(), default=0)
    for lid, b in list(updated_bounds.items()):
        nw = max(lane_rights.get(lid, 0), overall_max_w)
        cw = b[2] - b[0]
        if nw > cw:
            updated_bounds[lid] = (b[0], b[1], b[0] + nw, b[3])

    # Post-process: lane heights from compute_bpmn_lane_positions are a fixed
    # guess (default 500px). Multiple stacked rows plus deep branch-stacking
    # can push a lane's actual content past that guess -- without this pass,
    # the next lane's elements would start at their originally-allocated Y
    # and collide with the overflow. Shift every lane (and everything placed
    # in it) down by the cumulative overflow from all preceding lanes,
    # processed top-to-bottom.
    lane_order_by_y = sorted(updated_bounds.keys(), key=lambda lid: updated_bounds[lid][1])
    cumulative_shift = 0
    for lid in lane_order_by_y:
        b = updated_bounds[lid]
        if cumulative_shift:
            b = (b[0], b[1] + cumulative_shift, b[2], b[3] + cumulative_shift)
            updated_bounds[lid] = b
            for e in elements_by_lane.get(lid, []):
                if e in pos:
                    l, t, r, bo = pos[e]
                    pos[e] = (l, t + cumulative_shift, r, bo + cumulative_shift)
        actual_bottom = max([pos[e][3] for e in elements_by_lane.get(lid, []) if e in pos], default=b[3])
        overflow = actual_bottom + v_gap - b[3]
        if overflow > 0:
            updated_bounds[lid] = (b[0], b[1], b[2], b[3] + overflow)
            cumulative_shift += overflow

    return pos, updated_bounds


def _connector_path(src, tgt):
    """src/tgt: (left, top, right, bottom) in EA's raw DiagramObject convention
    (top/bottom negative, more-negative = lower on the page). Returns a
    DiagramLink.Path waypoint string routing between the centers of whichever
    borders face each other, or None if the boxes overlap (let EA auto-route).

    Verified empirically (2026-07-05, Sandbox, confirmed against a manual
    reference edit): DiagramLink.Path -- not .Geometry's EDGE field -- is what
    actually controls rendered routing; setting only Geometry had no visible
    effect. A single waypoint at the source's own vertical center produces a
    clean side-to-side route when the target is beside the source. When the
    target is above/below, a single waypoint at (source's own horizontal
    center, target's own vertical center) produces a clean elbow: straight out
    of the source's top/bottom-center, bending at the target's own center line
    to enter its left/right-center (or straight into its top/bottom-center if
    the two happen to share the same horizontal center).
    """
    sl, st, sr, sb = src
    tl, tt, tr, tb = tgt
    scx, scy = (sl + sr) / 2, (st + sb) / 2
    tcx, tcy = (tl + tr) / 2, (tt + tb) / 2

    y_disjoint = tt <= sb or tb >= st
    x_disjoint = tl >= sr or tr <= sl

    # Check vertical (Y-disjoint) first: a box can be X-disjoint too just as a
    # side effect of horizontal centering choices elsewhere, even though the
    # dominant visual relationship is "below/above", not "beside".
    if y_disjoint:
        return f"{int(scx)}:{int(tcy)};"
    if x_disjoint:
        if tl >= sr:
            mx = (sr + tl) / 2
        else:
            mx = (sl + tr) / 2
        return f"{int(mx)}:{int(scy)};"
    return None


def _message_flow_path(src, tgt):
    """MessageFlow-specific routing: always exits/enters top or bottom-center
    on BOTH ends, never a side -- if the flow starts at the bottom (source
    above target) it ends at the receiving activity's top, and vice versa
    (explicit user rule, 2026-07-05). This differs from _connector_path's
    generic vertical case, which enters the target's *side* when the boxes
    aren't X-aligned -- appropriate for a sequence-flow branch (which reads
    as a sideways continuation) but not for a MessageFlow, which reads as a
    cross-lane/pool crossing and should look that way regardless of X
    alignment. Uses a 2-waypoint elbow (bend at the midpoint between the two
    boxes) when they aren't X-aligned; collapses to a single straight
    vertical line when they are (the common case once
    compute_bpmn_flow_layout's message-flow position alignment has run).
    """
    sl, st, sr, sb = src
    tl, tt, tr, tb = tgt
    scx, scy = (sl + sr) / 2, (st + sb) / 2
    tcx, tcy = (tl + tr) / 2, (tt + tb) / 2

    if tt <= sb:
        # target below: exit source's bottom-center, enter target's top-center
        my = (sb + tt) / 2
        return f"{int(scx)}:{int(my)};{int(tcx)}:{int(my)};"
    if tb >= st:
        # target above: exit source's top-center, enter target's bottom-center
        my = (st + tb) / 2
        return f"{int(scx)}:{int(my)};{int(tcx)}:{int(my)};"
    # Not actually vertically separated (shouldn't normally happen for a
    # cross-lane message flow) -- fall back to the generic side-to-side rule.
    return _connector_path(src, tgt)


def set_tagged_values(elem, stereo, fields):
    tag_defs = BPMN_TAGGED_VALUES.get(stereo, {})
    if not tag_defs:
        return
    label_to_prop = {v: k for k, v in tag_defs.items()}
    for field_key, field_val in fields.items():
        prop_key = label_to_prop.get(field_key)
        if prop_key and field_val:
            tv = elem.TaggedValues.AddNew(prop_key, field_val)
            tv.Update()


# ---------------------------------------------------------------------------
# generate(): MD -> EA
# ---------------------------------------------------------------------------

def generate(config, qea_path=None, md_path=None):
    qea_path = qea_path or config.default_qea
    md_path = md_path or config.default_md
    guid_map_file = os.path.join(SCRIPT_DIR, config.guid_map_file)

    elements, connectors = parse_md(config, md_path)
    total_conns = sum(len(v) for v in connectors.values())
    print(f"Parsed {len(elements)} elements, {total_conns} connectors "
          f"({', '.join(f'{k}: {len(v)}' for k, v in connectors.items() if v)})")

    elem_types = {eid: data["label"] for eid, data in elements.items()
                  if data.get("label") and data["label"] not in ("Lane", "Pool")}

    guid_map = {}
    if os.path.exists(guid_map_file):
        with open(guid_map_file, "r") as f:
            guid_map = json.load(f)
    elem_guid_map = guid_map.get("elements", {})

    with ea_session.ea_repository(qea_path, technology="BPMN2.0") as repo:
        root = ea_session.get_model_root(repo)
        proc_arch = None
        for i in range(root.Packages.Count):
            p = root.Packages.GetAt(i)
            if p.Name == config.parent_package_name:
                proc_arch = p
                break
        if not proc_arch:
            proc_arch = root.Packages.AddNew(config.parent_package_name, "Package")
            proc_arch.Update()
            root.Update()

        proc_arch.Elements.Refresh()

        collab_elem = None
        collab_guid = guid_map.get("_collaboration_model", "")
        if collab_guid:
            try:
                collab_elem = repo.GetElementByGuid(collab_guid)
            except Exception:
                collab_elem = None
        if not collab_elem:
            for i in range(proc_arch.Elements.Count):
                e = proc_arch.Elements.GetAt(i)
                if e.Name == config.collab_name:
                    collab_elem = e
                    break

        proc_arch.Elements.Refresh()
        pkg_elems_by_name = {}
        for i in range(proc_arch.Elements.Count):
            e = proc_arch.Elements.GetAt(i)
            pkg_elems_by_name[e.Name] = e

        created_count = 0
        updated_count = 0
        object_ids = {}

        def create_element(eid, parent_elem):
            nonlocal created_count, updated_count
            elem_data = elements[eid]
            name = elem_data["fields"].get("Name", eid)
            raw_label = elem_data["label"]
            stereo = LABEL_TO_STEREO.get(raw_label, raw_label)
            obj_type = OBJECT_TYPE_MAP.get(stereo, "Class")
            notes = elem_data["fields"].get("Description", "")

            guid = elem_guid_map.get(eid, "")
            existing = None
            if guid:
                try:
                    existing = repo.GetElementByGuid(guid)
                except Exception:
                    pass
            if not existing:
                md_guid = elem_data["fields"].get("GUID", "")
                if md_guid:
                    try:
                        existing = repo.GetElementByGuid(md_guid)
                    except Exception:
                        pass
            if not existing:
                existing = pkg_elems_by_name.get(name)

            if existing:
                existing.Name = name
                existing.StereotypeEx = f"BPMN2.0::{stereo}"
                existing.Notes = notes
                if parent_elem:
                    existing.ParentID = parent_elem.ElementID
                existing.Update()
                elem_guid_map[eid] = existing.ElementGUID
                object_ids[eid] = existing.ElementID
                updated_count += 1
                pkg_elems_by_name[existing.Name] = existing
                return existing
            else:
                new_elem = proc_arch.Elements.AddNew(name, obj_type)
                new_elem.StereotypeEx = f"BPMN2.0::{stereo}"
                new_elem.Notes = notes
                if parent_elem:
                    new_elem.ParentID = parent_elem.ElementID
                new_elem.Update()
                # Capture GUID/ID BEFORE Refresh() (reference may go stale after)
                elem_guid_map[eid] = new_elem.ElementGUID
                object_ids[eid] = new_elem.ElementID
                pkg_elems_by_name[new_elem.Name] = new_elem
                created_count += 1
                return new_elem

        collab_eid = None
        for eid, elem_data in elements.items():
            if elem_data["label"] == "BPMN Collaboration":
                collab_eid = eid
                break

        if collab_eid:
            collab_elem = create_element(collab_eid, None)

        if collab_elem:
            # Pass 1: Pools, parented directly under the CollaborationModel
            for eid, elem_data in elements.items():
                if eid not in object_ids and elem_data.get("label") == "Pool":
                    create_element(eid, collab_elem)
            # Pass 2: Lanes, parented under their Pool (if any) else the CollaborationModel
            for eid, elem_data in elements.items():
                if eid not in object_ids and elem_data.get("label") == "Lane":
                    pool = get_pool_from_lane_fields(elem_data.get("fields", {}))
                    if pool and pool in object_ids:
                        parent = repo.GetElementByID(object_ids[pool])
                    else:
                        parent = collab_elem
                    create_element(eid, parent)
            # Pass 3: everything else, parented under its Lane (if resolvable) else the CollaborationModel
            for eid, elem_data in elements.items():
                if eid in object_ids:
                    continue
                lane = get_lane_from_fields(elem_data.get("fields", {}))
                if lane and lane in object_ids:
                    parent = repo.GetElementByID(object_ids[lane])
                else:
                    parent = collab_elem
                create_element(eid, parent)
            # Pass 4: anything still missed
            for eid in elements:
                if eid not in object_ids:
                    create_element(eid, collab_elem)

        # Re-run parentage fixup: Lanes -> their Pool, everything else -> its Lane
        for eid, elem_data in elements.items():
            if eid == collab_eid:
                continue
            if elem_data.get("label") == "Pool":
                continue
            if elem_data.get("label") == "Lane":
                target = get_pool_from_lane_fields(elem_data.get("fields", {}))
            else:
                target = get_lane_from_fields(elem_data.get("fields", {}))
            if target and target in object_ids:
                oid = object_ids.get(eid)
                if oid:
                    try:
                        ea_elem = repo.GetElementByID(oid)
                        target_oid = object_ids[target]
                        if ea_elem and ea_elem.ParentID != target_oid:
                            ea_elem.ParentID = target_oid
                            ea_elem.Update()
                    except Exception:
                        pass

        for eid, elem_oid in object_ids.items():
            elem_data = elements[eid]
            raw_label = elem_data["label"]
            stereo = LABEL_TO_STEREO.get(raw_label, raw_label)
            try:
                ea_elem = repo.GetElementByID(elem_oid)
            except Exception:
                try:
                    guid = elem_guid_map.get(eid, "")
                    ea_elem = repo.GetElementByGuid(guid) if guid else None
                except Exception:
                    ea_elem = None
                if not ea_elem:
                    continue
            if ea_elem:
                set_tagged_values(ea_elem, stereo, elem_data["fields"])

        print(f"Created {created_count} new element(s), updated {updated_count}")

        conn_counts = {}
        for conn_type in config.generate_connector_categories:
            conn_list = connectors.get(conn_type, [])
            if not conn_list:
                continue
            count = 0
            uml_type = CONNECTOR_TYPES[conn_type]
            stereo_ex = CONNECTOR_STEREOTYPE_EX[conn_type]
            short_stereo = CONNECTOR_STEREOTYPES_SHORT.get(conn_type, conn_type)
            for flow in conn_list:
                src_oid = object_ids.get(flow["source"])
                tgt_oid = object_ids.get(flow["target"])
                if not src_oid or not tgt_oid:
                    continue
                try:
                    src_elem = repo.GetElementByID(src_oid)
                    tgt_elem = repo.GetElementByID(tgt_oid)
                except Exception:
                    continue
                if not src_elem or not tgt_elem:
                    continue

                exists = False
                src_elem.Connectors.Refresh()
                for i in range(src_elem.Connectors.Count):
                    conn = src_elem.Connectors.GetAt(i)
                    if conn.SupplierID != tgt_elem.ElementID:
                        continue
                    cstereo = conn.StereotypeEx or conn.Stereotype or ""
                    if cstereo in (stereo_ex, short_stereo):
                        exists = True
                        if cstereo == short_stereo:
                            conn.StereotypeEx = stereo_ex
                        if flow["condition"]:
                            conn.Name = flow["condition"]
                        conn.Update()
                        break

                if not exists:
                    new_conn = src_elem.Connectors.AddNew("", uml_type)
                    new_conn.SupplierID = tgt_elem.ElementID
                    new_conn.Direction = "Unidirectional"
                    new_conn.StereotypeEx = stereo_ex
                    if flow["condition"]:
                        new_conn.Name = flow["condition"]
                    new_conn.Update()
                    count += 1
            conn_counts[conn_type] = count

        for ctype, cnt in conn_counts.items():
            if cnt:
                print(f"  Created {cnt} new {ctype}(s)")

        # Diagram
        diag = None
        diag_guid_key = config.diag_guid_key
        existing_diag_guid = guid_map.get(diag_guid_key)
        if existing_diag_guid:
            try:
                diag = repo.GetDiagramByGuid(existing_diag_guid)
            except Exception:
                diag = None

        if not diag and collab_eid:
            md_diag_guid = elements[collab_eid]["fields"].get("Diagram GUID", "")
            if md_diag_guid:
                try:
                    diag = repo.GetDiagramByGuid(md_diag_guid)
                except Exception:
                    pass

        if not diag and collab_elem:
            collab_elem.Diagrams.Refresh()
            for i in range(collab_elem.Diagrams.Count):
                d = collab_elem.Diagrams.GetAt(i)
                if d.Name == config.diagram_name:
                    diag = d
                    break

        if not diag and collab_elem:
            diag = collab_elem.Diagrams.AddNew(config.diagram_name, config.diagram_type)
            diag.Update()
            collab_elem.Update()
            guid_map[diag_guid_key] = diag.DiagramGUID
            print("  Created new diagram under CollaborationModel")

        if diag:
            # The real toolbox-selector EA uses is Diagram.StyleEx's
            # "MDGDgm=<Technology>::<StereotypeName>;" key -- NOT
            # StereotypeEx (accepted by Update() but never persists -- reads
            # back blank even in the same session) and NOT a t_xref
            # "Stereotypes" diagram-property row (persists, but doesn't
            # drive the toolbox either -- both were tried and ruled out
            # empirically, see github issue #5). Confirmed against a
            # diagram the user built correctly by hand in EA's own GUI
            # (Diagram_Type='Analysis', Stereotype=None), and confirmed
            # diag.StyleEx does persist via plain COM, unlike StereotypeEx.
            #
            # "Collaboration" (not "Business Process", the user's generic
            # hand-built test reference's own type) is used here because our
            # diagrams are each rooted in a CollaborationModel element with
            # Pools/Lanes -- the diagram's toolbox type should match what the
            # diagram actually represents, not just whichever BPMN toolbox
            # was used to first confirm the underlying mechanism worked.
            mdgdgm_value = "MDGDgm=BPMN2.0::Collaboration;"
            diag.Stereotype = ""
            diag.StereotypeEx = ""
            diag.StyleEx = mdgdgm_value
            diag.Update()

            dg_guid = diag.DiagramGUID
            if dg_guid:
                db = sqlite3.connect(qea_path)
                c = db.cursor()
                # Diagram.Type is read-only via COM once a diagram exists (raises
                # "can not be set"), so a wrong native Diagram_Type from an older
                # run can only be fixed via direct SQL. "BusinessProcess" (this
                # config's old diagram_type default) isn't a real Diagram_Type --
                # BPMN2.0's diagram stereotypes apply to "Analysis" per
                # MDGTechnologies/BPMN 2.0 Technology.xml.
                c.execute("SELECT Diagram_Type, StyleEx FROM t_diagram WHERE ea_guid=?", (dg_guid,))
                row = c.fetchone()
                if row and row[0] != "Analysis":
                    c.execute("UPDATE t_diagram SET Diagram_Type='Analysis' WHERE ea_guid=?", (dg_guid,))
                    db.commit()
                    print(f"  Corrected diagram Type to 'Analysis' (was {row[0]!r}, invalid)")
                # Also force StyleEx via SQL: COM's setter silently refuses to
                # overwrite an already-present (possibly stale/different)
                # MDGDgm value on an existing diagram -- same read-once-only
                # behavior as Type.
                if row and row[1] != mdgdgm_value:
                    c.execute("UPDATE t_diagram SET StyleEx=? WHERE ea_guid=?", (mdgdgm_value, dg_guid))
                    db.commit()
                    print(f"  Corrected StyleEx to {mdgdgm_value!r} (was {row[1]!r})")
                # Remove any stale t_xref Stereotypes row from the older,
                # incorrect fix attempt -- the verified-working reference
                # diagram has none.
                c.execute("DELETE FROM t_xref WHERE Client=? AND Type='Stereotypes' AND Visibility='diagram property'",
                          (dg_guid,))
                db.commit()
                db.close()

        # Placement: flow-aware layout for all processes (first-time and re-run)
        if diag:
            lane_ids = {eid for eid, edata in elements.items() if edata.get("label") == "Lane"}
            pool_ids = {eid for eid, edata in elements.items() if edata.get("label") == "Pool"}
            lane_order = sorted(lane_ids)
            lanes_config = [{"id": lid} for lid in lane_order]

            pool_groups = {}
            for lid in lane_order:
                pool = get_pool_from_lane_fields(elements[lid].get("fields", {}))
                if pool and pool in pool_ids:
                    pool_groups.setdefault(pool, []).append(lid)

            # sequence_flows used by the flow-layout algorithm always come from
            # config.generate_connector_categories' "SequenceFlow" bucket.
            sequence_flows = connectors.get("SequenceFlow", [])
            message_flows = connectors.get("MessageFlow", [])
            data_associations = connectors.get("DataInputAssociation", []) + connectors.get("DataOutputAssociation", [])

            all_by_lane = {}
            for eid, edata in elements.items():
                if edata.get("label") in ("Lane", "Pool"):
                    continue
                lane = get_lane_from_fields(edata.get("fields", {}))
                if lane and lane in lane_ids:
                    all_by_lane.setdefault(lane, []).append(eid)
            for lane_id in all_by_lane:
                all_by_lane[lane_id] = sort_by_flow_order(all_by_lane[lane_id], sequence_flows)

            diag.DiagramObjects.Refresh()
            existing_count = diag.DiagramObjects.Count
            if existing_count > 0 and config.reflow_on_rerun:
                print(f"  Repositioning {existing_count} diagram objects using flow layout")
                placed_ids = get_placed_ids(diag)
                eid_by_oid = {oid: eid for eid, oid in object_ids.items()}
                lane_bounds, pool_bounds = compute_bpmn_lane_positions(lanes_config, pools=pool_groups)
                elem_pos, updated_bounds = compute_bpmn_flow_layout(
                    all_by_lane, lane_bounds, sequence_flows, elem_types,
                    message_flows=message_flows, data_associations=data_associations)
                all_bounds = dict(updated_bounds)
                all_bounds.update(pool_bounds)
                moved = 0
                for i in range(existing_count):
                    dobj = diag.DiagramObjects.GetAt(i)
                    oid = dobj.ElementID
                    eid = eid_by_oid.get(oid)
                    pos = elem_pos.get(eid) if eid else None
                    if pos is None and eid:
                        pos = all_bounds.get(eid)
                    if pos:
                        l, t, r, b = pos
                        if dobj.left != int(l) or dobj.top != int(-t) or dobj.right != int(r) or dobj.bottom != int(-b):
                            dobj.left = int(l)
                            dobj.top = int(-t)
                            dobj.right = int(r)
                            dobj.bottom = int(-b)
                            dobj.Update()
                            moved += 1
                if moved:
                    print(f"  Updated positions of {moved} object(s)")
                new_ids = [eid for eid, oid in object_ids.items()
                           if eid not in lane_ids and eid not in pool_ids and oid not in placed_ids]
                if new_ids:
                    new_positions = {eid: elem_pos[eid] for eid in new_ids if eid in elem_pos}
                    added = add_missing_elements(diag, new_ids, object_ids, new_positions)
                    if added:
                        print(f"  Added {added} new element(s) to existing diagram")
            elif existing_count > 0:
                # reflow_on_rerun disabled: preserve manual layout, only add new elements
                placed_ids = get_placed_ids(diag)
                new_ids = [eid for eid, oid in object_ids.items()
                           if eid not in lane_ids and eid not in pool_ids and oid not in placed_ids]
                if new_ids:
                    lane_bounds, pool_bounds = compute_bpmn_lane_positions(lanes_config, pools=pool_groups)
                    new_by_lane = {}
                    for eid in new_ids:
                        lane = get_lane_from_fields(elements[eid].get("fields", {}))
                        if lane and lane in lane_ids:
                            new_by_lane.setdefault(lane, []).append(eid)
                    if new_by_lane:
                        elem_pos, _ = compute_bpmn_flow_layout(all_by_lane, lane_bounds, sequence_flows, elem_types,
                                                                message_flows=message_flows,
                                                                data_associations=data_associations)
                        new_positions = {eid: elem_pos[eid] for eid in new_ids if eid in elem_pos}
                        added = add_missing_elements(diag, list(new_positions.keys()), object_ids, new_positions)
                        if added:
                            print(f"  Added {added} new element(s) to existing diagram")
            else:
                print("  Placing elements on diagram (first time)")
                lane_bounds, pool_bounds = compute_bpmn_lane_positions(lanes_config, pools=pool_groups)
                elem_pos, updated_bounds = compute_bpmn_flow_layout(
                    all_by_lane, lane_bounds, sequence_flows, elem_types,
                    message_flows=message_flows, data_associations=data_associations)
                positions = dict(updated_bounds)
                positions.update(pool_bounds)
                positions.update(elem_pos)
                all_ids = list(lane_ids) + list(pool_ids) + [
                    eid for eid in elements
                    if eid not in lane_ids and eid not in pool_ids
                    and get_lane_from_fields(elements[eid].get("fields", {})) in lane_ids]
                count = create_diagram_objects(diag, all_ids, object_ids, positions)
                if count:
                    diag.Update()
                    print(f"  Placed {count} elements on diagram")

        # Line style + border-centered connector routing (all processes)
        if diag:
            try:
                diag.DiagramLinks.Refresh()
                diag.DiagramObjects.Refresh()
                pos_map = {}
                for di in range(diag.DiagramObjects.Count):
                    dobj = diag.DiagramObjects.GetAt(di)
                    pos_map[dobj.ElementID] = (dobj.left, dobj.top, dobj.right, dobj.bottom)
                link_count = diag.DiagramLinks.Count
                for i in range(link_count):
                    dl = diag.DiagramLinks.GetAt(i)
                    dl.LineStyle = 9  # Orthogonal Rounded
                    try:
                        conn = repo.GetConnectorByID(dl.ConnectorID)
                    except Exception:
                        # Orphaned DiagramLink referencing a since-deleted
                        # connector (observed after deleting a stray connector
                        # via Element.Connectors.Delete(), which does not
                        # clean up DiagramLink rows on diagrams where it was
                        # rendered) -- skip rather than abort the whole pass.
                        dl.Update()
                        continue
                    src = pos_map.get(conn.ClientID)
                    tgt = pos_map.get(conn.SupplierID)
                    path = None
                    if src and tgt:
                        cstereo = conn.StereotypeEx or conn.Stereotype or ""
                        if "MessageFlow" in cstereo:
                            path = _message_flow_path(src, tgt)
                        else:
                            path = _connector_path(src, tgt)
                    dl.Path = path or ""
                    dl.Update()
                if link_count:
                    print(f"  Set Orthogonal Rounded linestyle + centered routing on {link_count} connector(s)")
            except Exception as e:
                print(f"  [linestyle] Failed: {e}")

        if collab_elem:
            guid_map["_collaboration_model"] = collab_elem.ElementGUID
        if diag:
            guid_map[diag_guid_key] = diag.DiagramGUID
        guid_map["elements"] = elem_guid_map
        with open(guid_map_file, "w") as f:
            json.dump(guid_map, f, indent=2)

    print("Done.")


# ---------------------------------------------------------------------------
# sync_to_md(): EA -> MD
# ---------------------------------------------------------------------------

def _find_package_and_elements(c, config):
    c.execute("SELECT Package_ID FROM t_package WHERE Name=? AND Parent_ID=1", (config.parent_package_name,))
    parent_row = c.fetchone()
    if not parent_row:
        raise RuntimeError(f"'{config.parent_package_name}' package not found under Model")
    parent_pkg_id = parent_row[0]

    c.execute("SELECT Package_ID FROM t_package WHERE Name=? AND Parent_ID=?",
              (config.package_name, parent_pkg_id))
    row = c.fetchone()
    if row:
        pkg_id = row[0]
        print(f"Found sub-package '{config.package_name}' (ID {pkg_id})")
        c.execute(
            "SELECT Object_ID, Name, Object_Type, IFNULL(Stereotype, ''), "
            "IFNULL(ParentID, 0), IFNULL(Note, ''), IFNULL(ea_guid, '') "
            "FROM t_object WHERE Package_ID=? ORDER BY Name", (pkg_id,)
        )
        elements = c.fetchall()
        return pkg_id, elements

    c.execute(
        "SELECT Object_ID, Name, Object_Type, IFNULL(Stereotype, ''), "
        "IFNULL(ParentID, 0), IFNULL(Note, ''), IFNULL(ea_guid, '') "
        "FROM t_object WHERE Package_ID=? AND Stereotype='CollaborationModel' AND Name LIKE ?",
        (parent_pkg_id, config.collab_name_like)
    )
    cm_row = c.fetchone()
    if not cm_row:
        raise RuntimeError(f"No '{config.name}' CollaborationModel found in {config.parent_package_name} package")
    cm_oid = cm_row[0]
    pkg_id = parent_pkg_id
    print(f"Found CollaborationModel '{cm_row[1]}' (OID {cm_oid}) in {config.parent_package_name} package")

    all_oids = [cm_oid]
    cursor = 0
    while cursor < len(all_oids):
        c.execute("SELECT Object_ID FROM t_object WHERE ParentID=?", (all_oids[cursor],))
        for (oid,) in c.fetchall():
            if oid not in all_oids:
                all_oids.append(oid)
        cursor += 1

    oid_list = ",".join(str(oid) for oid in all_oids)
    c.execute(
        f"SELECT Object_ID, Name, Object_Type, IFNULL(Stereotype, ''), "
        f"IFNULL(ParentID, 0), IFNULL(Note, ''), IFNULL(ea_guid, '') "
        f"FROM t_object WHERE Object_ID IN ({oid_list})"
    )
    elements = c.fetchall()
    return pkg_id, elements


def _elem_label(info):
    label = BPMN_TYPE_LABEL.get(info["type"], info["type"])
    stereo = info["stereo"] or info["type"]
    if stereo and stereo != info["type"]:
        label = stereo
    return label


def _write_flat(lines, elem_by_id, parent_of, tv_by_elem, cid):
    lane_info = {}
    pool_info = {}
    for info in elem_by_id.values():
        if info["type"] == "ActivityPartition":
            if info["stereo"] == "Pool":
                pool_info[info["oid"]] = {"name": info["name"], "safe_id": safe_id(info["name"])}
            else:
                lane_info[info["oid"]] = {"name": info["name"], "safe_id": safe_id(info["name"])}

    def find_lane_ancestor(oid):
        pid = parent_of.get(oid)
        while pid and pid in elem_by_id:
            if pid in lane_info:
                return lane_info[pid]["safe_id"]
            pid = parent_of.get(pid)
        return None

    non_lane_oids = set()
    lane_oids = set(lane_info.keys())
    pool_oids = set(pool_info.keys())
    for info in elem_by_id.values():
        oid = info["oid"]
        if oid == cid or oid in lane_oids or oid in pool_oids:
            continue
        non_lane_oids.add(oid)

    ordered_oids = sorted(pool_oids, key=lambda o: elem_by_id[o]["name"].lower())
    ordered_oids += sorted(lane_oids, key=lambda o: elem_by_id[o]["name"].lower())
    ordered_oids += sorted(non_lane_oids, key=lambda o: elem_by_id[o]["name"].lower())

    eid_by_oid = {}
    eid_count = {}
    for oid in ordered_oids:
        eid = safe_id(elem_by_id[oid]["name"])
        eid_count[eid] = eid_count.get(eid, 0) + 1
    for oid in ordered_oids:
        info = elem_by_id[oid]
        eid = safe_id(info["name"])
        label = _elem_label(info)
        if eid_count[eid] > 1:
            eid_by_oid[oid] = eid + "_" + safe_id(label)
        else:
            eid_by_oid[oid] = eid

    for oid in ordered_oids:
        info = elem_by_id[oid]
        eid = eid_by_oid[oid]
        label = _elem_label(info)

        lines.append(f"### {label}—{eid}")
        lines.append(f"- Name: {info['name']}")
        lines.append(f"- Type: {info['type']}")
        if info["stereo"]:
            lines.append(f"- Stereotype: {info['stereo']}")
        lines.append(f"- GUID: {info['guid']}")

        if oid in lane_oids:
            pool_oid = parent_of.get(oid)
            if pool_oid in pool_info:
                lines.append(f"- Pool: {pool_info[pool_oid]['safe_id']}")
        elif oid not in pool_oids:
            lane_ref = find_lane_ancestor(oid)
            if lane_ref:
                lines.append(f"- Lane: {lane_ref}")

        tags_meta = BPMN_TAGGED_VALUES.get(info["stereo"], {})
        if not tags_meta:
            tags_meta = BPMN_TAGGED_VALUES.get(info["type"], {})
        elem_tvs = tv_by_elem.get(oid, {})
        for k, label_text in sorted(tags_meta.items()):
            v = elem_tvs.get(k, "")
            if v and v not in ("<memo>", ""):
                lines.append(f"- {label_text}: {v}")

        notes = info["notes"].strip()
        if notes:
            lines.append(f"- Description: {notes[:500]}")
        lines.append("")

    return eid_by_oid


def _write_hierarchical(lines, elem_by_id, children_of, tv_by_elem, cid):
    def sort_topological(oid_list):
        lane_ids = [oid for oid in oid_list if elem_by_id[oid]["type"] == "ActivityPartition"]
        other_ids = [oid for oid in oid_list if oid not in lane_ids]
        lane_ids.sort(key=lambda oid: elem_by_id[oid]["name"].lower())
        other_ids.sort(key=lambda oid: elem_by_id[oid]["name"].lower())
        return lane_ids + other_ids

    def write_element(oid, depth=0):
        info = elem_by_id[oid]
        indent = "  " * depth
        prefix = "#" * (3 + depth)
        eid = safe_id(info["name"])
        label = _elem_label(info)

        lines.append(f"{prefix} {label}—{eid}")
        lines.append(f"{indent}- Name: {info['name']}")
        lines.append(f"{indent}- Type: {info['type']}")
        if info["stereo"]:
            lines.append(f"{indent}- Stereotype: {info['stereo']}")
        lines.append(f"{indent}- GUID: {info['guid']}")

        tags_meta = BPMN_TAGGED_VALUES.get(info["stereo"], {})
        if not tags_meta:
            tags_meta = BPMN_TAGGED_VALUES.get(info["type"], {})
        elem_tvs = tv_by_elem.get(oid, {})
        for k, label_text in sorted(tags_meta.items()):
            v = elem_tvs.get(k, "")
            if v and v not in ("<memo>", ""):
                lines.append(f"{indent}- {label_text}: {v}")

        notes = info["notes"].strip()
        if notes:
            lines.append(f"{indent}- Description: {notes[:500]}")
        lines.append("")

        for child_oid in children_of.get(oid, []):
            write_element(child_oid, depth + 1)

    top_children = sort_topological(children_of.get(cid, []))
    for child_oid in top_children:
        write_element(child_oid, 0)

    free_ids = [info["oid"] for info in elem_by_id.values()
                if info["oid"] != cid
                and (info["parent"] == 0 or info["parent"] not in elem_by_id)]
    for child_oid in sorted(free_ids, key=lambda o: elem_by_id[o]["name"].lower()):
        write_element(child_oid, 0)


def sync_to_md(config, qea_path=None, md_path=None):
    qea_path = qea_path or config.default_qea
    md_path = md_path or config.default_md

    conn = sqlite3.connect(qea_path)
    c = conn.cursor()

    pkg_id, elements = _find_package_and_elements(c, config)
    print(f"Found {len(elements)} elements")

    elem_by_id = {}
    cols = ["oid", "name", "type", "stereo", "parent", "notes", "guid"]
    for e in elements:
        elem_by_id[e[0]] = dict(zip(cols, e))

    oid_list = [str(e[0]) for e in elements]
    tv_by_elem = {}
    c.execute(f"""
        SELECT Object_ID, Property, Value
        FROM t_objectproperties
        WHERE Object_ID IN ({','.join(oid_list)})
    """)
    for tv_oid, prop, val in c.fetchall():
        if val and val.strip():
            tv_by_elem.setdefault(tv_oid, {})[prop] = val.strip()

    c.execute(
        "SELECT Diagram_ID, Name, ParentID, IFNULL(ea_guid, '') "
        "FROM t_diagram WHERE Package_ID=?", (pkg_id,)
    )
    diagram_by_parent = {}
    for d_id, d_name, d_parent, d_guid in c.fetchall():
        diagram_by_parent[d_parent] = {"name": d_name, "guid": d_guid}

    c.execute(f"""
        SELECT Start_Object_ID, End_Object_ID,
               IFNULL(Stereotype, ''), IFNULL(Name, ''), IFNULL(Notes, ''),
               IFNULL(ea_guid, '')
        FROM t_connector
        WHERE Start_Object_ID IN ({','.join(oid_list)})
          AND End_Object_ID IN ({','.join(oid_list)})
        ORDER BY Connector_ID
    """)
    connectors = c.fetchall()
    print(f"  {len(connectors)} connector(s)")
    conn.close()

    parent_of = {info["oid"]: info["parent"] for info in elem_by_id.values()}
    children_of = {}
    for info in elem_by_id.values():
        pid = info["parent"]
        if pid and pid != 0 and pid in elem_by_id:
            children_of.setdefault(pid, []).append(info["oid"])
    for pid in children_of:
        children_of[pid].sort(key=lambda oid: elem_by_id[oid]["name"].lower())

    lines = []
    lines.append(f"# EAxCRM — {config.header_name}")
    lines.append("")
    lines.append(f"**Model ID**: {config.model_id}")
    lines.append(f"**Purpose**: {config.purpose}")
    lines.append("**Version**: 1.0")
    lines.append("")

    collab_ids = [info["oid"] for info in elem_by_id.values()
                  if info["stereo"] == "CollaborationModel"]

    eid_by_oid = {}
    for cid in collab_ids:
        col = elem_by_id[cid]
        ccid = safe_id(col["name"])
        notes = col["notes"].strip()

        lines.append(f"## BPMN Collaboration—{ccid}")
        lines.append(f"- Name: {col['name']}")
        lines.append(f"- GUID: {col['guid']}")
        dia = diagram_by_parent.get(cid)
        if dia:
            lines.append(f"- Diagram Name: {dia['name']}")
            lines.append(f"- Diagram GUID: {dia['guid']}")
        for k, label in sorted(BPMN_TAGGED_VALUES.get("CollaborationModel", {}).items()):
            v = tv_by_elem.get(cid, {}).get(k, "")
            if v and v not in ("<memo>", ""):
                lines.append(f"- {label}: {v}")
        if notes:
            lines.append(f"- Description: {notes[:500]}")
        lines.append("")

        if config.hierarchical_format:
            _write_hierarchical(lines, elem_by_id, children_of, tv_by_elem, cid)
        else:
            eid_by_oid.update(_write_flat(lines, elem_by_id, parent_of, tv_by_elem, cid))

    if config.hierarchical_format:
        # All configured categories combined into one "Sequence Flows" section,
        # using element names directly (matches newsletter's real behavior).
        flow_connectors = [conn for conn in connectors if conn[2] in config.sync_connector_categories]
        if flow_connectors:
            lines.append("### Sequence Flows")
            lines.append("")
            seen = set()
            for src_id, tgt_id, stereo, name, notes, guid in flow_connectors:
                key = (src_id, tgt_id, name.strip())
                if key in seen:
                    continue
                seen.add(key)
                src_name = elem_by_id.get(src_id, {}).get("name", f"ID:{src_id}")
                tgt_name = elem_by_id.get(tgt_id, {}).get("name", f"ID:{tgt_id}")
                cond = f" [{name}]" if name.strip() else ""
                lines.append(f"- {src_name} → {tgt_name}{cond}")
            lines.append("")
    else:
        def add_connector_section(stereo_filter, heading_label):
            filtered = [conn for conn in connectors if conn[2] == stereo_filter]
            if not filtered:
                return
            lines.append(f"### {heading_label}")
            lines.append("")
            seen = set()
            for src_id, tgt_id, stereo, name, notes, guid in filtered:
                key = (src_id, tgt_id, name.strip())
                if key in seen:
                    continue
                seen.add(key)
                src_eid = eid_by_oid.get(src_id, safe_id(elem_by_id.get(src_id, {}).get("name", f"ID:{src_id}")))
                tgt_eid = eid_by_oid.get(tgt_id, safe_id(elem_by_id.get(tgt_id, {}).get("name", f"ID:{tgt_id}")))
                cond = f" [{name}]" if name.strip() else ""
                lines.append(f"- {src_eid} → {tgt_eid}{cond}")
            lines.append("")

        for category in config.sync_connector_categories:
            add_connector_section(category, CATEGORY_HEADING[category])

    output = "\n".join(lines) + "\n"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Written {len(lines)} lines to {md_path}")
    print("Done.")
