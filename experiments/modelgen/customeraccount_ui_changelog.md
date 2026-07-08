## 2026-07-08 11:52:27 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| SectionDomainLabel | Find by Domain (optional) | Label | {A455294B-1DD6-4b1f-A80E-0F67233DF930} |
| DomainLabel | Domain | Label | {BF1867F4-8925-4ee4-B7F0-BAC14A14A8FB} |
| DomainField | DomainField | TextField | {89C7EC25-6A33-4a9a-9B0E-497E5531B2DA} |
| SearchEmailsButton | Search Emails | Button | {F4A09847-0C8E-43f8-998D-E222C2FB2632} |
| SectionOrgContactLabel | Organisation & Contact | Label | {C938B402-0E32-478f-A817-2C4B2EB8B099} |
| ContactPhoneLabel | Phone (optional) | Label | {91DC1D85-F87A-4535-BD6D-FA57098D825B} |
| ContactPhoneField | ContactPhoneField | TextField | {1DB83C3E-F1E4-492d-A1FD-BE01B8DA4ABB} |
| ContactOptInCheckbox | This contact has given explicit consent for the newsletter | CheckBox | {7F3E99DA-2139-4454-B4D9-19D030016C43} |
| AddContactLink | + Add Contact | Hyperlink | {898B15F1-E781-4cef-90BE-AFFDC9E03925} |
| SectionAddressLabel | Address | Label | {6A009E1F-EF27-48fb-BCC1-DB5B51754B29} |
| AddressStreetTab | Street Address | Button | {F3FAC591-136E-4b72-9579-84C0D32B55FF} |
| AddressPOBoxTab | PO Box | Button | {4267ACB2-91F5-46c2-B02B-F6DF7E9D017F} |
| StreetNameLabel | Street Name | Label | {AF434026-ACC2-42c4-AE8C-6730CF37737D} |
| StreetNameField | StreetNameField | TextField | {8E7F0F1B-D62E-4e55-996E-CCA02C38A5B1} |
| HouseNumberLabel | House Number | Label | {B06CE72A-31B7-4511-B586-3983F3598AAA} |
| HouseNumberField | HouseNumberField | TextField | {521AC039-592D-47aa-B994-9CB58DB3E6E0} |
| PostalCodeLabel | Postal Code | Label | {7D0C521E-28B5-4f88-A54B-76923BA8AEDF} |
| PostalCodeField | PostalCodeField | TextField | {CE19D8A7-0ED0-4cd1-9B42-CD337C9853DD} |
| CityLabel | City | Label | {22E5CD87-34C2-4d95-B3B1-54F2DAC8010F} |
| CityField | CityField | TextField | {4A2812AB-3D50-4ef9-8B5A-FF303648CC43} |
| CountryLabel | Country | Label | {B7DE5AFB-D7AB-453c-B93E-0FE5CCB88F4A} |
| CountryField | CountryField | TextField | {3C7B4B53-9A09-4ed9-8216-8EE3EE85A4D8} |
| SectionAdditionalLabel | Additional Details (optional) | Label | {29782D05-51B6-47bd-AED2-5B0FA38C457E} |
| CustomerNotesLabel | Customer Notes | Label | {4669AAAE-6801-464a-B755-E37C41BB8CD0} |
| CustomerNotesField | CustomerNotesField | TextField | {F672729D-FAC1-4372-8A5B-9949A0027629} |

### Renamed
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountRoleLabel | Role | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} | Name: Role (optional) -> Role |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} | Notes: Staff creates a new Customer Account from an organisation name, a Contact name, and a Contact email. Required-to-save fields (Organisation Name, Contact Name, Contact Email) are the minimal data needed for the Save button to create the Customer + Contact; everything else (Role, and Customer.address/notes and Contact.phone, not yet on this screen) is nice-to-have and can be filled in later via an edit screen — decided 2026-07-06 while reviewing this screen against the Customer/Contact data model entities. -> Staff creates a new Customer Account from an organisation name, an address, and one or more Contacts. Required-to-save fields (Organisation Name, first Contact's Name/Email, and the Address block) are the minimal data needed for the Save button to create the Customer + Contact(s); Role/Phone/Opt-in per Contact and Customer Notes are nice-to-have and grouped under "Additional Details (optional)". Redesigned 2026-07-08 to catch up with the CRM-6..12 field/validation requirements (issue #7), which were approved after this screen was first built — see docs/superpowers/specs/2026-07-07-createaccountscreen-redesign-design.md for the full design. |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateCustomerAccount | Create Customer Account | Frame | {975FF198-BA12-49c7-A828-0A8C80EF2B29} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountContactNameLabel | Contact Name | Label | {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB} |  |
| CreateAccountContactNameField | ContactNameField | TextField | {BAF12E7E-0B73-44f0-A59A-50701990EB61} | Notes: Required to save. Name of the initial Contact person (Contact.name) -- added 2026-07-06; the screen previously only captured the Contact's email, with no way to record who that email actually belongs to. -> Required to save on the first Contact row (Contact.name). Repeats per added Contact row. |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} | Notes: Required to save. Email address for the initial Contact (Contact.email). -> Required to save on the first Contact row (Contact.email). Repeats per added Contact row. |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} | Notes: Optional / nice-to-have. May be left unassigned and set later (Contact.role). -> Optional on the first Contact row — defaults to Primary if left unassigned (CRM-8). Becomes required on every row once a 2nd Contact is added (CRM-9). "Secondary" added as a role option (CRM-10). |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| Cancel | Cancel | Button | {CA831324-5B0E-4087-98C6-2FC0B2855077} |  |
| MergeCustomerAccounts | Merge Customer Accounts | Frame | {A19CE38F-D0FF-4fb4-A940-BD2201821AE2} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| CustomerEmailHistory | Customer Email History | Frame | {4CB10ABA-8B5F-4ce7-B9F3-06DB286BAF00} |  |
| EmailHistoryContactLabel | Contact Domain | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactDomainValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| SuggestNewsletteropt-in | Suggest Newsletter opt-in | Frame | {1AE3F6BA-E741-4537-B062-32A2897CDE66} |  |
| contactemailaddress | contact email address | Label | {8171055F-E3C0-43fd-8544-1F7D12A93288} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt -in this contact | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-08 10:35:27 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| SectionDomainLabel | Find by Domain (optional) | Label | {28670252-BA5A-4045-9185-5172F8570017} |
| DomainLabel | Domain | Label | {6E013BC8-F5F8-42ed-91B9-516D12867D11} |
| DomainField | DomainField | TextField | {A314226A-BB94-46fc-94A7-54BE8A0D8A8C} |
| SearchEmailsButton | Search Emails | Button | {E1801A37-63FA-4c74-A5DD-182BCBDA0AFF} |
| SectionOrgContactLabel | Organisation & Contact | Label | {B0409A1B-67A5-454f-B054-8D173D2536BA} |
| ContactPhoneLabel | Phone (optional) | Label | {3CF64259-B8ED-4a62-8AF3-54B56C035C11} |
| ContactPhoneField | ContactPhoneField | TextField | {48FE224E-5992-48ee-B50C-3F4A1DF22E71} |
| ContactOptInCheckbox | This contact has given explicit consent for the newsletter | CheckBox | {517EB787-F1F5-4afd-9889-373E1CCCC51F} |
| AddContactLink | + Add Contact | Hyperlink | {D4F1AA8E-4E1B-4fb3-9F6C-7CEF7179B7A7} |
| SectionAddressLabel | Address | Label | {2D9444CD-947E-4ea4-8B97-ED28DB200FFE} |
| AddressStreetTab | Street Address | Button | {04E28D18-55BD-4f49-9522-C73A413F4AA6} |
| AddressPOBoxTab | PO Box | Button | {5FFA268D-4029-4195-93CF-22F152D0FD92} |
| StreetNameLabel | Street Name | Label | {78ED1336-683F-4a8d-A29C-F045782005F7} |
| StreetNameField | StreetNameField | TextField | {890D5C38-DB54-404e-9DB1-8B0AFFD01FF4} |
| HouseNumberLabel | House Number | Label | {92D81801-FE8D-4477-81B5-D3E5B99A13DF} |
| HouseNumberField | HouseNumberField | TextField | {70945ED4-0052-4539-A61F-4629AE967D3D} |
| PostalCodeLabel | Postal Code | Label | {8EB5FF94-AADE-4ef7-9B32-7B287516BAB4} |
| PostalCodeField | PostalCodeField | TextField | {AC35AFF7-09BD-4a9b-8035-E71F7D8E47BC} |
| CityLabel | City | Label | {E1887061-1489-4f9e-AEED-889896838609} |
| CityField | CityField | TextField | {A574B5AF-C49D-4f85-8BA5-4A5E17C696F1} |
| CountryLabel | Country | Label | {E870095E-7623-46a7-B4CD-4EE7EFF16DF0} |
| CountryField | CountryField | TextField | {7675358C-42FA-4047-AB07-95DD0C89EADE} |
| SectionAdditionalLabel | Additional Details (optional) | Label | {E28A945F-15C2-4bfe-B640-A0DF2863BA4F} |
| CustomerNotesLabel | Customer Notes | Label | {0946BE01-7EFD-4bba-A4EE-AF4D38C1F0A0} |
| CustomerNotesField | CustomerNotesField | TextField | {CB3A3821-4741-4385-B386-ABA51CFE714E} |

### Renamed
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountRoleLabel | Role | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} | Name: Role (optional) -> Role |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} | Notes: Staff creates a new Customer Account from an organisation name, a Contact name, and a Contact email. Required-to-save fields (Organisation Name, Contact Name, Contact Email) are the minimal data needed for the Save button to create the Customer + Contact; everything else (Role, and Customer.address/notes and Contact.phone, not yet on this screen) is nice-to-have and can be filled in later via an edit screen — decided 2026-07-06 while reviewing this screen against the Customer/Contact data model entities. -> Staff creates a new Customer Account from an organisation name, an address, and one or more Contacts. Required-to-save fields (Organisation Name, first Contact's Name/Email, and the Address block) are the minimal data needed for the Save button to create the Customer + Contact(s); Role/Phone/Opt-in per Contact and Customer Notes are nice-to-have and grouped under "Additional Details (optional)". Redesigned 2026-07-08 to catch up with the CRM-6..12 field/validation requirements (issue #7), which were approved after this screen was first built — see docs/superpowers/specs/2026-07-07-createaccountscreen-redesign-design.md for the full design. |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateCustomerAccount | Create Customer Account | Frame | {975FF198-BA12-49c7-A828-0A8C80EF2B29} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountContactNameLabel | Contact Name | Label | {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB} |  |
| CreateAccountContactNameField | ContactNameField | TextField | {BAF12E7E-0B73-44f0-A59A-50701990EB61} | Notes: Required to save. Name of the initial Contact person (Contact.name) -- added 2026-07-06; the screen previously only captured the Contact's email, with no way to record who that email actually belongs to. -> Required to save on the first Contact row (Contact.name). Repeats per added Contact row. |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} | Notes: Required to save. Email address for the initial Contact (Contact.email). -> Required to save on the first Contact row (Contact.email). Repeats per added Contact row. |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} | Notes: Optional / nice-to-have. May be left unassigned and set later (Contact.role). -> Optional on the first Contact row — defaults to Primary if left unassigned (CRM-8). Becomes required on every row once a 2nd Contact is added (CRM-9). "Secondary" added as a role option (CRM-10). |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| Cancel | Cancel | Button | {CA831324-5B0E-4087-98C6-2FC0B2855077} |  |
| MergeCustomerAccounts | Merge Customer Accounts | Frame | {A19CE38F-D0FF-4fb4-A940-BD2201821AE2} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| CustomerEmailHistory | Customer Email History | Frame | {4CB10ABA-8B5F-4ce7-B9F3-06DB286BAF00} |  |
| EmailHistoryContactLabel | Contact Domain | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactDomainValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| SuggestNewsletteropt-in | Suggest Newsletter opt-in | Frame | {1AE3F6BA-E741-4537-B062-32A2897CDE66} |  |
| contactemailaddress | contact email address | Label | {8171055F-E3C0-43fd-8544-1F7D12A93288} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt -in this contact | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-08 10:00:26 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| SectionOrgContactLabel | Organisation & Contact | Label | {58DE7231-8BA2-4c56-B64A-43150F939CFC} |
| ContactPhoneLabel | Phone (optional) | Label | {DAFE21EB-69FA-4194-A4D6-B70685AAA3D4} |
| ContactPhoneField | ContactPhoneField | TextField | {B49486B0-6C75-4c12-99DE-643F93D02BBF} |
| ContactOptInCheckbox | This contact has given explicit consent for the newsletter | CheckBox | {AA2C49C2-4969-4bd3-98D5-81D3680A61E3} |
| AddContactLink | + Add Contact | Hyperlink | {7F78E621-FF72-4265-91D2-8837CBFE10FE} |
| SectionAddressLabel | Address | Label | {60A7739B-5B02-48b0-8009-E714EE1E7EB6} |
| AddressStreetTab | Street Address | Button | {85C3EF10-958D-4b2e-A4E0-7182ABED57F6} |
| AddressPOBoxTab | PO Box | Button | {181F7D78-EE73-4d34-BC16-E03AFE8AA93C} |
| StreetNameLabel | Street Name | Label | {6AA953E4-DEC0-4ed1-9EFF-E0C07E4F89AE} |
| StreetNameField | StreetNameField | TextField | {886A24E6-DD0A-40fd-8BA0-9F951EAC2A0E} |
| HouseNumberLabel | House Number | Label | {6858D4F7-44CC-4815-8088-716D4718CF82} |
| HouseNumberField | HouseNumberField | TextField | {E1552551-87B8-4687-A06C-62C35059C27C} |
| PostalCodeLabel | Postal Code | Label | {86191A45-6FEB-47dd-BC99-3FFB291A3608} |
| PostalCodeField | PostalCodeField | TextField | {C4861069-987D-4472-84B4-3CE473227D34} |
| CityLabel | City | Label | {F8B29747-EF73-4dd2-A819-B8AD811BBC5D} |
| CityField | CityField | TextField | {3C525587-4823-4839-B745-4829762C5C10} |
| CountryLabel | Country | Label | {ADC0005F-48CF-40da-A7F7-809A7C6E4E40} |
| CountryField | CountryField | TextField | {26EE883D-96FA-41f0-BF1F-4C273F6ACCF2} |
| SectionAdditionalLabel | Additional Details (optional) | Label | {D7DA8A42-89C2-43cb-93D6-2226A01EAC74} |
| CustomerNotesLabel | Customer Notes | Label | {B6530A41-0B3E-4cfb-90E8-9A23EC2BA523} |
| CustomerNotesField | CustomerNotesField | TextField | {F365F573-569D-4fd8-AA72-BBA69330A4F3} |

### Renamed
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountRoleLabel | Role | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} | Name: Role (optional) -> Role |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} | Notes: Staff creates a new Customer Account from an organisation name, a Contact name, and a Contact email. Required-to-save fields (Organisation Name, Contact Name, Contact Email) are the minimal data needed for the Save button to create the Customer + Contact; everything else (Role, and Customer.address/notes and Contact.phone, not yet on this screen) is nice-to-have and can be filled in later via an edit screen — decided 2026-07-06 while reviewing this screen against the Customer/Contact data model entities. -> Staff creates a new Customer Account from an organisation name, an address, and one or more Contacts. Required-to-save fields (Organisation Name, first Contact's Name/Email, and the Address block) are the minimal data needed for the Save button to create the Customer + Contact(s); Role/Phone/Opt-in per Contact and Customer Notes are nice-to-have and grouped under "Additional Details (optional)". Redesigned 2026-07-08 to catch up with the CRM-6..12 field/validation requirements (issue #7), which were approved after this screen was first built — see docs/superpowers/specs/2026-07-07-createaccountscreen-redesign-design.md for the full design. |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateCustomerAccount | Create Customer Account | Frame | {975FF198-BA12-49c7-A828-0A8C80EF2B29} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountContactNameLabel | Contact Name | Label | {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB} |  |
| CreateAccountContactNameField | ContactNameField | TextField | {BAF12E7E-0B73-44f0-A59A-50701990EB61} | Notes: Required to save. Name of the initial Contact person (Contact.name) -- added 2026-07-06; the screen previously only captured the Contact's email, with no way to record who that email actually belongs to. -> Required to save on the first Contact row (Contact.name). Repeats per added Contact row. |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} | Notes: Required to save. Email address for the initial Contact (Contact.email). -> Required to save on the first Contact row (Contact.email). Repeats per added Contact row. |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} | Notes: Optional / nice-to-have. May be left unassigned and set later (Contact.role). -> Optional on the first Contact row — defaults to Primary if left unassigned (CRM-8). Becomes required on every row once a 2nd Contact is added (CRM-9). "Secondary" added as a role option (CRM-10). |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| Cancel | Cancel | Button | {CA831324-5B0E-4087-98C6-2FC0B2855077} |  |
| MergeCustomerAccounts | Merge Customer Accounts | Frame | {A19CE38F-D0FF-4fb4-A940-BD2201821AE2} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| CustomerEmailHistory | Customer Email History | Frame | {4CB10ABA-8B5F-4ce7-B9F3-06DB286BAF00} |  |
| EmailHistoryContactLabel | Contact Domain | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactDomainValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| SuggestNewsletteropt-in | Suggest Newsletter opt-in | Frame | {1AE3F6BA-E741-4537-B062-32A2897CDE66} |  |
| contactemailaddress | contact email address | Label | {8171055F-E3C0-43fd-8544-1F7D12A93288} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt -in this contact | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-06 21:56:43 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

## 2026-07-06 21:56:16 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |  |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateCustomerAccount | Create Customer Account | Frame | {975FF198-BA12-49c7-A828-0A8C80EF2B29} |  |
| Cancel | Cancel | Button | {CA831324-5B0E-4087-98C6-2FC0B2855077} |  |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountContactNameLabel | Contact Name | Label | {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |  |
| CreateAccountContactNameField | ContactNameField | TextField | {BAF12E7E-0B73-44f0-A59A-50701990EB61} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |  |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} |  |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| MergeCustomerAccounts | Merge Customer Accounts | Frame | {A19CE38F-D0FF-4fb4-A940-BD2201821AE2} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| CustomerEmailHistory | Customer Email History | Frame | {4CB10ABA-8B5F-4ce7-B9F3-06DB286BAF00} |  |
| EmailHistoryContactLabel | Contact Domain | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactDomainValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| SuggestNewsletteropt-in | Suggest Newsletter opt-in | Frame | {1AE3F6BA-E741-4537-B062-32A2897CDE66} |  |
| contactemailaddress | contact email address | Label | {8171055F-E3C0-43fd-8544-1F7D12A93288} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt -in this contact | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-06 21:42:55 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |  |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateCustomerAccount | Create Customer Account | Frame | {975FF198-BA12-49c7-A828-0A8C80EF2B29} |  |
| Cancel | Cancel | Button | {CA831324-5B0E-4087-98C6-2FC0B2855077} |  |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountContactNameLabel | Contact Name | Label | {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |  |
| CreateAccountContactNameField | ContactNameField | TextField | {BAF12E7E-0B73-44f0-A59A-50701990EB61} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |  |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} |  |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| MergeCustomerAccounts | Merge Customer Accounts | Frame | {A19CE38F-D0FF-4fb4-A940-BD2201821AE2} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| CustomerEmailHistory | Customer Email History | Frame | {4CB10ABA-8B5F-4ce7-B9F3-06DB286BAF00} |  |
| EmailHistoryContactLabel | Contact Domain | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactDomainValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| SuggestNewsletteropt-in | Suggest Newsletter opt-in | Frame | {1AE3F6BA-E741-4537-B062-32A2897CDE66} |  |
| contactemailaddress | contact email address | Label | {8171055F-E3C0-43fd-8544-1F7D12A93288} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt -in this contact | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-06 21:42:37 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

## 2026-07-06 21:41:26 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |  |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateCustomerAccount | Create Customer Account | Frame | {975FF198-BA12-49c7-A828-0A8C80EF2B29} |  |
| Cancel | Cancel | Button | {CA831324-5B0E-4087-98C6-2FC0B2855077} |  |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountContactNameLabel | Contact Name | Label | {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |  |
| CreateAccountContactNameField | ContactNameField | TextField | {BAF12E7E-0B73-44f0-A59A-50701990EB61} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |  |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} |  |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| MergeCustomerAccounts | Merge Customer Accounts | Frame | {A19CE38F-D0FF-4fb4-A940-BD2201821AE2} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| CustomerEmailHistory | Customer Email History | Frame | {4CB10ABA-8B5F-4ce7-B9F3-06DB286BAF00} |  |
| EmailHistoryContactLabel | Contact Domain | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactDomainValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| SuggestNewsletteropt-in | Suggest Newsletter opt-in | Frame | {1AE3F6BA-E741-4537-B062-32A2897CDE66} |  |
| contactemailaddress | contact email address | Label | {8171055F-E3C0-43fd-8544-1F7D12A93288} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt -in this contact | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-06 21:40:56 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

## 2026-07-06 21:33:47 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| CreateAccountContactNameLabel | Contact Name | Label | {BE9FF8C0-8C57-48f2-BB01-73D7E95AC3EB} |
| CreateAccountContactNameField | ContactNameField | TextField | {BAF12E7E-0B73-44f0-A59A-50701990EB61} |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} | Notes: Staff creates a new Customer Account from an organisation name and one initial Contact email. Role is optional at this point. -> Staff creates a new Customer Account from an organisation name, a Contact name, and a Contact email. Required-to-save fields (Organisation Name, Contact Name, Contact Email) are the minimal data needed for the Save button to create the Customer + Contact; everything else (Role, and Customer.address/notes and Contact.phone, not yet on this screen) is nice-to-have and can be filled in later via an edit screen — decided 2026-07-06 while reviewing this screen against the Customer/Contact data model entities. |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateCustomerAccount | Create Customer Account | Frame | {975FF198-BA12-49c7-A828-0A8C80EF2B29} |  |
| Cancel | Cancel | Button | {CA831324-5B0E-4087-98C6-2FC0B2855077} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} | Notes: Organisation name for the new Customer. -> Required to save. Organisation name for the new Customer (Customer.name). |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} | Notes: Email address for the initial Contact. -> Required to save. Email address for the initial Contact (Contact.email). |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |  |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} | Notes:  -> Optional / nice-to-have. May be left unassigned and set later (Contact.role). |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| MergeCustomerAccounts | Merge Customer Accounts | Frame | {A19CE38F-D0FF-4fb4-A940-BD2201821AE2} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| CustomerEmailHistory | Customer Email History | Frame | {4CB10ABA-8B5F-4ce7-B9F3-06DB286BAF00} |  |
| EmailHistoryContactLabel | Contact Domain | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactDomainValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| SuggestNewsletteropt-in | Suggest Newsletter opt-in | Frame | {1AE3F6BA-E741-4537-B062-32A2897CDE66} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| contactemailaddress | contact email address | Label | {8171055F-E3C0-43fd-8544-1F7D12A93288} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt -in this contact | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-06 21:22:21 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| CreateCustomerAccount | Create Customer Account | Frame | {975FF198-BA12-49c7-A828-0A8C80EF2B29} |
| Cancel | Cancel | Button | {CA831324-5B0E-4087-98C6-2FC0B2855077} |
| MergeCustomerAccounts | Merge Customer Accounts | Frame | {A19CE38F-D0FF-4fb4-A940-BD2201821AE2} |
| CustomerEmailHistory | Customer Email History | Frame | {4CB10ABA-8B5F-4ce7-B9F3-06DB286BAF00} |
| SuggestNewsletteropt-in | Suggest Newsletter opt-in | Frame | {1AE3F6BA-E741-4537-B062-32A2897CDE66} |
| contactemailaddress | contact email address | Label | {8171055F-E3C0-43fd-8544-1F7D12A93288} |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |  |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |  |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} |  |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| EmailHistoryContactLabel | Contact Domain | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactDomainValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt -in this contact | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-06 21:21:17 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| Cancel | Cancel | Control |  |
| CreateAccountEmailField | ContactEmailField | Control |  |
| CreateAccountEmailLabel | Contact Email | Control |  |
| CreateAccountOrgField | OrgNameField | Control |  |
| CreateAccountOrgLabel | Organisation Name | Control |  |
| CreateAccountRoleCombo | RoleCombo | Control |  |
| CreateAccountRoleLabel | Role (optional) | Control |  |
| CreateAccountSaveButton | Save | Control |  |
| EmailHistoryContactLabel | Contact Domain | Control |  |
| EmailHistoryContactValue | ContactDomainValue | Control |  |
| EmailHistoryContinueButton | Continue | Control |  |
| EmailHistoryHeader | Customer Email History | Control |  |
| EmailHistoryScanButton | Scan Mailboxes | Control |  |
| EmailHistoryTable | Matched Communications | Control |  |
| MergeButton | Merge | Control |  |
| MergeCancelButton | Cancel | Control |  |
| MergeExistingLabel | Matched Existing Account | Control |  |
| MergeExistingSummary | ExistingAccountSummary | Control |  |
| MergeHeader | Merge Customer Accounts | Control |  |
| MergeNewLabel | New Account | Control |  |
| MergeNewSummary | NewAccountSummary | Control |  |
| OptInCheckbox | Opt -in this contact | Control |  |
| OptInConfirmButton | Confirm | Control |  |
| OptInDeclineButton | Decline | Control |  |
| OptInHeader | Suggest Newsletter Opt-in | Control |  |
| OptInMessage | OptInMessage | Control |  |
| contactemailaddress | contact email address | Control |  |

## 2026-07-06 21:13:17 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| CreateCustomerAccount | Create Customer Account | Control |  |
| CustomerEmailHistory | Customer Email History | Control |  |
| MergeCustomerAccounts | Merge Customer Accounts | Control |  |
| SuggestNewsletteropt-in | Suggest Newsletter opt-in | Control |  |

### Deleted
| eid | Name | Type | GUID |
|-----|------|------|------|
| CreateAccountEmailField | ContactEmailField | Control |  |
| CreateAccountEmailLabel | Contact Email | Control |  |
| CreateAccountOrgField | OrgNameField | Control |  |
| CreateAccountOrgLabel | Organisation Name | Control |  |
| CreateAccountRoleCombo | RoleCombo | Control |  |
| CreateAccountRoleLabel | Role (optional) | Control |  |
| CreateAccountSaveButton | Save | Control |  |
| EmailHistoryContactLabel | Contact Email | Control |  |
| EmailHistoryContactValue | ContactEmailValue | Control |  |
| EmailHistoryContinueButton | Continue | Control |  |
| EmailHistoryHeader | Customer Email History | Control |  |
| EmailHistoryScanButton | Scan Mailboxes | Control |  |
| EmailHistoryTable | Matched Communications | Control |  |
| MergeButton | Merge | Control |  |
| MergeCancelButton | Cancel | Control |  |
| MergeExistingLabel | Matched Existing Account | Control |  |
| MergeExistingSummary | ExistingAccountSummary | Control |  |
| MergeHeader | Merge Customer Accounts | Control |  |
| MergeNewLabel | New Account | Control |  |
| MergeNewSummary | NewAccountSummary | Control |  |
| OptInCheckbox | Opt this contact in | Control |  |
| OptInConfirmButton | Confirm | Control |  |
| OptInDeclineButton | Decline | Control |  |
| OptInHeader | Suggest Newsletter Opt-in | Control |  |
| OptInMessage | OptInMessage | Control |  |

## 2026-07-06 19:25:17 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

## 2026-07-06 19:24:50 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |  |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |  |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} |  |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| EmailHistoryContactLabel | Contact Email | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactEmailValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt this contact in | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-06 19:17:26 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |  |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |  |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} |  |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| EmailHistoryContactLabel | Contact Email | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryContactValue | ContactEmailValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |
| OptInCheckbox | Opt this contact in | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-06 19:16:56 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

## 2026-07-06 19:15:42 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

## 2026-07-06 19:15:08 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |  |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |  |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |  |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} |  |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryContactLabel | Contact Email | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContactValue | ContactEmailValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |
| OptInCheckbox | Opt this contact in | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |

## 2026-07-06 19:14:06 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |  |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryContactValue | ContactEmailValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |

## 2026-07-06 19:12:48 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| CreateAccountEmailField | ContactEmailField | Control |  |
| CreateAccountEmailLabel | Contact Email | Control |  |
| CreateAccountHeader | Create Customer Account | Control |  |
| CreateAccountOrgField | OrgNameField | Control |  |
| CreateAccountOrgLabel | Organisation Name | Control |  |
| CreateAccountRoleCombo | RoleCombo | Control |  |
| CreateAccountRoleLabel | Role (optional) | Control |  |
| CreateAccountSaveButton | Save | Control |  |
| EmailHistoryContactLabel | Contact Email | Control |  |
| EmailHistoryContactValue | ContactEmailValue | Control |  |
| EmailHistoryContinueButton | Continue | Control |  |
| EmailHistoryHeader | Customer Email History | Control |  |
| EmailHistoryScanButton | Scan Mailboxes | Control |  |
| EmailHistoryTable | Matched Communications | Control |  |
| MergeButton | Merge | Control |  |
| MergeCancelButton | Cancel | Control |  |
| MergeExistingLabel | Matched Existing Account | Control |  |
| MergeExistingSummary | ExistingAccountSummary | Control |  |
| MergeHeader | Merge Customer Accounts | Control |  |
| MergeNewLabel | New Account | Control |  |
| MergeNewSummary | NewAccountSummary | Control |  |
| OptInCheckbox | Opt this contact in | Control |  |
| OptInConfirmButton | Confirm | Control |  |
| OptInDeclineButton | Decline | Control |  |
| OptInHeader | Suggest Newsletter Opt-in | Control |  |
| OptInMessage | OptInMessage | Control |  |

## 2026-07-06 19:11:37 — Audit, run cap-ui-eacrm

### Checkpoints
- Sync from EA

### Deleted
| eid | Name | Type | GUID |
|-----|------|------|------|
| CreateAccountEmailField | ContactEmailField | Control |  |
| CreateAccountEmailLabel | Contact Email | Control |  |
| CreateAccountHeader | Create Customer Account | Control |  |
| CreateAccountOrgField | OrgNameField | Control |  |
| CreateAccountOrgLabel | Organisation Name | Control |  |
| CreateAccountRoleCombo | RoleCombo | Control |  |
| CreateAccountRoleLabel | Role (optional) | Control |  |
| CreateAccountSaveButton | Save | Control |  |
| EmailHistoryContactLabel | Contact Email | Control |  |
| EmailHistoryContactValue | ContactEmailValue | Control |  |
| EmailHistoryContinueButton | Continue | Control |  |
| EmailHistoryHeader | Customer Email History | Control |  |
| EmailHistoryScanButton | Scan Mailboxes | Control |  |
| EmailHistoryTable | Matched Communications | Control |  |
| MergeButton | Merge | Control |  |
| MergeCancelButton | Cancel | Control |  |
| MergeExistingLabel | Matched Existing Account | Control |  |
| MergeExistingSummary | ExistingAccountSummary | Control |  |
| MergeHeader | Merge Customer Accounts | Control |  |
| MergeNewLabel | New Account | Control |  |
| MergeNewSummary | NewAccountSummary | Control |  |
| OptInCheckbox | Opt this contact in | Control |  |
| OptInConfirmButton | Confirm | Control |  |
| OptInDeclineButton | Decline | Control |  |
| OptInHeader | Suggest Newsletter Opt-in | Control |  |
| OptInMessage | OptInMessage | Control |  |

## 2026-07-06 19:11:04 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |  |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |  |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |  |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |  |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |  |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |  |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |  |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |  |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |  |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |  |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} |  |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |  |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |  |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |  |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |  |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |  |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |  |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |  |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |  |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |  |
| EmailHistoryContactLabel | Contact Email | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |  |
| EmailHistoryContactValue | ContactEmailValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |  |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |  |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |  |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |  |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |  |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |  |
| OptInCheckbox | Opt this contact in | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |  |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |  |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |  |

## 2026-07-06 19:10:37 — Audit, run cap-ui-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| CreateAccountScreen | Create Customer Account | Screen | {D856F705-54EF-4f5b-963B-7193F99EEB38} |
| MergeAccountsScreen | Merge Customer Accounts | Screen | {BD83141A-3F68-4e06-ABAA-CFB1F20D5D68} |
| EmailHistoryScreen | Retrieve Customer Email History | Screen | {18A7FBC2-28B0-4043-9304-8C5068B7DD8D} |
| OptInScreen | Suggest Newsletter Opt-in | Screen | {B037917E-C155-4167-A348-D4EA003F747E} |
| CreateAccountHeader | Create Customer Account | Header | {95707E93-1976-4bf9-A7D6-3B14DCA7C5DF} |
| CreateAccountOrgLabel | Organisation Name | Label | {F3464C6E-98F1-4306-9E25-53DF1D727FBB} |
| CreateAccountOrgField | OrgNameField | TextField | {1CAD9E69-C02C-4cbb-B2C0-6E8B6F3BE0AA} |
| CreateAccountEmailLabel | Contact Email | Label | {6F79EB95-46D2-4781-8AF0-21C923B3FC17} |
| CreateAccountEmailField | ContactEmailField | TextField | {59032069-A217-43e1-853A-40192D4D0B30} |
| CreateAccountRoleLabel | Role (optional) | Label | {64E3F738-6013-42e6-ABFF-56AEDB9A6CC2} |
| CreateAccountRoleCombo | RoleCombo | ComboBox | {00DAE181-F318-426d-93EB-1C0ADB06CFF0} |
| CreateAccountSaveButton | Save | Button | {C36B94EF-B3A5-4998-B56E-30495392AB2B} |
| MergeHeader | Merge Customer Accounts | Header | {88BC7565-848C-4947-ACD4-0B5F87D3CED0} |
| MergeNewLabel | New Account | Label | {2BD56BBA-C370-43db-8762-B1B01BBB5884} |
| MergeNewSummary | NewAccountSummary | TextBlock | {392FF052-CB26-4cd7-8A90-EF87226FE119} |
| MergeExistingLabel | Matched Existing Account | Label | {A3AE6314-8751-439c-9A0C-6BE9A86A5F80} |
| MergeExistingSummary | ExistingAccountSummary | TextBlock | {D063D316-BFE7-41eb-8F63-2AF875F106BD} |
| MergeButton | Merge | Button | {88E3E477-1D90-4522-B793-F14F74370696} |
| MergeCancelButton | Cancel | Button | {07DB66E8-B99B-46c9-BA02-14A16B08E789} |
| EmailHistoryHeader | Customer Email History | Header | {62F8DACA-E86A-40b1-8BEA-4DEDE39B013F} |
| EmailHistoryContactLabel | Contact Email | Label | {1E82D3EF-4658-423f-9409-BC1863997CB1} |
| EmailHistoryContactValue | ContactEmailValue | TextBlock | {A19391A0-1832-4861-8E90-4597C9A90A2F} |
| EmailHistoryScanButton | Scan Mailboxes | Button | {1CB3461F-6C78-45a3-8C20-78847FEF0B10} |
| EmailHistoryTable | Matched Communications | Table | {111D3E6E-E80E-43de-A809-18D9FE3B7F39} |
| EmailHistoryContinueButton | Continue | Button | {DC8F0AA8-CB6E-41e2-A15A-012485C22452} |
| OptInHeader | Suggest Newsletter Opt-in | Header | {47BED7D8-662F-4bce-A8C2-94678C4C5ABB} |
| OptInMessage | OptInMessage | TextBlock | {4B23955B-2AA7-46fe-8814-9BD1257C4886} |
| OptInCheckbox | Opt this contact in | CheckBox | {6CAF68D1-533F-4ce8-9035-104302DEAB0C} |
| OptInConfirmButton | Confirm | Button | {562B3DE5-29BD-4f3e-A83E-4EB8A5E3B518} |
| OptInDeclineButton | Decline | Button | {78452001-58C2-4248-8876-9451C3FBBD43} |
|  | Create Customer Account -> Merge Customer Accounts | Navigation | {B228B47B-B7BD-4aad-B345-DF38890E8332} |
|  | Create Customer Account -> Retrieve Customer Email History | Navigation | {2FA2CEFF-BCAA-4250-A707-B57C6F4DD349} |
|  | Retrieve Customer Email History -> Suggest Newsletter Opt-in | Navigation | {D4FC0236-7B78-4c40-B391-E4D2CA4D0AE8} |

