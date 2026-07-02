# EAxCRM — ArchiMate Model

**Model ID**: m-eacrm
**Purpose**: Enterprise Architect Customer Relationship Manager
**Version**: 2.0
**Elements**: 66 (was 44)
**Relationships**: 91 (was 57)
**Changes in v2.0**: Added Sales Management function with 5 sub-processes, Vendor actor, and 7 new business objects with corresponding data objects and services. Updated Purchase Data description for removed attributes.

## Elements

### BusinessActor — e-customer
- Name: Customer
- Description: An organization that uses Sparx EA and receives services from EAxpertise.
- GUID: {B148F708-0B53-57AF-8062-C4CA1EC8F666}
- Layer: Business

### BusinessActor — e-vendor
- Name: Vendor
- Description: Supplier organization (e.g. Sparx Systems, Prolaborate) that provides license and service quotes.
- GUID: {47E9FF94-8596-4CB4-9A23-DBCBCC1BF184}
- Layer: Business

### BusinessRole — e-role-primary
- Name: Primary Contact
- Description: The main point of contact for the customer.
- GUID: {FBB0A3A1-4CA9-57DF-B3EE-64FD5F30A3BF}
- Layer: Business

### BusinessRole — e-role-purchase
- Name: Purchase Contact
- Description: Handles procurement and purchasing decisions.
- GUID: {4790AB0F-805C-5E4B-BC8B-EABA5A78A5DD}
- Layer: Business

### BusinessRole — e-role-sales
- Name: Sales Contact
- Description: Involved in sales conversations and opportunities.
- GUID: {3D3C32B1-E658-5B07-837D-14B6FC938371}
- Layer: Business

### BusinessRole — e-role-license
- Name: License Holder
- Description: Holds and manages Sparx EA license entitlements.
- GUID: {5E37383A-2C3A-53A9-9B2C-CFAD9B873207}
- Layer: Business

### BusinessFunction — e-func-insight
- Name: Customer Insight
- Description: Manage contact information, retrieve communications, and store customer documents.
- GUID: {EA783C60-73B7-557A-B2E6-95B012B4B467}
- Layer: Business

### BusinessFunction — e-func-newsletter
- Name: Newsletter Management
- Description: Create, review, and send newsletters to opted-in contacts every 6 weeks.
- GUID: {CD9BE9D0-8CB9-583F-8F3B-BB17CFAE59B8}
- Layer: Business

### BusinessFunction — e-func-sales
- Name: Sales Management
- Description: Manage offers, sales invoices, purchases, vendor quotes, deliveries, and service subscriptions for customers.
- GUID: {EC36EAFE-A71D-4B5D-800A-6B9BEB71F23C}
- Layer: Business

### BusinessProcess — e-process-imap
- Name: Retrieve Communications
- Description: Fetch emails from 3-5 IMAP accounts and store them with attachments.
- GUID: {003ADBFC-AA69-5544-952C-B4ECBEF16D77}
- Layer: Business

### BusinessProcess — e-process-parse
- Name: Parse Documents
- Description: Extract text content from PDF and TXT attachments.
- GUID: {986D8C82-81ED-5D82-8A30-04B10592754B}
- Layer: Business

### BusinessProcess — e-process-scrape
- Name: Scrape News Sources
- Description: Fetch articles from SparxSystems.com and sparxsystems.eu.
- GUID: {3C445BDB-333C-5CE9-9DE5-9FC2E473C61E}
- Layer: Business

### BusinessProcess — e-process-compose
- Name: Compose Newsletter
- Description: Select 5 articles, write headings and summaries, add logo, and format the EAxNewsletter.
- GUID: {E0903B06-3A03-57C6-8D7B-ED888D04E5DD}
- Layer: Business

### BusinessProcess — e-process-review
- Name: Review Newsletter
- Description: Manual review and approval before sending.
- GUID: {50D57F5D-E41C-55A1-9D40-2A96969CEEB2}
- Layer: Business

### BusinessProcess — e-process-send
- Name: Send Newsletter
- Description: Send the EAxNewsletter to all opted-in contacts.
- GUID: {1E921810-5230-57FC-A082-F4D9CA7553DC}
- Layer: Business

### BusinessProcess — e-process-optin
- Name: Manage Opt-in
- Description: Mark email addresses in CRM as opted-in for newsletter delivery.
- GUID: {2B91C473-5506-5CD4-BF43-17B60A0D82D2}
- Layer: Business

### BusinessProcess — e-process-rfq
- Name: Handle RFQ
- Description: Receive and register incoming customer requests for quotes.
- GUID: {48D2A2B9-7357-4856-B27A-0424D1D8894B}
- Layer: Business

### BusinessProcess — e-process-offer
- Name: Manage Offer
- Description: Prepare, review, accept, or reject sales offers with license and service line items.
- GUID: {DA0A79F5-B2A0-4D11-96BE-1250C761E275}
- Layer: Business

### BusinessProcess — e-process-procure
- Name: Procure Licenses & Services
- Description: Request vendor quotes, place purchase orders, and receive license files and service agreements.
- GUID: {C0F0E339-627F-4C61-8B8A-A283816CDE56}
- Layer: Business

### BusinessProcess — e-process-deliver
- Name: Manage Delivery
- Description: Prepare and send delivery packages containing license files and service credentials to customers.
- GUID: {CE6A0B79-B4CF-4C00-89D0-FE71AEB0A810}
- Layer: Business

### BusinessProcess — e-process-invoice
- Name: Manage Invoicing & Payment
- Description: Prepare sales invoices, handle payment validation, and remind customers of overdue payments.
- GUID: {43EF4805-AD6E-47CE-85DA-5A759213C49B}
- Layer: Business

### BusinessObject — e-bo-customer
- Name: Customer Data
- Description: Customer master data including name and address.
- GUID: {FC29A4BD-5FCF-5B4E-B4E9-48E1643ABE90}
- Layer: Business

### BusinessObject — e-bo-contact
- Name: Contact Data
- Description: Contact person details with role, name, email, and opt-in status.
- GUID: {2D4934DB-0E97-55E5-B178-104665B76CAC}
- Layer: Business

### BusinessObject — e-bo-communication
- Name: Communication Data
- Description: Email metadata and body retrieved from IMAP accounts.
- GUID: {A9BC9B53-1E95-59B5-B5A0-ACAB75CF1CB4}
- Layer: Business

### BusinessObject — e-bo-document
- Name: Document Data
- Description: Parsed content from PDF and TXT attachments, especially license communications.
- GUID: {2A2CE011-F37A-5CDD-AD8D-1E7395393C15}
- Layer: Business

### BusinessObject — e-bo-newsletter
- Name: Newsletter Data
- Description: The composed EAxNewsletter with articles, branding, and delivery status.
- GUID: {D856F985-CF23-5C1A-B65F-A60FB217C63B}
- Layer: Business

### BusinessObject — e-bo-license
- Name: License Data
- Description: License entitlement records per customer, including start and expiry dates.
- GUID: {B5D55803-1BAB-567B-97F0-84DC6E786C19}
- Layer: Business

### BusinessObject — e-bo-lineitem
- Name: License Line Item Data
- Description: Individual products or services under a license, including 12-month service rentals.
- GUID: {2EFEE2DC-C7DB-51AE-962F-64340833C27B}
- Layer: Business

### BusinessObject — e-bo-purchase
- Name: Purchase Data
- Description: Procurement event linking a quote to its procurement invoice. Can be a Product purchase (with quote/invoice PDFs) or a Service procurement.
- GUID: {4488B57F-D62F-59BA-9589-6E2353750068}
- Layer: Business

### BusinessObject — e-bo-offer
- Name: Offer Data
- Description: Sales proposal document sent to a customer, containing license and service line items with pricing.
- GUID: {FCC24A4D-3843-4C72-B149-ACCBA154E285}
- Layer: Business

### BusinessObject — e-bo-quote
- Name: Quote Data
- Description: Pricing quote received from a vendor in response to a license or service request.
- GUID: {84782D32-D9F2-4D40-B68F-00A0B0A5831D}
- Layer: Business

### BusinessObject — e-bo-delivery
- Name: Delivery Data
- Description: Handover package containing license files, service agreements, and delivery notes sent to the customer.
- GUID: {A05C31DD-50DB-4FDA-A5AF-CCCDF0D48B86}
- Layer: Business

### BusinessObject — e-bo-salesinvoice
- Name: Sales Invoice Data
- Description: Outgoing invoice sent to a customer for purchased licenses and services.
- GUID: {F88321BE-50E7-47B8-AFA4-81EB711A0DE2}
- Layer: Business

### BusinessObject — e-bo-procurementinvoice
- Name: Procurement Invoice Data
- Description: Incoming invoice from a vendor for procured licenses or services.
- GUID: {AA6C9C32-36D1-4FA4-8449-5D47B2D8E580}
- Layer: Business

### BusinessObject — e-bo-service
- Name: Service Data
- Description: Resold service subscriptions (SaaS, training, support) with billing frequency, start/expiry months, and renewal status.
- GUID: {687D1D7C-683A-40AA-916A-908CD02CF0CB}
- Layer: Business

### BusinessObject — e-bo-vendor
- Name: Vendor Data
- Description: Supplier organization information including banking details and payment currency.
- GUID: {D0D36D39-F5A0-4D62-892B-512D240B7337}
- Layer: Business

### ApplicationComponent — e-app-django
- Name: EAxCRM Django Application
- Description: The core Django web application serving the CRM.
- GUID: {E92F8E14-C57E-5916-803F-19761371CA3F}
- Layer: Application

### ApplicationService — e-svc-customer
- Name: Customer Management Service
- Description: CRUD operations for customers and contacts.
- GUID: {96C42354-9D90-51A8-A4E3-002C2100E98F}
- Layer: Application

### ApplicationService — e-svc-imap
- Name: IMAP Fetch Service
- Description: Connects to IMAP accounts and retrieves unseen emails with attachments.
- GUID: {DB26E61C-8FC5-58E8-AC35-C4B7C0802592}
- Layer: Application

### ApplicationService — e-svc-parse
- Name: Document Parse Service
- Description: Extracts text from PDF and TXT file attachments.
- GUID: {2AD065BF-A77D-5CA0-AA14-5DBC270FB33A}
- Layer: Application

### ApplicationService — e-svc-scrape
- Name: News Scrape Service
- Description: Scrapes SparxSystems.com and sparxsystems.eu for recent articles.
- GUID: {F377500E-851B-5C07-A34C-A2B46ECC53D4}
- Layer: Application

### ApplicationService — e-svc-newsletter
- Name: Newsletter Service
- Description: Composes, previews, and sends the EAxNewsletter.
- GUID: {7FACC8A1-C9D6-58AB-8C70-5BE8E9AD3426}
- Layer: Application

### ApplicationService — e-svc-sales
- Name: Sales Management Service
- Description: CRUD operations for offers, sales invoices, purchases, quotes, deliveries, services, and vendors.
- GUID: {CBE22C39-BFDA-401D-94CA-E0C50C1D3617}
- Layer: Application

### DataObject — e-data-customer
- Name: Customer Record
- Description: Database record containing customer name, address, and metadata.
- GUID: {0E3CBE98-6A3A-5B98-BFD7-42C3A554762D}
- Layer: Application

### DataObject — e-data-contact
- Name: Contact Record
- Description: Database record for a contact with FK to customer, role, name, email, opt-in flag.
- GUID: {9D2A332A-B410-5593-B08B-28E491DBDA79}
- Layer: Application

### DataObject — e-data-email
- Name: Email Record
- Description: Stored email with sender, subject, body, date, and original raw file.
- GUID: {A9A7DBEA-A838-5A26-8118-30201ACC5750}
- Layer: Application

### DataObject — e-data-attachment
- Name: Attachment Record
- Description: Parsed PDF or TXT attachment linked to an email, with extracted text content.
- GUID: {842E3445-6B06-57A6-8078-16DBBB814B2B}
- Layer: Application

### DataObject — e-data-article
- Name: Article Record
- Description: Scraped news article with source URL, heading, summary, and selection status.
- GUID: {C126DF4C-BDC6-525C-8C05-700E81017C56}
- Layer: Application

### DataObject — e-data-newsletter
- Name: Newsletter Record
- Description: Composed newsletter with HTML/text body, status (Draft/Review/Sent), and send date.
- GUID: {50876AE0-19AC-5948-9565-6963DBA594BF}
- Layer: Application

### DataObject — e-data-license
- Name: License Record
- Description: Database record with license type, start/expiry dates, and link to source attachment or purchase.
- GUID: {3B0B3298-D7AD-51A6-A6BB-9BB6E7EF496E}
- Layer: Application

### DataObject — e-data-lineitem
- Name: License Line Item Record
- Description: Database record for a product or service under a license with description, quantity, and service flag.
- GUID: {7B99A2C4-2306-5BAA-B6DC-5739D93E9C1F}
- Layer: Application

### DataObject — e-data-purchase
- Name: Purchase Record
- Description: Database record with type (Product/Service), purchase date, and links to originating quote and fulfilling procurement invoice.
- GUID: {5B3A680E-B680-5B82-83A8-EABD703B2627}
- Layer: Application

### DataObject — e-data-offer
- Name: Offer Record
- Description: Database record for a sales proposal with offer number, amount, currency, status, and PDF file.
- GUID: {77F38D68-7170-4F7B-B15A-BF489FFFD66C}
- Layer: Application

### DataObject — e-data-quote
- Name: Quote Record
- Description: Database record for a vendor quote with quote number, amount, and PDF file.
- GUID: {0A2721B0-C230-4596-8A0E-5C8E932259E0}
- Layer: Application

### DataObject — e-data-delivery
- Name: Delivery Record
- Description: Database record for a delivery handover with sent date, status, and linked attachments.
- GUID: {C1195A6C-3853-4235-86EC-08EF707D0CF6}
- Layer: Application

### DataObject — e-data-salesinvoice
- Name: Sales Invoice Record
- Description: Database record for an outgoing sales invoice with invoice number, amount, currency, and paid status.
- GUID: {E1227B80-468B-4AC6-9AA6-206C64048A56}
- Layer: Application

### DataObject — e-data-procurementinvoice
- Name: Procurement Invoice Record
- Description: Database record for an incoming vendor invoice with invoice number, amount, currency, and paid status.
- GUID: {1AC9B4FD-587B-4401-9CEF-706CE833471F}
- Layer: Application

### DataObject — e-data-service
- Name: Service Record
- Description: Database record for a resold service with type, billing frequency, start/expiry months, and status.
- GUID: {20CE65DE-DEAA-4742-943A-B5F54DA938E0}
- Layer: Application

### DataObject — e-data-vendor
- Name: Vendor Record
- Description: Database record for a supplier organization with banking details and payment currency.
- GUID: {ED5DFFD8-4064-4C4F-BEEE-6B2FC4DCC3DF}
- Layer: Application

### Node — e-node-nas
- Name: QNAP NAS
- Description: The target deployment environment running the application locally.
- GUID: {87B0EDE5-B6F8-5D65-AFCF-3FF4C92C8CD2}
- Layer: Technology

### Device — e-device-nas
- Name: QNAP Hardware
- Description: Physical NAS hardware, Intel/ARM processor, running QNAP QTS/QuTS hero.
- GUID: {B1D03642-187F-57D8-AACF-7CA7D6C2AAFB}
- Layer: Technology

### SystemSoftware — e-sw-django
- Name: Django 6.x + Python 3.13
- Description: The web framework and runtime powering the CRM application.
- GUID: {00309B45-F55A-5372-9B7E-891D73D932A1}
- Layer: Technology

### SystemSoftware — e-sw-sqlite
- Name: SQLite
- Description: Embedded database engine, file-based, zero-configuration, ideal for NAS deployment.
- GUID: {33F1813D-51B7-52DB-B6F0-6981E7A0CE90}
- Layer: Technology

### SystemSoftware — e-sw-container
- Name: Docker (Container Station)
- Description: Container runtime on QNAP for deploying the application in Phase 3.
- GUID: {7274A594-0500-58FA-9B64-1D5041128195}
- Layer: Technology

### Artifact — e-art-dockerfile
- Name: Dockerfile
- Description: Container image definition for the EAxCRM Django application.
- GUID: {C15F3C3D-74DA-526B-AC69-FB4D3A50CD93}
- Layer: Technology

### Artifact — e-art-db
- Name: SQLite Database File
- Description: The file-based SQLite database storing all CRM data.
- GUID: {48E6E353-BD82-5D9D-8FB3-0AFF8CF07E18}
- Layer: Technology

## Relationships

### Association — r-cust-pri
- Source: e-customer
- Target: e-role-primary
- GUID: {90A18075-C6B3-5C6A-8136-D7AB2A4CB25C}

### Association — r-cust-pur
- Source: e-customer
- Target: e-role-purchase
- GUID: {3BA64862-788F-518C-B060-DC752985B89A}

### Association — r-cust-sal
- Source: e-customer
- Target: e-role-sales
- GUID: {DDC586ED-C401-5AED-AC80-5551C5F9CB1C}

### Association — r-cust-lic
- Source: e-customer
- Target: e-role-license
- GUID: {E658DE11-7324-56B5-9B8C-5DAA90B648CD}

### Composition — r-comp-insight-imap
- Source: e-func-insight
- Target: e-process-imap
- GUID: {3211E5CD-055C-5FFE-86D8-FA44B9B1B933}

### Composition — r-comp-insight-parse
- Source: e-func-insight
- Target: e-process-parse
- GUID: {3B6CC1AC-9856-5588-A25C-12D20C26C0D4}

### Composition — r-comp-newsletter-scrape
- Source: e-func-newsletter
- Target: e-process-scrape
- GUID: {56464A8A-2879-51CB-8181-D4147303B0E4}

### Composition — r-comp-newsletter-compose
- Source: e-func-newsletter
- Target: e-process-compose
- GUID: {407AEC21-3390-5C04-9BE1-609CD9361EFC}

### Composition — r-comp-newsletter-review
- Source: e-func-newsletter
- Target: e-process-review
- GUID: {8700C437-6020-5FC0-86D5-D2B230A6DE66}

### Composition — r-comp-newsletter-send
- Source: e-func-newsletter
- Target: e-process-send
- GUID: {EA546CF5-A36A-596C-9B0A-3493ECA526A7}

### Composition — r-comp-newsletter-optin
- Source: e-func-newsletter
- Target: e-process-optin
- GUID: {4AAD3CA0-733E-5706-BA4A-5A53C3D11E63}

### Access — r-access-imap-cust
- Source: e-process-imap
- Target: e-bo-customer
- GUID: {11B27096-0227-59B1-9437-4B21014ABD61}

### Access — r-access-imap-cont
- Source: e-process-imap
- Target: e-bo-contact
- GUID: {F4DD0541-D008-57D1-BF35-FF8EF3C422C6}

### Access — r-access-imap-comm
- Source: e-process-imap
- Target: e-bo-communication
- GUID: {F32C58F3-936F-5E20-8089-C5F892C2D7AA}

### Access — r-access-parse-doc
- Source: e-process-parse
- Target: e-bo-document
- GUID: {AE82C1F3-1BBE-5598-8137-2CA6784BB906}

### Access — r-access-parse-lic
- Source: e-process-parse
- Target: e-bo-license
- GUID: {0FA2A899-D273-5D72-9996-8D7913E5DE44}

### Access — r-access-parse-lli
- Source: e-process-parse
- Target: e-bo-lineitem
- GUID: {DA5CF7C4-5D8D-5717-BB12-6C7D341A70F6}

### Access — r-access-compose-news
- Source: e-process-compose
- Target: e-bo-newsletter
- GUID: {56C00A50-53AB-5C74-8356-9B180567E9AB}

### Access — r-access-send-news
- Source: e-process-send
- Target: e-bo-newsletter
- GUID: {DB4C7954-7ABB-5A87-B140-FE04406F0E8A}

### Assignment — r-assign-svc-customer
- Source: e-app-django
- Target: e-svc-customer
- GUID: {8A70BB0D-1B05-50D6-88AE-A309C5DA0309}

### Assignment — r-assign-svc-imap
- Source: e-app-django
- Target: e-svc-imap
- GUID: {0D5F48C8-1179-53CC-919E-FF5A3E8A0BD5}

### Assignment — r-assign-svc-parse
- Source: e-app-django
- Target: e-svc-parse
- GUID: {4B1777B6-C570-5961-B1B0-B59326D6C28C}

### Assignment — r-assign-svc-scrape
- Source: e-app-django
- Target: e-svc-scrape
- GUID: {A37F21EC-56C5-538D-977D-8D0F1D5F64D5}

### Assignment — r-assign-svc-newsletter
- Source: e-app-django
- Target: e-svc-newsletter
- GUID: {FCD1FDCE-41E9-5201-AF57-0623EEEE6568}

### Flow — r-flow-cust-data
- Source: e-svc-customer
- Target: e-data-customer
- GUID: {A1C10AAC-7A5E-5885-8E23-6B1402ADDDFC}

### Flow — r-flow-cont-data
- Source: e-svc-customer
- Target: e-data-contact
- GUID: {22B2E0F2-7B26-517F-9EA0-5F5C145D41F2}

### Flow — r-flow-imap-data
- Source: e-svc-imap
- Target: e-data-email
- GUID: {74F07D95-03A3-54A9-911E-F7C470C43CF9}

### Flow — r-flow-parse-data
- Source: e-svc-parse
- Target: e-data-attachment
- GUID: {2CA2AB5D-09B0-563D-B0B8-032D545F8C77}

### Flow — r-flow-scrape-data
- Source: e-svc-scrape
- Target: e-data-article
- GUID: {174A0F19-AC49-56E7-B3A8-854E1569CAD2}

### Flow — r-flow-newsletter-data
- Source: e-svc-newsletter
- Target: e-data-newsletter
- GUID: {BF308ED3-974C-57FC-93EA-DC6D0DDAB607}

### Flow — r-flow-parse-lic
- Source: e-svc-parse
- Target: e-data-license
- GUID: {4D57F7F0-60AB-54B8-BF3C-A66C75B33237}

### Flow — r-flow-parse-lli
- Source: e-svc-parse
- Target: e-data-lineitem
- GUID: {5CDCE6CB-59FB-53B6-9554-4982706CC7A2}

### Flow — r-flow-cust-purch
- Source: e-svc-customer
- Target: e-data-purchase
- GUID: {F13031A2-FAA8-55B7-B089-9C37E824CA9A}

### Realization — r-realize-svc-cust-imap
- Source: e-svc-customer
- Target: e-process-imap
- GUID: {F6FFCD39-ECAE-5848-B4C5-E48FC9F38254}

### Realization — r-realize-svc-imap-imap
- Source: e-svc-imap
- Target: e-process-imap
- GUID: {9D6C6F1A-B375-5069-B4F1-8925BD3CF3EF}

### Realization — r-realize-svc-parse-parse
- Source: e-svc-parse
- Target: e-process-parse
- GUID: {0B893712-3499-570C-AE30-7ACDCBC93D1F}

### Realization — r-realize-svc-scrape-scrape
- Source: e-svc-scrape
- Target: e-process-scrape
- GUID: {569ECA4D-9829-5BED-B54F-0937A5DA724C}

### Realization — r-realize-svc-news-compose
- Source: e-svc-newsletter
- Target: e-process-compose
- GUID: {AC4DEF2E-1FC1-5DFD-8548-8B40B22BCADF}

### Realization — r-realize-svc-news-review
- Source: e-svc-newsletter
- Target: e-process-review
- GUID: {BDA1E0F4-9CAC-5FB8-ADC6-F3E9BB669937}

### Realization — r-realize-svc-news-send
- Source: e-svc-newsletter
- Target: e-process-send
- GUID: {8DEF4B32-1D5A-5F3E-9551-D50A66E60F90}

### Realization — r-realize-svc-cust-optin
- Source: e-svc-customer
- Target: e-process-optin
- GUID: {A348126B-22A2-5298-AC8B-5C695032D2FF}

### Realization — r-realize-data-cust-bo
- Source: e-data-customer
- Target: e-bo-customer
- GUID: {14759541-66B7-5EBF-9ED0-610D6C2FB6B8}

### Realization — r-realize-data-contact-bo
- Source: e-data-contact
- Target: e-bo-contact
- GUID: {AC6B5903-0EA4-5F1E-A4BB-D342C8E53C1A}

### Realization — r-realize-data-email-bo
- Source: e-data-email
- Target: e-bo-communication
- GUID: {09B6C23A-7966-54D8-9208-CC34189280CD}

### Realization — r-realize-data-attach-bo
- Source: e-data-attachment
- Target: e-bo-document
- GUID: {65E6F3BC-4A87-521F-A33B-9C5B5C147E1B}

### Realization — r-realize-data-article-bo
- Source: e-data-article
- Target: e-bo-newsletter
- GUID: {02C30CB4-434F-578A-8F7C-F120D373CA0B}

### Realization — r-realize-data-newsletter-bo
- Source: e-data-newsletter
- Target: e-bo-newsletter
- GUID: {A88F4786-C41F-5B4A-B9F1-9FE3BD21DD85}

### Realization — r-realize-data-license-bo
- Source: e-data-license
- Target: e-bo-license
- GUID: {37712CDC-BCA0-5834-A269-87CC4C44C5FE}

### Realization — r-realize-data-lineitem-bo
- Source: e-data-lineitem
- Target: e-bo-lineitem
- GUID: {5B893313-1BCF-5C47-8872-41214367BBAB}

### Realization — r-realize-data-purchase-bo
- Source: e-data-purchase
- Target: e-bo-purchase
- GUID: {2E8423B7-0C51-5ED3-BF6D-0CC534CA1E00}

### Composition — r-comp-node-device
- Source: e-node-nas
- Target: e-device-nas
- GUID: {09B9D184-9A7C-5267-9E0B-076C84239874}

### Assignment — r-assign-sw-django
- Source: e-node-nas
- Target: e-sw-django
- GUID: {C295BFE6-243B-5A46-9B9A-AF2AA1D8B6CD}

### Assignment — r-assign-sw-sqlite
- Source: e-node-nas
- Target: e-sw-sqlite
- GUID: {C07C8120-B807-5B5C-A4F0-A5A12317E849}

### Assignment — r-assign-sw-container
- Source: e-node-nas
- Target: e-sw-container
- GUID: {D6AF62B1-2DB4-5AD8-81B9-6EE00B25036F}

### Realization — r-realize-sw-django-app
- Source: e-sw-django
- Target: e-app-django
- GUID: {7F40860B-C49D-569F-9EDA-7ED8D75A1AA3}

### Realization — r-realize-art-db-sw
- Source: e-art-db
- Target: e-sw-sqlite
- GUID: {1CCCA3BC-C3DA-59ED-B2DC-3C3010BB01DA}

### Realization — r-realize-art-docker-sw
- Source: e-art-dockerfile
- Target: e-sw-container
- GUID: {D8033287-7DC1-5A3C-823C-86825A100A73}

### Composition — r-comp-sales-rfq
- Source: e-func-sales
- Target: e-process-rfq
- GUID: {F0610CEC-F312-45D2-86C5-B3E74B189080}

### Composition — r-comp-sales-offer
- Source: e-func-sales
- Target: e-process-offer
- GUID: {E0CA4399-D2A4-4488-873D-2B8C418B33E9}

### Composition — r-comp-sales-procure
- Source: e-func-sales
- Target: e-process-procure
- GUID: {F9915566-31D6-4837-B66C-F03E0DDD0C4F}

### Composition — r-comp-sales-deliver
- Source: e-func-sales
- Target: e-process-deliver
- GUID: {F2969231-2BF3-4305-9DDF-C3FE40B53363}

### Composition — r-comp-sales-invoice
- Source: e-func-sales
- Target: e-process-invoice
- GUID: {3A018BD4-5BD5-478E-8B2A-7D13B456D34F}

### Access — r-access-rfq-quote
- Source: e-process-rfq
- Target: e-bo-quote
- GUID: {71A73B6E-D0F1-44C0-A159-AC60B4310883}

### Access — r-access-offer-offer
- Source: e-process-offer
- Target: e-bo-offer
- GUID: {3CA578FE-501B-4556-A938-49230CC25C89}

### Access — r-access-offer-service
- Source: e-process-offer
- Target: e-bo-service
- GUID: {5620769B-53CE-4F7A-BD4F-7015D0AB5813}

### Access — r-access-procure-quote
- Source: e-process-procure
- Target: e-bo-quote
- GUID: {1237BA52-893F-43D2-8998-79801CC3E134}

### Access — r-access-procure-vendor
- Source: e-process-procure
- Target: e-bo-vendor
- GUID: {3931A7E9-D9A6-42B3-BF36-157580DE2699}

### Access — r-access-deliver-delivery
- Source: e-process-deliver
- Target: e-bo-delivery
- GUID: {DB53B304-02CD-42BC-A486-7B3210C349B2}

### Access — r-access-invoice-salesinv
- Source: e-process-invoice
- Target: e-bo-salesinvoice
- GUID: {5BBD6F89-544E-44B0-9781-E60D6971B8B8}

### Access — r-access-invoice-procinv
- Source: e-process-invoice
- Target: e-bo-procurementinvoice
- GUID: {205609E0-1C38-4EDA-A15A-56AF942F9C7C}

### Access — r-access-invoice-purchase
- Source: e-process-invoice
- Target: e-bo-purchase
- GUID: {D52E9D33-3457-4C41-A389-8AEB68EE7940}

### Assignment — r-assign-svc-sales
- Source: e-app-django
- Target: e-svc-sales
- GUID: {3F885F37-B8E9-4935-8329-CB4B3D11885A}

### Flow — r-flow-sales-offer
- Source: e-svc-sales
- Target: e-data-offer
- GUID: {F0494600-CC7D-499E-A082-8F9C4A40D533}

### Flow — r-flow-sales-quote
- Source: e-svc-sales
- Target: e-data-quote
- GUID: {7ADC52DF-D3A7-480B-A26C-7755B5EE833D}

### Flow — r-flow-sales-delivery
- Source: e-svc-sales
- Target: e-data-delivery
- GUID: {0EB9C3C2-A695-40E9-B753-F1E1AC0ED08A}

### Flow — r-flow-sales-salesinv
- Source: e-svc-sales
- Target: e-data-salesinvoice
- GUID: {9CDA7399-C7E2-47B2-95E2-FDCA0212AF18}

### Flow — r-flow-sales-procinv
- Source: e-svc-sales
- Target: e-data-procurementinvoice
- GUID: {EAA0BBA3-6B31-43F5-9A6F-F67F8080B238}

### Flow — r-flow-sales-service
- Source: e-svc-sales
- Target: e-data-service
- GUID: {AEAFF6AB-C21B-4A20-9BE9-7CE42760AAA3}

### Flow — r-flow-sales-vendor
- Source: e-svc-sales
- Target: e-data-vendor
- GUID: {CD05EBCE-A3AD-4435-92F5-FCDF4271B566}

### Realization — r-realize-svc-rfq
- Source: e-svc-sales
- Target: e-process-rfq
- GUID: {21492691-ABF7-4F8C-AC50-11FA10D0C97B}

### Realization — r-realize-svc-offer
- Source: e-svc-sales
- Target: e-process-offer
- GUID: {BDB87E8E-F09C-4C57-824D-C1F0C1BB74D0}

### Realization — r-realize-svc-procure
- Source: e-svc-sales
- Target: e-process-procure
- GUID: {90E46CFD-A95C-4E89-9393-209CBC69F64A}

### Realization — r-realize-svc-deliver
- Source: e-svc-sales
- Target: e-process-deliver
- GUID: {0A155C80-66FB-43FE-8D38-6D6FA5B567F3}

### Realization — r-realize-svc-invoice
- Source: e-svc-sales
- Target: e-process-invoice
- GUID: {52697271-FC05-4C58-87A5-12950DD72261}

### Realization — r-realize-data-offer-bo
- Source: e-data-offer
- Target: e-bo-offer
- GUID: {4C9489C7-D9B1-4D30-A454-0670D89F602B}

### Realization — r-realize-data-quote-bo
- Source: e-data-quote
- Target: e-bo-quote
- GUID: {84228782-8D6E-4A43-8C05-45B29709F2E4}

### Realization — r-realize-data-delivery-bo
- Source: e-data-delivery
- Target: e-bo-delivery
- GUID: {CBDA9E65-B373-444A-8A48-E5841B65D014}

### Realization — r-realize-data-salesinv-bo
- Source: e-data-salesinvoice
- Target: e-bo-salesinvoice
- GUID: {76EB362E-0E4E-41B3-84C3-C7265C87D5EC}

### Realization — r-realize-data-procinv-bo
- Source: e-data-procurementinvoice
- Target: e-bo-procurementinvoice
- GUID: {2BA1D208-4FE2-4973-93DF-DA077D2FAAC4}

### Realization — r-realize-data-service-bo
- Source: e-data-service
- Target: e-bo-service
- GUID: {16C2808F-A17A-4225-BECB-7E7EEE7EEE76}

### Realization — r-realize-data-vendor-bo
- Source: e-data-vendor
- Target: e-bo-vendor
- GUID: {7D19D94F-D32D-4B36-B582-7F0B7164A279}
