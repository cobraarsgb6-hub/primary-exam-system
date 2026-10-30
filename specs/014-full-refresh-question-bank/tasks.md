# Implementation Tasks: 014-full-refresh-question-bank
## Phase P13: التجدد الكامل لبنك الأسئلة وإعادة التوليد الديناميكي

- [x] **Task 1: Build Dynamic Question Synthesizer Engine in Code.gs**
  - Implement algorithmic question generators for Math (Prime factors, FDP, Long division, BODMAS, Place value, Divisibility, Rounding) and Science (Circuits, Forces).
  - Ensure correct answer and 3 realistic distractors are computed dynamically with detailed pedagogical explanations.
  - Stratify questions across L1 (Foundational), L2 (Core), and L3 (Challenging).

- [x] **Task 2: Integrate Full Refresh Protocol into getExamData & Session Management**
  - Update `getExamData(examCode, studentName, studentToken, isPractice, refreshSalt)`.
  - In practice mode (`isPractice=true` or `PRAC_` prefix): bypass static attempt locks and generate fresh questions each call.
  - Shuffle and sample balanced questions across L1, L2, L3.

- [x] **Task 3: Client Quiz Runtime Refresh Integration**
  - Add interactive `🔄 تدريب بأسئلة متغيرة (Refresh Questions)` button in `QuizApp.js.html` quiz header.
  - Wire button to re-fetch/re-generate questions with a fresh salt and reset the timer.
  - Expose `window.refreshQuizQuestions()` for tests and user interaction.

- [x] **Task 4: Build Automated Verification Suite**
  - Create `tests/dynamicRefreshBank.test.js` validating:
    - Numerical variability across consecutive generation calls.
    - Mathematical correctness of generated answers and explanations.
    - Distribution across L1, L2, L3 tiers.
    - Client refresh action and DOM updates.
  - Register test in `package.json`.

- [x] **Task 5: Bundle & Run Full Quality Gates**
  - Run `python bundle.py` to compile `Index.bundle.html` and synchronize `Index.html` and android assets.
  - Run `npm test`.
  - Run `python tests/test_multisubject_navigation.py`.
  - Run `python tests/test_adversarial_concurrency.py`.
