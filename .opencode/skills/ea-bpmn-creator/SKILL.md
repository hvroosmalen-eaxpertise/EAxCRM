---
name: ea-bpmn-creator
description: Reference for generating/syncing BPMN 2.0 process diagrams (Sales, Newsletter, Manage Customer Account) in EAxCRM via the shared bpmn_config.py/bpmn_engine.py — Collaboration/Lane/Pool structure, flow-aware layout algorithm, connector routing, and the BPMN diagram-type/toolbox fix. Read ea-model-common first for shared COM/session/GUID-map/Sandbox patterns.
---

# EA BPMN Creator (EAxCRM Project Skill)

## Overview

Covers the 3 BPMN 2.0 process diagrams: Sales, Newsletter, and Manage Customer Account. **Read `ea-model-common` first** for the coordinate system, GUID map pattern, COM session lifecycle, Sandbox isolation protocol, and the general diagram-type/toolbox mechanism — this skill only covers what's BPMN-specific.

**BPMN engine (2026-07-05, issue #3):** the 3 BPMN generate scripts and their matching `sync_*_process_from_ea.py` scripts are thin config + CLI wrappers (~15 lines each) around a shared `experiments/modelgen/bpmn_config.py` (per-process `ProcessConfig` dataclass instances + shared BPMN vocabulary constants) and `experiments/modelgen/bpmn_engine.py` (`parse_md`, `generate`, `sync_to_md`, and the BPMN-only layout functions). See `docs/superpowers/specs/2026-07-03-bpmn-config-driven-engine-design.md` for the design.

## Activity Description Convention (Why / What / How / Context)

**Applies to `Activity` stereotypes only** — not events, not gateways, not data objects. Events/gateways stay short; their descriptions rarely benefit from the four-part shape.

Every BPMN Activity's `Description` is one paragraph structured as:

> **Why:** <the motivation — the pain, missing capability, or requirement this activity addresses; cite CRM-/SAL-/NWS-/DEL-/PRO- requirement IDs when relevant>. **What:** <what the activity actually produces or changes — the artifact/state transition, not the UI>. **How:** <the mechanics — inputs, systems touched, outputs, dedup/idempotency rules, defaults>. **Context:** <where this activity sits in the flow — upstream trigger, downstream feeds, references to sibling activities/screens, distinctions from lookalike activities>.

Rules:
- Sentence-cased inline labels: `**Why:** X. **What:** Y. **How:** Z. **Context:** W.` — not markdown sub-headings, not YAML.
- All four labels present, in that order, even if a field is one sentence.
- One paragraph, no bullets — bullets fragment the reasoning chain and read worse in EA's Notes pane.
- Refer to requirements by ID (`CRM-6`, `SAL-4`) not by full name; refer to sibling elements by their Activity/Gateway/Screen name, not GUID.

Example (from `EAxCRM-CustomerAccountProcess.md`, `Suggest Newsletter Opt-in`):

> **Why:** Primary and License Holder are the two roles most likely to be the right person to ask about newsletter consent; prompting only these avoids pestering every Contact, while requiring an explicit confirmation (rather than the gateway match itself setting opt_in) keeps consent affirmative and auditable rather than inferred (CRM-16, CRM-11). **What:** a suggested opt-in for the account's Contact, with opt_in and opt_in_date only written on explicit Confirm. **How:** OptInScreen shows the eligible Contact with a message and Confirm/Decline buttons; Confirm sets Contact.opt_in=True and stamps opt_in_date, Decline leaves both untouched — either way the process ends at Account Ready. **Context:** reached only when the "Primary or License Holder role?" gateway resolves positive after Retrieve Customer Email History; the ongoing opt-in bookkeeping thereafter belongs to Newsletter Management's Manage Opt-in process, not this one.

Lint (informal): a hand-authored Activity description that does not contain all four labels `Why:`, `What:`, `How:`, `Context:` is non-conformant. When adding a new Activity to any BPMN MD, populate the template even if some fields are terse — an empty Why or How usually means the activity itself is under-specified.

**Rendering:** the `**bold**` markdown spans on `Why:`/`What:`/`How:`/`Context:` are converted to RTF at generate time by `bpmn_engine.set_element_notes`; EA's Notes pane shows each label in **bold** and — because `_md_bold_to_rtf` emits a `\par` break before every bold span after the first — each label starts on its own line. So although the MD source is one inline paragraph, EA renders it as four visually separated sections. Do NOT skip the conversion by setting `elem.Notes` directly — the raw asterisks will show literally, and the labels will run into one wall of text. See `ea-model-common`'s "Rich-Text Notes" section for the shared rule.

## Known BPMN-Specific Failure Modes

| Failure | Symptom | Root Cause |
|---------|---------|------------|
| **Flat hierarchy** | Elements under Package, not Lane | Created elements under the Process Architecture package instead of under Lane elements. |
| **Diagram under Package** | Wrong tree structure | Created diagram under `Package.Diagrams.AddNew()` instead of `CollaborationModel.Diagrams.AddNew()`. |
| **Only one stereotype form checked** | Connector not matched | Checked only short-form stereotype (`SequenceFlow`) without also checking long form (`BPMN2.0::SequenceFlow`). |
| **Orphaned DiagramLink after deleting a connector** | `repo.GetConnectorByID(dl.ConnectorID)` throws EA's internal error 61704 (not transient) while iterating `diag.DiagramLinks` | Deleting a connector via `Element.Connectors.Delete(index)` does not clean up `t_diagramlinks` rows on diagrams where that connector was rendered. `diag.DiagramLinks.Delete(index)` also fails (its own delete path needs to resolve the same dangling connector). **Do not SQL-delete the orphaned row** (an earlier version of this note suggested `DELETE FROM t_diagramlinks WHERE ...` directly — no longer allowed, see `ea-model-common`'s hard rule). Current handling: `bpmn_engine.py`'s linestyle/routing loop wraps `GetConnectorByID` in try/except and skips gracefully instead of aborting the whole pass, accepting the stray row as a known, harmless leftover rather than cleaning it up. If a genuine COM-only cleanup path is found later, prefer it; otherwise this is an accepted cosmetic wart, not something to SQL-patch. |

## BPMN Diagram Type and Toolbox (corrected 2026-07-06)

See `ea-model-common`'s "Diagram Type and Toolbox" for the full mechanism/history. For BPMN specifically: native `Diagram_Type` is `"Analysis"` (NOT `"BusinessProcess"`, which isn't a real type), and `StyleEx`'s `MDGDgm` value must match what the diagram's root `CollaborationModel` element represents — all 3 real process diagrams are `BPMN2.0::Collaboration`, not `BPMN2.0::Business Process` (a different, generic BPMN type that only happened to be used by the hand-built scratch reference that confirmed the mechanism):

```python
diag = collab_elem.Diagrams.AddNew(name, "Analysis")  # NOT "BusinessProcess"
diag.Stereotype = ""
diag.StereotypeEx = ""
diag.StyleEx = "MDGDgm=BPMN2.0::Collaboration;"  # the real toolbox selector
diag.Update()
```

**Fixed 2026-07-06 to be COM-only (see `ea-model-common`'s hard rule):** `Type`/`StyleEx` are set correctly at diagram-creation time only, via plain COM. An existing diagram found with the wrong `Type`/`StyleEx` can no longer be auto-corrected in code — `bpmn_engine.py`'s diagram-creation block now logs a warning naming the diagram instead of falling back to SQL. All 3 real process diagrams were re-verified correct after this change (no warnings on a real run).

## Diagram Placement Under the Right Parent

BPMN diagrams must be under the **CollaborationModel element**, NOT under the package:

```python
diag = collab_elem.Diagrams.AddNew("Sales Process Architecture", "Analysis")
```

## Element Creation: 3-Pass Strategy

For BPMN models with Lanes:

1. **Pass 1**: Create Lanes under CollaborationModel
2. **Pass 2**: Create non-Lane elements under their parent Lane (set ParentID)
3. **Pass 3**: Any missed elements (no lane) fall back to CollaborationModel

```python
# Pass 1: Create Lanes first
lane_ids = {}
for eid, data in lanes:
    new_elem = proc_arch.Elements.AddNew(data["name"], "Activity")
    lane_ids[eid] = new_elem.ElementID

# Pass 2: Create other elements under their lane
for eid, data in other_els:
    lane_eid = get_lane_for_element(data)
    parent_id = lane_ids.get(lane_eid, 0)
    new_elem = proc_arch.Elements.AddNew(data["name"], data["type"])
    new_elem.ParentID = parent_id
    # Capture GUID BEFORE Refresh()
    guid_map[eid] = new_elem.ElementGUID
```

## BPMN Connector Handling

### Stereotype Existence Check

Connectors from EA may return stereotypes in short form (`SequenceFlow`) or long form (`BPMN2.0::SequenceFlow`). Always check both:

```python
def connector_exists(connectors, src_id, tgt_id):
    for i in range(connectors.Count - 1, -1, -1):
        c = connectors.GetAt(i)
        stereo = c.Stereotype or c.StereotypeEx or ""
        if "SequenceFlow" not in stereo:  # checks both forms
            continue
        if c.ClientID == src_id and c.SupplierID == tgt_id:
            return True
    return False
```

### Connector Creation

```python
conn = connectors.AddNew("", "SequenceFlow")
conn.ClientID = src_element_id
conn.SupplierID = tgt_element_id
conn.StereotypeEx = "BPMN2.0::SequenceFlow"
conn.Update()
```

### Connector Routing — Border-Centered Attachment (rewritten 2026-07-05)

**`DiagramLink.Path` controls rendered routing — `.Geometry`'s `EDGE` field does not, by itself.** Confirmed empirically: setting only `.Geometry`'s `EDGE` substring (with `Path` untouched/empty) produced zero visible change across several trials. All routing control happens through `Path`'s absolute waypoint coordinates; `Geometry` is metadata (label positions, etc.) that can be left alone.

The general rule, verified against a user-provided manual reference edit in EA's GUI: **classify the relationship by Y-overlap first, not X-overlap.** Two boxes can end up X-disjoint purely as a side effect of some other positioning choice even when the *dominant* visual relationship is vertical (above/below). Checking X first misclassifies that case as a horizontal connector.

```python
def _connector_path(src, tgt):
    """src/tgt: (left, top, right, bottom) in EA's raw DiagramObject
    convention (top/bottom negative, more-negative = lower on the page).
    Returns a Path waypoint string, or None to let EA auto-route (boxes
    overlap in both axes)."""
    sl, st, sr, sb = src
    tl, tt, tr, tb = tgt
    scx, scy = (sl + sr) / 2, (st + sb) / 2
    tcx, tcy = (tl + tr) / 2, (tt + tb) / 2

    y_disjoint = tt <= sb or tb >= st
    x_disjoint = tl >= sr or tr <= sl

    if y_disjoint:
        return f"{int(scx)}:{int(tcy)};"
    if x_disjoint:
        mx = (sr + tl) / 2 if tl >= sr else (sl + tr) / 2
        return f"{int(mx)}:{int(scy)};"
    return None

# Applied to every DiagramLink, every run:
diag.DiagramLinks.Refresh()
diag.DiagramObjects.Refresh()
pos_map = {}
for di in range(diag.DiagramObjects.Count):
    dobj = diag.DiagramObjects.GetAt(di)
    pos_map[dobj.ElementID] = (dobj.left, dobj.top, dobj.right, dobj.bottom)
for i in range(diag.DiagramLinks.Count):
    dl = diag.DiagramLinks.GetAt(i)
    dl.LineStyle = 9  # Orthogonal Rounded (NOT 5 -- that's Tree Horizontal!)
    conn = repo.GetConnectorByID(dl.ConnectorID)
    src, tgt = pos_map.get(conn.ClientID), pos_map.get(conn.SupplierID)
    dl.Path = (_connector_path(src, tgt) or "") if src and tgt else ""
    dl.Update()
```

See `bpmn_engine.py::_connector_path` for the canonical implementation, applied unconditionally on every `generate()` run (default BPMN diagram behavior, not a one-off customization).

## BPMN Lane Layout

See `bpmn_engine.py` for the BPMN-only layout functions.

### Pool Support (verified 2026-07-05, synthetic test)

Pool → one or more Lanes → flow elements (a Pool never directly contains flow elements). A `### Lane—...` entry declares its parent Pool via `- Pool: <pool-eid>`, mirroring how flow elements declare `- Lane:`. Verified end-to-end with a synthetic 2-lane-1-pool + cross-lane MessageFlow fixture:
- `compute_bpmn_lane_positions(..., pools={pool_id: [lane_id, ...]})` groups same-pool lanes into one stacked column wrapped in a pool bounding box.
- The Pool/Lane stereotype-override in both MD writers already round-trips a Pool as `### Pool—...` correctly.
- Cross-**lane** MessageFlow alignment applies generally, not just cross-**pool** — a message flow between two lanes of the *same* pool gets the same clean vertical-alignment treatment automatically.

### BPMN Element Sizes

From `bpmn_config.BPMN_ELEMENT_SIZES`:

| BPMN Type | Width | Height |
|-----------|-------|--------|
| Activity/Task | 110 | 60 |
| StartEvent/EndEvent/IntermediateEvent | 30 | 30 |
| Gateway (all variants) | 42 | 42 |
| DataObject/DataStore/Artifact | 35 | 50 |
| TextAnnotation | 80 | 50 |

### Flow Layout (`compute_bpmn_flow_layout`)

Default layout for all 3 BPMN processes (2026-07-05).

**Row-per-flow structure (explicit user rule):** "A Start Event must be placed in the left hand column and from there sequence flows go to the right from activity to activity (or gateway or other elements). DataObjects and DataStores are always living in their own row [below or above the rows with activities]." Concretely, per lane:

1. Find the **connected components** of the lane's sequence-flow graph (undirected — a fork and its branches, or a merge and its inputs, are one component even though the edges are directed). Each component is one independent flow.
2. **Each component becomes its own row**, stacked vertically in the lane, in MD-declaration order: within a row, the longest acyclic path is placed in a straight horizontal line **starting at the lane's left column** (`lane_left + 70`) and flowing rightward.
3. **Gateway forks within one row do NOT start a new row** — they stack below/near the fork point within that same row's vertical space.
4. Branch handling *within* a row's flow (elements not on that row's own longest path) — three passes, in this order:
   1. **Gateway-fork groups**: elements whose predecessor is on the row's main path stack in one vertical column, below that row, centered under the gateway's **main-path successor** (not the gateway itself — a gateway diamond is narrow, so centering a wide activity box under it looks cramped).
   2. **Chain continuation**: any element that is the sole successor of a predecessor which in turn has only that one child continues that predecessor's row horizontally, same vertical center, immediately to its right, instead of dropping to a new row below. Applied repeatedly, so an entire multi-element branch chain flows left-to-right after its first activity. Restricted to elements with exactly one predecessor total, so a genuine merge point (2+ predecessors) is never accidentally inlined off just one of its incoming edges.
   3. **Chained remainder / merge points**: anything still unplaced stacks below its predecessor(s)' actual bottom edge + gap.
5. **DataObjects/DataStores**: always their own row, below all flow rows in the lane (computed from actual max bottom used, not a fixed row-count offset).

**Parameters:**
- `h_gap = 60` (horizontal space between elements)
- `v_gap = 30` (vertical space between rows within one flow; `v_gap * 2` between independent flow rows)
- Elements start at `lane_left + 70` (clears lane+pool double border)
- Lane width = widest lane's *actual placed content* width
- All lanes are expanded to the widest lane's width so they share a uniform right edge

**MessageFlow-aware alignment (explicit user rule):** "A MessageFlow normally crosses to an element in another lane... it starts in the middle top or bottom center of an activity and ends in the center bottom or top of the receiving activity — both elements are center aligned to each other in their own lane/pool." Pass `message_flows=[...]` to `compute_bpmn_flow_layout`:
- Lanes are processed **top-to-bottom** so a receiving lane's elements can align to an already-placed sending lane's elements.
- For each component, if its **leading element** is the source/target of a cross-lane MessageFlow to/from an already-placed element, the whole row is horizontally shifted so that leading element is **centered** on the partner's X.
- Scoped to the row's leading element only.
- Verified against Sales' real `Create RFQ → Confirm Customer Account` MessageFlow: both ended up with `cx=215.0` exactly.

**MessageFlow connector routing is a separate rule from position** (explicit user rule): "if a message flow starts at the bottom it should end in the receiving activity's top, and vice versa." Use `_message_flow_path(src, tgt)` instead of `_connector_path` whenever the connector's stereotype contains `"MessageFlow"`:
- Always exits/enters **top or bottom-center on both ends, never a side**.
- Uses a 2-waypoint elbow when the boxes aren't X-aligned; collapses to a single straight vertical line when they are.

**DataObject/DataStore alignment (explicit user rule):** "DataObjects and DataStore live in their own row. They are positioned above or below the activity they are connected to, which can exist in another lane/pool. The connector preferably has no bends." DataObjects stay in their existing dedicated row below the flow rows in their own lane, but are horizontally **centered on their connected activity's X** (via `DataInputAssociation`/`DataOutputAssociation`, passed as `data_associations=[...]`), wherever that activity ended up. Placed in a pass after ALL lanes' flow elements are placed.

**Shared-target overlap (fixed 2026-07-05):** two DataObjects connected to the same activity computed the same preferred center-X independently and overlapped. Fix: cascade — prefer the aligned X, but never place further left than the current packing pointer, so a second DataObject sharing a target's X stacks immediately to the right of the first.

**Longest path algorithm (`find_longest_path`):** DFS with visited-set, handles cycles. Starts from nodes with no incoming edges (and at least one outgoing), scoped to one connected component. Returns node IDs in traversal order.

**Overlap bug classes (fixed 2026-07-03 through 2026-07-05):**
- **Predecessor is itself a branch element**: stack below that element's *actual* bottom edge (`pos[p][3] + v_gap`), not the row's shared y.
- **Multiple siblings sharing one predecessor**: track `next_y_for_pred = {}` — each time a child of `p` is placed, advance `next_y_for_pred[p]` to below that child.
- **DataObjects row fixed offset**: compute the DataObjects row's start from the actual max bottom used by the branch section, not a row-count constant.
- **Fixed per-branch-row Y constant caused unrelated collisions**: recompute the fallback Y *dynamically* from the actual current max bottom, not a one-time snapshot.
- **Merge points resolved using only the first predecessor found**: when 2+ predecessors are already placed, clear the *max* of all their bottoms.
- **DFS traversal order can place a merge point before all its predecessors exist**: after the main placement pass, run a correction pass over every element with 2+ predecessors and re-clear against the now-complete predecessor set.
- **Lane height is a fixed guess computed before content is placed**: a post-processing pass walks lanes top-to-bottom and shifts every subsequent lane down by any overflow.

All of these were found and fixed by writing a **pure-Python overlap checker** (no EA/COM needed — just call `compute_bpmn_flow_layout` directly and check pairwise bounding-box intersection) against Sales' real MD, then verified end-to-end via a GUID-stripped Sandbox run + `SaveDiagramImageToFile`. Iterating this way (pure math → sandbox → image) is much faster than round-tripping through EA for every attempt.

### Re-run Position Management

**HARD RULE (Han, 2026-07-09) — never reflow an existing diagram.** `ProcessConfig.reflow_on_rerun` defaults to `False`. On a rerun against an existing diagram, `bpmn_engine.generate()` only:

- adds elements newly present in the MD (placed via `compute_bpmn_flow_layout` on the empty spots),
- removes elements no longer referenced by the MD,
- updates element data (name, notes, stereotype, parent) — data-only writes never touch layout.

Existing element positions and existing connector routings/linestyles are preserved. The connector-routing block is now gated on `is_new_diag or config.reflow_on_rerun`, so an existing connector's Path/LineStyle is never reset on rerun either.

Only in two cases does the full flow-aware layout run:
1. **First-time creation** (`is_new_diag == True`): the diagram is new, so there's no user layout to preserve.
2. **Explicit opt-in**: caller passes a `ProcessConfig` with `reflow_on_rerun=True`. This is a one-off script or a `--reflow` flag, never a default. If you're tempted to enable this permanently, don't.

Older versions of this skill described "Reflow-on-rerun is the default … Consequence: any manually-tuned layout on a live diagram will be overwritten" — that behaviour has been retired. If you see a run log line `Repositioning N diagram objects using flow layout` against a diagram the user has tuned, something is wrong: verify `config.reflow_on_rerun` and stop the run.

See memory `feedback_ea_no_reflow_existing_diagrams.md` for the incident that drove this rule.

## Quick Reference

| Diagram | Element sizing | Connector LineStyle | Diagram_Type / StyleEx MDGDgm |
|---|---|---|---|
| BPMN (all 3 processes) | Fixed per BPMN type, `BPMN_ELEMENT_SIZES` | `9` (Orthogonal Rounded) | `Analysis` / `BPMN2.0::Collaboration` |

## Source Files

| File | Purpose |
|------|---------|
| `experiments/modelgen/bpmn_config.py` | `ProcessConfig` dataclass + `CUSTOMER_ACCOUNT`/`SALES`/`NEWSLETTER` instances + shared BPMN vocabulary (`LABEL_TO_STEREO`, `OBJECT_TYPE_MAP`, `BPMN_TAGGED_VALUES`, `CONNECTOR_TYPES`, `BPMN_ELEMENT_SIZES`, etc.) |
| `experiments/modelgen/bpmn_engine.py` | Shared BPMN engine: `parse_md`, `generate`, `sync_to_md`, `_connector_path`, and the BPMN-only layout functions (`compute_bpmn_lane_positions` (pool-aware), `compute_bpmn_flow_layout`, `find_longest_path`, `sort_by_flow_order`, `get_lane_from_fields`, `get_pool_from_lane_fields`) |
| `experiments/modelgen/generate_customeraccount_process_from_md.py` | Thin wrapper: `bpmn_engine.generate(bpmn_config.CUSTOMER_ACCOUNT)` |
| `experiments/modelgen/generate_sales_process_from_md.py` | Thin wrapper: `bpmn_engine.generate(bpmn_config.SALES)` |
| `experiments/modelgen/generate_newsletter_process_from_md.py` | Thin wrapper: `bpmn_engine.generate(bpmn_config.NEWSLETTER)` |
| `experiments/modelgen/sync_customeraccount_process_from_ea.py` | Thin wrapper: `bpmn_engine.sync_to_md(bpmn_config.CUSTOMER_ACCOUNT)` |
| `experiments/modelgen/sync_sales_process_from_ea.py` | Thin wrapper: `bpmn_engine.sync_to_md(bpmn_config.SALES)` |
| `experiments/modelgen/sync_newsletter_process_from_ea.py` | Thin wrapper: `bpmn_engine.sync_to_md(bpmn_config.NEWSLETTER)` (hierarchical MD writer) |
