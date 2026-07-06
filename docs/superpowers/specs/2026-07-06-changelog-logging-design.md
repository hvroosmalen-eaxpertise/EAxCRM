# Changelog: Structured Audit Logging for EAxCRM Generators

**Date**: 2026-07-06

**Issue**: [#2](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/2) — Log element/relationship add/remove events with timestamps

**Status**: Design

## Problem

All EAxCRM generator/sync output goes only to stdout — once the terminal scrolls, the record of what was Created/Updated/Deleted is gone. The `.qea` file is a binary SQLite blob that `git diff` cannot meaningfully compare, and several runs have hung during cleanup (`RefreshModelView`/`CloseFile`) with no way to confirm what actually landed without re-deriving state from scratch.

## Solution

A shared `changelog.py` utility that each generator and sync script calls at every create/update/delete/rename site. Output is per-generator Markdown files (newest-first, ~1 MB cap) that are human-readable and git-diffable.

## Components

### 1. Shared `changelog.py` API

```python
class ChangeLog:
    def __init__(self, filepath: str, max_bytes: int = 1_000_000):
        ...

    def log(self, action: str, eid: str, name: str, kind: str,
            guid: str = "", changes: dict = None, run_id: str = ""):
        ...

    def checkpoint(self, phase: str, run_id: str = ""):
        ...

    def log_diff(self, diff: dict, run_id: str = ""):
        ...

    def close(self):
        ...
```

- `action`: `"created"`, `"updated"`, `"deleted"`, `"renamed"`, `"synced"`
- `changes`: optional dict of field_name -> (old_value, new_value) for updates/renames
- `checkpoint`: logs a phase boundary marker (for hang diagnostics)
- `log_diff`: accepts structured diff dict and logs everything in one batch (used by sync scripts)
- `close`: finalizes the entry, prepends to file, trims if over limit

### 2. Output format (Markdown, newest at top)

```markdown
## 2026-07-06 16:30:42 — Sales (generate), run sp-eacrm-20260706-163042

### Phase: Element creation complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| CreateRFQ | Create RFQ | Activity | {guid} |

### Updated
| eid | Name | Type | Changes |
|-----|------|------|---------|
| AcceptOffer | Accept Offer | Activity | Notes updated, ParentID changed |

### Deleted
| eid | Name | Type |
|-----|------|------|
| OldElement | Old Element | DataObject |

### Connectors
| Action | Type | Source | Target | Condition |
|--------|------|--------|--------|-----------|
| created | SequenceFlow | CreateRFQ | RegisterRFQ | |
| deleted | MessageFlow | Vendor_SendQuote | ReceiveQuote | |
```

### 3. Generator changes (MD → EA)

Replace existing `print("  Created: ...")` / `print("  Updated: ...")` / `print("  Deleted: ...")` with `clog.log()` calls at each action site.

**Call sites per generator:**

| Generator | Call sites | Notes |
|-----------|-----------|-------|
| `generate_archimate.py` | 4 (element create/update, relation create/update) | Currently has per-element prints with timestamps |
| `generate_uml_datamodel.py` | 5 (entity create/update, attr add/delete, connector create/delete) | Currently has indented per-entity prints |
| `generate_requirements_from_md.py` | 4 (req create/update, connector create/delete, realisation create/delete) | Most thorough current reporting |
| `bpmn_engine.py` `generate()` | 3 (element create/update, connector create per type) | Currently only prints aggregate counts — needs per-element logging added |

### 4. Sync changes (EA → MD)

Before/after MD diff to determine what changed:

1. **Parse old MD** on disk → dict of `{eid: {name, type, stereo, guid, lane, ...}}` + connector list
2. **Generate new content in memory** (string buffer, not written to disk yet)
3. **Parse the buffer** → same dict structure
4. **compute_diff(old_data, new_data)**:
   - eids in new but not old = `created`
   - eids in old but not new = `deleted`
   - eids in both with different field values = `updated`
   - GUID matches but eid changed = `renamed`
   - Connectors compared by (type, source, target) tuples
5. **clog.log_diff(diff)** → write everything in one batch
6. **Write new MD to disk**

No LLM needed — existing MD parsers (`_parse_md_flat`, `_parse_md_hierarchical`) are reused for the diff side.

**Affected sync scripts:**
- `sync_datamodel_from_ea.py`
- `sync_requirements_from_ea.py`
- `bpmn_engine.py` `sync_to_md()` (used by all 3 BPMN sync wrappers)

### 5. Size cap and prepend mechanics

```python
def _finalize_entry(filepath: str, entry: str, max_bytes: int):
    old = read_file(filepath) if exists(filepath) else ""
    combined = entry + old  # prepend
    while len(combined.encode("utf-8")) > max_bytes:
        combined = _trim_last_section(combined)
    write_atomically(filepath, combined)
```

`_trim_last_section()` finds the last `## `-delimited block and removes it. `write_atomically()` writes to a `.tmp` sibling then renames, so a crash during write doesn't corrupt the changelog.

## File layout

Per-generator changelog files in `experiments/modelgen/`:

```
experiments/modelgen/
  archimate_changelog.md
  uml_datamodel_changelog.md
  requirements_changelog.md
  sales_changelog.md
  newsletter_changelog.md
  customeraccount_changelog.md
```

## Non-goals

- **ArchiMate/UML Data Model engine unification** — tracked in issue [#6](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/6), not part of this issue
- **CI regression check** — also tracked in issue #6

## Implementation order

1. Write `changelog.py` with `ChangeLog` class, prepend logic, size cap, atomic write
2. Wire into `bpmn_engine.py` `generate()` and `sync_to_md()` (covers 3 generators + 3 syncs at once)
3. Wire into `generate_archimate.py`
4. Wire into `generate_uml_datamodel.py` and `sync_datamodel_from_ea.py`
5. Wire into `generate_requirements_from_md.py` and `sync_requirements_from_ea.py`
6. Add `checkpoint()` calls to all scripts for hang diagnostics
