# EAxCRM — Process Architecture

**Model ID**: pa-eacrm
**Purpose**: BPMN 2.0 process model for the EAxCRM system
**Version**: 1.0

## BPMN Collaboration—eaxcrmnewsletterprocessarchitecture
- Name: EAxCRM Newsletter Process Architecture
- GUID: {493037E688D640EB93F0ABA9CD604A27}
- Diagram Name: Newsletter Process Architecture
- Diagram GUID: {B4C63BA59F4D4E15B64550BEAC936469}
- Description: BPMN 2.0 collaboration model for the EAxCRM newsletter process, covering automated article scraping from news sources, manual newsletter composition, internal review workflow, and targeted distribution to opted-in contacts.

### Lane—eaxpertise
- Name: EAxpertise
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {A9AA6847F0E040D791A3DE4AF1691F7A}
- Description: EAxpertise team managing the newsletter lifecycle from scheduling through review and distribution.

### Lane—newssource
- Name: News Source
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {EF5F8879F40340D7B0F24F3F626C161E}
- Description: Automated news sources (SparxSystems.com, sparxsystems.eu) providing articles for the newsletter via scheduled scraping.

### Gateway—6weekselapsed
- Name: 6 weeks elapsed?
- Type: Decision
- Stereotype: Gateway
- GUID: {DF4184869BB9446B91D2D483980E8C5E}
- Description: Gateway checking if 6 weeks have elapsed since the last newsletter was sent.

### DataObject—approvednewsletter
- Name: Approved Newsletter
- Type: Artifact
- Stereotype: DataObject
- GUID: {BFF99CE86F0E4E19976F716D462AA6CC}
- Description: DataObject for the final reviewed and approved newsletter ready to send.

### DataObject—articlepool
- Name: Article Pool
- Type: Artifact
- Stereotype: DataObject
- GUID: {4C989ABD027C4183BEC4748FF71A3383}
- Description: DataObject storing all scraped article metadata (heading, summary, source URL) for selection.

### Activity—browseavailablearticles
- Name: Browse Available Articles
- Type: Activity
- Stereotype: Activity
- GUID: {74650264C8CC48A39C70C25A659AD454}
- Description: Activity to browse the article pool and identify suitable content for the newsletter.

### Activity—checkcadence
- Name: Check Cadence
- Type: Activity
- Stereotype: Activity
- GUID: {77F028F9AB654487A85E1231B8A47238}
- Description: Activity checking whether 6 weeks have elapsed since the last newsletter was sent, ensuring the target cadence is maintained.

### Activity—composenewsletter
- Name: Compose Newsletter
- Type: Activity
- Stereotype: Activity
- GUID: {7187A777FB0142AFADB3139A9D430976}
- Description: Activity to write and format the newsletter content using selected articles and the standard EAxNewsletter template (logo + article pointers).

### DataObject—contactlist
- Name: Contact List
- Type: Artifact
- Stereotype: DataObject
- GUID: {11A5924B5BE54CBEB2D12F81973325CF}
- Description: DataObject storing the list of opted-in contacts to receive the newsletter.

### Activity—extractheadingsandsummaries
- Name: Extract Headings and Summaries
- Type: Activity
- Stereotype: Activity
- GUID: {B696E5D0BB194595A48AB9BAF7EA08D7}
- Description: Activity to parse scraped article content and extract headings and summaries for newsletter use.

### Activity—fetchurllist
- Name: Fetch URL List
- Type: Activity
- Stereotype: Activity
- GUID: {82813DB6227840AFBA62C2FA5407484A}
- Description: Activity to retrieve the configured list of news source URLs to scrape.

### DataObject—newsletterdraft
- Name: Newsletter Draft
- Type: Artifact
- Stereotype: DataObject
- GUID: {B83D2906B88F4FE68C52B8F9B91D6E19}
- Description: DataObject for the work-in-progress newsletter draft before submission.

### EndEvent—newslettersent
- Name: Newsletter Sent
- Type: Event
- Stereotype: EndEvent
- GUID: {495E1BB97EAC4A24B9952A88D0CD1FC9}
- Description: EndEvent marking successful newsletter distribution to all recipients.

### Gateway—reviewapproved
- Name: Review Approved?
- Type: Decision
- Stereotype: Gateway
- GUID: {B69F543B265F436EBFF8DA3AA4C14CBF}
- Description: Gateway checking whether the newsletter review was approved or needs revision.

### StartEvent—scheduledscrape
- Name: Scheduled Scrape
- Type: Event
- Stereotype: StartEvent
- GUID: {78CC3E5BFF7A45B3979FCB311D74141F}
- Description: StartEvent triggering the automated scraping process on a scheduled basis.

### Activity—scrapearticles
- Name: Scrape Articles
- Type: Activity
- Stereotype: Activity
- GUID: {7C704A3C623B4CF99CC701CBC58FB3D8}
- Description: Activity to fetch article HTML content from news source URLs using requests and BeautifulSoup.

### EndEvent—scrapecomplete
- Name: Scrape Complete
- Type: Event
- Stereotype: EndEvent
- GUID: {A7786B7223294AB9A1C710C50DB65128}
- Description: EndEvent marking successful completion of the article scraping cycle.

### Activity—selectarticles
- Name: Select Articles
- Type: Activity
- Stereotype: Activity
- GUID: {87D437B13D024169BC69B4DEEE00BDFC}
- Description: Activity to pick specific articles from the pool, typically 5 article pointers (heading + summary + link).

### DataObject—selectedarticles
- Name: Selected Articles
- Type: Artifact
- Stereotype: DataObject
- GUID: {3E0B3D007F314C7A9F0D819C1BB69B97}
- Description: DataObject storing the curated selection of articles for the newsletter.

### Activity—sendnewsletter
- Name: Send Newsletter
- Type: Activity
- Stereotype: Activity
- GUID: {10B37700801243C2A155A78322CCFCB7}
- Description: Activity to dispatch the approved newsletter to all opted-in contacts via email.

### DataObject—sentnewsletter
- Name: Sent Newsletter
- Type: Artifact
- Stereotype: DataObject
- GUID: {180D9BC621314D72960A461767AD7E32}
- Description: DataObject storing the archive of the sent newsletter for audit and reference.

### StartEvent—startnewsletter
- Name: Start Newsletter
- Type: Event
- Stereotype: StartEvent
- GUID: {FC9AAF21A9C6483A920FCD355F1FE53C}
- Description: StartEvent triggering the newsletter composition process.

### Activity—storenewarticles
- Name: Store New Articles
- Type: Activity
- Stereotype: Activity
- GUID: {15965C67230546C48D16CBFFD4DB6839}
- Description: Activity to persist newly scraped articles to the database, avoiding duplicates.

### Activity—submitforreview
- Name: Submit for Review
- Type: Activity
- Stereotype: Activity
- GUID: {EDC1DD7F5F3D42F8A006DAA3E91C1DE2}
- Description: Activity to submit the completed newsletter draft for internal review before sending.

### DataObject—urllist
- Name: URL List
- Type: Artifact
- Stereotype: DataObject
- GUID: {CEC76BB3E11A4C498936D895A48AA3E5}
- Description: DataObject storing the configured list of news source URLs to scrape periodically.

### CollaborationModel—eaxcrmsalesprocessarchitecture
- Name: EAxCRM Sales Process Architecture
- Type: Activity
- Stereotype: CollaborationModel
- GUID: {6ACCD057-B99E-48a4-8BE0-AC1FCC601245}
- Is Closed: false
- Description: BPMN 2.0 collaboration model covering the end-to-end sales process at EAxpertise, from customer RFQ through delivery and payment.

#### Lane—customer
  - Name: Customer
  - Type: ActivityPartition
  - Stereotype: Lane
  - GUID: {D78E6C97-1010-40da-8A34-28B2A84F29D6}
  - Description: The customer organization requesting quotes and purchasing Sparx EA licenses and services.

##### Activity—acceptdelivery
    - Name: Accept Delivery
    - Type: Activity
    - Stereotype: Activity
    - GUID: {863E019F-D8AA-4a29-AC98-9A5E9BC1DE9E}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Customer confirms receipt of license files and/or service access credentials.

##### Gateway—acceptoffer
    - Name: accept offer
    - Type: Decision
    - Stereotype: Gateway
    - GUID: {48A6D2C0-48A8-41c7-9B44-28B014D9A5E4}
    - Gateway Type: Exclusive
    - Description: Customer decision gateway: accept the offer or reject it (ends the process).

##### Activity—acceptoffer
    - Name: Accept Offer
    - Type: Activity
    - Stereotype: Activity
    - GUID: {AAF91171-3C57-46bb-B549-0BE31011BA78}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Customer formally accepts the offer, triggering the fulfillment phase.

##### Activity—activatedelivery
    - Name: Activate Delivery
    - Type: Activity
    - Stereotype: Activity
    - GUID: {F1FA7EC6-06B5-41cc-BAFC-1DCD1EDE3B27}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Customer activates the delivered licenses and services in their environment.

##### Activity—createrfq
    - Name: Create RFQ
    - Type: Activity
    - Stereotype: Activity
    - GUID: {8078EDB0-256C-4dd4-8810-573EAA0F0B0B}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Customer drafts and sends a Request For Quote detailing their license and service needs.

##### Activity—paysalesinvoice
    - Name: Pay SalesInvoice
    - Type: Activity
    - Stereotype: Activity
    - GUID: {4E4972A7-0D2D-4135-BA47-2B403D9B8309}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: Manual
    - Description: Customer pays the sales invoice via bank transfer.

##### DataObject—payment
    - Name: Payment
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {332D8643-81C6-4b64-A250-E8898028D48E}
    - Is Collection: false
    - Description: Payment record by Bank.

##### DataObject—purchaseorder
    - Name: Purchase Order
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {A9A7B62D-3F33-4b05-8239-DF34F4EF35FE}
    - Is Collection: false
    - Description: A Purchase order is the acceptance for the payment. It can come with a Customer Purchase Order code and information on invoicing.

##### Activity—rejectoffer
    - Name: Reject Offer
    - Type: Activity
    - Stereotype: Activity
    - GUID: {F443524E-4717-4e31-9D4D-D01A05B478B6}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Customer reject the Offer and decides not to go with Purchase.

##### Activity—requestrevisedoffer
    - Name: Request Revised Offer
    - Type: Activity
    - Stereotype: Activity
    - GUID: {A1BAB8A5-7D52-47e6-9E90-4440D5D6EE88}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Customer request a revised offer

##### Activity—reviewoffer
    - Name: Review Offer
    - Type: Activity
    - Stereotype: Activity
    - GUID: {997B9124-402C-42ee-9A11-03E89D90DF86}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Customer reviews the offer prepared by EAxpertise and decides whether to accept.

##### DataObject—rfq
    - Name: RFQ
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {76AD2E52-11A3-4657-8F06-F937D33F3C19}
    - Is Collection: false
    - Description: The Request For Quote document artifact exchanged between Customer and EAxpertise.

##### StartEvent—startrfq
    - Name: Start RFQ
    - Type: Event
    - Stereotype: StartEvent
    - GUID: {94A14FAC-00B9-43fc-B10E-9FABE868C74C}
    - Description: The customer initiates the process by submitting a request for a quote to EAxpertise.

#### Lane—eaxpertise
  - Name: EAxpertise
  - Type: ActivityPartition
  - Stereotype: Lane
  - GUID: {0D1DE3F6-9F36-4387-901D-5E82190C78A4}
  - Description: EAxpertise as the reseller — manages offers, licenses, services, and coordinates with vendors.

##### IntermediateEvent—checkpayment
    - Name: check payment
    - Type: Event
    - Stereotype: IntermediateEvent
    - GUID: {B6F6A5F0-31B9-4876-AB37-29EB93616701}
    - Description: Check if the sales invoice has been paid by the customer. Outcome determines next step.

##### Activity—determinelicenses
    - Name: Determine Licenses
    - Type: Activity
    - Stereotype: Activity
    - GUID: {F1B9706F-D357-48a3-BA36-4AAF2618F4A4}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Identify which Sparx EA license types and quantities the customer needs.

##### Activity—determineservices
    - Name: Determine Services
    - Type: Activity
    - Stereotype: Activity
    - GUID: {52A9A807-5186-4dcd-ABC4-2F48A42DC2E4}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Services can be resold from Vendor or provided by EAxpertise.

##### EndEvent—endrejectedsales
    - Name: End Rejected Sales
    - Type: Event
    - Stereotype: EndEvent
    - GUID: {32ADEDC2-2890-40b6-A489-51A28FA5AC67}
    - Description: The sales process terminates because the customer rejected the offer.

##### EndEvent—endsales
    - Name: End Sales
    - Type: Event
    - Stereotype: EndEvent
    - GUID: {AC4B3F30-5771-4426-8445-30325797259B}
    - Description: The sales process is complete — payment received and delivery activated.

##### Activity—finaliseversionofoffer
    - Name: Finalise Version of Offer
    - Type: Activity
    - Stereotype: Activity
    - GUID: {8C9B0572-1DB2-4bdd-9D33-D8A279C87BE0}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Consolidate license and service line items into the final offer document.

##### Activity—handleapprovedoffer
    - Name: Handle Approved Offer
    - Type: Activity
    - Stereotype: Activity
    - GUID: {01C496AC-DFE7-4ea9-B482-1E95EF851677}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Receive the accepted offer and initiate procurement of licenses and services.

##### Activity—handlerejectedoffer
    - Name: Handle Rejected Offer
    - Type: Activity
    - Stereotype: Activity
    - GUID: {CC8DB595-33FA-423a-A7BB-E2C32C478029}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Close the sales process.

##### DataObject—offer
    - Name: Offer
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {CB5267A2-D848-4021-A26E-DDB979177C3A}
    - Is Collection: false
    - Description: The sales proposal document sent to the customer, containing license and service line items with pricing.

##### Activity—preparerevisedoffer
    - Name: Prepare (Revised) Offer
    - Type: Activity
    - Stereotype: Activity
    - GUID: {9C3B3106-2A1F-46ef-818F-374EC58FC6FB}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: EAxpertise prepares a sales offer based on the customer's RFQ requirements.

##### Activity—preparedelivery
    - Name: Prepare Delivery
    - Type: Activity
    - Stereotype: Activity
    - GUID: {677F24EF-13D2-43bc-A2EF-241AC495066E}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Create the formal handover package and delivery note for the customer.

##### Activity—preparesalesinvoice
    - Name: Prepare SalesInvoice
    - Type: Activity
    - Stereotype: Activity
    - GUID: {6BA1904F-38DB-4de6-A6D7-4377B1C95D3F}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Generate the outgoing sales invoice based on the accepted offer.

##### Activity—registerrfq
    - Name: Register RFQ
    - Type: Activity
    - Stereotype: Activity
    - GUID: {1E8282D2-3F1C-41ce-B8A5-671AAD90ACFC}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Log the incoming RFQ into the CRM system and assign a reference number.

##### Activity—requestlicenses
    - Name: Request Licenses
    - Type: Activity
    - Stereotype: Activity
    - GUID: {FA528F49-DC3F-4b41-8377-D9D2457F83C9}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Send license purchase request to the Vendor with the agreed line items.

##### Activity—requestservices
    - Name: Request Services
    - Type: Activity
    - Stereotype: Activity
    - GUID: {3ACC3D25-DD6F-43d9-80BB-66BC6EC18134}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Send service order request to the Vendor with the agreed service details.

##### DataObject—salesinvoice
    - Name: Sales Invoice
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {E47CCCC5-9862-4bde-A10D-7AFE0D040DFA}
    - Is Collection: false
    - Description: Invoice sent to Customer.

##### Gateway—servicesrequired
    - Name: services required
    - Type: Decision
    - Stereotype: Gateway
    - GUID: {4DDEC500-6564-4478-BEF0-982F04F01488}
    - Gateway Type: Exclusive
    - Description: Check if the customer's RFQ includes service items beyond license procurement.

##### Activity—validatepayment
    - Name: Validate Payment
    - Type: Activity
    - Stereotype: Activity
    - GUID: {6BF00CC4-39CF-4db4-A20B-06D3A43AC93F}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: Manual
    - Description: Manually verify in the banking portal that the customer's transfer has arrived.

#### Lane—vendor
  - Name: Vendor
  - Type: ActivityPartition
  - Stereotype: Lane
  - GUID: {4CE7A835-2E5A-4392-ACA7-2A54C08DA636}
  - Description: The supplier (e.g. Sparx Systems, Prolaborate, Ability Engineering) providing license and service quotes.

##### DataObject—licensedocument
    - Name: License Document
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {B5EBA936-39BC-4694-858E-2474715E89E0}
    - Is Collection: false
    - Description: License registration files delivered by the vendor.

##### DataObject—licenseinvoice
    - Name: License Invoice
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {C206CCD5-D481-40b3-BA1C-18FFD705326E}
    - Is Collection: false
    - Description: Incoming invoice from the vendor for purchased licenses.

##### DataObject—licensequote
    - Name: License Quote
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {6C0747AF-BB4C-4885-BAF6-4FC496E23590}
    - Is Collection: false
    - Description: Pricing quote from the vendor for requested license line items.

##### Activity—preparelicensequote
    - Name: Prepare License Quote
    - Type: Activity
    - Stereotype: Activity
    - GUID: {9D0A23BA-1725-473a-9C0D-D9BDAD113492}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Vendor prepares a pricing quote for the requested license and service line items.

##### Activity—prepareservicequote
    - Name: Prepare Service Quote
    - Type: Activity
    - Stereotype: Activity
    - GUID: {2AFFF14D-B7CB-4200-843E-64C9993FD879}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Vendor provides Service pricing.

##### Activity—providelicenses
    - Name: Provide Licenses
    - Type: Activity
    - Stereotype: Activity
    - GUID: {656EB0F6-7CD3-403a-9FE7-B4CC7B29A86D}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Vendor delivers license files.

##### Activity—provideservices
    - Name: Provide Service(s)
    - Type: Activity
    - Stereotype: Activity
    - GUID: {85628578-F197-45fd-8942-CC0812EFEEEF}
    - Completion Quantity: 1
    - Is Called Activity: false
    - Is For Compensation: false
    - Loop: None
    - Start Quantity: 1
    - Task Type: User
    - Description: Vendor activates the contracted services (support portal, training slots, SaaS tenant) and provide service agreement.

##### DataObject—servicedocument
    - Name: Service Document
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {9651C011-400C-4d72-9689-35FC5CC0DF2D}
    - Is Collection: false
    - Description: Service agreement document delivered by the vendor.

##### DataObject—serviceinvoice
    - Name: Service Invoice
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {D47CACA8-4CFE-44f4-829E-E9C4785A8D99}
    - Is Collection: false
    - Description: Incoming invoice from the vendor for procured services.

##### DataObject—servicequote
    - Name: Service Quote
    - Type: Artifact
    - Stereotype: DataObject
    - GUID: {117B4799-A108-4e69-BCF6-6BCF203A4EEC}
    - Is Collection: false
    - Description: Pricing quote from the vendor for requested service line items.

## BPMN Collaboration—eaxcrmsalesprocessarchitecture
- Name: EAxCRM Sales Process Architecture
- GUID: {6ACCD057-B99E-48a4-8BE0-AC1FCC601245}
- Diagram Name: Sales Process Architecture
- Diagram GUID: {A8CAE468-7CBC-46c0-9DCE-C695E50C1F36}
- Is Closed: false
- Description: BPMN 2.0 collaboration model covering the end-to-end sales process at EAxpertise, from customer RFQ through delivery and payment.

### Lane—customer
- Name: Customer
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {D78E6C97-1010-40da-8A34-28B2A84F29D6}
- Description: The customer organization requesting quotes and purchasing Sparx EA licenses and services.

#### Activity—acceptdelivery
  - Name: Accept Delivery
  - Type: Activity
  - Stereotype: Activity
  - GUID: {863E019F-D8AA-4a29-AC98-9A5E9BC1DE9E}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Customer confirms receipt of license files and/or service access credentials.

#### Gateway—acceptoffer
  - Name: accept offer
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {48A6D2C0-48A8-41c7-9B44-28B014D9A5E4}
  - Gateway Type: Exclusive
  - Description: Customer decision gateway: accept the offer or reject it (ends the process).

#### Activity—acceptoffer
  - Name: Accept Offer
  - Type: Activity
  - Stereotype: Activity
  - GUID: {AAF91171-3C57-46bb-B549-0BE31011BA78}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Customer formally accepts the offer, triggering the fulfillment phase.

#### Activity—activatedelivery
  - Name: Activate Delivery
  - Type: Activity
  - Stereotype: Activity
  - GUID: {F1FA7EC6-06B5-41cc-BAFC-1DCD1EDE3B27}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Customer activates the delivered licenses and services in their environment.

#### Activity—createrfq
  - Name: Create RFQ
  - Type: Activity
  - Stereotype: Activity
  - GUID: {8078EDB0-256C-4dd4-8810-573EAA0F0B0B}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Customer drafts and sends a Request For Quote detailing their license and service needs.

#### Activity—paysalesinvoice
  - Name: Pay SalesInvoice
  - Type: Activity
  - Stereotype: Activity
  - GUID: {4E4972A7-0D2D-4135-BA47-2B403D9B8309}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Manual
  - Description: Customer pays the sales invoice via bank transfer.

#### DataObject—payment
  - Name: Payment
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {332D8643-81C6-4b64-A250-E8898028D48E}
  - Is Collection: false
  - Description: Payment record by Bank.

#### DataObject—purchaseorder
  - Name: Purchase Order
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {A9A7B62D-3F33-4b05-8239-DF34F4EF35FE}
  - Is Collection: false
  - Description: A Purchase order is the acceptance for the payment. It can come with a Customer Purchase Order code and information on invoicing.

#### Activity—rejectoffer
  - Name: Reject Offer
  - Type: Activity
  - Stereotype: Activity
  - GUID: {F443524E-4717-4e31-9D4D-D01A05B478B6}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Customer reject the Offer and decides not to go with Purchase.

#### Activity—requestrevisedoffer
  - Name: Request Revised Offer
  - Type: Activity
  - Stereotype: Activity
  - GUID: {A1BAB8A5-7D52-47e6-9E90-4440D5D6EE88}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Customer request a revised offer

#### Activity—reviewoffer
  - Name: Review Offer
  - Type: Activity
  - Stereotype: Activity
  - GUID: {997B9124-402C-42ee-9A11-03E89D90DF86}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Customer reviews the offer prepared by EAxpertise and decides whether to accept.

#### DataObject—rfq
  - Name: RFQ
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {76AD2E52-11A3-4657-8F06-F937D33F3C19}
  - Is Collection: false
  - Description: The Request For Quote document artifact exchanged between Customer and EAxpertise.

#### StartEvent—startrfq
  - Name: Start RFQ
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {94A14FAC-00B9-43fc-B10E-9FABE868C74C}
  - Description: The customer initiates the process by submitting a request for a quote to EAxpertise.

### Lane—eaxpertise
- Name: EAxpertise
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {0D1DE3F6-9F36-4387-901D-5E82190C78A4}
- Description: EAxpertise as the reseller — manages offers, licenses, services, and coordinates with vendors.

#### IntermediateEvent—checkpayment
  - Name: check payment
  - Type: Event
  - Stereotype: IntermediateEvent
  - GUID: {B6F6A5F0-31B9-4876-AB37-29EB93616701}
  - Description: Check if the sales invoice has been paid by the customer. Outcome determines next step.

#### Activity—determinelicenses
  - Name: Determine Licenses
  - Type: Activity
  - Stereotype: Activity
  - GUID: {F1B9706F-D357-48a3-BA36-4AAF2618F4A4}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Identify which Sparx EA license types and quantities the customer needs.

#### Activity—determineservices
  - Name: Determine Services
  - Type: Activity
  - Stereotype: Activity
  - GUID: {52A9A807-5186-4dcd-ABC4-2F48A42DC2E4}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Services can be resold from Vendor or provided by EAxpertise.

#### EndEvent—endrejectedsales
  - Name: End Rejected Sales
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {32ADEDC2-2890-40b6-A489-51A28FA5AC67}
  - Description: The sales process terminates because the customer rejected the offer.

#### EndEvent—endsales
  - Name: End Sales
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {AC4B3F30-5771-4426-8445-30325797259B}
  - Description: The sales process is complete — payment received and delivery activated.

#### Activity—finaliseversionofoffer
  - Name: Finalise Version of Offer
  - Type: Activity
  - Stereotype: Activity
  - GUID: {8C9B0572-1DB2-4bdd-9D33-D8A279C87BE0}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Consolidate license and service line items into the final offer document.

#### Activity—handleapprovedoffer
  - Name: Handle Approved Offer
  - Type: Activity
  - Stereotype: Activity
  - GUID: {01C496AC-DFE7-4ea9-B482-1E95EF851677}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Receive the accepted offer and initiate procurement of licenses and services.

#### Activity—handlerejectedoffer
  - Name: Handle Rejected Offer
  - Type: Activity
  - Stereotype: Activity
  - GUID: {CC8DB595-33FA-423a-A7BB-E2C32C478029}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Close the sales process.

#### DataObject—offer
  - Name: Offer
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {CB5267A2-D848-4021-A26E-DDB979177C3A}
  - Is Collection: false
  - Description: The sales proposal document sent to the customer, containing license and service line items with pricing.

#### Activity—preparerevisedoffer
  - Name: Prepare (Revised) Offer
  - Type: Activity
  - Stereotype: Activity
  - GUID: {9C3B3106-2A1F-46ef-818F-374EC58FC6FB}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: EAxpertise prepares a sales offer based on the customer's RFQ requirements.

#### Activity—preparedelivery
  - Name: Prepare Delivery
  - Type: Activity
  - Stereotype: Activity
  - GUID: {677F24EF-13D2-43bc-A2EF-241AC495066E}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Create the formal handover package and delivery note for the customer.

#### Activity—preparesalesinvoice
  - Name: Prepare SalesInvoice
  - Type: Activity
  - Stereotype: Activity
  - GUID: {6BA1904F-38DB-4de6-A6D7-4377B1C95D3F}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Generate the outgoing sales invoice based on the accepted offer.

#### Activity—registerrfq
  - Name: Register RFQ
  - Type: Activity
  - Stereotype: Activity
  - GUID: {1E8282D2-3F1C-41ce-B8A5-671AAD90ACFC}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Log the incoming RFQ into the CRM system and assign a reference number.

#### Activity—requestlicenses
  - Name: Request Licenses
  - Type: Activity
  - Stereotype: Activity
  - GUID: {FA528F49-DC3F-4b41-8377-D9D2457F83C9}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Send license purchase request to the Vendor with the agreed line items.

#### Activity—requestservices
  - Name: Request Services
  - Type: Activity
  - Stereotype: Activity
  - GUID: {3ACC3D25-DD6F-43d9-80BB-66BC6EC18134}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Send service order request to the Vendor with the agreed service details.

#### DataObject—salesinvoice
  - Name: Sales Invoice
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {E47CCCC5-9862-4bde-A10D-7AFE0D040DFA}
  - Is Collection: false
  - Description: Invoice sent to Customer.

#### Gateway—servicesrequired
  - Name: services required
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {4DDEC500-6564-4478-BEF0-982F04F01488}
  - Gateway Type: Exclusive
  - Description: Check if the customer's RFQ includes service items beyond license procurement.

#### Activity—validatepayment
  - Name: Validate Payment
  - Type: Activity
  - Stereotype: Activity
  - GUID: {6BF00CC4-39CF-4db4-A20B-06D3A43AC93F}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Manual
  - Description: Manually verify in the banking portal that the customer's transfer has arrived.

### Lane—vendor
- Name: Vendor
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {4CE7A835-2E5A-4392-ACA7-2A54C08DA636}
- Description: The supplier (e.g. Sparx Systems, Prolaborate, Ability Engineering) providing license and service quotes.

#### DataObject—licensedocument
  - Name: License Document
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {B5EBA936-39BC-4694-858E-2474715E89E0}
  - Is Collection: false
  - Description: License registration files delivered by the vendor.

#### DataObject—licenseinvoice
  - Name: License Invoice
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {C206CCD5-D481-40b3-BA1C-18FFD705326E}
  - Is Collection: false
  - Description: Incoming invoice from the vendor for purchased licenses.

#### DataObject—licensequote
  - Name: License Quote
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {6C0747AF-BB4C-4885-BAF6-4FC496E23590}
  - Is Collection: false
  - Description: Pricing quote from the vendor for requested license line items.

#### Activity—preparelicensequote
  - Name: Prepare License Quote
  - Type: Activity
  - Stereotype: Activity
  - GUID: {9D0A23BA-1725-473a-9C0D-D9BDAD113492}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Vendor prepares a pricing quote for the requested license and service line items.

#### Activity—prepareservicequote
  - Name: Prepare Service Quote
  - Type: Activity
  - Stereotype: Activity
  - GUID: {2AFFF14D-B7CB-4200-843E-64C9993FD879}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Vendor provides Service pricing.

#### Activity—providelicenses
  - Name: Provide Licenses
  - Type: Activity
  - Stereotype: Activity
  - GUID: {656EB0F6-7CD3-403a-9FE7-B4CC7B29A86D}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Vendor delivers license files.

#### Activity—provideservices
  - Name: Provide Service(s)
  - Type: Activity
  - Stereotype: Activity
  - GUID: {85628578-F197-45fd-8942-CC0812EFEEEF}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: User
  - Description: Vendor activates the contracted services (support portal, training slots, SaaS tenant) and provide service agreement.

#### DataObject—servicedocument
  - Name: Service Document
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {9651C011-400C-4d72-9689-35FC5CC0DF2D}
  - Is Collection: false
  - Description: Service agreement document delivered by the vendor.

#### DataObject—serviceinvoice
  - Name: Service Invoice
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {D47CACA8-4CFE-44f4-829E-E9C4785A8D99}
  - Is Collection: false
  - Description: Incoming invoice from the vendor for procured services.

#### DataObject—servicequote
  - Name: Service Quote
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {117B4799-A108-4e69-BCF6-6BCF203A4EEC}
  - Is Collection: false
  - Description: Pricing quote from the vendor for requested service line items.

### CollaborationModel—eaxcrmnewsletterprocessarchitecture
- Name: EAxCRM Newsletter Process Architecture
- Type: Activity
- Stereotype: CollaborationModel
- GUID: {493037E688D640EB93F0ABA9CD604A27}
- Description: BPMN 2.0 collaboration model for the EAxCRM newsletter process, covering automated article scraping from news sources, manual newsletter composition, internal review workflow, and targeted distribution to opted-in contacts.

#### Gateway—6weekselapsed
  - Name: 6 weeks elapsed?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {DF4184869BB9446B91D2D483980E8C5E}
  - Description: Gateway checking if 6 weeks have elapsed since the last newsletter was sent.

#### DataObject—approvednewsletter
  - Name: Approved Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {BFF99CE86F0E4E19976F716D462AA6CC}
  - Description: DataObject for the final reviewed and approved newsletter ready to send.

#### DataObject—articlepool
  - Name: Article Pool
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {4C989ABD027C4183BEC4748FF71A3383}
  - Description: DataObject storing all scraped article metadata (heading, summary, source URL) for selection.

#### Activity—browseavailablearticles
  - Name: Browse Available Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {74650264C8CC48A39C70C25A659AD454}
  - Description: Activity to browse the article pool and identify suitable content for the newsletter.

#### Activity—checkcadence
  - Name: Check Cadence
  - Type: Activity
  - Stereotype: Activity
  - GUID: {77F028F9AB654487A85E1231B8A47238}
  - Description: Activity checking whether 6 weeks have elapsed since the last newsletter was sent, ensuring the target cadence is maintained.

#### Activity—composenewsletter
  - Name: Compose Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {7187A777FB0142AFADB3139A9D430976}
  - Description: Activity to write and format the newsletter content using selected articles and the standard EAxNewsletter template (logo + article pointers).

#### DataObject—contactlist
  - Name: Contact List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {11A5924B5BE54CBEB2D12F81973325CF}
  - Description: DataObject storing the list of opted-in contacts to receive the newsletter.

#### Lane—eaxpertise
  - Name: EAxpertise
  - Type: ActivityPartition
  - Stereotype: Lane
  - GUID: {A9AA6847F0E040D791A3DE4AF1691F7A}
  - Description: EAxpertise team managing the newsletter lifecycle from scheduling through review and distribution.

#### Activity—extractheadingsandsummaries
  - Name: Extract Headings and Summaries
  - Type: Activity
  - Stereotype: Activity
  - GUID: {B696E5D0BB194595A48AB9BAF7EA08D7}
  - Description: Activity to parse scraped article content and extract headings and summaries for newsletter use.

#### Activity—fetchurllist
  - Name: Fetch URL List
  - Type: Activity
  - Stereotype: Activity
  - GUID: {82813DB6227840AFBA62C2FA5407484A}
  - Description: Activity to retrieve the configured list of news source URLs to scrape.

#### Lane—newssource
  - Name: News Source
  - Type: ActivityPartition
  - Stereotype: Lane
  - GUID: {EF5F8879F40340D7B0F24F3F626C161E}
  - Description: Automated news sources (SparxSystems.com, sparxsystems.eu) providing articles for the newsletter via scheduled scraping.

#### DataObject—newsletterdraft
  - Name: Newsletter Draft
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {B83D2906B88F4FE68C52B8F9B91D6E19}
  - Description: DataObject for the work-in-progress newsletter draft before submission.

#### EndEvent—newslettersent
  - Name: Newsletter Sent
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {495E1BB97EAC4A24B9952A88D0CD1FC9}
  - Description: EndEvent marking successful newsletter distribution to all recipients.

#### Gateway—reviewapproved
  - Name: Review Approved?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {B69F543B265F436EBFF8DA3AA4C14CBF}
  - Description: Gateway checking whether the newsletter review was approved or needs revision.

#### StartEvent—scheduledscrape
  - Name: Scheduled Scrape
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {78CC3E5BFF7A45B3979FCB311D74141F}
  - Description: StartEvent triggering the automated scraping process on a scheduled basis.

#### Activity—scrapearticles
  - Name: Scrape Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {7C704A3C623B4CF99CC701CBC58FB3D8}
  - Description: Activity to fetch article HTML content from news source URLs using requests and BeautifulSoup.

#### EndEvent—scrapecomplete
  - Name: Scrape Complete
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {A7786B7223294AB9A1C710C50DB65128}
  - Description: EndEvent marking successful completion of the article scraping cycle.

#### Activity—selectarticles
  - Name: Select Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {87D437B13D024169BC69B4DEEE00BDFC}
  - Description: Activity to pick specific articles from the pool, typically 5 article pointers (heading + summary + link).

#### DataObject—selectedarticles
  - Name: Selected Articles
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {3E0B3D007F314C7A9F0D819C1BB69B97}
  - Description: DataObject storing the curated selection of articles for the newsletter.

#### Activity—sendnewsletter
  - Name: Send Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {10B37700801243C2A155A78322CCFCB7}
  - Description: Activity to dispatch the approved newsletter to all opted-in contacts via email.

#### DataObject—sentnewsletter
  - Name: Sent Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {180D9BC621314D72960A461767AD7E32}
  - Description: DataObject storing the archive of the sent newsletter for audit and reference.

#### StartEvent—startnewsletter
  - Name: Start Newsletter
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {FC9AAF21A9C6483A920FCD355F1FE53C}
  - Description: StartEvent triggering the newsletter composition process.

#### Activity—storenewarticles
  - Name: Store New Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {15965C67230546C48D16CBFFD4DB6839}
  - Description: Activity to persist newly scraped articles to the database, avoiding duplicates.

#### Activity—submitforreview
  - Name: Submit for Review
  - Type: Activity
  - Stereotype: Activity
  - GUID: {EDC1DD7F5F3D42F8A006DAA3E91C1DE2}
  - Description: Activity to submit the completed newsletter draft for internal review before sending.

#### DataObject—urllist
  - Name: URL List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {CEC76BB3E11A4C498936D895A48AA3E5}
  - Description: DataObject storing the configured list of news source URLs to scrape periodically.

### Sequence Flows

- Start RFQ → Create RFQ
- Create RFQ → Register RFQ [email]
- Register RFQ → Prepare (Revised) Offer
- Prepare (Revised) Offer → Determine Licenses
- Determine Licenses → Prepare License Quote [email license request]
- Prepare License Quote → Determine Licenses [email license pricing]
- Determine Licenses → services required
- services required → Determine Services [yes]
- Determine Services → Finalise Version of Offer
- services required → Finalise Version of Offer [no]
- Review Offer → accept offer
- Finalise Version of Offer → Review Offer [email offer]
- accept offer → Accept Offer [yes]
- Handle Approved Offer → Request Licenses
- Handle Approved Offer → Request Services
- Accept Offer → Handle Approved Offer [email acceptance and invoice details]
- Request Licenses → Provide Licenses [license quote acceptance]
- Request Services → Provide Service(s) [service quote acceptance]
- Request Licenses → Prepare Delivery
- Request Services → Prepare Delivery
- Prepare Delivery → Accept Delivery
- Provide Service(s) → Prepare Delivery
- Provide Licenses → Prepare Delivery
- Accept Delivery → Activate Delivery
- Activate Delivery → Prepare SalesInvoice [delivery activated]
- Prepare SalesInvoice → Pay SalesInvoice
- Pay SalesInvoice → Validate Payment
- Validate Payment → check payment
- check payment → End Sales [received]
- check payment → Pay SalesInvoice [payment not received]
- Determine Services → Prepare Service Quote [email service request]
- Prepare Service Quote → Determine Services [email service pricing]
- accept offer → Request Revised Offer [partial acceptance]
- accept offer → Reject Offer [no]
- Request Revised Offer → Prepare (Revised) Offer
- Handle Rejected Offer → End Rejected Sales
- Reject Offer → Handle Rejected Offer
- Start Newsletter → Check Cadence
- Check Cadence → 6 weeks elapsed?
- 6 weeks elapsed? → Browse Available Articles [yes]
- 6 weeks elapsed? → Newsletter Sent [no]
- Browse Available Articles → Select Articles
- Select Articles → Compose Newsletter
- Compose Newsletter → Submit for Review
- Submit for Review → Review Approved?
- Review Approved? → Send Newsletter [yes]
- Review Approved? → Compose Newsletter [no]
- Send Newsletter → Newsletter Sent
- Scheduled Scrape → Fetch URL List
- Fetch URL List → Scrape Articles
- Scrape Articles → Extract Headings and Summaries
- Extract Headings and Summaries → Store New Articles
- Store New Articles → Scrape Complete
- Start Newsletter → Check Cadence
- Check Cadence → 6 weeks elapsed?
- 6 weeks elapsed? → Browse Available Articles [yes]
- 6 weeks elapsed? → Newsletter Sent [no]
- Browse Available Articles → Select Articles
- Select Articles → Compose Newsletter
- Compose Newsletter → Submit for Review
- Submit for Review → Review Approved?
- Review Approved? → Send Newsletter [yes]
- Review Approved? → Compose Newsletter [no]
- Send Newsletter → Newsletter Sent
- Scheduled Scrape → Fetch URL List
- Fetch URL List → Scrape Articles
- Scrape Articles → Extract Headings and Summaries
- Extract Headings and Summaries → Store New Articles
- Store New Articles → Scrape Complete

