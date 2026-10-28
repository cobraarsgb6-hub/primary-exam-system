from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html')
    page.wait_for_selector('#screen-gateway.active')
    
    # 1. Warm up first
    page.evaluate("() => openStudentPortal('ali')")
    page.evaluate("() => returnToGateway()")
    
    # Measure warmed up transitions for Ali
    times_ali = []
    for _ in range(5):
        t0 = time.perf_counter()
        page.evaluate("() => openStudentPortal('ali')")
        times_ali.append((time.perf_counter() - t0) * 1000)
        page.evaluate("() => returnToGateway()")

    # Measure warmed up transitions for Mostafa
    times_mostafa = []
    for _ in range(5):
        t0 = time.perf_counter()
        page.evaluate("() => openStudentPortal('mostafa')")
        times_mostafa.append((time.perf_counter() - t0) * 1000)
        page.evaluate("() => returnToGateway()")

    print('Ali portal warmed transition times (ms):', [round(t, 2) for t in times_ali])
    print(f'Average warmed Ali transition: {sum(times_ali)/len(times_ali):.2f}ms')
    print('Mostafa portal warmed transition times (ms):', [round(t, 2) for t in times_mostafa])
    print(f'Average warmed Mostafa transition: {sum(times_mostafa)/len(times_mostafa):.2f}ms')

    browser.close()
