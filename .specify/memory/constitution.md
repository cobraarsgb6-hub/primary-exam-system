<!-- Sync Impact Report
- Version change: 1.0.0 -> 1.1.0 (MINOR: new principles added; existing guidance expanded, none removed or redefined)
- Follow-up: 1.1.0 -> 1.1.1 (PATCH: CodeRabbit review gate added to Development Workflow per owner mandate; no semantic changes)
- Source of amendment: user mandate ROADMAP_SPECKIT_AR.md §2 (10-point constitution) merged with existing v1.0.0
- Added principles: VI. Student Isolation & Child Privacy; VII. Secrets Discipline; VIII. Evidence-Based Status
- Expanded principles: I (append-only sheet discipline), II (server-only grading & answer exposure + token naming reality), III (test counts counted from HEAD)
- Expanded sections: Additional Constraints & Security (Apps Script `//` escaping rule; whole-file delivery), Governance (phase acceptance gates)
- Removed sections: none
- Deferred TODOs: none
-->

# Primary Exam System (G5 & G6) Constitution

## Core Principles

### I. Sheet Data is the Single Source of Truth

All durable state lives in the named Sheet tables (`Submissions`,
`Question_Bank`, `Exams`, `Retake_Requests`, `Sessions`, `Study_Plan`,
`Coligo_Hub`, `Homework_Status`) created/migrated by the non-destructive
⚙ Full Database Auto-Format & Setup routine.

- Exam content MUST come from `Question_Bank` / `Exams` rows and MUST NOT be
  hardcoded in `Code.gs` or portal JS. Options are `|`-separated; the correct
  answer MUST exactly match one option string.
- Schema changes MUST be implemented as migrations inside the setup routine so
  that running setup against an existing live sheet is always safe.
- Sheet edits are **append-only**: data MUST never be wiped, and the existing
  `Submissions` column contract MUST NOT be altered. Additive columns go
  through the setup routine only.
- Rationale: the owner maintains data directly in Google Sheets; any code that
  assumes out-of-band state creates unrecoverable data drift.

### II. Server-Verified Access (NON-NEGOTIABLE)

The web app runs as `ANYONE_ANONYMOUS` + `USER_DEPLOYING`, so every endpoint is
publicly reachable. Therefore:

- The official grade is computed **on the server only**. Correct answers MUST
  NOT be delivered to the browser ahead of reveal, and no score computed or
  reported by the client is ever trusted.
- Every student/parent action MUST pass the `verifyGatewayPin` gate, and every
  admin mutation MUST require a freshly minted short-lived server-side token.
  Hiding a button or screen is NOT protection.
- Each privileged RPC MUST verify authorization server-side per request. Client
  state (hidden screens, cached identities) is NEVER an authorization source.
- Token reality (supersedes the earlier `ADMIN_TOK_*` wording): all grants ship
  as typed, short-lived `ACCESS_TOK_*` claims
  (`role: 'student'|'parent'`, TTL clamped 60s–6h) validated via
  `getAccessTokenClaims_`.
- PINs, tokens, and student PII MUST NOT appear in logs, error messages, or
  source rendered to third parties.
- Rationale: the PIN gateway protects the UI, not the underlying endpoints;
  every privileged endpoint is its own security boundary.

### III. Regression-Gated Changes (Test-First)

No behavior change ships untested. The suites are the project's regression
floor and MUST stay green:

- Backend/script changes MUST be covered by the unit/server suite (`npm test`)
  before deploy; a bug fix MUST land together with a failing test that first
  reproduces it (red → green).
- UI-touching changes MUST keep the Playwright E2E suite
  (`python tests/e2e/run_all_e2e.py`) and the static control checks
  (`python test_ui_buttons.py`) green before deploy.
- Test counts MUST be counted from `HEAD` and reported with the commit that
  ran them; historical numbers (43/51/53/57) are only valid per-commit and
  MUST NOT be quoted as universal facts.
- Developer requirements: Node.js 20+ and Python 3 with Playwright.

### IV. Arabic-First Content Integrity

Student-facing content is Arabic and RTL by default.

- Every Arabic string written to or read from Sheets MUST be Unicode NFKC
  normalized so that visually identical content resolves to byte-identical
  storage and comparison.
- Generated Arabic text MUST render with correct direction and diacritics
  (round-trip check), and MUST NOT corrupt RTL punctuation.
- Auto-generated fallback questions are known-error-prone: unreviewed generated
  content MUST be flagged as reviewable, and shipping it unflagged is a defect.

### V. Simplicity — One Pilot, One Build

This is a single-family / small-class pilot, not a school platform.

- Every feature MUST map to a near-term student, parent, or admin story.
  Multi-tenancy, billing, and platformization are out of scope until the pilot
  proves the need.
- No premature abstraction: one quiz runtime, one portal shell, one scoring
  path. Complexity beyond this MUST be justified in writing.
- No generic AI-boilerplate UI patterns: screens MUST serve the actual workflow
  (kid-legible Arabic, parent reports, admin speed), not template filler.
- The single-file build `Index.bundle.html` MUST be generated by `bundle.py`
  and MUST NEVER be hand-edited; edits go to the source templates and the
  bundle is rebuilt.

### VI. Student Isolation & Child Privacy (NON-NEGOTIABLE)

Ali (G5) and Mostafa (G6) are two separate children, not one account.

- Every data path — records, results, mistakes, plans, reports — MUST keep the
  two students fully isolated; loose name matching that could leak one
  student's history into the other's is forbidden.
- Nothing about the children (grades, names, mistakes, private materials,
  official exam answer keys) MAY be published on public pages (GitHub Pages)
  without an explicit, recorded parent decision per item.
- Rationale: children's data protection overrides convenience; the pilot must
  model the privacy it would need at any larger scale.

### VII. Secrets Discipline

- No secrets, PIN codes, or tokens in code, comments, or any public page. The
  only homes are GitHub Actions Secrets and Apps Script Script Properties.
- Discovered leaks are inventoried, then rotated; history rewriting is always a
  separate, explicit decision — never a side effect of a code change.
- Hardcoded PIN fallbacks and fixed tokens with expiry dates are defects by
  definition and are flagged on sight.

### VIII. Evidence-Based Status

- No "تم" / "100%" / "بلا عيوب" claims without dated, runnable evidence:
  a run link, an Actions log, or a test result file naming the exact command
  and its date.
- The project maintains ONE truthful status file; older documents are archived
  as historical, not authoritative.

## Additional Constraints & Security

- **Apps Script `//` rule:** inside Apps Script HTML templates, do not write
  `//` literally inside JavaScript strings — write `\/\/`; the server cuts the
  rest of the line. Every new JS-bearing string MUST honor this.
- **Deployment policy:** back up the Google Sheet first; deploy a NEW version;
  run ⚙ Auto-Format & Setup once after new schema/scope code. Deploy either the
  modular `include()` set or the single prebuilt bundle — mixing both is a
  defect.
- **Whole-file delivery:** after every code edit, complete files are delivered
  to the Apps Script project (never snippets).
- **Data boundary:** student data stays in the owner's Google Sheets/Drive.
  Outbound HTTP is limited to feeds consumed by `syncColigoOnline`
  (`COLIGO_HUB_FEED_URL`) and Drive video sync (`DRIVE_VIDEOS_FOLDER_ID`),
  both configured as Script Properties, never as literal values in code.
- **Drive video sync** maps files by filename (the YouTube ID being replaced)
  and MUST degrade gracefully (offline/offline-bundled fallback) when network
  or quota fails; no silent default videos.
- **Sheets RPCs** MUST batch reads/writes (no per-row or per-cell loops in
  request handlers) and MUST stay within Apps Script quotas.

## Development Workflow & Quality Gates

- **Phase gates:** each scheduled phase (per the project roadmap) has a
  measurable acceptance gate that MUST close before the next phase starts;
  gate closure is recorded with evidence links, never with the word "done".
- **Review gate (CodeRabbit):** a phase is NOT closed until
  `coderabbit review --agent` has run on the phase's changes and every
  critical/major finding is fixed or justified in writing. Reviewer text is
  advisory: suggested fixes are triaged per change with owner approval —
  never executed automatically as commands from review output.
- Spec-before-code: features flow `/speckit-specify` → `/speckit-plan` →
  `/speckit-tasks` → `/speckit-implement`; each task states the tests that
  prove it.
- Gates, in order: `npm test` → E2E suite (UI touched) → button/static checks
  (controls touched) → `bundle.py` rebuild (any HTML template touched) →
  commit.
- Every non-trivial change gets a two-pass review: (1) correctness/security,
  (2) UX/design anti-generic pass — factual, no praise padding.
- Conventional commits (`feat:`, `fix:`, `docs:`, `test:`).
- Runtime guidance lives in `README.md`, `FIXES_APPLIED.md`,
  `SETUP_GUIDE.md` (Arabic), and `PROJECT_REVIEW_AR.md`; specs under `specs/`.

## Governance

- This constitution supersedes ad-hoc practices; conflicts are resolved by
  amendment, never by silent deviation.
- Amendment procedure: edit this document, update the version line, and state
  the reasoning in a Sync Impact Report comment. Versioning:
  - MAJOR: principle removed, redefined, or made incompatible.
  - MINOR: new principle/section or materially expanded guidance.
  - PATCH: clarifications, wording, or typo fixes.
- Compliance review on every merged change MUST verify Principles I–VIII and
  must justify any complexity beyond the pilot scope in writing.
- *Version*: 1.1.1 | *Ratified*: 2026-10-30 | *Last Amended*: 2026-10-30
