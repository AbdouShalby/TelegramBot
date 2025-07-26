#!/usr/bin/env python3
"""
🤖 Telegram Bot Launcher
تشغيل بوت التيليجرام مع فحص المتطلبات
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """فحص إصدار Python"""
    if sys.version_info < (3, 8):
        print("❌ خطأ: يتطلب Python 3.8 أو أحدث")
        print(f"الإصدار الحالي: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_requirements():
    """فحص المتطلبات المثبتة"""
    requirements = [
        'python-telegram-bot==20.7',
        'python-dotenv',
        'apscheduler',
        'pytz',
        'nest_asyncio'
    ]
    
    missing = []
    for req in requirements:
        try:
            __import__(req.replace('-', '_'))
            print(f"✅ {req}")
        except ImportError:
            missing.append(req)
            print(f"❌ {req} غير مثبت")
    
    if missing:
        print(f"\n📦 تثبيت المتطلبات المفقودة...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print("✅ تم تثبيت جميع المتطلبات")
            return True
        except subprocess.CalledProcessError:
            print("❌ فشل في تثبيت المتطلبات")
            print("جرب تشغيل: pip install -r requirements.txt")
            return False
    
    return True

def check_env_file():
    """فحص ملف .env"""
    if not Path('.env').exists():
        print("⚠️  ملف .env غير موجود")
        if Path('.env.example').exists():
            print("💡 انسخ .env.example إلى .env وأضف التوكن الخاص بك")
        else:
            print("💡 أنشئ ملف .env وأضف BOT_TOKEN=your_token_here")
        return False
    
    # فحص وجود التوكن
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'BOT_TOKEN=' in content and 'your_bot_token_here' not in content:
                print("✅ ملف .env موجود مع التوكن")
                return True
            else:
                print("⚠️  يرجى تحديث BOT_TOKEN في ملف .env")
                return False
    except Exception as e:
        print(f"❌ خطأ في قراءة ملف .env: {e}")
        return False

def check_database():
    """فحص قاعدة البيانات"""
    if not Path('projects_new.json').exists():
        print("❌ ملف قاعدة البيانات projects_new.json غير موجود")
        return False
    
    try:
        import json
        with open('projects_new.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'categories' in data:
                print("✅ قاعدة البيانات صحيحة")
                return True
            else:
                print("❌ قاعدة البيانات تالفة")
                return False
    except Exception as e:
        print(f"❌ خطأ في قراءة قاعدة البيانات: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء تشغيل بوت التيليجرام...")
    print("=" * 50)
    
    # فحص المتطلبات
    checks = [
        ("فحص إصدار Python", check_python_version),
        ("فحص المكتبات المطلوبة", check_requirements),
        ("فحص ملف الإعدادات", check_env_file),
        ("فحص قاعدة البيانات", check_database)
    ]
    
    for name, check_func in checks:
        print(f"\n🔍 {name}...")
        if not check_func():
            print(f"\n❌ فشل في {name}")
            print("يرجى إصلاح المشاكل أعلاه قبل تشغيل البوت")
            return False
    
    print("\n" + "=" * 50)
    print("✅ جميع الفحوصات نجحت!")
    print("🤖 تشغيل البوت...")
    print("=" * 50)
    
    # تشغيل البوت
    try:
        import bot_new
        return True
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت بواسطة المستخدم")
        return True
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل البوت: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nاضغط Enter للخروج...")
        sys.exit(1)
