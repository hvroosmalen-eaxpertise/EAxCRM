"""Shared EA COM automation session lifecycle.

Used by all generate_*.py / sync_*.py scripts to open an isolated EA instance,
activate an MDG technology, and clean up only the EA.exe process the session
itself spawned. NEVER touches a pre-existing EA.exe (e.g. one the user has
open interactively) -- see AGENTS.md "MANDATORY: NEVER Kill EA Processes".

DispatchEx (not Dispatch) is used deliberately: plain Dispatch("EA.Repository")
can attach to an EA automation server already registered in COM's Running
Object Table -- e.g. the user's own open EA instance on the same .qea file --
instead of spawning a clean one. That contention was the suspected cause of
EA's "Internal application error 61704" on repo.Models.GetAt(0).
"""
import subprocess
import threading
import time
import xml.etree.ElementTree as ET
from contextlib import contextmanager

import win32com.client


@contextmanager
def hang_guard(pids, timeout=90):
    """Force-kill `pids` if the wrapped block hasn't finished within `timeout`.

    Some EA COM calls (RefreshModelView/RefreshOpenDiagrams, CloseFile) have
    been observed to hang indefinitely -- not raise, just never return -- with
    no way to detect or interrupt the call itself. try/except is useless
    against this since nothing is thrown.

    The watchdog thread only ever runs `taskkill` (a plain OS command), never
    touches the COM object -- COM objects are apartment-threaded (STA) and
    calling one from a thread that didn't create it either fails outright or
    corrupts state, so the watchdog must never call into `repo` itself.
    Killing the EA.exe process out from under a blocked win32com call has
    been confirmed (2026-07-07 incident) to reliably unblock it: the pending
    call raises (caught by the surrounding try/except in the wrapped block)
    rather than hanging forever.
    """
    cancelled = threading.Event()

    def _watchdog():
        if not cancelled.wait(timeout):
            for pid in pids:
                try:
                    subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                                    capture_output=True, timeout=5)
                except Exception:
                    pass

    t = threading.Thread(target=_watchdog, daemon=True)
    t.start()
    try:
        yield
    finally:
        cancelled.set()


def get_ea_pids():
    """Return set of PIDs for all currently running EA.exe processes."""
    try:
        out = subprocess.check_output(
            ["powershell", "-command",
             "Get-Process -Name 'EA' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"],
            text=True, timeout=10
        )
        return set(int(pid.strip()) for pid in out.strip().splitlines() if pid.strip())
    except Exception:
        return set()


def kill_new_ea_processes(before_pids):
    """Kill only EA.exe processes that started after before_pids was captured."""
    new_pids = get_ea_pids() - before_pids
    for pid in new_pids:
        try:
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True, timeout=5)
        except Exception:
            pass
    return new_pids


@contextmanager
def ea_repository(qea_path, technology=None):
    """Open an isolated EA automation session; yields repo.

    On exit: refreshes the model tree/diagrams, closes the file, and kills
    only the EA.exe process this session spawned.
    """
    before_pids = get_ea_pids()
    print("  Spawning isolated EA.App instance (DispatchEx)...", flush=True)
    app = win32com.client.DispatchEx("EA.App")
    repo = app.Repository
    print(f"  Opening {qea_path} ...", flush=True)
    repo.OpenFile(qea_path)
    print(f"Connected: {repo.ConnectionString}", flush=True)

    if technology:
        t0 = time.time()
        try:
            repo.ActivateTechnology(technology)
            print(f"  Activated {technology} MDG technology [{time.time() - t0:.2f}s]", flush=True)
        except Exception as e:
            print(f"  Note: ActivateTechnology failed: {e} [{time.time() - t0:.2f}s]", flush=True)

    try:
        yield repo
    finally:
        spawned_pids = get_ea_pids() - before_pids
        with hang_guard(spawned_pids):
            try:
                repo.RefreshModelView(0)
                repo.RefreshOpenDiagrams(True)
            except Exception as e:
                print(f"  [refresh] RefreshModelView(0) failed: {e}", flush=True)
            try:
                repo.CloseFile()
            except Exception:
                pass
        killed = kill_new_ea_processes(before_pids)
        if killed:
            print(f"  Cleaned up {len(killed)} zombie EA process(es)", flush=True)


def sql_rows(repo, sql):
    """Run a SQL query via Repository.SQLQuery and yield each row as a dict.

    Backend-agnostic: routes through EA's own DB abstraction, so the same
    call works whether the .qea is backed by SQLite, SQL Server, Postgres,
    etc. THIS IS THE ONLY CORRECT WAY to run SQL-shaped reads against the
    EA repository from generator/sync scripts -- never `sqlite3.connect(qea)`.

    Returns a list of {column_name: text} dicts. NULL columns come back as
    the empty string (EA's XML uses <ColName/> self-closing tags for NULLs;
    they map to child.text == None, which we normalize to "").

    IMPORTANT silent-failure trap (verified empirically 2026-07-16):
      - Bad SQL (nonexistent table, syntax error) does NOT raise; it returns
        the same empty <EADATA> as a legitimate zero-row result.
      - Callers that need to distinguish "no rows" from "query broken" MUST
        validate the SQL by other means (schema probe, small sanity SELECT
        first) rather than trusting the empty-result path.

    Empirically-verified return shape:
      <?xml version="1.0" encoding="UTF-16" ...?>
      <EADATA version="1.0" exporter="Enterprise Architect">
        <Dataset_0>
          <Data>
            <Row><ColA>val</ColA><ColB>val</ColB></Row>
            ...
          </Data>
        </Dataset_0>
      </EADATA>
    """
    xml = repo.SQLQuery(sql)
    if not xml:
        return []
    # EA declares UTF-16 but hands the string over already decoded, so parse
    # as str; ElementTree accepts str input and ignores the declared encoding
    # when there's no BOM.
    root = ET.fromstring(xml)
    return [
        {child.tag: (child.text or "") for child in row}
        for row in root.findall("./Dataset_0/Data/Row")
    ]


def get_model_root(repo, retries=5, delay=2):
    """repo.Models.GetAt(0) has been observed to transiently fail with EA's
    internal error 61704 immediately after OpenFile/ActivateTechnology.
    Retry briefly before giving up.
    """
    last_err = None
    for attempt in range(retries):
        try:
            return repo.Models.GetAt(0)
        except Exception as e:
            last_err = e
            print(f"  Models.GetAt(0) failed (attempt {attempt + 1}/{retries}): {e}", flush=True)
            time.sleep(delay)
    raise RuntimeError(f"repo.Models.GetAt(0) failed after {retries} retries: {last_err}")
