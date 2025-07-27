#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def rebuild_projects_json():
    """إعادة بناء ملف projects_new.json من الصفر"""
    
    # البيانات الأساسية
    data = {
        "categories": {
            "stores": {
                "name": "المتاجر الإلكترونية",
                "icon": "🛍️",
                "description": "متاجر إلكترونية احترافية لدعم التجارة الإلكترونية",
                "subcategories": {
                    "single_vendor": {
                        "name": "بائع واحد",
                        "icon": "🏪",
                        "description": "متاجر لتاجر واحد فقط",
                        "projects": [
                            {
                                "id": "fleetcart",
                                "name": "FleetCart",
                                "description": "متجر إلكتروني احترافي للبائع الواحد مع جميع المميزات المطلوبة",
                                "technologies": ["Laravel", "MySQL", "Bootstrap"],
                                "features": ["متجر بائع واحد", "لوحة إدارة شاملة", "نظام دفع متكامل", "إدارة المنتجات", "تصميم متجاوب", "نظام الطلبات", "إدارة العملاء", "تقارير مفصلة"],
                                "demo": {
                                    "website": "https://fleetcart.envaysoft.com/",
                                    "admin_panel": {
                                        "link": "https://fleetcart.envaysoft.com/admin",
                                        "email": "admin@fleetcart.com",
                                        "password": "password"
                                    }
                                },
                                "notes": "متجر إلكتروني متكامل للبائع الواحد مع جميع المميزات الأساسية والمتقدمة",
                                "price": {
                                    "amount": 800,
                                    "currency": "USD",
                                    "text": "800 دولار"
                                },
                                "delivery_time": "شهر"
                            }
                        ]
                    },
                    "multi_vendor": {
                        "name": "متعدد البائعين",
                        "icon": "🏬",
                        "description": "متاجر تدعم عدة تجار",
                        "projects": [
                            {
                                "id": "6valley",
                                "name": "6Valley",
                                "description": "منصة تجارة إلكترونية متعددة البائعين مع تطبيقات موبايل وميزات متقدمة",
                                "technologies": ["Laravel", "MySQL", "Bootstrap", "Flutter"],
                                "features": ["متعدد البائعين", "لوحة إدارة شاملة", "لوحة تاجر", "لوحة مستخدم", "تطبيق موبايل", "نظام دفع", "إدارة المنتجات", "نظام عمولات", "تصميم متجاوب"],
                                "demo": {
                                    "website": "https://6valley.6amtech.com/",
                                    "admin_panel": {
                                        "link": "https://6valley.6amtech.com/admin/auth/login",
                                        "email": "admin@6valley.com",
                                        "password": "12345678"
                                    },
                                    "vendor_panel": {
                                        "link": "https://6valley.6amtech.com/seller/auth/login",
                                        "email": "seller@6valley.com",
                                        "password": "12345678"
                                    }
                                },
                                "notes": "منصة تجارة إلكترونية متكاملة متعددة البائعين مع تطبيقات موبايل",
                                "versions": [
                                    {
                                        "id": "website_only",
                                        "name": "موقع فقط",
                                        "description": "منصة تجارة إلكترونية متعددة البائعين مع جميع المميزات الأساسية",
                                        "price": {
                                            "amount": 900,
                                            "currency": "USD",
                                            "text": "900 دولار"
                                        },
                                        "delivery_time": "شهر",
                                        "features": ["لوحة إدارة شاملة", "لوحة تاجر", "لوحة مستخدم", "موقع إلكتروني", "نظام دفع", "إدارة المنتجات", "نظام عمولات", "تصميم متجاوب"]
                                    },
                                    {
                                        "id": "with_user_app",
                                        "name": "مع تطبيق المستخدمين",
                                        "description": "منصة تجارة إلكترونية مع تطبيق موبايل للمستخدمين",
                                        "price": {
                                            "amount": 1200,
                                            "currency": "USD",
                                            "text": "1200 دولار"
                                        },
                                        "delivery_time": "شهر ونصف",
                                        "features": ["جميع مميزات الموقع", "تطبيق موبايل للمستخدمين", "إشعارات فورية", "تجربة تسوق محسنة"]
                                    },
                                    {
                                        "id": "with_delivery",
                                        "name": "مع تطبيق التوصيل",
                                        "description": "منصة تجارة إلكترونية شاملة مع تطبيق التوصيل",
                                        "price": {
                                            "amount": 1500,
                                            "currency": "USD",
                                            "text": "1500 دولار"
                                        },
                                        "delivery_time": "شهرين",
                                        "features": ["جميع مميزات النسخ السابقة", "تطبيق موبايل للتوصيل", "نظام تتبع الطلبات", "إدارة شاملة للتوصيل"]
                                    }
                                ]
                            }
                        ]
                    },
                    "classified_ads": {
                        "name": "إعلانات مبوبة",
                        "icon": "📢",
                        "description": "مواقع الإعلانات المبوبة والتصنيفية",
                        "projects": [
                            {
                                "id": "quickad",
                                "name": "Quickad",
                                "description": "Quickad Ads Laravel PHP Classified Script هو سكريبت إعلانات مبوبة PHP مميز مع تصميم Material وClassic متجاوب بالكامل. مبني ليكون جميل وسريع وقوي. إعداد بنقرة واحدة - يمكن للمستخدمين إعداد هذا القالب بسهولة وسهل الاستخدام والتخصيص.",
                                "technologies": ["Laravel", "MySQL", "Bootstrap"],
                                "features": ["إعلانات مبوبة شاملة", "تصميم Material وClassic", "متجاوب بالكامل", "إعداد بنقرة واحدة", "سهل الاستخدام", "قابل للتخصيص", "سريع وقوي", "لوحة إدارة متقدمة", "لوحة مستخدم", "بحث متقدم", "فئات متعددة", "نظام مراسلة", "إدارة الإعلانات"],
                                "demo": {
                                    "website": "https://classified.bylancer.com/",
                                    "admin_panel": {
                                        "link": "https://classified.bylancer.com/login",
                                        "email": "admin",
                                        "password": "admin"
                                    },
                                    "user_panel": {
                                        "link": "https://classified.bylancer.com/login",
                                        "email": "demo",
                                        "password": "demo"
                                    }
                                },
                                "notes": "سكريبت إعلانات مبوبة مميز مبني بـ Laravel مع تصميم عصري وإعداد سهل، مناسب لإنشاء مواقع إعلانات مثل OLX ودوبيزل.",
                                "price": {
                                    "amount": 800,
                                    "currency": "USD",
                                    "text": "800 دولار"
                                },
                                "delivery_time": "شهر"
                            },
                            {
                                "id": "laraclassifier",
                                "name": "LaraClassifier",
                                "description": "LaraClassifier هو أقوى تطبيق ويب للإعلانات المبوبة في السوق. تطبيق إعلانات مبوبة مفتوح المصدر وقابل للتوسع مع تصميم متجاوب بالكامل. مليء بالكثير من المميزات.",
                                "technologies": ["Laravel", "MySQL", "Bootstrap", "Vue"],
                                "features": ["أقوى تطبيق إعلانات مبوبة", "مفتوح المصدر", "قابل للتوسع والتطوير", "تصميم متجاوب بالكامل", "مليء بالمميزات", "لوحة إدارة قوية", "لوحة مستخدم متقدمة", "بحث متطور", "فئات متعددة", "نظام مراسلة", "إدارة شاملة للإعلانات", "واجهة Vue.js حديثة", "أمان عالي"],
                                "demo": {
                                    "website": "https://demo.laraclassifier.com/",
                                    "admin_panel": {
                                        "link": "https://demo.laraclassifier.com/admin",
                                        "email": "admin@domain.tld",
                                        "password": "123456"
                                    },
                                    "user_panel": {
                                        "link": "https://demo.laraclassifier.com/auth/login",
                                        "email": "user@domain.tld",
                                        "password": "123456"
                                    }
                                },
                                "notes": "أقوى تطبيق إعلانات مبوبة مفتوح المصدر في السوق مبني بـ Laravel مع واجهة Vue.js حديثة، قابل للتوسع والتطوير مع مميزات شاملة.",
                                "price": {
                                    "amount": 1000,
                                    "currency": "USD",
                                    "text": "1000 دولار"
                                },
                                "delivery_time": "شهر"
                            },
                            {
                                "id": "eclassify",
                                "name": "eClassify",
                                "description": "eClassify هو حل شامل متكامل للإعلانات المبوبة مع تطبيق موبايل للإعلانات المبوبة، واجهة ويب، ولوحة إدارة Laravel - مثالي لبناء نسخة من OLX، بوابة عقارية، أو بوابة وظائف.",
                                "technologies": ["Laravel", "MySQL", "Next.js", "React", "Flutter"],
                                "features": ["حل شامل متكامل", "تطبيق موبايل Flutter", "واجهة Next.js حديثة", "لوحة إدارة Laravel", "مثالي لـ OLX Clone", "بوابة عقارية", "بوابة وظائف", "لوحة طاقم العمل", "تقنيات حديثة", "تصميم متجاوب", "نظام شامل", "إدارة متقدمة", "واجهة React تفاعلية"],
                                "demo": {
                                    "website": "https://eclassifyweb.wrteam.me/",
                                    "admin_panel": {
                                        "link": "https://eclassify.wrteam.me/",
                                        "email": "admin@gmail.com",
                                        "password": "admin123"
                                    },
                                    "staff_panel": {
                                        "link": "https://eclassify.wrteam.me/",
                                        "email": "staff@gmail.com",
                                        "password": "Staff@123"
                                    },
                                    "user_app": {
                                        "link": "https://play.google.com/store/apps/details?id=com.eclassify.wrteam",
                                        "email": "user@demo.com",
                                        "password": "123456"
                                    }
                                },
                                "notes": "حل إعلانات مبوبة متكامل مع أحدث التقنيات (Next.js, React, Flutter) مثالي لبناء منصات مثل OLX والبوابات العقارية ومواقع الوظائف.",
                                "versions": [
                                    {
                                        "id": "website_only",
                                        "name": "موقع",
                                        "description": "حل إعلانات مبوبة متكامل مع واجهة Next.js ولوحة إدارة Laravel",
                                        "price": {
                                            "amount": 1200,
                                            "currency": "USD",
                                            "text": "1200 دولار"
                                        },
                                        "delivery_time": "شهر",
                                        "features": ["واجهة Next.js حديثة", "لوحة إدارة Laravel", "لوحة طاقم العمل", "نظام إعلانات شامل", "تصميم متجاوب", "إدارة متقدمة"]
                                    },
                                    {
                                        "id": "with_mobile_app",
                                        "name": "مع التطبيق",
                                        "description": "حل إعلانات مبوبة متكامل مع تطبيق Flutter للموبايل",
                                        "price": {
                                            "amount": 1600,
                                            "currency": "USD",
                                            "text": "1600 دولار"
                                        },
                                        "delivery_time": "شهر ونصف",
                                        "features": ["جميع مميزات الموقع", "تطبيق Flutter للموبايل", "تطبيق على Google Play", "واجهة موبايل متطورة", "تجربة مستخدم محسنة", "إشعارات فورية"]
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }
    
    # حفظ الملف
    with open('projects_new_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print('✅ تم إنشاء ملف projects_new_fixed.json بنجاح!')
    
    # التحقق من صحة الملف
    with open('projects_new_fixed.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    stores = test_data['categories']['stores']['subcategories']
    print(f'الأقسام الفرعية: {list(stores.keys())}')
    
    if 'classified_ads' in stores:
        projects = stores['classified_ads']['projects']
        print(f'مشاريع الإعلانات المبوبة: {len(projects)}')
        for p in projects:
            print(f'  - {p["name"]}')

if __name__ == '__main__':
    rebuild_projects_json()
