# EAxCRM — Data Model

**Model ID**: dm-eacrm
**Purpose**: Logical data model for the EAxCRM Django application
**Version**: 1.0

## Entities

### Class—article
- Name: Article
- Description: A scraped news article with source URL, heading, summary, and selection status for inclusion in a newsletter.
- GUID: {A8A1C7F5-AB9E-477d-82C1-96C80B5C9F42}
- Attributes:
  - id: int <<PK>>
  - source_url: string(200)
  - heading: string(500)
  - summary: text
  - body: text
  - included: boolean
  - discovered_date: datetime

### Class—attachment
- Name: Attachment
- Description: A file attached to a communication, with extracted text content.
- GUID: {7166AEE8-CF2D-4372-BC23-068A510B0124}
- Attributes:
  - id: int <<PK>>
  - filename: string(500)
  - content_type: string(200)
  - file: string(500)
  - parsed_text: text

### Class—communication
- Name: Communication
- Description: Email message retrieved from an IMAP account.
- GUID: {94C6CD4B-43EF-4e8d-A190-EC98D38FF05B}
- Attributes:
  - id: int <<PK>>
  - message_id: string(500)
  - from_address: string(254)
  - to_addresses: text
  - subject: string(500)
  - body: text
  - received_date: datetime
  - raw_email: string(500)
  - linked_to_contact: boolean
  - created_at: datetime

### Class—contact
- Name: Contact
- Description: A person associated with a customer, with a specific role.
- GUID: {DEF8F388-8B44-4425-9F79-7FE63A4C6A0E}
- Attributes:
  - id: int <<PK>>
  - name: string(200)
  - email: string(254)
  - role: string(20)
  - phone: string(50)
  - opt_in: boolean
  - opt_in_date: datetime
  - created_at: datetime
  - updated_at: datetime

### Class—customer
- Name: Customer
- Description: An organization that uses Sparx EA and receives services from EAxpertise.
- GUID: {700996C9-A075-4773-9696-9C9C89125192}
- Attributes:
  - id: int <<PK>>
  - name: string(200)
  - address: text
  - notes: text
  - created_at: datetime
  - updated_at: datetime

### Class—imapaccount
- Name: ImapAccount
- Description: IMAP email account configuration for retrieving communications.
- GUID: {3BD8E116-FF59-4ce7-B1DA-F3B3D854FD53}
- Attributes:
  - id: int <<PK>>
  - email_address: string(254)
  - host: string(200)
  - port: int
  - username: string(200)
  - password: string(200)
  - use_ssl: boolean
  - last_sync: datetime
  - enabled: boolean

### Class—invoice
- Name: Invoice
- Description: An invoice from Sparx Systems (or another supplier) received after quote approval. Holds the procured licenses and services.
- GUID: {3A60FD60-3797-41df-8BED-20A2148B32F5}
- Attributes:
  - id: int <<PK>>
  - invoice_number: string(100)
  - date: date
  - amount: float
  - pdf: string(500)
  - paid: boolean
  - paid_date: date
  - cancelled: boolean
  - notes: text
  - created_at: datetime
  - updated_at: datetime

### Class—license
- Name: License
- Description: License entitlement per customer, including type, start and expiry dates. Can be linked to a purchase and optionally renew a previous license.
- GUID: {B9E262AA-8193-4c39-B5B8-38AF63395457}
- Attributes:
  - id: int <<PK>>
  - license_type: string(200)
  - start_date: date
  - expiry_date: date
  - notes: text
  - created_at: datetime
  - updated_at: datetime

### Class—licenselineitem
- Name: LicenseLineItem
- Description: Individual product or service line items under a license, including 12-month service rentals.
- GUID: {1C8F5735-6BF1-4461-819D-2B729F60AD46}
- Attributes:
  - id: int <<PK>>
  - description: string(500)
  - is_service: boolean
  - quantity: int
  - created_at: datetime

### Class—newsletter
- Name: Newsletter
- Description: A composed EAxNewsletter with articles, branding, delivery status.
- GUID: {AE7A31BB-F127-4567-AC90-1275F4DFDF2B}
- Attributes:
  - id: int <<PK>>
  - title: string(200)
  - subject: string(500)
  - body_html: text
  - body_text: text
  - status: string(10)
  - created_date: datetime
  - sent_date: datetime

### Class—newslettercontact
- Name: NewsletterContact
- Description: Join record linking a newsletter to a contact for send-out tracking, including open and bounce status.
- GUID: {C59F7286-C6EC-4a02-8CA1-E8F24BC7DA65}
- Attributes:
  - id: int <<PK>>
  - sent_date: datetime
  - opened_date: datetime
  - bounced: boolean

### Class—newssource
- Name: NewsSource
- Description: A website scraped for news articles (e.g. SparxSystems.com, sparxsystems.eu).
- GUID: {4381BA0B-6FDB-4af5-A6DC-B71AFD2F0E12}
- Attributes:
  - id: int <<PK>>
  - name: string(200)
  - url: string(200)
  - enabled: boolean

### Class—purchase
- Name: Purchase
- Description: A procurement event for a product or service. Links the Quote that triggered it and the Invoice that fulfilled it.
- GUID: {E16E85CB-5C83-403e-B2FC-517E644EFFC1}
- Attributes:
  - id: int <<PK>>
  - type: string(10)
  - purchase_date: date
  - service_name: string(200)
  - start_month: date
  - expiry_month: date
  - notes: text
  - created_at: datetime
  - updated_at: datetime

### Class—quote
- Name: Quote
- Description: A quote from Sparx Systems (or another supplier) received by email. Reviewed and approved before an invoice is issued.
- GUID: {5C91AF36-E5D9-43aa-BE25-C75405EF7557}
- Attributes:
  - id: int <<PK>>
  - quote_number: string(100)
  - date: date
  - amount: float
  - pdf: string(500)
  - seen: boolean
  - order_placed: boolean
  - cancelled: boolean
  - notes: text
  - created_at: datetime
  - updated_at: datetime

### Class—service
- Name: Service
- GUID: {BBA9619D-9886-4ae6-B9E3-BE69D5959DFB}
- Attributes:
  - (none)

## Relationships

### Association—r-contact-customer
- Source: contact (*)
- Target: customer (1)
- GUID: {C9CA64AF-AFAE-4d9a-9EF9-2014013769F5}

### Association—r-communication-imapaccount
- Source: communication (*)
- Target: imapaccount (1)
- GUID: {2676BB60-3D47-4de3-96BC-4D20293529F5}

### Association—r-attachment-communication
- Source: attachment (*)
- Target: communication (1)
- GUID: {FA6FAD91-7BCF-4ee5-AF68-64E54104BF93}

### Association—r-article-newssource
- Source: article (*)
- Target: newssource (1)
- GUID: {8341222A-BF61-42f4-A635-37C1DD32DC82}

### Association—r-article-newsletter
- Source: article (*)
- Target: newsletter (1)
- GUID: {48E2FEB9-37B8-4165-A2FD-DE27E7C538C6}

### Association—r-newslettercontact-newsletter
- Source: newslettercontact (*)
- Target: newsletter (1)
- GUID: {35628AA4-C765-40bd-8CC4-ACD9186AB74A}

### Association—r-newslettercontact-contact
- Source: newslettercontact (*)
- Target: contact (1)
- GUID: {43479F65-F6DA-4335-A2C7-AEB3FA2CB947}

### Association—r-purchase-customer
- Source: purchase (*)
- Target: customer (1)
- GUID: {005D5D29-0CDA-4b1e-962B-0ED9E2AACA7E}

### Association—r-purchase-quote
- Source: purchase (0..1)
- Target: quote (1)
- Description: Links a procurement event to its originating quote.
- GUID: {7200B9F1-1AAA-4032-98C6-B4765443EA80}

### Association—r-purchase-invoice
- Source: purchase (0..1)
- Target: invoice (1)
- Description: Links a procurement event to its fulfilling invoice.
- GUID: {A4A6C418-1F9B-44a8-9052-8765271B7C7A}

### Association—r-license-customer
- Source: license (*)
- Target: customer (1)
- GUID: {089753EB-B3EF-43aa-A242-08921CDF4DE4}

### Association—r-license-purchase
- Source: license (*)
- Target: purchase (1)
- GUID: {70E45BC5-BD6B-499b-A5BE-34929E9D5C8B}

### Association—r-license-invoice
- Source: license (*)
- Target: invoice (0..1)
- Description: Links a license to the invoice that procured it.
- GUID: {937308B4-849A-444f-8129-1E2E7D04DD92}

### Association—r-license-license
- Source: license (*)
- Target: license (0..1)
- Description: Self-referential — renewed_license FK on License pointing to a previous License.
- GUID: {12777B6B-618F-4b07-9ED2-2C914402AF57}

### Association—r-licenselineitem-license
- Source: licenselineitem (*)
- Target: license (1)
- GUID: {136C85F5-62C6-412a-8860-DCBC2E2A0378}

### Association—r-license-attachment
- Source: license (*)
- Target: attachment (0..1)
- Description: Links a license to the source attachment (PDF/TXT) from which it was extracted.
- GUID: {4B8D0033-C3D1-4201-BEA7-6603066E0229}

