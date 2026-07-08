# EAxCRM — Newsletter Process Architecture

**Model ID**: nlp-eacrm
**Purpose**: BPMN 2.0 newsletter process model for the EAxCRM system
**Version**: 1.0

## BPMN Collaboration—EAxCRMNewsletterProcessArchitecture
- Name: EAxCRM Newsletter Process Architecture
- GUID: {71833B05-38F3-41c7-9A4F-2085B324EDC1}
- Diagram Name: Newsletter Process Architecture
- Diagram GUID: {952FA72C-BBBB-40c5-A57B-F6E2A73510E8}
- Is Closed: false
- Description: BPMN 2.0 collaboration model for the EAxCRM newsletter process, covering automated article scraping from news sources, manual newsletter composition, internal review workflow, and targeted distribution to opted-in contacts.

### Lane—EAxpertise
- Name: EAxpertise
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {6973247D-950D-4573-8C1A-879FF6DEB761}
- Description: EAxpertise team managing the newsletter lifecycle from scheduling through review and distribution.

#### Gateway—6weekselapsed
  - Name: 6 weeks elapsed?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {F4EE9DB2-4FD2-4346-8335-CA820CDE4A10}
  - Gateway Type: Exclusive
  - Description: Gateway checking if 6 weeks have elapsed since the last newsletter was sent.

#### DataObject—ApprovedNewsletter
  - Name: Approved Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {FE488401-E4A4-46bb-94B1-E4A040E83D4B}
  - Data In/Out: None
  - Is Collection: false
  - Description: DataObject for the final reviewed and approved newsletter ready to send.

#### Activity—BrowseAvailableArticles
  - Name: Browse Available Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {455033B7-11F0-4402-BF53-3486C82FABF5}
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
  - GUID: {7631A5C3-E4F2-4187-8296-CBBC0E4A50C0}
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
  - GUID: {A42F3D07-163F-419d-875D-4990E66CCEB4}
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
  - GUID: {D9BC4C9F-7CFB-45a2-8583-0E76DD73A14F}
  - Data In/Out: Input
  - Is Collection: false
  - Description: DataObject storing the list of opted-in contacts to receive the newsletter.

#### DataObject—NewsletterDraft
  - Name: Newsletter Draft
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {13104C69-4C00-4b6a-9ADA-804BD2C19D5A}
  - Data In/Out: None
  - Is Collection: false
  - Description: DataObject for the work-in-progress newsletter draft before submission.

#### EndEvent—NewsletterSent
  - Name: Newsletter Sent
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {39C46955-C543-40b6-80DC-81D4BA479199}
  - Event Type: None
  - Description: EndEvent marking successful newsletter distribution to all recipients.

#### Gateway—ReviewApproved
  - Name: Review Approved?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {9B1679CC-5F72-4346-A707-517769F52CF7}
  - Gateway Type: Exclusive
  - Description: Gateway checking whether the newsletter review was approved or needs revision.

#### Activity—SelectArticles
  - Name: Select Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {2F3FCFF5-54A1-4e9c-A0C9-3657228F3D43}
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
  - GUID: {637A19F4-7220-40d0-847E-3848A0FEEEEB}
  - Data In/Out: None
  - Is Collection: false
  - Description: DataObject storing the curated selection of articles for the newsletter.

#### Activity—SendNewsletter
  - Name: Send Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {3F77A46D-C3EA-450e-872F-245A4462A82E}
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
  - GUID: {93163D6D-1C14-4f5b-96C1-BBF5772E41C6}
  - Data In/Out: Output
  - Is Collection: false
  - Description: DataObject storing the archive of the sent newsletter for audit and reference.

#### StartEvent—StartNewsletter
  - Name: Start Newsletter
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {0AA82059-B629-4ee7-A3D5-735F2B0057C7}
  - Event Type: None
  - Description: StartEvent triggering the newsletter composition process.

#### Activity—SubmitforReview
  - Name: Submit for Review
  - Type: Activity
  - Stereotype: Activity
  - GUID: {18B57B90-3035-4c52-865A-A5CFFAA0010A}
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
- GUID: {44320F6A-FEF0-4542-A842-998C0635269B}
- Description: Automated news sources (SparxSystems.com, sparxsystems.eu) providing articles for the newsletter via scheduled scraping.

#### DataObject—ArticlePool
  - Name: Article Pool
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {4607D2DC-C6CE-4c27-B0BC-CAA48E8CAD22}
  - Data In/Out: Output
  - Is Collection: false
  - Description: DataObject storing all scraped article metadata (heading, summary, source URL) for selection.

#### Activity—ExtractHeadingsandSummaries
  - Name: Extract Headings and Summaries
  - Type: Activity
  - Stereotype: Activity
  - GUID: {2824BEE2-F8F6-4180-8BA2-2A16FF9DD879}
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
  - GUID: {7BC27FA6-8291-4ee8-A7AC-798AA7569FC8}
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
  - GUID: {7760A66A-9FD9-4f45-BB6A-0C11AD23728C}
  - Event Type: None
  - Description: StartEvent triggering the automated scraping process on a scheduled basis.

#### Activity—ScrapeArticles
  - Name: Scrape Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {AA61373F-634E-43d0-AC90-504243D1C4A2}
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
  - GUID: {BD798C4C-6184-47ae-8D07-577B1628EC5F}
  - Event Type: None
  - Description: EndEvent marking successful completion of the article scraping cycle.

#### Activity—StoreNewArticles
  - Name: Store New Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {D8C742DC-A1ED-482f-BBFD-7CBC9114F78A}
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
  - GUID: {F87D2342-0B7D-4611-8FB0-2125288DFE8A}
  - Data In/Out: Input
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

