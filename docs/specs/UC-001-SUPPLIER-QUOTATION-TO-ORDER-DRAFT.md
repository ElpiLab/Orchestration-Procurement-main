# UC-001-SUPPLIER-QUOTATION-TO-ORDER-DRAFT

## Intent

Convert one supplier quotation PDF into a structured internal order draft so a
procurement employee can review the extracted information without re-entering
it manually.

## Actors

Primary  
Procurement employee

Secondary  
Extraction and validation service

## Preconditions

- The user has one text-based supplier quotation PDF.
- The quotation uses a simple, supported layout.
- The user can provide optional instructions about the desired draft.

## Flow

1. The user uploads one supplier quotation PDF.
2. The user optionally enters instructions for transforming the quotation.
3. The system extracts the supplier name, quotation reference, products,
   quantities, unit prices, currency, and total when present.
4. The system validates required fields and checks line totals or the grand
   total when enough values are available.
5. The system displays an internal order draft with extracted values, warnings,
   missing fields, and a clear human-review status.
6. The user reviews the draft; the system does not submit an order.

## Errors

- The uploaded file is not a PDF.
- No file is provided.
- The PDF contains no extractable text.
- The PDF uses an unsupported or ambiguous layout.
- Required quotation data is missing.
- A quantity, price, or total is invalid.
- Calculated totals do not match the extracted totals.
- The request exceeds the one-file-at-a-time scope.

## Acceptance

### Valid quotation

Given a supported text-based quotation containing supplier, reference, item,
quantity, price, currency, and total data  
When the user uploads it  
Then the system displays an internal order draft with those values and marks it
for human review.

### Missing or uncertain data

Given a quotation with missing or uncertain fields  
When the system processes it  
Then the draft identifies the affected fields and displays a warning instead of
silently inventing values.

### Invalid quotation

Given an unsupported file, unreadable PDF, invalid value, or inconsistent total  
When the user uploads it  
Then the system reports the problem clearly and does not create a
submission-ready draft.

### No automatic submission

Given any successfully extracted quotation  
When the draft is displayed  
Then the system clearly identifies it as an internal draft requiring human
review and does not send it to a supplier.

## Tests

Unit  
- Extract fields from representative quotation text.
- Validate required fields and numeric values.
- Detect inconsistent line or grand totals.
- Preserve missing and uncertain values as warnings.

Integration  
- Upload a supported PDF and receive the expected draft response.
- Reject unsupported files and unreadable PDFs with clear errors.

E2E  
- Upload a representative quotation through the user interface and review the
  resulting internal order draft.
