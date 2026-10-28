with open(r"C:\Users\co0ob\Projects\primary-exam-system\Index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(1850, 1980):
    l = lines[i]
    # Check for backticks, quotes, slashes
    if '`' in l or '\\' in l or '/' in l or '?' in l or '"' in l:
        print(f"Line {i+1}: {repr(l.strip())}")
