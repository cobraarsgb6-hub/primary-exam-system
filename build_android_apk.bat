@echo off
chcp 65001 >nul
title بناء تطبيق منارة الإيمان للأندرويد (Manaret El-Eman APK Builder)
echo ===============================================================================
echo 🚀 منارة الإيمان - بناء تطبيق الأندرويد للامتحانات (APK Builder)
echo ===============================================================================
echo.

cd /d "%~dp0\android"

echo ⏳ جارٍ تحديث ملفات المنظومة داخل التطبيق (Syncing Assets)...
if not exist "app\src\main\assets\www" mkdir "app\src\main\assets\www"
python "..\bundle.py" >nul 2>&1
if exist "..\Index.bundle.html" (
    copy /y "..\Index.bundle.html" "app\src\main\assets\www\index.html" >nul
) else (
    copy /y "..\Index.html" "app\src\main\assets\www\index.html" >nul
)
if exist "..\Mostafa_Corel_Workspace.html" (
    copy /y "..\Mostafa_Corel_Workspace.html" "app\src\main\assets\www\Mostafa_Corel_Workspace.html" >nul
)
echo [OK] تم تجميع وتحديث واجهة المنظومة للأندرويد بنجاح.
echo.

echo 🔍 جارٍ التحقق من بيئة Gradle و Android SDK...
where gradlew >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] تم العثور على محرك Gradle. جارٍ بناء الـ APK...
    call gradlew assembleDebug
    goto FINISH
)

where gradle >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] تم العثور على محرك Gradle. جارٍ بناء الـ APK...
    call gradle assembleDebug
    goto FINISH
)

echo.
echo ⚠️ ملاحظة هامة:
echo لم يتم العثور على Gradle أو Android Studio مثبتين في المسار الافتراضي للويندوز.
echo.
echo 📌 لديك خياران فوريان لبناء الـ APK:
echo 1) فتح مجلد "primary-exam-system\android" في Android Studio والضغط على "Build APK".
echo 2) رفع المشروع على GitHub، حيث تم تجهيز GitHub Actions تلقائياً لبناء الـ APK وتحميله فوراً.
echo.
pause
exit /b 0

:FINISH
echo.
echo ===============================================================================
echo 🎉 تم بناء تطبيق الـ APK بنجاح!
echo مسار الملف: android\app\build\outputs\apk\debug\app-debug.apk
echo ===============================================================================
echo.
pause
