with open(r"C:\Users\co0ob\Projects\primary-exam-system\Index.html", "r", encoding="utf-8") as f:
    text = f.read()

s_idx = text.find("<script>")
e_idx = text.rfind("</script>")
script = text[s_idx+8:e_idx]

import re
lines = script.splitlines()
for i, l in enumerate(lines):
    sq = re.findall(r'[\u2018\u2019\u201C\u201D\u00AB\u00BB\u200B\u200C\u200D]', l)
    if sq:
        print(f"Script Line {i+1} (Doc Line {s_idx+i}): {sq} in: {l[:100]}")
