import os
import json
import subprocess
import sys

CATALOG_PATH = r"C:\Users\co0ob\Projects\primary-exam-system\youtube_catalog.json"
OUTPUT_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\videos\arabic"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total videos to check/download: {len(items)}")

results = []

for idx, item in enumerate(items, 1):
    url = item["url"]
    vid_id = url.split("v=")[-1]
    expected_file = os.path.join(OUTPUT_DIR, f"{vid_id}.mp4")
    
    print(f"\n[{idx}/{len(items)}] Processing: {vid_id} - {item['title'][:40]}...")
    
    if os.path.exists(expected_file) and os.path.getsize(expected_file) > 100000:
        print(f"  -> Already exists ({os.path.getsize(expected_file) / (1024*1024):.2f} MB). Skipping download.")
        results.append({
            "id": vid_id,
            "title": item["title"],
            "author": item["author"],
            "url": url,
            "file": expected_file,
            "filename": f"{vid_id}.mp4",
            "size_mb": round(os.path.getsize(expected_file) / (1024*1024), 2),
            "status": "ready"
        })
        continue

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--remote-components", "ejs:github",
        "--js-runtimes", "node",
        "-f", "best[ext=mp4]/best",
        "-o", os.path.join(OUTPUT_DIR, "%(id)s.%(ext)s"),
        "--no-playlist",
        url
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if proc.returncode == 0:
            actual_file = os.path.join(OUTPUT_DIR, f"{vid_id}.mp4")
            if not os.path.exists(actual_file):
                # Search for any file with this vid_id in folder
                candidates = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(vid_id)]
                if candidates:
                    actual_file = os.path.join(OUTPUT_DIR, candidates[0])
            size_mb = round(os.path.getsize(actual_file) / (1024*1024), 2) if os.path.exists(actual_file) else 0
            print(f"  -> SUCCESS ({size_mb} MB)")
            results.append({
                "id": vid_id,
                "title": item["title"],
                "author": item["author"],
                "url": url,
                "file": actual_file,
                "filename": os.path.basename(actual_file),
                "size_mb": size_mb,
                "status": "downloaded"
            })
        else:
            print(f"  -> FAILED: {proc.stderr[:200]}")
            results.append({
                "id": vid_id,
                "title": item["title"],
                "author": item["author"],
                "url": url,
                "status": "error",
                "error": proc.stderr[:200]
            })
    except Exception as e:
        print(f"  -> EXCEPTION: {e}")
        results.append({
            "id": vid_id,
            "title": item["title"],
            "author": item["author"],
            "url": url,
            "status": "error",
            "error": str(e)
        })

output_manifest = os.path.join(OUTPUT_DIR, "manifest.json")
with open(output_manifest, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nFinished! Manifest saved to:", output_manifest)
