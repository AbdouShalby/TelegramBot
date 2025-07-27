#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def add_classified_ads_section():
    """إضافة قسم الإعلانات المبوبة بطريقة برمجية آمنة"""

    # قراءة الملف الحالي
    try:
        with open('projects_new.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f'❌ خطأ في JSON: {e}')
        print('🔧 سأحاول إصلاح الملف...')

        # قراءة الملف كـ text وإصلاح المشكلة
        with open('projects_new.json', 'r', encoding='utf-8') as f:
            content = f.read()

        # إصلاح المشاكل الشائعة
        content = content.replace('        }\n          ]\n        }', '        }')
        content = content.replace('          ]\n        }\n      }', '          ]\n        }\n      }')

        # محاولة تحليل JSON مرة أخرى
        try:
            data = json.loads(content)
            print('✅ تم إصلاح الملف!')
        except:
            print('❌ فشل في إصلاح الملف. سأستخدم backup.')
            # استخدام backup أو إنشاء هيكل جديد
            return False
    
    # التأكد من وجود الهيكل الصحيح
    if 'categories' not in data:
        data['categories'] = {}
    
    if 'stores' not in data['categories']:
        data['categories']['stores'] = {
            'name': 'المتاجر الإلكترونية',
            'icon': '🛍️',
            'description': 'متاجر إلكترونية احترافية لدعم التجارة الإلكترونية',
            'subcategories': {}
        }
    
    if 'subcategories' not in data['categories']['stores']:
        data['categories']['stores']['subcategories'] = {}
    
    # إضافة قسم الإعلانات المبوبة
    data['categories']['stores']['subcategories']['classified_ads'] = {
        'name': 'إعلانات مبوبة',
        'icon': '📢',
        'description': 'مواقع الإعلانات المبوبة والتصنيفية',
        'projects': [
            {
                'id': 'quickad',
                'name': 'Quickad',
                'description': 'Quickad Ads Laravel PHP Classified Script هو سكريبت إعلانات مبوبة PHP مميز مع تصميم Material وClassic متجاوب بالكامل. مبني ليكون جميل وسريع وقوي. إعداد بنقرة واحدة - يمكن للمستخدمين إعداد هذا القالب بسهولة وسهل الاستخدام والتخصيص.',
                'technologies': ['Laravel', 'MySQL', 'Bootstrap'],
                'features': [
                    'إعلانات مبوبة شاملة',
                    'تصميم Material وClassic',
                    'متجاوب بالكامل',
                    'إعداد بنقرة واحدة',
                    'سهل الاستخدام',
                    'قابل للتخصيص',
                    'سريع وقوي',
                    'لوحة إدارة متقدمة',
                    'لوحة مستخدم',
                    'بحث متقدم',
                    'فئات متعددة',
                    'نظام مراسلة',
                    'إدارة الإعلانات'
                ],
                'demo': {
                    'website': 'https://classified.bylancer.com/',
                    'admin_panel': {
                        'link': 'https://classified.bylancer.com/login',
                        'email': 'admin',
                        'password': 'admin'
                    },
                    'user_panel': {
                        'link': 'https://classified.bylancer.com/login',
                        'email': 'demo',
                        'password': 'demo'
                    }
                },
                'notes': 'سكريبت إعلانات مبوبة مميز مبني بـ Laravel مع تصميم عصري وإعداد سهل، مناسب لإنشاء مواقع إعلانات مثل OLX ودوبيزل.',
                'price': {
                    'amount': 800,
                    'currency': 'USD',
                    'text': '800 دولار'
                },
                'delivery_time': 'شهر'
            },
            {
                'id': 'laraclassifier',
                'name': 'LaraClassifier',
                'description': 'LaraClassifier هو أقوى تطبيق ويب للإعلانات المبوبة في السوق. تطبيق إعلانات مبوبة مفتوح المصدر وقابل للتوسع مع تصميم متجاوب بالكامل. مليء بالكثير من المميزات.',
                'technologies': ['Laravel', 'MySQL', 'Bootstrap', 'Vue'],
                'features': [
                    'أقوى تطبيق إعلانات مبوبة',
                    'مفتوح المصدر',
                    'قابل للتوسع والتطوير',
                    'تصميم متجاوب بالكامل',
                    'مليء بالمميزات',
                    'لوحة إدارة قوية',
                    'لوحة مستخدم متقدمة',
                    'بحث متطور',
                    'فئات متعددة',
                    'نظام مراسلة',
                    'إدارة شاملة للإعلانات',
                    'واجهة Vue.js حديثة',
                    'أمان عالي'
                ],
                'demo': {
                    'website': 'https://demo.laraclassifier.com/',
                    'admin_panel': {
                        'link': 'https://demo.laraclassifier.com/admin',
                        'email': 'admin@domain.tld',
                        'password': '123456'
                    },
                    'user_panel': {
                        'link': 'https://demo.laraclassifier.com/auth/login',
                        'email': 'user@domain.tld',
                        'password': '123456'
                    }
                },
                'notes': 'أقوى تطبيق إعلانات مبوبة مفتوح المصدر في السوق مبني بـ Laravel مع واجهة Vue.js حديثة، قابل للتوسع والتطوير مع مميزات شاملة.',
                'price': {
                    'amount': 1000,
                    'currency': 'USD',
                    'text': '1000 دولار'
                },
                'delivery_time': 'شهر'
            },
            {
                'id': 'eclassify',
                'name': 'eClassify',
                'description': 'eClassify هو حل شامل متكامل للإعلانات المبوبة مع تطبيق موبايل للإعلانات المبوبة، واجهة ويب، ولوحة إدارة Laravel - مثالي لبناء نسخة من OLX، بوابة عقارية، أو بوابة وظائف.',
                'technologies': ['Laravel', 'MySQL', 'Next.js', 'React', 'Flutter'],
                'features': [
                    'حل شامل متكامل',
                    'تطبيق موبايل Flutter',
                    'واجهة Next.js حديثة',
                    'لوحة إدارة Laravel',
                    'مثالي لـ OLX Clone',
                    'بوابة عقارية',
                    'بوابة وظائف',
                    'لوحة طاقم العمل',
                    'تقنيات حديثة',
                    'تصميم متجاوب',
                    'نظام شامل',
                    'إدارة متقدمة',
                    'واجهة React تفاعلية'
                ],
                'demo': {
                    'website': 'https://eclassifyweb.wrteam.me/',
                    'admin_panel': {
                        'link': 'https://eclassify.wrteam.me/',
                        'email': 'admin@gmail.com',
                        'password': 'admin123'
                    },
                    'staff_panel': {
                        'link': 'https://eclassify.wrteam.me/',
                        'email': 'staff@gmail.com',
                        'password': 'Staff@123'
                    },
                    'user_app': {
                        'link': 'https://play.google.com/store/apps/details?id=com.eclassify.wrteam',
                        'email': 'user@demo.com',
                        'password': '123456'
                    }
                },
                'notes': 'حل إعلانات مبوبة متكامل مع أحدث التقنيات (Next.js, React, Flutter) مثالي لبناء منصات مثل OLX والبوابات العقارية ومواقع الوظائف.',
                'versions': [
                    {
                        'id': 'website_only',
                        'name': 'موقع',
                        'description': 'حل إعلانات مبوبة متكامل مع واجهة Next.js ولوحة إدارة Laravel',
                        'price': {
                            'amount': 1200,
                            'currency': 'USD',
                            'text': '1200 دولار'
                        },
                        'delivery_time': 'شهر',
                        'features': ['واجهة Next.js حديثة', 'لوحة إدارة Laravel', 'لوحة طاقم العمل', 'نظام إعلانات شامل', 'تصميم متجاوب', 'إدارة متقدمة']
                    },
                    {
                        'id': 'with_mobile_app',
                        'name': 'مع التطبيق',
                        'description': 'حل إعلانات مبوبة متكامل مع تطبيق Flutter للموبايل',
                        'price': {
                            'amount': 1600,
                            'currency': 'USD',
                            'text': '1600 دولار'
                        },
                        'delivery_time': 'شهر ونصف',
                        'features': ['جميع مميزات الموقع', 'تطبيق Flutter للموبايل', 'تطبيق على Google Play', 'واجهة موبايل متطورة', 'تجربة مستخدم محسنة', 'إشعارات فورية']
                    }
                ]
            }
        ]
    }
    
    # حفظ الملف
    with open('projects_new.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print('✅ تم إضافة قسم الإعلانات المبوبة بنجاح!')
    
    # التحقق من صحة الملف
    with open('projects_new.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    stores = test_data['categories']['stores']['subcategories']
    print(f'الأقسام الفرعية: {list(stores.keys())}')
    
    if 'classified_ads' in stores:
        projects = stores['classified_ads']['projects']
        print(f'مشاريع الإعلانات المبوبة: {len(projects)}')
        for p in projects:
            print(f'  - {p["name"]}')

if __name__ == '__main__':
    add_classified_ads_section()
