import urllib.request
import re

url = "https://coligolms.com/static/js/main.35058892.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

idx = content.find("interceptors.request.use")
if idx != -1:
    print("Context around interceptors.request.use:")
    print(content[max(0, idx - 500) : idx + 500])
else:
    print("Not found")
