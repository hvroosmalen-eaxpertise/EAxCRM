---
name: ea-ldm-creator
description: Reference for generating/syncing the EAxCRM Data Model (UML Class diagram) via generate_ldm_from_md.py — per-entity sizing scaled to attribute count, Orthogonal Square connector routing, and the non-BPMN grid layout. Read ea-model-common first for shared COM/session/GUID-map/Sandbox patterns.
---

# EA Data Model Creator (EAxCRM Project Skill)

## Overview

Covers `experiments/modelgen/generate_ldm_from_md.py` and `sync_ldm_from_ea.py`, generating the "EAxCRM Data Model" UML Class diagram. **Read `ea-model-common` first** for the coordinate system, GUID map pattern, COM session lifecycle, and Sandbox isolation protocol — this skill only covers what's specific to UML Class entities with real attributes.

## Diagram Placement and Type

Data Model diagrams are created under the **package** (`dm_pkg.Diagrams.AddNew`), not under an element. Native `Diagram_Type` is `"Logical"` with no stereotype needed — unlike ArchiMate/BPMN, "Logical" is a **native EA diagram type** with its own built-in Class-diagram toolbox (not from an MDG Technology extension), so it doesn't need the `StyleEx`/`MDGDgm` treatment described in `ea-model-common`. Confirmed: querying the live diagram's `t_diagram` row shows `Diagram_Type='Logical'`, `Stereotype=None`, no `t_xref` "Stereotypes" row at all — and the toolbox already works.

## UML Classes With Attributes Need Per-Instance Height, Not a Fixed Size

The `90x70` fixed default that works for ArchiMate elements only holds for elements that render as a plain icon box with no attribute compartment. **This does NOT apply here** — these are real UML `Class` elements with actual EA `Attributes` added via `sync_attributes()`, and EA renders an attribute compartment that needs to grow with the number of attributes, or a fixed height clips entities with many attributes and wastes space on ones with few.

Use `diagram_utils.compute_uml_class_height(attr_count)` (header + one row per attribute + padding) and `diagram_utils.compute_uml_class_width(name, attr_labels)` (longest of the class name or any "attrname: type" label, converted to a pixel estimate) to compute a per-entity size, and pass a `sizes={eid: (w, h)}` dict to `compute_grid_positions()` — these take precedence over the type-based `type_sizes`/`default_size` path. Set `cell_width`/`cell_height` to at least the largest computed size in the batch, or rows/columns will overlap.

```python
def compute_uml_class_width(name, attr_labels, char_width=5.5, min_width=120, padding=10): ...
def compute_uml_class_height(attr_count, header_height=30, row_height=16, min_height=70, padding=6): ...
```

Both formulas are approximations, not EA-confirmed constants like ArchiMate's 90×70 default — tuned interactively (2026-07-02) against a `Sandbox` test diagram until attribute compartments visually fit without excess trailing whitespace. If these ever look off again, recalibrate the same way: drop a fresh toolbox-dragged Class with a matching attribute count/name length into a sandbox diagram, compare, adjust the constants — don't just guess new numbers.

## Layout: Non-BPMN Grid

Same `diagram_utils.compute_grid_positions()` as ArchiMate — see `ea-archimate-creator` for the general usage pattern. The difference here is passing computed `sizes={eid: (w, h)}` instead of relying on `type_sizes`/`default_size`.

## Connector LineStyle

Set to `8` (Orthogonal Square) — a 2026-07-02 user preference, different from BPMN's `9` (Orthogonal Rounded). Use `diagram_utils.set_diagram_link_style(diag, 8)` — idempotent, only touches connectors whose `LineStyle` doesn't already match.

## Quick Reference

| Element sizing | Constant/formula | Connector LineStyle | Diagram_Type |
|---|---|---|---|
| Per-entity, scales with attribute count/name length | `compute_uml_class_width()` + `compute_uml_class_height()` | `8` (Orthogonal Square) | `Logical` (native, no MDGDgm needed) |

## Source Files

| File | Purpose |
|------|---------|
| `experiments/modelgen/generate_ldm_from_md.py` | UML Data Model diagram generator |
| `experiments/modelgen/sync_ldm_from_ea.py` | Reads EA data model back to MD |
