# Sparx EA Model (EAxCRM)

This directory contains the Sparx Enterprise Architect model files for the EAxCRM project. These files are **separate from the Django CRM app** and are managed independently.

## Files

| File | Description |
|---|---|---|
| `EAxCRM-Archimate.md` | ArchiMate model (Markdown, 71 elements, 107 relations, 1 diagram) |
| `EAxCRM-DataModel.md` | Data model (Markdown, 19 entities, 30 relationships) |
| `EAxCRM-Requirements.md` | Requirements model (Markdown, 41 requirements) |
| `EAxCRM-NewsletterProcess.md` | Newsletter BPMN process (Markdown, 26 elements, 2 lanes, 16 sequence flows) |
| `EAxCRM-SalesProcess.md` | Sales BPMN process (Markdown, 49 elements, 3 lanes, 25 sequence flows, 17 message flows, 22 data associations) |
| `EAxCRM-CustomerAccountProcess.md` | Manage Customer Account BPMN process (Markdown, 1 CollaborationModel, 1 Lane, 14 elements, 10 sequence flows, data associations) — generated into EA (2026-07-03) |
| `EAxCRM-SalesProcess-CRUD.md` | Sales process CRUD matrix — maps which activities create/read/update/delete each data object, cross-referenced to data model entities |
| `EAxCRM-CustomerAccountUI.md` | Manage Customer Account UI wireframes (Markdown, 4 screens, 26 controls, 3 navigation links) — generated into EA (2026-07-06, issue #4) |
| `EAxCRM.qea` | Sparx EA project file (ArchiMate + data model + requirements + process architecture + wireframes) |

## Generators

Data model and requirements generators use Sparx EA's COM API (`EA.Repository`) exclusively. The process model sync reads via direct SQLite (COM API doesn't detect elements added by another EA session). Each model has a **generator** (MD → EA) and/or a **sync** (EA → MD).

### ArchiMate Model
```
python experiments/modelgen/generate_archimate.py
```
Reads `EAxCRM-Archimate.md`, generates the elements and relationships in the single "EAxCRM ArchiMate" diagram.

### Data Model (UML Class Diagram)
- **Generate** (MD → EA): `python experiments/modelgen/generate_uml_datamodel.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_datamodel_from_ea.py`
- 19 class entities with attributes, 30 associations with cardinality, named directionally

### Requirements Model
- **Generate** (MD → EA): `python experiments/modelgen/generate_requirements_from_md.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_requirements_from_ea.py`
- 41 requirements with ID/Alias, Status, Version, parent hierarchy (Aggregation connectors), entity mappings (Realisation connectors)
- Notes field composes Description + optional `Rationale:` / `Test Cases:` sections; Rationale/Test Cases are also stored as EA Tagged Values (added 2026-07-07, issue #7)
- Naming convention: lead with the GUI component (`ScreenName: ...`) for screen-specific requirements, or a `<Rule Name> Rule: ...` for cross-cutting business rules — not a restated full-sentence "must" statement

### Wireframe Model (issue #4)
- **Generate** (MD → EA): `python experiments/modelgen/generate_customeraccount_ui_from_md.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_customeraccount_ui_from_ea.py`
- Thin config + CLI wrapper around a shared engine, same split as BPMN:
  `experiments/modelgen/wireframe_config.py` (per-flow `WireframeFlow` +
  Wireframing MDG vocabulary) and `experiments/modelgen/wireframe_engine.py`
  (parsing, generation, sync) — see the `ea-wireframe-creator` skill for the
  full layout/toolbox rules. Each Screen gets its own EA Webpage Wireframe
  diagram (explicit per-control bounds, no computed layout) plus a shared
  sitemap overview diagram showing navigation between screens.

### Process Model (BPMN 2.0)
Three separate BPMN collaboration models. As of the issue #3 refactor
(2026-07-05), each process's `generate_*_process_from_md.py` /
`sync_*_process_from_ea.py` is a thin config + CLI wrapper around a shared
engine: `experiments/modelgen/bpmn_config.py` (per-process `ProcessConfig` +
shared BPMN vocabulary) and `experiments/modelgen/bpmn_engine.py` (parsing,
generation, sync, and BPMN-specific layout — see the `ea-bpmn-creator`
skill for the full layout/routing rules).

#### Newsletter Process
- **Generate** (MD → EA): `python experiments/modelgen/generate_newsletter_process_from_md.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_newsletter_process_from_ea.py`
- 1 CollaborationModel (EAxCRM Newsletter Process Architecture), 2 Lanes (EAxpertise, News Source), 26 elements, 16 SequenceFlows
- Uses `#### ` nesting format: elements under `### Lane—` headers store their lane membership via `Parent`
- MD Diagram GUID stored in collaboration element's `- Diagram GUID:` field

#### Sales Process
- **Generate** (MD → EA): `python experiments/modelgen/generate_sales_process_from_md.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_sales_process_from_ea.py`
- 1 CollaborationModel (EAxCRM Sales Process Architecture), 3 Lanes (Customer, EAxpertise, Vendor), 50 elements, 25 SequenceFlows, 17 MessageFlows, 11 DataOutputAssociations, 11 DataInputAssociations
- Uses flat `### ` format with `- Lane:` field on each element
- Flow references use element IDs (eids) for collision-safe round-trip
- v1.1: added `ConfirmCustomerAccount` IntermediateEvent (EAxpertise lane) between `CreateRFQ` and `RegisterRFQ`, referencing the Manage Customer Account process

#### Manage Customer Account Process
- **Generate** (MD → EA): `python experiments/modelgen/generate_customeraccount_process_from_md.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_customeraccount_process_from_ea.py`
- 1 CollaborationModel (Manage Customer Account), 1 Lane (EAxpertise — no self-service, always staff-driven), 14 elements, 10 SequenceFlows, plus Data Input/Output Associations
- Covers: create account from minimal data (org name + one Contact email), fuzzy-match duplicate detection with merge, email history retrieval via IMAP scan, and role-gated (Primary/License Holder) newsletter opt-in suggestion requiring explicit user confirmation

## ArchiMate Model

- **Layers**: Business, Application, Technology
- **Elements**: 71 (actors, roles, functions, processes, objects, components, services, data objects, nodes, artifacts)
- **Relations**: 107 (composition, assignment, realization, flow, access, serving, association, triggering)
- **Diagram**: Application Layer type with all elements arranged by layer; connectors use type properties (StereotypeEx + Connector_Type) rather than display names
- **v2.0**: Added Sales Management function, Vendor actor, 7 new business objects (Offer, Quote, Delivery, SalesInvoice, ProcurementInvoice, Service, Vendor) with corresponding data objects, service, and processes
- **v2.1**: Added Manage Customer Account function with 4 sub-processes (Create Customer Account, Flag Duplicate Accounts, Merge Customer Accounts, Retrieve Customer Email History), reusing existing Customer/Contact/Communication business objects; added a Triggering relation from Handle RFQ to Create Customer Account

See `AGENTS.md` for COM API interaction details, connector type mapping, and model state.
