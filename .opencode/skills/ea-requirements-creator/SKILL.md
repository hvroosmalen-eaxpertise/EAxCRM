---
name: ea-requirements-creator
description: Reference for generating/syncing the EAxCRM Requirements diagram via generate_requirements_from_md.py — fixed element sizing (same as ArchiMate default) and the non-BPMN grid layout. Read ea-model-common first for shared COM/session/GUID-map/Sandbox patterns.
---

# EA Requirements Creator (EAxCRM Project Skill)

## Overview

Covers `experiments/modelgen/generate_requirements_from_md.py` and `sync_requirements_from_ea.py`, generating the "EAxCRM Requirements" diagram. **Read `ea-model-common` first** for the coordinate system, GUID map pattern, COM session lifecycle, and Sandbox isolation protocol — this skill covers the little that's Requirements-specific, since it mostly follows the same patterns as ArchiMate/Data Model.

## Diagram Placement and Sizing

Requirements diagrams are created under the **package** (`pkg.Diagrams.AddNew`), same as ArchiMate/Data Model, not under an element. Element sizing is fixed, same as the ArchiMate default: `default_size=(90, 70)` — Requirement elements don't have an attribute compartment that needs per-instance sizing the way Data Model Classes do, so `ea-archimate-creator`'s "Element Sizing" notes apply directly here (explicit bounds are always required; auto-sizing via COM never happens regardless of diagram type/technology).

## Layout: Non-BPMN Grid

Same `diagram_utils.compute_grid_positions()` pattern as ArchiMate — see `ea-archimate-creator` for the full usage pattern (grid cells, anchoring new elements below existing content on re-run, add-only preservation of manual layout).

## Connector LineStyle

Not set (same as ArchiMate — ask before assuming a value).

## Quick Reference

| Element sizing | Constant/formula | Connector LineStyle |
|---|---|---|
| Fixed, same as ArchiMate default | `default_size=(90, 70)` | not set |

## Audit Trail

Requirements' changelog wiring (`requirements_changelog.md`) follows the exact same pattern as the other generators — see `ea-model-common`'s changelog reference and `changelog.py` itself.

## Source Files

| File | Purpose |
|------|---------|
| `experiments/modelgen/generate_requirements_from_md.py` | Requirements diagram generator |
| `experiments/modelgen/sync_requirements_from_ea.py` | Reads EA requirements back to MD |
