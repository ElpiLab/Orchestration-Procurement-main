# TASKS.md

PHASE: 3
STATUS: done

(0=Bootstrap | 1=Specify | 2=Design | 3=Develop | 4=Validate | 5=Deploy)

## Current Use Case

Supplier quotation PDF to internal order draft

## Backlog

- Presentation-ready procAi browser UI, review queue, and demo-only line
  decisions completed
- User workspace activated with quotation intake, overview, sent, rejected,
  and draft sections; procurement workspace activated with same-day overview,
  pending/validated queues, seeded demo requests, review actions, and
  interactive queue filters
- Local Docker deployment documented; remote deployment intentionally deferred
- Fast Track (2026-10-20): UI color palette restyled after lhotse.de
  (midnight `#121923`, paper `#f3f3ed`, mist `#adc1d1`, slate `#56616b`,
  action blue `#1f63d8`). Scope: `static/styles.css` tokens only; no behavior
  change, DESIGN skipped. Acceptance: all hard-coded colors map to palette
  tokens; `pytest` passes; `/`, `/user`, `/procurement` visually checked.
- Fast Track (2026-10-22): Slice 0 hygiene and UI contract. Scope: repository
  hygiene, anonymized agent evidence, neutral notification copy, and a
  contract test documenting the existing UI. Acceptance: no tracked bytecode,
  no personal path or email in the agent log or UI, and the contract test plus
  existing tests pass. DESIGN skipped because this slice does not change
  application behavior or architecture.
  Prompt note: step 3 already done by me, verify and skip.

## Working agreement

- Keep one active use case small enough to deliver vertically.
- Update this file when the lifecycle phase or active use case changes.
- Link decisions and validation evidence from the relevant project artefact.
