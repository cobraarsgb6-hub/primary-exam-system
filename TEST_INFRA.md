# ⚠️ مستند أرشيف تاريخي (HISTORICAL ARCHIVE)
> [!CAUTION]
> **تنبيه:** هذا المستند يمثل تقريرًا أو خطة مرحلية من فترات التطوير السابقة وهو غير نشط حالياً.
> المرجع المعتمد الوحيد للحالة الراهنة الحية هو: [CURRENT_STATUS_AR.md](CURRENT_STATUS_AR.md)
> خارطة الطريق المعتمدة المكتملة: [ROADMAP_SPECKIT_AR.md](ROADMAP_SPECKIT_AR.md)

---

# Testing Infrastructure & Verification Architecture (TEST_INFRA)

## 1. System Overview & Testing Philosophy

The `primary-exam-system` testing framework utilizes an **Opaque-Box E2E Testing Architecture** designed to rigorously validate all functional, architectural, and security contracts of the Google Apps Script backend (`Code.gs`) and HTML5 single-page application frontend (`Index.html`).

Because Google Apps Script web applications rely on the client-side `google.script.run` asynchronous remote procedure call (RPC) mechanism, client execution outside the GAS iframe requires a high-fidelity RPC Mock Bridge. The testing infrastructure injects an authentic in-browser mock bridge via Playwright's `page.add_init_script`, providing:
1. Full 16-endpoint server contract emulation with authentic schema types and return signatures.
2. Direct access to the complete 28-exam catalog, 25-item curriculum study plan, and question bank.
3. Bidirectional state synchronisation, session lifecycle tracking, atomic submission logging, and study plan auto-completion.
4. Programmatic fault-injection capabilities (simulating server timeouts, lock contention `BUSY`, concurrency breaches, diacritic variance, and schema anomalies).

---

## 2. Test Directory Structure

```
primary-exam-system/
├── TEST_INFRA.md                      # Comprehensive testing infrastructure documentation (this file)
├── TEST_READY.md                      # Test readiness declaration and execution manifest
├── package.json                       # Node.js test script entrypoint
├── tests/
│   ├── server.test.js                 # Server-side GAS VM runtime tests (11 unit tests)
│   ├── cumulative.test.js             # Cumulative generator signature and contract tests (2 unit tests)
│   └── e2e/
│       ├── mock_bridge.js             # Injectable GAS RPC Mock Bridge (16 endpoints + authentic data)
│       ├── tier1_core_coverage.py     # Tier 1: Core Feature Coverage (25 tests)
│       ├── tier2_boundary_corner.py   # Tier 2: Boundary & Corner Cases (20 tests)
│       ├── tier3_cross_feature.py     # Tier 3: Cross-Feature Integration Scenarios (4 scenarios)
│       ├── tier4_real_world.py        # Tier 4: Real-World Application Scenarios (2 scenarios)
│       └── run_all_e2e.py             # Master Test Runner (runs all 4 tiers, collects pass/fail metrics)
```

---

## 3. Execution Environment & Dependencies

- **Node.js**: `v22.23.2` built-in test runner (`node --test`), `node:vm`, `node:assert/strict`
- **Python**: `3.14.7` with `playwright` (`1.60.0`), `lxml`, `pandas`
- **Browser Automation Engine**: Playwright Chromium (headless mode)
- **Zero External Dependencies**: Operates entirely with pre-installed workspace packages without requiring `pytest` or `npm install`.

---

## 4. RPC Mock Bridge Specification (`tests/e2e/mock_bridge.js`)

The Mock Bridge intercepts `window.google.script.run` inside the headless Chromium context and fulfills all 16 public server endpoints:

| # | Endpoint | Description | Return Contract |
|---|----------|-------------|-----------------|
| 1 | `getStudentAvailableExams(studentKey)` | Fetches registered exam catalog for student | `{ success: true, exams: [...], driveVideos: {...} }` |
| 2 | `getTodayMission(studentKey)` | Returns designated daily mission | `{ success: true, mission: { examCode, title, lesson, skills, ... } }` |
| 3 | `getStudentExamStatus(studentName, examCode)` | Queries historical attempts and retake eligibility | `{ success: true, attempts: [...], hasSubmitted: bool, canAttempt: bool, retakeStatus: string, maxAttempts: 2 }` |
| 4 | `getExamData(examCode, studentName)` | Generates secure question set (withholds answers) | `{ success: true, sessionKey: string, remainingSeconds: int, exam: {...}, questions: [...] }` |
| 5 | `submitExamAnswers(payload)` | Atomic scoring, review generation, study plan update | `{ success: true, earnedScore: int, totalScore: int, percentage: int, rating: string, durationSpent: string, review: [...] }` |
| 6 | `requestExamRetake(payload)` | Submits formal student retake petition | `{ success: true, message: string }` |
| 7 | `approveRetakeRequest(id)` | Admin authorization granting additional attempt | `{ success: true, message: string }` |
| 8 | `rejectRetakeRequest(id)` | Admin decline of student retake petition | `{ success: true, message: string }` |
| 9 | `getAdminDashboardData()` | Aggregated parent view data | `{ success: true, sheetUrl: string, submissions: [...], retakeRequests: [...], studyPlan: [...] }` |
| 10 | `createWeeklyExam(payload)` | Generates weekly milestone retest exam | `{ success: true, examCode: string, message: string }` |
| 11 | `createMonthlyExam(payload)` | Generates monthly cumulative synthesis exam | `{ success: true, examCode: string, message: string }` |
| 12 | `createMistakesReviewExam(payload)` | Generates targeted mistake review exam | `{ success: true, examCode: string, message: string }` |
| 13 | `syncGoogleDriveVideos(folderUrlOrId)` | Scans Drive folder and updates video mapping | `{ success: true, message: string, videoMap: {...} }` |
| 14 | `syncColigoOnline(manualTrigger)` | Synchronizes external LMS course materials | `{ success: true, message: string }` |
| 15 | `setupColigoAutoSyncTrigger()` | Configures daily cloud sync trigger | `{ success: true, message: string }` |
| 16 | `getColigoHubData()` | Fetches synchronized LMS materials | `{ success: true, items: [...], count: int }` |

### State Management & Fault Injection API (`window.__mockBridge`)
Tests configure runtime conditions dynamically via `window.__mockBridge.state`:
- `forceTimeout`: Forces submit or question retrieval to fail with `TIME_EXPIRED`.
- `forceBusy`: Forces lock contention simulation returning `{ success: false, code: 'BUSY' }`.
- `forceMaxAttempts`: Forces attempt limit exhaustion (`MAX_ATTEMPTS`).
- `forceStudentMismatch`: Simulates session hijacking / student identity mismatch (`STUDENT_MISMATCH`).
- `forceEmptyQuestions`: Simulates missing question bank data (`NO_QUESTIONS`).
- `resetState()`: Restores clean database state between tests.

---

## 5. Comprehensive 4-Tier Test Matrix (51 Tests Total)

### Tier 1: Core Feature Coverage (25 tests)
- **1. Gateway & Portal Isolation (5 tests)**:
  - `T1.1.1`: Click Ali Gateway -> Verify `#screen-student.active`, blue theme, Grade 5 badge.
  - `T1.1.2`: Click Mostafa Gateway -> Verify `#screen-student.active`, purple theme, Grade 6 badge.
  - `T1.1.3`: Return to Gateway -> Verify `#screen-gateway.active`, student selection cleared.
  - `T1.1.4`: Portal transition latency measurement (<50ms assertion).
  - `T1.1.5`: Direct portal switching (`switchPortal`) transitions cleanly between brothers.
- **2. Daily Missions & Concept Refreshers (5 tests)**:
  - `T1.2.1`: Ali Today Mission button triggers `#start-modal.active` with `DAILY_Y5_ENG_W1D1`.
  - `T1.2.2`: Mostafa Today Mission button triggers `#start-modal.active` with `DAILY_Y6_ARB_W1D4`.
  - `T1.2.3`: Concept refresher accordion expands and renders pedagogical rules without layout shift.
  - `T1.2.4`: Modal close button dismisses start dialog and restores student screen.
  - `T1.2.5`: Video lesson thumbnail triggers educational video preview modal (`#video-modal.active`).
- **3. 28-Exam Catalog & Quiz Engine (5 tests)**:
  - `T1.3.1`: Verify all 14 Ali exams render cards with correct titles and durations.
  - `T1.3.2`: Verify all 11 Mostafa exams render cards with correct titles and Arabic metadata.
  - `T1.3.3`: Verify 3 Foundational exams render correctly in catalog.
  - `T1.3.4`: Starting English Fantasy exam displays authentic reading passage box.
  - `T1.3.5`: Question pagination navigates forward/back and records option selections.
- **4. Assessment Submission & Scoring Engine (5 tests)**:
  - `T1.4.1`: Submit 100% correct answers -> renders result screen with 100% and Mastery badge.
  - `T1.4.2`: Submit partial answers -> calculates exact earned/total score.
  - `T1.4.3`: Submit blank answers -> scores 0% with "Needs Review" rating.
  - `T1.4.4`: Detailed pedagogical explanation expands on question review cards.
  - `T1.4.5`: Completion updates corresponding Study Plan status to `Completed`.
- **5. Parent Analytics & Administration (5 tests)**:
  - `T1.5.1`: Open Parent Portal -> renders Submissions tab with historical records.
  - `T1.5.2`: Switch to Analytics tab -> renders performance charts and radar overview.
  - `T1.5.3`: Toggle student filter in Admin -> updates student analytics title and metrics.
  - `T1.5.4`: Study Plan tab week filter (`W1`, `W2`, `W3`, `W4`) filters table rows accurately.
  - `T1.5.5`: Retake requests table renders student requests with Approve/Reject actions.

### Tier 2: Boundary & Corner Cases (20 tests)
- **1. Timeouts & Session Expirations (5 tests)**:
  - `T2.1.1`: Server-side expired session returns `TIME_EXPIRED` on submit.
  - `T2.1.2`: Client timer reaches `00:00` -> auto-triggers submission.
  - `T2.1.3`: Manipulated future client timestamp rejected by server `expiresAt`.
  - `T2.1.4`: Stale `localStorage` session restored after expiration -> triggers reset.
  - `T2.1.5`: Duration 0 or negative metadata defaults safely to 20 minutes.
- **2. Attempt Limits & Concurrency (5 tests)**:
  - `T2.2.1`: Attempt count >= 2 without approved retake returns `MAX_ATTEMPTS`.
  - `T2.2.2`: Approved retake increments allowed attempts by exactly 1.
  - `T2.2.3`: Rapid double-click on Submit button sends exactly one submission (idempotency).
  - `T2.2.4`: Student identity mismatch (Ali submitting Mostafa session) returns `STUDENT_MISMATCH`.
  - `T2.2.5`: Lock contention during concurrent submission (`BUSY`) handles gracefully without crashing UI.
- **3. Input Sanitization & Arabic Diacritics (5 tests)**:
  - `T2.3.1`: Arabic answers match correctly regardless of Harakat presence (Fatha, Kasra, Damma).
  - `T2.3.2`: Arabic answers match correctly regardless of Tatweel (`\u0640`) character insertion.
  - `T2.3.3`: Arabic answers with non-NFKC diacritic order match expected answers.
  - `T2.3.4`: HTML injection (`<script>`, `<img onerror=...>`) in retake reason is escaped in DOM.
  - `T2.3.5`: Special quotes and smart apostrophes (`'`, `’`, `"`, `”`) in answers match standard quotes.
- **4. Data & Schema Anomalies (5 tests)**:
  - `T2.4.1`: `Question_Bank` missing `Week` and `Difficulty` columns handles non-destructively.
  - `T2.4.2`: Missing options string or empty options list handled without unhandled exception.
  - `T2.4.3`: Malformed review JSON in Submissions sheet falls back to empty array / safe render.
  - `T2.4.4`: Zero-question exam request returns clean `NO_QUESTIONS` error code.
  - `T2.4.5`: Corrupted `localStorage` data key does not block quiz launch (`safeStorage` resilience).

### Tier 3: Cross-Feature Integration Scenarios (4 scenarios)
- `T3.1`: Full student remediation loop (Quiz Failure -> Score logged -> Retake Requested -> Admin Approved -> Retake Passed -> Study Plan updated).
- `T3.2`: Dynamic passage pool rotation (Consecutive sessions load different passage variants without text overlap).
- `T3.3`: Multi-week cumulative synthesis (W2 cumulative draws 50% W1 and 50% W2 items with zero question duplication).
- `T3.4`: Progress restoration on refresh (Mid-exam page refresh restores selected radio buttons and timer).

### Tier 4: Real-World Application Scenarios (2 scenarios)
- `T4.1`: Dual-student morning routine on shared browser (Ali completes homework -> exits -> Mostafa completes homework on same browser -> verify complete data isolation).
- `T4.2`: Comprehensive weekend parent audit (Parent reviews analytics radar, filters Study Plan W1–W4, checks mistake breakdowns).

---

## 6. Verification Commands

```powershell
# 1. Run Server VM Unit Tests (GAS mocks)
node --test tests/server.test.js tests/cumulative.test.js

# 2. Run Individual E2E Tiers
python tests/e2e/tier1_core_coverage.py
python tests/e2e/tier2_boundary_corner.py
python tests/e2e/tier3_cross_feature.py
python tests/e2e/tier4_real_world.py

# 3. Run Complete 4-Tier E2E Master Runner
python tests/e2e/run_all_e2e.py
```

---

## 7. Pass/Fail Quality Gates

1. **Zero Console Errors**: No unhandled JavaScript exceptions during execution.
2. **Strict Score Accuracy**: Scoring engine produces exact point tallies matching canonical answers.
3. **Data Safety**: Submissions and study plan progress persist without data loss across sessions.
4. **Sub-50ms DOM Rendering**: Direct DOM screen switching performs under 50ms on warmed browser instances.
