#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
  COLIGO CLOUD SYNC & GOOGLE SHEETS PIPELINE
  Fully autonomous cloud-based ingestion for Ali Ahmed & Mostafa Ahmed
  Runs on GitHub Actions Cron / Cloudflare Worker / Local Task Scheduler
================================================================================
"""

import os
import sys
import json
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "resources", "coligo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Resolve Auth Token from Environment or Local Config
TOKEN = os.environ.get("COLIGO_TOKEN")
if not TOKEN:
    ls_file = os.path.join(OUTPUT_DIR, "local_storage.json")
    if os.path.exists(ls_file):
        with open(ls_file, "r", encoding="utf-8") as f:
            ls = json.load(f)
            TOKEN = ls.get("token")

if not TOKEN:
    print("[ERROR] No Coligo token found in environment (COLIGO_TOKEN) or local_storage.json")
    sys.exit(1)

WEBHOOK_URL = os.environ.get("GAS_WEBHOOK_URL")

HEADERS = {
    "Authorization": f"JWT {TOKEN}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[Warning] Failed to fetch {url}: {e}")
        return None

def run_sync():
    print("🚀 [Cloud Sync] Starting Autonomous Coligo LMS Ingestion...")
    
    # A. Fetch Latest 100 Notifications (Daily Announcements, Homework & Grades)
    notif_url = "https://prod-api.coligolms.com/api/v0/users/me/notifications?limit=100"
    notifs = fetch_json(notif_url) or []
    print(f"✅ Fetched {len(notifs)} recent notifications from Coligo.")

    # Save locally
    with open(os.path.join(OUTPUT_DIR, "all_notifications.json"), "w", encoding="utf-8") as f:
        json.dump(notifs, f, ensure_ascii=False, indent=2)

    # B. Extract Active Homework & Materials
    homework_items = []
    for n in notifs:
        msg = n.get("message", "")
        # Filter for homework, quizzes, announcements
        if any(k in msg.lower() for k in ["homework", "واجب", "quiz", "announcement", "created in", "material"]):
            homework_items.append({
                "id": n.get("_id"),
                "date": n.get("createdAt"),
                "message": msg,
                "type": n.get("type"),
                "read": n.get("state") == "@notification-state/read"
            })

    print(f"📌 Filtered {len(homework_items)} active school events/homework items.")

    # C. Push to Google Apps Script / Google Sheets Webhook if configured
    if WEBHOOK_URL:
        print("☁️ Pushing synced data to Google Apps Script Webhook...")
        payload = json.dumps({
            "action": "sync_coligo_feed",
            "secret": os.environ.get("SYNC_SECRET", "manaret_eleman_secure_sync"),
            "timestamp": time.time(),
            "notificationsCount": len(notifs),
            "homework": homework_items[:30]
        }).encode("utf-8")
        
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                result = resp.read().decode("utf-8")
                print("✅ Successfully synchronized with Google Sheets Cloud Database:", result)
        except Exception as e:
            print("[Warning] Could not reach Google Apps Script webhook:", e)
    else:
        print("ℹ️ Note: GAS_WEBHOOK_URL not set in environment. Saved locally to resources/coligo/")

    print("🎉 Coligo Cloud Ingestion Completed Flawlessly.")

if __name__ == "__main__":
    import time
    run_sync()
