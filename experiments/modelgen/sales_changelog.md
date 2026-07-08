## 2026-07-06 22:03:33 — Audit, run sp-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| StartRFQ_CreateRFQ | StartRFQ -> CreateRFQ | SequenceFlow |  |
| RegisterRFQ_PrepareRevisedOffer | RegisterRFQ -> PrepareRevisedOffer | SequenceFlow |  |
| PrepareRevisedOffer_DetermineServices | PrepareRevisedOffer -> DetermineServices | SequenceFlow |  |
| DetermineLicenses_licensesrequired | DetermineLicenses -> licensesrequired | SequenceFlow |  |
| servicesrequired_RequestServiceQuote | servicesrequired -> RequestServiceQuote | SequenceFlow |  |
| servicesrequired_FinaliseVersionofOffer | servicesrequired -> FinaliseVersionofOffer | SequenceFlow |  |
| ReviewOffer_AcceptOfferGateway | ReviewOffer -> AcceptOfferGateway | SequenceFlow |  |
| AcceptOfferGateway_AcceptOfferActivity | AcceptOfferGateway -> AcceptOfferActivity | SequenceFlow |  |
| HandleApprovedOffer_RequestLicenses | HandleApprovedOffer -> RequestLicenses | SequenceFlow |  |
| HandleApprovedOffer_RequestServices | HandleApprovedOffer -> RequestServices | SequenceFlow |  |
| RequestLicenses_PrepareDelivery | RequestLicenses -> PrepareDelivery | SequenceFlow |  |
| RequestServices_PrepareDelivery | RequestServices -> PrepareDelivery | SequenceFlow |  |
| AcceptDelivery_ActivateDelivery | AcceptDelivery -> ActivateDelivery | SequenceFlow |  |
| ValidatePayment_checkpayment | ValidatePayment -> checkpayment | SequenceFlow |  |
| checkpayment_EndSales | checkpayment -> EndSales | SequenceFlow |  |
| AcceptOfferGateway_RequestRevisedOffer | AcceptOfferGateway -> RequestRevisedOffer | SequenceFlow |  |
| AcceptOfferGateway_RejectOffer | AcceptOfferGateway -> RejectOffer | SequenceFlow |  |
| RequestRevisedOffer_PrepareRevisedOffer | RequestRevisedOffer -> PrepareRevisedOffer | SequenceFlow |  |
| HandleRejectedOffer_EndRejectedSales | HandleRejectedOffer -> EndRejectedSales | SequenceFlow |  |
| PrepareRevisedOffer_DetermineLicenses | PrepareRevisedOffer -> DetermineLicenses | SequenceFlow |  |
| checkpayment_RemindPayment | checkpayment -> RemindPayment | SequenceFlow |  |
| DetermineServices_servicesrequired | DetermineServices -> servicesrequired | SequenceFlow |  |
| licensesrequired_FinaliseVersionofOffer | licensesrequired -> FinaliseVersionofOffer | SequenceFlow |  |
| licensesrequired_RequestLicenseQuote | licensesrequired -> RequestLicenseQuote | SequenceFlow |  |
| ConfirmCustomerAccount_RegisterRFQ | ConfirmCustomerAccount -> RegisterRFQ | SequenceFlow |  |
| CreateRFQ_RegisterRFQ | CreateRFQ -> RegisterRFQ | MessageFlow |  |
| PrepareLicenseQuote_RequestLicenseQuote | PrepareLicenseQuote -> RequestLicenseQuote | MessageFlow |  |
| FinaliseVersionofOffer_ReviewOffer | FinaliseVersionofOffer -> ReviewOffer | MessageFlow |  |
| AcceptOfferActivity_HandleApprovedOffer | AcceptOfferActivity -> HandleApprovedOffer | MessageFlow |  |
| RequestLicenses_ProvideLicenses | RequestLicenses -> ProvideLicenses | MessageFlow |  |
| RequestServices_ProvideServices | RequestServices -> ProvideServices | MessageFlow |  |
| PrepareDelivery_AcceptDelivery | PrepareDelivery -> AcceptDelivery | MessageFlow |  |
| ProvideServices_PrepareDelivery | ProvideServices -> PrepareDelivery | MessageFlow |  |
| ProvideLicenses_PrepareDelivery | ProvideLicenses -> PrepareDelivery | MessageFlow |  |
| ActivateDelivery_PrepareSalesInvoice | ActivateDelivery -> PrepareSalesInvoice | MessageFlow |  |
| PrepareSalesInvoice_PaySalesInvoice | PrepareSalesInvoice -> PaySalesInvoice | MessageFlow |  |
| PaySalesInvoice_ValidatePayment | PaySalesInvoice -> ValidatePayment | MessageFlow |  |
| RemindPayment_PaySalesInvoice | RemindPayment -> PaySalesInvoice | MessageFlow |  |
| RequestServiceQuote_PrepareServiceQuote | RequestServiceQuote -> PrepareServiceQuote | MessageFlow |  |
| PrepareServiceQuote_RequestServiceQuote | PrepareServiceQuote -> RequestServiceQuote | MessageFlow |  |
| RejectOffer_HandleRejectedOffer | RejectOffer -> HandleRejectedOffer | MessageFlow |  |
| RequestLicenseQuote_PrepareLicenseQuote | RequestLicenseQuote -> PrepareLicenseQuote | MessageFlow |  |
| CreateRFQ_ConfirmCustomerAccount | CreateRFQ -> ConfirmCustomerAccount | MessageFlow |  |
| RFQ_RegisterRFQ | RFQ -> RegisterRFQ | DataInputAssociation |  |
| Offer_ReviewOffer | Offer -> ReviewOffer | DataInputAssociation |  |
| LicenseQuote_RequestLicenseQuote | LicenseQuote -> RequestLicenseQuote | DataInputAssociation |  |
| PurchaseOrder_HandleApprovedOffer | PurchaseOrder -> HandleApprovedOffer | DataInputAssociation |  |
| ServiceQuote_RequestServiceQuote | ServiceQuote -> RequestServiceQuote | DataInputAssociation |  |
| LicenseDocument_PrepareDelivery | LicenseDocument -> PrepareDelivery | DataInputAssociation |  |
| ServiceDocument_PrepareDelivery | ServiceDocument -> PrepareDelivery | DataInputAssociation |  |
| LicenseInvoice_PrepareSalesInvoice | LicenseInvoice -> PrepareSalesInvoice | DataInputAssociation |  |
| ServiceInvoice_PrepareSalesInvoice | ServiceInvoice -> PrepareSalesInvoice | DataInputAssociation |  |
| SalesInvoice_PaySalesInvoice | SalesInvoice -> PaySalesInvoice | DataInputAssociation |  |
| Payment_ValidatePayment | Payment -> ValidatePayment | DataInputAssociation |  |
| CreateRFQ_RFQ | CreateRFQ -> RFQ | DataOutputAssociation |  |
| FinaliseVersionofOffer_Offer | FinaliseVersionofOffer -> Offer | DataOutputAssociation |  |
| PrepareLicenseQuote_LicenseQuote | PrepareLicenseQuote -> LicenseQuote | DataOutputAssociation |  |
| AcceptOfferActivity_PurchaseOrder | AcceptOfferActivity -> PurchaseOrder | DataOutputAssociation |  |
| PrepareServiceQuote_ServiceQuote | PrepareServiceQuote -> ServiceQuote | DataOutputAssociation |  |
| ProvideLicenses_LicenseDocument | ProvideLicenses -> LicenseDocument | DataOutputAssociation |  |
| ProvideServices_ServiceDocument | ProvideServices -> ServiceDocument | DataOutputAssociation |  |
| ProvideLicenses_LicenseInvoice | ProvideLicenses -> LicenseInvoice | DataOutputAssociation |  |
| ProvideServices_ServiceInvoice | ProvideServices -> ServiceInvoice | DataOutputAssociation |  |
| PrepareSalesInvoice_SalesInvoice | PrepareSalesInvoice -> SalesInvoice | DataOutputAssociation |  |
| PaySalesInvoice_Payment | PaySalesInvoice -> Payment | DataOutputAssociation |  |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| EAxCRMSalesProcessArchitecture | EAxCRM Sales Process Architecture | CollaborationModel | {6ACCD057-B99E-48a4-8BE0-AC1FCC601245} |  |
| Customer | Customer | Lane | {D78E6C97-1010-40da-8A34-28B2A84F29D6} |  |
| EAxpertise | EAxpertise | Lane | {0D1DE3F6-9F36-4387-901D-5E82190C78A4} |  |
| Vendor | Vendor | Lane | {4CE7A835-2E5A-4392-ACA7-2A54C08DA636} |  |
| AcceptDelivery | Accept Delivery | Activity | {863E019F-D8AA-4a29-AC98-9A5E9BC1DE9E} |  |
| AcceptOfferActivity | Accept Offer | Activity | {AAF91171-3C57-46bb-B549-0BE31011BA78} |  |
| AcceptOfferGateway | Accept Offer? | Gateway | {48A6D2C0-48A8-41c7-9B44-28B014D9A5E4} |  |
| ActivateDelivery | Activate Delivery | Activity | {F1FA7EC6-06B5-41cc-BAFC-1DCD1EDE3B27} |  |
| checkpayment | check payment | IntermediateEvent | {B6F6A5F0-31B9-4876-AB37-29EB93616701} |  |
| ConfirmCustomerAccount | Confirm Customer Account | IntermediateEvent | {AD32AD89-C0CA-4001-ACFB-56C1F46601AC} |  |
| CreateRFQ | Create RFQ | Activity | {8078EDB0-256C-4dd4-8810-573EAA0F0B0B} |  |
| DetermineLicenses | Determine Licenses | Activity | {F1B9706F-D357-48a3-BA36-4AAF2618F4A4} |  |
| DetermineServices | Determine Services | Activity | {52A9A807-5186-4dcd-ABC4-2F48A42DC2E4} |  |
| EndRejectedSales | End Rejected Sales | EndEvent | {32ADEDC2-2890-40b6-A489-51A28FA5AC67} |  |
| EndSales | End Sales | EndEvent | {AC4B3F30-5771-4426-8445-30325797259B} |  |
| FinaliseVersionofOffer | Finalise Version of Offer | Activity | {8C9B0572-1DB2-4bdd-9D33-D8A279C87BE0} |  |
| HandleApprovedOffer | Handle Approved Offer | Activity | {01C496AC-DFE7-4ea9-B482-1E95EF851677} |  |
| HandleRejectedOffer | Handle Rejected Offer | Activity | {CC8DB595-33FA-423a-A7BB-E2C32C478029} |  |
| LicenseDocument | License Document | DataObject | {B5EBA936-39BC-4694-858E-2474715E89E0} |  |
| LicenseInvoice | License Invoice | DataObject | {C206CCD5-D481-40b3-BA1C-18FFD705326E} |  |
| LicenseQuote | License Quote | DataObject | {6C0747AF-BB4C-4885-BAF6-4FC496E23590} |  |
| licensesrequired | licenses required? | Gateway | {137E4E47-AE30-4019-AFB4-F5848F6C75E7} |  |
| Offer | Offer | DataObject | {CB5267A2-D848-4021-A26E-DDB979177C3A} |  |
| PaySalesInvoice | Pay SalesInvoice | Activity | {4E4972A7-0D2D-4135-BA47-2B403D9B8309} |  |
| Payment | Payment | DataObject | {332D8643-81C6-4b64-A250-E8898028D48E} |  |
| PrepareRevisedOffer | Prepare (Revised) Offer | Activity | {9C3B3106-2A1F-46ef-818F-374EC58FC6FB} |  |
| PrepareDelivery | Prepare Delivery | Activity | {677F24EF-13D2-43bc-A2EF-241AC495066E} |  |
| PrepareLicenseQuote | Prepare License Quote | Activity | {9D0A23BA-1725-473a-9C0D-D9BDAD113492} |  |
| PrepareSalesInvoice | Prepare SalesInvoice | Activity | {6BA1904F-38DB-4de6-A6D7-4377B1C95D3F} |  |
| PrepareServiceQuote | Prepare Service Quote | Activity | {2AFFF14D-B7CB-4200-843E-64C9993FD879} |  |
| ProvideLicenses | Provide Licenses | Activity | {656EB0F6-7CD3-403a-9FE7-B4CC7B29A86D} |  |
| ProvideServices | Provide Service(s) | Activity | {85628578-F197-45fd-8942-CC0812EFEEEF} |  |
| PurchaseOrder | Purchase Order | DataObject | {A9A7B62D-3F33-4b05-8239-DF34F4EF35FE} |  |
| RegisterRFQ | Register RFQ | Activity | {1E8282D2-3F1C-41ce-B8A5-671AAD90ACFC} |  |
| RejectOffer | Reject Offer | Activity | {F443524E-4717-4e31-9D4D-D01A05B478B6} |  |
| RemindPayment | Remind Payment | Activity | {6133EFAA-E2BB-4e3e-ACBF-5DC7BA76353F} |  |
| RequestLicenseQuote | Request License Quote | Activity | {54201F7E-AA1B-49bb-AB58-CE578A450AE4} |  |
| RequestLicenses | Request Licenses | Activity | {FA528F49-DC3F-4b41-8377-D9D2457F83C9} |  |
| RequestRevisedOffer | Request Revised Offer | Activity | {A1BAB8A5-7D52-47e6-9E90-4440D5D6EE88} |  |
| RequestServiceQuote | Request Service Quote | Activity | {71C21043-6571-451e-BFD8-B8901AA0EB81} |  |
| RequestServices | Request Services | Activity | {3ACC3D25-DD6F-43d9-80BB-66BC6EC18134} |  |
| ReviewOffer | Review Offer | Activity | {997B9124-402C-42ee-9A11-03E89D90DF86} |  |
| RFQ | RFQ | DataObject | {76AD2E52-11A3-4657-8F06-F937D33F3C19} |  |
| SalesInvoice | Sales Invoice | DataObject | {E47CCCC5-9862-4bde-A10D-7AFE0D040DFA} |  |
| ServiceDocument | Service Document | DataObject | {9651C011-400C-4d72-9689-35FC5CC0DF2D} |  |
| ServiceInvoice | Service Invoice | DataObject | {D47CACA8-4CFE-44f4-829E-E9C4785A8D99} |  |
| ServiceQuote | Service Quote | DataObject | {117B4799-A108-4e69-BCF6-6BCF203A4EEC} |  |
| servicesrequired | services required? | Gateway | {4DDEC500-6564-4478-BEF0-982F04F01488} |  |
| StartRFQ | Start RFQ | StartEvent | {94A14FAC-00B9-43fc-B10E-9FABE868C74C} |  |
| ValidatePayment | Validate Payment | Activity | {6BF00CC4-39CF-4db4-A20B-06D3A43AC93F} |  |

## 2026-07-06 14:22:47 — Audit, run sp-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| StartRFQ_CreateRFQ | StartRFQ -> CreateRFQ | SequenceFlow |  |
| ConfirmCustomerAccount_RegisterRFQ | ConfirmCustomerAccount -> RegisterRFQ | SequenceFlow |  |
| RegisterRFQ_PrepareRevisedOffer | RegisterRFQ -> PrepareRevisedOffer | SequenceFlow |  |
| PrepareRevisedOffer_DetermineServices | PrepareRevisedOffer -> DetermineServices | SequenceFlow |  |
| DetermineLicenses_licensesrequired | DetermineLicenses -> licensesrequired | SequenceFlow |  |
| servicesrequired_RequestServiceQuote | servicesrequired -> RequestServiceQuote | SequenceFlow |  |
| servicesrequired_FinaliseVersionofOffer | servicesrequired -> FinaliseVersionofOffer | SequenceFlow |  |
| ReviewOffer_AcceptOfferGateway | ReviewOffer -> AcceptOfferGateway | SequenceFlow |  |
| AcceptOfferGateway_AcceptOfferActivity | AcceptOfferGateway -> AcceptOfferActivity | SequenceFlow |  |
| HandleApprovedOffer_RequestLicenses | HandleApprovedOffer -> RequestLicenses | SequenceFlow |  |
| HandleApprovedOffer_RequestServices | HandleApprovedOffer -> RequestServices | SequenceFlow |  |
| RequestLicenses_PrepareDelivery | RequestLicenses -> PrepareDelivery | SequenceFlow |  |
| RequestServices_PrepareDelivery | RequestServices -> PrepareDelivery | SequenceFlow |  |
| AcceptDelivery_ActivateDelivery | AcceptDelivery -> ActivateDelivery | SequenceFlow |  |
| ValidatePayment_checkpayment | ValidatePayment -> checkpayment | SequenceFlow |  |
| checkpayment_EndSales | checkpayment -> EndSales | SequenceFlow |  |
| AcceptOfferGateway_RequestRevisedOffer | AcceptOfferGateway -> RequestRevisedOffer | SequenceFlow |  |
| AcceptOfferGateway_RejectOffer | AcceptOfferGateway -> RejectOffer | SequenceFlow |  |
| RequestRevisedOffer_PrepareRevisedOffer | RequestRevisedOffer -> PrepareRevisedOffer | SequenceFlow |  |
| HandleRejectedOffer_EndRejectedSales | HandleRejectedOffer -> EndRejectedSales | SequenceFlow |  |
| PrepareRevisedOffer_DetermineLicenses | PrepareRevisedOffer -> DetermineLicenses | SequenceFlow |  |
| checkpayment_RemindPayment | checkpayment -> RemindPayment | SequenceFlow |  |
| DetermineServices_servicesrequired | DetermineServices -> servicesrequired | SequenceFlow |  |
| licensesrequired_FinaliseVersionofOffer | licensesrequired -> FinaliseVersionofOffer | SequenceFlow |  |
| licensesrequired_RequestLicenseQuote | licensesrequired -> RequestLicenseQuote | SequenceFlow |  |
| CreateRFQ_ConfirmCustomerAccount | CreateRFQ -> ConfirmCustomerAccount | MessageFlow |  |
| PrepareLicenseQuote_RequestLicenseQuote | PrepareLicenseQuote -> RequestLicenseQuote | MessageFlow |  |
| FinaliseVersionofOffer_ReviewOffer | FinaliseVersionofOffer -> ReviewOffer | MessageFlow |  |
| AcceptOfferActivity_HandleApprovedOffer | AcceptOfferActivity -> HandleApprovedOffer | MessageFlow |  |
| RequestLicenses_ProvideLicenses | RequestLicenses -> ProvideLicenses | MessageFlow |  |
| RequestServices_ProvideServices | RequestServices -> ProvideServices | MessageFlow |  |
| PrepareDelivery_AcceptDelivery | PrepareDelivery -> AcceptDelivery | MessageFlow |  |
| ProvideServices_PrepareDelivery | ProvideServices -> PrepareDelivery | MessageFlow |  |
| ProvideLicenses_PrepareDelivery | ProvideLicenses -> PrepareDelivery | MessageFlow |  |
| ActivateDelivery_PrepareSalesInvoice | ActivateDelivery -> PrepareSalesInvoice | MessageFlow |  |
| PrepareSalesInvoice_PaySalesInvoice | PrepareSalesInvoice -> PaySalesInvoice | MessageFlow |  |
| PaySalesInvoice_ValidatePayment | PaySalesInvoice -> ValidatePayment | MessageFlow |  |
| RemindPayment_PaySalesInvoice | RemindPayment -> PaySalesInvoice | MessageFlow |  |
| RequestServiceQuote_PrepareServiceQuote | RequestServiceQuote -> PrepareServiceQuote | MessageFlow |  |
| PrepareServiceQuote_RequestServiceQuote | PrepareServiceQuote -> RequestServiceQuote | MessageFlow |  |
| RejectOffer_HandleRejectedOffer | RejectOffer -> HandleRejectedOffer | MessageFlow |  |
| RequestLicenseQuote_PrepareLicenseQuote | RequestLicenseQuote -> PrepareLicenseQuote | MessageFlow |  |
| RFQ_RegisterRFQ | RFQ -> RegisterRFQ | DataInputAssociation |  |
| Offer_ReviewOffer | Offer -> ReviewOffer | DataInputAssociation |  |
| LicenseQuote_RequestLicenseQuote | LicenseQuote -> RequestLicenseQuote | DataInputAssociation |  |
| PurchaseOrder_HandleApprovedOffer | PurchaseOrder -> HandleApprovedOffer | DataInputAssociation |  |
| ServiceQuote_RequestServiceQuote | ServiceQuote -> RequestServiceQuote | DataInputAssociation |  |
| LicenseDocument_PrepareDelivery | LicenseDocument -> PrepareDelivery | DataInputAssociation |  |
| ServiceDocument_PrepareDelivery | ServiceDocument -> PrepareDelivery | DataInputAssociation |  |
| LicenseInvoice_PrepareSalesInvoice | LicenseInvoice -> PrepareSalesInvoice | DataInputAssociation |  |
| ServiceInvoice_PrepareSalesInvoice | ServiceInvoice -> PrepareSalesInvoice | DataInputAssociation |  |
| SalesInvoice_PaySalesInvoice | SalesInvoice -> PaySalesInvoice | DataInputAssociation |  |
| Payment_ValidatePayment | Payment -> ValidatePayment | DataInputAssociation |  |
| CreateRFQ_RFQ | CreateRFQ -> RFQ | DataOutputAssociation |  |
| FinaliseVersionofOffer_Offer | FinaliseVersionofOffer -> Offer | DataOutputAssociation |  |
| PrepareLicenseQuote_LicenseQuote | PrepareLicenseQuote -> LicenseQuote | DataOutputAssociation |  |
| AcceptOfferActivity_PurchaseOrder | AcceptOfferActivity -> PurchaseOrder | DataOutputAssociation |  |
| PrepareServiceQuote_ServiceQuote | PrepareServiceQuote -> ServiceQuote | DataOutputAssociation |  |
| ProvideLicenses_LicenseDocument | ProvideLicenses -> LicenseDocument | DataOutputAssociation |  |
| ProvideServices_ServiceDocument | ProvideServices -> ServiceDocument | DataOutputAssociation |  |
| ProvideLicenses_LicenseInvoice | ProvideLicenses -> LicenseInvoice | DataOutputAssociation |  |
| ProvideServices_ServiceInvoice | ProvideServices -> ServiceInvoice | DataOutputAssociation |  |
| PrepareSalesInvoice_SalesInvoice | PrepareSalesInvoice -> SalesInvoice | DataOutputAssociation |  |
| PaySalesInvoice_Payment | PaySalesInvoice -> Payment | DataOutputAssociation |  |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| EAxCRMSalesProcessArchitecture | EAxCRM Sales Process Architecture | CollaborationModel | {6ACCD057-B99E-48a4-8BE0-AC1FCC601245} |  |
| Customer | Customer | Lane | {D78E6C97-1010-40da-8A34-28B2A84F29D6} |  |
| EAxpertise | EAxpertise | Lane | {0D1DE3F6-9F36-4387-901D-5E82190C78A4} |  |
| Vendor | Vendor | Lane | {4CE7A835-2E5A-4392-ACA7-2A54C08DA636} |  |
| AcceptDelivery | Accept Delivery | Activity | {863E019F-D8AA-4a29-AC98-9A5E9BC1DE9E} |  |
| AcceptOfferActivity | Accept Offer | Activity | {AAF91171-3C57-46bb-B549-0BE31011BA78} |  |
| AcceptOfferGateway | Accept Offer? | Gateway | {48A6D2C0-48A8-41c7-9B44-28B014D9A5E4} |  |
| ActivateDelivery | Activate Delivery | Activity | {F1FA7EC6-06B5-41cc-BAFC-1DCD1EDE3B27} |  |
| checkpayment | check payment | IntermediateEvent | {B6F6A5F0-31B9-4876-AB37-29EB93616701} |  |
| CreateRFQ | Create RFQ | Activity | {8078EDB0-256C-4dd4-8810-573EAA0F0B0B} |  |
| ConfirmCustomerAccount | Confirm Customer Account | IntermediateEvent | {AD32AD89-C0CA-4001-ACFB-56C1F46601AC} |  |
| DetermineLicenses | Determine Licenses | Activity | {F1B9706F-D357-48a3-BA36-4AAF2618F4A4} |  |
| DetermineServices | Determine Services | Activity | {52A9A807-5186-4dcd-ABC4-2F48A42DC2E4} |  |
| EndRejectedSales | End Rejected Sales | EndEvent | {32ADEDC2-2890-40b6-A489-51A28FA5AC67} |  |
| EndSales | End Sales | EndEvent | {AC4B3F30-5771-4426-8445-30325797259B} |  |
| FinaliseVersionofOffer | Finalise Version of Offer | Activity | {8C9B0572-1DB2-4bdd-9D33-D8A279C87BE0} |  |
| HandleApprovedOffer | Handle Approved Offer | Activity | {01C496AC-DFE7-4ea9-B482-1E95EF851677} |  |
| HandleRejectedOffer | Handle Rejected Offer | Activity | {CC8DB595-33FA-423a-A7BB-E2C32C478029} |  |
| LicenseDocument | License Document | DataObject | {B5EBA936-39BC-4694-858E-2474715E89E0} |  |
| LicenseInvoice | License Invoice | DataObject | {C206CCD5-D481-40b3-BA1C-18FFD705326E} |  |
| LicenseQuote | License Quote | DataObject | {6C0747AF-BB4C-4885-BAF6-4FC496E23590} |  |
| licensesrequired | licenses required? | Gateway | {137E4E47-AE30-4019-AFB4-F5848F6C75E7} |  |
| Offer | Offer | DataObject | {CB5267A2-D848-4021-A26E-DDB979177C3A} |  |
| PaySalesInvoice | Pay SalesInvoice | Activity | {4E4972A7-0D2D-4135-BA47-2B403D9B8309} |  |
| Payment | Payment | DataObject | {332D8643-81C6-4b64-A250-E8898028D48E} |  |
| PrepareRevisedOffer | Prepare (Revised) Offer | Activity | {9C3B3106-2A1F-46ef-818F-374EC58FC6FB} |  |
| PrepareDelivery | Prepare Delivery | Activity | {677F24EF-13D2-43bc-A2EF-241AC495066E} |  |
| PrepareLicenseQuote | Prepare License Quote | Activity | {9D0A23BA-1725-473a-9C0D-D9BDAD113492} |  |
| PrepareSalesInvoice | Prepare SalesInvoice | Activity | {6BA1904F-38DB-4de6-A6D7-4377B1C95D3F} |  |
| PrepareServiceQuote | Prepare Service Quote | Activity | {2AFFF14D-B7CB-4200-843E-64C9993FD879} |  |
| ProvideLicenses | Provide Licenses | Activity | {656EB0F6-7CD3-403a-9FE7-B4CC7B29A86D} |  |
| ProvideServices | Provide Service(s) | Activity | {85628578-F197-45fd-8942-CC0812EFEEEF} |  |
| PurchaseOrder | Purchase Order | DataObject | {A9A7B62D-3F33-4b05-8239-DF34F4EF35FE} |  |
| RegisterRFQ | Register RFQ | Activity | {1E8282D2-3F1C-41ce-B8A5-671AAD90ACFC} |  |
| RejectOffer | Reject Offer | Activity | {F443524E-4717-4e31-9D4D-D01A05B478B6} |  |
| RemindPayment | Remind Payment | Activity | {6133EFAA-E2BB-4e3e-ACBF-5DC7BA76353F} |  |
| RequestLicenseQuote | Request License Quote | Activity | {54201F7E-AA1B-49bb-AB58-CE578A450AE4} |  |
| RequestLicenses | Request Licenses | Activity | {FA528F49-DC3F-4b41-8377-D9D2457F83C9} |  |
| RequestRevisedOffer | Request Revised Offer | Activity | {A1BAB8A5-7D52-47e6-9E90-4440D5D6EE88} |  |
| RequestServiceQuote | Request Service Quote | Activity | {71C21043-6571-451e-BFD8-B8901AA0EB81} |  |
| RequestServices | Request Services | Activity | {3ACC3D25-DD6F-43d9-80BB-66BC6EC18134} |  |
| ReviewOffer | Review Offer | Activity | {997B9124-402C-42ee-9A11-03E89D90DF86} |  |
| RFQ | RFQ | DataObject | {76AD2E52-11A3-4657-8F06-F937D33F3C19} |  |
| SalesInvoice | Sales Invoice | DataObject | {E47CCCC5-9862-4bde-A10D-7AFE0D040DFA} |  |
| ServiceDocument | Service Document | DataObject | {9651C011-400C-4d72-9689-35FC5CC0DF2D} |  |
| ServiceInvoice | Service Invoice | DataObject | {D47CACA8-4CFE-44f4-829E-E9C4785A8D99} |  |
| ServiceQuote | Service Quote | DataObject | {117B4799-A108-4e69-BCF6-6BCF203A4EEC} |  |
| servicesrequired | services required? | Gateway | {4DDEC500-6564-4478-BEF0-982F04F01488} |  |
| StartRFQ | Start RFQ | StartEvent | {94A14FAC-00B9-43fc-B10E-9FABE868C74C} |  |
| ValidatePayment | Validate Payment | Activity | {6BF00CC4-39CF-4db4-A20B-06D3A43AC93F} |  |

