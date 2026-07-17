# Design: Promote mature model tooling out of `experiments/`

**Date:** 2026-07-17
**Closes:** issue #25
**Status:** implemented

## Context

`experiments/modelgen/` had grown from a POC into the primary way the EA
model is edited, tested, and CI-validated. Around 50 files lived there,
mixing four distinct roles:

1. **Library modules** — `ea_session.py`, `bpmn_engine.py`,
   `wireframe_engine.py`, `changelog.py`, `diagram_utils.py`,
   `ameff_reader.py`, `cleanup.py`, `dedup_archimate_connectors.py`,
   plus their configs.
2. **Documented workflow entrypoints** — `generate_*_from_md.py` (7),
   `sync_*_from_ea.py` (5), `seed_requirements_properties.py`.
   Referenced from AGENTS.md, README.md, and every `ea-*` skill.
3. **Tests** — `conftest.py`, `test_*.py` (6).
4. **Per-domain state / scratch** — `<domain>_changelog.md` (7),
   `<domain>_guid_map.json` (7), `run_log.txt`, `run_err.txt`.

The `experiments/` label had stopped fitting: this code is gated by
`ea-code-validator` (EA001–003), is round-trip authoritative for the
model, and is invoked from CI. Calling it "experimental" understated
how load-bearing it had become.

`experiments/pdm/` (issue #16) was in the same situation on a shorter
timeline: mature enough that the DDL round-trip works, but still
labelled experimental.

## Decision

Promote both to first-class top-level folders:

- `experiments/modelgen/` → `modelgen/`
- `experiments/pdm/` → `pdm/`

`experiments/` retains only true POCs (`imap/`, `parsing/`).

## Alternatives considered

- **`tools/modelgen/`** — sibling-to-`scripts/` grouping. Rejected;
  extra nesting without payoff. `modelgen/` at the root is how
  AGENTS.md already refers to the scripts colloquially.
- **Split in place (`experiments/modelgen/{lib,wip}/`)** — smaller
  blast radius, but leaves the misleading `experiments/` label on
  mature code and doesn't answer issue #25 (the ask was about
  *location signalling maturity*, not internal layering).

## Consequences

- All Python imports inside `modelgen/` are bare sibling imports
  (`from ea_session import ...`); no import path changes needed.
- `.opencode/skills/ea-code-validator/engine.py` scope constant
  simplified from `MODELGEN_DIR_PART = ("experiments", "modelgen")`
  to `MODELGEN_DIR_NAME = "modelgen"`.
- 34+ doc/skill files updated to reference the new paths. Historical
  `docs/superpowers/plans|specs/` and `.superpowers/sdd/` task briefs
  were left as point-in-time records.
- `modelgen/run_log.txt` and `modelgen/run_err.txt` added to
  `.gitignore` (previously tracked accidentally).

## Incidental fix (out of scope but caught during verification)

`modelgen/cleanup.py` had module-level destructive COM code with no
`if __name__ == "__main__":` guard. An import-smoke-test during
verification triggered a full delete of 74 ArchiMate elements from the
live `.qea`. Recovery via `generate_archimate.py` succeeded but
regenerated element layout is default. `cleanup.py` now wraps its
body in `main()` behind a `__main__` guard so `import cleanup` is
safe.
