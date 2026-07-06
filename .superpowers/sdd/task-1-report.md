# Task 1 Report: Create changelog.py + tests

**Status:** DONE

## Commits Made

| SHA | Message |
|-----|---------|
| `0741cd9` | `feat: add changelog.py -- structured audit logging utility` |

## Files Created

- `experiments/modelgen/changelog.py` — `ChangeLog` class + `compute_md_diff()` module-level function
- `experiments/modelgen/test_changelog.py` — 17 pytest tests

## Test Results

```
python -m pytest experiments/modelgen/test_changelog.py -v
```

**Result:** 17 passed in 1.05s

| Test | Status |
|------|--------|
| `test_compute_md_diff_created_deleted` | PASS |
| `test_compute_md_diff_updated` | PASS |
| `test_compute_md_diff_empty_old` | PASS |
| `test_compute_md_diff_empty_new` | PASS |
| `test_compute_md_diff_no_changes` | PASS |
| `test_log_creates_file` | PASS |
| `test_prepend_newest_first` | PASS |
| `test_log_updated_with_changes` | PASS |
| `test_log_deleted` | PASS |
| `test_size_cap_trims_oldest` | PASS |
| `test_checkpoint` | PASS |
| `test_log_diff_created_deleted` | PASS |
| `test_empty_buffer_no_file` | PASS |
| `test_log_deleted_no_guid` | PASS |
| `test_multiple_same_run_id` | PASS |
| `test_unicode_changes_display` | PASS |
| `test_multiple_connectors_logged` | PASS |

## Concerns

1. **Element regex over-matches:** The `compute_md_diff` function's `extract_elements()` regex matches ANY `##`/`###`/`####` header containing an em-dash, including `### SequenceFlow—sf1` under a `## Relationships` section. This means connector section headers are treated as elements in the diff. This is by design (the brief specifies the exact regex), but consumers should be aware that the diff may show "created" or "deleted" entries for connector headers, not just pure BPMN elements like Activities/Gateways/Events. This is accurate behavior for the current pattern but may confuse if someone expects only "Elements" section content.

2. **No description field in the interface:** The format example shows `## 2026-07-06 16:30:42 — Sales (generate), run sp-eacrm-...` but the `ChangeLog` constructor only accepts `(filepath, max_bytes)`. The description "Sales (generate)" is currently hardcoded as "Audit". Consumers will likely need a `description` parameter — this should be added when integrating into generators/syncs.

3. **Connector source/target semantics in log_diff:** When `log_diff` processes the `"connectors"` list, it passes `(type, source, target)` as the `(eid, name, kind)` tuple to `log()`. This is semantically overloaded but renders correctly in the Connectors table. Test coverage validates the rendering is correct.
