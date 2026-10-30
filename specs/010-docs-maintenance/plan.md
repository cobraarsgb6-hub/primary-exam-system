# خطة التنفيذ للمرحلة P9: التوثيق والصيانة (010-docs-maintenance)

## 1. الهيكلية المعمارية للوثائق الموحدة
- **الحالة الراهنة الحية:** `CURRENT_STATUS_AR.md`
- **خارطة الطريق الرسمية:** `ROADMAP_SPECKIT_AR.md`
- **المواصفات التنفيذية المنفذة:** مجلد `specs/001-*` إلى `specs/010-*`
- **الدليل الإرشادي التشغيلي الرئيسي:** `README.md`
- **دليل الإعداد والأمان:** `SECURITY_SETUP.md` و`SETUP_GUIDE.md`

## 2. قائمة الملفات التي سيتم وسمها كأرشيف تاريخي
تطبيق الترويسة التنبيهية القياسية:
```markdown
> [!CAUTION]
> **مستند تاريخي غير نشط (HISTORICAL ARCHIVE)**
> هذا الملف يمثل تقريرًا أو خطة مرحلية من فترات التطوير السابقة.
> **المرجع المعتمد الوحيد للحالة الراهنة:** [`CURRENT_STATUS_AR.md`](CURRENT_STATUS_AR.md)
> **خارطة الطريق الرسمية:** [`ROADMAP_SPECKIT_AR.md`](ROADMAP_SPECKIT_AR.md)
```
الملفات المستهدفة:
1. `CODEX_PROJECT_PLAN_REVIEW_AR.md`
2. `FIXES_APPLIED.md`
3. `FIX_PLAN.md`
4. `GLM_OPERATIONAL_PLAN.md`
5. `PEDAGOGICAL_DIAGNOSTIC_REPORT.md`
6. `PROJECT.md`
7. `PROJECT_COMPLETE_LIFECYCLE_DOSSIER.md`
8. `PROJECT_COMPREHENSIVE_AUDIT_REPORT.md`
9. `PROJECT_MASTER_DOCUMENTATION.md`
10. `PROJECT_MASTER_HISTORY_AND_AUDIT.md`
11. `PROJECT_REVIEW_AR.md`
12. `TEST_INFRA.md`
13. `TEST_READY.md`
14. `WEEKLY_MONTHLY_PLAN.md`

## 3. خطة تحديث `README.md`
- شرح شامل للنظام (طلاب، مواد، فئات، آليات التصحيح).
- توضيح دور وأسماء الملفات:
  - `Index.template.html`: القالب المصدري الرئيسي للواجهة.
  - `bundle.py`: سكريبت التجميع والدمج المستقل.
  - `Index.bundle.html`: الملف المجمّع لخادم Google Apps Script (HTML Service).
  - `Index.html`: الرابط المباشر لبيئة Apps Script.
  - `index.html`: النسخة المخصصة لـ GitHub Pages وتطبيق Android WebView المستقل.
- دليل التشغيل والاختبار الكامل.
- دليل استكشاف الأخطاء والأنماط الممنوعة (Pitfalls & Invariants).
- إدارة ومراقبة الرموز والحصص.

## 4. التحقق والاختبار
- اختبار سلامة التوثيق ووجود الترويسات.
- تشغيل اختبارات الوحدة واختبارات E2E للتأكد من عدم وجود أي تأثير جانبي.
