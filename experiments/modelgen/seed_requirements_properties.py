"""Set ID (Alias), Status, and Version on requirements in EA via COM API.

Run after sync_requirements_from_ea.py to populate EA with spec-compliant IDs.
Usage:
    python seed_requirements_properties.py [--qea M:\\path\\EAxCRM.qea]
"""
import sys, os, argparse
import ea_session
from changelog import ChangeLog

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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


def main():
    parser = argparse.ArgumentParser(description="Seed requirement properties in EA")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    args = parser.parse_args()

    try:
        import win32com.client
    except ImportError:
        print("FAIL: win32com not installed. Run: pip install pywin32")
        sys.exit(1)

    with ea_session.ea_repository(args.qea) as repo:
        root = ea_session.get_model_root(repo)
        pkg = find_package(root, "EAxCRM Requirements")
        if not pkg:
            print("FAIL: 'EAxCRM Requirements' package not found")
            sys.exit(1)

        clog = ChangeLog(os.path.join(SCRIPT_DIR, "requirements_changelog.md"))
        clog.checkpoint("Seeding properties")

        pkg.Elements.Refresh()
        count = 0
        for i in range(pkg.Elements.Count):
            el = pkg.Elements.GetAt(i)
            if el.Type != "Requirement":
                continue
            if el.Name in ID_MAP:
                aid, status, version = ID_MAP[el.Name]
                changed = False
                old_alias = el.Alias
                old_status = el.Status
                old_version = el.Version
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
                    actual_changes = {}
                    if old_alias != aid:
                        actual_changes["Alias"] = (old_alias, aid)
                    if old_status != status:
                        actual_changes["Status"] = (old_status, status)
                    if old_version != version:
                        actual_changes["Version"] = (old_version, version)
                    clog.log("updated", aid, el.Name, "Requirement", el.ElementGUID,
                             changes=actual_changes)
                    print(f"  Updated {aid:8s}  {el.Name}")
                else:
                    print(f"  Skipped {aid:8s}  (no change)")
                count += 1
            else:
                print(f"  ?         {el.Name}")

        print(f"Processed {count} requirements.")
        try:
            clog.checkpoint("Seed complete")
        finally:
            clog.close()


if __name__ == "__main__":
    main()
