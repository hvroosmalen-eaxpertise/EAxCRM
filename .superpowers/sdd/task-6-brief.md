# Task 6: Update AGENTS.md with Changelog section

**Goal:** Add a `## Changelog / Audit Logging` section to AGENTS.md documenting the new structured logging system.

## Context

Tasks 1-5 created `changelog.py` and wired it into all 9 generator/sync scripts. AGENTS.md must document this new system for future development sessions.

## Location

Insert before the `## Next Steps` section (currently line 495 in AGENTS.md).

## Content to Add

Write a section titled `## Changelog / Audit Logging` with:

### What it is
- A structured Markdown changelog system for tracking EA model changes
- Each generator/sync script logs creates, updates, and deletes per-element
- Sync scripts use `compute_md_diff()` for full MD diff on the regenerated file

### Files Involved
- `experiments/modelgen/changelog.py` — the `ChangeLog` class + `compute_md_diff()` function
- Per-script changelog files (auto-generated, git-tracked):

| Script | Changelog File |
|--------|---------------|
| BPMN engine (all 3 processes) | `sales_changelog.md`, `newsletter_changelog.md`, `customeraccount_changelog.md` |
| `generate_archimate.py` | `archimate_changelog.md` |
| `generate_uml_datamodel.py` / `sync_datamodel_from_ea.py` | `uml_datamodel_changelog.md` |
| `generate_requirements_from_md.py` / `sync_requirements_from_ea.py` / `seed_requirements_properties.py` | `requirements_changelog.md` |

### Integration Point
- `ChangeLog` is designed as a pure Python stdlib dependency (no pip installs)
- Generators log per-element: `clog.log(action, id, label, type, guid, changes=dict)`
- Sync scripts read old MD → build new MD → diff → `clog.log_diff(diff)`
- All `clog.close()` calls wrapped in `try/finally`
- Logged to `experiments/modelgen/*_changelog.md`

### Best Practices
- Generator scripts already capture `old_notes` before overwriting (e.g., ArchiMate generator, seed_requirements_properties)
- Element GUID is always captured from existing COM API return values — no extra API calls
- Checkpoints organize the log into phases (e.g., "Parsed MD", "Diagram complete", "Sync from EA")

### When to Wire New Scripts
- New generator: import `ChangeLog`, open with `checkpoint("Parsed MD")`, log create/update per element/relation, close with `checkpoint("Diagram complete")` in `try/finally`
- New sync script: import `ChangeLog, compute_md_diff`, read old file, build new content, compute diff, `checkpoint("Sync from EA")`, `log_diff(diff)`, close in `try/finally`, then write

## Steps

1. Read `AGENTS.md` to confirm insertion point
2. Edit `AGENTS.md` to add the new section before `## Next Steps`
3. Commit: `git add AGENTS.md && git commit -m "docs: add changelog / audit logging section to AGENTS.md"`
4. Write report to `\\HAN-ELITEBOOK\Users\hanva\source\repos\EAxCRM\.superpowers\sdd\task-6-report.md`

Return: status, commit hash, any concerns.
