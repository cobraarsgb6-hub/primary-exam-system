# Dispatch Instructions — E2E Test Writer

## Mission
Design and implement the complete 4-Tier Opaque-Box E2E Test Suite for `primary-exam-system` per the project Dual Track specifications.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Survey Reference
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_testing\handoff.md
(Read Section 5 for the exact 4-tier specifications and RPC bridge requirements!)

## Scope Boundaries
- You are responsible for the E2E Testing Track.
- DO NOT modify `Code.gs` or `Index.html` (implementation files).
- You OWN and write exclusively:
  1. `C:\Users\co0ob\Projects\primary-exam-system\TEST_INFRA.md` (at project root)
  2. `C:\Users\co0ob\Projects\primary-exam-system\tests\e2e\` (test scripts and runners)
  3. `C:\Users\co0ob\Projects\primary-exam-system\TEST_READY.md` (upon completion)

## Deliverables
1. **`TEST_INFRA.md`**: Follow template in PROJECT.md and testing survey handoff.
2. **RPC Mock Bridge (`tests/e2e/mock_bridge.js`)**: An injectable script for `page.add_init_script` providing high-fidelity `window.google.script.run` mocks for all 16 endpoints with authentic data matching the 28 exams, question bank, and study plan.
3. **Tier 1 — Core Feature Coverage (>=25 tests)**:
   - Gateway & portal isolation (5 tests)
   - Daily missions & concept refreshers (5 tests)
   - 28-Exam catalog & quiz engine (5 tests)
   - Assessment submission & scoring engine (5 tests)
   - Parent analytics & administration (5 tests)
4. **Tier 2 — Boundary & Corner Cases (>=20 tests)**:
   - Timeouts & session expirations (5 tests)
   - Attempt limits & concurrency (5 tests)
   - Input sanitization & Arabic diacritics (5 tests)
   - Data & schema anomalies (5 tests)
5. **Tier 3 — Cross-Feature Combinations (>=4 scenarios)**:
   - Full student remediation loop (Fail -> Retake -> Approve -> Pass -> Plan update)
   - Dynamic passage pool rotation
   - Multi-week cumulative synthesis
   - Progress restoration on refresh
6. **Tier 4 — Real-World Application Scenarios (>=2 scenarios)**:
   - Dual-student morning routine on shared browser
   - Comprehensive weekend parent audit
7. **Master Runner (`tests/e2e/run_all_e2e.py`)**: Runs all 4 tiers, outputs structured pass/fail metrics.
8. **`TEST_READY.md`**: Publish at project root summarizing all tiers, test counts, commands, and feature checklist.

## Handoff Requirements
Write `handoff.md` in your working directory with observation, execution commands, and verification proof.


## 2026-10-25T15:59:38Z
You are the E2E Test Writer for the primary-exam-system.
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\test_writer_e2e
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\test_writer_e2e\DISPATCH.md
Authoritative request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
PROJECT plan: C:\Users\co0ob\Projects\primary-exam-system\PROJECT.md
Testing survey reference: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_survey_testing\handoff.md

1. View ORIGINAL_REQUEST.md and your DISPATCH.md.
2. Initialize progress.md in your working directory.
3. Write C:\Users\co0ob\Projects\primary-exam-system\TEST_INFRA.md at project root.
4. Build the complete 4-tier E2E test suite under C:\Users\co0ob\Projects\primary-exam-system\tests\e2e\ including mock_bridge.js and tests for Tiers 1-4.
5. Execute the test runner to verify all tests pass.
6. Create C:\Users\co0ob\Projects\primary-exam-system\TEST_READY.md upon complete passing.
7. Write your handoff report to C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\test_writer_e2e\handoff.md and notify parent via send_message.
