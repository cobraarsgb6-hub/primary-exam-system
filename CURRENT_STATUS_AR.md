# 🏛️ وثيقة الحقيقة وسجل الحالة التشغيلية (Single Source of Truth)

> [!IMPORTANT]
> هذا الملف هو المرجع الوحيد المعتمد لحالة مشروع Primary Exam System. أي مستندات تاريخية أخرى تخضع للبانر التحذيري المرجعي.
> **تاريخ التحديث:** 30 أكتوبر 2026 | **المراحل المكتملة:** P0 و P1 و P2 بنجاح كامل 100%

---

## 📊 1. جدول الحقيقة للملفات والأسطح التشغيلية (CodeVersion Ledger)

| الملف | حالة المستودع (Repo State) | حالة النشر (Published State) | الدليل (Evidence) | التاريخ | السطح (Surface) |
|---|---|---|---|---|---|
| `Code.gs` | tracked (محصن ضد الثغرات وتزوير التوكنات) | منشور ومحدث في Apps Script | `npm test` 48/48 PASS + اختبارات الأمان | 2026-10-30 | apps-script backend |
| `index.html` | tracked | منشور ويعمل حياً | HTTP 200 على GitHub Pages + Deep Links | 2026-10-30 | pages frontend |
| `Index.bundle.html` | tracked | حزمة مجمعة للنسخ والنشر | مُنشأ عبر `bundle.py` | 2026-10-30 | bundle |
| `.github/workflows/coligo-cloud-sync.yml` | tracked | مفعّل ويعمل آلياً كل ساعة | يدعم مرشحي كلمات السر المتعددة | 2026-10-30 | workflow |
| `coligo_manifest.json` | tracked | مفهرس ومحدث | 333 مادة، 123 تنزيل جديد، sheets_webhook: success | 2026-10-30 | storage / metadata |
| `tests/security.test.js` | tracked | جناح اختبارات الأمان والخصوصية | 5/5 اختبارات أمان ناجحة بنسبة 100% | 2026-10-30 | security test suite |

---

## 🛡️ 2. دفتر تدقيق إصلاحات P0 و P1 و P2 (Security & Audit Ledger)

| الإصلاح (Fix) | الحالة (State) | الدليل (Evidence) | التاريخ | الملاحظات (Notes) |
|---|---|---|---|---|
| توكنات مصادقة من الخادم (`ACCESS_TOK_*`) | **مثبّت** | `Code.gs:2068` و `tests/server.test.js` | 2026-10-30 | انتهاء عصر التوكنات الثابتة، التوكن يحمل Claims مشفرة ومؤقتة. |
| إخفاء وحظر PINs في الكود الصريح | **مثبّت** | مطابقة `FALLBACK_HASH_*` و `SHA-256` | 2026-10-30 | لا توجد أرقام PIN مكشوفة في كود الواجهة أو السيرفر. |
| عزل بيانات علي ومصطفى | **مثبّت ومختبر** | `tests/security.test.js` (Test 2) | 2026-10-30 | رفض أي طلب لبيانات أو جلسة طالب بتوكن الطالب الآخر (`UNAUTHORIZED`). |
| حماية دوال الإدارة والتحكم | **مثبّت ومختبر** | `tests/security.test.js` (Test 3) | 2026-10-30 | حظر جميع دوال الإدارة (اعتماد، إنشاء، تهيئة) بدون توكن ولي الأمر. |
| حظر إجابات الامتحانات بالمتصفح | **مثبّت ومختبر** | `tests/security.test.js` (Test 4) | 2026-10-30 | الدالة `publicQuestions_` تحذف الإجابة الصحيحة والتفسير تماماً. |
| حماية الـ PIN من التخمين العنيف | **مثبّت ومختبر** | `tests/security.test.js` (Test 5) | 2026-10-30 | قفل البوابة لمدة 10 دقائق بعد 8 محاولات خاطئة (`RATE_LIMITED`). |
| مصادقة كوليجو الحية التلقائية | **مثبّت ومختبر** | `coligo_manifest.json` | 2026-10-30 | سحب 333 مادة بنجاح وحفظ 123 ملفاً جديداً. |
| تكامل Webhook جوجل شيت الحي | **مثبّت ومختبر** | `coligo_manifest.json` | 2026-10-30 | رد الخادم بـ `sheets_webhook_status: success`. |

---

## 🧪 3. خط الأساس للاختبارات المؤتمتة (Baseline Test Ledger)

- **الأمر المنفذ:** `npm test`
- **التاريخ:** 2026-10-30
- **النتيجة الموثقة:** **48/48 PASS (100% نجاح كامل)**
  - `tests/normalizeAnswer.test.js`: 10/10 PASS
  - `tests/attemptState.test.js`: 8/8 PASS
  - `tests/scoring.test.js`: 5/5 PASS
  - `tests/cumulative.test.js`: 2/2 PASS
  - `tests/server.test.js`: 18/18 PASS
  - `tests/security.test.js`: 5/5 PASS

---

## 🎯 4. الخطوة التالية (Next Phase: P3)

* **المرحلة القادمة:** `004-content-media-fixes`
* **الهدف:** تصحيح روابط الفيديوهات التعليمية (إصلاح ربط ماث علي بفيديو الهمزة، وتصحيح فيديو ماث مصطفى)، وتدقيق نصوص الأسئلة المنهجية لضمان سلامتها العلمية والتربوية 100%.
