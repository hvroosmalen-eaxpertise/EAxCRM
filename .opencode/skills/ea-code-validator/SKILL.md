---
name: ea-code-validator
description: >
  Enforce project-specific rules on EA-touching Python code.  Invoke before
  committing any change under modelgen/ or any .py that imports
  ea_session/bpmn_engine or references EAinterop.  Runs a set of registered
  rules and prints flake8-style findings; exits non-zero on any violation.
---

# EA Code Validator

Enforces project rules that keep EA-related Python code correct.
See `docs/superpowers/specs/2026-07-16-skill-code-validator-design.md`
for the full design and `docs/superpowers/plans/2026-07-16-skill-code-validator-plan.md`
for the implementation plan.

## When to invoke

- Before committing any file under `modelgen/`.
- Before committing any `.py` that imports `ea_session` or `bpmn_engine`,
  or references `EAinterop`.
- Before merging a PR that touches those files.

The pre-commit hook installed by `scripts/install-hooks.ps1` /
`scripts/install-hooks.sh` runs `--changed` automatically at commit time,
so manual invocation is only needed when the hook is not installed or when
inspecting the whole tree.

## Usage

```
python .opencode/skills/ea-code-validator/cli.py            # whole repo
python .opencode/skills/ea-code-validator/cli.py path/...   # specific files/dirs
python .opencode/skills/ea-code-validator/cli.py --changed  # git-staged files only
python .opencode/skills/ea-code-validator/cli.py --only EA001,EA002
python .opencode/skills/ea-code-validator/cli.py --list     # list registered rules
```

Exit codes: **0** clean, **1** any finding, **2** internal error.
Output: `path:line: EA00X message` (flake8-style).

## Rules

Each rule lives in `rules/<id>_<slug>.py` and registers itself on import.
Adding a rule:

1. Create the rule module (see existing rules for the shape).
2. Add `from . import <module>` to `rules/__init__.py`.
3. Add positive/negative fixtures under `tests/fixtures/<id>_positive/`
   and `tests/fixtures/<id>_negative/`.
4. Extend `tests/test_rules.py` if the rule needs bespoke assertions.

The `--list` flag prints every registered rule with its one-line
description.

## Scope

Only files identified as *EA-touching* are scanned:

- anything under `modelgen/`, or
- any `.py` whose text contains `ea_session`, `bpmn_engine`, `EAinterop`,
  or `win32com` together with `EA.App` / `EA.Repository`.

Plain Django / newsletter / contacts code is skipped even if passed on
the command line.
