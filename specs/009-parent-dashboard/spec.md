# Phase 8 Specification: Parent Command Dashboard & Multi-Subject Analytics (`009-parent-dashboard`)

## 1. Context & Business Value
Parents need an immediate, bird's-eye diagnostic view of their children's learning progression across all 5 primary subjects (Mathematics, Science, English, Arabic, ICT). Rather than navigating raw spreadsheet rows, the Parent Dashboard provides instant answers to:
- *"Which specific skills need reinforcement this week?"*
- *"Are scores improving or declining over time?"*
- *"What pedagogical intervention should I take based on the student's mastery percentage?"*
- *"What is scheduled for next week, and how can I export the grade summary?"*

All of this must be accessible securely with the Parent PIN (`1990`) while strictly preserving student privacy on static web hosting.

## 2. User Stories
- **US-P8.1 (At-a-Glance Weekly Skill Deficiencies):** As a parent, I want to see a dedicated "Recurrent Weaknesses" card highlighting skills where the child made $\ge 2$ mistakes, so that I know exactly what to review this week without opening Google Sheets.
- **US-P8.2 (Weekly & Monthly Score Trend Indicators):** As a parent, I want to see the performance trajectory (e.g. `📈 Improving (+12%)`, `⚖️ Stable`, or `📉 Needs Attention`) calculated from chronological submissions.
- **US-P8.3 (Automated Pedagogical Action Recommendations):** As a parent, I want actionable guidance tailored to mastery brackets:
  - $\ge 85\%$: "إثراء وتحدٍ (Challenge & Extension)"
  - $70\% - 84\%$: "مراجعة تدريبية وتثبيت (Targeted Practice)"
  - $50\% - 69\%$: "إعادة تدريس المفهوم (Concept Re-teaching)"
  - $< 50\%$: "مراجعة مشتركة وتدخل مع ولي الأمر (Parent Intervention)"
- **US-P8.4 (Month Calendar & Next Week Ahead):** As a parent, I want to review the full 28-day roadmap calendar and preview next week's scheduled lessons and milestones for Ali and Mostafa.
- **US-P8.5 (CSV / Printable Results Export):** As a parent, I want to export submission reports to CSV or print a formatted PDF summary for offline tracking and portfolio records.
- **US-P8.6 (Retake Approvals & Security Isolation):** As a parent, I want to approve or decline student retake requests directly from the dashboard with real-time updates.

## 3. Functional Requirements
1. **Server-Side & Client-Side Aggregation (`Code.gs` & `Portal.js.html`):**
   - Enhance analytics computation to aggregate mistakes by Unit/Topic across all previous submissions.
   - Categorize skills into `Mastered` ($\ge 85\%$), `Developing` ($70-84\%$), and `Needs Review` ($<70\%$ or $\ge 2$ mistakes).
   - Calculate performance trend from the last 3-5 submissions.
2. **Pedagogical Action Card:**
   - Display recommended action banner in the Parent Analytics view matching the active student's average percentage.
3. **Weekly & Monthly Calendar View:**
   - Visual month progression showing completed, active, and upcoming milestone exams.
4. **Export Capabilities:**
   - Client-side CSV export generator downloading `student_submissions_<name>.csv` with date, exam code, score, duration, and status.
5. **Security & Data Privacy:**
   - Parent features gated by valid `adminToken` (minted via PIN `1990`).
   - Sensitive student reports are only served to authenticated parent sessions.

## 4. Acceptance Criteria
- [ ] Parent can answer "What skills need review this week?" directly from the Analytics tab for both Ali and Mostafa.
- [ ] Recurrent weaknesses card groups by skill/unit and highlights items with $\ge 2$ mistakes.
- [ ] Score trend indicator (Improving/Stable/Declining) renders dynamically.
- [ ] 4-tier pedagogical action policy renders according to score thresholds.
- [ ] Results CSV export button downloads clean, formatted assessment data.
- [ ] 100% pass on all unit tests (`npm test`) and E2E Playwright tests.
