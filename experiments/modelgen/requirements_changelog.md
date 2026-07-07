## 2026-07-07 12:13:41 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Renamed
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| createaccountscreencreatescustomerandcontactsatomically | CreateAccountScreen: creates Customer and Contacts atomically | Requirement | {D13E63E8-1DA9-4f10-BF1C-8AFC333666C7} | Name: Create Customer Account must create Customer and Contacts atomically -> CreateAccountScreen: creates Customer and Contacts atomically |
| createaccountscreenstructuredstreetaddressorpobox | CreateAccountScreen: structured street address or PO Box | Requirement | {D356ED58-643D-45e6-BC31-CFA401E6C7D1} | Name: Customer address must support both structured street address and PO Box -> CreateAccountScreen: structured street address or PO Box |
| primarycontactruleatleastonecontactmustalwaysbeprimary | Primary Contact Rule: at least one Contact must always be Primary | Requirement | {5E968ECB-4896-45fa-9FAE-4518F9F92ECF} | Name: At least one Contact per Customer must always be Primary -> Primary Contact Rule: at least one Contact must always be Primary |
| contactrolerulerequiredonceasecondcontactexists | Contact Role Rule: required once a second Contact exists | Requirement | {D97412A1-AF30-45ac-AE2D-E6A4A423CF65} | Name: Role becomes required once a second Contact is added -> Contact Role Rule: required once a second Contact exists |
| contactrolerulesecondaryroleadded | Contact Role Rule: Secondary role added | Requirement | {D37E1D4E-051B-455c-8B98-23F98FC4A551} | Name: Role list must include Secondary -> Contact Role Rule: Secondary role added |
| newsletterconsentruleoptindefaultstofalse | Newsletter Consent Rule: opt-in defaults to false | Requirement | {EAAD0687-E661-4943-93EB-86376B3FA8EF} | Name: Newsletter opt-in must default to false and stay editable in two places -> Newsletter Consent Rule: opt-in defaults to false |
| createaccountscreennotesandphonecapturableatcreation | CreateAccountScreen: notes and phone capturable at creation | Requirement | {0EF04071-8682-4579-A08F-8A4F75EE8713} | Name: Notes and phone must be capturable opportunistically at creation time -> CreateAccountScreen: notes and phone capturable at creation |

## 2026-07-07 12:09:55 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Updated
| eid | Name | Type | GUID | Changes |
|-----|------|------|------|---------|
| createcustomeraccountmustcreatecustomerandcontactsatomically | Create Customer Account must create Customer and Contacts atomically | Requirement | {D13E63E8-1DA9-4f10-BF1C-8AFC333666C7} | Notes: The Create Customer Account screen shall create one Customer record and one or more Contact records in a single atomic save operation. A Customer must never be persisted without at least one associated Contact, since the account-creation process treats the organization and its initial contact(s) as one unit of work. -> The Create Customer Account screen shall create one Customer record and one or more Contact records in a single atomic save operation. A Customer must never be persisted without at least one associated Contact, since the account-creation process treats the organization and its initial contact(s) as one unit of work.

Rationale:
Matches the existing BPMN process (EAxCRM-CustomerAccountProcess.md), where account creation is modeled as one atomic activity. Prevents orphan Customer records with no way to reach anyone at the organization.

Test Cases:
- Save with 1 Customer + 1 Contact succeeds and both rows exist.
- Save attempt with Customer fields filled but zero Contacts fails validation.
- A mid-save failure (e.g. DB error on second Contact) rolls back the Customer too — no partial commit. |
| customeraddressmustsupportbothstructuredstreetaddressandpobox | Customer address must support both structured street address and PO Box | Requirement | {D356ED58-643D-45e6-BC31-CFA401E6C7D1} | Notes: The system shall record a Customer's address as either a structured street address (Street Name, House Number, Postal Code, City, Country) or an unstructured PO Box string, selected via a mode toggle on the create screen. Address is mandatory — the rep must actively locate it if not present in the source email. -> The system shall record a Customer's address as either a structured street address (Street Name, House Number, Postal Code, City, Country) or an unstructured PO Box string, selected via a mode toggle on the create screen. Address is mandatory — the rep must actively locate it if not present in the source email.

Rationale:
Real-world postal addresses aren't always street-based; forcing one shape either loses PO Box customers or forces reps to cram a PO Box into a street-shaped field.

Test Cases:
- Street mode requires all five fields before save.
- PO Box mode requires only the PO Box text field; street fields stay null.
- Switching modes clears/ignores the other mode's fields rather than submitting both. |
| atleastonecontactpercustomermustalwaysbeprimary | At least one Contact per Customer must always be Primary | Requirement | {5E968ECB-4896-45fa-9FAE-4518F9F92ECF} | Notes: Regardless of how many Contacts are entered on account creation, exactly one must carry the role Primary. This holds even when only one Contact is entered — in that case the first (and only) Contact row defaults its role to Primary automatically rather than being left blank. -> Regardless of how many Contacts are entered on account creation, exactly one must carry the role Primary. This holds even when only one Contact is entered — in that case the first (and only) Contact row defaults its role to Primary automatically rather than being left blank.

Rationale:
Ensures every account always has one unambiguous point of contact, and gives a clear successor path when combined with the Secondary role (CRM-10).

Test Cases:
- Single-contact save with role left untouched saves with role = Primary.
- Two-contact save where neither is marked Primary is rejected.
- Two-contact save with exactly one Primary succeeds. |
| rolebecomesrequiredonceasecondcontactisadded | Role becomes required once a second Contact is added | Requirement | {D97412A1-AF30-45ac-AE2D-E6A4A423CF65} | Notes: Role is optional only when exactly one Contact exists on the form. As soon as a second Contact row is added, role becomes a required field for every Contact on the form, including ones already entered. -> Role is optional only when exactly one Contact exists on the form. As soon as a second Contact row is added, role becomes a required field for every Contact on the form, including ones already entered.

Rationale:
Prevents accounts with multiple unnamed-function contacts, where reps can no longer tell who does what.

Test Cases:
- One contact, role left at its default, saves fine (subject to CRM-8).
- Add a second contact, leave either role blank — save is rejected.
- Fill both roles — save succeeds. |
| rolelistmustincludesecondary | Role list must include Secondary | Requirement | {D37E1D4E-051B-455c-8B98-23F98FC4A551} | Notes: The Contact role choices shall include Secondary, alongside Primary/Purchase/Sales/License Holder. Secondary denotes a colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties, and is the expected successor role if the Primary contact leaves the organization. -> The Contact role choices shall include Secondary, alongside Primary/Purchase/Sales/License Holder. Secondary denotes a colleague-level backup to the Primary contact with no Purchase, Sales, or License Holder duties, and is the expected successor role if the Primary contact leaves the organization.

Rationale:
Organizations commonly designate a backup point of contact; without this role it would be miscategorized as Purchase/Sales or left blank, losing the succession signal.

Test Cases:
- Role dropdown lists Secondary as a selectable option.
- A Contact saved with role=Secondary persists and displays correctly.
- Filtering/reporting by role can isolate Secondary contacts. |
| newsletteroptinmustdefaulttofalseandstayeditableintwoplaces | Newsletter opt-in must default to false and stay editable in two places | Requirement | {EAAD0687-E661-4943-93EB-86376B3FA8EF} | Notes: Contact.opt_in shall default to False when created via Create Customer Account, and shall only be set True if the rep has explicit evidence of consent in the source email. The same field must remain independently editable later via the existing Suggest Newsletter Opt-in screen. -> Contact.opt_in shall default to False when created via Create Customer Account, and shall only be set True if the rep has explicit evidence of consent in the source email. The same field must remain independently editable later via the existing Suggest Newsletter Opt-in screen.

Rationale:
Marketing consent is a legal/compliance flag and must never be inferred just because a customer initiated contact; giving reps two deliberate checkpoints (creation-time and a later prompt) increases the chance of capturing real consent without ever defaulting to true.

Test Cases:
- New Contact via create screen has opt_in=False when the checkbox is left untouched.
- Checking the box at creation sets opt_in=True and stamps opt_in_date.
- opt_in can later be toggled from the Suggest Newsletter Opt-in screen independent of the create screen's state. |
| notesandphonemustbecapturableopportunisticallyatcreationtime | Notes and phone must be capturable opportunistically at creation time | Requirement | {0EF04071-8682-4579-A08F-8A4F75EE8713} | Notes: The create screen shall include optional fields for Customer.notes (free text) and Contact.phone, since both are sometimes directly available in the source email (footer/signature) and cheaper to capture immediately than via a later edit step. -> The create screen shall include optional fields for Customer.notes (free text) and Contact.phone, since both are sometimes directly available in the source email (footer/signature) and cheaper to capture immediately than via a later edit step.

Rationale:
Reduces follow-up data-entry work when the information is already visible to the rep; both remain optional since they're often absent from a first email.

Test Cases:
- Save succeeds with both fields blank.
- Save succeeds with notes and/or phone filled in.
- Values persist correctly on the respective Customer/Contact records. |

## 2026-07-07 11:52:34 — Audit

### Checkpoints
- Parsed MD
- Diagram complete

### Created
| eid | Name | Type | GUID |
|-----|------|------|------|
| Contact->createcustomeraccountmustcreatecustomerandcontactsatomically | Contact | Realisation | {1C74879A-4D2C-4c13-ABBA-27DC5E85B651} |
| Customer->createcustomeraccountmustcreatecustomerandcontactsatomically | Customer | Realisation | {0BCDDF7D-0CFE-4c97-9BFC-CDC96E52AF63} |
| Customer->customeraddressmustsupportbothstructuredstreetaddressandpobox | Customer | Realisation | {C55E5F91-7486-4351-9CF2-F7936E3C317F} |
| Contact->atleastonecontactpercustomermustalwaysbeprimary | Contact | Realisation | {50B15DAC-B55D-4b70-BB1A-FE73FAF96159} |
| Customer->atleastonecontactpercustomermustalwaysbeprimary | Customer | Realisation | {8ADE32B6-5F31-4448-B360-D28E798E12FF} |
| Contact->rolebecomesrequiredonceasecondcontactisadded | Contact | Realisation | {A66D55F8-E283-481b-9BD3-87094DC4C12F} |
| Contact->rolelistmustincludesecondary | Contact | Realisation | {9AC979CD-7676-4ee7-9405-01AC8A460983} |
| Contact->newsletteroptinmustdefaulttofalseandstayeditableintwoplaces | Contact | Realisation | {EDF5DBD2-F491-4404-985A-8C30B03F0D8E} |
| Contact->notesandphonemustbecapturableopportunisticallyatcreationtime | Contact | Realisation | {80479810-50A0-44df-8FFD-DE61A9E76BE2} |
| Customer->notesandphonemustbecapturableopportunisticallyatcreationtime | Customer | Realisation | {F001412D-C782-4ccb-BE49-2DF5EADFD2BF} |

## 2026-07-06 16:33:27 — Audit

### Checkpoints
- Seeding properties
- Seed complete

## 2026-07-06 16:32:48 — Audit

### Checkpoints
- Sync from EA

## 2026-07-06 16:21:02 — Audit

### Checkpoints
- Sync from EA

### Deleted
| eid | Name | Type | GUID |
|-----|------|------|------|
| eaxcrmmustdetectandflagpotentialduplicatecustomeraccountsformergeordiscard | EAxCRM must detect and flag potential duplicate Customer Accounts for merge or discard | Requirement |  |
| eaxcrmmustretrievecustomeremailhistorybyscanningconfiguredimapmailboxes | EAxCRM must retrieve customer email history by scanning configured IMAP mailboxes | Requirement |  |
| eaxcrmmustsuggestnewsletteroptinforprimaryandlicenseholdercontactspendinguserconfirmation | EAxCRM must suggest newsletter opt-in for Primary and License Holder Contacts pending user confirmation | Requirement |  |
| eaxcrmmustsupportcreatingacustomeraccountwithaminimalinitialcontact | EAxCRM must support creating a Customer Account with a minimal initial Contact | Requirement |  |
| eaxcrmmustverifyorcreatethecustomeraccountwhenregisteringanrfqfromanunrecognizedorganization | EAxCRM must verify or create the Customer Account when registering an RFQ from an unrecognized organization | Requirement |  |

