"""Create/update Requirements in EAxCRM.qea from Markdown model file.

Usage:
    python generate_requirements_from_md.py [--qea M:\\path\\EAxCRM.qea] [--md M:\\path\\EAxCRM-Requirements.md]
"""
import sys, os, argparse, json, re, subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-Requirements.md"
GUID_MAP_PATH = os.path.join(SCRIPT_DIR, "requirements_guid_map.json")


def parse_md(path):
    """Parse requirements Markdown into a list of dicts."""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    requirements = []
    current = None

    for line in lines:
        line = line.rstrip()
        # Detect requirement section header
        m = re.match(r"^### Requirement\u2014(\S+)", line)
        if m:
            if current:
                requirements.append(current)
            current = {"id": m.group(1), "name": "", "alias": "", "description": "",
                       "status": "Proposed", "version": "1.0", "guid": "", "parents": []}
            continue
        if current is None:
            continue

        # Parse fields
        m = re.match(r"^- Name:\s*(.*)", line)
        if m:
            current["name"] = m.group(1).strip()
            continue
        m = re.match(r"^- ID:\s*(.*)", line)
        if m:
            current["alias"] = m.group(1).strip()
            continue
        m = re.match(r"^- Description:\s*(.*)", line)
        if m:
            current["description"] = m.group(1).strip()
            continue
        m = re.match(r"^- Status:\s*(.*)", line)
        if m:
            current["status"] = m.group(1).strip()
            continue
        m = re.match(r"^- Version:\s*(.*)", line)
        if m:
            current["version"] = m.group(1).strip()
            continue
        m = re.match(r"^- GUID:\s*(.*)", line)
        if m:
            current["guid"] = m.group(1).strip()
            continue
        m = re.match(r"^\s{2}-\s+(.+)", line)
        if m and len(line) > 4 and line.startswith("  - "):
            # Parent reference under "Parents:"
            parent_id = m.group(1).strip()
            if parent_id and parent_id != "(none \u2014 top-level)":
                current.setdefault("parents", []).append(parent_id)

    if current:
        requirements.append(current)
    return requirements


def load_guid_map():
    if os.path.exists(GUID_MAP_PATH):
        with open(GUID_MAP_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_guid_map(guid_map):
    with open(GUID_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(guid_map, f, indent=2)
    print(f"Saved {len(guid_map)} GUID mappings to {GUID_MAP_PATH}")


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
    parser = argparse.ArgumentParser(description="Generate requirements in EAxCRM.qea from Markdown")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    args = parser.parse_args()

    requirements = parse_md(args.md)
    print(f"Parsed {len(requirements)} requirements from MD")

    # Build lookup by safe_id
    req_by_id = {}
    for r in requirements:
        req_by_id[r["id"]] = r

    guid_map = load_guid_map()
    print(f"Loaded {len(guid_map)} GUID mappings")

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
        # Build existing elements lookup
        pkg.Elements.Refresh()
        existing_by_name = {}
        existing_by_guid = {}
        for i in range(pkg.Elements.Count):
            el = pkg.Elements.GetAt(i)
            if el.Type == "Requirement":
                existing_by_name[el.Name] = el
                existing_by_guid[el.ElementGUID] = el

        # Track which elements we touched (to detect orphans later)
        touched_ids = set()

        # Create or update elements
        print("\n--- Requirements ---")
        for req in requirements:
            md_guid = req["guid"]
            existing = None

            # 1) Look up by EA GUID from map
            ea_guid = guid_map.get(md_guid) if md_guid else None
            if ea_guid:
                try:
                    existing = repo.GetElementByGuid(ea_guid)
                except:
                    pass

            # 2) Look up by MD GUID directly
            if not existing and md_guid and md_guid in existing_by_guid:
                existing = existing_by_guid[md_guid]

            # 3) Look up by name
            if not existing and req["name"] in existing_by_name:
                existing = existing_by_name[req["name"]]

            if existing:
                # Update existing
                changed = False
                if existing.Name != req["name"]:
                    existing.Name = req["name"]
                    changed = True
                if existing.Alias != req["alias"]:
                    existing.Alias = req["alias"]
                    changed = True
                if (existing.Notes or "").strip() != req["description"]:
                    existing.Notes = req["description"]
                    changed = True
                if existing.Status != req["status"]:
                    existing.Status = req["status"]
                    changed = True
                if existing.Version != req["version"]:
                    existing.Version = req["version"]
                    changed = True
                if changed:
                    existing.Update()
                    print(f"  Updated {req['alias']:8s}  {req['name']}")
                else:
                    print(f"  Current {req['alias']:8s}  {req['name']}")

                # Sync GUID map
                if md_guid:
                    guid_map[md_guid] = existing.ElementGUID
                else:
                    # Assign a placeholder GUID key
                    guid_map[f"_{req['id']}"] = existing.ElementGUID

                touched_ids.add(existing.ElementID)
            else:
                # Create new
                new_el = pkg.Elements.AddNew(req["name"], "Requirement")
                new_el.Alias = req["alias"]
                new_el.Notes = req["description"]
                new_el.Status = req["status"]
                new_el.Version = req["version"]
                new_el.Update()
                pkg.Elements.Refresh()

                # Store GUID mapping
                if md_guid:
                    guid_map[md_guid] = new_el.ElementGUID
                else:
                    guid_map[f"_{req['id']}"] = new_el.ElementGUID

                print(f"  Created {req['alias']:8s}  {req['name']}  [{new_el.ElementGUID}]")
                touched_ids.add(new_el.ElementID)

        # Refresh elements list to pick up new IDs and build GUID→element map
        pkg.Elements.Refresh()
        fresh_by_guid = {}
        fresh_by_id = {}
        for i in range(pkg.Elements.Count):
            el = pkg.Elements.GetAt(i)
            if el.Type == "Requirement":
                fresh_by_guid[el.ElementGUID] = el
                fresh_by_id[el.ElementID] = el

        # --- Connectors (Aggregation = parent-child) ---
        print("\n--- Relationships ---")

        # Build existing connector index: {(client_id, supplier_id): connector}
        existing_conns = {}
        for el_id, el in fresh_by_id.items():
            el.Connectors.Refresh()
            for j in range(el.Connectors.Count):
                conn = el.Connectors.GetAt(j)
                if conn.Type == "Aggregation":
                    existing_conns[(conn.ClientID, conn.SupplierID)] = conn

        def resolve_element(req):
            """Resolve a requirement dict to an EA element via GUID map."""
            ea_guid = guid_map.get(req.get("guid", "")) or guid_map.get(f"_{req['id']}")
            if ea_guid and ea_guid in fresh_by_guid:
                return fresh_by_guid[ea_guid]
            return None

        for req in requirements:
            child_el = resolve_element(req)
            if not child_el:
                print(f"  SKIP '{req['id']}': child element not found")
                continue

            for parent_id_str in req.get("parents", []):
                parent_req = req_by_id.get(parent_id_str)
                if not parent_req:
                    print(f"  WARN '{req['id']}': parent '{parent_id_str}' not in MD")
                    continue

                parent_el = resolve_element(parent_req)
                if not parent_el:
                    print(f"  WARN '{req['id']}': parent element '{parent_id_str}' not found")
                    continue

                # Check if connector already exists
                key = (child_el.ElementID, parent_el.ElementID)
                if key in existing_conns:
                    print(f"  Connector exists: {req['id']} -> {parent_id_str}")
                    del existing_conns[key]
                else:
                    conn = child_el.Connectors.AddNew("", "Aggregation")
                    conn.SupplierID = parent_el.ElementID
                    conn.Update()
                    print(f"  Created connector: {req['id']} -> {parent_id_str}")

        # --- Delete orphan connectors ---
        for (client_id, supplier_id), conn in existing_conns.items():
            try:
                src_el = repo.GetElementByID(client_id)
                src_el.Connectors.Refresh()
                for k in range(src_el.Connectors.Count):
                    c = src_el.Connectors.GetAt(k)
                    if c.ConnectorID == conn.ConnectorID:
                        src_el.Connectors.Delete(k)
                        child_name = fresh_by_id.get(client_id, fresh_by_id.get(client_id, str(client_id)))
                        parent_name = fresh_by_id.get(supplier_id, fresh_by_id.get(supplier_id, str(supplier_id)))
                        print(f"  Deleted orphan connector: {child_name} -> {parent_name}")
                        break
            except:
                pass

        save_guid_map(guid_map)

    finally:
        try:
            repo.CloseFile()
        except:
            pass

    after_pids = get_ea_pids()
    new_pids = after_pids - before_pids
    if new_pids:
        for pid in new_pids:
            try:
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True, timeout=5)
            except:
                pass


if __name__ == "__main__":
    main()
