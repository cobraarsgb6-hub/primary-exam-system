# Implementation Plan: P11 — 012-studio-labs-stem
## استديو ومعامل وكروت العلوم والرياضيات لمصطفى وعلي

### Phase 1: Architecture & Data Modeling
1. إنشاء ملف `StemStudioLabs.js.html` لتخزين بنية بيانات `STEM_STUDIO_DATA` لـ 18 وحدة تعليمية متكاملة.
2. لكل وحدة:
   - `id`, `subjectCode`, `student`, `unitNumber`, `title`, `titleEn`, `icon`, `videoId`
   - `theory`: `conceptOverview`, `goldenRules` (array), `workedExamples` (array), `examTraps` (array)
   - `flashcards`: 10 بطاقات تعليمية فريدة (`id`, `front`, `back`, `tip`)
   - `labConfig`: نوع المعمل، عناصر التحكم، دالة الرسم والتشغيل التفاعلية (SVG/Canvas/JS).

### Phase 2: UI Component & Modal Integration
1. تصميم مكون `StudioModal` في `Index.template.html` يضم:
   - شريط العنوان والتنقل بين الوحدات
   - 4 تبويبات رئيسية: 📖 الشرح النظري | 🗂️ كروت المراجعة (10) | 🔬 المعمل التفاعلي | 🎬 الفيديو المعزول
   - كروت تفاعلية مزودة بتأثير التقليب ثلاثي الأبعاد وأزرار التالي/السابق والقلب
   - مساحة المعمل التفاعلي الحية المتجاوبة
2. ربط استعراض الوحدات داخل `openSubjectDetail` في `Portal.js.html`:
   - إضافة قسم "استديو ومعامل الوحدات الدراسية (Interactive Units & Labs)" داخل مساحة عمل المادة.
   - إمكانية فتح أي وحدة مباشرة بنقرة زر واحدة.

### Phase 3: Interactive Simulations Implementation
- برمجة 18 محاكاة تفاعلية حية (بدون مكتبات خارجية ثقيلة، باستخدام Native Vanilla JS + SVG/Canvas):
  1. Circulatory: نبض القلب وسريان الدم المؤكسج وغير المؤكسج مع متحكم نبضات (BPM).
  2. Forces: هبوط المظلة مع تغيير الكتلة ومساحة السطح ومقاومة الهواء.
  3. Circuits: اختبار توصيل المواد (جرافيت، حديد، بلاستيك، خشب) وإضاءة المصباح.
  4. Mixtures: محاكاة خطوات الفصل (مغناطيس، ترشيح، تسخين التبخير).
  5. Changes: دورق التفاعلات الفيزيائية والكيميائية مع تصاعد الغاز أو تغير الحالة.
  6. Measurements: قراءة تقعر السطح بالأسطوانة المدرجة وتدريج الترمومتر.
  7. Place Value: لوحة الملايين التفاعلية مع إزاحة الخانات بالضرب والقسمة.
  8. Prime Tree: شجرة تحليل العوامل التفاعلية لأي رقم مع الصيغة الأسية.
  9. Long Multiplication: خطوات الضرب المطول التفاعلي شبكة وحمل خانات.
  10. Long Division: خطوات القسمة المطولة (Bus Stop) مع البواقي.
  11. FDP: قرص وشريط الكسور والعشري والنسب المئوية مع قراءات متزامنة.
  12. BODMAS: حاسبة ترتيب العمليات مع خط الأعداد السالبة.
  13. Plant Anatomy: مجهر تشريح الساق وصعود الصبغة عبر أوعية الخشب.
  14. Pollination: نقل حبوب اللقاح ونمو أنبوب اللقاح ومحاكي انتشار البذور.
  15. Sound Waves: محاكي تذبذب الجزيئات وتضاغطها في المواد المختلفة.
  16. Pitch & Loudness: راسم الموجات الصوتي مع تردد وسعة وموالف نغمات.
  17. Divisibility: فاحص قابلية القسمة اللحظي مع مصفوفة الإضاءة والتبرير.
  18. Rounding: تلة التقريب الكروية مع الانزلاق للمضاعف الأقرب.

### Phase 4: Bundling & Verification
1. تحديث `Index.template.html` ليشمل `StemStudioLabs.js.html`.
2. إضافة تنسيقات CSS الخاصة بكروت المراجعة والمعامل في `Styles.html`.
3. كتابة اختبار آلي شامل `tests/stemStudioLabs.test.js`.
4. تشغيل `bundle.py` ومزامنة `Index.bundle.html` و `index.html` وتطبيقات الأندرويد.
5. تشغيل `npm test` و Playwright للتحقق من اجتياز 100%.
