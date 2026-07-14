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

_Filled during Phases A–D. Each finding has the same shape: question →
observed EA behaviour → evidence → implication for adoption._

### F1 — NotNull encoding (Phase A, 2026-07-09, polarity corrected Phase B)

**Question**: which EA property records column-level `NOT NULL`?

**Observation**: `Attribute.AllowDuplicates` is the storage — **NOT
inverted**. `AllowDuplicates=True` ⇔ DDL emits `NOT NULL`.
`AllowDuplicates=False` ⇔ DDL emits `NULL`. Phase A recorded the polarity
backwards; Phase B's DDL against a slice built with `AllowDuplicates=False`
for intended-NOT-NULL columns proved every column came out `NULL`,
forcing the correction.

**Evidence**: pre-toggle sandbox showed `Table1.attribute 1` with
`AllowDuplicates=True` and `table1_baseline.sql` emitting `NOT NULL`; the
post-toggle sandbox (Han flipped NotNull *off*) showed
`AllowDuplicates=False` and `table1_baseline-null.sql` emitting `NULL`.
Re-checked in Phase B: the `Customer-Contact-Contactrole-PostgreSQL.sql`
generated from tables where `AllowDuplicates=False` on all
intended-NOT-NULL columns emits every column as `NULL` — confirming the
opposite of Phase A's original conclusion.

**Implication**: no adoption blocker; the mapping is stable, just the
opposite of what UML "isUnique" would suggest. When automating table
creation via COM, write `Attribute.AllowDuplicates = True` for a NOT NULL
column.

### F2 — PK-implicit NotNull in generated DDL (Phase A, 2026-07-09)

**Question**: does EA emit `NOT NULL` on PK columns automatically, or must
the column also be flagged NotNull explicitly?

**Observation**: EA emits `NOT NULL` on the PK column in the `CREATE TABLE`
statement even when the column-level NotNull is not set — the `PRIMARY KEY`
constraint is added by a separate `ALTER TABLE`.

**Evidence**: `sandbox_baseline.sql` line 20 emits `id uuid NOT NULL,` and
line 40 adds `ALTER TABLE "Table1" ADD CONSTRAINT "PK_Table1" PRIMARY KEY
(id)`. The `id` column has `AllowDuplicates=True` on disk yet still gets
`NOT NULL` in the DDL.

**Implication**: no adoption blocker. When modelling PK columns in Phase B,
do not also set NotNull on them — EA handles it. Setting both is harmless
but redundant.

### F3 — Package-level Generate DDL covers all tables in one run (Phase A, 2026-07-09)

**Question**: does the "Generate DDL" wizard scope automatically to every
table in the selected package, or one table per invocation?

**Observation**: right-clicking the **package** (not a table) and running
"Generate DDL" produces a single SQL script covering every table plus all
their PKs, indexes, and FKs, in the correct application order (drops with
CASCADE → creates → PKs+indexes → FKs).

**Evidence**: `sandbox_baseline.sql` contains both `Table1` and `Table2`
`CREATE TABLE`s, both `PK_TableN` `ALTER TABLE`s, the `IXFK_Table1_Table2`
`CREATE INDEX`, and the `FK_Table1_Table2` `ALTER TABLE`. Compare with
`table1_baseline.sql` which was generated on Table1 alone and omits
Table2's `CREATE TABLE` entirely (leaving the FK dangling).

**Implication**: no adoption blocker. Phase C's step C1 stands as written —
package-level generation is the right scope. The one-table-only
right-click *is* possible and produces broken output; document this as a
gotcha for anyone running the workflow later.

### F4 — CHECK-constraint representation for enum-like columns (Phase B4, 2026-07-14)

**Question**: how does EA store a table-level CHECK constraint so the DDL
generator emits `ALTER TABLE ... ADD CONSTRAINT ... CHECK (<expression>)`?

**Observation**: another Operation on the table, stereotyped **`check`**, named
`CK_<table>_<column>` — same pattern as PK/FK/index. **The load-bearing field
is `t_operation.Code`** (`Method.Code` in COM), where the Database Builder UI
writes the expression when you paste it into the constraint editor. EA's
Postgres DDL template `%DDLCheckConstraint%` emits
`CHECK (%constraintProperty:"CHECKSTATEMENT"%)`, and `constraintProperty:"CHECKSTATEMENT"`
resolves to `Code` on the operation. A tagged value literally named
`CHECKSTATEMENT` also *works* as a fallback, but is redundant — an empirical
removal (delete the tagged value, keep only `Code`, regenerate) still
produced the correct `CHECK (role IN (...))` in the DDL, confirming `Code`
alone drives the emission.

Constraint-storage tables (`t_objectconstraint`, `t_attributeconstraint`,
`t_connectorconstraint`, `t_operationconstraint`) are NOT used — even though
the Database Builder UI has a "Constraints" tab, the actual CHECK ends up as
a stereotyped Operation, alongside PK/FK/index.

Notes on a check-op will emit as `COMMENT ON CONSTRAINT ... IS '...'` in the
Postgres DDL — useful for documentation but not the load-bearing field for
the CHECK clause itself.

**Evidence**: `experiments/pdm/Customer-Contact-Contactrole-PostgreSQL.sql`
(generated 2026-07-14 14:10) emits
`ALTER TABLE contact ADD CONSTRAINT "CK_contact_role" CHECK (role IN
('Primary','Purchase','Sales','License Holder','Secondary'))` once
`t_operationtag` has a row with `Property='CHECKSTATEMENT'` and the
expression as `VALUE`. Earlier runs with the expression only in
`t_operation.Notes` (with no CHECKSTATEMENT tagged value) emitted `CHECK ()`
empty and moved the expression to a `COMMENT ON CONSTRAINT`.

Investigation trail: `t_xref` for the check-op only carries its stereotype
cross-ref; four constraint tables all empty; the answer came from reading
EA's own DDL template sources (`DDLCreateTableConstraints` → dispatches on
`constraintProperty:"TYPE"` → `%DDLCheckConstraint%` reads
`constraintProperty:"CHECKSTATEMENT"`).

**Implication**: no adoption blocker; automation writes the expression to
`Method.Code` on a check-stereotyped Operation (matches Database Builder UI
convention; no tagged value needed). Lookup-table variant vs CHECK variant
is a modelling choice, not a mechanics limitation.

### F5 — Round-trip cost: single-column type change → regenerate → diff
_(pending — Phase C4)_

### F6 — FK parent resolution requires FKINFO on connector StyleEx (Phase B, 2026-07-09)

**Question**: with the three-artefact FK pattern (FK op + index op + Association
connector with role names), what makes EA's DDL generator emit
`REFERENCES <parent_table> (<parent_column>)` instead of `REFERENCES  ()`?

**Observation**: the Association connector's `StyleEx` field must carry
`FKINFO=SRC=<fk_op_name>:DST=<pk_op_name>:;`. Without it, DDL emits an empty
`REFERENCES  ()` even when the connector's SupplierID, ClientEnd.Role, and
SupplierEnd.Role are all correct. `Method.StyleEx='FKIDX=<index_op_id>;'` on
the FK op is also required (pairs FK with its index), but on its own it's
insufficient — both StyleEx encodings are needed.

**Evidence**: `experiments/pdm/Customer-Contact-Contactrole-PostgreSQL.sql`
generated with `FKIDX` set but connector StyleEx empty emitted
`FOREIGN KEY (customer_id) REFERENCES  ()`. After adding
`FKINFO=SRC=FK_contact_customer:DST=PK_customer:;` to the same connector's
StyleEx (nothing else changed), regeneration produced
`FOREIGN KEY (customer_id) REFERENCES customer (id)`. The raw `t_connector`
row for Table1's reference FK shows the same encoding.

**Implication**: no adoption blocker, but any automation script must set both
`Method.StyleEx=FKIDX=...` on the FK op and `Connector.StyleEx=FKINFO=...`
on its Association. The EA Database Builder UI does this transparently
when you add a foreign key.

### F7 — Target DBMS lives on Element.GenType (mirrored to PDATA2) (Phase B, 2026-07-09)

**Question**: which EA property records the target DBMS for a Table?

**Observation**: `Element.GenType` — not the `DBVersion` tagged value (which
is the DB *version string*, e.g. "Postgres 17"; both empty in our model).
Default for a Class is `'Java'`; must be set to `'PostgreSQL'` for the DDL
wizard to emit Postgres DDL. Mirrored to the polymorphic `t_object.PDATA2`
column.

**Evidence**: `Table1` had `GenType='PostgreSQL'` from the sandbox author.
Three newly-COM-created tables defaulted to `'Java'`; regenerating DDL
picked up an empty schema until `GenType='PostgreSQL'` was set explicitly.

**Implication**: no adoption blocker. COM automation must set `GenType` on
each table. Also worth remembering more generally that `t_object.PDATA1..5`
are polymorphic — meaning depends on element type/stereotype (see
`_opencode_memory` note on PDATA columns).

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
