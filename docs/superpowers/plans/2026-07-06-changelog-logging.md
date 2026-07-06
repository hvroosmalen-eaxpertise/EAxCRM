# Changelog Logging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-element/connector structured audit logging (Markdown files, newest-at-top, ~1 MB cap) to all EAxCRM generator and sync scripts.

**Architecture:** A shared `changelog.py` utility with a `ChangeLog` class. Each generator calls `clog.log()` at each create/update/delete site. Each sync script does a before/after MD diff and calls `clog.log_diff()` with the structured result. Phase checkpoints for hang diagnostics.

**Tech Stack:** Python 3.13 stdlib only (no new dependencies).

## Global Constraints

- No new dependencies beyond Python 3.13 stdlib
- COM API calls not duplicated — changelog hooks reuse existing return values
- Per-generator changelog files created in `experiments/modelgen/`
- No LLM required for diff computations

---

## File Structure

| File | Change | Responsibility |
|------|--------|----------------|
| `experiments/modelgen/changelog.py` | **Create** | `ChangeLog` class — log(), checkpoint(), log_diff(), prepend, size cap, atomic write |
| `experiments/modelgen/test_changelog.py` | **Create** | Tests for format, prepend, trim, atomic write |
| `experiments/modelgen/bpmn_config.py` | **Modify** | Add `changelog_file` field to `ProcessConfig`, paths on each config instance |
| `experiments/modelgen/bpmn_engine.py` | **Modify** | Add changelog calls in `generate()` (per-element/connector) and `sync_to_md()` (MD diff + log_diff); add `compute_md_diff()` |
| `experiments/modelgen/generate_archimate.py` | **Modify** | Add changelog calls in element and relation loops |
| `experiments/modelgen/generate_uml_datamodel.py` | **Modify** | Add changelog calls for entities, attributes, connectors |
| `experiments/modelgen/sync_datamodel_from_ea.py` | **Modify** | Add MD diff + log_diff |
| `experiments/modelgen/generate_requirements_from_md.py` | **Modify** | Add changelog calls for requirements, connectors, realisations |
| `experiments/modelgen/sync_requirements_from_ea.py` | **Modify** | Add MD diff + log_diff |
| `experiments/modelgen/ea_session.py` | **Modify** | Add changelog checkpoint at session start |

---

### Task 1: Create `changelog.py` + tests

**Files:**
- Create: `experiments/modelgen/changelog.py`
- Create: `experiments/modelgen/test_changelog.py`

**Interfaces:**
- Produces: `ChangeLog(filepath, max_bytes=1_000_000)` with methods:
  - `log(action, eid, name, kind, guid="", changes=None, run_id="")`
  - `checkpoint(phase, run_id="")`
  - `log_diff(diff: dict, run_id="")`
  - `close()` — finalizes entry, prepends to file, trims if over limit

- [ ] **Step 1: Write failing tests**

```python
"""Tests for changelog.py."""
import os
import tempfile
from changelog import ChangeLog


def make_changelog(max_bytes=10000):
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "test_changelog.md")
    return ChangeLog(path, max_bytes=max_bytes), path


def test_log_creates_file():
    clog, path = make_changelog()
    clog.log("created", "elem1", "Element One", "Activity", guid="{abc}")
    clog.close()
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert "created" in content.lower() or "Created" in content
    assert "Element One" in content
    assert "elem1" in content


def test_prepend_newest_first():
    clog, path = make_changelog()
    clog.log("created", "old", "Old Elem", "Activity")
    clog.close()
    clog2 = ChangeLog(path)
    clog2.log("created", "new", "New Elem", "Activity")
    clog2.close()
    with open(path) as f:
        content = f.read()
    assert content.index("New Elem") < content.index("Old Elem")


def test_log_updated_with_changes():
    clog, path = make_changelog()
    clog.log("updated", "elem1", "E One", "Activity",
             changes={"Notes": ("old note", "new note")})
    clog.close()
    with open(path) as f:
        content = f.read()
    assert "Notes" in content
    assert "old note" in content or "→" in content


def test_log_deleted():
    clog, path = make_changelog()
    clog.log("deleted", "old_elem", "Old Element", "DataObject")
    clog.close()
    with open(path) as f:
        content = f.read()
    assert "Deleted" in content


def test_size_cap_trims_oldest():
    clog, path = make_changelog(max_bytes=500)
    for i in range(50):
        clog.log("created", f"e{i}", f"Element {i}", "Activity")
    clog.close()
    with open(path) as f:
        content = f.read()
    assert len(content.encode("utf-8")) <= 600


def test_checkpoint():
    clog, path = make_changelog()
    clog.checkpoint("Elements complete")
    clog.log("created", "e1", "E One", "Activity")
    clog.close()
    with open(path) as f:
        content = f.read()
    assert "Elements complete" in content


def test_log_diff_created_deleted():
    clog, path = make_changelog()
    diff = {
        "created": [{"eid": "new_e", "name": "New Elem", "type": "Activity", "guid": "{g1}"}],
        "deleted": [{"eid": "old_e", "name": "Old Elem", "type": "DataObject"}],
        "updated": [],
        "connectors": [{"action": "created", "type": "SequenceFlow", "source": "a", "target": "b"}],
    }
    clog.log_diff(diff)
    clog.close()
    with open(path) as f:
        content = f.read()
    assert "New Elem" in content
    assert "Old Elem" in content
    assert "a → b" in content or "a" in content


def test_empty_buffer_no_file():
    clog, path = make_changelog()
    clog.close()
    assert not os.path.exists(path)
```

Run: `python -m pytest experiments/modelgen/test_changelog.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 2: Implement `changelog.py`**

```python
"""Shared changelog utility for EAxCRM generator/sync audit logging.

Logs element/connector create/update/delete/rename events to per-generator
Markdown files (newest-at-top, ~1 MB cap), plus phase checkpoints for hang
diagnostics.
"""
import os
import tempfile
from datetime import datetime, timezone


class ChangeLog:
    def __init__(self, filepath: str, max_bytes: int = 1_000_000):
        self.filepath = filepath
        self.max_bytes = max_bytes
        self._buffer = []

    def log(self, action: str, eid: str, name: str, kind: str,
            guid: str = "", changes: dict = None, run_id: str = ""):
        self._buffer.append({
            "action": action, "eid": eid, "name": name, "kind": kind,
            "guid": guid, "changes": changes, "run_id": run_id,
        })

    def checkpoint(self, phase: str, run_id: str = ""):
        self._buffer.append({"action": "_checkpoint", "phase": phase, "run_id": run_id})

    def log_diff(self, diff: dict, run_id: str = ""):
        for action in ("created", "updated", "deleted"):
            for item in diff.get(action, []):
                entry = dict(item)
                entry["action"] = action
                entry["run_id"] = run_id
                self._buffer.append(entry)
        for conn in diff.get("connectors", []):
            conn = dict(conn)
            conn["run_id"] = run_id
            self._buffer.append(conn)

    def close(self):
        if not self._buffer:
            return
        entry = self._format_entry()
        self._buffer = []
        old = ""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                old = f.read()
        combined = entry + old
        while len(combined.encode("utf-8")) > self.max_bytes:
            combined = self._trim_last_section(combined)
        dirname = os.path.dirname(self.filepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        self._write_atomic(self.filepath, combined)

    def _format_entry(self):
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        run_name = self._get_run_name()
        lines = [f"## {now} — {run_name}", ""]
        phases = [e for e in self._buffer if e.get("action") == "_checkpoint"]
        if phases:
            lines.append("### Checkpoints")
            for p in phases:
                lines.append(f"- {p['phase']}")
            lines.append("")
        for action_key, heading in [("created", "### Created"), ("updated", "### Updated"),
                                     ("deleted", "### Deleted"), ("renamed", "### Renamed"),
                                     ("synced", "### Synced")]:
            items = [e for e in self._buffer if e.get("action") == action_key]
            if not items:
                continue
            lines.append(heading)
            if action_key in ("updated", "renamed"):
                lines.append("| eid | Name | Type | GUID | Changes |\n|-----|------|------|------|---------|")
                for item in items:
                    chgs = self._format_changes(item.get("changes"))
                    lines.append(f"| {item['eid']} | {item['name']} | {item['kind']} | {item.get('guid', '')} | {chgs} |")
            else:
                lines.append("| eid | Name | Type | GUID |\n|-----|------|------|------|")
                for item in items:
                    lines.append(f"| {item['eid']} | {item['name']} | {item['kind']} | {item.get('guid', '')} |")
            lines.append("")
        conns = [e for e in self._buffer if "source" in e and "target" in e and "type" in e]
        if conns:
            lines.append("### Connectors\n| Action | Type | Source | Target | Condition |\n|--------|------|--------|--------|-----------|")
            for item in conns:
                lines.append(f"| {item.get('action', '')} | {item.get('type', '')} | {item.get('source', '')} | {item.get('target', '')} | {item.get('condition', '')} |")
            lines.append("")
        return "\n".join(lines) + "\n"

    def _get_run_name(self):
        rid = self._buffer[0].get("run_id", "") if self._buffer else ""
        return rid or os.path.basename(self.filepath).replace("_changelog.md", "").replace("_", " ").title()

    def _format_changes(self, changes):
        if not changes:
            return ""
        parts = []
        for k, v in changes.items():
            if isinstance(v, tuple):
                parts.append(f"{k}: {v[0]} → {v[1]}")
            else:
                parts.append(f"{k}: {v}")
        return "; ".join(parts)

    def _trim_last_section(self, content):
        lines = content.splitlines(keepends=True)
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("## ") and i > 0:
                return "".join(lines[:i])
        return content

    def _write_atomic(self, path, content):
        dirname = os.path.dirname(path) or "."
        fd, tmppath = tempfile.mkstemp(dir=dirname, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)
            os.replace(tmppath, path)
        except Exception:
            if os.path.exists(tmppath):
                os.unlink(tmppath)
            raise
```

- [ ] **Step 3: Run tests**

Run: `python -m pytest experiments/modelgen/test_changelog.py -v`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add experiments/modelgen/changelog.py experiments/modelgen/test_changelog.py
git commit -m "feat: add changelog.py — structured audit logging utility"
```


### Task 2: Wire BPMN engine — `bpmn_config.py` + `bpmn_engine.py`

**Files:**
- Modify: `experiments/modelgen/bpmn_config.py`
- Modify: `experiments/modelgen/bpmn_engine.py`

**Interfaces:**
- `ProcessConfig` gets `changelog_file: str = ""` field
- Each process instance gets a changelog path (e.g. `sales_changelog.md`)
- `bpmn_engine.generate()` opens/closes a `ChangeLog`, calls `.log()` inside `create_element()` for each element create/update and after each connector create
- `bpmn_engine.sync_to_md()` does MD diff via `compute_md_diff()`, calls `.log_diff()`
- New function `compute_md_diff(old_content, new_content, format_hint)` → diff dict

- [ ] **Step 1: Add `changelog_file` to `ProcessConfig`**

In `bpmn_config.py`, add field to dataclass and paths to each instance:

```python
@dataclass
class ProcessConfig:
    ...
    changelog_file: str = ""

CUSTOMER_ACCOUNT = ProcessConfig(
    ...
    changelog_file=os.path.join(SCRIPT_DIR, "customeraccount_changelog.md"),
)
SALES = ProcessConfig(
    ...
    changelog_file=os.path.join(SCRIPT_DIR, "sales_changelog.md"),
)
NEWSLETTER = ProcessConfig(
    ...
    changelog_file=os.path.join(SCRIPT_DIR, "newsletter_changelog.md"),
)
```

Need to add `import os` and `SCRIPT_DIR` to bpmn_config.py (or define SCRIPT_DIR if not there).

- [ ] **Step 2: Hook changelog into `generate()`**

After `parse_md()`, open a `ChangeLog`:

```python
clog = None
if config.changelog_file:
    clog = ChangeLog(config.changelog_file)
    clog.checkpoint("Parsed MD", run_id=getattr(config, "model_id", ""))
```

Inside `create_element()`, after the existing update/create blocks:

```python
# After the "existing" update path:
if existing:
    ...
    if clog:
        changes = {}
        if existing.Name != name: changes["Name"] = (existing.Name, name)
        if changes:
            clog.log("updated", eid, name, stereo, existing.ElementGUID, changes=changes)
        else:
            clog.log("updated", eid, name, stereo, existing.ElementGUID)
    ...

# After the "new_elem" create path:
if clog:
    clog.log("created", eid, name, stereo, new_elem.ElementGUID)
```

After connector creation loop:

```python
if clog:
    for flow in conn_list:
        clog.log("created" if flow newly created else "exists", "", "",
                 conn_type, "", changes={"source": flow["source"], "target": flow["target"],
                                          "condition": flow.get("condition", "")})
```

Before `print("Done.")`:

```python
if clog:
    clog.close()
```

- [ ] **Step 3: Add `compute_md_diff()` for sync direction**

```python
def compute_md_diff(old_content: str, new_content: str) -> dict:
    """Compare two process MD texts and return structured diff dict."""
    import re
    # Extract element headers: ### Type—eid or #### Type—eid
    def extract_elements(text):
        elems = {}
        for line in text.splitlines():
            m = re.match(r"#{2,4}\s+(.+?)[—–]\s*(.+)", line)
            if m:
                label = m.group(1).strip()
                eid = m.group(2).strip()
                elems[eid] = {"type": label}
        return elems

    old_elems = extract_elements(old_content) if old_content else {}
    new_elems = extract_elements(new_content)

    old_ids = set(old_elems.keys())
    new_ids = set(new_elems.keys())

    diff = {
        "created": [{"eid": eid, "name": eid, "type": new_elems[eid]["type"]}
                     for eid in sorted(new_ids - old_ids)],
        "deleted": [{"eid": eid, "name": eid, "type": old_elems[eid]["type"]}
                     for eid in sorted(old_ids - new_ids)],
        "updated": [],
        "connectors": [],
    }
    for eid in sorted(old_ids & new_ids):
        old_t = old_elems[eid]["type"]
        new_t = new_elems[eid]["type"]
        if old_t != new_t:
            diff["updated"].append({"eid": eid, "name": eid, "type": new_t,
                                    "changes": {"Type": (old_t, new_t)}})

    # Connector diff — extract lines under connector section headings
    def extract_connectors(text):
        conns = set()
        in_conn_section = False
        for line in text.splitlines():
            if re.match(r"###\s+(Sequence|Message|Data)", line):
                in_conn_section = True
                continue
            if line.startswith("## "):
                in_conn_section = False
                continue
            if in_conn_section and line.startswith("- "):
                m = re.match(r"- (.+?)\s*[→➡]\s*(.+?)(?:\s*\[(.+?)\])?$", line[2:])
                if m:
                    conns.add((m.group(1).strip(), m.group(2).strip()))
        return conns

    old_conns = extract_connectors(old_content) if old_content else set()
    new_conns = extract_connectors(new_content)

    for src, tgt in sorted(new_conns - old_conns):
        diff["connectors"].append({"action": "created", "type": "connector",
                                    "source": src, "target": tgt, "condition": ""})
    for src, tgt in sorted(old_conns - new_conns):
        diff["connectors"].append({"action": "deleted", "type": "connector",
                                    "source": src, "target": tgt, "condition": ""})

    return diff
```

- [ ] **Step 4: Hook changelog into `sync_to_md()`**

Before the final write block, read old MD (if exists), diff, log, then write:

```python
old_content = ""
if os.path.exists(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        old_content = f.read()

new_content = "\n".join(lines) + "\n"
diff = compute_md_diff(old_content, new_content)

clog = None
if config.changelog_file:
    clog = ChangeLog(config.changelog_file)
    clog.log_diff(diff, run_id=config.model_id)
    clog.close()

with open(md_path, "w", encoding="utf-8") as f:
    f.write(new_content)
```

- [ ] **Step 5: Run a smoke test**

Run: `python experiments/modelgen/generate_sales_process_from_md.py`
Expected: No errors. A file `experiments/modelgen/sales_changelog.md` exists with the run's changes.

- [ ] **Step 6: Commit**

```bash
git add experiments/modelgen/bpmn_config.py experiments/modelgen/bpmn_engine.py
git commit -m "feat: wire changelog logging into BPMN engine"
```


### Task 3: Wire `generate_archimate.py`

**Files:**
- Modify: `experiments/modelgen/generate_archimate.py`

- [ ] **Step 1: Open changelog after phase 1 startup**

After `log("Parsed ... elements, ... relationships")`, open:

```python
from changelog import ChangeLog
...
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
clog = ChangeLog(os.path.join(SCRIPT_DIR, "archimate_changelog.md"))
clog.checkpoint("Parsed MD")
```

- [ ] **Step 2: Add `.log()` calls inside element creation/update**

In the element loop (around `log(f"  [{i+1}/{len(elements)}] Created: ...")` and `log(f"  [{i+1}/{len(elements)}] Updated: ...")`):

```python
if guid_md:  # existing element → update
    ...
    clog.log("updated", elem_id, name, archi_type, ea_elem.ElementGUID,
             changes={"Notes": (old_notes, notes)} if old_notes != notes else None)
else:  # new element
    ...
    clog.log("created", elem_id, name, archi_type, new_elem.ElementGUID)
```

- [ ] **Step 3: Add `.log()` calls inside relationship creation**

In the relationship loop:

```python
if existing_guid:  # already exists
    clog.log("updated", rel_id, rel_type, rel_type, existing_guid)
else:  # newly created
    clog.log("created", rel_id, rel_type, rel_type, new_conn.ConnectorGUID,
             changes={"source": src_elem_id, "target": tgt_elem_id})
```

- [ ] **Step 4: Close changelog before `Done.`**

```python
clog.checkpoint("Diagram complete")
clog.close()
```

- [ ] **Step 5: Run smoke test**

Run: `python experiments/modelgen/generate_archimate.py`
Expected: No errors. `experiments/modelgen/archimate_changelog.md` exists.

- [ ] **Step 6: Commit**

```bash
git add experiments/modelgen/generate_archimate.py
git commit -m "feat: add changelog logging to ArchiMate generator"
```


### Task 4: Wire UML Data Model generator + sync

**Files:**
- Modify: `experiments/modelgen/generate_uml_datamodel.py`
- Modify: `experiments/modelgen/sync_datamodel_from_ea.py`

- [ ] **Step 1: Open changelog in `generate_uml_datamodel.py`**

After `Parsed N entities, M relationships`:

```python
from changelog import ChangeLog
clog = ChangeLog(os.path.join(SCRIPT_DIR, "uml_datamodel_changelog.md"))
clog.checkpoint("Parsed MD")
```

- [ ] **Step 2: Add `.log()` calls in entity loop**

Replace `print(f"  Created: '{name}'")` / `print(f"  Updated: '{name}'")`:

```python
clog.log("created", safe_id(name), name, "Class", new_elem.ElementGUID if new_elem else "")
clog.log("updated", safe_id(name), name, "Class", ea_elem.ElementGUID, changes=...)
```

- [ ] **Step 3: Add `.log()` for attribute add/delete**

In attribute sync section, replace `print(f"    Deleted attribute '{a.Name}'")`:

```python
clog.log("deleted", a.Name, a.Name, "Attribute", "", changes={"entity": name})
```

- [ ] **Step 4: Add `.log()` for connector create/delete**

```python
clog.log("created", "", "", rel_type, new_conn.ConnectorGUID,
         changes={"source": src_name, "target": tgt_name})
```

- [ ] **Step 5: Close changelog**

```python
clog.checkpoint("Diagram complete")
clog.close()
```

- [ ] **Step 6: Wire MD diff in `sync_datamodel_from_ea.py`**

This script writes a data model MD. Apply same `compute_md_diff` pattern as bpmn engine sync: read old MD, build new content in memory, diff, `clog.log_diff()`, write.

Add after the final lines-building:

```python
from changelog import ChangeLog
old_content = ""
md_path = args.md or r"M:\EAxCRM\models\EAxCRM-DataModel.md"
if os.path.exists(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        old_content = f.read()

new_content = "\n".join(lines) + "\n"
diff = compute_md_diff(old_content, new_content)  # can reuse from bpmn_engine or write inline

clog = ChangeLog(os.path.join(SCRIPT_DIR, "uml_datamodel_changelog.md"))
clog.log_diff(diff)
clog.close()
```

Use a lightweight inline regex-based diff for the data model MD format (entities have `### Entity—eid` headers, relationships have a dedicated section).

- [ ] **Step 7: Commit**

```bash
git add experiments/modelgen/generate_uml_datamodel.py experiments/modelgen/sync_datamodel_from_ea.py
git commit -m "feat: add changelog to UML Data Model generator and sync"
```


### Task 5: Wire Requirements generator + sync

**Files:**
- Modify: `experiments/modelgen/generate_requirements_from_md.py`
- Modify: `experiments/modelgen/sync_requirements_from_ea.py`

- [ ] **Step 1: Open changelog in `generate_requirements_from_md.py`**

After `Parsed N requirements from MD`:

```python
from changelog import ChangeLog
clog = ChangeLog(os.path.join(SCRIPT_DIR, "requirements_changelog.md"))
clog.checkpoint("Parsed MD")
```

- [ ] **Step 2: Add `.log()` in requirement loops**

Replace `print(f"  Updated CRM-{alias}  {name}")` and `print(f"  Created CRM-{alias}  {name}  [{guid}]")`:

```python
clog.log("updated", f"CRM-{alias}", name, "Requirement", guid, changes=...)
clog.log("created", f"CRM-{alias}", name, "Requirement", guid)
clog.log("deleted", req_id, name, "Requirement")  # if orphan cleanup removes any
```

- [ ] **Step 3: Add `.log()` for connector/realisation changes**

```python
clog.log("created", "", "", "Realisation", guid,
         changes={"source": entity_name, "target": f"CRM-{alias}"})
```

- [ ] **Step 4: Close changelog**

```python
clog.close()
```

- [ ] **Step 5: Wire sync via MD diff**

Same `compute_md_diff` pattern in `sync_requirements_from_ea.py`.

- [ ] **Step 6: Commit**

```bash
git add experiments/modelgen/generate_requirements_from_md.py experiments/modelgen/sync_requirements_from_ea.py
git commit -m "feat: add changelog to Requirements generator and sync"
```


### Task 6: Add checkpoints for hang diagnostics across all scripts

**Files:**
- Modify: `experiments/modelgen/generate_archimate.py`
- Modify: `experiments/modelgen/generate_uml_datamodel.py`
- Modify: `experiments/modelgen/generate_requirements_from_md.py`
- Modify: `experiments/modelgen/bpmn_engine.py`
- Modify: `experiments/modelgen/ea_session.py`

- [ ] **Step 1: Add checkpoint calls at each major phase boundary in each script**

Checkpoint locations:

| Script | Checkpoints |
|--------|-------------|
| `generate_archimate.py` | After "Parsed MD", before element loop, after element loop ("Elements complete"), before relation loop, after relation loop, before diagram phase, after diagram |
| `generate_uml_datamodel.py` | After parsing, before entities, after entities, before relationships, after relationships, before diagram, after diagram |
| `generate_requirements_from_md.py` | After parsing, before requirements, after requirements, before connectors, after connectors, before diagram, after diagram |
| `bpmn_engine.generate()` | After "Parsed MD", before element creation, after element creation ("Elements complete"), before connector creation, after connector creation, before diagram, after diagram |
| `bpmn_engine.sync_to_md()` | After "Parsed MD", before element write, after element write, before connector write, after connector write |

Example pattern:

```python
clog.checkpoint("Elements complete")
clog.checkpoint("Relationships complete")
clog.checkpoint("Diagram complete")
```

- [ ] **Step 2: Run all generators to verify no regressions**

Run each of:
```bash
python experiments/modelgen/generate_sales_process_from_md.py
python experiments/modelgen/generate_archimate.py
python experiments/modelgen/generate_uml_datamodel.py
python experiments/modelgen/generate_requirements_from_md.py
```

Expected: All succeed. Changelog files exist in `experiments/modelgen/` with checkpoint entries.

- [ ] **Step 3: Commit**

```bash
git add experiments/modelgen/
git commit -m "feat: add checkpoint logging for hang diagnostics"
```
