# Dispatch Instructions — Explorer Survey Testing & Verification

## Mission
Survey the test infrastructure, test suites, verification harnesses, and compliance tools of the primary-exam-system.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Scope Boundaries
- Focus: All test files, runner scripts, package.json, lint configurations, and verification scripts in the workspace.
- Investigate:
  1. Existing test suites (unit tests, integration tests, E2E tests).
  2. Tools available for AST syntax validation (Node.js, Babel/Acorn/htmlparser2, etc.), HTML validation, and GAS mock environments.
  3. Coverage of all 28 exams and study plan items.
  4. Feasibility of automated E2E testing (headless browser, DOM simulation, RPC mocking, latency benchmarking).
  5. Requirements for setting up the 4-tier E2E testing track (Tier 1 Feature Coverage >= 5 per feature, Tier 2 Boundary & Corner >= 5, Tier 3 Cross-Feature Combinations, Tier 4 Real-World Application Scenarios).
- Read-only: DO NOT modify any code.
- Write your findings to: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_testing\handoff.md`.

## Handoff Requirements
Include:
- Inventory of existing tests and runners.
- Feasibility analysis for automated testing and verification tools in this environment.
- Feature coverage mapping against user requirements R1, R2, R3.
- Test architecture recommendations for the E2E Testing Track.
