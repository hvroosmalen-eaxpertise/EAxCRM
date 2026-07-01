# EAxCRM — Sales Process Architecture

**Model ID**: sp-eacrm
**Purpose**: BPMN 2.0 sales process model for the EAxCRM system
**Version**: 1.0

## BPMN Collaboration—EAxCRMSalesProcessArchitecture
- Name: EAxCRM Sales Process Architecture
- GUID: {6ACCD057-B99E-48a4-8BE0-AC1FCC601245}
- Diagram Name: Sales Process Architecture
- Diagram GUID: {A8CAE468-7CBC-46c0-9DCE-C695E50C1F36}
- Is Closed: false
- Description: BPMN 2.0 collaboration model covering the end-to-end sales process at EAxpertise, from customer RFQ through delivery and payment.

### Lane—Customer
- Name: Customer
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {D78E6C97-1010-40da-8A34-28B2A84F29D6}
- Description: The customer organization requesting quotes and purchasing Sparx EA licenses and services.

### Lane—EAxpertise
- Name: EAxpertise
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {0D1DE3F6-9F36-4387-901D-5E82190C78A4}
- Description: EAxpertise as the reseller — manages offers, licenses, services, and coordinates with vendors.

### Lane—Vendor
- Name: Vendor
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {4CE7A835-2E5A-4392-ACA7-2A54C08DA636}
- Description: The supplier (e.g. Sparx Systems, Prolaborate, Ability Engineering) providing license and service quotes.

### Activity—AcceptDelivery
- Name: Accept Delivery
- Type: Activity
- Stereotype: Activity
- GUID: {863E019F-D8AA-4a29-AC98-9A5E9BC1DE9E}
- Lane: Customer
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Customer confirms receipt of license files and/or service access credentials.

### Activity—AcceptOffer_Activity
- Name: Accept Offer
- Type: Activity
- Stereotype: Activity
- GUID: {AAF91171-3C57-46bb-B549-0BE31011BA78}
- Lane: Customer
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Customer formally accepts the offer, triggering the fulfillment phase.

### Gateway—AcceptOffer_Gateway
- Name: Accept Offer?
- Type: Decision
- Stereotype: Gateway
- GUID: {48A6D2C0-48A8-41c7-9B44-28B014D9A5E4}
- Lane: Customer
- Gateway Type: Exclusive
- Description: Customer formally accepts the offer, triggering the fulfillment phase.

### Activity—ActivateDelivery
- Name: Activate Delivery
- Type: Activity
- Stereotype: Activity
- GUID: {F1FA7EC6-06B5-41cc-BAFC-1DCD1EDE3B27}
- Lane: Customer
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Customer activates the delivered licenses and services in their environment.

### IntermediateEvent—checkpayment
- Name: check payment
- Type: Event
- Stereotype: IntermediateEvent
- GUID: {B6F6A5F0-31B9-4876-AB37-29EB93616701}
- Lane: EAxpertise
- Description: Check if the sales invoice has been paid by the customer. Outcome determines next step.

### Activity—CreateRFQ
- Name: Create RFQ
- Type: Activity
- Stereotype: Activity
- GUID: {8078EDB0-256C-4dd4-8810-573EAA0F0B0B}
- Lane: Customer
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Customer drafts and sends a Request For Quote detailing their license and service needs.

### Activity—DetermineLicenses
- Name: Determine Licenses
- Type: Activity
- Stereotype: Activity
- GUID: {F1B9706F-D357-48a3-BA36-4AAF2618F4A4}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Identify which Sparx EA license types and quantities the customer needs.

### Activity—DetermineServices
- Name: Determine Services
- Type: Activity
- Stereotype: Activity
- GUID: {52A9A807-5186-4dcd-ABC4-2F48A42DC2E4}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Services can be resold from Vendor or provided by EAxpertise.

### EndEvent—EndRejectedSales
- Name: End Rejected Sales
- Type: Event
- Stereotype: EndEvent
- GUID: {32ADEDC2-2890-40b6-A489-51A28FA5AC67}
- Lane: EAxpertise
- Description: The sales process terminates because the customer rejected the offer.

### EndEvent—EndSales
- Name: End Sales
- Type: Event
- Stereotype: EndEvent
- GUID: {AC4B3F30-5771-4426-8445-30325797259B}
- Lane: EAxpertise
- Description: The sales process is complete — payment received and delivery activated.

### Activity—FinaliseVersionofOffer
- Name: Finalise Version of Offer
- Type: Activity
- Stereotype: Activity
- GUID: {8C9B0572-1DB2-4bdd-9D33-D8A279C87BE0}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Consolidate license and service line items into the final offer document.

### Activity—HandleApprovedOffer
- Name: Handle Approved Offer
- Type: Activity
- Stereotype: Activity
- GUID: {01C496AC-DFE7-4ea9-B482-1E95EF851677}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Receive the accepted offer and initiate procurement of licenses and services.

### Activity—HandleRejectedOffer
- Name: Handle Rejected Offer
- Type: Activity
- Stereotype: Activity
- GUID: {CC8DB595-33FA-423a-A7BB-E2C32C478029}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Close the sales process.

### DataObject—LicenseDocument
- Name: License Document
- Type: Artifact
- Stereotype: DataObject
- GUID: {B5EBA936-39BC-4694-858E-2474715E89E0}
- Lane: Vendor
- Is Collection: false
- Description: License registration files delivered by the vendor.

### DataObject—LicenseInvoice
- Name: License Invoice
- Type: Artifact
- Stereotype: DataObject
- GUID: {C206CCD5-D481-40b3-BA1C-18FFD705326E}
- Lane: Vendor
- Is Collection: false
- Description: Incoming invoice from the vendor for purchased licenses.

### DataObject—LicenseQuote
- Name: License Quote
- Type: Artifact
- Stereotype: DataObject
- GUID: {6C0747AF-BB4C-4885-BAF6-4FC496E23590}
- Lane: Vendor
- Is Collection: false
- Description: Pricing quote from the vendor for requested license line items.

### Gateway—licensesrequired
- Name: licenses required?
- Type: Decision
- Stereotype: Gateway
- GUID: {137E4E47-AE30-4019-AFB4-F5848F6C75E7}
- Lane: EAxpertise
- Gateway Type: Exclusive
- Description: Does the customer require Sparx EA license entitlements (new or renewal) as part of this purchase? If yes, route to license quote request. If no, proceed to finalize the offer.

### DataObject—Offer
- Name: Offer
- Type: Artifact
- Stereotype: DataObject
- GUID: {CB5267A2-D848-4021-A26E-DDB979177C3A}
- Lane: EAxpertise
- Is Collection: false
- Description: The sales proposal document sent to the customer, containing license and service line items with pricing.

### Activity—PaySalesInvoice
- Name: Pay SalesInvoice
- Type: Activity
- Stereotype: Activity
- GUID: {4E4972A7-0D2D-4135-BA47-2B403D9B8309}
- Lane: Customer
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: Manual
- Description: Customer pays the sales invoice via bank transfer.

### DataObject—Payment
- Name: Payment
- Type: Artifact
- Stereotype: DataObject
- GUID: {332D8643-81C6-4b64-A250-E8898028D48E}
- Lane: Customer
- Is Collection: false
- Description: Payment record by Bank.

### Activity—PrepareRevisedOffer
- Name: Prepare (Revised) Offer
- Type: Activity
- Stereotype: Activity
- GUID: {9C3B3106-2A1F-46ef-818F-374EC58FC6FB}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: EAxpertise prepares a sales offer based on the customer's RFQ requirements.

### Activity—PrepareDelivery
- Name: Prepare Delivery
- Type: Activity
- Stereotype: Activity
- GUID: {677F24EF-13D2-43bc-A2EF-241AC495066E}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Create the formal handover package and delivery note for the customer.

### Activity—PrepareLicenseQuote
- Name: Prepare License Quote
- Type: Activity
- Stereotype: Activity
- GUID: {9D0A23BA-1725-473a-9C0D-D9BDAD113492}
- Lane: Vendor
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Vendor prepares a pricing quote for the requested license and service line items.

### Activity—PrepareSalesInvoice
- Name: Prepare SalesInvoice
- Type: Activity
- Stereotype: Activity
- GUID: {6BA1904F-38DB-4de6-A6D7-4377B1C95D3F}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Generate the outgoing sales invoice based on the accepted offer.

### Activity—PrepareServiceQuote
- Name: Prepare Service Quote
- Type: Activity
- Stereotype: Activity
- GUID: {2AFFF14D-B7CB-4200-843E-64C9993FD879}
- Lane: Vendor
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Vendor provides Service pricing.

### Activity—ProvideLicenses
- Name: Provide Licenses
- Type: Activity
- Stereotype: Activity
- GUID: {656EB0F6-7CD3-403a-9FE7-B4CC7B29A86D}
- Lane: Vendor
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Vendor delivers license files.

### Activity—ProvideServices
- Name: Provide Service(s)
- Type: Activity
- Stereotype: Activity
- GUID: {85628578-F197-45fd-8942-CC0812EFEEEF}
- Lane: Vendor
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Vendor activates the contracted services (support portal, training slots, SaaS tenant) and provide service agreement.

### DataObject—PurchaseOrder
- Name: Purchase Order
- Type: Artifact
- Stereotype: DataObject
- GUID: {A9A7B62D-3F33-4b05-8239-DF34F4EF35FE}
- Lane: Customer
- Is Collection: false
- Description: A Purchase order is the acceptance for the payment. It can come with a Customer Purchase Order code and information on invoicing.

### Activity—RegisterRFQ
- Name: Register RFQ
- Type: Activity
- Stereotype: Activity
- GUID: {1E8282D2-3F1C-41ce-B8A5-671AAD90ACFC}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Log the incoming RFQ into the CRM system and assign a reference number.

### Activity—RejectOffer
- Name: Reject Offer
- Type: Activity
- Stereotype: Activity
- GUID: {F443524E-4717-4e31-9D4D-D01A05B478B6}
- Lane: Customer
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Customer reject the Offer and decides not to go with Purchase.

### Activity—RemindPayment
- Name: Remind Payment
- Type: Activity
- Stereotype: Activity
- GUID: {6133EFAA-E2BB-4e3e-ACBF-5DC7BA76353F}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: Abstract
- Description: Notify the Customer that Payment is not received. Reasons for non-payments could be wrong email address, bounced email, ...

### Activity—RequestLicenseQuote
- Name: Request License Quote
- Type: Activity
- Stereotype: Activity
- GUID: {54201F7E-AA1B-49bb-AB58-CE578A450AE4}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: Abstract
- Description: Send a formal request to the vendor (Sparx Systems) for a pricing quote on the required license line items. The vendor responds with a LicenseQuote.

### Activity—RequestLicenses
- Name: Request Licenses
- Type: Activity
- Stereotype: Activity
- GUID: {FA528F49-DC3F-4b41-8377-D9D2457F83C9}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Send license purchase request to the Vendor with the agreed line items.

### Activity—RequestRevisedOffer
- Name: Request Revised Offer
- Type: Activity
- Stereotype: Activity
- GUID: {A1BAB8A5-7D52-47e6-9E90-4440D5D6EE88}
- Lane: Customer
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Customer request a revised offer

### Activity—RequestServiceQuote
- Name: Request Service Quote
- Type: Activity
- Stereotype: Activity
- GUID: {71C21043-6571-451e-BFD8-B8901AA0EB81}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: Abstract
- Description: Send a formal request to the vendor for a pricing quote on the required service line items (SaaS, training, support). The vendor responds with a ServiceQuote.

### Activity—RequestServices
- Name: Request Services
- Type: Activity
- Stereotype: Activity
- GUID: {3ACC3D25-DD6F-43d9-80BB-66BC6EC18134}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Send service order request to the Vendor with the agreed service details.

### Activity—ReviewOffer
- Name: Review Offer
- Type: Activity
- Stereotype: Activity
- GUID: {997B9124-402C-42ee-9A11-03E89D90DF86}
- Lane: Customer
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: Customer reviews the offer prepared by EAxpertise and decides whether to accept.

### DataObject—RFQ
- Name: RFQ
- Type: Artifact
- Stereotype: DataObject
- GUID: {76AD2E52-11A3-4657-8F06-F937D33F3C19}
- Lane: Customer
- Is Collection: false
- Description: The Request For Quote document artifact exchanged between Customer and EAxpertise.

### DataObject—SalesInvoice
- Name: Sales Invoice
- Type: Artifact
- Stereotype: DataObject
- GUID: {E47CCCC5-9862-4bde-A10D-7AFE0D040DFA}
- Lane: EAxpertise
- Is Collection: false
- Description: Invoice sent to Customer.

### DataObject—ServiceDocument
- Name: Service Document
- Type: Artifact
- Stereotype: DataObject
- GUID: {9651C011-400C-4d72-9689-35FC5CC0DF2D}
- Lane: Vendor
- Is Collection: false
- Description: Service agreement document delivered by the vendor.

### DataObject—ServiceInvoice
- Name: Service Invoice
- Type: Artifact
- Stereotype: DataObject
- GUID: {D47CACA8-4CFE-44f4-829E-E9C4785A8D99}
- Lane: Vendor
- Is Collection: false
- Description: Incoming invoice from the vendor for procured services.

### DataObject—ServiceQuote
- Name: Service Quote
- Type: Artifact
- Stereotype: DataObject
- GUID: {117B4799-A108-4e69-BCF6-6BCF203A4EEC}
- Lane: Vendor
- Is Collection: false
- Description: Pricing quote from the vendor for requested service line items.

### Gateway—servicesrequired
- Name: services required?
- Type: Decision
- Stereotype: Gateway
- GUID: {4DDEC500-6564-4478-BEF0-982F04F01488}
- Lane: EAxpertise
- Gateway Type: Exclusive
- Description: Check if the customer's RFQ includes service items beyond license procurement.

### StartEvent—StartRFQ
- Name: Start RFQ
- Type: Event
- Stereotype: StartEvent
- GUID: {94A14FAC-00B9-43fc-B10E-9FABE868C74C}
- Lane: Customer
- Description: The customer initiates the process by submitting a request for a quote to EAxpertise.

### Activity—ValidatePayment
- Name: Validate Payment
- Type: Activity
- Stereotype: Activity
- GUID: {6BF00CC4-39CF-4db4-A20B-06D3A43AC93F}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: Manual
- Description: Manually verify in the banking portal that the customer's transfer has arrived.

### Sequence Flows

- StartRFQ → CreateRFQ
- RegisterRFQ → PrepareRevisedOffer
- PrepareRevisedOffer → DetermineServices
- DetermineLicenses → licensesrequired
- servicesrequired → RequestServiceQuote [yes]
- servicesrequired → FinaliseVersionofOffer [no]
- ReviewOffer → AcceptOffer_Gateway [yes]
- AcceptOffer_Gateway → AcceptOffer_Activity [yes]
- HandleApprovedOffer → RequestLicenses
- HandleApprovedOffer → RequestServices
- RequestLicenses → PrepareDelivery
- RequestServices → PrepareDelivery
- AcceptDelivery → ActivateDelivery
- ValidatePayment → checkpayment
- checkpayment → EndSales [received]
- AcceptOffer_Gateway → RequestRevisedOffer [partial acceptance]
- AcceptOffer_Gateway → RejectOffer [no]
- RequestRevisedOffer → PrepareRevisedOffer
- HandleRejectedOffer → EndRejectedSales
- PrepareRevisedOffer → DetermineLicenses
- checkpayment → RemindPayment
- DetermineServices → servicesrequired
- licensesrequired → FinaliseVersionofOffer [no]
- licensesrequired → RequestLicenseQuote [yes]

### Message Flows

- CreateRFQ → RegisterRFQ [email]
- PrepareLicenseQuote → RequestLicenseQuote [email license pricing]
- FinaliseVersionofOffer → ReviewOffer [email offer]
- AcceptOffer_Activity → HandleApprovedOffer [email acceptance and invoice details]
- RequestLicenses → ProvideLicenses [license quote acceptance]
- RequestServices → ProvideServices [service quote acceptance]
- PrepareDelivery → AcceptDelivery
- ProvideServices → PrepareDelivery
- ProvideLicenses → PrepareDelivery
- ActivateDelivery → PrepareSalesInvoice [delivery activated]
- PrepareSalesInvoice → PaySalesInvoice
- PaySalesInvoice → ValidatePayment [payment by bank]
- RemindPayment → PaySalesInvoice [email payment not received]
- RequestServiceQuote → PrepareServiceQuote [email service request]
- PrepareServiceQuote → RequestServiceQuote [email service pricing]
- RejectOffer → HandleRejectedOffer
- RequestLicenseQuote → PrepareLicenseQuote [email license request]

### Data Input Associations

- RFQ → RegisterRFQ
- Offer → ReviewOffer
- LicenseQuote → RequestLicenseQuote
- PurchaseOrder → HandleApprovedOffer
- ServiceQuote → RequestServiceQuote
- LicenseDocument → PrepareDelivery
- ServiceDocument → PrepareDelivery
- LicenseInvoice → PrepareSalesInvoice
- ServiceInvoice → PrepareSalesInvoice
- SalesInvoice → PaySalesInvoice
- Payment → ValidatePayment

### Data Output Associations

- CreateRFQ → RFQ
- FinaliseVersionofOffer → Offer
- PrepareLicenseQuote → LicenseQuote
- AcceptOffer_Activity → PurchaseOrder
- PrepareServiceQuote → ServiceQuote
- ProvideLicenses → LicenseDocument
- ProvideServices → ServiceDocument
- ProvideLicenses → LicenseInvoice
- ProvideServices → ServiceInvoice
- PrepareSalesInvoice → SalesInvoice
- PaySalesInvoice → Payment

