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
import os
import subprocess
import sys

import pytest

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
# UML Data Model generator regression
# -------------------------------------------------------------------------


@pytest.mark.ea
class TestUmlDataModelGenerator:
    def test_generate_uml_datamodel(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_uml_datamodel.py"),
             "--qea", qea_path, "--state-dir", md_dir],
            capture_output=True, text=True, timeout=300,
        )
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr)
        assert proc.returncode == 0, f"generate_uml_datamodel failed: {proc.stderr}"
        assert "updated" in proc.stdout or "Done" in proc.stdout

    def test_generate_uml_datamodel_idempotent(self, sandbox_qea):
        qea_path, md_dir = sandbox_qea

        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "generate_uml_datamodel.py"),
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
