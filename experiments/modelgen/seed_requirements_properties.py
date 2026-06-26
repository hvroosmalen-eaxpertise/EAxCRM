"""Set ID (Alias), Status, and Version on requirements in EA via COM API.

Run after sync_requirements_from_ea.py to populate EA with spec-compliant IDs.
Usage:
    python seed_requirements_properties.py [--qea M:\\path\\EAxCRM.qea]
"""
import sys, os, argparse

DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"

# Mapping: EA Name → (ID, Status, Version)
ID_MAP = {
    "EAxCRM must support the procurement process": ("PRO-1", "Approved", "1.0"),
    "EAXCRM must support the sales process": ("SAL-1", "Approved", "1.0"),
    "Procurement can be done via Prolaborate": ("PRO-5.4", "Approved", "1.0"),
    "Procument can be done via multiple parties": ("PRO-5", "Approved", "1.0"),
    "EAxCRM must show a UX that shows the current state of Procuement": ("RPT-4", "Proposed", "1.0"),
    "Procurement can be done via Ability Engineering": ("PRO-5.3", "Approved", "1.0"),
    "Procurement can be done via Sparx Systems EU": ("PRO-5.2", "Approved", "1.0"),
    "Procurement can be done via Sparx Systems LTD": ("PRO-5.1", "Approved", "1.0"),
}


def find_package(parent, name):
    for i in range(parent.Packages.Count):
        p = parent.Packages.GetAt(i)
        if p.Name == name:
            return p
        found = find_package(p, name)
        if found:
            return found
    return None


def get_ea_pids():
    import subprocess
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq EA.exe", "/FO", "CSV"],
            capture_output=True, text=True, timeout=10
        )
        pids = set()
        for line in result.stdout.strip().split("\n")[1:]:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                try:
                    pids.add(int(parts[1].strip('"')))
                except ValueError:
                    pass
        return pids
    except:
        return set()


def main():
    parser = argparse.ArgumentParser(description="Seed requirement properties in EA")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    args = parser.parse_args()

    try:
        import win32com.client
    except ImportError:
        print("FAIL: win32com not installed. Run: pip install pywin32")
        sys.exit(1)

    before_pids = get_ea_pids()

    repo = win32com.client.Dispatch("EA.Repository")
    repo.OpenFile(args.qea)
    print(f"Connected: {repo.ConnectionString}")

    root = repo.Models.GetAt(0)
    pkg = find_package(root, "EAxCRM Requirements")
    if not pkg:
        print("FAIL: 'EAxCRM Requirements' package not found")
        repo.CloseFile()
        sys.exit(1)

    try:
        pkg.Elements.Refresh()
        count = 0
        for i in range(pkg.Elements.Count):
            el = pkg.Elements.GetAt(i)
            if el.Type != "Requirement":
                continue
            if el.Name in ID_MAP:
                aid, status, version = ID_MAP[el.Name]
                changed = False
                if el.Alias != aid:
                    el.Alias = aid
                    changed = True
                if el.Status != status:
                    el.Status = status
                    changed = True
                if el.Version != version:
                    el.Version = version
                    changed = True
                if changed:
                    el.Update()
                    print(f"  Updated {aid:8s}  {el.Name}")
                else:
                    print(f"  Skipped {aid:8s}  (no change)")
                count += 1
            else:
                print(f"  ?         {el.Name}")

        print(f"Processed {count} requirements.")

    finally:
        try:
            repo.CloseFile()
        except:
            pass

    after_pids = get_ea_pids()
    new_pids = after_pids - before_pids
    if new_pids:
        import subprocess
        for pid in new_pids:
            try:
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True, timeout=5)
            except:
                pass


if __name__ == "__main__":
    main()
