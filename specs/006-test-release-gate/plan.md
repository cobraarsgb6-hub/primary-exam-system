# Architectural Implementation Plan: P5 Test Suite Harmonization & Release Gate

## 1. Architectural Strategy
1. **Mock Bridge & PIN Gateway Resolution:**
   - Extend `tests/e2e/mock_bridge.js` to return genuine tokens (`STUDENT_TOK_MOS_VALID`, `STUDENT_TOK_ALI_VALID`, `ADMIN_TOK_MOCK_VALID`) for simulated gateway PIN requests.
   - Inject `window.__testBypassPin = true;` in `tests/e2e/harness.py` for synchronous component/flow testing while preserving real interactive dialog resolution in `tests/test_multisubject_navigation.py`.
2. **Quiz App & Portal Runtime Safeguards:**
   - In `Portal.js.html`, declare `currentStudentToken` and `currentStudentTokenKey` globally to prevent `ReferenceError`.
   - In `QuizApp.js.html`, update `loadAndStartQuiz` to assign `activeExamCode = code;` dynamically so generated submissions correctly advance corresponding Study Plan records.
   - Cleanly guard `loadStudentColigoMaterials` against undefined calls.
3. **Continuous Integration Gate:**
   - Update `.github/workflows/deploy-pages.yml` with a pre-flight test job running on Node.js 20.
   - Verify bundle consistency (`bundle.py`).
4. **Verification & Ledger Documentation:**
   - Run all suites to 100% PASS.
   - Document results in `CURRENT_STATUS_AR.md`.
