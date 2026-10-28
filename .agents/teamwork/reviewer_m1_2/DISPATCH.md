# Dispatch Instructions — Reviewer M1-2

## Mission
Independently review the Milestone 1 frontend deliverables with emphasis on AST compliance, HTML5 nesting, transition latency (<50ms), and 4-tier E2E suite execution.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Worker Handoff
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\handoff.md

## Scope & Verification
- Perform AST and strict HTML5 DOM validation on `Index.html`:
  * Confirm 0 unclosed tags, 0 orphaned tags, no scripts outside `<html>`.
  * Validate Node.js AST compilation via `node --check`.
- Execute verification benchmarks and tests:
  * `python test_transitions.py`
  * `python test_ui_buttons.py`
  * `python test_render_all.py`
  * `python test_e2e_quiz.py`
  * `python tests/e2e/run_all_e2e.py`
- Write your review handoff report to: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\reviewer_m1_2\handoff.md`.
- In your report and completion message, provide a clear, unambiguous verdict: **APPROVE** or **REQUEST_CHANGES**.


## 2026-10-25T16:25:25Z
You are Reviewer M1-2 for Milestone 1.
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\reviewer_m1_2
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\reviewer_m1_2\DISPATCH.md
Authoritative request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
Worker M1 handoff: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\handoff.md

1. View ORIGINAL_REQUEST.md, DISPATCH.md, and worker_m1/handoff.md.
2. Initialize progress.md in your working directory.
3. Perform strict HTML5 DOM and Node AST verification on Index.html.
4. Run python test_transitions.py, python test_ui_buttons.py, python test_e2e_quiz.py, and python tests/e2e/run_all_e2e.py.
5. Write your handoff report to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\reviewer_m1_2\handoff.md with a clear verdict: APPROVE or REQUEST_CHANGES.
6. Notify parent via send_message.
