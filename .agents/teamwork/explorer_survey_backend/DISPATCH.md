# Dispatch Instructions — Explorer Survey Backend

## Mission
Survey the Google Apps Script backend, data models, and database synchronization of the primary-exam-system.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Scope Boundaries
- Focus: `Code.gs`, `Question_Bank.csv`, `Exams.csv`, and any other backend/data files.
- Investigate:
  1. Complete AST syntax and GAS preprocessor/Caja sandbox constraints.
  2. Unicode NFKC normalization and absence of hardcoded secrets/JWT.
  3. Google Sheets data structures: Question_Bank, Exams, Study_Plan, Submissions.
  4. Bidirectional sync, auto-healing schema migrations, historical data safety.
  5. Submission processing, grading logic, point calculation, study plan marking.
- Read-only: DO NOT modify any code.
- Write your findings to: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_backend\handoff.md`.

## Handoff Requirements
Include:
- Inventory of backend functions, routes, and data flows.
- Detailed code quality, syntax, security, and architectural observations.
- List of features, constraints, edge cases, and existing defects.
- Recommendations for milestones and remediation.

## 2026-10-25T15:38:14Z
From: b60602f6-9563-4ac1-9709-5890290e1ced
Content:
You are the Backend Survey Explorer for the primary-exam-system.
Your working directory is: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_backend
Your dispatch instructions are at: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_backend\DISPATCH.md
The authoritative user request is at: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md

Follow these instructions strictly:
1. First, view/read C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md and your DISPATCH.md.
2. Initialize your progress.md in your working directory to signal liveness.
3. Investigate Code.gs, Question_Bank.csv, Exams.csv, and related backend files. Analyze functions, data structures, Google Sheets sync, schema migration/auto-healing, grading logic, and Caja/GAS preprocessor constraints.
4. You are strictly read-only on the codebase. Do not modify source code.
5. Write your comprehensive analysis and findings to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_backend\handoff.md.
6. When complete, send a message to your parent with a concise summary and confirmation of handoff.md path.
