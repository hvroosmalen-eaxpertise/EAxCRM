# Sparx EA Model (EAxCRM)

This directory contains the Sparx Enterprise Architect model files for the EAxCRM project. These files are **separate from the Django CRM app** and are managed independently.

## Files

| File | Description |
|---|---|
| `EAxCRM-Archimate.md` | ArchiMate model source of truth (Markdown, 44 elements, 57 relations) |
| `EAxCRM-DataModel.md` | Data model (Markdown, 17 entities, 22 relationships) |
| `EAxCRM.qea` | Sparx EA project file (populated ArchiMate model + data model) |

## Generators

Both Markdown models drive generators that sync into the `.qea` Sparx EA project:

### ArchiMate Model
```
python experiments/modelgen/generate_archimate.py
```
Reads `EAxCRM-Archimate.md`, generates 44 elements and 57 relationships in an Application Layer diagram.

### Data Model (UML Class Diagram)
```
python experiments/modelgen/generate_uml_datamodel.py
```
Reads `EAxCRM-DataModel.md`, generates 17 class entities with attributes, 22 associations with cardinality, and a Logical diagram. The reverse sync reads EA and rewrites the Markdown:

```
python experiments/modelgen/sync_datamodel_from_ea.py
```

The generators use Sparx EA's COM API (`EA.Repository`) exclusively — no direct SQLite. Elements, connectors, and diagrams are all created via the EA interop (`EA.dll`) with `AddNew`, `StereotypeEx`, and `Update`.

## ArchiMate Model

- **Layers**: Business, Application, Technology
- **Elements**: 44 (actors, roles, processes, objects, components, services, data objects, nodes, artifacts)
- **Relations**: 57 (composition, assignment, realization, flow, access, serving, association)
- **Diagram**: Application Layer type with all 44 elements arranged by layer; connectors use type properties (StereotypeEx + Connector_Type) rather than display names

See `AGENTS.md` for COM API interaction details and connector type mapping.
