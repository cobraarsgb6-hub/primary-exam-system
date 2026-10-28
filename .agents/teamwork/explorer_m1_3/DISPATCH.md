# Dispatch Instructions — Explorer M1-3 (NFKC & Latency Verification)

## Mission
Investigate Unicode NFKC diacritic normalization in `Index.html` (lines 2053, 2271), verify DOM rendering transition latency (<50ms requirement), and audit all 51 UI controls for dead buttons.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Project Scope
Path: C:\Users\co0ob\Projects\primary-exam-system\PROJECT.md
Frontend Survey Findings: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_frontend\handoff.md

## Scope Boundaries
- Focus on `Index.html` Unicode normalization, DOM latency, and button verification.
- Formulate exact before/after code blocks for:
  1. Arabic combining mark NFKC reordering on lines 2053 and 2271.
  2. Transition latency verification commands (`test_transitions.py`).
  3. Interactive button responsiveness commands (`test_ui_buttons.py`).
- Strictly read-only on codebase. Write handoff to `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_3\handoff.md`.


## 2026-10-25T15:59:38Z
You are Explorer M1-3 for Milestone 1 (Frontend Defect Remediation).
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_3
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_3\DISPATCH.md
Authoritative request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
PROJECT plan: C:\Users\co0ob\Projects\primary-exam-system\PROJECT.md

1. View ORIGINAL_REQUEST.md and your DISPATCH.md.
2. Initialize progress.md in your working directory.
3. Investigate Index.html Arabic Shadda/Haraka combining marks on lines 2053 and 2271 for NFKC normalization.
4. Verify DOM screen transition latency benchmark scripts and all 51 UI button handlers.
5. Strictly read-only on codebase. Write your handoff report to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_3\handoff.md.
6. When done, notify parent via send_message.
