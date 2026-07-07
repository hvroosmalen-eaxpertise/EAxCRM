---
name: ea-archimate-creator
description: Reference for generating the EAxCRM ArchiMate diagram via generate_archimate.py — element sizing (DEFAULT_ELEMENT_SIZES, all 90x70), the ArchiMate diagram-type/toolbox fix (Diagram_Type=Logical, MDGDgm=ArchiMate3::Application), and the non-BPMN grid layout. Read ea-model-common first for shared COM/session/GUID-map/Sandbox patterns.
---

# EA ArchiMate Creator (EAxCRM Project Skill)

## Overview

Covers `experiments/modelgen/generate_archimate.py`, generating the single "EAxCRM ArchiMate" diagram (Business/Application/Technology layers in one view). **Read `ea-model-common` first** for the coordinate system, GUID map pattern, COM session lifecycle, Sandbox isolation protocol, and the general diagram-type/toolbox mechanism — this skill only covers what's ArchiMate-specific.

## ArchiMate Diagram Type and Toolbox (user-confirmed correct 2026-07-06)

Same mechanism as BPMN (see `ea-model-common`'s "Diagram Type and Toolbox"): `StyleEx`'s `MDGDgm=` key, not `Stereotype`/`StereotypeEx`. Native `Diagram_Type` is `"Logical"` (NOT `"Application Layer"` — that's only the human alias of the `Application` stereotype, not a real `Diagram_Type`):

```python
diag = eax_pkg.Diagrams.AddNew(name, "Logical")  # NOT "Application Layer"
diag.Stereotype = ""
diag.StereotypeEx = ""
diag.StyleEx = "MDGDgm=ArchiMate3::Application;"  # the real toolbox selector
diag.Update()
```

This is the one case where the value derived directly from reading `MDGTechnologies/ArchiMate3.xml` (rather than copied from an unrelated reference diagram) turned out correct on the first attempt, and the user has confirmed the toolbox works as applied. **Fixed 2026-07-06 to be COM-only (see `ea-model-common`'s hard rule):** `generate_archimate.py`'s `ensure_diagram_toolbox()` sets `Type`/`StyleEx` correctly at diagram-creation time only, via plain COM — no more SQLite. An existing diagram found with the wrong `Type`/`StyleEx` can no longer be auto-corrected in code; it logs a warning instead. Re-verified correct after this change (no warning on a real run).

There are only 5 ArchiMate3 diagram stereotypes total (from `MDGTechnologies/ArchiMate3.xml`'s `<DiagramProfile>` block), each single-layer: `Business`, `Application`, `Technology`, `Motivation`, `Implementation` — all apply to the same native `"Logical"` type. There is no combined/multi-layer diagram stereotype in this MDG — `Application` was used here since that's what this diagram's type string was already trying to say; Business/Technology/Motivation/Implementation shapes remain reachable via the toolbox's "more tools" picker even though `Application` is the default page.

## Diagram Placement

ArchiMate diagrams are created under the **package** (`eax_pkg.Diagrams.AddNew`), not under an element — unlike BPMN's CollaborationModel-anchored diagrams. See `generate_archimate.py:416`.

## Element Sizing

**Confirmed native default (2026-07-02):** three separate elements dragged fresh from the ArchiMate3 toolbox and left unresized — `ApplicationComponent1` (Component), `BusinessActor1` (Class), and `BusinessObject1` (Class) — all came back exactly **90×70**. This suggests this EA installation's native new-element default is uniformly 90×70 regardless of ArchiMate stereotype/shape. `DEFAULT_ELEMENT_SIZES` (in `diagram_utils.py`) sets every entry to `(90, 70)` for this reason. If a genuinely different shape (e.g. a `Node` 3D box or `Interface` circle) turns out to need a different size, get a fresh toolbox-dragged, unresized reference for that specific type before changing its entry — don't guess.

**CONFIRMED (2026-07-02) via a full live run:** EA's COM API does **not** auto-size a `DiagramObject` — leaving `right`/`bottom` unset produces a permanent 0×0, invisible object, confirmed both same-session and end-to-end (file committed, diagram reopened fresh). Do not attempt position-only placement — explicit bounds are always required.

What must NOT happen is forcing one flat, identical box onto every element regardless of type — that distorts non-Class shapes badly (a `Node` 3D box, `Interface` circle, `Component` two-tab all render squashed into a generic rectangle). Use `DEFAULT_ELEMENT_SIZES` (keyed by Sparx EA base `Object_Type` — see `ELEMENT_BASE_TYPE`) via the `type_sizes` param of `compute_grid_positions` so each element gets a size appropriate to its actual shape (in this case, they're all still 90×70, but the mechanism is type-based, not hardcoded).

**Diagram Type/Stereotype/Technology do not affect sizing.** Confirmed by inspecting a diagram the user built by hand in EA's GUI: its `Type` was actually `'Logical'`, `Stereotype`/`StereotypeEx` were both empty, yet a manually drag-and-dropped `ApplicationComponent` still got a real size (`90x70`). Auto-sizing is triggered by EA's interactive drag-and-drop UI action — a different internal code path that `DiagramObjects.AddNew()` + `Update()` (the only path available via COM automation) never runs, regardless of how the diagram itself is typed/tagged. Do not spend time trying `diag.MDGTechnology` (read-only via COM — `AttributeError: can not be set`) or passing a combined `"Technology::Type"` string to `Diagrams.AddNew()` (silently produces an invalid generic `'Logical'` diagram) — neither affects element sizing.

If an existing diagram ever ends up with 0×0 objects, use `diagram_utils.repair_zero_size_objects(diag, repo, type_sizes=...)` to fix sizes in place without disturbing existing left/top positions.

## Layout: Non-BPMN Grid

Uses `diagram_utils.compute_grid_positions()`, **not** `compute_diagonal_positions()` (kept only as a legacy fallback — its old row-jump formula compounded, sprawling new elements thousands of pixels from the rest of the diagram after only a handful of rows).

```python
positions = diagram_utils.compute_grid_positions(
    element_ids, elem_types=elem_types,               # {eid: base_type}, optional
    type_sizes=diagram_utils.DEFAULT_ELEMENT_SIZES,    # per-type box size, optional
    default_size=diagram_utils.DEFAULT_ELEMENT_SIZE,   # (90, 70)
    start_x=20, start_y=20,
    per_row=8, cell_width=180, cell_height=100, h_gap=20, v_gap=20)
```

Row/column advance **linearly** (no compounding) — a uniform grid cell holds each element's own type-appropriate box, centered within the cell.

**When adding new elements to an existing diagram**, anchor them below the diagram's real current content instead of continuing an index-based formula:

```python
_, max_bottom = diagram_utils.get_diagram_extent(diag)  # real current extent
new_positions = diagram_utils.compute_grid_positions(
    new_ids, elem_types=elem_types, type_sizes=diagram_utils.DEFAULT_ELEMENT_SIZES,
    start_x=20, start_y=max_bottom + 40, per_row=8, ...)
```

Existing elements' positions are preserved on re-run (add-only), unlike BPMN's reflow-on-rerun default.

## Connector LineStyle

Not yet set for ArchiMate (ask before assuming a value) — see the Quick Reference below for how this compares to the other diagram types.

## Quick Reference

| Element sizing | Constant/formula | Connector LineStyle | Diagram_Type / StyleEx MDGDgm |
|---|---|---|---|
| Fixed per instance, uniform across all confirmed types | `DEFAULT_ELEMENT_SIZES` → `(90, 70)` for every entry (Class, Activity, Component, Interface, Node, Device, Requirement) | not set | `Logical` / `ArchiMate3::Application` |

## Design Phase

For ArchiMate specifically: Business layer at top, Application layer middle, Technology layer bottom (see `ea-model-common`'s "Design Phase Before First-Run Layout" for the general process).

## Source Files

| File | Purpose |
|------|---------|
| `experiments/modelgen/generate_archimate.py` | ArchiMate diagram generator — `parse_md`, `sync_elements`, `sync_relations`, `set_diagram_stereotype` |
