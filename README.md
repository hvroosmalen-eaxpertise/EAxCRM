# EAxCRM — Enterprise Architect Customer Relationship Manager

A Django CRM for managing Sparx EA customers, their communications, license entitlements, and newsletter campaigns.

## Features

- **Customer Insight** — manage contacts (with role), IMAP-imported communications, documents, license entitlements, purchases linked to quotes and invoices
- **Sales Management** — create Offers (proposals) with optional Services (SaaS, Training, Support), track SalesInvoices and ProcurementInvoices in EUR/USD
- **Newsletter** — scrape articles from SparxSystems.com, compose EAxNewsletter, send to opted-in contacts (Draft → Review → Sent workflow)
- **Document Ingestion** — drag-and-drop PDF/TXT documents to auto-parse and populate License, Service, Quote, and Invoice entities

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | Python 3.13 + Django 6.x |
| Database | PostgreSQL (dev/test + prod, chosen 2026-07-09 — see `EAxCRM-Archimate.md` v2.4 Technology layer split) |
| IMAP | imaplib + email stdlib |
| PDF parsing | PyMuPDF (fitz) |
| Scraping | requests + BeautifulSoup |
| UI | Django Admin |
| Auth | Django built-in |

## Data Model

**19 entities**, **30 relationships**, **41 requirements**, **3 BPMN processes** (newsletter: 26 elements, 2 lanes, 16 flows; sales: 50 elements, 3 lanes, 64 flows; customer account: 13 elements, 1 lane, 9 flows) — maintained in Sparx EA as the canonical source.

| Procurement Flow | Sales Flow |
|---|---|
| Vendor → Quote → Purchase → ProcurementInvoice → License | Offer → SalesInvoice → Customer |
| | Service → Offer / SalesInvoice (optional) |
| | Delivery → Customer / SalesInvoice |

See `models/EAxCRM-DataModel.md` for the full entity list, `models/EAxCRM-Requirements.md` for requirements, `models/EAxCRM-NewsletterProcess.md` and `models/EAxCRM-SalesProcess.md` for BPMN specs, and `AGENTS.md` for design context.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Testing

The Django app has no test suite yet. `modelgen/` has pytest coverage:

```bash
cd modelgen
pytest test_pure_functions.py          # pure logic, any platform, no EA needed
pytest -m ea test_generators_regression.py   # Windows + EA required; runs generators against a sandboxed EAxCRM.qea copy
```

## Code validator (pre-commit hook)

`.opencode/skills/ea-code-validator/` enforces project rules on EA-touching Python (no direct EA-repo queries, generate/sync pairing, no writes to existing-diagram geometry). Install the pre-commit hook once per clone:

```bash
# PowerShell
powershell -NoProfile -File scripts/install-hooks.ps1

# or POSIX sh (Git Bash / WSL / macOS / Linux)
sh scripts/install-hooks.sh
```

Ad-hoc runs: `python .opencode/skills/ea-code-validator/cli.py --list` to see rules, `... --changed` for staged files only, `... path/...` for a subtree. See the skill's `SKILL.md` for full flag reference and the design doc under `docs/superpowers/specs/`.

## Project Structure

```
EAxCRM/
├── contacts/           # CRM app (Customer, Contact, Communication, Purchase, License, SalesInvoice, ProcurementInvoice, Offer, Service, Vendor, Delivery)
├── newsletter/         # Newsletter app (Newsletter, NewsSource, Article)
├── eacrm/              # Django project settings
├── models/             # Sparx EA model files (.qea, .md) — see models/README.md
├── modelgen/           # Production model generators (Markdown ↔ Sparx EA: LDM, requirements, BPMN, ArchiMate, wireframes)
│   ├── changelog.py                    # Structured audit logging (per-run Markdown, prepend, size cap)
│   ├── test_pure_functions.py          # Layout math, MD parsing, graph algorithms — no EA needed
│   ├── test_generators_regression.py   # Runs each generator against a sandboxed EAxCRM.qea copy
│   └── *_changelog.md                  # Per-domain audit log (archimate, ldm, requirements, sales, newsletter, customeraccount)
├── pdm/                # Physical data model generator (issue #16 — <<table>> stereotype → Postgres DDL)
├── experiments/        # Remaining POCs
│   ├── imap/           # IMAP retrieval experiments
│   └── parsing/        # PDF parsing experiments
├── EAxCRM.sln          # Visual Studio solution file
├── EAxCRM.pyproj       # Python project file (Django, Python 3.13)
├── manage.py
└── requirements.txt
```

See `AGENTS.md` for detailed design context.
