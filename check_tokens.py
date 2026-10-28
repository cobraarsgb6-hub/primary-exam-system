with open(r"C:\Users\co0ob\Projects\primary-exam-system\Index.html", "r", encoding="utf-8") as f:
    text = f.read()

s_idx = text.find("<script>")
e_idx = text.rfind("</script>")
script = text[s_idx+8:e_idx]

import re

# Check for smart quotes
smart_quotes = re.findall(r'[\u2018\u2019\u201C\u201D\u00AB\u00BB]', script)
print("Smart quotes in script:", len(smart_quotes))

# Check for zero width spaces / line separators
bad_chars = [
    ('\u2028', 'LINE SEPARATOR'),
    ('\u2029', 'PARAGRAPH SEPARATOR'),
    ('\uFEFF', 'BYTE ORDER MARK'),
    ('\u200B', 'ZERO WIDTH SPACE'),
    ('\u200C', 'ZERO WIDTH NON-JOINER'),
    ('\u200D', 'ZERO WIDTH JOINER'),
    ('\u00A0', 'NO-BREAK SPACE'),
]

for ch, name in bad_chars:
    cnt = script.count(ch)
    if cnt > 0:
        print(f"Found {cnt} of {name}!")

# Let's check for any invalid token around line 1900-1950 of the file
lines = text.splitlines()
print("\nScanning for non-ascii or unusual characters around line 1910-1930 of Index.html:")
for i in range(1900, min(1940, len(lines))):
    l = lines[i]
    non_ascii = [c for c in l if ord(c) > 127]
    if non_ascii:
        print(f"L{i+1}: {non_ascii} in {l[:60]}")
