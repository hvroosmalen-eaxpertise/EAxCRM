## 2026-07-17 10:42:30 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| e-customer | Customer | BusinessActor | {C1BA8F2F-19A2-414a-9342-6CDBEF02170D} |
| e-vendor | Vendor | BusinessActor | {BB4422FC-5EE0-458f-A745-DB3EF68DDFCA} |
| e-role-primary | Primary Contact | BusinessRole | {811BDA10-0DA2-403d-8F91-3EBB0DDF523C} |
| e-role-purchase | Purchase Contact | BusinessRole | {0454E4BA-00C8-4175-8BE3-DC71CB1FA1DD} |
| e-role-sales | Sales Contact | BusinessRole | {770EEF50-2421-40e4-86E7-FBA6EC8972A0} |
| e-role-license | License Holder | BusinessRole | {F0D44113-DC04-438e-BAAA-FB75093AAFF4} |
| e-func-insight | Customer Insight | BusinessFunction | {968F7E2D-AA52-4d30-998A-B4B2A407D2CF} |
| e-func-newsletter | Newsletter Management | BusinessFunction | {15038C92-26E4-4149-829C-430BC36E1508} |
| e-func-sales | Sales Management | BusinessFunction | {2766B1CD-98EC-4416-9AD0-F15E7A6BD894} |
| e-func-account | Manage Customer Account | BusinessFunction | {5CD4E03B-6DB1-44f5-82B3-9CC9ECA9FBBB} |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C941745A-EF66-46bb-92B2-186F861A83FC} |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {8F5698D8-D690-4043-9838-07023AFBB822} |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {E587CAC4-DDF1-4ae4-9520-EFA2BBD34FEE} |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {16EB355F-0987-4509-88F6-4E30F524A2E0} |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {07CBE85A-84F8-401f-8450-658131FAC4D3} |
| e-process-imap | Retrieve Communications | BusinessProcess | {4323CE1E-5974-424f-AADF-2243A7F2C7C2} |
| e-process-parse | Parse Documents | BusinessProcess | {175F0BE1-A31D-4a60-9547-D15BE6C8BD53} |
| e-process-scrape | Scrape News Sources | BusinessProcess | {9D6A82A7-D422-47c9-8EA0-FB57E023C290} |
| e-process-compose | Compose Newsletter | BusinessProcess | {0D9A5F96-6B06-485a-843E-EFD3A6B703D4} |
| e-process-review | Review Newsletter | BusinessProcess | {C1CAA7DF-571D-4e21-AF93-C25926C116F5} |
| e-process-send | Send Newsletter | BusinessProcess | {ABD553CB-86CE-4df6-B3F1-A7027F08A33F} |
| e-process-optin | Manage Opt-in | BusinessProcess | {01F29C6E-0DE3-4ed9-AF90-963A3EE96025} |
| e-process-rfq | Handle RFQ | BusinessProcess | {61D78040-3A18-4c8e-BE43-A7A443D1F559} |
| e-process-offer | Manage Offer | BusinessProcess | {692C91B2-AF19-43e0-82A1-5BE80CC76952} |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {B3427505-C03B-459c-865D-4536AE8B61B5} |
| e-process-deliver | Manage Delivery | BusinessProcess | {444BD8F9-DD2E-422e-A31C-418F83CC6BB2} |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {FFF2F723-FC37-417c-A595-06AA29AA021D} |
| e-bo-customer | Customer Data | BusinessObject | {E74F3724-738C-4af6-9433-A7C91FD1703C} |
| e-bo-contact | Contact Data | BusinessObject | {E172AFB6-A99B-47f6-8AED-2A3C175B2C87} |
| e-bo-communication | Communication Data | BusinessObject | {FD676BEE-58DC-442d-B065-5189FADB49FF} |
| e-bo-document | Document Data | BusinessObject | {97EDA37E-B3F4-40b3-BE16-FF25516DAF27} |
| e-bo-newsletter | Newsletter Data | BusinessObject | {58095A83-8C55-4409-99DE-C9CBCCB0EE4F} |
| e-bo-license | License Data | BusinessObject | {D2FFC119-121F-408e-BB2D-770845671C40} |
| e-bo-lineitem | License Line Item Data | BusinessObject | {0AE49707-FD00-46f7-BE5E-F3482304DED6} |
| e-bo-purchase | Purchase Data | BusinessObject | {15764D31-CFF4-4cff-96A9-08D6D4F9ACDC} |
| e-bo-offer | Offer Data | BusinessObject | {09597932-EF0E-4f27-A90C-3119A8A1102F} |
| e-bo-quote | Quote Data | BusinessObject | {FCCE1407-E625-44e6-A27A-16D704CC9BB8} |
| e-bo-delivery | Delivery Data | BusinessObject | {92495AC9-6E7C-4404-9462-67D07F056F8C} |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {7146D1EF-DC1F-49d4-B422-513E83287C3A} |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {97378B6B-402F-4392-B829-ADD1C0BA50E2} |
| e-bo-service | Service Data | BusinessObject | {372BA17C-1D48-4a2b-BE5C-630091823F6C} |
| e-bo-vendor | Vendor Data | BusinessObject | {5A58FDDE-F52C-4ab0-863D-06F266817635} |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {C1EDD0AE-85D2-4f97-B547-F81C85EE4E16} |
| e-svc-customer | Customer Management Service | ApplicationService | {B10DF4E2-0405-4fa3-95AD-93DD8DD80C8A} |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {7CB24E08-39B2-44dd-BBCC-F7D4E4163E21} |
| e-svc-parse | Document Parse Service | ApplicationService | {A8DB1ECC-0683-4dbc-BD5E-F16FEDCDBD23} |
| e-svc-scrape | News Scrape Service | ApplicationService | {C368AAB9-CDCA-4bd0-BCE7-23121DC81002} |
| e-svc-newsletter | Newsletter Service | ApplicationService | {439ADB42-6063-4555-A0D5-E5C16669590A} |
| e-svc-sales | Sales Management Service | ApplicationService | {38F80115-5970-492e-AD41-A27184CAA054} |
| e-data-customer | Customer Record | DataObject | {38755035-A014-4e91-8916-83CF0B5EB552} |
| e-data-contact | Contact Record | DataObject | {4EC2CCB2-2A8E-462c-933F-C0A41E1EE343} |
| e-data-email | Email Record | DataObject | {6DD22B64-1839-4070-9C13-9EF1F46F4B1B} |
| e-data-attachment | Attachment Record | DataObject | {8202BB81-C84E-488d-BA58-C931459E2209} |
| e-data-article | Article Record | DataObject | {E5140148-E045-4373-84CF-91C861113B84} |
| e-data-newsletter | Newsletter Record | DataObject | {A4C30C82-1BAE-4526-9984-861185627FF8} |
| e-data-license | License Record | DataObject | {AD785C56-FC25-478f-8682-BB2208CF353E} |
| e-data-lineitem | License Line Item Record | DataObject | {1359CF37-731E-48bf-82AA-7F3D75ED7E04} |
| e-data-purchase | Purchase Record | DataObject | {BBAF5B13-86B9-4203-AFAF-E19075A470A7} |
| e-data-offer | Offer Record | DataObject | {863487A7-E636-4456-91DA-1ACFF8E7F2DC} |
| e-data-quote | Quote Record | DataObject | {6DCDD9C2-425E-4dab-8E22-039E3ECAFC6D} |
| e-data-delivery | Delivery Record | DataObject | {1F49BD55-1FE2-488e-B184-8F37CAEECECE} |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {6CFCA7A4-03D4-431e-A888-4B99C0E44535} |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {91B4CE04-76DA-411c-9CCA-5A830AEE1277} |
| e-data-service | Service Record | DataObject | {8B729032-BDB1-4634-A3AF-C0FB7B34A4C1} |
| e-data-vendor | Vendor Record | DataObject | {7F8F9059-02BE-4f8b-8FB9-60DAC052A4D0} |
| e-node-nas | QNAP NAS | Node | {D31B01B3-03F1-4b8a-8008-52426A6C65E7} |
| e-device-nas | QNAP Hardware | Device | {5B61036F-F1D5-42bc-B363-500339F38B96} |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {6A1B9734-A007-402f-B011-23FC9FE3130D} |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {23D95BE7-4BAD-4c98-8BA2-783428B3F44C} |
| e-sw-container | Docker (Container Station) | SystemSoftware | {03966C11-6A12-47f3-822D-3A77B1551F06} |
| e-art-dockerfile | Dockerfile | Artifact | {63C5E706-CDC4-4b4b-9FE8-A23346D58C8F} |
| e-art-db | SQLite Database File (dev/test) | Artifact | {629D49BC-4B40-4e9c-AA8F-C81258272467} |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A2D412F6-CE85-40eb-B41A-48B68690EE34} |
| e-businessactor1 | BusinessActor1 | BusinessActor | {50EBE3A9-0579-4f00-8AF8-090308F50A51} |
| r-cust-pri | Association | Association | {25B15A87-260D-4998-88C3-3A29EBE00FEB} |
| r-cust-pur | Association | Association | {9B68D3A0-F7B2-43a2-A18D-E96489D05098} |
| r-cust-sal | Association | Association | {4AE98835-A137-4f8a-AB04-9C4FF8014C0C} |
| r-cust-lic | Association | Association | {843A717D-AE40-4dca-A0C1-4030B3294089} |
| r-comp-insight-imap | Composition | Composition | {E5B063DC-4779-430b-97C4-F9DA41D064C8} |
| r-comp-insight-parse | Composition | Composition | {3FEE0458-AF07-435a-B435-A6FEE89FC4C3} |
| r-comp-newsletter-scrape | Composition | Composition | {E190CE51-04E2-4084-98DB-4702A731CF32} |
| r-comp-newsletter-compose | Composition | Composition | {BC6BFA36-43A2-4016-9A0C-D4D105AF80BD} |
| r-comp-newsletter-review | Composition | Composition | {E44706DA-4F53-4d81-BB59-44A0573F8A9D} |
| r-comp-newsletter-send | Composition | Composition | {81E855F7-02BB-4e09-8A6B-005ABF5AF2FB} |
| r-comp-newsletter-optin | Composition | Composition | {AB0DB919-47AB-41d1-A409-5FADCF5CFCD3} |
| r-access-imap-cust | Access | Access | {1F69C45F-DEDF-4da2-8C80-31DD1F6F1C65} |
| r-access-imap-cont | Access | Access | {6CAB9A38-190F-4887-A5F8-F0CDB747C81A} |
| r-access-imap-comm | Access | Access | {BF92766B-1341-4ae6-A7E6-6BD1C35F6DAE} |
| r-access-parse-doc | Access | Access | {7DD68FEE-EFC8-47fa-AD0F-E54E190E3468} |
| r-access-parse-lic | Access | Access | {099FDD7C-996E-4464-9715-A98D6002AFAD} |
| r-access-parse-lli | Access | Access | {78E23CA0-D863-459a-80F3-E7AB8A84ED2B} |
| r-access-compose-news | Access | Access | {406FFE67-BD2A-4334-ADCC-29DA024054C0} |
| r-access-send-news | Access | Access | {E98E4642-C7F7-41a7-B4E1-E53B7D6418E2} |
| r-assign-svc-customer | Assignment | Assignment | {C83A2208-C09A-4e18-95A3-464458C93DE0} |
| r-assign-svc-imap | Assignment | Assignment | {5E60CE8E-3FAC-47ae-92DC-62CCF8FBE04E} |
| r-assign-svc-parse | Assignment | Assignment | {4BF2FCEF-D95C-4592-9C47-78BCA51706D6} |
| r-assign-svc-scrape | Assignment | Assignment | {196F40E9-4129-4d6d-BDF4-33018EF8DAC3} |
| r-assign-svc-newsletter | Assignment | Assignment | {AB1533AF-BBD7-473f-BF74-0135CC227E36} |
| r-access-cust-data | Access | Access | {3149FBF4-9AAD-458c-8FB2-2E220754FC43} |
| r-access-cont-data | Access | Access | {1A7262F4-9BE3-46d5-B16D-6C055992571C} |
| r-access-imap-data | Access | Access | {C5203BDD-50F9-4d6c-A509-3268BF507A5B} |
| r-access-parse-data | Access | Access | {1377B1D9-C697-401d-ADA5-34ADEFDE30A0} |
| r-access-scrape-data | Access | Access | {73597DAC-7A3D-4ca6-B410-CE643FAB655B} |
| r-access-newsletter-data | Access | Access | {EAF237DB-8513-4273-8E07-47516CD93468} |
| r-access-parse-lic-data | Access | Access | {18E024E3-C821-40b2-A748-5754DF9049C1} |
| r-access-parse-lli-data | Access | Access | {C65C444E-828C-40dd-A2B1-982B340257EF} |
| r-access-cust-purch | Access | Access | {00A856E7-B472-4bb0-8835-5C663952201E} |
| r-realize-svc-cust-imap | Realization | Realization | {A104EBE9-F7ED-4a3d-8DD6-070D8EAAD467} |
| r-realize-svc-imap-imap | Realization | Realization | {FF33C8B9-238A-42d3-AE0F-832529B078B7} |
| r-realize-svc-cust-createaccount | Realization | Realization | {3FC2E92F-0097-4774-9307-589C94159D7C} |
| r-realize-svc-cust-dedupe | Realization | Realization | {DCE7C147-AC00-4282-B03F-D9AB7C84CBD6} |
| r-realize-svc-cust-merge | Realization | Realization | {F6FFE584-2E7D-4e25-BB51-57DC506134D3} |
| r-realize-svc-cust-emailhistory | Realization | Realization | {C4D50ACC-DA58-45d0-999E-56C74D2D599E} |
| r-realize-svc-imap-emailhistory | Realization | Realization | {74C3502F-B4F5-4850-8A9C-4BD890F41B9A} |
| r-realize-svc-parse-parse | Realization | Realization | {8192B7C3-5BDF-4f02-9DC8-3A7E6869D21C} |
| r-realize-svc-scrape-scrape | Realization | Realization | {4069BC27-9382-442b-93F6-42CD6D9A49D4} |
| r-realize-svc-news-compose | Realization | Realization | {B26DBC9F-96B1-428e-BFC1-9007A29CD09B} |
| r-realize-svc-news-review | Realization | Realization | {DE1BCBC9-7A6D-4616-816F-53D84E312679} |
| r-realize-svc-news-send | Realization | Realization | {1F47CF8C-1F4A-496b-9D6D-6D6BC10F191E} |
| r-realize-svc-cust-optin | Realization | Realization | {6DFB24DB-8FD4-4ecf-A591-F281636ABC45} |
| r-realize-data-cust-bo | Realization | Realization | {BE67FFE2-648E-4870-AB91-CC46845BCB24} |
| r-realize-data-contact-bo | Realization | Realization | {F6D3772C-3DAC-4df3-93B3-2EB34A0E86D4} |
| r-realize-data-email-bo | Realization | Realization | {FF58DB48-B80E-4789-8619-7ABB6AD42B06} |
| r-realize-data-attach-bo | Realization | Realization | {CEA4242F-A7A0-40bb-B5C2-EEC9F0D76EC1} |
| r-realize-data-article-bo | Realization | Realization | {E70B118D-68EC-4160-AC61-8BD5F7C785E6} |
| r-realize-data-newsletter-bo | Realization | Realization | {1B7901AC-73DC-4889-8649-7F20DDC95643} |
| r-realize-data-license-bo | Realization | Realization | {DE00672C-71A3-4efc-84F5-80B0789F55F4} |
| r-realize-data-lineitem-bo | Realization | Realization | {28B3C8F0-E5B9-4aad-A0F5-E0BF9CE4E5A1} |
| r-realize-data-purchase-bo | Realization | Realization | {562FB9AA-4967-4f48-80E5-D4A640F12FC5} |
| r-comp-node-device | Composition | Composition | {11AD662E-073F-4497-B99C-011E3DE580AA} |
| r-assign-sw-django | Assignment | Assignment | {93D08B1B-F63A-419d-BC1E-D29D839A9B2A} |
| r-assign-sw-sqlite | Assignment | Assignment | {D0F16D6C-82E0-44cd-9450-DFA357A59016} |
| r-assign-sw-container | Assignment | Assignment | {A3B259E4-AEC1-422d-8ABC-EA93ADAC016C} |
| r-realize-sw-django-app | Realization | Realization | {F218B98D-1B10-4d7c-86AC-64E7D57013BC} |
| r-realize-art-db-sw | Realization | Realization | {D2DBA85F-9B98-4ea1-8B75-3B714C83E65E} |
| r-realize-art-docker-sw | Realization | Realization | {CDDB6920-2D81-434e-A568-D167717D50AA} |
| r-serve-sqlite-app-dev | Serving | Serving | {216B69C9-0E37-4a4d-BE23-7734085199E5} |
| r-comp-sales-rfq | Composition | Composition | {6E277832-F1D5-4dfb-9779-72E832902DCD} |
| r-comp-sales-offer | Composition | Composition | {EB8CBA6E-99AC-467e-803D-97C5C62E1EDF} |
| r-comp-sales-procure | Composition | Composition | {44A58532-53BE-47c2-9A44-E312088297F2} |
| r-comp-sales-deliver | Composition | Composition | {0575256D-EB61-4057-A3AE-4C25893FC65E} |
| r-comp-sales-invoice | Composition | Composition | {0378000C-6EAA-4f14-8E17-573A7AF1C940} |
| r-comp-account-create | Composition | Composition | {04DCF088-8F88-44db-901F-6E0CA8C83583} |
| r-comp-account-dedupe | Composition | Composition | {2B9258AE-DEF7-4846-8527-62E6FEB6B2B5} |
| r-comp-account-merge | Composition | Composition | {112B91EB-4259-4d93-ACF7-0D61EE491A22} |
| r-comp-account-emailhistory | Composition | Composition | {EECEE799-9E06-47b5-B275-B0001CB425C4} |
| r-comp-account-optinsuggest | Composition | Composition | {DBE63EA4-D74B-4b3c-AFFB-7CA4A9B22812} |
| r-access-rfq-quote | Access | Access | {641BC4AF-CBDC-4151-B43B-AB2135EE1E12} |
| r-access-createaccount-customer | Access | Access | {DF983EBA-8F93-4a4e-A737-61C2BC5DB473} |
| r-access-createaccount-contact | Access | Access | {8B4BA729-5775-4fdd-AD66-7B5DD8D88662} |
| r-access-dedupe-customer | Access | Access | {9F73DE90-E534-4012-840A-43510224C935} |
| r-access-merge-customer | Access | Access | {8160B303-2914-40a0-9975-5CB38F61C55E} |
| r-access-merge-contact | Access | Access | {F69FA620-D124-4c15-AD8D-7129E90D6BAF} |
| r-access-emailhistory-communication | Access | Access | {6EC2F41F-8F8A-4264-9BB8-753CD540A876} |
| r-access-dedupe-contact | Access | Access | {53AFEC7B-4D27-45b6-B518-98A6C28AFAAA} |
| r-access-emailhistory-contact | Access | Access | {DBA8B120-FFE1-4ec7-9736-FEA6F35279D2} |
| r-access-optinsuggest-contact | Access | Access | {93BB0148-2D8F-49b9-A8EA-9107C107F2D8} |
| r-trigger-rfq-createaccount | Triggering | Triggering | {68B84CDE-FE16-4a50-80DD-33D0625DC59B} |
| r-access-offer-offer | Access | Access | {C6F01871-FCB1-42ab-A48C-B95877861526} |
| r-access-offer-service | Access | Access | {65821462-BC0E-4b4b-9F4A-08A7603B4B5C} |
| r-access-procure-quote | Access | Access | {CA448650-41B3-4f87-A46C-B35D04FC3510} |
| r-access-procure-vendor | Access | Access | {37A586A5-09F1-4e6c-81AD-70585486BB7B} |
| r-access-deliver-delivery | Access | Access | {8181FA87-2A3B-4626-8FFC-61FF62C940C2} |
| r-access-invoice-salesinv | Access | Access | {599D7EC0-09FA-4488-A4F6-20CE3114D3FC} |
| r-access-invoice-procinv | Access | Access | {6190D3A0-FBB2-4bf6-A437-0B1F6B1D7C48} |
| r-access-invoice-purchase | Access | Access | {E301E5C9-F77C-46d3-B42F-5A882C2A76D6} |
| r-assign-svc-sales | Assignment | Assignment | {7373094F-49A4-41dc-B74A-BC0153F90F4E} |
| r-access-sales-offer | Access | Access | {9BC592B7-48F4-4242-A0B1-DF626B57BF52} |
| r-access-sales-quote | Access | Access | {5A2C86E8-5FE7-481f-9BA7-6795F24226EF} |
| r-access-sales-delivery | Access | Access | {C1786808-E90F-4ab0-8FD5-138EE287047F} |
| r-access-sales-salesinv | Access | Access | {CEF379C7-C7AC-4a53-9780-23080DBC8030} |
| r-access-sales-procinv | Access | Access | {40DA9C92-5C26-4d59-9900-D4A87771FEBB} |
| r-access-sales-service | Access | Access | {0A6CB0EC-A50A-4424-B850-E557777AE1E7} |
| r-access-sales-vendor | Access | Access | {DE460C60-5DE7-46a2-92CC-E289EAEF18D2} |
| r-realize-svc-rfq | Realization | Realization | {D0968A86-60AE-4955-9720-EAF6FB967798} |
| r-realize-svc-offer | Realization | Realization | {23D83E63-6F79-48b9-A0BA-5C224BC81035} |
| r-realize-svc-procure | Realization | Realization | {7544AB2E-077B-4f60-8CFC-A5E412400CF4} |
| r-realize-svc-deliver | Realization | Realization | {A28A8BA9-139C-4853-A567-A92CF986DE7F} |
| r-realize-svc-invoice | Realization | Realization | {517C5341-8644-47bf-8ED2-6D96C71BFDC0} |
| r-realize-data-offer-bo | Realization | Realization | {97F7EDB4-3341-4f83-930A-A2FF947E74C0} |
| r-realize-data-quote-bo | Realization | Realization | {2D0D2258-FABD-4161-B0A3-BA072D088436} |
| r-realize-data-delivery-bo | Realization | Realization | {69937C74-1542-42a2-8CF2-84B155DF58D9} |
| r-realize-data-salesinv-bo | Realization | Realization | {99FCF1F1-1C90-49e7-B7B5-68CA853503F8} |
| r-realize-data-procinv-bo | Realization | Realization | {7578C8FB-2956-4b63-8591-97C9FC7DA3FE} |
| r-realize-data-service-bo | Realization | Realization | {27696578-B075-4ebf-BE91-B6D13978E15E} |
| r-realize-data-vendor-bo | Realization | Realization | {BB0D9946-6FBB-41ff-B3B6-7D6B08BBA03D} |
| r-assignment-node-nas-sw-sqlite | Assignment | Assignment | {E1C21BF5-8AC5-4951-B783-5C683FDEB8A7} |
| r-association-customer-art-db-prod | Association | Association | {05F54927-5C14-4931-8EED-5E61DA54F4A5} |
| r-composition-art-db-prod-art-db-prod | Composition | Composition | {F356DAB8-2160-4667-901B-F5062EF2BE0D} |
| r-assignment-node-nas-art-db-prod | Assignment | Assignment | {B527392E-0E20-40be-8113-179F6A7DBB6D} |
| r-assignment-art-db-prod-sw-django | Assignment | Assignment | {3045F017-F88F-4737-926B-0BDACE2A6873} |
| r-serving-art-db-prod-app-django | Serving | Serving | {65490C71-EB00-4edb-8FCB-CE6EBF4EECEB} |
| r-realization-art-db-prod-art-db-prod | Realization | Realization | {90F171E0-37A2-4d65-B234-A90B588D1283} |

## 2026-07-16 13:34:51 — Audit

### Checkpoints
- Loaded MD + guid_map
- Sync complete

## 2026-07-14 16:09:23 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL Database Instance -> Secondary Contact; Notes: The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. -> Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-access-cust-data | Access | Access | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-access-cont-data | Access | Access | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-access-imap-data | Access | Access | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-access-parse-data | Access | Access | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-access-scrape-data | Access | Access | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-access-newsletter-data | Access | Access | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-access-parse-lic-data | Access | Access | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-access-parse-lli-data | Access | Access | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-access-cust-purch | Access | Access | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |  |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |  |
| r-realize-art-db-prod-sw | Realization | Realization | {D92206DB-324C-43d1-8579-C9214F009D0A} |  |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |  |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-access-sales-offer | Access | Access | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-access-sales-quote | Access | Access | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-access-sales-delivery | Access | Access | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-access-sales-salesinv | Access | Access | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-access-sales-procinv | Access | Access | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-access-sales-service | Access | Access | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-access-sales-vendor | Access | Access | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-14 16:00:06 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL Database Instance -> Secondary Contact; Notes: The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. -> Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |  |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |  |
| r-realize-art-db-prod-sw | Realization | Realization | {D92206DB-324C-43d1-8579-C9214F009D0A} |  |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |  |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-14 15:59:32 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL Database Instance -> Secondary Contact; Notes: The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. -> Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |  |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |  |
| r-realize-art-db-prod-sw | Realization | Realization | {D92206DB-324C-43d1-8579-C9214F009D0A} |  |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |  |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-14 15:56:11 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL Database Instance -> Secondary Contact; Notes: The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. -> Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |  |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |  |
| r-realize-art-db-prod-sw | Realization | Realization | {D92206DB-324C-43d1-8579-C9214F009D0A} |  |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |  |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-14 15:55:45 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL Database Instance -> Secondary Contact; Notes: The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. -> Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |  |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |  |
| r-realize-art-db-prod-sw | Realization | Realization | {D92206DB-324C-43d1-8579-C9214F009D0A} |  |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |  |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-14 15:26:15 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL Database Instance -> Secondary Contact; Notes: The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. -> Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |  |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |  |
| r-realize-art-db-prod-sw | Realization | Realization | {D92206DB-324C-43d1-8579-C9214F009D0A} |  |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |  |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-14 15:25:44 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| r-realize-art-db-prod-sw | Realization | Realization | {D92206DB-324C-43d1-8579-C9214F009D0A} |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL Database Instance -> Secondary Contact; Notes: The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. -> Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |  |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |  |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |  |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-09 16:37:07 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL Database Instance -> Secondary Contact; Notes: The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. -> Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |  |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |  |
| r-realize-art-db-prod-sw | Realization | Realization | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |  |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-09 16:36:33 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL Database Instance -> Secondary Contact; Notes: The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. -> Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |  |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |  |
| r-realize-art-db-prod-sw | Realization | Realization | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |  |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-09 16:35:30 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| r-assign-sw-sqlite | Assignment | Assignment | {E428B70C-404D-4ccf-9F80-6D65A41C99CB} |
| r-comp-devws-device | Composition | Composition | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |
| r-assign-sw-rdbms | Assignment | Assignment | {10B1A3BC-F580-4155-9AC2-C8CB997E585D} |
| r-assign-sw-django-dev | Assignment | Assignment | {9FC456FE-49E5-4226-8682-2BD774DBA360} |
| r-serve-rdbms-app | Serving | Serving | {430561CE-EA27-4cbc-ACB3-9FF0FF06A85D} |
| r-serve-sqlite-app-dev | Serving | Serving | {080CE31C-0ED1-4843-B908-AB7D495E6955} |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} |  |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} | Notes: The target deployment environment running the application locally. -> Production deployment environment running the EAxCRM application and PostgreSQL 16, both containerised on QNAP Container Station (TEC-5). |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-node-devws | Windows Dev Workstation | Node | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Secondary Contact -> Windows Dev Workstation; Notes: Colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties; the expected successor role when the Primary contact leaves the organization (CRM-10). -> Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. |
| e-device-devws | Windows Dev Hardware | Device | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Workstation -> Windows Dev Hardware; Notes: Local development and test environment (Han's daily machine) running Django natively against a SQLite file — used for authoring and pre-production verification before promotion to the QNAP NAS. See TEC-5. -> The developer's Windows 11 workstation hosting the dev/test environment. |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite (local dev/test) | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} | Name: SQLite -> SQLite (local dev/test); Notes: Embedded database engine, file-based, zero-configuration, ideal for NAS deployment. -> Embedded database engine used for local development and test only (TEC-1). Not the production target — SQLite's single-writer model is unsuitable for concurrent multi-user access. |
| e-sw-rdbms | PostgreSQL 16 | SystemSoftware | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: Windows Dev Hardware -> PostgreSQL 16; Notes: The developer's Windows 11 workstation hosting the dev/test environment. -> Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File (dev/test) | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} | Name: SQLite Database File -> SQLite Database File (dev/test); Notes: The file-based SQLite database storing all CRM data. -> The file-based SQLite database used in local dev/test only. Never the production data store. |
| e-art-db-prod | PostgreSQL Database Instance | Artifact | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} | Name: PostgreSQL 16 -> PostgreSQL Database Instance; Notes: Production RDBMS chosen for TEC-1 — server-based, transactional (MVCC), supports concurrent multi-user writes. Django's reference backend (via psycopg); no licensing cost. Runs as a Docker container on QNAP Container Station alongside the Django application container. -> The production PostgreSQL 16 database instance holding all CRM data in production — realising e-sw-rdbms. |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-realize-art-db-prod-sw | Realization | Realization | {09F4F40A-A0A4-4f25-90F8-E63E18E2CA1B} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-09 12:46:28 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| e-role-secondary | Secondary Contact | BusinessRole | {A7029E0C-4ECB-4a50-8AC2-6D48C30649AE} |
| r-cust-sec | Association | Association | {BA2C8566-7285-4626-90A0-E1FCFBAED95B} |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {2D02D6F8-4131-4775-B741-D33C7DE8C99F} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-06 22:01:35 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {2D02D6F8-4131-4775-B741-D33C7DE8C99F} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

## 2026-07-06 14:34:20 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| e-customer | Customer | BusinessActor | {84865198-4B96-476e-8985-C1963A9AAAA5} |  |
| e-vendor | Vendor | BusinessActor | {9F7FA8C1-6F5C-4d9d-A12F-60C5A9C3B862} |  |
| e-role-primary | Primary Contact | BusinessRole | {90AF07BF-49BC-42a2-9269-0C0859527700} |  |
| e-role-purchase | Purchase Contact | BusinessRole | {01E0C49C-5BDD-4d98-9662-2FE8D9F94DE4} |  |
| e-role-sales | Sales Contact | BusinessRole | {99B5C17A-BEC7-4a6f-9298-1E256BDB8FFA} |  |
| e-role-license | License Holder | BusinessRole | {B3B0578F-2B92-4b58-A7DA-F5A8C70CC782} |  |
| e-func-insight | Customer Insight | BusinessFunction | {EE4D98ED-4CA6-477d-B3D9-3D001152864E} |  |
| e-func-newsletter | Newsletter Management | BusinessFunction | {6696FBE6-88B7-4040-A956-BFE6D05CD42B} |  |
| e-func-sales | Sales Management | BusinessFunction | {62619A5C-5582-400c-912D-627C051A8C23} |  |
| e-func-account | Manage Customer Account | BusinessFunction | {9C65C325-3DCF-4e4c-BCFD-CE2EB28EFF21} |  |
| e-process-createaccount | Create Customer Account | BusinessProcess | {C404DB7E-7C1B-4aa1-BB5D-69890A1264AB} |  |
| e-process-dedupe | Flag Duplicate Accounts | BusinessProcess | {E2046359-CBCA-4ddf-B40D-BC6F6BCAA809} |  |
| e-process-merge | Merge Customer Accounts | BusinessProcess | {F3C436C7-128E-4b1d-9EF2-5E4215221E7B} |  |
| e-process-emailhistory | Retrieve Customer Email History | BusinessProcess | {07A40D3A-9850-4484-AE7B-B3EB2B1CC791} |  |
| e-process-optinsuggest | Suggest Newsletter Opt-in | BusinessProcess | {7A22EFB4-265C-42e3-A3D8-E04119031439} |  |
| e-process-imap | Retrieve Communications | BusinessProcess | {E03D8B3D-505B-4723-BDC1-AAD8D357A42D} |  |
| e-process-parse | Parse Documents | BusinessProcess | {7696A72A-B578-4919-A6D3-1D7682779FF9} |  |
| e-process-scrape | Scrape News Sources | BusinessProcess | {E5B12331-5BEC-479e-9B59-F0A1B53E1148} |  |
| e-process-compose | Compose Newsletter | BusinessProcess | {903468B3-673B-49d7-977A-5819E3941177} |  |
| e-process-review | Review Newsletter | BusinessProcess | {083CE10B-3818-4fac-8DA5-26197272BA23} |  |
| e-process-send | Send Newsletter | BusinessProcess | {5784E12A-1D05-4211-81DA-A63F3CF52DC4} |  |
| e-process-optin | Manage Opt-in | BusinessProcess | {4E089DFE-4BB9-47ad-86EE-B717467A7844} |  |
| e-process-rfq | Handle RFQ | BusinessProcess | {6E4FBD04-AC30-425b-8AC7-A388AAC5259C} |  |
| e-process-offer | Manage Offer | BusinessProcess | {42BAAA98-7377-4170-AF59-B25F20CD6E26} |  |
| e-process-procure | Procure Licenses & Services | BusinessProcess | {92EE0D8F-CA48-49da-8D75-2A4D5D18DE6E} |  |
| e-process-deliver | Manage Delivery | BusinessProcess | {7F983699-DDFF-4d06-A41A-DF3F644A41AD} |  |
| e-process-invoice | Manage Invoicing & Payment | BusinessProcess | {DFCB9C7C-1A57-451a-AD76-5EF7C5155B71} |  |
| e-bo-customer | Customer Data | BusinessObject | {3EC5A5C4-6CB7-48b1-8BA8-07B53B487DDC} |  |
| e-bo-contact | Contact Data | BusinessObject | {6713A1DB-2498-444e-9D48-FCF86DD6953A} |  |
| e-bo-communication | Communication Data | BusinessObject | {8CD8BF07-A081-4f9d-865C-499F16919487} |  |
| e-bo-document | Document Data | BusinessObject | {78E314B0-4F81-4a96-8A94-424E024E605A} |  |
| e-bo-newsletter | Newsletter Data | BusinessObject | {A958F5AA-FAEC-4a38-A711-B64144CC4A7F} |  |
| e-bo-license | License Data | BusinessObject | {9CC60D0D-2B78-4acd-AF07-D3553D346E2C} |  |
| e-bo-lineitem | License Line Item Data | BusinessObject | {B99B13DD-158B-46ad-8378-038C6C3C978B} |  |
| e-bo-purchase | Purchase Data | BusinessObject | {8DFAFFFB-B230-4821-8A68-78A36C0A6515} |  |
| e-bo-offer | Offer Data | BusinessObject | {55C94A0B-C3F7-4850-A1E2-E79A5BF905AD} |  |
| e-bo-quote | Quote Data | BusinessObject | {BBF2E13D-6E50-4f0a-AC9B-BB1BE90321EC} |  |
| e-bo-delivery | Delivery Data | BusinessObject | {6C253FD9-1E39-4dba-B1BC-E9F2ED15D58F} |  |
| e-bo-salesinvoice | Sales Invoice Data | BusinessObject | {12141256-DD3E-4d6b-A376-E1F15553FFCE} |  |
| e-bo-procurementinvoice | Procurement Invoice Data | BusinessObject | {EB949854-DB1F-4529-848A-3F688F45F004} |  |
| e-bo-service | Service Data | BusinessObject | {20CC3394-5EE0-40f5-AD76-DACF62434B9F} |  |
| e-bo-vendor | Vendor Data | BusinessObject | {F43B627B-D346-489d-8A9E-6D82E53526CA} |  |
| e-app-django | EAxCRM Django Application | ApplicationComponent | {BC8873CA-13C6-465c-9D3D-B4667593EA3B} |  |
| e-svc-customer | Customer Management Service | ApplicationService | {EE36DF2E-5F30-48d6-B5C7-6D165DCEB445} |  |
| e-svc-imap | IMAP Fetch Service | ApplicationService | {628BDBCE-2828-48ea-80F1-94AF2D05EC47} |  |
| e-svc-parse | Document Parse Service | ApplicationService | {820DC7B9-763D-465a-A1F3-5B5CC4B031C5} |  |
| e-svc-scrape | News Scrape Service | ApplicationService | {E4682BBF-2031-494d-A114-0526EF6C5300} |  |
| e-svc-newsletter | Newsletter Service | ApplicationService | {710263BD-A65B-4312-90D4-99D3BCC6A27F} |  |
| e-svc-sales | Sales Management Service | ApplicationService | {1FDBAACD-9655-4819-BACC-678012148B5E} |  |
| e-data-customer | Customer Record | DataObject | {439E556D-1452-4fff-8C97-01B98F8A2A7F} |  |
| e-data-contact | Contact Record | DataObject | {878B8F69-E8C6-4222-BB93-2868EA64CB69} |  |
| e-data-email | Email Record | DataObject | {46DB2BD0-E051-4696-94D6-2FA44FB23EF0} |  |
| e-data-attachment | Attachment Record | DataObject | {EE5F9D62-90F4-4069-A4E5-E58FC61EFED6} |  |
| e-data-article | Article Record | DataObject | {6C92F5B2-A90C-4ef3-9661-0E18AE75FC3D} |  |
| e-data-newsletter | Newsletter Record | DataObject | {DCD4A099-4B92-4eac-858A-5DA0D7E856DD} |  |
| e-data-license | License Record | DataObject | {BAD06CC0-2637-4571-BB26-2A58184511BB} |  |
| e-data-lineitem | License Line Item Record | DataObject | {C708871A-BF1E-4850-982A-225767663A01} |  |
| e-data-purchase | Purchase Record | DataObject | {E2E773D8-9AEC-4d60-B9C5-846D8089C3EF} |  |
| e-data-offer | Offer Record | DataObject | {B373BD91-00B4-4f7b-B4CA-FB5C5D358242} |  |
| e-data-quote | Quote Record | DataObject | {11E659C8-90BF-44b4-B238-02D82C712A4B} |  |
| e-data-delivery | Delivery Record | DataObject | {F80B301A-8733-4d3a-B1FA-63A280A103F2} |  |
| e-data-salesinvoice | Sales Invoice Record | DataObject | {41B47389-BBD7-4318-B4C8-568A50BFF785} |  |
| e-data-procurementinvoice | Procurement Invoice Record | DataObject | {3EA49FBC-5E7D-40fb-8E67-E14C2C9BDC8E} |  |
| e-data-service | Service Record | DataObject | {CBC8C8B9-33AE-4acc-8898-B4E7DFB51CE9} |  |
| e-data-vendor | Vendor Record | DataObject | {77B7FEB3-2C8B-43af-B96D-52C712C65DDD} |  |
| e-node-nas | QNAP NAS | Node | {303FAF28-0D71-477a-B47D-A6441D733987} |  |
| e-device-nas | QNAP Hardware | Device | {47F29442-0623-444b-9ABF-02A20C0B0952} |  |
| e-sw-django | Django 6.x + Python 3.13 | SystemSoftware | {427A3B98-729E-4786-A3D3-12AED32882C7} |  |
| e-sw-sqlite | SQLite | SystemSoftware | {ABCEFDBE-A210-40e0-85B3-79A07424BA2D} |  |
| e-sw-container | Docker (Container Station) | SystemSoftware | {D20DF3AB-6F1D-4a04-BEDC-F9ACE6FEE412} |  |
| e-art-dockerfile | Dockerfile | Artifact | {92AC4198-AD07-4675-8476-0D7B2F703C0F} |  |
| e-art-db | SQLite Database File | Artifact | {1C510B32-2870-4999-8F6E-8FEC974DB94C} |  |
| r-cust-pri | Association | Association | {FA43B17B-BB74-4599-9CAD-6C98E2BA6CCF} |  |
| r-cust-pur | Association | Association | {C80A7EC2-69A8-4cff-88EC-3FDBD036445D} |  |
| r-cust-sal | Association | Association | {12B9A805-79A8-41a4-882A-AE0ED80412A5} |  |
| r-cust-lic | Association | Association | {4A9D4919-0698-4d8f-A388-E1C04A9F3AC2} |  |
| r-comp-insight-imap | Composition | Composition | {4C8FB42A-6B9C-41eb-AFAA-1DE829A8DBC3} |  |
| r-comp-insight-parse | Composition | Composition | {CE385CE7-0DBA-4308-AD68-EBDA3EBC7CF4} |  |
| r-comp-newsletter-scrape | Composition | Composition | {20227EDF-2646-4b71-BF91-516923F6158E} |  |
| r-comp-newsletter-compose | Composition | Composition | {712E199E-6D11-466e-BD19-E4CCFAF0DBD4} |  |
| r-comp-newsletter-review | Composition | Composition | {1204CD5C-DC65-410a-ADB2-B9032DE959E4} |  |
| r-comp-newsletter-send | Composition | Composition | {B681E675-47E1-430e-93CB-FF6C9C962E92} |  |
| r-comp-newsletter-optin | Composition | Composition | {933D6418-472D-4bcf-A567-8E179C30FF5B} |  |
| r-access-imap-cust | Access | Access | {F210256F-A011-4cee-B561-7920AD0A8E0A} |  |
| r-access-imap-cont | Access | Access | {A991DB9B-8783-4aff-89A9-6879AD74A813} |  |
| r-access-imap-comm | Access | Access | {463ADE1E-3266-4873-B4F5-B4426C7131C8} |  |
| r-access-parse-doc | Access | Access | {F306941A-6467-40bd-8EB3-9559E659E0F4} |  |
| r-access-parse-lic | Access | Access | {840CBFA4-1737-4160-86C4-C58A4E5BC2EC} |  |
| r-access-parse-lli | Access | Access | {41768CE8-A5BF-4139-A59E-B58C577238B8} |  |
| r-access-compose-news | Access | Access | {3F467112-86E2-4c76-B604-A1432FA854A3} |  |
| r-access-send-news | Access | Access | {1DDD23E7-2AF4-4240-927D-5B3CDCBB6286} |  |
| r-assign-svc-customer | Assignment | Assignment | {AC2F378A-4258-4c1b-85A1-1F7A9AB768B0} |  |
| r-assign-svc-imap | Assignment | Assignment | {301CE967-EEFF-4fcf-A936-1FA990A44B35} |  |
| r-assign-svc-parse | Assignment | Assignment | {27C24A11-5602-4a15-A734-69B427F35FE8} |  |
| r-assign-svc-scrape | Assignment | Assignment | {381A1575-499E-4ccd-826C-6F7420D66B38} |  |
| r-assign-svc-newsletter | Assignment | Assignment | {C911E58E-0D7F-4b87-85DE-402895114CF1} |  |
| r-flow-cust-data | Flow | Flow | {43C9F566-1A6F-45a6-88DE-D1A370BD7D19} |  |
| r-flow-cont-data | Flow | Flow | {A183BCDC-AE1E-4571-9A75-FB967410EAD5} |  |
| r-flow-imap-data | Flow | Flow | {DFAD9891-6866-4ae4-9B4A-85D8C8E5E35E} |  |
| r-flow-parse-data | Flow | Flow | {451D076D-F1ED-43f8-A033-25B8A2177E02} |  |
| r-flow-scrape-data | Flow | Flow | {C1CA7B8C-B99B-457b-B86D-9BA9C4E5F36C} |  |
| r-flow-newsletter-data | Flow | Flow | {45D59D37-2B67-455d-B8DA-E6DA8C9796CC} |  |
| r-flow-parse-lic | Flow | Flow | {5C0C097C-DC8C-440c-8B88-C69264C5B52A} |  |
| r-flow-parse-lli | Flow | Flow | {6CEE844A-E4CE-4b4d-9D73-08A0FCE41B79} |  |
| r-flow-cust-purch | Flow | Flow | {EEFAF3D4-B2F8-4fc3-BD6E-99A5024F144D} |  |
| r-realize-svc-cust-imap | Realization | Realization | {9AD2B932-0A57-4615-8AF4-C6D14EF6E4D4} |  |
| r-realize-svc-imap-imap | Realization | Realization | {F142A7A4-9E03-41d5-B85A-2AA67DB73745} |  |
| r-realize-svc-cust-createaccount | Realization | Realization | {8E65FCAD-0902-4230-A62F-547C8A34856B} |  |
| r-realize-svc-cust-dedupe | Realization | Realization | {64521C64-B4E2-42e5-AE90-6BBD2A96A9B3} |  |
| r-realize-svc-cust-merge | Realization | Realization | {B8034EE4-8769-4e1c-AB3B-1C8B2CA2F2FB} |  |
| r-realize-svc-cust-emailhistory | Realization | Realization | {6CF2917A-3A62-400d-BED8-D41A15211A29} |  |
| r-realize-svc-imap-emailhistory | Realization | Realization | {E2853592-667B-4da1-B230-9C02C9B5075C} |  |
| r-realize-svc-parse-parse | Realization | Realization | {CA038C29-D471-46b8-A6D5-5A5F8C7A3F66} |  |
| r-realize-svc-scrape-scrape | Realization | Realization | {56F0D9E0-6360-4344-A774-49A4856D7332} |  |
| r-realize-svc-news-compose | Realization | Realization | {00686521-84DE-42cf-A41C-E9CC8236CD42} |  |
| r-realize-svc-news-review | Realization | Realization | {C26DC231-406B-4438-BFDC-DD39DF1C9D5B} |  |
| r-realize-svc-news-send | Realization | Realization | {0A0BEF3E-0277-4be0-97DE-71E296C48BFF} |  |
| r-realize-svc-cust-optin | Realization | Realization | {61A4757B-3435-4fc4-AF75-751F438A1FF3} |  |
| r-realize-data-cust-bo | Realization | Realization | {033A0499-BE3E-4851-AAD7-92688A122D81} |  |
| r-realize-data-contact-bo | Realization | Realization | {C5E58162-731F-4577-97E1-1A727E0988A2} |  |
| r-realize-data-email-bo | Realization | Realization | {2E97DAD8-7B70-4623-8DF8-E3AF9FFCEBDC} |  |
| r-realize-data-attach-bo | Realization | Realization | {5FA0AC7A-C5BD-4d51-8304-027DAA80C8D2} |  |
| r-realize-data-article-bo | Realization | Realization | {57E20FD7-DE53-4687-A800-AB65A0C9D0B2} |  |
| r-realize-data-newsletter-bo | Realization | Realization | {8469B90D-3477-4d41-B0A1-8851D8D19A6F} |  |
| r-realize-data-license-bo | Realization | Realization | {E0AD4990-EB52-487a-8EBB-EED4355108B5} |  |
| r-realize-data-lineitem-bo | Realization | Realization | {0D89CC1D-76F6-461d-809F-2E702E1B1DE7} |  |
| r-realize-data-purchase-bo | Realization | Realization | {D92B6820-40D1-4fa2-BA6C-46BECA99E964} |  |
| r-comp-node-device | Composition | Composition | {46AF5D98-DE9D-45ce-A34A-7C5C05227AC2} |  |
| r-assign-sw-django | Assignment | Assignment | {97775862-2140-4269-A753-8A9CA5C6C2BA} |  |
| r-assign-sw-sqlite | Assignment | Assignment | {2D02D6F8-4131-4775-B741-D33C7DE8C99F} |  |
| r-assign-sw-container | Assignment | Assignment | {A50E02A7-0101-4237-AEA7-C2F6AAF2DDF2} |  |
| r-realize-sw-django-app | Realization | Realization | {C0BCC244-EFD0-45ec-870D-D88888DDBF06} |  |
| r-realize-art-db-sw | Realization | Realization | {FFA5E413-11E1-4cae-A595-DD4B6422BA1E} |  |
| r-realize-art-docker-sw | Realization | Realization | {0BFC73D6-4449-4ac7-88A4-4A4E65198F2B} |  |
| r-comp-sales-rfq | Composition | Composition | {4F1E0C5E-0B89-4ba3-B963-6EBFA5AE015D} |  |
| r-comp-sales-offer | Composition | Composition | {68A010A5-924B-401b-87F3-ED32E4A7301B} |  |
| r-comp-sales-procure | Composition | Composition | {359B44BF-B598-46ea-9773-DDAFA7749F54} |  |
| r-comp-sales-deliver | Composition | Composition | {63492D0D-2967-4198-90E4-E03DF73F4E2A} |  |
| r-comp-sales-invoice | Composition | Composition | {5E87FE03-B9FA-4e12-91E9-5E73507B6CE2} |  |
| r-comp-account-create | Composition | Composition | {BB88FCE6-B4D4-4358-A785-C274B02C8805} |  |
| r-comp-account-dedupe | Composition | Composition | {2D477CC0-47A2-4a35-9D92-142A7F4AAD16} |  |
| r-comp-account-merge | Composition | Composition | {29EF0918-3665-4b9b-B4B6-0C9F47394C35} |  |
| r-comp-account-emailhistory | Composition | Composition | {9022444A-FCC3-4f74-A4E3-D1258325CD8E} |  |
| r-comp-account-optinsuggest | Composition | Composition | {20DEFD80-EC8F-4d12-BE38-515F19E1B518} |  |
| r-access-rfq-quote | Access | Access | {4032080F-871D-4a81-B6C8-6F00224ADC95} |  |
| r-access-createaccount-customer | Access | Access | {3F0F3CBA-713B-4055-8E34-B4E6E2AA8B4B} |  |
| r-access-createaccount-contact | Access | Access | {B83CAB70-19E6-4de5-88B9-FCAE0D6D10B8} |  |
| r-access-dedupe-customer | Access | Access | {1D67D73E-8D1A-4707-97DC-90EEACE5778C} |  |
| r-access-merge-customer | Access | Access | {B7FB493C-D3AB-4ed2-AA44-8EFA262A8299} |  |
| r-access-merge-contact | Access | Access | {26F9A18D-47E5-4081-B99F-2567A5EE064F} |  |
| r-access-emailhistory-communication | Access | Access | {293A7A65-2332-4092-9C68-7A0B240E02CC} |  |
| r-access-dedupe-contact | Access | Access | {48C62950-C494-4ca1-9E1B-F7A8D3E524A2} |  |
| r-access-emailhistory-contact | Access | Access | {366B728A-E0CA-49bc-9CAC-F5133DF2F06E} |  |
| r-access-optinsuggest-contact | Access | Access | {7F64BF5B-A070-4402-9199-B52BEF206D50} |  |
| r-trigger-rfq-createaccount | Triggering | Triggering | {6CF08CAD-B268-4588-A8D8-406340CF08BF} |  |
| r-access-offer-offer | Access | Access | {D368BF88-3083-411f-BB03-B799515199CD} |  |
| r-access-offer-service | Access | Access | {ED4D4AF9-5DB9-49b5-9ED9-2CEE6DE8A31E} |  |
| r-access-procure-quote | Access | Access | {A2C42891-BD3A-4bc3-93A5-38CA78B1BB18} |  |
| r-access-procure-vendor | Access | Access | {07C9CB83-6666-4c9a-973E-354F22451B09} |  |
| r-access-deliver-delivery | Access | Access | {1F78BD2A-0BE9-4d3c-8744-87B77D07EBF2} |  |
| r-access-invoice-salesinv | Access | Access | {61CBB23E-2F55-415d-A72C-443167620C0D} |  |
| r-access-invoice-procinv | Access | Access | {01DB5AB0-08DC-4076-8F20-897D2D43C45E} |  |
| r-access-invoice-purchase | Access | Access | {32D14077-2747-4a5e-970A-5795DBB259DB} |  |
| r-assign-svc-sales | Assignment | Assignment | {A2A4F92C-8D8B-4acf-8606-56EF66403969} |  |
| r-flow-sales-offer | Flow | Flow | {266C6CB7-594E-4b48-8050-EC41776A59D7} |  |
| r-flow-sales-quote | Flow | Flow | {21BF84D3-A2EA-4934-ACE6-F4AC8F5634CE} |  |
| r-flow-sales-delivery | Flow | Flow | {FBBF72CE-AC07-4f98-977B-8DCB89B16E74} |  |
| r-flow-sales-salesinv | Flow | Flow | {875C5E5C-7B22-4bf0-A2DC-A9508DC5D800} |  |
| r-flow-sales-procinv | Flow | Flow | {DBE3F4A6-58C9-4894-86AF-1BFD0C28B043} |  |
| r-flow-sales-service | Flow | Flow | {C8290318-B825-40ba-8C2B-1245FBB0B89D} |  |
| r-flow-sales-vendor | Flow | Flow | {B677A545-3741-4e08-800E-7A3E8C244C2A} |  |
| r-realize-svc-rfq | Realization | Realization | {58197EF5-A441-407f-B1D5-725CD1A3645E} |  |
| r-realize-svc-offer | Realization | Realization | {05330DE4-821C-4c84-B655-7FE8353CAB94} |  |
| r-realize-svc-procure | Realization | Realization | {E7B1712B-C0DE-4cea-8225-9AA5C073007E} |  |
| r-realize-svc-deliver | Realization | Realization | {7D0D51A9-FCE0-4c5f-9714-B86F257FE5A1} |  |
| r-realize-svc-invoice | Realization | Realization | {AC02D002-F2DF-41b1-AE23-4906E5A70E5D} |  |
| r-realize-data-offer-bo | Realization | Realization | {3050A38D-1D8C-4903-A41B-C5DE6EFE3695} |  |
| r-realize-data-quote-bo | Realization | Realization | {615236D5-3687-4fce-B020-D70CAD1CC5A9} |  |
| r-realize-data-delivery-bo | Realization | Realization | {BF3591DE-E762-4cc9-9A4B-93F909797094} |  |
| r-realize-data-salesinv-bo | Realization | Realization | {C4AB9BC5-2ED6-4dfd-B38A-E04A173EC2C5} |  |
| r-realize-data-procinv-bo | Realization | Realization | {E22621B7-16AC-47dc-A16B-DC7F4035CE72} |  |
| r-realize-data-service-bo | Realization | Realization | {8223BD91-E99D-4d67-875C-DAB49A0763BF} |  |
| r-realize-data-vendor-bo | Realization | Realization | {B4E8B867-13FC-4f05-9575-95068C226DCF} |  |

