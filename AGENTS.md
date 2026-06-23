# EAxCRM — Enterprise Architect Customer Relationship Manager

## Purpose
A CRM system for managing Sparx EA customers, their communications, and newsletter campaigns.

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

### 2. Newsletter Management
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

## Design Decisions
- Newsletter content sourced from SparxSystems.com and sparxsystems.eu
- Newsletter frequency: once per 6 weeks
- Opt-in required for newsletter contacts (initial opt-in via CRM-marked email addresses)
- Experiments for IMAP and PDF parsing done in isolated `experiments/` directory before integrating into main app
- Database field for passwords encrypted at rest
- No AI dependencies by design; optional small local LLM later if needed (ollama)

## Models (files in ../models/)
- `EAxCRM-Archimate.md` — ArchiMate model source of truth (Markdown, 44 elements, 57 relations, 1 diagram)
- `EAxCRM.qea` — Sparx EA project file (populated with ArchiMate model + data model)

## Active Context
- ArchiMate model fully generated with 44 elements, 57 relationships, 1 diagram
- ApplicationService Object_Type fixed to 'Activity' (confirmed correct shape in EA)
- Diagram preservation works: subsequent runs skip element placement, only update type/stereotype
- GUID map has 45 entries (44 elements + 1 diagram), saved to `archimate_guid_map.json`
- Remote configured: https://github.com/hvroosmalen-eaxpertise/EAxCRM (committed and pushed)

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

## Next Steps
1. Open EAxCRM.qea in Sparx EA to verify diagram rendering
2. Create the logical data model generator (`generate_datamodel.py`) reading from a Markdown model file
3. Build IMAP experiment, PDF parsing experiment
