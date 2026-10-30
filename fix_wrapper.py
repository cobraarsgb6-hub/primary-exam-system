import os

with open(r"C:\Users\co0ob\Projects\primary-exam-system\build_flawless_cambridge_lab.py", "r", encoding="utf-8") as f:
    raw = f.read()

# If it starts with <!DOCTYPE html>, wrap it properly:
if raw.startswith("<!DOCTYPE html>"):
    # find where python footer might be or wrap the whole HTML
    idx = raw.rfind("target_paths = [")
    if idx != -1:
        html_part = raw[:idx]
        python_part = raw[idx:]
        # Remove any trailing triple quotes from html_part if present
        html_part = html_part.strip().rstrip("'''").strip()
        new_content = "import os\n\nhtml_content = '''" + html_part + "'''\n\n" + python_part
    else:
        new_content = "import os\n\nhtml_content = '''" + raw + "'''\n\n" + '''
target_paths = [
    r"C:\\Users\\co0ob\\Projects\\primary-exam-system\\resources\\coligo\\Mostafa\\Science 106\\Electricity_Mastery_Guide_Stage6.html",
    r"C:\\Users\\co0ob\\.gemini\\antigravity\\brain\\54d05bb7-093a-4520-bc55-e8fbc272480c\\Electricity_Mastery_Guide_Stage6.html",
    r"C:\\Users\\co0ob\\Projects\\primary-exam-system\\build_precision_phet_lab.py"
]

for p in target_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Updated precision lab: {p} ({len(html_content)} bytes)")
'''
    with open(r"C:\Users\co0ob\Projects\primary-exam-system\build_flawless_cambridge_lab.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Fixed build_flawless_cambridge_lab.py structure!")
else:
    print("Already wrapped!")
