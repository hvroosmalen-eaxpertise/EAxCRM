## 2026-07-08 12:48:51 — Audit, run cap-eacrm

### Deleted
| eid | Name | Type | GUID |
|-----|------|------|------|
| ConfirmCustomerAccount | Confirm Customer Account | IntermediateEvent |  |

### Connectors
| Action | Type | Source | Target | Condition |
|--------|------|--------|--------|-----------|
| deleted | connector | ConfirmCustomerAccount | CreateCustomerAccount |  |

## 2026-07-06 22:02:57 — Audit, run cap-eacrm

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| NewCustomerContact_CreateCustomerAccount | NewCustomerContact -> CreateCustomerAccount | SequenceFlow |  |
| CreateCustomerAccount_Duplicatefound | CreateCustomerAccount -> Duplicatefound | SequenceFlow |  |
| Duplicatefound_MergeCustomerAccounts | Duplicatefound -> MergeCustomerAccounts | SequenceFlow |  |
| Duplicatefound_RetrieveCustomerEmailHistory | Duplicatefound -> RetrieveCustomerEmailHistory | SequenceFlow |  |
| MergeCustomerAccounts_MergedintoExistingAccount | MergeCustomerAccounts -> MergedintoExistingAccount | SequenceFlow |  |
| RetrieveCustomerEmailHistory_PrimaryorLicenseHolderrole | RetrieveCustomerEmailHistory -> PrimaryorLicenseHolderrole | SequenceFlow |  |
| PrimaryorLicenseHolderrole_SuggestNewsletterOptin | PrimaryorLicenseHolderrole -> SuggestNewsletterOptin | SequenceFlow |  |
| PrimaryorLicenseHolderrole_AccountReady | PrimaryorLicenseHolderrole -> AccountReady | SequenceFlow |  |
| SuggestNewsletterOptin_AccountReady | SuggestNewsletterOptin -> AccountReady | SequenceFlow |  |
| ConfirmCustomerAccount_CreateCustomerAccount | ConfirmCustomerAccount -> CreateCustomerAccount | SequenceFlow |  |
| EmailHistory_RetrieveCustomerEmailHistory | EmailHistory -> RetrieveCustomerEmailHistory | DataInputAssociation |  |
| CustomerAccount_RetrieveCustomerEmailHistory | CustomerAccount -> RetrieveCustomerEmailHistory | DataInputAssociation |  |
| RetrieveCustomerEmailHistory_EmailHistory | RetrieveCustomerEmailHistory -> EmailHistory | DataOutputAssociation |  |
| CreateCustomerAccount_CustomerAccount | CreateCustomerAccount -> CustomerAccount | DataOutputAssociation |  |
| CreateCustomerAccount_Contact | CreateCustomerAccount -> Contact | DataOutputAssociation |  |
| SuggestNewsletterOptin_Contact | SuggestNewsletterOptin -> Contact | DataOutputAssociation |  |

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| ManageCustomerAccount | Manage Customer Account | CollaborationModel | {4D4520AB-EE90-4f73-96FC-116E44DB6007} |  |
| EAxpertise | EAxpertise | Lane | {9402009C-1B33-4877-A69A-CC2EB57691DB} |  |
| AccountReady | Account Ready | EndEvent | {12F7CED7-5CE5-4070-9B73-FB982C101863} |  |
| ConfirmCustomerAccount | Confirm Customer Account | IntermediateEvent | {AD32AD89-C0CA-4001-ACFB-56C1F46601AC} |  |
| Contact | Contact | DataObject | {77AAEBE9-8BA5-4668-9967-629293E99856} |  |
| CreateCustomerAccount | Create Customer Account | Activity | {B4CEA509-838B-4b2b-B8E5-59FE53AC4FA3} |  |
| CustomerAccount | Customer Account | DataObject | {B84756F7-0FA9-4e95-B29A-A861F396ADAC} |  |
| Duplicatefound | Duplicate found? | Gateway | {94E22195-3195-45af-9628-105DBBACEEBB} |  |
| EmailHistory | Email History | DataObject | {F55B3C35-F57B-4535-966F-DDF831EC9807} |  |
| MergeCustomerAccounts | Merge Customer Accounts | Activity | {13A26AFF-4D25-412d-ABBA-565E20C30048} |  |
| MergedintoExistingAccount | Merged into Existing Account | EndEvent | {EAFD19F6-F227-49ee-A9C1-47B8E36AD178} |  |
| NewCustomerContact | New Customer Contact | StartEvent | {739C876F-E4AE-4102-9663-966D2C925D01} |  |
| PrimaryorLicenseHolderrole | Primary or License Holder role? | Gateway | {16CF0C0D-548F-4cb0-8B2A-E536B593612B} |  |
| RetrieveCustomerEmailHistory | Retrieve Customer Email History | Activity | {CA27AF88-ED2F-4653-8059-A61D0BA88A8E} |  |
| SuggestNewsletterOptin | Suggest Newsletter Opt-in | Activity | {8D50E44F-E7EB-4a7f-B861-D0766947A995} |  |

