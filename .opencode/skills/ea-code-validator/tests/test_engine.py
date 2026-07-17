"""Engine-level tests: scope discovery, rule registration, crash isolation."""
from __future__ import annotations

import pathlib
import textwrap

import pytest

import engine  # noqa: E402


# ---------------------------------------------------------------------------
# Scope discovery


def _write(tmp: pathlib.Path, rel: str, body: str) -> pathlib.Path:
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(body), encoding="utf-8")
    return p.resolve()


def test_scope_includes_modelgen_dir(tmp_path: pathlib.Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    a = _write(tmp_path, "modelgen/generate_x.py", "print(1)\n")
    _write(tmp_path, "other/plain.py", "print(1)\n")
    scope = engine.discover_scope([tmp_path], respect_gitignore=False)
    assert a in scope
    assert all(p.name != "plain.py" for p in scope)


def test_scope_includes_ea_session_importer(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    a = _write(tmp_path, "elsewhere/uses_ea.py", "from ea_session import ea_repository\n")
    scope = engine.discover_scope([tmp_path], respect_gitignore=False)
    assert a in scope


def test_scope_excludes_plain_django(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, "contacts/models.py",
           "from django.db import models\nclass X(models.Model):\n    pass\n")
    scope = engine.discover_scope([tmp_path], respect_gitignore=False)
    assert scope == []


def test_scope_excludes_ignored_dirs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write(tmp_path, ".venv/modelgen/junk.py", "print(1)\n")
    scope = engine.discover_scope([tmp_path], respect_gitignore=False)
    assert scope == []


def test_scope_excludes_own_fixtures(tmp_path, monkeypatch):
    """Fixtures under ea-code-validator/tests/fixtures/ must not be scanned."""
    monkeypatch.chdir(tmp_path)
    # A path shaped like our own fixture tree — should be skipped.
    _write(
        tmp_path,
        ".opencode/skills/ea-code-validator/tests/fixtures/ea001_positive/x.py",
        "from ea_session import ea_repository  # noqa\nimport sqlite3\n",
    )
    scope = engine.discover_scope([tmp_path], respect_gitignore=False)
    assert scope == []


def test_scope_win32com_ea_dispatch(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    a = _write(tmp_path, "elsewhere/direct_ea.py",
               "import win32com.client\n"
               "app = win32com.client.Dispatch('EA.App')\n")
    scope = engine.discover_scope([tmp_path], respect_gitignore=False)
    assert a in scope


# ---------------------------------------------------------------------------
# Registration + crash isolation
#
# These tests mutate engine's global rule lists, so they save/restore.


@pytest.fixture
def _clean_rules():
    saved_file = list(engine._file_rules)
    saved_repo = list(engine._repo_rules)
    saved_loaded = engine._rules_loaded
    engine._file_rules.clear()
    engine._repo_rules.clear()
    engine._rules_loaded = True  # skip auto-load during these tests
    try:
        yield
    finally:
        engine._file_rules[:] = saved_file
        engine._repo_rules[:] = saved_repo
        engine._rules_loaded = saved_loaded


def test_register_file_and_repo_rules(_clean_rules):
    class F:
        id = "TEST_F"
        description = "file"
        def check(self, path, source, tree): return []

    class R:
        id = "TEST_R"
        description = "repo"
        def check(self, files): return []

    engine.register(F())
    engine.register(R())
    ids = {r.id for r in engine.registered_rules()}
    assert ids == {"TEST_F", "TEST_R"}


def test_duplicate_id_rejected(_clean_rules):
    class F:
        id = "DUP"
        description = "d"
        def check(self, path, source, tree): return []

    engine.register(F())
    with pytest.raises(ValueError):
        engine.register(F())


def test_rule_crash_isolated(_clean_rules, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    target = _write(tmp_path, "modelgen/x.py", "print(1)\n")

    class Boom:
        id = "BOOM"
        description = "always crashes"
        def check(self, path, source, tree):
            raise RuntimeError("kaboom")

    class Good:
        id = "GOOD"
        description = "always finds one"
        def check(self, path, source, tree):
            yield engine.Finding(path, 1, self.id, "hi")

    engine.register(Boom())
    engine.register(Good())

    findings, errors = engine.run([tmp_path], respect_gitignore=False)
    assert any(f.rule_id == "GOOD" for f in findings)
    assert any("BOOM" in e for e in errors)


# ---------------------------------------------------------------------------
# Finding formatting


def test_finding_format_relative(tmp_path):
    f = engine.Finding(tmp_path / "a" / "b.py", 42, "EA999", "bad thing")
    assert f.format(root=tmp_path) == "a/b.py:42: EA999 bad thing"


def test_finding_format_absolute_when_outside_root(tmp_path):
    other = pathlib.Path("/somewhere/else/x.py")
    f = engine.Finding(other, 1, "EA999", "msg")
    out = f.format(root=tmp_path)
    assert out.endswith(":1: EA999 msg")
