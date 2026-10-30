# Phase 7 Specification: Question Types & Isolated Mistakes Notebook (`008-question-types-mistakes`)

## 1. Context & Business Value
Standard MCQ-only assessments suffer from high guessing rates (~25%) and fail to evaluate synthetic recall, spelling, grammatical composition, and sequence logic. Additionally, learning from past failures requires students to review and re-test solely on questions they previously answered incorrectly, strictly isolated by student identity (Ali Year 5 vs Mostafa Grade 6).

## 2. User Stories
- **US-P7.1 (Free-Text Fill-in Question Evaluation):** As a student (Ali or Mostafa), I want to answer short-answer / fill-in-the-blank (`FILL_IN`) questions in both English and Arabic, so that my active recall and spelling are tested without hints.
- **US-P7.2 (Arabic & English String Normalization on Backend):** As a system, I must normalize text responses on the server (handling Arabic hamzas, tashkeel, tatweel, letter substitutions, case insensitivity, punctuation, and extra whitespace) so that correct student answers are graded fairly and accurately without false negatives.
- **US-P7.3 (Interactive Question Types & Negative Visual Badges):** As a student, I want questions to support `TRUE_FALSE` and visual callout badges for negative/caution words (`NOT`, `EXCEPT`, `LEAST`, `مضاد`, `ليس`, `ما عدا`) so that I don't overlook tricky instructions.
- **US-P7.4 (Curriculum Question Type Mix Invariant):** As a parent/educator, I want milestone and weekly exams to cap MCQ at a maximum of 65%, incorporating at least 3 distinct question types (MCQ, Fill-in, True/False) to stimulate diverse cognitive processes.
- **US-P7.5 (Strictly Isolated Mistakes Notebook):** As a student, I want to access my personal Mistakes Notebook ("دفتر أخطائي") generated strictly from official previous exam submissions where I earned 0 points, isolated completely so Ali never sees Mostafa's mistakes and Mostafa never sees Ali's mistakes.
- **US-P7.6 (Targeted Mistakes Review Exam):** As a parent or student, I want to generate a personalized "من أخطائي" review exam that compiles questions from the student's notebook with fresh shuffled distractors or fill-in prompts to ensure mastery before major milestones.

## 3. Functional Requirements
1. **`FILL_IN` Server Scoring:**
   - Extend `calculateScore_` / `gradeItem_` to handle question type `FILL_IN` (and `TEXT`).
   - Multiple valid answers supported via pipe delimiter (e.g. `alef|alif|ألف`).
   - Normalization applies `normalizeAnswer_` (which folds alefs, removes harakat/tatweel, converts digits, trims whitespace, lowercases).
2. **`TRUE_FALSE` Question Type:**
   - Two radio options: `True` / `False` (or `صح` / `خطأ`).
   - Normalized comparison against canonical truth.
3. **Visual Badge Injection for Negative Keywords:**
   - Detect negative keywords (`NOT`, `EXCEPT`, `NEVER`, `LEAST`, `مضاد`, `ليس`, `ما عدا`, `غير`) in question text and wrap or highlight them with `<span class="badge-negative">` or visual emphasis.
4. **Isolated Mistakes Notebook Engine:**
   - RPC `getStudentMistakes(studentKey, studentToken)`: queries `Submissions` table, parses detailed review JSON, filters items where `isCorrect === false` for the authenticated student only, and deduplicates by `questionId` or text.
   - RPC `createMistakesReviewExam`: constructs a custom exam from past mistakes for the student.
5. **Security & Data Isolation:**
   - Student tokens must match the requested student mistakes ledger.
   - Rejection of cross-student requests.

## 4. Acceptance Criteria
- [ ] Backend grading correctly assesses `FILL_IN` questions in Arabic and English, allowing valid punctuation/harakat variations.
- [ ] Ali's mistakes notebook returns only Ali's previous submission mistakes; Mostafa's returns only Mostafa's.
- [ ] Milestone exam generation maintains <= 65% MCQ ratio when mixed question types are present in the bank.
- [ ] Negative keywords in question stems are highlighted with distinct visual styling.
- [ ] Full automated unit tests pass in `npm test` and integration verified via E2E.
