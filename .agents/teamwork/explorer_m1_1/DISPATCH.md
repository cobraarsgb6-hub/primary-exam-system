# Dispatch Instructions — Explorer M1-1 (Inspector & Modal Fixes)

## Mission
Investigate and design the exact implementation plan for Defect 1 (`renderInspectorQuestions` crash at line 3684) and Defect 2 (`startQuizAction` undefined at line 2392) in `Index.html`.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Project Scope
Path: C:\Users\co0ob\Projects\primary-exam-system\PROJECT.md
Frontend Survey Findings: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_frontend\handoff.md

## Scope Boundaries
- Focus on `Index.html` controls and modals.
- Formulate exact before/after code blocks for:
  1. `Index.html:3684`: `switchParentView('inspector')` -> invoke `setupInspectorChips(activeAdminStudent)`
  2. `Index.html:2392`: `#btn-sum-start-quiz` -> invoke `selectStudentExam(sum.relatedExamId); promptStartConfirmation();`
- Ensure zero syntax/AST errors under `node --check`.
- Strictly read-only on codebase. Write handoff to `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_1\handoff.md`.


## 2026-10-25T15:59:38Z
You are Explorer M1-1 for Milestone 1 (Frontend Defect Remediation).
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_1
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_1\DISPATCH.md
Authoritative request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
PROJECT plan: C:\Users\co0ob\Projects\primary-exam-system\PROJECT.md

1. View ORIGINAL_REQUEST.md and your DISPATCH.md.
2. Initialize progress.md in your working directory.
3. Investigate Index.html at lines 3684 and 2392.
4. Formulate the precise fix strategy and exact code blocks for the Worker.
5. Strictly read-only on codebase. Write your handoff report to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_1\handoff.md.
6. When done, notify parent via send_message.
