# Dispatch Instructions — Worker M2 (Backend Normalization & Catalog Sync)

## Mission
Implement Milestone 2 on `Code.gs` and `Exams.csv`: Arabic Unicode NFKC normalization, bilingual header resolution, custom question protection, and 28-exam catalog synchronization.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Survey References
1. Backend Survey Report: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_backend\handoff.md`
2. Testing Survey Report: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_testing\handoff.md`

## Scope of Changes
1. **Unicode NFKC Normalization**:
   - Normalize the 50 Arabic combining mark characters in `Code.gs` (lines 160, 175, 176, 1507, 1508, 1528, 3857, 4118) to strict Unicode NFKC canonical order (`code.normalize('NFKC')`).
   - In `normalizeAnswer_` (lines 376–383), explicitly invoke `.normalize('NFKC')` and letter variant folding (`[أإآ] -> ا`, `ة -> ه`, `ى -> ي`) before diacritic stripping.
2. **Bilingual Header Resolution**:
   - Update `headerIndex_` in `Code.gs` to support both Arabic and English column header aliases (e.g. `معرف السؤال` and `Question ID`, `كود الامتحان` and `Exam Code`, etc.) so that reordered columns in Google Sheets with Arabic headers resolve correctly without relying on fragile fixed-index fallbacks.
3. **Protect Custom Teacher Questions in Auto-Healing**:
   - In `ensureDatabaseUpToDate_` and `migrateAndSyncDatabase()` (lines 4086–4166), ensure existing custom questions or exams are preserved or non-destructively merged rather than unconditionally wiped with `clearContents()`.
4. **Complete 28-Exam Database Catalog**:
   - In `Exams.csv`, ensure all 28 exams are defined by adding the 3 foundational exams:
     * `EX_Y5_ENG_ADV01` (Ali Year 5 Adverbials Foundational Exam)
     * `EX_Y6_ARB_PRIO01` (Mostafa Grade 6 Arabic Foundational Diagnostic)
     * `EX_Y6_ENG_FANTASY01` (Mostafa Grade 6 English Fantasy Reading Exam)

## Write Ownership
You EXCLUSIVELY own:
- `C:\Users\co0ob\Projects\primary-exam-system\Code.gs`
- `C:\Users\co0ob\Projects\primary-exam-system\Exams.csv`
DO NOT modify `Index.html` or `tests/e2e/`.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Verification Requirements
Worker MUST execute and verify:
1. `node -e "const fs = require('fs'); const code = fs.readFileSync('Code.gs', 'utf8'); console.log('NFKC:', code === code.normalize('NFKC'));"` -> returns `true`.
2. AST syntax check: `node -e "const fs = require('fs'); new Function(fs.readFileSync('Code.gs', 'utf8')); console.log('Syntax OK');"`
3. Unit tests: `npm test` (all 12 tests pass)
4. Cumulative tests: `node --test tests/cumulative.test.js` (pass)
5. 28-Exam verification: `node .agents/teamwork/explorer_survey_testing/test_all_28_exams.js` (all 28 pass)
6. Master E2E runner: `python tests/e2e/run_all_e2e.py` (all 51 pass)

Write handoff report to `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m2\handoff.md`.


## 2026-10-25T16:45:40Z
[Message] timestamp=2026-10-25T16:45:40Z sender=b60602f6-9563-4ac1-9709-5890290e1ced priority=MESSAGE_PRIORITY_HIGH content=You are Worker M2 (Backend Implementer) for Milestone 2.
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m2
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m2\DISPATCH.md
Authoritative request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
PROJECT plan: C:\Users\co0ob\Projects\primary-exam-system\PROJECT.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Instructions:
1. View ORIGINAL_REQUEST.md and your DISPATCH.md.
2. Initialize progress.md in your working directory.
3. Read the Backend Survey report (explorer_survey_backend/handoff.md) and Testing Survey report (explorer_survey_testing/handoff.md).
4. Implement the required changes in Code.gs and Exams.csv.
5. Run all build and test verification commands documented in DISPATCH.md.
6. Write your handoff report to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m2\handoff.md.
7. Notify parent via send_message when complete.
