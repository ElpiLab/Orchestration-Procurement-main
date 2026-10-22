# procAi UI Contract

Status: Proposed

This document freezes the current presentation contract for Slice 0. Future
slices may replace hard-coded values with server-provided data, but they must
preserve the markup, visible copy, classes, hooks, tokens, fonts, and browser
behaviour listed here. New error states may append CSS rules without changing
the existing design.

## Shared shell

The draftroom, user, and procurement pages use the `topbar`, `brand`,
`brand__mark`, `brand__muted`, `status-dot`, `meta-divider`, `shell` or
role-specific shell, `role-switcher`, and three role cards:
`role-card--all`, `role-card--user`, and `role-card--procurement`. Each card
has the corresponding `data-role` hook where present and links to `/`,
`/user`, or `/procurement`. The workspace header uses `workspace__header` and
the green `pill--green` with `PROCESSING LOCAL`.

The shared copy includes `procAi`, `LOCAL POC`, the year `2026`, the workflow
labels `QUOTATION INTELLIGENCE`, `Human in the loop`, and the
not-submitted message:
`This is an internal draft. It has not been submitted to a supplier.`

Fonts are Space Grotesk and DM Mono. Design tokens are `--ink`, `--muted`,
`--paper`, `--panel`, `--panel-soft`, `--green`, `--blue`, and `--amber`.

## Draftroom (`/` and result from `POST /order-drafts`)

The intro panel contains:

- `From supplier PDF` / `to a draft worth reviewing.`
- `Upload`, `Extract`, and `Review`, numbered `01`, `02`, and `03`
- `Human in the loop` and `This demo creates an internal draft only. No order
  is sent.`

The upload card has `data-upload-card`, `data-upload-form`, `data-file-name`,
`#quotation-file`, and `#instructions`. Its copy includes `Drop a quotation PDF
here`, `OPTIONAL INSTRUCTIONS`, and `Create internal draft`.

The result area contains `EXTRACTION RESULT`, `Ready for human review`, the
`NEEDS_REVIEW` amber pill, metrics labelled `SUPPLIER`, `REFERENCE`, `CURRENCY`,
and `TOTAL`, and the `Review queue` table. Its eight headers are `SUPPLIER`,
`PRODUCT DESCRIPTION`, `QTY`, `UNIT PRICE`, `LINE TOTAL`, `ONBOARDED?`, `COST
CENTER`, and `DECISION`.

Review rows use `data-review-row`, `data-onboarded`, `table-input`,
`data-row-status`, and `data-row-action="validate|reject"`. The page also
contains `Validation notes`, `Fields to verify`, `NEXT ACTIONS`, the review
fields `REQUESTER`, `COST CENTER`, `NEED-BY DATE`, and `AMOUNT TO VALIDATE`
with `data-review-field`, and action buttons
`data-action="queue|validate|prepare"` with `data-action-feedback`.

## User page (`/user`)

The page title is `Internal Draft`. It contains four
`user-section-card` sections:

- `OVERVIEW` / `Your requests at a glance`
- `SENT` / `Requests sent`
- `REJECTED` / `Requests needing changes`
- `DRAFTS` / `Continue a draft`

The overview uses `user-stat-row`. Empty states are `No sent requests yet`
and `No rejected requests`. The draft action is `View draft queue →`.

## Procurement page (`/procurement`)

The page contains `Review queue`, `Order overview`, and `DEMO QUEUE · LOCAL
ONLY`. The metric labels are `Orders today`, `Pending review`, `Validated`,
and `Total value`, with their existing sublabels.

The queue tabs use `queue-tabs`, `queue-tab`, `queue-tab--active`, and
`data-queue-filter="all|pending|validated"`. The queue table has headers
`REQUEST`, `PRODUCT DESCRIPTION`, `QTY`, `UNIT PRICE`, `LINE TOTAL`, `STATUS`,
`COST CENTER`, and `DECISION`. Rows are under `data-queue-rows` and use
`data-request-status`, `data-row-status`, and `data-row-action`.

## State classes and browser behaviour

The JavaScript state classes are `is-dragging`, `is-warning`, `is-complete`,
`row-status--validated`, `row-status--rejected`, `row-status--warning`,
`queue-badge--pending`, `queue-badge--validated`, `queue-badge--rejected`,
and `queue-tab--active`.

`static/app.js` displays the selected file name, supports drag and drop for
PDF files, changes the submit button to `Extracting quotation...`, validates
required action fields, shows demo action feedback, validates or rejects
review rows, updates queue status badges, and filters procurement rows through
the three queue tabs. These behaviours remain client-side until a later slice
wires them to persistence.
