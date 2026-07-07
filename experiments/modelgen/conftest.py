"""Shared pytest fixtures and markers for EAxCRM modelgen tests."""
import os, re, shutil, subprocess, sys, tempfile, time
import pytest
import win32com.client

import ea_session

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"


def strip_guid_from_md(source_path: str, target_path: str) -> None:
    """Copy MD file stripping all - GUID: and - Diagram GUID: lines."""
    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()
    stripped = re.sub(
        r"^- (GUID|Diagram GUID): .*\n", "",
        content, flags=re.MULTILINE,
    )
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(stripped)


def _kill_ea_cleanly(before_pids):
    """Murder EA processes without COM CloseFile gymnastics.

    EA's COM CloseFile() can trigger SEH exceptions when the process is
    already shutting down (0x800706be / 0x800706ba). This helper skips
    CloseFile entirely and just kills the new EA.exe processes directly,
    which is what almost every generator's try/finally does anyway.
    """
    new_pids = ea_session.get_ea_pids() - before_pids
    for pid in new_pids:
        try:
            subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                           capture_output=True, timeout=5)
        except Exception:
            pass
    time.sleep(0.5)  # let OS release locks before file cleanup


def pytest_configure(config):
    """Register the 'ea' and 'slow' markers."""
    config.addinivalue_line("markers", "ea: tests that require a Windows EA installation")
    config.addinivalue_line("markers", "slow: tests that take >60s (EA COM API)")


@pytest.fixture(scope="module")
def sandbox_qea():
    """Copy EAxCRM.qea to a temp file; yield (qea_path, md_dir_path).

    md_dir_path is a temp directory where test-specific MD files can be
    written (with GUIDs stripped). Cleans up both on teardown.
    """
    qea_tmp = tempfile.NamedTemporaryFile(suffix=".qea", delete=False)
    qea_tmp.close()
    shutil.copy2(DEFAULT_QEA, qea_tmp.name)

    md_dir = tempfile.mkdtemp(prefix="sandbox_md_")

    before_pids = ea_session.get_ea_pids()
    try:
        yield (qea_tmp.name, md_dir)
    finally:
        os.unlink(qea_tmp.name)
        shutil.rmtree(md_dir, ignore_errors=True)
        _kill_ea_cleanly(before_pids)


@pytest.fixture(scope="module")
def sandbox_qea_with_repo(sandbox_qea):
    """Like sandbox_qea but also opens an EA session for the caller.

    Uses raw win32com (no CloseFile) to avoid Windows SEH exceptions from
    EA's COM shutdown. The process is killed on teardown via _kill_ea_cleanly.

    Yields (qea_path, md_dir, repo).
    """
    qea_path, md_dir = sandbox_qea
    before = ea_session.get_ea_pids()
    app = win32com.client.DispatchEx("EA.App")
    repo = app.Repository
    repo.OpenFile(qea_path)
    try:
        yield (qea_path, md_dir, repo)
    finally:
        _kill_ea_cleanly(before)
