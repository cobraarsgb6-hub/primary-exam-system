# Implementation Tasks: 015-dynamic-level-banks
## Phase P14: تعميق بنك الأسئلة وتوسيع مستويات L1 / L2 / L3

- [x] **Task 1: Expand Sample Bank & Level Matrix in Code.gs**
  - Enrich `sampleBankWithLevels()` with authentic L1, L2, L3 stratified question rows across all subjects (Math, Science, English, Arabic, ICT, Social Studies).
  - Ensure zero placeholders: every item has rich explanation, authentic distractors, and difficulty tag ('Easy'/'Medium'/'Hard').

- [x] **Task 2: Synchronize Mock Bridge Server Catalog**
  - Update `tests/e2e/mock_bridge.js` to mirror all expanded bank items and level distributions.

- [x] **Task 3: Automated Verification Suite for Level Banks**
  - Build `tests/dynamicLevelBanks.test.js` validating:
    - Minimum density thresholds per subject/lesson.
    - Strict classification into Easy (L1), Medium (L2), Hard (L3).
    - Explanation quality and absence of placeholders.
  - Register in `package.json`.

- [x] **Task 4: Bundle & Full Quality Gates**
  - Run `python bundle.py` and sync `Index.html`, `index.html`, and Android assets.
  - Run `npm test`.
  - Run `python tests/test_multisubject_navigation.py` and `python tests/test_adversarial_concurrency.py`.
