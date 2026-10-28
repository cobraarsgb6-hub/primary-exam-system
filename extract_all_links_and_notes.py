import json
import urllib.request
import os

OUTPUT_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo"
LS_FILE = os.path.join(OUTPUT_DIR, "local_storage.json")

with open(LS_FILE, "r", encoding="utf-8") as f:
    ls = json.load(f)

token = ls['token']
semester_id = '6aa6b7d7382ba9a416a84790'

students = [
    {"name": "Ali", "id": "68da68c843e7498ddb5573ba", "grade": "Year 5A"},
    {"name": "Mostafa", "id": "68e6ac96b5f1511f61d47eea", "grade": "Year 6A"}
]

headers = {
    'Authorization': f'JWT {token}',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0'
}

all_links_and_notes = []

for s in students:
    s_name = s["name"]
    s_id = s["id"]
    courses_url = f"https://prod-api.coligolms.com/api/v1/semesters/{semester_id}/users/{s_id}/courses"
    req = urllib.request.Request(courses_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
            courses = data.get("data", data)
    except Exception as e:
        print(f"Error courses {s_name}: {e}")
        continue

    for c in courses:
        cid = c.get("_id")
        cname = c.get("title") or c.get("name")
        mat_url = f"https://prod-api.coligolms.com/api/v2/courses/{cid}/materials"
        req_m = urllib.request.Request(mat_url, headers=headers)
        try:
            with urllib.request.urlopen(req_m) as resp_m:
                materials = json.load(resp_m)
        except Exception as e:
            continue

        for m in materials:
            m_type = m.get("type")
            if m_type in ["@material-type/link", "@material-type/note"] or m.get("link") or ("youtube.com" in str(m.get("url", ""))):
                item = {
                    "student": s_name,
                    "grade": s["grade"],
                    "course": cname,
                    "course_id": cid,
                    "type": m_type,
                    "title": m.get("title"),
                    "url": m.get("url") or m.get("link"),
                    "content": m.get("content"),
                    "description": m.get("description"),
                    "created_at": m.get("publishAt") or m.get("createdAt")
                }
                all_links_and_notes.append(item)
                print(f"[{s_name}] [{cname}] [{m_type}] {m.get('title')}: {m.get('url') or m.get('content')}")

out_path = os.path.join(OUTPUT_DIR, "all_links_and_notes.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_links_and_notes, f, ensure_ascii=False, indent=2)

print(f"\nTotal Links & Notes found: {len(all_links_and_notes)}")
