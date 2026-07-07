# EAxCRM — Manage Customer Account UI

**Model ID**: cap-ui-eacrm
**Purpose**: Wireframe mockups for the Manage Customer Account screens

## Flow—ManageCustomerAccountUI
- Name: Manage Customer Account UI
- Sitemap Diagram Name: Manage Customer Account UI — Sitemap

### Screen—CreateAccountScreen
- Name: Create Customer Account
- Type: Screen
- Stereotype: WireframeWebsite
- GUID: {D856F705-54EF-4f5b-963B-7193F99EEB38}
- Diagram Name: Create Customer Account
- Diagram GUID: {2937D2C5-B598-402e-8B30-BF158A32E48D}
- Description: Staff creates a new Customer Account from an organisation name, a Contact name, and a Contact email. Required-to-save fields (Organisation Name, Contact Name, Contact Email) are the minimal data needed for the Save button to create the Customer + Contact; everything else (Role, and Customer.address/notes and Contact.phone, not yet on this screen) is nice-to-have and can be filled in later via an edit screen — decided 2026-07-06 while reviewing this screen against the Customer/Contact data model entities.

#### Control—CreateAccountHeader
- Name: Create Customer Account
- Type: Header
- Screen: CreateAccountScreen
- Bounds: 46, 108, 575, 47
- GUID: {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF}

#### Control—CreateCustomerAccount
- Name: Create Customer Account
- Type: Frame
- Screen: CreateAccountScreen
- Bounds: 34, 28, 550, 420
- GUID: {975FF198-BA12-49c7-A828-0A8C80EF2B29}

#### Control—Cancel
- Name: Cancel
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 191, 341, 100, 30
- State: Normal
- GUID: {CA831324-5B0E-4087-98C6-2FC0B2855077}

#### Control—CreateAccountEmailLabel
- Name: Contact Email
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 251, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {6F79EB95-46D2-4781-8AF0-21C923B3FC17}

#### Control—CreateAccountContactNameLabel
- Name: Contact Name
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 211, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB}

#### Control—CreateAccountEmailField
- Name: ContactEmailField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 251, 250, 24
- Description: Required to save. Email address for the initial Contact (Contact.email).
- GUID: {59032069-A217-43e1-853A-40192D4D0B30}

#### Control—CreateAccountContactNameField
- Name: ContactNameField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 211, 250, 24
- Description: Required to save. Name of the initial Contact person (Contact.name) -- added 2026-07-06; the screen previously only captured the Contact's email, with no way to record who that email actually belongs to.
- GUID: {BAF12E7E-0B73-44f0-A59A-50701990EB61}

#### Control—CreateAccountOrgLabel
- Name: Organisation Name
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 171, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {F3464C6E-98F1-4306-9E25-53DF1D727FBB}

#### Control—CreateAccountOrgField
- Name: OrgNameField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 171, 250, 24
- Description: Required to save. Organisation name for the new Customer (Customer.name).
- GUID: {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA}

#### Control—CreateAccountRoleLabel
- Name: Role (optional)
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 291, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2}

#### Control—CreateAccountRoleCombo
- Name: RoleCombo
- Type: ComboBox
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 291, 180, 24
- Description: Optional / nice-to-have. May be left unassigned and set later (Contact.role).
- DropDownState: Closed
- Items: Primary, Purchase, Sales, License Holder
- GUID: {00DAE181-F318-426d-93EB-1C0ADB06CFF0}

#### Control—CreateAccountSaveButton
- Name: Save
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 341, 100, 30
- State: Normal
- GUID: {C36B94EF-B3A5-4998-B56E-30495392AB2B}

### Screen—MergeAccountsScreen
- Name: Merge Customer Accounts
- Type: Screen
- Stereotype: WireframeWebsite
- GUID: {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68}
- Diagram Name: Merge Customer Accounts
- Diagram GUID: {877D39EF-03B8-4feb-8610-8C4C169C4E48}
- Description: Shown when the duplicate check flags a likely match. Staff compares the new account against the existing one and either merges or cancels.

#### Control—MergeCustomerAccounts
- Name: Merge Customer Accounts
- Type: Frame
- Screen: MergeAccountsScreen
- Bounds: 23, 28, 550, 380
- GUID: {A19CE38F-D0FF-4fb4-A940-BD2201821AE2}

#### Control—MergeCancelButton
- Name: Cancel
- Type: Button
- Screen: MergeAccountsScreen
- Parent: MergeCustomerAccounts
- Bounds: 153, 274, 100, 30
- State: Normal
- GUID: {07DB66E8-B99B-46c9-BA02-14A16B08E789}

#### Control—MergeExistingLabel
- Name: Matched Existing Account
- Type: Label
- Screen: MergeAccountsScreen
- Parent: MergeCustomerAccounts
- Bounds: 273, 164, 200, 13
- Align Text: Left
- Multiline: false
- GUID: {A3AE6314-8751-439c-9A0C-6BE9A86A5F80}

#### Control—MergeButton
- Name: Merge
- Type: Button
- Screen: MergeAccountsScreen
- Parent: MergeCustomerAccounts
- Bounds: 33, 274, 100, 30
- State: Normal
- GUID: {88E3E477-1D90-4522-B793-F14F74370696}

#### Control—MergeHeader
- Name: Merge Customer Accounts
- Type: Header
- Screen: MergeAccountsScreen
- Parent: MergeCustomerAccounts
- Bounds: 34, 107, 525, 47
- GUID: {88BC7565-848C-4947-ACD4-0B5F87D3CED0}

#### Control—MergeNewLabel
- Name: New Account
- Type: Label
- Screen: MergeAccountsScreen
- Parent: MergeCustomerAccounts
- Bounds: 33, 164, 200, 13
- Align Text: Left
- Multiline: false
- GUID: {2BD56BBA-C370-43db-8762-B1B01BBB5884}

#### Control—MergeExistingSummary
- Name: ExistingAccountSummary
- Type: TextBlock
- Screen: MergeAccountsScreen
- Parent: MergeCustomerAccounts
- Bounds: 270, 188, 220, 60
- Description: The existing Customer Account the fuzzy match flagged.
- GUID: {D063D316-BFE7-41eb-8F63-2AF875F106BD}

#### Control—MergeNewSummary
- Name: NewAccountSummary
- Type: TextBlock
- Screen: MergeAccountsScreen
- Parent: MergeCustomerAccounts
- Bounds: 30, 190, 220, 60
- Description: Organisation name and Contact email just entered.
- GUID: {392FF052-CB26-4cd7-8A90-EF87226FE119}

### Screen—EmailHistoryScreen
- Name: Retrieve Customer Email History
- Type: Screen
- Stereotype: WireframeWebsite
- GUID: {18A7FBC2-28B0-4043-9304-8C5068B7DD8D}
- Diagram Name: Retrieve Customer Email History
- Diagram GUID: {0987C65C-A8FC-4d2b-B7FC-A0F6A002FE87}
- Description: Staff triggers a scan of the configured IMAP mailboxes for the Contact's email address and reviews the matched Communications.

#### Control—CustomerEmailHistory
- Name: Customer Email History
- Type: Frame
- Screen: EmailHistoryScreen
- Bounds: 31, 26, 728, 507
- GUID: {4CB10ABA-8B5F-4ce7-B9F3-06DB286BAF00}

#### Control—EmailHistoryContactLabel
- Name: Contact Domain
- Type: Label
- Screen: EmailHistoryScreen
- Parent: CustomerEmailHistory
- Bounds: 107, 164, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {1E82D3EF-4658-423f-9409-BC1863997CB1}

#### Control—EmailHistoryContinueButton
- Name: Continue
- Type: Button
- Screen: EmailHistoryScreen
- Parent: CustomerEmailHistory
- Bounds: 106, 454, 100, 30
- State: Normal
- GUID: {DC8F0AA8-CB6E-41e2-A15A-012485C22452}

#### Control—EmailHistoryHeader
- Name: Customer Email History
- Type: Header
- Screen: EmailHistoryScreen
- Parent: CustomerEmailHistory
- Bounds: 108, 98, 478, 47
- GUID: {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F}

#### Control—EmailHistoryTable
- Name: Matched Communications
- Type: Table
- Screen: EmailHistoryScreen
- Parent: CustomerEmailHistory
- Bounds: 106, 254, 460, 180
- Description: Sender, subject, date for each matched Communication.
- GUID: {111D3E6E-E80E-43de-A809-18D9FE3B7F39}

#### Control—EmailHistoryScanButton
- Name: Scan Mailboxes
- Type: Button
- Screen: EmailHistoryScreen
- Parent: CustomerEmailHistory
- Bounds: 106, 204, 150, 30
- State: Normal
- GUID: {1CB3461F-6C78-45a3-8C20-78847FEF0B10}

#### Control—EmailHistoryContactValue
- Name: ContactDomainValue
- Type: TextBlock
- Screen: EmailHistoryScreen
- Parent: CustomerEmailHistory
- Bounds: 207, 161, 250, 20
- GUID: {A19391A0-1832-4861-8E90-4597C9A90A2F}

### Screen—OptInScreen
- Name: Suggest Newsletter Opt-in
- Type: Screen
- Stereotype: WireframeWebsite
- GUID: {B037917E-C155-4167-A348-D4EA003F747E}
- Diagram Name: Suggest Newsletter Opt-in
- Diagram GUID: {CCDFE18F-404E-4617-9DB7-9507A920072A}
- Description: Shown when the Contact has (or was just assigned) the Primary or License Holder role. Opt-in is only set after explicit confirmation here — never automatically.

#### Control—SuggestNewsletteropt-in
- Name: Suggest Newsletter opt-in
- Type: Frame
- Screen: OptInScreen
- Bounds: 54, 75, 550, 380
- GUID: {1AE3F6BA-E741-4537-B062-32A2897CDE66}

#### Control—contactemailaddress
- Name: contact email address
- Type: Label
- Screen: OptInScreen
- Parent: SuggestNewsletteropt-in
- Bounds: 87, 274, 139, 13
- Align Text: Left
- Multiline: false
- GUID: {8171055F-E3C0-43fd-8544-1F7D12A93288}

#### Control—OptInConfirmButton
- Name: Confirm
- Type: Button
- Screen: OptInScreen
- Parent: SuggestNewsletteropt-in
- Bounds: 79, 341, 100, 30
- State: Normal
- GUID: {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518}

#### Control—OptInDeclineButton
- Name: Decline
- Type: Button
- Screen: OptInScreen
- Parent: SuggestNewsletteropt-in
- Bounds: 199, 341, 100, 30
- State: Normal
- GUID: {78452001-58C2-4248-8876-9451C3FBBD43}

#### Control—OptInCheckbox
- Name: Opt -in this contact
- Type: CheckBox
- Screen: OptInScreen
- Parent: SuggestNewsletteropt-in
- Bounds: 79, 301, 250, 20
- Enabled: true
- State: Unchecked
- GUID: {6CAF68D1-533F-4ce8-9035-104302DEAB0C}

#### Control—OptInHeader
- Name: Suggest Newsletter Opt-in
- Type: Header
- Screen: OptInScreen
- Parent: SuggestNewsletteropt-in
- Bounds: 79, 141, 498, 47
- GUID: {47BED7D8-662F-4bce-A8C2-94678C4C5ABB}

#### Control—OptInMessage
- Name: OptInMessage
- Type: TextBlock
- Screen: OptInScreen
- Parent: SuggestNewsletteropt-in
- Bounds: 79, 234, 400, 40
- Description: This contact holds the Primary or License Holder role and is eligible for the EAxNewsletter.
- GUID: {4B23955B-2AA7-46fe-8814-9BD1257C4886}

## Navigation

- CreateAccountScreen → MergeAccountsScreen [Save, duplicate found]
- CreateAccountScreen → EmailHistoryScreen [Save, no duplicate]
- EmailHistoryScreen → OptInScreen [Continue, Primary or License Holder role]

