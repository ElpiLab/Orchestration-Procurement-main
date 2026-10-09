# PROJECT.md

Complete this document during **BOOTSTRAP**. Keep it concise and specific to
the project created from this template.

## Purpose

- Project name: Procurement Orchestration
- User or organisational problem: Procurement users spend time manually reading supplier quotations and re-entering offer information into internal procurement documents. This project explores whether document extraction can reduce that repetitive data-entry work.
- Intended users: Employees who need to convert a supplier quotation into an internal procurement request.
- Project goal: Accept one supplier quotation PDF and produce a clear, structured internal order draft for the user to review.
- Initial use case: A user uploads one supplier quotation PDF. The system extracts the relevant offer information, validates the extracted data, and returns an internal order draft.
- In scope for this phase:
  - One supplier quotation PDF at a time.
  - Text-based PDFs with a simple, consistent quotation layout.
  - Extraction of supplier name, quotation reference, products, quantities, unit prices, currency, and total when present.
  - Basic validation of required extracted fields and arithmetic consistency when enough data is available.
  - A structured internal order draft that clearly identifies extracted values and missing or uncertain values.
  - Human review before any real order is placed.
  - Optional user instructions that clarify how the quotation should be transformed into the internal draft.
- Out of scope for this phase:
  - OCR for scanned-image PDFs, handwritten documents, or poor-quality scans.
  - Multiple quotation files or quotation comparison.
  - Catalog, SKU, stock, or ERP lookup.
  - Supplier selection, negotiation, or communication.
  - Sending or submitting an order to a supplier.
  - Approval workflows, purchasing limits, authentication, and user accounts.
  - Database persistence and order history.
  - OCI Punchout and other external procurement integrations.
  - Production deployment and automated purchasing decisions.
- Success criteria: For representative text-based supplier quotations, the system extracts the relevant offer data into the correct fields, flags missing or uncertain values for review, preserves the source quotation reference, and never presents an internal draft as a submitted order.

## Architecture

The POC uses a small Clean Architecture boundary with dependencies pointing
inward:

`domain ← application ← interfaces ← infrastructure`

- `domain`: quotation, quotation item, extracted field, validation warning, and
  internal order draft models. Domain rules cover required fields, numeric
  values, totals, and the draft review status.
- `application`: the quotation-to-order-draft use case. It coordinates text
  extraction, field mapping, validation, and draft creation.
- `interfaces`: a browser UI for PDF upload and draft review, plus an HTTP
  endpoint for the same workflow.
- `infrastructure`: PDF text extraction and any replaceable extraction/model
  adapter. The application does not depend directly on a specific extraction
  provider.

The first POC is stateless: the uploaded PDF and generated draft are processed
in one request and are not persisted. SQLite persistence and draft history are
deferred until the core workflow is demonstrated successfully. See
`docs/adr/ADR-001-stateless-first-poc.md`.

## Structure

```text
src/app/domain
src/app/application
src/app/interfaces
src/app/interfaces/templates
src/app/interfaces/static
src/app/infrastructure
tests/unit
tests/integration
```

## Commands

Document the commands for the selected stack:

| Activity | Command |
|---|---|
| Install | `pip install -r environments/python/requirements.txt` |
| Unit tests | `pytest tests/unit` |
| Integration tests | `pytest tests/integration` |
| E2E tests | `pytest tests/e2e` |
| Run locally | `uvicorn app.interfaces.api:app --app-dir src --reload` |
| Build container | `docker build --tag procurement-orchestration:validation .` |
| Run container | `docker run --rm --publish 8000:8000 procurement-orchestration:validation` |
| Build/release | Local Docker image only; no remote artifact publishing |

## Dependencies

Dependency manifest: `environments/python/requirements.txt`.

Runtime: Python 3.12, as declared by `environments/python/.python-version`.
The POC requires `pypdf` for text extraction and `python-multipart` for file
uploads. Never commit credentials or secrets.

## Deployment

The class POC is deployed locally as a Docker container. Open
`http://localhost:8000` after starting the container. The GitHub Actions CD
template remains inactive because no remote deployment target has been selected.
No deployment credentials or repository secrets are required.
