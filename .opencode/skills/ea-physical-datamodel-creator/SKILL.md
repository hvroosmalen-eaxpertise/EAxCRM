---
name: ea-physical-datamodel-creator
description: Reference for building physical (DDL-generation-oriented) data models in Sparx EA — tables, columns, PK/FK/index/CHECK as stereotyped Operations, the FKIDX/FKINFO StyleEx encodings that make DDL emit FOREIGN KEY REFERENCES correctly, and the Data Modeling diagram type. Read ea-model-common first for shared COM/session/GUID-map/Sandbox patterns. Distinct from ea-datamodel-creator, which covers the logical UML Class model.
---

# EA Physical Data Model Creator (EAxCRM Project Skill)

## Overview

Covers building tables that EA's Postgres/whatever-else DDL wizard can turn
into valid `CREATE TABLE` / `ALTER TABLE` scripts, plus the COM automation
that produces them idempotently.

Reference implementation: **`experiments/pdm/build_pdm_slice.py`** — builds
the Customer + Contact + ContactRole slice under `Sandbox → Database
Architecture` from a small table/column/FK spec. Uses `ea_session` for
isolation and `--reset` for re-runs.

Full mechanics discovery + evidence trail lives in
`docs/superpowers/specs/2026-07-09-physical-data-model-experiment-design.md`
(issue #16). Findings F1..F7 in §7 are the empirical proofs behind every
mapping below — read them if any mechanic looks surprising, since each
answer took a specific probe to pin down.

**Read `ea-model-common` first** for the coordinate system, GUID map
pattern, COM session lifecycle, and Sandbox isolation protocol — this skill
covers only what's specific to physical data models.

**Distinct from `ea-datamodel-creator`.** That skill is the logical UML
Class model (per-entity sizing scaled to attribute count, Orthogonal Square
routing). Physical models have their own diagram type, their own entity
shape (Table stereotype with tabular column compartment, no attribute-count
sizing), and their own constructs (PK/FK/index/check as stereotyped
Operations). Do not merge the two.

## Diagram Type

**Native `Diagram_Type='Logical'`**, but with `MetaType='Extended::Data
Modeling'` and `TConnectorNotation=Information Engineering` (crow's-foot).
When creating a fresh Data Modeling diagram via COM, set the native type at
creation time and then the `StyleEx` metadata (see `ea-model-common`'s
"Living With COM-Only Constraints" section for why this must be at creation
time; the same rule applies here). Existing diagrams that already have the
right MetaType stay usable — do not try to re-set it from COM.

Currently the sandbox diagram was hand-created; `build_pdm_slice.py`
targets it by name (`"Database Architecture"`) rather than creating a new
one. When adopting for the real model, do add a `Diagrams.AddNew(...,
"Logical")` + `StyleEx` set at creation time.

## Table = Class stereotyped `table`, GenType MUST be the target DBMS

```python
el = pkg.Elements.AddNew(name, "Class")
el.StereotypeEx = "table"
el.GenType = "PostgreSQL"   # F7 — otherwise defaults to 'Java' and DDL is empty
el.Update()
```

**`Element.GenType` is the load-bearing DBMS field.** It mirrors polymorphic
`t_object.PDATA2`. The `DBVersion` tagged value (also standard on tables)
is the DB *version* string (e.g. "PostgreSQL 17") — cosmetic, not the DBMS
selector. Confirmed by inspecting Table1's `PDATA2='PostgreSQL'` after a
UI-set DB, and by watching COM-created tables emit empty DDL until
`GenType` was set explicitly.

**Where does the target DBMS come from at DDL-generation time**: the
package-level Generate DDL wizard reads each table's own `GenType` — not a
package property, not a project default. So every table needs it. Set it on
create.

Standard tagged values on the Table (`DBVersion`, `Owner`, `Tablespace`)
are optional — DDL generator leaves them empty by default and that's fine.

Related: `t_object.PDATA1..5` are polymorphic — the same column means
different things depending on element type/stereotype. Check both the
COM property AND the mirrored PDATA when investigating an EA-internal
field.

## Column = Attribute stereotyped `column`, NotNull via AllowDuplicates=True

Postgres-native datatype strings work directly: `uuid`, `varchar`
(with `Length` set), `timestamp with time zone`, `integer`, `boolean`,
`real`. EA does not need a datatype-mapping layer for the emitted DDL.

```python
a = el.Attributes.AddNew(name, "varchar")
a.StereotypeEx = "column"
a.Length = "200"                    # string, not int
a.AllowDuplicates = True            # F1 — TRUE means NOT NULL in the emitted DDL
                                     # FALSE means the column is nullable
a.Pos = column_index                # F3-adjacent — DDL preserves attribute Pos order
                                     # (falls back to alphabetical when Pos is 0)
a.Update()
```

**F1 NotNull polarity is inverted from the UML meaning.** EA reuses the
UML "isUnique" flag (`Attribute.AllowDuplicates`) for physical column
nullability. `AllowDuplicates=True` ⇔ DDL emits `NOT NULL`;
`AllowDuplicates=False` ⇔ DDL emits `NULL`. The naming is backwards
compared to what you'd guess — Phase A got this wrong the first time by
matching the string "duplicates" to "distinct → NOT NULL". Trust the
inverted mapping, not the intuition.

**F2 PK columns implicitly get `NOT NULL`.** The DDL wizard emits `NOT
NULL` on any PK column, regardless of `AllowDuplicates`. Setting NotNull
on a PK column is harmless but redundant.

**Column order** — set `Attribute.Pos` incrementally as you add columns.
When left unset (all 0), the DDL wizard falls back to alphabetical, which
usually mangles the intended column order.

## Primary Key = Operation stereotyped `PK`

```python
op = el.Methods.AddNew(f"PK_{table_name}", "")
op.StereotypeEx = "PK"
op.Update()
p = op.Parameters.AddNew(pk_col_name, pk_col_type)
p.Kind = "in"
p.Update()
```

Emits `ALTER TABLE ... ADD CONSTRAINT "PK_<name>" PRIMARY KEY (<col>)`.

For multi-column PKs, add multiple `in`-parameters in the order they
should appear in the `PRIMARY KEY (...)` clause. (Untested against
multi-column PKs in this project as of 2026-07-14 — verify empirically
before shipping automation that uses them.)

## Foreign Key = three coordinated artefacts on the child (F6)

FKs need **three linked things**, all on the child table:

1. **Operation stereotyped `FK`** — named `FK_<child>_<parent>`, FK column
   as in-parameter, tagged values `Delete`/`Update`/`property` (mirror
   encoding of the two above), and — critically — `Method.StyleEx =
   "FKIDX=<index_op_MethodID>;"` linking to its supporting index op:

   ```python
   fk_op = el.Methods.AddNew(f"FK_{child}_{parent}", "")
   fk_op.StereotypeEx = "FK"
   fk_op.Update()
   fk_op.Parameters.AddNew(fk_col, fk_col_type).Kind = "in"
   for name, val in [("Delete", "No Action"),
                     ("Update", "No Action"),
                     ("property", "Delete No Action=1;Update No Action=1;")]:
       tv = fk_op.TaggedValues.AddNew(name, val); tv.Update()
   # After creating the index op below, come back and link:
   fk_op.StyleEx = f"FKIDX={index_op.MethodID};"; fk_op.Update()
   ```

2. **Operation stereotyped `index`** — named `IXFK_<child>_<parent>`, same
   FK column as in-parameter. This is the supporting index; the FK op's
   `FKIDX` StyleEx points at this op's `MethodID`.

3. **Association connector stereotyped `FK`** with role names on the ends
   AND `Connector.StyleEx = "FKINFO=SRC=<fk_op>:DST=<pk_op>:;"` — without
   this, DDL emits `REFERENCES  ()` empty even when everything else is
   correct:

   ```python
   c = child.Connectors.AddNew("", "Association")
   c.SupplierID = parent.ElementID
   c.StereotypeEx = "FK"
   c.Direction = "Source -> Destination"
   c.StyleEx = (f"FKINFO=SRC=FK_{child.Name}_{parent.Name}:"
                f"DST=PK_{parent.Name}:;")
   c.Update()
   c.ClientEnd.Role       = f"FK_{child.Name}_{parent.Name}"
   c.ClientEnd.Cardinality = "0..*"
   c.ClientEnd.Update()
   c.SupplierEnd.Role       = f"PK_{parent.Name}"
   c.SupplierEnd.Cardinality = "1"
   c.SupplierEnd.Update()
   ```

**Both StyleEx encodings are required; neither is sufficient alone.**
`FKIDX` pairs the FK operation with its index; `FKINFO` gives the DDL
generator the info to resolve parent table + column from the connector
via the role names. Miss either and the DDL degrades:

- Missing `FKINFO` → `REFERENCES  ()` empty (the bug that ate most of a
  Phase B iteration until we found it by inspecting Table1's raw
  `t_connector` row and diffing StyleEx)
- Missing `FKIDX` → FK works but is not paired with an index on
  regeneration; can also break some downstream tooling

## Index = Operation stereotyped `index`

Same shape as the FK's supporting index op (`IXFK_...`), but standalone
(not paired via `FKIDX`):

```python
op = el.Methods.AddNew(f"IX_{table}_{col}", "")
op.StereotypeEx = "index"
op.Update()
op.Parameters.AddNew(col, col_type).Kind = "in"
```

## CHECK constraint = Operation stereotyped `check`, expression in Method.Code (F4)

```python
op = el.Methods.AddNew(f"CK_{table}_{col}", "")
op.StereotypeEx = "check"
op.Code = "role IN ('Primary','Purchase','Sales','License Holder','Secondary')"
op.Update()
```

**The load-bearing field is `Method.Code`** (persists as `t_operation.Code`).
The Database Builder UI writes to it when you paste the expression into
the constraint editor. Empirical confirmation: on the same op, removing
the `CHECKSTATEMENT` tagged value (an alias EA also honours) but keeping
`Code` populated still produced correct `CHECK (role IN (...))` in the
regenerated DDL. So `Code` alone is enough.

The template dispatch is `%DDLCheckConstraint%`, which emits
`CHECK (%constraintProperty:"CHECKSTATEMENT"%)`, and `CHECKSTATEMENT`
resolves to `Code` for a check-stereotyped Method.

**`Element.Notes` on a check-op emits as `COMMENT ON CONSTRAINT ... IS
'...'` in Postgres DDL.** Useful for documentation, not the load-bearing
field for the CHECK clause itself.

**Constraint tables (`t_objectconstraint`, `t_attributeconstraint` [which
does not exist], `t_connectorconstraint`, `t_operationconstraint`) are
NOT used for CHECK constraints in the physical model.** A connector-level
constraint typed `Invariant` is UML/OCL and is ignored by the DDL wizard.
Do not go looking there.

## DDL generation (F3)

Right-click the **package** (not a table) → **Code Engineering → Generate
DDL** → select target DBMS in the wizard → save. Package-scope emits every
table in the correct application order: drops with `CASCADE` → creates →
PKs+indexes → FKs. Do NOT right-click a single table — that scope emits
one `CREATE TABLE` but leaves any FKs on it dangling (references to
tables not in the script).

Target DBMS in the wizard should match every table's own `GenType`. The
wizard does not aggregate; it walks each table and uses its own `GenType`.

The DDL wizard is user-triggered — no COM path to invoke Generate DDL
directly.

## Quick Reference

| Construct | EA representation | Load-bearing fields |
|---|---|---|
| Table | Class stereotyped `table` | `GenType='PostgreSQL'` (F7) |
| Column | Attribute stereotyped `column` | `AllowDuplicates=True` ⇔ NOT NULL (F1); `Pos` for column order; native datatype string in `Type` (+ `Length` for varchar) |
| Primary key | Operation stereotyped `PK`, name `PK_<table>` | in-parameter names the PK column; PK columns get implicit NOT NULL (F2) |
| Foreign key | 3 artefacts on child (F6) | FK op `.StyleEx=FKIDX=<index_op.MethodID>;` + Association connector `.StyleEx=FKINFO=SRC=<fk_op>:DST=<pk_op>:;` |
| Index | Operation stereotyped `index` | in-parameter names the column |
| CHECK | Operation stereotyped `check` | `Method.Code` holds the SQL expression (F4) |
| DDL scope | Package-level Generate DDL (F3) | right-click package, not table |

## Source Files

| File | Purpose |
|------|---------|
| `experiments/pdm/build_pdm_slice.py` | COM builder for the Customer + Contact + ContactRole slice — idempotent, `--reset` deletes only its own 3 tables; do not use for real model until adopted |
| `experiments/pdm/*.sql` | Generated DDL evidence — `sandbox_baseline.sql` (Table1+Table2), `Customer-Contact-Contactrole-PostgreSQL.sql` (slice) |
| `docs/superpowers/specs/2026-07-09-physical-data-model-experiment-design.md` | Full spec + findings F1..F7 with evidence trail |
| `docs/superpowers/plans/2026-07-09-physical-data-model-experiment-plan.md` | Phase A/B/C/D plan |

## Adoption Status (as of 2026-07-14)

**Experimental — not yet adopted.** The slice lives under
`Sandbox → Database Architecture` in `EAxCRM.qea` as a committed reference
shape (`77240bb`, `c70ef71`). The real `Data Architecture` package is
untouched. Adoption recommendation goes to issue #16 after Phase D. Do
NOT run `build_pdm_slice.py` against any package outside the sandbox
until adoption is decided.
