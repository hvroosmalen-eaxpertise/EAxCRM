# Diagram Object Placement Implementation Plan

> **For agentic workers:** Inline execution. Steps use checkbox syntax.

**Goal:** Centralize diagram placement into `diagram_utils.py`, implement BPMN lane layout, diagonal cascade layout, add-missing-element detection for all generators, and create Sales Process generator.

**Architecture:** A shared `diagram_utils.py` module with layout computation and diagram management functions. All 5 generators consume it. No position round-tripping through MD.

**Tech Stack:** Python 3.13, EA COM API (win32com), win32com.client.Dispatch("EA.Repository")

## Global Constraints

- No TDD for EA COM API code (no test framework available for win32com)
- Never use SQLite writes to EA (hard rule from AGENTS.md)
- BPMN2.0 MDG must be activated via `repo.ActivateTechnology("BPMN2.0")` before element/connector creation
- `repo.CloseFile()` may hang — use try/finally with except: pass
- COM API `Object_Type` is read-only on existing elements — only set at creation
- Diagram GUIDs stored in `newsletter_guid_map.json`, `archimate_guid_map.json`, etc.

---
## Files

| File | Action | Responsibility |
|---|---|---|
| `experiments/modelgen/diagram_utils.py` | Create | Centralized layout + diagram management |
| `experiments/modelgen/generate_newsletter_process_from_md.py` | Modify | BPMN layout via utils, add re-run detection |
| `experiments/modelgen/generate_sales_process_from_md.py` | Create | Sales Process MD→EA generator |
| `experiments/modelgen/generate_uml_datamodel.py` | Modify | Diagonal layout via utils |
| `experiments/modelgen/generate_requirements_from_md.py` | Modify | Diagonal layout via utils |
| `experiments/modelgen/generate_archimate.py` | Modify | Add re-run new-element detection + diagonal layout |
| `models/EAxCRM-NewsletterProcess.md` | Modify | Add `- Lane:` fields to all elements |
| `models/EAxCRM-SalesProcess.md` | Create | Sales Process BPMN spec |
| `experiments/modelgen/newsletter_guid_map.json` | Modify | May be regenerated (backwards compatible) |

### Task 0: Create `diagram_utils.py`

**Create:** `experiments/modelgen/diagram_utils.py`

**Interfaces (module-level functions):**

```python
def compute_bpmn_lane_positions(lanes, lane_height=500, lane_width=1000, gap=250):
    """Returns {lane_id: (left, top, right, bottom)}"""

def compute_bpmn_element_positions(elements_by_lane, lane_bounds,
                                    elem_width=180, elem_height=70,
                                    h_gap=30, v_gap=30):
    """Returns {element_id: (left, top, right, bottom)} — 4 per row inside each lane"""

def compute_diagonal_positions(element_ids, per_row=8, step=200, row_gap=200,
                                elem_width=180, elem_height=120):
    """Returns {element_id: (left, top, right, bottom)} — diagonal cascade"""

def get_placed_ids(diag):
    """Returns set of ElementIDs already on the diagram from DiagramObjects collection"""

def add_missing_elements(diag, element_ids, object_ids, positions):
    """Creates DiagramObjects for ElementIDs not yet placed. Returns count added."""

def create_diagram_objects(diag, element_ids, object_ids, positions):
    """Creates DiagramObjects for all given element_ids at specified positions. Returns count."""

def get_lane_from_fields(fields):
    """Returns lane_id from element's fields dict, or None"""
```

- [ ] **Create `diagram_utils.py`** — Implement all functions

```python
"""
Shared diagram layout utilities for EA COM API generators.
"""
import pythoncom
from win32com.client import Dispatch


def compute_bpmn_lane_positions(lanes, lane_height=500, lane_width=1000, gap=250):
    positions = {}
    y = 30
    for lane in lanes:
        lid = lane.get("id") or lane.get("eid")
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


def _create_single_diagram_object(diag, element_id, pos, repo):
    l, t, r, b = pos
    dobj = diag.DiagramObjects.AddNew("", "")
    dobj.ElementID = element_id
    dobj.left = l
    dobj.top = t
    dobj.right = r
    dobj.bottom = b
    dobj.Update()


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
        _create_single_diagram_object(diag, oid, pos)
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
        _create_single_diagram_object(diag, oid, pos)
        count += 1
    if count:
        diag.Update()
    return count


def get_lane_from_fields(fields):
    return fields.get("Lane") or fields.get("lane") or None
```

- [ ] **Commit**

```bash
git add experiments/modelgen/diagram_utils.py
git commit -m "feat: create diagram_utils.py with shared layout functions"
```

### Task 1: Update Newsletter Generator

**Modify:** `experiments/modelgen/generate_newsletter_process_from_md.py`

- [ ] **Remove hardcoded `pos` dict and `draw_order` list** (lines 550-588)
- [ ] **Import diagram_utils** at top of file
- [ ] **Replace first-time placement** — compute lane positions + element positions via utils
- [ ] **Add re-run new-element detection** — get_placed_ids, find missing, compute append positions
- [ ] **Read `- Lane:` field** from parsed element fields

Replace the placement section (lines 539-605) with:

```python
# Place diagram objects only if this is a fresh diagram (no objects yet)
if diag:
    diag.DiagramObjects.Refresh()
    existing_count = diag.DiagramObjects.Count
    if existing_count > 0:
        print(f"  Diagram has {existing_count} objects, preserving positions")
        # Add any new elements not yet on the diagram
        placed = diagram_utils.get_placed_ids(diag)
        new_ids = [eid for eid in element_ids
                   if eid not in placed
                   and eid not in ("eaxpertise", "newssource")]
        if new_ids:
            # Build lane membership for new elements
            new_by_lane = {}
            for eid in new_ids:
                lane = diagram_utils.get_lane_from_fields(elements[eid].get("fields", {}))
                if lane:
                    new_by_lane.setdefault(lane, []).append(eid)
            if new_by_lane:
                existing_lane_positions = diagram_utils.compute_bpmn_lane_positions(
                    [{"id": "eaxpertise"}, {"id": "newssource"}])
                existing_bounds = {}
                for i in range(diag.DiagramObjects.Count):
                    dobj = diag.DiagramObjects.GetAt(i)
                    existing_bounds[dobj.ElementID] = (dobj.left, dobj.top, dobj.right, dobj.bottom)
                new_positions = {}
                for lane_id, eids in new_by_lane.items():
                    # Find elements already in this lane to compute append offset
                    lane_oids = [oid for eid, oid in object_ids.items()
                                 if diagram_utils.get_lane_from_fields(
                                     elements.get(eid, {}).get("fields", {})) == lane_id
                                 and oid in placed]
                    lane_elem_ids = [eid for eid, oid in object_ids.items() if oid in lane_oids]
                    # Append after existing lane elements
                    lane_bounds = existing_lane_positions.get(lane_id, (0, 0, 1000, 500))
                    all_lane_elements = lane_elem_ids + eids
                    all_positions = diagram_utils.compute_bpmn_element_positions(
                        {lane_id: all_lane_elements}, {lane_id: lane_bounds})
                    for eid in eids:
                        new_positions[eid] = all_positions[eid]
                added = diagram_utils.add_missing_elements(diag, new_ids, object_ids, new_positions)
                if added:
                    print(f"  Added {added} new element(s) to existing diagram")
    else:
        print("  Placing elements on diagram (first time)")
        # Lane positions
        lanes_config = [{"id": "eaxpertise", "name": "EAxpertise"},
                        {"id": "newssource", "name": "News Source"}]
        lane_bounds = diagram_utils.compute_bpmn_lane_positions(lanes_config)
        # Group elements by lane
        elements_by_lane = {"eaxpertise": [], "newssource": []}
        for eid, edata in elements.items():
            lane = diagram_utils.get_lane_from_fields(edata.get("fields", {}))
            if lane in elements_by_lane:
                elements_by_lane[lane].append(eid)
            else:
                print(f"  Warning: {eid} has no lane assignment, skipping diagram placement")
        # Compute positions
        lane_element_bounds = {}
        for lid, lane_b in lane_bounds.items():
            lane_element_bounds[lid] = lane_b
        lane_positions = diagram_utils.compute_bpmn_element_positions(
            elements_by_lane, lane_element_bounds)
        # Add lane positions
        for lid, lb in lane_bounds.items():
            lane_positions[lid] = lb
        all_element_ids = ["eaxpertise", "newssource"] + [
            eid for eid in elements if eid not in ("eaxpertise", "newssource")]
        count = diagram_utils.create_diagram_objects(diag, all_element_ids, object_ids, lane_positions)
        print(f"  Placed {count} elements on diagram")
        diag.Update()
```

- [ ] **Commit**

```bash
git add experiments/modelgen/generate_newsletter_process_from_md.py
git commit -m "feat: newsletter generator uses diagram_utils, re-run adds new elements"
```

### Task 2: Update Data Model Generator

**Modify:** `experiments/modelgen/generate_uml_datamodel.py`

- [ ] **Import diagram_utils**
- [ ] **Replace first-time placement** — use `compute_diagonal_positions()`
- [ ] **Replace re-run placement** — use `add_missing_elements()` with diagonal positions

Replace the grid constant block and placement code. The first-time block becomes:

```python
# Compute diagonal positions
eid_list = [ent["id"] for ent in entities]
positions = diagram_utils.compute_diagonal_positions(eid_list,
    per_row=8, step=200, row_gap=200, elem_width=200, elem_height=120)
count = diagram_utils.create_diagram_objects(diag, eid_list, object_ids, positions)
print(f"  Placed {count} entities on diagram")
```

Re-run block becomes:

```python
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
```

- [ ] **Commit**

```bash
git add experiments/modelgen/generate_uml_datamodel.py
git commit -m "feat: data model generator uses diagram_utils diagonal layout"
```

### Task 3: Update Requirements Generator

**Modify:** `experiments/modelgen/generate_requirements_from_md.py`

Same changes as Task 2 but use `elem_width=220, elem_height=100`.

- [ ] **Import diagram_utils**, replace grid with diagonal
- [ ] **Commit**

### Task 4: Update ArchiMate Generator

**Modify:** `experiments/modelgen/generate_archimate.py`

- [ ] **Import diagram_utils**
- [ ] **Replace first-time layer-row layout** with diagonal layout
- [ ] **Add re-run new-element detection** (currently missing entirely)

```python
# In Phase 3, first-time creation:
eid_list = [el["id"] for el in elements]
positions = diagram_utils.compute_diagonal_positions(eid_list,
    per_row=8, step=200, row_gap=200, elem_width=180, elem_height=100)
count = diagram_utils.create_diagram_objects(diag, eid_list, object_ids, positions)
print(f"  Placed {count} elements in diagram")

# Re-run:
placed = diagram_utils.get_placed_ids(diag)
new_els = [el for el in elements if object_ids.get(el["id"]) not in placed]
if new_els:
    new_ids = [el["id"] for el in new_els]
    new_positions = diagram_utils.compute_diagonal_positions(new_ids,
        start_index=len(placed), per_row=8, step=200, row_gap=200,
        elem_width=180, elem_height=100)
    added = diagram_utils.add_missing_elements(diag, new_ids, object_ids, new_positions)
    print(f"  Added {added} new element(s) to existing diagram")
else:
    print("  Diagram already has all elements — preserving manual layout")
```

Note: remove the `LAYER_Y` dict, `layer_counters`, and old placement loop.

- [ ] **Commit**

### Task 5: Add Lane Fields to Newsletter MD

**Modify:** `models/EAxCRM-NewsletterProcess.md`

- [ ] **Add `- Lane: eaxpertise`** to all EAxpertise-lane elements (gateways, activities, events, data objects that belong to the EAxpertise team)
- [ ] **Add `- Lane: newssource`** to News Source elements (scheduledscrape, scrapearticles, etc.)

Current lane membership (from existing hardcoded `pos` dict):
**EAxpertise:** startnewsletter, checkcadence, 6weekselapsed, browseavailablearticles, selectarticles, selectedarticles, composenewsletter, newsletterdraft, submitforreview, reviewapproved, approvednewsletter, sendnewsletter, contactlist, sentnewsletter, newslettersent

**News Source:** scheduledscrape, fetchurllist, urllist, scrapearticles, extractheadingsandsummaries, articlepool, storenewarticles, scrapecomplete

- [ ] **Commit**

### Task 6: Create Sales Process MD

**Create:** `models/EAxCRM-SalesProcess.md`

- [ ] Extract sales CollaborationModel data from EA using a sync query, write to dedicated MD
- [ ] Add `- Lane:` fields to all elements (Customer, eaxpertise, vendor)
- [ ] Min scope: CollaborationModel, 3 Lanes, ~28 elements, SequenceFlows
- [ ] **Commit**

### Task 7: Create Sales Process Generator

**Create:** `experiments/modelgen/generate_sales_process_from_md.py`

- [ ] Copy newsletter generator structure, adapt for Sales Process
- [ ] 3 Lanes: Customer, EAxpertise, Vendor
- [ ] BPMN layout via `diagram_utils`
- [ ] Same first-time + re-run pattern as newsletter generator
- [ ] Use `sales_guid_map.json`
- [ ] **Commit**

### Task 8: Update AGENTS.md

- [ ] Document `diagram_utils.py` module
- [ ] Document changed generator behavior
- [ ] Add Sales Process generator to the list
- [ ] **Commit**

### Task 9: Push

- [ ] `git push`
