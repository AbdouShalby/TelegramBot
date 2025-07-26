@echo off
title Stop Company Projects Bot
color 0C

echo ========================================
echo    Stop Company Projects Bot
echo ========================================
echo.
echo [%time%] Stopping bot instances...
echo.

:: إيقاف البوت الرئيسي
echo [%time%] Stopping main bot process...
taskkill /F /FI "WINDOWTITLE eq Company Projects Bot*" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ Main bot stopped successfully!
) else (
    echo [%time%] ℹ️ No main bot process found.
)

:: إيقاف جميع نسخ pythonw.exe
echo [%time%] Stopping background Python processes...
taskkill /F /IM pythonw.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ Background processes stopped!
) else (
    echo [%time%] ℹ️ No background processes found.
)

:: إيقاف جميع نسخ python.exe (للأمان)
echo [%time%] Checking for any remaining Python processes...
taskkill /F /IM python.exe >nul 2>&1

:: التحقق من إيقاف جميع النسخ
timeout /t 2 /nobreak >nul
tasklist /FI "IMAGENAME eq python.exe" | findstr "python.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ⚠️ Some Python processes may still be running.
    echo [%time%] You can check manually with: tasklist /FI "IMAGENAME eq python.exe"
) else (
    echo [%time%] ✅ All bot processes stopped successfully!
)

echo.
echo [%time%] Bot stop operation completed.
echo [%time%] Press any key to exit...
pause >nul 