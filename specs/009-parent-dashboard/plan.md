# Implementation Plan: Phase 8 (`009-parent-dashboard`)

## 1. Architecture & Component Blueprint

### A. Analytics Aggregation Engine (`Portal.js.html`)
1. **Skill & Weakness Grouping:**
   - In `renderAnalyticsUI()`, aggregate each review question by its `unit` or topic (using metadata or regex extraction from question text).
   - Compute total attempts and failed attempts per skill.
   - Any skill with $\ge 2$ errors or accuracy $< 70\%$ is classified as `Recurrent Weakness`.
2. **Score Trend Computation:**
   - Take the chronological array of student submissions.
   - Compare average of oldest half vs newest half (or last 3 vs prior 3).
   - If change $> +5\% \rightarrow$ `📈 تصاعدي (+X%) / Improving`.
   - If change $< -5\% \rightarrow$ `📉 تراجع (-X%) / Needs Attention`.
   - Otherwise $\rightarrow$ `⚖️ مستقر / Stable`.
3. **4-Tier Action Recommendation Banner:**
   - Insert high-contrast callout banner based on `avgPercentage`:
     - $\ge 85\%$: 🌟 `خطة الإثراء والتحدي` (Unlock higher difficulty / bonus challenges).
     - $70\% - 84\%$: 📘 `خطة التثبيت والممارسة` (Focus on timed speed and confidence).
     - $50\% - 69\%$: 💡 `خطة إعادة الشرح والتعزيز` (Review video lessons and core law checkpoints).
     - $< 50\%$: 🚨 `خطة التدخل المشترك مع ولي الأمر` (Joint parent-student step-by-step walkthrough).
4. **CSV Export Action:**
   - Add `exportSubmissionsCSV()` function generating an RFC 4180 compliant CSV string with BOM (`\uFEFF` for Arabic Excel support).
   - Trigger browser download with a single click.

### B. Unit & Regression Tests (`tests/parentDashboard.test.js`)
1. Test score trend logic (improving, declining, stable).
2. Test recurrent weaknesses grouping ($\ge 2$ errors threshold).
3. Test 4-tier action recommendation mapping.
4. Test CSV export string generation with proper escaping and Arabic UTF-8 BOM.

### C. Bundle & E2E Verification
1. Re-bundle with `python bundle.py`.
2. Run full test suite `npm test` (targeting 67+ tests passing).
3. Run `python tests/e2e/run_all_e2e.py` (51/51 tests passing).
