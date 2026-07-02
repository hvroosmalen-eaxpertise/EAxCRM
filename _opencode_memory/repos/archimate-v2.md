# ArchiMate Model v2.0

## Date
2026-07-01

## Changes
- Expanded from 44 elements / 57 relationships to 66 elements / 90 relationships
- Added Sales Management BusinessFunction with 5 sub-processes (Handle RFQ, Manage Offer, Procure Licenses & Services, Manage Delivery, Manage Invoicing & Payment)
- Added Vendor BusinessActor
- Added 7 BusinessObjects: Offer Data, Quote Data, Delivery Data, Sales Invoice Data, Procurement Invoice Data, Service Data, Vendor Data
- Added corresponding ApplicationService (Sales Management Service) and DataObjects
- Added 33 new relationships (Composition, Access, Assignment, Flow, Realization)
- Fixed stale descriptions on Purchase Data and Purchase Record (removed references to removed attributes)
- File: models/EAxCRM-Archimate.md

## ArchiMate -> UML Data Model -> BPMN Coverage
The ArchiMate model now covers all three core features:
1. Customer Insight (existing)
2. Newsletter Management (existing)
3. Sales Management (new in v2.0)

Each BusinessFunction decomposes into BusinessProcesses that align with the BPMN models. BusinessObjects map to data model entities.
