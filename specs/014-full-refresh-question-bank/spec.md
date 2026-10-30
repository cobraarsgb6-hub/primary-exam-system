# Feature Specification: 014-full-refresh-question-bank
## Phase P13: التجدد الكامل لبنك الأسئلة وإعادة التوليد الديناميكي (Full Refresh & Dynamic Sampling)

### 1. Architectural Objective
Ensure that in Practice & Training Mode, every browser refresh or click of "تجديد الأسئلة / تدريب جديد" pulls a fresh, unrepeated subset of questions from the bank and recalculates numerical and algorithmic variables on the fly (Dynamic Number Synthesis for Math & Science), strictly complying with **Constitutional Rules 14 and 15**:
- **Rule 14 (Question Density):** Every lesson/unit possesses $\ge 45$ unique question possibilities (15 Foundational L1, 15 Core L2, 15 Advanced L3) via rich bank entries and dynamic algorithmic question generators yielding infinite distinct permutations.
- **Rule 15 (Full Refresh Guarantee):** In training/practice mode, refreshing the page or generating a new training session must NEVER serve identical static numbers or frozen question sequences.

---

### 2. Detailed Technical Scope

#### A. Algorithmic Question Synthesizers (Dynamic Numbers & Formulas)
Implement dynamic math and science generator engines in both `Code.gs` and client offline runtime:
1. **Math 106 (Mostafa):**
   - *Prime Factor Tree & Index Notation:* Dynamic composite numbers $N \in [24, 180]$, prime factor decomposition $N = p_1^{a} \cdot p_2^{b}$, dynamic distractors.
   - *Fractions, Decimals, Percentages (FDP):* Randomized irreducible fractions, calculating exact percentage and decimal equivalence.
   - *Long Division (Bus Stop Method):* Random 3-digit dividend $\div$ 1-digit or 2-digit divisor with quotient and remainder.
   - *BODMAS Operations & Negative Numbers:* Random expressions evaluating precedence ($a + b \times c - d$, $(a + b) \div c$).
   - *Place Value to 10M:* Random 7-8 digit numbers with dynamic digit underlining.
2. **Math 105 (Ali):**
   - *Divisibility Multi-Tester:* Dynamic integer generated and checked against divisibility rules for 2, 3, 4, 5, 6, 8, 9, 10, 25, 100.
   - *Rounding & Number Hill:* Dynamic 4-6 digit integers rounded to nearest 10, 100, 1000, 10000, or 100000.
3. **Science 106 & 105:**
   - *Circuits & Brightness:* Dynamic series/parallel cell count and bulb count calculating voltage and relative luminosity.
   - *Forces & Air Resistance:* Dynamic parachute surface area and fall speed parameters.
4. **English & Arabic Combinatorial Generators:**
   - Adverbial phrases, relative clauses, 5 nouns, and types of predicate with parameterized sentence slots.

#### B. Full Refresh on Reload & Practice Mode
1. **Zero-Stale Cache Protocol:**
   - Practice sessions bypass stored active sessions in the database, appending a dynamic timestamp salt (`Date.now() + random`).
   - Refreshing or restarting practice mode always triggers a fresh question generation run.
2. **"تجديد الأسئلة فورياً (Refresh Bank)" Action:**
   - A prominent button in `screen-quiz` during practice mode allows instant re-sampling with 1-click.
   - Re-evaluates correct answers, points, and explanations according to the new numbers.

#### C. Difficulty Tier Stratification (L1, L2, L3)
- Questions carry explicit difficulty tags:
  - `L1` / `Foundational` (Direct definition, simple application)
  - `L2` / `Standard` (Multi-step calculation, contextual application)
  - `L3` / `Challenging` (Inverse reasoning, word problems, multi-variable logic)
- Balanced exam generation samples evenly across tiers (e.g., 5 L1, 5 L2, 5 L3 for a 15-question exam).

---

### 3. Acceptance Criteria
1. Consecutive requests for the same practice exam code with `isPractice=true` or refresh salt yield different question sets or different numerical values with probability $\ge 99\%$.
2. Algorithmic math generators dynamically compute correct answers and distractor options (e.g., if numbers change from $24$ to $72$, the correct prime factorization updates from $2^3 \times 3$ to $2^3 \times 3^2$).
3. The quiz UI features a working "🔄 تدريب بأسئلة متغيرة (Refresh)" button that restarts the quiz with fresh questions without page crash or error.
4. Zero placeholders: All generated questions contain fully formed questions, options, answers, and pedagogical mistake explanations.
5. Automated tests in `tests/dynamicRefreshBank.test.js` and `tests/server.test.js` pass 100%.
