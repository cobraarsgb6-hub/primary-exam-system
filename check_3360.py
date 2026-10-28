with open(r"C:\Users\co0ob\Projects\primary-exam-system\Index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(3320, 3420):
    if i < len(lines):
        print(f"{i+1}: {repr(lines[i])}")
