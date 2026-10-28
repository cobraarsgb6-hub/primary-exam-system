# BRIEFING — 2026-10-25T16:46:00Z

## Mission
Implement Milestone 2 on Code.gs and Exams.csv: Arabic Unicode NFKC normalization, answer normalization engine with letter folding, bilingual header resolution, custom question non-destructive auto-healing, and 28-exam catalog completion.

## 🔒 My Identity
- Archetype: worker_m2
- Roles: implementer, qa, specialist
- Working directory: C:\Users\co0ob\Projects\primary-exam-system\.agents\teamwork\worker_m2
- Original parent: b60602f6-9563-4ac1-9709-5890290e1ced
- Milestone: Milestone 2 (Backend Normalization & Catalog Sync)

## 🔒 Key Constraints
- Exclusively own `Code.gs` and `Exams.csv`.
- DO NOT modify `Index.html` or `tests/e2e/`.
- Non-destructive schema migrations and preserve custom questions.
- Strict NFKC canonical normalization for Code.gs (`code === code.normalize('NFKC')`).
- Genuine logic only; no hardcoding of test outputs or results.

## Current Parent
- Conversation ID: b60602f6-9563-4ac1-9709-5890290e1ced
- Updated: 2026-10-25T16:46:00Z

## Task Summary
- **What to build**: Milestone 2 Backend Normalization & Catalog Sync
  1. Arabic Unicode NFKC canonical normalization across Code.gs.
  2. Answer normalization engine update in `normalizeAnswer_` (NFKC + letter folding [أإآ] -> ا, ة -> ه, ى -> ي).
  3. Bilingual header resolution in `headerIndex_` for Arabic/English headers.
  4. Non-destructive custom question preservation in `ensureDatabaseUpToDate_` and `migrateAndSyncDatabase()`.
  5. Add 3 foundational exams (`EX_Y5_ENG_ADV01`, `EX_Y6_ARB_PRIO01`, `EX_Y6_ENG_FANTASY01`) to `Exams.csv`.
- **Success criteria**:
  - `Code.gs` is 100% NFKC identical (`code === code.normalize('NFKC')` is true).
  - AST syntax check passes.
  - `npm test` passes 12/12.
  - `node --test tests/cumulative.test.js` passes.
  - `node .agents/teamwork/explorer_survey_testing/test_all_28_exams.js` passes 28/28.
  - `python tests/e2e/run_all_e2e.py` passes 51/51.
- **Interface contracts**: PROJECT.md § Interface Contracts
- **Code layout**: PROJECT.md § Code Layout

## Key Decisions Made
- Prioritize minimal, exact edits to `Code.gs` and `Exams.csv`.

## Artifact Index
- `DISPATCH.md` — Assignment instructions
- `progress.md` — Liveness heartbeat and step log
- `handoff.md` — 5-component handoff report

## Change Tracker
- **Files modified**: None yet
- **Build status**: Untested
- **Pending issues**: None

## Quality Status
- **Build/test result**: Untested
- **Lint status**: 0 violations
- **Tests added/modified**: None yet

## Loaded Skills
- None specified
