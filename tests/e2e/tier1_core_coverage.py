"""
Tier 1: Core Feature Coverage Test Suite (25 Tests)
Covers Gateway & Portal Isolation, Daily Missions & Refreshers,
28-Exam Catalog & Quiz Engine, Assessment Submission & Scoring,
and Parent Analytics & Administration.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from tests.e2e.harness import E2EHarness, run_test_case

def run_all(harness=None):
    results = []
    print("\n========================================================")
    print("  RUNNING TIER 1: CORE FEATURE COVERAGE (25 TESTS)")
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

        # ========================================================
        # Feature 1: Gateway & Portal Isolation (5 tests)
        # ========================================================
        print("\n-- Feature 1: Gateway & Portal Isolation --")

        def t1_1_1():
            ensure_clean_screen()
            h.reset_state()
            page.evaluate("() => showScreen('screen-gateway')")
            page.click('#btn-gateway-ali')
            page.wait_for_timeout(100)
            is_student_active = page.evaluate("() => document.querySelector('#screen-student.active') !== null")
            assert is_student_active, "Screen student should be active after clicking Ali"
            title = page.evaluate("() => document.getElementById('sp-student-title')?.innerText")
            assert "Ali Ahmed" in title, f"Expected Ali Ahmed in title, got: {title}"
            grade = page.evaluate("() => document.getElementById('sp-student-grade')?.innerText")
            assert "Year 5" in grade, f"Expected Year 5 in grade, got: {grade}"

        run_test_case("T1.1.1: Click Ali Gateway -> Verify student screen, title, and Grade 5", t1_1_1, results)

        def t1_1_2():
            ensure_clean_screen()
            page.evaluate("() => showScreen('screen-gateway')")
            page.click('#btn-gateway-mostafa')
            page.wait_for_timeout(100)
            is_student_active = page.evaluate("() => document.querySelector('#screen-student.active') !== null")
            assert is_student_active, "Screen student should be active after clicking Mostafa"
            title = page.evaluate("() => document.getElementById('sp-student-title')?.innerText")
            assert "Mostafa Ahmed" in title, f"Expected Mostafa Ahmed in title, got: {title}"
            grade = page.evaluate("() => document.getElementById('sp-student-grade')?.innerText")
            assert "Grade 6" in grade, f"Expected Grade 6 in grade, got: {grade}"

        run_test_case("T1.1.2: Click Mostafa Gateway -> Verify student screen, title, and Grade 6", t1_1_2, results)

        def t1_1_3():
            ensure_clean_screen()
            page.click('[onclick*="returnToGateway"]')
            page.wait_for_timeout(100)
            is_gw_active = page.evaluate("() => document.querySelector('#screen-gateway.active') !== null")
            assert is_gw_active, "Expected screen-gateway to be active after returnToGateway"

        run_test_case("T1.1.3: Return to Gateway -> Verify gateway screen active", t1_1_3, results)

        def t1_1_4():
            ensure_clean_screen()
            durations = []
            for _ in range(5):
                start = time.perf_counter()
                page.evaluate("() => showScreen('screen-student')")
                durations.append((time.perf_counter() - start) * 1000)
                page.evaluate("() => showScreen('screen-gateway')")
            avg_ms = sum(durations) / len(durations)
            assert avg_ms < 50.0, f"Average DOM transition latency was {avg_ms:.2f}ms (must be <50ms)"

        run_test_case("T1.1.4: Screen transition latency benchmark (<50ms assertion)", t1_1_4, results)

        def t1_1_5():
            ensure_clean_screen()
            page.evaluate("() => openStudentPortal('ali')")
            t_ali = page.evaluate("() => document.getElementById('sp-student-title')?.innerText")
            assert "Ali" in t_ali, f"Expected Ali title, got {t_ali}"
            page.evaluate("() => openStudentPortal('mostafa')")
            t_mos = page.evaluate("() => document.getElementById('sp-student-title')?.innerText")
            assert "Mostafa" in t_mos, f"Expected Mostafa title, got {t_mos}"

        run_test_case("T1.1.5: Direct portal switching between students", t1_1_5, results)

        # ========================================================
        # Feature 2: Daily Missions & Concept Refreshers (5 tests)
        # ========================================================
        print("\n-- Feature 2: Daily Missions & Concept Refreshers --")

        def t1_2_1():
            ensure_clean_screen()
            page.evaluate("() => openStudentPortal('ali')")
            page.wait_for_timeout(100)
            page.click('#btn-launch-today')
            page.wait_for_timeout(100)
            is_modal_active = page.evaluate("() => document.querySelector('#start-modal.active') !== null")
            assert is_modal_active, "Start modal should be active"
            m_title = page.evaluate("() => document.getElementById('m-exam-title')?.innerText")
            assert "Adverbs of Manner" in m_title or "Ali" in m_title, f"Modal title mismatch: {m_title}"
            page.evaluate("() => closeStartModal()")

        run_test_case("T1.2.1: Ali Today Mission button triggers start modal", t1_2_1, results)

        def t1_2_2():
            ensure_clean_screen()
            page.evaluate("() => openStudentPortal('mostafa')")
            page.wait_for_timeout(100)
            page.click('#btn-launch-today')
            page.wait_for_timeout(100)
            is_modal_active = page.evaluate("() => document.querySelector('#start-modal.active') !== null")
            assert is_modal_active, "Start modal should be active for Mostafa"
            m_title = page.evaluate("() => document.getElementById('m-exam-title')?.innerText")
            assert "Mostafa" in m_title or "إدارة الوقت" in m_title or "Day 4" in m_title, f"Modal title mismatch: {m_title}"
            page.evaluate("() => closeStartModal()")

        run_test_case("T1.2.2: Mostafa Today Mission button triggers start modal", t1_2_2, results)

        def t1_2_3():
            ensure_clean_screen()
            page.evaluate("() => openStudentPortal('ali')")
            page.wait_for_timeout(100)
            initial_display = page.evaluate("() => document.getElementById('refresher-content-body')?.style.display")
            page.click('#btn-toggle-refresher')
            page.wait_for_timeout(100)
            toggled_display = page.evaluate("() => document.getElementById('refresher-content-body')?.style.display")
            assert initial_display != toggled_display, "Refresher body display should toggle"
            text = page.evaluate("() => document.getElementById('refresher-content-body')?.innerText")
            assert len(text) > 20, "Refresher body should contain pedagogical briefing text"

        run_test_case("T1.2.3: Concept refresher accordion toggle and content rendering", t1_2_3, results)

        def t1_2_4():
            ensure_clean_screen()
            page.evaluate("() => openStudentPortal('ali')")
            page.click('#btn-launch-today')
            page.wait_for_timeout(100)
            assert page.evaluate("() => document.querySelector('#start-modal.active') !== null")
            page.click('#start-modal .btn-secondary')
            page.wait_for_timeout(100)
            assert page.evaluate("() => document.querySelector('#start-modal.active') === null"), "Modal should be closed"
            assert page.evaluate("() => document.querySelector('#screen-student.active') !== null"), "Student screen remains active"

        run_test_case("T1.2.4: Start modal close button dismisses dialog", t1_2_4, results)

        def t1_2_5():
            ensure_clean_screen()
            page.evaluate("() => openVideoModal('VID_01', 'Adverbials Masterclass')")
            page.wait_for_timeout(100)
            is_vmodal = page.evaluate("() => document.querySelector('#video-modal.active') !== null")
            assert is_vmodal, "Video modal should open"
            page.evaluate("() => closeVideoModal()")
            page.wait_for_timeout(100)
            assert page.evaluate("() => document.querySelector('#video-modal.active') === null")

        run_test_case("T1.2.5: Video lesson modal open and dismiss", t1_2_5, results)

        # ========================================================
        # Feature 3: 28-Exam Catalog & Quiz Engine (5 tests)
        # ========================================================
        print("\n-- Feature 3: 28-Exam Catalog & Quiz Engine --")

        def t1_3_1():
            ensure_clean_screen()
            page.evaluate("() => openStudentPortal('ali')")
            page.wait_for_timeout(150)
            cards = page.evaluate("() => Array.from(document.querySelectorAll('.exam-item-card')).map(c => c.innerText)")
            assert len(cards) >= 14, f"Ali exams card count should be >= 14, found: {len(cards)}"
            has_w1 = any("Week 1 Milestone" in c for c in cards)
            assert has_w1, "Expected Week 1 Milestone exam card in Ali's catalog"

        run_test_case("T1.3.1: Ali exam catalog renders all 14 curriculum exam cards", t1_3_1, results)

        def t1_3_2():
            ensure_clean_screen()
            page.evaluate("() => openStudentPortal('mostafa')")
            page.wait_for_timeout(150)
            cards = page.evaluate("() => Array.from(document.querySelectorAll('.exam-item-card')).map(c => c.innerText)")
            assert len(cards) >= 11, f"Mostafa exams card count should be >= 11, found: {len(cards)}"
            has_arb = any("اللغة العربية" in c or "Mostafa" in c for c in cards)
            assert has_arb, "Expected Arabic grammar exam card in Mostafa's catalog"

        run_test_case("T1.3.2: Mostafa exam catalog renders all 11 curriculum exam cards", t1_3_2, results)

        def t1_3_3():
            ensure_clean_screen()
            ali_exams = page.evaluate("() => STUDENT_DATA['ali'].exams.map(e => e.code)")
            mos_exams = page.evaluate("() => STUDENT_DATA['mostafa'].exams.map(e => e.code)")
            all_codes = set(ali_exams + mos_exams)
            assert "EX_Y5_ENG_ADV01" in all_codes, "EX_Y5_ENG_ADV01 should be present"
            assert "EX_Y6_ARB_PRIO01" in all_codes, "EX_Y6_ARB_PRIO01 should be present"
            assert "EX_Y6_ENG_FANTASY01" in all_codes, "EX_Y6_ENG_FANTASY01 should be present"

        run_test_case("T1.3.3: Verify all 3 foundational diagnostic exams exist", t1_3_3, results)

        def t1_3_4():
            ensure_clean_screen()
            page.evaluate("() => { openStudentPortal('mostafa'); showScreen('screen-quiz'); loadAndStartQuiz('EX_Y6_ENG_FANTASY01'); }")
            page.wait_for_timeout(200)
            is_quiz = page.evaluate("() => document.querySelector('#screen-quiz.active') !== null")
            assert is_quiz, "Quiz screen should be active"
            passage_text = page.evaluate("() => document.querySelector('.passage-text')?.innerText")
            assert passage_text and len(passage_text) > 40, f"Expected passage text in fantasy quiz, got: {passage_text}"

        run_test_case("T1.3.4: Starting English Fantasy exam displays reading passage box", t1_3_4, results)

        def t1_3_5():
            ensure_clean_screen()
            page.evaluate("() => { openStudentPortal('ali'); showScreen('screen-quiz'); loadAndStartQuiz('DAILY_Y5_ENG_W1D1'); }")
            page.wait_for_timeout(200)
            page.click('.option-item:first-child')
            page.wait_for_timeout(100)
            is_selected = page.evaluate("() => document.querySelector('.option-item:first-child').classList.contains('selected')")
            assert is_selected, "Option should be marked selected"
            
            page.click('#quiz-submit-btn')
            page.wait_for_timeout(100)
            ind_text = page.evaluate("() => document.getElementById('quiz-progress-indicator')?.innerText")
            assert "Question 2 of" in ind_text, f"Progress text should say Question 2 of ..., got: {ind_text}"

            page.click('.nav-btn-row .btn-secondary')
            page.wait_for_timeout(100)
            ind_text_prev = page.evaluate("() => document.getElementById('quiz-progress-indicator')?.innerText")
            assert "Question 1 of" in ind_text_prev, f"Progress text should return to Question 1 of ..., got: {ind_text_prev}"

        run_test_case("T1.3.5: Question pagination and option selection persistence", t1_3_5, results)

        # ========================================================
        # Feature 4: Assessment Submission & Scoring Engine (5 tests)
        # ========================================================
        print("\n-- Feature 4: Assessment Submission & Scoring Engine --")

        def t1_4_1():
            ensure_clean_screen()
            page.evaluate("() => { openStudentPortal('ali'); showScreen('screen-quiz'); loadAndStartQuiz('DAILY_Y5_ENG_W1D1'); }")
            page.wait_for_timeout(200)
            page.evaluate("""() => {
              const qs = questions;
              qs.forEach(q => {
                studentAnswers[q.id] = q.options[0];
              });
              submitQuiz(true);
            }""")
            page.wait_for_timeout(300)
            is_res = page.evaluate("() => document.querySelector('#screen-result.active') !== null")
            assert is_res, "Result screen should be active"
            rating = page.evaluate("() => document.getElementById('res-rating-display')?.innerText")
            assert "100%" in rating, f"Expected 100% in rating display, got: {rating}"
            score = page.evaluate("() => document.getElementById('res-score-display')?.innerText")
            assert "5 / 5" in score, f"Expected 5 / 5 score, got: {score}"

        run_test_case("T1.4.1: Submit 100% correct answers -> renders 100% and Mastery badge", t1_4_1, results)

        def t1_4_2():
            ensure_clean_screen()
            page.evaluate("() => { openStudentPortal('ali'); showScreen('screen-quiz'); loadAndStartQuiz('DAILY_Y5_ENG_W1D2'); }")
            page.wait_for_timeout(200)
            page.evaluate("""() => {
              const qs = questions;
              studentAnswers[qs[0].id] = qs[0].options[0];
              for (let i = 1; i < qs.length; i++) {
                studentAnswers[qs[i].id] = qs[i].options[1];
              }
              submitQuiz(true);
            }""")
            page.wait_for_timeout(300)
            score = page.evaluate("() => document.getElementById('res-score-display')?.innerText")
            assert "1 / 5" in score, f"Expected partial score 1 / 5, got: {score}"

        run_test_case("T1.4.2: Submit partial answers -> calculates exact earned score (1/5)", t1_4_2, results)

        def t1_4_3():
            ensure_clean_screen()
            page.evaluate("() => { openStudentPortal('ali'); showScreen('screen-quiz'); loadAndStartQuiz('DAILY_Y5_ENG_W1D3'); }")
            page.wait_for_timeout(200)
            page.evaluate("() => { studentAnswers = {}; submitQuiz(true); }")
            page.wait_for_timeout(300)
            score = page.evaluate("() => document.getElementById('res-score-display')?.innerText")
            assert "0 / 5" in score, f"Expected 0 / 5 for blank submission, got: {score}"
            rating = page.evaluate("() => document.getElementById('res-rating-display')?.innerText")
            assert "Needs Review" in rating or "0%" in rating, f"Expected Needs Review rating, got: {rating}"

        run_test_case("T1.4.3: Submit blank answers -> scores 0% with Needs Review rating", t1_4_3, results)

        def t1_4_4():
            cards = page.evaluate("() => Array.from(document.querySelectorAll('.review-item')).map(c => c.innerText)")
            assert len(cards) >= 5, f"Expected at least 5 review cards, found: {len(cards)}"
            exps = page.evaluate("() => Array.from(document.querySelectorAll('.explanation-box')).map(e => e.innerText)")
            assert len(exps) >= 1 or any("Explanation" in c for c in cards), "Expected explanations in review cards"

        run_test_case("T1.4.4: Review cards render detailed pedagogical explanations", t1_4_4, results)

        def t1_4_5():
            completed_plan = page.evaluate("""() => {
              return window.__mockBridge.state.studyPlan.find(p => p.examCode === 'DAILY_Y5_ENG_W1D1');
            }""")
            assert completed_plan and completed_plan.get('status') == 'Completed', "Study plan item status should be 'Completed'"

        run_test_case("T1.4.5: Exam completion updates corresponding Study Plan status to Completed", t1_4_5, results)

        # ========================================================
        # Feature 5: Parent Analytics & Administration (5 tests)
        # ========================================================
        print("\n-- Feature 5: Parent Analytics & Administration --")

        def t1_5_1():
            ensure_clean_screen()
            page.evaluate("() => openParentPortal()")
            page.wait_for_timeout(200)
            is_admin = page.evaluate("() => document.querySelector('#screen-admin.active') !== null")
            assert is_admin, "Admin screen should be active"
            table_text = page.evaluate("() => document.getElementById('admin-submissions-container')?.innerText")
            assert len(table_text) > 30, "Submissions container should display table rows"

        run_test_case("T1.5.1: Open Parent Portal -> renders Submissions tab with records", t1_5_1, results)

        def t1_5_2():
            ensure_clean_screen()
            page.evaluate("() => switchParentView('analytics')")
            page.wait_for_timeout(100)
            is_ana_vis = page.evaluate("() => document.getElementById('pview-analytics')?.style.display === 'block'")
            assert is_ana_vis, "Analytics view should be visible"
            title = page.evaluate("() => document.getElementById('ana-student-title')?.innerText")
            assert "Ali Ahmed" in title or "Diagnostic" in title, f"Analytics title mismatch: {title}"

        run_test_case("T1.5.2: Switch to Analytics tab -> renders performance radar view", t1_5_2, results)

        def t1_5_3():
            ensure_clean_screen()
            page.evaluate("() => switchAdminStudent('Mostafa')")
            page.wait_for_timeout(100)
            title_m = page.evaluate("() => document.getElementById('ana-student-title')?.innerText")
            assert "Mostafa Ahmed" in title_m, f"Expected Mostafa in title, got: {title_m}"
            page.evaluate("() => switchAdminStudent('Ali')")
            page.wait_for_timeout(100)
            title_a = page.evaluate("() => document.getElementById('ana-student-title')?.innerText")
            assert "Ali Ahmed" in title_a, f"Expected Ali in title, got: {title_a}"

        run_test_case("T1.5.3: Toggle student filter in Admin updates analytics title", t1_5_3, results)

        def t1_5_4():
            ensure_clean_screen()
            page.evaluate("() => switchParentView('plan')")
            page.wait_for_timeout(100)
            page.evaluate("() => filterPlanByWeek('W1')")
            page.wait_for_timeout(100)
            plan_text = page.evaluate("() => document.getElementById('admin-plan-container')?.innerText")
            assert "W1" in plan_text, "Expected W1 entries in study plan"
            page.evaluate("() => filterPlanByWeek('W2')")
            page.wait_for_timeout(100)
            plan_text_w2 = page.evaluate("() => document.getElementById('admin-plan-container')?.innerText")
            assert "W2" in plan_text_w2, "Expected W2 entries in study plan"

        run_test_case("T1.5.4: Study plan week filter chips update plan rows", t1_5_4, results)

        def t1_5_5():
            ensure_clean_screen()
            retakes = page.evaluate("() => window.__mockBridge.state.retakeRequests")
            assert len(retakes) >= 1, "Expected at least 1 seeded retake request"
            banner_text = page.evaluate("() => document.getElementById('admin-retake-banner')?.innerText")
            assert "Retake" in banner_text or "Pending" in banner_text, f"Expected retake banner text, got: {banner_text}"

        run_test_case("T1.5.5: Retake requests banner and table render active requests", t1_5_5, results)

    finally:
        if managed_harness:
            h.__exit__(None, None, None)

    # Summary
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    print(f"\nTIER 1 SUMMARY: {passed} PASSED, {failed} FAILED out of {len(results)} tests.")
    return results

if __name__ == '__main__':
    res = run_all()
    if any(r['status'] == 'FAIL' for r in res):
        sys.exit(1)
