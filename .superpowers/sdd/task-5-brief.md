# Task 5: Wire Requirements generator + sync + seed scripts

**Goal:** Add changelog logging to the Requirements generator, sync, and seed scripts.

## Context

Tasks 1-4 wired the BPMN engine, ArchiMate generator, and UML Data Model scripts. Now wire the Requirements scripts.

## Files

- **Modify:** `experiments/modelgen/generate_requirements_from_md.py`
- **Modify:** `experiments/modelgen/sync_requirements_from_ea.py`
- **Modify:** `experiments/modelgen/seed_requirements_properties.py`

## generate_requirements_from_md.py

Pattern: element create/update loops + diagram placement.

1. Add `from changelog import ChangeLog` import
2. After the "Parsed N requirements..." print, open changelog:
   ```python
   SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
   clog = ChangeLog(os.path.join(SCRIPT_DIR, "requirements_changelog.md"))
   clog.checkpoint("Parsed MD")
   ```
3. In the element loop — the generator has a create/update pattern similar to ArchiMate generator. Read the actual file's variable names and adapt. For each create/update:
   - Create: `clog.log("created", req["id"], req["name"], "Requirement", new_elem.ElementGUID if new_elem else "")`
   - Update: `clog.log("updated", req["id"], req["name"], "Requirement", existing.ElementGUID)`
4. In the connector loops (parent Aggregation, entity Realisation), add:
   - `clog.log("created", rel_id, label, "Realisation"|"Aggregation", new_conn.ConnectorGUID)`
   - `clog.log("updated", ...)` for existing connectors if detected
5. Before "Done.", close:
   ```python
   clog.checkpoint("Diagram complete")
   clog.close()
   ```

## sync_requirements_from_ea.py

Pattern: reads from EA via COM API, writes MD. Same approach as sync_datamodel_from_ea.py.

1. Add `from changelog import ChangeLog, compute_md_diff` import
2. Before writing MD, read existing content:
   ```python
   old_content = ""
   if os.path.exists(args.md):
       with open(args.md, "r", encoding="utf-8") as f:
           old_content = f.read()
   ```
3. After building `new_content`, compute diff and log:
   ```python
   diff = compute_md_diff(old_content, new_content)
   SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
   clog = ChangeLog(os.path.join(SCRIPT_DIR, "requirements_changelog.md"))
   clog.checkpoint("Sync from EA")
   try:
       clog.log_diff(diff)
   finally:
       clog.close()
   ```
4. Keep existing write-to-disk logic unchanged.

## seed_requirements_properties.py

This sets ID/Status/Version via COM API. It iterates requirements and updates `ea_elem.Alias`, `ea_elem.Status`, `ea_elem.Version`.

1. Add `from changelog import ChangeLog` import
2. Open changelog before the loop:
   ```python
   SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
   clog = ChangeLog(os.path.join(SCRIPT_DIR, "requirements_changelog.md"))
   clog.checkpoint("Seeding properties")
   ```
3. In the loop, log each update:
   ```python
   clog.log("updated", safe_id(name), name, "Requirement", ea_elem.ElementGUID,
            changes={"alias": alias_from_spec, "status": status, "version": version})
   ```
4. Close at end:
   ```python
   try:
       clog.checkpoint("Seed complete")
   finally:
       clog.close()
   ```

## Global Constraints

- No new dependencies beyond Python 3.13 stdlib
- COM API calls not duplicated — changelog hooks reuse existing return values
- Use `try/finally` on all `clog.close()` calls

## Steps

1. Modify `generate_requirements_from_md.py`
2. Modify `sync_requirements_from_ea.py`
3. Modify `seed_requirements_properties.py`
4. **Smoke test generate**: `python experiments/modelgen/generate_requirements_from_md.py` — verify `requirements_changelog.md` exists
5. **Smoke test sync**: `python experiments/modelgen/sync_requirements_from_ea.py` — verify no errors
6. **Smoke test seed**: `python experiments/modelgen/seed_requirements_properties.py` — verify no errors
7. **Commit** with message: `feat: add changelog to Requirements scripts`

## Report

Write report to `\\HAN-ELITEBOOK\Users\hanva\source\repos\EAxCRM\.superpowers\sdd\task-5-report.md`: status, commits, test results, concerns.
