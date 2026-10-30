# Implementation Plan: Source of Truth (P0)

**Branch**: `001-source-of-truth` | **Date**: 2026-10-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-source-of-truth/spec.md`

## Summary

Reconcile the diverged repository (local `master` ahead 1 doc-commit,
behind 1 bot-generated cloud-sync commit `7271ba6`) WITHOUT losing the ~100+
untracked Coligo material directories and 21 helper scripts, verify the
October-28 security fixes already present in live `Code.gs`, document the
quarantine of legacy token/PIN-bearing copies, collapse all activity
documentation into one truth file (`CURRENT_STATUS_AR.md`, which already
exists in proto-form), record the live Pages URL (verified reachable today)
and the Web App URL (owner-supplied, else "غير معروف"), and record a dated,
honest baseline of the currently-RED test suite. No product behavior changes.

## Technical Context

**Language/Version**: Git operations (`git` CLI, PowerShell tooling); Python 3
is used only to READ/hash-compare, never to mutate data outside git; content
is Arabic Markdown documents (RTL discipline applies to system-rendered
content only).

**Primary Dependencies**: Existing GitHub Actions automations
(`coligo-cloud-sync.yml` hourly cron; `deploy-pages.yml` on push) MUST keep
running; `bundle.py` stays untouched; no new dependencies.

**Storage**: The truth ledger lives in `CURRENT_STATUS_AR.md` (single
authoritative file). The ledger's row/entry schema is defined in
`contracts/truth-ledger-format.md`.

**Testing**: Baseline record only — `npm test` (known RED: legacy contract),
E2E/button suites recorded as counts-at-`HEAD`; fixing tests is NOT in this
phase (FR-008; test refresh belongs to P5's gate work).

**Target Platform**: Local repository + GitHub (`origin/master`); published
surfaces = GitHub Pages (`https://cobraarsgb6-hub.github.io/primary-exam-system/`
— verified reachable 2026-10-30) and the Apps Script Web App (URL currently
not stored in-repo; owner-supplied or "غير معروف").

**Performance Goals**: N/A (process/documentation phase) — bounded by: zero
lost files, zero broken workflows.

**Constraints**: Scrictly append-only discipline entails NO deletion of
material content; byte-identical untracked duplicates of incoming tracked
bot files may be replaced by their canonical tracked version (documented,
hashed). No force push, no history rewrite, no new tools.

**Scale/Scope**: 1 reconciliation commit set, ~120 untracked paths
inventoried, 19 documentation files classified (1 truth + 1 roadmap active +
17 historical/corrected), 4 ledger entries (Oct-28 fixes), 1 baseline test
record, 1 URL record. Phase touches docs + git only.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Status | Evidence / Notes |
|---|---|---|
| I. Sheet Data SoT / append-only | PASS by design | Merge MUST delete NO material: byte-identical untracked duplicates of incoming tracked files are replaced by their canonical tracked copy (hash-verified both sides), everything else is preserved or committed. Legacy snapshots (`Code.gs.bak`, `legacy_index.html`, `android\…\www\index.html`) stay on disk (quarantined), deletion is a separate explicit decision. |
| II. Server-Verified Access | PASS | Live `Code.gs` verified clean during research: typed `ACCESS_TOK_*` claims via `storeAccessToken_`/`getAccessTokenClaims_`, PIN hashes only from Script Properties, zero hardcoded PINs. Legacy token-bearing copies exist (`legacy_index.html`, `Code.gs.bak`, android copy) → ledger marks them quarantined/non-authoritative; README's stale `ADMIN_TOK_*` claim gets corrected. |
| III. Regression-Gated (Test-First) | ATTENTION (recorded, not executed) | Baseline record is the deliverable: `npm test` is RED against current contract (verified during mastery research); P0 records it honestly with command+date, and MUST NOT claim green. Fixing suites belongs to P5. |
| IV. Arabic-First / NFKC | PASS | Status content is Arabic; ledger keys remain ASCII-safe (commit ids, paths); NFKC applies where the system renders content. |
| V. Simplicity | PASS | No new scripts/engines: plain `git` + existing tooling; the plan invents only document schemas. |
| VI. Student Isolation / Privacy | PASS | No new publication; existing Pages content review is P2's job (recorded, not changed here). |
| VII. Secrets Discipline | PASS | No secrets moved; Web App URL is not a secret (it's a public `/exec` URL by design) and goes into the truth file; nothing secret enters any file. |
| VIII. Evidence-Based Status | PASS (this IS the phase) | Every ledger row carries source+date; "غير معروف" is a legal recorded state anywhere evidence is missing (e.g., Apps Script side until owner export). |

Verdict: **No violations.** Complexity Tracking: empty.

## Project Structure

### Documentation (this feature)

```text
specs/001-source-of-truth/
├── spec.md / plan.md / research.md / quickstart.md
├── contracts/truth-ledger-format.md   # schema contract for CURRENT_STATUS_AR.md
└── tasks.md                           # /speckit-tasks output (NOT here)

CURRENT_STATUS_AR.md                   # THE single authoritative status file (promoted)
ROADMAP_SPECKIT_AR.md                  # active phase tracker (stays authoritative for phases)
```

### Source Code (repository root)

```text
Code.gs / Index.template.html / HubData.js.html / Portal.js.html /
QuizApp.js.html / Styles.html / Index.bundle.html / index.html
    → untouched in P0 EXCEPT: zero-diff confirmations recorded
Code.gs.bak / legacy_index.html / android\app\src\main\assets\www\index.html
    → quarantined entries in ledger; files NOT deleted
.github/workflows/*.yml                → must remain valid (validated, not rewritten)
README.md                              → corrected stale claims (ACCESS_TOK_ text)
17 legacy docs (*_AR.md, FIX_PLAN, TEST_READY, …)
    → "historical, not authoritative" banner + rewrite-driven claim fixes
resources/coligo/**  (≈100 dirs)  + 21 helper .py scripts
    → inventoried; hash-compared vs incoming bot commit; preserved
my-project/  (39-file stray Spec Kit scaffold, origin unknown)
    → inventoried; owner decides keep/remove (no silent deletion)
```

**Structure Decision**: No new directories beyond this spec's folder; the
repository's existing layout is reconciled, not reorganized.

## Complexity Tracking

No violations requiring justification.
