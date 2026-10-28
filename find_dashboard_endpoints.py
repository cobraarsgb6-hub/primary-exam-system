import os
import json
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\.coligo_session"

endpoints = []

def on_request(req):
    if "prod-api.coligolms.com" in req.url:
        endpoints.append({"url": req.url, "method": req.method})
        print(f"[{req.method}] {req.url}")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=True
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.on("request", on_request)

    print("\n>>> Visiting Dashboard...")
    page.goto("https://coligolms.com/parent/dashboard", wait_until="domcontentloaded", timeout=30000)
    time.sleep(4)

    print("\n>>> Visiting Gradebook...")
    page.goto("https://coligolms.com/parent/gradebook", wait_until="domcontentloaded", timeout=30000)
    time.sleep(4)

    print("\n>>> Visiting Announcements...")
    page.goto("https://coligolms.com/parent/announcements", wait_until="domcontentloaded", timeout=30000)
    time.sleep(4)

    context.close()
