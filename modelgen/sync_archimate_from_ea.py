"""Read the ArchiMate model from EAxCRM.qea and write it as Markdown.

Reverse of ``generate_archimate.py``:
  generate:  MD -> EA (creates/updates elements, connectors, diagram)
  sync:      EA -> MD (reads current EA state, regenerates MD)

Round-trip preserves stable identifiers:
- Element/relation ids from the existing MD are kept when the element/rel can
  be matched by ``guid_map`` -> ea_guid. New-in-EA items get a synthesized
  ``e-<safe_name>`` / ``r-<type>-<safe_name>`` id, deduped against existing.
- The MD header preamble (everything above ``## Elements``) is preserved
  verbatim -- it's human-authored (version notes, changelog).
- The ``archimate_guid_map.json`` is refreshed to reflect actual EA state:
  entries for removed-in-EA elements/rels are dropped; new-in-EA get added.

Reads use ``ea_session.sql_rows(repo, sql)`` (which wraps
``Repository.SQLQuery``) exclusively -- never ``sqlite3.connect(qea)``. This
is the HARD RULE from ``ea-model-common``: shipped generate/sync code must
be backend-portable, since the .qea SQLite file is only one of several EA
repository backends.

Usage:
    python sync_archimate_from_ea.py [--qea PATH] [--md PATH] [--state-dir DIR]
"""
import argparse
import json
import os
import re
import sys

import ea_session
from changelog import ChangeLog, compute_md_diff
from generate_archimate import (
    ARCHIMATE_ELEMENT_STEREOTYPES,
    ARCHIMATE_RELATION_STEREOTYPES,
    CONNECTOR_BASE_TYPE,
    _normalize_stereotype,
    _rel_key,
)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QEA = r"M:\EAxCRM\models\EAxCRM.qea"
DEFAULT_MD = r"M:\EAxCRM\models\EAxCRM-Archimate.md"


# --- Reverse maps built from generate_archimate.py's forward maps ---
# Keys are the SHORT stereotype form ("ArchiMate_BusinessActor"), which is
# what t_object.Stereotype / t_connector.Stereotype actually contain.
STEREO_TO_ELEMENT_TYPE = {
    _normalize_stereotype(v): k for k, v in ARCHIMATE_ELEMENT_STEREOTYPES.items()
}
STEREO_TO_RELATION_TYPE = {
    _normalize_stereotype(v): k for k, v in ARCHIMATE_RELATION_STEREOTYPES.items()
}

# ArchiMate layer per element type. Derived from the ArchiMate 3 spec's
# element-catalogue layers (Business / Application / Technology). Anything
# not in this map falls through to "" and is not emitted.
LAYER_BY_ELEMENT_TYPE = {
    "BusinessActor": "Business",
    "BusinessRole": "Business",
    "BusinessFunction": "Business",
    "BusinessProcess": "Business",
    "BusinessObject": "Business",
    "BusinessService": "Business",
    "ApplicationComponent": "Application",
    "ApplicationCollaboration": "Application",
    "ApplicationInterface": "Application",
    "ApplicationService": "Application",
    "ApplicationFunction": "Application",
    "DataObject": "Application",
    "Node": "Technology",
    "Device": "Technology",
    "SystemSoftware": "Technology",
    "TechnologyService": "Technology",
    "Artifact": "Technology",
    "Grouping": "",
    "Location": "",
}


def log(msg):
    print(msg, flush=True)


def safe_id(text):
    """Kebab-case, alphanumerics only, collapse-and-trim separators."""
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s


def synthesize_element_id(name, existing_ids):
    base = f"e-{safe_id(name)}"
    candidate, n = base, 2
    while candidate in existing_ids:
        candidate = f"{base}-{n}"
        n += 1
    return candidate


def synthesize_relation_id(rel_type, src_id, tgt_id, existing_ids):
    # r-<type>-<src-suffix>-<tgt-suffix> keeps ids stable-ish and readable.
    src_short = src_id.removeprefix("e-")[:20]
    tgt_short = tgt_id.removeprefix("e-")[:20]
    base = f"r-{rel_type.lower()}-{src_short}-{tgt_short}"
    candidate, n = base, 2
    while candidate in existing_ids:
        candidate = f"{base}-{n}"
        n += 1
    return candidate


# --- Existing MD parsing (id + md_guid extraction; header preservation) ---

def load_existing_md(md_path):
    """Return (header_text, existing_element_index, existing_relation_index).

    header_text: everything up to (not including) the ``## Elements`` line,
        preserved verbatim to survive the round-trip.
    existing_element_index: {md_guid: {id, type, name}} for elements whose
        ``- GUID:`` field is non-empty and non-placeholder.
    existing_relation_index: {md_guid: {id, type, source, target}} likewise.

    If the MD file doesn't exist yet (very first sync), returns a minimal
    fallback header and empty indexes.
    """
    fallback_header = (
        "# EAxCRM - ArchiMate Model\n\n"
        "**Model ID**: m-eacrm\n"
        "**Purpose**: Enterprise Architect Customer Relationship Manager\n"
        "**Version**: sync-init\n\n"
    )
    if not os.path.exists(md_path):
        return {
            "header": fallback_header,
            "elements_by_guid": {},
            "relations_by_guid": {},
            "all_elements": [],
            "all_relations": [],
        }

    with open(md_path, encoding="utf-8") as f:
        lines = f.readlines()

    header_lines = []
    section = None
    for line in lines:
        if line.rstrip() == "## Elements":
            section = "elements"
            break
        header_lines.append(line)
    header_text = "".join(header_lines)

    elements_by_guid = {}
    relations_by_guid = {}
    all_elements = []
    all_relations = []
    current = None

    def commit_current(entry):
        if not entry:
            return
        if entry["kind"] == "elements":
            all_elements.append(entry)
            g = entry["guid"]
            if g and g != "{}":
                elements_by_guid[g] = entry
        else:
            all_relations.append(entry)
            g = entry["guid"]
            if g and g != "{}":
                relations_by_guid[g] = entry

    for line in lines:
        stripped = line.rstrip()
        if stripped == "## Elements":
            commit_current(current)
            section = "elements"
            current = None
            continue
        if stripped == "## Relationships":
            commit_current(current)
            section = "relationships"
            current = None
            continue
        if section is None:
            continue

        if stripped.startswith("### "):
            commit_current(current)
            remainder = stripped[4:].strip()
            m = re.match(r"(\w+)\s*[—\-]+\s*(\S+)", remainder)
            if m:
                current = {
                    "kind": section,
                    "type": m.group(1),
                    "id": m.group(2),
                    "name": "",
                    "source": "",
                    "target": "",
                    "guid": "",
                }
            else:
                current = None
            continue

        if current is None or not stripped.startswith("- "):
            continue
        kv = stripped[2:].strip()
        if ": " not in kv:
            continue
        key, value = kv.split(": ", 1)
        value = value.strip()
        if key == "Name":
            current["name"] = value
        elif key in ("GUID", "Guid", "guid"):
            current["guid"] = value
        elif key == "Source":
            current["source"] = value
        elif key == "Target":
            current["target"] = value

    commit_current(current)

    return {
        "header": header_text,
        "elements_by_guid": elements_by_guid,
        "relations_by_guid": relations_by_guid,
        "all_elements": all_elements,
        "all_relations": all_relations,
    }


# --- EA state reads (COM-only, all SQL via ea_session.sql_rows) ---

def find_eaxcrm_package(repo):
    """Find the EAxCRM ArchiMate package (currently 'EAxCRM' under 'Application Architecture').

    Returns Package_ID as int, or raises on ambiguity/absence.
    """
    rows = ea_session.sql_rows(repo, """
        SELECT Package_ID, Name FROM t_package WHERE Name = 'EAxCRM'
    """)
    if not rows:
        raise RuntimeError("EAxCRM package not found in repo (Name='EAxCRM')")
    if len(rows) > 1:
        # If ever ambiguous (e.g. someone made a second 'EAxCRM' package under
        # a different parent), fall back to the one under 'Application
        # Architecture'.
        rows = ea_session.sql_rows(repo, """
            SELECT p.Package_ID, p.Name
            FROM t_package p
            JOIN t_package parent ON parent.Package_ID = p.Parent_ID
            WHERE p.Name = 'EAxCRM' AND parent.Name = 'Application Architecture'
        """)
        if len(rows) != 1:
            raise RuntimeError(f"EAxCRM package ambiguous or missing under Application Architecture: {rows}")
    return int(rows[0]["Package_ID"])


def read_elements(repo, pkg_id):
    """Return list of element dicts in stable-order (Object_ID ascending)."""
    rows = ea_session.sql_rows(repo, f"""
        SELECT Object_ID, Name, Object_Type, IFNULL(Stereotype,'') AS Stereotype,
               ea_guid, IFNULL(Note,'') AS Note
        FROM t_object
        WHERE Package_ID = {pkg_id}
        ORDER BY Object_ID
    """)
    elements = []
    for r in rows:
        archimate_type = STEREO_TO_ELEMENT_TYPE.get(r["Stereotype"])
        if not archimate_type:
            # Skip non-ArchiMate content parked in this package (Notes,
            # Boundaries, etc.). Log so genuine surprises are visible.
            if r["Stereotype"] or r["Object_Type"] not in ("Note", "Boundary", "Text"):
                log(f"  SKIP non-ArchiMate element {r['Object_ID']} "
                    f"'{r['Name']}' (Object_Type={r['Object_Type']!r}, "
                    f"Stereotype={r['Stereotype']!r})")
            continue
        elements.append({
            "object_id": int(r["Object_ID"]),
            "name": r["Name"],
            "type": archimate_type,
            "layer": LAYER_BY_ELEMENT_TYPE.get(archimate_type, ""),
            "description": r["Note"].strip(),
            "ea_guid": r["ea_guid"],
        })
    return elements


def read_relations(repo, object_ids):
    """Return list of relation dicts for connectors whose BOTH endpoints are
    in ``object_ids``. Access relations also carry Direction + AccessMode tag
    (if present) for round-tripping issue #17 #6 semantics later."""
    if not object_ids:
        return []
    id_list = ",".join(str(i) for i in object_ids)

    # Main connector query. Include Direction always (cheap, semantic for
    # Access + Dynamic categories per ArchiMate 3).
    rows = ea_session.sql_rows(repo, f"""
        SELECT Connector_ID, Start_Object_ID, End_Object_ID,
               Connector_Type, IFNULL(Stereotype,'') AS Stereotype,
               IFNULL(Direction,'') AS Direction, ea_guid,
               IFNULL(Notes,'') AS Notes
        FROM t_connector
        WHERE Start_Object_ID IN ({id_list})
          AND End_Object_ID IN ({id_list})
        ORDER BY Connector_ID
    """)

    # AccessMode tags. Do a single wide query, then attach in Python -- one
    # query per connector would (a) be N+1 and (b) hide silent SQL failures
    # in the "no rows" case.
    access_conn_ids = [
        int(r["Connector_ID"]) for r in rows if r["Stereotype"] == "ArchiMate_Access"
    ]
    access_mode_by_conn = {}
    if access_conn_ids:
        access_id_list = ",".join(str(i) for i in access_conn_ids)
        tag_rows = ea_session.sql_rows(repo, f"""
            SELECT ElementID, IFNULL(VALUE,'') AS Value
            FROM t_connectortag
            WHERE Property = 'AccessMode'
              AND ElementID IN ({access_id_list})
        """)
        access_mode_by_conn = {int(r["ElementID"]): r["Value"] for r in tag_rows}

    relations = []
    for r in rows:
        norm = _normalize_stereotype(r["Stereotype"])
        rel_type = STEREO_TO_RELATION_TYPE.get(norm)
        if not rel_type:
            log(f"  SKIP connector {r['Connector_ID']} with unknown stereotype "
                f"{r['Stereotype']!r} (type={r['Connector_Type']!r})")
            continue
        # Sanity check: t_connector.Connector_Type should match the base type
        # generate_archimate expects for this stereotype. Mismatch would mean
        # someone retyped the connector by hand and the model is now
        # inconsistent -- flag it, keep going.
        expected_base = CONNECTOR_BASE_TYPE.get(rel_type, "Association")
        if r["Connector_Type"] != expected_base:
            log(f"  WARN connector {r['Connector_ID']} ({rel_type}) has "
                f"Connector_Type={r['Connector_Type']!r}, expected "
                f"{expected_base!r}. Run dedup_archimate_connectors.py to fix.")

        conn_id = int(r["Connector_ID"])
        relations.append({
            "connector_id": conn_id,
            "type": rel_type,
            "start_object_id": int(r["Start_Object_ID"]),
            "end_object_id": int(r["End_Object_ID"]),
            "direction": r["Direction"],
            "access_mode": access_mode_by_conn.get(conn_id, ""),
            "ea_guid": r["ea_guid"],
            "notes": r["Notes"].strip(),
        })
    return relations


# --- Reconciliation: match EA state against existing MD ids ---

def reconcile_ids(elements, relations, guid_map, md_state):
    """Assign an MD id + md_guid to each EA element/relation.

    For each EA element with ea_guid X:
      1. Reverse-lookup guid_map to find md_guid where guid_map[md_guid] == X.
      2. If found and that md_guid is in existing_elem_index, reuse the MD's
         id AND md_guid -- perfect round-trip.
      3. If not, this is a new-in-EA element: synthesize an id, use the EA
         guid itself as the md_guid (they're both GUIDs; identical is fine).

    Same for relations (using _rel_key semantics).
    Populates each dict with 'id' and 'md_guid' fields in-place. Returns the
    set of surviving md_guids (for guid_map cleanup).
    """
    # Reverse index: ea_guid -> md_guid (only entries where value is the ea_guid)
    reverse_guid_map = {}
    for md_g, ea_g in guid_map.items():
        if md_g.startswith("_diagram_") or md_g.startswith("rel:") or md_g == "{}":
            # Diagram GUID keys and rel-fallback keys reuse: leave alone;
            # they aren't element/rel md_guids. "{}" placeholder-key entries
            # are unreliable (the generate side collides all placeholders on
            # this key, so it points at whichever placeholder-GUID MD entry
            # was created last -- never trustworthy).
            continue
        reverse_guid_map[ea_g] = md_g

    existing_elem_index = md_state["elements_by_guid"]
    existing_rel_index = md_state["relations_by_guid"]

    # Fallback indexes for name-based recovery when the GUID chain is broken
    # (typically MD entries authored with placeholder "GUID: {}" that were
    # never round-tripped through generate to receive a real EA guid, or
    # cases where the generate-side placeholder collision has scrambled the
    # guid_map). Preserves MD id continuity where an EA object plainly
    # matches by name/endpoints even though no GUID mapping survived.
    # Iterate ALL parsed MD entries -- especially the {}-GUID ones, which
    # are exactly the ones that need name-matching to survive.
    existing_by_name = {}  # (type, name) -> existing entry
    for entry in md_state["all_elements"]:
        existing_by_name[(entry["type"], entry["name"])] = entry
    existing_by_endpoints = {}  # (type, source, target) -> existing entry
    for entry in md_state["all_relations"]:
        existing_by_endpoints[(entry["type"], entry["source"], entry["target"])] = entry

    used_ids = set()
    surviving_md_guids = set()

    matched_by_name_count = 0
    new_in_ea_count = 0
    for el in elements:
        md_g = reverse_guid_map.get(el["ea_guid"])
        existing = existing_elem_index.get(md_g) if md_g else None
        match_source = "guid"
        if not existing:
            # Name-match fallback for MD entries whose GUIDs got scrambled.
            existing = existing_by_name.get((el["type"], el["name"]))
            if existing:
                match_source = "name"
                matched_by_name_count += 1
                log(f"  NAME-MATCH element '{el['name']}' -> preserved id "
                    f"'{existing['id']}' (MD GUID was '{existing['guid']}', "
                    f"EA guid '{el['ea_guid']}')")
        if existing:
            el["id"] = existing["id"]
            # GUID match: MD already has the right GUID, keep it as-is
            # (respects the MD as source-of-truth for identifiers).
            # Name match: MD's GUID was a bad placeholder; heal it with the
            # real EA guid so subsequent round-trips work via guid.
            el["md_guid"] = existing["guid"] if match_source == "guid" else el["ea_guid"]
            el["_matched"] = True
        else:
            el["id"] = synthesize_element_id(el["name"], used_ids)
            el["md_guid"] = el["ea_guid"]
            el["_matched"] = False
            new_in_ea_count += 1
        used_ids.add(el["id"])
        surviving_md_guids.add(el["md_guid"])

    # Build object_id -> id map for relation source/target resolution
    id_by_obj = {el["object_id"]: el["id"] for el in elements}

    used_rel_ids = set()
    for rel in relations:
        src_id = id_by_obj.get(rel["start_object_id"])
        tgt_id = id_by_obj.get(rel["end_object_id"])
        if not src_id or not tgt_id:
            # Endpoint not in the ArchiMate elements list (shouldn't happen
            # because the SQL already filtered by IN (object_ids), but guard).
            log(f"  SKIP rel {rel['connector_id']}: endpoint not in element set")
            rel["id"] = None
            continue
        rel["source"] = src_id
        rel["target"] = tgt_id

        md_g = reverse_guid_map.get(rel["ea_guid"])
        existing = existing_rel_index.get(md_g) if md_g else None
        match_source = "guid"
        if not existing:
            existing = existing_by_endpoints.get((rel["type"], src_id, tgt_id))
            if existing:
                match_source = "endpoint"
                log(f"  ENDPOINT-MATCH rel {rel['type']} {src_id}->{tgt_id} "
                    f"-> preserved id '{existing['id']}' (MD GUID was "
                    f"'{existing['guid']}', EA guid '{rel['ea_guid']}')")
        if existing:
            rel["id"] = existing["id"]
            rel["md_guid"] = existing["guid"] if match_source == "guid" else rel["ea_guid"]
            rel["_matched"] = True
        else:
            rel["id"] = synthesize_relation_id(rel["type"], src_id, tgt_id,
                                                used_rel_ids)
            rel["md_guid"] = rel["ea_guid"]
            rel["_matched"] = False
        used_rel_ids.add(rel["id"])
        surviving_md_guids.add(rel["md_guid"])

    return surviving_md_guids


# --- MD emission ---

def emit_md(header_text, elements, relations):
    parts = [header_text.rstrip() + "\n\n"]
    parts.append("## Elements\n\n")
    for el in elements:
        parts.append(f"### {el['type']} — {el['id']}\n")
        parts.append(f"- Name: {el['name']}\n")
        if el["description"]:
            parts.append(f"- Description: {el['description']}\n")
        parts.append(f"- GUID: {el['md_guid']}\n")
        if el["layer"]:
            parts.append(f"- Layer: {el['layer']}\n")
        parts.append("\n")
    parts.append("## Relationships\n\n")
    for rel in relations:
        if rel.get("id") is None:
            continue
        parts.append(f"### {rel['type']} — {rel['id']}\n")
        parts.append(f"- Source: {rel['source']}\n")
        parts.append(f"- Target: {rel['target']}\n")
        parts.append(f"- GUID: {rel['md_guid']}\n")
        # Direction is only semantically meaningful for a few relation types.
        # Emit it selectively rather than blindly, because:
        #   - Composition/Aggregation store Direction="Destination -> Source"
        #     as a generate-side rendering swap (whole-end diamond, see
        #     ea-archimate-creator skill) -- NOT authored semantics. Round-
        #     tripping it would confuse a future generate re-run.
        #   - Realization/Association/Assignment have no direction-driven
        #     semantics in ArchiMate 3.
        # Access is the case with real Read/Write/Read-Write semantics
        # (issue #17 #6) so we always emit its Direction + AccessMode.
        # Flow and Triggering are dynamic-category with a direction that
        # matters (data flow / trigger direction), so emit when non-default.
        default_dirs = ("Source -> Destination", "Unspecified", "")
        if rel["type"] == "Access":
            # Emit only when non-default: default is "Source -> Destination"
            # (Read/Write per #6's future interpretation). Non-default carries
            # real Read vs. Write semantics; emit so it round-trips.
            if rel["direction"] not in default_dirs:
                parts.append(f"- Direction: {rel['direction']}\n")
            if rel["access_mode"]:
                parts.append(f"- AccessMode: {rel['access_mode']}\n")
        elif rel["type"] in ("Flow", "Triggering", "Influence"):
            if rel["direction"] not in default_dirs:
                parts.append(f"- Direction: {rel['direction']}\n")
        parts.append("\n")
    return "".join(parts)


# --- GUID map refresh ---

def refresh_guid_map(guid_map_path, elements, relations):
    """Rewrite the guid map to reflect actual EA state: keep only entries for
    surviving elements/rels, add new-in-EA entries. Preserve any bookkeeping
    keys (diagram GUIDs, prefixed "rel:" fallbacks) that aren't element/rel
    md_guids -- those are not derivable from the EA state alone."""
    old_map = {}
    if os.path.exists(guid_map_path):
        with open(guid_map_path, encoding="utf-8") as f:
            old_map = json.load(f)

    new_map = {}
    # Preserve bookkeeping keys (diagram guid tokens, rel-id fallback keys)
    for k, v in old_map.items():
        if k.startswith("_") or k.startswith("rel:"):
            new_map[k] = v

    for el in elements:
        new_map[el["md_guid"]] = el["ea_guid"]
    for rel in relations:
        if rel.get("id") is not None:
            new_map[rel["md_guid"]] = rel["ea_guid"]

    with open(guid_map_path, "w", encoding="utf-8") as f:
        json.dump(new_map, f, indent=2)
    return new_map


def main():
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(
        description="Sync ArchiMate model from EAxCRM.qea to Markdown (COM-only)")
    parser.add_argument("--qea", default=DEFAULT_QEA)
    parser.add_argument("--md", default=DEFAULT_MD)
    parser.add_argument("--state-dir", default=SCRIPT_DIR,
                        help="Directory for the changelog and GUID-map files.")
    args = parser.parse_args()

    guid_map_path = os.path.join(args.state_dir, "archimate_guid_map.json")
    changelog_path = os.path.join(args.state_dir, "archimate_changelog.md")

    # Load existing MD (for header + id preservation)
    md_state = load_existing_md(args.md)
    log(f"Existing MD: {len(md_state['all_elements'])} elements "
        f"({len(md_state['elements_by_guid'])} with real GUID), "
        f"{len(md_state['all_relations'])} relations "
        f"({len(md_state['relations_by_guid'])} with real GUID)")

    # Load existing guid_map (for id reverse-lookup)
    guid_map = {}
    if os.path.exists(guid_map_path):
        with open(guid_map_path, encoding="utf-8") as f:
            guid_map = json.load(f)
    log(f"Loaded {len(guid_map)} GUID mappings")

    clog = ChangeLog(changelog_path)
    clog.checkpoint("Loaded MD + guid_map")

    log("Opening EA session...")
    with ea_session.ea_repository(args.qea, technology="ArchiMate3") as repo:
        pkg_id = find_eaxcrm_package(repo)
        log(f"EAxCRM package: Package_ID={pkg_id}")

        elements = read_elements(repo, pkg_id)
        log(f"Read {len(elements)} elements from EA")

        object_ids = [el["object_id"] for el in elements]
        relations = read_relations(repo, object_ids)
        log(f"Read {len(relations)} relations from EA")

    # ea_repository context manager has closed the session; the rest is pure
    # Python (reconciliation, MD emission, file writes).

    reconcile_ids(elements, relations, guid_map, md_state)

    # Preserve MD-declaration order for matched items (minimizes cosmetic
    # diff on re-sync); append new-in-EA items after their matched siblings
    # in Object_ID / Connector_ID order.
    elem_md_order = {e["id"]: i for i, e in enumerate(md_state["all_elements"])}
    elements.sort(key=lambda el: (elem_md_order.get(el["id"], 10**9), el["object_id"]))
    rel_md_order = {r["id"]: i for i, r in enumerate(md_state["all_relations"])}
    relations.sort(key=lambda rel: (rel_md_order.get(rel.get("id"), 10**9),
                                     rel["connector_id"]))

    new_elements = [el for el in elements if not el.get("_matched")]
    new_relations = [rel for rel in relations
                     if rel.get("id") is not None and not rel.get("_matched")]
    if new_elements:
        log(f"  {len(new_elements)} new-in-EA element(s) synthesised MD ids:")
        for el in new_elements[:10]:
            log(f"    + {el['type']} '{el['name']}' -> {el['id']}")
        if len(new_elements) > 10:
            log(f"    ... (+{len(new_elements) - 10} more)")
    if new_relations:
        log(f"  {len(new_relations)} new-in-EA relation(s) synthesised MD ids:")
        for rel in new_relations[:10]:
            log(f"    + {rel['type']} {rel['source']} -> {rel['target']}: {rel['id']}")
        if len(new_relations) > 10:
            log(f"    ... (+{len(new_relations) - 10} more)")

    md_text = emit_md(md_state["header"], elements, relations)

    prev_md = ""
    if os.path.exists(args.md):
        with open(args.md, encoding="utf-8") as f:
            prev_md = f.read()

    with open(args.md, "w", encoding="utf-8", newline="\n") as f:
        f.write(md_text)
    log(f"Wrote {args.md} ({len(md_text)} chars)")

    refreshed = refresh_guid_map(guid_map_path, elements, relations)
    log(f"Refreshed guid_map ({len(refreshed)} entries)")

    # Changelog diff -- lets a subsequent diff-review show only what actually
    # changed. compute_md_diff parses a name-lookup out of the MD; if the
    # ArchiMate MD's format isn't a match, this gracefully logs an empty
    # summary rather than crashing.
    try:
        diff = compute_md_diff(prev_md, md_text)
        if diff:
            clog.log("synced", "archimate", "ArchiMate", "ArchiMate", "",
                     changes={"diff_summary": diff})
    except Exception as e:
        log(f"  compute_md_diff failed (non-fatal): {e}")

    clog.checkpoint("Sync complete")
    clog.close()

    log("\nDone.")


if __name__ == "__main__":
    main()
