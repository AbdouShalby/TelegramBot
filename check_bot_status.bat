@echo off
title Check Bot Status
color 0B

echo ========================================
echo    Check Bot Status
echo ========================================
echo.
echo [%time%] Checking bot status...
echo.

:: فحص البوت الرئيسي
echo [%time%] Checking main bot process...
tasklist /FI "WINDOWTITLE eq Company Projects Bot*" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ Main bot is RUNNING
    echo [%time%] Process details:
    tasklist /FI "WINDOWTITLE eq Company Projects Bot*" /FO TABLE
) else (
    echo [%time%] ❌ Main bot is NOT RUNNING
)

echo.

:: فحص نسخ pythonw.exe
echo [%time%] Checking background Python processes...
tasklist /FI "IMAGENAME eq pythonw.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ⚠️ Found background Python processes:
    tasklist /FI "IMAGENAME eq pythonw.exe" /FO TABLE
) else (
    echo [%time%] ℹ️ No background Python processes found.
)

echo.

:: فحص جميع نسخ Python
echo [%time%] Checking all Python processes...
tasklist /FI "IMAGENAME eq python.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] 📋 All Python processes:
    tasklist /FI "IMAGENAME eq python.exe" /FO TABLE
) else (
    echo [%time%] ℹ️ No Python processes found.
)

echo.
echo [%time%] Status check completed.
echo [%time%] Press any key to exit...
pause >nul 