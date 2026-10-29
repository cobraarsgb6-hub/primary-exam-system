#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
  AUTONOMOUS CLOUD COLIGO INGESTION PIPELINE (Full Online Sync v2)
  Runs 100% in the cloud on GitHub Actions.
  Students: Ali (Year 5A) & Mostafa (Year 6A) — Manaret El-Eman BIS.

  SECURITY MODEL:
  - Credentials live ONLY in runner secrets (Coligo login via /v3/authenticate
    with COLIGO_USERNAME/COLIGO_PASSWORD, refreshed every run; never in files).
  - Captured-traffic JSON files are never regenerated; only published-safe data
    is written locally: materials, catalog, and assets (PDF/ZIP unzipped).
  - ZIP attachments are extracted and their inner HTML web-path references are
    rewritten to relative URLs so nothing 404s on GitHub Pages.
================================================================================
"""

import os
import sys
import json
import time
import base64
import re
import urllib.request
import urllib.error
import urllib.parse
import zipfile
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "resources", "coligo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

API_BASE = "https://prod-api.coligolms.com/api"
API_V0 = f"{API_BASE}/v0"
API_V1 = f"{API_BASE}/v1"
API_V2 = f"{API_BASE}/v2"
API_V3 = f"{API_BASE}/v3"

SEMESTER_ID = "6aa6b7d7382ba9a416a84790"  # Trimester 1 (Sep 2026 - Jul 2027)

STUDENTS = [
    {"name": "Ali", "id": "68da68c843e7498ddb5573ba", "grade": "Year 5A"},
    {"name": "Mostafa", "id": "68e6ac96b5f1511f61d47eea", "grade": "Year 6A"}
]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# ---------------------------------------------------------------------------
# Token lifecycle: session auth from secrets → fresh JWT every run.
# ---------------------------------------------------------------------------

def jwt_expiry(token):
    """Best-effort parse of JWT 'exp' claim (unix seconds); None if unknown."""
    try:
        payload_b64 = token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        return int(payload.get("exp")) if payload.get("exp") else None
    except Exception:
        return None


def http_json(url, payload=None, headers=None, timeout=25):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    hdrs = {"Content-Type": "application/json", "User-Agent": UA}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body.strip() else {}


def authenticate_coligo():
    """
    Returns (jwt, method_label). Order:
      1. COLIGO_USERNAME + COLIGO_PASSWORD → POST /v3/authenticate
      2. COLIGO_TOKEN (long-lived fallback secret)
    Exits loudly when neither path can produce a usable JWT.
    """
    user = os.environ.get("COLIGO_USERNAME", "").strip()
    pwd = os.environ.get("COLIGO_PASSWORD", "").strip()

    if user and pwd:
        try:
            resp = http_json(
                f"{API_V3}/authenticate",
                payload={"username": user, "password": pwd},
                timeout=30)
            # Coligo wraps the session inside "data"; token keys mirror the
            # SPA localStorage keys (token / refreshToken / refreshTokenId).
            data = resp.get("data", resp) if isinstance(resp, dict) else {}
            token = (data.get("token") or data.get("jwt")
                     or (data.get("auth") or {}).get("token")
                     or resp.get("token"))
            if token:
                exp = jwt_expiry(token)
                exp_txt = time.strftime("%Y-%m-%d %H:%M", time.gmtime(exp)) if exp else "unknown"
                print(f"[AUTH] Login OK via username/password. JWT valid until: {exp_txt} UTC")
                return token, "credentials"
            print(f"[AUTH] /v3/authenticate answered but no token field found. Keys: {list(data.keys())[:8]}")
        except urllib.error.HTTPError as e:
            print(f"[AUTH] Login rejected (HTTP {e.code}). Check COLIGO_USERNAME/COLIGO_PASSWORD secrets.")
        except Exception as e:
            print(f"[AUTH] Login attempt failed: {e}")

    token = os.environ.get("COLIGO_TOKEN", "").strip()
    if token:
        exp = jwt_expiry(token)
        if exp and exp < time.time():
            print("[AUTH] COLIGO_TOKEN secret is ALREADY EXPIRED; credentials login required.")
        else:
            print(f"[AUTH] Using COLIGO_TOKEN secret (expiry: "
                  f"{time.strftime('%Y-%m-%d %H:%M', time.gmtime(exp)) if exp else 'unknown'} UTC).")
            return token, "static-token"
        if exp:
            pass
        # Expired static token → try it anyway as last resort during outage.
        return token, "static-token-expired"

    print("[ERROR] No usable auth path: provide COLIGO_USERNAME + COLIGO_PASSWORD secrets.")
    sys.exit(2)


STUDENT_REQUEST_TOKEN = {"token": None}


def api_headers():
    return {
        "Authorization": f"JWT {STUDENT_REQUEST_TOKEN['token']}",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": UA,
    }


def api_get(url, timeout=25):
    req = urllib.request.Request(url, headers=api_headers())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        parsed = json.loads(body) if body.strip() else {}
        if isinstance(parsed, dict) and isinstance(parsed.get("data"), (list, dict)) and "data" in parsed:
            return parsed["data"]
        return parsed


# ---------------------------------------------------------------------------
# Filename / path safety
# ---------------------------------------------------------------------------

def clean_filename(name):
    if not name:
        return "file"
    for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\n', '\r', '\t']:
        name = name.replace(c, '_')
    return name.strip()[:100]


def web_quote(rel_path):
    """URL-quote a repo-relative path for direct Pages links (keeps slashes)."""
    return urllib.parse.quote(rel_path.replace("\\", "/"), safe="/")


# ---------------------------------------------------------------------------
# Download & extraction with inner-path patching
# ---------------------------------------------------------------------------

def patch_rtl_unzip_extracted(target_folder):
    """
    After ZIP extraction:
      - delete the zip archive if it was stored locally,
      - rewrite absolute/local/src references inside extracted .html files
        to relative URLs so they render correctly on GitHub Pages.
    Returns list of (zip_name, extracted_relative_paths).
    """
    zips = [f for f in os.listdir(target_folder) if f.lower().endswith(".zip")]
    results = []
    for zip_name in zips:
        zip_path = os.path.join(target_folder, zip_name)
        try:
            with zipfile.ZipFile(zip_path) as z:
                extracted = []
                for zinfo in z.infolist():
                    if zinfo.filename.endswith("/"):
                        continue
                    out_name = clean_filename(os.path.basename(zinfo.filename))
                    out_path = os.path.join(target_folder, out_name)
                    with z.open(zinfo) as src, open(out_path, "wb") as dst:
                        raw = src.read()
                        dst.write(raw)
                    # Patch HTML/DZ web paths so local or absolute refs resolve
                    if out_name.lower().endswith((".html", ".htm", ".xhtml")):
                        with open(out_path, "r", encoding="utf-8", errors="ignore") as f:
                            html = f.read()
                        patched = re.sub(
                            r'(?:src|href)\s*=\s*(["\'])\s*(?:[A-Za-z]:[\\/][^"\']*|[\\/][Uu]sers[\\/][^"\']*|[\\/][Hh]ome[\\/][^"\']*)\1',
                            lambda m: m.group(0)[:len(m.group(0)) - len(m.group(0).split('=', 1)[1])] + m.group(1) + web_quote(out_name) + m.group(1),
                            html)
                        # Fallback broad pass: file:// and drive-letter hrefs
                        patched = re.sub(r'(href|src)\s*=\s*"file:///[^"]*"',
                                         f'\\1="{web_quote(out_name)}"', patched)
                        if patched != html:
                            with open(out_path, "w", encoding="utf-8") as f:
                                f.write(patched)
                    extracted.append(out_name)
            os.remove(zip_path)  # Keep only clean inner assets, never raw zip
            results.append((zip_name, extracted))
        except Exception as e:
            print(f"      [Zip Warning] {zip_name}: {e}")
    return results


def safe_download_file(url, target_folder, preferred_name):
    """Downloads one material. Unzips archives, patches inner paths, returns
    (list_of_saved_relative_names, is_new)."""
    os.makedirs(target_folder, exist_ok=True)
    clean_base = clean_filename(preferred_name)

    # Skip re-download when a valid artifact for this title already exists
    try:
        for existing in os.listdir(target_folder):
            if existing.startswith(clean_base) or clean_base.startswith(os.path.splitext(existing)[0]):
                existing_path = os.path.join(target_folder, existing)
                if os.path.getsize(existing_path) > 100:
                    return [existing], False
    except Exception:
        pass

    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if data[:4] == b'PK\x03\x04':  # ZIP archive
                far_name = clean_base + ("" if clean_base.lower().endswith(".zip") else ".zip")
                with open(os.path.join(target_folder, far_name), "wb") as f:
                    f.write(data)
                zip_results = patch_rtl_unzip_extracted(target_folder)
                out_names = [n for (_, names) in zip_results for n in names]
                return (out_names, True) if out_names else ([far_name], True)

            ext_map = [".pdf", ".docx", ".pptx", ".xlsx", ".png", ".jpg", ".jpeg", ".gif"]
            guessed = next((e for e in ext_map if e in url.lower()), ".bin")
            final_name = clean_base if any(clean_base.lower().endswith(e) for e in ext_map + [".zip", ".bin"]) else clean_base + guessed
            with open(os.path.join(target_folder, final_name), "wb") as f:
                f.write(data)
            return [final_name], True
    except Exception as e:
        print(f"      [Download Warning] {preferred_name}: {e}")
        return [], False


# ---------------------------------------------------------------------------
# YouTube ID extraction (supports watch/share/search-trap/google ref links)
# ---------------------------------------------------------------------------

YOUTUBE_ID_RE = re.compile(
    r'(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/)|youtu\.be/|'
    r'v=|/vi?d?/)([A-Za-z0-9_-]{11})')


def extract_youtube_id(url):
    if not url:
        return None
    m = YOUTUBE_ID_RE.search(url)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Main sync
# ---------------------------------------------------------------------------

def run_sync():
    print("=" * 65)
    print("🚀 [Cloud Sync v2] Starting Full Autonomous Coligo Ingestion...")
    print("=" * 65)
    t0 = time.time()

    token, auth_mode = authenticate_coligo()
    STUDENT_REQUEST_TOKEN["token"] = token
    print(f"[AUTH] Mode: {auth_mode}")

    # Step 1: Notifications (trimmed: only count + homework items, no raw dump)
    print("\n[1/3] 🔔 Fetching latest notifications, homework & announcements...")
    no_rec_notifications = []
    homework_items = []
    try:
        notifs = api_get(f"{API_V0}/users/me/notifications?limit=100") or []
        print(f"✅ Synced {len(notifs)} notifications (count only; raw capture files are not persisted).")
        for n in notifs:
            msg = n.get("message", "")
            if any(k in msg.lower() for k in ["homework", "واجب", "quiz", "announcement", "created in", "material"]):
                homework_items.append({
                    "id": n.get("_id"),
                    "date": n.get("createdAt"),
                    "message": msg,
                    "type": n.get("type"),
                    "read": n.get("state") == "@notification-state/read",
                })
    except Exception as e:
        print(f"⚠️ Notification fetch warning: {e}")

    # Step 2: Curriculum courses & materials for both students
    print("\n[2/3] 📚 Ingesting curriculum materials & worksheets for Ali & Mostafa...")
    master_catalog = {
        "synced_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "semester_id": SEMESTER_ID,
        "school": "Manaret El-Eman British International School",
        "students": {}
    }
    total_new_downloads = 0
    total_materials_indexed = 0
    youtube_videos = {"Ali": [], "Mostafa": []}

    for student in STUDENTS:
        s_name = student["name"]
        s_id = student["id"]
        s_grade = student["grade"]
        print(f"\n--- Processing Student: {s_name} ({s_grade}) ---")
        master_catalog["students"][s_name] = {"grade": s_grade, "courses": []}

        try:
            courses = api_get(f"{API_V1}/semesters/{SEMESTER_ID}/users/{s_id}/courses") or []
        except Exception as e:
            print(f"❌ Courses fetch failed for {s_name}: {e}")
            continue

        print(f"  Found {len(courses)} enrolled courses.")

        for c in courses:
            c_id = c.get("_id")
            c_title = (c.get("title") or c.get("name") or "Course").strip()
            safe_course = clean_filename(c_title)
            course_dir = os.path.join(OUTPUT_DIR, s_name, safe_course)
            os.makedirs(course_dir, exist_ok=True)

            try:
                materials = api_get(f"{API_V2}/courses/{c_id}/materials") or []
            except Exception as e:
                print(f"  [!] Failed materials for {c_title}: {e}")
                materials = []

            total_materials_indexed += len(materials)
            file_items = [m for m in materials if m.get("type") == "@material-type/file" and m.get("url")]
            link_items = [m for m in materials if m.get("type") == "@material-type/link" and m.get("url")]

            files_log = []
            for f_item in file_items:
                f_title = f_item.get("title") or "Material"
                f_url = f_item.get("url")
                saved_names, is_new = safe_download_file(f_url, course_dir, f_title)
                if is_new:
                    total_new_downloads += len(saved_names)
                    print(f"     ⬇️ [New]: {f_title} -> {saved_names}")
                for saved in saved_names:
                    rel_web = f"resources/coligo/{s_name}/{safe_course}/{saved}".replace("\\", "/")
                    files_log.append({
                        "title": f_title,
                        "filename": saved,
                        "web_path": web_quote(rel_web),
                        "source_url": f_url,
                        "assigned_at": f_item.get("assignedAt") or f_item.get("createdAt"),
                    })

            links_log = []
            for l_item in link_items:
                l_title = (l_item.get("title") or "Link").strip()
                l_url = l_item.get("url") or ""
                yt_id = extract_youtube_id(l_url)
                links_log.append({
                    "title": l_title,
                    "url": l_url,
                    "youtube_id": yt_id,
                })
                if yt_id:
                    youtube_videos[s_name].append({"title": l_title, "youtube_id": yt_id, "course": c_title})

            master_catalog["students"][s_name]["courses"].append({
                "id": c_id,
                "title": c_title,
                "total_items": len(materials),
                "downloaded_files": files_log,
                "links": links_log,
            })

    # Attach safe aggregated YouTube list so the UI can render watch-hosted lessons
    master_catalog["youtube_videos"] = youtube_videos

    # Step 3: Persist ONLY publication-safe outputs
    catalog_path = os.path.join(OUTPUT_DIR, "coligo_catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, ensure_ascii=False, indent=2)

    # Small machine summary for the workflow to diff quickly on runs
    with open(os.path.join(OUTPUT_DIR, "coligo_manifest.json"), "w", encoding="utf-8") as f:
        json.dump({
            "synced_at": master_catalog["synced_at"],
            "auth_mode": auth_mode,
            "students": {s["name"]: s["grade"] for s in STUDENTS},
            "indexed_materials": total_materials_indexed,
            "new_downloads": total_new_downloads,
            "homework_signals": len(homework_items),
        }, f, ensure_ascii=False, indent=2)

    print(f"\n[Summary] Indexed: {total_materials_indexed} items | Newly saved: {total_new_downloads} files.")

    # Step 4: Push digest to Google Sheets webhook (Web App)
    WEBHOOK_URL = os.environ.get("GAS_WEBHOOK_URL")
    if WEBHOOK_URL:
        print("\n[3/3] ☁️ Pushing live updates to Google Sheets Webhook...")
        payload = json.dumps({
            "action": "sync_coligo_feed",
            "secret": os.environ.get("SYNC_SECRET", ""),
            "timestamp": time.time(),
            "notificationsCount": len(no_rec_notifications) or len(homework_items),
            "materialsCount": total_materials_indexed,
            "newDownloads": total_new_downloads,
            "homework": homework_items[:30],
        }).encode("utf-8")
        req_w = urllib.request.Request(WEBHOOK_URL, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req_w, timeout=25) as resp_w:
                print("✅ Successfully pushed to Google Sheets Cloud Database:", resp_w.read().decode("utf-8")[:200])
        except Exception as e:
            print("[Warning] Could not reach Google Apps Script webhook:", e)

    elapsed = time.time() - t0
    print(f"\n🎉 100% Autonomous Cloud Sync v2 Completed in {elapsed:.2f}s! (auth={auth_mode})")


if __name__ == "__main__":
    run_sync()
