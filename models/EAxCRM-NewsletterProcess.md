# EAxCRM — Newsletter Process Architecture

**Model ID**: nlp-eacrm
**Purpose**: BPMN 2.0 newsletter process model for the EAxCRM system
**Version**: 1.0

## BPMN Collaboration—eaxcrmnewsletterprocessarchitecture
- Name: EAxCRM Newsletter Process Architecture
- GUID: {041CB75251274077AD901B60A22113C9}
- Diagram Name: Newsletter Process Architecture
- Diagram GUID: {2B166076863746D7A07013B7637711AB}

### Lane—eaxpertise
- Name: EAxpertise
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {BB939AA635654B1987BF869B9BA324C3}

#### Gateway—6weekselapsed
  - Name: 6 weeks elapsed?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {DAA2F889E90F49A38457057A6660F0DD}

#### DataObject—approvednewsletter
  - Name: Approved Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {322856D49A484978B70D4C1B5A7C8C8E}

#### Activity—browseavailablearticles
  - Name: Browse Available Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {0620E7F5D356404F802FAB9DF640A20C}

#### Activity—checkcadence
  - Name: Check Cadence
  - Type: Activity
  - Stereotype: Activity
  - GUID: {D515606735D84D819E179FA37E928766}

#### Activity—composenewsletter
  - Name: Compose Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {2C8D4690C80F4CAA9AB9BE21311AB0B4}

#### DataObject—contactlist
  - Name: Contact List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {E873BDE49CAD4413A0DCB8FFDA6C82B1}

#### DataObject—newsletterdraft
  - Name: Newsletter Draft
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {C2E06FCE066D48689E27DB327BBA504F}

#### EndEvent—newslettersent
  - Name: Newsletter Sent
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {6CC7D7BF28214C228A7EC6D008B1AE67}

#### Gateway—reviewapproved
  - Name: Review Approved?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {F66024AAD2DF4D4DBAB18A50DF26FA26}

#### Activity—selectarticles
  - Name: Select Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {F56539EDC4574F5EA4E9852E55C17231}

#### DataObject—selectedarticles
  - Name: Selected Articles
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {089BF9BB84C442F9BD40D6280DE855A6}

#### Activity—sendnewsletter
  - Name: Send Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {A1BF55B0B23D4A7690F69127A46C1A0D}

#### DataObject—sentnewsletter
  - Name: Sent Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {F25026769A444585A92227C0AB2B0074}

#### StartEvent—startnewsletter
  - Name: Start Newsletter
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {C302821497694DE8A8EF8CE07404105B}

#### Activity—submitforreview
  - Name: Submit for Review
  - Type: Activity
  - Stereotype: Activity
  - GUID: {B73FDEBEA3C04D7A876236E83D5B3D9B}

### Lane—newssource
- Name: News Source
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {B5747F80D0EF4CCCBDA12F6DC4E955E2}

#### DataObject—articlepool
  - Name: Article Pool
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {131C2E96AC68490594F4D09955D1426F}

#### Activity—extractheadingsandsummaries
  - Name: Extract Headings and Summaries
  - Type: Activity
  - Stereotype: Activity
  - GUID: {20E4F1B59DAE478E940FA07475C9B8DE}

#### Activity—fetchurllist
  - Name: Fetch URL List
  - Type: Activity
  - Stereotype: Activity
  - GUID: {76A337017BBE442B89E33F6C1F673553}

#### StartEvent—scheduledscrape
  - Name: Scheduled Scrape
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {A137C0CB3E8F4043BB20EB7FE0AB0D8C}

#### Activity—scrapearticles
  - Name: Scrape Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {F9BF305AE0EC40EAB11313E298726CA3}

#### EndEvent—scrapecomplete
  - Name: Scrape Complete
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {393E5B57C0644F488CC8F0578519B8C0}

#### Activity—storenewarticles
  - Name: Store New Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {75F2DB0F3A1847DDB6FB545F6D1F5944}

#### DataObject—urllist
  - Name: URL List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {C2CD373DA8064CF7A7A34F470FEE38B8}

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

