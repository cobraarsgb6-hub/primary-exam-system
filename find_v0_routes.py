import urllib.request
import re

url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

v0_routes = set(re.findall(r'["\'](/api/v0/[^"\']+)["\']', content))
print("v0 routes count:", len(v0_routes))
for r in sorted(v0_routes)[:40]:
    print(" ", r)

# Also search for baseURL string definition
base_defs = re.findall(r'baseURL:\s*["\']([^"\']+)["\']', content)
print("baseURL definitions:", base_defs)
