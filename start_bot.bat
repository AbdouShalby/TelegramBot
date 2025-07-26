@echo off
chcp 65001 >nul
title بوت التيليجرام - مشاريع الشركة

echo 🤖 بوت التيليجرام - مشاريع الشركة
echo ================================
echo 📅 %date% - %time%
echo.

REM فحص Python
echo 🔍 فحص Python...
python --version >nul 2>&1
if not %errorlevel% == 0 (
    echo ❌ Python غير مثبت أو غير متاح
    echo 💡 شغل setup_bot.bat أولاً
    echo.
    pause
    exit /b 1
)

echo ✅ Python متوفر

REM فحص ملف .env
echo 🔍 فحص ملف الإعدادات...
if not exist ".env" (
    echo ❌ ملف .env غير موجود
    echo 💡 شغل setup_bot.bat أولاً
    echo.
    pause
    exit /b 1
)

REM فحص التوكن
findstr /C:"your_bot_token_here" .env >nul
if %errorlevel% == 0 (
    echo ⚠️  التوكن لم يتم تحديثه في ملف .env
    echo 💡 حدث التوكن أولاً ثم شغل البوت
    echo.
    start notepad .env
    pause
    exit /b 1
)

echo ✅ ملف الإعدادات صحيح

REM فحص قاعدة البيانات
echo 🔍 فحص قاعدة البيانات...
if not exist "projects_new.json" (
    echo ❌ قاعدة البيانات غير موجودة
    pause
    exit /b 1
)

echo ✅ قاعدة البيانات موجودة

REM فحص المكتبات
echo 🔍 فحص المكتبات...
python -c "import telegram, dotenv, apscheduler" >nul 2>&1
if not %errorlevel% == 0 (
    echo ❌ بعض المكتبات غير مثبتة
    echo 💡 شغل setup_bot.bat أولاً
    echo.
    pause
    exit /b 1
)

echo ✅ جميع المكتبات متوفرة

echo.
echo 🚀 تشغيل البوت...
echo ================================
echo 💡 لإيقاف البوت اضغط Ctrl+C
echo.

REM تشغيل البوت
python bot_new.py

REM في حالة إنهاء البوت
echo.
echo 🛑 تم إيقاف البوت
echo.
pause
