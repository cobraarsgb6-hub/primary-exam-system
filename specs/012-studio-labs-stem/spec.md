# Feature Specification: P11 — 012-studio-labs-stem
## استديو ومعامل وكروت العلوم والرياضيات لمصطفى وعلي

### 1. الهدف المعماري (Architectural Objective)
تعميم تجربة "معمل الكهرباء" لتشمل جميع دروس العلوم والرياضيات لمصطفى (G6) وعلي (G5) عبر بناء استديو تعليمي تفاعلي كامل لكل وحدة من الـ 18 وحدة دراسية. يحتوي كل درس إلزامياً على أركان الدرس الأربعة وفقاً للمادة 12 من الدستور:
1. الشرح النظري المهيكل (Nagwa / Cambridge Format).
2. 10 كروت مراجعة تفاعلية (Flip Flashcards) مع تقليب سلس واختبار فوري.
3. معمل تفاعلي ومحاكاة حية مخصصة للدرس (SVG / Canvas / JS) بدون أي محاكاة وهمية.
4. مشغل فيديو معزول أو بطاقة «الفيديو قيد الإعداد» في حال عدم توفر فيديو معتمد.

### 2. نطاق الوحدات الـ 18 (18 Units Matrix)
#### علوم مصطفى (Science 106 - 6 وحدات):
1. `sci106_circulatory`: محاكاة نبض القلب والدورة الدموية المزدوجة (Circulatory System: Heart, Blood Vessels & Double Circulation).
2. `sci106_forces`: محاكاة القوى والاحتكاك ومقاومة الهواء والمظلات (Forces, Friction & Air Resistance).
3. `sci106_circuits`: معمل الكهرباء المتكامل والدوائر والتوصيل (Electric Circuits, Series/Parallel, Conductors & Insulators).
4. `sci106_mixtures`: معمل فصل المخاليط بالترشيح والتبخير (Mixtures & Separation Techniques).
5. `sci106_changes`: معمل التغيرات الفيزيائية والكيميائية العكسية وغير العكسية (Reversible vs Irreversible Changes).
6. `sci106_measurements`: أداة القياسات المعملية وقراءة التدريج والحرارة (Scientific Measurements & Investigation).

#### رياضيات مصطفى (Math 106 - 6 وحدات):
7. `math106_place_value`: لوحة القيمة المكانية حتى 10,000,000 (Place Value to 10M & Exponent Shifting).
8. `math106_prime_factors`: شجرة العوامل الأولية والصيغة الأسية (Prime Factor Tree & Index Notation).
9. `math106_multiplication`: الضرب المطول التفاعلي بخطوات مجزأة (Step-by-Step Long Multiplication).
10. `math106_division`: القسمة المطولة بطريقة الحافلة وتفسير البواقي (Long Division - Bus Stop Method).
11. `math106_fdp`: محول الكسور والعشري والنسب المئوية مع قرص تفاعلي (FDP Visual Converter).
12. `math106_bodmas`: محاكي ترتيب العمليات والأعداد السالبة (BODMAS & Negative Numbers).

#### علوم علي (Science 105 - 4 وحدات):
13. `sci105_plant_anatomy`: تشريح النبات التفاعلي وتتبع صبغة أوعية الخشب واللحاء (Plant Anatomy, Xylem & Phloem).
14. `sci105_pollination`: تلقيح الأزهار وانتشار البذور (Pollination & Seed Dispersal).
15. `sci105_sound_vibrations`: اهتزازات الصوت وتذبذب الجزيئات في الأوساط (Sound Vibrations & Waves).
16. `sci105_pitch_loudness`: مختبر حدة وشدة الصوت والراسم التذبذبي (Pitch vs Loudness Laboratory).

#### رياضيات علي (Math 105 - وحدتان):
17. `math105_divisibility`: فاحص قابلية القسمة الذكي (2, 3, 4, 5, 6, 8, 9, 10, 25, 100) (Divisibility Multi-Tester).
18. `math105_rounding_pv`: محاكي التقريب والقيمة المكانية حتى 1,000,000 (Place Value & Rounding Number Hill).

### 3. معايير القبول (Acceptance Criteria)
- كل وحدة من الـ 18 وحدة تحتوي على تبويب شرح نظري لا يقل عن 250 كلمة يشرح القواعد والأمثلة والأخطاء الشائعة.
- كل وحدة تحتوي على 10 كروت مراجعة فريدة تماماً تدعم التقليب التفاعلي والتنقل.
- كل وحدة تحتوي على معمل تفاعلي حقيقي (SVG/Canvas/JS) يتجاوب مع مدخلات الطالب (Sliders, Buttons, Toggles).
- حظر الـ Placeholders بالكامل: منع نصوص "سيتم إضافة الشرح" أو الكروت المكررة.
- اختبار آلي شامل `tests/stemStudioLabs.test.js` يتحقق من وجود وصحة جميع الـ 18 وحدة وكروتها الـ 180 ومعاملها الـ 18.
- إعادة بناء الحزمة عبر `bundle.py` بنجاح واختبار التشغيل الكامل بنسبة 100%.
