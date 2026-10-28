from playwright.sync_api import sync_playwright

def run_adversarial_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page_errors = []
        console_errors = []
        page.on('pageerror', lambda e: page_errors.append(str(e)))
        page.on('console', lambda m: console_errors.append(m.text) if m.type == 'error' else None)

        # Edge Case 1: Unknown student in URL
        page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html?student=unknown_person')
        page.wait_for_timeout(300)
        active_screen = page.evaluate("() => { const el = document.querySelector('.screen.active'); return el ? el.id : null; }")
        print('Edge Case 1 (Unknown student): Active screen ->', active_screen)
        assert active_screen == 'screen-gateway', 'Should fallback to screen-gateway'

        # Edge Case 2A: Ali with invalid exam code
        page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html?student=ali&exam=NON_EXISTENT_EXAM_999')
        page.wait_for_timeout(300)
        active_screen = page.evaluate("() => { const el = document.querySelector('.screen.active'); return el ? el.id : null; }")
        active_exam_ali = page.evaluate("() => activeExamCode")
        print('Edge Case 2A (Ali with invalid exam): Active screen ->', active_screen, '| activeExamCode ->', active_exam_ali)
        assert active_screen == 'screen-student'
        assert active_exam_ali == 'EX_Y5_ENG_ADV01', f'Should retain valid activeExamCode or first exam, got {active_exam_ali}'

        # Edge Case 2B: Mostafa with invalid exam code (when previous activeExamCode is Ali's exam)
        page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html?student=mostafa&exam=NON_EXISTENT_EXAM_999')
        page.wait_for_timeout(300)
        active_screen = page.evaluate("() => { const el = document.querySelector('.screen.active'); return el ? el.id : null; }")
        active_exam_mos = page.evaluate("() => activeExamCode")
        mos_first = page.evaluate("() => STUDENT_DATA['mostafa'].exams[0].code")
        print('Edge Case 2B (Mostafa with invalid exam): Active screen ->', active_screen, '| activeExamCode ->', active_exam_mos, '| Expected first:', mos_first)
        assert active_screen == 'screen-student'
        assert active_exam_mos == mos_first, f'Should fallback to Mostafa first exam ({mos_first}), got {active_exam_mos}'

        # Edge Case 3: Admin URL param
        page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html?admin=1')
        page.wait_for_timeout(300)
        active_screen = page.evaluate("() => { const el = document.querySelector('.screen.active'); return el ? el.id : null; }")
        print('Edge Case 3 (Admin param): Active screen ->', active_screen)
        assert active_screen == 'screen-admin'

        # Edge Case 4: Inspector chips with non-existent student or null
        res_chips_null = page.evaluate("() => { setupInspectorChips(null); return document.querySelectorAll('#inspect-exam-chips .inspect-chip').length; }")
        res_chips_bad = page.evaluate("() => { setupInspectorChips('non_existent'); return document.querySelectorAll('#inspect-exam-chips .inspect-chip').length; }")
        print('Edge Case 4 (setupInspectorChips null/bad):', res_chips_null, 'chips for null,', res_chips_bad, 'chips for non_existent')
        assert res_chips_null > 0, 'Null should fallback to activeAdminStudent or Ali'
        assert res_chips_bad == 0, 'Bad student should safely return 0 chips without error'

        # Mock alert before bad lesson
        page.evaluate("() => { window.alert = () => {}; }")
        # Edge Case 5: Lesson summary with non-existent lessonId
        page.evaluate("() => openLessonSummaryModal('fake_lesson_id_999')")
        summary_modal_open = page.evaluate("() => document.getElementById('lesson-summary-modal').classList.contains('active')")
        print('Edge Case 5 (Bad lesson ID): modal active ->', summary_modal_open)
        assert not summary_modal_open, 'Modal should not activate on missing summary data'

        print('Console errors across edge cases:', console_errors)
        print('Page errors across edge cases:', page_errors)
        assert len(page_errors) == 0, f'Page errors: {page_errors}'
        assert len(console_errors) == 0, f'Console errors: {console_errors}'
        print('ALL ADVERSARIAL EDGE CASE TESTS PASSED 100%!')
        browser.close()

if __name__ == '__main__':
    run_adversarial_tests()
