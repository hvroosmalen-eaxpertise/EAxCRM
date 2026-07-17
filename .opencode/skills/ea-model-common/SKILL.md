---
name: ea-model-common
description: Shared EA COM API infrastructure for all EAxCRM diagram-generator skills — coordinate system, GUID map idempotency, COM session lifecycle, Sandbox isolation protocol, and diagram-type/toolbox fundamentals. Referenced by ea-bpmn-creator, ea-archimate-creator, ea-ldm-creator, ea-pdm-creator, ea-requirements-creator, and ea-wireframe-creator; read this first regardless of which modeling language you're working in.
---

# EA Model Common (EAxCRM Project Skill)

## Overview

This skill holds the infrastructure shared by every EAxCRM diagram generator, split out of the single `ea-diagram-creator` skill (github issue #4) once a genuinely different modeling language (Wireframe) needed its own patterns without dragging BPMN/ArchiMate specifics along. Language-specific skills (`ea-bpmn-creator`, `ea-archimate-creator`, `ea-ldm-creator`, `ea-pdm-creator`, `ea-requirements-creator`, `ea-wireframe-creator`) reference this one for the parts below rather than repeating them.

All generator scripts are under **`modelgen/`**, and the shared layout utilities are in **`modelgen/diagram_utils.py`**. See each language skill for its own generator script and `docs/superpowers/specs/` for design history.

## Rich-Text Notes: `Element.Notes` Does Not Interpret RTF/HTML Directly

**Rule:** any Element/Requirement/Connector Notes field that needs bold/italic/lists must go through `Repository.GetFieldFromFormat("RTF", <rtf-doc>)`. Direct assignment (`elem.Notes = "\\b Why:\\b0 …"` or `elem.Notes = "<b>Why:</b> …"`) is stored as literal characters — EA's Notes pane will display the raw `\b` control codes or `<b>` tags, not render them (verified 2026-07-07 while adding bold headers + numbered test cases to Requirements Notes, and re-verified 2026-07-09 after the same lesson was accidentally re-learned in the BPMN Activity Why/What/How/Context rollout).

**Working pattern:**

```python
def rtf_escape(text):
    # RTF specials: \\ { } ; non-ASCII becomes \\uNNNN? ; \\n becomes \\par
    ...

rtf = r"{\\rtf1\\ansi\\deff0 " + <body-with-\\b markers> + "}"
elem.Notes = repo.GetFieldFromFormat("RTF", rtf)
elem.Update()
```

Full worked implementations:
- Requirements: `modelgen/generate_requirements_from_md.py::build_notes` (Description + bold Rationale/Test Cases headers + hanging-indent numbered list).
- BPMN elements: `modelgen/bpmn_engine.py::set_element_notes` + `_md_bold_to_rtf` (converts markdown `**bold**` spans in a description to `\\b...\\b0`; every bold span after the first also gets a preceding `\\par` so successive labeled sections like Why/What/How/Context each start on their own line rather than flowing into one paragraph; falls back to plain assignment when no `**` is present).

**Convention when writing Notes in a new generator:** if the target field authoring style uses `**...**`, route it through the bpmn_engine helper (or copy the pattern). If it uses markdown headings/lists, extend the helper — do not go back to plain `.Notes = ...`.

## EA Coordinate System

### Rules

1. **Origin (0,0) is at the top-left** of the diagram canvas
2. **X increases to the right** (standard)
3. **Y is ALWAYS negative below origin** — the origin row is the topmost visible row
4. **RectTop > RectBottom** because a value closer to zero is higher on the page (e.g., `top=-30`, `bottom=-200`: `-30 > -200`)
5. **Height = |top - bottom|** (e.g., `|-30 - (-200)| = 170`)

### Assignment Pattern (see `diagram_utils.py:80-82`)

```python
# Layout functions return (left, visual_top, right, visual_bottom)
# visual_top < visual_bottom (positive Y down)
# At COM API time, negate Y:
dobj.left = l
dobj.top = -vt      # EA: Y is always negative below origin
dobj.Update()
```

## GUID Map Pattern for Idempotency

Each generator has its own GUID map file:

| Generator | GUID Map File |
|-----------|---------------|
| `generate_archimate.py` | `modelgen/archimate_guid_map.json` |
| `generate_ldm_from_md.py` | `modelgen/ldm_guid_map.json` |
| Customer Account (`bpmn_config.CUSTOMER_ACCOUNT`) | `modelgen/customeraccount_guid_map.json` |
| Sales (`bpmn_config.SALES`) | `modelgen/sales_guid_map.json` |
| Newsletter (`bpmn_config.NEWSLETTER`) | `modelgen/newsletter_guid_map.json` |
| `generate_requirements_from_md.py` | `modelgen/requirements_guid_map.json` |
| Manage Customer Account UI (`wireframe_config.CUSTOMER_ACCOUNT_UI`) | `modelgen/customeraccount_ui_guid_map.json` |

### Save/Load Pattern

```python
GUID_MAP_PATH = "modelgen/<name>_guid_map.json"

guid_map = {}
if os.path.exists(GUID_MAP_PATH):
    with open(GUID_MAP_PATH) as f:
        guid_map = json.load(f)

# Check before creating
if eid in guid_map:
    elem = repo.GetElementByGuid(guid_map[eid])
    if elem is not None:
        elem.Name = data["name"]
        elem.Update()
        continue

# Create new element
new_elem = proc_arch.Elements.AddNew(...)
guid_map[eid] = new_elem.ElementGUID

# Save after creation pass
with open(GUID_MAP_PATH, "w") as f:
    json.dump(guid_map, f, indent=2)
```

## Refresh() Stale-Proxy / Containment Bug

When you create an element with `ParentID` set (moving it under a Lane, or a Screen for wireframes), it **disappears from the `Package.Elements` collection** after `Update()` — it only shows up under its parent's own child `.Elements` collection from then on. This bites both creation-time proxy staleness and later read-back:

**Always capture ElementGUID and ElementID BEFORE calling Refresh()** on the batch you just created:

```python
element_guid = new_elem.ElementGUID
element_id = new_elem.ElementID
proc_arch.Elements.Refresh()
# After Refresh(), use repo.GetElementByGuid(guid) to get a fresh proxy
```

**When reading a parented hierarchy back** (sync direction), don't assume a flat scan of the owning package's `.Elements` will find everything — it will only find the top-level (unparented) elements. Recurse into each parent's own `.Elements` collection to find its children:

```python
# WRONG: misses every parented child entirely, no error raised
for i in range(pkg.Elements.Count):
    elem = pkg.Elements.GetAt(i)
    ...

# RIGHT: find parents first, then recurse into each one's own children
for parent_elem in top_level_parents:
    parent_elem.Elements.Refresh()
    for j in range(parent_elem.Elements.Count):
        child = parent_elem.Elements.GetAt(j)
        ...
```

This exact bug was found twice independently — once for BPMN Lane children, once for wireframe Screen/Control children — because the sync-direction code only scanned the flat package list. Confirmed it silently drops content rather than erroring, so a sync bug like this can go unnoticed until someone counts elements.

## Sparx COM `Update()` Quirks

### Setting `Connector.Type` and `StereotypeEx` in the same `Update()` drops the stereotype (2026-07-14)

Verified while retyping ArchiMate connectors from `Association` to `Dependency`/`ControlFlow`. Setting both properties on the same COM proxy before a single `Update()` persists the Type change but silently clears `StereotypeEx` (reads back as `''`). Retype-only calls (no stereotype touched) preserve the existing stereotype; adopt-only calls (no type change) work fine. It's the combination that breaks.

Fix — two `Update()` calls with a fresh proxy in between:

```python
conn.Type = new_type
conn.Update()
conn = repo.GetConnectorByGuid(conn.ConnectorGUID)  # fresh proxy
conn.StereotypeEx = new_stereo
conn.Update()
```

See `dedup_archimate_connectors.py:apply_plan` for the working pattern.

### Setting `Connector.Type` normalizes the stereotype to short form on read

Independent of the above — after a successful Type change, the same connector's `StereotypeEx` reads back as e.g. `"ArchiMate_Serving"` (short form) even if it was written as `"ArchiMate3::ArchiMate_Serving"`. Any code comparing stereotype strings must normalize to short form on both sides. See `generate_archimate._normalize_stereotype()`.

### `AddNew(_, "Composition")` silently normalizes to `Aggregation`

Reported downstream (issue #17 follow-up comment). When creating a Composition, `t_connector.Connector_Type` will be `"Aggregation"` regardless of what you passed. In EAxCRM we sidestep this by using `Association` as the base type for both Composition and Aggregation and letting the MDG stereotype (`ArchiMate3::ArchiMate_Composition`) drive the filled-diamond glyph — see `ea-archimate-creator`'s connector table.

### `Connector.TaggedValues.AddNew()` before `Update()` lands the tag orphaned with `ElementID = 0` (issue #17 #6, 2026-07-16)

`Connectors.AddNew(...).TaggedValues.AddNew("SomeProp", "value")` called BEFORE the connector's first `Update()` writes the tag row into `t_connectortag` with `ElementID = 0` -- orphaned, invisible to `Connector.TaggedValues` on subsequent reads, and impossible to look up by connector id later. Silent failure: no exception, tag exists in the table, but no connector owns it.

Fix -- always `Update()` the connector first (so it has a real `ConnectorID`), then set the tag:

```python
new_conn = src_elem.Connectors.AddNew("", "Dependency")
new_conn.SupplierID = tgt_elem.ElementID
new_conn.StereotypeEx = "ArchiMate3::ArchiMate_Access"
new_conn.Direction = "Bi-Directional"
new_conn.Update()          # commits the connector; ConnectorID is now real
set_connector_tag(new_conn, "AccessMode", "Read/Write")   # safe: post-Update
```

`generate_archimate.set_connector_tag(conn, prop, value)` enforces the order and raises `RuntimeError` if called on a connector with `ConnectorID == 0`. Use it -- don't roll your own `TaggedValues.AddNew()`. The same helper is idempotent (updates in place if the property already has a tag).

Same trap applies conceptually to `Element.TaggedValues` if you ever `AddNew` an element and try to tag it before its own `Update()`, but that's less commonly needed since element creation is usually followed by immediate `Update()` for other reasons.

## Diagram Object Management

### Deleting Existing Objects Before Re-Place

Iterate in reverse (deletions shift indices):

```python
for i in range(diag.DiagramObjects.Count - 1, -1, -1):
    dobj = diag.DiagramObjects.GetAt(i)
    elem_id = dobj.ElementID
    if elem_id in lane_element_ids:
        continue  # Don't delete lanes
    diag.DiagramObjects.Delete(i + 1)  # 1-indexed!
```

Note: `DiagramObjects.Delete()` is **1-indexed**. `Package.Packages.Delete()` is **0-indexed** (confirmed empirically while cleaning up a Sandbox test package — passing `i + 1` there raised "Index out of bounds"). Don't assume every `.Delete(index)` in the API uses the same convention; check empirically or by an existing working call site for that specific collection.

### Connector Rendering (DiagramLink)

Applies to all diagram types. Set on every `DiagramLink` after placing diagram objects:

```python
diag.DiagramLinks.Refresh()
for i in range(diag.DiagramLinks.Count):
    dl = diag.DiagramLinks.GetAt(i)
    dl.LineStyle = 9  # Orthogonal Rounded
    dl.Update()
```

**`LineStyle` enum values:**

| Value | Style |
|-------|-------|
| 1 | Direct |
| 2 | Auto Routing |
| 3 | Custom Line |
| 4 | Tree Vertical |
| 5 | **Tree Horizontal** (not Orthogonal Rounded — common mistake) |
| 6 | Lateral Vertical |
| 7 | Lateral Horizontal |
| 8 | Orthogonal Square |
| 9 | **Orthogonal Rounded** |

**CAUTION:** `LineStyle = 5` is Tree Horizontal, not Orthogonal Rounded. Always use `9` for Orthogonal Rounded (see each language skill's own quick-reference table for which value that language actually uses).

Use `diagram_utils.set_diagram_link_style(diag, line_style)` — idempotent, safe to call every run, only touches connectors whose `LineStyle` doesn't already match.

## Diagram Type and Toolbox (github issue #5 — CRITICAL, read before creating any new diagram type)

### HARD RULE: no `sqlite3` in generate/sync code -- reads or writes, use `Repository.SQLQuery` for SQL-shaped reads (2026-07-06, strengthened 2026-07-16)

**The shipped `generate()`/`sync_to_md()` code path (and any other production generator/sync logic) must never contain direct `sqlite3.connect(qea_path)` access to the `.qea` file — reads or writes, no exceptions, however tempting the shortcut looks.** The `.qea` SQLite file is only one supported EA repository backend; EA also runs on SQL Server, MySQL, Oracle, and Postgres, and this project is expected to move off SQLite as its EA backend at some point. Any code that directly opens the file with `sqlite3.connect()` breaks silently on that migration. The rule was previously framed as "bypasses EA's constraints" (write-side rationale); it now also covers reads for backend portability.

**Two correct primitives, pick the right shape for the task:**

1. **COM iteration** — `pkg.Elements.GetAt(i)`, `elem.Connectors.GetAt(i)`, `parent.Packages.GetAt(i)`, etc. Best for walking a small tree of related objects when you'll use most of each object's properties. Used by `sync_requirements_from_ea.py` and `wireframe_engine.sync_to_md()`.

2. **`Repository.SQLQuery(sql)` via the `ea_session.sql_rows(repo, sql)` helper** — best for bulk reads where SQL's WHERE/JOIN/ORDER is a natural fit and you'd otherwise iterate every element in a package just to filter it. Routes through EA's own DB abstraction, so the same call works whether the backend is SQLite, SQL Server, Postgres, etc. — backend-agnostic by construction. The helper parses EA's XML result into a list of `{column_name: text}` dicts.

**Working pattern (empirically verified 2026-07-16):**

```python
import ea_session

with ea_session.ea_repository(QEA, technology="ArchiMate3") as repo:
    rows = ea_session.sql_rows(repo, """
        SELECT Object_ID, Name, Object_Type, Stereotype, IFNULL(Note,'') AS Note, ea_guid
        FROM t_object
        WHERE Package_ID = 42 AND Object_Type = 'Class'
        ORDER BY Name
    """)
    for r in rows:
        print(r["Name"], r["ea_guid"])   # values are always strings
```

**Return shape** (from `repo.SQLQuery` before helper parses it):

```xml
<?xml version="1.0" encoding="UTF-16" standalone="no" ?>
<EADATA version="1.0" exporter="Enterprise Architect">
  <Dataset_0><Data>
    <Row><Package_ID>2</Package_ID><Name>Application Architecture</Name></Row>
    <Row><Package_ID>3</Package_ID><Name>Data Architecture</Name></Row>
  </Data></Dataset_0>
</EADATA>
```

**Silent-failure trap — verified: bad SQL does NOT raise.** A query against a non-existent table, a syntax error, or a mistyped column returns *the same empty `<EADATA>`* as a legitimate zero-row result. The `sql_rows()` helper returns `[]` in both cases with no way for the caller to distinguish. Consequence:

- Never trust an unexpectedly-empty result set. If a query MUST return rows (e.g. "find the ArchiMate package"), validate the SQL against a known-good schema first, or assert `len(rows) > 0` and fail loud.
- Prefer wide-scope queries (`SELECT ... FROM t_object WHERE Package_ID IN (...)`) over per-element queries in a loop — a typo in a per-element query silently produces "no attributes for any element" instead of failing fast.

**Portable-SQL discipline:** `LIMIT N` works today because the backend is SQLite, but is not portable to SQL Server (`TOP N`) or Oracle (`FETCH FIRST N`). Avoid backend-specific syntax in shipped queries. When you need "top N" for exploration, do it in Python after fetching, or accept the query is scratchpad-only. Standard SQL that works across all supported EA backends (`SELECT`, `WHERE`, `JOIN`, `ORDER BY`, `IFNULL`/`COALESCE`, `IN`) is the safe subset.

**Clarified distinction: ad-hoc `sqlite3` queries for investigation/diagnosis are fine.** Exploring `t_diagram`, `t_xref`, element nesting, etc. via a one-off scratch script — exactly how the `MDGDgm` mechanism was discovered — is a legitimate and encouraged empirical-verification technique (see "Use a Sandbox Package"). The rule is specifically about what ships in `wireframe_engine.py`/`bpmn_engine.py`/`generate_archimate.py`/`sync_ldm_from_ea.py`/`sync_archimate_from_ea.py` etc. Investigate with `sqlite3` all you want in a scratchpad script; never commit that query into the generator/sync code itself.

**Known offenders as of 2026-07-16** (follow-up debt, not patterns to copy):
- `bpmn_engine.sync_to_md()` at `bpmn_engine.py:1653` — copied the sqlite3 shape from sync_ldm_from_ea.py during the BPMN engine refactor (2026-07-05, commit 0f16da4).
- `sync_ldm_from_ea.py:47` — the very first sync script in the repo (2026-06-24, commit 045ed3a), written before this rule was formalized. Retrofit to `ea_session.sql_rows` planned as part of the #17 #7 push.

See "Living With COM-Only Constraints" below for what this means in practice for the Diagram_Type/StyleEx case specifically.

### Background: what the toolbox mechanism actually is

Every diagram generator originally created diagrams with an invalid native `Diagram_Type` string — one that *looks* plausible (a stereotype's human-readable alias) but isn't real. ArchiMate used `"Application Layer"` (the alias of the `Application` stereotype, not a `Diagram_Type` — the real type is `"Logical"`); BPMN used `"BusinessProcess"` (not real either — the real type is `"Analysis"`). Confirmed by reading the installed `MDGTechnologies/*.xml` technology definitions directly (`<Apply type="Diagram_Logical">` / `<Apply type="Diagram_Analysis">` / `<Apply type="Diagram_Custom">`) rather than guessing.

**Fixing the Type alone was not enough.** A first attempt also set `Diagram.StereotypeEx` + a `t_xref` "Stereotypes"/"diagram property" row (an existing, working BPMN pattern) but the toolbox *still* didn't show. The actual mechanism, found by reading a diagram the user built correctly by hand in EA's own GUI: **`Diagram.StyleEx`'s `MDGDgm=<Technology>::<Name>;` key** — not `Stereotype`/`StereotypeEx` (both blank on the working reference) and not any `t_xref` row (none present).

**Lesson confirmed twice: a reference diagram proves the *mechanism* (which field/key EA reads), not necessarily the *value* to copy onto a semantically-different diagram.** The hand-built BPMN reference was a generic scratch diagram typed `MDGDgm=BPMN2.0::Business Process;`; copying that exact value onto the real Customer Account/Sales/Newsletter diagrams was itself a bug — those are rooted in a `CollaborationModel` element with Pools/Lanes, so their own value must be `BPMN2.0::Collaboration` to match what they actually represent. Match the value to the diagram's own underlying element/stereotype, don't copy verbatim from whatever reference happened to confirm the mechanism.

### Living With COM-Only Constraints

`Diagram.Type` is read-only via COM once a diagram already exists (raises "can not be set"), and `Diagram.StyleEx`'s `MDGDgm` entry silently accepts a COM write but won't persist it if the key already holds *any* value, even blank. Both **can** be set correctly via plain COM on a **brand-new diagram, at creation time, before anything else touches it**:

```python
diag = elem.Diagrams.AddNew(name, DIAGRAM_NATIVE_TYPE)  # correct Type from the start
diag.Stereotype = ""
diag.StereotypeEx = ""
diag.StyleEx = "MDGDgm=<Technology>::<Name>;"  # blank field, COM write persists
diag.Update()
```

This covers the normal case: every diagram this project creates going forward starts out right, because the generator scripts always create with the correct `DIAGRAM_NATIVE_TYPE` and set `StyleEx` immediately, before it's ever committed with a wrong value.

**What COM genuinely cannot do:** correct an *existing* diagram whose `Diagram_Type` or `StyleEx` MDGDgm is already wrong (e.g. from an older buggy run, or if someone changes it by hand in EA to something incorrect). There is no COM-only fix for that specific situation. Do not reach for SQL here. Instead:
- Detect and report it (log a clear message naming the diagram and what's wrong), and
- Ask the user to correct it manually in EA's GUI (or, with explicit approval, recreate the diagram via COM from scratch — carrying over its existing `DiagramObjects`' positions read before deletion — since a full recreate is a destructive-enough action to need sign-off, unlike setting properties on first creation).

Can't verify toolbox rendering directly either way — only diagram *content* is exportable via `SaveDiagramImageToFile`, not IDE chrome. **Always get explicit user confirmation of the actual toolbox** before considering a diagram-type fix done for a new modeling language; treat MDG-technology-XML-derived values as a good first guess, not a verified fact, until the user confirms in their own EA session (see each language skill's own Diagram Type section for current verification status).

## Design Phase Before First-Run Layout

**Before placing a single element on a diagram for the first time, go through a deliberate design phase** rather than placing elements in MD-declaration (id) order, which produces a diagonal staircase with no semantic grouping, arbitrary connector crossings, and no visual hierarchy.

1. **Analyze element types and relationships** — group into core/related/peripheral, or by architectural layer, before computing any positions.
2. **Define layout zones** — partition the canvas (e.g. top-left/top-right/center/bottom-left/bottom-right for a data model; Business/Application/Technology bands for ArchiMate).
3. **Compute positions per zone**, then combine — each zone gets its own sub-layout (grid or flow), not one global formula.

See each language skill for its own layout algorithm (BPMN's flow layout, the shared non-BPMN grid, wireframe's explicit bounds).

## Use a Sandbox Package for Calibration/Testing

Never test new layout/sizing/style logic directly against a real diagram — the user has manually adjusted layouts there that must be preserved. Instead, create/reuse a `Sandbox` package directly under the root Model package (same level as `Application Architecture`, `Data Architecture`, etc.), with its own sub-packages, diagrams, and — critically — its **own separate GUID map file** so sandbox runs can never collide with a real generator's map.

### CRITICAL: a different target package is NOT sufficient isolation

**Incident, 2026-07-03 (BPMN engine refactor):** a "sandbox" dry-run targeting `parent_package_name="Sandbox"` still repositioned every element on the **real**, live, manually-tuned Customer Account diagram — because `repo.GetElementByGuid()` resolves **repo-wide**, ignoring which package the calling code thinks it's targeting. Any MD file previously synced out of the live model embeds real element GUIDs in its `- GUID:` fields — so re-running a generator against that MD, even with a different `parent_package_name`, finds and updates the real elements wherever they actually live, silently.

**A separate sandbox GUID map file is necessary but NOT sufficient.** It only prevents the sandbox script's own re-run tracking from colliding with a real generator's map — it does nothing to stop the MD's embedded `- GUID:` fields from matching real elements on the very first sandbox run.

**For genuine isolation, do one of:**
- Strip all `- GUID:` (and `- Diagram GUID:`) fields from a **temp copy** of the source MD before feeding it to the sandbox script:
  ```python
  import re
  text = open(real_md_path, encoding="utf-8").read()
  stripped = re.sub(r"^- (GUID|Diagram GUID): .*\n", "", text, flags=re.MULTILINE)
  open(temp_md_path, "w", encoding="utf-8").write(stripped)
  ```
- Or use synthetic/fabricated test data that never had real GUIDs to begin with. If the MD has never been synced even once yet (a brand-new flow being authored for the first time), it has no embedded GUIDs at all and this step isn't needed — confirmed safe for the wireframe generator's first Sandbox test.

**Also:** any code that repositions already-placed diagram objects (reflow/relayout on re-run) must clear/recompute the connector `DiagramLink.Path` for links whose endpoints moved — `Path` holds absolute waypoint coordinates computed for the *old* positions, and EA does not recompute it automatically when a box moves via COM.

### Visual self-verification via `SaveDiagramImageToFile`

You don't have to rely on the user checking every layout iteration in EA's GUI:

```python
with ea_session.ea_repository(qea_path) as repo:
    diag = repo.GetDiagramByGuid(diagram_guid)   # or GetDiagramByID
    repo.OpenDiagram(diag.DiagramID)             # must be open first
    proj = repo.GetProjectInterface()
    proj.SaveDiagramImageToFile(r"C:\path\to\out.png")   # 2-arg form errors;
                                                          # only takes the path
    repo.CloseDiagram(diag.DiagramID)
```
Then `Read` the PNG directly. Reserve asking the user to look for final confirmation once you're already confident, not for every intermediate trial. Note this only exports diagram *content*, never the IDE's toolbox panel — see "Diagram Type and Toolbox" above.

## Platform-Specific Gotchas

### Python 64-bit + EA 32-bit COM Bridge

Use the shared `modelgen/ea_session.py` module instead of hand-rolling a COM connection:

```python
import ea_session
with ea_session.ea_repository(qea_path, technology="ArchiMate3") as repo:
    root = ea_session.get_model_root(repo)  # retries on transient 61704 errors
    ...
```

- `ea_session.ea_repository()` uses `win32com.client.DispatchEx("EA.App")` + `.Repository` — **`DispatchEx`, not plain `Dispatch`**. Plain `Dispatch` can attach to an EA automation server already registered in COM's Running Object Table (e.g. the user's own open EA instance) instead of spawning an isolated one — confirmed to be the cause of EA's "Internal application error 61704" on `repo.Models.GetAt(0)`.
- `ea_session.get_model_root(repo)` retries `repo.Models.GetAt(0)` up to 5 times (2s apart) — this call has been observed to transiently fail right after `OpenFile`/`ActivateTechnology`.
- The context manager handles `RefreshModelView`/`RefreshOpenDiagrams`, `CloseFile`, and zombie cleanup automatically on exit — no need to repeat any of that per-script.
- The `technology=` argument accepts any MDG technology name (`"ArchiMate3"`, `"BPMN2.0"`, `"Wireframing"`, ...) — it's a generic `Repository.ActivateTechnology()` call, not hardcoded per language.

### Zombie EA Process Cleanup (MANDATORY)

EA zombie processes accumulate after every generator run. If left unchecked, they lock the `.qea` file, preventing EA from starting.

`ea_session.ea_repository()` handles this automatically: it snapshots `ea_session.get_ea_pids()` before spawning its own EA instance, and on exit calls `ea_session.kill_new_ea_processes(before_pids)` — which only kills PIDs that appeared *after* the snapshot, so a pre-existing EA instance (the user's own open session) is never touched, by construction. **Never** manually run `Get-Process -Name EA | Stop-Process -Force` — that has no way to distinguish the user's real session from a zombie. If you suspect a genuine leaked zombie (rare — e.g. a script crashed before reaching the `finally` block), confirm the PID's start time lines up with the crashed run before asking the user for permission to kill it.

## Elements Reused Across Diagrams and Packages

An EA element can legitimately appear on multiple diagrams — that's the whole point of a repository-backed model rather than a drawing tool: one underlying `Element` (one GUID, one set of Notes/tagged values) can be dropped onto any number of `Diagrams` as separate `DiagramObject` placements, each with its own position. Seeing the "same" element rendered on two different diagrams is normal and expected, not a modeling defect.

Likewise, an element's **owning package** (where it lives in the Project Browser tree) is independent of which diagram(s) render it — an element parented under one package can still be placed on a diagram that itself lives under a completely different package. Don't assume an element must be re-parented to appear on a given diagram.

**This is distinct from** two independently-created elements that merely share a name/description but have different GUIDs — that's real duplication, not reuse, and still worth flagging if found, since nothing in the model actually ties the two together (no shared GUID, no relationship between them).

## Element/Diagram Description Convention

Every element and diagram description (`Notes` field, synced from/to the MD's `- Description:` line) should be elaborate enough to independently answer, at minimum:

- **Why** does this exist / why is it relevant to the model?
- **What** is it, in plain terms?
- **How** does it work, if that's non-obvious (algorithm, trigger, manual vs. automated step)?
- **In what context** does it sit (which process/layer/diagram, what it connects to)?

A one-line restatement of the element's name is not sufficient. Apply this when authoring new elements/diagrams and when substantially revising existing ones — it does not require a blanket retrofit of every existing description in one pass.

## Checking Your Work

After placing diagram objects, verify coordinate correctness:

1. Every object should have negative `top` and `bottom` values
2. `top > bottom` for every object (e.g., `-30 > -200`)
3. `right > left` and `bottom < top` (both negative, `top > bottom`) — all four bounds are set per type
4. Elements are grouped semantically (related elements near each other)
5. Manual verification: open diagram in EA and check visual layout, and confirm the toolbox shows the expected shapes by default (see "Diagram Type and Toolbox" above)

## Shared Source Files

| File | Purpose |
|------|---------|
| `modelgen/ea_session.py` | Shared EA COM session lifecycle — isolated `DispatchEx` instance, `Models.GetAt(0)` retry, automatic zombie cleanup, and `sql_rows(repo, sql)` — the ONLY correct way to run SQL-shaped reads (routes through `Repository.SQLQuery`, backend-agnostic; see "HARD RULE"). Used by every generator/sync script |
| `modelgen/diagram_utils.py` | Shared **non-BPMN** layout functions — grid layout (`compute_grid_positions`), UML class sizing (`compute_uml_class_width/height`), connector line-style (`set_diagram_link_style`), `create_diagram_objects`/`add_missing_elements`/`get_placed_ids` (reused by the wireframe engine too) |
| `modelgen/changelog.py` | Shared audit-logging (`ChangeLog` class + `compute_md_diff()`) used by every generator/sync script — see the per-language skill for what it logs |
