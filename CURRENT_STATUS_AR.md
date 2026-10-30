# 🏛️ وثيقة الحقيقة وسجل الحالة التشغيلية (Single Source of Truth)

> [!IMPORTANT]
> هذا الملف هو المرجع الوحيد المعتمد لحالة مشروع Primary Exam System. أي مستندات تاريخية أخرى تخضع للبانر التحذيري المرجعي.
> **تاريخ التحديث:** 30 أكتوبر 2026 | **المراحل المكتملة:** P0 و P1 و P2 و P3 و P4 بنجاح كامل 100%

---

## 📊 1. جدول الحقيقة للملفات والأسطح التشغيلية (CodeVersion Ledger)

| الملف | حالة المستودع (Repo State) | حالة النشر (Published State) | الدليل (Evidence) | التاريخ | السطح (Surface) |
|---|---|---|---|---|---|
| `Code.gs` | tracked (محصن + مستويات الصعوبة والمصنع الخماسي) | منشور ومحدث في Apps Script | `npm test` 53/53 PASS + اختبارات الصعوبة | 2026-10-30 | apps-script backend |
| `Index.html` | tracked (تحكم ولي الأمر بالصعوبة والمدة والأسئلة) | منشور ويعمل حياً | HTTP 200 على GitHub Pages + Deep Links | 2026-10-30 | pages frontend |
| `Index.bundle.html` | tracked | حزمة مجمعة للنسخ والنشر (529.3 KB) | مُنشأ عبر `bundle.py` | 2026-10-30 | bundle |
| `.github/workflows/coligo-cloud-sync.yml` | tracked | مفعّل ويعمل آلياً كل ساعة | يدعم مرشحي كلمات السر المتعددة ومكتمل الأسرار | 2026-10-30 | workflow |
| `coligo_manifest.json` | tracked | مفهرس ومحدث | 333 مادة، 123 تنزيل جديد، sheets_webhook: success | 2026-10-30 | storage / metadata |
| `tests/security.test.js` | tracked | جناح اختبارات الأمان والخصوصية | 5/5 اختبارات أمان ناجحة بنسبة 100% | 2026-10-30 | security test suite |
| `tests/difficultyLevels.test.js` | tracked | جناح اختبارات الصعوبة والمصنع الخماسي | 5/5 اختبارات مستويات وصعوبة ناجحة | 2026-10-30 | difficulty test suite |

---

## 🛡️ 2. دفتر تدقيق إصلاحات P0 إلى P4 (Audit Ledger)

| الإصلاح (Fix) | الحالة (State) | الدليل (Evidence) | التاريخ | الملاحظات (Notes) |
|---|---|---|---|---|
| توكنات مصادقة من الخادم (`ACCESS_TOK_*`) | **مثبّت** | `Code.gs:2068` و `tests/server.test.js` | 2026-10-30 | انتهاء عصر التوكنات الثابتة، التوكن يحمل Claims مشفرة ومؤقتة. |
| إخفاء وحظر PINs في الكود الصريح | **مثبّت** | مطابقة `FALLBACK_HASH_*` و `SHA-256` | 2026-10-30 | لا توجد أرقام PIN مكشوفة في كود الواجهة أو السيرفر. |
| عزل بيانات علي ومصطفى | **مثبّت ومختبر** | `tests/security.test.js` (Test 2) | 2026-10-30 | رفض أي طلب لبيانات أو جلسة طالب بتوكن الطالب الآخر (`UNAUTHORIZED`). |
| حماية دوال الإدارة والتحكم | **مثبّت ومختبر** | `tests/security.test.js` (Test 3) | 2026-10-30 | حظر جميع دوال الإدارة (اعتماد، إنشاء، تهيئة) بدون توكن ولي الأمر. |
| حظر إجابات الامتحانات بالمتصفح | **مثبّت ومختبر** | `tests/security.test.js` (Test 4) | 2026-10-30 | الدالة `publicQuestions_` تحذف الإجابة الصحيحة والتفسير تماماً. |
| حماية الـ PIN من التخمين العنيف | **مثبّت ومختبر** | `tests/security.test.js` (Test 5) | 2026-10-30 | قفل البوابة لمدة 10 دقائق بعد 8 محاولات خاطئة (`RATE_LIMITED`). |
| مصادقة كوليجو الحية التلقائية | **مثبّت ومختبر** | `coligo_manifest.json` + `COLIGO_PASSWORD` | 2026-10-30 | سحب المواد بنجاح واكتمال الأسرار في GitHub Secrets. |
| تكامل Webhook جوجل شيت الحي | **مثبّت ومختبر** | `coligo_manifest.json` | 2026-10-30 | رد الخادم بـ `sheets_webhook_status: success`. |
| تصحيح لغوي لأسماء الأعلام بالظروف المتقدمة (P3) | **مثبّت** | `Code.gs` (`formatSubjectAfterFronted_`) | 2026-10-30 | منع تحويل `Commander Davis` إلى حروف صغيرة خطأ. |
| الدقة التاريخية لسؤال قمر سبوتنيك الصناعي (P3) | **مثبّت** | `Code.gs:1203` (1957 Sputnik) | 2026-10-30 | تثبيت حقيقة إطلاق أول قمر صناعي عام 1957 بدلاً من أرقام عشوائية. |
| ربط فيديوهات كامبريدج لماث 5 و 6 (P3) | **مثبّت** | `Index.html` و `Index.bundle.html` | 2026-10-30 | ربط فيديو قابلية القسمة لعلي وفيديو العوامل الأولية لمصطفى. |
| عزل مستويات الصعوبة التكيفية بالسيرفر (P4) | **مثبّت ومختبر** | `tests/difficultyLevels.test.js` | 2026-10-30 | عزل تام للأسئلة بحيث يحصل الطالب على أسئلة مستواه المحدد حصرياً. |
| تحكم ولي الأمر بالصعوبة والمدة وعدد الأسئلة (P4) | **مثبّت** | `Index.template.html` و `Portal.js.html` | 2026-10-30 | تحديد المستوى (L1/L2/L3) وعدد الأسئلة (5-30) والمدة (10-60 دقيقة). |
| شمول مصنع الامتحانات للمواد الخمس (P4) | **مثبّت ومختبر** | `Code.gs` و `tests/difficultyLevels.test.js` | 2026-10-30 | دعم كامل لمواد الرياضيات، العلوم، الإنجليزي، العربي، والحاسب الآلي. |
| شارات المستوى وتصفية امتحانات الطالب (P4) | **مثبّت** | `Index.html` و `Index.bundle.html` | 2026-10-30 | بطاقات مميزة (`L1: Foundational`, `L2: Standard`, `L3: Challenge`). |

---

## 🧪 3. خط الأساس للاختبارات المؤتمتة (Baseline Test Ledger)

- **الأمر المنفذ:** `npm test`
- **التاريخ:** 2026-10-30
- **النتيجة الموثقة:** **53/53 PASS (100% نجاح كامل)**
  - `tests/normalizeAnswer.test.js`: 10/10 PASS
  - `tests/attemptState.test.js`: 8/8 PASS
  - `tests/scoring.test.js`: 5/5 PASS
  - `tests/cumulative.test.js`: 2/2 PASS
  - `tests/server.test.js`: 18/18 PASS
  - `tests/security.test.js`: 5/5 PASS
  - `tests/difficultyLevels.test.js`: 5/5 PASS

---

## 🎯 4. الخطوة التالية (Next Phase: P5)

* **المرحلة القادمة:** `006-test-release-gate`
* **الهدف:** بوابة النشر النهائية، وتوحيد الاختبارات (Playwright E2E + Unit)، وتجهيز الحزمة الإنتاجية المعتمدة النهائية.
