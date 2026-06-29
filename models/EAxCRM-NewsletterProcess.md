# EAxCRM — Newsletter Process Architecture

**Model ID**: nlp-eacrm
**Purpose**: BPMN 2.0 newsletter process model for the EAxCRM system
**Version**: 1.0

## BPMN Collaboration—eaxcrmnewsletterprocessarchitecture
- Name: EAxCRM Newsletter Process Architecture
- GUID: {487E5134F92043139F6D96CEEE406AB8}
- Diagram Name: Newsletter Process Architecture
- Diagram GUID: {88D3D1AB8684491DAE9FCE26A0E8BD74}

### Lane—eaxpertise
- Name: EAxpertise
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {BC700F36BCBF4871B48D7C8A28E13663}

#### Gateway—6weekselapsed
  - Name: 6 weeks elapsed?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {3B7CDA4C242F4A9D93A03C1F4D81E5F3}

#### DataObject—approvednewsletter
  - Name: Approved Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {EA24972B56994800807158FF58D8937E}

#### Activity—browseavailablearticles
  - Name: Browse Available Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {FD1177A4D7C443DE83C5C9F03E8BE559}

#### Activity—checkcadence
  - Name: Check Cadence
  - Type: Activity
  - Stereotype: Activity
  - GUID: {87990E1ED3504B91B3D5D3487B9F355B}

#### Activity—composenewsletter
  - Name: Compose Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {8A66CED5BB49445B9A80B558BE1E9B01}

#### DataObject—contactlist
  - Name: Contact List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {23F54B5888664D8180554D4223CD03F1}

#### DataObject—newsletterdraft
  - Name: Newsletter Draft
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {B87B55DEF1CB4A75AA1096903E144C71}

#### EndEvent—newslettersent
  - Name: Newsletter Sent
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {F3E60B4E236540CA8CE22BAB9CF40A57}

#### Gateway—reviewapproved
  - Name: Review Approved?
  - Type: Decision
  - Stereotype: Gateway
  - GUID: {9AA96B992C5043C9A0A7D841962CC7E5}

#### Activity—selectarticles
  - Name: Select Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {61D20ABAB1014D3AA75CE4FE24C169A8}

#### DataObject—selectedarticles
  - Name: Selected Articles
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {4F077E96468B4AF0B6B876FB5F96B191}

#### Activity—sendnewsletter
  - Name: Send Newsletter
  - Type: Activity
  - Stereotype: Activity
  - GUID: {1C80A24E13D944E8B4A61CF9EA41226F}

#### DataObject—sentnewsletter
  - Name: Sent Newsletter
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {FEF859324F25467A8CB0B0921748C836}

#### StartEvent—startnewsletter
  - Name: Start Newsletter
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {41B5327A88A744B1B7801A86CB9DC672}

#### Activity—submitforreview
  - Name: Submit for Review
  - Type: Activity
  - Stereotype: Activity
  - GUID: {EF4CFC0F0CA74D31B80FBC84469E0136}

### Lane—newssource
- Name: News Source
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {CD21E59C9F6143B1BF79E34C90D7F3ED}

#### DataObject—articlepool
  - Name: Article Pool
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {9B722FF0F13E4B23A54CC6C0C10D0C3B}

#### Activity—extractheadingsandsummaries
  - Name: Extract Headings and Summaries
  - Type: Activity
  - Stereotype: Activity
  - GUID: {48B9D5AB75A04FA3B25B469F6337F473}

#### Activity—fetchurllist
  - Name: Fetch URL List
  - Type: Activity
  - Stereotype: Activity
  - GUID: {782FF756CC9F401D88AC5B19366456F1}

#### StartEvent—scheduledscrape
  - Name: Scheduled Scrape
  - Type: Event
  - Stereotype: StartEvent
  - GUID: {9BF1BE57183C490B9139E846F75BE241}

#### Activity—scrapearticles
  - Name: Scrape Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {0CDB0CE460614EADBAECC8B05CCAE380}

#### EndEvent—scrapecomplete
  - Name: Scrape Complete
  - Type: Event
  - Stereotype: EndEvent
  - GUID: {58CC762B14364BF7BA70E43B85DF4CDE}

#### Activity—storenewarticles
  - Name: Store New Articles
  - Type: Activity
  - Stereotype: Activity
  - GUID: {86E55904469F432A9906E252EA035FE6}

#### DataObject—urllist
  - Name: URL List
  - Type: Artifact
  - Stereotype: DataObject
  - GUID: {20B1BC48CA7248BBBDD718DA7314890D}

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

