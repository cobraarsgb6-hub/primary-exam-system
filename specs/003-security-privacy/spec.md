# Feature Specification: 003-security-privacy

**Feature Directory**: `specs/003-security-privacy`
**Status**: In Progress | Phase P2
**Created**: 2026-10-30
**Priority**: HIGH (Security & Children Privacy Invariant)

---

## 🎯 1. Executive Summary & Objective

تحصين شامل لكافة نقاط الاتصال (RPC & Endpoints) وسياسة الخصوصية لطالبي المنظومة (علي ومصطفى):
1. **Server-Side Authorization Invariant**: لا تُنفَّذ أي عملية حساسة (تصحيح، موافقة، تعديل بنك الأسئلة، تهيئة الجداول، جلب المهام) إلا بعد التحقق الخادمي الصارم من التوكن المشفر (`ACCESS_TOK_*` للطلاب و `ADMIN_TOK_*` لولي الأمر).
2. **Children Privacy & Isolation**: عزل تام بين بيانات علي ومصطفى، ومنع أي طالب من الاطلاع على نتائج أو أسئلة أو مهام الطالب الآخر.
3. **Public Exposure Lockdown**: حظر نشر أي مفاتيح إجابات رسمية أو روابط CDN مشفرة خاصة أو سجلات درجات في صفحات GitHub Pages أو الكود المصدري للواجهة.
4. **Entrance & PIN Security**: اعتماد نموذج الدخول المحمي برمز PIN مشفر بـ SHA-256 و Salt المنظومة (`1990` لولي الأمر، `2016` لعلي، `2014` لمصطفى) مع تقييد معدل المحاولات (Rate Limiting: 5 محاولات يتبعها حظر 10 دقائق).

---

## 👥 2. User Scenarios & Acceptance Criteria

### User Story 1: Rejection of Forged & Expired Tokens (Priority: P0)
- **السيناريو:** يحاول متسلل أو عميل متصفح إرسال توكن منتهي الصلاحية أو توكن تم تعديل حمولته أو توقيع وهمي.
- **معيار القبول:** رفض الطلب فوراً من الخادم دون قراءة الجداول أو تنفيذ أي استعلام، وإرجاع كود `UNAUTHORIZED` أو `EXPIRED_TOKEN`.

### User Story 2: Strict Student-to-Student Data Isolation (Priority: P0)
- **السيناريو:** طالب يحمل توكن معتمد لـ "علي" يحاول طلب مهام أو نتائج أو بدء جلسة امتحان باسم "مصطفى".
- **معيار القبول:** رفض الطلب خادمياً بكود `STUDENT_MISMATCH`، وحظر الوصول إلى بيانات الطالب الآخر.

### User Story 3: Admin Operation Protection (Priority: P0)
- **السيناريو:** استدعاء أي دالة إدارية (`approveRetakeRequest`, `setupDatabase`, `seedCompleteQuestionBank`, `syncColigoOnline`, `createWeeklyExam`) بدون توكن أدمن صالح.
- **معيار القبول:** رفض فوري ومطلق مع عدم إجراء أي تعديل على جداول Google Sheets.

### User Story 4: No Answer Keys on Client-Side (Priority: P0)
- **السيناريو:** فحص كود المتصفح والشبكة قبل وأثناء الامتحان.
- **معيار القبول:** إرجاع حقول الأسئلة العامة فقط (`id, grade, subject, unit, text, type, options, points, passage`) عبر `publicQuestions_`؛ حظر وصول `correctAnswer` و `explanation` إلا بعد التسليم والتصحيح الخادمي المعتمد.

---

## 🔒 3. Public Exposure Policy & Boundaries

| العنصر | الحالة | الموقع المعتمد | الحماية المفروضة |
| :--- | :--- | :--- | :--- |
| **رموز PIN** | مشفرة | Script Properties فقط | SHA-256 + Salt؛ لا وجود لأرقام صريحة في الكود |
| **إجابات الامتحانات الرسمية** | سرية خادمية | `Question_Bank` في Google Sheets | لا ترسل للمتصفح أبداً قبل التصحيح |
| **بيانات الدخول لكوليجو** | أسرار مشفرة | GitHub Secrets فقط | لا تُكتب في أي ملف بالمستودع |
| **كتالوج كوليجو العام** | عام آمن | `resources/coligo/coligo_catalog.json` | عناوين المواد وروابط الملفات العامة فقط بدون سجلات درجات |
