import re

with open(r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo\courses_dump.html", "r", encoding="utf-8") as f:
    text = f.read()

scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', text)
print("Scripts:")
for s in scripts:
    print(" ", s)
