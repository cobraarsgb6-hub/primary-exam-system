# Research: Skill Mastery Analytics

**Feature**: `001-skill-mastery-analytics` | **Date**: 2026-10-30
**Method**: facts gathered by a delegated code exploration of `Code.gs`,
`Portal.js.html`, `HubData.js.html`, `QuizApp.js.html`, `Index.template.html`,
tests, and sample CSV data; every decision below is grounded in verified code
reality (function names cited).

## Decision Log

### D1 — Skill taxonomy source: existing `Unit / Topic` + `Subject` metadata

- **Decision**: Derive "skill" directly from `Question_Bank` columns
  (`Subject`, `Unit / Topic`); no new per-question tagging, no AI clustering.
- **Rationale**: Every bank row already carries both fields (sample data
  verified, e.g. `English Grammar` / `Unit 2 - Lesson 3: Adverbials`); intro of
  a new taxonomy would add data-entry burden and violate constitution
  Principle V.
- **Alternatives considered**: per-question skill tags (rejected: burden,
  drift risk), automatic clustering of question text (rejected:
  non-deterministic, untestable).

### D2 — Grouping key: reuse `normalizeAnswer_`

- **Decision**: Unit key = `normalizeAnswer_(unit/topic string)` (already
  NFKC + tatweel/harakat stripping + alef unification + Arabic-digit → ASCII
  + whitespace collapse); display label = first-seen raw string.
- **Rationale**: Satisfies constitution Principle IV (NFKC) and FR-006 without
  new code; `normalizeAnswer.test.js` already guards its behavior.
- **Alternatives considered**: raw-string equality (fails invisible-Unicode
  edge case), plain `.normalize('NFKC')` only (weaker than what the codebase
  already runs elsewhere — worse consistency).

### D3 — Mastery metric: earned / attempted points over all graded attempts

- **Decision**: Per unit per student:
  `pct = Σ pointsAwarded / Σ maxPoints × 100` across **all** graded
  submissions touching that unit; badge bands متقن ≥ 80, قابل للتحسن 60–79,
  يحتاج مراجعة < 60; trend compares the latest attempt's unit percentage
  against the mean of earlier attempts (rising ≥ +5, falling ≤ −5, else flat).
- **Rationale**: Points are already the grading currency
  (`gradeAnswers_` emits `pointsAwarded`/`maxPoints` per question), so this is
  coloherence with the existing scoring rather than a second metric; matching
  spec FR-001 defaults.
- **Alternatives considered**: question-count percentage (ignores points
  asymmetry), time-decay weighting (v2, out of scope), latest-attempt-only
  (hides overall progress).

### D4 — Compute on read; no analytics sheet

- **Decision**: Aggregation happens per report render with one batched
  `getDataRange()` per sheet (`Submissions`, `Question_Bank`), then in-memory
  joins; no `Mastery` sheet, no stored aggregates.
- **Rationale**: Pilot scale (2 students, hundreds of rows) makes a stored
  durable aggregate pure overhead; constitution Principle V; existing bank
  readers already do full-scan reads, so no new perf pattern is introduced —
  and per-row loops stay out of request handlers.
- **Alternatives considered**: precomputed sheet with formule (rejected:
  write-time complexity, schema migration, drift).

### D5 — Per-question correctness join & "غير مصنّف" bucket

- **Decision**: Parse `Detailed Review JSON` per submission row → items
  `{questionId, isCorrect, pointsAwarded, maxPoints, ...}`; join
  `questionId → Question_Bank` for `Subject`/`Unit / Topic`; join misses land
  in the "غير مصنّف" bucket of their subject (never dropped).
  Rows whose detail is the expired-session marker
  (`{expiredSessionId}`, zero-score rows) are **excluded** from mastery.
- **Rationale**: `Detailed Review JSON` is the only per-question record in the
  system today (verified); mistake-review questions (`MISTAKE_*` ids) are
  themselves bank rows, so they join normally.
- **Alternatives considered**: re-grading from stored raw answers (rejected:
  duplicate logic, drift from graded truth); new normalized per-question
  submission table (rejected: schema change, not needed at pilot scale).

### D6 — Targeted practice via the existing exam factory

- **Decision**: New factory variant `createUnitPracticeExam` (admin-gated)
  slices `Question_Bank` by grade + subject + normalized unit key and writes a
  new `Exams` row: `Exam Type = 'Unit Practice'`,
  `Target Period = 'U:<unitKey>'`, via the existing `upsertExamRow_`; refusal
  requires at least one question in the slice, with a clear Arabic message and
  code `EMPTY_UNIT_POOL`.
- **Rationale**: Reuses session/retake invariants (students take exams through
  the standard session flow, `MAX_ATTEMPTS` respected); mirrors the weekly/
  monthly factories' refusal pattern.
- **Alternatives considered**: ad-hoc client-side quiz without an exam row
  (rejected: breaks session, retake accounting and history).

### D7 — Study Plan: measure-driven ordering, no plan-sheet writes

- **Decision**: Mastery recommendations order plan proposals at render time
  (weak first) on top of the existing `getTodayMission` + Study Plan screens;
  no writes to `Study_Plan` from this feature in v1.
- **Rationale**: `Study_Plan` rows are currently only seeded by the starter
  plan (`getStarterStudyPlan_`) and progressed via
  `markStudyPlanProgress_`; letting mastery *drive* content later keeps the
  feature non-destructive.
- **Alternatives considered**: server-side plan reordering (rejected:
  duplicates ownership of plan content in v1; revisit when plan generation is
  a real flow).

### D8 — Identity & authorization for the report

- **Decision**: New RPCs validate tokens through the existing token store
  (`storeAccessToken_`/`getAccessTokenClaims_`): student token
  (`role:'student'` from `verifyGatewayPin`) may only read its bound
  `studentKey` (`ali`|`mostafa`; `studentKeyForIdentity_` mapping unchanged);
  parent token (`role:'parent'` from `verifyAdminPin`) reads both students.
  Mirrors existing `ADMIN_REQUIRED_RESULT` guard pattern.
- **Rationale**: Satisfies spec FR-003 and constitution Principle II without
  inventing new auth; pilot has exactly two students.
- **Alternatives considered**: roster-based expansion (rejected: no roster
  sheet exists; out of pilot scope).

### D9 — Constitution token-name drift (`ADMIN_TOK_*` vs `ACCESS_TOK_*`)

- **Decision**: Keep implementation aligned with the current code reality
  (typed `ACCESS_TOK_*` claims); record a **PATCH amendment proposal** for the
  constitution's Principle II wording (intent unchanged: short-lived,
  server-verified grant per privileged call). Deliberately NOT edited inside
  plan execution.
- **Rationale**: Honest governance — constitution drift is documented, not
  silently"fixed" while coding.
- **Alternatives considered**: renaming tokens back to `ADMIN_TOK_`
  (rejected: cosmetic churn), editing constitution mid-plan (rejected: violates
  governance procedure — amendments go through the governance section).

### D10 — Test-suite refresh obligation (Principle III)

- **Decision**: `tests/server.test.js` asserts the legacy contract
  (`ADMIN_TOK_` prefix checks, PIN `1990`, 2-arg `getExamData`) and fails
  against current `Code.gs` (verified). Refreshing it to the current contract
  is a scheduled task **before** the mastery RPC extension, and the E2E
  mock_bridge's legacy `ADMIN_TOK_` expectations must be updated in the same
  effort.
- **Rationale**: Constitution Principle III requires a green regression floor;
  landing new features on a red suite is forbidden by the gate.
- **Alternatives considered**: skipping test refresh (rejected: gate
  violation), pinning tests to old contract only (rejected: tests must encode
  reality).

## Open Unknowns

None remaining — all Technical Context items resolved from the codebase
itself; no external research needed (shut scope: Google-provided platform,
no new dependencies).
