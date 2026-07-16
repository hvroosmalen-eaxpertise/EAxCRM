"""Rule engine for the EA code validator.

Discovers EA-touching Python files, parses each once, dispatches to
registered rules, and returns findings.  See
docs/superpowers/specs/2026-07-16-skill-code-validator-design.md.
"""
from __future__ import annotations

import ast
import inspect
import pathlib
import subprocess
from dataclasses import dataclass
from typing import Iterable, Protocol, runtime_checkable

EA_IMPORT_MARKERS = (
    "from ea_session",
    "import ea_session",
    "from bpmn_engine",
    "import bpmn_engine",
    "EAinterop",
)
EA_COM_MARKERS = ("EA.App", "EA.Repository")
MODELGEN_DIR_PART = ("experiments", "modelgen")
IGNORED_DIRS = {"__pycache__", ".venv", "venv", ".git", "node_modules"}


@dataclass(frozen=True)
class Finding:
    path: pathlib.Path
    line: int
    rule_id: str
    message: str

    def format(self, root: pathlib.Path | None = None) -> str:
        p = self.path
        if root is not None:
            try:
                p = self.path.relative_to(root)
            except ValueError:
                pass
        return f"{p.as_posix()}:{self.line}: {self.rule_id} {self.message}"


@runtime_checkable
class FileRule(Protocol):
    id: str
    description: str

    def check(
        self, path: pathlib.Path, source: str, tree: ast.AST
    ) -> Iterable[Finding]: ...


@runtime_checkable
class RepoRule(Protocol):
    id: str
    description: str

    def check(self, files: list[pathlib.Path]) -> Iterable[Finding]: ...


_file_rules: list[FileRule] = []
_repo_rules: list[RepoRule] = []
_rules_loaded = False


def register(rule: FileRule | RepoRule) -> None:
    seen = {r.id for r in _file_rules} | {r.id for r in _repo_rules}
    if rule.id in seen:
        raise ValueError(f"duplicate rule id: {rule.id}")
    params = list(inspect.signature(rule.check).parameters.values())
    if len(params) == 3:
        _file_rules.append(rule)
    elif len(params) == 1:
        _repo_rules.append(rule)
    else:
        raise TypeError(
            f"{rule.id}: check() must take (path, source, tree) or (files); "
            f"got {len(params)} params"
        )


def registered_rules() -> list[FileRule | RepoRule]:
    return [*_file_rules, *_repo_rules]


def load_rules() -> None:
    """Import the rules package so rule modules run their register() calls."""
    global _rules_loaded
    if _rules_loaded:
        return
    import rules  # noqa: F401
    _rules_loaded = True


def _is_ea_touching(path: pathlib.Path, source: str) -> bool:
    parts = path.parts
    for i in range(len(parts) - 1):
        if parts[i] == MODELGEN_DIR_PART[0] and parts[i + 1] == MODELGEN_DIR_PART[1]:
            return True
    if any(marker in source for marker in EA_IMPORT_MARKERS):
        return True
    if "win32com" in source and any(marker in source for marker in EA_COM_MARKERS):
        return True
    return False


def _git_tracked(root: pathlib.Path) -> set[pathlib.Path] | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return {
        (root / p.decode("utf-8")).resolve()
        for p in out.stdout.split(b"\x00") if p
    }


def _iter_py_files(paths: Iterable[pathlib.Path]) -> Iterable[pathlib.Path]:
    for path in paths:
        path = path.resolve()
        if path.is_file():
            if path.suffix == ".py":
                yield path
            continue
        if not path.is_dir():
            continue
        for child in path.rglob("*.py"):
            if any(part in IGNORED_DIRS for part in child.parts):
                continue
            yield child.resolve()


def discover_scope(
    paths: Iterable[pathlib.Path],
    respect_gitignore: bool = True,
) -> list[pathlib.Path]:
    root = pathlib.Path.cwd().resolve()
    tracked = _git_tracked(root) if respect_gitignore else None
    seen: set[pathlib.Path] = set()
    kept: list[pathlib.Path] = []
    for f in _iter_py_files(paths):
        if tracked is not None and f not in tracked:
            continue
        if f in seen:
            continue
        try:
            source = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if not _is_ea_touching(f, source):
            continue
        seen.add(f)
        kept.append(f)
    kept.sort()
    return kept


def run(
    paths: Iterable[pathlib.Path],
    only: set[str] | None = None,
    respect_gitignore: bool = True,
) -> tuple[list[Finding], list[str]]:
    """Run all matching rules.  Returns (findings, error_messages)."""
    load_rules()

    files = discover_scope(paths, respect_gitignore=respect_gitignore)
    file_rules = [r for r in _file_rules if only is None or r.id in only]
    repo_rules = [r for r in _repo_rules if only is None or r.id in only]

    findings: list[Finding] = []
    errors: list[str] = []

    for f in files:
        try:
            source = f.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(f))
        except (OSError, SyntaxError, UnicodeDecodeError) as exc:
            errors.append(f"{f}: could not parse ({exc})")
            continue
        for rule in file_rules:
            try:
                findings.extend(rule.check(f, source, tree))
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{rule.id}: crashed on {f}: {exc!r}")

    for rule in repo_rules:
        try:
            findings.extend(rule.check(files))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{rule.id}: crashed on repo pass: {exc!r}")

    findings.sort(key=lambda x: (str(x.path), x.line, x.rule_id))
    return findings, errors
