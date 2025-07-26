@echo off
echo 🚀 تشغيل بوت التيليجرام...
echo ================================

REM محاولة تشغيل البوت بطرق مختلفة
echo 🔍 البحث عن Python...

REM الطريقة الأولى: python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ تم العثور على Python
    echo 🤖 تشغيل البوت...
    python bot_new.py
    goto :end
)

REM الطريقة الثانية: python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ تم العثور على Python3
    echo 🤖 تشغيل البوت...
    python3 bot_new.py
    goto :end
)

REM الطريقة الثالثة: py
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ تم العثور على py launcher
    echo 🤖 تشغيل البوت...
    py bot_new.py
    goto :end
)

REM إذا لم يتم العثور على Python
echo ❌ لم يتم العثور على Python!
echo.
echo 💡 الحلول المقترحة:
echo 1. تثبيت Python من: https://www.python.org/downloads/
echo 2. إضافة Python إلى PATH
echo 3. إعادة تشغيل Command Prompt
echo 4. استخدام Microsoft Store لتثبيت Python
echo.
echo 📝 للمساعدة، راجع ملف setup_environment.md
echo.

:end
echo.
echo 🛑 اضغط أي مفتاح للخروج...
pause >nul
