# ArchiMate v2.0 Sync Blocker

## RESOLVED 2026-07-02
Root cause: `Dispatch("EA.Repository")` could attach to an already-registered
EA automation server (COM Running Object Table) instead of spawning an
isolated instance. Fixed by switching to `DispatchEx("EA.App")` + a
`Models.GetAt(0)` retry loop, in a new shared `modelgen/
ea_session.py` module used by every generator/sync script. v2.0 sync
confirmed live in EA: 66 elements, 91 relationships (not 90 — corrected
count), 1 diagram. See `AGENTS.md` "Bugfix: EA 61704 Error + Non-BPMN
Diagram Sizing/Layout (2026-07-02)" for full details.

## Date
2026-07-01

## What's Done
- Updated `models/EAxCRM-Archimate.md` to v2.0: 66 elements, 90 relationships
- Includes: Sales Management function, Vendor actor, 7 new business objects + data objects, 5 sales processes, Sales Management Service, 33 new relationships
- Updated stale Purchase Data/Purchase Record descriptions
- Updated `models/README.md` and `AGENTS.md` with new counts

## Blocker: `repo.Models.GetAt(0)` fails with EA internal error (61704)
Both `generate_archimate.py` and `generate_uml_datamodel.py` fail at the same point:
```
root = repo.Models.GetAt(0)
-> Internal application error (61704)
```

This happens after `repo.OpenFile()` and `repo.ActivateTechnology()` succeed. The error is NOT a file lock (same result with EA fully closed). Possible causes to investigate:
1. EA project file needs a version upgrade (the .qea might be from an older EA version)
2. COM API registration issue
3. The EA.exe version installed doesn't support the .qea file format

## Workaround Attempted
- Asked user to close EA → same error
- Tested `generate_uml_datamodel.py` → same error (rules out model-specific issue)
- All zombies cleaned up after each attempt

## Next Session
Start by diagnosing why `repo.Models` fails with internal error. Try:
1. Manually open `EAxCRM.qea` in EA to trigger any version upgrade prompt
2. Close EA, kill all EA.exe processes
3. Re-run the generator
