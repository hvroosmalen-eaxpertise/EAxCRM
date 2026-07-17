---
name: ea-wireframe-creator
description: Reference for generating/syncing EA Wireframe (UI mockup) diagrams via wireframe_config.py/wireframe_engine.py — explicit per-control bounds (no flow-layout algorithm), one diagram per Screen + a sitemap overview, canonical stereotype casing, and the Wireframing diagram-type/toolbox fix. Read ea-model-common first for shared COM/session/GUID-map/Sandbox patterns.
---

# EA Wireframe Creator (EAxCRM Project Skill)

## Overview

Covers EA's built-in **Wireframing** MDG technology (UI mockups for Screens/Buttons/Labels/etc.), added for github issue #4. **Read `ea-model-common` first** for the coordinate system, GUID map pattern, COM session lifecycle, and Sandbox isolation protocol — this skill covers what's genuinely different about wireframes: **a wireframe's positions ARE its content** (there's no "flow" to derive a button's position from, unlike BPMN/ArchiMate), so layout is explicit per-control bounds authored in the MD, not a computed algorithm.

Architecture mirrors the BPMN config/engine split (`bpmn_config.py`/`bpmn_engine.py`) rather than folding into it or into the shared non-BPMN grid path — the underlying logic is fundamentally different in both directions. See `docs/superpowers/specs/2026-07-06-wireframe-diagrams-design.md` for the full design.

Ground truth for every stereotype/tagged-value name below came from reading the installed `MDGTechnologies/Wireframing.xml` technology definition directly — the online Sparx user guide returned 403 to automated fetches, so don't rely on it; read the local XML file instead if anything here needs re-verifying.

## MD Schema

Same `### Type—id` / `- Field: value` convention as the other generators:

```markdown
## Flow—ManageCustomerAccountUI
- Name: Manage Customer Account UI
- Sitemap Diagram Name: Manage Customer Account UI — Sitemap
- Description: ...

### Screen—CreateAccountScreen
- Name: Create Customer Account
- Type: Screen
- Description: ...

#### Control—CreateAccountSaveButton
- Name: Save
- Type: Button
- Screen: CreateAccountScreen
- Bounds: 20, 200, 100, 30
- State: Normal

## Navigation
- CreateAccountScreen → MergeAccountsScreen [Save, duplicate found]
```

- **`- Bounds: x, y, width, height`**: ordinary top-left-origin, positive-Y-down (like any mockup tool). `wireframe_engine.py`'s `parse_bounds()`/diagram-object placement flips the sign internally for EA's own convention (see `ea-model-common`'s coordinate rules) — the MD author never deals with that.
- **Unlike BPMN/ArchiMate, `"Flow"` is a documentation-only grouping** (the MD header) — there's no EA element analogous to BPMN's `CollaborationModel` anchoring the diagrams. Screens and their diagrams are created directly under the flow's package.
- **`## Navigation`**: flat list of `ScreenA -> ScreenB [trigger]`. Rendered as a plain **labeled Association connector** between the two Screen elements — there is no dedicated navigation-connector stereotype in the Wireframing MDG, this is a project convention.

## Control Type → Stereotype Table (casing matters!)

`wireframe_config.CONTROL_TYPE_TO_STEREO` maps the MD's `- Type:` value to an EA stereotype short name + base Sparx type (`GUIElement` for most controls, `Text` for text blocks, `Screen` for the screen container itself).

**Casing bug found and fixed (2026-07-06):** the Wireframing MDG's own `UIToolboxes` Tag entries reference some stereotypes in a *different, non-canonical* case than their actual `<Stereotype name="...">` definition — e.g. the toolbox page lists `Wireframing::Wireframebutton(UML::GUIElement)` (lowercase "button"), but the real definition is `<Stereotype name="WireframeButton" metatype="Button">` (capital "Button"). **Both work for *creating* an element** (EA's stereotype matching is case-insensitive there), but **`elem.StereotypeEx` reads back the canonical case** — so a config using the toolbox-tag casing breaks the reverse stereo→MD-Type lookup used during sync, silently falling back to displaying the raw stereotype name instead of the friendly MD type. Confirmed by grepping the actual `<Stereotype name="...">` definitions in the XML directly, not the `UIToolboxes` Tag list. If adding a new control type, look up its canonical case the same way — don't copy from the Tag list.

## Tagged Values

Each control type has a small, specific set of tagged values defined in `wireframe_config.WIREFRAME_TAGGED_VALUES` (an allow-list per type, used both ways: only listed names are set on generate, and only listed names are read back on sync):

| Control Type | Tagged Values |
|---|---|
| Button | `State` (Normal/Focused/Selected/Disabled) |
| CheckBox | `Enabled`, `State` (Checked/Unchecked) |
| ComboBox | `DropDownState` (Open/Closed), `Items` (comma-separated list, shown literally as static mockup text — not a real dropdown) |
| Radio | `Enabled`, `State` (Selected/Unselected) |
| Label | `Align Text` (Left/Center/Right), `Multiline` |

`wireframe_engine.set_tagged_values()` is idempotent — updates an existing `TaggedValue` in place rather than adding a duplicate on re-run (unlike the plain `elem.TaggedValues.AddNew()` pattern used elsewhere, which doesn't check for an existing entry first).

## Diagram Structure: One Per Screen + a Sitemap

Since each screen mockup needs real canvas space for its controls (unlike BPMN's small boxes that fit many per diagram), each Screen element gets its **own child diagram** (`elem.Diagrams.AddNew(...)` — the Screen element itself owns the diagram, double-click-navigable in EA's Project Browser, the same general EA feature BPMN's `CollaborationModel` uses, just applied to a leaf element here instead of a process root). A separate lightweight **sitemap diagram** (under the flow's package, not anchored to any element) shows every Screen as a small box (via `diagram_utils.compute_grid_positions`, not explicit bounds — this one overview diagram doesn't need pixel-perfect layout) with the Navigation connectors between them, labeled with their triggers.

## Controls Are Parented Under Their Screen (containment gotcha)

Controls are created with `ParentID` set to their Screen's `ElementID` — this means they **disappear from the flow package's own flat `Elements` collection** (same gotcha documented in `ea-model-common`'s "Refresh() Stale-Proxy / Containment Bug", first found for BPMN Lane children, found *again* independently for wireframe Controls). During `sync_to_md`, you must find Screens in the package's flat list first, then recurse into **each Screen's own `.Elements` collection** to find its Controls — scanning only the flat package list silently drops every control with no error.

## Diagram Type and Toolbox (unverified — see caveat)

Same `StyleEx`/`MDGDgm` mechanism as BPMN/ArchiMate (see `ea-model-common`). Native `Diagram_Type` for every Wireframing diagram stereotype is **`"Custom"`** (`Diagram_Custom` in the MDG XML) — different from ArchiMate's `"Logical"` and BPMN's `"Analysis"`. The Webpage Wireframe stereotype's own `styleex` property is `Whiteboard=1;`, which must be combined with the `MDGDgm` token:

```python
diag = elem.Diagrams.AddNew(name, "Custom")
diag.Stereotype = ""
diag.StereotypeEx = ""
diag.StyleEx = "MDGDgm=Wireframing::Webpage Wireframe;Whiteboard=1;"  # see caveat below
diag.Update()
```

**Caveat: this is unverified against a real EA-built reference diagram, unlike the BPMN/ArchiMate fix.** No user confirmation has happened yet for wireframes specifically. If the toolbox doesn't show correctly, get a real reference the same way the BPMN one was obtained: have the user hand-build + correctly type a Webpage Wireframe diagram in EA's GUI, then **read its `Diagram.StyleEx`/`Diagram.Type` via COM** (`repo.GetDiagramByGuid(guid)` then just read the properties directly — reading is not the constrained operation, only *overwriting an already-non-empty StyleEx* is) and compare against what the generator currently produces — **don't just trust the MDG XML's stated values**, per the hard lesson in `ea-model-common` (a reference diagram proves the mechanism, but the specific value must match what the target diagram actually represents, and even the mechanism itself should be confirmed, not assumed, for a technology not yet user-verified).

**Hard rule (2026-07-06, see `ea-model-common`): no SQLite, ever, for this or any other diagram fix.** An earlier version of this generator batched `Diagram_Type`/`StyleEx` corrections via direct SQL after the COM session closed — removed. `generate()` now only sets `Type`/`StyleEx` correctly via COM at diagram-creation time (the normal case, since new diagrams are always created with the right `DIAGRAM_NATIVE_TYPE`/`StyleEx` from the start). If an *existing* diagram is ever found with the wrong `Diagram_Type` or `StyleEx`, `generate()` logs a warning naming the diagram and what's wrong rather than attempting any fix — there is no COM-only way to correct it after the fact, so it needs a manual fix in EA's GUI (or an explicit, user-approved recreate-the-diagram pass, carrying over existing `DiagramObjects` positions first).

## Layout: Explicit Bounds, Add-and-Update on Re-run

Unlike BPMN (which never reflows an existing diagram — see ea-bpmn-creator's "Re-run Position Management") or ArchiMate/Data Model/Requirements (add-only, preserve manual layout), wireframes **push MD bounds changes through for already-placed controls too** on every `generate()` run, not just newly-added ones — a wireframe's positions are its authored content, so if the MD changes a control's `Bounds`, the diagram should reflect that on next generate. New controls are still added via the same `diagram_utils.add_missing_elements` used elsewhere; already-placed ones are compared against their MD-declared bounds and only updated if actually different. Consequence: **any manual layout tuning done in EA's GUI on an already-authored control will be overwritten on the next generate if the MD's `Bounds` for that control disagrees.** Data-only edits (Description, Name, etc. — leaving `Bounds` alone) do NOT touch positions: the bounds-diff check reads `current_bounds == new_bounds` and skips the write.

## Button Description Convention

Every `Button` control's `Description` field is its **onclick contract** — what the button does, what state it changes, and where the flow goes next. Because the Notes pane is where staff (and future-me) look for behavioural intent, an unlabelled Button is a real documentation gap.

Rules:
- One-line imperative starting with the action verb (`Persists…`, `Discards…`, `Runs…`, `Sets…`, `Advances…`, `Leaves…`).
- Cite the governing requirement ID in parentheses when one applies (e.g. `CRM-6`, `CRM-14`, `CRM-15`, `CRM-16`).
- Plain text — no `**bold**` labels, no four-part Why/What/How/Context shape. That template is for BPMN Activities; a Button description is one thing.
- Reference the downstream flow explicitly ("routes to X", "ends the process at Y") rather than leaving the transition implicit — it's the click contract, not just a UI label.

Example (from CreateAccountScreen's Save button):

> Persists the Customer + Contact(s) as one atomic transaction (CRM-6); on success routes to the Duplicate found? check, which decides between Merge Customer Accounts and Retrieve Customer Email History.

**Lint** (`wireframe_engine.py`, first pass — non-fatal): each Button with no `Description` prints `[lint] Button 'X' on screen 'Y' has no Description — add one so its click contract is documented in EA.`; a tally line at the end of the run reports the total. Sync does not fail on lint hits — it's a heads-up, not a gate.

## Quick Reference

| Diagram type | Element sizing | Diagram_Type / StyleEx MDGDgm |
|---|---|---|
| Webpage Wireframe (per screen + sitemap) | Explicit per-control `- Bounds:` in MD, no computed layout | `Custom` / `Wireframing::Webpage Wireframe;Whiteboard=1;` (unverified, see caveat above) |

## Source Files

| File | Purpose |
|------|---------|
| `modelgen/wireframe_config.py` | `WireframeFlow` dataclass + `CUSTOMER_ACCOUNT_UI` instance + Wireframing MDG vocabulary (`CONTROL_TYPE_TO_STEREO`, `WIREFRAME_TAGGED_VALUES`, `DIAGRAM_NATIVE_TYPE`, `DIAGRAM_STYLEEX_MDGDGM`) |
| `modelgen/wireframe_engine.py` | `parse_md`, `generate`, `sync_to_md`, `set_tagged_values`, `reset_diagram_stereotype_com`/`apply_diagram_toolbox_fixes` |
| `modelgen/generate_customeraccount_ui_from_md.py` | Thin wrapper: `wireframe_engine.generate(wireframe_config.CUSTOMER_ACCOUNT_UI)` |
| `modelgen/sync_customeraccount_ui_from_ea.py` | Thin wrapper: `wireframe_engine.sync_to_md(wireframe_config.CUSTOMER_ACCOUNT_UI)` |
| `models/EAxCRM-CustomerAccountUI.md` | First real content: Create Customer Account, Merge Customer Accounts, Retrieve Customer Email History, Suggest Newsletter Opt-in |
