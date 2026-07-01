---
name: ea-diagram-creator
description: Reference for creating and populating Sparx Enterprise Architect diagrams programmatically via COM API in EAxCRM — covers coordinate conventions, COM API gotchas, GUID map idempotency, initial diagram design phase, and BPMN diagram techniques
---

# EA Diagram Creator (EAxCRM Project Skill)

## Overview

This skill lives at **`.opencode/skills/ea-diagram-creator/SKILL.md`** in the EAxCRM project root. It replaces the global superpowers skill of the same name. All generator scripts are under **`experiments/modelgen/`**, and the shared layout utilities are in **`experiments/modelgen/diagram_utils.py`**.

**Diagram generators in this project:**

| Script | Diagram | Type | Layout |
|--------|---------|------|--------|
| `generate_archimate.py` | EAxCRM ArchiMate | Application Layer | Diagonal cascade |
| `generate_uml_datamodel.py` | EAxCRM Data Model | Logical | Diagonal cascade |
| `generate_sales_process_from_md.py` | Sales Process Architecture | BusinessProcess | BPMN lane-based |
| `generate_newsletter_process_from_md.py` | Newsletter Process Architecture | BusinessProcess | BPMN lane-based |
| `generate_requirements_from_md.py` | EAxCRM Requirements | Logical | Diagonal cascade |

## Known Failure Modes (RED Phase)

| Failure | Symptom | Root Cause |
|---------|---------|------------|
| **Positive Y** | Elements at top of diagram | Assumed Y increases downward (like screen coords). EA Y is always negative below origin at (0,0). |
| **Top < Bottom** | Elements invisible or distorted | Assumed standard rect convention (top < bottom). EA has Top > Bottom because -30 > -200. |
| **Flat hierarchy** | Elements under Package, not Lane | Created elements under the Process Architecture package instead of under Lane elements. |
| **Stale COM proxy** | Wrong GUID/ID returned | Captured ElementGUID after Refresh() instead of before; parented elements disappear from Package.Elements after Update(). |
| **SQLite writes** | Schema-locked writes, fragile | Used direct SQLite to set t_xref or Object_Type instead of COM API accessors. |
| **Diagram under Package** | Wrong tree structure | Created diagram under Package.Diagrams.AddNew() instead of CollaborationModel.Diagrams.AddNew(). |
| **No GUID map** | Duplicate elements on re-run | Didn't save/check element GUIDs, so every run created duplicates. |
| **No position preservation** | Layout reset on re-run | Deleted and re-placed all diagram objects instead of only placing new ones. |
| **Only one stereotype** | Connector not matched | Checked only short-form stereotype (SequenceFlow) without also checking long form (BPMN2.0::SequenceFlow). |
| **No design phase** | Unreadable initial layout | Placed elements in arbitrary (id) order without considering relationships or semantic groups. |

## INITIAL DIAGRAM DESIGN PHASE (CRITICAL)

**This is the most important part of this skill.** Before placing a single element on a diagram for the first time, you MUST go through a deliberate design phase.

### The Problem with the Current Approach

The current `compute_diagonal_positions()` places elements in the order they appear in the Markdown source file (id order), producing a diagonal staircase that:
- Has no semantic grouping (related elements are scattered)
- Makes connectors cross each other arbitrarily
- Provides no visual hierarchy (all elements same size regardless of type)
- Requires manual re-layout for every new diagram

### The Design Phase Process

For every first-run diagram creation, follow these steps:

#### Step 1: Analyze Element Types and Relationships

Before computing positions, group the elements:

```python
# For non-BPMN diagrams (ArchiMate, Data Model, Requirements):
element_groups = {
    "core": [],      # Central entities/actors (appear in center)
    "related": [],   # Directly connected to core
    "peripheral": [],# Less important, edge of diagram
}
# Group based on: relationship count, stereotype, name patterns
```

For data models: Core entities (Customer, Purchase, License) go in center, related entities (Contact, Quote, SalesInvoice) around them, peripheral entities (Attachment, NewsSource) at edges.

For ArchiMate: Business layer at top, Application layer middle, Technology layer bottom.

#### Step 2: Define Layout Zones

Partition the diagram canvas into zones:

```python
# Data Model zone layout (example):
#   Top-left:    Customer-related (Customer, Contact)
#   Top-right:   Sales-related (Quote, ProcurementInvoice, Purchase)
#   Center:      License & Service
#   Bottom-left: Communications
#   Bottom-right: Newsletter
```

#### Step 3: Compute Positions Per Zone

Draw each zone with its own sub-layout (grid or horizontal flow), then combine:

```python
def compute_zone_positions(elements_in_zone, zone_rect, layout="grid",
                           elem_width=180, elem_height=70, padding=30):
    """Place elements within a zone rectangle using specified layout."""
    x0, y0, x1, y1 = zone_rect
    positions = {}
    per_row = max(1, int((x1 - x0 - padding) / (elem_width + padding)))
    for idx, eid in enumerate(elements_in_zone):
        col = idx % per_row
        row = idx // per_row
        x = x0 + padding + col * (elem_width + padding)
        y = y0 + padding + row * (elem_height + padding)
        positions[eid] = (x, y, x + elem_width, y + elem_height)
    return positions
```

## EA Coordinate System

### Rules

1. **Origin (0,0) is at the top-left** of the diagram canvas
2. **X increases to the right** (standard)
3. **Y is ALWAYS negative below origin** — the origin row is the topmost visible row
4. **RectTop > RectBottom** because a value closer to zero is higher on the page (e.g., `top=-30`, `bottom=-200`: `-30 > -200`)
5. **Height = |top - bottom|** (e.g., `|-30 - (-200)| = 170`)

### Assignment Pattern (see `diagram_utils.py:80-82`)

```python
# Layout functions return (left, visual_top, right, visual_bottom)
# visual_top < visual_bottom (positive Y down)
# At COM API time, negate Y:
dobj.left = l
dobj.top = -vt      # EA: Y is always negative below origin
dobj.Update()
```

## COM API Diagram Creation Patterns

### Diagram Placement Under the Right Parent

- **BPMN diagrams** (Sales, Newsletter): Must be under the **CollaborationModel element**, NOT under the package. See `generate_sales_process_from_md.py:582-587`:
  ```python
  diag = collab_elem.Diagrams.AddNew("Sales Process Architecture", "BusinessProcess")
  ```
- **ArchiMate diagrams**: Under the **package** (`eax_pkg.Diagrams.AddNew`). See `generate_archimate.py:416`.
- **Data Model diagrams**: Under the **package** (`dm_pkg.Diagrams.AddNew`). See `generate_uml_datamodel.py:544`.
- **Requirements diagrams**: Under the **package** (`pkg.Diagrams.AddNew`). See `generate_requirements_from_md.py:339`.

### BPMN Diagram Stereotype (needs 3 things)

`StereotypeEx` alone doesn't persist BPMN stereotypes on diagrams. You must also set the short-form Stereotype:

```python
diag.Stereotype = "Collaboration"
diag.StereotypeEx = "BPMN2.0::Collaboration"
diag.Update()
```

See `generate_sales_process_from_md.py:590-612` for the full pattern with SQLite t_xref fallback.

### Refresh() Stale-Proxy Bug

When you create an element with `ParentID` set (moving it under a Lane), it disappears from the `Package.Elements` collection after `Update()`. Subsequent `Refresh()` on the collection invalidates COM proxies for elements created in the same batch.

**Always capture ElementGUID and ElementID BEFORE calling Refresh().** This pattern is used in every generator:

```python
element_guid = new_elem.ElementGUID
element_id = new_elem.ElementID
proc_arch.Elements.Refresh()
# After Refresh(), use repo.GetElementByGuid(guid) to get a fresh proxy
```

### Element Creation: 3-Pass Strategy

For BPMN models with Lanes (see `generate_sales_process_from_md.py`):

1. **Pass 1**: Create Lanes under CollaborationModel
2. **Pass 2**: Create non-Lane elements under their parent Lane (set ParentID)
3. **Pass 3**: Any missed elements (no lane) fall back to CollaborationModel

```python
# Pass 1: Create Lanes first
lane_ids = {}
for eid, data in lanes:
    new_elem = proc_arch.Elements.AddNew(data["name"], "Activity")
    lane_ids[eid] = new_elem.ElementID

# Pass 2: Create other elements under their lane
for eid, data in other_els:
    lane_eid = get_lane_for_element(data)
    parent_id = lane_ids.get(lane_eid, 0)
    new_elem = proc_arch.Elements.AddNew(data["name"], data["type"])
    new_elem.ParentID = parent_id
    # Capture GUID BEFORE Refresh()
    guid_map[eid] = new_elem.ElementGUID
```

## GUID Map Pattern for Idempotency

Each generator has its own GUID map file (see AGENTS.md):

| Generator | GUID Map File |
|-----------|---------------|
| `generate_archimate.py` | `experiments/modelgen/archimate_guid_map.json` |
| `generate_uml_datamodel.py` | `experiments/modelgen/datamodel_guid_map.json` |
| `generate_sales_process_from_md.py` | `experiments/modelgen/sales_guid_map.json` |
| `generate_newsletter_process_from_md.py` | `experiments/modelgen/newsletter_guid_map.json` |
| `generate_requirements_from_md.py` | `experiments/modelgen/requirements_guid_map.json` |

### Save/Load Pattern

```python
GUID_MAP_PATH = "experiments/modelgen/<name>_guid_map.json"

guid_map = {}
if os.path.exists(GUID_MAP_PATH):
    with open(GUID_MAP_PATH) as f:
        guid_map = json.load(f)

# Check before creating
if eid in guid_map:
    elem = repo.GetElementByGuid(guid_map[eid])
    if elem is not None:
        elem.Name = data["name"]
        elem.Update()
        continue

# Create new element
new_elem = proc_arch.Elements.AddNew(...)
guid_map[eid] = new_elem.ElementGUID

# Save after creation pass
with open(GUID_MAP_PATH, "w") as f:
    json.dump(guid_map, f, indent=2)
```

### Re-run Position Management

On re-runs, the **Newsletter generator** repositions ALL diagram objects using flow layout (see "BPMN Lane Layout → Re-run Position Management" above). Other generators only place NEW diagram objects:

```python
placed = diagram_utils.get_placed_ids(diag)
new_ids = [eid for eid in element_ids if object_ids.get(eid) not in placed]
if new_ids:
    added = diagram_utils.add_missing_elements(diag, new_ids, object_ids, positions)
```

See `get_placed_ids()` in `diagram_utils.py:58-64`.

## BPMN Connector Handling

### Stereotype Existence Check

Connectors from EA may return stereotypes in short form (`SequenceFlow`) or long form (`BPMN2.0::SequenceFlow`). Always check both:

```python
def connector_exists(connectors, src_id, tgt_id):
    for i in range(connectors.Count - 1, -1, -1):
        c = connectors.GetAt(i)
        stereo = c.Stereotype or c.StereotypeEx or ""
        if "SequenceFlow" not in stereo:  # checks both forms
            continue
        if c.ClientID == src_id and c.SupplierID == tgt_id:
            return True
    return False
```

### Connector Creation

```python
conn = connectors.AddNew("", "SequenceFlow")
conn.ClientID = src_element_id
conn.SupplierID = tgt_element_id
conn.StereotypeEx = "BPMN2.0::SequenceFlow"
conn.Update()
```

### Connector EDGE Fix (Center-Edge Attachment)

After element positions are set, force each connector's EDGE to the correct edge and add a midpoint waypoint at center-Y:

```python
diag.DiagramLinks.Refresh()
diag.DiagramObjects.Refresh()
pos_map = {}
for di in range(diag.DiagramObjects.Count):
    dobj = diag.DiagramObjects.GetAt(di)
    pos_map[dobj.ElementID] = (dobj.left, dobj.top, dobj.right, dobj.bottom)

for i in range(diag.DiagramLinks.Count):
    dl = diag.DiagramLinks.GetAt(i)
    dl.LineStyle = 9  # Orthogonal Rounded (NOT 5 — that's Tree Horizontal!)
    conn = repo.GetConnectorByID(dl.ConnectorID)
    src = pos_map.get(conn.ClientID)
    tgt = pos_map.get(conn.SupplierID)
    if src and tgt:
        srcl, srct, srcr, srcb = src
        tgtl, tgtt, tgtr, tgtb = tgt
        src_cy = (srct + srcb) / 2
        tgt_cy = (tgtt + tgtb) / 2
        if srcr <= tgtl:  # forward flow
            edge = "2"     # right edge of source
            mx = int((srcr + tgtl) / 2)
            dl.Path = f"{mx}:{int(src_cy)};"  # single midpoint at center-Y
        else:  # backward flow
            edge = "4"     # left edge of source
            mx = int((srcl + tgtr) / 2)
            dl.Path = f"{mx}:{int(src_cy)};"
        geo = dl.Geometry
        new_geo = re.sub(r'EDGE=\d', f'EDGE={edge}', geo)
        if new_geo != geo:
            dl.Geometry = new_geo
    dl.Update()
```

Key points:
- EDGE=2 means right edge, EDGE=4 means left edge (source side only)
- A single midpoint waypoint at center-Y guides EA to attach at edge centers on both ends
- Uses `LineStyle=9` (Orthogonal Rounded) — see §Diagram Object Management → Connector Rendering for the full enum
- The EDGE field in Geometry is set AFTER positions so EA uses correct relative positions

## Diagram Object Management

### Deleting Existing Objects Before Re-Place

Iterate in reverse (deletions shift indices):

```python
for i in range(diag.DiagramObjects.Count - 1, -1, -1):
    dobj = diag.DiagramObjects.GetAt(i)
    elem_id = dobj.ElementID
    if elem_id in lane_element_ids:
        continue  # Don't delete lanes
    diag.DiagramObjects.Delete(i + 1)  # 1-indexed!
```

Note: `DiagramObjects.Delete()` is 1-indexed. You cannot delete the last remaining diagram object (usually a lane survives).

### Connector Rendering (DiagramLink)

Applies to all diagram types (BPMN, ArchiMate, UML, etc.). Set on every `DiagramLink` after placing diagram objects:

```python
diag.DiagramLinks.Refresh()
for i in range(diag.DiagramLinks.Count):
    dl = diag.DiagramLinks.GetAt(i)
    dl.LineStyle = 9  # Orthogonal Rounded
    dl.Update()
```

**`LineStyle` enum values:**

| Value | Style |
|-------|-------|
| 1 | Direct |
| 2 | Auto Routing |
| 3 | Custom Line |
| 4 | Tree Vertical |
| 5 | **Tree Horizontal** (not Orthogonal Rounded — common mistake) |
| 6 | Lateral Vertical |
| 7 | Lateral Horizontal |
| 8 | Orthogonal Square |
| 9 | **Orthogonal Rounded** |

**CAUTION:** `LineStyle = 5` is Tree Horizontal, not Orthogonal Rounded. Always use `9` for Orthogonal Rounded.

Separate from `LineStyle`, the `EDGE` attribute in the Geometry string and the `Path` property control which element edge the connector attaches to (see BPMN → Connector EDGE Fix).

## BPMN Lane Layout

For BPMN diagrams with lanes, see `diagram_utils.py`.

### BPMN Element Sizes

From `diagram_utils.BPMN_ELEMENT_SIZES`:

| BPMN Type | Width | Height |
|-----------|-------|--------|
| Activity/Task | 110 | 60 |
| StartEvent/EndEvent/IntermediateEvent | 30 | 30 |
| Gateway (all variants) | 42 | 42 |
| DataObject/DataStore/Artifact | 35 | 50 |
| TextAnnotation | 80 | 50 |

### Flow Layout (`compute_bpmn_flow_layout`)

Replaces the old grid-based layout. Uses longest-path DFS placement:

1. **Row 0**: Longest acyclic path in each lane — elements placed in a straight horizontal line
2. **Row 1**: Remaining flow elements (side branches) — below their predecessor
3. **Row 2**: DataObjects — below all flow elements

**Parameters:**
- `h_gap = 60` (horizontal space between elements)
- `v_gap = 30` (vertical space between rows)
- Elements start at `lane_left + 70` (clears lane+pool double border)
- Lane width = widest lane's content width (`max_width = tw + 90` for 70px left + 20px right margin)
- All lanes are expanded to the widest lane's width so they share a uniform right edge

**Longest path algorithm (`find_longest_path`):**
- DFS with visited-set, handles cycles
- Starts from nodes with no incoming edges (and at least one outgoing)
- Returns node IDs in traversal order

### Re-run Position Management

On re-run (existing diagram), ALL elements are repositioned using flow layout, not just new ones:

```python
computing positions via compute_bpmn_flow_layout
elem_pos, updated_bounds = compute_bpmn_flow_layout(...)
for each existing diagram object:
    if eid in elem_pos:
        dobj.left = int(l)
        dobj.top = int(-t)       # Y coordinate negation
        dobj.right = int(r)
        dobj.bottom = int(-b)    # Y coordinate negation
        dobj.Update()
    elif eid in updated_bounds:
        # Also update lane bounds (width may have expanded)
```

New elements (not yet in diagram) are added after repositioning existing ones.

## Non-BPMN Layout (Diagonal Cascade — Legacy)

For non-BPMN diagrams (ArchiMate, Data Model, Requirements), `diagram_utils.py:45-55`:

```
Start position: {20, 20}
Per row: 8 elements
Step: 200 right, 200 down
Row gap: 200
Wrap after 8: reset X to column 0, continue Y with row offset
```

**This layout is a legacy fallback.** For new diagrams, use the Design Phase approach (see above) with zone-based layout instead.

## Platform-Specific Gotchas

### Python 64-bit + EA 32-bit COM Bridge
- Python 3.13 64-bit can call EA's 32-bit COM server via COM API
- Use `win32com.client.Dispatch("EA.App")` + `.Repository` instead of `Dispatch("EA.Repository")` — avoids hangs when many zombie EA processes exist
- `repo.OpenFile()` can hang if EA is in a bad state. Use try/finally with `except: pass`.
- EA processes accumulate between runs — track pre-existing PIDs and only kill your own zombies.

### NEVER Kill EA Processes Externally
```python
before_pids = set(p.Id for p in psutil.process_iter() if p.name() == "EA.exe")
# Later, only kill PIDs not in before_pids
```

Never use `Get-Process -Name EA | Stop-Process` — the user may have EA open.

## Checking Your Work

After placing diagram objects, verify coordinate correctness:

1. Every object should have negative `top` and `bottom` values
2. `top > bottom` for every object (e.g., `-30 > -200`)
3. `right > left` and `bottom < top` (both negative, `top > bottom`) — all four bounds are set per type
4. Lanes span the diagram width (left=0, right=full width)
5. Elements are grouped semantically (related elements near each other)
6. Manual verification: open diagram in EA and check visual layout

## Source Files in This Project

| File | Purpose |
|------|---------|
| `experiments/modelgen/diagram_utils.py` | Shared layout functions — diagonal cascade, BPMN lane grid, BPMN flow layout (`compute_bpmn_flow_layout`, `find_longest_path`), connector helpers |
| `experiments/modelgen/generate_archimate.py` | ArchiMate diagram generator |
| `experiments/modelgen/generate_uml_datamodel.py` | UML Data Model diagram generator |
| `experiments/modelgen/generate_sales_process_from_md.py` | Sales Process BPMN generator |
| `experiments/modelgen/generate_newsletter_process_from_md.py` | Newsletter Process BPMN generator |
| `experiments/modelgen/generate_requirements_from_md.py` | Requirements diagram generator |
| `experiments/modelgen/sync_datamodel_from_ea.py` | Reads EA data model back to MD |
| `experiments/modelgen/sync_sales_process_from_ea.py` | Reads EA sales process back to MD |
| `experiments/modelgen/sync_newsletter_process_from_ea.py` | Reads EA newsletter process back to MD |
| `experiments/modelgen/sync_requirements_from_ea.py` | Reads EA requirements back to MD |
