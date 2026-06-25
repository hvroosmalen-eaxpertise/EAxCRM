# EAxCRM — Enterprise Architect Customer Relationship Manager

A Django CRM for managing Sparx EA customers, their communications, license entitlements, and newsletter campaigns.

## Features

- **Customer Insight** — manage contacts (with role), IMAP-imported communications, documents, license entitlements, purchases linked to quotes and invoices
- **Sales Management** — create Offers (proposals) with optional Services (SaaS, Training, Support), track SalesInvoices and ProcurementInvoices in EUR/USD
- **Newsletter** — scrape articles from SparxSystems.com, compose EAxNewsletter, send to opted-in contacts (Draft → Review → Sent workflow)

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

**17 entities**, **22 relationships** — maintained in Sparx EA as the canonical source.

| Procurement Flow | Sales Flow |
|---|---|
| Quote → Purchase → ProcurementInvoice → License | Offer → SalesInvoice → Customer |
| | Service → Offer / SalesInvoice (optional) |

See `models/EAxCRM-DataModel.md` for the full entity list and `AGENTS.md` for design context.

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
├── contacts/           # CRM app (Customer, Contact, Communication, Purchase, License, Invoice, Service)
├── newsletter/         # Newsletter app (Newsletter, NewsSource, Article)
├── eacrm/              # Django project settings
├── models/             # Sparx EA model files (.qea, .md) — see models/README.md
├── experiments/        # Isolated POCs (IMAP, PDF parsing, modelgen)
│   ├── modelgen/       # Model generators (Markdown ↔ Sparx EA .qea)
│   ├── imap/           # IMAP retrieval experiments
│   └── parsing/        # PDF parsing experiments
└── requirements.txt
```

See `AGENTS.md` for detailed design context.
