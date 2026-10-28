from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html')
    
    # 1. Gateway
    print("1. Gateway open")
    
    # 2. Click Ali
    page.click('#btn-gateway-ali')
    page.wait_for_timeout(500)
    
    # 3. Check exams list in Ali portal
    exams_ali = page.evaluate("() => Array.from(document.querySelectorAll('.exam-item-card')).map(c => c.innerText)")
    print('Ali exams count:', len(exams_ali))
    for e in exams_ali[:4]:
        print('  Ali Exam:', e.replace('\n', ' -- '))
        
    # Check refresher notes
    refresher_ali = page.evaluate("() => document.getElementById('sp-refresher-container')?.innerText")
    print('Ali refresher text length:', len(refresher_ali or ''))
    print('Ali refresher snippet:', (refresher_ali or '')[:150].replace('\n', ' '))
    
    # 4. Return to Gateway
    page.click('[onclick*="returnToGateway"]')
    page.wait_for_timeout(300)
    
    # 5. Click Mostafa
    page.click('#btn-gateway-mostafa')
    page.wait_for_timeout(500)
    
    exams_mostafa = page.evaluate("() => Array.from(document.querySelectorAll('.exam-item-card')).map(c => c.innerText)")
    print('Mostafa exams count:', len(exams_mostafa))
    for e in exams_mostafa[:4]:
        print('  Mostafa Exam:', e.replace('\n', ' -- '))
        
    refresher_mostafa = page.evaluate("() => document.getElementById('sp-refresher-container')?.innerText")
    print('Mostafa refresher snippet:', (refresher_mostafa or '')[:150].replace('\n', ' '))
    
    # 6. Click Parent Portal
    page.click('[onclick*="openParentPortal"]')
    page.wait_for_timeout(600)
    
    # 7. Check Study Plan tab
    page.evaluate("() => switchParentView('plan')")
    page.wait_for_timeout(500)
    plan_text = page.evaluate("() => document.getElementById('admin-plan-container')?.innerText")
    print('Study plan text length:', len(plan_text or ''))
    print('Study plan snippet:\n', (plan_text or '')[:400])
    
    # 8. Filter to W1
    page.evaluate("() => filterPlanByWeek('W1')")
    page.wait_for_timeout(300)
    plan_w1_text = page.evaluate("() => document.getElementById('admin-plan-container')?.innerText")
    print('\nW1 filtered length:', len(plan_w1_text or ''))
    print('W1 filtered snippet:\n', (plan_w1_text or '')[:300])

    browser.close()
