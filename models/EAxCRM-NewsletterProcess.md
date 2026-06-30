# EAxCRM — Newsletter Process Architecture

**Model ID**: nlp-eacrm
**Purpose**: BPMN 2.0 newsletter process model for the EAxCRM system
**Version**: 1.0

## BPMN Collaboration—EAxCRMNewsletterProcessArchitecture
- Name: EAxCRM Newsletter Process Architecture
- GUID: {9488855B-5E6D-4910-877D-F4704A4D97D4}
- Is Closed: false
- Description: BPMN 2.0 collaboration model for the EAxCRM newsletter process, covering automated article scraping from news sources, manual newsletter composition, internal review workflow, and targeted distribution to opted-in contacts.

### Lane—EAxpertise
- Name: EAxpertise
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {F607A12D-DF35-4e94-B4D4-4685A6636134}
- Description: EAxpertise team managing the newsletter lifecycle from scheduling through review and distribution.

#### Gateway—6weekselapsed
  - Name: 6 weeks elapsed?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {0DFCA552-352D-461f-B5A1-CD426917926D}
  - Gateway Type: Exclusive
  - Description: Gateway checking if 6 weeks have elapsed since the last newsletter was sent.

#### DataObject—ApprovedNewsletter
  - Name: Approved Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {B2CC93C4-32BC-4f54-98D0-BE8EFA70B3E0}
  - Is Collection: false
  - Description: DataObject for the final reviewed and approved newsletter ready to send.

#### Activity—BrowseAvailableArticles
  - Name: Browse Available Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {2FDCB0FE-164B-4e4d-85C2-FA804FBEA7CD}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity to browse the article pool and identify suitable content for the newsletter.

#### Activity—CheckCadence
  - Name: Check Cadence
  - Type: Activity
  - Stereotype: Activity
  - GUID: {3218BB8A-2F73-4b89-9F0B-8CCECB306E0D}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity checking whether 6 weeks have elapsed since the last newsletter was sent, ensuring the target cadence is maintained.

#### Activity—ComposeNewsletter
  - Name: Compose Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {94905D88-3711-440a-8C43-69421780BEF8}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity to write and format the newsletter content using selected articles and the standard EAxNewsletter template (logo + article pointers).

#### DataObject—ContactList
  - Name: Contact List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {06DF44D0-7E1E-4175-93CF-68EE9428D156}
  - Is Collection: false
  - Description: DataObject storing the list of opted-in contacts to receive the newsletter.

#### DataObject—NewsletterDraft
  - Name: Newsletter Draft
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {D59C5A81-90BC-40b1-8EBA-C53B2108A33A}
  - Is Collection: false
  - Description: DataObject for the work-in-progress newsletter draft before submission.

#### EndEvent—NewsletterSent
  - Name: Newsletter Sent
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {BE7228CB-6384-4099-8E85-4A6EF2F9D093}
  - Description: EndEvent marking successful newsletter distribution to all recipients.

#### Gateway—ReviewApproved
  - Name: Review Approved?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {C7A531A7-161B-46e0-BCAA-37F3226973B6}
  - Gateway Type: Exclusive
  - Description: Gateway checking whether the newsletter review was approved or needs revision.

#### Activity—SelectArticles
  - Name: Select Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {09089596-99C5-4155-BBB3-1A2D5E8DD36C}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity to pick specific articles from the pool, typically 5 article pointers (heading + summary + link).

#### DataObject—SelectedArticles
  - Name: Selected Articles
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {3874679B-8E5C-4560-96AD-4C7974D93B2D}
  - Is Collection: false
  - Description: DataObject storing the curated selection of articles for the newsletter.

#### Activity—SendNewsletter
  - Name: Send Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {A124D465-171A-403d-94DA-3843285943B2}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity to dispatch the approved newsletter to all opted-in contacts via email.

#### DataObject—SentNewsletter
  - Name: Sent Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {BDC58A19-F164-4453-9C14-1B7CDD00018C}
  - Is Collection: false
  - Description: DataObject storing the archive of the sent newsletter for audit and reference.

#### StartEvent—StartNewsletter
  - Name: Start Newsletter
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {A2F3FEB2-4559-4a4b-ABC7-E7BCB4E23E2C}
  - Description: StartEvent triggering the newsletter composition process.

#### Activity—SubmitforReview
  - Name: Submit for Review
  - Type: Activity
  - Stereotype: Activity
  - GUID: {39581342-E38D-4ba7-ACB5-498A99416EEC}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity to submit the completed newsletter draft for internal review before sending.

### Lane—NewsSource
- Name: News Source
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {4989F926-0A9F-46a3-ABF1-2D7FFF4E31F2}
- Description: Automated news sources (SparxSystems.com, sparxsystems.eu) providing articles for the newsletter via scheduled scraping.

#### DataObject—ArticlePool
  - Name: Article Pool
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {D3C404A9-C323-4cfa-9029-42BF63A5B33B}
  - Is Collection: false
  - Description: DataObject storing all scraped article metadata (heading, summary, source URL) for selection.

#### Activity—ExtractHeadingsandSummaries
  - Name: Extract Headings and Summaries
  - Type: Activity
  - Stereotype: Activity
  - GUID: {3507D125-D007-4124-82D0-934D20FD422E}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity to parse scraped article content and extract headings and summaries for newsletter use.

#### Activity—FetchURLList
  - Name: Fetch URL List
  - Type: Activity
  - Stereotype: Activity
  - GUID: {8C0F5662-6269-4a57-AD6E-A7C20CE51414}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity to retrieve the configured list of news source URLs to scrape.

#### StartEvent—ScheduledScrape
  - Name: Scheduled Scrape
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {2E951233-9FA6-47fc-9545-B0B924229E9A}
  - Description: StartEvent triggering the automated scraping process on a scheduled basis.

#### Activity—ScrapeArticles
  - Name: Scrape Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {963DDAE6-6090-479f-B533-7BE3D9BA7446}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity to fetch article HTML content from news source URLs using requests and BeautifulSoup.

#### EndEvent—ScrapeComplete
  - Name: Scrape Complete
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {C6B4F238-4005-4950-B30F-387F059D03F9}
  - Description: EndEvent marking successful completion of the article scraping cycle.

#### Activity—StoreNewArticles
  - Name: Store New Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {4FE6A127-F6BB-468b-8439-569A21863021}
  - Completion Quantity: 1
  - Is Called Activity: false
  - Is For Compensation: false
  - Loop: None
  - Start Quantity: 1
  - Task Type: Abstract
  - Description: Activity to persist newly scraped articles to the database, avoiding duplicates.

#### DataObject—URLList
  - Name: URL List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {DF204F41-0D18-4abe-B0B8-780A2A9E7482}
  - Is Collection: false
  - Description: DataObject storing the configured list of news source URLs to scrape periodically.

### Sequence Flows

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

