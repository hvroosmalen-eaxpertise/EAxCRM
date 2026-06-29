# EAxCRM — Newsletter Process Architecture

**Model ID**: nlp-eacrm
**Purpose**: BPMN 2.0 newsletter process model for the EAxCRM system
**Version**: 1.0

## BPMN Collaboration—eaxcrmnewsletterprocessarchitecture
- Name: EAxCRM Newsletter Process Architecture
- GUID: {A0D4932408ED4508B129AB88CABAE1ED}
- Diagram Name: Newsletter Process Architecture
- Diagram GUID: {C6997B1F338440E8A81F160870C77794}
- Description: BPMN 2.0 collaboration model for the EAxCRM newsletter process, covering automated article scraping from news sources, manual newsletter composition, internal review workflow, and targeted distribution to opted-in contacts.

### Lane—eaxpertise
- Name: EAxpertise
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {C875A38F0FAA4CD19024A410E59FB002}
- Description: EAxpertise team managing the newsletter lifecycle from scheduling through review and distribution.

#### Gateway—6weekselapsed
  - Name: 6 weeks elapsed?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {E7124704D63C4F2AAF840EE8CE786693}
  - Description: Gateway checking if 6 weeks have elapsed since the last newsletter was sent.

#### DataObject—approvednewsletter
  - Name: Approved Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {D0694C59AC994C988F5BFBC2CEBFF4A3}
  - Description: DataObject for the final reviewed and approved newsletter ready to send.

#### Activity—browseavailablearticles
  - Name: Browse Available Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {6BF5D6991C2A478EA879D611103A5D4F}
  - Description: Activity to browse the article pool and identify suitable content for the newsletter.

#### Activity—checkcadence
  - Name: Check Cadence
  - Type: Activity
  - Stereotype: Activity
  - GUID: {5C48164041EC48B38E96EC40A5802154}
  - Description: Activity checking whether 6 weeks have elapsed since the last newsletter was sent, ensuring the target cadence is maintained.

#### Activity—composenewsletter
  - Name: Compose Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {73F2021D08C14B6C9EFEC2124E11E404}
  - Description: Activity to write and format the newsletter content using selected articles and the standard EAxNewsletter template (logo + article pointers).

#### DataObject—contactlist
  - Name: Contact List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {2BBB354F111D4DFEBD78209CD8DD84EA}
  - Description: DataObject storing the list of opted-in contacts to receive the newsletter.

#### DataObject—newsletterdraft
  - Name: Newsletter Draft
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {E38200DF08FB47478A4A4544FC2DFFF7}
  - Description: DataObject for the work-in-progress newsletter draft before submission.

#### EndEvent—newslettersent
  - Name: Newsletter Sent
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {78F98D1BB5E346AB9CFB77DF7F8F14A6}
  - Description: EndEvent marking successful newsletter distribution to all recipients.

#### Gateway—reviewapproved
  - Name: Review Approved?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {A074F711D40D4158B296C69740497AB7}
  - Description: Gateway checking whether the newsletter review was approved or needs revision.

#### Activity—selectarticles
  - Name: Select Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {D006121385444A6FA3532CBB340321F4}
  - Description: Activity to pick specific articles from the pool, typically 5 article pointers (heading + summary + link).

#### DataObject—selectedarticles
  - Name: Selected Articles
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {2FFB047649E7473981BBC848F14547B7}
  - Description: DataObject storing the curated selection of articles for the newsletter.

#### Activity—sendnewsletter
  - Name: Send Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {8B193D60EF29400D922285E2B781B448}
  - Description: Activity to dispatch the approved newsletter to all opted-in contacts via email.

#### DataObject—sentnewsletter
  - Name: Sent Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {820A683D7DF84145B4F2FFD624F5113F}
  - Description: DataObject storing the archive of the sent newsletter for audit and reference.

#### StartEvent—startnewsletter
  - Name: Start Newsletter
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {E5D4E434C3D645A7AB9359A8D978AFAF}
  - Description: StartEvent triggering the newsletter composition process.

#### Activity—submitforreview
  - Name: Submit for Review
  - Type: Activity
  - Stereotype: Activity
  - GUID: {C6A33004B107420EAF9B76B052A7843D}
  - Description: Activity to submit the completed newsletter draft for internal review before sending.

### Lane—newssource
- Name: News Source
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {05BFE966C0944301927ACF4FC2FA8D0D}
- Description: Automated news sources (SparxSystems.com, sparxsystems.eu) providing articles for the newsletter via scheduled scraping.

#### DataObject—articlepool
  - Name: Article Pool
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {140FC6C3E72D47A28665922FB309C586}
  - Description: DataObject storing all scraped article metadata (heading, summary, source URL) for selection.

#### Activity—extractheadingsandsummaries
  - Name: Extract Headings and Summaries
  - Type: Activity
  - Stereotype: Activity
  - GUID: {54318CD9DAFA4FBBAD31880DD7920643}
  - Description: Activity to parse scraped article content and extract headings and summaries for newsletter use.

#### Activity—fetchurllist
  - Name: Fetch URL List
  - Type: Activity
  - Stereotype: Activity
  - GUID: {6F5FF5A9482A4D4D9BFA0CE7E4D2D444}
  - Description: Activity to retrieve the configured list of news source URLs to scrape.

#### StartEvent—scheduledscrape
  - Name: Scheduled Scrape
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {2A63CB6AAA1A4ACAA1406019E7B5B90B}
  - Description: StartEvent triggering the automated scraping process on a scheduled basis.

#### Activity—scrapearticles
  - Name: Scrape Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {8CE235AE5C4F4168982B86236B310803}
  - Description: Activity to fetch article HTML content from news source URLs using requests and BeautifulSoup.

#### EndEvent—scrapecomplete
  - Name: Scrape Complete
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {C6C890C8FB2E4F43B68D3453DEDD0508}
  - Description: EndEvent marking successful completion of the article scraping cycle.

#### Activity—storenewarticles
  - Name: Store New Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {19682013800C4A3F9B33D5768F51B0DF}
  - Description: Activity to persist newly scraped articles to the database, avoiding duplicates.

#### DataObject—urllist
  - Name: URL List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {DDF91DE3855C4F52A54473500E64DBA6}
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

