import re

with open(r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo\Mostafa\Science 106\Electricity_Mastery_Guide_Stage6.html", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
for i, l in enumerate(lines):
    if "<div" in l and ("rounded" in l or "shadow" in l) and "border" in l:
        print(f"Line {i+1}: {l.strip()[:100]}")
