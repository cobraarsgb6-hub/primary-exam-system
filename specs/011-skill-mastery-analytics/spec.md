# Feature Specification: Skill Mastery Analytics

**Feature Branch**: `001-skill-mastery-analytics`

**Created**: 2026-10-30

**Status**: Draft

**Input**: User description: "تحليل إتقان المهارات — لوحة إتقان المهارات لكل طالب: تستخرج درجة إتقان كل مهارة (مادة / درس) لكل طالب من نتائج الامتحانات المسجلة، مع اتجاه التقدم وأسوأ المناطق وتوصيات دراسة قابلة للتنفيذ."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student sees his own mastery map (Priority: P1)

A student signs in to the student portal (after the PIN gateway) and opens his
mastery report. He sees a list of his subjects; under each subject, the
lessons/units he has been examined on, each with a whole-number mastery
percentage (0–100), how many questions he attempted, and a level badge in
Arabic: متقن (80%+), قابل للتحسن (60–79%), يحتاج مراجعة (below 60%),
لم يبدأ بعد (never attempted). The report is refreshed automatically after
every graded submission — he never runs a manual refresh.

**Why this priority**: The student is the end learner; self-knowledge of weak
areas is the core value of the feature and is deliverable alone as the MVP.

**Independent Test**: Submit known answers to a set of exams, open the mastery
report, and verify each unit's percentage, badge, and trend against the
recorded answers — fully verified without any other story implemented.

**Acceptance Scenarios**:

1. **Given** a student with at least one recorded submission, **When** he opens
   the mastery report, **Then** every unit he attempted appears once under its
   subject with the correct percentage, attempt count, and badge.
2. **Given** a subject with attempted and never-attempted units, **When** the
   report opens, **Then** unattempted units show "لم يبدأ بعد" and are not
   counted in any percentage.
3. **Given** a student just graded a submission, **When** he reopens the report
   in a later session, **Then** the affected units already reflect the new
   attempt without any manual action.
4. **Given** a unit attempted more than once (retakes), **When** the report
   opens, **Then** the percentage reflects all recorded attempts for that unit
   and the trend arrow compares the latest attempt with the earlier average.

---

### User Story 2 - Parent spots the weak spots in seconds (Priority: P2)

A parent opens the Parent Portal (her own child after the PIN gateway) and
immediately sees the same mastery map for her child — subjects, units,
percentages, badges — plus a top-3 list of the weakest units ("أسوأ ثلاثة
دروس"). From any weak unit, she can see what is recommended, and can generate
a targeted practice for that lesson slice using the existing exam-generation
capability, without retyping anything.

**Why this priority**: Parents are the paying, motivating stakeholders of the
pilot; weak-spot visibility is the report's reason to exist for them.

**Independent Test**: With a mixed record of strong and weak units, a parent
locates the weakest unit and launches a targeted practice from it in under a
minute — no other story needed.

**Acceptance Scenarios**:

1. **Given** a child with mixed results, **When** the parent opens the report,
   **Then** the weakest three units appear with their subject names and
   percentages, sorted weakest first.
2. **Given** a weak unit, **When** the parent chooses the targeted-practice
   action, **Then** an exam limited to that unit's question pool is offered for
   creation, and refusal with a clear Arabic message when that pool is empty.
3. **Given** two children of the same parent (if configured), **When** she
   switches between them, **Then** each view shows only that child's data —
   never the other child's.

---

### User Story 3 - Mastery drives the Study Plan (Priority: P3)

When the student or parent opens the existing Study Plan, the plan reflects the
mastery data: units marked "يحتاج مراجعة" appear first with recommended
sessions, and units marked "متقن" drop to the end or are skipped. The parent
can accept the proposed adjustment with one action.

**Why this priority**: Closes the loop from measurement to action; valuable,
but the report alone (P1) and parent weak-spot workflow (P2) already deliver
standalone value.

**Independent Test**: With known mastery levels, open the Study Plan and verify
the ordering of recommended sessions matches the mastery levels — independent
of the parent targeted-practice flow.

**Acceptance Scenarios**:

1. **Given** units below the 60% line, **When** the Study Plan opens, **Then**
   those units appear first with study-session suggestions before mastered
   units.
2. **Given** all units of a subject are at 80%+, **When** the student opens the
   plan, **Then** the system proposes moving to the next unattempted unit (no
   endless repetition of defeated material).

---

### Edge Cases

- A submission recorded while the report page is open — the report of another
  open session MUST NOT show the other student's pending/partial data.
- A unit name differing only in invisible Unicode differences across exam rows
  MUST count as one unit, not two.
- A question whose unit/lesson field is empty or blank-string MUST appear under
  "غير مصنّف" for its subject — never silently dropped, so data gaps stay
  visible.
- A student with zero submissions MUST see an actionable empty state (guidance
  to take the next scheduled exam), not a blank screen.
- Retake requests that are still pending MUST NOT affect mastery until the
  retake is graded.
- The same question appearing in multiple exams MUST count once per each
  recorded attempt (attempts are samples, not unique questions).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST compute, per student, per subject, per
  unit/lesson: total points attempted, correct points earned, mastery
  percentage (earned ÷ attempted × 100, displayed rounded to whole numbers,
  compared internally with full precision), based on all recorded graded
  attempts.
- **FR-002**: The system MUST expose the mastery map to the student after the
  PIN gateway, covering every subject he has been examined on.
- **FR-003**: The system MUST expose the same mastery map to the parent,
  restricted server-side to her own child(ren); cross-child leakage MUST be
  impossible.
- **FR-004**: The system MUST update mastery immediately when a submission is
  graded, so the next report view reflects it without a manual refresh action.
- **FR-005**: The system MUST derive the skill (unit/lesson) from the question
  bank's existing subject and unit/lesson fields; the system MUST NOT require
  adding a new human-entered tag per question for v1.
- **FR-006**: The system MUST group question rows into units after Unicode
  NFKC normalization of the unit/lesson text; rows that differ only after NFKC
  MUST belong to one unit.
- **FR-007**: The system MUST show per-unit: percentage, attempt count,
  question count covered, badge, and trend (rising / flat / falling) when
  multiple attempts exist.
- **FR-008**: The system MUST rank the three weakest units (lowest percentage
  with at least one attempt) per student for the parent view.
- **FR-009**: The system MUST offer, from a weak unit, targeted practice
  generation limited to that unit's question pool; it MUST refuse with a clear
  Arabic message when the pool has no questions.
- **FR-010**: The system MUST surface "غير مصنّف" questions (missing unit) in
  the report rather than omitting them.
- **FR-011**: The system MUST NOT include pending (ungraded) retake requests in
  mastery figures.
- **FR-012**: The system MUST present all student-facing labels in Arabic RTL
  (badges, headings, empty states) per the project's Arabic-first rule.

### Key Entities *(include if feature involves data)*

- **Student**: the learner whose mastery is measured; identified per the
  existing portal account; owner of the report.
- **Question**: bank record with subject + unit/lesson + points + correct
  answer + difficulty; the grouping unit of mastery.
- **Submission attempt**: one graded exam sitting by a student, resolving each
  question to correct/incorrect; the measurement unit.
- **Mastery record**: per student × subject × unit: attempted points, earned
  points, attempt count, latest attempt result, trend; recomputed from
  attempts, never hand-edited.
- **Study recommendation**: derived ordering of review targets feeding the
  existing Study Plan and the targeted-practice action.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A student opens the mastery report and sees his full subject/unit
  map in under 5 seconds on the family's home connection.
- **SC-002**: 100% of units with recorded attempts appear under exactly the
  correct subject — zero miscategorized units in an audit of the pilot data.
- **SC-003**: A parent identifies the child's weakest unit in under 30 seconds
  (direct find-ability test with the pilot family) and can launch targeted
  practice for it in under 1 minute.
- **SC-004**: After a graded submission, the next report view reflects it in
  100% of cases (no stale values observed across 20 consecutive submissions).
- **SC-005**: In the pilot's first month, at least half of the practice
  sessions started target a "يحتاج مراجعة" unit (evidence the report drives
  action, not just decoration).

## Assumptions

- Pilot scope: the report covers the student's own data and the parent's own
  child(ren); a class-wide admin analytics view is out of scope for v1.
- Mastery definition (reasonable default, documented): simple mastery over all
  recorded graded attempts per unit at free weights — difficulty-weighted or
  time-decayed scoring is out of scope for v1.
- Level bands (default): متقن ≥ 80, قابل للتحسن 60–79, يحتاج مراجعة < 60,
  based on common primary-education mastery practice.
- The skill taxonomy reuses the existing unit/lesson metadata in the question
  bank (every sample row has it populated); introducing a richer skills
  taxonomy is deferred until the pilot shows the need.
- Exam generation for targeted practice reuses the existing exam-generation
  capability and its refusal rules; no new generation engine in this feature.
- Partial/interrupted submissions that were never fully persisted contribute
  nothing; only graded attempts count.
