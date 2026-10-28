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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

endpoints = []
for v in ["v0", "v1", "v2", "v3"]:
    # Children info
    endpoints.append(f"https://prod-api.coligolms.com/api/{v}/parents/{user.get('_id')}/children")
    endpoints.append(f"https://prod-api.coligolms.com/api/{v}/parents/children")
    endpoints.append(f"https://prod-api.coligolms.com/api/{v}/users/students/{children[0]}")
    # Courses
    endpoints.append(f"https://prod-api.coligolms.com/api/{v}/courses?studentId={children[0]}")
    endpoints.append(f"https://prod-api.coligolms.com/api/{v}/students/{children[0]}/courses")
    endpoints.append(f"https://prod-api.coligolms.com/api/{v}/parent/courses?studentId={children[0]}")
    # Announcements
    endpoints.append(f"https://prod-api.coligolms.com/api/{v}/announcements?studentId={children[0]}")
    endpoints.append(f"https://prod-api.coligolms.com/api/{v}/schools/{school_id}/announcements")

for ep in endpoints:
    req = urllib.request.Request(ep, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"\n[SUCCESS 200] {ep}")
            if isinstance(data, list):
                print(f"  List count: {len(data)}")
                if data:
                    print("  Item sample:", json.dumps(data[0], ensure_ascii=False, indent=2)[:300])
            elif isinstance(data, dict):
                print("  Keys:", list(data.keys()))
                print("  Data sample:", json.dumps(data, ensure_ascii=False, indent=2)[:300])
    except urllib.error.HTTPError as e:
        # print first 60 chars of error
        err_msg = e.read().decode('utf-8', errors='ignore')[:60]
        # Only print if not 404
        if e.code != 404:
            print(f"[{e.code}] {ep} -> {err_msg}")
    except Exception as e:
        pass
