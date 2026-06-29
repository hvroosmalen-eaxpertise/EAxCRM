# Sparx EA Model (EAxCRM)

This directory contains the Sparx Enterprise Architect model files for the EAxCRM project. These files are **separate from the Django CRM app** and are managed independently.

## Files

| File | Description |
|---|---|---|
| `EAxCRM-Archimate.md` | ArchiMate model (Markdown, 44 elements, 57 relations, 1 diagram) |
| `EAxCRM-DataModel.md` | Data model (Markdown, 19 entities, 30 relationships) |
| `EAxCRM-Requirements.md` | Requirements model (Markdown, 34 requirements) |
| `EAxCRM-ProcessModel.md` | BPMN 2.0 process model (Markdown, 3 lanes, 45 elements, 59 sequence flows) |
| `EAxCRM.qea` | Sparx EA project file (ArchiMate + data model + requirements + process architecture) |

## Generators

Data model and requirements generators use Sparx EA's COM API (`EA.Repository`) exclusively. The process model sync reads via direct SQLite (COM API doesn't detect elements added by another EA session). Each model has a **generator** (MD → EA) and/or a **sync** (EA → MD).

### ArchiMate Model
```
python experiments/modelgen/generate_archimate.py
```
Reads `EAxCRM-Archimate.md`, generates 44 elements and 57 relationships in an Application Layer diagram.

### Data Model (UML Class Diagram)
- **Generate** (MD → EA): `python experiments/modelgen/generate_uml_datamodel.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_datamodel_from_ea.py`
- 19 class entities with attributes, 30 associations with cardinality, named directionally

### Requirements Model
- **Generate** (MD → EA): `python experiments/modelgen/generate_requirements_from_md.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_requirements_from_ea.py`
- 34 requirements with ID/Alias, Status, Version, parent hierarchy (Aggregation connectors), entity mappings (Realisation connectors)

### Process Model (BPMN 2.0)
- **Sync** (EA → MD): `python experiments/modelgen/sync_process_from_ea.py`
- Reads CollaborationModel elements with Pools, Lanes, Activities, Events, Gateways, DataObjects, and SequenceFlow connectors
- Also reads nested diagram names from `t_diagram` for each CollaborationModel
- 1 CollaborationModel element (Sales Process Architecture) with 3 Lanes (Customer, EAxpertise, Vendor), 45 elements, 59 sequence flows

## ArchiMate Model

- **Layers**: Business, Application, Technology
- **Elements**: 44 (actors, roles, processes, objects, components, services, data objects, nodes, artifacts)
- **Relations**: 57 (composition, assignment, realization, flow, access, serving, association)
- **Diagram**: Application Layer type with all 44 elements arranged by layer; connectors use type properties (StereotypeEx + Connector_Type) rather than display names

See `AGENTS.md` for COM API interaction details, connector type mapping, and model state.
