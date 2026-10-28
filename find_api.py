import re

with open(r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo\courses_dump.html", "r", encoding="utf-8") as f:
    text = f.read()

urls = set(re.findall(r'https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9_.-]+)*', text))
filtered = [u for u in urls if not any(x in u for x in ['google', 'gstatic', 'w3.org', 'schema.org', 'cloudflare'])]
print("URLs found in HTML:")
for u in filtered:
    print(" ", u)
