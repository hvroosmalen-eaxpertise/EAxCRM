# Task 1: Create changelog.py + tests

**Goal:** Create the shared `ChangeLog` utility and its tests.

## Context

This is the first task in implementing structured audit logging for all EAxCRM generator/sync scripts (6 generators + 6 syncs total). The `ChangeLog` class will be used by all of them.

## Files

- **Create:** `experiments/modelgen/changelog.py`
- **Create:** `experiments/modelgen/test_changelog.py`

## Interface: `ChangeLog(filepath, max_bytes=1_000_000)`

```python
clog = ChangeLog(filepath)  # filepath is the .md changelog path
clog.log(action, eid, name, kind, guid="", changes=None, run_id="")
clog.checkpoint(phase, run_id="")
clog.log_diff(diff: dict, run_id="")
clog.close()  # finalizes entry, prepends to file, trims if over limit
```

## Format

Each `close()` writes a new `##` section prepended to the file:

```markdown
## 2026-07-06 16:30:42 — Sales (generate), run sp-eacrm-20260706-163042

### Checkpoints
- Parsed MD
- Elements complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| CreateRFQ | Create RFQ | Activity | {guid} |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| AcceptOffer | Accept Offer | Activity | {guid} | Notes: old -> new |

### Deleted
| eid | Name | Type | GUID |
|-----|------|------|------|

### Connectors
| Action | Type | Source | Target | Condition |
|--------|------|--------|--------|-----------|
| created | SequenceFlow | CreateRFQ | RegisterRFQ | |
```

## Additional requirement: `compute_md_diff()` in changelog.py

This function goes in `changelog.py` as a module-level function (not a method). It compares two MD texts and returns a structured diff dict that `log_diff()` can consume:

```python
def compute_md_diff(old_content: str, new_content: str) -> dict:
    """Compare two process MD texts and return structured diff dict."""
    import re
    def extract_elements(text):
        elems = {}
        for line in text.splitlines():
            m = re.match(r"#{2,4}\s+(.+?)[\u2014\u2013]\s*(.+)", line)
            if m:
                label = m.group(1).strip()
                eid = m.group(2).strip()
                elems[eid] = {"type": label}
        return elems

    old_elems = extract_elements(old_content) if old_content else {}
    new_elems = extract_elements(new_content)

    old_ids = set(old_elems.keys())
    new_ids = set(new_elems.keys())

    diff = {
        "created": [{"eid": eid, "name": eid, "type": new_elems[eid]["type"]}
                     for eid in sorted(new_ids - old_ids)],
        "deleted": [{"eid": eid, "name": eid, "type": old_elems[eid]["type"]}
                     for eid in sorted(old_ids - new_ids)],
        "updated": [],
        "connectors": [],
    }
    for eid in sorted(old_ids & new_ids):
        old_t = old_elems[eid]["type"]
        new_t = new_elems[eid]["type"]
        if old_t != new_t:
            diff["updated"].append({"eid": eid, "name": eid, "type": new_t,
                                    "changes": {"Type": (old_t, new_t)}})

    def extract_connectors(text):
        conns = set()
        in_conn_section = False
        for line in text.splitlines():
            if re.match(r"###\s+(Sequence|Message|Data)", line):
                in_conn_section = True
                continue
            if line.startswith("## "):
                in_conn_section = False
                continue
            if in_conn_section and line.startswith("- "):
                m = re.match(r"- (.+?)\s*[\u2192\u279e]\s*(.+?)(?:\s*\[(.+?)\])?$", line[2:])
                if m:
                    conns.add((m.group(1).strip(), m.group(2).strip()))
        return conns

    old_conns = extract_connectors(old_content) if old_content else set()
    new_conns = extract_connectors(new_content)

    for src, tgt in sorted(new_conns - old_conns):
        diff["connectors"].append({"action": "created", "type": "connector",
                                    "source": src, "target": tgt, "condition": ""})
    for src, tgt in sorted(old_conns - new_conns):
        diff["connectors"].append({"action": "deleted", "type": "connector",
                                    "source": src, "target": tgt, "condition": ""})

    return diff
```

## Steps

1. **Write failing tests** (in test_changelog.py): test_log_creates_file, test_prepend_newest_first, test_log_updated_with_changes, test_log_deleted, test_size_cap_trims_oldest, test_checkpoint, test_log_diff_created_deleted, test_empty_buffer_no_file, test_compute_md_diff (two texts with different elements)
2. **Implement changelog.py** with all methods + compute_md_diff
3. **Run tests** via `python -m pytest experiments/modelgen/test_changelog.py -v` — all PASS
4. **Commit** with message: `feat: add changelog.py — structured audit logging utility`

## Report

Write a report file at `\\HAN-ELITEBOOK\Users\hanva\source\repos\EAxCRM\.superpowers\sdd\task-1-report.md` containing:
- Status (DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED)
- Commits made (SHAs)
- Test results (command run, summary output)
- Any concerns

## Global Constraints

- No new dependencies beyond Python 3.13 stdlib
- No LLM required for diff computations
