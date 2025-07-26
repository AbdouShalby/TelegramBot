@echo off
title Company Projects Bot
color 0A

echo ========================================
echo    Company Projects Bot
echo ========================================
echo.
echo [%time%] Starting bot...
echo.

:: التحقق من وجود البوت شغال
echo [%time%] Checking for existing bot instances...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Company Projects Bot*" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] Found existing bot instance, stopping it...
    taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Company Projects Bot*" >nul 2>&1
    timeout /t 3 /nobreak >nul
)

:: إيقاف جميع نسخ pythonw.exe
echo [%time%] Stopping background Python processes...
taskkill /F /IM pythonw.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: التحقق من وجود ملف البوت
if not exist "bot_new.py" (
    echo [%time%] ERROR: bot_new.py not found!
    echo [%time%] Please make sure you're in the correct directory.
    pause
    exit /b 1
)

:: التحقق من وجود قاعدة البيانات
if not exist "projects_new.json" (
    echo [%time%] ERROR: projects_new.json not found!
    echo [%time%] Please make sure all files are present.
    pause
    exit /b 1
)

:: تشغيل البوت
echo [%time%] Starting bot...
echo [%time%] Bot will run in console mode...
echo.

:: تشغيل البوت في النافذة الحالية
python bot_new.py

echo.
echo [%time%] Bot stopped. Press any key to exit...
pause 