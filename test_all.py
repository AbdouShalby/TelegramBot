#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import asyncio

# إضافة المجلد الحالي إلى مسار Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_json_structure():
    """اختبار هيكل JSON"""
    print("🧪 اختبار هيكل JSON...")
    
    try:
        with open('projects_new.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ تم تحميل JSON بنجاح")
        
        # اختبار Single Vendor
        single_projects = data['categories']['stores']['subcategories']['single_vendor']['projects']
        print(f"📊 مشاريع Single Vendor: {len(single_projects)}")
        
        for project in single_projects:
            print(f"  🛠️ {project['name']}")
            versions = project.get('versions', [])
            print(f"    📋 الإصدارات: {len(versions)}")
            for version in versions:
                print(f"      • {version['name']} - {version['price']['text']}")
        
        # اختبار Multi Vendor
        multi_projects = data['categories']['stores']['subcategories']['multi_vendor']['projects']
        print(f"\n📊 مشاريع Multi Vendor: {len(multi_projects)}")
        
        for project in multi_projects:
            print(f"  🛠️ {project['name']}")
            versions = project.get('versions', [])
            print(f"    📋 الإصدارات: {len(versions)}")
            for version in versions:
                print(f"      • {version['name']} - {version['price']['text']}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في JSON: {e}")
        return False

def test_database():
    """اختبار قاعدة البيانات"""
    print("\n🧪 اختبار قاعدة البيانات...")
    
    try:
        from database import ProjectDatabase
        
        db = ProjectDatabase()
        print("✅ تم إنشاء قاعدة البيانات بنجاح")
        
        # اختبار الحصول على الفئات
        categories = db.get_categories()
        print(f"📁 الفئات: {list(categories.keys())}")
        
        # اختبار الحصول على مشاريع Single Vendor
        single_projects = db.get_projects("stores", "single_vendor")
        print(f"🏪 مشاريع Single Vendor: {len(single_projects)}")
        
        # اختبار الحصول على مشاريع Multi Vendor
        multi_projects = db.get_projects("stores", "multi_vendor")
        print(f"🏬 مشاريع Multi Vendor: {len(multi_projects)}")
        
        # اختبار الحصول على إصدارات المشروع
        if single_projects:
            project = single_projects[0]
            versions = db.get_project_versions("stores", "single_vendor", project['id'])
            print(f"📋 إصدارات المشروع {project['name']}: {len(versions)}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
        return False

def test_formatters():
    """اختبار التنسيق"""
    print("\n🧪 اختبار التنسيق...")
    
    try:
        from database import ProjectDatabase
        from formatters import MessageFormatter
        
        db = ProjectDatabase()
        formatter = MessageFormatter()
        
        # اختبار تنسيق القائمة الرئيسية
        main_menu = formatter.format_main_menu()
        print(f"✅ القائمة الرئيسية: {len(main_menu)} حرف")
        
        # اختبار تنسيق المشروع مع الإصدارات
        projects = db.get_projects("stores", "single_vendor")
        if projects:
            project = projects[0]
            project_text = formatter.format_project_with_versions(project)
            print(f"✅ تنسيق المشروع: {len(project_text)} حرف")
            
            # اختبار تنسيق الإصدار
            versions = project.get("versions", [])
            if versions:
                version_text = formatter.format_version_details(project, versions[0])
                print(f"✅ تنسيق الإصدار: {len(version_text)} حرف")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في التنسيق: {e}")
        return False

def test_callback_parsing():
    """اختبار parsing الـ callback data"""
    print("\n🧪 اختبار parsing الـ callback data...")
    
    # اختبار الـ callback data للمشاريع
    test_cases = [
        "project_stores_single_vendor_active",
        "project_stores_multi_vendor_active_multi",
        "version_stores_single_vendor_active_website_only",
        "version_stores_multi_vendor_active_multi_with_user_app"
    ]
    
    for choice in test_cases:
        print(f"📝 اختبار: {choice}")
        
        if choice.startswith("project_"):
            parts = choice.split("_", 1)
            if len(parts) >= 2:
                remaining = parts[1]
                remaining_parts = remaining.split("_")
                
                if len(remaining_parts) >= 3:
                    category_id = remaining_parts[0]
                    subcategory_id = remaining_parts[1] + "_" + remaining_parts[2]
                    project_id = "_".join(remaining_parts[3:])
                    print(f"  ✅ Category: {category_id}, Subcategory: {subcategory_id}, Project: {project_id}")
                else:
                    print(f"  ❌ Invalid structure")
            else:
                print(f"  ❌ Invalid format")
        
        elif choice.startswith("version_"):
            parts = choice.split("_", 1)
            if len(parts) >= 2:
                remaining = parts[1]
                remaining_parts = remaining.split("_")
                
                if len(remaining_parts) >= 4:
                    category_id = remaining_parts[0]
                    subcategory_id = remaining_parts[1] + "_" + remaining_parts[2]
                    project_id = remaining_parts[3]
                    version_id = "_".join(remaining_parts[4:])
                    print(f"  ✅ Category: {category_id}, Subcategory: {subcategory_id}, Project: {project_id}, Version: {version_id}")
                else:
                    print(f"  ❌ Invalid structure")
            else:
                print(f"  ❌ Invalid format")
    
    return True

def test_telegram_connection():
    """اختبار الاتصال بتيليجرام"""
    print("\n🧪 اختبار الاتصال بتيليجرام...")
    
    try:
        from config import BOT_TOKEN
        from telegram import Bot
        
        async def test_bot():
            bot = Bot(token=BOT_TOKEN)
            me = await bot.get_me()
            print(f"✅ البوت متصل: @{me.username}")
            print(f"🆔 معرف البوت: {me.id}")
            print(f"📝 اسم البوت: {me.first_name}")
        
        asyncio.run(test_bot())
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False

def main():
    """تشغيل جميع الاختبارات"""
    print("🚀 بدء اختبار البوت...")
    print("=" * 50)
    
    tests = [
        ("JSON Structure", test_json_structure),
        ("Database", test_database),
        ("Formatters", test_formatters),
        ("Callback Parsing", test_callback_parsing),
        ("Telegram Connection", test_telegram_connection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: نجح")
            else:
                print(f"❌ {test_name}: فشل")
        except Exception as e:
            print(f"❌ {test_name}: خطأ - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 النتيجة: {passed}/{total} اختبار نجح")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! البوت جاهز للاستخدام.")
    else:
        print("⚠️ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء.")

if __name__ == "__main__":
    main() 