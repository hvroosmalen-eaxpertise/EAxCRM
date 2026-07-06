# Task 3: Wire generate_archimate.py

**Goal:** Add changelog logging to the ArchiMate model generator.

## Context

Tasks 1-2 created `changelog.py` and wired the BPMN engine. Now wire the standalone ArchiMate generator.

## Files

- **Modify:** `experiments/modelgen/generate_archimate.py`

## Steps

### Step 1: Add import near the top

Find where other imports are, add:
```python
from changelog import ChangeLog
```

### Step 2: Open changelog after parsing

After the line `log("Parsed {len(elements)} elements, {len(relationships)} relationships")`, add:
```python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
clog = ChangeLog(os.path.join(SCRIPT_DIR, "archimate_changelog.md"))
clog.checkpoint("Parsed MD")
```

### Step 3: Log inside element creation/update loop

In the element loop (around `log(f"  [{i+1}/{len(elements)}] Created: ...")`), add:

For existing elements (the `if guid_md:` / update path):
```python
clog.log("updated", elem_id, name, archi_type, ea_elem.ElementGUID,
         changes=({"Notes": (old_notes, notes)} if old_notes != notes else None))
```

For new elements (the `else:` / create path):
```python
clog.log("created", elem_id, name, archi_type, new_elem.ElementGUID)
```

### Step 4: Log inside relationship creation loop

In the relationship loop, for existing relations:
```python
clog.log("updated", rel_id, rel_type, rel_type, existing_guid)
```

For newly created relations:
```python
clog.log("created", rel_id, rel_type, rel_type, new_conn.ConnectorGUID,
         changes={"source": src_elem_id, "target": tgt_elem_id})
```

### Step 5: Close changelog before "Done."

Before the final print statements:
```python
clog.checkpoint("Diagram complete")
clog.close()
```

## Steps

1. Add import, open changelog after parsing
2. Add log calls in element loop (create + update paths)
3. Add log calls in relationship loop
4. Close changelog
5. **Smoke test**: `python experiments/modelgen/generate_archimate.py` — no errors, `archimate_changelog.md` exists
6. **Commit** with message: `feat: add changelog logging to ArchiMate generator`

## Report

Write report to `\\HAN-ELITEBOOK\Users\hanva\source\repos\EAxCRM\.superpowers\sdd\task-3-report.md`: status, commits, test results, concerns.

## Global Constraints

- No new dependencies beyond Python 3.13 stdlib
- COM API calls not duplicated — changelog hooks reuse existing return values
