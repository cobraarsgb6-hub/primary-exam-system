# Dispatch Instructions — Explorer M1-2 (Deep-Linking & SafeStorage)

## Mission
Investigate and design the exact implementation plan for Defect 3 (URL deep-linking parameter precedence at line 2788) and Defect 4 (unshielded `localStorage` sandbox crashes at lines 2708, 2719, 2913, 3390, 3713) in `Index.html`.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Project Scope
Path: C:\Users\co0ob\Projects\primary-exam-system\PROJECT.md
Frontend Survey Findings: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_frontend\handoff.md

## Scope Boundaries
- Focus on `Index.html` deep-linking and storage resilience.
- Formulate exact before/after code blocks for:
  1. `Index.html:2788`: Prioritizing `preferredExamCode` when valid.
  2. Defining a robust `safeStorage` wrapper object (with try/catch for getItem, setItem, removeItem) to shield against GAS iframe `SecurityError`.
  3. Replacing unshielded `localStorage` calls with `safeStorage`.
- Ensure zero syntax/AST errors.
- Strictly read-only on codebase. Write handoff to `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_2\handoff.md`.


## 2026-10-25T15:59:38Z
Sender: b60602f6-9563-4ac1-9709-5890290e1ced
Message:
You are Explorer M1-2 for Milestone 1 (Frontend Defect Remediation).
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_2
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_2\DISPATCH.md
Authoritative request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
PROJECT plan: C:\Users\co0ob\Projects\primary-exam-system\PROJECT.md

1. View ORIGINAL_REQUEST.md and your DISPATCH.md.
2. Initialize progress.md in your working directory.
3. Investigate Index.html at line 2788 (URL parameter precedence) and unshielded localStorage calls (lines 2708, 2719, 2913, 3390, 3713).
4. Formulate the precise safeStorage implementation and replacement strategy for the Worker.
5. Strictly read-only on codebase. Write your handoff report to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_2\handoff.md.
6. When done, notify parent via send_message.
