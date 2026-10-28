import urllib.request
import re

url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

# Find occurrences of "/courses"
matches = [m.start() for m in re.finditer(r'/courses', content)]
print(f"Total occurrences of /courses: {len(matches)}")
for idx in matches[:15]:
    snippet = content[max(0, idx - 80) : idx + 80]
    print(" ->", snippet.replace('\n', ' '))
