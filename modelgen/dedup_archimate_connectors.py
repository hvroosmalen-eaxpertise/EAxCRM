"""One-off cleanup for duplicate ArchiMate connectors in EAxCRM.qea.

Github issue #17: before the GUID-based existence check landed in
``generate_archimate.py``, the ``sync_relations`` loop matched purely on
``(ClientID, SupplierID)`` off a stale ``Connectors`` snapshot, so any rerun
could silently duplicate connectors. This script cleans up whatever drift
has already accumulated in the shipped ``.qea`` and backfills the guid map.

Usage:
    python dedup_archimate_connectors.py [--qea PATH] [--md PATH] [--apply]

Defaults to a dry-run (prints the plan without touching the model). Pass
``--apply`` to execute the deletions.

Design:
    For each MD relation, compute the expected 4-tuple
    ``(client_ea_id, supplier_ea_id, base_type, normalized_stereotype)``.
    Scan connectors on the src EA element, bucket matches into "strict" (same
    normalized stereotype) and "legacy" (blank stereotype on the live
    connector, e.g. Flow relations from the pre-fix era). Keep the lowest
    ConnectorID as the survivor (most likely already referenced by diagram
    placements); delete the rest via COM so EA's referential integrity to
    ``t_diagramlinks``/``t_connectortag`` stays consistent. Legacy survivors
    also get their ``StereotypeEx`` set so subsequent generator runs match on
    Tier 2 without re-adopting.

COM-only. Never write directly to the ``.qea`` SQLite file -- bypasses EA's
constraints (2026-07-06 hard rule, see ea-model-common skill).
"""
import argparse
import os
import sys
import time

import ea_session
import generate_archimate as ga


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def resolve_pair(rel, elem_by_id, guid_map):
    src = elem_by_id.get(rel["source"])
    tgt = elem_by_id.get(rel["target"])
    if not src or not tgt:
        return None, None, "source/target element not found in MD"
    src_ea = guid_map.get(src["guid"])
    tgt_ea = guid_map.get(tgt["guid"])
    if not src_ea or not tgt_ea:
        return None, None, "source/target not in guid_map (element not yet in EA)"
    return src_ea, tgt_ea, None


def scan_and_plan(repo, relations, elements, guid_map):
    """Build a plan of survivors, duplicates, adoptions, and retypes.

    A connector candidate for an MD relation is any connector on the src
    element with matching ``ClientID/SupplierID``. We then bucket by whether
    its stereotype and Type match what the MD expects:

    - **strict**: normalized_stereotype matches. May still need a retype if
      the base Type is stale (e.g. an Access connector left over from when
      CONNECTOR_BASE_TYPE mapped Access to Association).
    - **legacy**: stereotype is blank -- adopt it (set StereotypeEx). Also
      needs retype if Type is wrong.

    Strict candidates outrank legacy ones. Lowest ConnectorID within the
    winning bucket is the survivor (most likely already referenced by
    diagram placements); the rest go to the delete list.
    """
    elem_by_id = {e["id"]: e for e in elements}

    # Group MD relations by src EA element GUID so we can Refresh Connectors
    # once per element.
    by_src = {}
    for rel in relations:
        if not rel.get("sparx_stereotype"):
            continue
        src_ea, tgt_ea, err = resolve_pair(rel, elem_by_id, guid_map)
        if err:
            log(f"  SKIP rel '{rel['id']}': {err}")
            continue
        by_src.setdefault(src_ea, []).append((rel, tgt_ea))

    plan = []
    stats = {"strict": 0, "legacy_adopted": 0, "retyped": 0,
             "duplicates": 0, "missing": 0}

    for src_ea, rels in by_src.items():
        try:
            src_elem = repo.GetElementByGuid(src_ea)
        except Exception:
            src_elem = None
        if not src_elem:
            log(f"  SKIP src {src_ea}: element not found in repo")
            continue

        src_elem.Connectors.Refresh()
        connectors = [src_elem.Connectors.GetAt(i)
                      for i in range(src_elem.Connectors.Count)]

        for rel, tgt_ea in rels:
            try:
                tgt_elem = repo.GetElementByGuid(tgt_ea)
            except Exception:
                tgt_elem = None
            if not tgt_elem:
                log(f"  SKIP rel '{rel['id']}': target element {tgt_ea} not in repo")
                continue

            base_type = ga.CONNECTOR_BASE_TYPE.get(rel["type"], "Association")
            full_stereo = rel["sparx_stereotype"]
            norm_stereo = ga._normalize_stereotype(full_stereo)

            # Tier 1: GUID-first repair. If guid_map has this rel_key and the
            # stored connector still points at the expected pair, that IS the
            # survivor -- even if its stereotype/type disagree with the MD
            # (the "MD changed its mind" case, e.g. a Flow relation the user
            # reclassified as Access). Compute repair actions and skip the
            # structural scan for this rel.
            rel_key = ga._rel_key(rel)
            stored_ea_guid = guid_map.get(rel_key)
            if stored_ea_guid:
                try:
                    cand = repo.GetConnectorByGuid(stored_ea_guid)
                except Exception:
                    cand = None
                if (cand
                        and cand.ClientID == src_elem.ElementID
                        and cand.SupplierID == tgt_elem.ElementID):
                    c_stereo = ga._normalize_stereotype(
                        cand.StereotypeEx or cand.Stereotype or "")
                    needs_retype = cand.Type != base_type
                    needs_restereo = c_stereo != norm_stereo
                    if needs_retype or needs_restereo:
                        if needs_retype:
                            stats["retyped"] += 1
                        if needs_restereo:
                            stats["legacy_adopted"] += 1
                    else:
                        stats["strict"] += 1
                    plan.append({
                        "rel_id": rel["id"],
                        "rel_type": rel["type"],
                        "rel_key": rel_key,
                        "src_ea": src_ea,
                        "src_elem_id": src_elem.ElementID,
                        "survivor_id": cand.ConnectorID,
                        "survivor_guid": cand.ConnectorGUID,
                        "dup_ids": [],
                        "dup_guids": [],
                        "adopt_stereo": full_stereo if needs_restereo else None,
                        "retype_from": cand.Type if needs_retype else None,
                        "retype_to": base_type if needs_retype else None,
                    })
                    continue

            strict = []
            legacy = []
            for c in connectors:
                if c.ClientID != src_elem.ElementID:
                    continue
                if c.SupplierID != tgt_elem.ElementID:
                    continue
                c_stereo = ga._normalize_stereotype(c.StereotypeEx or c.Stereotype or "")
                if c_stereo == norm_stereo:
                    strict.append(c)
                elif c_stereo == "" and norm_stereo != "":
                    # Blank stereo: only claim it as legacy if the base type
                    # is one we might have written previously OR the expected
                    # new type (avoids stealing an unrelated blank connector
                    # of some other type between the same pair).
                    if c.Type in (base_type, "Association"):
                        legacy.append(c)

            if strict:
                strict.sort(key=lambda c: c.ConnectorID)
                survivor = strict[0]
                dups = strict[1:] + legacy
                adopt = None
                stats["strict"] += 1
            elif legacy:
                legacy.sort(key=lambda c: c.ConnectorID)
                survivor = legacy[0]
                dups = legacy[1:]
                adopt = full_stereo
                stats["legacy_adopted"] += 1
            else:
                stats["missing"] += 1
                log(f"  MISS rel '{rel['id']}' ({rel['type']}): no connector matches "
                    f"({rel['source']} -> {rel['target']}, stereo={norm_stereo!r})")
                continue

            retype_from = survivor.Type if survivor.Type != base_type else None
            if retype_from:
                stats["retyped"] += 1

            stats["duplicates"] += len(dups)
            plan.append({
                "rel_id": rel["id"],
                "rel_type": rel["type"],
                "rel_key": ga._rel_key(rel),
                "src_ea": src_ea,
                "src_elem_id": src_elem.ElementID,
                "survivor_id": survivor.ConnectorID,
                "survivor_guid": survivor.ConnectorGUID,
                "dup_ids": [c.ConnectorID for c in dups],
                "dup_guids": [c.ConnectorGUID for c in dups],
                "adopt_stereo": adopt,
                "retype_from": retype_from,
                "retype_to": base_type if retype_from else None,
            })

    return plan, stats


def apply_plan(repo, plan):
    """Execute the plan: delete duplicates, adopt legacy stereotypes, refresh."""
    # Group by src element to Refresh once per element after all its
    # deletions land.
    by_elem = {}
    for entry in plan:
        by_elem.setdefault(entry["src_elem_id"], []).append(entry)

    for src_elem_id, entries in by_elem.items():
        # Find the src element via its ElementID (any entry has its GUID).
        src_ea = entries[0]["src_ea"]
        src_elem = repo.GetElementByGuid(src_ea)

        # Collect all connector-IDs we want gone on this element.
        dup_ids = set()
        for entry in entries:
            dup_ids.update(entry["dup_ids"])

        # Adopt legacy connectors and/or retype them first: set StereotypeEx
        # and Type while survivor is still resolvable by GUID (deletions
        # don't affect other connectors but Refresh invalidates cached
        # objects).
        for entry in entries:
            if entry["adopt_stereo"] is None and entry["retype_from"] is None:
                continue
            surv_guid = entry["survivor_guid"]
            try:
                surv = repo.GetConnectorByGuid(surv_guid)
            except Exception:
                surv = None
            if surv is None:
                log(f"  WARN could not resolve survivor {surv_guid}, skipping fix")
                continue
            # Sparx quirk: setting Type and StereotypeEx in a single Update()
            # silently drops the StereotypeEx (verified against a Dependency
            # + ArchiMate_Access retype -- StereotypeEx read back as blank).
            # Do two Updates: retype first, then set the stereotype on the
            # re-fetched connector.
            actions = []
            if entry["retype_from"] is not None:
                surv.Type = entry["retype_to"]
                surv.Update()
                actions.append(f"type {entry['retype_from']}->{entry['retype_to']}")
                surv = repo.GetConnectorByGuid(surv_guid)
            if entry["adopt_stereo"] is not None:
                surv.StereotypeEx = entry["adopt_stereo"]
                surv.Update()
                actions.append(f"stereo->{entry['adopt_stereo']}")
            log(f"  FIXED connector {surv_guid}: {', '.join(actions)}")

        # Delete duplicates. Iterate from the highest index down so indexes
        # remain valid mid-loop; pass refresh=False and Refresh once at the
        # end.
        if dup_ids:
            src_elem.Connectors.Refresh()
            for i in range(src_elem.Connectors.Count - 1, -1, -1):
                c = src_elem.Connectors.GetAt(i)
                if c.ConnectorID in dup_ids:
                    log(f"  DELETE connector id={c.ConnectorID} guid={c.ConnectorGUID}")
                    src_elem.Connectors.DeleteAt(i, False)
            src_elem.Connectors.Refresh()
            src_elem.Update()


def print_plan(plan, stats):
    print()
    print("Plan:")
    for entry in plan:
        actions = []
        if entry["retype_from"] is not None:
            actions.append(f"retype {entry['retype_from']}->{entry['retype_to']}")
        if entry["adopt_stereo"]:
            actions.append(f"adopt stereo -> {entry['adopt_stereo']}")
        if entry["dup_ids"]:
            actions.append(f"delete {entry['dup_ids']}")
        if not actions:
            continue
        print(f"  rel '{entry['rel_id']}' ({entry['rel_type']}): "
              f"keep id={entry['survivor_id']}  [{'; '.join(actions)}]")
    print()
    print(f"Summary: {stats['strict']} strict matches, "
          f"{stats['legacy_adopted']} legacy blank-stereo adoptions, "
          f"{stats['retyped']} retypes, "
          f"{stats['duplicates']} duplicate connectors to delete, "
          f"{stats['missing']} MD rels with no matching connector.")


def main():
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(
        description="Dedup duplicate ArchiMate connectors in EAxCRM.qea (COM-only).")
    parser.add_argument("--qea", default=ga.DEFAULT_QEA)
    parser.add_argument("--md", default=ga.DEFAULT_MD)
    parser.add_argument("--state-dir", default=SCRIPT_DIR,
                        help="Directory for the guid-map file (default: script dir).")
    parser.add_argument("--apply", action="store_true",
                        help="Execute deletions. Without this flag the script "
                             "prints the plan only (dry-run).")
    args = parser.parse_args()

    ga.GUID_MAP_PATH = os.path.join(args.state_dir, "archimate_guid_map.json")

    elements, relations = ga.parse_md(args.md)
    print(f"Parsed {len(elements)} elements, {len(relations)} relationships")

    guid_map = ga.load_guid_map()
    print(f"Loaded {len(guid_map)} GUID mappings")

    try:
        import win32com.client  # noqa: F401
    except ImportError:
        print("FAIL: win32com not installed. Run: pip install pywin32")
        sys.exit(1)

    log("Opening EA session...")
    with ea_session.ea_repository(args.qea, technology="ArchiMate3") as repo:
        log("Scanning connectors...")
        plan, stats = scan_and_plan(repo, relations, elements, guid_map)
        print_plan(plan, stats)

        if not args.apply:
            print("\nDry-run only. Re-run with --apply to execute.")
            return

        if (stats["duplicates"] == 0
                and stats["legacy_adopted"] == 0
                and stats["retyped"] == 0):
            print("\nNothing to do.")
            return

        log("Applying plan...")
        apply_plan(repo, plan)

        # Backfill guid_map with survivor GUIDs so subsequent
        # generate_archimate.py runs hit Tier 1 immediately.
        for entry in plan:
            guid_map[entry["rel_key"]] = entry["survivor_guid"]
        ga.save_guid_map(guid_map)
        log("guid_map backfilled with survivor GUIDs.")

    print("\nDone.")


if __name__ == "__main__":
    main()
