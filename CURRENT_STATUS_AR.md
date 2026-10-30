# 🏛️ وثيقة الحقيقة وسجل الحالة التشغيلية (Single Source of Truth)

> [!IMPORTANT]
> هذا الملف هو المرجع الوحيد المعتمد لحالة مشروع Primary Exam System. أي مستندات تاريخية أخرى تخضع للبانر التحذيري المرجعي.
> **تاريخ التحديث:** 30 أكتوبر 2026 | **المرحلة الحالية:** P0 (`001-source-of-truth`)

---

## 📊 1. جدول الحقيقة للملفات والأسطح التشغيلية (CodeVersion Ledger)

| الملف | حالة المستودع (Repo State) | حالة النشر (Published State) | الدليل (Evidence) | التاريخ | السطح (Surface) |
|---|---|---|---|---|---|
| `Code.gs` | tracked (محدث بحماية التوكن والترتيب) | منشور في المستودع (يتطلب نسخ لـ Apps Script) | `npm test` 43/43 PASS | 2026-10-30 | apps-script backend |
| `index.html` | tracked | منشور ويعمل حياً | HTTP 200 على GitHub Pages | 2026-10-30 | pages frontend |
| `Index.bundle.html` | tracked | حزمة مجمعة للنسخ والنشر | مُنشأ عبر `bundle.py` | 2026-10-30 | bundle |
| `.github/workflows/coligo-cloud-sync.yml` | tracked | مفعّل ويعمل آلياً كل ساعة | سجل Actions (Commit `7271ba6`) | 2026-10-30 | workflow |
| `coligo_manifest.json` | tracked | مفهرس ومحدث | 333 مادة، 230 تنزيل | 2026-10-30 | storage / metadata |

---

## 🛡️ 2. دفتر تدقيق إصلاحات 28 و30 أكتوبر (OctFixLedger)

| الإصلاح (Fix) | الحالة (State) | الدليل (Evidence) | التاريخ | الملاحظات (Notes) |
|---|---|---|---|---|
| توكنات مصادقة من الخادم (`ACCESS_TOK_*`) | **مثبّت** | `Code.gs:2068` و `tests/server.test.js` | 2026-10-30 | انتهاء عصر التوكنات الثابتة، التوكن يحمل Claims مشفرة ومؤقتة. |
| إخفاء وحظر PINs في الكود الصريح | **مثبّت** | مطابقة `FALLBACK_HASH_*` و `SHA-256` | 2026-10-30 | لا توجد أرقام PIN مكشوفة في كود الواجهة أو السيرفر. |
| قاعدة الهروب من قطع النصوص `\/\/` | **مثبّت** | `bundle.py:15` | 2026-10-30 | المعالج الآلي يحمي أي مسار `//` من القطع في بيئة Apps Script. |
| فحص تطابق الطالب مع الجلسة قبل التوكن | **مثبّت** | `Code.gs:1751` و `server.test.js:303` | 2026-10-30 | التحقق من `STUDENT_MISMATCH` قبل رفض التوكن لمنع التداخل بين الطالبين. |
| شريط الأخطاء الاختياري | **غير مطلوب** | قرار المعمارية D5 | 2026-10-30 | تم استبداله بمعالجة الأخطاء المدمجة داخل النوافذ التفاعلية. |

---

## 🧪 3. خط الأساس للاختبارات المؤتمتة (Baseline Test Ledger)

- **الأمر المنفذ:** `npm test`
- **التاريخ:** 2026-10-30
- **النتيجة الموثقة:** **43/43 PASS (100% نجاح كامل)**
  - `tests/normalizeAnswer.test.js`: 10/10 PASS
  - `tests/attemptState.test.js`: 8/8 PASS
  - `tests/scoring.test.js`: 5/5 PASS
  - `tests/cumulative.test.js`: 2/2 PASS
  - `tests/server.test.js`: 18/18 PASS
- **الملف المرجعي:** [`specs/001-source-of-truth/baseline-tests-2026-10-30.txt`](file:///C:/Users/co0ob/Projects/primary-exam-system/specs/001-source-of-truth/baseline-tests-2026-10-30.txt)

---

## 🔑 4. مدخلات المالك المطلوبة للمرحلة التالية P1 (Owner Inputs)

للانتقال فوراً إلى المرحلة **P1: `002-live-integration`** قبل انتهاء صلاحية جلسة Coligo في **4 نوفمبر 2026**، يلزم توفير:
1. `COLIGO_PASSWORD` (لتحديث الـ Secret في GitHub Actions لضمان استمرار السحب الآلي).
2. رابط نشر Web App الحالي (`https://script.google.com/macros/s/.../exec`) لإضافته إلى `GAS_WEBHOOK_URL`.
