# Feature Specification: P6 — Cumulative Multi-Subject Exam Schedule & Adaptive Learning Engine

**Feature Directory:** `specs/007-schedule-cumulative`  
**Status:** In Progress / Implementing  
**Author:** Antigravity Architect (for Ahmed Ibrahim)  
**Date:** October 30, 2026  

---

## 1. Executive Summary & Problem Statement
Currently, `primary-exam-system` features baseline exam generation for W1 and M1, but lacks a complete automated cumulative schedule spanning W1 through W4 and the Monthly Capstone (M1) as detailed in `EXAM_SCHEDULE_PLAN.md`. Furthermore, `Study_Plan` only contains English and Arabic items, omitting Mathematics, Science, and ICT.

Phase 6 implements:
1. **The `Exam_Schedule` table**: A structured 30-day curriculum schedule for Ali (Year 5) and Mostafa (Grade 6).
2. **Complete 5-Subject `Study_Plan`**: Incorporating Math, Science, English, Arabic, and ICT across all 4 weeks.
3. **Cumulative Exam Generation Engine**:
   - `W1`: Days 1–7 (10–12 questions).
   - `W2`: Days 1–14 (12–15 questions, ~50% W2 / 50% W1).
   - `W3`: Days 1–21 (15–18 questions, ~40% W3 / 30% W2 / 30% W1).
   - `W4`: Days 1–28 (18–22 questions, ~30% W4 / 25% W3 / 25% W2 / 20% W1).
   - `M1`: Full Month (20–25 questions, ~25% per week, zero W4 duplicate questions).
4. **Coverage First & Non-Duplication Policy**:
   - Every covered lesson must be represented by at least 1 question.
   - If a lesson lacks questions in the bank, surface a descriptive pedagogical alert (`Warning: Lesson X needs questions in Question_Bank`) rather than duplicating existing items.
   - Zero Question ID overlap between the Milestone exam (W1–W4 / M1) and the Daily exam held on the same day.
5. **Adaptive Progression**:
   - Score < 70%: Target skill generates 2 reinforcement questions on the following daily session.
   - Score >= 85%: Unlocks an additional Challenge-tier question on the next session.
6. **Difficulty Ordering**: Easy → Medium → Challenge.

---

## 2. Data Model & Sheet Schemas

### A. `Exam_Schedule` Sheet
Columns:
1. `Schedule ID`
2. `Date`
3. `Student`
4. `Grade Level`
5. `Subject`
6. `Exam Code`
7. `Exam Title`
8. `Exam Type` (`Daily`, `Weekly`, `Monthly`)
9. `Period` (`W1`, `W2`, `W3`, `W4`, `M1`)
10. `Questions Count`
11. `Duration (Mins)`
12. `Difficulty`
13. `Status` (`Scheduled`, `Active`, `Completed`)
14. `Daily Pair Code` (The distinct non-overlapping daily quiz paired on milestone days)

### B. `Study_Plan` Expansion
Expands from 25 items to 60+ items covering the 5 core subjects:
- **Ali Ahmed (Year 5 / G5):** Math, Science, English, Arabic, ICT.
- **Mostafa Ahmed (Grade 6 / G6):** Math, Science, English, Arabic, ICT.

---

## 3. Acceptance Criteria
1. **Full Month Schedule Generation**: `setupDatabase` or `initializeMonthSchedule` populates `Exam_Schedule` and full 5-subject `Study_Plan`.
2. **Cumulative Period Slicing**: W2, W3, W4, and M1 tests confirm multi-week question synthesis adhering to the target percentage distribution and lesson coverage.
3. **Zero Same-Day Question Overlap**: Automated test verifies that paired daily exams and milestone exams share 0 question IDs.
4. **Adaptive Response Rules**: Tests verify score threshold triggers (<70% and >=85%).
5. **Full Test Suite Integrity**: All unit (`npm test`) and E2E suites remain 100% green.
