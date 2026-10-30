# Spec: Phase 4 Exam Engine Levels (005-exam-engine-levels)

## Objective
Enable true adaptive difficulty levels across all 5 subjects (English, Arabic, Mathematics, Science, ICT Computing), give parents complete granular control over exam duration, question count, and difficulty level (Level 1 Foundational, Level 2 Standard, Level 3 Challenge), and guarantee server-side strict question isolation by difficulty.

## Requirements & Scope
1. **Question Difficulty Isolation**:
   - `loadBankQuestionsByPeriod_` must strictly enforce difficulty matching when a target level is specified.
   - `buildExamQuestions_` must pass the exam's configured difficulty to the bank loader so students receive exclusively the questions matching their exam level.
2. **5-Subject Complete Coverage**:
   - Both Weekly and Monthly Exam Factories must seamlessly support:
     1. Mathematics
     2. Science
     3. English Grammar / Literacy
     4. Arabic Language
     5. ICT Computing
     6. Comprehensive All-Subjects Synthesis
3. **Unique Exam Codes & Registry**:
   - Exam codes must incorporate subject and difficulty identifiers (e.g. `EX_Y5_ALI_W1_MATH_CHA`) preventing collisions and overwrites.
   - The `Exams` sheet must record the target difficulty alongside duration and question count.
4. **Parent Customization Controls**:
   - Parent Operations UI must provide adjustable inputs for:
     - Target Period (W1-W5, M1-M3)
     - Subject Focus
     - Difficulty Level (Foundational / Standard / Challenging / All)
     - Question Count (5 to 30)
     - Duration in Minutes (10 to 60)
5. **Student Experience & Badge Transparency**:
   - Student catalog cards must render clear, authentic difficulty badges (`L1: Foundational`, `L2: Standard`, `L3: Challenge`).
   - The student difficulty selector must filter catalog assessments by the chosen level or show all when reset.
