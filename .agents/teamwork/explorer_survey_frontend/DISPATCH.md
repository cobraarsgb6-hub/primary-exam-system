# Dispatch Instructions — Explorer Survey Frontend

## Mission
Survey the frontend architecture, DOM structure, student portals, and user interactivity of the primary-exam-system.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Scope Boundaries
- Focus: `Index.html` and any related client-side assets/scripts.
- Investigate:
  1. Full HTML5 structure, tag well-formedness, nesting, script tags placement (zero orphaned tags, no scripts outside <html>).
  2. Student assessment gateways (Ali G5, Mostafa G6), DOM screen transitions (<50ms).
  3. Daily missions, weekly milestone exams, cumulative exam generator, parent analytics dashboard, video learning modals.
  4. Concept refresher modals/cards for each subject.
  5. Event listeners, memory leaks, dead buttons, console errors, offline/GAS client-side RPC (`google.script.run`) wrappers and mocks.
- Read-only: DO NOT modify any code.
- Write your findings to: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_frontend\handoff.md`.

## Handoff Requirements
Include:
- Complete inventory of UI components, modals, screens, and student flows.
- Detailed HTML/CSS/JS structural observations and defect list.
- Assessment of performance (transition latency, DOM paint overhead).
- Recommendations for milestones and remediation.


## 2026-10-25T15:38:14Z
From: b60602f6-9563-4ac1-9709-5890290e1ced
Content:
You are the Frontend Survey Explorer for the primary-exam-system.
Your working directory is: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_frontend
Your dispatch instructions are at: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_frontend\DISPATCH.md
The authoritative user request is at: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md

Follow these instructions strictly:
1. First, view/read C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md and your DISPATCH.md.
2. Initialize your progress.md in your working directory to signal liveness.
3. Investigate Index.html and any client-side assets/scripts. Examine DOM nesting, HTML5 well-formedness, script tags placement, portals (Ali G5, Mostafa G6), screens, modals, transition speed (<50ms requirement), daily missions, weekly milestone exams, cumulative generator, parent analytics, and dead buttons/event listeners.
4. You are strictly read-only on the codebase. Do not modify source code.
5. Write your comprehensive analysis and findings to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_frontend\handoff.md.
6. When complete, send a message to your parent with a concise summary and confirmation of handoff.md path.
