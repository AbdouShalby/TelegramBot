@echo off
chcp 65001 >nul
echo 🐍 تثبيت Python على ويندوز
echo ================================

echo 🔍 فحص وجود Python...

REM فحص Python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python مثبت بالفعل
    python --version
    goto :install_packages
)

REM فحص winget
winget --version >nul 2>&1
if %errorlevel% == 0 (
    echo 📦 استخدام winget لتثبيت Python...
    winget install Python.Python.3 --accept-source-agreements --accept-package-agreements
    if %errorlevel% == 0 (
        echo ✅ تم تثبيت Python بنجاح
        goto :refresh_path
    )
)

REM فحص Chocolatey
choco --version >nul 2>&1
if %errorlevel% == 0 (
    echo 🍫 استخدام Chocolatey لتثبيت Python...
    choco install python -y
    if %errorlevel% == 0 (
        echo ✅ تم تثبيت Python بنجاح
        goto :refresh_path
    )
)

REM إذا فشل التثبيت التلقائي
echo ❌ فشل التثبيت التلقائي
echo.
echo 💡 يرجى تثبيت Python يدوياً:
echo 1. اذهب إلى: https://www.python.org/downloads/
echo 2. حمل أحدث إصدار Python
echo 3. شغل الملف المحمل
echo 4. ✅ تأكد من تفعيل "Add Python to PATH"
echo 5. اضغط Install
echo.
echo بعد التثبيت، شغل هذا الملف مرة أخرى
goto :end

:refresh_path
echo 🔄 تحديث متغيرات البيئة...
call refreshenv >nul 2>&1
timeout /t 3 >nul

:install_packages
echo.
echo 📦 تثبيت مكتبات البوت...
echo ================================

REM تحديث pip
echo 🔧 تحديث pip...
python -m pip install --upgrade pip

REM تثبيت المكتبات
echo 📚 تثبيت المكتبات المطلوبة...
python -m pip install python-telegram-bot==20.7
python -m pip install python-dotenv==1.0.0
python -m pip install APScheduler==3.10.4
python -m pip install pytz==2023.3
python -m pip install nest-asyncio==1.5.8

if %errorlevel% == 0 (
    echo ✅ تم تثبيت جميع المكتبات بنجاح
) else (
    echo ❌ حدث خطأ في تثبيت المكتبات
    echo جرب تشغيل: pip install -r requirements.txt
)

echo.
echo 🎉 التثبيت مكتمل!
echo الآن يمكنك تشغيل البوت باستخدام: start_bot.bat

:end
echo.
pause
