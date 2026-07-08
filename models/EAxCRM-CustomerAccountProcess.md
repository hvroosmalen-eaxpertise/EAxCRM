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
- Description: Create a new Customer (organisation name) with exactly one initial Contact (email address). Role is optional at this point — it may be left unassigned or set immediately (e.g. to Primary) if known.

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
- Description: User reviews the flagged match and merges the new Contact/data into the existing Customer Account. Any resulting duplicate Contact records may be manually removed afterward (delete action).

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
- Description: Why: staff need a fast way to see everything a Customer Account has ever communicated, without manually searching three separate mailboxes. What: composes a running Email History for the account -- a list of contact moments (sender, participants, date) matched against the Contact's email address, not just a raw dump of messages. How: reads the account's Contact email as the search key, scans the configured IMAP mailboxes (han@eaxpertise.nl, sales@eaxpertise.nl, info@eaxpertise.nl), and appends newly matched Communications to the Email History without duplicating ones already linked from a prior run. Context: an unmatched email is flagged for manual linking rather than silently dropped (CRM-2), and this activity is distinct from the create-time "Search Emails" domain lookup on CreateAccountScreen, which only prefills fields before the account exists.

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
- Description: System suggests opting the Primary/License Holder Contact in to the newsletter. opt_in and opt_in_date are only set after explicit user confirmation — never automatically.

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

