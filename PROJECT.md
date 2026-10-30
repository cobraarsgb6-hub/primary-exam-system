# ⚠️ مستند أرشيف تاريخي (HISTORICAL ARCHIVE)
> [!CAUTION]
> **تنبيه:** هذا المستند يمثل تقريرًا أو خطة مرحلية من فترات التطوير السابقة وهو غير نشط حالياً.
> المرجع المعتمد الوحيد للحالة الراهنة الحية هو: [CURRENT_STATUS_AR.md](CURRENT_STATUS_AR.md)
> خارطة الطريق المعتمدة المكتملة: [ROADMAP_SPECKIT_AR.md](ROADMAP_SPECKIT_AR.md)

---

﻿# Project: primary-exam-system Audit, Verification & Hardening

## Architecture
The `primary-exam-system` is an assessment, learning, and analytics platform designed for primary school students (Ali - Year 5, Mostafa - Grade 6) and their parents. It comprises:
1. **Backend (`Code.gs`)**: Google Apps Script (V8 runtime) with 18 client-invoked RPC endpoints, dynamic question-bank sampling, `LockService`-guarded sessions, server-side grading, retake lifecycle, the weekly/monthly/mistakes exam factory, study-plan advancement, and Google Drive / Coligo LMS integration. Admin mutations require a short-lived `ADMIN_TOK_*` token issued by `verifyAdminPin` / `verifyGatewayPin`; sheet-menu wrappers call unguarded `*_` cores.
2. **Frontend (`Index.html` + templates)**: single-page application split into `Index.html` (shell/screens), `Styles.html` (CSS), `HubData.js.html` (catalogs, standalone engine, video/Coligo/homework UI), `QuizApp.js.html` (quiz runtime + submission), and `Portal.js.html` (student dashboard, Parent Portal, Study Plan, exam factory). `bundle.py` resolves the `include()` directives into `Index.bundle.html` for offline/Android use.
3. **Data Layer (Google Sheets + CSVs)**: 8 managed sheets (`Submissions`, `Question_Bank`, `Exams`, `Retake_Requests`, `Sessions`, `Study_Plan`, `Coligo_Hub`, `Homework_Status`) with non-destructive schema migration, bilingual (Arabic/English) header resolution, and strict preservation of historical submissions.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | HTML5 DOM & AST Integrity | 100% well-formed HTML5, 0 orphaned tags, no scripts outside `<html>`, clean Node AST | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Screen Transition Speed | Sub-50ms screen transitions (Gateway <-> Student <-> Quiz <-> Result <-> Admin) | M1 | ORIGINAL_REQUEST §R2 |
| 3 | Question Bank Inspector Tab | Fix `renderInspectorQuestions` crash to load question chips and previews cleanly | M1 | Frontend Survey |
| 4 | Lesson Summary Quiz Launch | Fix `startQuizAction` undefined error on `#btn-sum-start-quiz` | M1 | Frontend Survey |
| 5 | URL Parameter Deep-Linking | Ensure `preferredExamCode` from URL parameters takes precedence over default | M1 | Frontend Survey |
| 6 | GAS Iframe Sandbox Shielding | Resilient `safeStorage` helper wrapping `localStorage` to avoid `SecurityError` | M1 | Frontend Survey |
| 7 | Zero Dead Buttons & Errors | All 51 static controls, dynamic cards, and tabs execute with 0 console errors | M1 | ORIGINAL_REQUEST §R2 |
| 8 | Unicode NFKC Normalization | Normalize 50 Arabic Shadda/Haraka characters in `Code.gs` and 2 lines in `Index.html` | M2 | ORIGINAL_REQUEST §R1 |
| 9 | Answer Normalization Engine | Update `normalizeAnswer_` to explicitly invoke `.normalize('NFKC')` and letter folding | M2 | Backend Survey |
| 10 | Arabic Header Resilience | Support both Arabic and English column headers in Sheets to prevent index misalignment | M2 | Backend Survey |
| 11 | Non-Destructive Auto-Healing | Protect custom teacher questions from `clearContents()` in `ensureDatabaseUpToDate_` | M2 | Backend Survey |
| 12 | Complete 28-Exam Database Catalog | Ensure all 28 exams (25 curriculum + 3 foundational) are present and registered in `Exams.csv` | M2 | Testing Survey |
| 13 | Historical Submissions Protection | Guarantee `Submissions` table is never cleared, altered, or seeded with demo data | M3 | ORIGINAL_REQUEST §R3 |
| 14 | Bidirectional Sheets Sync | Validate schema auto-healing for missing columns (`Week`, `Difficulty`, `Exam Type`, etc.) | M3 | ORIGINAL_REQUEST §R3 |
| 15 | Grading & Study Plan Advancement | Validate score calculation, rating assignment, review JSON, and marking `Completed` | M3 | ORIGINAL_REQUEST §R2, R3 |
| 16 | Attempt Limits & Retake Approval | Enforce `MAX_ATTEMPTS = 2`, retake request logging, and admin approval unlocking | M3 | Backend Survey |
| 17 | Concept Refreshers & Video Modals | Instant population of concept briefings, golden rules, and video modals for all subjects | M3 | ORIGINAL_REQUEST §R2 |
| 18 | 4-Tier E2E Test Suite (Tiers 1-4) | Comprehensive opaque-box test suite: 25 Tier 1, 20 Tier 2, 4 Tier 3, 2 Tier 4 tests | M4 (Phase 1) | ORIGINAL_REQUEST §R1-R3 |
| 19 | Adversarial Coverage Hardening | White-box stress-testing, oracle fuzzing, and edge-case hardening (Tier 5) | M4 (Phase 2) | Dual Track Requirement |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Frontend Remediation & Sandbox Shielding | Fix Question Bank inspector tab crash, lesson summary start button, URL deep-linking, safeStorage wrapper, and verify <50ms DOM latency and 0 console errors | none | DONE |
| M2 | Backend NFKC Normalization & Data Catalog Sync | Normalize Arabic Shadda/Haraka to NFKC in Code.gs and Index.html; update normalizeAnswer_ with NFKC + letter folding; make header resolution bilingual; add foundational exams to Exams.csv; protect custom questions | none | DONE |
| M3 | Database Integrity, Grading & Study Plan Sync | Validate bidirectional sync, schema auto-healing, historical submission safety, session timer locks, retake lifecycle, and study plan auto-completion | M1, M2 | DONE |
| M4 | 100% E2E Test Suite Pass & Adversarial Hardening | Phase 1: Pass 100% of Tiers 1-4 E2E tests once TEST_READY.md is published. Phase 2: Adversarial coverage hardening (Tier 5) with Challenger -> Worker -> Reviewer loop | M3, E2E-Track | PARTIAL (Phase 1 DONE: 51/51; Phase 2 pending) |

## E2E Testing Track (Parallel)
| # | Name | Scope | Output | Status |
|---|------|-------|--------|--------|
| T-E2E | 4-Tier E2E Test Suite Creation | Build RPC mock bridge + Tier 1 (25 tests), Tier 2 (20 tests), Tier 3 (4 scenarios), Tier 4 (2 scenarios) | `TEST_INFRA.md`, `TEST_READY.md` | DONE |

## Interface Contracts
### Client ↔ Server RPC (`google.script.run`)
- `getStudentAvailableExams(studentKey)` -> `{ success, exams: [{ code, title, grade, subject, count, duration, type, period }], driveVideos }`
- `getTodayMission(studentKey)` -> `{ success, mission: { planId, week, day, dateTitle, subject, lesson, skills, questionsCount, examCode } }`
- `getExamData(examCode, studentName)` -> `{ success, sessionKey, sessionId, exam, questions: [{ id, text, type, options, points }], remainingSeconds, attempt }` (strictly NO `correctAnswer` or `explanation`)
- `submitExamAnswers({ sessionKey, examCode, studentName, answers: { [qId]: answer } })` -> `{ success, alreadySubmitted, earnedScore, totalScore, percentage, rating, durationSpent, review, submittedAt, sessionId }`
- `getStudentExamStatus(studentName, examCode)` -> `{ success, attempts, maxAttempts, canAttempt, retake }`
- `requestExamRetake(payload)` / `approveRetakeRequest(id, adminToken)` / `rejectRetakeRequest(id, adminToken)`
- `verifyGatewayPin(pin)` / `verifyAdminPin(pin)` -> `{ success, token }` (SHA-256 salted hash, token cached ≤30 min)
- `getAdminDashboardData(adminToken)` -> `{ success, sheetUrl, submissions, exams, allQuestions, retakeRequests, studyPlan, driveVideos, driveFolderId }`
- `createWeeklyExam(payload, adminToken)` / `createMonthlyExam(payload, adminToken)` / `createMistakesReviewExam(payload, adminToken)` -> `{ success, examCode, studentUrl, message }`; creation is idempotent and refused when the target bank slice is empty.
- `syncGoogleDriveVideos(folderRef, adminToken)` / `syncColigoOnline(force, adminToken)` / `setupColigoAutoSyncTrigger(adminToken)`
- `getColigoHubData()` / `recordHomeworkStatus(studentName, subject, done)`

### Internal helpers
- `markStudyPlanProgress_(studentName, examCode)` — advances exactly one matching `Study_Plan` row to `Completed` after a successful submission (never fails the submission).
- `loadBankQuestionsByPeriod_(grade, subject, period)` — serves generated weekly/monthly exams from the `Question_Bank` period slice.
- `getSheetHeaderMap_(sheet)` / `canonicalHeader_(header)` — resolve Arabic header aliases to canonical English keys; `ensureSheetHeaders_` treats an alias as the canonical column and never appends duplicates.

## Code Layout
- `Code.gs`: Google Apps Script server backend (92 functions)
- `Index.html`: portal shell, screens and modals; pulls the four templates via `include()`
- `Styles.html`, `HubData.js.html`, `QuizApp.js.html`, `Portal.js.html`: extracted frontend modules
- `Index.bundle.html`: fully resolved single-file build (also copied to `android/app/src/main/assets/www/index.html`)
- `Question_Bank.csv`: Source question items and pedagogical explanations
- `Exams.csv`: Exam definitions and schedule
- `tests/`: Node VM server/unit tests (`server.test.js` is the fake-Sheets harness; 43 tests across 5 files)
- `tests/e2e/`: Playwright E2E suites (Tiers 1-4, 51 scenarios)
- `test_ui_buttons.py`: 51 static button audit
