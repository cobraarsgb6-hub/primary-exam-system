# Architectural Implementation Plan: P6 Cumulative Multi-Subject Exam Schedule

## 1. Architectural Strategy

### A. Database Layer (`Code.gs`)
1. **Add `Exam_Schedule` Table:**
   - In `setupDatabase_`, ensure `Exam_Schedule` sheet is created with 14 canonical headers.
   - Seed sample 30-day schedule entries for Ali and Mostafa.
2. **Expand `Study_Plan`:**
   - Expand `getStarterStudyPlan_` to include complete 4-week roadmaps for Mathematics, Science, English, Arabic, and ICT for both Ali and Mostafa.

### B. Exam Generation Engine (`Code.gs`)
1. **Implement `loadCumulativeBankQuestionsByPeriod_`:**
   - Accepts `(grade, subject, targetPeriod, targetDifficulty, excludeQuestionIds)`.
   - Resolves weeks included:
     - `W1`: `['W1']`
     - `W2`: `['W1', 'W2']`
     - `W3`: `['W1', 'W2', 'W3']`
     - `W4`: `['W1', 'W2', 'W3', 'W4']`
     - `M1`: `['W1', 'W2', 'W3', 'W4']`
   - Groups available bank questions by `Lesson` (or `Unit`).
   - Guarantees at least 1 question per covered lesson (Coverage First).
   - Enforces target difficulty ratios based on exam type.
   - Sorts final question list: `Easy` → `Medium` → `Challenge`.
   - Returns `{ questions, warnings, coveredLessons }`.
2. **Implement Same-Day Non-Duplication:**
   - `buildPairedDailyExam_(milestoneExamCode)` creates a distinct 3–5 question quiz ensuring `excludeQuestionIds` filters out all IDs used in the milestone exam.
3. **Implement Adaptive Rules:**
   - `getAdaptiveQuestionRecommendations_(studentName, subject)` inspects recent submissions:
     - Under 70% in a skill: adds 2 reinforcement questions.
     - 85%+ in a skill: adds 1 challenge question.

### C. Frontend & Mock Bridge
1. **Expose Schedule to Parent & Student UI:**
   - In `Portal.js.html` & `mock_bridge.js`, support querying `getExamSchedule(studentKey)` to display the scheduled daily mission and milestone roadmap.
2. **Re-bundle:**
   - Compile via `python bundle.py`.

### D. Testing
1. **Unit Test Suite (`tests/scheduleCumulative.test.js`):**
   - Test `Exam_Schedule` creation and schema.
   - Test 5-subject `Study_Plan` coverage.
   - Test cumulative question expansion (W1, W2, W3, W4, M1) with zero same-day question overlap.
   - Test adaptive difficulty ordering and alerts on missing lessons.
2. **Run full verification (`npm test` + `run_all_e2e.py`).**
