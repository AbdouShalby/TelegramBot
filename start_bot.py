#!/usr/bin/env python3
"""
🤖 Telegram Projects Bot Starter
مشغل بوت مشاريع التيليجرام
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """التحقق من المتطلبات"""
    print("🔍 التحقق من المتطلبات...")
    
    # التحقق من Python
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ مطلوب. الإصدار الحالي: {sys.version}")
        return False
    
    # التحقق من الملفات المطلوبة
    required_files = [
        'bot_new.py',
        'config.py', 
        'database.py',
        'formatters.py',
        'projects_new.json',
        'requirements.txt'
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ الملف المطلوب غير موجود: {file}")
            return False
    
    # التحقق من ملف .env
    if not Path('.env').exists():
        print("⚠️ ملف .env غير موجود")
        create_env = input("هل تريد إنشاؤه؟ (y/n): ").lower().strip()
        if create_env == 'y':
            token = input("أدخل توكن البوت: ").strip()
            if token:
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(f"BOT_TOKEN={token}\n")
                print("✅ تم إنشاء ملف .env")
            else:
                print("❌ توكن البوت مطلوب")
                return False
        else:
            return False
    
    print("✅ جميع المتطلبات متوفرة")
    return True

def install_dependencies():
    """تثبيت التبعيات"""
    print("📦 تثبيت التبعيات...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ تم تثبيت التبعيات")
        return True
    except subprocess.CalledProcessError:
        print("❌ فشل في تثبيت التبعيات")
        print("جرب تشغيل: pip install -r requirements.txt")
        return False

def start_bot():
    """تشغيل البوت"""
    print("🚀 تشغيل البوت...")
    try:
        # تشغيل البوت
        subprocess.run([sys.executable, "bot_new.py"])
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت")
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")

def main():
    """الدالة الرئيسية"""
    print("🤖 مشغل بوت مشاريع التيليجرام")
    print("=" * 40)
    
    # التحقق من المتطلبات
    if not check_requirements():
        print("\n❌ فشل في التحقق من المتطلبات")
        input("اضغط Enter للخروج...")
        return
    
    # تثبيت التبعيات
    if not install_dependencies():
        print("\n❌ فشل في تثبيت التبعيات")
        input("اضغط Enter للخروج...")
        return
    
    # تشغيل البوت
    start_bot()

if __name__ == "__main__":
    main()
