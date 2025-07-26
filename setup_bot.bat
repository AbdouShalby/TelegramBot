@echo off
chcp 65001 >nul
echo 🤖 إعداد بوت التيليجرام
echo ================================

REM فحص وجود Python
echo 🔍 فحص Python...
python --version >nul 2>&1
if not %errorlevel% == 0 (
    echo ❌ Python غير مثبت
    echo 💡 شغل ملف install_python.bat أولاً
    pause
    exit /b 1
)

echo ✅ Python متوفر
python --version

REM فحص ملف .env
echo.
echo 🔍 فحص ملف الإعدادات...
if not exist ".env" (
    if exist ".env.example" (
        echo 📋 إنشاء ملف .env من المثال...
        copy ".env.example" ".env" >nul
        echo ✅ تم إنشاء ملف .env
    ) else (
        echo 📝 إنشاء ملف .env جديد...
        echo BOT_TOKEN=your_bot_token_here > .env
        echo BOT_USERNAME=YourBotUsername >> .env
        echo BOT_NAME=اسم البوت >> .env
        echo DATABASE_FILE=projects_new.json >> .env
        echo LOG_LEVEL=INFO >> .env
        echo ✅ تم إنشاء ملف .env
    )
    
    echo.
    echo ⚠️  يرجى تحديث التوكن في ملف .env
    echo 1. افتح ملف .env
    echo 2. استبدل your_bot_token_here بالتوكن الحقيقي
    echo 3. احفظ الملف
    echo.
    echo 💡 للحصول على التوكن:
    echo 1. تحدث مع @BotFather في تيليجرام
    echo 2. أرسل /newbot
    echo 3. اتبع التعليمات
    echo 4. انسخ التوكن إلى ملف .env
    echo.
    
    REM فتح ملف .env للتحرير
    echo 📝 فتح ملف .env للتحرير...
    start notepad .env
    
    echo اضغط أي مفتاح بعد تحديث التوكن...
    pause >nul
) else (
    echo ✅ ملف .env موجود
)

REM فحص قاعدة البيانات
echo.
echo 🔍 فحص قاعدة البيانات...
if exist "projects_new.json" (
    echo ✅ قاعدة البيانات موجودة
) else (
    echo ❌ ملف قاعدة البيانات غير موجود
    echo تأكد من وجود ملف projects_new.json
    pause
    exit /b 1
)

REM تثبيت المكتبات
echo.
echo 📦 فحص وتثبيت المكتبات...
python -c "import telegram" >nul 2>&1
if not %errorlevel% == 0 (
    echo 📚 تثبيت المكتبات المطلوبة...
    python -m pip install -r requirements.txt
    if not %errorlevel% == 0 (
        echo ❌ فشل في تثبيت المكتبات
        echo جرب تشغيل install_python.bat
        pause
        exit /b 1
    )
)

echo ✅ جميع المكتبات مثبتة

echo.
echo 🎉 الإعداد مكتمل!
echo ================================
echo.
echo 🚀 لتشغيل البوت استخدم:
echo   start_bot.bat
echo.
echo 🔧 لإعادة الإعداد استخدم:
echo   setup_bot.bat
echo.
echo 📊 لفحص حالة البوت استخدم:
echo   check_bot_status.bat
echo.

pause
