# EAxCRM Requirements Specification

**Version:** 1.0
**Date:** 2026-06-26
**Status:** Draft

## Scope

This specification defines the full set of functional and technical requirements for the EAxCRM system. Requirements are grouped by domain. Each requirement has a unique ID for traceability.

Existing requirements in the EA model (from `EAxCRM-Requirements.md`) are preserved and renumbered here.

---

## 1. Customer Management

| ID | Requirement | Priority |
|----|-------------|----------|
| CRM-1 | EAxCRM must manage Customer organizations and their Contacts with specific roles (Primary, Purchase, Sales, License Holder) | High |
| CRM-2 | EAxCRM must store communication history per customer, retrieved from multiple IMAP accounts (han@eaxpertise.nl, sales@eaxpertise.nl, info@eaxpertise.nl) | High |
| CRM-3 | EAxCRM must extract and store license entitlements from email attachments (PDF/TXT) | High |
| CRM-4 | EAxCRM must track license renewals linked to the original purchase | Medium |
| CRM-5 | EAxCRM must store documents (quotes, invoices, deliveries) linked to customers | High |

## 2. Procurement

| ID | Requirement | Priority |
|----|-------------|----------|
| PRO-1 | EAxCRM must support the procurement process from Quote to Purchase to ProcurementInvoice | High |
| PRO-2 | Procurement must be trackable per Vendor with linked Quote and ProcurementInvoice PDFs | High |
| PRO-3 | EAxCRM must store vendor bank details (IBAN, BIC/SWIFT, payment currency) | Medium |
| PRO-4 | EAxCRM must support multi-currency invoices (EUR, USD) from Sparx Systems | Medium |
| PRO-5 | Procurement can be done via multiple parties: Sparx Systems LTD, Sparx Systems EU, Ability Engineering, Prolaborate | High |

## 3. Sales

| ID | Requirement | Priority |
|----|-------------|----------|
| SAL-1 | EAxCRM must support the sales process from Offer to SalesInvoice | High |
| SAL-2 | EAxCRM must distinguish procured services (resold, from a Vendor) from EAxpertise's own services | Medium |
| SAL-3 | EAxCRM must detect service expiry and notify the user when renewal is needed | High |
| SAL-4 | EAxCRM must link each SalesInvoice to its originating Offer | High |

## 4. Delivery

| ID | Requirement | Priority |
|----|-------------|----------|
| DEL-1 | EAxCRM must record delivery emails containing license files and/or service agreements | High |
| DEL-2 | EAxCRM must link deliveries to the Customer, the SalesInvoice they fulfill, and the attachments included | Medium |

## 5. Newsletter

| ID | Requirement | Priority |
|----|-------------|----------|
| NWS-1 | EAxCRM must support composing newsletters from scraped articles on SparxSystems.com and sparxsystems.eu | Medium |
| NWS-2 | EAxCRM must enforce a Draft → Review → Send workflow with manual approval | High |
| NWS-3 | EAxCRM must track per-contact delivery status (sent, opened, bounced) | Medium |
| NWS-4 | EAxCRM must enforce a minimum 6-week interval between newsletters | Low |

## 6. Reporting & UX

| ID | Requirement | Priority |
|----|-------------|----------|
| RPT-1 | EAxCRM must provide a view of all customer license entitlements with start/expiry dates | High |
| RPT-2 | EAxCRM must provide a dashboard of upcoming service renewals | High |
| RPT-3 | EAxCRM must provide procurement reports grouped by Vendor | Medium |
| RPT-4 | EAxCRM must show the current procurement state per Vendor (quotes received, invoices paid/pending) | Medium |

## 7. Technical Constraints

| ID | Requirement | Priority |
|----|-------------|----------|
| TEC-1 | EAxCRM must use SQLite as its database backend | High |
| TEC-2 | EAxCRM must encrypt sensitive data (passwords) at rest | High |
| TEC-3 | EAxCRM must use the Django Admin interface as its primary UI | High |
| TEC-4 | EAxCRM must operate without AI dependencies | High |
| TEC-5 | EAxCRM must run on Windows for development and Docker/QNAP NAS for production | High |

## EA Storage

Requirements properties are stored in EA's `t_object` columns:
- **ID** → `Alias` column (accessed via `el.Alias` in COM API)
- **Status** → `Status` column (accessed via `el.Status` in COM API)
- **Version** → `Version` column (accessed via `el.Version` in COM API)

## Traceability

### Sources
- Existing EA model: `EAxCRM-Requirements.md` (8 requirements covering procurement and sales)
- Data model discussions: Customer insight, IMAP retrieval, license lifecycle
- CRM domain analysis: Delivery tracking, vendor management, service renewals
- Newsletter workflow: Draft → Review → Send, 6-week cadence

## Update 2026-07-07: Create Customer Account field/validation requirements (issue #7)

Added 7 requirements — CRM-6 through CRM-12 — capturing the field and validation rules decided for the Create Customer Account screen (see [issue #7](https://github.com/hvroosmalen-eaxpertise/EAxCRM/issues/7)): atomic Customer+Contact creation, structured street address vs. PO Box, the "at least one Primary contact" rule, role becoming required once a second contact exists, the new Secondary contact role, opt-in defaulting to false, and opportunistic capture of notes/phone.

This update also changed the Requirements Model format itself:
- Each requirement may now carry a **Rationale** and a **Test Cases** list, in addition to Description. All three are composed together into the EA element's Notes field, with Rationale/Test Cases also stored as EA Tagged Values for structured access.
- New requirement names lead with either the **GUI component** (`CreateAccountScreen: ...`) or a **business-rule name** (`<Rule Name> Rule: ...`), rather than a restated full-sentence "must" requirement — this only applies going forward; existing requirement names were left as-is.

**Note:** this reused the CRM-6–CRM-9 ID range that a 2026-07-02 planning note (see `AGENTS.md`) had reserved for the Manage Customer Account *BPMN process*-level requirements (duplicate detection, merge, email history, opt-in suggestion). Those were never generated into EA, so no real collision occurred, but that reservation is now stale — those process-level requirements should use CRM-13 onward (and a fresh SAL-5) if/when they're written.

### Mapping from Existing EA Requirements

| Existing EA ID | New ID |
|----------------|--------|
| EAxCRM must support the procurement process | PRO-1 |
| Procument can be done via multiple parties | PRO-5 (with corrected spelling) |
| Procurement can be done via Sparx Systems LTD | PRO-5 (child) |
| Procurement can be done via Sparx Systems EU | PRO-5 (child) |
| Procurement can be done via Ability Engineering | PRO-5 (child) |
| Procurement can be done via Prolaborate | PRO-5 (child) |
| EAxCRM must show a UX that shows the current state of Procuement | RPT-4 |
| EAXCRM must support the sales process | SAL-1 |
