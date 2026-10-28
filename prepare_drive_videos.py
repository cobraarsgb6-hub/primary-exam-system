import os
import json
import shutil
import re

src_dir = r"C:\Users\co0ob\Projects\primary-exam-system\videos\arabic"
dest_dir = r"C:\Users\co0ob\Projects\primary-exam-system\videos\ready_for_drive"
manifest_path = os.path.join(src_dir, "manifest.json")

os.makedirs(dest_dir, exist_ok=True)

with open(manifest_path, "r", encoding="utf-8") as f:
    items = json.load(f)

for item in items:
    vid_id = item["id"]
    raw_title = item["title"]
    clean_title = re.sub(r'[\\/*?:"<>|]', '-', raw_title)
    clean_title = clean_title.replace("  ", " ").strip()
    formatted_name = f"[{vid_id}] {clean_title[:50].strip()}.mp4"
    src_file = os.path.join(src_dir, f"{vid_id}.mp4")
    dest_file = os.path.join(dest_dir, formatted_name)
    if os.path.exists(src_file) and not os.path.exists(dest_file):
        shutil.copy2(src_file, dest_file)
        print("Copied:", formatted_name)

print("\nTotal ready files in ready_for_drive:", len(os.listdir(dest_dir)))
