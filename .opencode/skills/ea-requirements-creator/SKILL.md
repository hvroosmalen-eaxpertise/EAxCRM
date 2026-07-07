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

## Notes Composition and Tagged Values (added 2026-07-07, RTF formatting added 2026-07-07)

Each requirement's MD block may include `- Rationale:` (single line) and `- Test Cases:` (a `  - ` bullet list) fields alongside `- Description:`. `build_notes(repo, req)` in `generate_requirements_from_md.py` composes these into the EA element's `Notes` field with real rich-text formatting — bold `Rationale:`/`Test Cases:` section headers and a hanging-indent numbered list for test cases — so all three read clearly together when viewing the element in EA, not just as a wall of plain text.

**Why not assign the Notes text directly:** setting `element.Notes = someRtfString` does *not* work — EA treats the assignment as plain text and the RTF control codes show up literally (e.g. `{\rtf1\ansi...\par}` visible as text). EA's internal Notes storage is its own HTML-like format, not plain RTF or plain text. The correct pattern (`build_notes_rtf()` + `build_notes()`): build a proper RTF document string with `\b Rationale:\b0` bold runs and `\li720\fi-360` hanging-indent numbered lines (escaping backslashes/braces/non-ASCII via `rtf_escape()`), then convert it with `repo.GetFieldFromFormat("RTF", rtf_string)` before assigning the result to `.Notes`. `GetFieldFromFormat`/`GetFormatFromField` are EA's documented converters between its internal Notes format and external formats like RTF/HTML — because `build_notes()` needs a live `Repository` for this conversion, it takes `repo` as its first argument (unlike most `build_*` helpers in this codebase, which stay pure).

The same Rationale/Test Cases values are *also* written as EA Tagged Values (`Rationale`, `TestCases`) via `set_tagged_value()`, an idempotent helper (finds and updates an existing tag by name instead of the `TaggedValues.AddNew()`-always pattern used in `bpmn_engine.py`, which would duplicate tags on repeated syncs).

`sync_requirements_from_ea.py` reverse-syncs by reading Rationale/TestCases from Tagged Values directly, and strips the `\r?\n\r?\n<b>Rationale:</b>` section back out of `Notes` (EA's internal format, not the original plain-text `\n\nRationale:`) before writing the `- Description:` line, to avoid duplicating that text into both fields.

## Naming Convention (added 2026-07-07)

New requirement `Name` values should lead with either:
- The **GUI component** they belong to, e.g. `CreateAccountScreen: creates Customer and Contacts atomically` — for requirements that are specific to one screen/control, or
- The **business rule** they encode, e.g. `Primary Contact Rule: at least one Contact must always be Primary` — for cross-cutting domain rules that aren't tied to a single screen.

Avoid restating the requirement as a full "EAxCRM must ..." sentence in the Name — that belongs in the Description.

## Source Files

| File | Purpose |
|------|---------|
| `experiments/modelgen/generate_requirements_from_md.py` | Requirements diagram generator |
| `experiments/modelgen/sync_requirements_from_ea.py` | Reads EA requirements back to MD |
