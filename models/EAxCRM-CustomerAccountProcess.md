# EAxCRM — Manage Customer Account Process

**Model ID**: cap-eacrm
**Purpose**: BPMN 2.0 process model for creating and maintaining Customer Accounts in EAxCRM
**Version**: 1.0

## BPMN Collaboration—ManageCustomerAccount
- Name: Manage Customer Account
- GUID: {4D4520AB-EE90-4f73-96FC-116E44DB6007}
- Diagram Name: Manage Customer Account
- Diagram GUID: {2AC2AE34-0087-46a0-BE9F-FD5B6F64B58B}
- Is Closed: false
- Description: BPMN 2.0 process for creating a new Customer Account from minimal data, flagging/merging likely duplicates, retrieving the customer's email history, and suggesting newsletter opt-in for eligible Contact roles. Always staff-driven (single EAxCRM user) — the system assists (duplicate detection, email history) but never creates or merges an account automatically. Referenced from the Sales Process (see EAxCRM-SalesProcess.md, "Confirm Customer Account" message event, before RegisterRFQ) as one possible entry point into this process — the other being an unsolicited email, phone call, or RFQ arriving directly (see the New Customer Contact start event) with no prior Sales activity.

### Lane—EAxpertise
- Name: EAxpertise
- Type: ActivityPartition
- Stereotype: Lane
- GUID: {9402009C-1B33-4877-A69A-CC2EB57691DB}
- Description: The single EAxCRM user who creates and maintains Customer Accounts. No Customer-facing lane — there is no self-service account creation.

### EndEvent—AccountReady
- Name: Account Ready
- Type: Event
- Stereotype: EndEvent
- GUID: {12F7CED7-5CE5-4070-9B73-FB982C101863}
- Lane: EAxpertise
- Event Type: None
- Description: The Customer Account exists, is not a duplicate, and any applicable opt-in decision has been made.

### DataObject—Contact
- Name: Contact
- Type: Artifact
- Stereotype: DataObject
- GUID: {77AAEBE9-8BA5-4668-9967-629293E99856}
- Data In/Out: None
- Is Collection: false
- Description: Why: almost every step in this process reads or writes a field on the account's Contact (role, opt_in, opt_in_date) -- without an explicit DataObject, that dependency was invisible in the diagram, only implied inside 'Customer Account'. What: the single Contact record (name, email, role, opt-in status) attached to the Customer Account being processed. How: created alongside the Customer as part of Create Customer Account (role may be unset initially), later updated by Suggest Newsletter Opt-in (opt_in and opt_in_date only, and only on explicit confirmation) and by Merge Customer Accounts when folded into an existing account's Contact set. Context: represents the single initial Contact created with the account, not the full Contact list once more are added later via CRM-9/CRM-10.

### Activity—CreateCustomerAccount
- Name: Create Customer Account
- Type: Activity
- Stereotype: Activity
- GUID: {B4CEA509-838B-4b2b-B8E5-59FE53AC4FA3}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: **Why:** Every downstream CRM activity (offers, licenses, communications, newsletter) needs a Customer + Contact pair to attach to; without an explicit, atomic create step there is no single point where the pair comes into existence with the fields required for CRM-6..CRM-12 to hold. **What:** A new Customer record (organisation name, address per CRM-7's street-or-PO-Box mode) together with one initial Contact (name, email, optional role/phone/opt-in) — persisted as one atomic transaction (CRM-6). **How:** Staff enter the minimal required fields on CreateAccountScreen (Save is blocked until CRM-6/7 conditions are met); optional Domain-based "Search Emails" prefills fields from IMAP before Save. On commit the Customer + Contact rows are inserted together; Contact.role defaults to Primary if left unset on the sole Contact (CRM-8); Contact.opt_in defaults False (CRM-11). **Context:** Entered either from the Sales Process ("Confirm Customer Account" signal event before RegisterRFQ) or directly on unsolicited contact (New Customer Contact start event); always followed by the Duplicate found? gateway.

### DataObject—CustomerAccount
- Name: Customer Account
- Type: Artifact
- Stereotype: DataObject
- GUID: {B84756F7-0FA9-4e95-B29A-A861F396ADAC}
- Lane: EAxpertise
- Data In/Out: Input
- Is Collection: false
- Description: The Customer + initial Contact record being created/processed by this instance of the process.

### Gateway—Duplicatefound
- Name: Duplicate found?
- Type: Decision
- Stereotype: Gateway
- GUID: {94E22195-3195-45af-9628-105DBBACEEBB}
- Lane: EAxpertise
- Gateway Type: Exclusive
- Description: Fuzzy-match the new account's organisation name and Contact email against existing Customer Accounts. Outcome determines whether to merge or continue.

### DataObject—EmailHistory
- Name: Email History
- Type: Artifact
- Stereotype: DataObject
- GUID: {F55B3C35-F57B-4535-966F-DDF831EC9807}
- Lane: EAxpertise
- Data In/Out: Input
- Is Collection: false
- Description: The set of Communication records matched and linked to this Customer Account.

### Activity—MergeCustomerAccounts
- Name: Merge Customer Accounts
- Type: Activity
- Stereotype: Activity
- GUID: {13A26AFF-4D25-412d-ABBA-565E20C30048}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: **Why:** Without merging on a flagged duplicate, the same organisation would silently accumulate multiple Customer records, fragmenting its licences, communications, and history across them; deleting the losing record outright would also destroy the audit trail of what happened to it (CRM-14). **What:** The losing Customer's Contact/notes are folded into the surviving Customer chosen by the rep, and the losing Customer.merged_into is set to point at the survivor — the losing row itself is retained, not deleted. **How:** On MergeAccountsScreen the rep compares the new account against the flagged match and clicks Merge; on commit, contact records move over, Customer.merged_into is set once and never cleared, and any resulting duplicate Contact rows are left in place for the rep to remove manually as a separate action. **Context:** Reached only from the Duplicate found? gateway on a positive match; terminates the process at "Merged into Existing Account" — no new Customer Account is created for this instance.

### EndEvent—MergedintoExistingAccount
- Name: Merged into Existing Account
- Type: Event
- Stereotype: EndEvent
- GUID: {EAFD19F6-F227-49ee-A9C1-47B8E36AD178}
- Lane: EAxpertise
- Event Type: None
- Description: The new account request was folded into an existing Customer Account; no new account was created.

### StartEvent—NewCustomerContact
- Name: New Customer Contact
- Type: Event
- Stereotype: StartEvent
- GUID: {739C876F-E4AE-4102-9663-966D2C925D01}
- Lane: EAxpertise
- Event Type: None
- Description: A new customer relationship begins — an unsolicited email, a phone call, or an RFQ from an organisation without an existing account.

### Gateway—PrimaryorLicenseHolderrole
- Name: Primary or License Holder role?
- Type: Decision
- Stereotype: Gateway
- GUID: {16CF0C0D-548F-4cb0-8B2A-E536B593612B}
- Lane: EAxpertise
- Gateway Type: Exclusive
- Description: Checks whether the account's Contact has (or has just been assigned) the Primary Contact or License Holder role — the two roles eligible for suggested newsletter opt-in.

### Activity—RetrieveCustomerEmailHistory
- Name: Retrieve Customer Email History
- Type: Activity
- Stereotype: Activity
- GUID: {CA27AF88-ED2F-4653-8059-A61D0BA88A8E}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: **Why:** Staff need a fast way to see everything a Customer Account has ever communicated, without manually searching three separate mailboxes, and a single Contact email address rarely captures the full picture — colleagues at the same organisation write from the same domain but different addresses. **What:** A running Email History for the account, built by scanning on the Contact's email domain (not a single address), returning the set of distinct sender/recipient addresses discovered plus the matched messages, so staff can review which of those addresses should become new Contacts on the account and which should link to existing Contacts. **How:** Reads the account's Contact email domain as the search key, scans the configured IMAP mailboxes (han@eaxpertise.nl, sales@eaxpertise.nl, info@eaxpertise.nl), links each matched Communication to the Customer (via customer_id) and, where the sender/recipient address matches a known Contact, to that Contact (via contact_id); addresses that don't yet match any Contact are surfaced for the rep to either create a new Contact or link manually. Communications already linked from a prior run are not re-added. **Context:** Distinct from the create-time "Search Emails" domain lookup on CreateAccountScreen, which only prefills fields before the account exists.

### Activity—SuggestNewsletterOptin
- Name: Suggest Newsletter Opt-in
- Type: Activity
- Stereotype: Activity
- GUID: {8D50E44F-E7EB-4a7f-B861-D0766947A995}
- Lane: EAxpertise
- Completion Quantity: 1
- Is Called Activity: false
- Is For Compensation: false
- Loop: None
- Start Quantity: 1
- Task Type: User
- Description: **Why:** Primary and License Holder are the two roles most likely to be the right person to ask about newsletter consent; prompting only these avoids pestering every Contact, while requiring an explicit confirmation (rather than the gateway match itself setting opt_in) keeps consent affirmative and auditable rather than inferred (CRM-16, CRM-11). **What:** A suggested opt-in for the account's Contact, with opt_in and opt_in_date only written on explicit Confirm. **How:** OptInScreen shows the eligible Contact with a message and Confirm/Decline buttons; Confirm sets Contact.opt_in=True and stamps opt_in_date, Decline leaves both untouched — either way the process ends at Account Ready. **Context:** Reached only when the "Primary or License Holder role?" gateway resolves positive after Retrieve Customer Email History; the ongoing opt-in bookkeeping thereafter belongs to Newsletter Management's Manage Opt-in process, not this one.

### Sequence Flows

- NewCustomerContact → CreateCustomerAccount
- CreateCustomerAccount → Duplicatefound
- Duplicatefound → MergeCustomerAccounts [duplicate found]
- Duplicatefound → RetrieveCustomerEmailHistory [no duplicate]
- MergeCustomerAccounts → MergedintoExistingAccount
- RetrieveCustomerEmailHistory → PrimaryorLicenseHolderrole
- PrimaryorLicenseHolderrole → SuggestNewsletterOptin [Primary or License Holder]
- PrimaryorLicenseHolderrole → AccountReady [no]
- SuggestNewsletterOptin → AccountReady

### Data Input Associations

- EmailHistory → RetrieveCustomerEmailHistory
- CustomerAccount → RetrieveCustomerEmailHistory

### Data Output Associations

- RetrieveCustomerEmailHistory → EmailHistory
- CreateCustomerAccount → CustomerAccount
- CreateCustomerAccount → Contact
- SuggestNewsletterOptin → Contact

