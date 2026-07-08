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

## 🚫 MANDATORY: NEVER Kill EA Processes
**You must NEVER kill or stop any EA.exe process.** Not external tools, not PowerShell, not taskkill, not Stop-Process, nothing. The user has EA open and may have unsaved diagram layout work.

The generator scripts (`generate_*.py`) have their own safe cleanup: they track PIDs that existed *before* the script started via `before_pids`, and only kill new PIDs that their own EA COM API invocation created. That is the ONLY acceptable EA process cleanup mechanism.

**Rule**: If you need to clear a lock on `EAxCRM.qea`, ask the user to close EA. Never touch EA processes yourself.

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
| Database | Production-grade, multi-user-capable RDBMS (engine TBD, 2026-07-08 — SQLite's single-writer model doesn't fit multi-user production; SQLite may still suit local dev) |
| IMAP | imaplib + email stdlib |
| PDF parsing | PyMuPDF (fitz) |
| Scraping | requests + BeautifulSoup (no AI) |
| UI | Django Admin (responsive, built-in) |
| Auth | Django built-in (local network only) |
| Deployment | Native dev on Windows → Docker on QNAP NAS (Phase 3) |

## Data Model Summary
**Current state (as of 2026-07-08):** 19 entities, 1 enumeration, 31 relationships

### Entities
| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| Customer | Organization that uses Sparx EA | name, address_mode, street_name/house_number/postal_code/city/country (street mode) or po_box (PO Box mode), notes |
| Contact | Person associated with a customer, with role | name, email, role (ContactRole), opt_in |
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
- Contact.role is typed against the ContactRole Enumeration (Primary, Purchase, Sales, License Holder, Secondary) rather than a plain string — see "Enumeration support" below
- Newsletter content sourced from SparxSystems.com and sparxsystems.eu
- Newsletter frequency: once per 6 weeks
- Opt-in required for newsletter contacts (initial opt-in via CRM-marked email addresses)
- Experiments for IMAP and PDF parsing done in isolated `experiments/` directory before integrating into main app
- Database field for passwords encrypted at rest
- No AI dependencies by design; optional small local LLM later if needed (ollama)

## Models (files in ../models/)
- `EAxCRM-Archimate.md` — ArchiMate model source of truth (Markdown, 71 elements, 107 relations, 1 diagram; v2.0 adds Sales Management, Vendor, and 7 new business objects; v2.1 adds Manage Customer Account function)
- `EAxCRM-Requirements.md` — Requirements model (Markdown, 41 requirements)
- `EAxCRM-CustomerAccountProcess.md` — Manage Customer Account BPMN process (Markdown, 13 elements, 9 sequence flows, data associations)
- `EAxCRM.qea` — Sparx EA project file (populated with ArchiMate model + data model + requirements + 3 BPMN processes + wireframe diagrams)

## Active Context
- **Issue #7 follow-through (2026-07-08):** closed the remaining data-model checklist items from issue #7. (1) `Customer.address` decomposed into `address_mode` ("street"/"pobox") plus `street_name`/`house_number`/`postal_code`/`city`/`country` (street mode) or `po_box` (PO Box mode), matching CRM-7 and the already-built CreateAccountScreen wireframe. (2) `Contact.role` is now typed against a new **ContactRole Enumeration** (Primary, Purchase, Sales, License Holder, Secondary) instead of a plain `string(20)`. **Enumeration support is new** in `generate_uml_datamodel.py`/`sync_datamodel_from_ea.py` — a `### Enumeration—<id>` MD block with a `- Literals:` list round-trips as an EA `Object_Type='Enumeration'` element; literals are Attributes with `Type="int"`/`Stereotype="enum"` (matching EA's own built-in "Enumeration Name" template — confirmed by inspecting one live in the model). Note: EA's `Attribute.Classifier` COM property isn't accessible via dynamic dispatch in this setup (raises `AttributeError`) — enum-typed attributes are linked by matching `Attribute.Type` against the Enumeration's name (case-insensitively) on the EA→MD sync side, not via a real classifier reference. Reusable for other string fields with fixed value sets later (`Offer.status`, `Service.status`, etc.) if wanted. Issue #7's "Update CustomerAccountUI wireframe" and "new requirements" checklist items were already done in prior sessions; only "Implement Django form/view" remains, gated behind explicit Django-implementation instruction per the rule below.
- **Cross-check pass (2026-07-08):** audited DataModel/CustomerAccountProcess/Requirements/CustomerAccountUI + ArchiMate for missing relationships and descriptions. Fixed: (1) a real bug in `bpmn_engine.py` — the EA→MD sync truncated all element/collaboration Notes at 500 chars (`notes[:500]`, 3 spots), silently clipping several rich Why/What/How/Context descriptions mid-word; removed the slice and restored the 3 affected descriptions (ManageCustomerAccount collaboration, Contact DataObject, Retrieve Customer Email History activity) in `EAxCRM-CustomerAccountProcess.md`. (2) Added missing `Description` fields to 14 data-model relationships that had none (contact-customer, communication-imapaccount, attachment-communication, article-newssource, article-newsletter, newslettercontact-newsletter/contact, purchase-customer, license-customer, licenselineitem-license, attachment-delivery, delivery-customer, delivery-salesinvoice, license-salesinvoice). (3) Enriched Contact/Customer/Communication entity descriptions to document known-but-unimplemented gaps: Contact.role has no enforced enum (Primary/Purchase/Sales/License Holder/Secondary per CRM-1/CRM-10, plain string(20) today); Customer.address is still a single unstructured string despite CRM-7 requiring structured street/PO-Box fields; Communication.linked_to_contact is a boolean flag only — CRM-2 needs a real FK to Contact/Customer, which doesn't exist yet. **Not yet fixed (flagged for a decision):** the ArchiMate Technology layer (`e-sw-sqlite`, `e-art-db`) still names/describes SQLite as the production DB, contradicting the TEC-1 decision above; `e-process-optinsuggest` (Suggest Newsletter Opt-in) has no ApplicationService Realization unlike its 4 sibling Manage-Customer-Account business processes; no formal CRM-13+ requirements exist yet for the process-level behaviors (dedupe/merge/email-history/opt-in-suggest) or for the new "Find by Domain" UI feature — only the screen-level field rules (CRM-6..12) are captured.
- **Architecture decision (2026-07-08):** production database moves off SQLite to a production-grade, multi-user-capable RDBMS — SQLite's single-writer model doesn't fit reliable concurrent multi-user access. Engine intentionally not yet chosen (kept technology-abstract). Django stays as the framework (this was specifically about the DB, not the framework — a C# desktop client + remote DB + services alternative was discussed and set aside once the actual friction, SQLite, was identified). SQLite may still be fine for local dev. TEC-1 requirement revised accordingly (GUID unchanged, eid renamed `eaxcrmmustuseaproductiongrademultiusercapablerelationaldatabase`); README.md/AGENTS.md Tech Stack tables updated to match. **Sequencing:** continue modelling first; implementation (Django app, incremental, one BPMN process at a time) comes later once the model is mature enough.
- CreateAccountScreen wireframe redesigned (2026-07-08) to catch up with CRM-6..12 (issue #7) plus a user-requested "Find by Domain" email-lookup block — see `docs/superpowers/specs/2026-07-07-createaccountscreen-redesign-design.md` for the full design and its data-model cross-check (flags `Customer.address` needing decomposition into structured fields, and `Contact.role` needing a documented enum). Generated into scratch files (`models/EAxCRM-scratch-createaccountscreen*.qea`, not the real `EAxCRM.qea`) for review — not yet committed or applied to the real model.
- ArchiMate model v2.0 **confirmed synced live in EA** (2026-07-02, after fixing the 61704 blocker) — 66 elements, 91 relationships, 1 diagram — added Sales Management function, Vendor actor, Offer/Quote/Delivery/SalesInvoice/ProcurementInvoice/Service/Vendor business objects
- ApplicationService Object_Type fixed to 'Activity' (confirmed correct shape in EA)
- Diagram preservation works: subsequent runs skip element placement, only update type/stereotype
- GUID map has 67 entries (66 elements + 1 diagram), saved to `archimate_guid_map.json`
- Remote configured: https://github.com/hvroosmalen-eaxpertise/EAxCRM (committed and pushed)
- Data model has 19 entities and 30 relationships — updated 2026-07-08
- Requirements model expanded from 8 to 34 requirements with IDs, Status, Version — updated 2026-07-08
- Requirements model expanded from 39 to 41 requirements (CRM-6 through CRM-12) — 2026-07-07, covering the Create Customer Account screen's field/validation rules (issue #7). Notes field now composes Description + Rationale + Test Cases sections; Rationale/TestCases are also stored as EA Tagged Values for structured access. Naming convention for new requirements: lead with the GUI component name (e.g. `CreateAccountScreen: ...`) when the requirement is screen-specific, or a business-rule name (e.g. `Primary Contact Rule: ...`) when it's a cross-cutting domain rule — not a restated full-sentence "must" requirement.
- **Note:** this reuses the CRM-6..CRM-9 ID range that a 2026-07-02 planning note (see "Requirements Model" below) had reserved for the Manage Customer Account *BPMN process*-level requirements (dedupe/merge/email-history/opt-in-suggestion). Those were never actually generated into EA, so no real collision occurred, but that reservation is now stale — when those process-level requirements are eventually written, use CRM-13 onward (and a fresh SAL-5, since SAL namespace is untouched).
- New entities: Vendor, Delivery; expanded: Service (+5 attributes then -2), Attachment (+delivery_id)
- New relationships: License→SalesInvoice (billed_on), Delivery→Customer (delivered_to), Delivery→SalesInvoice (fulfills), Attachment→Delivery (included_in)
- `generate_uml_datamodel.py` diagram phase now adds missing entities to existing diagram instead of skipping entirely
- Newsletter process parser fixed: `### ` handler now captures elements (was resetting `current=None`, losing all `### ` items)
- Sync script deduplicates SequenceFlows by (src_id, tgt_id, name) — removed 16 duplicate flow lines from MD
- Newsletter model complete: 26 elements, 2 Lanes, 16 SequenceFlows, 39 total connectors, 7 scraping pipeline elements added
- Sales process model complete: 49 elements (3 Lanes, 27 activities, 5 events, 3 gateways, 11 DataObjects), 25 SequenceFlows, 17 MessageFlows, 11 DataIO associations each — 1 CollaborationModel included in the sync count of 50
- `diagram_utils.py` created: shared module for BPMN lane layout and diagonal layout across all generators
- `generate_sales_process_from_md.py` created: full connector support (SequenceFlow, MessageFlow, DataInput/OutputAssoc), BPMN lane layout via diagram_utils
- `EAxCRM-SalesProcess.md` created: flat `### ` structure with `- Lane:` fields on all 41 non-lane elements
- Connector duplicate detection fixed: checks both short-form (SequenceFlow) and long-form (BPMN2.0::SequenceFlow) stereotypes

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
- **Zombie cleanup is MANDATORY** after every generator run: run `Get-Process -Name EA | Stop-Process -Force` to clean up zombie EA processes that the generator created. Zombies lock the `.qea` file and prevent EA from starting.
- **Exception:** Always ask the user first if they have a real EA session open. Never kill if the user is actively working in EA.
- The generator scripts' `kill_new_ea_processes()` handles intra-run cleanup safely (only kills PIDs that didn't exist before the script started).
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

## Bugfix: safe_id Case Collision (2026-06-30)
All four BPMN scripts (`sync_sales_process_from_ea.py`, `sync_newsletter_process_from_ea.py`, `generate_sales_process_from_md.py`, `generate_newsletter_process_from_md.py`) had `safe_id()` lowercasing names via `name.lower()`, causing distinct elements with same name but different capitalization (e.g. Gateway "Accept Offer" vs Activity "Accept Offer") to collide to the same dict key.

**Fix**: Changed `safe_id()` from `re.sub(r"[^a-z0-9]", "", name.lower())` to `re.sub(r"[^a-zA-Z0-9]", "", name)` — preserves case so `"AcceptOffer"` and `"acceptoffer"` produce different keys.

**Collision handling in sync_sales_process_from_ea.py**: When two elements generate the same `safe_id(name)`, append `_TypeSuffix` for uniqueness. The eid is used in both `### Type—eid` headers AND flow references for consistent round-trip. Flow references now use eids (not element names) throughout the sales MD. This affected 2 of 45 elements (Gateway and Activity both named "Accept Offer").

**Side effect**: The underscore `_` in suffixed eids (`AcceptOffer_Activity`) is stripped by `safe_id()`, so dict keys become `AcceptOfferActivity` — resolves correctly against flow text.

**Impact**: Sales GUID map had 86 stale entries from earlier buggy runs. Reset to empty, generator ran clean with 0 created, 45 updated (all via name-based fallback since GUID map was empty). Idempotent re-run confirmed.

## Bugfix: LineStyle 5 is Tree Horizontal, not Orthogonal Rounded (2026-07-01)

Both sales and newsletter BPMN generators used `dl.LineStyle = 5` with comment `# Orthogonal Rounded`. EA's `LineStyle=5` is actually **Tree Horizontal**. Orthogonal Rounded is `LineStyle = 9`.

**Fix**: Changed both generators to `dl.LineStyle = 9`. Updated `ea-diagram-creator` skill with the full LineStyle enum table to prevent recurrence.

## BPMN Element Sizing: Type-Appropriate Bounds (2026-07-01)

**Approach**: All four bounds (`left`, `top`, `right`, `bottom`) are set on every diagram object (matching the Sales Process generator convention). EA renders each BPMN stereotype at its native visual shape within these bounds.

**BPMN element dimensions** in `BPMN_ELEMENT_SIZES` (`diagram_utils.py`):

| BPMN Type | Width | Height |
|-----------|-------|--------|
| Activity/Task | 110 | 60 |
| StartEvent/EndEvent/IntermediateEvent | 30 | 30 |
| Gateway (all variants) | 42 | 42 |
| DataObject/DataStore/Artifact | 35 | 50 |
| TextAnnotation | 80 | 50 |

**Grid**: Elements are arranged left-to-right in rows within each lane, centered within uniform grid cells (using `elem_width + h_gap` spacing, default 180+30=210). Each element uses its own width/height for the bounding box, not the grid cell size. Smaller types are visually centered within their cell.

**Two key changes**:
1. `_place_diagram_object()` sets `right` and `bottom` (was left/top-only on 2026-06-30)
2. `compute_bpmn_element_positions()` now accepts `elem_types` parameter — a dict of `{eid: label_string}` — to look up per-element sizes from `BPMN_ELEMENT_SIZES`. Falls back to uniform `elem_width`/`elem_height` if `elem_types` is None.

**Sorting**: `sort_by_flow_order()` applied to newsletter generator (first-time and re-run placement). Uses DFS pre-order traversal from flow-participant elements with no incoming edges. DataObjects append at end. Cycles handled by visited-element skip.

## Process Architecture
- Process Architecture package is at root level in the EA project
- `<<CollaborationModel>>` elements (Activity with CollaborationModel stereotype) describe logical processes
- BPMN adornments mapped: taskType (Abstract/User/Manual), gatewayType, loopCharacteristics, etc. (see `bpmn_config.BPMN_TAGGED_VALUES`)
- Per-process models: `EAxCRM-CustomerAccountProcess.md`, `EAxCRM-SalesProcess.md`, `EAxCRM-NewsletterProcess.md`, each with a thin generate/sync wrapper over the shared `bpmn_engine.py` (see issue #3 refactor, 2026-07-05)
- `sync_process_from_ea.py` (dead code, combined all processes into `EAxCRM-ProcessModel.md`) and that orphaned MD file were both deleted 2026-07-05 — superseded by the per-process sync scripts

## Requirements Model
- `EAxCRM-Requirements.md` holds 41 requirements with ID, Status, Version, GUID, parent hierarchy, and entity mappings
- ID stored in EA's `t_object.Alias` field, synced via COM API
- Status and Version are standard EA `t_object` columns
- Entity → Requirement mappings use Realisation connectors (entity is source, requirement is target)
- Notes field (`t_object.Notes`) composes Description, then optional `Rationale:` and `Test Cases:` sections (see `build_notes()` in `generate_requirements_from_md.py`) so all three are visible together on the element. Rationale and Test Cases are *also* stored as EA Tagged Values (`Rationale`, `TestCases`) for structured/reportable access — added 2026-07-07 for CRM-6..12
- Naming convention (2026-07-07 on): lead with the GUI component (`CreateAccountScreen: ...`) for screen-specific requirements, or a business-rule name (`<Rule Name> Rule: ...`) for cross-cutting domain rules — not a restated full-sentence "must" requirement
- **STALE — superseded 2026-07-07**: the 2026-07-02 plan below to use CRM-6 through CRM-9 (and SAL-5) for the Manage Customer Account *BPMN process*-level requirements was never generated into EA; those IDs are now used instead by the Create Customer Account UI field/validation requirements (issue #7). If the process-level requirements below are still needed, use CRM-13 onward and a fresh SAL-5.
- Original 2026-07-02 plan (**MD only, never generated into EA, IDs since reassigned — see note above**): create Customer Account from minimal data, fuzzy-match duplicate detection + merge, email history retrieval via IMAP scan, role-gated opt-in suggestion requiring user confirmation, and verify/create Customer Account when an RFQ arrives from an unrecognized org — all in support of the Manage Customer Account process
- `sync_requirements_from_ea.py` — COM API only, reads from EA → MD (outputs `- Entities:` lines)
- `seed_requirements_properties.py` — COM API only, sets ID/Status/Version in EA from spec mapping
- `generate_requirements_from_md.py` — COM API only, creates/updates requirements in EA from MD, including parent Aggregation connectors, Realisation connectors to entities, and diagram placement (idempotent, saves GUID map)

## HARD RULE: COM API Only for Writes
- **NEVER use SQLite to create, update, or delete anything in EA** — not elements, not connectors, not diagrams, not t_xref, not tagged values, nothing.
- All generators use the **EA COM API** (`win32com.client.Dispatch("EA.Repository")`) exclusively
- Sync scripts may use SQLite for **read-only** queries (EA → MD direction only)
- Direct SQLite writes to `EAxCRM.qea` are **FORBIDDEN** — EA must always be the access layer

### Attribute Type Mapping
- **MD → EA** (`generate_uml_datamodel.py`): `text` → `string`
- **EA → MD** (`sync_datamodel_from_ea.py`): `memo` → `string`
- EA's `memo` type is a structured tag artifact, not used — all text attributes use `string` in both EA and MD

## Newsletter Process Model
- Elements placed directly under "Process Architecture" package (no sub-package)
- `EAxCRM-NewsletterProcess.md` holds the BPMN spec (1 CollaborationModel, 2 Lanes, 26 elements, 16 SequenceFlows, 39 total connectors incl DataAssociations)
- `generate_newsletter_process_from_md.py` — MD → EA generator (COM API only, like data model generator)
- `sync_newsletter_process_from_ea.py` — EA → MD sync (reads Newsletter Process Architecture package)
- Uses same GUID map pattern (`newsletter_guid_map.json`) for idempotent re-runs
- **DFS traversal**: parents created before children so `ParentID` is correctly set (critical for multi-lane models — flat depth-sort causes all depth-2 elements to inherit the last depth-1 parent)
- **Stereotype mapping**: MD header `"BPMN Collaboration"` maps to EA Stereotype `"CollaborationModel"` via `LABEL_TO_STEREO` dict
- **Flat MD support**: Sync outputs all descendants of CollaborationModel at `### ` level (flat hierarchy). Parser `### ` handler captures these as proper elements (bugfix 2026-06-29: was setting `current=None`, losing all `### ` elements).
- **Flow deduplication**: Sync script deduplicates SequenceFlows by (src_id, tgt_id, name) to avoid duplicate flow lines from duplicate connectors in EA (32→16 after fix).
- **7 scraping elements**: Scheduled Scrape, Fetch URL List, Scrape Articles, Extract Headings and Summaries, Store New Articles, URL List, Scrape Complete — completing the full newsletter pipeline from scraping through review and distribution.

## Sales Process Model
- `EAxCRM-SalesProcess.md` holds the BPMN spec (1 CollaborationModel, 3 Lanes, 50 elements, 25 SequenceFlows, 17 MessageFlows, 11 DataOutputAssoc, 11 DataInputAssoc)
- `generate_sales_process_from_md.py` — MD → EA generator (COM API only, full connector support)
- `sales_guid_map.json` — GUID map for idempotent re-runs
- Flat `### ` structure (all elements at same level, Lane field on each element indicates membership)
- Lane fields used for diagram placement via diagram_utils BPMN lane layout
- Connector existence check matches both short-form ("SequenceFlow") and long-form ("BPMN2.0::SequenceFlow") stereotypes
- v1.1 (2026-07-02): added `ConfirmCustomerAccount` IntermediateEvent (EAxpertise lane), inserted between `CreateRFQ` and `RegisterRFQ` — `CreateRFQ → RegisterRFQ` MessageFlow replaced by `CreateRFQ → ConfirmCustomerAccount` (MessageFlow, crosses Customer/EAxpertise) + `ConfirmCustomerAccount → RegisterRFQ` (SequenceFlow, same lane). References the new Manage Customer Account process — not a literal cross-diagram BPMN link, just a design/documentation pointer plus an ArchiMate Triggering relation (`r-trigger-rfq-createaccount`)

## Manage Customer Account Process
- `EAxCRM-CustomerAccountProcess.md` holds the BPMN spec (1 CollaborationModel, 1 Lane "EAxpertise", 12 elements, 9 SequenceFlows, 2 DataInputAssoc, 4 DataOutputAssoc). Follows the same flat `### ` + `- Lane:` format as the Sales Process.
- Fills a real gap: no existing process created the Customer/Contact records that Sales Process/Newsletter Management/Customer Insight all assume already exist.
- Flow: `NewCustomerContact` → `CreateCustomerAccount` (org name + exactly one Contact, role optional) → `Duplicatefound` gateway (fuzzy match on org name + Contact email) → either `MergeCustomerAccounts` (→ `MergedintoExistingAccount`) or `RetrieveEmailHistory` (IMAP scan across the 3 mailboxes) → `PrimaryorLicenseHolderrole` gateway → optionally `SuggestNewsletterOptin` (system suggests, **user must explicitly confirm** — opt_in is never set automatically) → `AccountReady`
- Single Lane only (`EAxpertise`) — always staff-driven via the EAxCRM app, no self-service/Customer lane, no separate system/IMAP lane
- No new Data Model entities/fields needed — reuses existing `Customer`/`Contact`/`Communication`
- Generated into EA (2026-07-03) via `generate_customeraccount_process_from_md.py` / `sync_customeraccount_process_from_ea.py`; synced live from EA 2026-07-08
- Requirements for this process were planned as CRM-6 through CRM-9 and SAL-5, but that ID range was reassigned 2026-07-07 to the Create Customer Account UI requirements (issue #7) before these process-level ones were ever generated into EA — write these as CRM-13+ / a fresh SAL-5 instead. See "Requirements Model" below.
- New ArchiMate additions (v2.1): BusinessFunction `Manage Customer Account` (`e-func-account`) with 4 BusinessProcesses (`e-process-createaccount`, `e-process-dedupe`, `e-process-merge`, `e-process-emailhistory`), reusing existing `Customer Data`/`Contact Data`/`Communication Data` BusinessObjects and the `Customer Management Service`/`IMAP Fetch Service` ApplicationServices; Triggering relation from `Handle RFQ` to `Create Customer Account`

### Generator Scripts (experiments/modelgen/)

## Cross-Session Memory
- `opencode-memory` plugin (`@mathew-cf/opencode-memory@1.0.1`) installed in `~\.config\opencode\opencode.jsonc`
- Memory directory at `_opencode_memory/` in the repo root (tracked by git, pushed to GitHub)
- Environment variable `OPENCODE_MEMORY_DIR` set permanently to the repo path
- 7 category subdirs: `preferences/`, `repos/`, `technical/`, `people/`, `workflows/`, `snippets/`, `notes/`
- **Keyword search** via ripgrep: available (Windows x64 supported)
- **Semantic search** via rag-cli: unavailable on Windows (no prebuilt binary; would need Rust/cargo)
- Skill auto-registered at `~/.agents/skills/opencode-memory/`
- Tools: `memory_search`, `memory_list`, `memory_save`, `memory_access`, `memory_setup`
- Session tools: `session_search`, `session_read`, `session_list`
- To re-bootstrap (e.g. after model download fix): `bunx @mathew-cf/opencode-memory init --skip-skills` (remove the re-created `.git` afterward)
- `.gitignore` excludes `_opencode_memory/.git/` to prevent nested repo issues if init is re-run

## CRUD File Update Rule
`models/EAxCRM-SalesProcess-CRUD.md` must be updated whenever:
- Data Input/Output Associations in the sales process change
- DataObject elements are added, renamed, or removed in the sales process
- Data model entities that map to BPMN data objects change (rename, add, remove)
- Run the sync/generator scripts first, then update the CRUD matrix to match

## Bugfix: EA 61704 Error + Non-BPMN Diagram Sizing/Layout (2026-07-02)

**61704 blocker resolved**: `generate_archimate.py` (and all other generator/
sync scripts) previously used `win32com.client.Dispatch("EA.Repository")`,
which can attach to an EA automation server already registered in COM's
Running Object Table — e.g. the user's own open EA instance on the same
file — instead of spawning an isolated one. Switched every script to
`DispatchEx("EA.App")` via a new shared `experiments/modelgen/ea_session.py`
module, which also retries `Models.GetAt(0)` (observed to transiently fail
right after `OpenFile`/`ActivateTechnology`) and centralizes zombie-process
cleanup (before/after PID diffing — never touches a pre-existing EA
instance). This unblocked the ArchiMate v2.0 sync, now confirmed live in EA.

**Two real zombie-cleanup bugs found and fixed** (both leaked an EA.exe on
every run): `generate_sales_process_from_md.py` and
`generate_newsletter_process_from_md.py` captured `before_pids` *after*
`repo.OpenFile()` had already spawned the process, so their own instance was
always excluded from the kill diff. `cleanup.py` had no cleanup logic at all.

**Non-BPMN diagram layout rewritten** (`diagram_utils.py`): the old
`compute_diagonal_positions()` row-jump formula compounded by
`per_row * step` per row, sprawling new elements thousands of pixels from
the rest of the diagram. Replaced with `compute_grid_positions()` — linear,
non-compounding row/column advance, anchored below the diagram's real
current extent (`get_diagram_extent()`) instead of a blind index
continuation.

**Element sizing**: confirmed empirically that EA's COM API does not
auto-size a `DiagramObject` (`right`/`bottom` left unset → permanent 0×0,
invisible — verified both via COM read-back and visually in EA's GUI).
Diagram `Type`/`Stereotype`/`MDGTechnology` do not affect this either.
`DEFAULT_ELEMENT_SIZES` in `diagram_utils.py` now sets every ArchiMate/
Requirements type to a uniform `(90, 70)`, confirmed against three elements
dragged fresh from the ArchiMate3 toolbox (`ApplicationComponent1`,
`BusinessActor1`, `BusinessObject1`) and left unresized. UML Data Model
entities are different — they show a real attribute compartment, so
`compute_uml_class_width()`/`compute_uml_class_height()` scale the box with
each entity's own attribute count/name length instead of a fixed size
(tuned interactively against a `Sandbox` test diagram).

**Connector LineStyle**: `generate_uml_datamodel.py` now sets `LineStyle = 8`
(Orthogonal Square) on every connector via the new
`diagram_utils.set_diagram_link_style()` — a UML Data Model-specific
preference, distinct from BPMN's `LineStyle = 9` (Orthogonal Rounded).
ArchiMate connectors are not yet styled this way.

**Sandbox workflow**: never test new layout/sizing/style logic against a
real diagram — use a `Sandbox` package directly under the root Model
package, with its own GUID map file, so it can never collide with a real
generator's state. See the `ea-diagram-creator` skill for the full pattern.

## Bugfix: BPMN Event tagged value was `eventType`, real EA tag is `eventDefinition` (2026-07-02)

Every BPMN generator/sync script (`generate_sales_process_from_md.py`,
`generate_newsletter_process_from_md.py`, `generate_customeraccount_process_from_md.py`,
`sync_sales_process_from_ea.py`, `sync_newsletter_process_from_ea.py`,
`sync_process_from_ea.py`) used the tagged-value property key `"eventType"`
for `StartEvent`/`EndEvent` — this never matched any real EA/BPMN2.0-MDG
property, so it silently wrote/read nothing. Confirmed via EA's own Tagged
Values browser (screenshot of the `IntermediateEvent (from BPMN2.0)` panel):
the real property is **`eventDefinition`**, with the standard BPMN 2.0
vocabulary as its value list — `None, Cancel, Compensation, Conditional,
Escalation, Error, Link, Message, Multiple, Timer, Signal, ParallelMultiple`.
Fixed by renaming the key everywhere (the MD-facing label stays `Event Type`
— only the internal EA property name changed, no MD syntax change needed).

Also found and fixed: `IntermediateEvent` had **no tagged-value entry at
all** in `generate_sales_process_from_md.py`, `generate_newsletter_process_from_md.py`,
`generate_customeraccount_process_from_md.py`, and `sync_newsletter_process_from_ea.py`
(only `sync_sales_process_from_ea.py`/`sync_process_from_ea.py` had it) —
added `"IntermediateEvent": {"eventDefinition": "Event Type", "triggerType": "Trigger"}`
to all four.

**Not yet confirmed**: `triggerType` (labeled `Trigger`/`Result` for Start/End)
may be equally wrong — EA's browser showed a `catchOrThrow` property
(values `Catch`/`Throw`) for `IntermediateEvent` instead, which looks like
the more likely real property. Left `triggerType` unchanged pending
confirmation — don't assume it's correct just because `eventDefinition`
was fixed.

`ConfirmCustomerAccount` (Sales Process, EAxpertise lane) set to
`Event Type: Signal` in `EAxCRM-SalesProcess.md` — a deliberate choice over
the originally-designed Message event, made after inspecting the real
tagged-value options in EA.

## Changelog / Audit Logging

### What it is
- A structured Markdown changelog system for tracking EA model changes
- Each generator/sync script logs creates, updates, and deletes per-element
- Sync scripts use `compute_md_diff()` for full MD diff on the regenerated file

### Files Involved
- `experiments/modelgen/changelog.py` — the `ChangeLog` class + `compute_md_diff()` function
- Per-script changelog files (auto-generated, git-tracked):

| Script | Changelog File |
|--------|---------------|
| BPMN engine (all 3 processes) | `sales_changelog.md`, `newsletter_changelog.md`, `customeraccount_changelog.md` |
| `generate_archimate.py` | `archimate_changelog.md` |
| `generate_uml_datamodel.py` / `sync_datamodel_from_ea.py` | `uml_datamodel_changelog.md` |
| `generate_requirements_from_md.py` / `sync_requirements_from_ea.py` / `seed_requirements_properties.py` | `requirements_changelog.md` |

### Integration Point
- `ChangeLog` is designed as a pure Python stdlib dependency (no pip installs)
- Generators log per-element: `clog.log(action, id, label, type, guid, changes=dict)`
- Sync scripts read old MD → build new MD → diff → `clog.log_diff(diff)`
- All `clog.close()` calls wrapped in `try/finally`
- Logged to `experiments/modelgen/*_changelog.md`

### Best Practices
- Generator scripts already capture `old_notes` before overwriting (e.g., ArchiMate generator, seed_requirements_properties)
- Element GUID is always captured from existing COM API return values — no extra API calls
- Checkpoints organize the log into phases (e.g., "Parsed MD", "Diagram complete", "Sync from EA")

### When to Wire New Scripts
- New generator: import `ChangeLog`, open with `checkpoint("Parsed MD")`, log create/update per element/relation, close with `checkpoint("Diagram complete")` in `try/finally`
- New sync script: import `ChangeLog, compute_md_diff`, read old file, build new content, compute diff, `checkpoint("Sync from EA")`, `log_diff(diff)`, close in `try/finally`, then write

## Next Steps
1. **Test entity → requirement Realisation connector round-trip**: delete/add entity mappings in MD, run generator, verify connectors update; modify in EA, run sync, verify MD updates
2. Build IMAP experiment, PDF parsing experiment
3. **Add Pools, Lanes, Tasks, Events, Gateways** to existing CollaborationModels in EA, run sync scripts to verify MD output
4. **Extend BPMN generators** — add support for CallActivity, SubProcess, ChoreographyTask, Message, and other BPMN 2.0 element types
5. **Build `generate_customeraccount_process_from_md.py`** (and its sync counterpart) following the Sales Process generator pattern, then run `generate_archimate.py` and `generate_sales_process_from_md.py` to push the v2.1 ArchiMate additions and Sales Process v1.1 event into `EAxCRM.qea` — test in the `Sandbox` package first per the `ea-diagram-creator` skill
6. **Generate the Manage Customer Account process-level requirements** into EA via `generate_requirements_from_md.py` once the process is confirmed — use CRM-13+ and a fresh SAL-5, since CRM-6..9 were reassigned 2026-07-07 to the Create Customer Account UI requirements (issue #7)
