"""One-shot builder for the Physical Data Model experiment slice (issue #16).

Creates customer + contact + contactrole tables under Sandbox → Database
Architecture, following the empirically confirmed EA mapping from spec §4
(with the Phase-B corrections):
  - Class stereotyped 'table', GenType='PostgreSQL'
  - Attributes stereotyped 'column'; NotNull via AllowDuplicates=True
    (F1 polarity CORRECTED — DDL emits NOT NULL when AllowDuplicates=True)
  - Attribute.Pos set incrementally so DDL preserves the intended column
    order rather than falling back to alphabetical
  - PK as Operation stereotyped 'PK' with the PK column as in-parameter
  - FK as three linked artefacts:
      * Operation stereotyped 'FK', StyleEx='FKIDX=<idx op id>;' so EA
        pairs the FK with its supporting index
      * Operation stereotyped 'index'
      * Association connector stereotyped 'FK' with Client/SupplierEnd.Role
        naming the FK op and PK op respectively

Usage:
  python pdm/build_pdm_slice.py             # idempotent build
  python pdm/build_pdm_slice.py --reset     # delete only our 3
                                            # tables + rebuild
  PDM_ONLY=customer python pdm/build_pdm_slice.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath("modelgen"))
from ea_session import ea_repository, get_model_root

QEA = os.path.abspath("models/EAxCRM.qea")
OUR_TABLE_NAMES = {"customer", "contact", "contactrole"}

# --- Slice definition -------------------------------------------------------

TABLES = [
    {
        "name": "customer",
        "columns": [
            # (name, type, length, not_null)
            ("id",             "uuid",                     "0",    True),
            ("name",           "varchar",                  "200",  True),
            ("notes",          "varchar",                  "2000", False),
            ("address_mode",   "varchar",                  "10",   True),
            ("street_name",    "varchar",                  "200",  False),
            ("house_number",   "varchar",                  "20",   False),
            ("postal_code",    "varchar",                  "20",   False),
            ("city",           "varchar",                  "100",  False),
            ("country",        "varchar",                  "100",  False),
            ("po_box",         "varchar",                  "200",  False),
            ("created_at",     "timestamp with time zone", "0",    True),
            ("updated_at",     "timestamp with time zone", "0",    True),
            ("merged_into_id", "uuid",                     "0",    False),
        ],
        "pk": "id",
    },
    {
        "name": "contact",
        "columns": [
            ("id",          "uuid",                     "0",   True),
            ("name",        "varchar",                  "200", True),
            ("email",       "varchar",                  "254", True),
            ("phone",       "varchar",                  "50",  False),
            ("opt_in",      "boolean",                  "0",   True),
            ("opt_in_date", "timestamp with time zone", "0",   False),
            ("role",        "varchar",                  "30",  True),
            ("customer_id", "uuid",                     "0",   True),
            ("created_at",  "timestamp with time zone", "0",   True),
            ("updated_at",  "timestamp with time zone", "0",   True),
        ],
        "pk": "id",
    },
    {
        "name": "contactrole",
        "columns": [
            ("code",  "varchar", "30",  True),
            ("label", "varchar", "100", True),
        ],
        "pk": "code",
    },
]

FKS = [
    # (child_table, child_column, parent_table, parent_pk_column)
    ("customer", "merged_into_id", "customer",    "id"),
    ("contact",  "customer_id",    "customer",    "id"),
    ("contact",  "role",           "contactrole", "code"),
]

TABLE_POSITIONS = {
    "customer":    (280,  580,  -400, -600),
    "contact":     (620,  920,  -400, -600),
    "contactrole": (960, 1160,  -400, -520),
}


# --- Helpers ----------------------------------------------------------------

def find_pkg(root, name):
    if root.Name == name:
        return root
    for sub in root.Packages:
        f = find_pkg(sub, name)
        if f:
            return f
    return None


def reset_our_tables(db, diagram):
    """Delete our three tables (only) from the package + diagram."""
    # Diagram objects first (by ElementID lookup)
    if diagram:
        to_kill = []
        for i in range(diagram.DiagramObjects.Count):
            obj = diagram.DiagramObjects.GetAt(i)
            el = None
            try:
                for e in db.Elements:
                    if e.ElementID == obj.ElementID and e.Name in OUR_TABLE_NAMES:
                        el = e
                        break
            except Exception:
                pass
            if el:
                to_kill.append(i)
        # delete in reverse to keep indices valid
        for i in reversed(to_kill):
            diagram.DiagramObjects.Delete(i)
        diagram.DiagramObjects.Refresh()
        diagram.Update()

    # Elements
    to_kill = []
    for i in range(db.Elements.Count):
        el = db.Elements.GetAt(i)
        if el.Name in OUR_TABLE_NAMES:
            to_kill.append(i)
    for i in reversed(to_kill):
        db.Elements.Delete(i)
    db.Elements.Refresh()
    print(f"  reset: deleted {len(to_kill)} of our tables")


def get_or_create_table(pkg, name):
    for el in pkg.Elements:
        if el.Name == name and el.Type == "Class":
            # ensure GenType stays PostgreSQL
            if el.GenType != "PostgreSQL":
                el.GenType = "PostgreSQL"
                el.Update()
            print(f"    [skip] table {name} exists (id={el.ElementID})")
            return el, False
    el = pkg.Elements.AddNew(name, "Class")
    el.StereotypeEx = "table"
    el.GenType = "PostgreSQL"
    el.Update()
    print(f"    [add ] table {name} (id={el.ElementID})")
    return el, True


def get_or_create_column(el, name, type_, length, not_null, pos):
    # F1 (Phase B correction): AllowDuplicates=True ⇔ NOT NULL
    want_allow_dup = bool(not_null)
    for a in el.Attributes:
        if a.Name == name:
            changed = False
            if a.AllowDuplicates != want_allow_dup:
                a.AllowDuplicates = want_allow_dup
                changed = True
            if a.Pos != pos:
                a.Pos = pos
                changed = True
            if changed:
                a.Update()
            return False
    a = el.Attributes.AddNew(name, type_)
    a.StereotypeEx = "column"
    a.Length = length
    a.AllowDuplicates = want_allow_dup
    a.Pos = pos
    a.Update()
    return True


def ensure_op_parameter(op, param_col, param_type):
    """Add the parameter if the op has none (recovers from earlier crash)."""
    if op.Parameters.Count == 0:
        p = op.Parameters.AddNew(param_col, param_type)
        p.Kind = "in"
        p.Update()
        return True
    return False


def get_or_create_operation(el, name, stereotype, param_col, param_type,
                            tagged_values=None):
    for m in el.Methods:
        if m.Name == name:
            fixed_param = ensure_op_parameter(m, param_col, param_type)
            if fixed_param:
                print(f"      recovered missing param on {name}")
            return m, False
    m = el.Methods.AddNew(name, "")
    m.StereotypeEx = stereotype
    m.Update()
    p = m.Parameters.AddNew(param_col, param_type)
    p.Kind = "in"
    p.Update()
    if tagged_values:
        for tv_name, tv_value in tagged_values.items():
            tv = m.TaggedValues.AddNew(tv_name, tv_value)
            tv.Update()
    return m, True


def set_fk_index_linkage(fk_op, index_op):
    """Set FKIDX=<index_op.MethodID>; on the FK op's StyleEx so EA pairs FK
    with its supporting index (observed on Table1's FK_Table1_Table2)."""
    want = f"FKIDX={index_op.MethodID};"
    if fk_op.StyleEx != want:
        fk_op.StyleEx = want
        fk_op.Update()
        return True
    return False


def get_or_create_fk_connector(child_el, parent_el, fk_op_name, pk_op_name):
    want_styleex = f"FKINFO=SRC={fk_op_name}:DST={pk_op_name}:;"
    for c in child_el.Connectors:
        if (c.SupplierID == parent_el.ElementID
                and c.ClientEnd.Role == fk_op_name
                and c.SupplierEnd.Role == pk_op_name):
            # ensure StyleEx has FKINFO — required for DDL to resolve REFERENCES
            if c.StyleEx != want_styleex:
                c.StyleEx = want_styleex
                c.Update()
            return c, False
    c = child_el.Connectors.AddNew("", "Association")
    c.SupplierID = parent_el.ElementID
    c.StereotypeEx = "FK"
    c.Direction = "Source -> Destination"
    c.StyleEx = want_styleex  # DDL generator reads FKINFO from here for parent resolution
    c.Update()
    c.ClientEnd.Role = fk_op_name
    c.ClientEnd.Cardinality = "0..*"
    c.ClientEnd.Update()
    c.SupplierEnd.Role = pk_op_name
    c.SupplierEnd.Cardinality = "1"
    c.SupplierEnd.Update()
    return c, True


def place_on_diagram(diagram, el, bounds):
    L, R, T, B = bounds
    for obj in diagram.DiagramObjects:
        if obj.ElementID == el.ElementID:
            return False
    obj = diagram.DiagramObjects.AddNew("", "")
    obj.ElementID = el.ElementID
    obj.left = L
    obj.right = R
    obj.top = T
    obj.bottom = B
    obj.Update()
    return True


# --- Main -------------------------------------------------------------------

def main():
    reset = "--reset" in sys.argv
    proof_only = os.environ.get("PDM_ONLY")
    allowed = set(proof_only.split(",")) if proof_only else None

    print(f"Opening {QEA}  (reset={reset}, only={allowed})")
    with ea_repository(QEA) as repo:
        root = get_model_root(repo)
        sb = find_pkg(root, "Sandbox")
        db = None
        for sub in sb.Packages:
            if sub.Name == "Database Architecture":
                db = sub
                break
        if db is None:
            raise SystemExit("Sandbox -> Database Architecture not found")

        diagram = None
        for dg in db.Diagrams:
            if dg.Name == "Database Architecture":
                diagram = dg
                break

        if reset:
            reset_our_tables(db, diagram)

        # 1. Tables + columns + PK operations
        table_els = {}
        for spec in TABLES:
            if allowed and spec["name"] not in allowed:
                continue
            name = spec["name"]
            print(f"\n  Table {name}")
            el, _ = get_or_create_table(db, name)
            table_els[name] = el
            for i, (col_name, col_type, col_len, col_notnull) in enumerate(spec["columns"]):
                created = get_or_create_column(el, col_name, col_type,
                                                col_len, col_notnull, pos=i)
                print(f"    {'[add ]' if created else '[skip]'} col "
                      f"{col_name} {col_type}({col_len}) "
                      f"{'NOT NULL' if col_notnull else 'NULL'} pos={i}")
            pk_col = spec["pk"]
            pk_type = next(c[1] for c in spec["columns"] if c[0] == pk_col)
            _, created = get_or_create_operation(
                el, f"PK_{name}", "PK", pk_col, pk_type)
            print(f"    {'[add ]' if created else '[skip]'} op PK_{name}({pk_col}: {pk_type})")

        # 2. FKs (three artefacts + connector, plus FKIDX linkage)
        for child_name, child_col, parent_name, parent_col in FKS:
            if allowed and (child_name not in allowed or parent_name not in allowed):
                continue
            print(f"\n  FK {child_name}.{child_col} -> {parent_name}.{parent_col}")
            child = table_els[child_name]
            parent = table_els[parent_name]
            child_col_type = next(c[1] for spec in TABLES if spec["name"] == child_name
                                  for c in spec["columns"] if c[0] == child_col)
            fk_op_name = f"FK_{child_name}_{parent_name}"
            ix_op_name = f"IXFK_{child_name}_{parent_name}"
            pk_op_name = f"PK_{parent_name}"

            fk_op, created = get_or_create_operation(
                child, fk_op_name, "FK", child_col, child_col_type,
                tagged_values={
                    "Delete": "No Action",
                    "Update": "No Action",
                    "property": "Delete No Action=1;Update No Action=1;",
                })
            print(f"    {'[add ]' if created else '[skip]'} op {fk_op_name}")

            ix_op, created = get_or_create_operation(
                child, ix_op_name, "index", child_col, child_col_type)
            print(f"    {'[add ]' if created else '[skip]'} op {ix_op_name} (id={ix_op.MethodID})")

            if set_fk_index_linkage(fk_op, ix_op):
                print(f"    [set ] FKIDX={ix_op.MethodID}; on {fk_op_name}")

            _, created = get_or_create_fk_connector(child, parent, fk_op_name, pk_op_name)
            print(f"    {'[add ]' if created else '[skip]'} conn Association FK")

        # 3. Diagram placement
        if diagram:
            print("\n  Diagram placement")
            for name, el in table_els.items():
                if name in TABLE_POSITIONS:
                    placed = place_on_diagram(diagram, el, TABLE_POSITIONS[name])
                    print(f"    {'[add ]' if placed else '[skip]'} obj {name}")

        print("\nDone.")


if __name__ == "__main__":
    main()
