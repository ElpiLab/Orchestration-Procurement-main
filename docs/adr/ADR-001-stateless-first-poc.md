# ADR-001: Stateless First POC

## Status

Accepted for the first POC; persistence remains a planned extension.

## Context

The first demonstrable workflow is one supplier quotation PDF uploaded through a
UI and transformed into an internal order draft for human review. The project
does not yet require user accounts, order history, or reopening drafts.

## Decision

Process each upload and draft in memory for the first POC. Do not add a database
or persistence layer to the first vertical slice.

The POC domain model still has explicit entities:

- `Quotation`: supplier and quotation-level data.
- `QuotationItem`: product, quantity, unit price, and line total.
- `ExtractionResult`: extracted values, confidence or uncertainty, and warnings.
- `OrderDraft`: the internal draft, source reference, validation messages, and
  human-review status.

These entities are application/domain concepts, not a commitment to one table
layout.

## Alternatives considered

- SQLite from the start: enables history earlier, but adds schema, repository,
  lifecycle, and migration work before the extraction workflow is proven.
- External database: unnecessary for a local classroom POC and introduces
  deployment and credential concerns.

## Consequences

- The first demo remains small and easy to run locally.
- Uploaded files and drafts disappear after the request or process ends.
- A later persistence slice can introduce SQLite behind a repository boundary
  without changing the domain workflow.
- The UI must clearly communicate that the draft is temporary and requires
  human review.
