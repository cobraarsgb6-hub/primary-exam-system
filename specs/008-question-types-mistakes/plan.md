# Implementation Plan: Phase 7 (`008-question-types-mistakes`)

## 1. Technical Architecture & Component Impact

### A. Server Scoring & Normalization (`Code.gs`)
1. **Multi-Answer Delimiter Support:**
   - In `gradeItem_` or `calculateScore_`:
     - If `correctAnswer` contains `|`, split on `|` and check if student's normalized answer matches *any* candidate normalized answer.
     - E.g. `22|twenty two|٢٢` matches `22` or `twenty two` or `٢٢`.
2. **Support `FILL_IN`, `TRUE_FALSE`, `MATCHING`, `ORDERING` in Question Type:**
   - `buildExamQuestions_` and `publicQuestions_` must preserve `type` so the frontend renders the correct input widget (text input for `FILL_IN`, 2 buttons for `TRUE_FALSE`, etc.).
   - If `type === 'FILL_IN'`, `options` can be empty array `[]`.

### B. Isolated Mistakes Notebook Engine (`Code.gs`)
1. **Endpoint `getStudentMistakes(studentKey, studentToken)`:**
   - Validate token via `isStudentTokenValid_(studentToken, studentKey)`.
   - Query `Submissions` table for rows matching target student.
   - Parse `Review Details` / `detailedReview` JSON.
   - Extract unique questions where `isCorrect === false`.
   - Return `{ success: true, student: targetStudent, mistakesCount: items.length, mistakes: items }`.

2. **Refine `createMistakesReviewExam(payload)`:**
   - Ensure it isolates by `studentName`.
   - Pull up to `questionCount` (default 10) mistaken questions, assigning `difficulty: 'Reinforcement'`, `type: 'Review'`.
   - Save into `Exams` sheet and return `{ success: true, examCode: examCode, questionsCount: questions.length }`.

### C. Negative Keywords Styling (`Portal.js.html` / `Index.template.html`)
1. **Negative Keyword Styler:**
   - In `renderQuestionCard`: regex match words `\b(NOT|EXCEPT|NEVER|LEAST)\b` and Arabic `(مضاد|ليس|ما عدا|غير)` and wrap in `<span class="badge-negative">`.
   - Add `.badge-negative` CSS styling with amber/red outline or background for attention.

### D. Testing & Verification
1. **Unit Test Suite (`tests/questionTypesMistakes.test.js`):**
   - Test `FILL_IN` grading with English and Arabic normalization.
   - Test pipe delimiter multi-answer matching (`a|b|c`).
   - Test cross-student isolation in `getStudentMistakes` (Ali cannot see Mostafa's mistakes).
   - Test `createMistakesReviewExam` builds exams strictly from student's own failed questions.
2. **E2E & Bundle:**
   - Update `mock_bridge.js` with `getStudentMistakes`.
   - Run `bundle.py`.
   - Run `npm test` and `run_all_e2e.py`.
