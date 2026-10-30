# Feature Specification: 002-live-integration

**Feature Directory**: `specs/002-live-integration`
**Created**: 2026-10-30
**Status**: Ready for Owner Inputs & Plan Execution
**Priority**: CRITICAL (Token Expiry Risk: 2026-11-04)

---

## 🎯 1. Executive Summary & Objective

إغلاق حلقة التكامل السحابي الحية (End-to-End Live Integration) بين:
1. **Coligo Portal Ingestion**: سحب التحديثات والدروس والواجبات والمواد التعليمية آلياً.
2. **GitHub Actions**: تشغيل المزامنة 24/7 كل ساعة عبر سير العمل (`coligo-cloud-sync.yml`).
3. **Google Apps Script Webhook**: استقبال إشارات المزامنة والنتائج والواجبات على سيرفر Apps Script.
4. **Google Sheets Relational Database**: تخزين النتائج الرسمية في جدول `Submissions` بنتائج الـ 11 عموداً، ونتائج التدريبات الحرة في `External_Practice_Results`.

---

## 👥 2. User Scenarios & Acceptance Criteria

### User Story 1: Coligo Scheduled Autonomous Sync (Priority: P1)
- **السيناريو:** يعمل سير العمل في GitHub Actions كل ساعة، ويسحب الدروس والواجبات والمواد لـ Ali (Year 5) و Mostafa (Grade 6).
- **معيار القبول:** تسجيل `auth_mode` في `coligo_manifest.json`، وتسجيل رابط تشغيل (Action Run URL) ناجح دون أخطاء مصادقة، مع خطة صريحة لتجديد الجلسة بعد 4 نوفمبر 2026.

### User Story 2: Live GAS Webhook & Sheets Ingestion (Priority: P1)
- **السيناريو:** عند انتهاء سحب Coligo، يرسل السكربت إشارة Webhook موثقة بـ `SYNC_SECRET` إلى رابط Web App في Apps Script.
- **معيار القبول:** تحديث جدول `Coligo_Hub` و `Homework_Status` في Google Sheets بنجاح، وظهور `sheets_webhook_status: success` داخل المانيفست.

### User Story 3: Authentic End-to-End Submissions (Priority: P1)
- **السيناريو:** يقوم الطالب بإجراء امتحان عبر المنصة، ويتم تصحيحه خادمياً في `Code.gs`، وتصل النتيجة الرسمية إلى Google Sheets.
- **معيار القبول:** تسجيل صف حقيقي في جدول `Submissions` يحتوي كافة البيانات الرسمية والدرجة المعتمدة، مع عزل تدريبات الدروس في جدول `External_Practice_Results`.

### User Story 4: Direct Deep-Link Exam Routing (Priority: P2)
- **السيناريو:** فتح رابط الامتحان من لوحة التحكم أو الرسائل بصيغة `?student=ali&exam=EX_Y5_ENG_ADV01`.
- **معيار القبول:** فتح شاشة الامتحان المحددة مباشرة للطالب المحدد داخل بيئة Apps Script دون التوقف عند الشاشة الرئيسية.

---

## 🔐 3. Required Owner Inputs & Setup Checklist

> [!IMPORTANT]
> هذه المدخلات مطلوبة لإتمام تشغيل الربط السحابي:

- [ ] **1. `COLIGO_PASSWORD`**: كلمة سر حساب Coligo لتحديث GitHub Repository Secret.
- [ ] **2. `GAS_WEBHOOK_URL`**: الرابط الحالي المنشور لتطبيق Google Apps Script Web App (ينتهي بـ `/exec`).
- [ ] **3. `SYNC_SECRET`**: الرمز السري المشترك بين GitHub Actions و Script Properties في Google Apps Script.
