# Quickstart: Validating Skill Mastery Analytics

**Feature**: `001-skill-mastery-analytics` | **Date**: 2026-10-30
Proof that the feature works end-to-end without reading implementation code.
Detail-level: scenarios + commands + expected outcomes; references:
[data-model.md](data-model.md), [contracts/mastery-api.md](contracts/mastery-api.md).

## Prerequisites

- Node.js 20+ and Python 3 with Playwright installed (see project `README.md`
  → "Run tests").
- A backed-up Google Sheet (deploy discipline from `README.md` → Deploy
  step 1) whenever server code is deployed to the live web app.
- Test data: pilot sheet has graded submissions for `Ali Ahmed` and
  `Mostafa Ahmed`; `Question_Bank` populated (45 sample rows minimum), incl.
  rows for a weak unit and at least one question missing its `Unit / Topic`
  value for the «غير مصنّف» case.

## Regression floor FIRST (constitutional gate)

```bash
npm test                          # 43+ unit/server tests — MUST be green
                                  # (includes refreshed legacy contract tests
                                  #  + new mastery aggregation tests)
python tests/e2e/run_all_e2e.py   # 51 existing scenarios — MUST stay green
python test_ui_buttons.py         # 51 static control checks — MUST stay green
python bundle.py                  # required after any template HTML change;
                                  # Index.bundle.html regenerated, never edited
```

Expected: all suites pass. If `tests/server.test.js` still mis-matches the
current contract (legacy `ADMIN_TOK_*`/PIN-1990 asserts), the test-refresh
task has not landed — do not proceed to feature tests.

## Validation scenarios

### S1 — Student mastery view (spec US1)

1. Enter the student PIN (gateway), open the student panel's mastery/progress
   screen.
2. **Expected**: subjects appear; under each, units with whole-number %,
   Arabic badges (متقن / قابل للتحسن / يحتاج مراجعة / لم يبدأ بعد), attempt
   counts, and trend arrows where ≥ 2 attempts exist. Page interactive in
   < 5 s. Empty-state guidance shows for a fresh student (zero attempts).

### S2 — Parent weak spots + targeted practice (spec US2)

1. Enter the parent PIN, open analytics/plan tabs.
2. **Expected**: weakest top-3 units per child, weakest first, with subject
   + percentage. Choosing targeted practice on a weak unit creates a unit
   practice exam (`UPR_*` exam code, `Unit Practice` type) and a success
   message in Arabic; the student then takes it through the standard exam
   flow (session, timer, submission).

### S3 — Refusal rule

1. Choose targeted practice on a unit whose Question_Bank slice is empty.
2. **Expected**: refusal with an Arabic message (`EMPTY_UNIT_POOL` behavior —
   "add questions first"), no exam row created, no broken UI.

### S4 — NFKC grouping (constitution IV / FR-006)

1. In test data, add two rows for the same unit whose text differs only in
   invisible Unicode variants (e.g. different tão-el hamza forms or Arabic
   digits).
2. **Expected**: the mastery report shows ONE unit, not two; labels render
   correctly RTL.

### S5 — «غير مصنّف» visibility (FR-010)

1. Include a graded submission whose question is missing from the bank or has
   an empty unit/topic.
2. **Expected**: counted under «غير مصنّف» for its subject; excluded from the
   weakest top-3 ranking but visible with its own metrics.

### S6 — Cross-child isolation (FR-003, security)

1. From a student token of one child, request the other child's mastery data
   (API-level check mirroring the contract).
2. **Expected**: `STUDENT_MISMATCH` failure; parent token sees both children;
   no screen/route leaks one child into the other's view.

### S7 — Instant freshness (SC-004)

1. Submit an exam that changes a unit's percentage; reopen the mastery view in
   a new session.
2. **Expected**: the unit's numbers already reflect the submission — no
   manual refresh anywhere.

## Acceptance tracing

Quickstart success = S1–S7 pass on top of a green regression floor. That maps
directly to spec SC-001..SC-005 and the P1/P2/P3 acceptance scenarios in
[spec.md](spec.md).
