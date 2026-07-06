# Task 4: Wire UML Data Model generator + sync

**Goal:** Add changelog logging to the UML Data Model generator and sync scripts.

## Context

Tasks 1-3 created `changelog.py`, wired the BPMN engine, and wired the ArchiMate generator. Now wire the UML Data Model scripts.

## Files

- **Modify:** `experiments/modelgen/generate_uml_datamodel.py`
- **Modify:** `experiments/modelgen/sync_datamodel_from_ea.py`

## Steps

### generate_uml_datamodel.py

1. Add `from changelog import ChangeLog, compute_md_diff` import
2. After `Parsed N entities, M relationships` print, open changelog:
   ```python
   SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
   clog = ChangeLog(os.path.join(SCRIPT_DIR, "uml_datamodel_changelog.md"))
   clog.checkpoint("Parsed MD")
   ```
3. In the entity loop, replace the `print(f"  Created: '{name}'")` / `print(f"  Updated: '{name}'")` with:
   - Create: `clog.log("created", safe_id(name), name, "Class", new_elem.ElementGUID if new_elem else "")`
   - Update: `clog.log("updated", safe_id(name), name, "Class", ea_elem.ElementGUID)`
4. In the attribute sync section, replace `print(f"    Deleted attribute '{a.Name}'")` with:
   - `clog.log("deleted", a.Name, a.Name, "Attribute", changes={"entity": name})`
5. In the connector loop, replace `print(f"  Created rel: ...")` with:
   - `clog.log("created", src_name + "_" + tgt_name, src_name + " -> " + tgt_name, rel_type, new_conn.ConnectorGUID)`
6. Before script ends, close:
   ```python
   clog.checkpoint("Diagram complete")
   clog.close()
   ```

### sync_datamodel_from_ea.py

1. Add `from changelog import ChangeLog, compute_md_diff` import
2. Read the existing data model MD file before writing:
   ```python
   md_path = r"M:\EAxCRM\models\EAxCRM-DataModel.md"
   old_content = ""
   if os.path.exists(md_path):
       with open(md_path, "r", encoding="utf-8") as f:
           old_content = f.read()
   ```
3. Build the output in memory (currently the script appends to `lines` list then writes), then:
   ```python
   new_content = "\n".join(lines) + "\n"
   diff = compute_md_diff(old_content, new_content)
   SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
   clog = ChangeLog(os.path.join(SCRIPT_DIR, "uml_datamodel_changelog.md"))
   clog.log_diff(diff)
   clog.close()
   ```
4. Then write to disk (the existing write logic)

## Steps

1. Modify `generate_uml_datamodel.py` with changelog calls
2. Modify `sync_datamodel_from_ea.py` with MD diff + log_diff
3. **Smoke test generate**: `python experiments/modelgen/generate_uml_datamodel.py` — no errors, `uml_datamodel_changelog.md` exists
4. **Smoke test sync**: `python experiments/modelgen/sync_datamodel_from_ea.py` — no errors
5. **Commit** with message: `feat: add changelog to UML Data Model generator and sync`

## Report

Write report to `\\HAN-ELITEBOOK\Users\hanva\source\repos\EAxCRM\.superpowers\sdd\task-4-report.md`: status, commits, test results, concerns.

## Global Constraints

- No new dependencies beyond Python 3.13 stdlib
- COM API calls not duplicated — changelog hooks reuse existing return values
