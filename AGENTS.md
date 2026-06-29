# EAxCRM — Enterprise Architect Customer Relationship Manager

## Purpose
A CRM system for managing Sparx EA customers, their communications, and newsletter campaigns.

## MANDATORY: Model Sync Before Discussion
**Before ANY discussion or work involving the data model (entities, attributes, relationships), you MUST first run:**
```
python experiments\modelgen\sync_datamodel_from_ea.py
```
This reads the current state from `EAxCRM.qea` and updates `EAxCRM-DataModel.md`. Only then do you have the current model to discuss.

Without this sync, any conversation about the model is based on stale data. The EA repo is the canonical source — the MD file must reflect it before we proceed.

**After any sync that changes the model, you MUST update this AGENTS.md** to document new entities, renamed entities, new attributes, and new relationships. Review the diff of `EAxCRM-DataModel.md` and update the "Data Model Summary" section below.

## Modelling vs Implementation Level
Unless I say "implement in Django" or "update the models.py", we stay at **modelling level** — only the EA data model (`EAxCRM.qea`) and `EAxCRM-DataModel.md` are changed. No Django code, no database migrations, no Python model files. This avoids premature coupling between the logical model and the implementation.

## Core Features

### 1. Customer Insight
- Manage contacts with multiple roles per customer (Primary, Purchase, Sales, License Holder)
- Retrieve communications from 3-5 IMAP accounts (han@eaxpertise.nl, sales@eaxpertise.nl, info@eaxpertise.nl)
- Store documents related to customers (emails with PDF/TXT attachments, especially license communications)
- Name and email are the most important contact fields; contacts typically share one address per customer
- Track license entitlements per customer with start/expiry dates (typically end of month); licenses vary by type and have line items; some line items are services rented on a 12-month basis
- Track purchases per customer linked to quote and invoice PDFs stored on OneDrive
- Licenses can be renewals linked to a previous purchase
- A purchase can be a Product (with quote/invoice PDFs + license entitlements) or a Service (with name, start_month, expiry_month)
- Service expiry_month signals renewal needed; a renewal aggregates all expiring licenses and services for a customer

### 2. Sales Management
- Offer is a sales proposal to a customer with optional service line items
- Services (SaaS, Training, Support) can be procured (linked to Purchase) or EAxpertise's own
- Services can be part of an Offer; the actual line items sold are on the SalesInvoice
- SalesInvoice is the outgoing invoice to the customer, references the originating Offer
- ProcurementInvoice (was Invoice) is the incoming invoice from Sparx Systems — can be USD or EUR
- Offers are typically in EUR
- Service status, auto_renew, and renewal_notice_sent fields enable expiry notifications

### 3. Newsletter Management
- Create and send EAxNewsletter to opted-in contacts
- Compose from news sources: SparxSystems.com, sparxsystems.eu
- Newsletter format: logo + ~5 article pointers (heading + summary + link to full article)
- Targeted to Sparx EA users
- Send cadence: every 6 weeks
- Require manual review before sending (Draft → Review → Sent workflow)

## Tech Stack
| Layer | Choice |
|---|---|
| Framework | Python 3.13 + Django 6.0.6 |
| Database | SQLite (file-based, ideal for QNAP NAS) |
| IMAP | imaplib + email stdlib |
| PDF parsing | PyMuPDF (fitz) |
| Scraping | requests + BeautifulSoup (no AI) |
| UI | Django Admin (responsive, built-in) |
| Auth | Django built-in (local network only) |
| Deployment | Native dev on Windows → Docker on QNAP NAS (Phase 3) |

## Data Model Summary
**Current state (as of 2026-06-29):** 19 entities, 30 relationships

### Entities
| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| Customer | Organization that uses Sparx EA | name, address |
| Contact | Person associated with a customer, with role | name, email, role, opt_in |
| Quote | Incoming quote from Sparx Systems | quote_number, date, amount, pdf |
| ProcurementInvoice | Incoming invoice from supplier (was Invoice) | invoice_number, date, amount, currency |
| Purchase | Procurement event, links Quote → ProcurementInvoice | type, purchase_date |
| License | License entitlement per customer | license_type, start_date, expiry_date |
| LicenseLineItem | Line items under a license | description, is_service, quantity |
| Service | Resold service (procured or own) | service_name, service_type, unit_price, billing_frequency, start_month, expiry_month, cancelled_date, auto_renew, status |
| Offer | Sales proposal to customer | offer_number, date, amount, currency, status |
| SalesInvoice | Outgoing invoice to customer | invoice_number, date, amount, currency, paid |
| Vendor | Supplier organization (Sparx Systems, Prolaborate) | name, address, bank_account_holder, iban, bic_swift, payment_currency |
| Delivery | Handover email with license files, service agreements | sent_date, to_address, subject, body, status |
| Communication | Email from IMAP | subject, from_address, body, received_date |
| Attachment | File attached to a communication | filename, content_type, file |
| ImapAccount | IMAP config | email_address, host, username |
| Article | Scraped news article | source_url, heading, summary |
| NewsSource | Website scraped for articles | name, url |
| Newsletter | Composed EAxNewsletter | title, subject, status |
| NewsletterContact | Join: newsletter → contact | sent_date, opened_date, bounced |

### Procurement Flow
Quote → Purchase → ProcurementInvoice → License (via Purchase)
Vendor → Quote (*), Vendor → ProcurementInvoice (*)

### Sales Flow
Offer → SalesInvoice (Customer)
Service → Offer (optional)
Service → SalesInvoice (optional)
Service → Purchase (optional, if procured)
Service → Vendor (optional, if procured)
License → SalesInvoice (billed_on)
Delivery → SalesInvoice (fulfills)
Delivery → Customer (delivered_to)
Attachment → Delivery (included_in)

### Key Relationships
- Purchase → Customer (M:1), License (*) → Purchase (M:1)
- Service → Purchase (0..1, if procured)
- Service → Offer (0..1), Service → SalesInvoice (0..1)
- Service → Vendor (0..1, if procured)
- SalesInvoice → Customer (M:1), SalesInvoice → Offer (0..1)
- Offer → Customer (M:1)
- Vendor → Quote (*), Vendor → ProcurementInvoice (*)
- Vendor → License (*), Vendor → Service (*)
- Newsletter content sourced from SparxSystems.com and sparxsystems.eu
- Newsletter frequency: once per 6 weeks
- Opt-in required for newsletter contacts (initial opt-in via CRM-marked email addresses)
- Experiments for IMAP and PDF parsing done in isolated `experiments/` directory before integrating into main app
- Database field for passwords encrypted at rest
- No AI dependencies by design; optional small local LLM later if needed (ollama)

## Models (files in ../models/)
- `EAxCRM-Archimate.md` — ArchiMate model source of truth (Markdown, 44 elements, 57 relations, 1 diagram)
- `EAxCRM-Requirements.md` — Requirements model (Markdown, 33 requirements)
- `EAxCRM.qea` — Sparx EA project file (populated with ArchiMate model + data model + requirements)

## Active Context
- ArchiMate model fully generated with 44 elements, 57 relationships, 1 diagram
- ApplicationService Object_Type fixed to 'Activity' (confirmed correct shape in EA)
- Diagram preservation works: subsequent runs skip element placement, only update type/stereotype
- GUID map has 45 entries (44 elements + 1 diagram), saved to `archimate_guid_map.json`
- Remote configured: https://github.com/hvroosmalen-eaxpertise/EAxCRM (committed and pushed)
- Data model has 19 entities and 30 relationships — updated 2026-06-29
- Requirements model expanded from 8 to 34 requirements with IDs, Status, Version — updated 2026-06-29
- New entities: Vendor, Delivery; expanded: Service (+5 attributes then -2), Attachment (+delivery_id)
- New relationships: License→SalesInvoice (billed_on), Delivery→Customer (delivered_to), Delivery→SalesInvoice (fulfills), Attachment→Delivery (included_in)
- `generate_uml_datamodel.py` diagram phase now adds missing entities to existing diagram instead of skipping entirely

## Generator Scripts (experiments/modelgen/)
- `generate_archimate.py`: Reads `EAxCRM-Archimate.md` and generates/populates `EAxCRM.qea`
- Idempotent: saves GUID map to `archimate_guid_map.json`, re-runs update existing without duplicates
- 4-phase approach:
  - **Phase 1**: COM API for elements (create/update using `StereotypeEx`), MDG activation
  - **Phase 1b**: SQLite to fix `Object_Type`, `t_object.Stereotype` (short form), and `t_xref.Description` (FQName with `ArchiMate3::`)
  - **Phase 2**: COM API for relationships (create connectors, set `StereotypeEx`, `SupplierID`)
  - **Phase 3**: COM API for diagram objects + SQLite for diagram type/stereotype/t_xref

### Element Object_Type Mapping
Controls the UML base type shape in Sparx EA. Set via `ELEMENT_BASE_TYPE` in the generator:

| ArchiMate Type    | Object_Type | Shape Purpose              |
|-------------------|-------------|----------------------------|
| BusinessActor     | Class       | Default UML class shape    |
| BusinessRole      | Class       | Default UML class shape    |
| BusinessFunction  | Activity    | Rounded-corner activity    |
| BusinessProcess   | Activity    | Rounded-corner activity    |
| BusinessObject    | Class       | Default UML class shape    |
| BusinessService   | Class       | Default UML class shape    |
| ApplicationComponent | Component | UML component shape (two small rectangles) |
| ApplicationCollaboration | Class | Ellipse shape |
| ApplicationInterface | Interface | UML interface shape (circle) |
| ApplicationService | Activity   | Rounded-corner activity    |
| ApplicationFunction | Class     | Default UML class shape    |
| DataObject        | Class       | Default UML class shape    |
| Node              | Node        | UML node shape (3D box)    |
| Device            | Device      | UML device shape           |
| SystemSoftware    | Class       | Default UML class shape    |
| TechnologyService | Class       | Default UML class shape    |
| Artifact          | Class       | Uses MDG stereotype for visual |
| Grouping          | Class       | Default UML class shape    |
| Location          | Class       | Default UML class shape    |

### Stereotype Storage (t_object column vs t_xref)
- `t_object.Stereotype` stores the **short name** (e.g. `ArchiMate_BusinessActor`)
- `t_xref.Description` stores the FQName with the MDG prefix:
  ```
  @STEREO;Name=ArchiMate_BusinessActor;FQName=ArchiMate3::ArchiMate_BusinessActor;@ENDSTEREO;
  ```
  - `Type` = `'Stereotypes'`, `Visibility` = `'element property'`, `Client` = element `ea_guid`

### Connector Type Mapping (ArchiMate → Sparx EA)
| ArchiMate | Connector_Type | Stereotype `(t_xref FQName: ArchiMate3::...)` |
|---|---|---|
| Composition | Aggregation | ArchiMate_Composition |
| Aggregation | Aggregation | ArchiMate_Aggregation |
| Assignment | Association | ArchiMate_Assignment |
| Realization | Realisation | ArchiMate_Realization |
| Association | Association | ArchiMate_Association |
| Triggering | Association | ArchiMate_Triggering |
| Flow | Association | ArchiMate_Flow |
| Serving | Association | ArchiMate_Serving |
| Access | Association | ArchiMate_Access |
| Influence | Association | ArchiMate_Influence |

### Diagram Configuration
- `Diagram_Type` = `'ArchiMateBusiness'`
- `t_diagram.Stereotype` = `'ArchiMate_ArchimateDiagram'`
- `t_xref` (Visibility='diagram property'): `@STEREO;Name=ArchiMate_ArchimateDiagram;FQName=ArchiMate3::ArchiMate_ArchimateDiagram;@ENDSTEREO;`

### Diagram Preservation
- On first creation, diagram GUID is saved to `archimate_guid_map.json` with key `_diagram_eax_archimate`
- On re-runs, generator loads diagram by GUID (or falls back to name lookup)
- If diagram already exists (by GUID or name), element placement is skipped — preserves manual layout
- Only diagram type/stereotype/t_xref are updated on re-runs

## Critical Context: COM API + SQLite Interactions
- All model operations go through COM API (elements, relationships, diagram). Direct SQLite is used only as a workaround for COM API limitations:
  - Phase 1b: Fix `Object_Type` and `t_xref.Description` via SQLite (COM API `AddNew` doesn't always set the right base type, and `StereotypeEx` leaves `t_xref.Description` NULL for elements)
- `repo.CloseFile()` can hang; use try/finally with except: pass
- EA processes (EA.exe) accumulate between runs — script tracks pre-existing PIDs and only kills its own zombie EA processes after each phase
- **NEVER kill EA processes externally** (e.g. `Get-Process -Name EA | Stop-Process`). The user has EA open. Only the scripts' `kill_new_ea_processes()` may kill zombie processes, and it only kills PIDs that didn't exist before the script started.
- GUID map file: `experiments/modelgen/archimate_guid_map.json`

## Markdown Model File Format
The generator reads `.md` files with the following structure:

```markdown
## Elements

### Type—ID
- Name: Element Name
- Description: Description text
- GUID: {00000000-0000-0000-0000-000000000000}
- Layer: Business | Application | Technology | Composite

## Relationships

### Type—ID
- Source: source_element_id
- Target: target_element_id
- GUID: {00000000-0000-0000-0000-000000000000}
```

Where `Type` matches one of the ArchiMate types listed in `ARCHIMATE_ELEMENT_STEREOTYPES` or `ARCHIMATE_RELATION_STEREOTYPES` in the generator.

## Bugfix: Attribute Deletion via Collection Index (2026-06-25)
`sync_attributes()` used `a.AttributeID` with `Attributes.Delete()` which expects a 0-based collection index, not the EA internal ID. Caused "Index out of bounds" when removing attributes from Purchase (`service_name`, `start_month`, `expiry_month`).

**Fix**: Iterate in reverse index order so deletions don't shift indices:
```python
for i in range(ea_elem.Attributes.Count - 1, -1, -1):
    a = ea_elem.Attributes.GetAt(i)
    if a.Name not in md_names:
        ea_elem.Attributes.Delete(i)
```

## Bugfix: COM API Only — No SQLite Dependency (2026-06-25)
Three fixes in `generate_uml_datamodel.py`:

### Bug 1: Wrong connector direction in orphan detection
The orphan detection loop iterated `ea_elem.Connectors` and assumed `ea_elem` was the **source** element. But EA's COM API returns connectors where the element participates as **either** source or target. When iterating a target element's connectors, `conn.SupplierID` returned the target's own ID, making every connector appear self-referencing `(ElementGUID, ElementGUID)` — which never matched any MD pair, so all connectors were falsely identified as orphans.

**Fix**: Use `conn.ClientID` (actual source) and `conn.SupplierID` (actual target) to determine the true direction, regardless of which element's Connectors collection is being iterated.

### Bug 2: Orphan deletion via source element
Original code tried `ea_elem.Connectors.Delete(index)` on the iterated element, which is wrong when the iterated element is the target. COM API's `Connector.Delete()` method doesn't exist.

**Fix**: After collecting orphan `ConnectorID`s via COM API, locate each orphan by `ConnectorID` using `repo.GetConnectorByID()`, then delete from its true source element's `Connectors` collection.

### Fix 3: Cardinality via COM API instead of SQLite
Originally used `sqlite3.connect()` to write `SourceCard`/`DestCard` directly. EA COM API's `Connector.SourceCard`/`DestCard` are read-only, but `Connector.ClientEnd.Cardinality` and `Connector.SupplierEnd.Cardinality` can be set.

**Fix**: Removed `sqlite3` dependency entirely. Set cardinality via COM API using `conn.ClientEnd.Cardinality` and `conn.SupplierEnd.Cardinality`.

### Result
`generate_uml_datamodel.py` is now **pure COM API** — zero SQLite calls. Works with any EA repository backend (SQLite, SQL Server, Oracle, etc.).

### Round-Trip Test Results (2026-06-25)
Full delete/recreate orphan test passed:
1. Add `r-imapaccount-quote` to MD → sync → 17 connectors in EA ✓
2. Sync EA→MD → relationship appears in re-synced MD ✓
3. Remove relationship from MD → sync → 1 orphan deleted, back to 16 ✓
4. Final EA→MD sync → clean MD, no remnants ✓

## Process Architecture
- `EAxCRM-ProcessModel.md` holds the BPMN 2.0 process model (1 CollaborationModel, 32 elements, 35 SequenceFlows)
- Process Architecture package is at root level in the EA project
- `<<CollaborationModel>>` elements (Activity with CollaborationModel stereotype) describe logical processes
- `sync_process_from_ea.py` — reads BPMN 2.0 elements and SequenceFlow connectors from EA → MD (direct SQLite, since COM API doesn't detect elements added by another EA session)
- Sales process modelled: 3 Lanes (Customer, EAxpertise, Vendor), 21 Activities, 4 Events, 2 Gateways, 1 DataObject
- BPMN adornments mapped: taskType (Abstract/User/Manual), gatewayType, loopCharacteristics, etc. (see BPMN_TAGGED_VALUES dict)
- All 32 elements have descriptions
- Future: create `generate_process_from_md.py` for bidirectional sync

## Requirements Model
- `EAxCRM-Requirements.md` holds 33 requirements with ID, Status, Version, GUID, parent hierarchy, and entity mappings
- ID stored in EA's `t_object.Alias` field, synced via COM API
- Status and Version are standard EA `t_object` columns
- Entity → Requirement mappings use Realisation connectors (entity is source, requirement is target)
- 57 Realisation connectors link 29 entity mappings across all 33 requirements
- `sync_requirements_from_ea.py` — COM API only, reads from EA → MD (outputs `- Entities:` lines)
- `seed_requirements_properties.py` — COM API only, sets ID/Status/Version in EA from spec mapping
- `generate_requirements_from_md.py` — COM API only, creates/updates requirements in EA from MD, including parent Aggregation connectors, Realisation connectors to entities, and diagram placement (idempotent, saves GUID map)

## Generator Scripts (experiments/modelgen/)
- All scripts in this directory use the **EA COM API** (win32com.client.Dispatch) exclusively
- Direct SQLite writes to `EAxCRM.qea` are **FORBIDDEN** — EA must always be the access layer

### Attribute Type Mapping
- **MD → EA** (`generate_uml_datamodel.py`): `text` → `string`
- **EA → MD** (`sync_datamodel_from_ea.py`): `memo` → `string`
- EA's `memo` type is a structured tag artifact, not used — all text attributes use `string` in both EA and MD

## Next Steps
1. **TOMORROW: Test bidirectional sync** — make changes in EA, run `sync_datamodel_from_ea.py`, verify MD updates with correct notes/types/attributes; then run `generate_uml_datamodel.py` to push back, verify EA reflects changes
2. **Test entity → requirement Realisation connector round-trip**: delete/add entity mappings in MD, run generator, verify connectors update; modify in EA, run sync, verify MD updates
3. Build IMAP experiment, PDF parsing experiment
4. **Extend BPMN model** — add Pools, Lanes, Tasks, Events, Gateways to the CollaborationModel in EA, run `sync_process_from_ea.py` to verify MD output
5. **Create `generate_process_from_md.py`** — MD → EA generator for BPMN 2.0 process elements
