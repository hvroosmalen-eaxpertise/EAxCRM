# Sparx EA Model (EAxCRM)

This directory contains the Sparx Enterprise Architect model files for the EAxCRM project. These files are **separate from the Django CRM app** and are managed independently.

## Files

| File | Description |
|---|---|
| `EAxCRM-Archimate.md` | ArchiMate model source of truth (Markdown, 44 elements, 57 relations) |
| `EAxCRM.qea` | Sparx EA project file (populated ArchiMate model + data model) |

## Generator

The Markdown model drives a generator that syncs into the `.qea` Sparx EA project:

```
python experiments/modelgen/generate_archimate.py
```

The generator uses Sparx EA's COM API (`EA.Repository`) for element/diagram creation and direct SQLite writes for connector stereotypes (COM API does not persist `StereotypeEx` on connectors).

## ArchiMate Model

- **Layers**: Business, Application, Technology
- **Elements**: 44 (actors, roles, processes, objects, components, services, data objects, nodes, artifacts)
- **Relations**: 57 (composition, assignment, realization, flow, access, serving, association)
- **Diagram**: Composite overview with all 44 elements arranged by layer

See `AGENTS.md` for COM API interaction details and connector type mapping.
