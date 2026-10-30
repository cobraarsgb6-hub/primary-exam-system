import os
import re

history_path = r'C:\Users\co0ob\.gemini\config\MASTER_HISTORY_CATALOG.md'
if os.path.exists(history_path):
    with open(history_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    matches = re.findall(r'https?://[^\s\)\"\'>]+', text)
    primary = [m for m in matches if any(k in m.lower() for k in ['exam', 'primary', 'github.io', 'script.google.com', 'pages.dev', 'coligo', 'cloudflare', 'vercel'])]
    print("=== Found in MASTER_HISTORY_CATALOG ===")
    for m in set(primary):
        print(m)

# Also check primary-exam-system files for deployed URL
proj_dir = r'C:\Users\co0ob\Projects\primary-exam-system'
print("\n=== Checking files in primary-exam-system ===")
for root, dirs, files in os.walk(proj_dir):
    # skip .git
    if '.git' in root:
        continue
    for f in files:
        if f.endswith(('.md', '.py', '.json', '.html', '.js')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                    cnt = fl.read()
                f_matches = re.findall(r'https?://[^\s\)\"\'>]+', cnt)
                f_primary = [m for m in f_matches if any(k in m.lower() for k in ['github.io', 'script.google.com', 'pages.dev', 'workers.dev'])]
                if f_primary:
                    print(f"{f}:", set(f_primary))
            except Exception:
                pass

# Also check scheduled tasks on windows!
print("\n=== Checking Windows Scheduled Tasks ===")
import subprocess
try:
    tasks = subprocess.check_output(['schtasks', '/query', '/fo', 'LIST'], text=True, errors='ignore')
    for block in tasks.split('\n\n'):
        if any(k in block.lower() for k in ['exam', 'primary', 'coligo', 'antigravity', 'sync']):
            print("--- TASK ---")
            print(block.strip())
except Exception as e:
    print("Error querying schtasks:", e)
