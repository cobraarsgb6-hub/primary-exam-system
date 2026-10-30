# خطة التنفيذ: مشغل الفيديو المعزول (011-isolated-video-player)

## 1. الهيكلية المعمارية لمشغل الفيديو المعزول
- **المكون البصري:** داخل `Index.template.html` (نافذة `video-modal`):
  - استبدال الـ iframe الخام بمكون متكامل `isolated-player-container`.
  - طبقة درع الحماية الشفاف: `isolated-player-shield` بنظام `position: absolute; inset: 0; pointer-events: auto; z-index: 10;`.
  - شاشة الإنجاز والاحتفال: `isolated-player-celebration` بنظام `z-index: 20; display: none;`.
  - شريط التحكم المخصص للمنصة: `isolated-player-controls` مثبت أسفل الفيديو مباشرة.
- **التنسيقات والأنماط (CSS):** داخل `Styles.html`:
  - أنماط شريط التحكم (أزرار التشغيل، التقديم، شريط التمرير، عداد الوقت).
  - أنماط طبقة الدرع الشفافة وطبقة شاشة الإنجاز.
- **المنطق البرمجي (JavaScript):** داخل `HubData.js.html`:
  - بناء كائن إدارة مشغل الفيديو `IsolatedVideoPlayer`.
  - إدارة دورة حياة YouTube IFrame API (`onYouTubeIframeAPIReady`, `YT.Player`).
  - عداد المراقبة الزمني التلقائي (Ticker Interval كل 250ms) لكشف وصول الفيديو إلى `duration - 2`.
  - دوال التحكم: `togglePlay()`, `seekRelative(seconds)`, `seekTo(percent)`, `setVolume(val)`, `replayVideo()`.
  - دالة `openVideoModal(videoId, title)`:
    - فحص وجود المعرّف وصحته؛ إذا كان فارغاً يتم إظهار بطاقة الفراغ الأنيقة دون تشغيل أي iframe.
    - تهيئة المشغل المعزول بـ `youtube-nocookie.com`.
    - ربط زري الإنجاز بـ المعمل التفاعلي وامتحان التدريب.

## 2. مصفوفة التحقق والاختبار
- إنشاء `tests/isolatedVideoPlayer.test.js`:
  - التحقق من تكوين الرابط `youtube-nocookie.com` والمعاملات الإلزامية (`controls=0`, `modestbranding=1`, `enablejsapi=1`, `rel=0`).
  - التحقق من وجود درع الحماية الشفاف المانع للنقر.
  - التحقق من منطق الاقتطاع قبل ثانيتين من النهاية والانتقال لشاشة الإنجاز.
  - التحقق من بطاقة الفراغ عند غياب الفيديو وعدم تحميل فيديوهات وهمية.
- تشغيل `bundle.py` لتحديث الحزم ومزامنة `Index.bundle.html` و `index.html`.
- تشغيل `npm test` للتأكد من نجاح جميع الاختبارات.
