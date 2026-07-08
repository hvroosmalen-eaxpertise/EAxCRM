# Create Customer Account Screen Redesign

**Status**: Approved (design agreed interactively via brainstorming skill)

## Goal

Bring the `CreateAccountScreen` wireframe (`models/EAxCRM-CustomerAccountUI.md`)
up to date with the CRM-6..12 field/validation requirements (issue #7),
which were designed and approved *after* the wireframe was originally built.
The current screen only has Organisation Name, a single Contact Name/Email
pair, and an optional Role combo (Primary/Purchase/Sales/License Holder) —
it explicitly has no address, notes, phone, multi-contact, or opt-in
support yet (per the screen's own `- Description:` field).

## Requirements Coverage

| Requirement | What the screen needs |
|---|---|
| CRM-6 | Atomic Customer+Contact(s) creation — already implicit in the single-Save-button flow, no new control needed |
| CRM-7 | Street address (5 fields) OR PO Box (1 field), mandatory, via a mode toggle |
| CRM-8 | At least one Contact must be Primary; single-contact saves default Role to Primary |
| CRM-9 | Role becomes required once a 2nd Contact row is added |
| CRM-10 | Role list gains a "Secondary" option |
| CRM-11 | Contact.opt_in checkbox, unchecked by default, per Contact |
| CRM-12 | Optional Customer.notes and Contact.phone, capturable at creation |

## Layout Design

Three sections, replacing the current flat field list — mirroring the
original screen's own stated design philosophy (required-to-save fields
prominent, nice-to-have fields de-emphasized):

### 1. Organisation & Contact (always expanded — required)
- Organisation Name (required)
- One repeatable **Contact row**: Name (required on first row), Email
  (required on first row), Role (optional on first row, defaults to
  Primary; required once a 2nd row exists), Phone (optional), Opt-in
  checkbox (optional, unchecked by default) — Phone and Opt-in are Contact
  fields, so they belong on each row, not in a shared section
- "+ Add Contact" link/button below the row. The wireframe draws one
  example row; the control documents (via its Description) that Save
  requires Role once a 2nd row is added

### 2. Address (always expanded — mandatory per CRM-7)
- Two tabs: "Street Address" | "PO Box"
- Street tab (drawn as the default/expanded state): Street Name, House
  Number, Postal Code, City, Country — laid out as one full-width row plus
  two 2-up rows to control vertical space
- PO Box tab: single PO Box text field. A static wireframe can only
  visually foreground one tab state at a time; the PO Box field's existence
  is documented via the tab control's Description rather than drawn
  alongside the Street fields

### 3. Additional Details (collapsed by default — optional)
- Customer Notes (multi-line) — the only field left here once Phone/Opt-in
  moved to the Contact row, since Notes is the one remaining Customer-level
  (not Contact-level) optional field
- No native "collapsible section" control exists in EA's Wireframing MDG
  (confirmed in `2026-07-06-wireframe-diagrams-design.md`'s control-type
  survey — Button/CheckBox/ComboBox/Image/Label/List/Radio/Table/Header/
  Hyperlink/NavigationControl/TextField/TextBlock/Frame only). The section
  is represented as a Frame with a Header labeled "Additional Details
  (optional)"; its Description documents that it is collapsed by default
  in the real UI, drawn expanded here for documentation completeness

## Sizing

Frame grows from 550×420 to roughly 600×820 to fit the address block and
one example Contact row without crowding. Save/Cancel stay at the bottom,
same style as today.

## Verification Plan

Per `feedback_ea_sandbox_testing` — generate into a scratch `.qea` copy (not
`EAxCRM.qea`), left in place (not deleted) for the user to open and review
in EA before any of this lands in the real model.

## Addendum: Find by Domain lookup (2026-07-08, added after initial review)

The user asked for a Domain field + button, above the Organisation & Contact
section, to search the configured IMAP mailboxes for existing emails from a
given domain and prefill the fields below (Organisation Name, first
Contact's Name/Email, Address) before Save — distinct from the existing
"Retrieve Customer Email History" screen further down the flow, which
retrieves the *full* communication history after the account already
exists. This is a lookup aid only: the Domain value itself is not saved to
`Customer`.

New controls: `SectionDomainLabel` ("Find by Domain (optional)"),
`DomainLabel`, `DomainField`, `SearchEmailsButton` — placed at the top of
the frame (y=170–224), pushing every other section down by 80px. Frame
grew from 600×800 to 600×880 to fit.

Regenerated into a **second** scratch file,
`models/EAxCRM-scratch-createaccountscreen-v2.qea` — not the original
`EAxCRM-scratch-createaccountscreen.qea`, since the user had that file open
for review in their own EA session at the time (writing into it would have
hung on a file-lock dialog, per `feedback_ea_process_safety`). Generator
reported "Added 25 control(s)" (21 from the initial redesign + 4 new),
clean exit, no hang.

## As-Built Notes (2026-07-08)

Implemented and generated successfully into
`models/EAxCRM-scratch-createaccountscreen.qea` (persistent scratch copy of
`EAxCRM.qea`, not deleted — open it in EA and navigate to the "Create
Customer Account" diagram to review). `generate_customeraccount_ui_from_md.py`
reported "Added 21 control(s) to 'Create Customer Account'" and exited
cleanly — the 12 pre-existing controls were matched by their original GUIDs
and repositioned in place rather than duplicated, confirming the add-and-update
idempotent path worked as designed.

Two adaptations to the approved design, forced by EA's actual Wireframing
MDG vocabulary (`wireframe_config.CONTROL_TYPE_TO_STEREO` — no "Tabs" or
"collapsible section" control exists):
- **Address tabs** → a pair of `Button` controls styled side-by-side, the
  active one set to `State: Selected`. Documented on each button's
  Description.
- **"Additional Details" section header** → a `Label` (not a native
  section/accordion widget), with its Description noting it's collapsed by
  default in the real UI.

Final frame size: 600×800 (vs. the ~600×820 estimate — came in slightly
under). Final Y-layout, top to bottom: Organisation & Contact (y=170–420,
including the repeatable Contact row and "+ Add Contact") → Address
(y=440–614, tabs + Street fields laid out as 1 full-width row + two 2-up
rows) → Additional Details (y=614–710, Customer Notes only) → Save/Cancel
(y=720).

## Data Model Cross-Check (UI ↔ EAxCRM-DataModel.md)

Compared every field now on the redesigned screen against the current
`Contact`/`Customer` entity attributes in `models/EAxCRM-DataModel.md`
(re-read directly, not from memory).

**Current attributes:**
- `Contact`: id (PK), name string(200), email string(254), role string(20),
  phone string(50), opt_in boolean, opt_in_date datetime, created_at,
  updated_at
- `Customer`: id (PK), name string(200), address string (no length set),
  notes string(2000), created_at, updated_at

| Wireframe field | Matching attribute | Assessment |
|---|---|---|
| Organisation Name | `Customer.name` string(200) | Match, no change needed |
| Contact Name | `Contact.name` string(200) | Match, no change needed |
| Contact Email | `Contact.email` string(254) | Match, no change needed (254 is the correct RFC 5321 max) |
| Contact Role | `Contact.role` string(20) | Match on length (longest value "License Holder" = 15 chars fits), but see **type gap** below |
| Contact Phone | `Contact.phone` string(50) | Match, reasonable for international formats |
| Contact Opt-in | `Contact.opt_in` boolean (+`opt_in_date` datetime, auto-set, not a UI field) | Match, no change needed |
| Customer Notes | `Customer.notes` string(2000) | Match, no change needed |
| **Address block** (Street Name, House Number, Postal Code, City, Country, PO Box, mode toggle) | `Customer.address` — a single untyped `string` | **Missing entirely — see below** |

### Gap 1 (significant): structured address has no home in the data model

`Customer.address` is one generic `string` field. The wireframe now needs
**six** discrete pieces of information CRM-7 introduced: `street_name`,
`house_number`, `postal_code`, `city`, `country`, `po_box`, plus a mode flag
recording which format is in use (`address_type`: Street | POBox). None of
these exist as attributes today — everything would have to be crammed back
into one string, defeating the point of collecting them as structured
fields.

This is a real design decision, not something to pick silently:
- **Option A** — decompose `Customer.address` into the six discrete
  attributes above (`address_type` string(10) or an enum, `street_name`
  string(200), `house_number` string(20), `postal_code` string(20), `city`
  string(100), `country` string(100), `po_box` string(50)). Cleaner for
  querying/reporting (e.g. "customers in country X"), but is a real schema
  migration touching every existing `Customer.address` value.
- **Option B** — keep `Customer.address` as one formatted string, composed
  from the structured wireframe entry at save time (app-level string-join
  logic, not a data-model change). Simpler, no migration, but loses the
  ability to query/report on individual address components later.

**Recommendation: Option A.** The whole point of CRM-7 was to stop treating
address as an opaque blob (the PO-Box-vs-street problem it was solving is a
structure problem); collecting structured fields in the UI just to
re-flatten them into a string on save would keep the original problem at
the database layer while adding UI complexity for no query-time benefit.

### Gap 2 (moderate): `Contact.role` is an unconstrained string, not an enum

The five allowed values (Primary, Purchase, Sales, License Holder,
**Secondary** — the last one new as of CRM-10) currently live *only* in the
wireframe's `RoleCombo` control's `Items` tagged value — the data model's
`Contact.role` attribute has no documented value list at all, `<<enum>>`
stereotype, or `choices`-equivalent. Nothing stops an invalid value from
being saved today, and the canonical source of truth for "what roles
exist" is arguably backwards (UI mockup, not data model).

**Recommendation**: document the five allowed values directly on
`Contact.role` in `EAxCRM-DataModel.md` (e.g. as an `<<enum>>`-stereotyped
attribute or a `Notes`/tagged-value listing the choices), so "Secondary" is
recorded as a real data-model change (issue #7's requirement CRM-10),
not just a wireframe-only addition. `string(20)` length itself is fine as-is.

### No other gaps found

Phone, opt_in/opt_in_date, and notes attributes were already sized/typed
appropriately for what the redesigned screen now asks for — no changes
needed there.
