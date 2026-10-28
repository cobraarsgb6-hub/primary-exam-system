# Dispatch Instructions — Challenger M1-2 (UI Race & Concurrency Adversary)

## Mission
Adversarially challenge and stress-test the Milestone 1 frontend interface (`Index.html`) for concurrency races, event listener leaks, rapid clicking, and modal thrashing.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Worker Handoff
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\handoff.md

## Adversarial Focus
1. **Button Fuzzing & Rapid Double-Clicks**:
   - Rapid-fire clicking on `#btn-gateway-ali`, `#btn-gateway-mostafa`, and `#btn-launch-today` in bursts of 50ms.
   - Rapidly open and close `#lesson-summary-modal` and `#start-modal` 20 times in succession.
   - Click `#btn-sum-start-quiz` with undefined and mismatched `relatedExamId` properties.
2. **Tab Thrashing in Parent Portal**:
   - Rapidly switch parent tabs (`history` -> `analytics` -> `plan` -> `inspector` -> `operations` -> `inspector`) with alternating students (Ali / Mostafa).
   - Ensure 0 unhandled console errors or DOM orphaned elements.
3. Write your empirical challenge report to: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\challenger_m1_2\handoff.md`.
4. State your verdict clearly: **APPROVE** or **REQUEST_CHANGES**.


## 2026-10-25T16:25:25Z
You are Challenger M1-2 for Milestone 1.
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\challenger_m1_2
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\challenger_m1_2\DISPATCH.md
Authoritative request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
Worker M1 handoff: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\handoff.md

1. View ORIGINAL_REQUEST.md, DISPATCH.md, and worker_m1/handoff.md.
2. Initialize progress.md in your working directory.
3. Adversarially test all 51 UI buttons with burst clicks, double-submits, rapid screen switching, and modal thrashing in Playwright.
4. Verify 0 console errors or detached elements.
5. Write your handoff report to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\challenger_m1_2\handoff.md with a clear verdict: APPROVE or REQUEST_CHANGES.
6. Notify parent via send_message.
