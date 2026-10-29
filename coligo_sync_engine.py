#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
  COLIGO LMS AUTOMATED FULL INGESTION & INCREMENTAL SYNC ENGINE
  Manaret El-Eman British International School
  Students: Ali Ahmed (Year 5A) & Mostafa Ahmed (Year 6A)
================================================================================
"""

import os
import sys
import json
import time
import zipfile
import io
import urllib.request
import urllib.error

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "resources", "coligo")

os.makedirs(OUTPUT_DIR, exist_ok=True)

TOKEN = os.environ.get("COLIGO_TOKEN")
if not TOKEN:
    print("[ERROR] Configure COLIGO_TOKEN in the environment; local credential files are not read.")
    sys.exit(1)
USER = {}
SEMESTER_ID = "6aa6b7d7382ba9a416a84790"  # Trimester 1 (Sep 2026 - Jul 2027)

STUDENTS = [
    {"name": "Ali", "id": "68da68c843e7498ddb5573ba", "grade": "Year 5A"},
    {"name": "Mostafa", "id": "68e6ac96b5f1511f61d47eea", "grade": "Year 6A"}
]


def ar(text):
    """
    Format Arabic text for terminal display:
    - If running in classic Windows CMD (no WT_SESSION), reshape & apply BiDi
      so characters are joined and read right-to-left properly.
    - If running in Windows Terminal (WT_SESSION present), native BiDi is active.
    """
    if not text or "WT_SESSION" in os.environ:
        return str(text)
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)

HEADERS = {
    "Authorization": f"JWT {TOKEN}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_filename(name):
    if not name:
        return "file"
    for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\n', '\r', '\t']:
        name = name.replace(c, '_')
    return name.strip()[:100]

def safe_download_file(url, target_folder, preferred_name):
    os.makedirs(target_folder, exist_ok=True)
    clean_base = clean_filename(preferred_name)

    # Check if already extracted or downloaded
    for existing in os.listdir(target_folder):
        if existing.startswith(clean_base) or clean_base.startswith(os.path.splitext(existing)[0]):
            existing_path = os.path.join(target_folder, existing)
            if os.path.getsize(existing_path) > 100:  # Valid existing file
                return existing, False  # Already exists

    req = urllib.request.Request(url, headers={"User-Agent": HEADERS["User-Agent"]})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
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

def sync_notifications():
    print("\n[1/3] 🔔 جاري سحب أحدث التنبيهات والدرجات والإعلانات المدرسية...")
    notif_url = "https://prod-api.coligolms.com/api/v0/users/me/notifications?limit=100"
    req = urllib.request.Request(notif_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            notifs = json.loads(resp.read().decode("utf-8"))
            notifs_path = os.path.join(OUTPUT_DIR, "all_notifications.json")
            with open(notifs_path, "w", encoding="utf-8") as f:
                json.dump(notifs, f, ensure_ascii=False, indent=2)
            print(ar(f"  ✓ تم سحب وتحديث {len(notifs)} إشعار بنجاح."))
            
            # Print top recent highlights
            print(ar("  📌 أحدث 3 تنبيهات من المدرسة:"))
            for n in notifs[:3]:
                msg = n.get("message") or n.get("title") or "تنبيه"
                ts = n.get("createdAt")
                t_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(ts/1000)) if ts else ""
                print(f"     • [{t_str}] {ar(msg)}")
            return notifs
    except Exception as e:
        print(f"  [Error fetching notifications] {e}")
        return []

def sync_all_curriculum():
    print("\n[2/3] 📚 جاري مزامنة كافة المواد والمقررات الدراسية لعلي ومصطفى...")
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
        
        print(f"\n=======================================================")
        print(ar(f"  الطالب: {s_name} ({s_grade})"))
        print(f"=======================================================")
        
        master_catalog["students"][s_name] = {
            "grade": s_grade,
            "courses": []
        }
        
        courses_url = f"https://prod-api.coligolms.com/api/v1/semesters/{SEMESTER_ID}/users/{s_id}/courses"
        req = urllib.request.Request(courses_url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                courses_resp = json.loads(resp.read().decode("utf-8"))
                courses = courses_resp.get("data", courses_resp) if isinstance(courses_resp, dict) else courses_resp
        except Exception as e:
            print(f"  [Error] Courses fetch failed for {s_name}: {e}")
            continue

        print(ar(f"  تم العثور على {len(courses)} مادة دراسية مسجلة."))

        for c in courses:
            c_id = c.get("_id")
            c_title = c.get("title") or c.get("name") or "Course"
            course_dir = os.path.join(OUTPUT_DIR, s_name, clean_filename(c_title))
            os.makedirs(course_dir, exist_ok=True)

            # Query materials
            mat_url = f"https://prod-api.coligolms.com/api/v2/courses/{c_id}/materials"
            req_m = urllib.request.Request(mat_url, headers=HEADERS)
            materials = []
            try:
                with urllib.request.urlopen(req_m, timeout=20) as resp_m:
                    materials = json.loads(resp_m.read().decode("utf-8"))
            except Exception as e:
                print(ar(f"    [!] تعذر سحب محتويات مادة {c_title}: {e}"))

            total_materials_indexed += len(materials)
            curriculum_materials[s_name][c_title] = {
                "course_id": c_id,
                "total_items": len(materials),
                "materials": materials
            }

            file_items = [m for m in materials if m.get("type") == "@material-type/file" and m.get("url")]
            link_items = [m for m in materials if m.get("type") == "@material-type/link" and m.get("url")]

            print(f"  -> {ar(c_title)}: {len(materials)} " + ar("عنصر") + f" ({len(file_items)} " + ar("ملفات") + " | " + f"{len(link_items)} " + ar("روابط") + ")")

            course_files_log = []
            for f_item in file_items:
                f_title = f_item.get("title") or "Material"
                f_url = f_item.get("url")
                
                saved_as, is_new = safe_download_file(f_url, course_dir, f_title)
                if saved_as:
                    if is_new:
                        print(f"     ⬇️ [" + ar("ملف جديد تم تحميله") + f"]: {ar(saved_as)}")
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

    # Save outputs
    catalog_path = os.path.join(OUTPUT_DIR, "coligo_catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, ensure_ascii=False, indent=2)

    all_mat_path = os.path.join(OUTPUT_DIR, "all_curriculum_materials.json")
    with open(all_mat_path, "w", encoding="utf-8") as f:
        json.dump(curriculum_materials, f, ensure_ascii=False, indent=2)

    print("\n[3/3] 💾 تم حفظ الفهارس وتحديث البيانات بنجاح:")
    print(ar(f"  • الملفات الجديدة التي تم تنزيلها: {total_new_downloads}"))
    print(ar(f"  • إجمالي المواد المفهرسة: {total_materials_indexed}"))
    print(ar(f"  • مسار كتالوج المواد: {all_mat_path}"))
    print(ar(f"  • مسار كتالوج التنزيلات: {catalog_path}"))

def main():
    print("=" * 65)
    print(ar("  🚀 مُحرك سحب ومزامنة بيانات كوليجو (Coligo LMS Sync Engine)"))
    print("=" * 65)
    t0 = time.time()
    sync_notifications()
    sync_all_curriculum()
    elapsed = time.time() - t0
    print("\n" + "=" * 65)
    print(ar(f"  ✨ اكتملت المزامنة بنجاح في {elapsed:.2f} ثانية!"))
    print("=" * 65)

if __name__ == "__main__":
    main()
