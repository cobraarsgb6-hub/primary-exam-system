import re

with open(r"C:\Users\co0ob\Projects\primary-exam-system\inspect_bundle.py", "r") as f:
    pass

import urllib.request
url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

# Search for headers added in axios / fetch
headers_matches = re.findall(r'headers:\s*\{[^}]{1,200}\}', content)
for m in headers_matches[:10]:
    print("Header config:", m)

# Search for school, language, tenant or custom header names
custom_headers = set(re.findall(r'["\'](x-[a-zA-Z0-9_-]+)["\']', content, re.IGNORECASE))
print("\nCustom X- headers found:", custom_headers)

# Search for interceptors
interceptors = re.findall(r'interceptors\.request\.use\([^)]+\)', content)
print("\nInterceptors:", interceptors[:5])
