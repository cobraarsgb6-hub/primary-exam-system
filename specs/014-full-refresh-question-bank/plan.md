# Implementation Plan: 014-full-refresh-question-bank
## Phase P13: التجدد الكامل لبنك الأسئلة وإعادة التوليد الديناميكي

### Architecture & Work Breakdown

```
Code.gs Backend
 ├── Dynamic Math & Science Synthesizer Engine (generateDynamicMathQuestions_)
 │    ├── Prime Factors with Index Notation
 │    ├── FDP Conversions
 │    ├── Long Division (Bus Stop)
 │    ├── BODMAS & Negative Numbers
 │    ├── Place Value to 10M & Rounding
 │    ├── Divisibility Tester
 │    └── Circuits & Forces
 ├── getExamData(code, studentName, studentToken, isPractice, refreshSalt)
 │    └── If isPractice or PRAC_ prefix: bypass stale cache, generate dynamic numbers & shuffle
 └── buildExamQuestions_ integration

Client Quiz Runtime (QuizApp.js.html & Index.template.html)
 ├── Quiz Header Refresh Button ("🔄 تدريب بأسئلة متغيرة")
 ├── practiceExamWithRefresh(code) triggering dynamic re-sampling
 └── Auto-refresh on page reload when activeScreen === 'screen-quiz' and in practice mode

Verification Suites
 ├── tests/dynamicRefreshBank.test.js (Tests dynamic numbers variation & L1/L2/L3 tiers)
 ├── tests/server.test.js (Tests practice mode bypassing static cache)
 └── Playwright E2E & Concurrency Suites
```

### Steps:
1. **Extend `Code.gs` with Dynamic Synthesizers:**
   - Create `generateDynamicQuestion_(templateKey, level)` that generates parameterized math and science questions with dynamically computed solutions.
   - Update `buildExamQuestions_` and `getExamData` to accept `isPractice` and `refreshSalt`, applying dynamic question synthesis.
2. **Update `QuizApp.js.html` & `Index.template.html`:**
   - Add "🔄 تدريب بأسئلة جديدة (Refresh Bank)" in quiz header and completion screens.
   - Support `practiceRandomBankQuestions()` with fresh salt.
3. **Build Automated Unit Test `tests/dynamicRefreshBank.test.js`:**
   - Test 1: Consecutive calls return distinct numerical values.
   - Test 2: Correct answer and options adapt dynamically to new parameters.
   - Test 3: L1, L2, L3 tier stratification.
   - Test 4: UI Refresh button resets question state with new items.
4. **Compile and Verify:**
   - Run `python bundle.py` to compile `Index.bundle.html` and sync `Index.html`.
   - Run `npm test`.
   - Run `python tests/test_multisubject_navigation.py`.
   - Run `python tests/test_adversarial_concurrency.py`.
