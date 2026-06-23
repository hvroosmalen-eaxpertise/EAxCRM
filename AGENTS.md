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
| Framework | Python 3.13 + Django 5.x |
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
- `EAxCRM.xmi` — ArchiMate model (AMEFF 3.1 format, deprecated but kept as reference)
- `EAxCRM-Archimate.md` — ArchiMate model source of truth (Markdown, 44 elements, 57 relations)
- `EAxCRM-Datamodel.xml` — UML data model for Sparx EA (XMI 1.1, will be replaced by Markdown)
- `EAxCRM.qea` — Sparx EA project file (populated with ArchiMate model + data model)

## Active Context
- Project is in Phase 0 setup
- No code committed yet
- Remote: https://github.com/hvroosmalen-eaxpertise/EAxCRM (no remote configured locally yet)
- Superpowers plugin installed globally via opencode.jsonc
- Pending: Django scaffold, IMAP experiment, PDF experiment, data models, admin UI, Docker

## Generator Scripts (experiments/modelgen/)
- `generate_archimate.py`: MD → Sparx EA via 3-phase approach (COM API for elements, SQLite for connectors, COM API for diagram objects + SQLite for diagram stereotype)
- `generate_archimate.py` is idempotent: saves GUID map to `archimate_guid_map.json`, re-runs update existing without duplicates

## Critical Context: COM API + SQLite Interactions
- `ElementGUID` is read-only (can't set programmatically); idempotency via JSON GUID mapping file
- Element `StereotypeEx` stores correctly via COM API (persists to `t_xref` with Visibility='element property')
- Connector `StereotypeEx` does NOT persist via COM API (t_connector.Stereotype stays NULL, no t_xref entry)
- Connector stereotypes must be set via direct SQLite writes to `t_connector.Stereotype` AND `t_xref` (Visibility='connector property')
- COM API + SQLite concurrent access works only when COM API hasn't started a write transaction; for consistency, use 3-phase approach:
  - Phase 1: COM API for elements (open file, sync, close file)
  - Phase 2: SQLite for connector creation/stereotypes (COM API closed)
  - Phase 3: COM API for diagram objects (open fresh, close) + SQLite for diagram stereotype
- `repo.CloseFile()` can hang; use try/finally with except: pass
- EA processes (EA.exe) accumulate between runs — kill all before re-running generator
- GUID map file: `experiments/modelgen/archimate_guid_map.json`

## Connector Type Mapping (ArchiMate → Sparx EA)
| ArchiMate | Connector_Type | Stereotype |
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

## Next Steps
- Open EAxCRM.qea in Sparx EA to verify diagram rendering (ArchiMate icons, connector display)
- Create the logical data model generator (`generate_datamodel.py`) reading from a Markdown model file (not yet created)
- Create skill files: `.opencode/skills/generate-archimate-model/SKILL.md` and `.opencode/skills/generate-datamodel/SKILL.md`
- Configure Git remote and make initial commit
- Build IMAP experiment, PDF parsing experiment
