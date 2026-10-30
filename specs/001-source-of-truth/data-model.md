# Data Model: Source of Truth (P0)

**Feature**: `001-source-of-truth` | **Derived from**: live git state + repo
survey evidence (see research.md F1–F11). No product-data entities; this is a
process/evidence model.

## Entities

### CodeVersion — one row per deployable-surface file

| Field | Type / allowed values | Rules |
|---|---|---|
| file | path (normalized ASCII, exact casing recorded) | covers Apps Script files, `Index.bundle.html`, `index.html` (Pages), `bundle.py`, workflows |
| repoState | `tracked@<commit>` / `modified-uncommitted` / `untracked` | full casing recorded (`index.html` ≠ `Index.html` — known Linux Pages trap) |
| publishedState | `published` / `unpublished` / `غير معروف` | Apps Script-side starts `غير معروف` until owner export (research D3) |
| evidence | source + date (command output link, HTTP probe, export receipt) | mandatory; `غير معروف` rows MUST state WHY unknown |
| roles | entry-points map | which file serves which surface (Apps Script `'Index'` vs Pages lowercase entry) |

Validation: no row may claim `published` without dated evidence link
(Principle VIII). Row set MUST cover 100% of deployable surfaces (SC-001).

### MaterialFile — untracked content survival guard

| Field | Values | Rules |
|---|---|---|
| path | exact untracked path | pre-merge inventory list (from `git status --porcelain`) |
| preState | `untracked` + (hash if file) | SHA-256 where file, folder checksummanifest where dir |
| outcome | `kept-untracked` / `committed` / `replaced-by-tracked-identical` / `exception-documented` | replaced-by-tracked-identical REQUIRES both-sides hash equality recorded in merge log |
| evidence | hash pair + decision note | mandatory for any replacement |

Validation: zero rows ending vanished (SC-002). Deletion is NEVER an outcome;
`replaced-by-tracked-identical` is the ONLY non-kept outcome.

### OctFixLedger — 4 prefilled fix states

| Fix | State (prefilled) | Evidence pointer | Transition rules |
|---|---|---|---|
| Server-minted typed tokens | مثبّت | `Code.gs` `storeAccessToken_` L2058 / `getAccessTokenClaims_` L2068 / `verifyGatewayPin` L2156 | may only move to مثبّت+stronger evidence; never regresses silently |
| No PINs in live code | مثبّت | live `Code.gs` grep; legacy copies quarantined | legacy quarantine evidence added (`legacy_index.html`, `Code.gs.bak`, android copy) |
| `//`→`\/\/` rule | مثبّت | `bundle.py` L4,15-28,58-59 + historical BUG-012 doc | modular fragments stay raw-by-design (escaped at bundle time) |
| Optional error bar | غير مطلوب | doc-only mention (roadmap L83); zero code ever | terminal state unless owner reorders requirement |

Ledger MUST contain exactly one of مثبّت/مدمج/غير مطلوب per fix after tasks —
zero `unknown` endpoints (SC-005).

### StatusRecord — `CURRENT_STATUS_AR.md` (the single truth file)

Sections (schema contract in `contracts/truth-ledger-format.md`):
1. **حالة المنظومة** — one paragraph, claim-free or evidence-linked.
2. **جدول الحقيقة** (CodeVersion rows).
3. **دفتر الإصلاحات** (OctFixLedger).
4. **سجلو الدمج** (merge outcome: divergence resolved shape `ahead 0/behind 0`,
   hash-equal replacements list, exceptions with reasons).
5. **به هيجة نظم أسطر** — baseline test record: command + date + counts +
   failures (honest RED allowed; expected: RED vs legacy-contract suite).
6. **منصة الوصول** — Pages URL (known+verified) + Web App URL
   (owner-supplied or `غير معروف`).
7. **مؤشّر التوثيق** — the 17 historical banners map + claim-conflict map
   citation (F10).

Validation: this file is the ONLY "authoritative" status; every other doc
carries its historical banner; no "100%/بلا عيوب" claim survives in ACTIVE
docs without a dated evidence link (SC-004).

### BotCommit — remote sync head semantics

The remote-extra commit `7271ba6` (hourly cloud-sync bot output) is treated as
canonical for catalog/manifest artifacts it produces; local uncommitted
modifications to those same files follow D2's hash rule — local content wins
only where hashes differ and the local copy is the newer artifact (recorded).

## Aggregation algorithm contract (prose, for tests)

1. Inventory: capture `git status --porcelain=v1 -b` output as the immutable
   pre-merge list (MaterialFile rows).
2. Fetch & compute the exact overlap between local untracked paths and
   incoming tracked paths of `origin/master`.
3. For each overlap: hash both sides; decide per D2; append one merge-log
   entry per decision.
4. Rebase local doc commit onto remote head; resolve the 9 modified tracked
   files with D2 discipline (catalog/manifest: hash rule; docs: evidence
   favoring facts).
5. Post-merge: verify zero lost rows; `git status` clean or exceptions
   documented; workflows still valid (`yml` parse + referenced files exist).
6. Fill truth table rows (repo side immediate; Apps Script side per D3);
   fill ledger; write the baseline record; update status file; add historical
   banners; correct README claims.
