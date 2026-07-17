---
title: EA Sync Scripts — COM dispatching and GUID handling
tags: [sparx-ea, com-api, modelgen, sync]
summary: Older sync scripts use raw DispatchEx without ea_session context manager; generators handle stale GUID maps via name-based fallback
created: 2026-07-08
updated: 2026-07-08
importance: medium
---

## COM dispatching

Two approaches exist in `modelgen/`:

| Approach | Used by | Notes |
|----------|---------|-------|
| `ea_session.ea_repository()` | BPMN generators/syncs, wireframe engine | Has `DispatchEx` retry + `Models.GetAt(0)` retry + zombie cleanup |
| Raw `win32com.client.DispatchEx("EA.App")` | `sync_requirements_from_ea.py`, `sync_ldm_from_ea.py` | Can hang on `OpenFile` if zombie EA processes exist; no retry logic |

The older scripts (`sync_requirements_from_ea.py` and `sync_ldm_from_ea.py`) predate `ea_session.py` and lack its robustness. If they hang, kill zombie EA processes manually or wait for the next `ea_session`-based script's cleanup.

## GUID map staleness

If elements are deleted and recreated in EA (e.g., newsletter element GUIDs regenerated), the GUID map becomes stale. Generators handle this via **name-based fallback**: if an element's GUID isn't found in the map, the generator does a name lookup against EA elements and updates the map. This is safe but means the first post-recreation run will "re-create" elements until it discovers them by name.

Key GUID map files and their purpose:

| Map file | Purpose | Entries |
|----------|---------|---------|
| `newsletter_guid_map.json` | Newsletter BPMN elements | 3 (collab model + diagram + element dict) |
| `sales_guid_map.json` | Sales BPMN elements | 3 (same pattern) |
| `customeraccount_guid_map.json` | Customer Account elements | 3 (same pattern) |
| `requirements_guid_map.json` | Requirement elements | 75 (one per requirement) |
| `ldm_guid_map.json` | LDM (UML Class) entities | 24 (one per entity) |
| `archimate_guid_map.json` | ArchiMate elements | 73 (one per element) |
| `customeraccount_ui_guid_map.json` | Wireframe screens | 2 (one per screen + navigation) |
