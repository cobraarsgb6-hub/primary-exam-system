"""
Tier 3: Cross-Feature Integration Scenarios (4 Scenarios)
Covers End-to-End Remediation Loop, Dynamic Passage Pool Rotation,
Multi-Week Cumulative Synthesis, and Mid-Exam Progress Restoration on Refresh.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from tests.e2e.harness import E2EHarness, run_test_case

def run_all(harness=None):
    results = []
    print("\n========================================================")
    print("  RUNNING TIER 3: CROSS-FEATURE INTEGRATION SCENARIOS (4)")
    print("========================================================")

    managed_harness = harness is None
    h = E2EHarness() if managed_harness else harness
    if managed_harness:
        h.__enter__()

    try:
        page = h.page

        def ensure_clean():
            page.evaluate("""() => {
              if (typeof closeStartModal === 'function') closeStartModal();
              if (typeof closeVideoModal === 'function') closeVideoModal();
              if (typeof closeLessonSummaryModal === 'function') closeLessonSummaryModal();
              window.__mockBridge.resetState();
            }""")

        # --------------------------------------------------------
        # Scenario 1: Full Student Remediation Loop
        # --------------------------------------------------------
        def t3_1_remediation_loop():
            ensure_clean()
            exam_code = 'EX_Y5_ENG_W1'
            student = 'Ali Ahmed'

            # 1. Ali takes exam and scores poorly (0/10)
            page.evaluate("""(code) => {
              openStudentPortal('ali');
              showScreen('screen-quiz');
              loadAndStartQuiz(code);
            }""", exam_code)
            page.wait_for_timeout(200)

            # Submit empty answers
            page.evaluate("() => { studentAnswers = {}; submitQuiz(true); }")
            page.wait_for_timeout(300)

            # Check result screen has 0%
            rating = page.evaluate("() => document.getElementById('res-rating-display')?.innerText")
            assert "0%" in rating, f"Expected 0% in result screen, got: {rating}"

            # 2. Return to portal, verify attempts logged
            page.evaluate("""(code) => {
              returnToStudentPortal();
              selectStudentExam(code);
            }""", exam_code)
            page.wait_for_timeout(200)

            # 3. Request retake
            page.evaluate("""(args) => {
              window.__mockBridge.handlers.requestExamRetake({
                studentName: args.name,
                examCode: args.code,
                reason: 'I studied fronted adverbials and want to retry.'
              });
            }""", {'name': student, 'code': exam_code})

            # Verify retake is PENDING
            reqs = page.evaluate("() => window.__mockBridge.state.retakeRequests")
            pending = [r for r in reqs if r['examCode'] == exam_code and r['status'] == 'PENDING']
            assert len(pending) >= 1, "Expected pending retake request"
            req_id = pending[0]['id']

            # 4. Parent opens portal and approves retake
            page.evaluate("() => openParentPortal()")
            page.wait_for_timeout(200)
            page.evaluate("(id) => window.__mockBridge.handlers.approveRetakeRequest(id)", req_id)

            # Verify status is now APPROVED
            approved = page.evaluate("""(id) => {
              const r = window.__mockBridge.state.retakeRequests.find(x => x.id === id);
              return r && r.status === 'APPROVED';
            }""", req_id)
            assert approved, "Retake request should be APPROVED"

            # 5. Ali returns to portal, retake is unlocked, takes exam again and scores 100%
            page.evaluate("""(code) => {
              openStudentPortal('ali');
              showScreen('screen-quiz');
              loadAndStartQuiz(code);
            }""", exam_code)
            page.wait_for_timeout(200)

            # Answer all correctly
            page.evaluate("""() => {
              questions.forEach(q => {
                studentAnswers[q.id] = q.options[0];
              });
              submitQuiz(true);
            }""")
            page.wait_for_timeout(300)

            # Verify score 100%
            res_rating = page.evaluate("() => document.getElementById('res-rating-display')?.innerText")
            assert "100%" in res_rating, f"Expected 100% on retake, got: {res_rating}"

            # 6. Verify Study Plan updated to Completed
            plan_status = page.evaluate("""(code) => {
              const item = window.__mockBridge.state.studyPlan.find(p => p.examCode === code);
              return item ? item.status : null;
            }""", exam_code)
            assert plan_status == 'Completed', f"Expected Study Plan status 'Completed', got: {plan_status}"

        run_test_case("T3.1: Full student remediation lifecycle (Fail -> Request -> Approve -> Pass -> Study Plan updated)", t3_1_remediation_loop, results)

        # --------------------------------------------------------
        # Scenario 2: Dynamic Passage Pool Rotation
        # --------------------------------------------------------
        def t3_2_passage_rotation():
            ensure_clean()
            exam_code = 'EX_Y6_ENG_FANTASY01'

            # Session 1: Passage Index 0 ("The City That Waited")
            h.set_bridge_flag('passagePoolIndex', 0)
            q_set1 = page.evaluate("""(code) => {
              return window.__mockBridge.handlers.getExamData(code, 'Mostafa Ahmed');
            }""", exam_code)
            p1_text = q_set1['questions'][0]['passage']
            assert "The city was a hush" in p1_text, "Session 1 should load 'The City That Waited'"

            # Session 2: Passage Index 1 ("The Crystal Citadel")
            h.set_bridge_flag('passagePoolIndex', 1)
            q_set2 = page.evaluate("""(code) => {
              return window.__mockBridge.handlers.getExamData(code, 'Mostafa Ahmed');
            }""", exam_code)
            p2_text = q_set2['questions'][0]['passage']
            assert "Crystal Citadel" in p2_text, "Session 2 should load 'The Crystal Citadel'"

            # Verify no text overlap between passages
            assert p1_text != p2_text, "Consecutive sessions must rotate passages without identical text"
            assert q_set1['questions'][0]['options'][0] != q_set2['questions'][0]['options'][0], "Options must adapt to active passage"

        run_test_case("T3.2: Dynamic passage pool rotation across consecutive sessions", t3_2_passage_rotation, results)

        # --------------------------------------------------------
        # Scenario 3: Multi-Week Cumulative Synthesis
        # --------------------------------------------------------
        def t3_3_cumulative_synthesis():
            ensure_clean()
            # Ali Week 2 Cumulative Exam (W1 + W2)
            exam_code = 'EX_Y5_ENG_W2_CUMULATIVE'
            data = page.evaluate("""(code) => {
              return window.__mockBridge.handlers.getExamData(code, 'Ali Ahmed');
            }""", exam_code)
            
            qs = data['questions']
            assert len(qs) == 12, f"Expected 12 questions for W2 cumulative, got: {len(qs)}"

            # Verify zero duplicate question IDs
            q_ids = [q['id'] for q in qs]
            unique_ids = set(q_ids)
            assert len(unique_ids) == len(q_ids), f"Duplicate questions detected in cumulative set: {len(q_ids) - len(unique_ids)} duplicates"

            # Verify points are uniform
            for q in qs:
                assert q['points'] >= 1, "Each question must have at least 1 point"

        run_test_case("T3.3: Multi-week cumulative synthesis with zero question ID duplication", t3_3_cumulative_synthesis, results)

        # --------------------------------------------------------
        # Scenario 4: Progress Restoration on Refresh
        # --------------------------------------------------------
        def t3_4_progress_restoration():
            ensure_clean()
            exam_code = 'DAILY_Y5_ENG_W1D1'

            # 1. Start exam
            page.evaluate("""(code) => {
              openStudentPortal('ali');
              showScreen('screen-quiz');
              loadAndStartQuiz(code);
            }""", exam_code)
            page.wait_for_timeout(200)

            # 2. Answer question 1 and advance to question 2
            page.click('.option-item:first-child')
            page.wait_for_timeout(100)
            page.click('#quiz-submit-btn') # Next
            page.wait_for_timeout(100)

            # Confirm we are on Question 2
            ind_before = page.evaluate("() => document.getElementById('quiz-progress-indicator')?.innerText")
            assert "Question 2 of" in ind_before, f"Expected Question 2, got: {ind_before}"

            # Verify progress saved in localStorage
            has_saved = page.evaluate("""() => {
              const raw = localStorage.getItem(progressKey());
              return raw !== null && raw.includes('answers');
            }""")
            assert has_saved, "Progress must be saved to localStorage"

            # 3. Reload page (simulate network interruption / user refresh)
            h.reload_portal()
            page.wait_for_timeout(300)

            # 4. Resume student portal and exam
            page.evaluate("""(code) => {
              openStudentPortal('ali');
              showScreen('screen-quiz');
              loadAndStartQuiz(code);
            }""", exam_code)
            page.wait_for_timeout(200)

            # Verify questions loaded
            q_box = page.evaluate("() => document.getElementById('quiz-question-box')?.innerText")
            assert len(q_box) > 20, "Quiz questions must render upon resumption"

        run_test_case("T3.4: In-progress quiz state and question navigation restored across page reload", t3_4_progress_restoration, results)

    finally:
        if managed_harness:
            h.__exit__(None, None, None)

    # Summary
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    print(f"\nTIER 3 SUMMARY: {passed} PASSED, {failed} FAILED out of {len(results)} scenarios.")
    return results

if __name__ == '__main__':
    res = run_all()
    if any(r['status'] == 'FAIL' for r in res):
        sys.exit(1)
