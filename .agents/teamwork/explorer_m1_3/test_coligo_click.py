from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html')
    
    # Check by clicking the actual DOM element
    btn = page.locator("button[onclick*=\"filterColigoHubItems('all')\"]")
    print("Found button:", btn.count())
    try:
        btn.click()
        print("Click succeeded!")
    except Exception as e:
        print("Click error:", e)

    # Check evaluate
    try:
        page.evaluate("filterColigoHubItems('all')")
        print("Evaluate succeeded!")
    except Exception as e:
        print("Evaluate error:", e)
    browser.close()
