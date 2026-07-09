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
- Description: Staff creates a new Customer Account from an organisation name, an address, and one or more Contacts. Required-to-save fields (Organisation Name, first Contact's Name/Email, and the Address block) are the minimal data needed for the Save button to create the Customer + Contact(s); Role/Phone/Opt-in per Contact and Customer Notes are nice-to-have and grouped under "Additional Details (optional)". Redesigned 2026-07-08 to catch up with the CRM-6..12 field/validation requirements (issue #7), which were approved after this screen was first built — see docs/superpowers/specs/2026-07-07-createaccountscreen-redesign-design.md for the full design.

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
- Bounds: 34, 28, 600, 880
- GUID: {975FF198-BA12-49c7-A828-0A8C80EF2B29}

#### Control—AddContactLink
- Name: + Add Contact
- Type: Hyperlink
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 480, 150, 20
- Description: Adds another Name/Email/Role/Phone/Opt-in row. One example row is drawn; adding a 2nd row makes Role required on every row (CRM-9).
- GUID: {898B15F1-E781-4cef-90BE-AFFDC9E03925}

#### Control—SectionAdditionalLabel
- Name: Additional Details (optional)
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 694, 300, 16
- Description: Collapsed by default in the real UI — drawn expanded here for documentation completeness (no native collapsible-section control exists in EA's Wireframing MDG).
- Align Text: Left
- Multiline: false
- GUID: {29782D05-51B6-47bd-AED2-5B0FA38C457E}

#### Control—SectionAddressLabel
- Name: Address
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 520, 300, 16
- Align Text: Left
- Multiline: false
- GUID: {6A009E1F-EF27-48fb-BCC1-DB5B51754B29}

#### Control—Cancel
- Name: Cancel
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 191, 800, 100, 30
- Description: Discards unsaved input and closes the screen without creating a Customer or Contact.
- State: Normal
- GUID: {CA831324-5B0E-4087-98C6-2FC0B2855077}

#### Control—CityLabel
- Name: City
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 654, 100, 13
- Align Text: Left
- Multiline: false
- GUID: {22E5CD87-34C2-4d95-B3B1-54F2DAC8010F}

#### Control—CityField
- Name: CityField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 148, 654, 140, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {4A2812AB-3D50-4ef9-8B5A-FF303648CC43}

#### Control—CreateAccountEmailLabel
- Name: Contact Email
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 348, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {6F79EB95-46D2-4781-8AF0-21C923B3FC17}

#### Control—CreateAccountContactNameLabel
- Name: Contact Name
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 314, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB}

#### Control—CreateAccountEmailField
- Name: ContactEmailField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 348, 250, 24
- Description: Required to save on the first Contact row (Contact.email). Repeats per added Contact row.
- GUID: {59032069-A217-43e1-853A-40192D4D0B30}

#### Control—CreateAccountContactNameField
- Name: ContactNameField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 314, 250, 24
- Description: Required to save on the first Contact row (Contact.name). Repeats per added Contact row.
- GUID: {BAF12E7E-0B73-44f0-A59A-50701990EB61}

#### Control—ContactPhoneField
- Name: ContactPhoneField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 416, 250, 24
- Description: Optional / nice-to-have (Contact.phone) — capturable at creation when visible in the source email footer/signature (CRM-12).
- GUID: {1DB83C3E-F1E4-492d-A1FD-BE01B8DA4ABB}

#### Control—CountryLabel
- Name: Country
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 304, 654, 80, 13
- Align Text: Left
- Multiline: false
- GUID: {B7DE5AFB-D7AB-453c-B93E-0FE5CCB88F4A}

#### Control—CountryField
- Name: CountryField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 384, 654, 120, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {3C7B4B53-9A09-4ed9-8216-8EE3EE85A4D8}

#### Control—CustomerNotesLabel
- Name: Customer Notes
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 724, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {4669AAAE-6801-464a-B755-E37C41BB8CD0}

#### Control—CustomerNotesField
- Name: CustomerNotesField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 724, 300, 50
- Description: Optional / nice-to-have (Customer.notes) — free text, capturable opportunistically at creation (CRM-12). Drawn taller to represent multi-line entry.
- GUID: {F672729D-FAC1-4372-8A5B-9949A0027629}

#### Control—DomainLabel
- Name: Domain
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 200, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {BF1867F4-8925-4ee4-B7F0-BAC14A14A8FB}

#### Control—DomainField
- Name: DomainField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 200, 180, 24
- Description: Email domain to search for (e.g. acme.com). Not saved to the Customer record — purely a lookup aid for prefilling the fields below.
- GUID: {89C7EC25-6A33-4a9a-9B0E-497E5531B2DA}

#### Control—SectionDomainLabel
- Name: Find by Domain (optional)
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 170, 300, 16
- Align Text: Left
- Multiline: false
- GUID: {A455294B-1DD6-4b1f-A80E-0F67233DF930}

#### Control—HouseNumberLabel
- Name: House Number
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 620, 100, 13
- Align Text: Left
- Multiline: false
- GUID: {B06CE72A-31B7-4511-B586-3983F3598AAA}

#### Control—HouseNumberField
- Name: HouseNumberField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 148, 620, 90, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {521AC039-592D-47aa-B994-9CB58DB3E6E0}

#### Control—SectionOrgContactLabel
- Name: Organisation & Contact
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 250, 300, 16
- Align Text: Left
- Multiline: false
- GUID: {C938B402-0E32-478f-A817-2C4B2EB8B099}

#### Control—CreateAccountOrgLabel
- Name: Organisation Name
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 280, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {F3464C6E-98F1-4306-9E25-53DF1D727FBB}

#### Control—CreateAccountOrgField
- Name: OrgNameField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 280, 250, 24
- Description: Required to save. Organisation name for the new Customer (Customer.name).
- GUID: {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA}

#### Control—ContactPhoneLabel
- Name: Phone (optional)
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 416, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {91DC1D85-F87A-4535-BD6D-FA57098D825B}

#### Control—AddressPOBoxTab
- Name: PO Box
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 188, 548, 100, 28
- Description: Address mode toggle (CRM-7), inactive tab. Selecting it swaps the Street fields below for a single PO Box text field — not drawn on this static diagram since only one tab's fields can be foregrounded at a time; documented here instead.
- State: Normal
- GUID: {4267ACB2-91F5-46c2-B02B-F6DF7E9D017F}

#### Control—PostalCodeLabel
- Name: Postal Code
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 254, 620, 90, 13
- Align Text: Left
- Multiline: false
- GUID: {7D0C521E-28B5-4f88-A54B-76923BA8AEDF}

#### Control—PostalCodeField
- Name: PostalCodeField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 344, 620, 100, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {CE19D8A7-0ED0-4cd1-9B42-CD337C9853DD}

#### Control—CreateAccountRoleLabel
- Name: Role
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 382, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2}

#### Control—CreateAccountRoleCombo
- Name: RoleCombo
- Type: ComboBox
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 382, 180, 24
- Description: Optional on the first Contact row — defaults to Primary if left unassigned (CRM-8). Becomes required on every row once a 2nd Contact is added (CRM-9). "Secondary" added as a role option (CRM-10).
- DropDownState: Closed
- Items: Primary, Purchase, Sales, License Holder, Secondary
- GUID: {00DAE181-F318-426d-93EB-1C0ADB06CFF0}

#### Control—CreateAccountSaveButton
- Name: Save
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 800, 100, 30
- Description: Persists the Customer + Contact(s) as one atomic transaction (CRM-6); on success routes to the Duplicate found? check, which decides between Merge Customer Accounts and Retrieve Customer Email History.
- State: Normal
- GUID: {C36B94EF-B3A5-4998-B56E-30495392AB2B}

#### Control—SearchEmailsButton
- Name: Search Emails
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 394, 200, 140, 24
- Description: Scans the configured IMAP mailboxes (han@/sales@/info@eaxpertise.nl) for emails from the given domain and prefills Organisation Name, first Contact's Name/Email, and Address below from the best match, for the rep to review/edit before Save. Distinct from the downstream "Retrieve Customer Email History" screen, which retrieves the full communication history after the account already exists.
- State: Normal
- GUID: {F4A09847-0C8E-43f8-998D-E222C2FB2632}

#### Control—AddressStreetTab
- Name: Street Address
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 548, 140, 28
- Description: Address mode toggle (CRM-7) — mandatory, mutually exclusive with PO Box. No native "Tabs" control exists in EA's Wireframing MDG (see wireframe_config.CONTROL_TYPE_TO_STEREO); represented as a pair of Buttons styled as tabs, State=Selected marking the active mode. Drawn as the default/active tab, showing the Street fields below.
- State: Selected
- GUID: {F3FAC591-136E-4b72-9579-84C0D32B55FF}

#### Control—StreetNameLabel
- Name: Street Name
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 586, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {AF434026-ACC2-42c4-AE8C-6730CF37737D}

#### Control—StreetNameField
- Name: StreetNameField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 586, 300, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {8E7F0F1B-D62E-4e55-996E-CCA02C38A5B1}

#### Control—ContactOptInCheckbox
- Name: This contact has given explicit consent for the newsletter
- Type: CheckBox
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 450, 320, 20
- Description: Contact.opt_in — unchecked by default, only set True with explicit evidence of consent in the source email (CRM-11). Per-Contact, repeats on each added row.
- Enabled: true
- State: Unchecked
- GUID: {7F3E99DA-2139-4454-B4D9-19D030016C43}

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
- Description: Abandons the merge and returns to Create Customer Account so the rep can reconsider the input.
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
- Description: Folds the new account's data into the flagged existing Customer Account, sets the losing Customer.merged_into to point at the survivor (CRM-14), and ends the process at Merged into Existing Account.
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
- Description: Advances to the "Primary or License Holder role?" gateway — routes to Suggest Newsletter Opt-in if the Contact carries an eligible role, otherwise ends the process at Account Ready.
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
- Description: Runs the domain-based IMAP scan across han@/sales@/info@eaxpertise.nl for messages under the Contact's email domain (CRM-15), populates the Matched Communications table, and surfaces discovered addresses to link to existing Contacts or turn into new ones.
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
- Description: Sets Contact.opt_in=True and stamps Contact.opt_in_date (CRM-11, CRM-16); ends the process at Account Ready.
- State: Normal
- GUID: {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518}

#### Control—OptInDeclineButton
- Name: Decline
- Type: Button
- Screen: OptInScreen
- Parent: SuggestNewsletteropt-in
- Bounds: 199, 341, 100, 30
- Description: Leaves Contact.opt_in and Contact.opt_in_date untouched; ends the process at Account Ready.
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
- MergeAccountsScreen → (end — Merged into Existing Account) [Merge]
- MergeAccountsScreen → CreateAccountScreen [Cancel]
- EmailHistoryScreen → OptInScreen [Continue, Primary or License Holder role]
- EmailHistoryScreen → (end — Account Ready) [Continue, any other role]
- OptInScreen → (end — Account Ready) [Confirm]
- OptInScreen → (end — Account Ready) [Decline]

