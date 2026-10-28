# Testing Infrastructure & Verification Survey Report

**Author**: Explorer Survey Testing Agent (`explorer_survey_testing`)  
**Target Audience**: Parent Orchestrator (`b60602f6-9563-4ac1-9709-5890290e1ced`), Auditor, and Implementer agents  
**Working Directory**: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_testing`  
**Date**: 2026-10-25  

---

## 1. Observation

### 1.1 Existing Test Suites and Test Runners
1. **`package.json` Configuration**:
   - Path: `C:\Users\co0ob\Projects\primary-exam-system\package.json`
   - Content:
     ```json
     {
       "name": "primary-exam-system",
       "version": "1.1.0",
       "private": true,
       "description": "Google Apps Script assessment portal for primary grades",
       "scripts": {
         "test": "node --test tests/server.test.js"
       }
     }
     ```
   - Running `node --test tests/server.test.js tests/cumulative.test.js` under Node.js v22.23.2 passed all 13 tests with zero failures in 795.49ms.

2. **Server-Side VM Test Suites (`tests/server.test.js` & `tests/cumulative.test.js`)**:
   - `tests/server.test.js` (359 lines): Uses Node.js `node:test`, `node:assert/strict`, and `node:vm` to mock Google Apps Script core runtime services (`SpreadsheetApp`, `PropertiesService`, `CacheService`, `LockService`, `Utilities`, `Session`, `Logger`, `FormApp`).
   - Covered server capabilities:
     - `getExamData`: bank sampling and secret answer withholding (line 167).
     - `submitExamAnswers`: proportional scoring (1/3 for 1 correct out of 3, line 176).
     - Empty answer and spoofed ID prevention (line 194).
     - Duplicate submission idempotency (line 210).
     - Maximum attempt enforcement (`MAX_ATTEMPTS`) and retake request approval lifecycle (lines 229–260).
     - Server-side session expiration enforcement (`TIME_EXPIRED`, line 262).
     - Student identity session mismatch prevention (`STUDENT_MISMATCH`, line 279).
     - Non-destructive `setupDatabase` execution preserving existing submissions (line 293).
     - Fresh database initialization and table auto-creation (line 307).
     - Dynamic question bank sampling based on question count metadata (line 338).
     - Admin dashboard data loading (line 352).
   - `tests/cumulative.test.js` (42 lines): Checks existence and signature of cumulative generator functions (`loadBankQuestionsByPeriod_`, `buildExamQuestions_`, `updateStudyPlanOnSubmission_`).

3. **Existing Root-Level Python Tests**:
   - `test_e2e_quiz.py` (79 lines): Uses `playwright.sync_api` to test 10 interactive portal steps (Ali Gateway -> Today Mission -> Start Modal -> Quiz Screen -> Gateway -> Mostafa Gateway -> Mostafa Today Mission -> Parent Portal -> Analytics View -> Student Switching). Ran headless Chromium with 100% success.
   - `test_render_all.py` (61 lines): Playwright script checking card counts, refresher text, and Parent Portal Study Plan filtering by week (`W1`).
   - `test_transitions.py` (30 lines): Playwright script verifying fast UI transitions across screens.
   - `test_ui_buttons.py` (45 lines): Playwright script verifying screen button responsiveness and monitoring browser console errors.
   - `test_passages.py` (21 lines): Standalone passage definition and string check script.
   - `test_click_course.py`, `test_api.py`, `test_api_jwt.py`: Coligo LMS sync and authenticated crawler scripts.

4. **Environment Runtimes and Tools**:
   - Node.js: `v22.23.2` with built-in test runner (`node --test`), `node:vm`, and `node:assert`.
   - npm: `12.2.0` (no local `node_modules` directory installed; `npm list` is empty).
   - Python: `3.14.7` with installed packages: `playwright` (1.60.0), `lxml` (6.1.1), `pandas` (3.0.3), `requests` (2.34.2), `openpyxl` (3.1.5). Note: `pytest` is not installed in the Python environment.

---

### 1.2 AST Syntax, DOM Structure & Unicode Compliance
1. **AST Syntax Validation**:
   - `Code.gs` (4,173 lines, 292,310 bytes): Evaluated via `new vm.Script(code, { filename: 'Code.gs' })`. Result: Valid ECMAScript syntax; 0 syntax errors.
   - `Index.html` Embedded JavaScript: 1 `<script>` block spanning lines 1548 to 4385 (2,837 lines, 168,075 characters). Evaluated via `new vm.Script(...)`. Result: Valid ECMAScript syntax; 0 syntax errors.

2. **DOM Tree Nesting & Well-Formedness in `Index.html`**:
   - Parsed with `lxml.html` and strict `html.parser.HTMLParser` checking all non-void element closing tags.
   - Result:
     - Root element: `<html>` enclosed by `<!DOCTYPE html>`.
     - Trailing content after `</html>`: None (100% clean).
     - Leading content before `<html>`: None except doctype.
     - Stack unmatched unclosed tags: `0`.
     - Tag mismatch / orphaned tag errors: `0`.

3. **Unicode NFKC Normalization Forensic Audit**:
   - `Code.gs`: `code == unicodedata.normalize('NFKC', code)` evaluated to `False`.
     - Discrepancy identified on exactly 8 lines: Lines 160, 175, 176, 1507, 1508, 1528, 3857, 4118.
     - Root Cause: Combining mark ordering in Arabic diacritics. In raw text, Shaddah (`U+0651`) precedes Fatha (`U+064E`) or Kasra (`U+0650`), whereas Unicode Canonical Composition (NFKC/NFC) standardizes the canonical combining class order.
   - `Index.html`: Evaluated to `False` on 2 lines: Lines 2053 and 2271 (Arabic diacritic ordering in lesson summaries and tips).
   - `Question_Bank.csv`: Evaluated to `False` (contains non-NFKC ordered Arabic diacritics).
   - `Exams.csv`: Evaluated to `True` (100% NFKC normalized).
   - Answer Normalization in `Code.gs` (`normalizeAnswer_`, lines 376–383):
     ```javascript
     function normalizeAnswer_(value) {
       return String(value || '')
         .replace(/\u0640/g, '')
         .replace(/[\u064B-\u0652]/g, '')
         .replace(/\s+/g, ' ')
         .trim()
         .toLowerCase();
     }
     ```
     `normalizeAnswer_` strips tatweel and harakat, but does NOT perform `.normalize('NFKC')` or fold Arabic letter variants (`أ/إ/آ -> ا`, `ة -> ه`, `ى -> ي`).

4. **Security & Secrets**:
   - Scanned for hardcoded JWTs (`ey...`), bearer tokens, and secrets across `Code.gs`.
   - Result: Zero hardcoded JWT tokens in `Code.gs`. Coligo token storage is dynamically handled via `PropertiesService.getScriptProperties().getProperty('COLIGO_JWT_TOKEN')` (lines 3568–3574).

---

### 1.3 Audit of the 28 Exams and Study Plan Items
1. **The 28 Exams Inventory**:
   Auditing across `Exams.csv`, `Question_Bank.csv`, `Code.gs`, and `Index.html` revealed the precise origin of the 28 exams:
   - **25 Curriculum Exams** (scheduled in `Exams.csv` and `Study_Plan`):
     - **Ali Ahmed (Year 5 English Grammar)**: 14 exams:
       - 6 Daily: `DAILY_Y5_ENG_W1D1` to `DAILY_Y5_ENG_W1D6`
       - 1 Weekly Milestone: `EX_Y5_ENG_W1`
       - 3 Daily: `DAILY_Y5_ENG_W2D8` to `DAILY_Y5_ENG_W2D10`
       - 3 Cumulative: `EX_Y5_ENG_W2_CUMULATIVE`, `EX_Y5_ENG_W3_CUMULATIVE`, `EX_Y5_ENG_W4_CUMULATIVE`
       - 1 Monthly Capstone: `EX_Y5_ENG_M1_CAPSTONE`
     - **Mostafa Ahmed (Grade 6 Arabic Language)**: 11 exams:
       - 3 Daily: `DAILY_Y6_ARB_W1D4` to `DAILY_Y6_ARB_W1D6`
       - 1 Weekly Milestone: `EX_Y6_ARB_W1`
       - 3 Daily: `DAILY_Y6_ARB_W2D8` to `DAILY_Y6_ARB_W2D10`
       - 3 Cumulative: `EX_Y6_ARB_W2_CUMULATIVE`, `EX_Y6_ARB_W3_CUMULATIVE`, `EX_Y6_ARB_W4_CUMULATIVE`
       - 1 Monthly Capstone: `EX_Y6_ARB_M1_CAPSTONE`
   - **3 Foundational / Heritage Diagnostic Exams** (defined in `Code.gs` in-memory catalog at lines 1604–1609):
     1. `EX_Y5_ENG_ADV01` (Ali Year 5 Adverbials Foundational Exam, 10 questions)
     2. `EX_Y6_ARB_PRIO01` (Mostafa Grade 6 Arabic Foundational Diagnostic, 10 questions)
     3. `EX_Y6_ENG_FANTASY01` (Mostafa Grade 6 English Fantasy Reading Exam, 10 questions)
   - **Total Unique Exams**: 25 + 3 = **28 exams**.

2. **Question Generation & Lifecycle Verification**:
   - An automated test harness (`test_all_28_exams.js`) was constructed to test `getExamData` -> answer mapping -> `submitExamAnswers` across all 28 exams in the GAS VM environment.
   - Result:
     - 28 out of 28 exams loaded questions successfully without errors.
     - 28 out of 28 exams completed submission and scored 100% (earned = total points).
     - Submissions sheet grew from 1 header to 29 rows (1 header + 28 recorded submissions).
     - Question counts verified: Daily exams = 5 questions; Milestone W1 = 10; Cumulative W2 = 12; Cumulative W3 = 15; Milestone W4 = 18; Capstone M1 = 20; Foundational = 10.

3. **Study Plan Verification**:
   - `Study_Plan` in `Code.gs` (`getStarterStudyPlan_`, lines 3431–3459) and `Index.html` (`studyPlan` fallback, line 3448) consists of 25 structured plan items spanning Days 1–30 across W1, W2, W3, W4, and M1.
   - `updateStudyPlanOnSubmission_` (lines 4049–4074): Queries `Study_Plan` sheet for student and exam code match, updating `Status` to `Completed`.

---

### 1.4 Client Latency & Standalone Mocking Behavior
1. **Screen Transition Latency**:
   - Benchmarked using Playwright headless Chromium (`benchmark_transitions.py`):
     - Warmed Gateway -> Ali Portal: **4.26ms** (average over 5 runs).
     - Warmed Gateway -> Mostafa Portal: **3.42ms** (average over 5 runs).
     - Warmed Gateway -> Parent Portal: **38.03ms** (average).
   - Requirement of `<50ms` direct DOM screen transition is satisfied.

2. **Critical Standalone Execution Observation**:
   - In `Index.html` (lines 3110–3132), every backend RPC checks `typeof google !== 'undefined' && google.script && google.script.run`.
   - When opened directly in a browser without GAS iframe wrapper, `google.script.run` is `undefined`.
   - Result: Frontend falls back to a hardcoded single dummy question (`sessionKey: 'DEMO_SESSION'`, question: `'Sample Assessment Question'`, line 3128) instead of real questions.
   - Consequence for E2E testing: To test true end-to-end functionality via Playwright or headless browser, an RPC mock/bridge (`window.google.script.run`) must be injected into the browser context via `page.add_init_script`.

---

## 2. Logic Chain

1. **Premise 1**: Requirement R1 demands AST syntax validity, DOM tree nesting integrity, and Google Apps Script sandbox compliance.
   - *Evidence*: `Index.html` passed strict HTML5 parser validation with 0 orphaned/unclosed tags. Node.js V8 parser compiled both `Code.gs` and embedded `<script>` with 0 errors.
   - *Deduction*: Architectural syntax is sound. However, 8 lines in `Code.gs` and 2 in `Index.html` exhibit non-NFKC combining mark ordering in Arabic text, which should be normalized to avoid diacritic comparison bugs.

2. **Premise 2**: Requirement R2 demands zero defect reliability across all 28 exams and study plan items.
   - *Evidence*: Investigation revealed exactly 28 exams (25 scheduled in CSV + 3 in-memory fallback catalog). All 28 exams were executed through `getExamData` and `submitExamAnswers` in `test_all_28_exams.js`, achieving 28/28 passes and 100% scoring accuracy.
   - *Deduction*: The backend question generator and scoring engine support the complete 28-exam catalog. However, `Exams.csv` currently omits the 3 foundational exams (`EX_Y5_ENG_ADV01`, `EX_Y6_ARB_PRIO01`, `EX_Y6_ENG_FANTASY01`), which rely exclusively on hardcoded fallback in `Code.gs`.

3. **Premise 3**: Automated E2E testing requires verifying the UI against realistic backend responses.
   - *Evidence*: `test_e2e_quiz.py` passed, but task log analysis revealed it ran against the offline `DEMO_SESSION` fallback because `google.script.run` was undefined.
   - *Deduction*: Existing Playwright tests only exercise DOM transitions and offline fallbacks. A production-grade 4-tier E2E testing suite must inject a full RPC bridge to test real questions, countdown timers, submissions, and error states.

4. **Premise 4**: The test runner ecosystem in this workspace has Node 22 (`node --test`) and Python 3.14 (`playwright`), but lacks `pytest` and npm packages.
   - *Evidence*: `python -m pip list` shows `playwright` 1.60.0 installed, but no `pytest`. Node.js has native `node --test` with 0 npm dependencies.
   - *Deduction*: The testing infrastructure should leverage Node.js built-in runner (`node --test`) for server VM tests and Python Playwright (or Node Playwright) for E2E browser tests without requiring external package installations.

---

## 3. Caveats

1. **Google Apps Script Cloud Quotas & Live Execution**:
   - Tests conducted locally in the Node.js `vm` harness simulate GAS services (`SpreadsheetApp`, `PropertiesService`, `LockService`). Live execution inside Google's Caja/V8 sandbox involves network latency and 6-minute execution quotas that cannot be measured offline.
2. **Coligo LMS Live API Dependencies**:
   - Coligo LMS syncing depends on valid JWT tokens and active external server connectivity (`prod-api.coligolms.com`). Offline tests mock or bypass this sync.
3. **Google Drive Video Streaming**:
   - Video streaming modals depend on real Google Drive permissions and MIME types, which are stubbed in offline testing.

---

## 4. Conclusion

1. **Current Test Readiness**:
   - Server-side unit testing is functional and fast (13 tests in ~800ms).
   - All 28 exams and 25 study plan items have been identified, verified, and mapped across the codebase.
   - DOM rendering is well under the 50ms performance threshold (~3.4ms–4.3ms).

2. **Identified Gaps to Resolve**:
   - **Diacritic Ordering**: Non-NFKC ordered Arabic diacritics in `Code.gs` (8 lines) and `Index.html` (2 lines) should be normalized.
   - **Exams Sheet Sync**: `Exams.csv` should include the 3 foundational exams so all 28 exams reside in the database rather than relying on code fallbacks.
   - **E2E RPC Mock Injection**: Playwright tests must inject `window.google.script.run` to validate real exam workflows rather than falling back to `DEMO_SESSION`.
   - **4-Tier E2E Test Suite**: Must be instantiated to cover Tier 1 (Feature Coverage), Tier 2 (Boundary & Corner Cases), Tier 3 (Cross-Feature Combinations), and Tier 4 (Real-World Application Scenarios).

---

## 5. Test Architecture & Requirements for the 4-Tier E2E Testing Track

### Track Overview
The 4-tier E2E test harness will run under Python (`playwright`) or Node.js (`node --test` + Playwright), connecting the DOM directly to a high-fidelity GAS RPC mock bridge.

```
┌─────────────────────────────────────────────────────────────┐
│                 4-Tier E2E Testing Track                    │
├─────────────────────────────────────────────────────────────┤
│ Tier 1: Core Feature Coverage (>= 5 tests per feature)      │
│   • Gateway & Portal Isolation (5 tests)                    │
│   • Daily Missions & Concept Refreshers (5 tests)           │
│   • 28-Exam Catalog & Quiz Engine (5 tests)                 │
│   • Assessment Submission & Scoring Engine (5 tests)        │
│   • Parent Analytics & Administration (5 tests)             │
├─────────────────────────────────────────────────────────────┤
│ Tier 2: Boundary & Corner Cases (>= 5 tests per domain)     │
│   • Timeouts & Session Expirations (5 tests)                │
│   • Attempt Limits & Concurrency (5 tests)                  │
│   • Input Sanitization & Arabic Diacritics (5 tests)        │
│   • Data & Schema Anomalies (5 tests)                       │
├─────────────────────────────────────────────────────────────┤
│ Tier 3: Cross-Feature Integration Combinations              │
│   • Full Student Cycle: Quiz -> Retake -> Approval -> Pass  │
│   • Dynamic Passage Adaptation across Consecutive Sessions  │
│   • Cumulative Exam Multi-Week Balanced Sampling            │
│   • Offline-to-Online Session Resumption & LocalStorage     │
├─────────────────────────────────────────────────────────────┤
│ Tier 4: Real-World Application Scenarios                    │
│   • Dual-Student Shared Device Morning Routine              │
│   • Weekend Comprehensive Parent Audit & Plan Review        │
└─────────────────────────────────────────────────────────────┘
```

### Detailed Tier Specifications

#### Tier 1: Core Feature Coverage (25 tests minimum)
1. **Gateway & Portal Isolation**:
   - `T1.1.1`: Click Ali Gateway -> Verify `#screen-student.active`, blue theme, Grade 5 badge.
   - `T1.1.2`: Click Mostafa Gateway -> Verify `#screen-student.active`, purple theme, Grade 6 badge.
   - `T1.1.3`: Return to Gateway -> Verify `#screen-gateway.active`, student selection cleared.
   - `T1.1.4`: Portal transition latency measurement (<50ms assertion).
   - `T1.1.5`: Direct portal switching (`switchPortal`) transitions cleanly between brothers.
2. **Daily Missions & Concept Refreshers**:
   - `T1.2.1`: Ali Today Mission button triggers `#start-modal.active` with `DAILY_Y5_ENG_W1D1`.
   - `T1.2.2`: Mostafa Today Mission button triggers `#start-modal.active` with `DAILY_Y6_ARB_W1D4`.
   - `T1.2.3`: Concept refresher accordion expands and renders pedagogical rules without layout shift.
   - `T1.2.4`: Modal close button dismisses start dialog and restores student screen.
   - `T1.2.5`: Video lesson thumbnail triggers educational video preview modal.
3. **28-Exam Catalog & Quiz Engine**:
   - `T1.3.1`: Verify all 14 Ali exams render cards with correct titles and durations.
   - `T1.3.2`: Verify all 11 Mostafa exams render cards with correct titles and Arabic metadata.
   - `T1.3.3`: Verify 3 Foundational exams render correctly in catalog.
   - `T1.3.4`: Starting English Fantasy exam displays authentic reading passage box.
   - `T1.3.5`: Question pagination navigates forward/back and records option selections.
4. **Assessment Submission & Scoring Engine**:
   - `T1.4.1`: Submit 100% correct answers -> renders result screen with 100% and Mastery badge.
   - `T1.4.2`: Submit partial answers -> calculates exact earned/total score.
   - `T1.4.3`: Submit blank answers -> scores 0% with "Needs Review" rating.
   - `T1.4.4`: Detailed pedagogical explanation expands on question review cards.
   - `T1.4.5`: Completion updates corresponding Study Plan status to `Completed`.
5. **Parent Analytics & Administration**:
   - `T1.5.1`: Open Parent Portal -> renders Submissions tab with historical records.
   - `T1.5.2`: Switch to Analytics tab -> renders performance charts and radar overview.
   - `T1.5.3`: Toggle student filter in Admin -> updates student analytics title and metrics.
   - `T1.5.4`: Study Plan tab week filter (`W1`, `W2`, `W3`, `W4`) filters table rows accurately.
   - `T1.5.5`: Retake requests table renders student requests with Approve/Reject actions.

#### Tier 2: Boundary & Corner Cases (20 tests minimum)
1. **Timeouts & Session Expirations**:
   - `T2.1.1`: Server-side expired session returns `TIME_EXPIRED` on submit.
   - `T2.1.2`: Client timer reaches `00:00` -> auto-triggers submission.
   - `T2.1.3`: Manipulated future client timestamp rejected by server `expiresAt`.
   - `T2.1.4`: Stale `localStorage` session restored after expiration -> triggers reset.
   - `T2.1.5`: Duration 0 or negative metadata defaults safely to 20 minutes.
2. **Attempt Limits & Concurrency**:
   - `T2.2.1`: Attempt count = 2 without approved retake returns `MAX_ATTEMPTS`.
   - `T2.2.2`: Approved retake increments allowed attempts by exactly 1.
   - `T2.2.3`: Rapid double-click on Submit button sends exactly one submission (idempotency).
   - `T2.2.4`: Student identity mismatch (Ali submitting Mostafa session) returns `STUDENT_MISMATCH`.
   - `T2.2.5`: Lock contention during concurrent submission releases cleanly.
3. **Input Sanitization & Arabic Diacritics**:
   - `T2.3.1`: Arabic answers match correctly regardless of Harakat presence (Fatha, Kasra, Damma).
   - `T2.3.2`: Arabic answers match correctly regardless of Tatweel (`\u0640`) character insertion.
   - `T2.3.3`: Arabic answers with non-NFKC diacritic order match expected answers.
   - `T2.3.4`: HTML injection (`<script>`, `<img onerror=...>`) in retake reason is escaped.
   - `T2.3.5`: Special quotes and smart apostrophes (`'`, `’`, `"`, `”`) in answers match standard quotes.
4. **Data & Schema Anomalies**:
   - `T2.4.1`: `Question_Bank` missing `Week` and `Difficulty` columns auto-heals non-destructively.
   - `T2.4.2`: Missing options string or empty options list handled without unhandled exception.
   - `T2.4.3`: Malformed review JSON in Submissions sheet falls back to empty array.
   - `T2.4.4`: Zero-question exam request returns clean `NO_QUESTIONS` error code.
   - `T2.4.5`: Corrupted `localStorage` data key does not block quiz launch.

#### Tier 3: Cross-Feature Integration Scenarios
1. `T3.1`: End-to-end Student Remediation Loop (Quiz Failure -> Score logged -> Retake Requested -> Admin Approved -> Retake Passed -> Study Plan updated).
2. `T3.2`: Dynamic Passage Pool Rotation (Consecutive sessions load different passage variants without text overlap).
3. `T3.3`: Multi-Week Cumulative Synthesis (W2 cumulative draws 50% W1 and 50% W2 items with zero question duplication).
4. `T3.4`: Network Interruption & Progress Restoration (Mid-exam page refresh restores selected radio buttons and timer).

#### Tier 4: Real-World Application Scenarios
1. `T4.1`: Dual-Student Morning Routine (Ali completes homework -> exits -> Mostafa completes homework on same browser -> verify complete data isolation).
2. `T4.2`: Comprehensive Weekend Parent Audit (Parent reviews analytics radar, filters Study Plan W1–W4, checks mistake breakdowns).

---

## 6. Verification Method

To independently verify the observations and findings in this report:

1. **Verify Existing Server Unit Tests**:
   ```powershell
   node --test tests/server.test.js tests/cumulative.test.js
   ```
   *Expected*: 13 tests pass in <1.0s.

2. **Verify 28-Exam Lifecycle and 100% Scoring**:
   ```powershell
   node .agents/teamwork/explorer_survey_testing/test_all_28_exams.js
   ```
   *Expected*: `28/28 PASSED, 0 FAILED`, 29 rows in Submissions sheet.

3. **Verify DOM Screen Transition Latencies (<50ms)**:
   ```powershell
   python .agents/teamwork/explorer_survey_testing/benchmark_transitions.py
   ```
   *Expected*: Ali portal ~4.26ms, Mostafa portal ~3.42ms, Parent portal ~38ms.

4. **Verify AST and HTML5 Well-Formedness**:
   ```powershell
   node -e "const vm=require('vm'), fs=require('fs'); new vm.Script(fs.readFileSync('Code.gs','utf8')); new vm.Script(fs.readFileSync('Index.html','utf8').match(/<script[\s\S]*?>([\s\S]*?)<\/script>/i)[1]); console.log('AST OK');"
   ```
   *Expected*: Outputs `AST OK` with exit code 0.

5. **Invalidation Conditions**:
   - If any of the 28 exams fails to return questions or fails to score upon submission.
   - If warmed DOM screen transitions exceed 50ms.
   - If `Index.html` exhibits unclosed HTML tags or syntax compilation errors.
