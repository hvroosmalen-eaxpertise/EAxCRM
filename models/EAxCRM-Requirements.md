# EAxCRM — Requirements

**Model ID**: r-eacrm
**Purpose**: Requirements for the EAxCRM system
**Version**: 1.0

### Requirement—eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder
- Name: EAxCRM must manage Customer organizations and their Contacts with specific roles (Primary, Purchase, Sales, License Holder)
- ID: CRM-1
- Description: The system shall store customer organizations and their associated contacts, each with one or more roles that determine their function in the CRM workflow.
- Rationale: EAxpertise sells to organizations, not individuals — but every interaction is actually with a named person, so both levels must be tracked, and the multi-role model (Primary/Purchase/Sales/License Holder) reflects that different people at the same customer often own different parts of the relationship.
- Test Cases:
  - A Customer can have multiple Contacts, each with one or more roles.
  - A Contact's role can be changed without affecting Customer data.
  - Filtering contacts by role (e.g. License Holder) returns only contacts with that role at that customer.
- Entities: Contact, Customer
- Status: Proposed
- Version: 1.0
- GUID: {C8A09A87-5B2B-4d72-896F-77C079F7C2DA}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustsupporttheprocurementprocess
- Name: EAxCRM must support the procurement process
- ID: PRO-1
- Description: The system shall manage the end-to-end procurement workflow from receiving a supplier quote, creating a purchase record, and recording the incoming invoice.
- Rationale: Every license/service EAxpertise resells is first procured from a vendor; without a structured procurement record there's no way to reconcile what was bought, at what cost, against what's later sold or entitled to a customer.
- Test Cases:
  - A Quote can be linked to a Purchase and the Purchase linked to a ProcurementInvoice, forming a complete chain.
  - A Purchase cannot be created without a Vendor.
  - The procurement workflow state (quote received → purchased → invoiced) is visible per Purchase.
- Entities: ProcurementInvoice, Purchase, Quote, Vendor
- Status: Approved
- Version: 1.0
- GUID: {119DE89A-BFF5-44ab-AC67-6FC9DB0F8C10}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustuseaproductiongrademultiusercapablerelationaldatabase
- Name: EAxCRM must use a production-grade, multi-user-capable relational database
- ID: TEC-1
- Description: The system shall use a production-grade relational database capable of reliable concurrent multi-user access in production. The specific database engine is not yet decided (2026-07-08) — this requirement is intentionally technology-abstract until an engine is chosen. SQLite may still be suitable for local development, but is no longer the production target.
- Rationale: SQLite's single-writer model is a poor fit once the CRM needs to support multiple concurrent users reliably in production; a server-based RDBMS gives proper transactional isolation and concurrent write support without abandoning the Django framework.
- Test Cases:
  - Multiple concurrent users can read and write CRM data simultaneously without lock-contention errors.
  - Standard Django migrations apply cleanly against the chosen production database engine.
  - The database survives an unexpected process restart without data corruption (transactional durability).
- Status: Proposed
- Version: 1.0
- GUID: {30EA2FCA-BEA7-4fd7-A7E8-F5ECD78B8ADF}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustsupportcomposingnewslettersfromscrapedarticlesonsparxsystemscomandsparxsystemseu
- Name: EAxCRM must support composing newsletters from scraped articles on SparxSystems.com and sparxsystems.eu
- ID: NWS-1
- Description: The system shall scrape news articles from SparxSystems.com and sparxsystems.eu and allow composing an EAxNewsletter from selected article summaries and links.
- Rationale: EAxpertise doesn't produce original content for its newsletter — SparxSystems.com/.eu already publish the source material, so scraping and curating from there is cheaper than authoring from scratch and keeps the newsletter tied to what Sparx itself is announcing.
- Test Cases:
  - Scraping SparxSystems.com and sparxsystems.eu produces Article records with heading, summary, and source link.
  - A Newsletter can be composed by selecting a subset of scraped Articles.
  - Re-scraping does not duplicate Articles already stored for the same source URL.
- Entities: Article, NewsSource, Newsletter
- Status: Proposed
- Version: 1.0
- GUID: {153BD677-35A4-4252-BEC1-20B170577F99}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustsupportthesalesprocess
- Name: EAXCRM must support the sales process
- ID: SAL-1
- Description: The system shall manage the sales workflow from creating an Offer to generating a SalesInvoice for the customer.
- Rationale: Every customer-facing sale needs a documented trail from proposal to billing so revenue can be reconciled and disputes resolved — without an Offer→SalesInvoice link, there's no record of what was actually agreed before an invoice was raised.
- Test Cases:
  - An Offer can be created for a Customer and later converted into a SalesInvoice.
  - A SalesInvoice cannot exist without a Customer.
  - The sales workflow state is visible per Offer (open, accepted, invoiced).
- Entities: Offer, SalesInvoice
- Status: Approved
- Version: 1.0
- GUID: {0475B655-DAC3-4672-A10B-4B1C42DC4E44}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustprovideaviewofallcustomerlicenseentitlementswithstartexpirydates
- Name: EAxCRM must provide a view of all customer license entitlements with start/expiry dates
- ID: RPT-1
- Description: The system shall display a consolidated view of each customer's active and expired license entitlements including their start and end dates.
- Rationale: Reps need a single place to answer "what does this customer currently own and when does it expire" without cross-referencing multiple purchase records by hand — this is the most common support/renewal question.
- Test Cases:
  - The view lists all License records for a customer with start and expiry dates.
  - Expired licenses are visually distinguished from active ones.
  - The view updates immediately after a new License is added via a Purchase.
- Entities: Customer, License
- Status: Proposed
- Version: 1.0
- GUID: {695AC932-66C2-43d0-B242-A9BE87C30800}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustrecorddeliveryemailscontaininglicensefilesandorserviceagreements
- Name: EAxCRM must record delivery emails containing license files and/or service agreements
- ID: DEL-1
- Description: The system shall store delivery emails sent to customers that contain license registration files and/or service agreement documents.
- Rationale: Delivery emails are the customer's proof that they received their license file/agreement — without a record, support has no way to confirm what was actually sent versus what the customer claims (or fails to claim) they received.
- Test Cases:
  - A Delivery record captures the sent date, recipient address, subject, and body of the delivery email.
  - A Delivery can be linked to the license file(s) or agreement document(s) it contained.
  - Delivery status (sent/failed) is recorded and queryable.
- Entities: Delivery
- Status: Proposed
- Version: 1.0
- GUID: {2553EA37-D4C2-4c1c-BA2B-65ADD9C06F80}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustsupportdraganddropdocumentingestionthatautomaticallyparsesandfillsentities
- Name: EAxCRM must support drag-and-drop document ingestion that automatically parses and fills entities
- ID: DOC-1
- Description: The system shall allow a user to drag and drop a document (PDF, TXT, email file) onto the UI, which then automatically parses the content and populates the correct entities (License, LicenseLineItem, Service, Quote, ProcurementInvoice, Communication, Contact) as accurately as possible, reducing manual data entry.
- Rationale: License PDFs, quotes, and invoices arrive as email attachments constantly; manually re-typing their contents into the CRM is slow and error-prone, so automatic parsing turns an existing document into structured data with minimal rep effort.
- Test Cases:
  - Dropping a license PDF creates/updates the corresponding License and LicenseLineItem records with parsed values.
  - Dropping an unparseable or unrecognized document does not corrupt existing records — it flags for manual review instead.
  - Parsed field values can be reviewed/corrected by the rep before being saved.
- Entities: Attachment, Communication, Contact, Customer, License, LicenseLineItem, ProcurementInvoice, Quote, Service
- Status: Proposed
- Version: 1.0
- GUID: {7248B806-6768-40d0-87E7-FEDE7509892A}
- Parents:
  - (none — top-level)

### Requirement—procurementcanbedoneviamultipleparties
- Name: Procurement can be done via multiple parties
- ID: PRO-5
- Description: There are several suppliers to EAxpertise.
- Rationale: EAxpertise doesn't buy exclusively from Sparx Systems' HQ — regional resellers (EU, LTD) and specialty partners (Ability Engineering, Prolaborate) each cover different products/regions, so the data model must support more than one Vendor per procurement category.
- Test Cases:
  - More than one Vendor record can exist and each can be linked to independent Purchases.
  - A Purchase records exactly one Vendor (the party actually procured from for that transaction).
  - Reports can be grouped/filtered by Vendor across all procurement.
- Entities: Vendor
- Status: Approved
- Version: 1.0
- GUID: {506DEB0C-8BE3-4a76-B52E-E00F3DBB672E}
- Parents:
  - eaxcrmmustsupporttheprocurementprocess

### Requirement—contactrolerulerequiredonceasecondcontactexists
- Name: Contact Role Rule: required once a second Contact exists
- ID: CRM-9
- Description: Role is optional only when exactly one Contact exists on the form. As soon as a second Contact row is added, role becomes a required field for every Contact on the form, including ones already entered.
- Rationale: Prevents accounts with multiple unnamed-function contacts, where reps can no longer tell who does what.
- Test Cases:
  - One contact, role left at its default, saves fine (subject to CRM-8).
  - Add a second contact, leave either role blank — save is rejected.
  - Fill both roles — save succeeds.
- Entities: Contact
- Status: Proposed
- Version: 1.0
- GUID: {D97412A1-AF30-45ac-AE2D-E6A4A423CF65}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—contactrolerulesecondaryroleadded
- Name: Contact Role Rule: Secondary role added
- ID: CRM-10
- Description: The Contact role choices shall include Secondary, alongside Primary/Purchase/Sales/License Holder. Secondary denotes a colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties, and is the expected successor role if the Primary contact leaves the organization.
- Rationale: Organizations commonly designate a backup point of contact; without this role it would be miscategorized as Purchase/Sales or left blank, losing the succession signal.
- Test Cases:
  - Role dropdown lists Secondary as a selectable option.
  - A Contact saved with role=Secondary persists and displays correctly.
  - Filtering/reporting by role can isolate Secondary contacts.
- Entities: Contact
- Status: Proposed
- Version: 1.0
- GUID: {D37E1D4E-051B-455c-8B98-23F98FC4A551}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—createaccountscreencreatescustomerandcontactsatomically
- Name: CreateAccountScreen: creates Customer and Contacts atomically
- ID: CRM-6
- Description: The Create Customer Account screen shall create one Customer record and one or more Contact records in a single atomic save operation. A Customer must never be persisted without at least one associated Contact, since the account-creation process treats the organization and its initial contact(s) as one unit of work.
- Rationale: Matches the existing BPMN process (EAxCRM-CustomerAccountProcess.md), where account creation is modeled as one atomic activity. Prevents orphan Customer records with no way to reach anyone at the organization.
- Test Cases:
  - Save with 1 Customer + 1 Contact succeeds and both rows exist.
  - Save attempt with Customer fields filled but zero Contacts fails validation.
  - A mid-save failure (e.g. DB error on second Contact) rolls back the Customer too — no partial commit.
- Entities: Contact, Customer
- Status: Proposed
- Version: 1.0
- GUID: {D13E63E8-1DA9-4f10-BF1C-8AFC333666C7}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—createaccountscreennotesandphonecapturableatcreation
- Name: CreateAccountScreen: notes and phone capturable at creation
- ID: CRM-12
- Description: The create screen shall include optional fields for Customer.notes (free text) and Contact.phone, since both are sometimes directly available in the source email (footer/signature) and cheaper to capture immediately than via a later edit step.
- Rationale: Reduces follow-up data-entry work when the information is already visible to the rep; both remain optional since they're often absent from a first email.
- Test Cases:
  - Save succeeds with both fields blank.
  - Save succeeds with notes and/or phone filled in.
  - Values persist correctly on the respective Customer/Contact records.
- Entities: Contact, Customer
- Status: Proposed
- Version: 1.0
- GUID: {0EF04071-8682-4579-A08F-8A4F75EE8713}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—createaccountscreenstructuredstreetaddressorpobox
- Name: CreateAccountScreen: structured street address or PO Box
- ID: CRM-7
- Description: The system shall record a Customer's address as either a structured street address (Street Name, House Number, Postal Code, City, Country) or an unstructured PO Box string, selected via a mode toggle on the create screen. Address is mandatory — the rep must actively locate it if not present in the source email.
- Rationale: Real-world postal addresses aren't always street-based; forcing one shape either loses PO Box customers or forces reps to cram a PO Box into a street-shaped field.
- Test Cases:
  - Street mode requires all five fields before save.
  - PO Box mode requires only the PO Box text field; street fields stay null.
  - Switching modes clears/ignores the other mode's fields rather than submitting both.
- Entities: Customer
- Status: Proposed
- Version: 1.0
- GUID: {D356ED58-643D-45e6-BC31-CFA401E6C7D1}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—eaxcrmmustdetectserviceexpiryandnotifytheuserwhenrenewalisneeded
- Name: EAxCRM must detect service expiry and notify the user when renewal is needed
- ID: SAL-3
- Description: The system shall monitor service expiry dates and alert the user when a service needs renewal, using the expiry_month and renewal_notice_sent fields.
- Rationale: Services (SaaS/Training/Support) generate recurring revenue only if renewed before they lapse; without an automatic expiry check, a rep would have to remember every service's date manually, which doesn't scale past a handful of customers.
- Test Cases:
  - A Service with expiry_month in the current or next period appears in the renewal alert.
  - Once renewal_notice_sent is set, the same service isn't re-alerted for that cycle.
  - A renewed Service (new expiry_month set) drops off the alert list.
- Entities: Service
- Status: Proposed
- Version: 1.0
- GUID: {992E6F5B-B58C-4342-9CDE-E2B500446150}
- Parents:
  - eaxcrmmustsupportthesalesprocess

### Requirement—eaxcrmmustdistinguishprocuredservicesresoldfromavendorfromeaxpertisesownservices
- Name: EAxCRM must distinguish procured services (resold, from a Vendor) from EAxpertise's own services
- ID: SAL-2
- Description: The system shall allow services to be marked as either procured from an external vendor or provided directly by EAxpertise.
- Rationale: Margin and vendor-liability differ completely between reselling someone else's service and EAxpertise's own — conflating them would corrupt procurement reporting and make it impossible to tell which services depend on a third party's continued availability.
- Test Cases:
  - A Service marked as procured requires a linked Vendor; a Service marked as EAxpertise's own does not.
  - Procurement reports include only vendor-sourced Services, not EAxpertise's own.
  - Changing a Service from procured to own clears its Vendor link.
- Entities: Purchase, Service, Vendor
- Status: Proposed
- Version: 1.0
- GUID: {703B044E-64E9-4d7c-BDC4-BB81228306A6}
- Parents:
  - eaxcrmmustsupportthesalesprocess

### Requirement—eaxcrmmustencryptsensitivedatapasswordsatrest
- Name: EAxCRM must encrypt sensitive data (passwords) at rest
- ID: TEC-2
- Description: The system shall encrypt stored passwords and other sensitive credentials, such as IMAP account passwords, in the database.
- Rationale: IMAP credentials for three live mailboxes are stored in the database; if the SQLite file were ever copied or leaked, plaintext passwords would hand over full mailbox access, so at-rest encryption is a baseline security requirement, not optional hardening.
- Test Cases:
  - Inspecting the raw SQLite file does not reveal a plaintext IMAP password.
  - The application can still decrypt and use the stored password to authenticate an IMAP connection.
  - Rotating an IMAP account's password re-encrypts and replaces the stored value without leaving the old value recoverable.
- Entities: ImapAccount
- Status: Proposed
- Version: 1.0
- GUID: {F6EFB60E-E9F5-4ea1-8EBD-49692050E063}
- Parents:
  - eaxcrmmustuseaproductiongrademultiusercapablerelationaldatabase

### Requirement—eaxcrmmustenforceadraftreviewsendworkflowwithmanualapproval
- Name: EAxCRM must enforce a Draft -> Review -> Send workflow with manual approval
- ID: NWS-2
- Description: The system shall require newsletters to go through three states: Draft (composition), Review (manual approval), and Sent (dispatch).
- Rationale: A newsletter goes out to every opted-in customer at once — an unreviewed send (typo, broken link, wrong article) can't be recalled, so a mandatory human review gate before Sent is the only real safeguard.
- Test Cases:
  - A Newsletter cannot transition directly from Draft to Sent — Review is required in between.
  - A Newsletter in Review can be sent back to Draft for edits.
  - Only a Newsletter in Review state can be marked Sent, via an explicit approval action.
- Entities: Newsletter
- Status: Proposed
- Version: 1.0
- GUID: {8B155267-3A23-4059-B049-269CB4A7E809}
- Parents:
  - eaxcrmmustsupportcomposingnewslettersfromscrapedarticlesonsparxsystemscomandsparxsystemseu

### Requirement—eaxcrmmustenforceaminimum6weekintervalbetweennewsletters
- Name: EAxCRM must enforce a minimum 6-week interval between newsletters
- ID: NWS-4
- Description: The system shall prevent sending newsletters more frequently than once every six weeks to maintain appropriate communication cadence.
- Rationale: Sending more frequently than the audience expects risks being perceived as spam and increases opt-outs — six weeks matches the project's stated cadence and gives enough time for genuinely new Sparx content to accumulate.
- Test Cases:
  - Attempting to send a newsletter less than 6 weeks after the last Sent newsletter is blocked.
  - A newsletter exactly 6 weeks (or more) after the last Sent one is allowed.
  - The interval is measured from the last *Sent* newsletter, not from Draft/Review timestamps.
- Entities: Newsletter
- Status: Proposed
- Version: 1.0
- GUID: {1016A374-E514-4b33-896D-88A4F0646BC5}
- Parents:
  - eaxcrmmustsupportcomposingnewslettersfromscrapedarticlesonsparxsystemscomandsparxsystemseu

### Requirement—eaxcrmmustextractandstorelicenseentitlementsfromemailattachmentspdftxt
- Name: EAxCRM must extract and store license entitlements from email attachments (PDF/TXT)
- ID: CRM-3
- Description: The system shall parse PDF and TXT email attachments to extract license entitlement details and store them as License records.
- Rationale: License PDFs/TXT attachments already contain every field a License record needs (type, dates, entitlements) — re-typing them by hand duplicates work the vendor's own document already did and introduces transcription errors.
- Test Cases:
  - Parsing a known-format license PDF produces a License record with correct type, start, and expiry dates.
  - Parsing an attachment with an unrecognized format does not silently create a malformed License record.
  - Parsed License records reference the source Attachment for traceability.
- Entities: Attachment, License
- Status: Proposed
- Version: 1.0
- GUID: {670E2717-2306-45cd-A3FC-F6F8CF33D0F6}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—eaxcrmmustlinkdeliveriestothecustomerthesalesinvoicetheyfulfillandtheattachmentsincluded
- Name: EAxCRM must link deliveries to the Customer, the SalesInvoice they fulfill, and the attachments included
- ID: DEL-2
- Description: The system shall associate each delivery record with the customer it was sent to, the sales invoice it fulfills, and the license files or documents attached.
- Rationale: A delivery in isolation ("we sent an email") is not useful for support or auditing — it only answers something when it's tied to *who* received it, *which invoice* it fulfilled, and *what files* were actually attached.
- Test Cases:
  - A Delivery record references exactly one Customer and at most one SalesInvoice it fulfills.
  - Attachments included in a Delivery are queryable from the Delivery record.
  - Deleting a SalesInvoice does not delete Deliveries that reference it — delivery history must survive.
- Entities: Attachment, Customer, Delivery, SalesInvoice
- Status: Proposed
- Version: 1.0
- GUID: {55A87EA4-3D17-4a2a-8DE6-DB0F1B57DA91}
- Parents:
  - eaxcrmmustrecorddeliveryemailscontaininglicensefilesandorserviceagreements

### Requirement—eaxcrmmustlinkeachsalesinvoicetoitsoriginatingoffer
- Name: EAxCRM must link each SalesInvoice to its originating Offer
- ID: SAL-4
- Description: The system shall maintain a reference from each SalesInvoice back to the Offer that generated it, ensuring auditability of the sales process.
- Rationale: Without a stored reference back to the Offer, there's no way to verify an invoice actually matches what was proposed and agreed — auditability of the sales process depends on this chain being unbroken.
- Test Cases:
  - A SalesInvoice created from an Offer stores a reference to that Offer.
  - Given a SalesInvoice, the originating Offer's line items/amount can be looked up.
  - Reports can trace revenue back to the originating Offer for any SalesInvoice.
- Entities: Offer, SalesInvoice
- Status: Proposed
- Version: 1.0
- GUID: {37F7E8D8-D5BD-46ec-B91A-7ED6F2E5B781}
- Parents:
  - eaxcrmmustsupportthesalesprocess

### Requirement—eaxcrmmustoperatewithoutaidependencies
- Name: EAxCRM must operate without AI dependencies
- ID: TEC-4
- Description: The system shall operate entirely without AI dependencies, using traditional parsing and scraping libraries such as PyMuPDF and BeautifulSoup.
- Rationale: Keeps the system deployable and predictable on a QNAP NAS with limited compute and no external API dependency/cost — parsing and scraping needs (PDF, HTML) are well served by deterministic libraries, so an AI dependency would add operational risk for no functional gain today.
- Test Cases:
  - The application has zero calls to any external AI/LLM API at runtime.
  - Document parsing (PDF/TXT) uses PyMuPDF only, with no ML-based extraction fallback.
  - The app runs fully offline except for the deliberate IMAP/scraping network calls (no internet-dependent AI service).
- Status: Proposed
- Version: 1.0
- GUID: {6A62DFB5-CBE7-4397-8640-263F0C242661}
- Parents:
  - eaxcrmmustuseaproductiongrademultiusercapablerelationaldatabase

### Requirement—eaxcrmmustprovideadashboardofupcomingservicerenewals
- Name: EAxCRM must provide a dashboard of upcoming service renewals
- ID: RPT-2
- Description: The system shall display a dashboard showing all services approaching their expiry date, sorted by urgency, to enable proactive renewal management.
- Rationale: Reactive renewal handling (waiting for a customer to complain about a lapsed license) loses revenue and damages trust — a proactive, urgency-sorted dashboard lets reps reach out before expiry instead of after.
- Test Cases:
  - Services within the renewal window appear on the dashboard, sorted soonest-expiry first.
  - A renewed service (expiry_month pushed out) drops off or moves down the dashboard accordingly.
  - The dashboard reflects auto_renew status so reps don't chase renewals that are already handled automatically.
- Entities: Service
- Status: Proposed
- Version: 1.0
- GUID: {9646F376-4EC0-4dfc-B050-239BA21CC691}
- Parents:
  - eaxcrmmustprovideaviewofallcustomerlicenseentitlementswithstartexpirydates

### Requirement—eaxcrmmustprovideprocurementreportsgroupedbyvendor
- Name: EAxCRM must provide procurement reports grouped by Vendor
- ID: RPT-3
- Description: The system shall generate reports summarizing procurements per vendor, including quote amounts, invoice totals, and payment status.
- Rationale: Spend and payment-status visibility per vendor is needed for cash-flow planning and vendor-relationship decisions (e.g. is Sparx Systems LTD or EU cheaper for a given license type) — without grouping by vendor this comparison requires manual spreadsheet work.
- Test Cases:
  - A report for a given Vendor totals quote amounts and invoice totals correctly across all its Purchases.
  - Payment status (paid/pending) is visible per procurement line in the report.
  - Switching the report's vendor filter changes only the displayed rows, not the underlying data.
- Entities: ProcurementInvoice, Quote, Vendor
- Status: Proposed
- Version: 1.0
- GUID: {D938A51D-6BF2-4882-9B88-035B63007259}
- Parents:
  - eaxcrmmustprovideaviewofallcustomerlicenseentitlementswithstartexpirydates

### Requirement—eaxcrmmustrunonwindowsfordevelopmentanddockerqnapnasforproduction
- Name: EAxCRM must run on Windows for development and Docker/QNAP NAS for production
- ID: TEC-5
- Description: The system shall support native Windows development and Docker-based deployment on a QNAP NAS for production use.
- Rationale: The developer's daily machine is Windows, but the always-on production host is a QNAP NAS — the app must work identically in both environments without code changes, only deployment configuration differing.
- Test Cases:
  - The app runs correctly via `runserver` on native Windows during development.
  - The same codebase runs unmodified inside a Docker container on QNAP Container Station.
  - Database file paths and settings are environment-configurable, not hardcoded to a Windows path.
- Status: Proposed
- Version: 1.0
- GUID: {82C5CC76-459B-49e5-AD85-A406DA3E2E53}
- Parents:
  - eaxcrmmustuseaproductiongrademultiusercapablerelationaldatabase

### Requirement—eaxcrmmustshowauxthatshowsthecurrentstateofprocurement
- Name: EAxCRM must show a UX that shows the current state of Procurement
- ID: RPT-4
- Description: The system shall display the current procurement state per vendor including which quotes have been received and which invoices are paid or pending.
- Rationale: "What's still outstanding with our vendors" is a recurring operational question (which quotes are we waiting on, which invoices are unpaid) that shouldn't require opening individual Purchase records one at a time.
- Test Cases:
  - The view shows, per Vendor, which quotes have been received and which are still outstanding.
  - Invoice payment status (paid/pending) is visible alongside each procurement line.
  - The view updates immediately when a new Quote or ProcurementInvoice is recorded.
- Entities: ProcurementInvoice, Quote, Vendor
- Status: Proposed
- Version: 1.0
- GUID: {2FC71345-5D8C-432b-B123-CC9F89E1B818}
- Parents:
  - eaxcrmmustsupporttheprocurementprocess

### Requirement—eaxcrmmuststorecommunicationhistorypercustomerretrievedfrommultipleimapaccountshaneaxpertisenlsaleseaxpertisenlinfoeaxpertisenl
- Name: EAxCRM must store communication history per customer, retrieved from multiple IMAP accounts (han@eaxpertise.nl, sales@eaxpertise.nl, info@eaxpertise.nl)
- ID: CRM-2
- Description: The system shall fetch and store emails from three IMAP accounts and associate them with the relevant customer for a complete communication history.
- Rationale: Support and sales context lives in email threads across three different mailboxes (han@, sales@, info@) — without consolidating them per customer, a rep has to manually search three inboxes to reconstruct history with any given customer.
- Test Cases:
  - Emails fetched from all three configured IMAP accounts are associated with the correct Customer based on sender/recipient address matching.
  - An email that doesn't match any known Customer is not silently dropped — it's flagged/left unassigned for manual linking.
  - A customer's communication history view shows emails from all three mailboxes in one chronological list.
- Entities: Communication, ImapAccount
- Status: Proposed
- Version: 1.0
- GUID: {7DEA2FF6-9EAC-47da-BE8B-9414FAFBF5DD}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—eaxcrmmuststoredocumentsquotesinvoicesdeliverieslinkedtocustomers
- Name: EAxCRM must store documents (quotes, invoices, deliveries) linked to customers
- ID: CRM-5
- Description: The system shall store customer-facing documents such as Sparx Systems quotes, incoming invoices, and delivery notes, linked to the relevant customer record.
- Rationale: Quotes, invoices, and delivery notes are the paper trail of the customer relationship — keeping them attached to the Customer record, rather than scattered across email/OneDrive, means a rep can answer "what have we sent/billed this customer" in one place.
- Test Cases:
  - A Quote, ProcurementInvoice, and Delivery can each be linked to a specific Customer.
  - All documents for a Customer are retrievable from that Customer's record.
  - Documents remain linked correctly if the same Customer has multiple concurrent Purchases.
- Entities: Customer, Delivery, ProcurementInvoice, Quote
- Status: Proposed
- Version: 1.0
- GUID: {3111DD70-D016-4cad-B7CC-D8FA9D63FAF0}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—eaxcrmmuststorevendorbankdetailsibanbicswiftpaymentcurrency
- Name: EAxCRM must store vendor bank details (IBAN, BIC/SWIFT, payment currency)
- ID: PRO-3
- Description: The system shall record vendor bank account information including IBAN, BIC/SWIFT code, and default payment currency for invoice processing.
- Rationale: Paying an incoming invoice requires knowing where to send the money and in what currency — storing IBAN/BIC/currency once per Vendor avoids re-sourcing payment details, and risking a wrong-account payment, every time an invoice comes in.
- Test Cases:
  - A Vendor record stores IBAN, BIC/SWIFT, and a default payment currency.
  - Vendor bank details are visible when processing a ProcurementInvoice for that vendor.
  - Two Vendors can have different default payment currencies without conflict (e.g. one EUR, one USD).
- Entities: Vendor
- Status: Proposed
- Version: 1.0
- GUID: {C7244ED6-A70C-43a2-A6C3-4A5D8AFD6A95}
- Parents:
  - eaxcrmmustsupporttheprocurementprocess

### Requirement—eaxcrmmustsupportmulticurrencyinvoiceseurusdfromsparxsystems
- Name: EAxCRM must support multi-currency invoices (EUR, USD) from Sparx Systems
- ID: PRO-4
- Description: The system shall handle incoming invoices in both EUR and USD from Sparx Systems and its subsidiaries.
- Rationale: Sparx Systems' entities invoice in different currencies depending on region/subsidiary — a single-currency assumption would make it impossible to record invoices accurately or reconcile actual spend.
- Test Cases:
  - A ProcurementInvoice can be recorded with currency = EUR.
  - A ProcurementInvoice can be recorded with currency = USD.
  - Reports correctly separate or convert totals across the two currencies rather than silently summing mismatched currencies together.
- Entities: ProcurementInvoice
- Status: Proposed
- Version: 1.0
- GUID: {9615BF5D-D930-4353-858D-0F75F8DA37C5}
- Parents:
  - eaxcrmmustsupporttheprocurementprocess

### Requirement—eaxcrmmusttracklicenserenewalslinkedtotheoriginalpurchase
- Name: EAxCRM must track license renewals linked to the original purchase
- ID: CRM-4
- Description: The system shall support creating renewal licenses that reference the original purchase record, enabling tracking of the full license lifecycle.
- Rationale: A renewal is conceptually a continuation of an earlier license, not a brand-new unrelated purchase — keeping the link lets a rep trace a customer's full license lifecycle instead of seeing disconnected fragments.
- Test Cases:
  - A renewal License record references the original Purchase it renews.
  - Querying a customer's license lifecycle shows the original purchase and all subsequent renewals in order.
  - A renewal License does not require re-entering data already present on the original Purchase.
- Entities: License, Purchase
- Status: Proposed
- Version: 1.0
- GUID: {B1887963-752B-404c-A21E-19BBF6A32F80}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—eaxcrmmusttrackpercontactdeliverystatussentopenedbounced
- Name: EAxCRM must track per-contact delivery status (sent, opened, bounced)
- ID: NWS-3
- Description: The system shall record whether each newsletter contact received, opened, or bounced the newsletter to measure engagement.
- Rationale: Newsletter engagement is the only real signal of whether the newsletter is reaching and working for a given contact — without it, EAxpertise can't tell a stale/dead email address from an active one.
- Test Cases:
  - Sending a Newsletter creates a NewsletterContact record per recipient with an initial "sent" status.
  - Opening the newsletter (tracked open) updates the corresponding NewsletterContact's opened_date.
  - A bounced delivery marks the NewsletterContact as bounced rather than sent.
- Entities: Contact, Newsletter, NewsletterContact
- Status: Proposed
- Version: 1.0
- GUID: {218F552E-5931-417c-A02B-DAE8B9F69C78}
- Parents:
  - eaxcrmmustsupportcomposingnewslettersfromscrapedarticlesonsparxsystemscomandsparxsystemseu

### Requirement—eaxcrmmustusethedjangoadmininterfaceasitsprimaryui
- Name: EAxCRM must use the Django Admin interface as its primary UI
- ID: TEC-3
- Description: The system shall use Django's built-in admin interface as the primary user interface for all CRM operations.
- Rationale: Building a custom UI is unnecessary effort for an internal single-tenant tool with a handful of users — Django Admin already provides CRUD, search, and filtering out of the box, keeping the project scoped to Django + SQLite with no separate frontend to maintain.
- Test Cases:
  - Every core entity (Customer, Contact, License, Offer, etc.) is manageable (create/edit/delete) through Django Admin.
  - List views support the filtering/search needed for day-to-day rep use (e.g. filter contacts by role).
  - No entity requires a custom-built page outside Django Admin to be usable.
- Status: Proposed
- Version: 1.0
- GUID: {FA4583F4-87B2-4685-9904-EB9A14B63BF3}
- Parents:
  - eaxcrmmustuseaproductiongrademultiusercapablerelationaldatabase

### Requirement—newsletterconsentruleoptindefaultstofalse
- Name: Newsletter Consent Rule: opt-in defaults to false
- ID: CRM-11
- Description: Contact.opt_in shall default to False when created via Create Customer Account, and shall only be set True if the rep has explicit evidence of consent in the source email. The same field must remain independently editable later via the existing Suggest Newsletter Opt-in screen.
- Rationale: Marketing consent is a legal/compliance flag and must never be inferred just because a customer initiated contact; giving reps two deliberate checkpoints (creation-time and a later prompt) increases the chance of capturing real consent without ever defaulting to true.
- Test Cases:
  - New Contact via create screen has opt_in=False when the checkbox is left untouched.
  - Checking the box at creation sets opt_in=True and stamps opt_in_date.
  - opt_in can later be toggled from the Suggest Newsletter Opt-in screen independent of the create screen's state.
- Entities: Contact
- Status: Proposed
- Version: 1.0
- GUID: {EAAD0687-E661-4943-93EB-86376B3FA8EF}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—primarycontactruleatleastonecontactmustalwaysbeprimary
- Name: Primary Contact Rule: at least one Contact must always be Primary
- ID: CRM-8
- Description: Regardless of how many Contacts are entered on account creation, exactly one must carry the role Primary. This holds even when only one Contact is entered — in that case the first (and only) Contact row defaults its role to Primary automatically rather than being left blank.
- Rationale: Ensures every account always has one unambiguous point of contact, and gives a clear successor path when combined with the Secondary role (CRM-10).
- Test Cases:
  - Single-contact save with role left untouched saves with role = Primary.
  - Two-contact save where neither is marked Primary is rejected.
  - Two-contact save with exactly one Primary succeeds.
- Entities: Contact, Customer
- Status: Proposed
- Version: 1.0
- GUID: {5E968ECB-4896-45fa-9FAE-4518F9F92ECF}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—procurementcanbedoneviaabilityengineering
- Name: Procurement can be done via Ability Engineering
- ID: PRO-5.3
- Description: Ability Engineering is a reseller of Sparx Systems licenses, providing an alternative procurement channel.
- Rationale: Recording Ability Engineering as its own Vendor lets purchases through this specific reseller be tracked and reported on independently of Sparx Systems' own channels.
- Test Cases:
  - A Vendor record for Ability Engineering can be created and linked to Purchases.
  - Procurement reports can filter/group specifically to Ability Engineering.
  - Ability Engineering coexists with the other Vendor records without ID or name collisions.
- Entities: Vendor
- Status: Approved
- Version: 1.0
- GUID: {675A33C1-835A-4fda-8B97-50BA072EAFA1}
- Parents:
  - procurementcanbedoneviamultipleparties

### Requirement—procurementcanbedoneviaprolaborate
- Name: Procurement can be done via Prolaborate
- ID: PRO-5.4
- Description: Prolaborate sells hosting services: hosting platform of Pro Cloud and EA SaaS.
- Rationale: Prolaborate is a distinct procurement channel specifically for hosting rather than licenses — tracking it separately from license vendors keeps hosting spend visible on its own line rather than blended into general license procurement.
- Test Cases:
  - A Vendor record for Prolaborate can be created and linked to Purchases for hosting services.
  - Procurement reports can filter/group specifically to Prolaborate.
  - Prolaborate purchases are distinguishable from Sparx Systems license purchases in reporting.
- Entities: Vendor
- Status: Approved
- Version: 1.0
- GUID: {492044AB-6D15-4455-B6D0-7C8F950480BC}
- Parents:
  - procurementcanbedoneviamultipleparties

### Requirement—procurementcanbedoneviasparxsystemseu
- Name: Procurement can be done via Sparx Systems EU
- ID: PRO-5.2
- Description: Sparx Systems EU is the European reseller of Sparx Systems licenses serving the EU market.
- Rationale: EU-region customers are typically procured through Sparx Systems EU rather than the Australian HQ — tracking it as its own Vendor keeps regional procurement (and any EU-specific pricing/currency) separate from LTD's.
- Test Cases:
  - A Vendor record for Sparx Systems EU can be created and linked to Purchases.
  - Procurement reports can filter/group specifically to Sparx Systems EU.
  - Sparx Systems EU and Sparx Systems LTD coexist as distinct Vendor records without being conflated.
- Entities: Vendor
- Status: Approved
- Version: 1.0
- GUID: {CEBF5E06-3BF4-4909-96A8-D91004A36647}
- Parents:
  - procurementcanbedoneviamultipleparties

### Requirement—procurementcanbedoneviasparxsystemsltd
- Name: Procurement can be done via Sparx Systems LTD
- ID: PRO-5.1
- Description: Sparx Systems LTD is the Australian headquarters and primary reseller of Sparx Systems licenses.
- Rationale: As the Australian headquarters and primary reseller, most core Sparx EA license procurement flows through this Vendor — it needs its own record so it isn't conflated with regional resellers or specialty partners covered by the other PRO-5.x vendors.
- Test Cases:
  - A Vendor record for Sparx Systems LTD can be created and linked to Purchases.
  - Procurement reports can filter/group specifically to Sparx Systems LTD.
  - The majority of License-related Purchases can be traced back to this Vendor.
- Entities: Vendor
- Status: Approved
- Version: 1.0
- GUID: {AE2C78B0-A8C3-4aef-B5AE-3C0AB921189B}
- Parents:
  - procurementcanbedoneviamultipleparties

### Requirement—duplicatedetectionfuzzymatchoncontactemailandorganisationname
- Name: Duplicate Detection: fuzzy-match on Contact email and organisation name
- ID: CRM-13
- Description: Immediately after Create Customer Account, the system shall fuzzy-match the new account's organisation name (Customer.name) and initial Contact.email against every existing Customer/Contact pair and flag the account as a likely duplicate if either matches closely enough. The result drives the "Duplicate found?" exclusive gateway — a match routes to Merge Customer Accounts, no match routes to Retrieve Customer Email History. Exact match thresholds/algorithm are an implementation detail deferred to build time, not fixed at the model level.
- Rationale: A fresh account can't be trusted to be genuinely new just because the rep didn't recognise the org — the same organisation reaches out under slightly different spellings or via a different contact often enough that skipping this check would silently grow duplicate Customer records, fragmenting license/communication history across them.
- Test Cases:
  - Creating an account with an organisation name that closely matches an existing Customer (e.g. minor spelling variation) is flagged as a likely duplicate.
  - Creating an account whose initial Contact.email matches an existing Contact's email is flagged as a likely duplicate, even if the organisation name differs.
  - An account with no close match on either field is not flagged, and the process proceeds directly to Retrieve Customer Email History.
- Entities: Contact, Customer
- Status: Proposed
- Version: 1.0
- GUID: {5D5B7251-46A9-45D2-9166-394C20FBE172}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—accountmergefoldsaflaggedduplicateintoanexistingaccountwithanaudittrail
- Name: Account Merge: folds a flagged duplicate into an existing account with an audit trail
- ID: CRM-14
- Description: When Merge Customer Accounts is performed on a flagged duplicate, the losing Customer's data (Contact/notes) shall be folded into the surviving Customer chosen by the user, and the losing Customer record shall be retained (not deleted) with its Customer.merged_into field set to the surviving Customer. Any resulting duplicate Contact records are removed manually by the rep as a separate action, not automatically by the merge itself. The process ends at Merged into Existing Account — no new Customer Account is created.
- Rationale: Deleting the losing record outright would destroy the audit trail of what happened to it; merged_into keeps "what happened to Customer X" answerable after the fact, while leaving orphaned-Contact cleanup manual avoids the merge silently deleting a Contact the rep still wanted to review first.
- Test Cases:
  - Merging Customer A (duplicate) into Customer B sets Customer A.merged_into = Customer B and does not delete Customer A's row.
  - After merge, Customer A's Contact(s) still exist and are queryable, pending manual removal by the rep.
  - The process reaches the Merged into Existing Account end event, and no new Customer record is created for the flagged duplicate.
- Entities: Customer
- Status: Proposed
- Version: 1.0
- GUID: {2E43D3B1-43D2-4954-B723-534FE8E70BA6}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—emailhistoryretrievalscansonnoduplicateanddedupesonrescan
- Name: Email History Retrieval: scans on no-duplicate and dedupes on re-scan
- ID: CRM-15
- Description: When the Duplicate found? gateway resolves to no duplicate, the system shall run Retrieve Customer Email History, scanning the three configured IMAP mailboxes (han@eaxpertise.nl, sales@eaxpertise.nl, info@eaxpertise.nl) for messages matching the account's Contact.email, and append newly matched Communications to the account's Email History. Communications already linked from a prior run of this activity are not re-added on a subsequent scan. An email that doesn't match any known Contact is flagged for manual linking rather than dropped (per CRM-2). This activity is distinct from CreateAccountScreen's "Search Emails" domain lookup, which only prefills fields before the account exists.
- Rationale: Staff need a reliable, one-click view of everything a Customer Account has ever communicated without manually searching three mailboxes — but re-running the scan (e.g. after new mail arrives) must not double up the history with Communications already linked, or the view stops being trustworthy.
- Test Cases:
  - After a non-duplicate account reaches Retrieve Customer Email History, matching emails from all three IMAP mailboxes appear in the account's Email History.
  - Re-running Retrieve Customer Email History for the same account after new mail arrives adds only the new Communications, not duplicates of ones already linked.
  - An email whose sender/recipient doesn't match any known Contact is flagged for manual linking rather than silently discarded.
- Entities: Communication, Contact
- Status: Proposed
- Version: 1.0
- GUID: {E342B1B4-E82D-457D-A525-70D21CDBEF6F}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—newsletteroptinsuggestiontriggersonlyforprimaryorlicenseholderroleandneverautosets
- Name: Newsletter Opt-in Suggestion: triggers only for Primary/License Holder role, never auto-sets
- ID: CRM-16
- Description: After Retrieve Customer Email History, the system shall check the account's Contact.role at the "Primary or License Holder role?" gateway. Only when the Contact carries the Primary or License Holder role does the process route to Suggest Newsletter Opt-in; any other role (or no role) routes straight to Account Ready. Suggest Newsletter Opt-in only sets Contact.opt_in and Contact.opt_in_date after the rep explicitly confirms — the suggestion itself never sets them. This is distinct from CRM-11, which governs the opt_in default (False) at account-creation time on CreateAccountScreen.
- Rationale: Primary and License Holder are the two roles most likely to be the right person to ask about newsletter consent, so limiting the prompt to them avoids pestering every Contact on an account; requiring explicit confirmation (rather than the gateway match itself setting opt_in) keeps consent an affirmative, auditable action rather than an inferred one, consistent with CRM-11's consent principle.
- Test Cases:
  - An account whose Contact role is Primary or License Holder reaches Suggest Newsletter Opt-in after email history retrieval.
  - An account whose Contact role is Purchase, Sales, Secondary, or unset routes directly to Account Ready, skipping the suggestion.
  - Reaching Suggest Newsletter Opt-in does not itself change Contact.opt_in — it only changes after the rep explicitly confirms.
- Entities: Contact
- Status: Proposed
- Version: 1.0
- GUID: {B69CEC39-9EE8-4B9D-9EB5-191221825829}
- Parents:
  - eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder

### Requirement—procurementmustbetrackablepervendorwithlinkedquoteandprocurementinvoicepdfs
- Name: Procurement must be trackable per Vendor with linked Quote and ProcurementInvoice PDFs
- ID: PRO-2
- Description: The system shall allow each procurement to be tracked per vendor, with digital copies of the original quote and the incoming invoice stored as attachments.
- Rationale: A procurement record without its supporting documents can't be independently verified later — attaching the PDFs directly to the Purchase/Vendor chain means the paper trail survives even if the original email is deleted.
- Test Cases:
  - A Purchase stores a reference to both the original Quote PDF and the incoming ProcurementInvoice PDF.
  - Procurements can be filtered/grouped by Vendor and show their attached documents.
  - A Purchase missing either PDF is visibly flagged as incomplete rather than silently accepted.
- Entities: ProcurementInvoice, Quote, Vendor
- Status: Proposed
- Version: 1.0
- GUID: {5DA68B35-5206-46cb-B4D1-A38D8D655197}
- Parents:
  - eaxcrmmustsupporttheprocurementprocess

