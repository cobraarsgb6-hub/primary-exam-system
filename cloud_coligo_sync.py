#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
  AUTONOMOUS CLOUD COLIGO INGESTION PIPELINE (Full Online Sync)
  Runs 100% in the cloud on GitHub Actions
  Downloads all new worksheets, booklets, and lesson files for Ali & Mostafa
  Pushes metadata and homework updates directly to Google Sheets Webhook
================================================================================
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import zipfile
import io
import ssl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "resources", "coligo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Resolve Auth Token from Environment or local file
TOKEN = os.environ.get("COLIGO_TOKEN")
if not TOKEN:
    ls_file = os.path.join(OUTPUT_DIR, "local_storage.json")
    if os.path.exists(ls_file):
        with open(ls_file, "r", encoding="utf-8") as f:
            ls = json.load(f)
            TOKEN = ls.get("token")

if not TOKEN:
    print("[ERROR] No Coligo token found in environment (COLIGO_TOKEN) or local_storage.json")
    sys.exit(1)

WEBHOOK_URL = os.environ.get("GAS_WEBHOOK_URL")
SEMESTER_ID = "6aa6b7d7382ba9a416a84790"  # Trimester 1 (Sep 2026 - Jul 2027)

STUDENTS = [
    {"name": "Ali", "id": "68da68c843e7498ddb5573ba", "grade": "Year 5A"},
    {"name": "Mostafa", "id": "68e6ac96b5f1511f61d47eea", "grade": "Year 6A"}
]

HEADERS = {
    "Authorization": f"JWT {TOKEN}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SSL_CTX = ssl._create_unverified_context()

def clean_filename(name):
    if not name:
        return "file"
    for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\n', '\r', '\t']:
        name = name.replace(c, '_')
    return name.strip()[:100]

def safe_download_file(url, target_folder, preferred_name):
    os.makedirs(target_folder, exist_ok=True)
    clean_base = clean_filename(preferred_name)

    # Check if already downloaded and valid
    try:
        for existing in os.listdir(target_folder):
            if existing.startswith(clean_base) or clean_base.startswith(os.path.splitext(existing)[0]):
                existing_path = os.path.join(target_folder, existing)
                if os.path.getsize(existing_path) > 100:
                    return existing, False  # Already exists
    except Exception:
        pass

    req = urllib.request.Request(url, headers={"User-Agent": HEADERS["User-Agent"]})
    try:
        with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
            data = resp.read()
            if data[:4] == b'PK\x03\x04':  # ZIP archive
                try:
                    z = zipfile.ZipFile(io.BytesIO(data))
                    extracted_names = []
                    for zinfo in z.infolist():
                        extracted_path = z.extract(zinfo, target_folder)
                        extracted_names.append(os.path.basename(extracted_path))
                    return (extracted_names[0] if extracted_names else clean_base), True
                except Exception:
                    pass

            ext = ".pdf" if ".pdf" in url.lower() else (".docx" if ".docx" in url.lower() else (".pptx" if ".pptx" in url.lower() else ".bin"))
            final_name = clean_base
            if not any(final_name.lower().endswith(e) for e in [".pdf", ".docx", ".pptx", ".xlsx", ".zip", ".bin"]):
                final_name += ext
            dest_path = os.path.join(target_folder, final_name)
            with open(dest_path, "wb") as f:
                f.write(data)
            return final_name, True
    except Exception as e:
        print(f"      [Download Warning] {preferred_name}: {e}")
        return None, False

def run_sync():
    print("=" * 65)
    print("🚀 [Cloud Sync] Starting Full Autonomous Coligo Ingestion...")
    print("=" * 65)
    t0 = time.time()

    # Step 1: Notifications
    print("\n[1/3] 🔔 Fetching latest notifications, homework & announcements...")
    notif_url = "https://prod-api.coligolms.com/api/v0/users/me/notifications?limit=100"
    req_n = urllib.request.Request(notif_url, headers=HEADERS)
    notifs = []
    try:
        with urllib.request.urlopen(req_n, timeout=20, context=SSL_CTX) as resp:
            notifs = json.loads(resp.read().decode("utf-8"))
            with open(os.path.join(OUTPUT_DIR, "all_notifications.json"), "w", encoding="utf-8") as f:
                json.dump(notifs, f, ensure_ascii=False, indent=2)
            print(f"✅ Synced {len(notifs)} notifications successfully.")
    except Exception as e:
        print(f"⚠️ Notification fetch warning: {e}")

    homework_items = []
    for n in notifs:
        msg = n.get("message", "")
        if any(k in msg.lower() for k in ["homework", "واجب", "quiz", "announcement", "created in", "material"]):
            homework_items.append({
                "id": n.get("_id"),
                "date": n.get("createdAt"),
                "message": msg,
                "type": n.get("type"),
                "read": n.get("state") == "@notification-state/read"
            })

    # Step 2: Curriculum Courses and Materials
    print("\n[2/3] 📚 Ingesting curriculum materials & worksheets for Ali & Mostafa...")
    master_catalog = {
        "synced_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "semester_id": SEMESTER_ID,
        "school": "Manaret El-Eman British International School",
        "students": {}
    }
    curriculum_materials = {"Ali": {}, "Mostafa": {}}
    total_new_downloads = 0
    total_materials_indexed = 0

    for student in STUDENTS:
        s_name = student["name"]
        s_id = student["id"]
        s_grade = student["grade"]
        print(f"\n--- Processing Student: {s_name} ({s_grade}) ---")

        master_catalog["students"][s_name] = {"grade": s_grade, "courses": []}

        courses_url = f"https://prod-api.coligolms.com/api/v1/semesters/{SEMESTER_ID}/users/{s_id}/courses"
        req_c = urllib.request.Request(courses_url, headers=HEADERS)
        courses = []
        try:
            with urllib.request.urlopen(req_c, timeout=20, context=SSL_CTX) as resp_c:
                c_resp = json.loads(resp_c.read().decode("utf-8"))
                courses = c_resp.get("data", c_resp) if isinstance(c_resp, dict) else c_resp
        except Exception as e:
            print(f"❌ Courses fetch failed for {s_name}: {e}")
            continue

        print(f"  Found {len(courses)} enrolled courses.")

        for c in courses:
            c_id = c.get("_id")
            c_title = c.get("title") or c.get("name") or "Course"
            course_dir = os.path.join(OUTPUT_DIR, s_name, clean_filename(c_title))
            os.makedirs(course_dir, exist_ok=True)

            mat_url = f"https://prod-api.coligolms.com/api/v2/courses/{c_id}/materials"
            req_m = urllib.request.Request(mat_url, headers=HEADERS)
            materials = []
            try:
                with urllib.request.urlopen(req_m, timeout=20, context=SSL_CTX) as resp_m:
                    materials = json.loads(resp_m.read().decode("utf-8"))
            except Exception as e:
                print(f"  [!] Failed materials for {c_title}: {e}")

            total_materials_indexed += len(materials)
            curriculum_materials[s_name][c_title] = {
                "course_id": c_id,
                "total_items": len(materials),
                "materials": materials
            }

            file_items = [m for m in materials if m.get("type") == "@material-type/file" and m.get("url")]
            link_items = [m for m in materials if m.get("type") == "@material-type/link" and m.get("url")]

            course_files_log = []
            for f_item in file_items:
                f_title = f_item.get("title") or "Material"
                f_url = f_item.get("url")
                saved_as, is_new = safe_download_file(f_url, course_dir, f_title)
                if saved_as:
                    if is_new:
                        print(f"     ⬇️ [New Download]: {saved_as}")
                        total_new_downloads += 1
                    course_files_log.append({
                        "title": f_title,
                        "filename": saved_as,
                        "local_path": os.path.join(course_dir, saved_as),
                        "url": f_url
                    })

            master_catalog["students"][s_name]["courses"].append({
                "id": c_id,
                "title": c_title,
                "total_items": len(materials),
                "downloaded_files": course_files_log,
                "links": [{"title": l.get("title"), "url": l.get("url")} for l in link_items]
            })

    # Save catalogs
    with open(os.path.join(OUTPUT_DIR, "coligo_catalog.json"), "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, ensure_ascii=False, indent=2)

    with open(os.path.join(OUTPUT_DIR, "all_curriculum_materials.json"), "w", encoding="utf-8") as f:
        json.dump(curriculum_materials, f, ensure_ascii=False, indent=2)

    print(f"\n[Summary] Indexed: {total_materials_indexed} items | Newly downloaded: {total_new_downloads} files.")

    # Step 3: Push to Webhook
    if WEBHOOK_URL:
        print("\n[3/3] ☁️ Pushing live updates to Google Sheets Webhook...")
        payload = json.dumps({
            "action": "sync_coligo_feed",
            "secret": os.environ.get("SYNC_SECRET", "manaret_eleman_secure_sync"),
            "timestamp": time.time(),
            "notificationsCount": len(notifs),
            "materialsCount": total_materials_indexed,
            "homework": homework_items[:30]
        }).encode("utf-8")
        req_w = urllib.request.Request(WEBHOOK_URL, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req_w, timeout=25, context=SSL_CTX) as resp_w:
                res = resp_w.read().decode("utf-8")
                print("✅ Successfully pushed to Google Sheets Cloud Database:", res)
        except Exception as e:
            print("[Warning] Could not reach Google Apps Script webhook:", e)

    elapsed = time.time() - t0
    print(f"\n🎉 100% Autonomous Cloud Sync Completed in {elapsed:.2f}s!")

if __name__ == "__main__":
    run_sync()
