# Skill Code Validator — Design

- **Issue:** [#18](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/18)
- **Date:** 2026-07-16
- **Status:** Approved (pending user sign-off on this document)

## Purpose

A validator that enforces project-specific rules on EA-touching Python code.
The rule set will grow; the initial catalog encodes three rules that have
been violated repeatedly:

1. **EA001** — no direct queries against the EA repository; all access
   must go through the `EAinterop.dll` / COM interface.
2. **EA002** — every generate script must be accompanied by a sync script.
3. **EA003** — scripts must not modify existing diagrams; only first-time
   diagram creation may write geometry.

## Locked decisions

| Decision | Choice |
| --- | --- |
| Location | New skill `.opencode/skills/ea-code-validator/` (sibling to the EA-domain creator skills). |
| Invocation | Shared rule engine driven by both the skill (on-demand) and a repo pre-commit / CI hook. |
| Scan scope | EA-touching Python only — files under `experiments/modelgen/` plus any `.py` importing `ea_session`/`bpmn_engine` or referencing `EAinterop`. |
| Rule authoring | Python check plugins; no YAML DSL. |
| Output | flake8-style `path:line: EA00X message`; exit 1 on any finding. |
| Waivers | None — rules are absolute. |
| First-cut catalog | EA001, EA002, EA003 (EA003 as a static heuristic). |

## 1. Layout & architecture

```
.opencode/skills/ea-code-validator/
├── SKILL.md               # human/agent-facing: what it enforces, how to run
├── cli.py                 # `python .opencode/skills/ea-code-validator/cli.py [paths...]`
├── engine.py              # discovery, dispatch, output formatting
├── rules/
│   ├── __init__.py        # imports each rule so registration is automatic
│   ├── ea001_no_direct_ea_query.py
│   ├── ea002_generate_needs_sync.py
│   └── ea003_no_existing_diagram_writes.py
└── tests/
    ├── fixtures/          # small sample files that should or shouldn't fire each rule
    └── test_rules.py
```

- Engine walks the target paths, filters to EA-touching Python (§4), and
  dispatches each file to every registered rule. Repo-level rules (like
  EA002) are invoked once with the whole file set.
- Output is flake8-shaped: `path:line: EA00X message`. Any finding → exit 1.
- No config file, no severities, no waivers.
- Rule registration is by import — each rule module calls
  `engine.register(Rule(...))` at import time; `rules/__init__.py` imports
  them all. Adding a new rule = drop a file in `rules/` and add one import
  line.

## 2. Rule authoring contract

Two rule shapes, both plain Python:

```python
# engine.py exposes:

@dataclass(frozen=True)
class Finding:
    path: pathlib.Path
    line: int          # 1-indexed; 0 for repo-level findings
    rule_id: str       # e.g. "EA001"
    message: str

class FileRule(Protocol):
    id: str
    description: str   # one line, shown in `--list`
    def check(self, path: pathlib.Path, source: str, tree: ast.AST) -> Iterable[Finding]: ...

class RepoRule(Protocol):
    id: str
    description: str
    def check(self, files: list[pathlib.Path]) -> Iterable[Finding]: ...
```

Registration by import side-effect:

```python
# rules/ea001_no_direct_ea_query.py
from ..engine import register, Finding

class Rule:
    id = "EA001"
    description = "No direct queries against the EA repository; use EAinterop/COM."
    def check(self, path, source, tree):
        ...
        yield Finding(path, node.lineno, self.id,
                      "sqlite3.connect on a .qea path — use ea_session.ea_repository() instead")

register(Rule())
```

Notes:

- Engine parses each file's AST once and passes it to every `FileRule` —
  rules do not re-parse.
- A rule may use regex over `source`, walk `tree`, or both. No DSL, no
  framework.
- `id` doubles as the CLI selector (`--only EA001`) and the token that
  appears in output. Duplicate IDs are a registration-time error.

## 3. The three concrete rules

### EA001 — no direct queries against the EA repository (`FileRule`)

Fires on any of:

- `import sqlite3` in an EA-touching file, or a call to `sqlite3.connect(...)`.
- Any call whose argument is a `.qea` path literal, or a variable named
  `qea_path`/`repo_path`/similar, passed to a DB driver (`sqlite3`,
  `pyodbc`, `sqlalchemy.create_engine`).
- Raw SQL strings (`re.search(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\b", ...)`)
  **unless** they appear as the argument to a call whose function ends in
  `.SQLQuery` (EA's own read-only COM method — explicitly allowed).

Message: `EA001 direct EA-repo query; use ea_session.ea_repository() + COM (Repository.SQLQuery for reads)`.

### EA002 — generate script must have a sync counterpart (`RepoRule`)

For every file matching `experiments/modelgen/generate_<name>_*.py` (or
`generate_<name>.py`), require at least one file matching
`experiments/modelgen/sync_<name>_*.py` in the same directory. The pairing
key is the stem after `generate_` up to the first suffix like
`_from_md`/`_from_ea`. Pairing is done within each directory that
contains a `generate_*.py` file, so fixtures under
`tests/fixtures/ea002_*/` are validated against their own directory
rather than against `experiments/modelgen/`.

Message on the *generate* file, line 1:
`EA002 no companion sync_<name>_from_ea.py found in experiments/modelgen/`.

Reverse direction (orphan `sync_*.py` with no `generate_*.py`) is **not**
flagged — sync scripts sometimes exist for read-only extraction.

### EA003 — no writes to existing-diagram geometry (`FileRule`, heuristic)

Walks the AST; flags:

- Any `Attribute` assignment to `.left`/`.top`/`.right`/`.bottom` on a
  target whose name matches `*diagram_object*` / `*dobj*` / `*do*`
  (case-insensitive), **and**
- Any `Call` to `.Update()` on such a target when a geometry assignment
  appears above it in the same function, **unless**
- The enclosing function or `if`-block contains a call to `.AddNew(...)`
  or `.CreateDiagramObject(...)` producing that same target within the
  last 20 lines — the "just-created" escape hatch.

Because the check is heuristic, the message is worded so a reader can tell
it's a *possible* violation:
`EA003 possible write to existing diagram geometry; only just-created DiagramObjects may be positioned`.

False-positive posture: with no waivers, legitimate first-time-creation
code that happens to fire EA003 should be restructured so the creating
call sits visibly close to the geometry write. That constraint is itself
desirable (project rule: never reflow an existing EA diagram).

## 4. Scope discovery

Two passes:

**Pass 1 — path filter.** Given the CLI arguments (or, with no args, the
whole repo), keep only `.py` files that are:

- under `experiments/modelgen/`, OR
- match a repo-wide substring scan for one of:
  - `from ea_session` / `import ea_session`
  - `from bpmn_engine` / `import bpmn_engine`
  - `EAinterop`
  - `win32com.client.*Dispatch*` combined with a string containing
    `EA.App` or `EA.Repository`

The substring scan runs directly on file bytes (no AST) so it is cheap and
works on files that fail to parse.

**Pass 2 — de-dup and sort.** Resolve to absolute paths, drop duplicates,
sort for deterministic output.

Rules then run:

- Each `FileRule` once per file in the resolved set.
- Each `RepoRule` once, with the full file set.

**Edge cases:**

- Files that import `ea_session` *transitively* (through an internal
  helper) are not auto-included. If they need to be governed, they should
  either move under `experiments/modelgen/` or add a direct import. Static
  reachability analysis is out of scope for v1.
- `__pycache__/`, `.venv/`, and git-ignored files are skipped by
  consulting `git ls-files` when available, falling back to a hardcoded
  ignore list otherwise.

## 5. Invocation

### Skill invocation (during a session)

`SKILL.md` describes when to reach for the validator — before committing
any change under `experiments/modelgen/` or any file that imports
`ea_session`/`bpmn_engine`. Action:

```
python .opencode/skills/ea-code-validator/cli.py
```

With no args it validates the whole repo. Flags:

| Flag | Effect |
| --- | --- |
| `<paths...>` | Validate only the given files/dirs. |
| `--only EA001[,EA002]` | Run a subset of rules. |
| `--list` | Print each registered rule's `id` and `description`, then exit 0. |
| `--changed` | Validate only files reported by `git diff --name-only --cached HEAD` (used by the pre-commit hook). |

Exit codes:

- **0** clean.
- **1** any finding.
- **2** internal error (rule crash, unparseable file that a rule needed
  to parse). Rule crashes are caught per-rule so one broken rule cannot
  mask findings from the others.

### Pre-commit hook

A repo-local hook — no external `pre-commit` framework dependency.

```
.git/hooks/pre-commit           # generated by an install script
```

Contents: `python .opencode/skills/ea-code-validator/cli.py --changed`.

A one-line install script (`scripts/install-hooks.ps1` + `scripts/install-hooks.sh`)
drops it in. `README.md` gets one paragraph pointing at the install script.

### CI

A single job in whatever CI config exists (or a new tiny GitHub Actions
workflow if none) runs `python .opencode/skills/ea-code-validator/cli.py`
on push and on PR. Fails the job on exit 1.

## 6. Testing

**Fixture-driven, no EA required.** All tests run against small Python
source fixtures under `.opencode/skills/ea-code-validator/tests/fixtures/`.
No `.qea`, no COM, no EA process.

```
tests/
├── fixtures/
│   ├── ea001_positive/                # must fire EA001
│   │   ├── sqlite3_connect_qea.py
│   │   ├── pyodbc_raw_sql.py
│   │   └── sqlalchemy_engine.py
│   ├── ea001_negative/                # must NOT fire EA001
│   │   ├── uses_sqlquery_com.py       # Repository.SQLQuery(...)
│   │   └── django_orm.py              # not EA-touching → not scanned
│   ├── ea002_positive/
│   │   └── generate_orphan_from_md.py # no sync sibling in this dir
│   ├── ea002_negative/
│   │   ├── generate_paired_from_md.py
│   │   └── sync_paired_from_ea.py
│   ├── ea003_positive/
│   │   └── writes_existing_geometry.py
│   └── ea003_negative/
│       └── writes_just_created_geometry.py
└── test_rules.py
```

`test_rules.py` walks each `*_positive/` directory and asserts the
corresponding rule fires with the expected `rule_id` on the expected line;
walks each `*_negative/` and asserts no findings from that rule.
Cross-rule interference is caught by a table-driven "run everything,
expect nothing" pass over `*_negative/` collectively.

Additional tests:

- Scope discovery (§4) correctly includes `experiments/modelgen/*.py` and
  files with the tracked imports, and excludes plain Django files.
- `--list` prints every registered rule (guards against forgetting to
  import a new rule in `rules/__init__.py`).
- A rule crash yields exit code 2 and does not suppress other rules'
  findings.

Runner: plain `pytest`. No new dependencies.

## Out of scope for v1

- Severity levels (`error`/`warning`/`info`) and configurable gating.
- Waiver / suppression mechanism (inline or central).
- Rules governing non-EA code (Django, newsletter, contacts).
- IDE integration (LSP, editor plugin).
- Auto-fix.
- Static reachability analysis for transitive `ea_session` imports.
- Rich JSON/SARIF output.

These are deferred until a concrete need appears.
