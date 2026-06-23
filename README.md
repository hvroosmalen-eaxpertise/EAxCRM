# EAxCRM — Enterprise Architect Customer Relationship Manager

A Django CRM for managing Sparx EA customers, communications, and newsletter campaigns.

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
├── contacts/           # CRM app (Customer, Contact, Communication, Purchase, License)
├── newsletter/         # Newsletter app (Newsletter, NewsSource, Article)
├── eacrm/              # Django project settings
├── models/             # Sparx EA model files (.qea, .md, .xmi)
├── experiments/        # Isolated POCs (IMAP, PDF parsing, modelgen)
│   └── modelgen/       # ArchiMate model generator (MD → Sparx EA .qea)
└── requirements.txt
```

## Sparx EA Model

The ArchiMate model source of truth is `models/EAxCRM-Archimate.md` (Markdown). Run the generator to sync to `EAxCRM.qea`:

```bash
python experiments/modelgen/generate_archimate.py
```

See `AGENTS.md` for detailed design context and COM API interaction notes.
