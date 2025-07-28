@echo off
title Telegram Bot Installation - Windows Server
color 0A

echo ========================================
echo    Telegram Bot Installation Script
echo ========================================
echo.
echo [%time%] Starting installation process...
echo.

:: التحقق من صلاحيات المدير
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [%time%] ERROR: This script requires Administrator privileges!
    echo [%time%] Please run as Administrator.
    pause
    exit /b 1
)

:: التحقق من وجود Python
echo [%time%] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [%time%] ERROR: Python is not installed or not in PATH!
    echo [%time%] Please install Python 3.11+ first.
    echo [%time%] Download from: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo [%time%] ✅ Python found:
    python --version
)

:: التحقق من وجود pip
echo [%time%] Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [%time%] ERROR: pip is not available!
    echo [%time%] Please reinstall Python with pip included.
    pause
    exit /b 1
) else (
    echo [%time%] ✅ pip found:
    pip --version
)

echo.

:: التحقق من وجود الملفات المطلوبة
echo [%time%] Checking required files...
set "missing_files="

if not exist "bot_new.py" (
    set "missing_files=%missing_files% bot_new.py"
)
if not exist "config.py" (
    set "missing_files=%missing_files% config.py"
)
if not exist "database.py" (
    set "missing_files=%missing_files% database.py"
)
if not exist "formatters.py" (
    set "missing_files=%missing_files% formatters.py"
)
if not exist "user_context.py" (
    set "missing_files=%missing_files% user_context.py"
)
if not exist "projects_new.json" (
    set "missing_files=%missing_files% projects_new.json"
)
if not exist "requirements.txt" (
    set "missing_files=%missing_files% requirements.txt"
)

if not "%missing_files%"=="" (
    echo [%time%] ERROR: Missing required files:%missing_files%
    echo [%time%] Please make sure all files are in the current directory.
    pause
    exit /b 1
) else (
    echo [%time%] ✅ All required files found.
)

echo.

:: تثبيت المتطلبات
echo [%time%] Installing Python requirements...
echo [%time%] This may take a few minutes...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [%time%] ERROR: Failed to install requirements!
    echo [%time%] Trying alternative installation method...
    
    echo [%time%] Installing packages individually...
    pip install python-telegram-bot==20.7
    pip install python-dotenv==1.0.0
    pip install APScheduler==3.10.4
    pip install pytz==2023.3
    pip install nest-asyncio==1.5.8
    
    if %errorlevel% neq 0 (
        echo [%time%] ERROR: Failed to install required packages!
        pause
        exit /b 1
    )
)

echo [%time%] ✅ Requirements installed successfully!
echo.

:: التحقق من صحة قاعدة البيانات
echo [%time%] Validating database file...
python -c "import json; json.load(open('projects_new.json', 'r', encoding='utf-8')); print('Database OK')" >nul 2>&1
if %errorlevel% neq 0 (
    echo [%time%] ERROR: Database file (projects_new.json) is invalid!
    echo [%time%] Please check the JSON structure.
    pause
    exit /b 1
) else (
    echo [%time%] ✅ Database file is valid.
)

echo.

:: إعداد Firewall (اختياري)
echo [%time%] Configuring Windows Firewall...
for /f "tokens=*" %%i in ('where python') do set "python_path=%%i"
if not "%python_path%"=="" (
    netsh advfirewall firewall add rule name="Telegram Bot Python" dir=out action=allow program="%python_path%" >nul 2>&1
    echo [%time%] ✅ Firewall rule added for Python.
)

for /f "tokens=*" %%i in ('where pythonw') do set "pythonw_path=%%i"
if not "%pythonw_path%"=="" (
    netsh advfirewall firewall add rule name="Telegram Bot Python Background" dir=out action=allow program="%pythonw_path%" >nul 2>&1
    echo [%time%] ✅ Firewall rule added for Python background.
)

echo.

:: اختبار تشغيل البوت
echo [%time%] Testing bot startup...
echo [%time%] Starting bot for 10 seconds to test...
timeout /t 2 /nobreak >nul

start "Bot Test" /MIN python bot_new.py
timeout /t 10 /nobreak >nul

tasklist /FI "WINDOWTITLE eq Bot Test" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ Bot started successfully!
    taskkill /F /FI "WINDOWTITLE eq Bot Test" >nul 2>&1
    echo [%time%] Test completed.
) else (
    echo [%time%] ⚠️ Bot test inconclusive. Check manually.
)

echo.

:: إنشاء مجلد للسجلات والنسخ الاحتياطية
echo [%time%] Creating directories...
if not exist "logs" mkdir logs
if not exist "backup" mkdir backup
echo [%time%] ✅ Directories created.

echo.

:: عرض معلومات التشغيل
echo ========================================
echo    Installation Completed Successfully!
echo ========================================
echo.
echo 🚀 Bot is ready to run!
echo.
echo 📋 Available commands:
echo   - run_bot_server.bat     : Start bot in server mode
echo   - stop_bot_server.bat    : Stop bot
echo   - check_bot_status.bat   : Check bot status
echo.
echo 📊 Files created:
echo   - logs/                  : Log files directory
echo   - backup/                : Backup files directory
echo.
echo 🔧 Next steps:
echo   1. Run: run_bot_server.bat
echo   2. Check status: check_bot_status.bat
echo   3. Monitor logs: type bot_log_YYYYMMDD.txt
echo.
echo ⚠️ Important:
echo   - Keep this directory secure
echo   - Monitor bot logs regularly
echo   - Create regular backups
echo.
echo [%time%] Installation completed successfully!
echo [%time%] Press any key to exit...
pause >nul
