# Contract: Mastery Report & Unit Practice RPCs

**Feature**: `001-skill-mastery-analytics`
**Transport**: existing `google.script.run` template calls to `Code.gs`
function endpoints (same style as `getTodayMission`, `createWeeklyExam`).
All payloads JSON; all errors follow the existing result shape
`{success:false, code:'<CODE>', message:'<Arabic>'}`.
Authorization reuses `storeAccessToken_` claims (`role:'student'` with bound
`studentKey`, or `role:'parent'`) — see research D8/D9.

---

## POST-style endpoint 1: `getMasteryReport(payload)`

**Request**

```json
{
  "token": "<short-lived ACCESS_TOK stored by the gateway>",
  "studentKey": "ali"                // optional; ignored/rejected for parent role
}
```

**Authorization**

- `role:'student'` + `studentKey` in payload: the claim's own key only —
  mismatches return `STUDENT_MISMATCH`.
- `role:'parent'`: returns every student (pilot: `ali`, `mostafa`); may pass
  `studentKey` to narrow to one child (still claims-checked).
- Missing/expired token → `UNAUTHORIZED` (same pattern as admin-guarded
  functions today).

**Response (success)**

```json
{
  "success": true,
  "generatedAt": "2026-10-30T18:20:00Z",
  "students": [
    {
      "studentKey": "ali",
      "displayName": "Ali Ahmed",
      "subjects": [
        {
          "subject": "English Grammar",
          "units": [
            {
              "unitKey": "unit 2 - lesson 3: adverbials",
              "unitLabel": "Unit 2 - Lesson 3: Adverbials",
              "attemptedPoints": 15,
              "earnedPoints": 12,
              "pct": 80,
              "submissionCount": 2,
              "questionRows": 10,
              "badge": "متقن",
              "trend": "rising"
            }
          ],
          "uncategorized": {
            "present": true,
            "unitLabel": "غير مصنّف",
            "attemptedPoints": 5,
            "earnedPoints": 2,
            "pct": 40,
            "submissionCount": 1,
            "questionRows": 2
          }
        }
      ],
      "weakest": [
        { "subject": "English Grammar", "unitKey": "…", "unitLabel": "…", "pct": 40 }
      ]
    }
  ],
  "errors": []
}
```

**Contract invariants**

- `pct` integer display value (round-half-up); internal precision full.
- `unitKey == normalizeAnswer_(unitLabel)`; all rows equal after NFKC share one
  unit (FR-006).
- `weakest` length ≤ 3, ascending pct, ≥ 1 submission each, «غير مصنّف»
  excluded from ranking but visible in `units`/`uncategorized`.
- Expired-session rows never appear in any metric.
- Empty state: student with zero graded attempts →
  `{success:true, students:[{studentKey, displayName, subjects:[], weakest:[], emptyState:{guidance:"بل عربي واضح", nextExamHint:"…"}}]}` — the UI shows the actionable empty state.

**Error codes**: `UNAUTHORIZED`, `STUDENT_MISMATCH`,
`SUBMISSIONS_SHEET_MISSING` (never happened — auto-setup guards), generic
`SERVER_ERROR`.

---

## POST-style endpoint 2: `createUnitPracticeExam(payload)`

**Request**

```json
{
  "token": "<parent-role token>",
  "grade": "Year 5 (G5)",
  "subject": "English Grammar",
  "unitKey": "unit 2 - lesson 3: adverbials",
  "studentKey": "ali"                 // optional ownership hint for title
}
```

**Authorization**: `role:'parent'` only (admin-gate pattern) — else
`UNAUTHORIZED`.

**Response (success)** — mirrors existing factory outputs:

```json
{
  "success": true,
  "examCode": "UPR_Y5_ALI_ADVB_U1",
  "message": "تم إنشاء تدريب وحدة: <unitLabel>",
  "questionsCount": 8
}
```

- Writes one `Exams` row via existing `upsertExamRow_` with
  `Exam Type='Unit Practice'`, `Target Period='U:<unitKey>'`, status ACTIVE.
- The student then takes it via the standard session flow.

**Failure codes**

| Code | Condition |
|---|---|
| `UNAUTHORIZED` | token not parent-valid |
| `EMPTY_UNIT_POOL` | no bank questions match the unit slice — Arabic refusal message instructs adding questions first (same philosophy as weekly/monthly factories) |
| `SERVER_ERROR` | unexpected sheet errors |

---

## Endpoints NOT changed but referenced by tasks

- `getTodayMission` / Study Plan reading: v1 orders recommendations at render
  time (client) per data-model § StudyRecommendation; plan-sheet writes are out
  of v1 scope.
- Session flow (`createSession_`, `validateSession_`, `submitExamAnswers`):
  `Unit Practice` exams ride the standard path with `MAX_ATTEMPTS=2`.
