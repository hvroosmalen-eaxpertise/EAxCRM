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
| Database | SQLite |
| IMAP | imaplib + email stdlib |
| PDF parsing | PyMuPDF (fitz) |
| Scraping | requests + BeautifulSoup |
| UI | Django Admin |
| Auth | Django built-in |

## Data Model

**19 entities**, **30 relationships**, **34 requirements**, **1 BPMN process** (3 lanes, 45 elements, 59 flows) — maintained in Sparx EA as the canonical source.

| Procurement Flow | Sales Flow |
|---|---|
| Vendor → Quote → Purchase → ProcurementInvoice → License | Offer → SalesInvoice → Customer |
| | Service → Offer / SalesInvoice (optional) |
| | Delivery → Customer / SalesInvoice |

See `models/EAxCRM-DataModel.md` for the full entity list, `models/EAxCRM-Requirements.md` for requirements, and `AGENTS.md` for design context.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
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
│   ├── imap/           # IMAP retrieval experiments
│   └── parsing/        # PDF parsing experiments
├── EAxCRM.sln          # Visual Studio solution file
├── EAxCRM.pyproj       # Python project file (Django, Python 3.13)
├── manage.py
└── requirements.txt
```

See `AGENTS.md` for detailed design context.
