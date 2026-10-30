import os
from playwright.sync_api import sync_playwright

def test_multisubject_and_filtering():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "Index.html").replace("\\", "/")
    url = f"file:///{file_path}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        
        console_errors = []
        page.on("pageerror", lambda err: console_errors.append(str(err)))
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        
        mock_bridge_path = os.path.join(base_dir, "tests", "e2e", "mock_bridge.js")
        if os.path.exists(mock_bridge_path):
            page.add_init_script(path=mock_bridge_path)
        page.goto(url)
        page.wait_for_timeout(300)
        
        print("=== Test 1: Enter Mostafa Portal & Test Subject Filtering ===")
        page.click("#btn-gateway-mostafa")
        page.wait_for_timeout(200)
        if page.query_selector("#portal-access-pin"):
            page.fill("#portal-access-pin", "2014")
            page.click("#portal-access-submit")
            page.wait_for_timeout(300)

        # In Coligo view, Today's Hub is default. Click Exam Center tab!
        print("Switching to Coligo Exam Center Tab...")
        page.click("#tab-nav-exams")
        page.wait_for_timeout(150)
        
        # Check initial cards count
        all_cards_count = page.evaluate("() => document.querySelectorAll('#sp-exams-list .exam-item-card').length")
        print(f"Total Mostafa exams shown initially: {all_cards_count}")
        assert all_cards_count >= 20, f"Expected at least 20 exams for Mostafa, got {all_cards_count}"
        
        # Click Math Subject Filter
        print("Clicking Math Subject Filter...")
        page.click("#esubj-MATH")
        page.wait_for_timeout(150)
        
        math_cards = page.evaluate("() => Array.from(document.querySelectorAll('#sp-exams-list .exam-item-card .exam-item-title')).map(e => e.innerText)")
        print(f"Mostafa Math cards ({len(math_cards)}):", math_cards)
        assert len(math_cards) >= 5, f"Expected at least 5 Math exams, got {len(math_cards)}"
        assert all("Math" in title or "Prime" in title or "Fraction" in title or "Division" in title for title in math_cards)
        
        # Click Science Subject Filter
        print("Clicking Science Subject Filter...")
        page.click("#esubj-SCIENCE")
        page.wait_for_timeout(150)
        sci_cards = page.evaluate("() => Array.from(document.querySelectorAll('#sp-exams-list .exam-item-card .exam-item-title')).map(e => e.innerText)")
        print(f"Mostafa Science cards ({len(sci_cards)}):", sci_cards)
        assert len(sci_cards) >= 3, f"Expected at least 3 Science exams, got {len(sci_cards)}"
        assert all("Science" in title or "Circulatory" in title or "Circuits" in title for title in sci_cards)

        # Click Arabic Subject Filter
        print("Clicking Arabic Subject Filter...")
        page.click("#esubj-ARABIC")
        page.wait_for_timeout(150)
        arb_cards = page.evaluate("() => Array.from(document.querySelectorAll('#sp-exams-list .exam-item-card .exam-item-title')).map(e => e.innerText)")
        print(f"Mostafa Arabic cards ({len(arb_cards)}):", arb_cards[:3], f"... (+ {len(arb_cards)-3} more)")
        assert len(arb_cards) >= 11, f"Expected at least 11 Arabic exams, got {len(arb_cards)}"

        # Combined Filter: Math + Daily
        print("Clicking Combined Filter: Math + Daily...")
        page.click("#esubj-MATH")
        page.wait_for_timeout(100)
        page.click("#efilter-DAILY")
        page.wait_for_timeout(150)
        daily_math = page.evaluate("() => Array.from(document.querySelectorAll('#sp-exams-list .exam-item-card .exam-item-title')).map(e => e.innerText)")
        print("Mostafa Daily Math cards:", daily_math)
        assert len(daily_math) == 3, f"Expected 3 Daily Math exams (D1, D2, D3), got {len(daily_math)}"

        # Start a Math Quiz
        print("Starting Math Quiz (DAILY_Y6_MATH_W1D1)...")
        page.evaluate("() => { selectStudentExam('DAILY_Y6_MATH_W1D1'); promptStartConfirmation(); }")
        page.wait_for_timeout(200)
        page.evaluate("() => confirmStartAssessment()")
        page.wait_for_timeout(300)
        
        # Verify quiz screen
        is_quiz_active = page.evaluate("() => document.getElementById('screen-quiz').classList.contains('active')")
        assert is_quiz_active, "Quiz screen should be active"
        
        q_text = page.evaluate("() => document.querySelector('.q-text')?.innerText")
        print("Loaded Question Text:", q_text)
        assert q_text and "prime factorization of 36" in q_text.lower(), f"Expected prime factor question, got: {q_text}"
        
        # Answer question 1
        page.click(".option-item:first-child")
        page.wait_for_timeout(100)
        is_selected = page.evaluate("() => document.querySelector('.option-item:first-child').classList.contains('selected')")
        assert is_selected, "Option should be selected"
        print("Answer selection verified successfully!")

        # Return to gateway
        page.evaluate("() => returnToGateway()")
        page.wait_for_timeout(200)

        print("\n=== Test 2: Enter Ali Portal & Test Multi-Subject ===")
        page.click("#btn-gateway-ali")
        page.wait_for_timeout(200)
        if page.query_selector("#portal-access-pin"):
            page.fill("#portal-access-pin", "2016")
            page.click("#portal-access-submit")
            page.wait_for_timeout(300)

        # Switch to Exam Center tab
        page.click("#tab-nav-exams")
        page.wait_for_timeout(150)

        # Filter Math for Ali
        page.click("#esubj-MATH")
        page.wait_for_timeout(150)
        ali_math = page.evaluate("() => Array.from(document.querySelectorAll('#sp-exams-list .exam-item-card .exam-item-title')).map(e => e.innerText)")
        print(f"Ali Math cards ({len(ali_math)}):", ali_math)
        assert len(ali_math) >= 4, f"Expected at least 4 Math exams for Ali, got {len(ali_math)}"
        assert any("Divisibility" in t for t in ali_math)

        # Filter Science for Ali
        page.click("#esubj-SCIENCE")
        page.wait_for_timeout(150)
        ali_sci = page.evaluate("() => Array.from(document.querySelectorAll('#sp-exams-list .exam-item-card .exam-item-title')).map(e => e.innerText)")
        print(f"Ali Science cards ({len(ali_sci)}):", ali_sci)
        assert len(ali_sci) >= 3, f"Expected at least 3 Science exams for Ali, got {len(ali_sci)}"
        assert any("Sound" in t for t in ali_sci)

        # Filter Arabic for Ali
        page.click("#esubj-ARABIC")
        page.wait_for_timeout(150)
        ali_arb = page.evaluate("() => Array.from(document.querySelectorAll('#sp-exams-list .exam-item-card .exam-item-title')).map(e => e.innerText)")
        print(f"Ali Arabic cards ({len(ali_arb)}):", ali_arb)
        assert len(ali_arb) >= 2, f"Expected at least 2 Arabic exams for Ali, got {len(ali_arb)}"
        assert any("الجملة الاسمية" in t for t in ali_arb)

        print("\n=== Verification Summary ===")
        print("Console errors count:", len(console_errors))
        if console_errors:
            print("Errors:", console_errors)
        assert len(console_errors) == 0, f"Found console errors: {console_errors}"
        print(">>> 100% PASS: Multi-Subject Selector, Dual Filtering & Real Question Generation Tested Cleanly! <<<")
        
        browser.close()

if __name__ == "__main__":
    test_multisubject_and_filtering()
