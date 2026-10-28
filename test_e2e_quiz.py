from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html')
    
    # 1. Click Ali
    print('1. Clicking Ali Gateway...')
    page.click('[onclick*="ali"]')
    page.wait_for_timeout(300)
    assert page.evaluate("() => document.querySelector('#screen-student.active') !== null")
    print('   -> In Ali Student Portal')
    
    # 2. Check today mission button
    print('2. Launching Today Mission for Ali...')
    page.click('#btn-launch-today')
    page.wait_for_timeout(300)
    is_modal_active = page.evaluate("() => document.querySelector('#start-modal.active') !== null")
    print('   -> Start Modal active:', is_modal_active)
    assert is_modal_active
    
    # 3. Confirm Start Assessment
    print('3. Confirming Start Assessment...')
    page.click('#start-modal .btn-primary')
    page.wait_for_timeout(500)
    is_quiz_active = page.evaluate("() => document.querySelector('#screen-quiz.active') !== null")
    print('   -> Quiz Screen active:', is_quiz_active)
    assert is_quiz_active
    
    # 4. Check if questions loaded in local mode
    q_text = page.evaluate("() => document.getElementById('quiz-question-box')?.innerText")
    print('   -> Quiz Question Box text snippet:', q_text[:80].replace('\n', ' '))
    
    # 5. Switch to Gateway
    print('5. Returning to Gateway...')
    page.evaluate("() => showScreen('screen-gateway')")
    page.wait_for_timeout(300)
    
    # 6. Click Mostafa
    print('6. Clicking Mostafa Gateway...')
    page.click('[onclick*="mostafa"]')
    page.wait_for_timeout(300)
    assert page.evaluate("() => document.querySelector('#screen-student.active') !== null")
    print('   -> In Mostafa Student Portal')
    
    # 7. Check Mostafa Today Mission
    print('7. Launching Today Mission for Mostafa...')
    page.click('#btn-launch-today')
    page.wait_for_timeout(300)
    is_modal_active = page.evaluate("() => document.querySelector('#start-modal.active') !== null")
    print('   -> Start Modal active for Mostafa:', is_modal_active)
    assert is_modal_active
    
    # 8. Close Modal and Open Parent Portal
    page.click('#start-modal .btn-secondary')
    page.wait_for_timeout(300)
    print('8. Opening Parent Portal...')
    page.click('[onclick*="openParentPortal"]')
    page.wait_for_timeout(500)
    assert page.evaluate("() => document.querySelector('#screen-admin.active') !== null")
    print('   -> In Parent Portal')
    
    # 9. Switch to Analytics View
    print('9. Switching to Analytics View...')
    page.evaluate("() => switchParentView('analytics')")
    page.wait_for_timeout(300)
    ana_title = page.evaluate("() => document.getElementById('ana-student-title')?.innerText")
    print('   -> Analytics Title:', ana_title)
    
    # 10. Switch between Ali and Mostafa in Admin
    page.evaluate("() => switchAdminStudent('Mostafa')")
    page.wait_for_timeout(300)
    ana_title_m = page.evaluate("() => document.getElementById('ana-student-title')?.innerText")
    print('   -> Analytics Title for Mostafa:', ana_title_m)
    
    browser.close()
    print('ALL E2E QUIZ & PORTAL TESTS PASSED WITH 100% SUCCESS!')
