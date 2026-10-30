# Feature Specification: 013-studio-labs-humanities
## Phase P12: استديو ومعامل وكروت اللغات والـ ICT والدراسات الاجتماعية لمصطفى وعلي

### 1. Architectural Objective
Provide complete theoretical curriculum explanations (Nagwa / Cambridge style), $\ge 10$ interactive 3D flashcards per unit, dedicated interactive application labs/tools (Sentence Builder, Interactive Parsing Lab, Flowchart Runner & Loop Tracer, and Arab World & Egypt Map Explorer) across all **19 Humanities units** (English, Arabic, ICT, Social Studies), while formally registering **Social Studies** in the `Code.gs` exam factory alongside the existing 5 subjects.

---

### 2. Units Scope (19 Full Units across 4 Disciplines)

#### A. English (6 Units: 3 Mostafa Grade 6, 3 Ali Year 5)
1. `eng106_relative_clauses` (Mostafa - English 106):
   - Theory: Defining vs Non-defining relative clauses, pronouns (`who`, `which`, `that`, `whose`, `where`), comma boundaries.
   - Flashcards: 10 cards on pronoun selection and punctuation.
   - Interactive Tool: Relative Clause Sentence Joiner & Inspector.
2. `eng106_connectives` (Mostafa - English 106):
   - Theory: Coordinating (FANBOYS) vs Subordinating conjunctions (although, whereas, since, unless), position and comma rules.
   - Flashcards: 10 cards on conjunction function and sentence synthesis.
   - Interactive Tool: Discourse Marker & Clause Builder.
3. `eng106_fiction_nonfiction` (Mostafa - English 106):
   - Theory: Linguistic features of formal reports vs narrative texts (passive voice, objective tone, sensory imagery).
   - Flashcards: 10 cards differentiating genres and register.
   - Interactive Tool: Real-time Text Genre Classifier & Feature Highlighter.
4. `eng105_adverbials` (Ali - English 105):
   - Theory: Fronted adverbials of Time, Place, and Manner; the mandatory comma rule.
   - Flashcards: 10 cards identifying adverbial types and commas.
   - Interactive Tool: Fronted Adverbial Sentence Arranger.
5. `eng105_direct_speech` (Ali - English 105):
   - Theory: Inverted commas ("..."), speech punctuation (commas, exclamation marks, question marks inside quotes), new speaker new line.
   - Flashcards: 10 cards correcting speech punctuation traps.
   - Interactive Tool: Dialogue Punctuation Fixer.
6. `eng105_fables_proverbs` (Ali - English 105):
   - Theory: Narrative structure of fables, personification, moral lessons, and common proverbs.
   - Flashcards: 10 cards analyzing proverb meanings and story elements.
   - Interactive Tool: Fable Moral & Plot Analyzer.

#### B. Arabic (5 Units: 3 Mostafa Grade 6, 2 Ali Year 5)
7. `arb106_five_nouns` (Mostafa - Arabic 106):
   - Theory: الأسماء الخمسة (أب، أخ، حم، فو، ذو)، علامات إعرابها الفرعية (الواو رفعاً، الألف نصباً، الياء جراً)، والشروط الأربعة (مفردة، مضافة، إضافتها لغير ياء المتكلم، خلو "فم" من الميم).
   - Flashcards: 10 cards on identification, case markers, and condition violations.
   - Interactive Tool: معمل فحص شروط وإعراب الأسماء الخمسة.
8. `arb106_types_of_predicate` (Mostafa - Arabic 106):
   - Theory: أنواع الخبر (مفرد، جملة اسمية ورابطها، جملة فعلية، شبه جملة جار ومجرور أو ظرف).
   - Flashcards: 10 cards classifying predicate types and extraction.
   - Interactive Tool: معمل تفكيك الجملة الاسمية وتحديد نوع الخبر والموقع الإعرابي.
9. `arb106_nakira_marifa` (Mostafa - Arabic 106):
   - Theory: النكرة والمعرفة (المعرف بأل، العلم، الضمائر بأنواعها، أسماء الإشارة، الأسماء الموصولة، المعرف بالإضافة).
   - Flashcards: 10 cards on identifying the 6 categories of definite nouns.
   - Interactive Tool: مصنف النكرة والمعرفة السريع.
10. `arb105_nominal_sentence` (Ali - Arabic 105):
    - Theory: ركنا الجملة الاسمية (المبتدأ والخبر) وعلامات الرفع الأصلية والفرعية (الضمة، الألف للمثنى، الواو لجمع المذكر السالم).
    - Flashcards: 10 cards on identifying subject/predicate and selecting correct case endings.
    - Interactive Tool: ميزان ضبط المبتدأ والخبر بالحركات.
11. `arb105_object_mafool` (Ali - Arabic 105):
    - Theory: المفعول به في الجملة الفعلية وعلامات نصبه (الفتحة للمفرد وجمع التكسير، الكسرة لجمع المؤنث السالم، الياء للمثنى وجمع المذكر السالم).
    - Flashcards: 10 cards on detecting direct objects and choosing exact accusative markers.
    - Interactive Tool: كاشف المفعول به وعلامة النصب.

#### C. ICT (4 Units: 2 Mostafa Grade 6, 2 Ali Year 5)
12. `ict106_flowcharts` (Mostafa - ICT 106):
    - Theory: الرموز القياسية لخرائط التدفق (Start/End Oval, Process Rectangle, Decision Diamond, Input/Output Parallelogram, Flowline Arrows).
    - Flashcards: 10 cards on flowchart symbol logic and algorithm dry-runs.
    - Interactive Tool: محاكي تشغيل وتتبع خريطة التدفق (Step-by-step Execution Engine).
13. `ict106_loops_variables` (Mostafa - ICT 106):
    - Theory: خوارزميات التكرار (Count-controlled Loops vs Condition-controlled Loops)، وتتبع المتغيرات وجداول التتبع (Trace Tables).
    - Flashcards: 10 cards on loop termination, off-by-one errors, and variable state.
    - Interactive Tool: جدول التتبع التفاعلي وحاسبة مخرجات الحلقات (Trace Table Simulator).
14. `ict105_scratch_logic` (Ali - ICT 105):
    - Theory: مبادئ البرمجة في سكراتش (لبنات الحركة، الإحداثيات X و Y، المتغيرات، التكرار 'كرر 10 مرات').
    - Flashcards: 10 cards on Scratch block behaviors and coordinate changes.
    - Interactive Tool: محاكي إحداثيات ومنصة سكراتش التفاعلية (Scratch Stage Coordinate Simulator).
15. `ict105_cyber_safety` (Ali - ICT 105):
    - Theory: الأمان الرقمي، البصمة الرقمية (Digital Footprint)، كلمات المرور القوية، والحماية من التصيد والرسائل المجهولة.
    - Flashcards: 10 cards on cyber safety rules and scenario evaluations.
    - Interactive Tool: فاحص قوة كلمات المرور ومكافح التصيد التفاعلي.

#### D. Social Studies (4 Units: 2 Mostafa Grade 6, 2 Ali Year 5) + Code.gs Integration
16. `soc106_arab_geography` (Mostafa - Social Studies 106):
    - Theory: الموقع الجغرافي للوطن العربي (بين آسيا وأفريقيا)، الممرات المائية والمضايق الاستراتيجية (مضيق هرمز، باب المندب، قناة السويس، مضيق جبل طارق)، وتضاريسه (جبال التوائية وانكسارية، الهضاب، والسهول الفيضية والساحلية).
    - Flashcards: 10 cards on straits, seas, mountain systems, and economic importance.
    - Interactive Tool: خريطة مضايق وتضاريس الوطن العربي التفاعلية (Interactive Straits & Topography Explorer).
17. `soc106_arab_environment` (Mostafa - Social Studies 106):
    - Theory: الأقاليم المناخية (البحر المتوسط، الصحراوي الحار، المداري)، والتحديات البيئية (التصحر، الجفاف، ندرة المياه العذبة) والحلول المستدامة.
    - Flashcards: 10 cards on climate zones and environmental strategies.
    - Interactive Tool: حاسبة البصمة البيئية والتكيف المناخي في الوطن العربي.
18. `soc105_egypt_geography` (Ali - Social Studies 105):
    - Theory: موقع مصر الجغرافي والفلكي، قلب العالم القديم، الإشراف على البحرين (الأحمر والمتوسط) وقناة السويس وتأثيرها التجاري والحضاري.
    - Flashcards: 10 cards on geographic coordinates, boundaries, and trade waterways.
    - Interactive Tool: مستكشف خريطة موقع مصر الجغرافي والممرات المائية.
19. `soc105_ancient_civilization` (Ali - Social Studies 105):
    - Theory: عوامل قيام الحضارة المصرية القديمة: العوامل الطبيعية (نهر النيل، الموقع الجغرافي، المناخ، الثروات المعدنية والصخور) والعوامل البشرية (الجيش القوي، الوحدة، الكفاح الإنساني).
    - Flashcards: 10 cards classifying natural vs human civilizational factors.
    - Interactive Tool: ميزان أركان الحضارة المصرية القديمة (Interactive Civilization Pillar Builder).

---

### 3. Backend Integration (Code.gs)
1. **Subject Family Recognition:** Update `subjectFamily_` in `Code.gs` to map `social`, `دراسات`, `soc` to `'social'`.
2. **Exam Factory Subject Support:**
   - In `createWeeklyExam_` and `createMonthlyExam_`, map `'social'` to prefix `'SOC'`.
   - Seed representative Social Studies questions in the question bank for both Grade 6 and Year 5.
3. **Admin UI Prompts:** Update admin menus to allow generating Social Studies weekly and monthly assessments.

---

### 4. Acceptance Criteria & Quality Gates
1. Exactly **19 units** defined in `HumanitiesStudioLabs.js.html` with full metadata and student/subject mappings.
2. Zero placeholders: Every unit has substantial Nagwa/Cambridge theory, rules, traps, exactly **10 3D flashcards** (190 total), and a dedicated, functioning interactive tool.
3. Integration with `#unit-studio-modal`: Clicking any humanities unit in English, Arabic, ICT, or Social Studies opens the studio modal and displays all 4 tabs seamlessly.
4. Social Studies fully integrated in `Code.gs` with automated tests verifying `createWeeklyExam` and `createMonthlyExam` for Social Studies.
5. 100% test pass on automated suites (`npm test`, `test_multisubject_navigation.py`, `test_adversarial_concurrency.py`).
