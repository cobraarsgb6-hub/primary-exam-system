# Original User Request

## 2026-10-25T15:35:22Z

Independent multi-agent architectural review, stress-testing, and complete end-to-end audit of the primary-exam-system (Google Apps Script backend and HTML/JS frontend) to ensure 100% zero-defect reliability across all student portals, exams, analytics, and data sync.

Working directory: C:\Users\co0ob\Projects\primary-exam-system
Integrity mode: development

## Requirements

### R1. Complete Forensic Codebase Audit
Audit all files (`Code.gs`, `Index.html`, `Question_Bank.csv`, `Exams.csv`, test suites) for AST syntax validity, DOM tree nesting, event handling, memory leaks, and Google Apps Script preprocessor/Caja sandbox constraints.

### R2. End-to-End System Reliability & Defect Isolation
Verify that all student assessment gateways (Ali G5, Mostafa G6), daily missions, weekly milestone exams, cumulative generators, parent analytics dashboard, and video learning modals execute flawlessly with zero console errors or dead buttons.

### R3. Autonomous Verification & Self-Healing Database Integrity
Validate the bidirectional synchronization between Google Apps Script and Google Sheets (`Question_Bank`, `Exams`, `Study_Plan`, `Submissions`), ensuring schema migrations auto-heal without touching historical student submissions.

## Acceptance Criteria

### Architectural Integrity & Syntax
- [ ] `Index.html` is 100% well-formed HTML5 with zero orphaned tags, no scripts outside `<html>`, and clean AST parsing under Node.js.
- [ ] `Code.gs` contains zero hardcoded JWT secrets, adheres to strict Unicode NFKC normalization, and compiles without warnings.

### Functional Interactivity & User Experience
- [ ] Ali and Mostafa portals transition in <50ms with direct DOM screen rendering.
- [ ] All 28 exams and study plan items are accessible, with concept refreshers populating instantly for every subject.
- [ ] Submission workflow successfully records student answers, scores points accurately, and marks corresponding study plan entries as `Completed`.
