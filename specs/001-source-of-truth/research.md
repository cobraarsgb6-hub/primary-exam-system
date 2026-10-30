# Research: Source of Truth (P0)

**Feature**: `001-source-of-truth` | **Date**: 2026-10-30
**Method**: delegated code/document exploration + direct git host commands +
a live HTTP probe of the published Pages site. Facts below are as of today.

## Verified facts (evidence table)

| # | Fact | Evidence |
|---|---|---|
| F1 | Branch `master` is **ahead 1 / behind 1** vs `origin/master`; local extra commit = `6ef8be3` (docs-only review append); remote extra = `7271ba6` (hourly cloud-sync bot commit: catalog+materials) | `git rev-list --left-right --count origin/master...HEAD` = `1 1`; `git log` both heads |
| F2 | 9 tracked modified files locally (sync workflow, docs, index.html, sync script, catalog+manifest JSONs) + ~120 untracked paths (≈100 `resources/coligo/**` material dirs incl. children's course content, 21 helper scripts, speckit scaffolding, `my-project/` stray scaffold, ROADMAP) | `git status --porcelain=v1 -b` |
| F3 | Live `Code.gs` is clean of hardcoded XXX: typed tokens (`storeAccessToken_` L2058, `getAccessTokenClaims_` L2068 with `ACCESS_TOK_` prefix check, `verifyGatewayPin` L2156 reading `*_PIN_HASH` Script Properties only; SHA-256 `hashPin_` L2133; rate limit 8→10min). Zero grep hits for `1990|ADMIN_TOK_` | exploration report §1a |
| F4 | Token/PIN-bearing legacy copies exist and stay quarantined: `legacy_index.html` (L6770/8013/8085-8131), `android\app\src\main\assets\www\index.html` (same), `Code.gs.bak` (L2040-2151) | exploration §1a |
| F5 | `//`→`\/\/` rule: implemented in `bundle.py` (docstring L4; string-literal-only replacement L15-28; applied to bundle + Pages index + android copy L58-59). Raw `'https://` literals only in `HubData.js.html` fragments (bundled copies are escaped). `Code.gs` serves `createHtmlOutputFromFile('Index')` (L842) while no `Index.html` source exists in-repo → Apps Script side is publish-state "غير معروف" until owner export | exploration §1b |
| F6 | "Optional error bar": doc mention only (roadmap L83); zero runtime code anywhere → ledger "غير مطلوب" with that reason (no fix was ever created) | exploration §1c |
| F7 | GitHub Pages live URL `https://cobraarsgb6-hub.github.io/primary-exam-system/?v=dynamic_v2` fetched TODAY: **HTTP 200, full portal rendered** (Manaret El-Eman hub — cloud banner, subjects, exams center, labs). | live probe (webfetch, 2026-10-30) |
| F8 | No deployed Apps Script Web-App URL stored anywhere in-repo (only in secret `GAS_WEBHOOK_URL`) → owner supplies it or row stays "غير معروف" | exploration §7 |
| F9 | A proto truth-file exists: `CURRENT_STATUS_AR.md` (10/30 04:08) with sections ثبت/غير منشور/يحتاج تحقق/حالة Git/القرار — promoted to THE authoritative file | exploration §6 |
| F10 | Claim-conflict map recorded: "100%/بلا عيوب/Zero-Defect" in `PROJECT_MASTER_HISTORY_AND_AUDIT.md:9`, `PROJECT_MASTER_DOCUMENTATION.md:6,258-345`, `TEST_READY.md:4,79,96`, `PROJECT_COMPREHENSIVE_AUDIT_REPORT.md:5,122,142,177`, `FIX_PLAN.md`; test-count conflicts 43/51/53/57 across ≥6 docs | exploration §2 |
| F11 | Workflows healthy-ish: `coligo-cloud-sync.yml` (hourly cron, webhook-fail→run-fail contract holds), `deploy-pages.yml` (hard-requires `coligo_catalog.json`, validates `/exec` URL), `build-apk.yml` (manual) — none dangling | exploration §5 |

## Decisions (with alternatives)

### D1 — Merge shape: rebase the single local doc commit onto remote bot commit

- **Decision**: `git fetch` → rebase local `6ef8be3` (docs-only) onto
  `origin/master` (bot head `7271ba6`). Conflicts expected ONLY with the 9
  locally-modified tracked files; catalog/manifest JSONs resolve as per D2.
- **Rationale**: one-side history is a pure merge, no rewrite, no force push
  (FR-002); local extra commit is documentation review text.
- **Alternatives**: manual cherry-pickų (over-engineered); merge commit
  creating criss-cross noise (rejected; rebase keeps linear clean state).

### D2 — Untracked-vs-incoming duplication rule (THE zero-loss rule)

- **Decision**: For every untracked local path that ALSO arrives tracked from
  `origin/master` (bot-uploaded materials): hash both sides first
  (SHA-256). Identical → the local untracked copy is replaced by the tracked
  canonical version (a byte-identical duplicate replacement — NOT loss;
  recorded in the merge log with both hashes). Different → the local file is
  preserved (committed as a variant or kept as an explicitly documented
  exception) — never silently overwritten.
- **Rationale**: the bot already ran and committed materials upstream; local
  untracked copies are the same sync artifacts. Hash discipline converts a
  dangerous default-overwrite into a provable no-loss operation; append-only
  wording preserved because this is a state framing fix (identical bytes),
  documented transparently.
- **Alternatives**: blind `git clean` (forbidden — destructive); skipping
  hash check and trusting names (rejected — violates FR-002 intent).

### D3 — Apps Script-side evidence acquisition

- **Decision**: Ledger rows for Apps Script-published state start as
  "غير معروف" until the owner supplies a dated export of the deployed
  project files (at minimum the current `Index`,`Code.gs` copies) — then
  rows upgrade to مثبّت with source+date. The repo rows are known and
  evidence-able immediately.
- **Rationale**: FR-001 forbids assuming; a browser export is honest
  evidence. `doGet` serves `'Index'` which exists only inside the Apps Script
  project.
- **Alternatives**: trust remote state from docs (rejected — that assumption
  caused this phase).

### D4 — Documentation collapse: promote, banner, correct — no content deletion

- **Decision**: `CURRENT_STATUS_AR.md` = single authoritative status
  (update with ledger + URLs + baseline); `ROADMAP_SPECKIT_AR.md` stays
  active as the phase plan tracker; every OTHER .md gets a short
  "historical, not authoritative" banner; `README.md` gets factual
  corrections (typed-token text, current file roles) but remains active as
  the living deploy guide. No document is deleted; claims are fixed in
  place or banner-marked with the claim-conflict map from F10 cited in the
  status file.
- **Rationale**: satisfies FR-004/FR-005 with minimal motion and zero
  information loss; the claim map becomes evidence-cited rather than lost.
- **Alternatives**: deleting legacy docs (forbidden: separate decision,
  owner's call later); editing claims inside all legacy docs (wasted effort —
  banner disclaims them).

### D5 — Oct-28 fix ledger states (prefilled from research)

| Fix | Prefill | Basis |
|---|---|---|
| Server-minted typed tokens | **مثبّت** | F3 (function+line evidence in live Code.gs) |
| No PINs in live code | **مثبّت** | F3 + F4 (legacy copies quarantined, non-authoritative) |
| `//`→`\/\/` rule | **مثبّت** | F5 (bundle.py implements; fragments raw-by-design) |
| Optional error bar | **غير مطلوب** | F6 (no code ever existed; doc-only mention) |

Tasks only add evidence-pointer polish; nothing here requires new code.

### D6 — Baseline test record (honest RED)

- **Decision**: Record `npm test` (plus E2E/button suites as count-probes)
  with command+UTC-ish date+counts+template evidence of failures. NO fixing
  inside P0; the RED baseline is the honest floor P5 later proves green.
- **Alternatives**: fixing suites now (scope violation FR-008); omitting the
  record (violates FR-007/Principle VIII).

### D7 — Stray `my-project/` scaffold (39 files, origin unknown)

- **Decision**: Inventory-only in P0; owner decides keep/delete later — no
  silent deletion (respecting unknown-user-work discipline).
- **Alternatives**: delete now (rejected — unknown provenance).

## Open Unknowns (handed to tasks, not silently resolved)

1. Web App `/exec` URL — owner input needed (FR-006 evidence; else stays
   "غير معروف" with reason).
2. Apps Script project export — owner input needed for D3 rows.
3. Exact conflict resolution inside the 9 modified tracked files — resolved
   during tasks with the hash/diff discipline, never by assumption.
