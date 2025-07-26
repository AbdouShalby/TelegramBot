#!/usr/bin/env python3
"""
🤖 Telegram Projects Bot Setup Script
تسكريبت إعداد بوت مشاريع التيليجرام
"""

import os
import sys
import subprocess
import json

def check_python_version():
    """التحقق من إصدار Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ مطلوب")
        print(f"الإصدار الحالي: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} متوفر")
    return True

def install_requirements():
    """تثبيت المتطلبات"""
    print("📦 تثبيت المتطلبات...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ تم تثبيت المتطلبات بنجاح")
        return True
    except subprocess.CalledProcessError:
        print("❌ فشل في تثبيت المتطلبات")
        return False

def create_env_file():
    """إنشاء ملف .env"""
    if os.path.exists('.env'):
        print("✅ ملف .env موجود بالفعل")
        return True
    
    print("📝 إنشاء ملف .env...")
    bot_token = input("أدخل توكن البوت: ").strip()
    
    if not bot_token:
        print("❌ توكن البوت مطلوب")
        return False
    
    env_content = f"""# Bot Configuration
BOT_TOKEN={bot_token}
BOT_USERNAME=ProjectsDetailsBot
BOT_NAME=مشاريع الشركة

# Database Configuration
DATABASE_FILE=projects_new.json

# Logging Configuration
LOG_LEVEL=INFO
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ تم إنشاء ملف .env")
    return True

def check_database():
    """التحقق من قاعدة البيانات"""
    if not os.path.exists('projects_new.json'):
        print("❌ ملف قاعدة البيانات غير موجود")
        return False
    
    try:
        with open('projects_new.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'categories' not in data:
            print("❌ بنية قاعدة البيانات غير صحيحة")
            return False
        
        print("✅ قاعدة البيانات صحيحة")
        return True
    except json.JSONDecodeError:
        print("❌ خطأ في تنسيق قاعدة البيانات")
        return False

def test_bot():
    """اختبار البوت"""
    print("🧪 اختبار البوت...")
    try:
        from config import BOT_TOKEN
        from database import db
        
        if not BOT_TOKEN:
            print("❌ توكن البوت غير محدد")
            return False
        
        categories = db.get_categories()
        if not categories:
            print("❌ لا توجد أقسام في قاعدة البيانات")
            return False
        
        print(f"✅ البوت جاهز - {len(categories)} قسم متاح")
        return True
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 إعداد بوت مشاريع التيليجرام")
    print("=" * 40)
    
    # التحقق من Python
    if not check_python_version():
        return False
    
    # تثبيت المتطلبات
    if not install_requirements():
        return False
    
    # إنشاء ملف .env
    if not create_env_file():
        return False
    
    # التحقق من قاعدة البيانات
    if not check_database():
        return False
    
    # اختبار البوت
    if not test_bot():
        return False
    
    print("\n🎉 تم إعداد البوت بنجاح!")
    print("\n📋 الخطوات التالية:")
    print("1. تشغيل البوت: python bot_new.py")
    print("2. أو استخدام: run_bot_server.bat")
    print("3. اختبار البوت في التيليجرام")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
