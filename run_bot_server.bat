@echo off
title Company Projects Bot - Server Version
color 0A

echo ========================================
echo    Company Projects Bot - Server
echo ========================================
echo.
echo [%time%] Starting bot management...
echo.

:: التحقق من وجود البوت شغال
echo [%time%] Checking for existing bot instances...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Company Projects Bot*" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] Found existing bot instance, stopping it...
    taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Company Projects Bot*" >nul 2>&1
    timeout /t 3 /nobreak >nul
)

:: إيقاف جميع نسخ pythonw.exe (النسخ الخلفية)
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

:: تشغيل البوت مع عنوان مخصص
echo [%time%] Starting bot with server configuration...
echo [%time%] Bot will run in background mode...
echo.

:: تشغيل البوت في الخلفية مع عنوان مخصص
start "Company Projects Bot - Server" /MIN pythonw.exe bot_new.py

:: التحقق من نجاح التشغيل
timeout /t 5 /nobreak >nul
tasklist /FI "WINDOWTITLE eq Company Projects Bot*" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ Bot started successfully!
    echo [%time%] Bot is running in background mode.
    echo [%time%] Use 'tasklist /FI "WINDOWTITLE eq Company Projects Bot*"' to check status.
) else (
    echo [%time%] ❌ Failed to start bot!
    echo [%time%] Check logs for errors.
)

echo.
echo [%time%] Server bot management completed.
echo [%time%] Press any key to exit...
pause >nul 