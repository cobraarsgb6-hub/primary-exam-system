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
from pathlib import PurePosixPath

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
    """Mint a fresh Coligo JWT on every run from GitHub username/password secrets."""
    user = os.environ.get("COLIGO_USERNAME", "").strip()
    pwd = os.environ.get("COLIGO_PASSWORD", "").strip()
    if not user or not pwd:
        raise RuntimeError("COLIGO_USERNAME and COLIGO_PASSWORD GitHub secrets are required.")
    try:
        resp = http_json(
            f"{API_V3}/authenticate",
            payload={"username": user, "password": pwd},
            timeout=30)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Coligo login rejected (HTTP {exc.code}).") from exc
    except Exception as exc:
        raise RuntimeError(f"Coligo login failed ({type(exc).__name__}).") from exc

    data = resp.get("data", resp) if isinstance(resp, dict) else {}
    if not isinstance(data, dict):
        data = {}
    token = (data.get("token") or data.get("jwt")
             or (data.get("auth") or {}).get("token")
             or (resp.get("token") if isinstance(resp, dict) else None))
    if not token:
        raise RuntimeError("Coligo authentication response did not contain a JWT.")
    exp = jwt_expiry(token)
    if exp and exp <= time.time():
        raise RuntimeError("Coligo authentication returned an expired JWT.")
    exp_txt = time.strftime("%Y-%m-%d %H:%M", time.gmtime(exp)) if exp else "unknown"
    print(f"[AUTH] Fresh Coligo JWT acquired; expiry {exp_txt} UTC.")
    return token, "credentials"


STUDENT_REQUEST_TOKEN = {"token": None}
AUTH_REFRESHED_AFTER_401 = False


def api_headers():
    return {
        "Authorization": f"JWT {STUDENT_REQUEST_TOKEN['token']}",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": UA,
    }


def api_get(url, timeout=25):
    global AUTH_REFRESHED_AFTER_401
    for attempt in range(5):
        req = urllib.request.Request(url, headers=api_headers())
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                parsed = json.loads(body) if body.strip() else {}
                if isinstance(parsed, dict) and isinstance(parsed.get("data"), (list, dict)) and "data" in parsed:
                    return parsed["data"]
                return parsed
        except urllib.error.HTTPError as exc:
            if exc.code == 401 and not AUTH_REFRESHED_AFTER_401:
                token, _ = authenticate_coligo()
                STUDENT_REQUEST_TOKEN["token"] = token
                AUTH_REFRESHED_AFTER_401 = True
                continue
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 4:
                raise
            retry_after = exc.headers.get("Retry-After") if exc.headers else None
            delay = min(30, max(1, int(retry_after))) if retry_after and retry_after.isdigit() else min(30, 2 ** attempt)
            time.sleep(delay)
        except urllib.error.URLError:
            if attempt == 4:
                raise
            time.sleep(min(30, 2 ** attempt))
    raise RuntimeError("Coligo API retry limit exhausted")


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
    """Safely extract ZIP materials while preserving their internal folders."""
    zips = [f for f in os.listdir(target_folder) if f.lower().endswith(".zip")]
    results = []
    for zip_name in zips:
        zip_path = os.path.join(target_folder, zip_name)
        try:
            with zipfile.ZipFile(zip_path) as archive:
                files = [item for item in archive.infolist() if not item.is_dir()]
                if len(files) > 1000 or sum(item.file_size for item in files) > 250 * 1024 * 1024:
                    raise ValueError("archive exceeds extraction safety limits")
                archive_root = os.path.join(target_folder, clean_filename(os.path.splitext(zip_name)[0]))
                os.makedirs(archive_root, exist_ok=True)
                extracted, member_paths = [], {}
                for item in files:
                    member = item.filename.replace("\\", "/")
                    path = PurePosixPath(member)
                    if path.is_absolute() or re.match(r"^[A-Za-z]:", member) or ".." in path.parts:
                        raise ValueError("archive contains an unsafe path")
                    parts = [clean_filename(part) for part in path.parts if part not in ("", ".")]
                    if not parts:
                        continue
                    rel_inside = "/".join(parts)
                    out_path = os.path.abspath(os.path.join(archive_root, *parts))
                    if os.path.commonpath([os.path.abspath(archive_root), out_path]) != os.path.abspath(archive_root):
                        raise ValueError("archive entry escapes extraction folder")
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    with archive.open(item) as src, open(out_path, "wb") as dst:
                        dst.write(src.read())
                    member_paths.setdefault(PurePosixPath(member).name.lower(), []).append(rel_inside)
                    extracted.append(os.path.relpath(out_path, target_folder).replace("\\", "/"))

                # Convert local absolute references only when a matching archive asset is unique.
                for rel_name in extracted:
                    out_path = os.path.join(target_folder, *rel_name.split("/"))
                    if not out_path.lower().endswith((".html", ".htm", ".xhtml")):
                        continue
                    with open(out_path, "r", encoding="utf-8", errors="ignore") as source:
                        html = source.read()
                    def rewrite_ref(match):
                        attr, quote, ref = match.group(1), match.group(2), match.group(3)
                        if not re.match(r"^(?:[A-Za-z]:[\\/]|file:|/Users/|/home/)", ref, re.I):
                            return match.group(0)
                        basename = PurePosixPath(urllib.parse.unquote(ref.replace("\\", "/"))).name.lower()
                        choices = member_paths.get(basename, [])
                        if len(choices) != 1:
                            return match.group(0)
                        html_inside = os.path.relpath(rel_name, os.path.relpath(archive_root, target_folder)).replace("\\", "/")
                        relative = os.path.relpath(choices[0], os.path.dirname(html_inside) or ".").replace("\\", "/")
                        return f"{attr}={quote}{web_quote(relative)}{quote}"
                    patched = re.sub(r"(src|href)\s*=\s*([\"'])(.*?)\2", rewrite_ref, html, flags=re.I)
                    if patched != html:
                        with open(out_path, "w", encoding="utf-8") as target:
                            target.write(patched)

            os.remove(zip_path)
            results.append((zip_name, extracted))
        except Exception as exc:
            print(f"      [Zip Warning] {zip_name}: {type(exc).__name__} — archive was not published.")
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
                if os.path.isdir(existing_path) and existing == clean_base:
                    cached_files = []
                    for root, _, names in os.walk(existing_path):
                        for name in names:
                            item = os.path.join(root, name)
                            if os.path.getsize(item) > 0:
                                cached_files.append(os.path.relpath(item, target_folder).replace("\\", "/"))
                    if cached_files:
                        return cached_files, False
                if os.path.isfile(existing_path) and os.path.getsize(existing_path) > 100:
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
                extracted = next((names for name, names in zip_results if name == far_name), None)
                return (extracted, True) if extracted else ([], False)

            ext_map = [".pdf", ".docx", ".pptx", ".xlsx", ".png", ".jpg", ".jpeg", ".gif"]
            guessed = next((e for e in ext_map if e in url.lower()), ".bin")
            final_name = clean_base if any(clean_base.lower().endswith(e) for e in ext_map + [".zip", ".bin"]) else clean_base + guessed
            with open(os.path.join(target_folder, final_name), "wb") as f:
                f.write(data)
            return [final_name], True
    except Exception as e:
        print(f"      [Download Warning] {preferred_name}: {type(e).__name__}.")
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
    # A Google teacher-search link may wrap a direct YouTube URL in q= or url=.
    m = YOUTUBE_ID_RE.search(urllib.parse.unquote(str(url)))
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Main sync
# ---------------------------------------------------------------------------

def run_sync():
    print("=" * 65)
    print("🚀 [Cloud Sync v2] Starting Full Autonomous Coligo Ingestion...")
    print("=" * 65)
    t0 = time.time()

    if not os.environ.get("GAS_WEBHOOK_URL", "").strip() or not os.environ.get("SYNC_SECRET", "").strip():
        raise RuntimeError("GAS_WEBHOOK_URL and SYNC_SECRET GitHub secrets are required for a complete sync.")

    token, auth_mode = authenticate_coligo()
    STUDENT_REQUEST_TOKEN["token"] = token
    print(f"[AUTH] Mode: {auth_mode}")

    # Step 1: Notifications (trimmed: only count + homework items, no raw dump)
    print("\n[1/3] 🔔 Fetching latest notifications, homework & announcements...")
    no_rec_notifications = []
    homework_items = []
    try:
        notifs = api_get(f"{API_V0}/users/me/notifications?limit=100") or []
        no_rec_notifications = notifs if isinstance(notifs, list) else []
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
        "students": {}
    }
    total_new_downloads = 0
    total_materials_indexed = 0
    youtube_videos = {"Ali": [], "Mostafa": []}
    subject_aliases = {
        "science": ("science",), "math": ("math",), "english": ("english",),
        "arabic": ("arabic",), "social": ("social studies",), "french": ("french",),
        "ict": ("ict", "computing"), "literature": ("literature",)
    }
    required_subjects = set(subject_aliases)

    for student in STUDENTS:
        s_name = student["name"]
        s_id = student["id"]
        s_grade = student["grade"]
        print(f"\n--- Processing Student: {s_name} ({s_grade}) ---")
        master_catalog["students"][s_name] = {"grade": s_grade, "courses": []}

        try:
            courses = api_get(f"{API_V1}/semesters/{SEMESTER_ID}/users/{s_id}/courses") or []
        except Exception as e:
            raise RuntimeError(f"Courses fetch failed for {s_name} ({type(e).__name__}); preserving previous catalog.") from e

        print(f"  Found {len(courses)} enrolled courses.")
        found_subjects = set()
        material_errors = []

        for c in courses:
            c_id = c.get("_id")
            c_title = (c.get("title") or c.get("name") or "Course").strip()
            title_key = c_title.lower()
            subject_key = next((key for key, aliases in subject_aliases.items()
                                if any(alias in title_key for alias in aliases)), None)
            if not subject_key:
                continue
            found_subjects.add(subject_key)
            safe_course = clean_filename(c_title)
            course_dir = os.path.join(OUTPUT_DIR, s_name, safe_course)
            os.makedirs(course_dir, exist_ok=True)

            try:
                materials = api_get(f"{API_V2}/courses/{c_id}/materials") or []
            except Exception as e:
                material_errors.append(c_title)
                print(f"  [!] Failed materials for {c_title} ({type(e).__name__}).")
                continue

            total_materials_indexed += len(materials)
            file_items = [m for m in materials if m.get("type") == "@material-type/file" and m.get("url")]
            link_items = [m for m in materials if m.get("type") == "@material-type/link" and m.get("url")]

            files_log = []
            download_errors = []
            for f_item in file_items:
                f_title = f_item.get("title") or "Material"
                f_url = f_item.get("url")
                saved_names, is_new = safe_download_file(f_url, course_dir, f_title)
                if not saved_names:
                    download_errors.append(f_title)
                    continue
                if is_new:
                    total_new_downloads += len(saved_names)
                    print(f"     ⬇️ [New]: {f_title} -> {saved_names}")
                for saved in saved_names:
                    rel_web = f"resources/coligo/{s_name}/{safe_course}/{saved}".replace("\\", "/")
                    files_log.append({
                        "title": f_title,
                        "filename": saved,
                        "web_path": web_quote(rel_web),
                        "assigned_at": f_item.get("assignedAt") or f_item.get("createdAt"),
                    })

            if download_errors:
                material_errors.extend(f"{c_title}/{name}" for name in download_errors)

            links_log = []
            for l_item in link_items:
                l_title = (l_item.get("title") or "Link").strip()
                l_url = l_item.get("url") or ""
                yt_id = extract_youtube_id(l_url)
                links_log.append({
                    "title": l_title,
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

        missing_subjects = sorted(required_subjects - found_subjects)
        if missing_subjects or material_errors:
            details = []
            if missing_subjects:
                details.append("missing subjects: " + ", ".join(missing_subjects))
            if material_errors:
                details.append("materials unavailable: " + ", ".join(material_errors))
            raise RuntimeError(f"Incomplete Coligo response for {s_name} ({'; '.join(details)}); preserving previous catalog.")

    # Attach safe aggregated YouTube list so the UI can render watch-hosted lessons
    master_catalog["youtube_videos"] = youtube_videos

    # Step 3: Persist ONLY publication-safe outputs
    catalog_path = os.path.join(OUTPUT_DIR, "coligo_catalog.json")
    catalog_tmp = catalog_path + ".tmp"
    with open(catalog_tmp, "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, ensure_ascii=False, indent=2)
    os.replace(catalog_tmp, catalog_path)

    # Small machine summary for the workflow to diff quickly on runs
    manifest_path = os.path.join(OUTPUT_DIR, "coligo_manifest.json")
    manifest_tmp = manifest_path + ".tmp"
    with open(manifest_tmp, "w", encoding="utf-8") as f:
        json.dump({
            "synced_at": master_catalog["synced_at"],
            "student_count": len(STUDENTS),
            "indexed_materials": total_materials_indexed,
            "new_downloads": total_new_downloads,
            "homework_signals": len(homework_items),
        }, f, ensure_ascii=False, indent=2)
    os.replace(manifest_tmp, manifest_path)

    print(f"\n[Summary] Indexed: {total_materials_indexed} items | Newly saved: {total_new_downloads} files.")

    # Step 4: Push digest to Google Sheets webhook (Web App)
    WEBHOOK_URL = os.environ["GAS_WEBHOOK_URL"].strip()
    print("\n[3/3] ☁️ Pushing live updates to Google Sheets Webhook...")
    payload = json.dumps({
            "action": "sync_coligo_feed",
            "secret": os.environ.get("SYNC_SECRET", ""),
            "timestamp": time.time(),
            "notificationsCount": len(no_rec_notifications) or len(homework_items),
            "materialsCount": total_materials_indexed,
            "newDownloads": total_new_downloads,
            "homeworkQueued": len(homework_items),
            "homework": [
                {**item, "message": str(item.get("message", ""))[:1200]}
                for item in homework_items[:100]
            ],
    }).encode("utf-8")
    req_w = urllib.request.Request(WEBHOOK_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req_w, timeout=25) as resp_w:
            response = json.loads(resp_w.read().decode("utf-8") or "{}")
            if resp_w.status >= 300 or not response.get("success"):
                raise RuntimeError("Apps Script rejected the Coligo sync summary.")
            print("✅ Sync summary recorded in Google Sheets.")
    except Exception as e:
        raise RuntimeError(f"Could not record sync summary in Google Sheets ({type(e).__name__}).") from e

    elapsed = time.time() - t0
    print(f"\n🎉 100% Autonomous Cloud Sync v2 Completed in {elapsed:.2f}s! (auth={auth_mode})")


if __name__ == "__main__":
    run_sync()
