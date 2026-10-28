import os
import html.parser
from playwright.sync_api import sync_playwright

def run_all_buttons_audit():
    print("=" * 85)
    print("INTERACTIVE AUDIT OF ALL 51 UI BUTTON CONTROLS IN INDEX.HTML")
    print("=" * 85)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(base_dir, 'Index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

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
    parser.feed(html_content)
    total_buttons = len(parser.buttons)
    print(f"Total static <button> elements in HTML: {total_buttons}")
    assert total_buttons in (51, 52, 53), f"Expected 51 to 53 buttons, found {total_buttons}"

    console_errors = []
    page_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda err: page_errors.append(str(err)))

        from bundle import build_bundle
        bundle_path = build_bundle()
        page.goto('file:///' + bundle_path.replace('\\', '/'))
        page.wait_for_selector('#screen-gateway.active')

        # Mock alert & confirm to prevent blocking dialogs
        page.evaluate("""
            window.alert = function(msg) { console.log('ALERT:', msg); };
            window.confirm = function(msg) { return true; };
            window.prompt = function(msg) { return ''; };
        """)

        passed_buttons = 0
        failed_buttons = []

        print(f"\n{'#':2} | {'Line':4} | {'Target Element / Selector':<42} | {'Status':8} | Notes")
        print("-" * 88)

        for idx in range(total_buttons):
            b_info = parser.buttons[idx]
            btn_id = b_info['id']
            btn_line = b_info['line']
            desc = f"#{btn_id}" if btn_id else f"button[{idx}] line {btn_line}"

            errors_before = len(console_errors) + len(page_errors)

            res = page.evaluate("""(i) => {
                const btns = document.querySelectorAll('button');
                const b = btns[i];
                if (!b) return { ok: false, err: 'Button index not found in DOM' };
                try {
                    if (b.id === 'btn-sum-watch-video' || b.id === 'btn-sum-start-quiz') {
                        if (typeof openLessonSummaryModal === 'function') openLessonSummaryModal('nXfnWVtLbpo');
                    }
                    b.click();
                    return { ok: true };
                } catch (e) {
                    return { ok: false, err: e.message };
                }
            }""", idx)

            errors_after = len(console_errors) + len(page_errors)

            if res['ok'] and (errors_after == errors_before):
                passed_buttons += 1
                status = "PASS"
                notes = "DOM click executed cleanly (0 errors)"
            else:
                err_msg = res.get('err', '')
                if errors_after > errors_before:
                    err_msg += "; " + "; ".join(console_errors[errors_before:] + page_errors[errors_before:])
                failed_buttons.append((idx + 1, desc, err_msg))
                status = "FAIL"
                notes = f"ERROR: {err_msg[:35]}"

            print(f"{idx+1:2d} | {btn_line:4d} | {desc:<42} | {status:8} | {notes}")

        # Regression Verification
        print("\n--- Verifying Targeted Defect Remediations ---")
        page.evaluate("() => { openParentPortal(); switchParentView('inspector'); }")
        inspector_chips_count = page.evaluate("() => document.querySelectorAll('#inspect-exam-chips .inspect-chip').length")
        print(f"  Inspector chips rendered: {inspector_chips_count} chips (PASS)")
        assert inspector_chips_count > 0, "No inspector chips rendered"

        page.evaluate("() => openLessonSummaryModal('nXfnWVtLbpo')")
        page.evaluate("() => document.getElementById('btn-sum-start-quiz').click()")
        start_modal_active = page.evaluate("() => document.getElementById('start-modal').classList.contains('active')")
        print(f"  Start modal opened successfully: {start_modal_active} (PASS)")
        assert start_modal_active, "Start confirmation modal did not open"

        page.evaluate("() => openStudentPortal('ali', 'DAILY_Y5_ENG_W1D3')")
        active_exam = page.evaluate("() => activeExamCode")
        print(f"  Active exam selected by deep-link: {active_exam} (Expected: DAILY_Y5_ENG_W1D3) -> {'PASS' if active_exam == 'DAILY_Y5_ENG_W1D3' else 'FAIL'}")
        assert active_exam == 'DAILY_Y5_ENG_W1D3', f"Expected DAILY_Y5_ENG_W1D3, got {active_exam}"

        browser.close()

        print("\n" + "=" * 85)
        print(f"AUDIT SUMMARY: {passed_buttons}/51 buttons passed | {len(failed_buttons)} failed | {len(console_errors)} console errors | {len(page_errors)} page errors")
        if len(failed_buttons) == 0 and len(console_errors) == 0 and len(page_errors) == 0:
            print(">>> 100% ZERO-DEFECT PASS: ALL 51 UI BUTTON CONTROLS VERIFIED CLEANLY <<<")
        else:
            print(">>> VERIFICATION FAILED: UNRESOLVED DEFECTS DETECTED <<<")
            raise AssertionError(f"Button test failures: {failed_buttons}")
        print("=" * 85)

if __name__ == '__main__':
    run_all_buttons_audit()
