## 2026-07-06 14:48:23 — Audit

### Checkpoints
- Sync from EA

## 2026-07-06 14:44:17 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| article | Article | Class | {A8A1C7F5-AB9E-477d-82C1-96C80B5C9F42} |  |
| attachment | Attachment | Class | {7166AEE8-CF2D-4372-BC23-068A510B0124} |  |
| communication | Communication | Class | {94C6CD4B-43EF-4e8d-A190-EC98D38FF05B} |  |
| contact | Contact | Class | {DEF8F388-8B44-4425-9F79-7FE63A4C6A0E} |  |
| customer | Customer | Class | {700996C9-A075-4773-9696-9C9C89125192} |  |
| delivery | Delivery | Class | {0CB6B189-C3BB-4eb4-9E09-DC17356387D7} |  |
| imapaccount | ImapAccount | Class | {3BD8E116-FF59-4ce7-B1DA-F3B3D854FD53} |  |
| license | License | Class | {B9E262AA-8193-4c39-B5B8-38AF63395457} |  |
| licenselineitem | LicenseLineItem | Class | {1C8F5735-6BF1-4461-819D-2B729F60AD46} |  |
| newsletter | Newsletter | Class | {AE7A31BB-F127-4567-AC90-1275F4DFDF2B} |  |
| newslettercontact | NewsletterContact | Class | {C59F7286-C6EC-4a02-8CA1-E8F24BC7DA65} |  |
| newssource | NewsSource | Class | {4381BA0B-6FDB-4af5-A6DC-B71AFD2F0E12} |  |
| offer | Offer | Class | {67448211-42F0-4105-97D5-4B065E0148E4} |  |
| procurementinvoice | ProcurementInvoice | Class | {3A60FD60-3797-41df-8BED-20A2148B32F5} |  |
| purchase | Purchase | Class | {E16E85CB-5C83-403e-B2FC-517E644EFFC1} |  |
| quote | Quote | Class | {5C91AF36-E5D9-43aa-BE25-C75405EF7557} |  |
| salesinvoice | SalesInvoice | Class | {B021AB28-9E3D-43b2-B5DB-D714BF7057F0} |  |
| service | Service | Class | {BBA9619D-9886-4ae6-B9E3-BE69D5959DFB} |  |
| vendor | Vendor | Class | {5AA443A4-1DA9-4417-8F5C-316C4238C9BB} |  |
| r-contact-customer | Contact -> Customer | Association | {C9CA64AF-AFAE-4d9a-9EF9-2014013769F5} |  |
| r-communication-imapaccount | Communication -> ImapAccount | Association | {2676BB60-3D47-4de3-96BC-4D20293529F5} |  |
| r-attachment-communication | Attachment -> Communication | Association | {FA6FAD91-7BCF-4ee5-AF68-64E54104BF93} |  |
| r-article-newssource | Article -> NewsSource | Association | {8341222A-BF61-42f4-A635-37C1DD32DC82} |  |
| r-article-newsletter | Article -> Newsletter | Association | {48E2FEB9-37B8-4165-A2FD-DE27E7C538C6} |  |
| r-newslettercontact-newsletter | NewsletterContact -> Newsletter | Association | {35628AA4-C765-40bd-8CC4-ACD9186AB74A} |  |
| r-newslettercontact-contact | NewsletterContact -> Contact | Association | {43479F65-F6DA-4335-A2C7-AEB3FA2CB947} |  |
| r-purchase-customer | Purchase -> Customer | Association | {005D5D29-0CDA-4b1e-962B-0ED9E2AACA7E} |  |
| r-purchase-quote | Purchase -> Quote | Association | {7200B9F1-1AAA-4032-98C6-B4765443EA80} |  |
| r-purchase-procurementinvoice | Purchase -> ProcurementInvoice | Association | {A4A6C418-1F9B-44a8-9052-8765271B7C7A} |  |
| r-license-customer | License -> Customer | Association | {089753EB-B3EF-43aa-A242-08921CDF4DE4} |  |
| r-license-purchase | License -> Purchase | Association | {70E45BC5-BD6B-499b-A5BE-34929E9D5C8B} |  |
| r-license-procurementinvoice | License -> ProcurementInvoice | Association | {937308B4-849A-444f-8129-1E2E7D04DD92} |  |
| r-license-license | License -> License | Association | {12777B6B-618F-4b07-9ED2-2C914402AF57} |  |
| r-licenselineitem-license | LicenseLineItem -> License | Association | {136C85F5-62C6-412a-8860-DCBC2E2A0378} |  |
| r-license-attachment | License -> Attachment | Association | {4B8D0033-C3D1-4201-BEA7-6603066E0229} |  |
| r-service-purchase | Service -> Purchase | Association | {8AAE733E-308E-40db-B07D-64A7E08D442D} |  |
| r-service-offer | Service -> Offer | Association | {13EA23A1-B91B-4ce0-AED7-7375E00FBF2F} |  |
| r-service-salesinvoice | Service -> SalesInvoice | Association | {9E02A6B2-34E5-46d4-8F6C-53E51F270E3F} |  |
| r-offer-customer | Offer -> Customer | Association | {6EADD078-EE1D-4034-A7E4-20BD81283F51} |  |
| r-salesinvoice-customer | SalesInvoice -> Customer | Association | {6DAB0EF7-1339-4aa8-BCB0-48AA5D774D4F} |  |
| r-salesinvoice-offer | SalesInvoice -> Offer | Association | {D2F37FB6-BCBA-492d-B67A-8B18E6DDC3F5} |  |
| r-service-vendor | Service -> Vendor | Association | {6DA30258-ACFE-4f0b-BEDF-65D801E9EF7B} |  |
| r-vendor-license | Vendor -> License | Association | {A9E35378-A873-4e12-BD07-9F63FE9AC5EA} |  |
| r-vendor-procurementinvoice | Vendor -> ProcurementInvoice | Association | {86C1E584-1F6C-4479-8BA0-CF0B3E309E07} |  |
| r-vendor-quote | Vendor -> Quote | Association | {79C894B6-9D84-4efb-A6A0-EBC1654E95AF} |  |
| r-attachment-delivery | Attachment -> Delivery | Association | {1F1B9287-E051-4747-83CF-AD42A7ADCACE} |  |
| r-delivery-customer | Delivery -> Customer | Association | {D9841B6E-10CB-4dba-843E-F05C3A697548} |  |
| r-delivery-salesinvoice | Delivery -> SalesInvoice | Association | {EE282559-8C02-4e00-B124-F64B3114CFA4} |  |
| r-license-salesinvoice | License -> SalesInvoice | Association | {0619E0BA-35D5-412d-9A65-691A9ED3CA4F} |  |
| r-customer-customer | Customer -> Customer | Association | {985DAD01-075E-4c1f-BF06-FC38270912D2} |  |

