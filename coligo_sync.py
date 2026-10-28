import os
import json
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\.coligo_session"
DOWNLOAD_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo"
AUTH_FILE = os.path.join(USER_DATA_DIR, "auth_state.json")

os.makedirs(USER_DATA_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

captured_tokens = {}

def handle_request(request):
    auth_header = request.headers.get("authorization")
    if auth_header and "Bearer" in auth_header:
        token = auth_header.split("Bearer")[-1].strip()
        captured_tokens["bearer"] = token
        captured_tokens["last_seen_url"] = request.url
        with open(AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(captured_tokens, f, indent=2)

def handle_response(response):
    url = response.url
    # Catch any courses / materials / students API calls
    if any(k in url.lower() for k in ["course", "student", "material", "worksheet", "assignment"]):
        try:
            if "application/json" in response.headers.get("content-type", ""):
                data = response.json()
                api_log_file = os.path.join(USER_DATA_DIR, "last_api_response.json")
                with open(api_log_file, "w", encoding="utf-8") as f:
                    json.dump({"url": url, "data": data}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

def main():
    print("=" * 60)
    print("  COLIGO LMS AUTOMATED SYNC & INGESTION ENGINE")
    print("=" * 60)
    print(f"📁 Session Storage: {USER_DATA_DIR}")
    print(f"📥 Downloads Folder: {DOWNLOAD_DIR}")
    print("Starting automated browser window...")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            accept_downloads=True,
            viewport=None
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        print("\nNavigating to https://coligolms.com/parent/courses ...")
        page.goto("https://coligolms.com/parent/courses", wait_until="commit", timeout=45000)
        
        print("\n>>> Log in if prompted, or browse through Ali and Mostafa's courses.")
        print(">>> The engine will automatically capture tokens, materials, and worksheets.")
        print(">>> Leave this window open or press Ctrl+C in this console when finished.\n")
        
        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nClosing browser and saving session...")
            context.close()

if __name__ == "__main__":
    main()
