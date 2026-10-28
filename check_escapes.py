with open(r"C:\Users\co0ob\Projects\primary-exam-system\Index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find all \' or \" inside the file
matches = [m.start() for m in re.finditer(r"\\['\"]", text)]
print("Total escaped quotes in Index.html:", len(matches))
for idx in matches:
    line_num = text[:idx].count('\n') + 1
    snippet = text[max(0, idx-30):min(len(text), idx+30)].replace('\n', ' ')
    print(f"L{line_num}: {snippet}")
