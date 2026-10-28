# Dispatch Instructions — Worker M1 (Frontend Defect Remediation)

## Mission
Implement the full Milestone 1 frontend remediations on `Index.html`, apply tests updates (`test_transitions.py`, `test_ui_buttons.py`), and verify all AST and browser tests pass with 0 errors.

## Authoritative User Request
Path: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
(You MUST view/read this file first!)

## Explorer Findings to Implement
1. M1-1 Report: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_1\handoff.md`
   - Fix 1: Question Bank Inspector tab crash (`Index.html:3684`) -> `setupInspectorChips(activeAdminStudent)`
   - Fix 2: Start Quiz button in Lesson Summary Modal (`Index.html:2386-2398`) -> `selectStudentExam(sum.relatedExamId); promptStartConfirmation();`
   - Defensive null-safety enhancement in `setupInspectorChips` (`Index.html:3605-3611`)
2. M1-2 Report: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_2\handoff.md`
   - Fix 3: URL Parameter Deep-Linking Precedence & Synchronous Card Activation (`Index.html:2787-2801`)
   - Fix 4: Resilient `safeStorage` Module Definition & In-Memory Fallback (`Index.html:2700`)
   - Replacement of unshielded `localStorage` calls with `safeStorage` in `saveProgress`, `loadProgress`, `clearProgress`, `checkExamStatus`, `onSubmissionSuccess`, and `clearDeviceLocks`
   - Expose `window.safeStorage = safeStorage;` in global exports
3. M1-3 Report: `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\explorer_m1_3\handoff.md`
   - Normalize Arabic Shadda/Haraka combining marks on lines 2071 and 2289 to strict Unicode NFKC canonical order
   - Update `test_transitions.py` and `test_ui_buttons.py` with modernized verification harnesses

## Write Ownership
You EXCLUSIVELY own:
- `C:\Users\co0ob\Projects\primary-exam-system\Index.html`
- `C:\Users\co0ob\Projects\primary-exam-system\test_transitions.py`
- `C:\Users\co0ob\Projects\primary-exam-system\test_ui_buttons.py`
DO NOT modify `Code.gs` or files in `tests/e2e/`.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Verification Requirements
Worker MUST run and verify:
1. Node.js AST syntax check: `node --check` on `<script>` block in `Index.html` (exit code 0)
2. `python test_transitions.py` (all transitions <50ms)
3. `python test_ui_buttons.py` (51/51 buttons pass with 0 errors)
4. `python test_render_all.py`
5. `python test_e2e_quiz.py`
6. `npm test` and `node --test tests/cumulative.test.js`

Document all commands and verbatim terminal outputs in `C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\handoff.md`.


## 2026-10-25T16:15:21Z
[Message] timestamp=2026-10-25T16:15:21Z sender=b60602f6-9563-4ac1-9709-5890290e1ced priority=MESSAGE_PRIORITY_HIGH content=You are Worker M1 (Frontend Implementer) for Milestone 1.
Your working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1
Your dispatch instructions: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m1\DISPATCH.md
Authoritative user request: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\ORIGINAL_REQUEST.md
PROJECT plan: C:\Users\co0ob\Projects\primary-exam-system\PROJECT.md
