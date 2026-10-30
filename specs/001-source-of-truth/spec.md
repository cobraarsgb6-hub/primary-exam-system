# Feature Specification: Source of Truth (P0)

**Feature Branch**: `001-source-of-truth`

**Created**: 2026-10-30

**Status**: Draft

**Input**: User description (from `ROADMAP_SPECKIT_AR.md` §P0): "حدّد النسخة المنشورة فعلياً من Code.gs وIndex.html (Apps Script) وقارنها بالمستودع المحلي وorigin/master، وأنشئ دمجاً آمناً لا يفقد ملفات المواد غير الملتزم بها، ودمج إصلاحات أمنية قائمة (توكن إدارة صادر من الخادم فقط، لا PINs في الكود، قاعدة منع // داخل نصوص JS). ثم وحّد التوثيق في ملف حالة واحد مسنود بأدلة، واحذف أي ادعاء اكتمال غير مثبت."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The maintainer sees exactly what is published (Priority: P1)

Ahmed opens the single status file and sees one table: every deployable file
(`Code.gs`, the Apps Script HTML templates, the built bundle, `index.html` for
GitHub Pages, the Coligo workflow) mapped to its repository commit and to its
**published-or-not** state, with dated evidence for every row. Any row whose
state cannot be proven reads "غير معروف" — documented truthfully, never
guessed.

**Why this priority**: Every later phase (P1–P9) depends on knowing what code
is really live before changing anything; this is the phase's core deliverable.

**Independent Test**: Pick any main file, follow its row's evidence, and
confirm for yourself whether the repo, the Apps Script project, and the
deployed app agree — verifiable row by row without any other story.

**Acceptance Scenarios**:

1. **Given** the reconciled repository, **When** Ahmed reads the status file,
   **Then** each deployable-surface file has one row with: file → repo
   commit → published state → evidence (source + date).
2. **Given** a file where the repo, the Apps Script copy, or the published app
   disagree, **When** Ahmed reads its row, **Then** the drift is stated
   explicitly (which side is ahead/behind), never hidden.
3. **Given** a file whose published state cannot be determined with the
   available tooling, **When** Ahmed reads its row, **Then** it says
   "غير معروف" plus the reason — an honest unknown, not an assumption.

---

### User Story 2 - The merge loses nothing (Priority: P1)

The local branch has diverged from `origin/master` (commits on both sides) and
material files exist that are not committed. When the local history and
`origin/master` are reconciled into one branch, every material file survives,
the working tree ends clean (or with an explicitly documented, justified set
of exceptions), and the running automations (hourly Coligo sync, Pages
deploy) keep working.

**Why this priority**: A broken/lost-material merge destroys irreplaceable
content; it must be impossible, not merely unlikely.

**Independent Test**: List material files before the merge, perform it, list
again after — zero missing files, and pipeline status checks pass afterwards.

**Acceptance Scenarios**:

1. **Given** the pre-merge inventory of uncommitted material files, **When**
   the merge completes, **Then** every listed file still exists (or was
   committed), and no tracked file was silently deleted by the merge.
2. **Given** the merge, **When** `git status` is read afterwards, **Then** it
   is clean or every exception is documented with a reason in the status file.
3. **Given** case-collision risk (`Index.html` vs `index.html` — known Linux
   Pages trap), **When** the merge completes, **Then** the repository contains
   one coherent casing set and it is documented which name serves which
   surface (Apps Script HTML includes vs GitHub Pages).

---

### User Story 3 - The October-28 security fixes are accounted for (Priority: P2)

For each already-created fix — server-minted typed tokens (no static
`ADMIN_TOK_*` acceptance), no PINs in code, the `//` → `\/\/` rule inside
Apps Script HTML, and the optional error crop/bar — the reconciled code ends
in exactly one of: **مثبت** (confirmed present, with evidence), **مدمج**
(merged in this phase, with commit), or **غير مطلوب** (documented reason). No
fix ends "unknown".

**Why this priority**: These four directly close documented security
violations; P2 (`003-security-privacy`) builds on them instead of redoing
them.

**Independent Test**: Read the status file's fix ledger; for each fix follow
its evidence pointer into the code at `HEAD` — presence provable per fix.

**Acceptance Scenarios**:

1. **Given** a fix whose code exists in the reconciled files, **When** the
   ledger is checked, **Then** the fix reads "مثبت" with the evidence pointer.
2. **Given** a fix missing from the reconciled files, **When** work completes,
   **Then** it reads "مدمج" with the introducing commit, or "غير مطلوب" with a
   written justification — never "unknown".

---

### User Story 4 - One truthful status, no magic claims (Priority: P2)

Documentation collapses to exactly ONE authoritative status file
(`CURRENT_STATUS`). Every other existing project document is explicitly
marked "historical, not authoritative". Unproven completion claims
("100%", "بلا عيوب", conflicting test-count numbers) are removed from active
documents or qualified with dated evidence. The deployed Web App URL is
recorded once, in the status file, and opening it does *not* 404 (or the 404
itself is documented with the reason). A baseline test run is recorded with
its exact command, date, and results — **even when tests fail**.

**Why this priority**: Document drift was the root cause of the
version-confusion problem this phase exists to kill.

**Independent Test**: Search active docs for unproven claims and for competing
status files; only one authoritative file remains, every claim in it is
linked to evidence, and the recorded baseline command reproduces the recorded
outcome.

**Acceptance Scenarios**:

1. **Given** the reconciled repository, **When** Ahmed opens the status file,
   **Then** it is the only file claiming authority; every other document
   carries its "historical" banner or pointer.
2. **Given** an active document, **When** it is searched for "100%" /
   "بلا عيوب" style claims, **Then** every such claim is either removed or
   carries a dated evidence link.
3. **Given** the recorded baseline test command, **When** it is re-run from
   `HEAD`, **Then** its result matches the recorded one (failing is an
   acceptable recorded state; hiding a failure is not).
4. **Given** the recorded Web App URL, **When** Ahmed opens it, **Then** it
   loads (or the failure is documented with cause and owner action needed).

## Edge Cases

- A repository state where the source CSV/HTML material files are untracked —
  they MUST survive any reconciliation untouched.
- `Code.gs.bak`, `legacy_index.html`, and other legacy copies: MUST be clearly
  identified as non-authoritative snapshots (they exist and are confusing),
  never mistaken for current code.
- A merge conflict inside documentation files: resolved in favor of evidence,
  not verbosity; conflicts are documented in the status file.
- The hourly Coligo sync or Pages deploy may run DURING reconciliation —
  it MUST not corrupt either state; any Actions run occurring mid-merge is
  recorded with its run link.
- No tooling available to programmatically export the currently deployed
  Apps Script code: acceptable evidence is the owner's dated manual export; if
  unavailable, the row reads "غير معروف" — the phase does not fabricate
  certainty.
- Already-scheduled fixes arriving mid-phase (e.g. another agent edits code):
  the ledger updates with the commit id rather than declaring stale results.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system-of-record MUST produce a file → commit → published
  table covering every deployable surface (Apps Script files, built bundle,
  GitHub Pages entry file, Coligo workflow), each row with dated evidence or
  an explicit "غير معروف".
- **FR-002**: The repository history MUST reach one reconciled state with
  `origin/master` such that: no material file is lost, the working tree is
  clean or its exceptions documented, and destructive operations (force push,
  history rewrite, file deletion of materials) are forbidden — history
  rewriting stays a separate explicit decision.
- **FR-003**: The October-28 fix set MUST be accounted for in a ledger with
  one of the states مثبت/مدمج/غير مطلوب per fix, each with an evidence
  pointer or justification.
- **FR-004**: Exactly ONE authoritative status file MUST exist at the end of
  the phase; all other documents MUST carry an explicit historical marker.
- **FR-005**: Active documents MUST contain no unproven completion claims;
  any surviving claim MUST carry dated evidence.
- **FR-006**: The deployed Web App URL MUST be recorded once in the status
  file, and the local branch's divergence MUST be resolved without losing
  either side's commits.
- **FR-007**: A baseline test record MUST exist containing: command, date,
  counts, and failures — recorded even (especially) when the suite fails.
- **FR-008**: This phase MUST NOT introduce new product behavior; code
  reconciliation is limited to adopting already-created fixes and
  documentation truth (no new features, no UI changes).
- **FR-009**: GitHub-side automations (hourly Coligo sync, Pages deploy)
  MUST remain operational after reconciliation (no broken workflow files,
  no broken deploy path).
- **FR-010**: The Arabic language of any status/report content MUST follow
  the project's NFKC/RTL discipline where rendered by the system.

### Key Entities *(include if feature involves data)*

- **CodeVersion**: file × location (repo / Apps Script / published app) ×
  commit-or-hash × evidence-source × evidence-date.
- **MaterialFile**: untracked or uncommitted content file with a pre-merge
  inventory and a post-merge survival check.
- **OctFixLedger**: fix id → state (مثبت/مدمج/غير مطلوب) → evidence pointer.
- **StatusRecord**: the single authoritative CURRENT_STATUS document, its
  update procedure, and its pointer to the recorded Web App URL and test
  baseline.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of deployable-surface files have a row with evidence or an
  explicit "غير معروف" — zero assumed states, zero silent gaps.
- **SC-002**: Zero material files lost across the merge (pre/post inventory
  comparison documented).
- **SC-003**: The baseline test record reproduces from `HEAD` (same command,
  same outcome as recorded), including failures recorded honestly.
- **SC-004**: Exactly one authoritative status file; one search over active
  documents returns zero unjustified "100%/بلا عيوب" claims.
- **SC-005**: The four October-28 fixes each close in exactly one ledger
  state (مثبت/مدمج/غير مطلوب) — zero "unknown" endpoints.
- **SC-006**: The long-running automations (hourly Coligo sync, Pages deploy)
  show zero failed runs caused by the reconciliation, with run links recorded.

## Assumptions

- "Published" means the two live surfaces: the Apps Script web app deployment
  and the GitHub Pages site; evidence comes from reading state (deployed URLs,
  Actions logs, editor exports) not from memory.
- The owner (Ahmed) can supply, on demand, a dated manual export of the
  Apps Script project when tooling cannot read it programmatically; absence of
  such evidence records an honest "غير معروف" rather than a guess.
- Git remotes (`origin`) remain unchanged; no history rewriting occurs in this
  phase.
- This phase produces no new features; its only code motion is adopting
  pre-existing October-28 fixes and documentation truth-keeping.
