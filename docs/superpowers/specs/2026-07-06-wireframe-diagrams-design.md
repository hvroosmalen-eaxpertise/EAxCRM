# Wireframe Diagrams Design (github issue #4)

**Status**: Approved (design agreed interactively; user opted to skip further
back-and-forth review and have implementation proceed directly)

## Goal

Add a generator/sync pair for EA "Wireframe" diagrams (Sparx EA's built-in UI
mockup toolbox), so screens can be designed in EA before the corresponding
Django view/template is built — the same MD-source-of-truth workflow already
used for BPMN, ArchiMate, Data Model, and Requirements. First real content:
the full Manage Customer Account screen flow (Create Customer Account, Merge
Customer Accounts, Retrieve Customer Email History, Suggest Newsletter
Opt-in), wireframed as Webpage Wireframe diagrams with a sitemap overview.

Also addresses the issue's secondary suggestion: split the single
`ea-diagram-creator` skill into one skill per modeling language.

## Background: EA's Wireframing MDG Technology

Confirmed by reading `MDGTechnologies/Wireframing.xml` directly (the
installed technology definition, not just the online docs — the docs site
returned 403 to automated fetches):

- Diagram stereotypes: `Apple Wireframe`, `Android Wireframe`,
  `Dialog Wireframe`, `Webpage Wireframe`, `Windows Phone Wireframe`. All
  apply to native `Diagram_Type = "Custom"` (`Diagram_Custom`), with a
  `styleex` property of `Whiteboard=1;` and a `toolbox` property (e.g.
  `Wireframing::Webpage` for the Webpage type).
- This project uses **Webpage Wireframe** (EAxCRM is a Django web app).
- Webpage screen container: stereotype `WireframeWebsite`, base type
  `UML::Screen`.
- Controls (base type `UML::GUIElement`, some `UML::Text`): `Wireframebutton`
  (Button), `Wireframecheckbox`, `Wireframecombobox`, `Wireframeimage`,
  `Wireframelabel`, `Wireframelist`, `Wireframeradio`, `WireframeTable`,
  `WireframeHeader`, `WireframeHyperlink`, `WireframeNavigationControl`,
  `WireframeTextField`, `WireframeTextBlock` (Text-based), and others.
- Per-control-type tagged values, e.g.: `WireframeButton` has `State`
  (Normal/Focused/Selected/Disabled); `WireframeCombobox` has
  `DropDownState` and `Items`; `WireframeCheckbox`/`WireframeRadio` have
  `Enabled` and `State`; `WireframeLabel` has `Align Text` and `Multiline`.
- **No dedicated navigation-connector stereotype exists** in this MDG —
  screen-to-screen navigation is a project convention we define ourselves
  (see below), not a built-in EA concept.

**Known risk, called out explicitly**: unlike the BPMN/ArchiMate diagram-type
fix (github issue #5), there is no user-built reference wireframe diagram to
empirically verify the `Diagram_Type`/`StyleEx` combination against this
time. The values above are the best evidence available (direct technology
XML), but per the hard lesson from issue #5 — reading the MDG XML alone
was *not* sufficient for BPMN/ArchiMate; a real reference diagram was needed
to find the actual `StyleEx` `MDGDgm=` mechanism and to catch a wrong value
copied from an unrelated reference. **This must be verified in EA's GUI
once available, and treated as unconfirmed until then.**

## Architecture

New files, mirroring the existing BPMN config/engine split
(`bpmn_config.py`/`bpmn_engine.py`) rather than folding into it — the
underlying logic is fundamentally different (explicit per-control bounds
instead of computed flow layout; one diagram per screen instead of one
diagram per process; no lanes/gateways/sequence flows):

```
experiments/modelgen/
├── wireframe_config.py                        # WireframeFlow dataclass + instances
├── wireframe_engine.py                        # parse_md, generate(), sync_to_md()
├── generate_customeraccount_ui_from_md.py      # thin wrapper
├── sync_customeraccount_ui_from_ea.py          # thin wrapper
├── customeraccount_ui_guid_map.json            # idempotency map (created on first run)
└── customeraccount_ui_changelog.md             # audit trail (created on first run)

models/
└── EAxCRM-CustomerAccountUI.md

.opencode/skills/
├── ea-model-common/SKILL.md      # shared: COM session lifecycle, coordinate
│                                  # system, changelog usage, sandbox isolation,
│                                  # zombie process cleanup -- referenced by all
│                                  # 5 language-specific skills below
├── ea-bpmn-creator/SKILL.md       # extracted from ea-diagram-creator
├── ea-archimate-creator/SKILL.md  # extracted from ea-diagram-creator
├── ea-datamodel-creator/SKILL.md  # extracted from ea-diagram-creator
├── ea-requirements-creator/SKILL.md # extracted from ea-diagram-creator
└── ea-wireframe-creator/SKILL.md  # new
```

`ea_session.py` and `changelog.py` are reused as-is, no changes needed.

## MD Schema

Same `### Type—id` / `- Field: value` convention as the other generators:

```markdown
# EAxCRM — Manage Customer Account UI

**Model ID**: cap-ui-eacrm
**Purpose**: Wireframe mockups for the Manage Customer Account screens

## Flow—ManageCustomerAccountUI
- Name: Manage Customer Account UI
- Sitemap Diagram Name: Manage Customer Account UI — Sitemap
- Sitemap Diagram GUID: {...}
- Description: ...

### Screen—CreateAccountScreen
- Name: Create Customer Account
- Type: Screen
- Stereotype: WireframeWebsite
- GUID: {...}
- Diagram Name: Create Customer Account
- Diagram GUID: {...}
- Description: ...

#### Control—CreateAccountOrgName
- Name: Organisation Name
- Type: TextField
- Screen: CreateAccountScreen
- Bounds: 20, 60, 300, 24
- Description: ...

#### Control—CreateAccountSaveButton
- Name: Save
- Type: Button
- Screen: CreateAccountScreen
- Bounds: 20, 200, 100, 30
- State: Normal

## Navigation
- CreateAccountScreen -> MergeAccountsScreen [Save, duplicate found]
- CreateAccountScreen -> EmailHistoryScreen [Save, no duplicate]
```

- **`- Bounds: x, y, width, height`**: ordinary top-left-origin,
  positive-Y-down (like any mockup tool). `wireframe_engine.py` flips the
  sign internally for EA's own DiagramObject convention (Y negative below
  origin, per the coordinate rules already documented for BPMN/ArchiMate) —
  the MD author never deals with that.
- **`- Type:`** on a Control maps to a stereotype via a
  `CONTROL_TYPE_TO_STEREO` table in `wireframe_config.py` (mirrors
  `bpmn_config.py`'s `LABEL_TO_STEREO`).
- Per-control-type tagged values (`State`, `Enabled`, `Items`, `Align Text`,
  `Multiline`) are optional extra `- Field:` lines, applied per type the
  same way `BPMN_TAGGED_VALUES` works today (a
  `WIREFRAME_TAGGED_VALUES` dict keyed by control type).
- Each Screen carries its own diagram identity (own Name/GUID) since each
  screen gets its own diagram; the Flow header carries the sitemap
  diagram's identity.
- **`## Navigation`**: flat list of `ScreenA -> ScreenB [trigger]`, same
  shape as `### Sequence Flows`. Rendered as a plain labeled
  Association connector between the two Screen elements (no dedicated
  navigation-connector stereotype exists in the Wireframing MDG, so this is
  a project convention, chosen for consistency with how BPMN/ArchiMate
  connectors round-trip through MD already).

## Generate Direction (MD -> EA)

`wireframe_engine.generate(flow_config)`:

1. Parse MD (Flow header, Screens, Controls, Navigation).
2. Create/update a `User Interface` top-level package (new architecture
   domain, parallel to Process/Application/Data Architecture), then a
   `<Flow Name> Architecture` sub-package under it — same
   get-or-create-package pattern as `generate_archimate.py`. Unlike BPMN,
   "Flow" is a documentation-only grouping (the MD header), not an actual
   EA element — there's no element analogous to BPMN's CollaborationModel
   anchoring the diagrams; Screens and their diagrams are created directly
   under the flow package, same as ArchiMate/Data Model/Requirements.
3. Create/update each Screen element (base type `Screen`, stereotype
   `WireframeWebsite`) directly under the flow package.
4. Create/update each Control element (base type `GUIElement` or `Text`,
   stereotype per `CONTROL_TYPE_TO_STEREO`), `ParentID` set to its Screen
   (containment, same pattern as BPMN Lane children).
5. Create/update one diagram per Screen (`Diagram_Type="Custom"`,
   `StyleEx` including `MDGDgm=Wireframing::Webpage Wireframe;Whiteboard=1;`
   — see risk note above), placing each Control at its explicit
   (sign-flipped) bounds. No flow-layout algorithm — bounds are authoritative.
6. Create/update the Navigation connectors (Association, labeled with the
   trigger text) between Screen elements.
7. Create/update the sitemap diagram: same `Diagram_Custom`/`StyleEx`
   treatment, showing every Screen element (as a small box — reuse
   `diagram_utils.compute_grid_positions` since a topology overview doesn't
   need precise bounds) plus the Navigation connectors between them.
8. GUID-map idempotency (element and diagram GUIDs) and changelog logging,
   identical pattern to the other generators — `.log()` at each
   create/update site, `.checkpoint()` at phase boundaries, `.close()` at
   the end.

Re-running `generate()` against an existing flow: Screens/Controls/
Navigation are updated in place (name/description/bounds changes applied);
new Controls/Screens are added without disturbing existing diagram
positions (matches the non-BPMN "preserve manual layout, only add what's
missing" convention — a wireframe's positions are hand-tuned content, not
something to auto-reflow).

## Sync Direction (EA -> MD)

`wireframe_engine.sync_to_md(flow_config)`: reads the flow package's
Screens/Controls/Navigation back into MD text (bounds sign-flipped back to
positive-Y-down), diffed against the old MD via `changelog.compute_md_diff()`
and logged via `ChangeLog.log_diff()`, then written to disk — identical
pattern to `bpmn_engine.sync_to_md()`.

## Skill Reorganization

Split `ea-diagram-creator/SKILL.md` into:

- **`ea-model-common`**: EA COM session lifecycle (`ea_session.py`
  patterns), the EA coordinate system rules, changelog usage, zombie
  process cleanup, and the Sandbox isolation protocol — the parts that
  apply regardless of modeling language.
- **`ea-bpmn-creator`**, **`ea-archimate-creator`**,
  **`ea-datamodel-creator`**, **`ea-requirements-creator`**: the
  language-specific sections of the current skill (BPMN lane layout,
  ArchiMate element sizing, UML class sizing, Requirements-specific
  patterns respectively), each referencing `ea-model-common` for the
  shared infrastructure rather than repeating it.
- **`ea-wireframe-creator`** (new): explicit-bounds authoring, the
  per-control tagged value table, one-diagram-per-screen + sitemap
  structure, and the `Diagram_Custom`/`StyleEx` risk note above.

## First Real Content

`EAxCRM-CustomerAccountUI.md` wireframes the full Manage Customer Account
screen flow: Create Customer Account, Merge Customer Accounts, Retrieve
Customer Email History, Suggest Newsletter Opt-in — each a lightweight but
real screen (a handful of controls, not exhaustive), linked by Navigation
entries matching the existing BPMN process's actual sequence flow branches.

## Validation Plan

1. Syntax/idempotency-check the new engine/config/scripts the same way
   prior generators were verified (dry runs, re-run for idempotency).
2. Run first against a GUID-stripped copy in the `Sandbox` package (same
   isolation protocol used for BPMN/ArchiMate testing), screenshot via
   `SaveDiagramImageToFile` to confirm visual content (box positions,
   labels) renders correctly — this does NOT confirm the toolbox itself
   (IDE chrome isn't exportable), only diagram content.
3. Once content is confirmed correct, run for real against the `User
   Interface` package to create the actual Manage Customer Account UI
   content.
4. Flag the `Diagram_Type`/`StyleEx` toolbox mechanism as unverified pending
   the user checking in EA's GUI — same caveat pattern used for the
   ArchiMate fix in issue #5 before it was user-confirmed.
