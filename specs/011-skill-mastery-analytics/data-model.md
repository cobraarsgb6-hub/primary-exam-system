# Data Model: Skill Mastery Analytics

**Feature**: `001-skill-mastery-analytics` | **Derived from**: real sheet
headers in `Code.gs` + sample CSV data. Storage-agnostic naming; **no new
sheets, no migrations**.

## Existing entities consumed (no changes)

### Question (sheet `Question_Bank`, 13 cols)

| Field | Type | Notes |
|---|---|---|
| Question ID | string | join key from review JSON; mistake rows use `MISTAKE_<student>_<hash>` |
| Grade Level | string | e.g. `Year 5 (G5)` |
| Subject | string | e.g. `English Grammar` |
| Unit / Topic | string | the **skill**; may be empty → «غير مصنّف» bucket |
| Question Text, Type, Options, Correct Answer, Points, Explanation, Exam Code, Week, Difficulty | as existing | unchanged |

Validation for mastery use: `Points` integer ≥ 0; rows with empty/blank
`Unit / Topic` MUST land in «غير مصنّف» instead of being dropped.

### Submission attempt (sheet `Submissions`, 11 cols)

| Field | Type | Notes |
|---|---|---|
| Timestamp, Student Name, School Grade, Exam Code | as existing | identity via `Student Name` (+ `studentKeyForIdentity_` mapping) |
| Score, Total, Percentage, Rating, Duration, Summary | as existing | exam-level facts |
| Detailed Review JSON | JSON array | per-question: `{questionId, questionText, studentAnswer, correctAnswer, isCorrect, pointsAwarded, maxPoints, explanation}` |

Rules:
- Only rows whose review items parse with `isCorrect ∈ {true,false}` count as
  graded attempts. Expired-session rows (detail `{expiredSessionId}`, zero
  score) are **excluded**.
- Pending retake **requests** (sheet `Retake_Requests`) never contribute; only
  graded submissions do.
- Attempts are samples: the same `questionId` across different exams/submission
  counts once per attempt.

### Existing support entities

- **Student**: identity = `studentKey` (`ali`, `mostafa` via
  `studentKeyForIdentity_`); display name = canonical full name. No roster
  sheet exists (pilot).
- **Exam (sheet `Exams`, 11 cols)**: gains ONE new exam type value —
  `Exam Type = 'Unit Practice'` (new row shape, same sheet via
  `upsertExamRow_`).
- **Study_Plan**: unchanged (read for ordering only in v1).

## New computed entity (not stored)

### MasteryRecord — dimension: studentKey × Subject × unitKey

- **unitKey**: `normalizeAnswer_(Unit / Topic)`; **unitLabel**: first-seen raw
  string for Arabic RTL display (subject display = first-seen raw subject).
- **Metrics** (all derived from review JSON × bank join):
  - `attemptedPoints` = Σ maxPoints
  - `earnedPoints` = Σ pointsAwarded
  - `pct` = earned ÷ attempted × 100, full precision internally, displayed
    rounded to whole numbers
  - `submissionCount` = graded submissions touching the unit
  - `questionRows` = per-question review items counted (repeats across
    attempts included)
  - `badge`: متقن ≥ 80; قابل للتحسن 60–79; يحتاج مراجعة < 60
- **Trend**: last attempt's unit pct vs mean of earlier attempts for the same
  unit: rising ≥ +5, falling ≤ −5, else flat (percentage-points).
- **State transitions**: none — pure recompute from attempts (constitution:
  never hand-edited). Deleting/correcting a submission row changes the next
  render by design.
- **Bucket «غير مصنّف»**: per student × subject, aggregates review items whose
  `questionId` is missing from the bank OR whose bank row has no unit/topic;
  reported with its own badge and never ranked in "weakest top-3" (data-gap
  signal only — but forced-visible per FR-010).

### UnitPracticeExam (new `Exams` row via factory)

- Fields: `Exam Code` (`UPR_*` pattern), title (Arabic, unit-specific),
  grade, subject, `عدد الأسئلة` = pool size, duration = standard, status
  ACTIVE, `Exam Type = 'Unit Practice'`, `Target Period = 'U:<unitKey>'`.
- Slice rule: bank rows where subject + grade match AND
  `normalizeAnswer_(Unit / Topic) == unitKey` (empty question pool → refuse).
- Lifecycle: standard exam/session/attempt flow (incl. `MAX_ATTEMPTS`).

### StudyRecommendation (computed ordering, v1 render-time)

- Per student: `يحتاج مراجعة` units first (ascending pct), then
  `قابل للتحسن`, then never-started units (original plan order), then
  `متقن` (or proposal to move to next unattempted unit when all mastered).
- Feeds: parent weakest top-3 (`weakest[]`), student plan view ordering, and
  the targeted-practice action (FR-009). Not persisted.

## Aggregation algorithm contract (prose, for tests)

1. Read `Submissions` (one batched read) → for each row: parse
   `Detailed Review JSON`; skip expired/zero-score marker rows; collect
   `(studentKey, examCode, item[])` graded attempts.
2. Read `Question_Bank` (one batched read) → map
   `Question ID → (subject, unit raw, unitKey, points)` (points authoritative
   from bank when `maxPoints` missing in item).
3. For each attempt item → attach subject/unit by `questionId`; misses →
   «غير مصنّف» bucket of the attempt's … (bank-only subjects; items without
   bank row and without recoverable subject go to a per-student
   general bucket).
4. Accumulate per MasteryRecord; compute pct, badge, trend
   (attempt-level unit pct per exam per unit for the trend series).
5. Rank weakest 3 (pct ascending, require `submissionCount ≥ 1`, exclude
   «غير مصنّف»).
