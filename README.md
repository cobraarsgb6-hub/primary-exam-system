# Primary Exam System — G5 & G6

A Google Apps Script + Google Sheets assessment portal for primary grades.

## Current status

The project is a **single-family / small-class pilot**, not a multi-tenant school platform. The student and parent portals are separated by a server-verified PIN gateway (`verifyGatewayPin`), and every admin mutation requires a short-lived `ADMIN_TOK_*` token. See [`FIXES_APPLIED.md`](FIXES_APPLIED.md) and [`PROJECT_REVIEW_AR.md`](PROJECT_REVIEW_AR.md).

## Files

| File | Purpose |
|---|---|
| `Code.gs` | Apps Script backend: setup, sessions, scoring, retakes, exam factory, Coligo/Drive sync |
| `Index.html` | Portal shell + all screens; pulls in the four templates below via `include()` |
| `Styles.html` | Extracted CSS |
| `HubData.js.html` | Static catalogs, standalone engine, video/Coligo/homework UI logic |
| `QuizApp.js.html` | Quiz runtime, timer, submission and result rendering |
| `Portal.js.html` | Student dashboard, Parent Portal, Study Plan, exam factory UI |
| `Index.bundle.html` | Fully resolved single-file build (offline + Android kiosk) |
| `bundle.py` | Builds `Index.bundle.html` from `Index.html` + includes |
| `Question_Bank.csv` | 45 sample questions |
| `Exams.csv` | 3 sample exam definitions |
| `appsscript.json` | Web app / runtime manifest |
| `SETUP_GUIDE.md` | Arabic setup guide |
| `tests/server.test.js` | Server regression tests (Node VM + fake Sheets) |
| `tests/e2e/` | 51-scenario Playwright suite |

## Run tests

```bash
npm test                      # 43 unit + server tests
python tests/e2e/run_all_e2e.py   # 51 E2E scenarios
python test_ui_buttons.py         # 51 static button controls
```

Requires Node.js 20+ and Python 3 with Playwright for the browser suites.

## Deploy

1. Back up the Google Sheet.
2. Copy `Code.gs` plus **either**:
   - `Index.html`, `Styles.html`, `HubData.js.html`, `QuizApp.js.html`, `Portal.js.html` (modular `include()` deployment), **or**
   - the contents of `Index.bundle.html` pasted as `Index.html` (single-file deployment).
3. Save and deploy a **new version**. The first run after adding Drive/UrlFetch/trigger code may ask for extra OAuth scopes.
4. Run **⚙️ Full Database Auto-Format & Setup** once. It is non-destructive and creates/migrates `Submissions`, `Question_Bank`, `Exams` (11 columns), `Retake_Requests`, `Sessions`, `Study_Plan`, `Coligo_Hub` and `Homework_Status`.
5. Open the web app URL.

### Optional integrations

| Script property | Purpose |
|---|---|
| `COLIGO_HUB_FEED_URL` | JSON feed consumed by `syncColigoOnline`. Accepts an array or `{items:[...]}` |
| `DRIVE_VIDEOS_FOLDER_ID` | Set automatically by **Sync Google Drive Videos** |

The Drive sync maps each video file by its filename (without extension), so name files after the YouTube ID they replace (for example `WYOD4qXW0SE.mp4`).

## Adding an exam

1. Add a row to `Exams` with status `ACTIVE` or `نشط`.
2. Add questions to `Question_Bank` with the same `Exam Code`.
3. Separate options with `|`; the correct answer must exactly match one option.
4. Reload the web app.

Weekly/monthly exams can instead be generated from the Parent Portal (or the sheet menu). They store `Exam Type` + `Target Period` and serve questions from the matching period slice of `Question_Bank`; creation is refused when that slice is empty.

## Known limitations

- The web app is deployed as `ANYONE_ANONYMOUS` + `USER_DEPLOYING`, so server RPCs run as the owner; the PIN gateway protects the UI, not the underlying endpoints.
- Question types are limited to MCQ and True/False.
- Some generated fallback questions still contain content errors.
- The UI is mostly English; Arabic content is RTL but the chrome is not localized.
- No skill-mastery analytics yet.
