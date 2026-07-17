# EAxCRM — Sales Process CRUD Matrix

**Model ID**: crud-eacrm
**Purpose**: Maps which BPMN activities Create, Read, Update, or Delete each Data Object in the sales process, cross-referenced to the data model entities.
**Version**: 1.0
**Sources**: `EAxCRM-SalesProcess.md` (BPMN), `EAxCRM-DataModel.md` (data model)

## Legend

| Column | Meaning |
|--------|---------|
| **Data Object (BPMN)** | The Artifact element from the BPMN model |
| **Lane** | Which pool/lane owns the data object |
| **Create** | Activity with a DataOutputAssoc to this data object |
| **Read** | Activity with a DataInputAssoc from this data object |
| **Update / Delete** | No activities currently update or delete data objects |
| **Transmission** | The MessageFlow (source → target) that sends the data object between lanes |
| **Data Model Entity** | The corresponding entity in `EAxCRM-DataModel.md` |

## Matrix

| Data Object (BPMN) | Lane | Create | Read | Update | Delete | Transmission | Data Model Entity |
|---|---|---|---|---|---|---|---|
| RFQ | Customer | CreateRFQ | RegisterRFQ | — | — | CreateRFQ → RegisterRFQ [email] | Communication |
| Offer | EAxpertise | FinaliseVersionofOffer | ReviewOffer | — | — | FinaliseVersionofOffer → ReviewOffer [email offer] | Offer |
| LicenseQuote | Vendor | PrepareLicenseQuote | RequestLicenseQuote | — | — | PrepareLicenseQuote → RequestLicenseQuote [email license pricing] | Quote |
| ServiceQuote | Vendor | PrepareServiceQuote | RequestServiceQuote | — | — | PrepareServiceQuote → RequestServiceQuote [email service pricing] | Quote |
| PurchaseOrder | Customer | AcceptOffer_Activity | HandleApprovedOffer | — | — | AcceptOffer_Activity → HandleApprovedOffer [email acceptance and invoice details] | Purchase |
| LicenseDocument | Vendor | ProvideLicenses | PrepareDelivery | — | — | ProvideLicenses → PrepareDelivery | Attachment (→ Delivery) |
| ServiceDocument | Vendor | ProvideServices | PrepareDelivery | — | — | ProvideServices → PrepareDelivery | Attachment (→ Delivery) |
| LicenseInvoice | Vendor | ProvideLicenses | PrepareSalesInvoice | — | — | *(bundled with LicenseDocument in ProvideLicenses → PrepareDelivery)* | ProcurementInvoice |
| ServiceInvoice | Vendor | ProvideServices | PrepareSalesInvoice | — | — | *(bundled with ServiceDocument in ProvideServices → PrepareDelivery)* | ProcurementInvoice |
| SalesInvoice | EAxpertise | PrepareSalesInvoice | PaySalesInvoice | — | — | PrepareSalesInvoice → PaySalesInvoice | SalesInvoice |
| Payment | Customer | PaySalesInvoice | ValidatePayment | — | — | PaySalesInvoice → ValidatePayment [payment by bank] | SalesInvoice.paid |

## Create-Read Lifecycle Per Data Object

### RFQ
1. **Create** — `CreateRFQ` (Customer) via DataOutputAssoc
2. **Transmit** — MessageFlow `CreateRFQ → RegisterRFQ` (Customer → EAxpertise)
3. **Read** — `RegisterRFQ` (EAxpertise) via DataInputAssoc

### Offer
1. **Create** — `FinaliseVersionofOffer` (EAxpertise) via DataOutputAssoc
2. **Transmit** — MessageFlow `FinaliseVersionofOffer → ReviewOffer` (EAxpertise → Customer)
3. **Read** — `ReviewOffer` (Customer) via DataInputAssoc

### LicenseQuote
1. **Create** — `PrepareLicenseQuote` (Vendor) via DataOutputAssoc
2. **Transmit** — MessageFlow `PrepareLicenseQuote → RequestLicenseQuote` (Vendor → EAxpertise)
3. **Read** — `RequestLicenseQuote` (EAxpertise) via DataInputAssoc

### ServiceQuote
1. **Create** — `PrepareServiceQuote` (Vendor) via DataOutputAssoc
2. **Transmit** — MessageFlow `PrepareServiceQuote → RequestServiceQuote` (Vendor → EAxpertise)
3. **Read** — `RequestServiceQuote` (EAxpertise) via DataInputAssoc

### PurchaseOrder
1. **Create** — `AcceptOffer_Activity` (Customer) via DataOutputAssoc
2. **Transmit** — MessageFlow `AcceptOffer_Activity → HandleApprovedOffer` (Customer → EAxpertise)
3. **Read** — `HandleApprovedOffer` (EAxpertise) via DataInputAssoc

### LicenseDocument
1. **Create** — `ProvideLicenses` (Vendor) via DataOutputAssoc
2. **Transmit** — MessageFlow `ProvideLicenses → PrepareDelivery` (Vendor → EAxpertise)
3. **Read** — `PrepareDelivery` (EAxpertise) via DataInputAssoc

### ServiceDocument
1. **Create** — `ProvideServices` (Vendor) via DataOutputAssoc
2. **Transmit** — MessageFlow `ProvideServices → PrepareDelivery` (Vendor → EAxpertise)
3. **Read** — `PrepareDelivery` (EAxpertise) via DataInputAssoc

### LicenseInvoice
1. **Create** — `ProvideLicenses` (Vendor) via DataOutputAssoc
2. **Transmit** — *(bundled with LicenseDocument in the same MessageFlow `ProvideLicenses → PrepareDelivery`)*
3. **Read** — `PrepareSalesInvoice` (EAxpertise) via DataInputAssoc

### ServiceInvoice
1. **Create** — `ProvideServices` (Vendor) via DataOutputAssoc
2. **Transmit** — *(bundled with ServiceDocument in the same MessageFlow `ProvideServices → PrepareDelivery`)*
3. **Read** — `PrepareSalesInvoice` (EAxpertise) via DataInputAssoc

### SalesInvoice
1. **Create** — `PrepareSalesInvoice` (EAxpertise) via DataOutputAssoc
2. **Transmit** — MessageFlow `PrepareSalesInvoice → PaySalesInvoice` (EAxpertise → Customer)
3. **Read** — `PaySalesInvoice` (Customer) via DataInputAssoc

### Payment
1. **Create** — `PaySalesInvoice` (Customer) via DataOutputAssoc
2. **Transmit** — MessageFlow `PaySalesInvoice → ValidatePayment` (Customer → EAxpertise) [payment by bank]
3. **Read** — `ValidatePayment` (EAxpertise) via DataInputAssoc

## Update / Delete

No activities in the current sales process model update or delete data objects. The process is a **create-once, read-once pipeline** — each data object is produced by one activity and consumed by one activity.

## Data Model Entity Mapping Notes

| BPMN Data Object | Why this entity |
|---|---|
| RFQ → Communication | RFQs arrive as emails; the formal Quote entity represents quotes *from* vendors, not customer requests |
| LicenseQuote → Quote | A vendor's pricing response, stored in the same Quote entity (distinguished by context) |
| ServiceQuote → Quote | Same Quote entity as LicenseQuote, different quote line items |
| LicenseDocument → Attachment | License files are file attachments linked to a Delivery |
| ServiceDocument → Attachment | Service agreement files are attachments linked to a Delivery |
| LicenseInvoice → ProcurementInvoice | Incoming invoice from a vendor for license procurement |
| ServiceInvoice → ProcurementInvoice | Incoming invoice from a vendor for service procurement |
| Payment → SalesInvoice.paid | Payment is tracked as boolean fields on SalesInvoice (paid / paid_date) — no separate Payment entity exists |

## Update Procedure

This file must be updated when any of the following change:

1. **BPMN sales process** (`EAxCRM-SalesProcess.md`):
   - Data Input/Output Associations are added, removed, or change target/source
   - New DataObject elements are added to the process
   - Activities are added or renamed that produce or consume data
   - MessageFlows change that transmit data objects between lanes

2. **Data model** (`EAxCRM-DataModel.md`):
   - Entities are renamed, added, or removed that correspond to BPMN data objects
   - Entity attributes change that affect how BPMN objects map to the data model (e.g., if a Payment entity is added)

3. **Commands to sync after changes:**
   ```
   # Regenerate sales process from EA (if changed in EA)
   python modelgen/sync_sales_process_from_ea.py

   # Regenerate data model from EA (if changed in EA)
   python modelgen/sync_ldm_from_ea.py
   ```
