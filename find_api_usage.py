import urllib.request
import re

url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

# Find patterns like y.API_URL, y.API_URL_V1, y.API_URL_V2
usages = re.findall(r'(?:y|API_URL[A-Z0-9_]*)\.concat\(([^)]+)\)', content)
print("concat usages:", len(usages))
routes = set()
for u in usages:
    parts = re.findall(r'["\']([^"\']+)["\']', u)
    for p in parts:
        if "/" in p:
            routes.add(p)

print("Found routes count:", len(routes))
for r in sorted(routes):
    print(" ", r)
