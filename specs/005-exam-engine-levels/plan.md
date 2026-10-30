# Plan: 005-exam-engine-levels

## Architectural Plan

### 1. Server Architecture (`Code.gs`)
- **Difficulty Mapping**:
  Create `matchDifficultyLevel_(rowDiff, targetDiff)` supporting canonical synonyms:
  - Level 1 / Foundational / Easy
  - Level 2 / Standard / Medium / Core
  - Level 3 / Challenging / Hard / Advanced
- **Strict Difficulty Filter**:
  In `loadBankQuestionsByPeriod_`, when `targetDifficulty` is not 'ALL', filter out questions that do not match the target level.
- **Exam Info & Schema Update**:
  In `getExamInfo(examCode)` and `setupDatabase_`, include and read the `Difficulty` column (index 11).
- **Exam Builder Propagation**:
  In `buildExamQuestions_(examCode)`, pass `exam.difficulty` to `loadBankQuestionsByPeriod_`.
- **Factory Expansion**:
  In `createWeeklyExam_` and `createMonthlyExam_`, accept and validate custom `count` (5-30) and `duration` (10-60), format subject code prefix for all 5 subjects (`MATH`, `SCI`, `ENG`, `ARB`, `ICT`, `ALL`), and generate unique exam codes.

### 2. Frontend Architecture (`Index.html`)
- **Parent Ops Controls**:
  Add question count and duration number inputs to both Weekly and Monthly exam generator cards.
- **Student Catalog Badges**:
  Update card rendering in `renderExamCards()` to read `ex.difficulty` (or inspect code tag) and display styled badges.
- **Difficulty Pill Filtering**:
  Enable `setAdaptiveDifficulty(level)` to filter student exam cards or display a filter reset option.
- **Bundle Regeneration**:
  Rebuild `Index.bundle.html` via `python bundle.py`.

### 3. Verification & Testing
- Create dedicated unit test suite in `tests/difficultyLevels.test.js`.
- Run full regression test suite (`npm test`).
