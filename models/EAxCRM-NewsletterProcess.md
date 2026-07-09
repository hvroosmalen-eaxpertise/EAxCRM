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
  - Description: **Why:** The article pool contains every scraped article going back multiple cycles; the composer needs a curated shortlist per issue, not a raw dump, or the newsletter becomes an inbox of everything Sparx has published. **What:** A human review pass over the current Article Pool, marking candidates worth including in this issue and setting aside stale/duplicate/irrelevant items. **How:** The composer scans Article Pool entries (heading + summary + source URL) in the CRM, flags interesting ones, and moves to Select Articles for the final cut. **Context:** First composition step after Check Cadence gives a green light; feeds Select Articles.

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
  - Description: **Why:** Sending more frequently than the audience expects risks being perceived as spam and increases opt-outs (NWS-4); the cadence check is the single guard keeping the interval honest. **What:** A check of the interval since the most recent Sent newsletter against the 6-week minimum, producing a yes/no signal for the "6 weeks elapsed?" gateway. **How:** Reads the last Sent Newsletter's sent_date, compares to today; only Sent newsletters count — Drafts and in-Review issues do not reset the clock. **Context:** Entered directly after Start Newsletter; feeds the "6 weeks elapsed?" gateway, which either releases the composition flow or short-circuits to Newsletter Sent (no-op) when the window hasn't opened yet.

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
  - Description: **Why:** Raw selected articles are pointers, not a newsletter — the issue still needs framing text, branding, and layout before it can go out; without a dedicated compose step the send stage would ship half-formed content. **What:** A formatted EAxNewsletter draft built from the SelectedArticles set, applying the standard template (logo, article pointers with heading/summary/link), producing the NewsletterDraft artifact. **How:** The composer opens the Newsletter draft record, pulls in each SelectedArticles entry as a formatted pointer block, adds intro/outro copy where needed, and saves as Draft. Re-entered from Review Approved? = no for revisions. **Context:** Immediately after Select Articles; feeds Submit for Review. Loop-back point for a rejected review.

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
  - Description: **Why:** The browsed shortlist may still be too broad — the newsletter's format targets a fixed handful of pointers (typically 5) so the reader isn't overwhelmed and each item gets attention. **What:** The final subset of Article Pool entries chosen for this issue, materialised as the SelectedArticles artifact. **How:** The composer picks ~5 articles from the browsed shortlist, ordered for the newsletter; the selection is a snapshot for this issue and does not remove articles from the pool for future issues. **Context:** Between Browse Available Articles and Compose Newsletter.

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
  - Description: **Why:** An approved newsletter delivers no value until it reaches the audience; the send step is also the moment engagement tracking (NWS-3) starts, so it must produce one NewsletterContact record per recipient. **What:** Dispatch of the ApprovedNewsletter to every Contact on the current ContactList (opted-in Contacts only), archived afterwards as SentNewsletter. **How:** Iterates the ContactList, sends the newsletter via SMTP per recipient, creates a NewsletterContact row per recipient with status=sent and sent_date=now; opens/bounces are captured later by tracking. Marks the Newsletter status Sent, resetting the cadence clock for NWS-4. **Context:** Entered only when Review Approved? = yes; ends the process at Newsletter Sent.

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
  - Description: **Why:** A newsletter goes out to every opted-in Contact in one shot — an unreviewed send (typo, broken link, wrong article) can't be recalled, so a mandatory human review gate is the only safeguard (NWS-2). **What:** Transition of the NewsletterDraft into the Review state so an approver can examine it end-to-end. **How:** The composer clicks Submit; the Newsletter status changes Draft → Review, and it becomes visible on the reviewer's queue. No content mutation happens here — only the state transition and hand-off. **Context:** Last composition-side step; feeds the Review Approved? gateway. On rejection the flow returns to Compose Newsletter for revisions; on approval it proceeds to Send Newsletter.

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
  - Description: **Why:** Raw scraped HTML is unusable in a newsletter directly — the composer needs heading + short summary + link, and doing that manually on every scrape cycle would swamp the value of automating the scrape itself. **What:** Structured Article records (heading, summary, source_url) derived from the scraped HTML content. **How:** Parses each fetched page with BeautifulSoup, extracts the visible title as heading and the lede/first paragraph as summary, keeping the source URL as the canonical link; deterministic parsing only (TEC-4 — no LLM). **Context:** Between Scrape Articles and Store New Articles.

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
  - Description: **Why:** The scrape has to run against an intentional, configured set of NewsSource URLs — not a hard-coded list — so adding or removing a source is a data change, not a code change. **What:** The current URLList, i.e. the enabled NewsSource entries at scrape-cycle start. **How:** Reads NewsSource rows where enabled=true and materialises the URL List artifact for the rest of the scrape pipeline. **Context:** First automated step after the Scheduled Scrape start event; feeds Scrape Articles.

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
  - Description: **Why:** The article pool that Compose Newsletter draws from has to be continuously topped up from SparxSystems.com/.eu; without an automated fetch, the composer would be back to manually copy-pasting from those sites (NWS-1). **What:** Raw article HTML pages for every URL in the URLList, ready for parsing. **How:** Iterates the URLList, GETs each source page (and any linked article detail pages it exposes) with `requests`, holding the raw HTML in memory for the next step; deterministic HTTP only (TEC-4). **Context:** Between Fetch URL List and Extract Headings and Summaries.

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
  - Description: **Why:** Re-scraping the same sources every cycle would silently duplicate every Article — the pool would rot into thousands of copies and become useless for browsing (NWS-1). **What:** The Article Pool grown with only newly-seen articles from this cycle. **How:** For each extracted article, upserts into the Article table keyed on source_url — existing rows are skipped, new rows inserted with heading/summary/discovered_date. **Context:** Last automated step of the scrape flow; ends at Scrape Complete, and the resulting Article Pool is what Browse Available Articles reads next cycle.

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

