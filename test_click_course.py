import os
import json
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\.coligo_session"
OUTPUT_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo"

print("Starting test_click_course...")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=True,
        viewport={"width": 1400, "height": 900}
    )
    page = context.pages[0] if context.pages else context.new_page()

    print("Navigating to courses...")
    page.goto("https://coligolms.com/parent/courses", wait_until="domcontentloaded", timeout=30000)
    time.sleep(4)

    card = page.locator("button.MuiCardActionArea-root:has-text('ICT 105')").first
    if not card.is_visible(timeout=3000):
        card = page.locator("h4:has-text('ICT 105')").first

    print("Found ICT 105 card, clicking...")
    card.click()
    time.sleep(5)

    print("New Page URL:", page.url)
    print("New Page Title:", page.title())

    # Screenshot
    shot_path = os.path.join(OUTPUT_DIR, "ict_course_page.png")
    page.screenshot(path=shot_path, full_page=True)
    print("Saved screenshot:", shot_path)

    # Dump HTML
    html_path = os.path.join(OUTPUT_DIR, "ict_course_dump.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(page.content())
    print("Saved HTML dump:", html_path)

    context.close()
    print("Completed test_click_course!")
