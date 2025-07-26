# 🔧 إعداد البيئة لتشغيل البوت

## 📋 المتطلبات الأساسية

### 1. تثبيت Python
```bash
# تحميل Python من الموقع الرسمي
https://www.python.org/downloads/

# أو استخدام Chocolatey (Windows)
choco install python

# أو استخدام winget (Windows 10/11)
winget install Python.Python.3
```

### 2. التحقق من تثبيت Python
```bash
python --version
# أو
python3 --version
# أو
py --version
```

### 3. تثبيت المتطلبات
```bash
# استخدام pip
pip install -r requirements.txt

# أو استخدام python -m pip
python -m pip install -r requirements.txt

# أو تثبيت المكتبات منفردة
pip install python-telegram-bot==20.7
pip install python-dotenv==1.0.0
pip install APScheduler==3.10.4
pip install pytz==2023.3
pip install nest-asyncio==1.5.8
```

## ⚙️ إعداد البوت

### 1. إنشاء ملف .env
```bash
# انسخ ملف .env.example إلى .env
copy .env.example .env

# أو في Linux/Mac
cp .env.example .env
```

### 2. تحديث التوكن
```env
BOT_TOKEN=your_actual_bot_token_here
BOT_USERNAME=YourBotUsername
BOT_NAME=اسم البوت
```

### 3. الحصول على توكن البوت
1. تحدث مع @BotFather في تيليجرام
2. أرسل `/newbot`
3. اتبع التعليمات لإنشاء البوت
4. احفظ التوكن في ملف .env

## 🚀 تشغيل البوت

### الطريقة الأولى: تشغيل مباشر
```bash
python bot_new.py
```

### الطريقة الثانية: استخدام ملفات batch (Windows)
```bash
# تشغيل على السيرفر
run_bot_server.bat

# فحص حالة البوت
check_bot_status.bat

# إيقاف البوت
stop_bot_server.bat
```

### الطريقة الثالثة: تشغيل في الخلفية (Linux/Mac)
```bash
nohup python bot_new.py &
```

## 🔍 استكشاف الأخطاء

### مشكلة: Python not found
**الحل:**
1. تأكد من تثبيت Python بشكل صحيح
2. أضف Python إلى PATH
3. أعد تشغيل Terminal/Command Prompt

### مشكلة: Module not found
**الحل:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### مشكلة: Conflict error
**الحل:**
```bash
# أوقف جميع نسخ البوت
stop_bot_server.bat
# انتظر 10 ثواني ثم شغل مرة أخرى
run_bot_server.bat
```

## 📊 مراقبة البوت

### فحص السجلات
```bash
# عرض السجل اليومي
type bot_log_YYYYMMDD.txt

# مثال
type bot_log_20250126.txt
```

### فحص العمليات
```bash
# Windows
tasklist /FI "IMAGENAME eq python.exe"

# Linux/Mac
ps aux | grep python
```

## 🛡️ الأمان

1. **لا تشارك ملف .env مع أحد**
2. **احتفظ بنسخة احتياطية من قاعدة البيانات**
3. **راقب السجلات بانتظام**
4. **استخدم HTTPS للروابط الخارجية**

## 📞 الدعم

في حالة وجود مشاكل:
1. راجع السجلات: `bot_log_YYYYMMDD.txt`
2. تأكد من صحة التوكن
3. تحقق من اتصال الإنترنت
4. جرب إعادة تشغيل البوت
