"""
Tier 4: Real-World Application Scenarios (2 Scenarios)
Covers Dual-Student Morning Routine on Shared Browser and
Comprehensive Weekend Parent Audit & Plan Review.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from tests.e2e.harness import E2EHarness, run_test_case

def run_all(harness=None):
    results = []
    print("\n========================================================")
    print("  RUNNING TIER 4: REAL-WORLD APPLICATION SCENARIOS (2)")
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
        # Scenario 1: Dual-Student Morning Routine on Shared Browser
        # --------------------------------------------------------
        def t4_1_dual_student_morning_routine():
            ensure_clean()

            # Part A: Ali Ahmed's Morning Session
            print("\n    [Step A] Ali Ahmed morning homework session...")
            # 1. Gateway -> Ali Portal
            page.evaluate("() => showScreen('screen-gateway')")
            page.click('#btn-gateway-ali')
            page.wait_for_timeout(150)
            ali_title = page.evaluate("() => document.getElementById('sp-student-title')?.innerText")
            assert "Ali Ahmed" in ali_title, f"Expected Ali Ahmed portal, got: {ali_title}"

            # 2. Launch Day 1 Mission
            page.click('#btn-launch-today')
            page.wait_for_timeout(100)
            page.click('#start-modal .btn-primary') # Start
            page.wait_for_timeout(200)

            # 3. Complete Ali's Quiz (100% correct)
            page.evaluate("""() => {
              questions.forEach(q => {
                studentAnswers[q.id] = q.options[0];
              });
              submitQuiz(true);
            }""")
            page.wait_for_timeout(300)

            # 4. Check Ali's Result Screen
            ali_score = page.evaluate("() => document.getElementById('res-score-display')?.innerText")
            assert "5 / 5" in ali_score, f"Expected 5/5 score for Ali, got: {ali_score}"

            # 5. Ali returns to Gateway
            page.evaluate("() => showScreen('screen-gateway')")
            page.wait_for_timeout(150)

            # Part B: Mostafa Ahmed's Morning Session (Same Browser)
            print("    [Step B] Mostafa Ahmed morning homework session on same browser...")
            # 1. Gateway -> Mostafa Portal
            page.click('#btn-gateway-mostafa')
            page.wait_for_timeout(150)
            mos_title = page.evaluate("() => document.getElementById('sp-student-title')?.innerText")
            assert "Mostafa Ahmed" in mos_title, f"Expected Mostafa Ahmed portal, got: {mos_title}"

            # 2. Launch Mostafa's Day 4 Mission
            page.click('#btn-launch-today')
            page.wait_for_timeout(100)
            page.click('#start-modal .btn-primary') # Start
            page.wait_for_timeout(200)

            # 3. Complete Mostafa's Arabic Quiz
            page.evaluate("""() => {
              questions.forEach(q => {
                studentAnswers[q.id] = q.options[0];
              });
              submitQuiz(true);
            }""")
            page.wait_for_timeout(300)

            # 4. Check Mostafa's Result Screen
            mos_score = page.evaluate("() => document.getElementById('res-score-display')?.innerText")
            assert "5 / 5" in mos_score, f"Expected 5/5 score for Mostafa, got: {mos_score}"

            # 5. Return to Gateway
            page.evaluate("() => showScreen('screen-gateway')")
            page.wait_for_timeout(100)

            # Part C: Verify Data Isolation in Backend Database
            subs = page.evaluate("() => window.__mockBridge.state.submissions")
            ali_subs = [s for s in subs if 'ali' in s['studentName'].lower()]
            mos_subs = [s for s in subs if 'mostafa' in s['studentName'].lower()]

            assert len(ali_subs) >= 1, "Ali's submission must be recorded distinctly"
            assert len(mos_subs) >= 1, "Mostafa's submission must be recorded distinctly"
            assert ali_subs[0]['examCode'] != mos_subs[0]['examCode'], "Exam codes must remain isolated across students"

        run_test_case("T4.1: Dual-student shared browser morning routine with complete data isolation", t4_1_dual_student_morning_routine, results)

        # --------------------------------------------------------
        # Scenario 2: Comprehensive Weekend Parent Audit
        # --------------------------------------------------------
        def t4_2_weekend_parent_audit():
            ensure_clean()

            # 1. Parent accesses Parent Portal
            page.evaluate("() => openParentPortal()")
            page.wait_for_timeout(200)
            is_admin = page.evaluate("() => document.querySelector('#screen-admin.active') !== null")
            assert is_admin, "Admin screen must be active"

            # 2. Submissions Tab Audit
            subs_text = page.evaluate("() => document.getElementById('admin-submissions-container')?.innerText")
            assert len(subs_text) > 40, "Submissions table must contain historical records"

            # 3. Study Plan Review & Multi-Week Filtering
            page.evaluate("() => switchParentView('plan')")
            page.wait_for_timeout(100)

            for wk in ['W1', 'W2', 'W3', 'W4']:
                page.evaluate("(w) => filterPlanByWeek(w)", wk)
                page.wait_for_timeout(100)
                plan_text = page.evaluate("() => document.getElementById('admin-plan-container')?.innerText")
                assert wk in plan_text, f"Study plan filter for {wk} must display {wk} lessons"

            # 4. Analytics & Diagnostic Evaluation Report
            page.evaluate("() => switchParentView('analytics')")
            page.wait_for_timeout(100)
            # Inspect Ali's Radar
            page.evaluate("() => switchAdminStudent('Ali')")
            page.wait_for_timeout(100)
            title_ali = page.evaluate("() => document.getElementById('ana-student-title')?.innerText")
            assert "Ali Ahmed" in title_ali, f"Expected Ali in Analytics title, got: {title_ali}"

            # Inspect Mostafa's Radar
            page.evaluate("() => switchAdminStudent('Mostafa')")
            page.wait_for_timeout(100)
            title_mos = page.evaluate("() => document.getElementById('ana-student-title')?.innerText")
            assert "Mostafa Ahmed" in title_mos, f"Expected Mostafa in Analytics title, got: {title_mos}"

            # 5. Retake Request Audit & Administrative Approval
            pending_before = page.evaluate("""() => {
              return window.__mockBridge.state.retakeRequests.filter(r => r.status === 'PENDING').length;
            }""")
            assert pending_before >= 1, "Expected at least 1 pending retake request for parent review"

            page.evaluate("() => window.__mockBridge.handlers.approveRetakeRequest('REQ-101')")
            page.wait_for_timeout(100)

            req = page.evaluate("""() => {
              return window.__mockBridge.state.retakeRequests.find(r => r.id === 'REQ-101');
            }""")
            assert req['status'] == 'APPROVED', "Parent approval must transition retake status to APPROVED"

            # 6. Coligo Hub Cloud Materials Sync
            coligo_data = page.evaluate("() => window.__mockBridge.handlers.getColigoHubData()")
            assert coligo_data['count'] >= 1, "Coligo Hub should return synchronized learning materials"

        run_test_case("T4.2: Comprehensive weekend parent audit (Submissions, Study Plan W1-W4, Analytics, Retakes, Coligo)", t4_2_weekend_parent_audit, results)

    finally:
        if managed_harness:
            h.__exit__(None, None, None)

    # Summary
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    print(f"\nTIER 4 SUMMARY: {passed} PASSED, {failed} FAILED out of {len(results)} scenarios.")
    return results

if __name__ == '__main__':
    res = run_all()
    if any(r['status'] == 'FAIL' for r in res):
        sys.exit(1)
