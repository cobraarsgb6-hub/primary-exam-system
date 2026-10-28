import urllib.request
import re

url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

versions = set(re.findall(r'/api/v[0-9]+[a-zA-Z0-9/_.-]*', content))
print("Versioned endpoints found:", len(versions))
for v in sorted(versions)[:30]:
    print(" ", v)
