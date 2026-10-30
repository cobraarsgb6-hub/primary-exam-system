# Implementation Plan: 013-studio-labs-humanities
## Phase P12: استديو ومعامل وكروت اللغات والـ ICT والدراسات الاجتماعية لمصطفى وعلي

### Architecture & Work Breakdown

```
Index.template.html
 ├── Includes StemStudioLabs.js
 ├── Includes HumanitiesStudioLabs.js  <-- [NEW P12]
 │    ├── window.HUMANITIES_STUDIO_DATA (19 Units, 190 Flashcards, 19 Interactive Tools)
 │    ├── Sentence Builders (English)
 │    ├── Interactive I'rab Parsers (Arabic)
 │    ├── Flowchart & Scratch Simulators (ICT)
 │    └── Map & Geography Explorers (Social Studies)
 └── Unified Studio Controller
      └── window.renderSubjectStudioUnits() merges STEM + Humanities data

Code.gs Backend
 ├── subjectFamily_ recognizes 'social' / 'دراسات'
 ├── createWeeklyExam_ / createMonthlyExam_ maps 'social' to 'SOC'
 └── Seeding Social Studies questions for G6 & G5 in question bank

Verification Suites
 ├── tests/humanitiesStudioLabs.test.js (Unit data, flashcards, simulation engines)
 ├── tests/difficultyLevels.test.js (Social Studies exam generation)
 └── Playwright E2E & Concurrency Suites
```

### Steps:
1. **Author `HumanitiesStudioLabs.js.html`:**
   - Define data structure for 19 units with complete, high-grade Arabic & English pedagogical content (definitions, examples, rules, traps, and 10 flashcards per unit).
   - Implement interactive JavaScript / DOM simulation engines for all 19 units:
     - 6 English interactive tools.
     - 5 Arabic interactive parsing tools.
     - 4 ICT flowchart / tracing tools.
     - 4 Social Studies map / geography tools.
   - Register into `window.HUMANITIES_STUDIO_DATA` and `window.HUMANITIES_STUDIO_MAP`.
2. **Unify Studio Controller in `StemStudioLabs.js.html` / `Portal.js.html`:**
   - Ensure `getStudioUnit(id)` searches both `STEM_STUDIO_MAP` and `HUMANITIES_STUDIO_MAP`.
   - Update `renderSubjectStudioUnits(subjectCode, containerId)` to search across all registered units.
3. **Include `HumanitiesStudioLabs.js.html` in `Index.template.html`:**
   - Add `<?!= include('HumanitiesStudioLabs.js'); ?>`.
4. **Update `Code.gs` Backend:**
   - Extend `subjectFamily_` to recognise Social Studies.
   - Extend `createWeeklyExam_` and `createMonthlyExam_` to handle prefix `SOC`.
   - Add seed questions for Social Studies in `sampleBankWithLevels()` and `setupDatabase` so exam creation succeeds.
5. **Add Automated Unit Tests:**
   - Create `tests/humanitiesStudioLabs.test.js` validating the 19 units, 190 flashcards, zero placeholders, and tool executions.
   - Update `tests/difficultyLevels.test.js` to assert Social Studies exam generation.
   - Add test file to `package.json`.
6. **Compile and Verify:**
   - Run `python bundle.py` to compile `Index.bundle.html` and sync `Index.html`.
   - Run `npm test`.
   - Run `python tests/test_multisubject_navigation.py`.
   - Run `python tests/test_adversarial_concurrency.py`.
