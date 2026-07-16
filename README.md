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

The Django app has no test suite yet. `experiments/modelgen/` has pytest coverage:

```bash
cd experiments/modelgen
pytest test_pure_functions.py          # pure logic, any platform, no EA needed
pytest -m ea test_generators_regression.py   # Windows + EA required; runs generators against a sandboxed EAxCRM.qea copy
```

## Project Structure

```
EAxCRM/
├── contacts/           # CRM app (Customer, Contact, Communication, Purchase, License, SalesInvoice, ProcurementInvoice, Offer, Service, Vendor, Delivery)
├── newsletter/         # Newsletter app (Newsletter, NewsSource, Article)
├── eacrm/              # Django project settings
├── models/             # Sparx EA model files (.qea, .md) — see models/README.md
├── experiments/        # Isolated POCs (IMAP, PDF parsing, modelgen)
│   ├── modelgen/       # Model generators (Markdown ↔ Sparx EA: data model, requirements, BPMN process)
│   │   ├── changelog.py        # Structured audit logging (per-run Markdown, prepend, size cap)
│   │   ├── test_pure_functions.py       # Layout math, MD parsing, graph algorithms — no EA needed
│   │   ├── test_generators_regression.py # Runs each generator against a sandboxed EAxCRM.qea copy
│   │   ├── archimate_changelog.md
│   │   ├── ldm_changelog.md
│   │   ├── requirements_changelog.md
│   │   ├── sales_changelog.md
│   │   ├── newsletter_changelog.md
│   │   └── customeraccount_changelog.md
│   ├── imap/           # IMAP retrieval experiments
│   └── parsing/        # PDF parsing experiments
├── EAxCRM.sln          # Visual Studio solution file
├── EAxCRM.pyproj       # Python project file (Django, Python 3.13)
├── manage.py
└── requirements.txt
```

See `AGENTS.md` for detailed design context.
