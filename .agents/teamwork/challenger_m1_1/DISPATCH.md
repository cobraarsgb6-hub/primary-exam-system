# Dispatch Instructions — Challenger M1-1 (Storage & Navigation Adversary)

## Mission
Adversarially challenge and stress-test the Milestone 1 frontend implementation (`Index.html`). Write test harnesses and edge-case probes to empirically verify correctness and fault resilience.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Worker Handoff
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\handoff.md

## Adversarial Focus
1. **`safeStorage` Resilience Under Attack**:
   - Inject hostile `DOMException` ('SecurityError', 'QuotaExceededError', 'InvalidAccessError') on `window.localStorage`.
   - Test `safeStorage.setItem`, `getItem`, `removeItem`, `keys()` with extreme keys, non-string values, large payloads (1MB+), and null/undefined values.
   - Verify that student quiz progress saving/loading and parent device lock resets NEVER throw unhandled exceptions.
2. **Deep-Linking Edge Cases**:
   - Test nonexistent student keys, invalid exam codes, XSS injection attempts in URL parameters (`?student=<script>...&exam=INVALID`), and verify graceful fallback to default exam.
3. Write your empirical challenge report to: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\challenger_m1_1\handoff.md`.
4. State your verdict clearly: **APPROVE** or **REQUEST_CHANGES**.


## 2026-10-25T16:25:25Z
You are Challenger M1-1 for Milestone 1.
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\challenger_m1_1
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\challenger_m1_1\DISPATCH.md
Authoritative request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
Worker M1 handoff: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\handoff.md

1. View ORIGINAL_REQUEST.md, DISPATCH.md, and worker_m1/handoff.md.
2. Initialize progress.md in your working directory.
3. Adversarially probe safeStorage under injected DOMException SecurityError, QuotaExceededError, and hostile key/value payloads.
4. Test URL deep-linking with boundary and malicious query parameters.
5. Write your handoff report to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\challenger_m1_1\handoff.md with a clear verdict: APPROVE or REQUEST_CHANGES.
6. Notify parent via send_message.
