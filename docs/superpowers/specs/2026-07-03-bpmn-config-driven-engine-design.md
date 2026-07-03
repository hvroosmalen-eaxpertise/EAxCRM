# BPMN Config-Driven Generation/Sync Engine — Design

Addresses [issue #3](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/3) — "More generic, config-driven approach for BPMN diagram generation/sync" (verified via `gh issue view 3`).

## Problem

`experiments/modelgen/` has 3 `generate_*_process_from_md.py` scripts (654–735 lines: customeraccount, sales, newsletter) and 6 `sync_*_from_ea.py` scripts (172–336 lines), sharing ~80–95% duplicated logic: flat MD parsing, `BPMN_TAGGED_VALUES`, `LABEL_TO_STEREO`, `OBJECT_TYPE_MAP`, connector creation, diagram placement, GUID map handling. A diff of `generate_customeraccount_process_from_md.py` vs. `generate_sales_process_from_md.py` shows the files have already drifted from copy-paste divergence (sales has `get_or_create_package` and `####`-nested connector-section parsing that customeraccount lacks). A recent bug fix (missing `IntermediateEvent` tagged values, wrong `eventType`→`eventDefinition` key, missing `dataInOut` tag) had to be applied in parallel across 6 near-identical files — duplication is a live bug source, not just repetition.

`sync_process_from_ea.py` (323 lines) was found during investigation to be dead code — a generic, package-wide predecessor to the three per-process sync scripts, not imported or referenced anywhere else in the repo.

## Scope

**In scope:**
- Shared config (`bpmn_config.py`) and engine (`bpmn_engine.py`) covering both directions: MD→EA generate and EA→MD sync
- Single shared source of truth for `BPMN_TAGGED_VALUES`, `LABEL_TO_STEREO`, `OBJECT_TYPE_MAP`, `CONNECTOR_TYPES`/`CONNECTOR_STEREOTYPE_EX`
- Investigating and reconciling the sales/customeraccount feature drift (`get_or_create_package`, `####` nested connector sections) before extraction, so the engine's feature set reflects real per-process requirements
- Migrating all 3 generate scripts and their matching sync scripts to thin config + engine-call wrappers
- Deleting `sync_process_from_ea.py`
- A regression check (MD-output diff + element/connector count comparison) run per process during migration

**Out of scope:**
- ArchiMate / UML Data Model generators (`generate_archimate.py`, `generate_uml_datamodel.py`) — different, non-flat MD syntax; only continue sharing `diagram_utils.py`'s non-BPMN layout functions (`compute_grid_positions`, `compute_uml_class_*`), which they already do
- `sync_datamodel_from_ea.py`, `sync_requirements_from_ea.py` — not BPMN, unaffected
- Changing MD file formats or output structure — refactor must be behavior-preserving
- A full automated CI harness against a throwaway `.qea` copy — the Sandbox-package pattern already gives adequate isolation for this migration; a heavier CI harness is a separate future effort if desired

## Architecture

### `experiments/modelgen/bpmn_config.py`

`ProcessConfig` dataclass, one instance per process, holding everything that varies between scripts:

```python
@dataclass
class ProcessConfig:
    name: str                       # "Customer Account", "Sales", "Newsletter"
    package_name: str               # e.g. "Manage Customer Account Architecture"
    default_md: str                 # DEFAULT_MD path
    guid_map_file: str              # basename, resolved relative to SCRIPT_DIR
    collab_name: str                # exact name used by generate side
    collab_name_like: str           # SQL LIKE pattern used by sync side lookup
    diagram_name: str               # usually == collab_name, kept separate (sales differs)
    lane_ids_fallback: set[str]     # used when MD has no explicit Lane elements
    uses_nested_packages: bool      # whether get_or_create_package applies
    supports_hash4_sections: bool   # whether #### nested connector parsing applies
    tagged_value_overrides: dict | None = None  # rare per-process tag additions
```

Module-level instances: `CUSTOMER_ACCOUNT`, `SALES`, `NEWSLETTER`.

Also holds the shared constants currently copy-pasted 6+ times: `BPMN_TAGGED_VALUES`, `LABEL_TO_STEREO`, `OBJECT_TYPE_MAP`, `CONNECTOR_TYPES`, `CONNECTOR_STEREOTYPE_EX`, `CONNECTOR_STEREOTYPES_SHORT`.

### `experiments/modelgen/bpmn_engine.py`

Parsing/writing logic, parameterized by `ProcessConfig` instead of module-level constants:

- `parse_md(config) -> (elements, connectors)` — MD parser, `####` handling gated by `config.supports_hash4_sections`
- `generate(config, qea_path, md_path=None)` — full EA-write flow: open repo → find/create package (nested or flat, per `config.uses_nested_packages`) → create/update elements → set tagged values → create connectors → place diagram → set line style → save GUID map → close repo
- `sync_to_md(config, qea_path, md_path=None)` — EA→MD flow (SQLite read → MD write)

Absorbs the BPMN-specific layout functions currently in `diagram_utils.py` (`compute_bpmn_lane_positions`, `compute_bpmn_element_positions`, `compute_bpmn_flow_layout`, `sort_by_flow_order`, `find_longest_path`, `get_lane_from_fields`) — consolidates "BPMN stuff" in one place. Non-BPMN layout functions (`compute_grid_positions`, `compute_uml_class_*`, `repair_zero_size_objects`, etc.) stay in `diagram_utils.py`, shared with ArchiMate/UML generators as today.

### Per-process scripts shrink to config + thin CLI wrapper

Example, `generate_customeraccount_process_from_md.py` (~15 lines instead of ~650):

```python
import argparse
import bpmn_engine
from bpmn_config import CUSTOMER_ACCOUNT

def main():
    parser = argparse.ArgumentParser(description="Generate Manage Customer Account process in EA")
    parser.add_argument("--qea", default=r"M:\EAxCRM\models\EAxCRM.qea")
    parser.add_argument("--md", default=CUSTOMER_ACCOUNT.default_md)
    args = parser.parse_args()
    bpmn_engine.generate(CUSTOMER_ACCOUNT, args.qea, args.md)

if __name__ == "__main__":
    main()
```

Same pattern for the 3 sync scripts, calling `bpmn_engine.sync_to_md(config, ...)`.

### Error handling

Unchanged from today — same try/except-around-COM-calls, same GUID-map fallback chains, same `ea_session.kill_new_ea_processes` cleanup. The refactor relocates this logic; it does not change behavior. No new failure modes should be introduced — the regression check below exists specifically to catch any that slip in.

## Testing & migration sequence

Pilot process: **Customer Account** (smallest, simplest MD structure — flat `###`, single lane; forces the config schema to handle the simple case cleanly before layering in sales' complexity).

1. Investigate the sales/customeraccount drift: determine whether customeraccount's MD genuinely never needs `####` nested sections / `get_or_create_package`, or whether that's a latent gap. Resolve before extraction.
2. Build `bpmn_config.py` + `bpmn_engine.py` against Customer Account's confirmed requirements.
3. Build a disposable pilot script targeting the `Sandbox` package (own GUID map, e.g. `sandbox_customeraccount_guid_map.json`) instead of `Process Architecture`, reusing the real `EAxCRM-CustomerAccountProcess.md` as input — per the established Sandbox-testing pattern, only the target package changes. Run and visually verify in EA (elements, tagged values, connectors, diagram layout) with no risk to the real, manually-tuned diagram.
4. Once confirmed, run the new engine for real via the (now-thin) `generate_customeraccount_process_from_md.py` against `Process Architecture`. Compare element/connector counts and GUID map contents against a pre-refactor baseline run — confirm no unexpected GUID churn.
5. Do the same for `sync_customeraccount_process_from_ea.py` → confirm the regenerated MD is byte-identical to the pre-refactor committed MD (`git diff` shows no changes).
6. The count/MD-diff comparison from steps 4–5 becomes the reusable regression check for porting the remaining processes.
7. Port Sales and Newsletter the same way (Sandbox dry-run → real run → diff check).
8. Delete `sync_process_from_ea.py`.

Sandbox scripts stay disposable and uncommitted. Only `bpmn_config.py`, `bpmn_engine.py`, and the shrunk per-process scripts are committed.
