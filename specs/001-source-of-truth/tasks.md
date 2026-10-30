# Tasks: Source of Truth (P0)

**Input**: Design documents from `/specs/001-source-of-truth/`

**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/truth-ledger-format.md ✅ | quickstart.md ✅

**Tests**: This is a process/evidence phase (FR-008 forbids new product behavior). No new test code is authored. FR-007 requires an HONEST baseline test record — recorded even when RED.

**Organization**: Tasks grouped by user story (US1 truth table, US2 zero-loss merge, US3 Oct-28 ledger, US4 single truthful status) in execution-safe order.

⚠️ **PROCESS-TRUTH PHASE NOTE**: The actual merge discipline (Phase 4 / US2) runs AFTER its inventory tasks in Phases 1–3, because a safe merge depends on them. Task order below is the physically safe order, not cosmetic.

## 🔒 HARD SAFETY RULES (apply to every task)

1. **FORBIDDEN**: `git clean`, force push, `push --force*`, history rewrite of `origin/*`, `git checkout -- .`, deleting/quarantining WITHOUT receipt, `git reset --hard` while untracked material files are at risk.
2. Every byte that changes place is pre-registered by SHA-256 in the inventory before the move.
3. The hourly bot (`0 * * * *`) may advance `origin/master` mid-work: re-fetch before each state-changing git step; if a new head appears, bind to the NEWEST head and record both heads in `merge-log.md`.
4. On any failure inside the rebase: `git rebase --abort` restores state; the staged move-aside copies stay at `C:\Users\co0ob\Projects\p0_merge_stage\` (outside repo) until verified.
5. PowerShell lesson (recorded): pass literal filenames, do NOT rely on `*` expansion for external commands; use `python` (3.14.7 verified) for UTF-8 path safety.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: parallel-safe (different files, no dependency on an incomplete task)
- **[Story]**: US1/US2/US3/US4 from spec.md

---

## Phase 1: Setup (Immutable Pre-Merge Evidence)

**Purpose**: Freeze the pre-merge world so nothing can be lost silently.

- [x] T001 Create `specs/001-source-of-truth/inventory/` and save the pre-merge state: `git status --porcelain=v1 -b`, `--untracked-files=all -z` decoded listing, and `git -c core.quotepath=false ls-tree -r --name-only <origin head>` → `inventory/pre-merge-status.txt`, `inventory/untracked-all.txt`, `inventory/ls-tree-origin.txt`
- [x] T002 Record heads evidence (local-only commit `6ef8be3`, remote heads incl. `7271ba6` and any newer like `9d4ed4a`) → `inventory/heads-evidence.md` with exact `git log --oneline` output
- [x] T003 [P] Re-fetch and record any further bot advancement into `heads-evidence.md` (pre-flight observation, no mutation)

**Checkpoint**: The pre-merge world is immutable-on-record. Merge work may not start before this signature exists.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the overlap/hash truth that makes the zero-loss merge provable.

**⚠️ CRITICAL**: No rebase begins until T008 passes.

- [x] T004 Compute the overlap set = untracked-local files ∩ tracked-in-origin files → `inventory/overlap-analysis.md` (path × present-on-origin × notes)
- [x] T005 [P] SHA-256 both sides for every overlap file (local working-tree bytes vs `<origin head>` blob bytes) → `inventory/overlap-hashes.csv` with equality flag
- [x] T006 Stage move-aside: for each overlap file, move the local untracked copy to `C:\Users\co0ob\Projects\p0_merge_stage\<hash8>\<relpath>` and write `inventory/stage-receipt.md` (from-path, to-path, sha256-before; NEVER delete bytes)
- [x] T007 Commit a WIP snapshot of ONLY tracked modifications (`git add -u` → commit `chore(p0): snapshot local tracked modifications pre-rebase`) — guarantees every losing variant survives in history
- [x] T008 Pre-rebase gate: re-fetch; recompute overlap (must be ZERO remaining collision with the new head); record divergence counts and new origin head into `heads-evidence.md`; proceed only if gate = PASS

**Checkpoint**: Merge can no longer lose a tracked or untracked byte.

---

## Phase 3: User Story 2 — The merge loses nothing (Priority: P1) 🎯 (executed first by dependency)

**Goal**: One reconciled branch: `behind 0` vs `origin/master`, zero material loss, clean tree or documented exceptions.

**Independent Test**: Survival audit — every path from `untracked-all.txt` + every pre-merge tracked file is accounted for as kept / moved-aside(with receipt) / replaced-by-tracked-identical(both hashes recorded) / committed.

### Implementation for User Story 2

- [x] T009 [US2] `git rebase <origin-head>` replaying the WIP commit onto the bot head; resolve conflicts ONLY in the conflicted files using the D2 rules of research.md — bot artifacts (`resources/coligo/coligo_catalog.json`, `coligo_manifest.json`): incoming unless local strictly-newer evidence; docs (`CURRENT_STATUS_AR.md`, `SECURITY_SETUP.md`, `GLM_OPERATIONAL_PLAN.md`, `CODEX_PROJECT_PLAN_REVIEW_AR.md`): keep local, add/remove as reconciled truth; code (`cloud_coligo_sync.py`, workflows, `index.html`): evidence-diff decides; every resolution choice logged with reason
- [x] T010 [US2] Confirm rebase completion; final shape `behind 0` (re-fetch may reveal new bot head → repeat T008→T009 shim once; log the bind)
- [x] T011 [US2] Zero-loss survival audit comparing Phase-1 inventory to post-merge reality → `inventory/survival-audit.py` + `inventory/survival-audit.md` (classifications per path; ZERO `vanished` outcomes enforced — any vanished path = phase fails)
- [x] T012 [US2] Post-merge logical commits: (a) material preservation commit for non-overlap untracked `resources/coligo/**`, (b) helper .py scripts archive commit, (c) speckit harness adoption commit (`.specify/`, `.agents/`, `.opencode/`, `ROADMAP_SPECKIT_AR.md`, `specs/`) — `my-project/` stays untracked + documented (data-model: owner decides)
- [x] T013 [US2] Validate automation integrity: `.github/workflows/coligo-cloud-sync.yml` + `deploy-pages.yml` parse-light check + referenced files exist (incl. tracked `resources/coligo/coligo_catalog.json`) → note in `merge-log.md`
- [x] T014 [US2] Write `specs/001-source-of-truth/merge-log.md`: divergence shape before/after, both-hash identical-replacement list, move-aside variants, exceptions with reasons

**Checkpoint**: US2 independently verifiable via `survival-audit.md` + `git status` + `merge-log.md`.

---

## Phase 4: User Story 1 — The maintainer sees exactly what is published (Priority: P1)

**Goal**: One truth table: file → repo commit → published state → dated evidence (or honest `غير معروف`).

**Independent Test**: Pick any main file, follow its row's evidence, confirm repo/Apps-Script/app agreement row by row.

### Implementation for User Story 1

- [x] T015 [P] [US1] Probe live surfaces NOW: GitHub Pages URL (HTTP status + spot content) and Web App `/exec` URL attempt (if owner-supplied it goes in the row; absence stays `غير معروف` with reason "not stored in-repo; owner input pending") → evidence recorded in `CURRENT_STATUS_AR.md`
- [x] T016 [US1] Build جدول الحقيقة rows in `CURRENT_STATUS_AR.md` strictly per `contracts/truth-ledger-format.md`: `Code.gs`, Apps Script HTML templates (`Index`/`HubData.js.html`/`Portal.js.html`/`QuizApp.js.html`/`Styles.html`), `Index.bundle.html`, `index.html` (Pages entry), `bundle.py`, `.github/workflows/*.yml`, `cloud_coligo_sync.py` — every row: repoState + publishedState + evidence + date; Apps Script rows start `غير معروف` until the owner's dated export (research D3)

**Checkpoint**: SC-001 satisfiable: 100% rows evidenced or honest-unknown.

---

## Phase 5: User Story 3 — October-28 fixes accounted (Priority: P2)

**Goal**: Each of the 4 fixes ends exactly one of مثبّت/مدمج/غير مطلوب with an evidence pointer — zero unknowns.

**Independent Test**: Follow each ledger evidence pointer into the code at final HEAD; presence provable per fix.

### Implementation for User Story 3

- [x] T017 [P] [US3] Fill دفتر الإصلاحات in `CURRENT_STATUS_AR.md` from research D5 prefill, adding exact file:line evidence: typed tokens (`Code.gs` `storeAccessToken_`) + `getAccessTokenClaims_` + `verifyGatewayPin`; PIN-free live code + quarantine list (`legacy_index.html`, `Code.gs.bak`, `android\app\src\main\assets\www\index.html`); `//`→`\/\/` rule (`bundle.py` with line refs); optional error bar → `غير مطلوب` (doc-only mention, zero runtime code)

**Checkpoint**: SC-005: zero `unknown` endpoints.

---

## Phase 6: User Story 4 — One truthful status, no magic claims (Priority: P2)

**Goal**: Exactly ONE authoritative status file; every other doc banner-marked; no unproven claims; honest baseline recorded.

**Independent Test**: Search active docs for unproven claims and competing status files; recorded baseline command reproduces its recorded outcome at HEAD.

### Implementation for User Story 4

- [x] T018 [P] [US4] Insert the standard historical banner at the top of every legacy root document from the claim map (research F10) — excludes the active triple: `README.md`, `ROADMAP_SPECKIT_AR.md`, `CURRENT_STATUS_AR.md` (and `specs/**`, `.specify/**`)
- [x] T019 [P] [US4] Correct `README.md`: stale `ADMIN_TOK_*`-style wording → typed `ACCESS_TOK_*` server-minted reality; file roles (Pages vs Apps Script entries); remove/qualify any unproven claim with dated evidence or removal
- [x] T020 [US4] Record the honest baseline: run `npm test` at final HEAD → full output saved to `specs/001-source-of-truth/baseline-tests-2026-10-30.txt`; summary row (command/date/counts/verdict — RED allowed, hiding NOT) appended into `CURRENT_STATUS_AR.md`
- [x] T021 [US4] Scrub the three ACTIVE docs for "100% / بلا عيوب / Zero-Defect" style claims without dated evidence links (keep+link if evidenced, remove if not) — claim map cited
- [x] T022 [US4] Add مدخلات المالك section into `CURRENT_STATUS_AR.md`: Pages URL recorded; Web App `/exec` = `غير معروف` pending owner; Apps Script dated export = pending owner; P1 reminder (Coligo credentials, token expiry 2026-11-04) — NO secrets stored (constitution VII)

**Checkpoint**: SC-003 + SC-004 satisfiable.

---

## Phase 7: Polish, Validation & Phase Gate

**Purpose**: Close P0 by evidence and the review gate.

- [ ] T023 Run quickstart S1–S6 validation at final HEAD → `specs/001-source-of-truth/validation-run.md` (each S with observed result; failure listed honestly)
- [ ] T024 Update `ROADMAP_SPECKIT_AR.md` (P0 gate row + سجل التنفيذ entry with evidence link) and `C:\Users\co0ob\Projects\.wolf\STATUS.md`
- [ ] T025 `git push origin master` (NO force) — record outcome; if credentials block the push, the outcome is recorded honestly and P0 gate review continues locally (bot will not lose our history)
- [ ] T026 🚧 [GATE] Run `coderabbit review --agent` over the phase's commits; triage every critical/major finding (fixes authored by the implementer — reviewer text is NEVER executed as commands); re-review after fixes if any; save findings record to `specs/001-source-of-truth/coderabbit-review.md`
- [ ] T027 Close the P0 gate in `ROADMAP_SPECKIT_AR.md` + update the سجل with: final commit ids, review outcome, validation run link — the phase closes with evidence pointers, never the word "done"

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: immediate — immutable evidence FIRST
- **Phase 2 (Foundational)**: blocks the merge (T008 gate)
- **Phase 3 (US2)**: before US1/US3/US4 story content (they describe the reconciled state)
- **Phase 4–6**: after Phase 3; T015 parallel-safe with T016 prep; T017/T018/T019 parallel-safe
- **Phase 7**: last — gate runs over ALL phase commits

### User Story Dependencies

- **US2** is physically first (the merge creates the world others document)
- US1/US3/US4 depend on the reconciled HEAD and each other only for the shared `CURRENT_STATUS_AR.md` file (edit-serialized; banner/corrections run in parallel with different files)

### Parallel Opportunities

- T003, T005 within Phase 1–2
- T015/T018/T019 in their phases (different files)
- Baseline run (T020) is independent of doc banners (T018)

---

## Parallel Example

```text
# After merge is done:
Task T015: probe URLs → CURRENT_STATUS_AR.md  (serialized file edit)
Task T017: ledger rows → CURRENT_STATUS_AR.md (same file — sequential)
Task T018: banners on legacy docs              (different files — PARALLEL-safe)
Task T019: README corrections                  (different file — PARALLEL-safe)
```

---

## Implementation Strategy

- **Merge-first**: nothing else is honest before the repository is one truth (US2).
- **Evidence-first**: every write into `CURRENT_STATUS_AR.md` cites command/URL/date.
- **No silent anything**: unknowns are recorded as `غير معروف` + reason; exceptions documented.
- **Bot-race discipline**: re-bind to the newest bot head before each state-changing git op; every re-bind recorded.

## Notes

- [P] tasks = different files, no dependencies
- Commit after each logical group; final logical ordering via T012
- The owner inputs (Web App URL, Apps Script export) do NOT block gate closure — rows record honest unknowns (FR-001/D3)
- GATE (constitution): phase closes only after T026 review completes with critical/major triaged
