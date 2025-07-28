# 🚀 دليل إعداد البوت على Windows Server VPS

## 📋 المتطلبات الأساسية

### 1. متطلبات النظام
- **نظام التشغيل**: Windows Server 2016/2019/2022
- **الذاكرة**: 2GB RAM كحد أدنى (4GB مُوصى به)
- **المساحة**: 10GB مساحة فارغة
- **الشبكة**: اتصال إنترنت مستقر

### 2. البرامج المطلوبة
- **Python 3.11+** (مُوصى به Python 3.11)
- **Git** (اختياري لتحديث المشروع)
- **Text Editor** (Notepad++ أو VS Code)

## 🔧 خطوات الإعداد

### الخطوة 1: تثبيت Python
```powershell
# تحميل Python من الموقع الرسمي
https://www.python.org/downloads/windows/

# أو استخدام winget (إذا كان متاح)
winget install Python.Python.3.11

# أو استخدام Chocolatey
choco install python --version=3.11.0
```

**⚠️ مهم**: تأكد من تحديد "Add Python to PATH" أثناء التثبيت

### الخطوة 2: التحقق من تثبيت Python
```cmd
python --version
py --version
pip --version
```

### الخطوة 3: رفع ملفات المشروع
1. **إنشاء مجلد للمشروع**:
   ```cmd
   mkdir C:\TelegramBot
   cd C:\TelegramBot
   ```

2. **رفع الملفات** (عبر FTP أو Remote Desktop):
   - `bot_new.py`
   - `config.py`
   - `database.py`
   - `formatters.py`
   - `user_context.py`
   - `projects_new.json`
   - `requirements.txt`
   - `run_bot_server.bat`
   - `stop_bot_server.bat`
   - `check_bot_status.bat`

### الخطوة 4: تثبيت المتطلبات
```cmd
cd C:\TelegramBot
pip install -r requirements.txt
```

أو تثبيت المكتبات منفردة:
```cmd
pip install python-telegram-bot==20.7
pip install python-dotenv==1.0.0
pip install APScheduler==3.10.4
pip install pytz==2023.3
pip install nest-asyncio==1.5.8
```

### الخطوة 5: إعداد متغيرات البيئة (اختياري)
إنشاء ملف `.env` في مجلد المشروع:
```env
BOT_TOKEN=7772858381:AAH2HVRp6b6udR4xzBjg33_VorLhqpqDMxs
BOT_USERNAME=ProjectsDetailsBot
BOT_NAME=مشاريع الشركة
DATABASE_FILE=projects_new.json
LOG_LEVEL=INFO
```

## 🚀 تشغيل البوت

### الطريقة الأولى: تشغيل مباشر (للاختبار)
```cmd
cd C:\TelegramBot
python bot_new.py
```

### الطريقة الثانية: تشغيل على السيرفر (مُوصى به)
```cmd
cd C:\TelegramBot
run_bot_server.bat
```

### الطريقة الثالثة: تشغيل كخدمة Windows
1. **إنشاء ملف خدمة** باستخدام `nssm` أو `sc create`
2. **تسجيل الخدمة** في Windows Services
3. **تشغيل الخدمة** تلقائياً عند بدء النظام

## 🔍 إدارة البوت

### فحص حالة البوت
```cmd
check_bot_status.bat
```

### إيقاف البوت
```cmd
stop_bot_server.bat
```

### عرض السجلات
```cmd
type bot_log_20250128.txt
```

### فحص العمليات يدوياً
```cmd
tasklist /FI "IMAGENAME eq python.exe"
tasklist /FI "IMAGENAME eq pythonw.exe"
```

## 🛡️ الأمان والحماية

### 1. إعدادات Firewall
```cmd
# السماح لـ Python بالوصول للإنترنت
netsh advfirewall firewall add rule name="Python Bot" dir=out action=allow program="C:\Python311\python.exe"
netsh advfirewall firewall add rule name="Python Bot Background" dir=out action=allow program="C:\Python311\pythonw.exe"
```

### 2. إعدادات المستخدم
- **إنشاء مستخدم مخصص** للبوت (اختياري)
- **تقييد الصلاحيات** للمجلد
- **تشفير ملف التوكن**

### 3. النسخ الاحتياطية
```cmd
# إنشاء نسخة احتياطية يومية
xcopy "C:\TelegramBot\projects_new.json" "C:\Backup\projects_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.json"
```

## 📊 المراقبة والصيانة

### 1. مراقبة الأداء
- **Task Manager**: مراقبة استخدام CPU والذاكرة
- **Event Viewer**: فحص أخطاء النظام
- **Bot Logs**: مراجعة سجلات البوت يومياً

### 2. التحديثات
```cmd
# تحديث المكتبات
pip install --upgrade -r requirements.txt

# تحديث ملفات المشروع (عبر Git أو يدوياً)
git pull origin main
```

### 3. إعادة التشغيل التلقائي
إنشاء مهمة في Task Scheduler:
1. **فتح Task Scheduler**
2. **إنشاء Basic Task**
3. **تحديد التوقيت**: عند بدء النظام
4. **الإجراء**: تشغيل `run_bot_server.bat`

## 🚨 استكشاف الأخطاء

### مشكلة: "Python is not recognized"
**الحل**:
```cmd
# إضافة Python إلى PATH يدوياً
set PATH=%PATH%;C:\Python311;C:\Python311\Scripts
```

### مشكلة: "Module not found"
**الحل**:
```cmd
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### مشكلة: "Conflict error"
**الحل**:
```cmd
stop_bot_server.bat
timeout /t 10
run_bot_server.bat
```

### مشكلة: "Network timeout"
**الحل**:
1. فحص اتصال الإنترنت
2. فحص إعدادات Firewall
3. تجربة VPN إذا لزم الأمر

## 📞 الدعم والمساعدة

### ملفات السجل المهمة
- `bot_log_YYYYMMDD.txt`: سجل البوت اليومي
- `user_contexts.json`: سياق المستخدمين
- `projects_new.json`: قاعدة بيانات المشاريع

### أوامر مفيدة
```cmd
# فحص اتصال الإنترنت
ping google.com

# فحص منافذ الشبكة
netstat -an | findstr :443
netstat -an | findstr :80

# فحص استخدام الذاكرة
wmic process where name="python.exe" get ProcessId,PageFileUsage,WorkingSetSize
```

## ✅ قائمة التحقق النهائية

- [ ] Python 3.11+ مثبت ومضاف إلى PATH
- [ ] جميع ملفات المشروع موجودة في `C:\TelegramBot`
- [ ] المكتبات المطلوبة مثبتة (`pip list`)
- [ ] ملف `projects_new.json` صحيح وقابل للقراءة
- [ ] التوكن صحيح في `config.py`
- [ ] Firewall يسمح لـ Python بالوصول للإنترنت
- [ ] البوت يعمل بدون أخطاء (`python bot_new.py`)
- [ ] ملفات `.bat` تعمل بشكل صحيح
- [ ] السجلات تُحفظ في `bot_log_YYYYMMDD.txt`

## 🎯 نصائح للأداء الأمثل

1. **استخدم SSD** لتحسين سرعة القراءة/الكتابة
2. **خصص 4GB RAM** للنظام كحد أدنى
3. **فعل Windows Updates** التلقائية
4. **راقب استخدام الموارد** بانتظام
5. **أنشئ نسخ احتياطية** دورية
6. **استخدم UPS** لحماية من انقطاع الكهرباء

---

**🚀 البوت جاهز للعمل على Windows Server VPS!**
