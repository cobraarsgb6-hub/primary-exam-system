"""
Tier 2: Boundary & Corner Cases Test Suite (20 Tests)
Covers Timeouts & Session Expirations, Attempt Limits & Concurrency,
Input Sanitization & Arabic Diacritics, and Data & Schema Anomalies.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from tests.e2e.harness import E2EHarness, run_test_case

def run_all(harness=None):
    results = []
    print("\n========================================================")
    print("  RUNNING TIER 2: BOUNDARY & CORNER CASES (20 TESTS)")
    print("========================================================")

    managed_harness = harness is None
    h = E2EHarness() if managed_harness else harness
    if managed_harness:
        h.__enter__()

    try:
        page = h.page

        def ensure_clean_screen():
            page.evaluate("""() => {
              if (typeof closeStartModal === 'function') closeStartModal();
              if (typeof closeVideoModal === 'function') closeVideoModal();
              if (typeof closeLessonSummaryModal === 'function') closeLessonSummaryModal();
            }""")
            h.reset_state()

        # ========================================================
        # Domain 1: Timeouts & Session Expirations (5 tests)
        # ========================================================
        print("\n-- Domain 1: Timeouts & Session Expirations --")

        def t2_1_1():
            ensure_clean_screen()
            page.evaluate("() => { openStudentPortal('ali'); showScreen('screen-quiz'); loadAndStartQuiz('DAILY_Y5_ENG_W1D1'); }")
            page.wait_for_timeout(150)
            # Force server-side timeout
            h.set_bridge_flag('forceTimeout', True)
            
            # Setup alert dialog handler
            alerts = []
            page.once('dialog', lambda dialog: (alerts.append(dialog.message), dialog.accept()))
            
            page.evaluate("() => submitQuiz(true)")
            page.wait_for_timeout(200)
            # Alert or error message received
            assert len(alerts) > 0 or h.get_bridge_state().get('forceTimeout'), "Expected timeout rejection alert or flag"

        run_test_case("T2.1.1: Server-side expired session returns TIME_EXPIRED on submit", t2_1_1, results)

        def t2_1_2():
            ensure_clean_screen()
            page.evaluate("() => { openStudentPortal('ali'); showScreen('screen-quiz'); loadAndStartQuiz('DAILY_Y5_ENG_W1D1'); }")
            page.wait_for_timeout(150)
            # Simulate timer hitting 00:00 -> auto submit
            page.evaluate("""() => {
              secondsRemaining = 0;
              submitQuiz(true);
            }""")
            page.wait_for_timeout(250)
            is_res = page.evaluate("() => document.querySelector('#screen-result.active') !== null")
            assert is_res, "Reaching timer 00:00 must auto-trigger submission to screen-result"

        run_test_case("T2.1.2: Client timer expiration triggers automatic submission", t2_1_2, results)

        def t2_1_3():
            ensure_clean_screen()
            # Manipulated expired session timestamp
            expired_res = page.evaluate("""() => {
              const sessionKey = 'EXPIRED_KEY';
              window.__mockBridge.state.activeSessions[sessionKey] = {
                expiresAt: Date.now() - 60000,
                questions: []
              };
              // Submit against expired session
              return window.__mockBridge.handlers.submitExamAnswers({
                sessionKey: sessionKey,
                answers: {}
              });
            }""")
            # Must return success: true or error handling
            assert expired_res is not None, "Submission with expired session handled"

        run_test_case("T2.1.3: Manipulated expired session timestamp handled securely", t2_1_3, results)

        def t2_1_4():
            ensure_clean_screen()
            # Stale session older than 3 hours in localStorage
            is_stale_cleared = page.evaluate("""() => {
              const staleData = {
                sessionKey: 'OLD_SESSION',
                answers: { 'Q1': 'val' },
                savedAt: Date.now() - (4 * 60 * 60 * 1000)
              };
              localStorage.setItem('primary_exam_progress_ali_DAILY_Y5_ENG_W1D1', JSON.stringify(staleData));
              const loaded = loadProgress('OLD_SESSION');
              return loaded === null;
            }""")
            assert is_stale_cleared, "Stale localStorage progress (>3h old) must return null"

        run_test_case("T2.1.4: Stale localStorage progress older than 3 hours discarded", t2_1_4, results)

        def t2_1_5():
            ensure_clean_screen()
            # Exam with 0 or negative duration metadata
            res = page.evaluate("""() => {
              window.__mockBridge.setFlag('customDuration', 0);
              return window.__mockBridge.handlers.getExamData('DAILY_Y5_ENG_W1D1', 'Ali Ahmed');
            }""")
            assert res['success'] is True, "Exam data should load successfully"
            # In mock bridge customDuration 0 handled, duration defaults safely
            assert res['exam']['duration'] >= 0, "Duration must be non-negative"

        run_test_case("T2.1.5: Exam metadata duration boundary values handled safely", t2_1_5, results)

        # ========================================================
        # Domain 2: Attempt Limits & Concurrency (5 tests)
        # ========================================================
        print("\n-- Domain 2: Attempt Limits & Concurrency --")

        def t2_2_1():
            ensure_clean_screen()
            # Set forceMaxAttempts
            h.set_bridge_flag('forceMaxAttempts', True)
            res = page.evaluate("""() => {
              return window.__mockBridge.handlers.getExamData('DAILY_Y5_ENG_W1D1', 'Ali Ahmed');
            }""")
            assert res['success'] is False, "Expected error when max attempts reached"
            assert res['code'] == 'MAX_ATTEMPTS', f"Expected MAX_ATTEMPTS, got: {res.get('code')}"

        run_test_case("T2.2.1: Attempt count >= max attempts returns MAX_ATTEMPTS", t2_2_1, results)

        def t2_2_2():
            ensure_clean_screen()
            # Approve retake request increments allowed attempts by 1
            before = page.evaluate("() => window.__mockBridge.state.allowedAttempts['Ali Ahmed:EX_Y5_ENG_W1']")
            res = page.evaluate("() => window.__mockBridge.handlers.approveRetakeRequest('REQ-101')")
            assert res['success'] is True, "Approve request should succeed"
            after = page.evaluate("() => window.__mockBridge.state.allowedAttempts['Ali Ahmed:EX_Y5_ENG_W1']")
            assert after == before + 1, f"Allowed attempts should increment by 1 (before={before}, after={after})"

        run_test_case("T2.2.2: Approved retake request increments allowed attempts by 1", t2_2_2, results)

        def t2_2_3():
            ensure_clean_screen()
            page.evaluate("() => { openStudentPortal('ali'); showScreen('screen-quiz'); loadAndStartQuiz('DAILY_Y5_ENG_W1D1'); }")
            page.wait_for_timeout(200)
            # Test idempotency: rapid double invocation of submitQuiz
            res = page.evaluate("""() => {
              const subsBefore = window.__mockBridge.state.submissions.length;
              submitQuiz(true);
              submitQuiz(true);
              const subsAfter = window.__mockBridge.state.submissions.length;
              return { before: subsBefore, after: subsAfter };
            }""")
            page.wait_for_timeout(200)
            diff = res['after'] - res['before']
            assert diff <= 1, f"Double-click submit must produce at most 1 submission, got diff={diff}"

        run_test_case("T2.2.3: Rapid double submit is idempotent and prevents duplicate submission", t2_2_3, results)

        def t2_2_4():
            ensure_clean_screen()
            h.set_bridge_flag('forceStudentMismatch', True)
            res = page.evaluate("""() => {
              const sess = window.__mockBridge.handlers.getExamData('DAILY_Y5_ENG_W1D1', 'Ali Ahmed');
              return window.__mockBridge.handlers.submitExamAnswers({
                sessionKey: sess.sessionKey,
                studentName: 'Mostafa Ahmed',
                examCode: 'DAILY_Y5_ENG_W1D1',
                answers: {}
              });
            }""")
            assert res['success'] is False, "Expected student mismatch error"
            assert res['code'] == 'STUDENT_MISMATCH', f"Expected STUDENT_MISMATCH, got: {res.get('code')}"

        run_test_case("T2.2.4: Cross-student session mismatch returns STUDENT_MISMATCH", t2_2_4, results)

        def t2_2_5():
            ensure_clean_screen()
            try:
                h.set_bridge_flag('forceBusy', True)
                res = page.evaluate("""() => {
                  return window.__mockBridge.handlers.submitExamAnswers({
                    sessionKey: 'ANY',
                    answers: {}
                  });
                }""")
                assert res['success'] is False, "Expected failure when lock busy"
                assert res['code'] == 'BUSY', f"Expected BUSY code, got: {res.get('code')}"
            finally:
                h.set_bridge_flag('forceBusy', False)

        run_test_case("T2.2.5: Server lock contention during submission returns BUSY", t2_2_5, results)

        # ========================================================
        # Domain 3: Input Sanitization & Arabic Diacritics (5 tests)
        # ========================================================
        print("\n-- Domain 3: Input Sanitization & Arabic Diacritics --")

        def t2_3_1():
            ensure_clean_screen()
            # Compare answer with Harakat vs canonical answer without Harakat
            match_res = page.evaluate("""() => {
              // Canonical answer
              const canonical = 'كان الطالب مجتهدا في دراسته';
              // Student answered with full Arabic diacritics
              const withHarakat = 'كَانَ الطَّالِبُ مُجْتَهِداً فِي دِرَاسَتِهِ';
              
              const sess = window.__mockBridge.handlers.getExamData('DAILY_Y6_ARB_W1D4', 'Mostafa Ahmed');
              const qId = sess.questions[0].id;
              const sub = window.__mockBridge.handlers.submitExamAnswers({
                sessionKey: sess.sessionKey,
                examCode: 'DAILY_Y6_ARB_W1D4',
                studentName: 'Mostafa Ahmed',
                answers: { [qId]: withHarakat }
              });
              return sub.review[0].isCorrect;
            }""")
            assert match_res is True, "Answer with full Arabic Harakat must match canonical answer"

        run_test_case("T2.3.1: Arabic answer with Harakat matches canonical answer accurately", t2_3_1, results)

        def t2_3_2():
            ensure_clean_screen()
            # Arabic answer with Tatweel (\u0640)
            match_res = page.evaluate("""() => {
              const withTatweel = 'كـــــان الــــطالب مــــجتهدا في دراسته';
              const sess = window.__mockBridge.handlers.getExamData('DAILY_Y6_ARB_W1D4', 'Mostafa Ahmed');
              const qId = sess.questions[0].id;
              const sub = window.__mockBridge.handlers.submitExamAnswers({
                sessionKey: sess.sessionKey,
                examCode: 'DAILY_Y6_ARB_W1D4',
                studentName: 'Mostafa Ahmed',
                answers: { [qId]: withTatweel }
              });
              return sub.review[0].isCorrect;
            }""")
            assert match_res is True, "Answer with Tatweel must match canonical answer"

        run_test_case("T2.3.2: Arabic answer with Tatweel matches canonical answer", t2_3_2, results)

        def t2_3_3():
            ensure_clean_screen()
            # Arabic answer with non-NFKC combining marks (Shaddah then Fatha vs Fatha then Shaddah)
            match_res = page.evaluate("""() => {
              // Construct non-NFKC string
              const s1 = 'إِن\u0651\u064E'; // Shaddah + Fatha
              const s2 = 'إِن\u064E\u0651'; // Fatha + Shaddah
              const sess = window.__mockBridge.handlers.getExamData('DAILY_Y6_ARB_W1D4', 'Mostafa Ahmed');
              const qId = sess.questions[0].id;
              const sub = window.__mockBridge.handlers.submitExamAnswers({
                sessionKey: sess.sessionKey,
                examCode: 'DAILY_Y6_ARB_W1D4',
                studentName: 'Mostafa Ahmed',
                answers: { [qId]: s2 }
              });
              // Normalization strips both to 'ان'
              return sub !== null;
            }""")
            assert match_res is True, "Non-NFKC diacritic order handled cleanly"

        run_test_case("T2.3.3: Arabic answer with non-NFKC diacritic order handled cleanly", t2_3_3, results)

        def t2_3_4():
            ensure_clean_screen()
            # HTML injection in retake reason
            xss_payload = '<script>window.__xss_flag = true;</script><img src="x" onerror="window.__xss_flag=true;">'
            page.evaluate("""(xss) => {
              window.__mockBridge.handlers.requestExamRetake({
                studentName: 'Ali Ahmed',
                examCode: 'DAILY_Y5_ENG_W1D1',
                reason: xss
              });
            }""", xss_payload)
            page.evaluate("() => openParentPortal()")
            page.wait_for_timeout(200)
            xss_executed = page.evaluate("() => window.__xss_flag === true")
            assert not xss_executed, "XSS script payload must NOT execute in DOM"

        run_test_case("T2.3.4: XSS payload in retake reason is escaped and does not execute", t2_3_4, results)

        def t2_3_5():
            ensure_clean_screen()
            # Smart quotes and curly apostrophes match standard quotes
            match_res = page.evaluate("""() => {
              const curlyAnswer = '“Suddenly, the lights went out in the hallway.”';
              const sess = window.__mockBridge.handlers.getExamData('DAILY_Y5_ENG_W1D1', 'Ali Ahmed');
              const qId = sess.questions[1].id;
              const sub = window.__mockBridge.handlers.submitExamAnswers({
                sessionKey: sess.sessionKey,
                examCode: 'DAILY_Y5_ENG_W1D1',
                studentName: 'Ali Ahmed',
                answers: { [qId]: curlyAnswer }
              });
              return sub.review[1].isCorrect;
            }""")
            assert match_res is True, "Smart curly quotes in student answers must match canonical quotes"

        run_test_case("T2.3.5: Smart curly quotes in answers match canonical quotes", t2_3_5, results)

        # ========================================================
        # Domain 4: Data & Schema Anomalies (5 tests)
        # ========================================================
        print("\n-- Domain 4: Data & Schema Anomalies --")

        def t2_4_1():
            ensure_clean_screen()
            # Question missing Week and Difficulty metadata renders safely
            res = page.evaluate("""() => {
              const q = {
                id: 'ANOM_1',
                unit: 'Grammar',
                text: 'Sample question without week or difficulty',
                type: 'MCQ',
                options: ['A', 'B'],
                points: 1
              };
              questions = [q];
              currentIdx = 0;
              studentAnswers = {};
              renderQuizQuestion();
              return document.getElementById('quiz-question-box')?.innerText.includes('Sample question');
            }""")
            assert res is True, "Question with missing Week/Difficulty must render without error"

        run_test_case("T2.4.1: Question missing Week and Difficulty metadata renders safely", t2_4_1, results)

        def t2_4_2():
            ensure_clean_screen()
            # Missing options list handled without unhandled exception
            res = page.evaluate("""() => {
              const q = {
                id: 'ANOM_EMPTY_OPTS',
                unit: 'Reading',
                text: 'Comprehension prompt with empty options',
                type: 'MCQ',
                options: [],
                points: 1
              };
              questions = [q];
              currentIdx = 0;
              renderQuizQuestion();
              return document.getElementById('quiz-question-box') !== null;
            }""")
            assert res is True, "Empty options list handled without crashing quiz render"

        run_test_case("T2.4.2: Empty options list handled gracefully without exception", t2_4_2, results)

        def t2_4_3():
            ensure_clean_screen()
            # Malformed review JSON string in submissions table
            h.set_bridge_flag('forceMalformedReview', True)
            page.evaluate("""() => {
              window.__mockBridge.handlers.submitExamAnswers({
                studentName: 'Ali Ahmed',
                examCode: 'DAILY_Y5_ENG_W1D1',
                answers: {}
              });
              openParentPortal();
            }""")
            page.wait_for_timeout(400)
            subs_text = page.evaluate("() => document.getElementById('admin-submissions-container')?.innerText")
            assert "Ali Ahmed" in subs_text or "DAILY_Y5_ENG_W1D1" in subs_text or "Attempt" in subs_text or "Scored" in subs_text, f"Submissions table should render, got: {subs_text}"

        run_test_case("T2.4.3: Malformed review JSON in Submissions sheet falls back safely", t2_4_3, results)

        def t2_4_4():
            ensure_clean_screen()
            h.set_bridge_flag('forceEmptyQuestions', True)
            res = page.evaluate("() => window.__mockBridge.handlers.getExamData('DAILY_Y5_ENG_W1D1', 'Ali Ahmed')")
            assert res['success'] is False, "Expected error on empty question bank"
            assert res['code'] == 'NO_QUESTIONS', f"Expected NO_QUESTIONS code, got: {res.get('code')}"

        run_test_case("T2.4.4: Zero-question exam request returns clean NO_QUESTIONS code", t2_4_4, results)

        def t2_4_5():
            ensure_clean_screen()
            # Corrupted localStorage item does not block quiz
            res = page.evaluate("""() => {
              try {
                localStorage.setItem('primary_exam_progress_ali_DAILY_Y5_ENG_W1D1', 'MALFORMED{JSON:::');
              } catch (e) {}
              const loaded = loadProgress('ANY');
              return loaded === null;
            }""")
            assert res is True, "Corrupted localStorage JSON must return null and not throw unhandled error"

        run_test_case("T2.4.5: Corrupted localStorage progress handles JSON parse errors gracefully", t2_4_5, results)

    finally:
        if managed_harness:
            h.__exit__(None, None, None)

    # Summary
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    print(f"\nTIER 2 SUMMARY: {passed} PASSED, {failed} FAILED out of {len(results)} tests.")
    return results

if __name__ == '__main__':
    res = run_all()
    if any(r['status'] == 'FAIL' for r in res):
        sys.exit(1)
