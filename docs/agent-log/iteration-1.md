Agent evidence: bootstrap discussion for the procAi supplier-quotation
prototype. Date: 2026-10-22. Agent: coding assistant (anonymized).

Scope: Free Text

I’ll update the bootstrap scope to Option B: one supplier quotation PDF becomes a validated internal order draft for human review. I’ll also update the active use case and backlog, while leaving architecture and implementation decisions for the next phase.

Edit , 

Read , lines 1 to 38
Completed with input: {
  "path": "<workspace>/docs/PROJECT.md",
  "view_range": [
    1,
    38
  ]
}

Read , lines 1 to 22
Completed with input: {
  "path": "<workspace>/docs/TASKS.md",
  "view_range": [
    1,
    22
  ]
}

Search for `free-text|free text|supplier quotation|order draft`

The project scope is now updated to **Option B** in `PROJECT.md`.

## New first-phase scope

```text
Supplier quotation PDF
        ↓
Extract quotation data
        ↓
Validate extracted data
        ↓
Generate internal order draft
        ↓
Human review
```

### The system will handle

- One supplier quotation PDF at a time
- Text-based PDFs with a simple, consistent layout
- Extraction of:
  - Supplier name
  - Quotation reference
  - Product descriptions
  - Quantities
  - Unit prices
  - Currency
  - Total amount, when available
- Basic validation and arithmetic consistency checks
- Missing or uncertain values flagged for human review
- Optional user instructions for transforming the quotation

### Still out of scope

- OCR and scanned-image PDFs
- Multiple quotations or quotation comparison
- Catalog, SKU, stock, or ERP lookup
- Supplier communication or order submission
- Approval workflows
- Authentication and user accounts
- Database persistence
- OCI Punchout
- Automated purchasing decisions

The active use case and backlog were also updated in `TASKS.md`.

The architecture section remains unchanged.


###
1. Specify the user workflow
2. Design the domain entities and data model
3. Decide whether persistence is needed
4. Build the extraction API
5. Build the UI
6. Add database persistence only if it supports the demo


### Entities:
UploadedQuotation
- id
- original_filename
- uploaded_at
- source_reference

Quotation
- supplier_name
- quotation_number
- quotation_date
- currency
- total_amount

QuotationItem
- product_description
- quantity
- unit_price
- line_total

ExtractionResult
- extracted_data
- confidence
- warnings
- missing_fields

OrderDraft
- id
- source_quotation_id
- status: NEEDS_REVIEW | READY_FOR_REVIEW
- items
- validation_messages