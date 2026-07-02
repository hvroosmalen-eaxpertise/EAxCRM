# Sparx EA Model (EAxCRM)

This directory contains the Sparx Enterprise Architect model files for the EAxCRM project. These files are **separate from the Django CRM app** and are managed independently.

## Files

| File | Description |
|---|---|---|
| `EAxCRM-Archimate.md` | ArchiMate model (Markdown, 71 elements, 107 relations, 1 diagram) |
| `EAxCRM-DataModel.md` | Data model (Markdown, 19 entities, 30 relationships) |
| `EAxCRM-Requirements.md` | Requirements model (Markdown, 39 requirements) |
| `EAxCRM-NewsletterProcess.md` | Newsletter BPMN process (Markdown, 26 elements, 2 lanes, 16 sequence flows) |
| `EAxCRM-SalesProcess.md` | Sales BPMN process (Markdown, 49 elements, 3 lanes, 25 sequence flows, 17 message flows, 22 data associations) |
| `EAxCRM-CustomerAccountProcess.md` | Manage Customer Account BPMN process (Markdown, 1 CollaborationModel, 1 Lane, 12 elements, 9 sequence flows, 6 data associations) — **not yet generated into EA**, design-only so far |
| `EAxCRM-ProcessModel.md` | Combined process model (Markdown, 71 elements, 98 connectors) — does not yet include the Customer Account process |
| `EAxCRM-SalesProcess-CRUD.md` | Sales process CRUD matrix — maps which activities create/read/update/delete each data object, cross-referenced to data model entities |
| `EAxCRM.qea` | Sparx EA project file (ArchiMate + data model + requirements + process architecture) |

## Generators

Data model and requirements generators use Sparx EA's COM API (`EA.Repository`) exclusively. The process model sync reads via direct SQLite (COM API doesn't detect elements added by another EA session). Each model has a **generator** (MD → EA) and/or a **sync** (EA → MD).

### ArchiMate Model
```
python experiments/modelgen/generate_archimate.py
```
Reads `EAxCRM-Archimate.md`, generates 71 elements and 107 relationships in an Application Layer diagram.

### Data Model (UML Class Diagram)
- **Generate** (MD → EA): `python experiments/modelgen/generate_uml_datamodel.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_datamodel_from_ea.py`
- 19 class entities with attributes, 30 associations with cardinality, named directionally

### Requirements Model
- **Generate** (MD → EA): `python experiments/modelgen/generate_requirements_from_md.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_requirements_from_ea.py`
- 39 requirements with ID/Alias, Status, Version, parent hierarchy (Aggregation connectors), entity mappings (Realisation connectors)

### Process Model (BPMN 2.0)
Two separate BPMN collaboration models, each with dedicated generators and sync scripts:

#### Newsletter Process
- **Generate** (MD → EA): `python experiments/modelgen/generate_newsletter_process_from_md.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_newsletter_process_from_ea.py`
- 1 CollaborationModel (EAxCRM Newsletter Process Architecture), 2 Lanes (EAxpertise, News Source), 26 elements, 16 SequenceFlows
- Uses `#### ` nesting format: elements under `### Lane—` headers store their lane membership via `Parent`
- MD Diagram GUID stored in collaboration element's `- Diagram GUID:` field

#### Sales Process
- **Generate** (MD → EA): `python experiments/modelgen/generate_sales_process_from_md.py`
- **Sync** (EA → MD): `python experiments/modelgen/sync_sales_process_from_ea.py`
- 1 CollaborationModel (EAxCRM Sales Process Architecture), 3 Lanes (Customer, EAxpertise, Vendor), 49 elements, 25 SequenceFlows, 17 MessageFlows, 11 DataOutputAssociations, 11 DataInputAssociations
- Uses flat `### ` format with `- Lane:` field on each element
- Flow references use element IDs (eids) for collision-safe round-trip
- v1.1: added `ConfirmCustomerAccount` IntermediateEvent (EAxpertise lane) between `CreateRFQ` and `RegisterRFQ`, referencing the Manage Customer Account process

#### Manage Customer Account Process
- **Generate/Sync**: not yet implemented — `EAxCRM-CustomerAccountProcess.md` is design-only (2026-07-02), following the same flat `### ` + `- Lane:` format as the Sales Process
- 1 CollaborationModel (Manage Customer Account), 1 Lane (EAxpertise — no self-service, always staff-driven), 12 elements, 9 SequenceFlows, 4 DataInputAssociations, 2 DataOutputAssociations
- Covers: create account from minimal data (org name + one Contact email), fuzzy-match duplicate detection with merge, email history retrieval via IMAP scan, and role-gated (Primary/License Holder) newsletter opt-in suggestion requiring explicit user confirmation

#### Combined Model
- **Sync**: `python experiments/modelgen/sync_process_from_ea.py` — reads ALL CollaborationModels
- Generates combined `EAxCRM-ProcessModel.md` (71 elements, 98 connectors) — stale until the Sales Process update and Customer Account process are generated into EA and re-synced

## ArchiMate Model

- **Layers**: Business, Application, Technology
- **Elements**: 71 (actors, roles, functions, processes, objects, components, services, data objects, nodes, artifacts)
- **Relations**: 107 (composition, assignment, realization, flow, access, serving, association, triggering)
- **Diagram**: Application Layer type with all elements arranged by layer; connectors use type properties (StereotypeEx + Connector_Type) rather than display names
- **v2.0**: Added Sales Management function, Vendor actor, 7 new business objects (Offer, Quote, Delivery, SalesInvoice, ProcurementInvoice, Service, Vendor) with corresponding data objects, service, and processes
- **v2.1**: Added Manage Customer Account function with 4 sub-processes (Create Customer Account, Flag Duplicate Accounts, Merge Customer Accounts, Retrieve Customer Email History), reusing existing Customer/Contact/Communication business objects; added a Triggering relation from Handle RFQ to Create Customer Account

See `AGENTS.md` for COM API interaction details, connector type mapping, and model state.
