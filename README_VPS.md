# 🤖 Telegram Projects Bot - VPS Ready

## 📋 نظرة عامة

هذا البوت مصمم لعرض مشاريع الشركة على تيليجرام مع دعم كامل لـ Windows Server VPS.

### ✨ المميزات الرئيسية
- 🛍️ **المتاجر الإلكترونية** (بائع واحد، متعدد البائعين، إعلانات مبوبة)
- 📚 **المنصات التعليمية** (منصات LMS، أنظمة إدارة المدارس)
- 🚚 **تطبيقات التوصيل والشحن**
- 📊 **إحصائيات مفصلة** لكل مشروع
- 🔗 **روابط ديمو** مع بيانات الدخول
- 💰 **أسعار وإصدارات** متعددة

## 🚀 التشغيل السريع

### 1. فحص النظام
```cmd
system_check.bat
```

### 2. التثبيت التلقائي
```cmd
install_bot.bat
```

### 3. تشغيل البوت
```cmd
run_bot_server.bat
```

### 4. فحص الحالة
```cmd
check_bot_status.bat
```

### 5. إيقاف البوت
```cmd
stop_bot_server.bat
```

## 📁 هيكل الملفات

```
TelegramBot/
├── 🤖 Core Files
│   ├── bot_new.py              # الملف الرئيسي للبوت
│   ├── config.py               # إعدادات البوت
│   ├── database.py             # إدارة قاعدة البيانات
│   ├── formatters.py           # تنسيق الرسائل
│   └── user_context.py         # إدارة سياق المستخدمين
│
├── 📊 Data Files
│   ├── projects_new.json       # قاعدة بيانات المشاريع
│   ├── user_contexts.json      # سياق المستخدمين
│   └── requirements.txt        # المكتبات المطلوبة
│
├── 🔧 Management Scripts
│   ├── run_bot_server.bat      # تشغيل البوت على السيرفر
│   ├── stop_bot_server.bat     # إيقاف البوت
│   ├── check_bot_status.bat    # فحص حالة البوت
│   ├── install_bot.bat         # تثبيت تلقائي
│   └── system_check.bat        # فحص شامل للنظام
│
├── 📚 Documentation
│   ├── README_VPS.md           # دليل VPS (هذا الملف)
│   ├── VPS_SETUP_GUIDE.md      # دليل الإعداد المفصل
│   └── setup_environment.md    # دليل إعداد البيئة
│
└── 📝 Logs
    ├── bot_log_YYYYMMDD.txt    # سجلات البوت اليومية
    └── backup/                 # النسخ الاحتياطية
```

## 🔧 المتطلبات التقنية

### نظام التشغيل
- ✅ Windows Server 2016/2019/2022
- ✅ Windows 10/11 (للاختبار)

### الموارد
- 💾 **RAM**: 2GB كحد أدنى (4GB مُوصى به)
- 💽 **Storage**: 10GB مساحة فارغة
- 🌐 **Network**: اتصال إنترنت مستقر

### البرامج
- 🐍 **Python 3.11+** (مُوصى به)
- 📦 **pip** (يأتي مع Python)
- 🔥 **Windows Firewall** (إعدادات تلقائية)

## 📊 قاعدة البيانات

### هيكل المشاريع
```json
{
  "categories": {
    "stores": {
      "name": "المتاجر الإلكترونية",
      "subcategories": {
        "single_vendor": { "projects": [...] },
        "multi_vendor": { "projects": [...] },
        "classified_ads": { "projects": [...] }
      }
    }
  }
}
```

### أنواع اللوحات المدعومة
- 🔧 **admin_panel**: لوحة الإدارة
- 👤 **user_panel**: لوحة المستخدم
- 🏪 **vendor_panel**: لوحة التاجر
- 👥 **staff_panel**: لوحة طاقم العمل
- 🎓 **instructor_panel**: لوحة المدرب
- 👨‍👩‍👧‍👦 **student_parent_panel**: لوحة الطالب وولي الأمر
- 📱 **user_app**: تطبيق المستخدم
- 🚚 **delivery_app**: تطبيق التوصيل

## 🛡️ الأمان

### إعدادات Firewall
```cmd
# تلقائياً عبر install_bot.bat
netsh advfirewall firewall add rule name="Telegram Bot Python" dir=out action=allow program="C:\Python311\python.exe"
```

### حماية الملفات
- 🔒 **config.py**: يحتوي على التوكن الحساس
- 📊 **projects_new.json**: قاعدة البيانات الرئيسية
- 👤 **user_contexts.json**: بيانات المستخدمين

### النسخ الاحتياطية
```cmd
# نسخة احتياطية يدوية
copy projects_new.json backup\projects_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.json
```

## 📈 المراقبة

### السجلات
- 📝 **bot_log_YYYYMMDD.txt**: سجل يومي مفصل
- 🔍 **مستويات السجل**: INFO, WARNING, ERROR
- 📊 **إحصائيات**: عدد المستخدمين، الرسائل، الأخطاء

### مراقبة الأداء
```cmd
# فحص استخدام الذاكرة
wmic process where name="python.exe" get ProcessId,PageFileUsage,WorkingSetSize

# فحص استخدام CPU
wmic process where name="python.exe" get ProcessId,PageFileUsage,PercentProcessorTime
```

## 🚨 استكشاف الأخطاء

### مشاكل شائعة وحلولها

#### 1. "Python is not recognized"
```cmd
# إضافة Python إلى PATH
set PATH=%PATH%;C:\Python311;C:\Python311\Scripts
```

#### 2. "Module not found"
```cmd
pip install -r requirements.txt --force-reinstall
```

#### 3. "Conflict error"
```cmd
stop_bot_server.bat
timeout /t 10
run_bot_server.bat
```

#### 4. "Database error"
```cmd
# فحص صحة JSON
python -c "import json; json.load(open('projects_new.json', 'r', encoding='utf-8'))"
```

#### 5. "Network timeout"
- فحص اتصال الإنترنت
- فحص إعدادات Firewall
- تجربة VPN إذا لزم الأمر

## 📞 الدعم

### ملفات مهمة للدعم
- 📝 `bot_log_YYYYMMDD.txt`: آخر سجل للبوت
- ⚙️ `config.py`: إعدادات البوت
- 📊 `projects_new.json`: قاعدة البيانات

### أوامر تشخيصية
```cmd
# فحص شامل
system_check.bat

# فحص حالة البوت
check_bot_status.bat

# عرض السجل
type bot_log_%date:~-4,4%%date:~-10,2%%date:~-7,2%.txt
```

## 🔄 التحديثات

### تحديث المكتبات
```cmd
pip install --upgrade -r requirements.txt
```

### تحديث ملفات المشروع
1. إيقاف البوت: `stop_bot_server.bat`
2. نسخ الملفات الجديدة
3. تشغيل البوت: `run_bot_server.bat`

## ✅ قائمة التحقق

- [ ] Python 3.11+ مثبت
- [ ] جميع الملفات موجودة
- [ ] المكتبات مثبتة
- [ ] قاعدة البيانات صحيحة
- [ ] Firewall مُعد
- [ ] البوت يعمل بدون أخطاء
- [ ] السجلات تُحفظ بشكل صحيح

---

## 🎯 البوت جاهز للعمل على VPS!

**للبدء السريع**: شغل `install_bot.bat` ثم `run_bot_server.bat`

**للدعم**: راجع `VPS_SETUP_GUIDE.md` للتفاصيل الكاملة
