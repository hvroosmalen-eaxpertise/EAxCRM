# Physical Data Model Experiment — Implementation Plan

**Date**: 2026-07-09
**Spec**: [2026-07-09-physical-data-model-experiment-design.md](../specs/2026-07-09-physical-data-model-experiment-design.md)
**Issue**: [#16](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/16)

## Overview

Executes the design's four phases (A baseline / B model / C generate & apply /
D findings) as concrete steps. Manual EA GUI work is on Han; COM inspection and
docs work is on Claude. Every step lists its **actor**, **inputs**,
**outputs**, and **exit criterion** so we can pick up mid-experiment without
losing state.

## Prerequisites

- Sandbox package with `Table1`, `Table2`, and the FK association (already
  present).
- Docker with a throwaway Postgres image reachable locally
  (`postgres:17-alpine` or similar). Confirm with `docker run --rm postgres:17
  --version` before Phase C.
- `experiments/pdm/` folder created and gitignored *only* for `.qea` scratch,
  not for `.sql` outputs — `.sql` outputs are commit artefacts.

## Phase A — Baseline & NotNull confirmation

### A1 — Fresh sandbox inspection snapshot (Claude)
- **Input**: current `models/EAxCRM.qea`
- **Do**: run `scratchpad/inspect_sandbox2.py`, save output to
  `experiments/pdm/sandbox_before.txt`
- **Output**: text snapshot of Sandbox state pre-experiment
- **Exit**: file exists and lists `Table1`, `Table2`, one FK connector

### A2 — Baseline DDL from unmodified sandbox (Han in EA GUI)
- **Do**: Database Builder → right-click `Database Architecture` package →
  Generate DDL → target = PostgreSQL → save output to
  `experiments/pdm/table1_baseline.sql`
- **Output**: SQL file
- **Exit**: file contains `CREATE TABLE table1` and `CREATE TABLE table2` with
  a foreign key clause; no EA errors in the log

### A3 — NotNull encoding lock-down (Han in EA GUI, Claude inspects)
- **Do (Han)**: toggle NotNull on `Table1.attribute 1`, save model (Ctrl+S)
- **Do (Claude)**: re-run `inspect_sandbox2.py`, compare `AllowDuplicates`
  before/after, write result into spec §7 as **F1**
- **Output**: F1 filled in, with the answer *"NotNull ⇔ AllowDuplicates=0"*
  confirmed or refuted
- **Exit**: F1 has a concrete answer plus the COM excerpt as evidence

### A4 — PK-implicit NotNull check (Claude reads DDL)
- **Do**: grep `table1_baseline.sql` for the `id uuid` line; confirm it has
  `NOT NULL PRIMARY KEY` even though the column-level flag was not set
- **Output**: F2 filled in
- **Exit**: F2 answered with SQL excerpt

## Phase B — Model the slice

### B1 — Create `customer` table (Han in EA GUI)
- **Where**: `Sandbox → Database Architecture`
- **Columns**: `id` (uuid, PK), `name` (varchar 200), `notes` (varchar 2000),
  `address_mode` (varchar 10, NotNull), `street_name` (varchar 200),
  `house_number` (varchar 20), `postal_code` (varchar 20),
  `city` (varchar 100), `country` (varchar 100), `po_box` (varchar 200),
  `created_at` (timestamp with time zone, NotNull),
  `updated_at` (timestamp with time zone, NotNull),
  `merged_into_id` (uuid, nullable)
- **PK**: Operation `PK_customer(id: uuid)` stereotype `PK`
- **Self-FK**: connector `Association` stereotype `FK` from `customer` to
  `customer`, with the child-side three-artefact pattern for
  `merged_into_id → id`
- **Exit**: element visible on the diagram, `Generate DDL` on this single
  table succeeds

### B2 — Create `contact` table (Han in EA GUI)
- **Columns**: `id` (uuid, PK), `name` (varchar 200), `email` (varchar 254),
  `phone` (varchar 50), `opt_in` (boolean), `opt_in_date` (timestamp with time
  zone), `role` (varchar 30, NotNull), `customer_id` (uuid, NotNull),
  `created_at` / `updated_at` (timestamp with time zone, NotNull)
- **PK**: `PK_contact(id: uuid)`
- **FK to customer**: full three-artefact pattern for
  `customer_id → customer.id`
- **Exit**: single-table Generate DDL succeeds

### B3 — Enum variant 1: `contactrole` lookup table (Han in EA GUI)
- **Table**: `contactrole` with `code` (varchar 30, PK) and `label`
  (varchar 100)
- **Seed data**: not modelled in EA — noted for a separate `INSERT` script if
  needed
- **FK**: `contact.role → contactrole.code`, three-artefact pattern
- **Exit**: single-table Generate DDL on `contactrole` succeeds

### B4 — Enum variant 2: CHECK constraint (Han in EA GUI, new mini-diagram)
- **Copy** the `contact` table onto a second diagram in the same package (or
  keep on the same diagram — decide during B2). Remove the FK to
  `contactrole`. Add a **table-level constraint** on `contact` (or an
  attribute-level constraint on `role`) expressing
  `role IN ('Primary','Purchase','Sales','License Holder','Secondary')`
- **Record** which representation EA accepts and what the DDL emits — that
  becomes **F4**
- **Exit**: F4 has both the EA-side representation and the DDL fragment

## Phase C — Generate & apply

### C1 — Package DDL, lookup-table variant (Han in EA GUI)
- **Do**: Generate DDL over the whole `Sandbox → Database Architecture` package
  with the lookup-table variant active
- **Output**: `experiments/pdm/eaxcrm_slice.sql`
- **Exit**: file contains `customer`, `contact`, `contactrole` plus all FKs
  and indexes

### C2 — Package DDL, CHECK variant (Han in EA GUI)
- **Do**: after temporarily removing the `contactrole` lookup table and its
  FK (or on the mini-diagram from B4), regenerate
- **Output**: `experiments/pdm/eaxcrm_slice_check.sql`
- **Exit**: file has the CHECK constraint inline and no `contactrole` table

### C3 — Apply both to Docker Postgres (Claude via terminal)
- **Do**: `docker run --rm -d --name pdm-pg -e POSTGRES_PASSWORD=x
  postgres:17-alpine`, then `psql` in each SQL file. Record any manual edits.
- **Output**: `experiments/pdm/apply_notes.md` — one paragraph per variant,
  either "applied cleanly" or "required these edits"
- **Exit**: both variants either apply cleanly or have edits documented

### C4 — Round-trip diff (Han in EA GUI + Claude on diff)
- **Do (Han)**: change `customer.name` from `varchar(200)` to `varchar(255)`
  in EA, regenerate `eaxcrm_slice.sql`
- **Do (Claude)**: `git diff experiments/pdm/eaxcrm_slice.sql` — record what
  changed and the total click-cost (approx clicks Han made) as **F5**
- **Exit**: F5 answered

## Phase D — Findings & recommendation

### D1 — Fill remaining findings (Claude)
- **Do**: complete F1..F5 in spec §7 with concrete evidence
- **Exit**: no "pending" entries remain

### D2 — Adoption recommendation (Claude drafts, Han decides)
- **Do**: append a §9 to the spec titled *Recommendation* — one of
  *adopt / adopt-with-caveats / shelve* — with reasoning tied to F1..F5
- **Exit**: §9 exists and Han signs off

### D3 — Post to issue and close (Claude)
- **Do**: post §9 as a comment on issue #16, then close the issue if adopted
  or shelved (leave open if adopt-with-caveats and follow-up work is queued)
- **Exit**: issue has the recommendation and its final status

## Time estimate

Rough — depends on how much clicking EA needs for connector-role wiring.

- Phase A: 30 min
- Phase B: 90 min (biggest chunk — three tables, three FKs, two variants)
- Phase C: 45 min
- Phase D: 30 min

Total: ~3.5 hours of focused work, splittable across sessions.

## Risks & fallbacks

- **EA DDL generator emits invalid Postgres**: fall back to hand-editing the
  SQL to make it apply, and file the delta as a finding. Only escalates to
  *shelve* if the fixes are structural.
- **CHECK-constraint representation has no reachable EA form**: F4 becomes a
  *no-representation* finding. Weakens the case for adoption but doesn't kill
  it — most CRUD apps live fine with lookup tables.
- **Sandbox commits leak into the tree**: pre-commit reminder — `git diff
  --stat models/EAxCRM.qea` before every commit; `git restore` if the
  sandbox-only changes look ready to slip through.
