import json
import urllib.request
import urllib.error

with open(r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo\local_storage.json", "r", encoding="utf-8") as f:
    ls = json.load(f)

token = ls.get("token")
user = json.loads(ls.get("user", "{}"))
school_id = user.get("schoolId")
children = user.get("parentInfo", {}).get("childrenIds", [])

headers = {
    "Authorization": f"JWT {token}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

endpoints = [
    # Students / Profile
    f"https://prod-api.coligolms.com/api/users/students/{children[0]}",
    f"https://prod-api.coligolms.com/api/users/students/{children[1]}",
    f"https://prod-api.coligolms.com/api/parents/{user.get('_id')}/children",
    # Courses
    f"https://prod-api.coligolms.com/api/courses?studentId={children[0]}",
    f"https://prod-api.coligolms.com/api/courses?studentId={children[1]}",
    # Announcements
    f"https://prod-api.coligolms.com/api/announcements?studentId={children[0]}",
    f"https://prod-api.coligolms.com/api/announcements?studentId={children[1]}"
]

for ep in endpoints:
    req = urllib.request.Request(ep, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"\n[✓ 200 OK] {ep}")
            if isinstance(data, list):
                print(f"  Count: {len(data)}")
                if data:
                    print("  Sample item:", json.dumps(data[0], ensure_ascii=False, indent=2)[:300])
            elif isinstance(data, dict):
                print("  Keys:", list(data.keys()))
                print("  Sample data:", json.dumps(data, ensure_ascii=False, indent=2)[:300])
    except urllib.error.HTTPError as e:
        print(f"\n[✗ {e.code}] {ep} -> {e.read().decode('utf-8', errors='ignore')[:150]}")
    except Exception as e:
        print(f"\n[ERROR] {ep}: {e}")
