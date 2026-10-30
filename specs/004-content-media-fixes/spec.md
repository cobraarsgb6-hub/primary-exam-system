# Spec: Phase 3 Content & Media Fixes (004-content-media-fixes)

## Objective
Fix dynamic question generation grammatical/historical inaccuracies and link authentic pedagogical media (curriculum video explanations) for both Grade 5 and Grade 6.

## Scope
1. **Adverbial Grammar Fix**:
   - Proper nouns like `Commander Davis` and `The Apollo rover` must not be lowercased into `commander davis` when preceded by fronted adverbials.
   - Introduced `formatSubjectAfterFronted_()` to only lowercase `The ` -> `the ` and preserve proper nouns.
2. **Historical Accuracy Fix**:
   - Fixed Q10 in `generateAliAdverbialExam_()` to refer factually to 1957 (Sputnik satellite launch) rather than random years.
3. **Curriculum Video Integration**:
   - Linked Ali Year 5 Math 105 to verified Cambridge Year 5 Divisibility Rules video (`Luq06b4D6bE`).
   - Linked Mostafa Year 6 Math 106 to verified Cambridge Year 6 Prime Factorization video (`XGbOiYhHY2c`).
   - Rebuilt production bundle `Index.bundle.html`.

## Verification
- Security and unit test suites: 48/48 PASS.
- Production bundle size: 525.1 KB.
