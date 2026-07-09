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
- Description: **Why:** The sales lifecycle can't be treated as complete on the seller's word alone — an explicit customer-side acceptance closes the delivery loop and unblocks invoicing without ambiguity. **What:** The customer's acknowledgement that the license files and/or service access credentials from EAxpertise's delivery package have arrived intact. **How:** The customer opens the delivery email, verifies attachments/credentials, and replies confirming receipt (or clicks a confirm link if one is offered). **Context:** Entered on the customer lane after Prepare Delivery reaches them; feeds Activate Delivery.

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
- Description: **Why:** Procurement and delivery can't start until the customer has committed — without an explicit acceptance step, EAxpertise would be ordering licences on assumption and risking unpaid stock. **What:** The customer's binding acceptance of the current Offer, producing a PurchaseOrder that references the accepted offer terms. **How:** Customer replies to the offer email accepting the terms and — where applicable — attaching a Purchase Order (with any Customer PO code and invoicing details); the PurchaseOrder artifact is captured in the CRM against the Offer. **Context:** The "yes" branch out of the Accept Offer? gateway; feeds Handle Approved Offer via message flow. Alternatives on the gateway are Request Revised Offer (partial acceptance) or Reject Offer.

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
- Description: **Why:** Delivery and activation are separate customer-side steps — an accepted delivery that isn't activated still leaves the customer unable to use what they bought, and downstream invoicing shouldn't depend on that gap. **What:** The customer applies the delivered license keys and, where applicable, logs into the delivered services/portals to confirm they are usable in their environment. **How:** Customer installs licence files into their Sparx EA (or hosted seat), signs in to any provisioned service (SaaS/support portal/training), and reports back if anything fails. **Context:** Immediately after Accept Delivery; triggers Prepare SalesInvoice via message flow, so activation success is what green-lights billing.

### IntermediateEvent—checkpayment
- Name: check payment
- Type: Event
- Stereotype: IntermediateEvent
- GUID: {B6F6A5F0-31B9-4876-AB37-29EB93616701}
- Lane: EAxpertise
- Event Type: Timer
- Description: Check if the sales invoice has been paid by the customer. Outcome determines next step.

### IntermediateEvent—ConfirmCustomerAccount
- Name: Confirm Customer Account
- Type: Event
- Stereotype: IntermediateEvent
- GUID: {AD32AD89-C0CA-4001-ACFB-56C1F46601AC}
- Lane: EAxpertise
- Event Type: Signal
- Description: Signal checkpoint before registering the RFQ — the user verifies the requesting organisation has a Customer Account, or creates one via the Manage Customer Account process (see EAxCRM-CustomerAccountProcess.md), before continuing.

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
- Description: **Why:** The sales process needs a concrete, written statement of what the customer wants before EAxpertise commits engineering time to quoting; a verbal enquiry is not enough to hang licence/service configuration off. **What:** An RFQ artifact from the customer, listing intended license types, quantities, and service needs. **How:** Customer drafts the RFQ (typically as an email with a short table or attachment) and sends it to EAxpertise's sales inbox; also emits the Confirm Customer Account signal so EAxpertise can create/verify the Customer Account before registering the RFQ. **Context:** First customer-lane activity after Start RFQ; feeds Register RFQ (via email message flow) and Confirm Customer Account (signal).

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
- Description: **Why:** The RFQ often says "we need a few Ultimate seats" without pinning down edition/quantity/renewal-vs-new — before quoting the vendor, EAxpertise needs to convert that into an unambiguous licence line-up. **What:** A decided list of license line items (type, quantity, new vs renewal, target start date) suitable for a vendor quote. **How:** EAxpertise cross-references the RFQ against the customer's existing entitlements (renewals vs. net-new), consults with the requester where anything is ambiguous, and records the resulting line items on the offer draft. **Context:** Entered from Prepare (Revised) Offer; feeds the "licenses required?" gateway.

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
- Description: **Why:** Services (training, support, SaaS hosting) are where a lot of the customer value sits, and the resold-vs-own distinction (SAL-2) directly affects margin and vendor liability — deciding it up front avoids re-quoting later. **What:** The set of Service line items for this offer, each tagged as procured (with a Vendor) or EAxpertise's own. **How:** EAxpertise picks the fitting services from its catalogue for the RFQ's needs, marks each as procured or own, and adds them to the offer draft; procured services will later drive Request Service Quote against the vendor. **Context:** Entered from Determine Licenses via Prepare (Revised) Offer chain; feeds the "services required?" gateway.

### EndEvent—EndRejectedSales
- Name: End Rejected Sales
- Type: Event
- Stereotype: EndEvent
- GUID: {32ADEDC2-2890-40b6-A489-51A28FA5AC67}
- Lane: EAxpertise
- Event Type: None
- Description: The sales process terminates because the customer rejected the offer.

### EndEvent—EndSales
- Name: End Sales
- Type: Event
- Stereotype: EndEvent
- GUID: {AC4B3F30-5771-4426-8445-30325797259B}
- Lane: EAxpertise
- Event Type: None
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
- Description: **Why:** The customer needs one document to review and accept — not a mail thread of licence and service snippets — and revision cycles must not lose track of which numbered version they refer to. **What:** The Offer artifact for this iteration: a single document combining license and service line items with pricing, a version number, and an expiry date. **How:** Consolidates the confirmed license and service line items (plus vendor pricing where already received) into the offer template, generates the PDF, saves the Offer record in the CRM, and increments the version if this is a revision. **Context:** Entered when both "licenses required?" and "services required?" gateways have converged; feeds Review Offer via message flow (email to customer).

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
- Description: **Why:** An accepted offer is a commitment on both sides — EAxpertise must move from "quoted" to "ordering" without delay, but also without accidentally re-doing quoting work; a dedicated hand-off step captures that transition explicitly. **What:** Internal recognition that the customer has accepted (with their PurchaseOrder attached) and the split of the accepted line items into vendor-facing licence and service orders. **How:** On receipt of the acceptance email, the accepted Offer's status becomes Accepted, the PurchaseOrder is stored against it, and the line items are prepared for the parallel Request Licenses and Request Services activities. **Context:** Immediately after the customer's Accept Offer activity; forks into Request Licenses and Request Services.

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
- Description: **Why:** Even a rejected offer needs a controlled shutdown — otherwise the CRM leaves an "in progress" opportunity open indefinitely, distorting pipeline reporting. **What:** The sales-side wrap-up of a rejected offer: status updates on the Offer, follow-up notes if any, no downstream fulfilment. **How:** On the RejectOffer message, EAxpertise sets the Offer status to Rejected, records any customer feedback in notes, and lets the process terminate at End Rejected Sales. **Context:** Entered only from the customer's Reject Offer activity via message flow; ends the process at End Rejected Sales.

### DataObject—LicenseDocument
- Name: License Document
- Type: Artifact
- Stereotype: DataObject
- GUID: {B5EBA936-39BC-4694-858E-2474715E89E0}
- Lane: Vendor
- Data In/Out: Input
- Is Collection: false
- Description: License registration files delivered by the vendor.

### DataObject—LicenseInvoice
- Name: License Invoice
- Type: Artifact
- Stereotype: DataObject
- GUID: {C206CCD5-D481-40b3-BA1C-18FFD705326E}
- Lane: Vendor
- Data In/Out: Input
- Is Collection: false
- Description: Incoming invoice from the vendor for purchased licenses.

### DataObject—LicenseQuote
- Name: License Quote
- Type: Artifact
- Stereotype: DataObject
- GUID: {6C0747AF-BB4C-4885-BAF6-4FC496E23590}
- Lane: Vendor
- Data In/Out: Input
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
- Data In/Out: Output
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
- Description: **Why:** Billing isn't closed until the money is in — the CRM has to distinguish "invoiced" from "paid" so RemindPayment can chase only genuinely overdue invoices. **What:** The customer's outbound bank payment for the SalesInvoice, producing the Payment artifact. **How:** Customer initiates a bank transfer for the invoice amount to EAxpertise's account; the resulting Payment is what Validate Payment later confirms. **Context:** First activity after Prepare SalesInvoice reaches the customer; feeds Validate Payment via bank-flow. Re-entered from RemindPayment when the first attempt is missed/delayed.

### DataObject—Payment
- Name: Payment
- Type: Artifact
- Stereotype: DataObject
- GUID: {332D8643-81C6-4b64-A250-E8898028D48E}
- Lane: Customer
- Data In/Out: Input
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
- Description: **Why:** The offer is the customer's decision document — it must reflect the RFQ (or the revised RFQ after Customer feedback) precisely, or the whole review/accept loop stalls on avoidable back-and-forth. **What:** An initial or revised draft Offer, ready to be split into licence and service line-item decisions. **How:** Reads the RFQ (or its revised version from Request Revised Offer), lays out the offer skeleton (customer, requested items, target dates), and pushes the flow into Determine Licenses and Determine Services in parallel. Revision-loop entries carry version and change history from the previous offer. **Context:** Entered right after Register RFQ (first time) or after a Request Revised Offer round; feeds Determine Licenses then Determine Services.

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
- Description: **Why:** The customer needs a single, auditable delivery — not a scatter of licence PDFs across separate emails — and Delivery records are the paper trail (DEL-1, DEL-2) that later prove what was actually sent. **What:** The Delivery record for this order plus the outgoing delivery email containing the LicenseDocument and ServiceDocument attachments, linked to Customer and to the SalesInvoice it fulfils. **How:** Collects the vendor-provided LicenseDocument(s) and ServiceDocument(s), attaches them to a new Delivery record referencing the Customer, composes the delivery email, sends it. **Context:** Joins after both Request Licenses and Request Services have produced vendor documents; feeds Accept Delivery via message flow.

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
- Description: **Why:** EAxpertise resells rather than sets its own licence prices — the vendor is authoritative on the cost side, so no offer can be finalised without a vendor quote in hand. **What:** The LicenseQuote artifact: the vendor's pricing for the requested licence line items. **How:** Vendor's sales team responds to the RequestLicenseQuote email with a pricing document; the vendor lane emits LicenseQuote back to EAxpertise via message flow. **Context:** Vendor-lane response to Request License Quote; the LicenseQuote feeds Finalise Version of Offer via the vendor artifact.

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
- Description: **Why:** An invoice must be traceable back to the offer it charges for (SAL-4) — otherwise revenue can't be reconciled against what was actually agreed, and disputes have no evidence base. **What:** The SalesInvoice artifact for this order: invoice number, amount, currency, PDF, and a link to the originating Offer. **How:** Picks up the accepted Offer plus the licence/service line items that were actually delivered, generates the invoice PDF and inserts the SalesInvoice record with a FK to the Offer; also incorporates the vendor's LicenseInvoice/ServiceInvoice amounts for reconciliation. **Context:** Entered after Activate Delivery; feeds Pay SalesInvoice via message flow.

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
- Description: **Why:** Service costs (hosting, training slots, support) come from the vendor, and are needed on the same offer as licences — quoting services separately risks the customer accepting a licence-only offer and being surprised by service costs later. **What:** The ServiceQuote artifact: the vendor's pricing for the requested service line items. **How:** Vendor's sales team responds to the RequestServiceQuote email with service pricing (per-seat, per-month, one-off, etc.); the vendor lane emits ServiceQuote back to EAxpertise via message flow. **Context:** Vendor-lane response to Request Service Quote; the ServiceQuote feeds Finalise Version of Offer.

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
- Description: **Why:** The customer's actual entitlement is the licence file itself — without a vendor-issued LicenseDocument in hand, EAxpertise has nothing to deliver, no matter what was ordered. **What:** The LicenseDocument artifact (registration file/certificate) plus a LicenseInvoice for the vendor's charge to EAxpertise. **How:** Vendor issues the licence registration file and mails it (with the invoice) to EAxpertise; the vendor lane emits LicenseDocument and LicenseInvoice back via message flow. **Context:** Vendor-lane response to Request Licenses; both artifacts feed Prepare Delivery (LicenseDocument) and Prepare SalesInvoice (LicenseInvoice).

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
- Description: **Why:** Services need concrete activation on the vendor side (portal seats, training bookings, SaaS tenant) and a signed service agreement — until both exist, "delivered" is a claim, not a fact. **What:** The ServiceDocument artifact (service agreement) plus a ServiceInvoice for the vendor's charge to EAxpertise, alongside the actual activation on the vendor's systems. **How:** Vendor provisions the service (creates SaaS tenant, allocates training slots, opens support portal seats), issues the service agreement PDF, and invoices EAxpertise; both artifacts return to EAxpertise via message flow. **Context:** Vendor-lane response to Request Services; both artifacts feed Prepare Delivery (ServiceDocument) and Prepare SalesInvoice (ServiceInvoice).

### DataObject—PurchaseOrder
- Name: Purchase Order
- Type: Artifact
- Stereotype: DataObject
- GUID: {A9A7B62D-3F33-4b05-8239-DF34F4EF35FE}
- Lane: Customer
- Data In/Out: Input
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
- Description: **Why:** An RFQ that never enters the CRM has no history — no offer versioning, no timing, no lookup. A dedicated register step also lets Confirm Customer Account tie the enquiry to a real Customer record. **What:** An RFQ record in the CRM linked to the Customer Account, ready to spawn an Offer. **How:** Parses the incoming RFQ email into the RFQ artifact, assigns a reference number, links it to the Customer confirmed by the Confirm Customer Account signal (never before), and hands over to Prepare (Revised) Offer. **Context:** Entered from Create RFQ via email message flow, gated by the Confirm Customer Account signal; feeds Prepare (Revised) Offer.

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
- Description: **Why:** The process must have a clean "no" path — otherwise a customer's silence blurs into either "still deciding" or "rejected", and EAxpertise can't close out the opportunity honestly. **What:** The customer's explicit rejection of the Offer, with no follow-up revision requested. **How:** Customer replies declining the offer (with or without a reason); the reply is what triggers EAxpertise's Handle Rejected Offer. **Context:** The "no" branch of the Accept Offer? gateway; feeds Handle Rejected Offer via message flow.

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
- Description: **Why:** Invoices go unpaid for benign reasons (wrong email address, bounced attachment, holiday) far more often than for malicious ones — a first-line reminder is cheap and usually enough to close the loop. **What:** A courteous reminder email to the customer that the SalesInvoice is outstanding, with the invoice PDF re-attached. **How:** Triggered by the check payment intermediate timer when Validate Payment shows no payment has arrived within the expected window; sends a reminder to the invoice-billing contact and re-routes back to Pay SalesInvoice. **Context:** Entered from the check payment timer on the "no payment" branch; feeds Pay SalesInvoice via message flow.

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
- Description: **Why:** EAxpertise can't quote the customer for licences without knowing what the vendor will charge for those exact line items — a formal quote request is the only reliable cost input, and the multi-vendor requirement (PRO-5) means picking the right vendor per line matters. **What:** A vendor-facing email listing the licence line items EAxpertise needs pricing for, targeted at the correct Vendor per PRO-5.x. **How:** Sends a structured email (line items + quantities + intended start date) to the chosen Vendor (Sparx Systems LTD/EU, Ability Engineering); the vendor responds later with LicenseQuote via message flow into this activity. **Context:** Entered from the "licenses required?" gateway = yes; feeds Finalise Version of Offer indirectly (through the returned LicenseQuote artifact).

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
- Description: **Why:** At this point the customer has accepted the offer, so EAxpertise must actually procure the licences — this is what turns an agreed quote into a real order at the vendor. **What:** A formal purchase request to the Vendor referencing their earlier LicenseQuote and the accepted quantities. **How:** Sends the licence purchase message to the Vendor (typically confirming the LicenseQuote number and quantities), which triggers Provide Licenses on the vendor's side. **Context:** Parallel branch out of Handle Approved Offer alongside Request Services; feeds Prepare Delivery once the vendor's LicenseDocument arrives.

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
- Description: **Why:** A partial acceptance is not a rejection — the customer wants most of the offer but with changes, and forcing a hard yes/no would either lose the sale or land EAxpertise with a mis-scoped commitment. **What:** The customer's structured feedback specifying what to change on the current offer (line items, quantities, pricing, timing). **How:** Customer replies to the offer with a change list; the message flows into EAxpertise's Prepare (Revised) Offer, which produces a new numbered version. **Context:** The "partial acceptance" branch of the Accept Offer? gateway; loops back to Prepare (Revised) Offer.

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
- Description: **Why:** Service pricing is set by the vendor per configuration (seats, hours, tenant size) and can't be assumed from a rate card — the offer's service side needs a fresh quote per RFQ. **What:** A vendor-facing email listing the service line items EAxpertise needs pricing for. **How:** Sends a structured email (service type, seats/hours, start date) to the correct Vendor for that service; the vendor responds later with ServiceQuote via message flow. **Context:** Entered from "services required?" gateway = yes; feeds Finalise Version of Offer via the returned ServiceQuote artifact.

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
- Description: **Why:** Just as with licences, an accepted service offer must trigger a real vendor-side provisioning order — otherwise the customer's activation later would fail. **What:** A formal service order to the Vendor referencing the earlier ServiceQuote and the accepted service configuration. **How:** Sends the service order message to the Vendor (confirming quote number, seats/hours, start date), which triggers Provide Service(s) on the vendor side. **Context:** Parallel branch out of Handle Approved Offer alongside Request Licenses; feeds Prepare Delivery once ServiceDocument arrives.

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
- Description: **Why:** The offer is EAxpertise's proposal, not a contract — the customer needs an explicit review pass to catch scope/pricing mismatches before committing budget. **What:** A customer-side evaluation of the received Offer against the internal need, resulting in an accept/partial/reject decision. **How:** Customer receives the offer email (with the PDF), circulates internally where needed, and returns to the Accept Offer? gateway with a decision. **Context:** Entered on the customer lane from Finalise Version of Offer via message flow; feeds the Accept Offer? gateway (yes/partial acceptance/no).

### DataObject—RFQ
- Name: RFQ
- Type: Artifact
- Stereotype: DataObject
- GUID: {76AD2E52-11A3-4657-8F06-F937D33F3C19}
- Lane: Customer
- Data In/Out: Input
- Is Collection: false
- Description: The Request For Quote document artifact exchanged between Customer and EAxpertise.

### DataObject—SalesInvoice
- Name: Sales Invoice
- Type: Artifact
- Stereotype: DataObject
- GUID: {E47CCCC5-9862-4bde-A10D-7AFE0D040DFA}
- Lane: EAxpertise
- Data In/Out: Output
- Is Collection: false
- Description: Invoice sent to Customer.

### DataObject—ServiceDocument
- Name: Service Document
- Type: Artifact
- Stereotype: DataObject
- GUID: {9651C011-400C-4d72-9689-35FC5CC0DF2D}
- Lane: Vendor
- Data In/Out: Input
- Is Collection: false
- Description: Service agreement document delivered by the vendor.

### DataObject—ServiceInvoice
- Name: Service Invoice
- Type: Artifact
- Stereotype: DataObject
- GUID: {D47CACA8-4CFE-44f4-829E-E9C4785A8D99}
- Lane: Vendor
- Data In/Out: Input
- Is Collection: false
- Description: Incoming invoice from the vendor for procured services.

### DataObject—ServiceQuote
- Name: Service Quote
- Type: Artifact
- Stereotype: DataObject
- GUID: {117B4799-A108-4e69-BCF6-6BCF203A4EEC}
- Lane: Vendor
- Data In/Out: Input
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
- Event Type: None
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
- Description: **Why:** The CRM has no live bank feed, so "paid" has to be a deliberate, human-verified state change — otherwise every unreconciled invoice would silently look outstanding and set off remind loops for no reason. **What:** Confirmation that the customer's transfer has landed in the EAxpertise bank account, matching the SalesInvoice amount. **How:** Reviewer opens the banking portal, matches incoming transfer against the SalesInvoice (by amount and invoice reference), and marks the SalesInvoice paid with paid_date; if nothing has arrived, the check payment timer eventually routes to Remind Payment. **Context:** Entered from Pay SalesInvoice via bank-flow; feeds the check payment intermediate timer, which either closes the process at End Sales or triggers Remind Payment.

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
- ConfirmCustomerAccount → RegisterRFQ

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
- CreateRFQ → ConfirmCustomerAccount [email]

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

