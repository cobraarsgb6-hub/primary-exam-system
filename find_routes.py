import re

with open(r"C:\Users\co0ob\Projects\primary-exam-system\inspect_bundle.py", "r") as f:
    pass

import urllib.request
url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

# Find occurrences of prod-api or routes
matches = re.findall(r'prod-api\.coligolms\.com[a-zA-Z0-9/_.-]*', content)
print("Matches prod-api:", set(matches))

# Look for courses endpoints e.g. /courses, /students, /materials
course_routes = set(re.findall(r'["\'](/v[0-9]/[^"\']+|/[a-zA-Z0-9_-]+/(?:courses|materials|students|announcements)[^"\']*)["\']', content))
print("\nAPI Routes found:", len(course_routes))
for r in sorted(course_routes)[:40]:
    print(" ", r)
