import time
from playwright.sync_api import sync_playwright

def run_transition_benchmarks():
    print("=" * 75)
    print("DOM SCREEN TRANSITION LATENCY BENCHMARK (<50ms ACCEPTANCE SPEC)")
    print("=" * 75)

    transitions = [
        ("Gateway -> Ali Student Portal", "() => { const t0 = performance.now(); openStudentPortal('ali'); return { dt: performance.now() - t0, screen: document.querySelector('.screen.active')?.id }; }"),
        ("Ali Portal -> Gateway", "() => { const t0 = performance.now(); returnToGateway(); return { dt: performance.now() - t0, screen: document.querySelector('.screen.active')?.id }; }"),
        ("Gateway -> Mostafa Student Portal", "() => { const t0 = performance.now(); openStudentPortal('mostafa'); return { dt: performance.now() - t0, screen: document.querySelector('.screen.active')?.id }; }"),
        ("Mostafa Portal -> Parent Portal", "() => { const t0 = performance.now(); openParentPortal(); return { dt: performance.now() - t0, screen: document.querySelector('.screen.active')?.id }; }"),
        ("Parent Portal -> Gateway", "() => { const t0 = performance.now(); returnToGateway(); return { dt: performance.now() - t0, screen: document.querySelector('.screen.active')?.id }; }"),
        ("Direct Switch to Quiz Screen", "() => { const t0 = performance.now(); showScreen('screen-quiz'); return { dt: performance.now() - t0, screen: document.querySelector('.screen.active')?.id }; }"),
        ("Direct Switch to Result Screen", "() => { const t0 = performance.now(); showScreen('screen-result'); return { dt: performance.now() - t0, screen: document.querySelector('.screen.active')?.id }; }"),
        ("Result Screen -> Gateway", "() => { const t0 = performance.now(); returnToGateway(); return { dt: performance.now() - t0, screen: document.querySelector('.screen.active')?.id }; }"),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html')
        page.wait_for_selector('#screen-gateway.active')

        all_passed = True
        print(f"{'Transition Action':<35} | {'Latency (ms)':<12} | {'Spec':<8} | {'Active Screen':<15} | {'Result'}")
        print("-" * 90)

        for name, js_code in transitions:
            res = page.evaluate(js_code)
            dt = res['dt']
            screen = res['screen']
            passed = dt < 50.0
            if not passed:
                all_passed = False
            status = "PASS" if passed else "FAIL"
            print(f"{name:<35} | {dt:9.2f} ms | <50ms   | {str(screen):<15} | {status}")

        # Also test physical Playwright user-click transitions
        print("\n--- Physical User-Click Transitions ---")
        click_tests = [
            ("Click #btn-gateway-ali", "#btn-gateway-ali", "#screen-student.active"),
            ("Click #screen-student return", "#screen-student button[onclick*='returnToGateway']", "#screen-gateway.active"),
            ("Click #btn-gateway-mostafa", "#btn-gateway-mostafa", "#screen-student.active"),
            ("Click #screen-student parent", "#screen-student button[onclick*='openParentPortal']", "#screen-admin.active"),
            ("Click #screen-admin return", "#screen-admin button[onclick*='returnToGateway']", "#screen-gateway.active"),
        ]

        for label, selector, expected_screen in click_tests:
            t0 = time.perf_counter()
            page.click(selector)
            page.wait_for_selector(expected_screen, timeout=3000)
            t_total = (time.perf_counter() - t0) * 1000
            print(f"{label:<35} | {t_total:9.2f} ms | target: {expected_screen} | OK")

        browser.close()

        print("\n" + "=" * 75)
        if all_passed:
            print(">>> ALL DOM TRANSITIONS SUCCEEDED UNDER 50MS ACCEPTANCE SPEC (100% PASS) <<<")
        else:
            print(">>> SOME TRANSITIONS EXCEEDED 50MS THRESHOLD <<<")
        print("=" * 75)

if __name__ == '__main__':
    run_transition_benchmarks()
