# Task 2: Wire BPMN engine — bpmn_config.py + bpmn_engine.py

**Goal:** Add changelog logging to the shared BPMN engine (covers Sales, Newsletter, and Customer Account processes).

## Context

Task 1 created `ChangeLog` + `compute_md_diff()` in `changelog.py`. Now we wire those into the BPMN config and engine.

## Files

- **Modify:** `experiments/modelgen/bpmn_config.py`
- **Modify:** `experiments/modelgen/bpmn_engine.py`

## Step 1: bpmn_config.py changes

1. Add `import os` at the top of the file
2. Add `SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))` at module level
3. Add `changelog_file: str = ""` field to `ProcessConfig` dataclass
4. Add `changelog_file` to each config instance:
   - CUSTOMER_ACCOUNT: `changelog_file=os.path.join(SCRIPT_DIR, "customeraccount_changelog.md")`
   - SALES: `changelog_file=os.path.join(SCRIPT_DIR, "sales_changelog.md")`
   - NEWSLETTER: `changelog_file=os.path.join(SCRIPT_DIR, "newsletter_changelog.md")`

## Step 2: bpmn_engine.py generate() changes

Add these changes to the `generate()` function:

### 2a: Import ChangeLog

At the top of the file, add:
```python
from changelog import ChangeLog
```

### 2b: Open changelog after parse_md()

After `elements, connectors = parse_md(config, md_path)`, add:
```python
clog = None
if config.changelog_file:
    clog = ChangeLog(config.changelog_file)
    clog.checkpoint("Parsed MD", run_id=config.model_id)
```

### 2c: Log inside create_element()

Inside the `create_element()` inner function, after the "existing" update block (where the element is updated via COM API), add:
```python
if clog:
    changes = {}
    if existing.Name != name:
        changes["Name"] = (existing.Name, name)
    if changes:
        clog.log("updated", eid, name, stereo, existing.ElementGUID, changes=changes)
    else:
        clog.log("updated", eid, name, stereo, existing.ElementGUID)
```

After the "new_elem" create block (where `new_elem` is created via COM API), add:
```python
if clog:
    clog.log("created", eid, name, stereo, new_elem.ElementGUID)
```

### 2d: Log connector creation

After the connector creation loop, add logging for each connector in `conn_list`:
```python
if clog:
    for flow in conn_list:
        src = flow.get("source", "")
        tgt = flow.get("target", "")
        cond = flow.get("condition", "")
        clog.log("created", src + "_" + tgt, src + " -> " + tgt,
                 conn_type, "", changes={"source": src, "target": tgt,
                                          "condition": cond})
```

### 2e: Add checkpoints and close

Before `print("Done.")`:
```python
if clog:
    clog.checkpoint("Diagram complete", run_id=config.model_id)
    clog.close()
```

## Step 3: bpmn_engine.py sync_to_md() changes

In the `sync_to_md()` function, BEFORE the final write block (`output = "...".join(lines) + "\n"` etc.):

```python
from changelog import ChangeLog, compute_md_diff

old_content = ""
if os.path.exists(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        old_content = f.read()

new_content = "\n".join(lines) + "\n"
diff = compute_md_diff(old_content, new_content)

clog = None
if config.changelog_file:
    clog = ChangeLog(config.changelog_file)
    clog.log_diff(diff, run_id=config.model_id)
    clog.close()

# Then write to disk as before:
with open(md_path, "w", encoding="utf-8") as f:
    f.write(new_content)
```

## Steps

1. Modify `bpmn_config.py` with the field, import, and SCRIPT_DIR
2. Modify `bpmn_engine.py` with import, generate() hooks, sync_to_md() MD diff + log_diff
3. **Smoke test**: `python experiments/modelgen/generate_sales_process_from_md.py` — no errors, `experiments/modelgen/sales_changelog.md` exists with content
4. **Test sync**: `python experiments/modelgen/sync_sales_process_from_ea.py` — no errors, changelog appended
5. **Commit** with message: `feat: wire changelog logging into BPMN engine`

## Report

Write report to `\\HAN-ELITEBOOK\Users\hanva\source\repos\EAxCRM\.superpowers\sdd\task-2-report.md` containing: status, commits, test results, concerns.

## Global Constraints

- No new dependencies beyond Python 3.13 stdlib
- COM API calls not duplicated — changelog hooks reuse existing return values
- Changelog files in `experiments/modelgen/`
