# EAxCRM — Requirements

**Model ID**: r-eacrm
**Purpose**: Requirements for the EAxCRM system
**Version**: 1.0

### Requirement—eaxcrmmustsupporttheprocurementprocess
- Name: EAxCRM must support the procurement process
- ID: PRO-1
- Description: The system shall manage the end-to-end procurement workflow from receiving a supplier quote, creating a purchase record, and recording the incoming invoice.
- Entities: ProcurementInvoice, Purchase, Quote, Vendor
- Status: Approved
- Version: 1.0
- GUID: {119DE89A-BFF5-44ab-AC67-6FC9DB0F8C10}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustmanagecustomerorganizationsandtheircontactswithspecificrolesprimarypurchasesaleslicenseholder
- Name: EAxCRM must manage Customer organizations and their Contacts with specific roles (Primary, Purchase, Sales, License Holder)
- ID: CRM-1
- Description: The system shall store customer organizations and their associated contacts, each with one or more roles that determine their function in the CRM workflow.
- Entities: Contact, Customer
- Status: Proposed
- Version: 1.0
- GUID: {C8A09A87-5B2B-4d72-896F-77C079F7C2DA}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustusesqliteasitsdatabasebackend
- Name: EAxCRM must use SQLite as its database backend
- ID: TEC-1
- Description: The system shall use a file-based SQLite database suitable for deployment on a QNAP NAS without requiring a separate database server.
- Status: Proposed
- Version: 1.0
- GUID: {30EA2FCA-BEA7-4fd7-A7E8-F5ECD78B8ADF}
- Parents:
  - (none — top-level)

### Requirement—eaxcrmmustsupportcomposingnewslettersfromscrapedarticlesonsparxsystemscomandsparxsystemseu
- Name: EAxCRM must support composing newsletters from scraped articles on SparxSystems.com and sparxsystems.eu
- ID: NWS-1
- Description: The system shall scrape news articles from SparxSystems.com and sparxsystems.eu and allow composing an EAxNewsletter from selected article summaries and links.
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
- Entities: Delivery
- Status: Proposed
- Version: 1.0
- GUID: {2553EA37-D4C2-4c1c-BA2B-65ADD9C06F80}
- Parents:
  - (none — top-level)

### Requirement—procurementcanbedoneviamultipleparties
- Name: Procurement can be done via multiple parties
- ID: PRO-5
- Description: There are several suppliers to EAxpertise.
- Entities: Vendor
- Status: Approved
- Version: 1.0
- GUID: {506DEB0C-8BE3-4a76-B52E-E00F3DBB672E}
- Parents:
  - eaxcrmmustsupporttheprocurementprocess

### Requirement—eaxcrmmustdetectserviceexpiryandnotifytheuserwhenrenewalisneeded
- Name: EAxCRM must detect service expiry and notify the user when renewal is needed
- ID: SAL-3
- Description: The system shall monitor service expiry dates and alert the user when a service needs renewal, using the expiry_month and renewal_notice_sent fields.
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
- Entities: ImapAccount
- Status: Proposed
- Version: 1.0
- GUID: {F6EFB60E-E9F5-4ea1-8EBD-49692050E063}
- Parents:
  - eaxcrmmustusesqliteasitsdatabasebackend

### Requirement—eaxcrmmustenforceadraftreviewsendworkflowwithmanualapproval
- Name: EAxCRM must enforce a Draft -> Review -> Send workflow with manual approval
- ID: NWS-2
- Description: The system shall require newsletters to go through three states: Draft (composition), Review (manual approval), and Sent (dispatch).
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
- Status: Proposed
- Version: 1.0
- GUID: {6A62DFB5-CBE7-4397-8640-263F0C242661}
- Parents:
  - eaxcrmmustusesqliteasitsdatabasebackend

### Requirement—eaxcrmmustprovideadashboardofupcomingservicerenewals
- Name: EAxCRM must provide a dashboard of upcoming service renewals
- ID: RPT-2
- Description: The system shall display a dashboard showing all services approaching their expiry date, sorted by urgency, to enable proactive renewal management.
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
- Status: Proposed
- Version: 1.0
- GUID: {82C5CC76-459B-49e5-AD85-A406DA3E2E53}
- Parents:
  - eaxcrmmustusesqliteasitsdatabasebackend

### Requirement—eaxcrmmustshowauxthatshowsthecurrentstateofprocuement
- Name: EAxCRM must show a UX that shows the current state of Procuement
- ID: RPT-4
- Description: The system shall display the current procurement state per vendor including which quotes have been received and which invoices are paid or pending.
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
- Status: Proposed
- Version: 1.0
- GUID: {FA4583F4-87B2-4685-9904-EB9A14B63BF3}
- Parents:
  - eaxcrmmustusesqliteasitsdatabasebackend

### Requirement—procurementcanbedoneviaabilityengineering
- Name: Procurement can be done via Ability Engineering
- ID: PRO-5.3
- Description: Ability Engineering is a reseller of Sparx Systems licenses, providing an alternative procurement channel.
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
- Entities: Vendor
- Status: Approved
- Version: 1.0
- GUID: {AE2C78B0-A8C3-4aef-B5AE-3C0AB921189B}
- Parents:
  - procurementcanbedoneviamultipleparties

### Requirement—procurementmustbetrackablepervendorwithlinkedquoteandprocurementinvoicepdfs
- Name: Procurement must be trackable per Vendor with linked Quote and ProcurementInvoice PDFs
- ID: PRO-2
- Description: The system shall allow each procurement to be tracked per vendor, with digital copies of the original quote and the incoming invoice stored as attachments.
- Entities: ProcurementInvoice, Quote, Vendor
- Status: Proposed
- Version: 1.0
- GUID: {5DA68B35-5206-46cb-B4D1-A38D8D655197}
- Parents:
  - eaxcrmmustsupporttheprocurementprocess

