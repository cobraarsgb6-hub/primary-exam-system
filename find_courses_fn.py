import urllib.request

url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

idx = content.find('/courses",')
if idx == -1:
    idx = content.find('/courses"')
if idx == -1:
    idx = content.find('/courses')

for m in [m.start() for m in __import__("re").finditer(r'/courses["\']', content)][:5]:
    print("--- MATCH ---")
    print(content[max(0, m - 200) : m + 200])
