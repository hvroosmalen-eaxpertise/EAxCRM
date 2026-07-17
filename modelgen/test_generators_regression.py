"""Sandbox integration tests: run generators on a temp copy of EAxCRM.qea.

All tests require Windows + EA installed (marked @pytest.mark.ea). Each test
copies EAxCRM.qea to a temp file and runs a generator against it using the
original MD file (GUIDs intact — the sandbox QEA is a byte-for-byte copy of
the real one, so GUIDs match).

NOTE: GUIDs are NOT stripped from MD files in these integration tests because
the generators (e.g. generate_archimate.py line 294) skip elements with no
GUID in MD. The sandbox QEA copy preserves all GUIDs from the original, so
the generator finds existing elements and updates them — this tests the
idempotency path (no crashes, valid output on a real-ish EA project).

Re-running within the same test module uses the same sandbox QEA copy.
"""
import json
import os
import subprocess
import sys
import textwrap

import pytest

import ea_session
from conftest import SCRIPT_DIR, DEFAULT_QEA

DEFAULT_MD_DIR = r"M:\EAxCRM\models"


def _generated_md(rel_path):
    return os.path.join(DEFAULT_MD_DIR, rel_path)


# -------------------------------------------------------------------------
# Sanity: basic EA connectivity on the sandbox copy
# -------------------------------------------------------------------------


@pytest.mark.ea
class TestSandboxConnectivity:
    """Verify the sandbox QEA is openable and has expected structure."""

    def test_open_and_read_root(self, sandbox_qea_with_repo):
        qea_path, md_dir, repo = sandbox_qea_with_repo
        root = repo.Models.GetAt(0)
        assert root is not None
        assert root.Name != ""
        assert root.Packages.Count > 0

    def test_has_expected_packages(self, sandbox_qea_with_repo):
        qea_path, md_dir, repo = sandbox_qea_with_repo
        root = repo.Models.GetAt(0)
        names = set()
        for i in range(root.Packages.Count):
            names.add(root.Packages.GetAt(i).Name)
        # EAxCRM model should have typical top-level packages
        assert "Application Architecture" in names or "Business Architecture" in names


# -------------------------------------------------------------------------
# ArchiMate generator regression
# -------------------------------------------------------------------------


@pytest.mark.ea
class TestArchimateGenerator:
    def test_generate_archimate(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_archimate.py"),
             "--qea", qea_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
        assert proc.returncode == 0, f"generate_archimate failed: {proc.stderr}"
        assert "updated" in proc.stdout or "Done" in proc.stdout

    def test_generate_archimate_idempotent(self, sandbox_qea):
        """Second run — should be idempotent (same output pattern)."""
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_archimate.py"),
             "--qea", qea_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        assert proc.returncode == 0, f"idempotent run failed: {proc.stderr}"
        assert "error" not in proc.stdout.lower()


# -------------------------------------------------------------------------
# Logical Data Model (LDM) generator regression
# -------------------------------------------------------------------------


@pytest.mark.ea
class TestLdmGenerator:
    def test_generate_ldm(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_ldm_from_md.py"),
             "--qea", qea_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
        assert proc.returncode == 0, f"generate_ldm failed: {proc.stderr}"
        assert "updated" in proc.stdout or "Done" in proc.stdout

    def test_generate_ldm_idempotent(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_ldm_from_md.py"),
             "--qea", qea_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        assert proc.returncode == 0
        assert "error" not in proc.stdout.lower()


# -------------------------------------------------------------------------
# Requirements generator regression
# -------------------------------------------------------------------------


@pytest.mark.ea
class TestRequirementsGenerator:
    def test_generate_requirements(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_requirements_from_md.py"),
             "--qea", qea_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
        assert proc.returncode == 0, f"generate_requirements failed: {proc.stderr}"
        assert "requirements" in proc.stdout or "All" in proc.stdout


# -------------------------------------------------------------------------
# BPMN Sales Process generator regression
# -------------------------------------------------------------------------


@pytest.mark.ea
class TestSalesProcessGenerator:
    def test_generate_sales_process(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_sales_process_from_md.py"),
             "--qea", qea_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
        assert proc.returncode == 0, f"generate_sales_process failed: {proc.stderr}"
        assert "updated" in proc.stdout or "Created" in proc.stdout


# -------------------------------------------------------------------------
# BPMN Newsletter Process generator regression
# -------------------------------------------------------------------------


@pytest.mark.ea
class TestNewsletterProcessGenerator:
    def test_generate_newsletter_process(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_newsletter_process_from_md.py"),
             "--qea", qea_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
        assert proc.returncode == 0, f"generate_newsletter_process failed: {proc.stderr}"
        assert "updated" in proc.stdout or "Created" in proc.stdout


# -------------------------------------------------------------------------
# Customer Account Process generator regression
# -------------------------------------------------------------------------


@pytest.mark.ea
class TestCustomerAccountProcessGenerator:
    def test_generate_customeraccount_process(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_customeraccount_process_from_md.py"),
             "--qea", qea_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
        assert proc.returncode == 0, f"generate_customeraccount_process failed: {proc.stderr}"
        assert "updated" in proc.stdout or "Created" in proc.stdout


# -------------------------------------------------------------------------
# Issue #19 regression: placeholder-GUID handling
# -------------------------------------------------------------------------


@pytest.mark.ea
class TestArchimatePlaceholderGuidRegression:
    """Issue #19 -- multiple MD elements with ``GUID: {}`` used to collide
    on ``guid_map["{}"]``. Every placeholder-GUID entry wrote to the same
    map slot, so on rerun the generator would silently rename existing EA
    elements to whatever placeholder entry came last, or create duplicates.

    The fix (``_el_key``) mirrors ``_rel_key`` -- placeholders fall back to
    a synthetic ``el:<id>`` key so each element gets its own slot.
    """

    # Names must not clash with any existing EA element in EAxCRM.qea's
    # ArchiMate package; using ``Issue19_*`` prefix to keep the pkg-name
    # fallback in sync_elements from adopting an unrelated existing element.
    _MD = textwrap.dedent("""\
        # Issue #19 regression fixture

        ## Elements

        ### BusinessActor — e-i19-alpha
        - Name: Issue19_Alpha
        - Description: Placeholder-GUID test element A
        - GUID: {}

        ### BusinessActor — e-i19-beta
        - Name: Issue19_Beta
        - Description: Placeholder-GUID test element B
        - GUID: {}

        ### BusinessActor — e-i19-gamma
        - Name: Issue19_Gamma
        - Description: Placeholder-GUID test element C
        - GUID: {}

        ## Relationships
        """)

    _EXPECTED_KEYS = ("el:e-i19-alpha", "el:e-i19-beta", "el:e-i19-gamma")
    _EXPECTED_NAMES = ("Issue19_Alpha", "Issue19_Beta", "Issue19_Gamma")

    def _run_generator(self, qea_path, md_path, md_dir):
        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_archimate.py"),
             "--qea", qea_path, "--md", md_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
        assert proc.returncode == 0, (
            f"generate_archimate failed (exit {proc.returncode}): {proc.stderr}"
        )
        return proc

    def test_placeholder_guids_do_not_collide_and_survive_rerun(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        md_path = os.path.join(md_dir, "issue19.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self._MD)

        # Fresh (empty) guid_map so the placeholder-GUID path exercises
        # element creation, not the map's cached lookup.
        guid_map_path = os.path.join(md_dir, "archimate_guid_map.json")
        with open(guid_map_path, "w", encoding="utf-8") as f:
            json.dump({}, f)

        # --- First run: three elements created, three distinct map keys ---
        first = self._run_generator(qea_path, md_path, md_dir)
        assert first.stdout.count("Created:") >= 3, (
            "expected 3 Created lines on first run; got:\n" + first.stdout
        )

        with open(guid_map_path, encoding="utf-8") as f:
            map1 = json.load(f)

        for k in self._EXPECTED_KEYS:
            assert k in map1, (
                f"guid_map missing {k!r} -- placeholders collided into "
                f"guid_map['{{}}']? keys={sorted(map1)}"
            )
        # And no stray "{}" key from the old collision path
        assert "{}" not in map1, (
            f"guid_map still has '{{}}' collision key: {map1['{}']!r}"
        )
        ea_guids = {map1[k] for k in self._EXPECTED_KEYS}
        assert len(ea_guids) == 3, (
            f"three placeholder-GUID elements collapsed to fewer EA GUIDs: "
            f"{ {k: map1[k] for k in self._EXPECTED_KEYS} }"
        )

        # --- Verify in EA: three distinct elements with expected names ---
        with ea_session.ea_repository(qea_path) as repo:
            resolved = {}
            for k, name in zip(self._EXPECTED_KEYS, self._EXPECTED_NAMES):
                elem = repo.GetElementByGuid(map1[k])
                assert elem is not None, f"{k} EA GUID does not resolve"
                resolved[k] = elem.Name
                assert elem.Name == name, (
                    f"{k} resolved to element named {elem.Name!r}, "
                    f"expected {name!r} -- silent rename bug still present"
                )
            assert len(set(resolved.values())) == 3, (
                f"three placeholder entries all resolve to same element name: {resolved}"
            )

        # --- Second run: idempotent, no rename thrash, same EA GUIDs ---
        second = self._run_generator(qea_path, md_path, md_dir)
        assert "Created:" not in second.stdout, (
            "second run created elements (should be pure updates):\n" + second.stdout
        )

        with open(guid_map_path, encoding="utf-8") as f:
            map2 = json.load(f)
        for k in self._EXPECTED_KEYS:
            assert map2[k] == map1[k], (
                f"{k} EA GUID changed between runs "
                f"({map1[k]} -> {map2[k]}) -- rename/duplicate thrash"
            )
