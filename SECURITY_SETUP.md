# متطلبات التشغيل الآلي والنشر

## GitHub Actions Secrets

أضف القيم التالية إلى `Settings → Secrets and variables → Actions` في المستودع:

- `COLIGO_USERNAME` و`COLIGO_PASSWORD`: تُستخدمان لإنشاء رمز جلسة جديد عند كل تشغيل للمزامنة، مع إعادة تسجيل الدخول مرة واحدة عند رفض الرمز بـ401.
- `GAS_WEBHOOK_URL`: رابط نشر Apps Script الذي ينتهي بـ`/exec`. الرابط ليس كلمة مرور؛ ستُضمّنه عملية بناء Pages داخل الصفحة العامة.
- `SYNC_SECRET`: قيمة عشوائية قوية مشتركة بين GitHub Actions وApps Script Property بنفس الاسم، لحماية ملخص المزامنة وسجل الواجبات.

لا تضف `COLIGO_TOKEN` ثابتًا؛ السكريبت يعتمد على تسجيل الدخول المتجدد ببيانات الحساب. لا تضع PIN أو سر المزامنة في كود الواجهة.

## Apps Script Properties

في Script Properties اضبط:

- `ADMIN_PIN_HASH`
- `ALI_PIN_HASH`
- `MOSTAFA_PIN_HASH`
- `SYNC_SECRET` (بنفس القيمة المخزنة في GitHub Actions)

تُستخدم PINs لمصادقة دخول الطلاب وولي الأمر. صفحة GitHub العامة تطلب PIN الطالب عند تسجيل نتيجة تدريب، وتخزن PIN في ذاكرة الصفحة فقط. نتائج الموقع العام تُحفظ في ورقة منفصلة باسم `External_Practice_Results` لأنها نتائج تدريب يرسلها المتصفح، وليست نتائج امتحان موثقة من محرك Apps Script.

## ما ينشره GitHub Pages

سير Pages مفعّل وينشر الموقع وكتالوج Coligo وملفات المواد الموجودة في مجلدي `resources/coligo/Ali` و`resources/coligo/Mostafa`. هذه الملفات والكتالوج متاحة لأي شخص يفتح الرابط؛ لا تعتبرها مخزنًا خاصًا. لا تنشر درجات، رموز دخول، أو روابط تنزيل موقعة/سرية فيها. مزامنة المواد قد تشمل ملفات مدرسية خاصة، فراجع صلاحية نشرها علنًا.

تعمل مزامنة Coligo كل ساعة عبر GitHub Actions، وتدفع التغييرات للفرع ثم تطلب تشغيل `deploy-pages.yml` مباشرة لأن دفع `GITHUB_TOKEN` لا يطلق سير عمل push آخر تلقائيًا. يعتمد استمرارها على صحة أسرار Actions، وصلاحية الحساب في Coligo، وحصص GitHub وGoogle.

## التفعيل والتحقق المطلوبان خارج الملفات

تعديل الملفات لا يضيف GitHub Secrets أو Apps Script Properties ولا ينشر نسخة Apps Script. أضف القيم المطلوبة، ثم نفّذ تشغيلًا يدويًا لسير `Autonomous Cloud Coligo Ingestion` وراجع نجاح خطوات السحب، التسجيل في Sheets، والنشر قبل الاعتماد على الجدول كل ساعة.
