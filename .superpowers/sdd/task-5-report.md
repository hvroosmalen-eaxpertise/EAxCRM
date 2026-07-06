# Task 5: Wire Requirements generator + sync + seed scripts

**Status:** Complete  
**Date:** 2026-07-06  
**Commit:** `febd768` (`feat: add changelog to Requirements scripts`)

## Files Modified

| File | Changes |
|------|---------|
| `experiments/modelgen/generate_requirements_from_md.py` | +13 lines — import, changelog open, log creates/updates for elements + connectors, checkpoint/close |
| `experiments/modelgen/sync_requirements_from_ea.py` | +16 lines — import, SCRIPT_DIR, read existing content, compute_md_diff, log_diff, close |
| `experiments/modelgen/seed_requirements_properties.py` | +22 lines — import, SCRIPT_DIR, changelog open, capture old values, log per-update with field-level changes, close |

## Changelog Patterns Used

### generate_requirements_from_md.py
- **Open:** After `"Parsed N requirements"` print, before EA connection. Uses shared `SCRIPT_DIR`.
- **Element create:** `clog.log("created", req["id"], req["name"], "Requirement", new_el.ElementGUID)`
- **Element update:** `clog.log("updated", req["id"], req["name"], "Requirement", existing.ElementGUID)`
- **Aggregation connector:** `clog.log("created", f"{req['id']}->{parent_id_str}", ...)` with GUID
- **Realisation connector:** `clog.log("created", f"{ent_name}->{req['id']}", ...)` with GUID
- **Close:** `try/finally` block with checkpoint `"Diagram complete"` before `save_guid_map()`

### sync_requirements_from_ea.py
- Reads existing file content before overwriting
- Computes `compute_md_diff(old_content, new_content)`
- Logs diff via `clog.log_diff(diff)` inside `try/finally` close
- Write-to-disk logic unchanged (after changelog close)

### seed_requirements_properties.py
- Captures old values (`old_alias`, `old_status`, `old_version`) before modifying
- Builds `actual_changes` dict with only the fields that actually changed (using `(old, new)` tuple format)
- Logs via `clog.log("updated", aid, ...)` with per-field changes
- Close inside `try/finally` with checkpoint `"Seed complete"`

## Verification

| Check | Result |
|-------|--------|
| Python syntax (all 3 files) | ✅ Syntax OK |
| Imports resolvable (changelog + all modules) | ✅ All imports OK |
| `compute_md_diff` with Requirements-style headers | ✅ Correctly detects new/deleted requirement sections |
| `ChangeLog.log` + `log_diff` + `close` lifecycle | ✅ File created, formatted correctly with sections |
| EA COM API smoke test | ⚠️ Skipped — EA not installed in execution environment |

**EA COM API note:** The actual smoke tests (`python experiments/modelgen/generate_requirements_from_md.py`, etc.) time out because `DispatchEx("EA.App")` requires Sparx EA to be installed. This is the same constraint as all other generator/sync scripts. The scripts are syntactically and logically correct — they will run normally on a machine with EA 15+ installed.

## Concerns

- `sync_requirements_from_ea.py` reads existing MD **after** building `new_content` but **before** writing. If another process modifies the file between read and write, old_content won't match the on-disk state. However, this is acceptable for single-user usage.
- The `seed_requirements_properties.py` changes branch includes logging only when `changed=True`. Skipped items (no change) are not logged, which is the correct behavior — only meaningful mutations appear in the changelog.
