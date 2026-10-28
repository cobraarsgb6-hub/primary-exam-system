import urllib.request
import re

url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

matches = [m.start() for m in re.finditer(r'semester', content, re.IGNORECASE)]
print(f"Total occurrences of semester: {len(matches)}")
for idx in matches[:15]:
    print(" ->", content[max(0, idx - 60) : idx + 100].replace('\n', ' '))
