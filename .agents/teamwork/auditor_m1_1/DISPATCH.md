# Dispatch Instructions — Forensic Auditor M1

## Mission
Conduct an independent forensic integrity audit of Milestone 1 work products (`Index.html`, test harnesses). Verify that the code implements genuine functionality without shortcuts, facades, dummy mocks, or hardcoded strings designed to fake test passage.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Worker Handoff
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\handoff.md

## Forensic Integrity Checks
1. **No Facades or Hardcoded Bypasses**:
   - Inspect `Index.html`: Ensure `safeStorage` genuinely stores and retrieves data in memory when `localStorage` is blocked, rather than returning hardcoded dummy strings.
   - Ensure `setupInspectorChips` actually binds and renders authentic student exam chips and calls `renderInspectQuestions`.
   - Ensure `#btn-sum-start-quiz` genuinely invokes `selectStudentExam` and `promptStartConfirmation`.
2. **Secrets & Security Check**:
   - Verify zero hardcoded JWT tokens, passwords, or credentials.
   - Verify no unescaped user input in storage or DOM innerHTML.
3. **HTML5 Well-Formedness & AST**:
   - Verify zero orphaned tags, zero scripts outside `<html>`, exactly one style tag in `<head>`, and clean AST syntax.
4. **Unicode NFKC Canonical Verification**:
   - Verify that Arabic strings in `Index.html` conform to strict Unicode NFKC canonical combining sequences.
5. Write your comprehensive forensic audit report to: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\auditor_m1_1\handoff.md`.
6. State your verdict clearly: **CLEAN** or **INTEGRITY VIOLATION**.


## 2026-10-25T16:25:25Z
You are Forensic Auditor M1 for Milestone 1.
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\auditor_m1_1
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\auditor_m1_1\DISPATCH.md
Authoritative request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
Worker M1 handoff: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\handoff.md

1. View ORIGINAL_REQUEST.md, DISPATCH.md, and worker_m1/handoff.md.
2. Initialize progress.md in your working directory.
3. Conduct forensic checks: zero dummy implementations, zero hardcoded test outputs, zero hardcoded JWT tokens or secrets, strict HTML5 well-formedness (0 orphaned tags, no scripts outside <html>), and strict Unicode NFKC canonical normalization.
4. Write your handoff report to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\auditor_m1_1\handoff.md with a clear binary verdict: CLEAN or INTEGRITY VIOLATION.
5. Notify parent via send_message.
