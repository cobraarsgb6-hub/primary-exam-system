# Primary Exam System — G5 & G6

A Google Apps Script + Google Sheets assessment portal for primary grades.

## Current status

The project is a **single-family / small-class pilot**, not a multi-tenant school platform. Authentication is intentionally not implemented because the app is used on one shared device. See [`FIXES_APPLIED.md`](FIXES_APPLIED.md) and [`PROJECT_REVIEW_AR.md`](PROJECT_REVIEW_AR.md).

## Files

| File | Purpose |
|---|---|
| `Code.gs` | Apps Script backend: setup, sessions, scoring, retakes, Forms |
| `Index.html` | Single-page portal: student, quiz, result, parent/teacher |
| `Question_Bank.csv` | 45 sample questions |
| `Exams.csv` | 3 sample exam definitions |
| `appsscript.json` | Web app / runtime manifest |
| `SETUP_GUIDE.md` | Arabic setup guide |
| `tests/server.test.js` | Server regression tests |

## Run tests

```bash
node --test tests/server.test.js
```

Requires Node.js 20+.

## Deploy

1. Back up the Google Sheet.
2. Copy `Code.gs` and `Index.html` into the Apps Script editor.
3. Save and deploy a **new version**.
4. Run **⚙️ Full Database Auto-Format & Setup** once. It is non-destructive and creates the `Sessions` tab if needed.
5. Open the web app URL.

## Adding an exam

1. Add a row to `Exams` with status `ACTIVE` or `نشط`.
2. Add questions to `Question_Bank` with the same `Exam Code`.
3. Separate options with `|`; the correct answer must exactly match one option.
4. Reload the web app.

## Known limitations

- No authentication/roles (by request for shared-device use).
- Question types are limited to MCQ and True/False.
- Some generated fallback questions still contain content errors.
- The UI is mostly English; Arabic content is RTL but the chrome is not localized.
- No skill-mastery analytics yet.
