# Diagram Object Placement — Design

## Problem

When generators place elements on EA diagrams, two issues cause poor results:

1. **Stacked elements** — all placed at (0,0) or overlapping because positions aren't set, are set to defaults, or collision with existing manual positions
2. **Missing new elements on re-runs** — ArchiMate and Newsletter generators skip placement entirely if the diagram already has objects, so new MD elements never appear

Additionally, BPMN process diagrams (Newsletter, Sales) need lane-aware placement — elements should sit inside their Lane/Pool.

## Scope

**In scope:**
- Centralized `diagram_utils.py` module with shared layout functions
- BPMN lane-aware layout for Newsletter and Sales Process diagrams
- Diagonal cascade layout for Data Model, Requirements, ArchiMate diagrams
- Add-missing-element detection for ALL generators on re-runs
- Collision-avoiding placement for new elements
- New Sales Process MD→EA generator (`generate_sales_process_from_md.py`)
- New `EAxCRM-SalesProcess.md` spec file

**Out of scope (decided against):**
- Position round-tripping through MD (positions live only in EA diagram objects)
- Sync script changes (no position reading needed)
- MD format changes for position data

## Architecture

### `experiments/modelgen/diagram_utils.py`

Shared module consumed by all generators. No UI, no side effects — pure function library.

#### Layout computation functions

```python
def compute_bpmn_lane_positions(
    lanes: list[dict],
    lane_height: int = 500,
    lane_width: int = 1000,
    gap: int = 250
) -> dict[str, tuple[int, int, int, int]]:
    """
    Returns {lane_id: (left, top, right, bottom)}.
    Lanes are stacked vertically.
    Lane config: {id: str, name: str}
    """
```

```python
def compute_bpmn_element_positions(
    elements_by_lane: dict[str, list[str]],
    lane_bounds: dict[str, tuple[int, int, int, int]],
    elem_width: int = 180,
    elem_height: int = 70,
    h_gap: int = 30,
    v_gap: int = 30
) -> dict[str, tuple[int, int, int, int]]:
    """
    Returns {element_id: (left, top, right, bottom)}.
    Elements placed left-to-right inside their lane, wrapping to next row.
    4 elements per row at default lane width (1000px minus padding).
    """
```

```python
def compute_diagonal_positions(
    element_ids: list[str],
    per_row: int = 8,
    step: int = 200,
    row_gap: int = 200,
    elem_width: int = 180,
    elem_height: int = 120
) -> dict[str, tuple[int, int, int, int]]:
    """
    Returns {element_id: (left, top, right, bottom)}.
    Elements placed diagonally (step right, step down), wrapping to a new
    diagonal row after `per_row` elements.
    """
```

#### Diagram object management functions

```python
def get_placed_ids(diag) -> set[int]:
    """Returns set of ElementIDs already on the diagram."""
```

```python
def create_diagram_objects(
    diag,
    element_ids: list[str],
    object_ids: dict[str, int],
    positions: dict[str, tuple[int, int, int, int]]
) -> int:
    """
    Creates DiagramObjects for all given element_ids at specified positions.
    Returns count of objects created.
    """
```

```python
def add_missing_elements(
    diag,
    element_ids: list[str],
    object_ids: dict[str, int],
    new_positions: dict[str, tuple[int, int, int, int]]
) -> int:
    """
    Only creates DiagramObjects for ElementIDs not yet on the diagram.
    Returns count of new objects created.
    """
```

#### Lane field helper

```python
def format_lane_field(lane_id: str) -> str:
    """Returns '- Lane: eaxpertise'"""
```

```python
def parse_lane_field(field_value: str) -> str | None:
    """Parses lane_id from field value, returns None if absent"""
```

## Per-Generator Behavior

### BPMN generators (Newsletter + Sales Process)

**First-time creation:**
1. Ensure diagram exists (same logic as current code)
2. Read Lane assignments from `- Lane:` field in element's MD fields
3. `compute_bpmn_lane_positions()` → lane bounds
4. Group element_ids by lane
5. `compute_bpmn_element_positions()` → element positions
6. `create_diagram_objects()` for lanes first, then elements

**Re-run (diagram has objects):**
1. Skip placement if diagram already has objects → preserve manual layout
2. `get_placed_ids()` → existing set
3. Find elements not yet placed (not in placed_ids AND not lanes)
4. For new elements: determine lane from `- Lane:` field
5. Compute new positions: "append" mode — place after the last element in same lane
6. `add_missing_elements()` for new elements only

**Key: Lanes themselves are never added on re-runs** (they already exist).

### Non-BPMN generators (Data Model, Requirements, ArchiMate)

**First-time creation:**
1. Ensure diagram exists
2. `compute_diagonal_positions(all_element_ids)` → positions
3. `create_diagram_objects()` for all elements

**Re-run (diagram has objects):**
1. `get_placed_ids()` → existing set
2. Find elements not yet placed
3. `compute_diagonal_positions(new_element_ids)` — placing new elements after existing ones
4. `add_missing_elements()` for new elements only

### Re-run: Collision Avoidance

**Non-BPMN:** Use `compute_diagonal_positions()` with the starting index set to the count of already-placed elements. If 12 elements exist, new elements are placed at indices 12, 13, ... — which positions them on a fresh diagonal row after existing elements.

**BPMN (per lane):**
1. Get all existing diagram objects in the lane
2. Find the rightmost object (max `right`), and the lowest object (max `bottom`)
3. Start placing new elements to the right of the rightmost: `x = max_right + h_gap`
4. If `x + elem_width` exceeds the lane's `right` bound, start a new row: `x = lane_left + 20`, `y = max_bottom + v_gap`
5. Fallback: if the lane has no existing elements (shouldn't happen since lanes are created at first), place at `(lane_left + 20, lane_top + 20)`

## Generators Affected

| Generator | Type | Change |
|---|---|---|
| `generate_newsletter_process_from_md.py` | BPMN | Remove hardcoded `pos` dict → `diagram_utils` BPMN layout. Add re-run new-element detection. Add `- Lane:` field parsing. |
| `generate_sales_process_from_md.py` | BPMN | **New file.** Read `EAxCRM-SalesProcess.md`, BPMN layout, 3 Lanes. |
| `generate_uml_datamodel.py` | Non-BPMN | Diagonal layout via utils (replaces 4-column grid). |
| `generate_requirements_from_md.py` | Non-BPMN | Diagonal layout via utils (replaces 5-column grid). |
| `generate_archimate.py` | Non-BPMN | Add re-run new-element detection (currently missing!). Diagonal layout. |

## Sync Scripts

No changes. No position reading from EA diagram objects. The existing element-only sync is sufficient.

## MD Format Changes

Only `EAxCRM-NewsletterProcess.md` needs new `- Lane:` fields per element:

```markdown
### Activity—sendnewsletter
- Name: Send Newsletter
- Type: Activity
- Stereotype: Activity
- GUID: {10B37700801243C2A155A78322CCFCB7}
- Lane: eaxpertise
- Description: Activity to dispatch...
```

New `EAxCRM-SalesProcess.md` will also have `- Lane:` fields.

## Sales Process MD Spec

The Sales Process has 3 Lanes (Customer, EAxpertise, Vendor) with roughly 21 Activities, 4 Events, 2 Gateways, 1 DataObject (per AGENTS.md). The MD spec will be created by:

1. Running a targeted sync against the sales CollaborationModel in EA (the sales process already exists in EA, synced to `EAxCRM-ProcessModel.md`)
2. Or by extracting the sales-relevant portion from `EAxCRM-ProcessModel.md` into a dedicated `EAxCRM-SalesProcess.md`
3. All elements will need `- Lane:` fields added

The preferred approach is a dedicated sync query that reads only the sales CollaborationModel's descendants and writes to `EAxCRM-SalesProcess.md`, then add Lane fields manually.

## Files Changed/Created

| File | Action |
|---|---|
| `experiments/modelgen/diagram_utils.py` | **New** |
| `experiments/modelgen/generate_newsletter_process_from_md.py` | **Update** |
| `experiments/modelgen/generate_sales_process_from_md.py` | **New** |
| `experiments/modelgen/generate_uml_datamodel.py` | **Update** |
| `experiments/modelgen/generate_requirements_from_md.py` | **Update** |
| `experiments/modelgen/generate_archimate.py` | **Update** |
| `models/EAxCRM-NewsletterProcess.md` | **Update** — add Lane fields |
| `models/EAxCRM-SalesProcess.md` | **New** |
