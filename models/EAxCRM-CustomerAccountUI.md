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

#### Control—SectionDomainLabel
- Name: Find by Domain (optional)
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 170, 300, 16
- Align Text: Left
- Multiline: false
- GUID: {C1BE2581-3547-4170-BDBF-9BCC757DE847}

#### Control—DomainLabel
- Name: Domain
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 200, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {3241C6D8-5000-4461-A097-7269E5AB6000}

#### Control—DomainField
- Name: DomainField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 200, 180, 24
- Description: Email domain to search for (e.g. acme.com). Not saved to the Customer record — purely a lookup aid for prefilling the fields below.
- GUID: {F78FC8DB-A3FE-4371-A351-ADDA75C36802}

#### Control—SearchEmailsButton
- Name: Search Emails
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 394, 200, 140, 24
- Description: Scans the configured IMAP mailboxes (han@/sales@/info@eaxpertise.nl) for emails from the given domain and prefills Organisation Name, first Contact's Name/Email, and Address below from the best match, for the rep to review/edit before Save. Distinct from the downstream "Retrieve Customer Email History" screen, which retrieves the full communication history after the account already exists.
- State: Normal
- GUID: {6618471F-CE74-4435-9F5F-FE37697DE8D4}

#### Control—SectionOrgContactLabel
- Name: Organisation & Contact
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 250, 300, 16
- Align Text: Left
- Multiline: false
- GUID: {4733839B-4E0F-4235-84B5-AA7531A8E507}

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

#### Control—CreateAccountContactNameLabel
- Name: Contact Name
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 314, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB}

#### Control—CreateAccountContactNameField
- Name: ContactNameField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 314, 250, 24
- Description: Required to save on the first Contact row (Contact.name). Repeats per added Contact row.
- GUID: {BAF12E7E-0B73-44f0-A59A-50701990EB61}

#### Control—CreateAccountEmailLabel
- Name: Contact Email
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 348, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {6F79EB95-46D2-4781-8AF0-21C923B3FC17}

#### Control—CreateAccountEmailField
- Name: ContactEmailField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 348, 250, 24
- Description: Required to save on the first Contact row (Contact.email). Repeats per added Contact row.
- GUID: {59032069-A217-43e1-853A-40192D4D0B30}

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

#### Control—ContactPhoneLabel
- Name: Phone (optional)
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 416, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {2E46E322-C3D4-4D2A-9840-1E762B241D17}

#### Control—ContactPhoneField
- Name: ContactPhoneField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 416, 250, 24
- Description: Optional / nice-to-have (Contact.phone) — capturable at creation when visible in the source email footer/signature (CRM-12).
- GUID: {8AD9DCDF-B1F8-4FC7-A638-D280D7DE9F3F}

#### Control—ContactOptInCheckbox
- Name: This contact has given explicit consent for the newsletter
- Type: CheckBox
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 450, 320, 20
- Description: Contact.opt_in — unchecked by default, only set True with explicit evidence of consent in the source email (CRM-11). Per-Contact, repeats on each added row.
- Enabled: true
- State: Unchecked
- GUID: {4EF63649-AD63-4CFD-93FD-A2B315F1777B}

#### Control—AddContactLink
- Name: + Add Contact
- Type: Hyperlink
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 480, 150, 20
- Description: Adds another Name/Email/Role/Phone/Opt-in row. One example row is drawn; adding a 2nd row makes Role required on every row (CRM-9).
- GUID: {93A4E782-8251-4148-A28C-1D2433FA3638}

#### Control—SectionAddressLabel
- Name: Address
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 520, 300, 16
- Align Text: Left
- Multiline: false
- GUID: {881723A0-7932-4F69-ADA9-2B23EB355C2D}

#### Control—AddressStreetTab
- Name: Street Address
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 548, 140, 28
- Description: Address mode toggle (CRM-7) — mandatory, mutually exclusive with PO Box. No native "Tabs" control exists in EA's Wireframing MDG (see wireframe_config.CONTROL_TYPE_TO_STEREO); represented as a pair of Buttons styled as tabs, State=Selected marking the active mode. Drawn as the default/active tab, showing the Street fields below.
- State: Selected
- GUID: {C98AC1BD-3A48-41C1-9CEC-FC658731FEEB}

#### Control—AddressPOBoxTab
- Name: PO Box
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 188, 548, 100, 28
- Description: Address mode toggle (CRM-7), inactive tab. Selecting it swaps the Street fields below for a single PO Box text field — not drawn on this static diagram since only one tab's fields can be foregrounded at a time; documented here instead.
- State: Normal
- GUID: {B82244F8-894D-4E05-B380-B369D99AD61D}

#### Control—StreetNameLabel
- Name: Street Name
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 586, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {527CE7AD-A7F8-4919-9838-8E7577629594}

#### Control—StreetNameField
- Name: StreetNameField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 586, 300, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {87098905-3137-459D-82AC-B517C2B92238}

#### Control—HouseNumberLabel
- Name: House Number
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 620, 100, 13
- Align Text: Left
- Multiline: false
- GUID: {D81C3DF1-6806-435F-A8C9-3FD1302C796C}

#### Control—HouseNumberField
- Name: HouseNumberField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 148, 620, 90, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {13A39942-007E-4429-8CFA-3C07AE55AA4C}

#### Control—PostalCodeLabel
- Name: Postal Code
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 254, 620, 90, 13
- Align Text: Left
- Multiline: false
- GUID: {29B49ECE-CB2D-406E-A8B5-E496D1F95151}

#### Control—PostalCodeField
- Name: PostalCodeField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 344, 620, 100, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {9079544C-BED9-428C-A72E-01C9474B2163}

#### Control—CityLabel
- Name: City
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 654, 100, 13
- Align Text: Left
- Multiline: false
- GUID: {2A7E737F-6B0F-47A8-BEAC-4EDCC9EAB543}

#### Control—CityField
- Name: CityField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 148, 654, 140, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {D5B0AF81-0281-42AB-B90F-681E9075A921}

#### Control—CountryLabel
- Name: Country
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 304, 654, 80, 13
- Align Text: Left
- Multiline: false
- GUID: {A612D790-D4D6-4F35-94AB-B52FFB1CCB71}

#### Control—CountryField
- Name: CountryField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 384, 654, 120, 24
- Description: Required to save when Street Address mode is active (CRM-7).
- GUID: {1AD4EB7C-39DC-4C41-A2AA-C0E1177F0CEE}

#### Control—SectionAdditionalLabel
- Name: Additional Details (optional)
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 694, 300, 16
- Align Text: Left
- Multiline: false
- Description: Collapsed by default in the real UI — drawn expanded here for documentation completeness (no native collapsible-section control exists in EA's Wireframing MDG).
- GUID: {E83E220F-42FF-4B20-8BF9-13B0354073CB}

#### Control—CustomerNotesLabel
- Name: Customer Notes
- Type: Label
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 724, 150, 13
- Align Text: Left
- Multiline: false
- GUID: {3F1A9CA8-E999-4222-8234-0B6AFD9DD912}

#### Control—CustomerNotesField
- Name: CustomerNotesField
- Type: TextField
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 204, 724, 300, 50
- Description: Optional / nice-to-have (Customer.notes) — free text, capturable opportunistically at creation (CRM-12). Drawn taller to represent multi-line entry.
- GUID: {E8B1B9D4-9A3B-4CC5-A59B-D9CB8A856DB3}

#### Control—CreateAccountSaveButton
- Name: Save
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 44, 800, 100, 30
- State: Normal
- GUID: {C36B94EF-B3A5-4998-B56E-30495392AB2B}

#### Control—Cancel
- Name: Cancel
- Type: Button
- Screen: CreateAccountScreen
- Parent: CreateCustomerAccount
- Bounds: 191, 800, 100, 30
- State: Normal
- GUID: {CA831324-5B0E-4087-98C6-2FC0B2855077}

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

