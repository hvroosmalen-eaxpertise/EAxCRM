"""Completeness tests: intended (from MD → guid_map) vs created (in EA).

For each generator that supports ``--state-dir``, seed a sandbox
md_dir with the current guid_map, run the generator against a
sandboxed ``.qea`` copy, then open the resulting repo and verify
every entry in the post-run guid_map resolves to a real object in EA.

**Answers the question:** "the generator was supposed to create N
things — did all N end up in the model?"

Marked ``@pytest.mark.slow`` — not part of the default fast suite.
Run with::

    python -m pytest -m slow modelgen/test_generators_completeness.py -v

The customer-account UI (wireframe) generator is excluded: it
hard-codes the guid_map path to ``modelgen/`` via ``wireframe_engine``
so running it against a sandbox would clobber the real
``customeraccount_ui_guid_map.json``. Adding ``--state-dir`` support
to ``wireframe_engine`` is tracked separately.
"""
import json
import os
import shutil
import subprocess
import sys
from typing import Iterator

import pytest

import ea_session
from conftest import SCRIPT_DIR


# ---------------------------------------------------------------------------
# Helpers


def _seed_guid_map(name: str, md_dir: str) -> None:
    """Copy modelgen/<name> to sandbox md_dir so the generator starts idempotent."""
    src = os.path.join(SCRIPT_DIR, name)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(md_dir, name))


def _iter_guid_entries(guid_map: dict) -> Iterator[tuple[str, str, str]]:
    """Yield (hint, key, guid) for each entry.

    The hint indicates which lookup to try first ('element', 'connector',
    'diagram'), but resolution falls back to the other kinds if the first
    lookup returns None — the archimate guid_map, for example, keys bare
    GUIDs for elements *and* connectors indiscriminately.

    Handles the three shapes used across generators: flat, prefixed
    (``_diagram_*``, ``rel:*``), and nested (``elements``/``diagrams``).
    """
    for k, v in guid_map.items():
        if isinstance(v, dict):
            hint = "diagram" if k == "diagrams" else "element"
            for inner_k, inner_v in v.items():
                if isinstance(inner_v, str):
                    yield hint, f"{k}/{inner_k}", inner_v
            continue
        if not isinstance(v, str):
            continue
        if k.startswith("_diagram_"):
            yield "diagram", k, v
        elif k.startswith("rel:"):
            yield "connector", k, v
        else:
            yield "element", k, v


def _resolve_any(repo, hint: str, guid: str):
    """Try element/connector/diagram lookups in an order biased by hint.

    EA's Get*ByGuid methods either return None or raise ``pywintypes.com_error``
    ("Can't find matching ID") when the GUID doesn't match that kind. Treat
    both outcomes as "not found" and keep trying the other kinds.
    """
    order = {
        "diagram": ("GetDiagramByGuid", "GetElementByGuid", "GetConnectorByGuid"),
        "connector": ("GetConnectorByGuid", "GetElementByGuid", "GetDiagramByGuid"),
        "element": ("GetElementByGuid", "GetConnectorByGuid", "GetDiagramByGuid"),
    }[hint]
    for method in order:
        try:
            obj = getattr(repo, method)(guid)
        except Exception:
            continue
        if obj is not None:
            return obj
    return None


def _verify_all_guids_resolve(qea_path: str, guid_map: dict) -> list[str]:
    """Return list of guid_map entries that do NOT resolve to any EA object."""
    missing: list[str] = []
    with ea_session.ea_repository(qea_path) as repo:
        for hint, key, guid in _iter_guid_entries(guid_map):
            if _resolve_any(repo, hint, guid) is None:
                missing.append(f"{hint}:{key}={guid}")
    return missing


def _run_generator(script: str, qea_path: str, md_dir: str) -> None:
    proc = subprocess.run(
        [sys.executable, os.path.join(SCRIPT_DIR, script),
         "--qea", qea_path, "--state-dir", md_dir],
        capture_output=True, text=True, timeout=300,
    )
    if proc.returncode != 0:
        raise AssertionError(
            f"{script} failed (exit {proc.returncode})\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def _completeness_check(script: str, guid_map_name: str, sandbox_qea) -> None:
    qea_path, md_dir = sandbox_qea
    _seed_guid_map(guid_map_name, md_dir)
    _run_generator(script, qea_path, md_dir)

    guid_map_path = os.path.join(md_dir, guid_map_name)
    assert os.path.exists(guid_map_path), (
        f"{script} did not produce {guid_map_name} in the sandbox md_dir"
    )
    with open(guid_map_path) as f:
        guid_map = json.load(f)

    total = sum(1 for _ in _iter_guid_entries(guid_map))
    assert total > 0, f"{guid_map_name} has zero entries after run"

    missing = _verify_all_guids_resolve(qea_path, guid_map)
    assert not missing, (
        f"{script} — {len(missing)}/{total} intended entries missing from EA:\n"
        + "\n".join(f"  - {m}" for m in missing[:20])
        + (f"\n  ... ({len(missing) - 20} more)" if len(missing) > 20 else "")
    )


# ---------------------------------------------------------------------------
# One test per generator (each ~30-60s of EA COM time)


@pytest.mark.ea
@pytest.mark.slow
class TestGeneratorCompleteness:
    def test_archimate(self, sandbox_qea):
        _completeness_check(
            "generate_archimate.py", "archimate_guid_map.json", sandbox_qea
        )

    def test_ldm(self, sandbox_qea):
        _completeness_check(
            "generate_ldm_from_md.py", "ldm_guid_map.json", sandbox_qea
        )

    def test_requirements(self, sandbox_qea):
        _completeness_check(
            "generate_requirements_from_md.py",
            "requirements_guid_map.json",
            sandbox_qea,
        )

    def test_sales_process(self, sandbox_qea):
        _completeness_check(
            "generate_sales_process_from_md.py",
            "sales_guid_map.json",
            sandbox_qea,
        )

    def test_newsletter_process(self, sandbox_qea):
        _completeness_check(
            "generate_newsletter_process_from_md.py",
            "newsletter_guid_map.json",
            sandbox_qea,
        )

    def test_customeraccount_process(self, sandbox_qea):
        _completeness_check(
            "generate_customeraccount_process_from_md.py",
            "customeraccount_guid_map.json",
            sandbox_qea,
        )
