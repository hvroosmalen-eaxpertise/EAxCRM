## 2026-07-06 22:04:01 — Audit, run nlp-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| StartNewsletter_CheckCadence | StartNewsletter -> CheckCadence | SequenceFlow |  |
| CheckCadence_6weekselapsed | CheckCadence -> 6weekselapsed | SequenceFlow |  |
| 6weekselapsed_BrowseAvailableArticles | 6weekselapsed -> BrowseAvailableArticles | SequenceFlow |  |
| 6weekselapsed_NewsletterSent | 6weekselapsed -> NewsletterSent | SequenceFlow |  |
| BrowseAvailableArticles_SelectArticles | BrowseAvailableArticles -> SelectArticles | SequenceFlow |  |
| SelectArticles_ComposeNewsletter | SelectArticles -> ComposeNewsletter | SequenceFlow |  |
| ComposeNewsletter_SubmitforReview | ComposeNewsletter -> SubmitforReview | SequenceFlow |  |
| SubmitforReview_ReviewApproved | SubmitforReview -> ReviewApproved | SequenceFlow |  |
| ReviewApproved_SendNewsletter | ReviewApproved -> SendNewsletter | SequenceFlow |  |
| ReviewApproved_ComposeNewsletter | ReviewApproved -> ComposeNewsletter | SequenceFlow |  |
| SendNewsletter_NewsletterSent | SendNewsletter -> NewsletterSent | SequenceFlow |  |
| ScheduledScrape_FetchURLList | ScheduledScrape -> FetchURLList | SequenceFlow |  |
| FetchURLList_ScrapeArticles | FetchURLList -> ScrapeArticles | SequenceFlow |  |
| ScrapeArticles_ExtractHeadingsandSummaries | ScrapeArticles -> ExtractHeadingsandSummaries | SequenceFlow |  |
| ExtractHeadingsandSummaries_StoreNewArticles | ExtractHeadingsandSummaries -> StoreNewArticles | SequenceFlow |  |
| StoreNewArticles_ScrapeComplete | StoreNewArticles -> ScrapeComplete | SequenceFlow |  |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| EAxCRMNewsletterProcessArchitecture | EAxCRM Newsletter Process Architecture | CollaborationModel | {71833B05-38F3-41c7-9A4F-2085B324EDC1} |  |
| EAxpertise | EAxpertise | Lane | {6973247D-950D-4573-8C1A-879FF6DEB761} |  |
| NewsSource | News Source | Lane | {44320F6A-FEF0-4542-A842-998C0635269B} |  |
| 6weekselapsed | 6 weeks elapsed? | Gateway | {F4EE9DB2-4FD2-4346-8335-CA820CDE4A10} |  |
| ApprovedNewsletter | Approved Newsletter | DataObject | {FE488401-E4A4-46bb-94B1-E4A040E83D4B} |  |
| BrowseAvailableArticles | Browse Available Articles | Activity | {455033B7-11F0-4402-BF53-3486C82FABF5} |  |
| CheckCadence | Check Cadence | Activity | {7631A5C3-E4F2-4187-8296-CBBC0E4A50C0} |  |
| ComposeNewsletter | Compose Newsletter | Activity | {A42F3D07-163F-419d-875D-4990E66CCEB4} |  |
| ContactList | Contact List | DataObject | {D9BC4C9F-7CFB-45a2-8583-0E76DD73A14F} |  |
| NewsletterDraft | Newsletter Draft | DataObject | {13104C69-4C00-4b6a-9ADA-804BD2C19D5A} |  |
| NewsletterSent | Newsletter Sent | EndEvent | {39C46955-C543-40b6-80DC-81D4BA479199} |  |
| ReviewApproved | Review Approved? | Gateway | {9B1679CC-5F72-4346-A707-517769F52CF7} |  |
| SelectArticles | Select Articles | Activity | {2F3FCFF5-54A1-4e9c-A0C9-3657228F3D43} |  |
| SelectedArticles | Selected Articles | DataObject | {637A19F4-7220-40d0-847E-3848A0FEEEEB} |  |
| SendNewsletter | Send Newsletter | Activity | {3F77A46D-C3EA-450e-872F-245A4462A82E} |  |
| SentNewsletter | Sent Newsletter | DataObject | {93163D6D-1C14-4f5b-96C1-BBF5772E41C6} |  |
| StartNewsletter | Start Newsletter | StartEvent | {0AA82059-B629-4ee7-A3D5-735F2B0057C7} |  |
| SubmitforReview | Submit for Review | Activity | {18B57B90-3035-4c52-865A-A5CFFAA0010A} |  |
| ArticlePool | Article Pool | DataObject | {4607D2DC-C6CE-4c27-B0BC-CAA48E8CAD22} |  |
| ExtractHeadingsandSummaries | Extract Headings and Summaries | Activity | {2824BEE2-F8F6-4180-8BA2-2A16FF9DD879} |  |
| FetchURLList | Fetch URL List | Activity | {7BC27FA6-8291-4ee8-A7AC-798AA7569FC8} |  |
| ScheduledScrape | Scheduled Scrape | StartEvent | {7760A66A-9FD9-4f45-BB6A-0C11AD23728C} |  |
| ScrapeArticles | Scrape Articles | Activity | {AA61373F-634E-43d0-AC90-504243D1C4A2} |  |
| ScrapeComplete | Scrape Complete | EndEvent | {BD798C4C-6184-47ae-8D07-577B1628EC5F} |  |
| StoreNewArticles | Store New Articles | Activity | {D8C742DC-A1ED-482f-BBFD-7CBC9114F78A} |  |
| URLList | URL List | DataObject | {F87D2342-0B7D-4611-8FB0-2125288DFE8A} |  |

