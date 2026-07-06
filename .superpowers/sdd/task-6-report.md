# Task 6 Report: Update AGENTS.md with Changelog section

**Status:** ✅ Complete

## Summary
Added a `## Changelog / Audit Logging` section to `AGENTS.md`, inserted before the existing `## Next Steps` section (which shifted from line 495 to line 529).

## Content Added
The new section documents:
- **What it is** — structured Markdown changelog for EA model change tracking
- **Files Involved** — `changelog.py` and the 4 per-script changelog files
- **Integration Point** — `ChangeLog` class API and `compute_md_diff()` usage
- **Best Practices** — old_notes capture, GUID capture, checkpoint organization
- **When to Wire New Scripts** — patterns for both generator and sync scripts

## Verification
- Section inserted cleanly at the correct location (before `## Next Steps`)
- Total file size: 535 lines (was 501; +34 lines added)
- No existing content was modified or removed

## Commit
```
9707bb1 docs: add changelog / audit logging section to AGENTS.md
 1 file changed, 34 insertions(+)
```

## Concerns
- None. The content matches the brief exactly and integrates cleanly with the existing document structure.
