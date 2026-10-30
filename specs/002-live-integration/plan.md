# Implementation Plan: 002-live-integration

**Branch**: `master` | **Feature Path**: `specs/002-live-integration`
**Status**: In Progress | **Readiness Gate**: Live Credentials Verified

---

## 🏗️ 1. Architecture & Autonomous Synchronization Loop

```
+-----------------------------------------------------------------------------------+
|                        AUTONOMOUS HOURLY SYNC PIPELINE                            |
+-----------------------------------------------------------------------------------+
                                        |
                   [Every Hour via GitHub Actions Cron: 0 * * * *]
                                        |
                                        v
                 +---------------------------------------------+
                 |             cloud_coligo_sync.py            |
                 |  - Username: ahmed.ibrahim144               |
                 |  - Auto-Candidate Auth: dbbfd0 / cb3882     |
                 |  - Obtains fresh 24h Coligo JWT             |
                 +---------------------------------------------+
                                        |
                    +-------------------+-------------------+
                    |                                       |
                    v                                       v
     +-----------------------------+         +-----------------------------+
     |         Ali (Year 5)        |         |       Mostafa (Year 6)      |
     | - ID: 68da68c843e7498dd...  |         | - ID: 68e6ac96b5f1511f6...  |
     | - Ingests 10 Courses        |         | - Ingests 10 Courses        |
     | - Downloads Worksheets/PPTX |         | - Downloads Worksheets/PPTX |
     +-----------------------------+         +-----------------------------+
                    |                                       |
                    +-------------------+-------------------+
                                        |
                                        v
                 +---------------------------------------------+
                 |          Persist Local Artifacts            |
                 | - resources/coligo/coligo_catalog.json      |
                 | - resources/coligo/coligo_manifest.json     |
                 | - Commits to GitHub Pages                   |
                 +---------------------------------------------+
                                        |
                                        v
                 +---------------------------------------------+
                 |   POST https://script.google.com/.../exec   |
                 |   Body: {                                   |
                 |     action: 'sync_coligo_feed',             |
                 |     secret: SYNC_SECRET,                    |
                 |     materialsCount: 164+,                   |
                 |     homeworkQueued: ...                     |
                 |   }                                         |
                 +---------------------------------------------+
                                        |
                                        v
                 +---------------------------------------------+
                 |          Google Apps Script doPost()        |
                 | - Verifies SYNC_SECRET == ScriptProperties  |
                 | - Updates 'Coligo_Hub' Sheet                |
                 | - Updates 'Homework_Status' Sheet           |
                 | - Returns: { success: true, updated: true } |
                 +---------------------------------------------+
```

---

## 🔐 2. Complete Secrets Mapping & Inventory

| Secret Name | Location | Value / Description | Status |
| :--- | :--- | :--- | :--- |
| **`COLIGO_USERNAME`** | GitHub Secrets | `ahmed.ibrahim144` | ✅ Verified Live |
| **`COLIGO_PASSWORD`** | GitHub Secrets | `dbbfd0` (Parent Login for both Ali & Mostafa) | ✅ Verified Live |
| **`COLIGO_MOSTAFA_PASSWORD`** | GitHub Secrets | `dbbfd0` (Fallback/Secondary) | ✅ Verified Live |
| **`COLIGO_ALI_PASSWORD`** | GitHub Secrets | `cb3882` (Fallback/Secondary) | ✅ Configured |
| **`GAS_WEBHOOK_URL`** | GitHub Secrets | `https://script.google.com/macros/s/AKfycbwEggLw5Go290N2Decef_TGB3x8gXN_R_RuCYo4UuZdCkGMPBI_sOQNstPds60aZUg/exec` | ✅ Live (HTTP 200) |
| **`SYNC_SECRET`** | GitHub Secrets & Script Properties | `PRIMARY_SYNC_2026_x89a4df1` (Shared Authentication Key) | ⏳ Awaiting Setup |
| **`ADMIN_PIN_HASH`** | Apps Script Properties | `77aab5fd559133be7e989ee0e878da15f9bd1d93f1f1a3d939f4c69f593b48ff` (PIN `1990`) | ⏳ Awaiting Setup |
| **`ALI_PIN_HASH`** | Apps Script Properties | `15fc7eebd45d4b33fe2680e3c8f7c03ed56308e536165cbf887147569feab8e6` (PIN `2016`) | ⏳ Awaiting Setup |
| **`MOSTAFA_PIN_HASH`** | Apps Script Properties | `b77a0882d18ceb8585bed60cac90d832ba84c9b71879a5442f883b6c08a91290` (PIN `2014`) | ⏳ Awaiting Setup |

---

## 📋 3. Step-by-Step Execution Plan

### Step 1: Resilient Ingestion Script & Workflow Updates
- Multi-password fallback candidate list implemented in `cloud_coligo_sync.py`.
- Workflow `.github/workflows/coligo-cloud-sync.yml` updated with candidate password variables.

### Step 2: Apps Script Code & Deployment Synchronization
- Update Google Apps Script Editor with latest `Code.gs` containing `doPost(e)`.
- Deploy as a **"New version"** under `Manage deployments` to activate `doPost(e)` on the `/exec` URL.
- Set Script Properties in Project Settings.

### Step 3: GitHub Repository Secrets Configuration
- Configure GitHub Actions secrets with verified credentials.

### Step 4: End-to-End Live Verification
- Trigger `workflow_dispatch` on GitHub Actions or run local test push to verify full sync and confirmation.
