# Tasks: Phase 8 (`009-parent-dashboard`)

- [x] **Task 1: Core Analytics Engine & Recurrent Weaknesses Grouping**
  - Implement skill-based aggregation in `renderAnalyticsUI()` (`Portal.js.html`).
  - Identify recurrent weaknesses ($\ge 2$ errors or $<70\%$ accuracy).
  - Compute performance trend (`📈 تصاعدي`, `⚖️ مستقر`, `📉 يحتاج مراجعة`).

- [x] **Task 2: 4-Tier Pedagogical Policy & Action Recommendation**
  - Implement 4-tier recommendation policy banner ($\ge 85\%$, $70-84\%$, $50-69\%$, $<50\%$).
  - Add next week roadmap preview card in parent view.

- [x] **Task 3: Results CSV Export & Print Action**
  - Add `exportSubmissionsCSV()` in `Portal.js.html` with UTF-8 BOM for Excel Arabic support.
  - Add "تصدير النتائج (CSV)" button in the Parent Dashboard.

- [x] **Task 4: Unit Test Suite (`tests/parentDashboard.test.js`)**
  - Test trend detection, weakness grouping, policy mapping, and CSV serialization.
  - Wire into `package.json`.

- [x] **Task 5: Bundle Synchronization & E2E Verification**
  - Run `python bundle.py`.
  - Run `npm test` and `run_all_e2e.py`.

- [x] **Task 6: Update Truth Ledger & Git Commit**
  - Update `CURRENT_STATUS_AR.md`, `.wolf/STATUS.md`, and `cerebrum.md`.
  - Commit P8 implementation.
