from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html')
    
    # First navigate to Parent Portal Operations tab where the button lives
    page.evaluate("() => { openParentPortal(); switchParentView('operations'); }")
    
    # Now click the button via DOM click()
    res = page.evaluate("""() => {
        const btn = document.querySelector("#coligo-filter-chips button");
        try {
            btn.click();
            return { success: true };
        } catch (e) {
            return { success: false, error: e.message };
        }
    }""")
    print("DOM click result:", res)
    browser.close()
