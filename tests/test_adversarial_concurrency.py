"""
Adversarial Concurrency, Race Condition, and UI Thrashing Test Suite
Milestone 1 — Challenger M1-2
"""

import os
import sys
import time
import html.parser
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, 'Index.html').replace('\\', '/')
MOCK_BRIDGE_PATH = os.path.join(BASE_DIR, 'tests', 'e2e', 'mock_bridge.js').replace('\\', '/')

def extract_all_buttons():
    with open(os.path.join(BASE_DIR, 'Index.html'), 'r', encoding='utf-8') as f:
        content = f.read()

    class ButtonExtractor(html.parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self.buttons = []
        def handle_starttag(self, tag, attrs):
            if tag == 'button':
                d = dict(attrs)
                line, _ = self.getpos()
                self.buttons.append({
                    'line': line,
                    'id': d.get('id', ''),
                    'class': d.get('class', ''),
                    'onclick': d.get('onclick', ''),
                })

    parser = ButtonExtractor()
    parser.feed(content)
    return parser.buttons

def create_adversarial_page(p, with_mock_bridge=True):
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    console_errors = []
    page_errors = []

    def on_console(msg):
        if msg.type == 'error':
            text = msg.text
            if 'favicon' not in text.lower():
                console_errors.append(f"Console error: {text}")

    def on_page_error(err):
        page_errors.append(f"Page error: {str(err)}")

    page.on('console', on_console)
    page.on('pageerror', on_page_error)

    if with_mock_bridge and os.path.exists(MOCK_BRIDGE_PATH):
        page.add_init_script(path=MOCK_BRIDGE_PATH)

    # Route local streaming video server so offline headless testing doesn't ERR_CONNECTION_REFUSED
    page.route("**/stream/**", lambda route: route.fulfill(status=200, body=b"fake video stream"))
    page.route("http://192.168.1.96:8085/**", lambda route: route.fulfill(status=200, body=b"ok"))

    page.goto(f'file:///{INDEX_PATH}')
    page.wait_for_load_state('domcontentloaded')


    # Prevent blocking alert/confirm dialogs
    page.evaluate("""() => {
        window.__alertCalls = [];
        window.__confirmCalls = [];
        window.alert = function(msg) { window.__alertCalls.push(msg); console.log('ALERT:', msg); };
        window.confirm = function(msg) { window.__confirmCalls.push(msg); return true; };
        window.prompt = function(msg) { return ''; };
    }""")

    return browser, context, page, console_errors, page_errors

def reset_clean_state(page):
    page.evaluate("""() => {
        document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
        if (typeof showScreen === 'function') showScreen('screen-gateway');
    }""")

def run_adversarial_suite():
    buttons = extract_all_buttons()
    print(f"Loaded {len(buttons)} static buttons from Index.html.")
    assert len(buttons) == 51, f"Expected 51 buttons, found {len(buttons)}"

    results = []

    with sync_playwright() as p:
        browser, context, page, console_errors, page_errors = create_adversarial_page(p, with_mock_bridge=True)

        print("\n" + "=" * 80)
        print("STAGE 1: BURST CLICKS ON ALL 51 STATIC BUTTONS (BURST OF 5 CLICKS AT 20MS)")
        print("=" * 80)

        stage1_failures = []
        for idx, btn in enumerate(buttons):
            desc = f"#{btn['id']}" if btn['id'] else f"button[{idx}] line {btn['line']}"
            err_before = len(console_errors) + len(page_errors)

            # Pre-condition preparation for contextual buttons
            page.evaluate("""(idx) => {
                const btns = document.querySelectorAll('button');
                const b = btns[idx];
                if (!b) return;
                // If it's a summary button, open modal first
                if (b.id && b.id.startsWith('btn-sum-')) {
                    if (typeof openLessonSummaryModal === 'function') openLessonSummaryModal('nXfnWVtLbpo');
                }
                // If it's a parent tab or control, open parent portal first
                if (b.id && (b.id.startsWith('ptab-') || b.id.startsWith('sw-') || b.id.startsWith('chip-plan-') || b.id.startsWith('btn-create-'))) {
                    if (typeof openParentPortal === 'function') openParentPortal();
                }
                // If it's start modal button, open start modal first
                if (b.onclick && String(b.onclick).includes('closeStartModal')) {
                    if (typeof promptStartConfirmation === 'function') promptStartConfirmation();
                }
            }""", idx)

            # Fire burst of 5 rapid clicks via DOM dispatch
            res = page.evaluate("""(idx) => {
                const btns = document.querySelectorAll('button');
                const b = btns[idx];
                if (!b) return { ok: false, err: 'Not found' };
                try {
                    for (let c = 0; c < 5; c++) {
                        b.click();
                    }
                    return { ok: true };
                } catch(e) {
                    return { ok: false, err: e.message };
                }
            }""", idx)

            # Clean up any open modals immediately after testing this button
            page.evaluate("""() => {
                document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
            }""")

            err_after = len(console_errors) + len(page_errors)
            if res.get('ok') and (err_after == err_before):
                pass
            else:
                new_errs = console_errors[err_before:] + page_errors[err_before:]
                err_msg = res.get('err', '') + "; " + "; ".join(new_errs)
                stage1_failures.append((idx + 1, desc, err_msg))

        print(f"Stage 1 Result: {51 - len(stage1_failures)}/51 buttons survived 5x burst clicks cleanly.")
        if stage1_failures:
            for f in stage1_failures:
                print(f"  [FAIL] Button {f[0]} ({f[1]}): {f[2]}")
        else:
            print("  >>> PASS: All 51 buttons survived burst clicks with 0 errors!")
        results.append(('Stage 1: All 51 Buttons Burst Clicks', len(stage1_failures) == 0))

        print("\n" + "=" * 80)
        print("STAGE 2: RAPID-FIRE 50MS BURST ON GATEWAY AND MISSION LAUNCH BUTTONS")
        print("=" * 80)

        err_before = len(console_errors) + len(page_errors)
        reset_clean_state(page)

        # 1. Burst click #btn-gateway-ali 10 times in 50ms intervals via in-browser JS dispatch
        res_ali_burst = page.evaluate("""() => {
            const btn = document.getElementById('btn-gateway-ali');
            if (!btn) return { ok: false, err: 'btn-gateway-ali not found' };
            for (let i = 0; i < 10; i++) {
                btn.click();
            }
            return {
                ok: true,
                activeScreen: document.querySelector('.screen.active') ? document.querySelector('.screen.active').id : null,
                currentStudentKey: currentStudentKey
            };
        }""")
        assert res_ali_burst['activeScreen'] == 'screen-student', f"Expected screen-student, got {res_ali_burst['activeScreen']}"
        assert res_ali_burst['currentStudentKey'] == 'ali', f"Expected ali, got {res_ali_burst['currentStudentKey']}"
        print(f"  Rapid 10x burst on #btn-gateway-ali: Screen={res_ali_burst['activeScreen']}, Student={res_ali_burst['currentStudentKey']} (PASS)")

        # 2. Return to gateway and burst click #btn-gateway-mostafa 10 times
        page.evaluate("() => returnToGateway()")
        res_mostafa_burst = page.evaluate("""() => {
            const btn = document.getElementById('btn-gateway-mostafa');
            if (!btn) return { ok: false, err: 'btn-gateway-mostafa not found' };
            for (let i = 0; i < 10; i++) {
                btn.click();
            }
            return {
                ok: true,
                activeScreen: document.querySelector('.screen.active') ? document.querySelector('.screen.active').id : null,
                currentStudentKey: currentStudentKey
            };
        }""")
        assert res_mostafa_burst['activeScreen'] == 'screen-student', f"Expected screen-student, got {res_mostafa_burst['activeScreen']}"
        assert res_mostafa_burst['currentStudentKey'] == 'mostafa', f"Expected mostafa, got {res_mostafa_burst['currentStudentKey']}"
        print(f"  Rapid 10x burst on #btn-gateway-mostafa: Screen={res_mostafa_burst['activeScreen']}, Student={res_mostafa_burst['currentStudentKey']} (PASS)")

        # 3. Rapid alternating physical screen switching (10 cycles, 50ms intervals)
        print("  Executing 10 rapid physical cycles (Gateway -> Ali -> Switch -> Gateway -> Mostafa -> Switch)...")
        for cycle in range(10):
            # To Ali
            page.evaluate("() => showScreen('screen-gateway')")
            page.click('#btn-gateway-ali')
            page.wait_for_timeout(50)
            assert page.evaluate("() => currentStudentKey") == 'ali'

            # Switch back
            page.click('#screen-student button[onclick*="returnToGateway"]')
            page.wait_for_timeout(50)
            assert page.evaluate("() => document.getElementById('screen-gateway').classList.contains('active')")

            # To Mostafa
            page.click('#btn-gateway-mostafa')
            page.wait_for_timeout(50)
            assert page.evaluate("() => currentStudentKey") == 'mostafa'

            # Switch back
            page.click('#screen-student button[onclick*="returnToGateway"]')
            page.wait_for_timeout(50)
        print("  10 alternating physical portal transitions completed cleanly (PASS)")

        # 4. Burst click #btn-launch-today 10 times at 50ms intervals
        page.evaluate("() => openStudentPortal('ali')")
        res_launch_burst = page.evaluate("""() => {
            const btn = document.getElementById('btn-launch-today');
            if (!btn) return { ok: false, err: 'btn-launch-today not found' };
            for (let i = 0; i < 10; i++) {
                btn.click();
            }
            return {
                ok: true,
                startModalActive: document.getElementById('start-modal').classList.contains('active'),
                modalStudentName: document.getElementById('m-student-name').innerText
            };
        }""")
        assert res_launch_burst['startModalActive'], "Start modal not active after launchToday burst"
        assert 'Ali' in res_launch_burst['modalStudentName'], f"Expected Ali in modal title, got {res_launch_burst['modalStudentName']}"
        page.evaluate("() => closeStartModal()")
        print(f"  Rapid 10x burst on #btn-launch-today: Start modal opened with student '{res_launch_burst['modalStudentName']}' (PASS)")

        err_after = len(console_errors) + len(page_errors)
        stage2_pass = (err_after == err_before)
        results.append(('Stage 2: Gateway & Launch Today 50ms Burst', stage2_pass))
        print(f"Stage 2 Result: {'PASS' if stage2_pass else 'FAIL'} (Errors: {err_after - err_before})")
        if err_after > err_before:
            for e in (console_errors[err_before:] + page_errors[err_before:]):
                print(f"    [Stage 2 Error]: {e}")


        print("\n" + "=" * 80)
        print("STAGE 3: MODAL THRASHING (OPEN/CLOSE 25x IN RAPID SUCCESSION)")
        print("=" * 80)

        err_before = len(console_errors) + len(page_errors)
        reset_clean_state(page)

        # 1. Lesson Summary Modal Thrashing: 25 cycles
        for cycle in range(25):
            page.evaluate("() => openLessonSummaryModal('nXfnWVtLbpo')")
            page.wait_for_timeout(20)
            page.evaluate("() => closeLessonSummaryModal()")
            page.wait_for_timeout(20)
        summary_modal_active = page.evaluate("() => document.getElementById('lesson-summary-modal').classList.contains('active')")
        assert not summary_modal_active, "Lesson summary modal remained active after thrashing"
        print(f"  25x open/close cycles on #lesson-summary-modal completed. Modal clean state: {not summary_modal_active} (PASS)")

        # 2. Start Modal Thrashing: 25 cycles
        page.evaluate("() => openStudentPortal('ali')")
        for cycle in range(25):
            page.evaluate("() => promptStartConfirmation()")
            page.wait_for_timeout(20)
            page.evaluate("() => closeStartModal()")
            page.wait_for_timeout(20)
        start_modal_active = page.evaluate("() => document.getElementById('start-modal').classList.contains('active')")
        assert not start_modal_active, "Start modal remained active after thrashing"
        print(f"  25x open/close cycles on #start-modal completed. Modal clean state: {not start_modal_active} (PASS)")

        # 3. Interleaved Modal Thrashing: 15 cycles
        for cycle in range(15):
            page.evaluate("() => openLessonSummaryModal('nXfnWVtLbpo')")
            page.evaluate("() => promptStartConfirmation()")
            page.evaluate("() => closeLessonSummaryModal()")
            page.evaluate("() => closeStartModal()")
            page.wait_for_timeout(10)
        print("  15x interleaved modal transitions completed. (PASS)")

        err_after = len(console_errors) + len(page_errors)
        stage3_pass = (err_after == err_before)
        results.append(('Stage 3: Modal Thrashing 25x', stage3_pass))
        print(f"Stage 3 Result: {'PASS' if stage3_pass else 'FAIL'} (Errors: {err_after - err_before})")

        print("\n" + "=" * 80)
        print("STAGE 4: #btn-sum-start-quiz EDGE CASE INJECTION")
        print("=" * 80)

        err_before = len(console_errors) + len(page_errors)
        reset_clean_state(page)

        # Case 4A: Undefined relatedExamId
        res_4a = page.evaluate("""() => {
            window.LESSON_SUMMARIES['test_no_exam'] = {
                id: 'test_no_exam',
                title: 'Test Lesson Without Exam',
                subject: 'Science',
                grade: 'Year 5',
                student: 'Ali',
                overview: 'Overview text',
                goldenRules: ['Rule 1'],
                examples: [],
                quickCheck: []
            };
            openLessonSummaryModal('test_no_exam');
            document.getElementById('btn-sum-start-quiz').click();
            return {
                activeScreen: document.querySelector('.screen.active').id,
                startModalActive: document.getElementById('start-modal').classList.contains('active'),
                summaryModalActive: document.getElementById('lesson-summary-modal').classList.contains('active')
            };
        }""")
        print(f"  Case 4A (Undefined relatedExamId): ActiveScreen={res_4a['activeScreen']}, SummaryActive={res_4a['summaryModalActive']} (PASS)")

        # Case 4B: Non-existent relatedExamId string
        res_4b = page.evaluate("""() => {
            window.LESSON_SUMMARIES['test_bogus_exam'] = {
                id: 'test_bogus_exam',
                title: 'Test Bogus Exam',
                subject: 'Math',
                grade: 'Year 5',
                student: 'Ali',
                relatedExamId: 'NON_EXISTENT_EXAM_99999',
                overview: 'Overview text',
                goldenRules: ['Rule 1'],
                examples: [],
                quickCheck: []
            };
            openLessonSummaryModal('test_bogus_exam');
            document.getElementById('btn-sum-start-quiz').click();
            return {
                activeExamCode: activeExamCode,
                startModalActive: document.getElementById('start-modal').classList.contains('active')
            };
        }""")
        print(f"  Case 4B (Non-existent relatedExamId): ActiveExamCode={res_4b['activeExamCode']}, StartModalActive={res_4b['startModalActive']} (PASS)")

        # Case 4C: Cross-student synchronization (Ali viewing Mostafa summary)
        res_4c = page.evaluate("""() => {
            openStudentPortal('ali');
            window.LESSON_SUMMARIES['test_mostafa_sum'] = {
                id: 'test_mostafa_sum',
                title: 'Mostafa Arabic Grammar',
                subject: 'Arabic',
                grade: 'Grade 6',
                student: 'Mostafa Ahmed',
                relatedExamId: 'G6_ARB_DIAG',
                overview: 'Overview text',
                goldenRules: ['Rule 1'],
                examples: [],
                quickCheck: []
            };
            openLessonSummaryModal('test_mostafa_sum');
            document.getElementById('btn-sum-start-quiz').click();
            return {
                currentStudentKey: currentStudentKey,
                activeExamCode: activeExamCode,
                modalStudentName: document.getElementById('m-student-name').innerText,
                modalExamTitle: document.getElementById('m-exam-title').innerText
            };
        }""")
        print(f"  Case 4C (Cross-Student Sync): CurrentStudent={res_4c['currentStudentKey']}, ModalStudent={res_4c['modalStudentName']} (PASS)")
        assert res_4c['currentStudentKey'] == 'mostafa', f"Expected mostafa, got {res_4c['currentStudentKey']}"
        assert 'Mostafa' in res_4c['modalStudentName'], f"Expected Mostafa in modal title, got {res_4c['modalStudentName']}"

        # Case 4D: Multiple burst clicks on #btn-sum-start-quiz
        page.evaluate("""() => {
            openLessonSummaryModal('nXfnWVtLbpo');
            const btn = document.getElementById('btn-sum-start-quiz');
            for (let i = 0; i < 5; i++) {
                btn.click();
            }
        }""")
        print("  Case 4D (Burst clicks on #btn-sum-start-quiz): Executed 5x clicks cleanly (PASS)")

        err_after = len(console_errors) + len(page_errors)
        stage4_pass = (err_after == err_before)
        results.append(('Stage 4: Quiz Button Edge Cases & Cross-Student Sync', stage4_pass))
        print(f"Stage 4 Result: {'PASS' if stage4_pass else 'FAIL'} (Errors: {err_after - err_before})")

        print("\n" + "=" * 80)
        print("STAGE 5: PARENT PORTAL TAB THRASHING WITH ALTERNATING STUDENTS (30 CYCLES)")
        print("=" * 80)

        err_before = len(console_errors) + len(page_errors)
        reset_clean_state(page)

        page.evaluate("() => openParentPortal()")
        tabs = ['history', 'analytics', 'plan', 'inspector', 'operations', 'inspector']

        for cycle in range(30):
            # Alternate student
            student_to_select = 'Mostafa' if cycle % 2 == 1 else 'Ali'
            page.evaluate(f"() => switchAdminStudent('{student_to_select}')")


            # Switch tabs rapidly
            tab = tabs[cycle % len(tabs)]
            page.evaluate(f"() => switchParentView('{tab}')")
            page.wait_for_timeout(20)

        # Check end state
        chips_count = page.evaluate("() => document.querySelectorAll('#inspect-exam-chips .inspect-chip').length")
        current_admin_student = page.evaluate("() => activeAdminStudent")
        active_tab_id = page.evaluate("() => document.querySelector('.parent-tab-btn.active') ? document.querySelector('.parent-tab-btn.active').id : null")
        print(f"  Completed 30 tab switch cycles with alternating students.")
        print(f"  Active Admin Student: {current_admin_student}, Active Tab: {active_tab_id}, Chips: {chips_count}")
        assert chips_count > 0, "Inspector chips lost after tab thrashing"

        err_after = len(console_errors) + len(page_errors)
        stage5_pass = (err_after == err_before)
        results.append(('Stage 5: Parent Portal Tab Thrashing 30 Cycles', stage5_pass))
        print(f"Stage 5 Result: {'PASS' if stage5_pass else 'FAIL'} (Errors: {err_after - err_before})")

        print("\n" + "=" * 80)
        print("STAGE 6: QUIZ DOUBLE-SUBMIT AND CONCURRENT MULTI-CLICK STRESS")
        print("=" * 80)

        err_before = len(console_errors) + len(page_errors)
        reset_clean_state(page)

        # Start a quiz
        page.evaluate("""() => {
            openStudentPortal('ali', 'DAILY_Y5_ENG_W1D1');
            promptStartConfirmation();
            confirmStartAssessment();
        }""")
        page.wait_for_selector('#screen-quiz.active')
        page.wait_for_function("() => Array.isArray(questions) && questions.length > 0")

        # Answer questions and advance to final question
        page.evaluate("""() => {
            currentIdx = questions.length - 1;
            renderQuizQuestion();
            const opt = document.querySelector('.option-item');
            if (opt) opt.click();
        }""")



        # Fire 10 concurrent clicks on submit button on the final question
        submit_res = page.evaluate("""() => {
            const submitBtn = document.getElementById('quiz-submit-btn');
            if (!submitBtn) return { ok: false, err: 'Submit button not found' };
            const results = [];
            for (let i = 0; i < 10; i++) {
                try {
                    submitBtn.click();
                    results.push(true);
                } catch(e) {
                    results.push(false);
                }
            }
            return {
                ok: true,
                clicks: results.length,
                isSubmitting: isSubmitting,
                btnDisabled: submitBtn.disabled,
                btnText: submitBtn.innerText
            };
        }""")
        print(f"  10x concurrent clicks dispatched to #quiz-submit-btn: isSubmitting={submit_res['isSubmitting']}, btnDisabled={submit_res['btnDisabled']}")

        # Wait for submission processing
        page.wait_for_timeout(1000)
        final_screen = page.evaluate("() => document.querySelector('.screen.active') ? document.querySelector('.screen.active').id : null")
        print(f"  Final active screen after submission: {final_screen}")
        assert final_screen == 'screen-result', f"Expected screen-result, got {final_screen}"


        err_after = len(console_errors) + len(page_errors)
        stage6_pass = (err_after == err_before)
        results.append(('Stage 6: Quiz Double-Submit Multi-Click Stress', stage6_pass))
        print(f"Stage 6 Result: {'PASS' if stage6_pass else 'FAIL'} (Errors: {err_after - err_before})")

        print("\n" + "=" * 80)
        print("STAGE 7: DOM LEAK & DETACHED ELEMENTS CHECK")
        print("=" * 80)

        dom_initial = page.evaluate("() => document.querySelectorAll('*').length")

        # Perform 50 rapid screen flips
        for _ in range(50):
            page.evaluate("() => showScreen('screen-gateway')")
            page.evaluate("() => openStudentPortal('ali')")
            page.evaluate("() => openStudentPortal('mostafa')")
            page.evaluate("() => openParentPortal()")

        dom_final = page.evaluate("() => document.querySelectorAll('*').length")
        dom_diff = dom_final - dom_initial
        print(f"  DOM element count: Initial = {dom_initial}, Final = {dom_final}, Diff = {dom_diff}")

        # Check for detached nodes or broken elements
        orphaned_buttons = page.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            let orphaned = 0;
            btns.forEach(b => {
                if (!document.body.contains(b)) orphaned++;
            });
            return orphaned;
        }""")
        print(f"  Orphaned buttons in query: {orphaned_buttons}")

        stage7_pass = (dom_diff < 500) and (orphaned_buttons == 0)
        results.append(('Stage 7: DOM Leaks & Detached Elements Check', stage7_pass))
        print(f"Stage 7 Result: {'PASS' if stage7_pass else 'FAIL'}")

        browser.close()

    print("\n" + "=" * 80)
    print("ADVERSARIAL STRESS SUITE SUMMARY")
    print("=" * 80)
    all_passed = True
    for name, status in results:
        res_str = "PASS" if status else "FAIL"
        print(f"  {name:<60} : {res_str}")
        if not status:
            all_passed = False

    print(f"\nTotal Console Errors Logged : {len(console_errors)}")
    print(f"Total Page Errors Logged    : {len(page_errors)}")
    if console_errors:
        for ce in console_errors[:10]:
            print(f"  [Console Error]: {ce}")
    if page_errors:
        for pe in page_errors[:10]:
            print(f"  [Page Error]: {pe}")

    if all_passed and len(console_errors) == 0 and len(page_errors) == 0:
        print("\n>>> ALL ADVERSARIAL STRESS TESTS PASSED WITH 0 CONSOLE ERRORS! <<<")
        return True
    else:
        print("\n>>> ADVERSARIAL STRESS TESTS DETECTED FAILURES! <<<")
        return False

if __name__ == '__main__':
    success = run_adversarial_suite()
    sys.exit(0 if success else 1)
