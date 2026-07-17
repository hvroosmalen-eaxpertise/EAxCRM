"""Rule-level tests: walk fixtures/<id>_{positive,negative}/ and assert.

Each rule's fixture directory pair drives its own parametrized tests.
"""
from __future__ import annotations

import ast
import pathlib

import pytest

import engine


FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def _run_rule(rule_id: str, path: pathlib.Path) -> list[engine.Finding]:
    engine.load_rules()
    rule = next(r for r in engine.registered_rules() if r.id == rule_id)
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    return list(rule.check(path, source, tree))


def _positives(rule_id: str) -> list[pathlib.Path]:
    return sorted((FIXTURES / f"{rule_id.lower()}_positive").glob("*.py"))


def _negatives(rule_id: str) -> list[pathlib.Path]:
    return sorted((FIXTURES / f"{rule_id.lower()}_negative").glob("*.py"))


# ---------------------------------------------------------------------------
# EA001


@pytest.mark.parametrize("path", _positives("EA001"), ids=lambda p: p.name)
def test_ea001_positive_fires(path):
    findings = _run_rule("EA001", path)
    assert findings, f"expected EA001 to fire on {path.name}"
    assert all(f.rule_id == "EA001" for f in findings)


@pytest.mark.parametrize("path", _negatives("EA001"), ids=lambda p: p.name)
def test_ea001_negative_silent(path):
    findings = _run_rule("EA001", path)
    assert findings == [], (
        f"expected EA001 to be silent on {path.name}, got: "
        + ", ".join(f.format() for f in findings)
    )


# ---------------------------------------------------------------------------
# EA002 (repo-level: give it the whole fixture directory as a file list)


def _run_repo_rule(rule_id: str, files: list[pathlib.Path]) -> list[engine.Finding]:
    engine.load_rules()
    rule = next(r for r in engine.registered_rules() if r.id == rule_id)
    return list(rule.check(files))


def test_ea002_positive_dir_fires():
    files = sorted((FIXTURES / "ea002_positive").glob("*.py"))
    findings = _run_repo_rule("EA002", files)
    assert findings, "expected EA002 to fire on ea002_positive/"
    assert all(f.rule_id == "EA002" for f in findings)
    assert any("orphan" in f.message for f in findings)


def test_ea002_negative_dir_silent():
    files = sorted((FIXTURES / "ea002_negative").glob("*.py"))
    findings = _run_repo_rule("EA002", files)
    assert findings == [], (
        "expected EA002 to be silent on ea002_negative/, got: "
        + ", ".join(f.format() for f in findings)
    )


def test_ea002_finds_sync_sibling_on_disk_when_not_in_input():
    """--changed passes only staged files.  If the sync sibling is on
    disk but not in the input list, EA002 must still recognise it."""
    generate_only = [FIXTURES / "ea002_negative" / "generate_paired_from_md.py"]
    findings = _run_repo_rule("EA002", generate_only)
    assert findings == [], (
        "EA002 must scan the enclosing directory for sync siblings, "
        "not just the input file list; got: "
        + ", ".join(f.format() for f in findings)
    )


# ---------------------------------------------------------------------------
# EA003


@pytest.mark.parametrize("path", _positives("EA003"), ids=lambda p: p.name)
def test_ea003_positive_fires(path):
    findings = _run_rule("EA003", path)
    assert findings, f"expected EA003 to fire on {path.name}"
    assert all(f.rule_id == "EA003" for f in findings)


@pytest.mark.parametrize("path", _negatives("EA003"), ids=lambda p: p.name)
def test_ea003_negative_silent(path):
    findings = _run_rule("EA003", path)
    assert findings == [], (
        f"expected EA003 to be silent on {path.name}, got: "
        + ", ".join(f.format() for f in findings)
    )


# ---------------------------------------------------------------------------
# EA004


@pytest.mark.parametrize("path", _positives("EA004"), ids=lambda p: p.name)
def test_ea004_positive_fires(path):
    findings = _run_rule("EA004", path)
    assert findings, f"expected EA004 to fire on {path.name}"
    assert all(f.rule_id == "EA004" for f in findings)


@pytest.mark.parametrize("path", _negatives("EA004"), ids=lambda p: p.name)
def test_ea004_negative_silent(path):
    findings = _run_rule("EA004", path)
    assert findings == [], (
        f"expected EA004 to be silent on {path.name}, got: "
        + ", ".join(f.format() for f in findings)
    )
