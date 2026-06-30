# EAxCRM — Newsletter Process Architecture

**Model ID**: nlp-eacrm
**Purpose**: BPMN 2.0 newsletter process model for the EAxCRM system
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
- Lane: eaxpertise
- Description: Gateway checking if 6 weeks have elapsed since the last newsletter was sent.

### DataObject—approvednewsletter
- Name: Approved Newsletter
- Type: Artifact
- Stereotype: DataObject
- GUID: {BFF99CE86F0E4E19976F716D462AA6CC}
- Lane: eaxpertise
- Description: DataObject for the final reviewed and approved newsletter ready to send.

### DataObject—articlepool
- Name: Article Pool
- Type: Artifact
- Stereotype: DataObject
- GUID: {4C989ABD027C4183BEC4748FF71A3383}
- Lane: newssource
- Description: DataObject storing all scraped article metadata (heading, summary, source URL) for selection.

### Activity—browseavailablearticles
- Name: Browse Available Articles
- Type: Activity
- Stereotype: Activity
- GUID: {74650264C8CC48A39C70C25A659AD454}
- Lane: eaxpertise
- Description: Activity to browse the article pool and identify suitable content for the newsletter.

### Activity—checkcadence
- Name: Check Cadence
- Type: Activity
- Stereotype: Activity
- GUID: {77F028F9AB654487A85E1231B8A47238}
- Lane: eaxpertise
- Description: Activity checking whether 6 weeks have elapsed since the last newsletter was sent, ensuring the target cadence is maintained.

### Activity—composenewsletter
- Name: Compose Newsletter
- Type: Activity
- Stereotype: Activity
- GUID: {7187A777FB0142AFADB3139A9D430976}
- Lane: eaxpertise
- Description: Activity to write and format the newsletter content using selected articles and the standard EAxNewsletter template (logo + article pointers).

### DataObject—contactlist
- Name: Contact List
- Type: Artifact
- Stereotype: DataObject
- GUID: {11A5924B5BE54CBEB2D12F81973325CF}
- Lane: eaxpertise
- Description: DataObject storing the list of opted-in contacts to receive the newsletter.

### Activity—extractheadingsandsummaries
- Name: Extract Headings and Summaries
- Type: Activity
- Stereotype: Activity
- GUID: {B696E5D0BB194595A48AB9BAF7EA08D7}
- Lane: newssource
- Description: Activity to parse scraped article content and extract headings and summaries for newsletter use.

### Activity—fetchurllist
- Name: Fetch URL List
- Type: Activity
- Stereotype: Activity
- GUID: {82813DB6227840AFBA62C2FA5407484A}
- Lane: newssource
- Description: Activity to retrieve the configured list of news source URLs to scrape.

### DataObject—newsletterdraft
- Name: Newsletter Draft
- Type: Artifact
- Stereotype: DataObject
- GUID: {B83D2906B88F4FE68C52B8F9B91D6E19}
- Lane: eaxpertise
- Description: DataObject for the work-in-progress newsletter draft before submission.

### EndEvent—newslettersent
- Name: Newsletter Sent
- Type: Event
- Stereotype: EndEvent
- GUID: {495E1BB97EAC4A24B9952A88D0CD1FC9}
- Lane: eaxpertise
- Description: EndEvent marking successful newsletter distribution to all recipients.

### Gateway—reviewapproved
- Name: Review Approved?
- Type: Decision
- Stereotype: Gateway
- GUID: {B69F543B265F436EBFF8DA3AA4C14CBF}
- Lane: eaxpertise
- Description: Gateway checking whether the newsletter review was approved or needs revision.

### StartEvent—scheduledscrape
- Name: Scheduled Scrape
- Type: Event
- Stereotype: StartEvent
- GUID: {78CC3E5BFF7A45B3979FCB311D74141F}
- Lane: newssource
- Description: StartEvent triggering the automated scraping process on a scheduled basis.

### Activity—scrapearticles
- Name: Scrape Articles
- Type: Activity
- Stereotype: Activity
- GUID: {7C704A3C623B4CF99CC701CBC58FB3D8}
- Lane: newssource
- Description: Activity to fetch article HTML content from news source URLs using requests and BeautifulSoup.

### EndEvent—scrapecomplete
- Name: Scrape Complete
- Type: Event
- Stereotype: EndEvent
- GUID: {A7786B7223294AB9A1C710C50DB65128}
- Lane: newssource
- Description: EndEvent marking successful completion of the article scraping cycle.

### Activity—selectarticles
- Name: Select Articles
- Type: Activity
- Stereotype: Activity
- GUID: {87D437B13D024169BC69B4DEEE00BDFC}
- Lane: eaxpertise
- Description: Activity to pick specific articles from the pool, typically 5 article pointers (heading + summary + link).

### DataObject—selectedarticles
- Name: Selected Articles
- Type: Artifact
- Stereotype: DataObject
- GUID: {3E0B3D007F314C7A9F0D819C1BB69B97}
- Lane: eaxpertise
- Description: DataObject storing the curated selection of articles for the newsletter.

### Activity—sendnewsletter
- Name: Send Newsletter
- Type: Activity
- Stereotype: Activity
- GUID: {10B37700801243C2A155A78322CCFCB7}
- Lane: eaxpertise
- Description: Activity to dispatch the approved newsletter to all opted-in contacts via email.

### DataObject—sentnewsletter
- Name: Sent Newsletter
- Type: Artifact
- Stereotype: DataObject
- GUID: {180D9BC621314D72960A461767AD7E32}
- Lane: eaxpertise
- Description: DataObject storing the archive of the sent newsletter for audit and reference.

### StartEvent—startnewsletter
- Name: Start Newsletter
- Type: Event
- Stereotype: StartEvent
- GUID: {FC9AAF21A9C6483A920FCD355F1FE53C}
- Lane: eaxpertise
- Description: StartEvent triggering the newsletter composition process.

### Activity—storenewarticles
- Name: Store New Articles
- Type: Activity
- Stereotype: Activity
- GUID: {15965C67230546C48D16CBFFD4DB6839}
- Lane: newssource
- Description: Activity to persist newly scraped articles to the database, avoiding duplicates.

### Activity—submitforreview
- Name: Submit for Review
- Type: Activity
- Stereotype: Activity
- GUID: {EDC1DD7F5F3D42F8A006DAA3E91C1DE2}
- Lane: eaxpertise
- Description: Activity to submit the completed newsletter draft for internal review before sending.

### DataObject—urllist
- Name: URL List
- Type: Artifact
- Stereotype: DataObject
- GUID: {CEC76BB3E11A4C498936D895A48AA3E5}
- Lane: newssource
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

