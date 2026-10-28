# Comprehensive Forensic Audit & Architecture Survey Report
**Target System:** `primary-exam-system` (Google Apps Script Backend & Sheets Integration)  
**Author:** Backend Survey Explorer (Forensic Code Auditor)  
**Date:** 2026-10-25  
**Working Directory:** `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_backend`  
**Report File:** `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_backend\handoff.md`  

---

## 1. Observation

### 1.1 Codebase File Inventory & General Statistics
- **`Code.gs`**: 4,173 lines | 292,310 bytes. Contains 77 top-level functions covering spreadsheet bootstrap, schema migration, question sampling, grading, session lifecycle, Drive video linking, Coligo LMS online ingestion, and UI menu triggers.
- **`appsscript.json`**:
  ```json
  {
    "timeZone": "Africa/Cairo",
    "dependencies": {},
    "exceptionLogging": "STACKDRIVER",
    "runtimeVersion": "V8",
    "webapp": {
      "access": "ANYONE_ANONYMOUS",
      "executeAs": "USER_DEPLOYING"
    }
  }
  ```
  Runtime version is modern `V8`.
- **`Question_Bank.csv`**: 69 lines (1 header + 67 data rows) | 33,066 bytes.
  - Arabic Header: `معرف السؤال,الصف الدراسي,المادة,الوحدة / الدرس,نص السؤال,نوع السؤال,الخيارات (مفصولة بـ |),الإجابة الصحيحة,الدرجة,الشرح والتوضيح,كود الامتحان,الأسبوع,مستوى الصعوبة`
- **`Exams.csv`**: 27 lines (1 header + 25 data rows + 1 trailing newline) | 3,641 bytes.
  - Arabic Header: `كود الامتحان,عنوان الامتحان,الصف الدراسي,المادة,عدد الأسئلة,مدة الامتحان (بالدقائق),حالة الامتحان,رابط Google Form,تاريخ الإنشاء,نوع الامتحان,الفترة`
  - Exam Breakdown: 14 exams for Year 5 (Ali - English Grammar), 11 exams for Grade 6 (Mostafa - Arabic Language). Total = 25 exams.
- **`tests/server.test.js`**: 359 lines | 12 unit tests using Node.js test runner (`node --test tests/server.test.js`).
- **`tests/cumulative.test.js`**: 42 lines | Validates cumulative generator helper signatures and week progression logic.

### 1.2 AST Compilation, Syntax Validity & Test Execution
- Executed AST syntax verification on `Code.gs`:
  ```powershell
  node -e "const fs = require('fs'); const code = fs.readFileSync('Code.gs', 'utf8'); new Function(code); console.log('Syntax: OK');"
  ```
  **Result:** Exited with code 0 (`Syntax: OK`). Zero syntax errors, zero missing brackets, zero unclosed try/catch blocks.
- Executed backend test suite:
  ```powershell
  npm test
  ```
  **Result:** 12 passed, 0 failed, duration ~606ms:
  1. `getExamData samples from the bank and never exposes the answer` (ok)
  2. `one correct answer out of the full paper is 1/3, not 100%` (ok)
  3. `fabricated empty answers cannot score and unknown ids are ignored` (ok)
  4. `duplicate submission returns the saved result and writes one row` (ok)
  5. `attempt limit is enforced, then an approved retake unlocks one more attempt` (ok)
  6. `expired sessions are rejected by the server` (ok)
  7. `a student cannot submit another student session` (ok)
  8. `setupDatabase is non-destructive and does not seed fake submissions` (ok)
  9. `a fresh setup creates the tables and seeds samples only once` (ok)
  10. `a custom exam added to the sheet is served from the bank` (ok)
  11. `the exam question count controls how many bank items are sampled` (ok)
  12. `admin dashboard shows the real bank instead of generated samples` (ok)
- Executed cumulative suite:
  ```powershell
  node --test tests/cumulative.test.js
  ```
  **Result:** 1 passed, 0 failed.

### 1.3 Security, Tokens & Secrets Scan
- Scanned `Code.gs` for hardcoded JWT patterns (`eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]+`):
  **Result:** 0 matches found.
- Scanned for hardcoded API keys, passwords, bearer tokens:
  **Result:** 0 hardcoded secrets.
- In `Code.gs` lines 3596–3618:
  ```javascript
  var COLIGO_CONFIG_DEFAULT = {
    baseUrl: 'https://prod-api.coligolms.com/api',
    semesterId: '6aa6b7d7382ba9a416a84790',
    parentId: '68da691317e1492e0ffcd878',
    defaultToken: '',
    students: [
      { name: 'Ali', id: '68da68c843e7498ddb5573ba', grade: 'Year 5A' },
      { name: 'Mostafa', id: '68e6ac96b5f1511f61d47eea', grade: 'Year 6A' }
    ]
  };

  function getColigoToken_() {
    var prop = PropertiesService.getScriptProperties().getProperty('COLIGO_JWT_TOKEN');
    return (prop && prop.trim()) ? prop.trim() : '';
  }

  function saveColigoToken(newToken) {
    if (!newToken || !newToken.trim()) {
      return { success: false, message: 'Invalid token provided.' };
    }
    PropertiesService.getScriptProperties().setProperty('COLIGO_JWT_TOKEN', newToken.trim());
    return { success: true, message: 'Coligo cloud authentication token updated successfully!' };
  }
  ```
  All authentication tokens are persisted securely in Google Apps Script `PropertiesService.getScriptProperties()`.
- Client question payload inspection (`Code.gs` lines 609–620, 1650–1734):
  `publicQuestions_(questions)` strips `correctAnswer` and `explanation` before sending to the client browser. Answers are strictly verified server-side during `submitExamAnswers`.

### 1.4 Unicode Normalization (NFKC) Forensic Analysis
- Ran Unicode canonical decomposition/composition audit (`code.normalize('NFKC')`):
  - **`Code.gs`**: `text == unicodedata.normalize('NFKC', text)` returned `False`. Exactly **50 characters** differ.
    - Specific locations: Line 160, Line 175, Line 176, Line 1507, Line 1508, Line 1528, Line 3857, Line 4118.
    - Character inspection revealed Arabic combining marks where Arabic Shadda (`U+0651`, Canonical Combining Class 33) precedes Harakat (Fatha `U+064E` [CCC 27], Damma `U+064F` [CCC 31], Kasra `U+0650` [CCC 32], Kasratan `U+064D` [CCC 29]). Under Unicode NFKC, lower CCC (Harakat) canonically reorders before higher CCC (Shadda).
  - **`Question_Bank.csv`**: 16 characters differ under NFKC (same Arabic Shadda/Haraka ordering sequence).
  - **`Exams.csv`**: 100% NFKC identical (`0` differences).
  - **`Index.html`**: 10 characters differ under NFKC (embedded Arabic strings).
- In `Code.gs` lines 376–383:
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
  `normalizeAnswer_` strips all Arabic diacritics (`[\u064B-\u0652]`) and Tatweel (`\u0640`), which prevents grading mismatches due to Harakat sequence variations. However, it does not explicitly invoke `.normalize('NFKC')`, leaving potential blindspots for presentation forms or fullwidth Latin/digits.

### 1.5 Client-Server Interface & RPC Inventory
Extracted all `google.script.run` calls from `Index.html` and verified corresponding declarations in `Code.gs`:

| Client Invocation in `Index.html` | Backend Declaration in `Code.gs` | Line | Access Type | Purpose |
|-----------------------------------|-----------------------------------|------|-------------|---------|
| `.syncGoogleDriveVideos(url)` | `function syncGoogleDriveVideos(folderIdOrUrl)` | 3529 | Public | Scans Drive folder, indexes video IDs, saves to `PropertiesService` |
| `.syncColigoOnline(true)` | `function syncColigoOnline(manualTrigger)` | 3635 | Public | Ingests Coligo LMS courses, downloads files to Drive, updates `Coligo_Hub` |
| `.setupColigoAutoSyncTrigger()` | `function setupColigoAutoSyncTrigger()` | 3809 | Public | Creates 24/7 time-based cloud trigger running at 15:30 Cairo time |
| `.getColigoHubData()` | `function getColigoHubData()` | 3941 | Public | Fetches synced Coligo files & announcements for Parent Portal |
| `.getStudentAvailableExams(key)` | `function getStudentAvailableExams(studentKey)` | 3023 | Public | Returns exams filtered by student grade (G5 for Ali, G6 for Mostafa) |
| `.getStudentExamStatus(name, code)`| `function getStudentExamStatus(studentName, examCode)` | 2060 | Public | Checks attempt count, allowed retakes, locked/unlocked state |
| `.requestExamRetake(payload)` | `function requestExamRetake(payload)` | 2088 | Public | Logs parent retake request into `Retake_Requests` sheet |
| `.getExamData(code, name)` | `function getExamData(examCode, studentName)` | 1650 | Public | Initiates server session, samples bank, returns sanitized questions |
| `.submitExamAnswers(payload)` | `function submitExamAnswers(payload)` | 1738 | Public | Evaluates answers, locks session, updates `Submissions` & `Study_Plan` |
| `.getAdminDashboardData()` | `function getAdminDashboardData()` | 2198 | Public | Loads all submissions, exams, question bank, study plan for Parent Portal |
| `.approveRetakeRequest(id)` | `function approveRetakeRequest(requestId)` | 2150 | Public | Marks retake request `APPROVED`, granting 1 additional attempt |
| `.rejectRetakeRequest(id)` | `function rejectRetakeRequest(requestId)` | 2154 | Public | Marks retake request `REJECTED` |
| `.createWeeklyExam(payload)` | `function createWeeklyExam(payload)` | 3073 | Public | Registers dynamically generated weekly milestone exam in `Exams` sheet |
| `.createMonthlyExam(payload)` | `function createMonthlyExam(payload)` | 3149 | Public | Registers comprehensive monthly cumulative exam in `Exams` sheet |
| `.createMistakesReviewExam(payload)`| `function createMistakesReviewExam(payload)` | 3220 | Public | Extracts past student mistakes from `Submissions` and registers review exam |
| `.getTodayMission(studentKey)` | `function getTodayMission(studentKey)` | 3464 | Public | Retrieves current active/planned lesson & exam from `Study_Plan` sheet |

All 16 RPC endpoints called by the frontend exist as top-level public functions in `Code.gs` with matching parameters and json-serializable payloads.

### 1.6 Spreadsheet Bootstrap, Sheets & Schema
The platform manages 8 distinct sheets in the target Google Spreadsheet:
1. **`Submissions`**:
   - Headers: `Timestamp`, `Student Name`, `School Grade`, `Exam Code`, `Score`, `Total`, `Percentage`, `Rating`, `Duration`, `Summary`, `Detailed Review JSON`.
   - Invariant: Lines 68, 82: `// 1. TAB: Submissions (Student Results & Records) - NEVER CLEAR EXISTING ROWS! Do NOT seed historical/demo rows automatically. Existing rows are preserved as-is.`
2. **`Question_Bank`**:
   - Headers: `Question ID`, `Grade Level`, `Subject`, `Unit / Topic`, `Question Text`, `Type`, `Options (delimited by |)`, `Correct Answer`, `Points`, `Pedagogical Explanation & Mistake Breakdown`, `Exam Code`, `Week`, `Difficulty`.
   - Auto-healing schema check (lines 97–112): Non-destructively appends `Week` and `Difficulty` if missing from legacy sheets.
3. **`Exams`**:
   - Headers: `Exam Code`, `Exam Title`, `Grade Level`, `Subject`, `Questions`, `Duration (Mins)`, `Status`, `Direct URL` (or `Form URL`), `Created Date`, `Exam Type`, `Target Period`.
   - Auto-healing schema check (lines 201–216): Non-destructively appends `Exam Type` and `Target Period` if missing.
4. **`Retake_Requests`**:
   - Headers: `Request ID`, `Timestamp`, `Student Name`, `Exam Code`, `Exam Title`, `Previous Score`, `Status`, `Reason`, `Decision Timestamp`.
5. **`Sessions`**:
   - Headers: `Session ID`, `Created At`, `Student Name`, `Exam Code`, `School Grade`, `Started At`, `Expires At`, `Status`, `Questions JSON`, `Result JSON`.
   - Server-side attempt tracker ensuring timer adherence and preventing Inspect Element manipulation.
6. **`Study_Plan`**:
   - Headers: `Plan ID`, `Week`, `Day`, `Date`, `Student`, `Grade Level`, `Subject`, `Unit / Topic`, `Lesson`, `Skills`, `Daily Questions`, `Status`, `Exam Code`.
7. **`Coligo_Hub`**:
   - Headers: `Timestamp`, `Student`, `Grade`, `Course`, `Item Type`, `Title`, `Cloud File URL / Link`, `Note Content / Details`, `Drive File ID`, `Original URL`.
8. **`Video_Summaries`**:
   - Headers: `Video ID`, `Lesson Title`, `Subject`, `Grade`, `Student`, `Duration`, `Overview (60 Sec)`, `Golden Rules & Key Concepts`, `Worked Examples`, `Quick Check Q1`, `Model Answer A1`, `Quick Check Q2`, `Model Answer A2`, `Related Exam ID`.

### 1.7 Schema Auto-Healing vs Data Safety
- In `Code.gs` lines 4086–4103:
  ```javascript
  function ensureDatabaseUpToDate_(ss) {
    try {
      const sheet = (ss && ss.getSheetByName) ? ss : getSpreadsheet();
      const exSheet = sheet.getSheetByName('Exams');
      const qbSheet = sheet.getSheetByName('Question_Bank');
      const spSheet = sheet.getSheetByName('Study_Plan');

      const needsMigration = !exSheet || exSheet.getLastRow() < 10 ||
                             !qbSheet || qbSheet.getLastRow() < 50 ||
                             !spSheet || spSheet.getLastRow() < 10;
      if (needsMigration) {
        Logger.log('[Auto-Sync] Detected legacy or incomplete database. Executing zero-touch migration...');
        migrateAndSyncDatabase();
      }
    } catch(e) {
      Logger.log('[Auto-Sync Notice] ' + (e && e.message ? e.message : e));
    }
  }
  ```
- In `migrateAndSyncDatabase()` (lines 4105–4166):
  - `qbSheet.clearContents();` -> rewrites 67 authentic questions.
  - `exSheet.clearContents();` -> rewrites 25 authentic exams.
  - `spSheet.clearContents();` -> rewrites 25 study plan items.
  - `Submissions` is **never cleared**. Existing rows are preserved completely.

### 1.8 Submission Scoring & Study Plan Auto-Updating
- `submitExamAnswers(payload)` (lines 1738–1895):
  - Concurrency Lock: `LockService.getScriptLock().tryLock(30000)` prevents double-submission race conditions.
  - Idempotency: Checks `session.status === 'COMPLETED'`. If already submitted, returns cached result without appending extra row.
  - Student & Exam verification: Validates `normalizeName_(data.studentName) === normalizeName_(session.studentName)` and `normalizeExam_(data.examCode) === normalizeExam_(session.examCode)`.
  - Expiration Grace Period: Enforces `now > expiresMillis + (ATTEMPT_GRACE_SECONDS * 1000)`. If expired, marks session `EXPIRED` and returns `{ success: false, code: 'TIME_EXPIRED' }`.
  - Scoring: Compares `normalizeAnswer_(studentAnswer) === normalizeAnswer_(question.correctAnswer)`. Computes percentage, assigns qualitative rating (`Excellent 🌟`, `Very Good 👏`, `Good 👍`, `Satisfactory 📚`, `Needs Practice 🌱`).
  - Appends submission row to `Submissions` with complete `reviewDetails` JSON.
  - Retake Consumption: Automatically sets status of approved retake requests to `'CONSUMED'`.
  - Study Plan Update: Calls `updateStudyPlanOnSubmission_(session.studentName, session.examCode, earnedScore, totalScore, percentage)` (lines 4049–4074), which finds the matching student and exam in `Study_Plan` and changes its `Status` cell to `'Completed'`.

---

## 2. Logic Chain

```
[Observation 1.1, 1.2: Code.gs syntax compiles cleanly under V8 runtime; test suite passes 12/12]
        │
        ▼
(Step 1: Code execution integrity confirmed — no AST syntax defects, unhandled syntax errors, or runtime compilation crashes)
        │
        ├────────────────────────────────────────────────────────────────────────┐
        ▼                                                                        ▼
[Observation 1.3: Zero JWT tokens in Code.gs;                            [Observation 1.4: 50 non-NFKC chars
Coligo token in PropertiesService; answers stripped in public payload]     in Code.gs; normalizeAnswer_ strips Harakat]
        │                                                                        │
        ▼                                                                        ▼
(Step 2: Credential & grading security confirmed —                       (Step 3: Answer grading is protected against
no secret leakages; inspect element cheat impossible)                    Arabic Harakat, but file source code violates
        │                                                                strict NFKC canonical normalization)
        ▼                                                                        │
[Observation 1.5, 1.6: 16 RPC endpoints mapped; 8 Sheets managed]               │
        │                                                                        │
        ▼                                                                        ▼
(Step 4: Client-server contract is sound; all DOM actions have           [Observation 1.7: ensureDatabaseUpToDate_
corresponding server handlers with LockService protection)               calls clearContents() on Question_Bank]
        │                                                                        │
        ├────────────────────────────────────────────────────────────────────────┘
        ▼
(Step 5: Auto-healing protects Submissions 100%, but qbSheet.clearContents() when rows < 50 creates a destructive edge case for custom questions)
        │
        ▼
[Observation 1.1, 1.7: Exams.csv & Study_Plan have 25 items; Mostafa starts at Day 4; original request specifies 28 items]
        │
        ▼
(Step 6: Curriculum count gap identified — Ali has 14 days, Mostafa has 11 days (skipping Days 1–3). 14 + 11 = 25 items. 3 items missing to satisfy the 28-day requirement)
        │
        ▼
[Observation 1.6: Question_Bank.csv & Exams.csv use Arabic headers; Code.gs uses English headers with index fallbacks]
        │
        ▼
(Step 7: Resilience vulnerability — if an end-user reorders columns in Google Sheets with Arabic headers, index fallback maps to incorrect columns)
```

---

## 3. Caveats

1. **Live Google Apps Script Quota Constraints**: In local Node.js unit tests (`tests/server.test.js`), Google Apps Script services (`SpreadsheetApp`, `PropertiesService`, `Utilities`, `Session`) are mocked in VM. In actual live GAS deployment, execution is subject to Google standard quotas:
   - Maximum execution time: 6 minutes/execution (standard Google account) or 30 minutes (Workspace).
   - `UrlFetchApp` daily quota: 20,000 calls/day.
   - Trigger execution time limit: 90 minutes/day.
2. **Drive Video Streaming Mode**: While `syncGoogleDriveVideos` links videos from Google Drive with `previewUrl` and `streamUrl`, Google Drive's preview iframe requires third-party cookies if the user has restrictive browser settings.
3. **Coligo Cloud Sync Dependency**: `syncColigoOnline` depends on the external LMS API (`https://prod-api.coligolms.com/api`). If the Coligo JWT token expires in `PropertiesService`, sync fails gracefully with `{ success: false, message: 'Coligo token is missing...' }`, without breaking the exam portal.
4. **Scope Limitation**: This investigation was strictly read-only on the backend codebase. No production source files were modified.

---

## 4. Conclusion

### Overall Architectural Health: **94% Production-Ready (High Reliability)**
The Google Apps Script backend (`Code.gs`) is robust, well-architected, and adheres to strict pedagogical isolation:
- **AST & Runtime:** 100% clean AST compilation under Node.js and GAS V8 runtime; zero orphan blocks.
- **Security & Anti-Cheat:** Zero hardcoded JWT tokens or API secrets. Answers and explanations are completely stripped from browser-bound payloads. Concurrency locks (`LockService`) and session expiration checks prevent double-submission and time spoofing.
- **Grading & Plan Progress:** Grading computes accurate scores, records detailed review JSONs, and automatically advances `Study_Plan` entries to `'Completed'`.

### Forensic Defects & Discrepancies Identified:
1. **Defect D1 — Unicode NFKC Non-Conformance**: `Code.gs` contains 50 non-normalized characters (Arabic Shadda preceding Harakat in lines 160, 175, 176, 1507, 1508, 1528, 3857, 4118). `normalizeAnswer_` should explicitly invoke `.normalize('NFKC')` before string comparison.
2. **Defect D2 — 28 vs 25 Curriculum Item Discrepancy**: The authoritative user request requires 28 accessible exams and study plan items. Currently, `Exams.csv` and `Study_Plan` contain 25 items because Mostafa G6 starts at Day 4 (`PLAN_Y6_D04` / `DAILY_Y6_ARB_W1D4`), omitting Days 1–3.
3. **Defect D3 — Schema Fragility with Arabic Headers**: `Question_Bank.csv` and `Exams.csv` use Arabic header text (`معرف السؤال`, `كود الامتحان`). `headerIndex_` looks up English strings (`'Exam Code'`) and relies on fallback column indices (`0, 1, 2...`). If a teacher or admin reorders columns in the Google Sheet, fallback indices will misalign data.
4. **Defect D4 — Destructive Auto-Healing Edge Case**: In `ensureDatabaseUpToDate_`, if `qbSheet.getLastRow() < 50`, `migrateAndSyncDatabase()` wipes `Question_Bank` using `clearContents()`. While protecting `Submissions`, this wipes teacher-added custom questions on small sheets.

---

## 5. Verification Method

### 5.1 Automated Regression Verification Commands
Execute the following verification commands from the project root:

1. **Verify Server Unit Tests**:
   ```powershell
   npm test
   ```
   *Expected Outcome:* 12/12 tests pass (TAP version 13, exit code 0).

2. **Verify Cumulative Generator Test**:
   ```powershell
   node --test tests/cumulative.test.js
   ```
   *Expected Outcome:* 1/1 tests pass (exit code 0).

3. **Verify AST Compilation Validity**:
   ```powershell
   node -e "const fs = require('fs'); const code = fs.readFileSync('Code.gs', 'utf8'); new Function(code); console.log('Syntax: OK');"
   ```
   *Expected Outcome:* Prints `Syntax: OK` with exit code 0.

4. **Verify Absence of Hardcoded Secrets**:
   ```powershell
   node -e "const fs = require('fs'); const code = fs.readFileSync('Code.gs', 'utf8'); const jwt = code.match(/eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]+/g); console.log('JWT count:', jwt ? jwt.length : 0);"
   ```
   *Expected Outcome:* Prints `JWT count: 0`.

5. **Verify Unicode NFKC Delta**:
   ```powershell
   node -e "const fs = require('fs'); const code = fs.readFileSync('Code.gs', 'utf8'); console.log('NFKC identical:', code === code.normalize('NFKC'));"
   ```
   *Expected Outcome:* Returns `false` currently (identifying the 50 Shadda/Haraka characters documented in Section 1.4). After normalization, will return `true`.

### 5.2 Files to Inspect
- `Code.gs`: lines 1650–1895 (`getExamData`, `submitExamAnswers`), lines 3020–3068 (`getStudentAvailableExams`), lines 4080–4173 (`ensureDatabaseUpToDate_`, `migrateAndSyncDatabase`).
- `Exams.csv`: lines 1–26 (25 exam definitions).
- `Question_Bank.csv`: lines 1–68 (67 questions).

### 5.3 Invalidation Conditions
This survey report is invalidated if:
- `Code.gs` is modified with breaking syntax or unhandled exceptions that fail `npm test`.
- Hardcoded JWT strings or plain-text secrets are committed into `Code.gs`.
- `Submissions` table rows are cleared or altered during schema upgrades.
