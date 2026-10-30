# Tasks: Phase 7 (`008-question-types-mistakes`)

- [x] **Task 1: Server-Side Multi-Type Grading & Pipe-Delimited Matching**
  - Update `normalizeAnswer_` / `calculateScore_` / `gradeItem_` in `Code.gs` to support `FILL_IN` and pipe delimiter `|` for candidate valid answers.
  - Ensure Arabic normalization (hamza, tashkeel, digits, tatweel) applies seamlessly to free-text answers.

- [x] **Task 2: Isolated Mistakes Notebook Engine & Endpoints**
  - Implement `getStudentMistakes(studentKey, studentToken)` with strict student isolation and deduplication.
  - Enhance `createMistakesReviewExam` to pull from isolated mistakes with fallback handling.

- [x] **Task 3: Negative Keywords Visual Styling & UI Multi-Type Rendering**
  - Add negative keyword regex styling (`NOT`, `EXCEPT`, `مضاد`, `ما عدا`) in question cards.
  - Support `FILL_IN` input rendering in exam runner alongside MCQ and True/False.

- [x] **Task 4: Unit Test Suite (`tests/questionTypesMistakes.test.js`)**
  - Write comprehensive tests for `FILL_IN` scoring, Arabic normalization, multi-answers, and student mistakes isolation.
  - Wire into `package.json` test runner.

- [x] **Task 5: Verification, E2E Mocking & Bundle Synchronization**
  - Add `getStudentMistakes` to `tests/e2e/mock_bridge.js`.
  - Re-bundle via `python bundle.py`.
  - Run `npm test` and `run_all_e2e.py`.

- [x] **Task 6: Update Truth Ledger & Git Commit**
  - Update `CURRENT_STATUS_AR.md`, `.wolf/STATUS.md`, and `cerebrum.md`.
  - Commit P7 changes.
