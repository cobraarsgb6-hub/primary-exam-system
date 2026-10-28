import os
import json
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\.coligo_session"
OUTPUT_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo"

captured = []

def on_request(req):
    if "coligo" in req.url:
        captured.append({
            "url": req.url,
            "method": req.method,
            "headers": {k: v for k, v in req.headers.items() if k in ["authorization", "content-type", "accept"]}
        })

def on_response(res):
    url = res.url
    if "prod-api.coligolms.com" in url:
        try:
            body = res.json()
            captured.append({
                "url": url,
                "status": res.status,
                "data": body
            })
            print(f"[API {res.status}] {url}")
        except Exception:
            pass

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=True,
        viewport={"width": 1400, "height": 900}
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.on("request", on_request)
    page.on("response", on_response)

    print("Navigating to https://coligolms.com/parent/courses ...")
    page.goto("https://coligolms.com/parent/courses", wait_until="domcontentloaded", timeout=30000)
    time.sleep(6)

    print("Navigating to https://coligolms.com/parent/dashboard ...")
    page.goto("https://coligolms.com/parent/dashboard", wait_until="domcontentloaded", timeout=30000)
    time.sleep(6)

    context.close()

with open(os.path.join(OUTPUT_DIR, "network_traffic.json"), "w", encoding="utf-8") as f:
    json.dump(captured, f, ensure_ascii=False, indent=2)

print("\nSaved network traffic. Total entries:", len(captured))
