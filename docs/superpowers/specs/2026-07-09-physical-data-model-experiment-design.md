# Physical Data Model Experiment — Design

**Date**: 2026-07-09
**Issue**: [#16 — Physical Data Modelling](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/16)
**Status**: Design, awaiting execution
**Author**: brainstormed with Claude, decisions by Han

## 1. Purpose

Learn Sparx EA's physical data modelling and DDL generation on a small slice of
EAxCRM, and produce an adoption recommendation. This is an experiment — not a
commitment to a permanent PDM layer.

The chosen DBMS is **PostgreSQL** (per commit 0bc4cfa, ArchiMate Technology layer
decision from issue #11).

## 2. Scope

**In scope** — three entities from `models/EAxCRM-DataModel.md`:

- `Customer` — carries the `merged_into` self-referential FK and the
  `address_mode` discriminator
- `Contact` — carries a cross-table FK to `Customer` and a `role` column
- `ContactRole` — modelled twice, once as a lookup table with FK and once as a
  CHECK constraint, so the DDL of both can be compared

That set exercises every mapping we care about: PK, FK-across-tables,
self-referential FK, NotNull, index, enum-like values, and a two-mode
discriminator.

**Out of scope**:

- COM automation for building the PDM (defer until adoption is decided)
- The other 17 entities in `EAxCRM-DataModel.md`
- Integration with Django migrations or Django model generation
- Changes to ArchiMate or the logical UML data-model packages
- Committing anything under `Sandbox` to `master`

## 3. Where the work lives

All modelling happens under the existing **Sandbox → Database Architecture**
package (`PackageID=29`, `guid={3EB11A76-E7A2-4cf2-A245-AEFEA513F6C0}`).
This package already contains `Table1`, `Table2`, and one FK association, which
serves as the reference shape.

Nothing outside `Sandbox` is touched. Sandbox stays local scratch and is not
committed.

Generated DDL and observation artefacts land in a new `experiments/pdm/` folder
in the repo — that folder is in scope for commit.

## 4. Mechanics reference (from sandbox inspection)

Empirically confirmed against the pre-existing `Table1`/`Table2` example. Each
row is the EA-side representation the Database Builder ultimately writes down.

| Concept | EA representation |
|---------|--------------------|
| Diagram | Logical-family diagram with `MetaType='Extended::Data Modeling'`, notation `Information Engineering` (crow's-foot) |
| Table | `Class` stereotyped `table`; tagged values `DBVersion`, `Owner`, `Tablespace` |
| Column | `Attribute` stereotyped `column`; datatype string is Postgres-native (`uuid`, `varchar` + `Length`, `timestamp with time zone`, `integer`, `real`) |
| Primary key | Operation stereotyped `PK`, named `PK_<Table>`, PK column(s) as `in` parameters |
| Foreign key | Three coordinated artefacts on the child: (1) Operation stereotyped `FK`, named `FK_<Child>_<Parent>`, with tagged values `Delete`, `Update`, and the `property=…` mirror; (2) Operation stereotyped `index`, named `IXFK_<Child>_<Parent>`; (3) `Association` connector **stereotyped `FK`**, `SupplierEnd.Role='PK_<Parent>'` @ `1`, `ClientEnd.Role='FK_<Child>_<Parent>'` @ `0..*` |
| Index | Operation stereotyped `index` |
| DDL generation | User-triggered via EA Database Builder (no scripting) |

**Open item — NotNull encoding.** Neither `t_attribute` nor `t_attributetag`
carries a dedicated NotNull column. The likely encoding is `AllowDuplicates`
inverted (`0 → NOT NULL`, `1 → NULL allowed`), matching EA's historical
convention. This is the first thing Phase A pins down. A UUID column serving as
`PK` does not need an explicit NotNull — the DDL generator emits it implicitly
alongside the `PRIMARY KEY` clause.

## 5. Approach — manual in EA GUI

No COM automation for the modelling work. Every mechanic gets verified by
hand, once, and recorded as a numbered finding. That respects the "verify EA COM
empirically" rule — we're not committing to an automation path until we know the
shape.

### Phase A — Baseline & NotNull confirmation

1. Open `Sandbox → Database Architecture → Database Architecture` diagram
2. Right-click `Table1` in the Database Builder → Generate DDL. Save the output
   to `experiments/pdm/table1_baseline.sql`. This proves the generator runs on
   the current sandbox state.
3. On any column, toggle NotNull once, save the model, re-inspect
   `AllowDuplicates` via COM, and confirm the mapping. Record as finding F1.

### Phase B — Model the slice

4. Create three tables under the same package:
   - `customer` with `id` (uuid PK), `name`, `notes`, `address_mode`,
     `street_name` … `country`, `po_box`, `created_at`, `updated_at`, plus
     `merged_into_id` (uuid, self-FK to `customer.id`, nullable)
   - `contact` with `id` (uuid PK), `name`, `email`, `phone`, `opt_in`,
     `opt_in_date`, `created_at`, `updated_at`, `role`, and
     `customer_id` (uuid, FK to `customer.id`, NOT NULL)
   - `contactrole` lookup table with `code` (varchar PK) and `label` (varchar).
     Model this only for the lookup-table variant of the enum comparison; skip
     it in the CHECK-constraint variant.
5. PKs modelled as Operations stereotyped `PK` (matches the sandbox pattern).
6. FKs modelled with the full three-artefact pattern from §4:
   - `contact.customer_id → customer.id`
   - `customer.merged_into_id → customer.id` (self-referential, nullable)
   - `contact.role → contactrole.code` (lookup-table variant only)
7. For the CHECK-constraint variant, express the enum as an element-level
   constraint on `contact` or an attribute-level constraint on `role`. Record
   which representation EA accepts and how the DDL differs.

### Phase C — Generate & apply

8. Package-level Generate DDL over the whole `Database Architecture` sandbox
   package. Save to `experiments/pdm/eaxcrm_slice.sql` (lookup-table variant)
   and `experiments/pdm/eaxcrm_slice_check.sql` (CHECK variant).
9. Apply both scripts to a throwaway Docker Postgres. Both must create cleanly
   — record any manual edits needed.
10. Change one column type in EA (e.g. `varchar(200) → varchar(255)`),
    regenerate, diff against the previous script. Record the round-trip cost.

### Phase D — Findings & recommendation

11. Extend §7 of this document with F1..Fn — one finding per resolved mechanics
    question, each with the EA screenshot or COM excerpt that proves it.
12. Post a summary comment on issue #16 with the adoption recommendation:
    **adopt**, **adopt-with-caveats**, or **shelve**, each with the reasons
    tied to the numbered findings.

## 6. Deliverables

- `experiments/pdm/table1_baseline.sql` — DDL from the untouched sandbox
- `experiments/pdm/eaxcrm_slice.sql` — DDL from the slice, lookup-table variant
- `experiments/pdm/eaxcrm_slice_check.sql` — DDL from the slice, CHECK variant
- Findings F1..Fn appended to §7 of this document
- Comment on issue #16 with the adoption recommendation

## 7. Findings

_To be filled in during Phases A–D. Each finding has the same shape:
question → observed EA behaviour → evidence (screenshot or COM excerpt) →
implication for adoption._

- **F1** — NotNull encoding (pending)
- **F2** — PK-implicit NotNull in generated DDL (pending)
- **F3** — Whether package-level Generate DDL covers all tables in one run
  (pending)
- **F4** — CHECK-constraint representation for enum-like columns (pending)
- **F5** — Round-trip cost: single-column type change → regenerate → diff
  (pending)

## 8. Success criteria

The experiment succeeds when all of the following are true:

- EA generates valid Postgres DDL from the sandbox package.
- Every mapping in §4 is confirmed by a numbered finding, including NotNull.
- Both slice variants (lookup table and CHECK) apply cleanly to Postgres.
- A round-trip change is documented with click-cost.
- Issue #16 carries an adoption recommendation grounded in the findings.

The experiment fails (and produces a "shelve" recommendation) if any of these
turn out to be blockers:

- The DDL generator produces invalid Postgres for standard constructs.
- A required mapping (PK, FK, NotNull, or CHECK) has no reachable EA
  representation.
- Round-trip cost is so high that maintenance would exceed the benefit.
