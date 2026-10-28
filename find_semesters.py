import urllib.request
import re

url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

semesters = set(re.findall(r'["\'](/api/v[0-9]/[^"\']*semesters[^"\']*)["\']', content))
print("Semesters API endpoints:")
for s in sorted(semesters):
    print(" ", s)

academic = set(re.findall(r'["\'](/api/v[0-9]/[^"\']*academic[^"\']*)["\']', content))
print("\nAcademic API endpoints:")
for a in sorted(academic):
    print(" ", a)
