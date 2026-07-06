# Task 2 Report: Wire BPMN engine — bpmn_config.py + bpmn_engine.py

**Status**: ✅ Complete

**Date**: 2026-07-06  
**Assignee**: AI agent

---

## Summary

Added structured audit-logging (changelog) to the shared BPMN engine, covering all three process generators (Sales, Newsletter, Customer Account). The `ChangeLog` class and `compute_md_diff()` from `changelog.py` (created in Task 1) are now wired into both `generate()` (MD → EA) and `sync_to_md()` (EA → MD) via config-driven `changelog_file` paths.

## Changes

### bpmn_config.py
| Change | Detail |
|--------|--------|
| Added `import os` | Module-level import |
| Added `SCRIPT_DIR` | `os.path.dirname(os.path.abspath(__file__))` for resolved paths |
| Added `changelog_file: str = ""` field | New field on `ProcessConfig` dataclass |
| Set CUSTOMER_ACCOUNT path | `os.path.join(SCRIPT_DIR, "customeraccount_changelog.md")` |
| Set SALES path | `os.path.join(SCRIPT_DIR, "sales_changelog.md")` |
| Set NEWSLETTER path | `os.path.join(SCRIPT_DIR, "newsletter_changelog.md")` |

### bpmn_engine.py

**Import**: `from changelog import ChangeLog` at module level.

**`generate()` — 5 hooks**:
1. After `parse_md()`: `clog = ChangeLog(...)` + checkpoint "Parsed MD"
2. Inside `create_element()` after existing update: logs "updated" with optional changes dict (currently Name field)
3. Inside `create_element()` after new element creation: logs "created"
4. After connector creation loop: logs each connector as "created" with source/target/condition
5. Before `print("Done.")`: checkpoint "Diagram complete" + `clog.close()`

**`sync_to_md()` — 1 hook**:
- Before final file write: reads existing MD, calls `compute_md_diff()`, passes diff through `clog.log_diff()`, writes changelog via `clog.close()`

## Files Modified
- `experiments/modelgen/bpmn_config.py` — +7 lines
- `experiments/modelgen/bpmn_engine.py` — +55 lines, -2 lines (net +53)

## Commit

```
93e9638 feat: wire changelog logging into BPMN engine
 2 files changed, 55 insertions(+), 2 deletions(-)
```

## Generated Artifact
- `experiments/modelgen/sales_changelog.md` — 11,157 bytes, contains structured audit:
  - 2 checkpoints (Parsed MD, Diagram complete)
  - 64 connector-created entries (25 SequenceFlow, 17 MessageFlow, 11 DataInputAssociation, 11 DataOutputAssociation)
  - 50 element-updated entries (existing elements, no Name changes)

## Test Results

### Existing tests (changelog.py)
```
17 passed in 1.09s
```
All `test_changelog.py` tests pass — no regressions.

### Smoke test: generate
```
python experiments/modelgen/generate_sales_process_from_md.py
```
- Parsed 50 elements, 64 connectors
- Created 0 new, updated 50
- Repositioned 49 diagram objects
- sales_changelog.md created with full content ✓

### Smoke test: sync
```
python experiments/modelgen/sync_sales_process_from_ea.py
```
- Found 50 elements, 65 connectors
- Written 672 lines to MD
- Changelog code path reached (no error), empty diff correctly suppressed (no audit entries when nothing changed)

## Concerns

1. **No-OP on identical sync**: When `sync_to_md()` produces MD identical to the existing file, `compute_md_diff()` returns empty lists, `log_diff()` makes no entries, and `close()` exits early without writing. This is correct behavior (no sense logging "nothing changed") but could be surprising if someone expects every run to produce an entry. Verified via unit test.

2. **Changelog files not git-committed**: The `.md` changelog files live in `experiments/modelgen/` but are not included in the commit. They should likely be added to `.gitignore` or committed — needs a decision from the team.

3. **Sales MD/QEA side-effects**: The smoke test also modified `models/EAxCRM-SalesProcess.md` and `models/EAxCRM.qea` (expected — generate/sync touch these). These changes are not part of this task's commit but are staged/untracked.

## Verification Checklist
- [x] `bpmn_config.py` — `import os`, `SCRIPT_DIR`, `changelog_file` field + all 3 instances
- [x] `bpmn_engine.py` — `from changelog import ChangeLog`
- [x] `generate()` — clog init after parse_md
- [x] `generate()` — log inside create_element (existing + new)
- [x] `generate()` — log connectors after connector loop
- [x] `generate()` — checkpoint + close before "Done."
- [x] `sync_to_md()` — MD diff + log_diff before write
- [x] No new dependencies beyond Python 3.13 stdlib
- [x] No COM API calls duplicated
- [x] Changelog files in `experiments/modelgen/`
- [x] All 17 unit tests pass
- [x] Both smoke tests pass (generate + sync)
