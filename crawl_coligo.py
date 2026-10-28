import os
import sys
import json
import time
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\.coligo_session"
OUTPUT_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo"
MANIFEST_FILE = os.path.join(OUTPUT_DIR, "coligo_manifest.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

manifest = {
    "scanned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "students": {
        "Ali": {"grade": "Year 5A", "courses": [], "announcements": [], "downloaded_files": []},
        "Mostafa": {"grade": "Year 6A", "courses": [], "announcements": [], "downloaded_files": []}
    }
}

def sanitize(name):
    if not name:
        return "untitled"
    for ch in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\n', '\r', '\t']:
        name = name.replace(ch, '_')
    return name.strip()[:80]

def download_attachment(page, element, dest_folder, fallback_name="attachment"):
    try:
        os.makedirs(dest_folder, exist_ok=True)
        with page.expect_download(timeout=6000) as download_info:
            element.click()
        download = download_info.value
        suggested = download.suggested_filename or (fallback_name + ".pdf")
        target_path = os.path.join(dest_folder, sanitize(suggested))
        download.save_as(target_path)
        print(f"      [✓ DOWNLOADED] {suggested} -> {target_path}")
        return target_path
    except Exception as e:
        # If no download triggered (maybe opened in tab or modal)
        return None

def process_student(page, student_name):
    print(f"\n=======================================================")
    print(f"  PROCESSING STUDENT: {student_name}")
    print(f"=======================================================")
    
    student_root = os.path.join(OUTPUT_DIR, student_name)
    os.makedirs(student_root, exist_ok=True)
    
    # 1. Switch to student if needed
    try:
        # Check current student shown in sidebar
        current_active = page.locator(".sidebar, [class*='sidebar'], nav").locator("text=Ali, text=Mostafa").first.inner_text()
        if student_name.lower() not in current_active.lower():
            print(f"Switching student to {student_name}...")
            # Click the child switcher dropdown
            switcher = page.locator("[class*='show-children'], [class*='child'], .v-select, div:has-text('Ali'):has-text('Mostafa')").first
            if switcher.is_visible(timeout=2000):
                switcher.click()
                time.sleep(1)
            # Click the student name
            target_btn = page.locator(f"text={student_name}").first
            target_btn.click()
            time.sleep(3)
    except Exception as e:
        print(f"Student switcher note: {e}")

    # 2. Check Dashboard Announcements & Weekly Plans
    print(f"\n--- Checking {student_name}'s Dashboard & Weekly Plans ---")
    page.goto("https://coligolms.com/parent/dashboard", wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # Find attachments in announcements (paperclip icons 📎 or links)
    announcements_box = page.locator("text=Announcements").first
    if announcements_box.is_visible(timeout=2000):
        pins = page.locator("svg[data-icon='paperclip'], i[class*='paperclip'], [class*='attach'], a[href*='.pdf'], a[href*='download'], svg:has-text('paperclip')").all()
        print(f"Found {len(pins)} attachment elements on Dashboard.")
        for idx, pin in enumerate(pins):
            try:
                dest = os.path.join(student_root, "Weekly_Plans_and_Announcements")
                saved = download_attachment(page, pin, dest, f"announcement_attachment_{idx+1}")
                if saved:
                    manifest["students"][student_name]["announcements"].append(saved)
            except Exception:
                pass

    # 3. Check Courses Page
    print(f"\n--- Checking {student_name}'s Courses ---")
    page.goto("https://coligolms.com/parent/courses", wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # Find course cards
    cards = page.locator("div[class*='card'], div[class*='course'], div:has(> h3), div:has(> h4)").all()
    print(f"Found {len(cards)} course elements.")

    # Collect course names and links
    course_links = []
    # Search for all clickable course headings or cards
    headings = page.locator("h3, h4, [class*='title'], [class*='subject']").all()
    for h in headings:
        try:
            txt = h.inner_text().strip()
            if any(term in txt.lower() for term in ["105", "106", "math", "science", "english", "arabic", "social", "french", "ict", "literature"]):
                if txt not in [c["name"] for c in course_links]:
                    # Find clickable ancestor or link
                    parent_link = h.locator("xpath=ancestor-or-self::a | xpath=ancestor::div[contains(@class,'card')]").first
                    course_links.append({"name": txt, "element": h})
        except Exception:
            pass

    print(f"Detected {len(course_links)} verified courses: {[c['name'] for c in course_links]}")
    manifest["students"][student_name]["courses"] = [c["name"] for c in course_links]

    # Visit each course
    for c_info in course_links:
        c_name = c_info["name"]
        print(f"\n>> Scanning Materials for: {c_name} ...")
        c_folder = os.path.join(student_root, sanitize(c_name))
        os.makedirs(c_folder, exist_ok=True)
        
        try:
            page.goto("https://coligolms.com/parent/courses", wait_until="domcontentloaded", timeout=20000)
            time.sleep(2)
            c_target = page.locator(f"text={c_name}").first
            if c_target.is_visible(timeout=2000):
                c_target.click()
                time.sleep(3)
                print(f"  Current Course URL: {page.url}")

                # Look for sub-tabs: Materials, Worksheets, Content, Assignments
                for tab_text in ["Materials", "Content", "Worksheets", "Resources", "Assignments", "شيتات", "المحتوى"]:
                    tab = page.locator(f"text={tab_text}").first
                    if tab.is_visible(timeout=1000):
                        print(f"  Switching to {tab_text} tab...")
                        tab.click()
                        time.sleep(2)

                # Find all downloadable files (pdf, pptx, docx, links with download)
                file_items = page.locator("a[href*='.pdf'], a[href*='.doc'], a[href*='.ppt'], button:has-text('Download'), [class*='download'], svg[data-icon='download'], i[class*='download']").all()
                print(f"  Found {len(file_items)} download targets in {c_name}.")
                for f_idx, f_elem in enumerate(file_items):
                    try:
                        title_text = f_elem.inner_text().strip() or f"Material_{f_idx+1}"
                        saved = download_attachment(page, f_elem, c_folder, title_text)
                        if saved:
                            manifest["students"][student_name]["downloaded_files"].append({
                                "course": c_name,
                                "file": saved
                            })
                    except Exception:
                        pass
        except Exception as e:
            print(f"  Error crawling course {c_name}: {e}")

def main():
    print("=" * 60)
    print("  COLIGO LMS AUTONOMOUS SCRAPER & SYNC")
    print("=" * 60)
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            accept_downloads=True,
            viewport={"width": 1366, "height": 768}
        )
        page = context.pages[0] if context.pages else context.new_page()

        print("\nNavigating to Dashboard...")
        page.goto("https://coligolms.com/parent/dashboard", wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)

        if "login" in page.url.lower():
            print("⚠️ Session expired or not found. Please log in.")
            return

        print("✓ Logged in session active! Starting automated extraction...")
        
        # Process Ali (Year 5)
        process_student(page, "Ali")
        
        # Process Mostafa (Grade 6)
        process_student(page, "Mostafa")

        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        print("\n" + "=" * 60)
        print("  ✓ COLIGO CRAWL FINISHED SUCCESSFULLY!")
        print(f"  📁 Output Directory: {OUTPUT_DIR}")
        print(f"  📄 Manifest File: {MANIFEST_FILE}")
        print("=" * 60)
        time.sleep(3)
        context.close()

if __name__ == "__main__":
    main()
