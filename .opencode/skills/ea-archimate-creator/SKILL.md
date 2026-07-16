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

## Connector `Type` + `StereotypeEx` per ArchiMate 3 (2026-07-14, user-confirmed)

The ArchiMate 3 spec's Relationship Summary Table groups relations into **categories**, and Sparx's ArchiMate3 MDG maps each category to a specific base UML `Connector_Type` (`t_connector.Connector_Type`). **The diamond/arrowhead glyph is rendered by the MDG stereotype, NOT by the base UML type** — this is why Composition and Aggregation both back onto `Association`, not UML `Aggregation`.

The authoritative map — set in `generate_archimate.py:CONNECTOR_BASE_TYPE`:

| ArchiMate | Category | base_type | StereotypeEx |
|---|---|---|---|
| Composition | Structural | `Association` | `ArchiMate3::ArchiMate_Composition` |
| Aggregation | Structural | `Association` | `ArchiMate3::ArchiMate_Aggregation` |
| Assignment | Structural | `Association` | `ArchiMate3::ArchiMate_Assignment` |
| Realization | Structural | `Realisation` | `ArchiMate3::ArchiMate_Realization` |
| Serving | Dependency | `Dependency` | `ArchiMate3::ArchiMate_Serving` |
| Access | Dependency | `Dependency` | `ArchiMate3::ArchiMate_Access` |
| Influence | Dependency | `Dependency` | `ArchiMate3::ArchiMate_Influence` |
| Association | Dependency | `Association` | `ArchiMate3::ArchiMate_Association` |
| Triggering | Dynamic | `ControlFlow` | `ArchiMate3::ArchiMate_Triggering` |
| Flow | Dynamic | `ControlFlow` | `ArchiMate3::ArchiMate_Flow` |

Getting the base type wrong isn't visually obvious in EA at first glance (arrow direction still renders), but the MDG stereotype glyph (filled diamond, dotted line, arrowhead shape) misrenders — e.g. an Access relation on base `Association` shows as a plain solid line instead of the dotted "observe/act-upon" style. Verified 2026-07-14 by retyping all 118 connectors in the EAxCRM model.

**Also from that pass — connector identity is a 4-tuple, not a pair.** ArchiMate allows multiple connectors between the same two elements as long as they differ in type and/or stereotype. So the natural key is `(ClientID, SupplierID, Connector_Type, normalized_stereotype)`, not `(ClientID, SupplierID)`. The generator's `sync_relations` resolves connectors GUID-first via `guid_map` and falls back to a 4-tuple structural scan (see [issue #17](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/17)).

**Element-pair validity is part of ArchiMate 3.** Not every relation is legal between every element-type pair. Example: between an `ApplicationService` and a `DataObject` only `Access` is allowed — a `Flow` between behavior and passive-structure elements is a spec violation. When the MD has one anyway, it needs to be edited to the correct relation type, and existing connectors migrated in place (below).

## Access relation Direction + AccessMode (issue #17 #6, 2026-07-16)

Access relations carry a Read/Write/Read-Write semantic that structural relations don't. Two optional MD fields on any Access rel let the author specify it:

```
### Access — r-access-example
- Source: e-func-hist
- Target: e-data-contact
- GUID: {...}
- Direction: Bi-Directional      # optional; default "Source -> Destination"
- AccessMode: Read/Write         # optional; also written as an EA TaggedValue
```

**Default (both fields omitted)**: `Direction = "Source -> Destination"`, no AccessMode tag. Reads as "Write" per ArchiMate 3 semantics (source writes to target).

**Direction values**:
- `Source -> Destination` — default, single direction from source to target
- `Destination -> Source` — reversed single direction (e.g. Read: target reads from source)
- `Bi-Directional` — both directions (Read/Write)

**AccessMode values** are free-form; the ArchiMate 3 conventional set is `Read`, `Write`, `Read/Write`, `None`. The value is stored as a TaggedValue named `AccessMode` on the connector; MDG-rendered diagrams display it.

**Round-trip**: `generate_archimate.py` applies both fields when creating/updating a connector. `sync_archimate_from_ea.py` emits both when non-default. So a manual EA edit (setting AccessMode via GUI, or reversing Direction) is captured on next sync and preserved on next generate re-run.

**Critical Sparx quirk — TaggedValue binding order**: `Connectors.AddNew(...).TaggedValues.AddNew("AccessMode", "Read")` called **before** the connector's first `Update()` lands the tag row in `t_connectortag` with `ElementID = 0` — orphaned, invisible to `Connector.TaggedValues` on subsequent reads, and impossible to look up by connector id. Silent failure. Always `Update()` the connector first so it has a real `ConnectorID`, THEN set the tag. `generate_archimate.set_connector_tag(conn, prop, value)` enforces this and raises loudly if called too early — use it, don't roll your own.

Note: the current EAxCRM ArchiMate model has 42 Access relations, all default (no Direction or AccessMode fields in MD). #6's implementation gives you the machinery; whether to annotate any specific Access rel with Read/Write semantics is a separate modeling decision.

## Repairing Existing Connectors: `dedup_archimate_connectors.py`

`experiments/modelgen/dedup_archimate_connectors.py` handles all model-repair scenarios — deduplication, adopting legacy blank stereotypes, retyping, and repairing a rel whose MD classification has changed. Two modes: default is dry-run (prints the plan), `--apply` executes.

Three-tier match logic:

1. **Tier 1 — GUID-first repair.** For each MD rel, if `archimate_guid_map.json` has the rel_key and the stored `ConnectorGUID` resolves to a connector on the expected `(client, supplier)`, that IS the survivor — **even if its stereotype/type disagree with the MD**. This is the "MD changed its mind" case (e.g. reclassifying a Flow as Access): the existing connector is retyped and re-stereotyped in place, preserving diagram placements.
2. **Tier 2 — structural scan.** For rels without a stored GUID (legacy connectors from before GUID tracking landed), scan by 4-tuple `(client, supplier, base_type, normalized_stereotype)`. Blank stereotypes get adopted (set to the MD-expected `StereotypeEx`).
3. Duplicates: lowest `ConnectorID` wins as survivor (most likely already referenced by diagram placements); rest deleted via `Connectors.DeleteAt(idx, False)` iterating from the top so indexes stay valid.

**Sparx quirk: setting `Type` and `StereotypeEx` in the same `Update()` silently drops the stereotype.** Do two Updates with a `GetConnectorByGuid` re-fetch between them — otherwise the connector reads back as `StereotypeEx = ''`. See `ea-model-common`'s "Sparx COM Update() Quirks" for the general form.

Typical workflow when the MD's relation types change:

```
# 1. Edit the MD (rename type + id).
# 2. Dry-run to see the plan.
python dedup_archimate_connectors.py
# 3. Apply.
python dedup_archimate_connectors.py --apply
# 4. Verify idempotency.
python generate_archimate.py   # expect 0 Created, all Exists
python dedup_archimate_connectors.py   # expect 0 retypes / adoptions / dups
```

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
| `experiments/modelgen/generate_archimate.py` | ArchiMate diagram generator — `parse_md`, `sync_elements`, `sync_relations` (GUID-first + 4-tuple identity), `CONNECTOR_BASE_TYPE` |
| `experiments/modelgen/dedup_archimate_connectors.py` | One-off repair tool — dedup, adopt legacy blank stereotypes, retype, and repair after MD reclassification. `--apply` to execute, dry-run by default |
