# Contract: Truth Ledger Format (`CURRENT_STATUS_AR.md`)

**Feature**: `001-source-of-truth` | **Reader**: Any agent or human maintaining
the project. This is a document-shape contract, not an API.

## Rules of authority

- Exactly ONE file claims authority for project state: `CURRENT_STATUS_AR.md`
  at repo root. (Active exceptions: `ROADMAP_SPECKIT_AR.md` = phase tracker,
  `README.md` = living deploy guide — both explicitly excepted in their
  headers; everything else carries a historical banner.)
- Every factual claim = pointer to evidence (command output, HTTP probe,
  export receipt, run link) + date. "غير معروف" is a valid row state and MUST
  state why the unknown persists.

## Row schemas

### جدول الحقيقة (CodeVersion)

```yaml
- file: "Code.gs"                     # exact path + casing
  repoState: "tracked@<commit>"        # or modified-uncommitted / untracked
  publishedState: published|unpublished|غير معروف
  evidence: "<pointer>"                # mandatory
  date: "YYYY-MM-DD"
  surface: "apps-script|pages|bundle|workflow|tooling"
```

### دفتر الإصلاحات (OctFixLedger)

```yaml
- fix: "server-minted-typed-tokens"
  state: مثبّت|مدمج|غير مطلوب           # no other terminals
  evidence: "<pointer>"
  date: "YYYY-MM-DD"
  notes: "<one line>"
```

Prefilled states (from research D5): server-minted typed tokens = مثبّت;
no-PINs-in-live-code = مثبّت; `\/\/` rule = مثبّت; optional error bar = غير مطلوب.

### سجل الدمج (merge log)

```yaml
- divergence: "ahead 1 -> 0, behind 1 -> 0 (rebase onto <remote head>)"
- hashEqualReplacement:                # plant: count + example row
    - path: "<untracked path>"
      localHash: "<sha256>"
      remoteHash: "<sha256>"           # equality recorded both sides
- exceptions:                          # anything not clean, with reason
    - path: "<path>"
      reason: "<reason>"
```

### خط الأساس (baseline tests)

```text
command: npm test
date: 2026-10-30
result: FAIL (legacy contract) | suite counts summary
evidence: output location / excerpt
NOTE: fixing suites is out of P0 scope; recorded RED is the honest floor.
```

### منصة الوصول (URLs)

```text
pages_url: https://cobraarsgb6-hub.github.io/primary-exam-system/?v=dynamic_v2   # probe 200 on 2026-10-30
webapp_url: <owner-supplied /exec URL> | "غير معروف — owner input pending"       # NEVER stored as secret(下发 it is public by design)
```

## Anti-patterns (contract violations)

- Writing a status claim without evidence/date (Principle VIII violation).
- Prefilling "published" for Apps Script side without owner export (D3).
- Deleting a document instead of banner-marking it (append-only discipline).
- Storing secrets in this file (VII) — the `/exec` URL is public by design;
  secrets stay in GitHub Secrets / Script Properties.
