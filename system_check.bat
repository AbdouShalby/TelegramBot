@echo off
title System Check - Telegram Bot
color 0B

echo ========================================
echo    System Check - Telegram Bot
echo ========================================
echo.
echo [%time%] Starting comprehensive system check...
echo.

:: فحص Python
echo [%time%] 1. Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ Python: 
    python --version
    for /f "tokens=*" %%i in ('where python') do echo [%time%]    Path: %%i
) else (
    echo [%time%] ❌ Python: NOT FOUND
    set "errors=1"
)

echo.

:: فحص pip
echo [%time%] 2. Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ pip: 
    pip --version
) else (
    echo [%time%] ❌ pip: NOT FOUND
    set "errors=1"
)

echo.

:: فحص المكتبات المطلوبة
echo [%time%] 3. Checking required packages...
set "packages=python-telegram-bot python-dotenv APScheduler pytz nest-asyncio"

for %%p in (%packages%) do (
    pip show %%p >nul 2>&1
    if !errorlevel! equ 0 (
        echo [%time%] ✅ %%p: INSTALLED
    ) else (
        echo [%time%] ❌ %%p: NOT INSTALLED
        set "errors=1"
    )
)

echo.

:: فحص الملفات المطلوبة
echo [%time%] 4. Checking required files...
set "files=bot_new.py config.py database.py formatters.py user_context.py projects_new.json requirements.txt"

for %%f in (%files%) do (
    if exist "%%f" (
        echo [%time%] ✅ %%f: EXISTS
    ) else (
        echo [%time%] ❌ %%f: MISSING
        set "errors=1"
    )
)

echo.

:: فحص ملفات التشغيل
echo [%time%] 5. Checking batch files...
set "batch_files=run_bot_server.bat stop_bot_server.bat check_bot_status.bat"

for %%b in (%batch_files%) do (
    if exist "%%b" (
        echo [%time%] ✅ %%b: EXISTS
    ) else (
        echo [%time%] ❌ %%b: MISSING
        set "errors=1"
    )
)

echo.

:: فحص قاعدة البيانات
echo [%time%] 6. Validating database...
if exist "projects_new.json" (
    python -c "import json; json.load(open('projects_new.json', 'r', encoding='utf-8')); print('OK')" >nul 2>&1
    if !errorlevel! equ 0 (
        echo [%time%] ✅ Database JSON: VALID
        
        :: عرض إحصائيات قاعدة البيانات
        for /f %%i in ('python -c "import json; data=json.load(open('projects_new.json', 'r', encoding='utf-8')); print(len(data.get('categories', {})))"') do (
            echo [%time%]    Categories: %%i
        )
    ) else (
        echo [%time%] ❌ Database JSON: INVALID
        set "errors=1"
    )
) else (
    echo [%time%] ❌ Database: FILE MISSING
    set "errors=1"
)

echo.

:: فحص الشبكة
echo [%time%] 7. Checking network connectivity...
ping -n 1 google.com >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ Internet: CONNECTED
) else (
    echo [%time%] ❌ Internet: NO CONNECTION
    set "errors=1"
)

ping -n 1 api.telegram.org >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ Telegram API: REACHABLE
) else (
    echo [%time%] ⚠️ Telegram API: NOT REACHABLE (may need VPN)
)

echo.

:: فحص العمليات الجارية
echo [%time%] 8. Checking running processes...
tasklist /FI "IMAGENAME eq python.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ⚠️ Python processes found:
    tasklist /FI "IMAGENAME eq python.exe" /FO TABLE
) else (
    echo [%time%] ✅ No Python processes running
)

tasklist /FI "IMAGENAME eq pythonw.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ⚠️ Background Python processes found:
    tasklist /FI "IMAGENAME eq pythonw.exe" /FO TABLE
) else (
    echo [%time%] ✅ No background Python processes running
)

echo.

:: فحص الذاكرة والموارد
echo [%time%] 9. Checking system resources...
for /f "skip=1 tokens=4" %%i in ('wmic OS get TotalVisibleMemorySize /value') do (
    if not "%%i"=="" (
        set /a "total_ram=%%i/1024"
        echo [%time%] 💾 Total RAM: !total_ram! MB
    )
)

for /f "skip=1 tokens=4" %%i in ('wmic OS get FreePhysicalMemory /value') do (
    if not "%%i"=="" (
        set /a "free_ram=%%i/1024"
        echo [%time%] 💾 Free RAM: !free_ram! MB
    )
)

echo.

:: فحص المساحة المتاحة
echo [%time%] 10. Checking disk space...
for /f "tokens=3" %%i in ('dir /-c ^| find "bytes free"') do (
    echo [%time%] 💽 Free Space: %%i bytes
)

echo.

:: فحص Firewall
echo [%time%] 11. Checking Windows Firewall...
netsh advfirewall show allprofiles state >nul 2>&1
if %errorlevel% equ 0 (
    echo [%time%] ✅ Windows Firewall: ACCESSIBLE
    
    :: فحص قواعد Python
    netsh advfirewall firewall show rule name="Telegram Bot Python" >nul 2>&1
    if !errorlevel! equ 0 (
        echo [%time%] ✅ Python firewall rule: EXISTS
    ) else (
        echo [%time%] ⚠️ Python firewall rule: NOT FOUND
    )
) else (
    echo [%time%] ⚠️ Windows Firewall: CANNOT ACCESS
)

echo.

:: النتيجة النهائية
echo ========================================
if defined errors (
    echo    ❌ SYSTEM CHECK FAILED
    echo ========================================
    echo.
    echo [%time%] Some issues were found. Please fix them before running the bot.
    echo [%time%] Check the errors above and follow the installation guide.
) else (
    echo    ✅ SYSTEM CHECK PASSED
    echo ========================================
    echo.
    echo [%time%] All checks passed! The system is ready to run the bot.
    echo [%time%] You can now run: run_bot_server.bat
)

echo.
echo [%time%] System check completed.
echo [%time%] Press any key to exit...
pause >nul
