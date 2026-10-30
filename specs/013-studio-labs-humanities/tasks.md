# Implementation Tasks: 013-studio-labs-humanities
## Phase P12: استديو ومعامل وكروت اللغات والـ ICT والدراسات الاجتماعية لمصطفى وعلي

- [ ] **Task 1: Code.gs Social Studies Integration**
  - Update `subjectFamily_` in `Code.gs` to support `social`, `دراسات`, `soc`.
  - Update `createWeeklyExam_` and `createMonthlyExam_` to handle prefix `SOC`.
  - Add Social Studies bank items to `sampleBankWithLevels()` and `setupDatabase` in `Code.gs`.
  - Add unit test in `tests/difficultyLevels.test.js` validating Social Studies weekly and monthly exam creation.

- [ ] **Task 2: Build Humanities Studio Data & Simulation Engines**
  - Construct `HumanitiesStudioLabs.js.html` with:
    - 6 English Units (106 & 105): Theory + 10 Flashcards + Interactive Sentence Builder / Classifier.
    - 5 Arabic Units (106 & 105): Theory + 10 Flashcards + Interactive I'rab Parsing Lab.
    - 4 ICT Units (106 & 105): Theory + 10 Flashcards + Flowchart Runner / Loop Trace Simulator.
    - 4 Social Studies Units (106 & 105): Theory + 10 Flashcards + Interactive Straits & Topography Explorer.
  - Exactly 19 units and 190 flashcards with zero placeholders.

- [ ] **Task 3: Unify Studio Workspace Rendering**
  - Connect `HumanitiesStudioLabs` into `window.STEM_STUDIO_MAP` / `window.HUMANITIES_STUDIO_MAP` so `renderSubjectStudioUnits` displays the correct units for English, Arabic, ICT, and Social Studies.
  - Include `HumanitiesStudioLabs.js.html` in `Index.template.html`.

- [ ] **Task 4: Build Automated Test Suite**
  - Create `tests/humanitiesStudioLabs.test.js` covering:
    - 19 units metadata & student/subject mapping.
    - 190 flashcards & zero placeholder verification.
    - DOM rendering for all 4 humanities subjects.
    - Execution of all 19 interactive tools.
  - Register test in `package.json`.

- [ ] **Task 5: Bundle & Full Quality Gates**
  - Run `python bundle.py` to compile `Index.bundle.html` and synchronize `Index.html` and android assets.
  - Run `npm test` (all unit and server tests passing).
  - Run `python tests/test_multisubject_navigation.py`.
  - Run `python tests/test_adversarial_concurrency.py`.
