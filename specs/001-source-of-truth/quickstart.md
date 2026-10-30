# Quickstart: Validating Source of Truth (P0)

**Feature**: `001-source-of-truth` | **Date**: 2026-10-30
Evidence-level validation only (docs + git). Detail: see
[data-model.md](data-model.md) and [contracts/truth-ledger-format.md](contracts/truth-ledger-format.md).

## Prerequisites

- Repo at `HEAD` when tasks begin: plan branch `001-source-of-truth` state
  with the pre-merge divergence (`ahead 1 / behind 1` — evidence dated
  2026-10-30).
- Owner availability window for two inputs: the deployed Web App `/exec` URL
  and (optionally now, else later) a dated Apps Script project export.

## Validation scenarios

### S1 — Truth table completeness (spec SC-001)

Open `CURRENT_STATUS_AR.md` → جدول الحقيقة. **Expected**: every deployable
surface file (Apps Script files, `Index.bundle.html`, `index.html`, `bundle.py`,
workflows, sync script) has a row with repoState + publishedState + evidence +
date; Apps Script rows either evidence-backed or explicit "غير معروف" with
reason. Zero rows without evidence link.

### S2 — Zero-loss merge (spec SC-002, US2)

Before merge: the pre-merge inventory snapshot is captured. After merge:
**Expected**: every inventory path still exists (kept / committed /
replaced-by-tracked-identical WITH both hashes recorded) — zero vanished
rows; `git status` clean or every exception documented; final shape
`ahead 0 / behind 0` (or documented equivalent).

### S3 — Oct-28 ledger closed (spec SC-005)

دفتر الإصلاحات: **Expected** exactly one of مثبّت/مدمج/غير مطلوب per fix ×4,
each with evidence pointer: typed tokens (Code.gs functions), PIN-free live
code + quarantined legacy copies, `\/\/` rule (bundle.py), error bar (غير مطلوب,
reason stated). No "unknown" state anywhere.

### S4 — One truth, no magic (spec SC-004)

Search active docs: **Expected** `CURRENT_STATUS_AR.md` is the only
authoritative claim file; all 17 legacy docs show the historical banner; no
unjustified "100%/بلا عيوب" strings remain in active docs (claim map cited);
README's token text reflects the typed-token reality (no stale ADMIN_TOK_
assertion).

### S5 — Honest baseline (spec SC-003)

Run the recorded baseline command exactly as recorded:
```bash
npm test
```
**Expected**: result matches the record (today's known state: RED against the
pre-fix contract — RED is an acceptable recorded outcome; a "green" that
contradicts the record is NOT). Command + date are in the status file.

### S6 — Automations intact (spec SC-006)

**Expected**: `coligo-cloud-sync.yml` and `deploy-pages.yml` parse and
reference existing files; the Pages URL probe returns 200
(`https://cobraarsgb6-hub.github.io/primary-exam-system/?v=dynamic_v2` —
verified live 2026-10-30); next scheduled hourly run documented after merge.

## Acceptance tracing

S1–S6 = Phase P0 gate. Closure requires: CodeRabbit review of the phase's
changes + this quickstart's expected outcomes observed + owner inputs
recorded (Web App URL; later Apps Script export) — per constitution
"Review gate (CodeRabbit)" and "Evidence-Based Status".
