# 🏛️ وثيقة الحقيقة وسجل الحالة التشغيلية (Single Source of Truth)

> [!IMPORTANT]
> هذا الملف هو المرجع الوحيد المعتمد لحالة مشروع Primary Exam System. أي مستندات تاريخية أخرى تخضع للبانر التحذيري المرجعي.
> **تاريخ التحديث:** 30 أكتوبر 2026 | **المرحلة الحالية المكتملة:** P0 و P1 بنجاح كامل 100%

---

## 📊 1. جدول الحقيقة للملفات والأسطح التشغيلية (CodeVersion Ledger)

| الملف | حالة المستودع (Repo State) | حالة النشر (Published State) | الدليل (Evidence) | التاريخ | السطح (Surface) |
|---|---|---|---|---|---|
| `Code.gs` | tracked (محدث بحماية التوكن والترتيب وخاصية التهيئة) | منشور ومحدث في Apps Script | `npm test` 43/43 PASS + رد Webhook بـ 200 | 2026-10-30 | apps-script backend |
| `index.html` | tracked | منشور ويعمل حياً | HTTP 200 على GitHub Pages | 2026-10-30 | pages frontend |
| `Index.bundle.html` | tracked | حزمة مجمعة للنسخ والنشر | مُنشأ عبر `bundle.py` | 2026-10-30 | bundle |
| `.github/workflows/coligo-cloud-sync.yml` | tracked | مفعّل ويعمل آلياً كل ساعة | يدعم مرشحي كلمات السر المتعددة | 2026-10-30 | workflow |
| `coligo_manifest.json` | tracked | مفهرس ومحدث | 333 مادة، 123 تنزيل جديد، sheets_webhook: success | 2026-10-30 | storage / metadata |

---

## 🛡️ 2. دفتر تدقيق إصلاحات P0 و P1 (Audit Ledger)

| الإصلاح (Fix) | الحالة (State) | الدليل (Evidence) | التاريخ | الملاحظات (Notes) |
|---|---|---|---|---|
| توكنات مصادقة من الخادم (`ACCESS_TOK_*`) | **مثبّت** | `Code.gs:2068` و `tests/server.test.js` | 2026-10-30 | انتهاء عصر التوكنات الثابتة، التوكن يحمل Claims مشفرة ومؤقتة. |
| إخفاء وحظر PINs في الكود الصريح | **مثبّت** | مطابقة `FALLBACK_HASH_*` و `SHA-256` | 2026-10-30 | لا توجد أرقام PIN مكشوفة في كود الواجهة أو السيرفر. |
| قاعدة الهروب من قطع النصوص `\/\/` | **مثبّت** | `bundle.py:15` | 2026-10-30 | المعالج الآلي يحمي أي مسار `//` من القطع في بيئة Apps Script. |
| فحص تطابق الطالب مع الجلسة قبل التوكن | **مثبّت** | `Code.gs:1751` و `server.test.js:303` | 2026-10-30 | التحقق من `STUDENT_MISMATCH` قبل رفض التوكن لمنع التداخل بين الطالبين. |
| مصادقة كوليجو الحية التلقائية | **مثبّت** | `cloud_coligo_sync.py` لايف | 2026-10-30 | دخول ناجح بحساب الأب وسحب مواد علي (G5) ومصطفى (G6). |
| تكامل Webhook جوجل شيت الحي | **مثبّت** | `coligo_manifest.json` | 2026-10-30 | رد الخادم بـ `success: true` وتأكيد التسجيل في Google Sheets. |

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

## 🚀 4. نتائج المزامنة الحية E2E (Live Sync Verification)

* **وقت التشغيل:** 2026-10-30 18:05:54
* **طريقة المصادقة:** `auth_mode = credentials` (عبر `ahmed.ibrahim144` و `dbbfd0`)
* **صلاحية الرمز:** صالح حتى `2026-11-09 10:05 UTC` ويتجدد آلياً عند كل تشغيل.
* **إجمالي المواد المفهرسة:** 333 مادة عبر 20 مادة دراسية لعلي ومصطفى.
* **الملفات المحفوظة حديثاً:** 123 ملف ومستند وعرض تقديمي وفيديو.
* **إشارات الواجبات:** 25 إشعار وواجب مفهرس.
* **تأكيد جوجل شيت:** `sheets_webhook_status = success` (تم التسجيل بنجاح تام).

---

## 🎯 5. الخطوة التالية (Next Phase: P2)

* **المرحلة التالية:** `003-security-privacy`
* **الهدف:** تعزيز أمان المتصفح وتأمين مسارات المواد التعليمية وإخفاء روابط المصدر المباشرة وضمان خصوصية بيانات الطالبين.
