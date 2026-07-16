# Skill Code Validator — Implementation Plan

- **Spec:** [2026-07-16-skill-code-validator-design.md](../specs/2026-07-16-skill-code-validator-design.md)
- **Issue:** [#18](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/18)
- **Date:** 2026-07-16

## Guiding approach

Bottom-up, test-first. Each step lands as its own commit, so review can
happen at any checkpoint. No step introduces a new runtime dependency;
`pytest` is the only new dev dependency (add to `requirements.txt` under a
dev section if one exists, else document as `pip install pytest`).

The engine ships first with no rules, then rules land one at a time.
Every rule step is: fixtures → test → implementation → green.

## Step 1 — Skeleton and empty engine

Files:

```
.opencode/skills/ea-code-validator/
├── SKILL.md
├── cli.py
├── engine.py
├── rules/__init__.py
└── tests/test_engine.py
```

- `engine.py` defines `Finding`, `FileRule`, `RepoRule`, `register(rule)`,
  and `run(paths) -> list[Finding]`. `run` handles: path resolution,
  scope discovery (§4 of the spec), AST parsing (once per file, cached
  per run), dispatching, and per-rule crash isolation.
- `cli.py` parses `<paths...>`, `--only`, `--list`, `--changed`, calls
  `engine.run(...)`, prints findings flake8-style, exits 0/1/2.
- `SKILL.md` names the trigger conditions (before committing files under
  `experiments/modelgen/` or any `.py` that imports `ea_session`/
  `bpmn_engine`), gives the one-line invocation, and lists the flags.
- `rules/__init__.py` is empty at this step — no rules yet.
- `tests/test_engine.py` covers: scope discovery includes/excludes
  correctly (a fixture under `experiments/modelgen/`, a fixture that
  imports `ea_session`, a Django-shaped fixture that must be excluded);
  `--list` prints registered rules (empty list at this step is fine);
  rule-crash isolation using an in-test throwaway rule.

**Checkpoint:** `python .opencode/skills/ea-code-validator/cli.py --list`
prints nothing and exits 0. `pytest .opencode/skills/ea-code-validator/tests`
passes.

## Step 2 — EA001 (no direct EA-repo queries)

Files:

- `rules/ea001_no_direct_ea_query.py`
- `rules/__init__.py` imports it
- `tests/fixtures/ea001_positive/{sqlite3_connect_qea,pyodbc_raw_sql,sqlalchemy_engine}.py`
- `tests/fixtures/ea001_negative/{uses_sqlquery_com,django_orm}.py`
- Test cases in `test_rules.py` (created here, extended by later steps).

Order:

1. Write the fixtures (each is a minimal, self-contained snippet).
2. Write the tests that walk `ea001_positive/` and assert EA001 fires on
   the expected line, and walk `ea001_negative/` and assert it does not.
3. Implement the rule until the tests pass.

**Checkpoint:** running the CLI against `experiments/modelgen/` produces
either zero EA001 findings or a real list of violations we'll want to
address separately (per the memory note that
`bpmn_engine.sync_to_md` and `sync_datamodel_from_ea.py` used raw SQLite —
those were addressed in commits d14867f and 96e943e, so v1 should ideally
be green on current HEAD; if not, that is a bug in EA001).

## Step 3 — EA002 (generate needs sync)

Files:

- `rules/ea002_generate_needs_sync.py`
- `rules/__init__.py` imports it
- `tests/fixtures/ea002_positive/generate_orphan_from_md.py`
- `tests/fixtures/ea002_negative/{generate_paired_from_md,sync_paired_from_ea}.py`

Order: fixtures → test → implementation.

Rule mechanics: for each directory in the file set that contains at least
one `generate_*.py`, build the pairing keys (stem after `generate_` up to
the first suffix like `_from_md`/`_from_ea`) and require a matching
`sync_<key>_*.py` in the same directory. Emit findings on line 1 of the
orphan `generate_*.py`.

**Checkpoint:** CLI is green on `experiments/modelgen/` (every generate
already has a sync sibling — verified in the current tree).

## Step 4 — EA003 (heuristic no writes to existing-diagram geometry)

Files:

- `rules/ea003_no_existing_diagram_writes.py`
- `rules/__init__.py` imports it
- `tests/fixtures/ea003_positive/writes_existing_geometry.py`
- `tests/fixtures/ea003_negative/writes_just_created_geometry.py`

Order: fixtures → test → implementation.

The heuristic (per spec §3): flag geometry writes on DiagramObject-shaped
names unless a `.AddNew(...)` / `.CreateDiagramObject(...)` producing
that name appears within the last 20 lines of the same function or
`if`-block.

This is the rule most likely to need iteration. If it fires on
legitimate first-time-creation code that already exists in the repo,
either the code should be tightened (moving the creating call closer to
the geometry write) or the heuristic should be adjusted — decision goes
to the user at the checkpoint, not resolved by adding a waiver.

**Checkpoint:** CLI on the whole repo. Any EA003 findings are triaged
with the user before proceeding.

## Step 5 — Pre-commit hook installer

Files:

- `scripts/install-hooks.ps1`
- `scripts/install-hooks.sh`
- One paragraph appended to `README.md` pointing at the installer.

Each installer writes `.git/hooks/pre-commit` (executable, POSIX line
endings on the `.sh` side) containing:

```sh
#!/usr/bin/env sh
python .opencode/skills/ea-code-validator/cli.py --changed
```

The Windows variant does the same via PowerShell's file writing (Git for
Windows runs the hook through its bundled sh). Installer is idempotent
— if the hook exists and is ours (marker line in a comment), overwrite;
if it exists and isn't ours, refuse and print the intended contents.

**Checkpoint:** run the installer, stage a file that would fire a rule,
try `git commit`, confirm the commit is blocked.

## Step 6 — CI job

- If a GitHub Actions workflow file already exists, add a job.
- If not, add `.github/workflows/validate.yml` with a single job:
  checkout, set up Python, `pip install pytest`, run
  `python .opencode/skills/ea-code-validator/cli.py` and
  `pytest .opencode/skills/ea-code-validator/tests`.

**Checkpoint:** open a small no-op PR and confirm CI runs and passes.

## Step 7 — Close issue #18

- Add a short comment to [#18](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/18)
  linking the spec, the plan, and the commits that landed each step.
- Close the issue.

## Verification, not just tests

At the end of Step 4, exercise the validator on the real
`experiments/modelgen/` directory (not fixtures) and eyeball the output.
Static tests confirm the rules fire on the fixtures; real-repo runs
confirm the scope filter, the exit code, and the message wording read
sensibly.

## Rollback

Every step is a single commit. To back out any step, `git revert` its
commit. No migrations, no external side effects until Step 5 (which only
writes a file under `.git/hooks/` on machines where the installer is
run).
