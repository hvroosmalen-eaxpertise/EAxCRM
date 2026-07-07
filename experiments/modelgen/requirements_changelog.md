## 2026-07-07 18:29:39 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| eaxcrmmustsupporttheprocurementprocess | EAxCRM must support the procurement process | Requirement | {119DE89A-BFF5-44ab-AC67-6FC9DB0F8C10} | Notes: The system shall manage the end-to-end procurement workflow from receiving a supplier quote, creating a purchase record, and recording the incoming invoice.

<b>Rationale:</b>
Every license/service EAxpertise resells is first procured from a vendor; without a structured procurement record there's no way to reconcile what was bought, at what cost, against what's later sold or entitled to a customer.

<b>Test Cases:</b>
1.	A Quote can be linked to a Purchase and the Purchase linked to a ProcurementInvoice, forming a complete chain.
2.	A Purchase cannot be created without a Vendor.
3.	The procurement workflow state (quote received → purchased → invoiced) is visible per Purchase. -> The system shall manage the end-to-end procurement workflow from receiving a supplier quote, creating a purchase record, and recording the incoming invoice.

<b>Rationale:</b>
Every license/service EAxpertise resells is first procured from a vendor; without a structured procurement record there's no way to reconcile what was bought, at what cost, against what's later sold or entitled to a customer.

<b>Test Cases:</b>
1.	A Quote can be linked to a Purchase and the Purchase linked to a ProcurementInvoice, forming a complete chain.
2.	A Purchase cannot be created without a Vendor.
3.	The procurement workflow state (quote received → purchased → invoiced) is visible per Purchase.
 |
| eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder | EAxCRM must manage Customer organizations and their Contacts with specific roles (Primary, Purchase, Sales, License Holder) | Requirement | {C8A09A87-5B2B-4d72-896F-77C079F7C2DA} | Notes: The system shall store customer organizations and their associated contacts, each with one or more roles that determine their function in the CRM workflow.

<b>Rationale:</b>
EAxpertise sells to organizations, not individuals — but every interaction is actually with a named person, so both levels must be tracked, and the multi-role model (Primary/Purchase/Sales/License Holder) reflects that different people at the same customer often own different parts of the relationship.

<b>Test Cases:</b>
1.	A Customer can have multiple Contacts, each with one or more roles.
2.	A Contact's role can be changed without affecting Customer data.
3.	Filtering contacts by role (e.g. License Holder) returns only contacts with that role at that customer. -> The system shall store customer organizations and their associated contacts, each with one or more roles that determine their function in the CRM workflow.

<b>Rationale:</b>
EAxpertise sells to organizations, not individuals — but every interaction is actually with a named person, so both levels must be tracked, and the multi-role model (Primary/Purchase/Sales/License Holder) reflects that different people at the same customer often own different parts of the relationship.

<b>Test Cases:</b>
1.	A Customer can have multiple Contacts, each with one or more roles.
2.	A Contact's role can be changed without affecting Customer data.
3.	Filtering contacts by role (e.g. License Holder) returns only contacts with that role at that customer.
 |
| eaxcrmmustusesqliteasitsdatabasebackend | EAxCRM must use SQLite as its database backend | Requirement | {30EA2FCA-BEA7-4fd7-A7E8-F5ECD78B8ADF} | Notes: The system shall use a file-based SQLite database suitable for deployment on a QNAP NAS without requiring a separate database server.

<b>Rationale:</b>
The production target is a QNAP NAS with no separate database server process; SQLite's file-based, zero-admin nature avoids operating a DB server on constrained NAS hardware.

<b>Test Cases:</b>
1.	The Django app runs against a single .db file with no external DB service running.
2.	Standard Django migrations apply cleanly against the SQLite backend.
3.	The application starts and serves requests on a fresh QNAP Docker deployment with only the .db file present. -> The system shall use a file-based SQLite database suitable for deployment on a QNAP NAS without requiring a separate database server.

<b>Rationale:</b>
The production target is a QNAP NAS with no separate database server process; SQLite's file-based, zero-admin nature avoids operating a DB server on constrained NAS hardware.

<b>Test Cases:</b>
1.	The Django app runs against a single .db file with no external DB service running.
2.	Standard Django migrations apply cleanly against the SQLite backend.
3.	The application starts and serves requests on a fresh QNAP Docker deployment with only the .db file present.
 |
| eaxcrmmustsupportcomposingnewslettersfromscrapedarticlesonsparxsystemscomandsparxsystemseu | EAxCRM must support composing newsletters from scraped articles on SparxSystems.com and sparxsystems.eu | Requirement | {153BD677-35A4-4252-BEC1-20B170577F99} | Notes: The system shall scrape news articles from SparxSystems.com and sparxsystems.eu and allow composing an EAxNewsletter from selected article summaries and links.

<b>Rationale:</b>
EAxpertise doesn't produce original content for its newsletter — SparxSystems.com/.eu already publish the source material, so scraping and curating from there is cheaper than authoring from scratch and keeps the newsletter tied to what Sparx itself is announcing.

<b>Test Cases:</b>
1.	Scraping SparxSystems.com and sparxsystems.eu produces Article records with heading, summary, and source link.
2.	A Newsletter can be composed by selecting a subset of scraped Articles.
3.	Re-scraping does not duplicate Articles already stored for the same source URL. -> The system shall scrape news articles from SparxSystems.com and sparxsystems.eu and allow composing an EAxNewsletter from selected article summaries and links.

<b>Rationale:</b>
EAxpertise doesn't produce original content for its newsletter — SparxSystems.com/.eu already publish the source material, so scraping and curating from there is cheaper than authoring from scratch and keeps the newsletter tied to what Sparx itself is announcing.

<b>Test Cases:</b>
1.	Scraping SparxSystems.com and sparxsystems.eu produces Article records with heading, summary, and source link.
2.	A Newsletter can be composed by selecting a subset of scraped Articles.
3.	Re-scraping does not duplicate Articles already stored for the same source URL.
 |
| eaxcrmmustsupportthesalesprocess | EAXCRM must support the sales process | Requirement | {0475B655-DAC3-4672-A10B-4B1C42DC4E44} | Notes: The system shall manage the sales workflow from creating an Offer to generating a SalesInvoice for the customer.

<b>Rationale:</b>
Every customer-facing sale needs a documented trail from proposal to billing so revenue can be reconciled and disputes resolved — without an Offer→SalesInvoice link, there's no record of what was actually agreed before an invoice was raised.

<b>Test Cases:</b>
1.	An Offer can be created for a Customer and later converted into a SalesInvoice.
2.	A SalesInvoice cannot exist without a Customer.
3.	The sales workflow state is visible per Offer (open, accepted, invoiced). -> The system shall manage the sales workflow from creating an Offer to generating a SalesInvoice for the customer.

<b>Rationale:</b>
Every customer-facing sale needs a documented trail from proposal to billing so revenue can be reconciled and disputes resolved — without an Offer→SalesInvoice link, there's no record of what was actually agreed before an invoice was raised.

<b>Test Cases:</b>
1.	An Offer can be created for a Customer and later converted into a SalesInvoice.
2.	A SalesInvoice cannot exist without a Customer.
3.	The sales workflow state is visible per Offer (open, accepted, invoiced).
 |
| eaxcrmmustprovideaviewofallcustomerlicenseentitlementswithstartexpirydates | EAxCRM must provide a view of all customer license entitlements with start/expiry dates | Requirement | {695AC932-66C2-43d0-B242-A9BE87C30800} | Notes: The system shall display a consolidated view of each customer's active and expired license entitlements including their start and end dates.

<b>Rationale:</b>
Reps need a single place to answer "what does this customer currently own and when does it expire" without cross-referencing multiple purchase records by hand — this is the most common support/renewal question.

<b>Test Cases:</b>
1.	The view lists all License records for a customer with start and expiry dates.
2.	Expired licenses are visually distinguished from active ones.
3.	The view updates immediately after a new License is added via a Purchase. -> The system shall display a consolidated view of each customer's active and expired license entitlements including their start and end dates.

<b>Rationale:</b>
Reps need a single place to answer "what does this customer currently own and when does it expire" without cross-referencing multiple purchase records by hand — this is the most common support/renewal question.

<b>Test Cases:</b>
1.	The view lists all License records for a customer with start and expiry dates.
2.	Expired licenses are visually distinguished from active ones.
3.	The view updates immediately after a new License is added via a Purchase.
 |
| eaxcrmmustrecorddeliveryemailscontaininglicensefilesandorserviceagreements | EAxCRM must record delivery emails containing license files and/or service agreements | Requirement | {2553EA37-D4C2-4c1c-BA2B-65ADD9C06F80} | Notes: The system shall store delivery emails sent to customers that contain license registration files and/or service agreement documents.

<b>Rationale:</b>
Delivery emails are the customer's proof that they received their license file/agreement — without a record, support has no way to confirm what was actually sent versus what the customer claims (or fails to claim) they received.

<b>Test Cases:</b>
1.	A Delivery record captures the sent date, recipient address, subject, and body of the delivery email.
2.	A Delivery can be linked to the license file(s) or agreement document(s) it contained.
3.	Delivery status (sent/failed) is recorded and queryable. -> The system shall store delivery emails sent to customers that contain license registration files and/or service agreement documents.

<b>Rationale:</b>
Delivery emails are the customer's proof that they received their license file/agreement — without a record, support has no way to confirm what was actually sent versus what the customer claims (or fails to claim) they received.

<b>Test Cases:</b>
1.	A Delivery record captures the sent date, recipient address, subject, and body of the delivery email.
2.	A Delivery can be linked to the license file(s) or agreement document(s) it contained.
3.	Delivery status (sent/failed) is recorded and queryable.
 |
| eaxcrmmustsupportdraganddropdocumentingestionthatautomaticallyparsesandfillsentities | EAxCRM must support drag-and-drop document ingestion that automatically parses and fills entities | Requirement | {7248B806-6768-40d0-87E7-FEDE7509892A} | Notes: The system shall allow a user to drag and drop a document (PDF, TXT, email file) onto the UI, which then automatically parses the content and populates the correct entities (License, LicenseLineItem, Service, Quote, ProcurementInvoice, Communication, Contact) as accurately as possible, reducing manual data entry.

<b>Rationale:</b>
License PDFs, quotes, and invoices arrive as email attachments constantly; manually re-typing their contents into the CRM is slow and error-prone, so automatic parsing turns an existing document into structured data with minimal rep effort.

<b>Test Cases:</b>
1.	Dropping a license PDF creates/updates the corresponding License and LicenseLineItem records with parsed values.
2.	Dropping an unparseable or unrecognized document does not corrupt existing records — it flags for manual review instead.
3.	Parsed field values can be reviewed/corrected by the rep before being saved. -> The system shall allow a user to drag and drop a document (PDF, TXT, email file) onto the UI, which then automatically parses the content and populates the correct entities (License, LicenseLineItem, Service, Quote, ProcurementInvoice, Communication, Contact) as accurately as possible, reducing manual data entry.

<b>Rationale:</b>
License PDFs, quotes, and invoices arrive as email attachments constantly; manually re-typing their contents into the CRM is slow and error-prone, so automatic parsing turns an existing document into structured data with minimal rep effort.

<b>Test Cases:</b>
1.	Dropping a license PDF creates/updates the corresponding License and LicenseLineItem records with parsed values.
2.	Dropping an unparseable or unrecognized document does not corrupt existing records — it flags for manual review instead.
3.	Parsed field values can be reviewed/corrected by the rep before being saved.
 |
| procurementcanbedoneviamultipleparties | Procurement can be done via multiple parties | Requirement | {506DEB0C-8BE3-4a76-B52E-E00F3DBB672E} | Notes: There are several suppliers to EAxpertise.

<b>Rationale:</b>
EAxpertise doesn't buy exclusively from Sparx Systems' HQ — regional resellers (EU, LTD) and specialty partners (Ability Engineering, Prolaborate) each cover different products/regions, so the data model must support more than one Vendor per procurement category.

<b>Test Cases:</b>
1.	More than one Vendor record can exist and each can be linked to independent Purchases.
2.	A Purchase records exactly one Vendor (the party actually procured from for that transaction).
3.	Reports can be grouped/filtered by Vendor across all procurement. -> There are several suppliers to EAxpertise.

<b>Rationale:</b>
EAxpertise doesn't buy exclusively from Sparx Systems' HQ — regional resellers (EU, LTD) and specialty partners (Ability Engineering, Prolaborate) each cover different products/regions, so the data model must support more than one Vendor per procurement category.

<b>Test Cases:</b>
1.	More than one Vendor record can exist and each can be linked to independent Purchases.
2.	A Purchase records exactly one Vendor (the party actually procured from for that transaction).
3.	Reports can be grouped/filtered by Vendor across all procurement.
 |
| eaxcrmmustdetectserviceexpiryandnotifytheuserwhenrenewalisneeded | EAxCRM must detect service expiry and notify the user when renewal is needed | Requirement | {992E6F5B-B58C-4342-9CDE-E2B500446150} | Notes: The system shall monitor service expiry dates and alert the user when a service needs renewal, using the expiry_month and renewal_notice_sent fields.

<b>Rationale:</b>
Services (SaaS/Training/Support) generate recurring revenue only if renewed before they lapse; without an automatic expiry check, a rep would have to remember every service's date manually, which doesn't scale past a handful of customers.

<b>Test Cases:</b>
1.	A Service with expiry_month in the current or next period appears in the renewal alert.
2.	Once renewal_notice_sent is set, the same service isn't re-alerted for that cycle.
3.	A renewed Service (new expiry_month set) drops off the alert list. -> The system shall monitor service expiry dates and alert the user when a service needs renewal, using the expiry_month and renewal_notice_sent fields.

<b>Rationale:</b>
Services (SaaS/Training/Support) generate recurring revenue only if renewed before they lapse; without an automatic expiry check, a rep would have to remember every service's date manually, which doesn't scale past a handful of customers.

<b>Test Cases:</b>
1.	A Service with expiry_month in the current or next period appears in the renewal alert.
2.	Once renewal_notice_sent is set, the same service isn't re-alerted for that cycle.
3.	A renewed Service (new expiry_month set) drops off the alert list.
 |
| eaxcrmmustdistinguishprocuredservicesresoldfromavendorfromeaxpertisesownservices | EAxCRM must distinguish procured services (resold, from a Vendor) from EAxpertise's own services | Requirement | {703B044E-64E9-4d7c-BDC4-BB81228306A6} | Notes: The system shall allow services to be marked as either procured from an external vendor or provided directly by EAxpertise.

<b>Rationale:</b>
Margin and vendor-liability differ completely between reselling someone else's service and EAxpertise's own — conflating them would corrupt procurement reporting and make it impossible to tell which services depend on a third party's continued availability.

<b>Test Cases:</b>
1.	A Service marked as procured requires a linked Vendor; a Service marked as EAxpertise's own does not.
2.	Procurement reports include only vendor-sourced Services, not EAxpertise's own.
3.	Changing a Service from procured to own clears its Vendor link. -> The system shall allow services to be marked as either procured from an external vendor or provided directly by EAxpertise.

<b>Rationale:</b>
Margin and vendor-liability differ completely between reselling someone else's service and EAxpertise's own — conflating them would corrupt procurement reporting and make it impossible to tell which services depend on a third party's continued availability.

<b>Test Cases:</b>
1.	A Service marked as procured requires a linked Vendor; a Service marked as EAxpertise's own does not.
2.	Procurement reports include only vendor-sourced Services, not EAxpertise's own.
3.	Changing a Service from procured to own clears its Vendor link.
 |
| eaxcrmmustencryptsensitivedatapasswordsatrest | EAxCRM must encrypt sensitive data (passwords) at rest | Requirement | {F6EFB60E-E9F5-4ea1-8EBD-49692050E063} | Notes: The system shall encrypt stored passwords and other sensitive credentials, such as IMAP account passwords, in the database.

<b>Rationale:</b>
IMAP credentials for three live mailboxes are stored in the database; if the SQLite file were ever copied or leaked, plaintext passwords would hand over full mailbox access, so at-rest encryption is a baseline security requirement, not optional hardening.

<b>Test Cases:</b>
1.	Inspecting the raw SQLite file does not reveal a plaintext IMAP password.
2.	The application can still decrypt and use the stored password to authenticate an IMAP connection.
3.	Rotating an IMAP account's password re-encrypts and replaces the stored value without leaving the old value recoverable. -> The system shall encrypt stored passwords and other sensitive credentials, such as IMAP account passwords, in the database.

<b>Rationale:</b>
IMAP credentials for three live mailboxes are stored in the database; if the SQLite file were ever copied or leaked, plaintext passwords would hand over full mailbox access, so at-rest encryption is a baseline security requirement, not optional hardening.

<b>Test Cases:</b>
1.	Inspecting the raw SQLite file does not reveal a plaintext IMAP password.
2.	The application can still decrypt and use the stored password to authenticate an IMAP connection.
3.	Rotating an IMAP account's password re-encrypts and replaces the stored value without leaving the old value recoverable.
 |
| eaxcrmmustenforceadraftreviewsendworkflowwithmanualapproval | EAxCRM must enforce a Draft -> Review -> Send workflow with manual approval | Requirement | {8B155267-3A23-4059-B049-269CB4A7E809} | Notes: The system shall require newsletters to go through three states: Draft (composition), Review (manual approval), and Sent (dispatch).

<b>Rationale:</b>
A newsletter goes out to every opted-in customer at once — an unreviewed send (typo, broken link, wrong article) can't be recalled, so a mandatory human review gate before Sent is the only real safeguard.

<b>Test Cases:</b>
1.	A Newsletter cannot transition directly from Draft to Sent — Review is required in between.
2.	A Newsletter in Review can be sent back to Draft for edits.
3.	Only a Newsletter in Review state can be marked Sent, via an explicit approval action. -> The system shall require newsletters to go through three states: Draft (composition), Review (manual approval), and Sent (dispatch).

<b>Rationale:</b>
A newsletter goes out to every opted-in customer at once — an unreviewed send (typo, broken link, wrong article) can't be recalled, so a mandatory human review gate before Sent is the only real safeguard.

<b>Test Cases:</b>
1.	A Newsletter cannot transition directly from Draft to Sent — Review is required in between.
2.	A Newsletter in Review can be sent back to Draft for edits.
3.	Only a Newsletter in Review state can be marked Sent, via an explicit approval action.
 |
| eaxcrmmustenforceaminimum6weekintervalbetweennewsletters | EAxCRM must enforce a minimum 6-week interval between newsletters | Requirement | {1016A374-E514-4b33-896D-88A4F0646BC5} | Notes: The system shall prevent sending newsletters more frequently than once every six weeks to maintain appropriate communication cadence.

<b>Rationale:</b>
Sending more frequently than the audience expects risks being perceived as spam and increases opt-outs — six weeks matches the project's stated cadence and gives enough time for genuinely new Sparx content to accumulate.

<b>Test Cases:</b>
1.	Attempting to send a newsletter less than 6 weeks after the last Sent newsletter is blocked.
2.	A newsletter exactly 6 weeks (or more) after the last Sent one is allowed.
3.	The interval is measured from the last *Sent* newsletter, not from Draft/Review timestamps. -> The system shall prevent sending newsletters more frequently than once every six weeks to maintain appropriate communication cadence.

<b>Rationale:</b>
Sending more frequently than the audience expects risks being perceived as spam and increases opt-outs — six weeks matches the project's stated cadence and gives enough time for genuinely new Sparx content to accumulate.

<b>Test Cases:</b>
1.	Attempting to send a newsletter less than 6 weeks after the last Sent newsletter is blocked.
2.	A newsletter exactly 6 weeks (or more) after the last Sent one is allowed.
3.	The interval is measured from the last *Sent* newsletter, not from Draft/Review timestamps.
 |
| eaxcrmmustextractandstorelicenseentitlementsfromemailattachmentspdftxt | EAxCRM must extract and store license entitlements from email attachments (PDF/TXT) | Requirement | {670E2717-2306-45cd-A3FC-F6F8CF33D0F6} | Notes: The system shall parse PDF and TXT email attachments to extract license entitlement details and store them as License records.

<b>Rationale:</b>
License PDFs/TXT attachments already contain every field a License record needs (type, dates, entitlements) — re-typing them by hand duplicates work the vendor's own document already did and introduces transcription errors.

<b>Test Cases:</b>
1.	Parsing a known-format license PDF produces a License record with correct type, start, and expiry dates.
2.	Parsing an attachment with an unrecognized format does not silently create a malformed License record.
3.	Parsed License records reference the source Attachment for traceability. -> The system shall parse PDF and TXT email attachments to extract license entitlement details and store them as License records.

<b>Rationale:</b>
License PDFs/TXT attachments already contain every field a License record needs (type, dates, entitlements) — re-typing them by hand duplicates work the vendor's own document already did and introduces transcription errors.

<b>Test Cases:</b>
1.	Parsing a known-format license PDF produces a License record with correct type, start, and expiry dates.
2.	Parsing an attachment with an unrecognized format does not silently create a malformed License record.
3.	Parsed License records reference the source Attachment for traceability.
 |
| eaxcrmmustlinkdeliveriestothecustomerthesalesinvoicetheyfulfillandtheattachmentsincluded | EAxCRM must link deliveries to the Customer, the SalesInvoice they fulfill, and the attachments included | Requirement | {55A87EA4-3D17-4a2a-8DE6-DB0F1B57DA91} | Notes: The system shall associate each delivery record with the customer it was sent to, the sales invoice it fulfills, and the license files or documents attached.

<b>Rationale:</b>
A delivery in isolation ("we sent an email") is not useful for support or auditing — it only answers something when it's tied to *who* received it, *which invoice* it fulfilled, and *what files* were actually attached.

<b>Test Cases:</b>
1.	A Delivery record references exactly one Customer and at most one SalesInvoice it fulfills.
2.	Attachments included in a Delivery are queryable from the Delivery record.
3.	Deleting a SalesInvoice does not delete Deliveries that reference it — delivery history must survive. -> The system shall associate each delivery record with the customer it was sent to, the sales invoice it fulfills, and the license files or documents attached.

<b>Rationale:</b>
A delivery in isolation ("we sent an email") is not useful for support or auditing — it only answers something when it's tied to *who* received it, *which invoice* it fulfilled, and *what files* were actually attached.

<b>Test Cases:</b>
1.	A Delivery record references exactly one Customer and at most one SalesInvoice it fulfills.
2.	Attachments included in a Delivery are queryable from the Delivery record.
3.	Deleting a SalesInvoice does not delete Deliveries that reference it — delivery history must survive.
 |
| eaxcrmmustlinkeachsalesinvoicetoitsoriginatingoffer | EAxCRM must link each SalesInvoice to its originating Offer | Requirement | {37F7E8D8-D5BD-46ec-B91A-7ED6F2E5B781} | Notes: The system shall maintain a reference from each SalesInvoice back to the Offer that generated it, ensuring auditability of the sales process.

<b>Rationale:</b>
Without a stored reference back to the Offer, there's no way to verify an invoice actually matches what was proposed and agreed — auditability of the sales process depends on this chain being unbroken.

<b>Test Cases:</b>
1.	A SalesInvoice created from an Offer stores a reference to that Offer.
2.	Given a SalesInvoice, the originating Offer's line items/amount can be looked up.
3.	Reports can trace revenue back to the originating Offer for any SalesInvoice. -> The system shall maintain a reference from each SalesInvoice back to the Offer that generated it, ensuring auditability of the sales process.

<b>Rationale:</b>
Without a stored reference back to the Offer, there's no way to verify an invoice actually matches what was proposed and agreed — auditability of the sales process depends on this chain being unbroken.

<b>Test Cases:</b>
1.	A SalesInvoice created from an Offer stores a reference to that Offer.
2.	Given a SalesInvoice, the originating Offer's line items/amount can be looked up.
3.	Reports can trace revenue back to the originating Offer for any SalesInvoice.
 |
| eaxcrmmustoperatewithoutaidependencies | EAxCRM must operate without AI dependencies | Requirement | {6A62DFB5-CBE7-4397-8640-263F0C242661} | Notes: The system shall operate entirely without AI dependencies, using traditional parsing and scraping libraries such as PyMuPDF and BeautifulSoup.

<b>Rationale:</b>
Keeps the system deployable and predictable on a QNAP NAS with limited compute and no external API dependency/cost — parsing and scraping needs (PDF, HTML) are well served by deterministic libraries, so an AI dependency would add operational risk for no functional gain today.

<b>Test Cases:</b>
1.	The application has zero calls to any external AI/LLM API at runtime.
2.	Document parsing (PDF/TXT) uses PyMuPDF only, with no ML-based extraction fallback.
3.	The app runs fully offline except for the deliberate IMAP/scraping network calls (no internet-dependent AI service). -> The system shall operate entirely without AI dependencies, using traditional parsing and scraping libraries such as PyMuPDF and BeautifulSoup.

<b>Rationale:</b>
Keeps the system deployable and predictable on a QNAP NAS with limited compute and no external API dependency/cost — parsing and scraping needs (PDF, HTML) are well served by deterministic libraries, so an AI dependency would add operational risk for no functional gain today.

<b>Test Cases:</b>
1.	The application has zero calls to any external AI/LLM API at runtime.
2.	Document parsing (PDF/TXT) uses PyMuPDF only, with no ML-based extraction fallback.
3.	The app runs fully offline except for the deliberate IMAP/scraping network calls (no internet-dependent AI service).
 |
| eaxcrmmustprovideadashboardofupcomingservicerenewals | EAxCRM must provide a dashboard of upcoming service renewals | Requirement | {9646F376-4EC0-4dfc-B050-239BA21CC691} | Notes: The system shall display a dashboard showing all services approaching their expiry date, sorted by urgency, to enable proactive renewal management.

<b>Rationale:</b>
Reactive renewal handling (waiting for a customer to complain about a lapsed license) loses revenue and damages trust — a proactive, urgency-sorted dashboard lets reps reach out before expiry instead of after.

<b>Test Cases:</b>
1.	Services within the renewal window appear on the dashboard, sorted soonest-expiry first.
2.	A renewed service (expiry_month pushed out) drops off or moves down the dashboard accordingly.
3.	The dashboard reflects auto_renew status so reps don't chase renewals that are already handled automatically. -> The system shall display a dashboard showing all services approaching their expiry date, sorted by urgency, to enable proactive renewal management.

<b>Rationale:</b>
Reactive renewal handling (waiting for a customer to complain about a lapsed license) loses revenue and damages trust — a proactive, urgency-sorted dashboard lets reps reach out before expiry instead of after.

<b>Test Cases:</b>
1.	Services within the renewal window appear on the dashboard, sorted soonest-expiry first.
2.	A renewed service (expiry_month pushed out) drops off or moves down the dashboard accordingly.
3.	The dashboard reflects auto_renew status so reps don't chase renewals that are already handled automatically.
 |
| eaxcrmmustprovideprocurementreportsgroupedbyvendor | EAxCRM must provide procurement reports grouped by Vendor | Requirement | {D938A51D-6BF2-4882-9B88-035B63007259} | Notes: The system shall generate reports summarizing procurements per vendor, including quote amounts, invoice totals, and payment status.

<b>Rationale:</b>
Spend and payment-status visibility per vendor is needed for cash-flow planning and vendor-relationship decisions (e.g. is Sparx Systems LTD or EU cheaper for a given license type) — without grouping by vendor this comparison requires manual spreadsheet work.

<b>Test Cases:</b>
1.	A report for a given Vendor totals quote amounts and invoice totals correctly across all its Purchases.
2.	Payment status (paid/pending) is visible per procurement line in the report.
3.	Switching the report's vendor filter changes only the displayed rows, not the underlying data. -> The system shall generate reports summarizing procurements per vendor, including quote amounts, invoice totals, and payment status.

<b>Rationale:</b>
Spend and payment-status visibility per vendor is needed for cash-flow planning and vendor-relationship decisions (e.g. is Sparx Systems LTD or EU cheaper for a given license type) — without grouping by vendor this comparison requires manual spreadsheet work.

<b>Test Cases:</b>
1.	A report for a given Vendor totals quote amounts and invoice totals correctly across all its Purchases.
2.	Payment status (paid/pending) is visible per procurement line in the report.
3.	Switching the report's vendor filter changes only the displayed rows, not the underlying data.
 |
| eaxcrmmustrunonwindowsfordevelopmentanddockerqnapnasforproduction | EAxCRM must run on Windows for development and Docker/QNAP NAS for production | Requirement | {82C5CC76-459B-49e5-AD85-A406DA3E2E53} | Notes: The system shall support native Windows development and Docker-based deployment on a QNAP NAS for production use.

<b>Rationale:</b>
The developer's daily machine is Windows, but the always-on production host is a QNAP NAS — the app must work identically in both environments without code changes, only deployment configuration differing.

<b>Test Cases:</b>
1.	The app runs correctly via `runserver` on native Windows during development.
2.	The same codebase runs unmodified inside a Docker container on QNAP Container Station.
3.	Database file paths and settings are environment-configurable, not hardcoded to a Windows path. -> The system shall support native Windows development and Docker-based deployment on a QNAP NAS for production use.

<b>Rationale:</b>
The developer's daily machine is Windows, but the always-on production host is a QNAP NAS — the app must work identically in both environments without code changes, only deployment configuration differing.

<b>Test Cases:</b>
1.	The app runs correctly via `runserver` on native Windows during development.
2.	The same codebase runs unmodified inside a Docker container on QNAP Container Station.
3.	Database file paths and settings are environment-configurable, not hardcoded to a Windows path.
 |
| eaxcrmmustshowauxthatshowsthecurrentstateofprocurement | EAxCRM must show a UX that shows the current state of Procurement | Requirement | {2FC71345-5D8C-432b-B123-CC9F89E1B818} | Notes: The system shall display the current procurement state per vendor including which quotes have been received and which invoices are paid or pending.

<b>Rationale:</b>
"What's still outstanding with our vendors" is a recurring operational question (which quotes are we waiting on, which invoices are unpaid) that shouldn't require opening individual Purchase records one at a time.

<b>Test Cases:</b>
1.	The view shows, per Vendor, which quotes have been received and which are still outstanding.
2.	Invoice payment status (paid/pending) is visible alongside each procurement line.
3.	The view updates immediately when a new Quote or ProcurementInvoice is recorded. -> The system shall display the current procurement state per vendor including which quotes have been received and which invoices are paid or pending.

<b>Rationale:</b>
"What's still outstanding with our vendors" is a recurring operational question (which quotes are we waiting on, which invoices are unpaid) that shouldn't require opening individual Purchase records one at a time.

<b>Test Cases:</b>
1.	The view shows, per Vendor, which quotes have been received and which are still outstanding.
2.	Invoice payment status (paid/pending) is visible alongside each procurement line.
3.	The view updates immediately when a new Quote or ProcurementInvoice is recorded.
 |
| eaxcrmmuststorecommunicationhistorypercustomerretrievedfrommultipleimapaccountshaneaxpertisenlsaleseaxpertisenlinfoeaxpertisenl | EAxCRM must store communication history per customer, retrieved from multiple IMAP accounts (han@eaxpertise.nl, sales@eaxpertise.nl, info@eaxpertise.nl) | Requirement | {7DEA2FF6-9EAC-47da-BE8B-9414FAFBF5DD} | Notes: The system shall fetch and store emails from three IMAP accounts and associate them with the relevant customer for a complete communication history.

<b>Rationale:</b>
Support and sales context lives in email threads across three different mailboxes (han@, sales@, info@) — without consolidating them per customer, a rep has to manually search three inboxes to reconstruct history with any given customer.

<b>Test Cases:</b>
1.	Emails fetched from all three configured IMAP accounts are associated with the correct Customer based on sender/recipient address matching.
2.	An email that doesn't match any known Customer is not silently dropped — it's flagged/left unassigned for manual linking.
3.	A customer's communication history view shows emails from all three mailboxes in one chronological list. -> The system shall fetch and store emails from three IMAP accounts and associate them with the relevant customer for a complete communication history.

<b>Rationale:</b>
Support and sales context lives in email threads across three different mailboxes (han@, sales@, info@) — without consolidating them per customer, a rep has to manually search three inboxes to reconstruct history with any given customer.

<b>Test Cases:</b>
1.	Emails fetched from all three configured IMAP accounts are associated with the correct Customer based on sender/recipient address matching.
2.	An email that doesn't match any known Customer is not silently dropped — it's flagged/left unassigned for manual linking.
3.	A customer's communication history view shows emails from all three mailboxes in one chronological list.
 |
| eaxcrmmuststoredocumentsquotesinvoicesdeliverieslinkedtocustomers | EAxCRM must store documents (quotes, invoices, deliveries) linked to customers | Requirement | {3111DD70-D016-4cad-B7CC-D8FA9D63FAF0} | Notes: The system shall store customer-facing documents such as Sparx Systems quotes, incoming invoices, and delivery notes, linked to the relevant customer record.

<b>Rationale:</b>
Quotes, invoices, and delivery notes are the paper trail of the customer relationship — keeping them attached to the Customer record, rather than scattered across email/OneDrive, means a rep can answer "what have we sent/billed this customer" in one place.

<b>Test Cases:</b>
1.	A Quote, ProcurementInvoice, and Delivery can each be linked to a specific Customer.
2.	All documents for a Customer are retrievable from that Customer's record.
3.	Documents remain linked correctly if the same Customer has multiple concurrent Purchases. -> The system shall store customer-facing documents such as Sparx Systems quotes, incoming invoices, and delivery notes, linked to the relevant customer record.

<b>Rationale:</b>
Quotes, invoices, and delivery notes are the paper trail of the customer relationship — keeping them attached to the Customer record, rather than scattered across email/OneDrive, means a rep can answer "what have we sent/billed this customer" in one place.

<b>Test Cases:</b>
1.	A Quote, ProcurementInvoice, and Delivery can each be linked to a specific Customer.
2.	All documents for a Customer are retrievable from that Customer's record.
3.	Documents remain linked correctly if the same Customer has multiple concurrent Purchases.
 |
| eaxcrmmuststorevendorbankdetailsibanbicswiftpaymentcurrency | EAxCRM must store vendor bank details (IBAN, BIC/SWIFT, payment currency) | Requirement | {C7244ED6-A70C-43a2-A6C3-4A5D8AFD6A95} | Notes: The system shall record vendor bank account information including IBAN, BIC/SWIFT code, and default payment currency for invoice processing.

<b>Rationale:</b>
Paying an incoming invoice requires knowing where to send the money and in what currency — storing IBAN/BIC/currency once per Vendor avoids re-sourcing payment details, and risking a wrong-account payment, every time an invoice comes in.

<b>Test Cases:</b>
1.	A Vendor record stores IBAN, BIC/SWIFT, and a default payment currency.
2.	Vendor bank details are visible when processing a ProcurementInvoice for that vendor.
3.	Two Vendors can have different default payment currencies without conflict (e.g. one EUR, one USD). -> The system shall record vendor bank account information including IBAN, BIC/SWIFT code, and default payment currency for invoice processing.

<b>Rationale:</b>
Paying an incoming invoice requires knowing where to send the money and in what currency — storing IBAN/BIC/currency once per Vendor avoids re-sourcing payment details, and risking a wrong-account payment, every time an invoice comes in.

<b>Test Cases:</b>
1.	A Vendor record stores IBAN, BIC/SWIFT, and a default payment currency.
2.	Vendor bank details are visible when processing a ProcurementInvoice for that vendor.
3.	Two Vendors can have different default payment currencies without conflict (e.g. one EUR, one USD).
 |
| eaxcrmmustsupportmulticurrencyinvoiceseurusdfromsparxsystems | EAxCRM must support multi-currency invoices (EUR, USD) from Sparx Systems | Requirement | {9615BF5D-D930-4353-858D-0F75F8DA37C5} | Notes: The system shall handle incoming invoices in both EUR and USD from Sparx Systems and its subsidiaries.

<b>Rationale:</b>
Sparx Systems' entities invoice in different currencies depending on region/subsidiary — a single-currency assumption would make it impossible to record invoices accurately or reconcile actual spend.

<b>Test Cases:</b>
1.	A ProcurementInvoice can be recorded with currency = EUR.
2.	A ProcurementInvoice can be recorded with currency = USD.
3.	Reports correctly separate or convert totals across the two currencies rather than silently summing mismatched currencies together. -> The system shall handle incoming invoices in both EUR and USD from Sparx Systems and its subsidiaries.

<b>Rationale:</b>
Sparx Systems' entities invoice in different currencies depending on region/subsidiary — a single-currency assumption would make it impossible to record invoices accurately or reconcile actual spend.

<b>Test Cases:</b>
1.	A ProcurementInvoice can be recorded with currency = EUR.
2.	A ProcurementInvoice can be recorded with currency = USD.
3.	Reports correctly separate or convert totals across the two currencies rather than silently summing mismatched currencies together.
 |
| eaxcrmmusttracklicenserenewalslinkedtotheoriginalpurchase | EAxCRM must track license renewals linked to the original purchase | Requirement | {B1887963-752B-404c-A21E-19BBF6A32F80} | Notes: The system shall support creating renewal licenses that reference the original purchase record, enabling tracking of the full license lifecycle.

<b>Rationale:</b>
A renewal is conceptually a continuation of an earlier license, not a brand-new unrelated purchase — keeping the link lets a rep trace a customer's full license lifecycle instead of seeing disconnected fragments.

<b>Test Cases:</b>
1.	A renewal License record references the original Purchase it renews.
2.	Querying a customer's license lifecycle shows the original purchase and all subsequent renewals in order.
3.	A renewal License does not require re-entering data already present on the original Purchase. -> The system shall support creating renewal licenses that reference the original purchase record, enabling tracking of the full license lifecycle.

<b>Rationale:</b>
A renewal is conceptually a continuation of an earlier license, not a brand-new unrelated purchase — keeping the link lets a rep trace a customer's full license lifecycle instead of seeing disconnected fragments.

<b>Test Cases:</b>
1.	A renewal License record references the original Purchase it renews.
2.	Querying a customer's license lifecycle shows the original purchase and all subsequent renewals in order.
3.	A renewal License does not require re-entering data already present on the original Purchase.
 |
| eaxcrmmusttrackpercontactdeliverystatussentopenedbounced | EAxCRM must track per-contact delivery status (sent, opened, bounced) | Requirement | {218F552E-5931-417c-A02B-DAE8B9F69C78} | Notes: The system shall record whether each newsletter contact received, opened, or bounced the newsletter to measure engagement.

<b>Rationale:</b>
Newsletter engagement is the only real signal of whether the newsletter is reaching and working for a given contact — without it, EAxpertise can't tell a stale/dead email address from an active one.

<b>Test Cases:</b>
1.	Sending a Newsletter creates a NewsletterContact record per recipient with an initial "sent" status.
2.	Opening the newsletter (tracked open) updates the corresponding NewsletterContact's opened_date.
3.	A bounced delivery marks the NewsletterContact as bounced rather than sent. -> The system shall record whether each newsletter contact received, opened, or bounced the newsletter to measure engagement.

<b>Rationale:</b>
Newsletter engagement is the only real signal of whether the newsletter is reaching and working for a given contact — without it, EAxpertise can't tell a stale/dead email address from an active one.

<b>Test Cases:</b>
1.	Sending a Newsletter creates a NewsletterContact record per recipient with an initial "sent" status.
2.	Opening the newsletter (tracked open) updates the corresponding NewsletterContact's opened_date.
3.	A bounced delivery marks the NewsletterContact as bounced rather than sent.
 |
| eaxcrmmustusethedjangoadmininterfaceasitsprimaryui | EAxCRM must use the Django Admin interface as its primary UI | Requirement | {FA4583F4-87B2-4685-9904-EB9A14B63BF3} | Notes: The system shall use Django's built-in admin interface as the primary user interface for all CRM operations.

<b>Rationale:</b>
Building a custom UI is unnecessary effort for an internal single-tenant tool with a handful of users — Django Admin already provides CRUD, search, and filtering out of the box, keeping the project scoped to Django + SQLite with no separate frontend to maintain.

<b>Test Cases:</b>
1.	Every core entity (Customer, Contact, License, Offer, etc.) is manageable (create/edit/delete) through Django Admin.
2.	List views support the filtering/search needed for day-to-day rep use (e.g. filter contacts by role).
3.	No entity requires a custom-built page outside Django Admin to be usable. -> The system shall use Django's built-in admin interface as the primary user interface for all CRM operations.

<b>Rationale:</b>
Building a custom UI is unnecessary effort for an internal single-tenant tool with a handful of users — Django Admin already provides CRUD, search, and filtering out of the box, keeping the project scoped to Django + SQLite with no separate frontend to maintain.

<b>Test Cases:</b>
1.	Every core entity (Customer, Contact, License, Offer, etc.) is manageable (create/edit/delete) through Django Admin.
2.	List views support the filtering/search needed for day-to-day rep use (e.g. filter contacts by role).
3.	No entity requires a custom-built page outside Django Admin to be usable.
 |
| procurementcanbedoneviaabilityengineering | Procurement can be done via Ability Engineering | Requirement | {675A33C1-835A-4fda-8B97-50BA072EAFA1} | Notes: Ability Engineering is a reseller of Sparx Systems licenses, providing an alternative procurement channel.

<b>Rationale:</b>
Recording Ability Engineering as its own Vendor lets purchases through this specific reseller be tracked and reported on independently of Sparx Systems' own channels.

<b>Test Cases:</b>
1.	A Vendor record for Ability Engineering can be created and linked to Purchases.
2.	Procurement reports can filter/group specifically to Ability Engineering.
3.	Ability Engineering coexists with the other Vendor records without ID or name collisions. -> Ability Engineering is a reseller of Sparx Systems licenses, providing an alternative procurement channel.

<b>Rationale:</b>
Recording Ability Engineering as its own Vendor lets purchases through this specific reseller be tracked and reported on independently of Sparx Systems' own channels.

<b>Test Cases:</b>
1.	A Vendor record for Ability Engineering can be created and linked to Purchases.
2.	Procurement reports can filter/group specifically to Ability Engineering.
3.	Ability Engineering coexists with the other Vendor records without ID or name collisions.
 |
| procurementcanbedoneviaprolaborate | Procurement can be done via Prolaborate | Requirement | {492044AB-6D15-4455-B6D0-7C8F950480BC} | Notes: Prolaborate sells hosting services: hosting platform of Pro Cloud and EA SaaS.

<b>Rationale:</b>
Prolaborate is a distinct procurement channel specifically for hosting rather than licenses — tracking it separately from license vendors keeps hosting spend visible on its own line rather than blended into general license procurement.

<b>Test Cases:</b>
1.	A Vendor record for Prolaborate can be created and linked to Purchases for hosting services.
2.	Procurement reports can filter/group specifically to Prolaborate.
3.	Prolaborate purchases are distinguishable from Sparx Systems license purchases in reporting. -> Prolaborate sells hosting services: hosting platform of Pro Cloud and EA SaaS.

<b>Rationale:</b>
Prolaborate is a distinct procurement channel specifically for hosting rather than licenses — tracking it separately from license vendors keeps hosting spend visible on its own line rather than blended into general license procurement.

<b>Test Cases:</b>
1.	A Vendor record for Prolaborate can be created and linked to Purchases for hosting services.
2.	Procurement reports can filter/group specifically to Prolaborate.
3.	Prolaborate purchases are distinguishable from Sparx Systems license purchases in reporting.
 |
| procurementcanbedoneviasparxsystemseu | Procurement can be done via Sparx Systems EU | Requirement | {CEBF5E06-3BF4-4909-96A8-D91004A36647} | Notes: Sparx Systems EU is the European reseller of Sparx Systems licenses serving the EU market.

<b>Rationale:</b>
EU-region customers are typically procured through Sparx Systems EU rather than the Australian HQ — tracking it as its own Vendor keeps regional procurement (and any EU-specific pricing/currency) separate from LTD's.

<b>Test Cases:</b>
1.	A Vendor record for Sparx Systems EU can be created and linked to Purchases.
2.	Procurement reports can filter/group specifically to Sparx Systems EU.
3.	Sparx Systems EU and Sparx Systems LTD coexist as distinct Vendor records without being conflated. -> Sparx Systems EU is the European reseller of Sparx Systems licenses serving the EU market.

<b>Rationale:</b>
EU-region customers are typically procured through Sparx Systems EU rather than the Australian HQ — tracking it as its own Vendor keeps regional procurement (and any EU-specific pricing/currency) separate from LTD's.

<b>Test Cases:</b>
1.	A Vendor record for Sparx Systems EU can be created and linked to Purchases.
2.	Procurement reports can filter/group specifically to Sparx Systems EU.
3.	Sparx Systems EU and Sparx Systems LTD coexist as distinct Vendor records without being conflated.
 |
| procurementcanbedoneviasparxsystemsltd | Procurement can be done via Sparx Systems LTD | Requirement | {AE2C78B0-A8C3-4aef-B5AE-3C0AB921189B} | Notes: Sparx Systems LTD is the Australian headquarters and primary reseller of Sparx Systems licenses.

<b>Rationale:</b>
As the Australian headquarters and primary reseller, most core Sparx EA license procurement flows through this Vendor — it needs its own record so it isn't conflated with regional resellers or specialty partners covered by the other PRO-5.x vendors.

<b>Test Cases:</b>
1.	A Vendor record for Sparx Systems LTD can be created and linked to Purchases.
2.	Procurement reports can filter/group specifically to Sparx Systems LTD.
3.	The majority of License-related Purchases can be traced back to this Vendor. -> Sparx Systems LTD is the Australian headquarters and primary reseller of Sparx Systems licenses.

<b>Rationale:</b>
As the Australian headquarters and primary reseller, most core Sparx EA license procurement flows through this Vendor — it needs its own record so it isn't conflated with regional resellers or specialty partners covered by the other PRO-5.x vendors.

<b>Test Cases:</b>
1.	A Vendor record for Sparx Systems LTD can be created and linked to Purchases.
2.	Procurement reports can filter/group specifically to Sparx Systems LTD.
3.	The majority of License-related Purchases can be traced back to this Vendor.
 |
| procurementmustbetrackablepervendorwithlinkedquoteandprocurementinvoicepdfs | Procurement must be trackable per Vendor with linked Quote and ProcurementInvoice PDFs | Requirement | {5DA68B35-5206-46cb-B4D1-A38D8D655197} | Notes: The system shall allow each procurement to be tracked per vendor, with digital copies of the original quote and the incoming invoice stored as attachments.

<b>Rationale:</b>
A procurement record without its supporting documents can't be independently verified later — attaching the PDFs directly to the Purchase/Vendor chain means the paper trail survives even if the original email is deleted.

<b>Test Cases:</b>
1.	A Purchase stores a reference to both the original Quote PDF and the incoming ProcurementInvoice PDF.
2.	Procurements can be filtered/grouped by Vendor and show their attached documents.
3.	A Purchase missing either PDF is visibly flagged as incomplete rather than silently accepted. -> The system shall allow each procurement to be tracked per vendor, with digital copies of the original quote and the incoming invoice stored as attachments.

<b>Rationale:</b>
A procurement record without its supporting documents can't be independently verified later — attaching the PDFs directly to the Purchase/Vendor chain means the paper trail survives even if the original email is deleted.

<b>Test Cases:</b>
1.	A Purchase stores a reference to both the original Quote PDF and the incoming ProcurementInvoice PDF.
2.	Procurements can be filtered/grouped by Vendor and show their attached documents.
3.	A Purchase missing either PDF is visibly flagged as incomplete rather than silently accepted.
 |
| createaccountscreencreatescustomerandcontactsatomically | CreateAccountScreen: creates Customer and Contacts atomically | Requirement | {D13E63E8-1DA9-4f10-BF1C-8AFC333666C7} | Notes: The Create Customer Account screen shall create one Customer record and one or more Contact records in a single atomic save operation. A Customer must never be persisted without at least one associated Contact, since the account-creation process treats the organization and its initial contact(s) as one unit of work.

<b>Rationale:</b>
Matches the existing BPMN process (EAxCRM-CustomerAccountProcess.md), where account creation is modeled as one atomic activity. Prevents orphan Customer records with no way to reach anyone at the organization.

<b>Test Cases:</b>
1.	Save with 1 Customer + 1 Contact succeeds and both rows exist.
2.	Save attempt with Customer fields filled but zero Contacts fails validation.
3.	A mid-save failure (e.g. DB error on second Contact) rolls back the Customer too — no partial commit. -> The Create Customer Account screen shall create one Customer record and one or more Contact records in a single atomic save operation. A Customer must never be persisted without at least one associated Contact, since the account-creation process treats the organization and its initial contact(s) as one unit of work.

<b>Rationale:</b>
Matches the existing BPMN process (EAxCRM-CustomerAccountProcess.md), where account creation is modeled as one atomic activity. Prevents orphan Customer records with no way to reach anyone at the organization.

<b>Test Cases:</b>
1.	Save with 1 Customer + 1 Contact succeeds and both rows exist.
2.	Save attempt with Customer fields filled but zero Contacts fails validation.
3.	A mid-save failure (e.g. DB error on second Contact) rolls back the Customer too — no partial commit.
 |
| createaccountscreenstructuredstreetaddressorpobox | CreateAccountScreen: structured street address or PO Box | Requirement | {D356ED58-643D-45e6-BC31-CFA401E6C7D1} | Notes: The system shall record a Customer's address as either a structured street address (Street Name, House Number, Postal Code, City, Country) or an unstructured PO Box string, selected via a mode toggle on the create screen. Address is mandatory — the rep must actively locate it if not present in the source email.

<b>Rationale:</b>
Real-world postal addresses aren't always street-based; forcing one shape either loses PO Box customers or forces reps to cram a PO Box into a street-shaped field.

<b>Test Cases:</b>
1.	Street mode requires all five fields before save.
2.	PO Box mode requires only the PO Box text field; street fields stay null.
3.	Switching modes clears/ignores the other mode's fields rather than submitting both. -> The system shall record a Customer's address as either a structured street address (Street Name, House Number, Postal Code, City, Country) or an unstructured PO Box string, selected via a mode toggle on the create screen. Address is mandatory — the rep must actively locate it if not present in the source email.

<b>Rationale:</b>
Real-world postal addresses aren't always street-based; forcing one shape either loses PO Box customers or forces reps to cram a PO Box into a street-shaped field.

<b>Test Cases:</b>
1.	Street mode requires all five fields before save.
2.	PO Box mode requires only the PO Box text field; street fields stay null.
3.	Switching modes clears/ignores the other mode's fields rather than submitting both.
 |
| primarycontactruleatleastonecontactmustalwaysbeprimary | Primary Contact Rule: at least one Contact must always be Primary | Requirement | {5E968ECB-4896-45fa-9FAE-4518F9F92ECF} | Notes: Regardless of how many Contacts are entered on account creation, exactly one must carry the role Primary. This holds even when only one Contact is entered — in that case the first (and only) Contact row defaults its role to Primary automatically rather than being left blank.

<b>Rationale:</b>
Ensures every account always has one unambiguous point of contact, and gives a clear successor path when combined with the Secondary role (CRM-10).

<b>Test Cases:</b>
1.	Single-contact save with role left untouched saves with role = Primary.
2.	Two-contact save where neither is marked Primary is rejected.
3.	Two-contact save with exactly one Primary succeeds. -> Regardless of how many Contacts are entered on account creation, exactly one must carry the role Primary. This holds even when only one Contact is entered — in that case the first (and only) Contact row defaults its role to Primary automatically rather than being left blank.

<b>Rationale:</b>
Ensures every account always has one unambiguous point of contact, and gives a clear successor path when combined with the Secondary role (CRM-10).

<b>Test Cases:</b>
1.	Single-contact save with role left untouched saves with role = Primary.
2.	Two-contact save where neither is marked Primary is rejected.
3.	Two-contact save with exactly one Primary succeeds.
 |
| contactrolerulerequiredonceasecondcontactexists | Contact Role Rule: required once a second Contact exists | Requirement | {D97412A1-AF30-45ac-AE2D-E6A4A423CF65} | Notes: Role is optional only when exactly one Contact exists on the form. As soon as a second Contact row is added, role becomes a required field for every Contact on the form, including ones already entered.

<b>Rationale:</b>
Prevents accounts with multiple unnamed-function contacts, where reps can no longer tell who does what.

<b>Test Cases:</b>
1.	One contact, role left at its default, saves fine (subject to CRM-8).
2.	Add a second contact, leave either role blank — save is rejected.
3.	Fill both roles — save succeeds. -> Role is optional only when exactly one Contact exists on the form. As soon as a second Contact row is added, role becomes a required field for every Contact on the form, including ones already entered.

<b>Rationale:</b>
Prevents accounts with multiple unnamed-function contacts, where reps can no longer tell who does what.

<b>Test Cases:</b>
1.	One contact, role left at its default, saves fine (subject to CRM-8).
2.	Add a second contact, leave either role blank — save is rejected.
3.	Fill both roles — save succeeds.
 |
| contactrolerulesecondaryroleadded | Contact Role Rule: Secondary role added | Requirement | {D37E1D4E-051B-455c-8B98-23F98FC4A551} | Notes: The Contact role choices shall include Secondary, alongside Primary/Purchase/Sales/License Holder. Secondary denotes a colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties, and is the expected successor role if the Primary contact leaves the organization.

<b>Rationale:</b>
Organizations commonly designate a backup point of contact; without this role it would be miscategorized as Purchase/Sales or left blank, losing the succession signal.

<b>Test Cases:</b>
1.	Role dropdown lists Secondary as a selectable option.
2.	A Contact saved with role=Secondary persists and displays correctly.
3.	Filtering/reporting by role can isolate Secondary contacts. -> The Contact role choices shall include Secondary, alongside Primary/Purchase/Sales/License Holder. Secondary denotes a colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties, and is the expected successor role if the Primary contact leaves the organization.

<b>Rationale:</b>
Organizations commonly designate a backup point of contact; without this role it would be miscategorized as Purchase/Sales or left blank, losing the succession signal.

<b>Test Cases:</b>
1.	Role dropdown lists Secondary as a selectable option.
2.	A Contact saved with role=Secondary persists and displays correctly.
3.	Filtering/reporting by role can isolate Secondary contacts.
 |
| newsletterconsentruleoptindefaultstofalse | Newsletter Consent Rule: opt-in defaults to false | Requirement | {EAAD0687-E661-4943-93EB-86376B3FA8EF} | Notes: Contact.opt_in shall default to False when created via Create Customer Account, and shall only be set True if the rep has explicit evidence of consent in the source email. The same field must remain independently editable later via the existing Suggest Newsletter Opt-in screen.

<b>Rationale:</b>
Marketing consent is a legal/compliance flag and must never be inferred just because a customer initiated contact; giving reps two deliberate checkpoints (creation-time and a later prompt) increases the chance of capturing real consent without ever defaulting to true.

<b>Test Cases:</b>
1.	New Contact via create screen has opt_in=False when the checkbox is left untouched.
2.	Checking the box at creation sets opt_in=True and stamps opt_in_date.
3.	opt_in can later be toggled from the Suggest Newsletter Opt-in screen independent of the create screen's state. -> Contact.opt_in shall default to False when created via Create Customer Account, and shall only be set True if the rep has explicit evidence of consent in the source email. The same field must remain independently editable later via the existing Suggest Newsletter Opt-in screen.

<b>Rationale:</b>
Marketing consent is a legal/compliance flag and must never be inferred just because a customer initiated contact; giving reps two deliberate checkpoints (creation-time and a later prompt) increases the chance of capturing real consent without ever defaulting to true.

<b>Test Cases:</b>
1.	New Contact via create screen has opt_in=False when the checkbox is left untouched.
2.	Checking the box at creation sets opt_in=True and stamps opt_in_date.
3.	opt_in can later be toggled from the Suggest Newsletter Opt-in screen independent of the create screen's state.
 |
| createaccountscreennotesandphonecapturableatcreation | CreateAccountScreen: notes and phone capturable at creation | Requirement | {0EF04071-8682-4579-A08F-8A4F75EE8713} | Notes: The create screen shall include optional fields for Customer.notes (free text) and Contact.phone, since both are sometimes directly available in the source email (footer/signature) and cheaper to capture immediately than via a later edit step.

<b>Rationale:</b>
Reduces follow-up data-entry work when the information is already visible to the rep; both remain optional since they're often absent from a first email.

<b>Test Cases:</b>
1.	Save succeeds with both fields blank.
2.	Save succeeds with notes and/or phone filled in.
3.	Values persist correctly on the respective Customer/Contact records. -> The create screen shall include optional fields for Customer.notes (free text) and Contact.phone, since both are sometimes directly available in the source email (footer/signature) and cheaper to capture immediately than via a later edit step.

<b>Rationale:</b>
Reduces follow-up data-entry work when the information is already visible to the rep; both remain optional since they're often absent from a first email.

<b>Test Cases:</b>
1.	Save succeeds with both fields blank.
2.	Save succeeds with notes and/or phone filled in.
3.	Values persist correctly on the respective Customer/Contact records.
 |

## 2026-07-07 14:07:14 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| eaxcrmmustsupporttheprocurementprocess | EAxCRM must support the procurement process | Requirement | {119DE89A-BFF5-44ab-AC67-6FC9DB0F8C10} | Notes: The system shall manage the end-to-end procurement workflow from receiving a supplier quote, creating a purchase record, and recording the incoming invoice. -> The system shall manage the end-to-end procurement workflow from receiving a supplier quote, creating a purchase record, and recording the incoming invoice.



 |
| eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder | EAxCRM must manage Customer organizations and their Contacts with specific roles (Primary, Purchase, Sales, License Holder) | Requirement | {C8A09A87-5B2B-4d72-896F-77C079F7C2DA} | Notes: The system shall store customer organizations and their associated contacts, each with one or more roles that determine their function in the CRM workflow. -> The system shall store customer organizations and their associated contacts, each with one or more roles that determine their function in the CRM workflow.



 |
| eaxcrmmustusesqliteasitsdatabasebackend | EAxCRM must use SQLite as its database backend | Requirement | {30EA2FCA-BEA7-4fd7-A7E8-F5ECD78B8ADF} | Notes: The system shall use a file-based SQLite database suitable for deployment on a QNAP NAS without requiring a separate database server. -> The system shall use a file-based SQLite database suitable for deployment on a QNAP NAS without requiring a separate database server.



 |
| eaxcrmmustsupportcomposingnewslettersfromscrapedarticlesonsparxsystemscomandsparxsystemseu | EAxCRM must support composing newsletters from scraped articles on SparxSystems.com and sparxsystems.eu | Requirement | {153BD677-35A4-4252-BEC1-20B170577F99} | Notes: The system shall scrape news articles from SparxSystems.com and sparxsystems.eu and allow composing an EAxNewsletter from selected article summaries and links. -> The system shall scrape news articles from SparxSystems.com and sparxsystems.eu and allow composing an EAxNewsletter from selected article summaries and links.



 |
| eaxcrmmustsupportthesalesprocess | EAXCRM must support the sales process | Requirement | {0475B655-DAC3-4672-A10B-4B1C42DC4E44} | Notes: The system shall manage the sales workflow from creating an Offer to generating a SalesInvoice for the customer. -> The system shall manage the sales workflow from creating an Offer to generating a SalesInvoice for the customer.



 |
| eaxcrmmustprovideaviewofallcustomerlicenseentitlementswithstartexpirydates | EAxCRM must provide a view of all customer license entitlements with start/expiry dates | Requirement | {695AC932-66C2-43d0-B242-A9BE87C30800} | Notes: The system shall display a consolidated view of each customer's active and expired license entitlements including their start and end dates. -> The system shall display a consolidated view of each customer's active and expired license entitlements including their start and end dates.



 |
| eaxcrmmustrecorddeliveryemailscontaininglicensefilesandorserviceagreements | EAxCRM must record delivery emails containing license files and/or service agreements | Requirement | {2553EA37-D4C2-4c1c-BA2B-65ADD9C06F80} | Notes: The system shall store delivery emails sent to customers that contain license registration files and/or service agreement documents. -> The system shall store delivery emails sent to customers that contain license registration files and/or service agreement documents.



 |
| eaxcrmmustsupportdraganddropdocumentingestionthatautomaticallyparsesandfillsentities | EAxCRM must support drag-and-drop document ingestion that automatically parses and fills entities | Requirement | {7248B806-6768-40d0-87E7-FEDE7509892A} | Notes: The system shall allow a user to drag and drop a document (PDF, TXT, email file) onto the UI, which then automatically parses the content and populates the correct entities (License, LicenseLineItem, Service, Quote, ProcurementInvoice, Communication, Contact) as accurately as possible, reducing manual data entry. -> The system shall allow a user to drag and drop a document (PDF, TXT, email file) onto the UI, which then automatically parses the content and populates the correct entities (License, LicenseLineItem, Service, Quote, ProcurementInvoice, Communication, Contact) as accurately as possible, reducing manual data entry.



 |
| procurementcanbedoneviamultipleparties | Procurement can be done via multiple parties | Requirement | {506DEB0C-8BE3-4a76-B52E-E00F3DBB672E} | Notes: There are several suppliers to EAxpertise. -> There are several suppliers to EAxpertise.



 |
| eaxcrmmustdetectserviceexpiryandnotifytheuserwhenrenewalisneeded | EAxCRM must detect service expiry and notify the user when renewal is needed | Requirement | {992E6F5B-B58C-4342-9CDE-E2B500446150} | Notes: The system shall monitor service expiry dates and alert the user when a service needs renewal, using the expiry_month and renewal_notice_sent fields. -> The system shall monitor service expiry dates and alert the user when a service needs renewal, using the expiry_month and renewal_notice_sent fields.



 |
| eaxcrmmustdistinguishprocuredservicesresoldfromavendorfromeaxpertisesownservices | EAxCRM must distinguish procured services (resold, from a Vendor) from EAxpertise's own services | Requirement | {703B044E-64E9-4d7c-BDC4-BB81228306A6} | Notes: The system shall allow services to be marked as either procured from an external vendor or provided directly by EAxpertise. -> The system shall allow services to be marked as either procured from an external vendor or provided directly by EAxpertise.



 |
| eaxcrmmustencryptsensitivedatapasswordsatrest | EAxCRM must encrypt sensitive data (passwords) at rest | Requirement | {F6EFB60E-E9F5-4ea1-8EBD-49692050E063} | Notes: The system shall encrypt stored passwords and other sensitive credentials, such as IMAP account passwords, in the database. -> The system shall encrypt stored passwords and other sensitive credentials, such as IMAP account passwords, in the database.



 |
| eaxcrmmustenforceadraftreviewsendworkflowwithmanualapproval | EAxCRM must enforce a Draft -> Review -> Send workflow with manual approval | Requirement | {8B155267-3A23-4059-B049-269CB4A7E809} | Notes: The system shall require newsletters to go through three states: Draft (composition), Review (manual approval), and Sent (dispatch). -> The system shall require newsletters to go through three states: Draft (composition), Review (manual approval), and Sent (dispatch).



 |
| eaxcrmmustenforceaminimum6weekintervalbetweennewsletters | EAxCRM must enforce a minimum 6-week interval between newsletters | Requirement | {1016A374-E514-4b33-896D-88A4F0646BC5} | Notes: The system shall prevent sending newsletters more frequently than once every six weeks to maintain appropriate communication cadence. -> The system shall prevent sending newsletters more frequently than once every six weeks to maintain appropriate communication cadence.



 |
| eaxcrmmustextractandstorelicenseentitlementsfromemailattachmentspdftxt | EAxCRM must extract and store license entitlements from email attachments (PDF/TXT) | Requirement | {670E2717-2306-45cd-A3FC-F6F8CF33D0F6} | Notes: The system shall parse PDF and TXT email attachments to extract license entitlement details and store them as License records. -> The system shall parse PDF and TXT email attachments to extract license entitlement details and store them as License records.



 |
| eaxcrmmustlinkdeliveriestothecustomerthesalesinvoicetheyfulfillandtheattachmentsincluded | EAxCRM must link deliveries to the Customer, the SalesInvoice they fulfill, and the attachments included | Requirement | {55A87EA4-3D17-4a2a-8DE6-DB0F1B57DA91} | Notes: The system shall associate each delivery record with the customer it was sent to, the sales invoice it fulfills, and the license files or documents attached. -> The system shall associate each delivery record with the customer it was sent to, the sales invoice it fulfills, and the license files or documents attached.



 |
| eaxcrmmustlinkeachsalesinvoicetoitsoriginatingoffer | EAxCRM must link each SalesInvoice to its originating Offer | Requirement | {37F7E8D8-D5BD-46ec-B91A-7ED6F2E5B781} | Notes: The system shall maintain a reference from each SalesInvoice back to the Offer that generated it, ensuring auditability of the sales process. -> The system shall maintain a reference from each SalesInvoice back to the Offer that generated it, ensuring auditability of the sales process.



 |
| eaxcrmmustoperatewithoutaidependencies | EAxCRM must operate without AI dependencies | Requirement | {6A62DFB5-CBE7-4397-8640-263F0C242661} | Notes: The system shall operate entirely without AI dependencies, using traditional parsing and scraping libraries such as PyMuPDF and BeautifulSoup. -> The system shall operate entirely without AI dependencies, using traditional parsing and scraping libraries such as PyMuPDF and BeautifulSoup.



 |
| eaxcrmmustprovideadashboardofupcomingservicerenewals | EAxCRM must provide a dashboard of upcoming service renewals | Requirement | {9646F376-4EC0-4dfc-B050-239BA21CC691} | Notes: The system shall display a dashboard showing all services approaching their expiry date, sorted by urgency, to enable proactive renewal management. -> The system shall display a dashboard showing all services approaching their expiry date, sorted by urgency, to enable proactive renewal management.



 |
| eaxcrmmustprovideprocurementreportsgroupedbyvendor | EAxCRM must provide procurement reports grouped by Vendor | Requirement | {D938A51D-6BF2-4882-9B88-035B63007259} | Notes: The system shall generate reports summarizing procurements per vendor, including quote amounts, invoice totals, and payment status. -> The system shall generate reports summarizing procurements per vendor, including quote amounts, invoice totals, and payment status.



 |
| eaxcrmmustrunonwindowsfordevelopmentanddockerqnapnasforproduction | EAxCRM must run on Windows for development and Docker/QNAP NAS for production | Requirement | {82C5CC76-459B-49e5-AD85-A406DA3E2E53} | Notes: The system shall support native Windows development and Docker-based deployment on a QNAP NAS for production use. -> The system shall support native Windows development and Docker-based deployment on a QNAP NAS for production use.



 |
| eaxcrmmustshowauxthatshowsthecurrentstateofprocurement | EAxCRM must show a UX that shows the current state of Procurement | Requirement | {2FC71345-5D8C-432b-B123-CC9F89E1B818} | Notes: The system shall display the current procurement state per vendor including which quotes have been received and which invoices are paid or pending. -> The system shall display the current procurement state per vendor including which quotes have been received and which invoices are paid or pending.



 |
| eaxcrmmuststorecommunicationhistorypercustomerretrievedfrommultipleimapaccountshaneaxpertisenlsaleseaxpertisenlinfoeaxpertisenl | EAxCRM must store communication history per customer, retrieved from multiple IMAP accounts (han@eaxpertise.nl, sales@eaxpertise.nl, info@eaxpertise.nl) | Requirement | {7DEA2FF6-9EAC-47da-BE8B-9414FAFBF5DD} | Notes: The system shall fetch and store emails from three IMAP accounts and associate them with the relevant customer for a complete communication history. -> The system shall fetch and store emails from three IMAP accounts and associate them with the relevant customer for a complete communication history.



 |
| eaxcrmmuststoredocumentsquotesinvoicesdeliverieslinkedtocustomers | EAxCRM must store documents (quotes, invoices, deliveries) linked to customers | Requirement | {3111DD70-D016-4cad-B7CC-D8FA9D63FAF0} | Notes: The system shall store customer-facing documents such as Sparx Systems quotes, incoming invoices, and delivery notes, linked to the relevant customer record. -> The system shall store customer-facing documents such as Sparx Systems quotes, incoming invoices, and delivery notes, linked to the relevant customer record.



 |
| eaxcrmmuststorevendorbankdetailsibanbicswiftpaymentcurrency | EAxCRM must store vendor bank details (IBAN, BIC/SWIFT, payment currency) | Requirement | {C7244ED6-A70C-43a2-A6C3-4A5D8AFD6A95} | Notes: The system shall record vendor bank account information including IBAN, BIC/SWIFT code, and default payment currency for invoice processing. -> The system shall record vendor bank account information including IBAN, BIC/SWIFT code, and default payment currency for invoice processing.



 |
| eaxcrmmustsupportmulticurrencyinvoiceseurusdfromsparxsystems | EAxCRM must support multi-currency invoices (EUR, USD) from Sparx Systems | Requirement | {9615BF5D-D930-4353-858D-0F75F8DA37C5} | Notes: The system shall handle incoming invoices in both EUR and USD from Sparx Systems and its subsidiaries. -> The system shall handle incoming invoices in both EUR and USD from Sparx Systems and its subsidiaries.



 |
| eaxcrmmusttracklicenserenewalslinkedtotheoriginalpurchase | EAxCRM must track license renewals linked to the original purchase | Requirement | {B1887963-752B-404c-A21E-19BBF6A32F80} | Notes: The system shall support creating renewal licenses that reference the original purchase record, enabling tracking of the full license lifecycle. -> The system shall support creating renewal licenses that reference the original purchase record, enabling tracking of the full license lifecycle.



 |
| eaxcrmmusttrackpercontactdeliverystatussentopenedbounced | EAxCRM must track per-contact delivery status (sent, opened, bounced) | Requirement | {218F552E-5931-417c-A02B-DAE8B9F69C78} | Notes: The system shall record whether each newsletter contact received, opened, or bounced the newsletter to measure engagement. -> The system shall record whether each newsletter contact received, opened, or bounced the newsletter to measure engagement.



 |
| eaxcrmmustusethedjangoadmininterfaceasitsprimaryui | EAxCRM must use the Django Admin interface as its primary UI | Requirement | {FA4583F4-87B2-4685-9904-EB9A14B63BF3} | Notes: The system shall use Django's built-in admin interface as the primary user interface for all CRM operations. -> The system shall use Django's built-in admin interface as the primary user interface for all CRM operations.



 |
| procurementcanbedoneviaabilityengineering | Procurement can be done via Ability Engineering | Requirement | {675A33C1-835A-4fda-8B97-50BA072EAFA1} | Notes: Ability Engineering is a reseller of Sparx Systems licenses, providing an alternative procurement channel. -> Ability Engineering is a reseller of Sparx Systems licenses, providing an alternative procurement channel.



 |
| procurementcanbedoneviaprolaborate | Procurement can be done via Prolaborate | Requirement | {492044AB-6D15-4455-B6D0-7C8F950480BC} | Notes: Prolaborate sells hosting services: hosting platform of Pro Cloud and EA SaaS. -> Prolaborate sells hosting services: hosting platform of Pro Cloud and EA SaaS.



 |
| procurementcanbedoneviasparxsystemseu | Procurement can be done via Sparx Systems EU | Requirement | {CEBF5E06-3BF4-4909-96A8-D91004A36647} | Notes: Sparx Systems EU is the European reseller of Sparx Systems licenses serving the EU market. -> Sparx Systems EU is the European reseller of Sparx Systems licenses serving the EU market.



 |
| procurementcanbedoneviasparxsystemsltd | Procurement can be done via Sparx Systems LTD | Requirement | {AE2C78B0-A8C3-4aef-B5AE-3C0AB921189B} | Notes: Sparx Systems LTD is the Australian headquarters and primary reseller of Sparx Systems licenses. -> Sparx Systems LTD is the Australian headquarters and primary reseller of Sparx Systems licenses.



 |
| procurementmustbetrackablepervendorwithlinkedquoteandprocurementinvoicepdfs | Procurement must be trackable per Vendor with linked Quote and ProcurementInvoice PDFs | Requirement | {5DA68B35-5206-46cb-B4D1-A38D8D655197} | Notes: The system shall allow each procurement to be tracked per vendor, with digital copies of the original quote and the incoming invoice stored as attachments. -> The system shall allow each procurement to be tracked per vendor, with digital copies of the original quote and the incoming invoice stored as attachments.



 |
| createaccountscreencreatescustomerandcontactsatomically | CreateAccountScreen: creates Customer and Contacts atomically | Requirement | {D13E63E8-1DA9-4f10-BF1C-8AFC333666C7} | Notes: The Create Customer Account screen shall create one Customer record and one or more Contact records in a single atomic save operation. A Customer must never be persisted without at least one associated Contact, since the account-creation process treats the organization and its initial contact(s) as one unit of work.

Rationale:
Matches the existing BPMN process (EAxCRM-CustomerAccountProcess.md), where account creation is modeled as one atomic activity. Prevents orphan Customer records with no way to reach anyone at the organization.

Test Cases:
- Save with 1 Customer + 1 Contact succeeds and both rows exist.
- Save attempt with Customer fields filled but zero Contacts fails validation.
- A mid-save failure (e.g. DB error on second Contact) rolls back the Customer too — no partial commit. -> The Create Customer Account screen shall create one Customer record and one or more Contact records in a single atomic save operation. A Customer must never be persisted without at least one associated Contact, since the account-creation process treats the organization and its initial contact(s) as one unit of work.



<b>Rationale:</b>

Matches the existing BPMN process (EAxCRM-CustomerAccountProcess.md), where account creation is modeled as one atomic activity. Prevents orphan Customer records with no way to reach anyone at the organization.



<b>Test Cases:</b>

1.	Save with 1 Customer + 1 Contact succeeds and both rows exist.

2.	Save attempt with Customer fields filled but zero Contacts fails validation.

3.	A mid-save failure (e.g. DB error on second Contact) rolls back the Customer too — no partial commit.

 |
| createaccountscreenstructuredstreetaddressorpobox | CreateAccountScreen: structured street address or PO Box | Requirement | {D356ED58-643D-45e6-BC31-CFA401E6C7D1} | Notes: The system shall record a Customer's address as either a structured street address (Street Name, House Number, Postal Code, City, Country) or an unstructured PO Box string, selected via a mode toggle on the create screen. Address is mandatory — the rep must actively locate it if not present in the source email.

Rationale:
Real-world postal addresses aren't always street-based; forcing one shape either loses PO Box customers or forces reps to cram a PO Box into a street-shaped field.

Test Cases:
- Street mode requires all five fields before save.
- PO Box mode requires only the PO Box text field; street fields stay null.
- Switching modes clears/ignores the other mode's fields rather than submitting both. -> The system shall record a Customer's address as either a structured street address (Street Name, House Number, Postal Code, City, Country) or an unstructured PO Box string, selected via a mode toggle on the create screen. Address is mandatory — the rep must actively locate it if not present in the source email.



<b>Rationale:</b>

Real-world postal addresses aren't always street-based; forcing one shape either loses PO Box customers or forces reps to cram a PO Box into a street-shaped field.



<b>Test Cases:</b>

1.	Street mode requires all five fields before save.

2.	PO Box mode requires only the PO Box text field; street fields stay null.

3.	Switching modes clears/ignores the other mode's fields rather than submitting both.

 |
| primarycontactruleatleastonecontactmustalwaysbeprimary | Primary Contact Rule: at least one Contact must always be Primary | Requirement | {5E968ECB-4896-45fa-9FAE-4518F9F92ECF} | Notes: Regardless of how many Contacts are entered on account creation, exactly one must carry the role Primary. This holds even when only one Contact is entered — in that case the first (and only) Contact row defaults its role to Primary automatically rather than being left blank.

Rationale:
Ensures every account always has one unambiguous point of contact, and gives a clear successor path when combined with the Secondary role (CRM-10).

Test Cases:
- Single-contact save with role left untouched saves with role = Primary.
- Two-contact save where neither is marked Primary is rejected.
- Two-contact save with exactly one Primary succeeds. -> Regardless of how many Contacts are entered on account creation, exactly one must carry the role Primary. This holds even when only one Contact is entered — in that case the first (and only) Contact row defaults its role to Primary automatically rather than being left blank.



<b>Rationale:</b>

Ensures every account always has one unambiguous point of contact, and gives a clear successor path when combined with the Secondary role (CRM-10).



<b>Test Cases:</b>

1.	Single-contact save with role left untouched saves with role = Primary.

2.	Two-contact save where neither is marked Primary is rejected.

3.	Two-contact save with exactly one Primary succeeds.

 |
| contactrolerulerequiredonceasecondcontactexists | Contact Role Rule: required once a second Contact exists | Requirement | {D97412A1-AF30-45ac-AE2D-E6A4A423CF65} | Notes: Role is optional only when exactly one Contact exists on the form. As soon as a second Contact row is added, role becomes a required field for every Contact on the form, including ones already entered.

Rationale:
Prevents accounts with multiple unnamed-function contacts, where reps can no longer tell who does what.

Test Cases:
- One contact, role left at its default, saves fine (subject to CRM-8).
- Add a second contact, leave either role blank — save is rejected.
- Fill both roles — save succeeds. -> Role is optional only when exactly one Contact exists on the form. As soon as a second Contact row is added, role becomes a required field for every Contact on the form, including ones already entered.



<b>Rationale:</b>

Prevents accounts with multiple unnamed-function contacts, where reps can no longer tell who does what.



<b>Test Cases:</b>

1.	One contact, role left at its default, saves fine (subject to CRM-8).

2.	Add a second contact, leave either role blank — save is rejected.

3.	Fill both roles — save succeeds.

 |
| contactrolerulesecondaryroleadded | Contact Role Rule: Secondary role added | Requirement | {D37E1D4E-051B-455c-8B98-23F98FC4A551} | Notes: The Contact role choices shall include Secondary, alongside Primary/Purchase/Sales/License Holder. Secondary denotes a colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties, and is the expected successor role if the Primary contact leaves the organization.

Rationale:
Organizations commonly designate a backup point of contact; without this role it would be miscategorized as Purchase/Sales or left blank, losing the succession signal.

Test Cases:
- Role dropdown lists Secondary as a selectable option.
- A Contact saved with role=Secondary persists and displays correctly.
- Filtering/reporting by role can isolate Secondary contacts. -> The Contact role choices shall include Secondary, alongside Primary/Purchase/Sales/License Holder. Secondary denotes a colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties, and is the expected successor role if the Primary contact leaves the organization.



<b>Rationale:</b>

Organizations commonly designate a backup point of contact; without this role it would be miscategorized as Purchase/Sales or left blank, losing the succession signal.



<b>Test Cases:</b>

1.	Role dropdown lists Secondary as a selectable option.

2.	A Contact saved with role=Secondary persists and displays correctly.

3.	Filtering/reporting by role can isolate Secondary contacts.

 |
| newsletterconsentruleoptindefaultstofalse | Newsletter Consent Rule: opt-in defaults to false | Requirement | {EAAD0687-E661-4943-93EB-86376B3FA8EF} | Notes: Contact.opt_in shall default to False when created via Create Customer Account, and shall only be set True if the rep has explicit evidence of consent in the source email. The same field must remain independently editable later via the existing Suggest Newsletter Opt-in screen.

Rationale:
Marketing consent is a legal/compliance flag and must never be inferred just because a customer initiated contact; giving reps two deliberate checkpoints (creation-time and a later prompt) increases the chance of capturing real consent without ever defaulting to true.

Test Cases:
- New Contact via create screen has opt_in=False when the checkbox is left untouched.
- Checking the box at creation sets opt_in=True and stamps opt_in_date.
- opt_in can later be toggled from the Suggest Newsletter Opt-in screen independent of the create screen's state. -> Contact.opt_in shall default to False when created via Create Customer Account, and shall only be set True if the rep has explicit evidence of consent in the source email. The same field must remain independently editable later via the existing Suggest Newsletter Opt-in screen.



<b>Rationale:</b>

Marketing consent is a legal/compliance flag and must never be inferred just because a customer initiated contact; giving reps two deliberate checkpoints (creation-time and a later prompt) increases the chance of capturing real consent without ever defaulting to true.



<b>Test Cases:</b>

1.	New Contact via create screen has opt_in=False when the checkbox is left untouched.

2.	Checking the box at creation sets opt_in=True and stamps opt_in_date.

3.	opt_in can later be toggled from the Suggest Newsletter Opt-in screen independent of the create screen's state.

 |
| createaccountscreennotesandphonecapturableatcreation | CreateAccountScreen: notes and phone capturable at creation | Requirement | {0EF04071-8682-4579-A08F-8A4F75EE8713} | Notes: The create screen shall include optional fields for Customer.notes (free text) and Contact.phone, since both are sometimes directly available in the source email (footer/signature) and cheaper to capture immediately than via a later edit step.



<b>Rationale:</b>

Reduces follow-up data-entry work when the information is already visible to the rep; both remain optional since they're often absent from a first email.



<b>Test Cases:</b>

1.	Save succeeds with both fields blank.

2.	Save succeeds with notes and/or phone filled in.

3.	Values persist correctly on the respective Customer/Contact records. -> The create screen shall include optional fields for Customer.notes (free text) and Contact.phone, since both are sometimes directly available in the source email (footer/signature) and cheaper to capture immediately than via a later edit step.



<b>Rationale:</b>

Reduces follow-up data-entry work when the information is already visible to the rep; both remain optional since they're often absent from a first email.



<b>Test Cases:</b>

1.	Save succeeds with both fields blank.

2.	Save succeeds with notes and/or phone filled in.

3.	Values persist correctly on the respective Customer/Contact records.

 |

## 2026-07-07 12:13:41 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Renamed
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| createaccountscreencreatescustomerandcontactsatomically | CreateAccountScreen: creates Customer and Contacts atomically | Requirement | {D13E63E8-1DA9-4f10-BF1C-8AFC333666C7} | Name: Create Customer Account must create Customer and Contacts atomically -> CreateAccountScreen: creates Customer and Contacts atomically |
| createaccountscreenstructuredstreetaddressorpobox | CreateAccountScreen: structured street address or PO Box | Requirement | {D356ED58-643D-45e6-BC31-CFA401E6C7D1} | Name: Customer address must support both structured street address and PO Box -> CreateAccountScreen: structured street address or PO Box |
| primarycontactruleatleastonecontactmustalwaysbeprimary | Primary Contact Rule: at least one Contact must always be Primary | Requirement | {5E968ECB-4896-45fa-9FAE-4518F9F92ECF} | Name: At least one Contact per Customer must always be Primary -> Primary Contact Rule: at least one Contact must always be Primary |
| contactrolerulerequiredonceasecondcontactexists | Contact Role Rule: required once a second Contact exists | Requirement | {D97412A1-AF30-45ac-AE2D-E6A4A423CF65} | Name: Role becomes required once a second Contact is added -> Contact Role Rule: required once a second Contact exists |
| contactrolerulesecondaryroleadded | Contact Role Rule: Secondary role added | Requirement | {D37E1D4E-051B-455c-8B98-23F98FC4A551} | Name: Role list must include Secondary -> Contact Role Rule: Secondary role added |
| newsletterconsentruleoptindefaultstofalse | Newsletter Consent Rule: opt-in defaults to false | Requirement | {EAAD0687-E661-4943-93EB-86376B3FA8EF} | Name: Newsletter opt-in must default to false and stay editable in two places -> Newsletter Consent Rule: opt-in defaults to false |
| createaccountscreennotesandphonecapturableatcreation | CreateAccountScreen: notes and phone capturable at creation | Requirement | {0EF04071-8682-4579-A08F-8A4F75EE8713} | Name: Notes and phone must be capturable opportunistically at creation time -> CreateAccountScreen: notes and phone capturable at creation |

## 2026-07-07 12:09:55 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| createcustomeraccountmustcreatecustomerandcontactsatomically | Create Customer Account must create Customer and Contacts atomically | Requirement | {D13E63E8-1DA9-4f10-BF1C-8AFC333666C7} | Notes: The Create Customer Account screen shall create one Customer record and one or more Contact records in a single atomic save operation. A Customer must never be persisted without at least one associated Contact, since the account-creation process treats the organization and its initial contact(s) as one unit of work. -> The Create Customer Account screen shall create one Customer record and one or more Contact records in a single atomic save operation. A Customer must never be persisted without at least one associated Contact, since the account-creation process treats the organization and its initial contact(s) as one unit of work.

Rationale:
Matches the existing BPMN process (EAxCRM-CustomerAccountProcess.md), where account creation is modeled as one atomic activity. Prevents orphan Customer records with no way to reach anyone at the organization.

Test Cases:
- Save with 1 Customer + 1 Contact succeeds and both rows exist.
- Save attempt with Customer fields filled but zero Contacts fails validation.
- A mid-save failure (e.g. DB error on second Contact) rolls back the Customer too — no partial commit. |
| customeraddressmustsupportbothstructuredstreetaddressandpobox | Customer address must support both structured street address and PO Box | Requirement | {D356ED58-643D-45e6-BC31-CFA401E6C7D1} | Notes: The system shall record a Customer's address as either a structured street address (Street Name, House Number, Postal Code, City, Country) or an unstructured PO Box string, selected via a mode toggle on the create screen. Address is mandatory — the rep must actively locate it if not present in the source email. -> The system shall record a Customer's address as either a structured street address (Street Name, House Number, Postal Code, City, Country) or an unstructured PO Box string, selected via a mode toggle on the create screen. Address is mandatory — the rep must actively locate it if not present in the source email.

Rationale:
Real-world postal addresses aren't always street-based; forcing one shape either loses PO Box customers or forces reps to cram a PO Box into a street-shaped field.

Test Cases:
- Street mode requires all five fields before save.
- PO Box mode requires only the PO Box text field; street fields stay null.
- Switching modes clears/ignores the other mode's fields rather than submitting both. |
| atleastonecontactpercustomermustalwaysbeprimary | At least one Contact per Customer must always be Primary | Requirement | {5E968ECB-4896-45fa-9FAE-4518F9F92ECF} | Notes: Regardless of how many Contacts are entered on account creation, exactly one must carry the role Primary. This holds even when only one Contact is entered — in that case the first (and only) Contact row defaults its role to Primary automatically rather than being left blank. -> Regardless of how many Contacts are entered on account creation, exactly one must carry the role Primary. This holds even when only one Contact is entered — in that case the first (and only) Contact row defaults its role to Primary automatically rather than being left blank.

Rationale:
Ensures every account always has one unambiguous point of contact, and gives a clear successor path when combined with the Secondary role (CRM-10).

Test Cases:
- Single-contact save with role left untouched saves with role = Primary.
- Two-contact save where neither is marked Primary is rejected.
- Two-contact save with exactly one Primary succeeds. |
| rolebecomesrequiredonceasecondcontactisadded | Role becomes required once a second Contact is added | Requirement | {D97412A1-AF30-45ac-AE2D-E6A4A423CF65} | Notes: Role is optional only when exactly one Contact exists on the form. As soon as a second Contact row is added, role becomes a required field for every Contact on the form, including ones already entered. -> Role is optional only when exactly one Contact exists on the form. As soon as a second Contact row is added, role becomes a required field for every Contact on the form, including ones already entered.

Rationale:
Prevents accounts with multiple unnamed-function contacts, where reps can no longer tell who does what.

Test Cases:
- One contact, role left at its default, saves fine (subject to CRM-8).
- Add a second contact, leave either role blank — save is rejected.
- Fill both roles — save succeeds. |
| rolelistmustincludesecondary | Role list must include Secondary | Requirement | {D37E1D4E-051B-455c-8B98-23F98FC4A551} | Notes: The Contact role choices shall include Secondary, alongside Primary/Purchase/Sales/License Holder. Secondary denotes a colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties, and is the expected successor role if the Primary contact leaves the organization. -> The Contact role choices shall include Secondary, alongside Primary/Purchase/Sales/License Holder. Secondary denotes a colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties, and is the expected successor role if the Primary contact leaves the organization.

Rationale:
Organizations commonly designate a backup point of contact; without this role it would be miscategorized as Purchase/Sales or left blank, losing the succession signal.

Test Cases:
- Role dropdown lists Secondary as a selectable option.
- A Contact saved with role=Secondary persists and displays correctly.
- Filtering/reporting by role can isolate Secondary contacts. |
| newsletteroptinmustdefaulttofalseandstayeditableintwoplaces | Newsletter opt-in must default to false and stay editable in two places | Requirement | {EAAD0687-E661-4943-93EB-86376B3FA8EF} | Notes: Contact.opt_in shall default to False when created via Create Customer Account, and shall only be set True if the rep has explicit evidence of consent in the source email. The same field must remain independently editable later via the existing Suggest Newsletter Opt-in screen. -> Contact.opt_in shall default to False when created via Create Customer Account, and shall only be set True if the rep has explicit evidence of consent in the source email. The same field must remain independently editable later via the existing Suggest Newsletter Opt-in screen.

Rationale:
Marketing consent is a legal/compliance flag and must never be inferred just because a customer initiated contact; giving reps two deliberate checkpoints (creation-time and a later prompt) increases the chance of capturing real consent without ever defaulting to true.

Test Cases:
- New Contact via create screen has opt_in=False when the checkbox is left untouched.
- Checking the box at creation sets opt_in=True and stamps opt_in_date.
- opt_in can later be toggled from the Suggest Newsletter Opt-in screen independent of the create screen's state. |
| notesandphonemustbecapturableopportunisticallyatcreationtime | Notes and phone must be capturable opportunistically at creation time | Requirement | {0EF04071-8682-4579-A08F-8A4F75EE8713} | Notes: The create screen shall include optional fields for Customer.notes (free text) and Contact.phone, since both are sometimes directly available in the source email (footer/signature) and cheaper to capture immediately than via a later edit step. -> The create screen shall include optional fields for Customer.notes (free text) and Contact.phone, since both are sometimes directly available in the source email (footer/signature) and cheaper to capture immediately than via a later edit step.

Rationale:
Reduces follow-up data-entry work when the information is already visible to the rep; both remain optional since they're often absent from a first email.

Test Cases:
- Save succeeds with both fields blank.
- Save succeeds with notes and/or phone filled in.
- Values persist correctly on the respective Customer/Contact records. |

## 2026-07-07 11:52:34 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| Contact->createcustomeraccountmustcreatecustomerandcontactsatomically | Contact | Realisation | {1C74879A-4D2C-4c13-ABBA-27DC5E85B651} |
| Customer->createcustomeraccountmustcreatecustomerandcontactsatomically | Customer | Realisation | {0BCDDF7D-0CFE-4c97-9BFC-CDC96E52AF63} |
| Customer->customeraddressmustsupportbothstructuredstreetaddressandpobox | Customer | Realisation | {C55E5F91-7486-4351-9CF2-F7936E3C317F} |
| Contact->atleastonecontactpercustomermustalwaysbeprimary | Contact | Realisation | {50B15DAC-B55D-4b70-BB1A-FE73FAF96159} |
| Customer->atleastonecontactpercustomermustalwaysbeprimary | Customer | Realisation | {8ADE32B6-5F31-4448-B360-D28E798E12FF} |
| Contact->rolebecomesrequiredonceasecondcontactisadded | Contact | Realisation | {A66D55F8-E283-481b-9BD3-87094DC4C12F} |
| Contact->rolelistmustincludesecondary | Contact | Realisation | {9AC979CD-7676-4ee7-9405-01AC8A460983} |
| Contact->newsletteroptinmustdefaulttofalseandstayeditableintwoplaces | Contact | Realisation | {EDF5DBD2-F491-4404-985A-8C30B03F0D8E} |
| Contact->notesandphonemustbecapturableopportunisticallyatcreationtime | Contact | Realisation | {80479810-50A0-44df-8FFD-DE61A9E76BE2} |
| Customer->notesandphonemustbecapturableopportunisticallyatcreationtime | Customer | Realisation | {F001412D-C782-4ccb-BE49-2DF5EADFD2BF} |

## 2026-07-06 16:33:27 — Audit

### Checkpoints
- Seeding properties
- Seed complete

## 2026-07-06 16:32:48 — Audit

### Checkpoints
- Sync from EA

## 2026-07-06 16:21:02 — Audit

### Checkpoints
- Sync from EA

### Deleted
| eid | Name | Type | GUID |
|-----|------|------|------|
| eaxcrmmustdetectandflagpotentialduplicatecustomeraccountsformergeordiscard | EAxCRM must detect and flag potential duplicate Customer Accounts for merge or discard | Requirement |  |
| eaxcrmmustretrievecustomeremailhistorybyscanningconfiguredimapmailboxes | EAxCRM must retrieve customer email history by scanning configured IMAP mailboxes | Requirement |  |
| eaxcrmmustsuggestnewsletteroptinforprimaryandlicenseholdercontactspendinguserconfirmation | EAxCRM must suggest newsletter opt-in for Primary and License Holder Contacts pending user confirmation | Requirement |  |
| eaxcrmmustsupportcreatingacustomeraccountwithaminimalinitialcontact | EAxCRM must support creating a Customer Account with a minimal initial Contact | Requirement |  |
| eaxcrmmustverifyorcreatethecustomeraccountwhenregisteringanrfqfromanunrecognizedorganization | EAxCRM must verify or create the Customer Account when registering an RFQ from an unrecognized organization | Requirement |  |

