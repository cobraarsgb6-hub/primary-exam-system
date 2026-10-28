import json
import urllib.request
import os

with open(r'primary-exam-system\resources\coligo\local_storage.json', 'r', encoding='utf-8') as f:
    ls = json.load(f)

token = ls.get('token')
headers = {
    'Authorization': f'JWT {token}',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

semester_id = '6aa6b7d7382ba9a416a84790'
students = [
    ('Ali', 'Year 5A', '68da68c843e7498ddb5573ba'),
    ('Mostafa', 'Year 6A', '68e6ac96b5f1511f61d47eea')
]

courses_by_student = {}

for name, grade, sid in students:
    url = f'https://prod-api.coligolms.com/api/v1/semesters/{semester_id}/users/{sid}/courses'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        d = json.loads(resp.read().decode('utf-8'))
        courses = d.get('data', [])
        print(f"\n=======================================================")
        print(f"  STUDENT: {name} ({grade}) - {len(courses)} Courses")
        print(f"=======================================================")
        courses_by_student[name] = []
        for c in courses:
            cid = c.get('_id')
            title = c.get('title') or c.get('name')
            code = c.get('code')
            print(f"  - {title} (ID: {cid}, Code: {code})")
            courses_by_student[name].append({'id': cid, 'title': title, 'code': code})

# Save courses info
with open(r'primary-exam-system\resources\coligo\courses_info.json', 'w', encoding='utf-8') as f:
    json.dump(courses_by_student, f, ensure_ascii=False, indent=2)

print("\nDone fetching courses.")
