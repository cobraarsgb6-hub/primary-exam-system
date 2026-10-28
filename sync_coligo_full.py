import os
import json
import urllib.request
import urllib.error
import zipfile
import io
import time
import re

OUTPUT_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo"
LS_FILE = os.path.join(OUTPUT_DIR, "local_storage.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(LS_FILE, "r", encoding="utf-8") as f:
    ls = json.load(f)

token = ls.get("token")
user = json.loads(ls.get("user", "{}"))
semester_id = "6aa6b7d7382ba9a416a84790" # Trimester 1 (Sep 2026 - Jul 2027)

students = [
    {"name": "Ali", "id": "68da68c843e7498ddb5573ba", "grade": "Year 5A"},
    {"name": "Mostafa", "id": "68e6ac96b5f1511f61d47eea", "grade": "Year 6A"}
]

headers = {
    "Authorization": f"JWT {token}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def clean_name(n):
    if not n:
        return "file"
    for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
        n = n.replace(c, '_')
    return n.strip()

def download_file(url, target_folder, preferred_name):
    os.makedirs(target_folder, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if data[:4] == b'PK\x03\x04': # Zip file
                try:
                    z = zipfile.ZipFile(io.BytesIO(data))
                    extracted_names = []
                    for zinfo in z.infolist():
                        extracted_path = z.extract(zinfo, target_folder)
                        extracted_names.append(os.path.basename(extracted_path))
                    return extracted_names[0] if extracted_names else preferred_name
                except Exception:
                    pass
            
            # Direct binary file
            ext = ".pdf" if ".pdf" in url.lower() else (".pptx" if ".pptx" in url.lower() else ".bin")
            final_name = clean_name(preferred_name)
            if not final_name.endswith(ext):
                final_name += ext
            dest_path = os.path.join(target_folder, final_name)
            with open(dest_path, "wb") as f:
                f.write(data)
            return final_name
    except Exception as e:
        print(f"      [Download Error] {e}")
        return None

catalog = {
    "synced_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "semester": "Trimester 1 (2026/2027)",
    "students": {}
}

print("=" * 65)
print("  COLIGO LMS AUTOMATED FULL INGESTION & DOWNLOAD ENGINE")
print("=" * 65)

total_downloaded = 0

for student in students:
    s_name = student["name"]
    s_id = student["id"]
    s_grade = student["grade"]
    print(f"\n=======================================================")
    print(f"  STUDENT: {s_name} ({s_grade})")
    print(f"=======================================================")
    
    catalog["students"][s_name] = {
        "grade": s_grade,
        "courses": []
    }
    
    courses_url = f"https://prod-api.coligolms.com/api/v1/semesters/{semester_id}/users/{s_id}/courses"
    req = urllib.request.Request(courses_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            courses_resp = json.loads(resp.read().decode("utf-8"))
            courses = courses_resp.get("data", courses_resp) if isinstance(courses_resp, dict) else courses_resp
    except Exception as e:
        print(f"Error fetching courses for {s_name}: {e}")
        continue

    print(f"Found {len(courses)} registered courses.")

    for c in courses:
        c_id = c.get("_id")
        c_title = c.get("title") or c.get("name") or "Course"
        print(f"\n-> [{c_title}] (ID: {c_id})")

        course_folder = os.path.join(OUTPUT_DIR, s_name, clean_name(c_title))
        os.makedirs(course_folder, exist_ok=True)

        course_data = {
            "id": c_id,
            "title": c_title,
            "materials_count": 0,
            "files": []
        }

        # Fetch materials
        mat_url = f"https://prod-api.coligolms.com/api/v2/courses/{c_id}/materials"
        req_m = urllib.request.Request(mat_url, headers=headers)
        try:
            with urllib.request.urlopen(req_m, timeout=20) as resp_m:
                materials = json.loads(resp_m.read().decode("utf-8"))
        except Exception as e:
            print(f"   Could not fetch materials: {e}")
            catalog["students"][s_name]["courses"].append(course_data)
            continue

        file_items = [m for m in materials if m.get("type") == "@material-type/file" and m.get("url")]
        course_data["materials_count"] = len(file_items)
        print(f"   Total downloadable files: {len(file_items)}")

        for f_item in file_items:
            f_title = f_item.get("title") or "Material"
            f_url = f_item.get("url")
            print(f"   ⬇️ Downloading: {f_title[:45]}...")
            
            saved_as = download_file(f_url, course_folder, f_title)
            if saved_as:
                print(f"      [✓ SAVED] {saved_as}")
                total_downloaded += 1
                course_data["files"].append({
                    "title": f_title,
                    "filename": saved_as,
                    "local_path": os.path.join(course_folder, saved_as),
                    "url": f_url
                })

        catalog["students"][s_name]["courses"].append(course_data)

catalog_path = os.path.join(OUTPUT_DIR, "coligo_catalog.json")
with open(catalog_path, "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 65)
print(f"  ✓ FULL SYNC FINISHED SUCCESSFULLY!")
print(f"  📦 Total Files Downloaded & Extracted: {total_downloaded}")
print(f"  📁 Location: {OUTPUT_DIR}")
print(f"  📄 Master Catalog: {catalog_path}")
print("=" * 65)
