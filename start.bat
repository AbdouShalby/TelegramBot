@echo off
chcp 65001 >nul
title Telegram Projects Bot

echo 🤖 بوت مشاريع التيليجرام
echo ========================

echo 🔍 التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت
    echo يرجى تثبيت Python 3.8+ من: https://python.org
    pause
    exit /b 1
)

echo ✅ Python متوفر

echo 📦 تثبيت المتطلبات...
python -m pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ❌ فشل في تثبيت المتطلبات
    echo جرب تشغيل: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ تم تثبيت المتطلبات

echo 🚀 تشغيل البوت...
python start_bot.py

pause
