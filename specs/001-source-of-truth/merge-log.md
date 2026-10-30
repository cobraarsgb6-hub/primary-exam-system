# Merge Log — P0 Reconciliation (T014)

**Date**: 2026-10-30 | **Executor**: p0_merge_tool.py + disciplined git rebase
**Result: `behind 0 / ahead N` vs `origin/master` · vanished=0 · lost_tracked=0 · modified=0 · workflows PARSE-OK**

## 1. Divergence shape & bot-race bindings

| Clock (relative) | origin/master | action |
|---|---|---|
| Phase start | `2573eae`, `7271ba6` known → `9d4ed4a` fetched | divergence: ahead 1 / behind 3, base `fd2e670` |
| After staging T006 | `6910a9e` (new hourly bot) | analyzed ONTO `6910a9e` (re-bind #1) |
| Pre-rebase T008 | `6910a9e` | overlap=0 vs 101 staged |
| Rebase lands | `6910a9e` | HEAD = `c01cc62` + `42d8d59` (rebound local commits) |
| Post-audit | (bot may re-add hourly) | recorded; **no new head at audit time** |

## 2. Move-aside ledger (T006)

- **101 files staged** to `C:\Users\co0ob\Projects\p0_merge_stage\<sha256-8>\<relpath>`:
  - 99 exact-overlap duplicates (byte-identical vs `9d4ed4a`/`6910a9e` blobs — SHA-256 recorded in `inventory/overlap-hashes.csv`)
  - 2 **case-collision** files: local `…/Social Studies 106/**Weekly Plan**/DOC003_6.docx` + `the_4_week_6.docx` vs upstream `…**Weekly plan**/` (same disk directory on NTFS; upstream content byte-identical → replacement without loss)
- Local original copies were removed ONLY after verified twin copy (receipt: `inventory/stage-receipt.md`).

## 3. Windows-realization notes (recorded, not "fixed")

- Upstream added 5 files inside directories whose names END WITH A DOT (`…/Electricity Ppt./`, `Force Ppt./`, `Heart , Lung circulation Ppt./`, `Mixture Ppt./`, `Ppt./`).
  - Checkout required `core.protectNTFS=false`; NTFS realized them via extended paths; they are tracked and clean at HEAD.
  - **Known consequence**: these dirs are invisible/hard to touch in Windows Explorer (dot-terminated names); P3 content-phase must normalize names on ingestion to keep Windows parity.
- Origin's tree also contains a case pair `Weekly Plan vs Weekly plan` (+ `Weekly plan5/…`) — documented for P3 (naming discipline), no content loss in P0.

## 4. Conflict resolutions (T009)

| File | Basis of decision | Decision |
|---|---|---|
| `resources/coligo/coligo_catalog.json` | Deep-diff (flat-mapped keys): local changed 4 keys vs base, remote changed the same 4; ONLY differing value was `synced_at` (local 2026-10-29 19:50:05 < remote 2026-10-30 07:52:01); zero local-only entries; zero student-level diffs | **Take bot (upstream) side** — local carried nothing remote lacks (byte-truths preserved inside the newer artifact) |
| `resources/coligo/coligo_manifest.json` | deep-walk: 2 key diffs = `new_downloads` 230→123 (per-run counter) + `synced_at`; everything else equal | **Take bot (upstream) side** |

Mechanics note: during `git rebase`, upstream = `--ours`; resolution executed with `git checkout --ours` for both files, then `git rebase --continue` with `GIT_EDITOR=:` (non-interactive).

## 5. Post-merge state (T010–T012)

- Replay commits: `6ef8be3` → `c01cc62`; WIP `4b6a2c8` → rebased as `42d8d59` (7 files, +113/−130 — the earlier catalog/manifest bytes thrived on the upstream side).
- Logical commits: `fd3283e` (2 publication-safe PNG assets), `c43d039` (23 helper .py scripts + skills-lock.json), `65e1f07` (speckit harness: `.specify/`, `.agents/skills/`, `.opencode/commands/`, `ROADMAP_SPECKIT_AR.md`, `specs/001 + specs/011`).
- Survival audit at head `42d8d59…`: **vanished=0 / lost_tracked=0 / modified=0 / untracked=44** (`inventory/survival-audit.md`).

## 6. Documented exceptions (remaining 44 untracked)

- `my-project/` (39 files, origin unknown) — inventory-only decision D7; owner decides later; NOT deleted, NOT committed.
- Phase receipts/reports created after the harness commit (state.json, stage-receipt.md, survival-*.{md,json}, overlap-*.{md,csv} regenerations, merge-log.md, validation-run.md, baseline-tests-2026-10-30.txt, coderabbit-review.md) — committed at phase close (T025/T027).

## 7. Automations (T013)

- `.github/workflows/coligo-cloud-sync.yml` — PARSE-OK (1 job / 5 steps), hourly cron `0 * * * *`.
- `.github/workflows/deploy-pages.yml` — PARSE-OK (1 job / 5 steps); requires `resources/coligo/coligo_catalog.json` — present at HEAD (tracked).
