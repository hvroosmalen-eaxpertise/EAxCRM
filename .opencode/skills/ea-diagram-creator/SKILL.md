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
| `generate_customeraccount_process_from_md.py` | Manage Customer Account | BusinessProcess | BPMN flow layout |
| `generate_sales_process_from_md.py` | Sales Process Architecture | BusinessProcess | BPMN flow layout |
| `generate_newsletter_process_from_md.py` | Newsletter Process Architecture | BusinessProcess | BPMN flow layout |
| `generate_requirements_from_md.py` | EAxCRM Requirements | Logical | Diagonal cascade |

**BPMN engine refactor (2026-07-05, issue #3):** the 3 BPMN generate scripts
and their matching `sync_*_process_from_ea.py` scripts are now thin
config + CLI wrappers (~15 lines each) around a shared
`experiments/modelgen/bpmn_config.py` (per-process `ProcessConfig`
dataclass instances + shared BPMN vocabulary constants) and
`experiments/modelgen/bpmn_engine.py` (`parse_md`, `generate`, `sync_to_md`,
and the BPMN-only layout functions moved out of `diagram_utils.py`). See
`docs/superpowers/specs/2026-07-03-bpmn-config-driven-engine-design.md` for
the design. `diagram_utils.py` keeps only the non-BPMN layout functions
(ArchiMate/UML Data Model/Requirements still use it directly).

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
| **Compounding row jump** | New elements placed thousands of px away | `compute_diagonal_positions`' row-jump formula multiplied by `per_row * step`, not just `elem_height`. Use `compute_grid_positions` for non-BPMN diagrams instead. |
| **One flat size for every type** | Node/Interface/Component rendered as generic boxes | Passed one hardcoded `elem_width`/`elem_height` to every element regardless of Object_Type. Use `type_sizes=DEFAULT_ELEMENT_SIZES` with `compute_grid_positions`. |
| **Position-only placement (no size)** | Diagram opens empty — 0×0 invisible elements, only connector lines visible | Assumed EA auto-sizes a `DiagramObject` if `right`/`bottom` are left unset. Confirmed false via a full live run + GUI check: explicit, type-appropriate bounds are always required for non-BPMN diagrams too. |
| **"Sandbox" package ≠ isolation** | A sandbox dry-run silently modified the real, live diagram instead of test data | `repo.GetElementByGuid()` resolves repo-wide, ignoring target package. Source MD embeds real GUIDs from a prior sync. Must strip `- GUID:` fields from a temp MD copy (or use synthetic data) for genuine isolation — see "Use a Sandbox Package" below. |
| **Reflow leaves stale connector Path** | Diagonal lines cutting through the diagram after boxes move | `DiagramLink.Path` holds absolute waypoints computed for the *old* positions; EA does not recompute it when a box moves via COM. Must explicitly recompute/clear `Path` whenever positions change. |
| **`.Geometry`'s `EDGE` field does nothing alone** | Setting `EDGE=N` in the Geometry string had zero visible effect on rendered routing | Routing is controlled by `DiagramLink.Path` (absolute waypoints), not `.Geometry`. See "Connector Routing" below. |
| **Orphaned DiagramLink after deleting a connector** | `repo.GetConnectorByID(dl.ConnectorID)` throws EA's internal error 61704 (not transient — happens every time) while iterating `diag.DiagramLinks` | Deleting a connector via `Element.Connectors.Delete(index)` does not clean up `t_diagramlinks` rows on diagrams where that connector was rendered — the row survives with a `ConnectorID` pointing at nothing. `diag.DiagramLinks.Delete(index)` also fails to remove it (its own delete path needs to resolve the same dangling connector). Confirm via SQLite (`SELECT COUNT(*) FROM t_connector WHERE Connector_ID=?` returns 0) then delete the single orphaned row directly: `DELETE FROM t_diagramlinks WHERE DiagramID=? AND ConnectorID=?` — same accepted-exception category as the diagram-stereotype `t_xref` fallback. `bpmn_engine.py`'s linestyle/routing loop now wraps `GetConnectorByID` in try/except and skips gracefully instead of aborting the whole pass. |

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

Each generator has its own GUID map file (see AGENTS.md). For the 3 BPMN
processes, the map filename lives in `bpmn_config.py`'s per-process
`ProcessConfig.guid_map_file` field rather than a per-script constant:

| Generator | GUID Map File |
|-----------|---------------|
| `generate_archimate.py` | `experiments/modelgen/archimate_guid_map.json` |
| `generate_uml_datamodel.py` | `experiments/modelgen/datamodel_guid_map.json` |
| Customer Account (`bpmn_config.CUSTOMER_ACCOUNT`) | `experiments/modelgen/customeraccount_guid_map.json` |
| Sales (`bpmn_config.SALES`) | `experiments/modelgen/sales_guid_map.json` |
| Newsletter (`bpmn_config.NEWSLETTER`) | `experiments/modelgen/newsletter_guid_map.json` |
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

### Connector Routing — Border-Centered Attachment (rewritten 2026-07-05)

**`DiagramLink.Path` controls rendered routing — `.Geometry`'s `EDGE` field
does not, by itself.** Confirmed empirically: setting only `.Geometry`'s
`EDGE` substring (with `Path` untouched/empty) produced zero visible change
across several trials. All routing control happens through `Path`'s absolute
waypoint coordinates; `Geometry` is metadata (label positions, etc.) that can
be left alone.

The general rule, verified against a user-provided manual reference edit in
EA's GUI: **classify the relationship by Y-overlap first, not X-overlap.**
Two boxes can end up X-disjoint (one entirely left/right of the other in raw
coordinate terms) purely as a side effect of some other positioning choice
(e.g. centering a branch under its logical successor) even when the
*dominant* visual relationship is vertical (above/below). Checking X first
misclassifies that case as a horizontal connector.

```python
def _connector_path(src, tgt):
    """src/tgt: (left, top, right, bottom) in EA's raw DiagramObject
    convention (top/bottom negative, more-negative = lower on the page).
    Returns a Path waypoint string, or None to let EA auto-route (boxes
    overlap in both axes)."""
    sl, st, sr, sb = src
    tl, tt, tr, tb = tgt
    scx, scy = (sl + sr) / 2, (st + sb) / 2
    tcx, tcy = (tl + tr) / 2, (tt + tb) / 2

    y_disjoint = tt <= sb or tb >= st
    x_disjoint = tl >= sr or tr <= sl

    if y_disjoint:
        # Target above/below: exit source's top/bottom-center, bend at the
        # target's own vertical center, enter its left/right-center (or
        # straight into its top/bottom-center if horizontally aligned).
        return f"{int(scx)}:{int(tcy)};"
    if x_disjoint:
        # Target beside (roughly same row): single waypoint at the source's
        # own vertical center produces a clean side-to-side route.
        mx = (sr + tl) / 2 if tl >= sr else (sl + tr) / 2
        return f"{int(mx)}:{int(scy)};"
    return None

# Applied to every DiagramLink, every run:
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
    src, tgt = pos_map.get(conn.ClientID), pos_map.get(conn.SupplierID)
    dl.Path = (_connector_path(src, tgt) or "") if src and tgt else ""
    dl.Update()
```

This replaces an earlier, narrower version of this fix that only handled the
horizontal case (single waypoint at source's center-Y) and used
`.Geometry`'s `EDGE` substring for the vertical/gateway-branch case — that
older approach never actually worked (see above), which is how the bug
survived until a user manually fixed one connector in the GUI and asked for
the fix to become the default. See `bpmn_engine.py::_connector_path` for the
canonical implementation, applied unconditionally on every `generate()` run
(not gated behind a per-process flag — this is default BPMN diagram
behavior, not a one-off customization).

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

For BPMN diagrams with lanes, see `bpmn_engine.py` (BPMN-only layout functions
moved here from `diagram_utils.py`, 2026-07-05).

### Pool Support (verified 2026-07-05, synthetic test)

Pool → one or more Lanes → flow elements (a Pool never directly contains flow
elements). A `### Lane—...` entry declares its parent Pool via `- Pool:
<pool-eid>`, mirroring how flow elements declare `- Lane:`. Verified
end-to-end with a synthetic 2-lane-1-pool + cross-lane MessageFlow fixture
(no real process MD uses Pool yet):
- `compute_bpmn_lane_positions(..., pools={pool_id: [lane_id, ...]})` groups
  same-pool lanes into one stacked column wrapped in a pool bounding box —
  confirmed the pool box correctly encloses both lanes.
- The Pool/Lane stereotype-override in both MD writers (`if stereo and
  stereo != info["type"]: label = stereo`) already round-trips a Pool as
  `### Pool—...` correctly (not mislabeled `Lane—`, since `Pool`'s
  stereotype differs from its base EA type `ActivityPartition`) — this was
  suspected as a risk during design but turned out to be a non-issue; no
  code change was needed, only the round-trip check to confirm it.
- Cross-**lane** MessageFlow alignment (see "MessageFlow-aware alignment"
  below) applies generally, not just cross-**pool** — a message flow between
  two lanes of the *same* pool got the same clean vertical-alignment
  treatment automatically, no Pool-specific code needed.

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

Now the **default layout for all 3 BPMN processes** (2026-07-05 — previously
Newsletter-only; Customer Account/Sales used a simpler grid packer that never
separated genuine gateway forks, silently overlapping siblings).

**Row-per-flow structure (2026-07-05, explicit user rule):** "A Start Event
must be placed in the left hand column and from there sequence flows go to
the right from activity to activity (or gateway or other elements).
DataObjects and DataStores are always living in their own row [below or
above the rows with activities]." Concretely, per lane:

1. Find the **connected components** of the lane's sequence-flow graph
   (undirected — a fork and its branches, or a merge and its inputs, are one
   component even though the edges are directed). Each component is one
   independent flow (typically rooted at its own StartEvent, though the rule
   applies to any component with no single shared entry point too).
2. **Each component becomes its own row**, stacked vertically in the lane, in
   MD-declaration order: within a row, the longest acyclic path is placed in
   a straight horizontal line **starting at the lane's left column**
   (`lane_left + 70`) and flowing rightward — see `_place_component_row`.
3. **Gateway forks within one row do NOT start a new row** — they stack
   below/near the fork point within that same row's vertical space (see
   branch handling below). The left-column rule is about independent flows,
   not alternate paths within one flow — confirmed via explicit user
   clarification.
4. Branch handling *within* a row's flow (elements not on that row's own
   longest path) — three passes, in this order because later passes may
   depend on positions the earlier ones establish:
   1. **Gateway-fork groups**: elements whose predecessor is on the row's
      main path stack in one vertical column, below that row, centered under
      the gateway's **main-path successor** (not the gateway itself — a
      gateway diamond is narrow, so centering a wide activity box under it
      looks cramped; centering under the wider neighboring activity looks
      balanced). Confirmed via user feedback + visual (`SaveDiagramImageToFile`)
      verification.
   2. **Chain continuation (generalized 2026-07-05)**: any element — not
      just Events, any type — that is the sole successor of a predecessor
      which in turn has only that one child continues that predecessor's row
      horizontally, same vertical center, immediately to its right, instead
      of dropping to a new row below. Applied repeatedly (not just one hop),
      so an entire multi-element branch chain flows left-to-right after its
      first activity, matching the explicit user rule: "with a gateway split
      the elements of the branch go down and flow left to right again after
      the first activity." (Originally this only covered a lone Event
      continuing a chain — "I like events in line with elements and not
      underneath" — then generalized once the same left-to-right expectation
      was stated for branches in general.) Restricted to elements with
      exactly one predecessor total, so a genuine merge point (2+
      predecessors) is never accidentally inlined off just one of its
      incoming edges — it goes through Pass 3's merge-point handling instead.
   3. **Chained remainder / merge points**: anything still unplaced stacks
      below its predecessor(s)' actual bottom edge + gap (see merge-point
      handling below for the multi-predecessor case).
5. **DataObjects/DataStores**: always their own row, below all flow rows in
   the lane (never a fixed row-count offset — see below).

**Parameters:**
- `h_gap = 60` (horizontal space between elements)
- `v_gap = 30` (vertical space between rows within one flow; `v_gap * 2`
  between independent flow rows)
- Elements start at `lane_left + 70` (clears lane+pool double border)
- Lane width = widest lane's *actual placed content* width (computed after
  all rows are placed, not from a single longest-path estimate — a lane can
  now have several rows of differing width)
- All lanes are expanded to the widest lane's width so they share a uniform
  right edge

**MessageFlow-aware alignment (2026-07-05, explicit user rule):** "A
MessageFlow normally crosses to an element in another lane... it starts in
the middle top or bottom center of an activity and ends in the center bottom
or top of the receiving activity — both elements are center aligned to each
other in their own lane/pool." Pass `message_flows=[...]` (same `{"source":
eid, "target": eid}` shape as `sequence_flows`) to `compute_bpmn_flow_layout`
to enable this:
- Lanes are processed **top-to-bottom** (by `lane_bounds[lid][1]`) instead of
  input order, so a receiving lane's elements can align to an
  already-placed sending lane's elements.
- For each component, if its **leading element** (the first element on its
  own longest path) is the source or target of a cross-lane MessageFlow to/
  from an element already placed in an earlier-processed lane, the whole row
  is horizontally shifted so that leading element is **centered** on the
  partner's X — see `_place_component_row`'s `preferred_cx` parameter.
- Scoped to the row's leading element only — a MessageFlow received
  mid-chain does not reposition the row. This covers the common BPMN pattern
  (a message-triggered start event/task) but not arbitrary mid-flow message
  reception.
- Verified against Sales' real `Create RFQ → Confirm Customer Account`
  MessageFlow: both ended up with `cx=215.0` exactly.

**MessageFlow connector routing is a separate rule from position, and from
`_connector_path`'s generic vertical case** (2026-07-05, explicit user
rule): "if a message flow starts at the bottom it should end in the
receiving activity's top, and vice versa." Use `_message_flow_path(src,
tgt)` instead of `_connector_path` whenever the connector's stereotype
contains `"MessageFlow"` (checked in the line-style/routing loop via
`conn.StereotypeEx or conn.Stereotype`):
- Always exits/enters **top or bottom-center on both ends, never a side** —
  unlike `_connector_path`'s generic vertical case, which enters the
  target's *side* when the boxes aren't X-aligned (the right call for a
  sequence-flow branch, which reads as a sideways continuation, but wrong
  for a MessageFlow, which reads as a cross-lane/pool crossing).
- Uses a 2-waypoint elbow (bend at the midpoint between the two boxes) when
  the boxes aren't X-aligned; collapses to a single straight vertical line
  when they are (the common case once the position-alignment above has run).
- These two rules compose: position-alignment (above) makes the common case
  X-aligned so the connector is a straight line; `_message_flow_path`
  guarantees a correct top/bottom-only look even for the remaining
  mid-chain-reception cases position-alignment doesn't cover.

**DataObject/DataStore alignment (2026-07-05, explicit user rule):**
"DataObjects and DataStore live in their own row. They are positioned above
or below the activity they are connected to, which can exist in another
lane/pool. The connector preferably has no bends." Since lanes are fixed,
non-overlapping vertical bands, a DataObject can never actually leave its
own lane's row regardless of which lane its connected activity is in — user
confirmed the practical rule: DataObjects stay in their existing dedicated
row below the flow rows in their own lane, but are horizontally **centered
on their connected activity's X** (via `DataInputAssociation`/
`DataOutputAssociation`, passed as `data_associations=[...]` to
`compute_bpmn_flow_layout`, same `{"source": eid, "target": eid}` shape as
`sequence_flows`), wherever that activity ended up, even in another lane —
so the connector is a straight line with no bends, same principle as the
MessageFlow position-alignment above. Placed in a pass after ALL lanes'
flow elements are placed (not interleaved per-lane), so the connected
activity's position is always known regardless of lane processing order.

**Shared-target overlap (fixed 2026-07-05):** two DataObjects connected to
the *same* (or nearby) activity computed the *same* preferred center-X
independently and landed exactly on top of each other. Fix: cascade —
prefer the aligned X, but never place further left than the current packing
pointer (`xp`), so a second DataObject sharing a target's X stacks
immediately to the right of the first instead of overlapping it. This is
the same "shared anchor, must not collide" pattern as the gateway-fork
sibling-stacking fix earlier in this section, applied to DataObjects too.

**Longest path algorithm (`find_longest_path`):**
- DFS with visited-set, handles cycles
- Starts from nodes with no incoming edges (and at least one outgoing),
  scoped to one connected component (not the whole lane)
- Returns node IDs in traversal order

**Overlap bug (fixed 2026-07-03):** when a branch element's predecessor is
*itself* another branch element (not on the main path) rather than a
main-path element, placing it in the same shared row band as its predecessor
nests it inside the predecessor's box. Fix: if the predecessor is on the main
path, use the shared row band; if the predecessor is itself a branch
element, stack below that element's *actual* bottom edge (`pos[p][3] +
v_gap`), not the row's shared y.

**Further overlap classes found on Sales (2026-07-05) — Customer Account's
single-fork structure never exercised these:**
- **Multiple siblings sharing one predecessor** (a real fork: predecessor
  has 2+ children, none of which is itself on the main path) all computed
  `pos[p][3] + v_gap` independently and landed on top of each other, since
  `pos[p]` (the shared parent's own box) never changes just because a
  sibling got placed near it. Fix: track `next_y_for_pred = {}` — each time
  a child of `p` is placed, advance `next_y_for_pred[p]` to below that
  child, so the next sibling stacks under the previous one, not the parent.
- **DataObjects row used a fixed `2 * (row_h + v_gap)` offset**, assuming
  the branch-stacking section above it only ever needed one row's worth of
  height. With siblings/chains now stacking multiple levels deep, that
  fixed offset placed DataObjects on top of a tall stack instead of below
  it. Fix: compute the DataObjects row's start from the actual max bottom
  used by the branch section, not a row-count constant.
- **A fixed per-branch-row Y constant caused *unrelated* collisions**:
  an independent "island" (its own disconnected StartEvent chain sharing no
  predecessor with anything else) and a gateway-fork group could both start
  at the same `lt + row_h + v_gap` baseline and collide if their X ranges
  happened to overlap. Fix: recompute the fallback Y *dynamically*, each
  time an island root needs placement, from the actual current max bottom
  across everything already placed in that lane's branch section — not a
  one-time snapshot (a snapshot taken once misses elements placed by later
  iterations of the same pass).
- **Merge points (an element with 2+ predecessors, e.g. two branches
  rejoining into one activity) resolved position using only the *first*
  predecessor found**, ignoring that a later, lower sibling might already
  occupy that spot. Fix: when 2+ predecessors are already placed, clear the
  *max* of all their bottoms, not just the first one's.
- **DFS traversal order can place a merge point before all its predecessors
  exist**: DFS fully explores one branch (predecessor A → the merge point)
  before backtracking to sibling branch (predecessor B), so the merge point
  gets positioned using only A, and B's later placement doesn't retroactively
  fix it. Fix: after the main placement pass, run a correction pass over
  every element with 2+ predecessors and re-clear against the now-complete
  predecessor set, moving it deeper if needed.
- **Lane height is a fixed guess (`lane_height=500` default) computed
  *before* content is placed.** Deep stacking from any of the above can push
  a lane's actual content past that guess, bleeding into the next lane's
  allocated space. Fix: a post-processing pass (after all lanes are placed)
  walks lanes top-to-bottom, and if a lane's actual content bottom exceeds
  its allocated bottom, shifts every subsequent lane (and everything already
  placed in it) down by the overflow.

All of these were found and fixed by writing a **pure-Python overlap
checker** (no EA/COM needed — just call `compute_bpmn_flow_layout` directly
and check pairwise bounding-box intersection) against Sales' real MD, then
verified end-to-end via a GUID-stripped Sandbox run + `SaveDiagramImageToFile`.
Iterating this way (pure math → sandbox → image) is much faster than
round-tripping through EA for every attempt.

### Re-run Position Management

**Reflow-on-rerun is now the default for all 3 BPMN processes** (2026-07-05
— previously Newsletter-only; Customer Account/Sales only ever added new
elements, preserving whatever manual layout existed). This is a deliberate,
user-approved behavior change, not a bug: the next `generate()` run against
an existing diagram repositions ALL elements using flow layout, not just new
ones. **Consequence:** any manually-tuned layout on a live diagram will be
overwritten the next time its generator runs. Always preview in `Sandbox`
first (with GUID-stripped input — see above) before running for real against
a diagram with an established manual layout.

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

## Non-BPMN Layout (Grid — `compute_grid_positions`)

For non-BPMN diagrams (ArchiMate, Data Model, Requirements), use
`diagram_utils.compute_grid_positions()`, **not** `compute_diagonal_positions()`
(kept only as a legacy fallback — its old row-jump formula compounded
`row * (per_row * step + row_gap - step)`, which for the default step/row_gap
sprawled new elements thousands of pixels from the rest of the diagram after
only a handful of rows; fixed 2026-07-02 but `compute_grid_positions` is
strictly preferred going forward).

```python
positions = diagram_utils.compute_grid_positions(
    element_ids, elem_types=elem_types,               # {eid: base_type}, optional
    type_sizes=diagram_utils.DEFAULT_ELEMENT_SIZES,    # per-type box size, optional
    default_size=diagram_utils.DEFAULT_ELEMENT_SIZE,   # (90, 70) -- see below
    start_x=20, start_y=20,
    per_row=8, cell_width=180, cell_height=100, h_gap=20, v_gap=20)
```

Row/column advance **linearly** (no compounding) — a uniform grid cell
(`cell_width` x `cell_height`) holds each element's own type-appropriate box,
centered within the cell (same technique as `compute_bpmn_element_positions`
for lanes). This keeps the layout compact and near the origin.

**When adding new elements to an existing diagram**, anchor them below the
diagram's real current content instead of continuing an index-based formula
(which can drift arbitrarily far from where existing elements actually ended
up, especially across re-runs with manually-adjusted layouts):

```python
_, max_bottom = diagram_utils.get_diagram_extent(diag)  # real current extent
new_positions = diagram_utils.compute_grid_positions(
    new_ids, elem_types=elem_types, type_sizes=diagram_utils.DEFAULT_ELEMENT_SIZES,
    start_x=20, start_y=max_bottom + 40, per_row=8, ...)
```

### Sizes Must Not Be Forced Flat Across Element Types — But Must Be Set

**CONFIRMED (2026-07-02) via a full live run, verified two ways: a direct COM
read-back after the run, and visually in EA's own GUI after refresh.** EA's
COM API does **not** auto-size a `DiagramObject` — leaving `right`/`bottom`
unset produces a permanent 0×0, invisible object. This was tested twice: once
as a same-session synchronous read-back, and once end-to-end (script exits,
file fully committed, diagram opened fresh in EA's GUI) — both showed the
same `right=0 bottom=0` result, and the GUI rendered the diagram as an empty
tangle of connector lines with no visible element boxes. **Do not attempt
position-only placement for non-BPMN diagrams again** — explicit bounds are
required.

What must NOT happen is forcing one flat, identical box (e.g. 180×100) onto
every element regardless of type — that distorts non-Class shapes badly (a
`Node` 3D box, `Interface` circle, `Component` two-tab all render squashed
into a generic rectangle). Use `DEFAULT_ELEMENT_SIZES` (keyed by Sparx EA base
`Object_Type` — see `ELEMENT_BASE_TYPE`) via the `type_sizes` param of
`compute_grid_positions` so each element gets a size appropriate to its
actual shape.

**Confirmed native default (2026-07-02):** three separate elements dragged
fresh from the ArchiMate3 toolbox and left unresized —
`ApplicationComponent1` (Component), `BusinessActor1` (Class), and
`BusinessObject1` (Class) — all came back exactly **90×70**. This suggests
this EA installation's native new-element default is uniformly 90×70
regardless of ArchiMate stereotype/shape, not a size that varies meaningfully
per type. `DEFAULT_ELEMENT_SIZES` currently sets every entry to `(90, 70)`
for this reason. If a genuinely different shape (e.g. a `Node` 3D box or
`Interface` circle) turns out to need a different size, get a fresh
toolbox-dragged, unresized reference for that specific type before changing
its entry — don't guess.

If an existing diagram ever ends up with 0×0 objects (e.g. from re-running
older position-only code against it), use
`diagram_utils.repair_zero_size_objects(diag, repo, type_sizes=...)` to fix
sizes in place without disturbing existing left/top positions.

### UML Classes With Attributes Need Per-Instance Height, Not a Fixed Size

The `90x70` fixed default only holds for elements that render as a plain icon
box with no attribute compartment (ArchiMate elements: BusinessActor,
BusinessObject, Component, etc. — confirmed above). **This does NOT apply to
`generate_uml_datamodel.py`'s entities**, which are real UML `Class` elements
with actual EA `Attributes` added via `sync_attributes()` — EA renders an
attribute compartment that needs to grow with the number of attributes, or a
fixed height clips entities with many attributes and wastes space on ones
with few.

Use `diagram_utils.compute_uml_class_height(attr_count)` (header + one row
per attribute + padding) and `diagram_utils.compute_uml_class_width(name,
attr_labels)` (longest of the class name or any "attrname: type" label,
converted to a pixel estimate) to compute a per-entity size, and pass a
`sizes={eid: (w, h)}` dict to `compute_grid_positions()` / a
`get_elem_size(elem)` callable to `repair_zero_size_objects()` — these take
precedence over the type-based `type_sizes`/`default_size` path. Set
`cell_width`/`cell_height` to at least the largest computed size in the
batch, or rows/columns will overlap. Both formulas are approximations, not
EA-confirmed constants like the 90×70 default — tuned interactively
(2026-07-02) against a `Sandbox` test diagram (see below) until attribute
compartments visually fit without excess trailing whitespace:

```python
def compute_uml_class_width(name, attr_labels, char_width=5.5, min_width=120, padding=10): ...
def compute_uml_class_height(attr_count, header_height=30, row_height=16, min_height=70, padding=6): ...
```

If these ever look off again, recalibrate the same way: drop a fresh
toolbox-dragged Class with a matching attribute count/name length into a
sandbox diagram (see "Use a Sandbox Package for Calibration/Testing" below),
compare, adjust the constants — don't just guess new numbers.

**Diagram Type/Stereotype/Technology do not affect sizing.** Confirmed by
inspecting a diagram the user built by hand in EA's GUI: its `Type` was
actually `'Logical'` (not an ArchiMate-specific type), `Stereotype`/
`StereotypeEx` were both empty, yet a manually drag-and-dropped
`ApplicationComponent` still got a real size (`90x70`). Auto-sizing is
triggered by EA's interactive drag-and-drop UI action — a different internal
code path that `DiagramObjects.AddNew()` + `Update()` (the only path
available via COM automation) never runs, regardless of how the diagram
itself is typed/tagged. Do not spend time trying `diag.MDGTechnology` (it's
read-only via COM — `AttributeError: can not be set`) or passing a combined
`"Technology::Type"` string to `Diagrams.AddNew()` (silently produces an
invalid generic `'Logical'` diagram) — neither affects element sizing.

This does **not** apply to BPMN diagrams, which already have their own
correct type-based sizing via `BPMN_ELEMENT_SIZES` and flow layout — leave
that untouched.

### Connector LineStyle by Diagram Type

Different diagram types use different `DiagramLink.LineStyle` conventions
(see the full enum table above). Use
`diagram_utils.set_diagram_link_style(diag, line_style)` — idempotent, safe
to call every run, only touches connectors whose `LineStyle` doesn't already
match:

| Diagram type | LineStyle | Value |
|---|---|---|
| BPMN (Sales/Newsletter process) | Orthogonal Rounded | `9` |
| UML Data Model (`generate_uml_datamodel.py`) | Orthogonal Square | `8` (set 2026-07-02, user preference) |
| ArchiMate (`generate_archimate.py`) | not yet set | — (ask before assuming a value) |

### Quick Reference: Confirmed Sizes/Settings by Diagram Type

| Diagram | Element sizing | Constant/formula | Connector LineStyle |
|---|---|---|---|
| ArchiMate (`generate_archimate.py`) | Fixed per instance, uniform across all confirmed types | `DEFAULT_ELEMENT_SIZES` → `(90, 70)` for every entry (Class, Activity, Component, Interface, Node, Device, Requirement) | not set |
| UML Data Model (`generate_uml_datamodel.py`) | Per-entity, scales with attribute count/name length | `compute_uml_class_width()` + `compute_uml_class_height()` | `8` (Orthogonal Square) |
| Requirements (`generate_requirements_from_md.py`) | Fixed, same as ArchiMate default | `default_size=(90, 70)` | not set |
| BPMN (Sales/Newsletter) | Fixed per BPMN type | `BPMN_ELEMENT_SIZES` | `9` (Orthogonal Rounded) |

### Use a Sandbox Package for Calibration/Testing

Never test new layout/sizing/style logic directly against a real diagram
(`EAxCRM ArchiMate`, `EAxCRM Data Model`, any BPMN process diagram, etc.) —
the user has manually adjusted layouts there that must be preserved. Instead,
create/reuse a `Sandbox` package directly under the root Model package (same
level as `Application Architecture`, `Data Architecture`, etc.), with its own
sub-packages, diagrams, and — critically — its **own separate GUID map file**
(e.g. `sandbox_datamodel_guid_map.json`) so sandbox runs can never collide
with a real generator's GUID map. `experiments/modelgen/sandbox_size_test.py`
and `sandbox_datamodel_demo.py` (both deleted after use, recreate as needed)
are worked examples: the latter reuses `generate_uml_datamodel.parse_md()`
and `sync_attributes()` against the *real* MD source but writes into
`Sandbox` instead of `Data Architecture > EAxCRM Data Model`, so real MD data
can be used to validate the full pipeline without any risk to production.

#### CRITICAL: a different target package is NOT sufficient isolation

**Incident, 2026-07-03 (BPMN engine refactor):** a "sandbox" dry-run targeting
`parent_package_name="Sandbox"` still repositioned every element on the
**real**, live, manually-tuned Customer Account diagram under
`Process Architecture` — and left its connector routing visibly broken
(stale `DiagramLink.Path` values drawing diagonal lines through the diagram
after boxes moved). Root cause: `repo.GetElementByGuid()` resolves
**repo-wide**, ignoring which package the calling code thinks it's targeting.
Any MD file previously synced out of the live model embeds real element
GUIDs in its `- GUID:` fields (that's the whole point of the idempotent
GUID-map pattern) — so re-running a generator against that MD, even with a
different `parent_package_name`, finds and updates the real elements
wherever they actually live, silently, with nothing in the script's own
output signaling the mismatch.

**A separate sandbox GUID map file is necessary but NOT sufficient.** It only
prevents the *sandbox script's own* re-run tracking from colliding with a
real generator's map — it does nothing to stop the MD's embedded `- GUID:`
fields from matching real elements on the very first sandbox run.

**For genuine isolation, do one of:**
- Strip all `- GUID:` (and `- Diagram GUID:`) fields from a **temp copy** of
  the source MD before feeding it to the sandbox script. This forces
  `create_element()`'s GUID-based lookup to fail and fall through to
  creating fresh elements in the Sandbox package. One-liner:
  ```python
  import re
  text = open(real_md_path, encoding="utf-8").read()
  stripped = re.sub(r"^- (GUID|Diagram GUID): .*\n", "", text, flags=re.MULTILINE)
  open(temp_md_path, "w", encoding="utf-8").write(stripped)
  # then run the generator with md_path=temp_md_path
  ```
- Or use synthetic/fabricated test data that never had real GUIDs to begin
  with (e.g. a hand-written test fixture MD for exercising a new code path
  like Pool support, which no real process MD uses yet).

**Also from the same incident:** any code that repositions already-placed
diagram objects (reflow/relayout on re-run) must clear the connector
`DiagramLink.Path` for links whose endpoints moved. Leaving a stale `Path`
in place produces visibly broken diagonal routing even when the box
positions themselves are now correct — `Path` holds absolute waypoint
coordinates computed for the *old* positions, and EA does not recompute it
automatically when a box moves via COM (`dobj.left/top/right/bottom =
...; dobj.Update()`). See `bpmn_engine.py`'s line-style/geometry pass, which
now recomputes `Path` for every connector on every run (see "Connector
Routing" below) rather than leaving stale values in place.

#### Visual self-verification via `SaveDiagramImageToFile`

**Discovered 2026-07-05** — you don't have to rely on the user checking every
layout iteration in EA's GUI. `EA.Project.SaveDiagramImageToFile` lets you
export a diagram to PNG and view it yourself with the `Read` tool:

```python
with ea_session.ea_repository(qea_path) as repo:
    diag = repo.GetDiagramByGuid(diagram_guid)   # or GetDiagramByID
    repo.OpenDiagram(diag.DiagramID)             # must be open first
    proj = repo.GetProjectInterface()
    proj.SaveDiagramImageToFile(r"C:\path\to\out.png")   # 2-arg form errors;
                                                          # only takes the path
    repo.CloseDiagram(diag.DiagramID)
```
Then `Read` the PNG directly — this closes the loop for iterating on layout/
routing algorithms without a human in the loop for every attempt. Reserve
asking the user to look for final confirmation once you're already confident,
not for every intermediate trial.

## Platform-Specific Gotchas

### Python 64-bit + EA 32-bit COM Bridge

Use the shared `experiments/modelgen/ea_session.py` module (all generators
do, as of 2026-07-02) instead of hand-rolling a COM connection:

```python
import ea_session
with ea_session.ea_repository(qea_path, technology="ArchiMate3") as repo:
    root = ea_session.get_model_root(repo)  # retries on transient 61704 errors
    ...
```

- `ea_session.ea_repository()` uses `win32com.client.DispatchEx("EA.App")` +
  `.Repository` — **`DispatchEx`, not plain `Dispatch`**. Plain `Dispatch`
  can attach to an EA automation server already registered in COM's Running
  Object Table (e.g. the user's own open EA instance on the same file)
  instead of spawning an isolated one — confirmed to be the cause of EA's
  "Internal application error 61704" on `repo.Models.GetAt(0)`.
- `ea_session.get_model_root(repo)` retries `repo.Models.GetAt(0)` up to 5
  times (2s apart) — this call has been observed to transiently fail right
  after `OpenFile`/`ActivateTechnology`.
- The context manager handles `RefreshModelView`/`RefreshOpenDiagrams`,
  `CloseFile`, and zombie cleanup automatically on exit (see below) — no
  need to repeat any of that per-script.

### Zombie EA Process Cleanup (MANDATORY)

EA zombie processes accumulate after every generator run. If left unchecked, they lock the `.qea` file, preventing EA from starting.

`ea_session.ea_repository()` handles this automatically: it snapshots
`ea_session.get_ea_pids()` before spawning its own EA instance, and on exit
calls `ea_session.kill_new_ea_processes(before_pids)` — which only kills
PIDs that appeared *after* the snapshot, so a pre-existing EA instance (the
user's own open session) is never touched, by construction. **Never**
manually run `Get-Process -Name EA | Stop-Process -Force` — that has no way
to distinguish the user's real session from a zombie. If you suspect a
genuine leaked zombie (rare — e.g. a script crashed before reaching the
`finally` block), confirm the PID's start time lines up with the crashed
run before asking the user for permission to kill it.

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
| `experiments/modelgen/ea_session.py` | Shared EA COM session lifecycle — isolated `DispatchEx` instance, `Models.GetAt(0)` retry, automatic zombie cleanup. Used by every generator/sync script |
| `experiments/modelgen/diagram_utils.py` | Shared **non-BPMN** layout functions — grid layout (`compute_grid_positions`), diagonal cascade (legacy), UML class sizing (`compute_uml_class_width/height`), connector line-style (`set_diagram_link_style`). BPMN-only functions moved to `bpmn_engine.py` (2026-07-05) |
| `experiments/modelgen/bpmn_config.py` | `ProcessConfig` dataclass + `CUSTOMER_ACCOUNT`/`SALES`/`NEWSLETTER` instances + shared BPMN vocabulary (`LABEL_TO_STEREO`, `OBJECT_TYPE_MAP`, `BPMN_TAGGED_VALUES`, `CONNECTOR_TYPES`, `BPMN_ELEMENT_SIZES`, etc.) — previously copy-pasted across all 6 BPMN scripts |
| `experiments/modelgen/bpmn_engine.py` | Shared BPMN engine: `parse_md`, `generate`, `sync_to_md`, `_connector_path`, and the BPMN-only layout functions (`compute_bpmn_lane_positions` (pool-aware), `compute_bpmn_flow_layout`, `find_longest_path`, `sort_by_flow_order`, `get_lane_from_fields`, `get_pool_from_lane_fields`) |
| `experiments/modelgen/generate_archimate.py` | ArchiMate diagram generator |
| `experiments/modelgen/generate_uml_datamodel.py` | UML Data Model diagram generator |
| `experiments/modelgen/generate_customeraccount_process_from_md.py` | Thin wrapper: `bpmn_engine.generate(bpmn_config.CUSTOMER_ACCOUNT)` |
| `experiments/modelgen/generate_sales_process_from_md.py` | Thin wrapper: `bpmn_engine.generate(bpmn_config.SALES)` |
| `experiments/modelgen/generate_newsletter_process_from_md.py` | Thin wrapper: `bpmn_engine.generate(bpmn_config.NEWSLETTER)` |
| `experiments/modelgen/generate_requirements_from_md.py` | Requirements diagram generator |
| `experiments/modelgen/sync_datamodel_from_ea.py` | Reads EA data model back to MD |
| `experiments/modelgen/sync_customeraccount_process_from_ea.py` | Thin wrapper: `bpmn_engine.sync_to_md(bpmn_config.CUSTOMER_ACCOUNT)` |
| `experiments/modelgen/sync_sales_process_from_ea.py` | Thin wrapper: `bpmn_engine.sync_to_md(bpmn_config.SALES)` |
| `experiments/modelgen/sync_newsletter_process_from_ea.py` | Thin wrapper: `bpmn_engine.sync_to_md(bpmn_config.NEWSLETTER)` (hierarchical MD writer) |
| `experiments/modelgen/sync_requirements_from_ea.py` | Reads EA requirements back to MD |
