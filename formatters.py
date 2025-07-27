from typing import Dict, List, Any
from config import MAX_PROJECTS_PER_MESSAGE

class MessageFormatter:
    """نظام تنسيق رسائل البوت"""
    
    @staticmethod
    def format_main_menu() -> str:
        """تنسيق القائمة الرئيسية"""
        return """🏢 *مشاريع الشركة*

مرحباً بك في بوت مشاريع الشركة! 🚀

اختر نوع المشروع الذي تبحث عنه:

🛍️ *المتاجر الإلكترونية*
📚 *المنصات التعليمية*  
🚚 *تطبيقات التوصيل*
⚙️ *أنظمة إدارة الأعمال*
📱 *تطبيقات الموبايل*

أو اكتب كلمة للبحث في المشاريع 🔍"""
    
    @staticmethod
    def format_category_menu(category: Dict[str, Any]) -> str:
        """تنسيق قائمة الأقسام الفرعية"""
        icon = category.get("icon", "📁")
        name = category.get("name", "قسم")
        description = category.get("description", "")
        
        text = f"{icon} *{name}*\n\n"
        if description:
            text += f"{description}\n\n"
        
        text += "اختر النوع المطلوب:"
        return text
    
    @staticmethod
    def format_subcategory_menu(subcategory: Dict[str, Any], projects: List[Dict[str, Any]], page: int = 0, total_pages: int = 1) -> str:
        """تنسيق قائمة المشاريع في قسم فرعي مع pagination"""
        icon = subcategory.get("icon", "📁")
        name = subcategory.get("name", "قسم فرعي")
        description = subcategory.get("description", "")
        
        text = f"{icon} *{name}*\n\n"
        if description:
            text += f"{description}\n\n"
        
        if projects:
            # حساب المشاريع في الصفحة الحالية
            projects_per_page = 3
            start_index = page * projects_per_page
            end_index = min(start_index + projects_per_page, len(projects))
            current_projects = projects[start_index:end_index]
            
            text += f"*المشاريع المتاحة ({len(projects)}):*\n\n"
            
            # إضافة معلومات الصفحة
            if total_pages > 1:
                text += f"📄 *الصفحة {page+1} من {total_pages}*\n\n"
            
            for i, project in enumerate(current_projects, start_index + 1):
                project_name = project.get('name', 'مشروع')
                
                # تقصير اسم المشروع إذا كان طويلاً
                if len(project_name) > 30:
                    project_name = project_name[:30]
                
                text += f"🛠️ *{project_name}*\n"
            
            # إضافة معلومات إضافية
            if total_pages > 1:
                text += f"\n💡 *استخدم أزرار التنقل للانتقال بين الصفحات*"
        else:
            text += "لا توجد مشاريع متاحة حالياً."
        
        return text
    
    @staticmethod
    def format_project_details(project: Dict[str, Any]) -> str:
        """تنسيق تفاصيل المشروع"""
        text = f"🛠️ *{project.get('name', 'مشروع')}*\n\n"
        text += f"📝 *الوصف:*\n{project.get('description', 'لا يوجد وصف')}\n\n"

        # السعر والوقت
        price = project.get("price", {})
        delivery_time = project.get("delivery_time")

        if price or delivery_time:
            text += "💼 *معلومات الطلب:*\n"
            if price:
                text += f"💰 السعر: {price.get('text', 'غير محدد')}\n"
            if delivery_time:
                text += f"⏰ مدة التسليم: {delivery_time}\n"
            text += "\n"

        # التقنيات
        technologies = project.get("technologies", [])
        if technologies:
            text += f"🧪 *التقنيات المستخدمة:*\n"
            for tech in technologies:
                text += f"• {tech}\n"
            text += "\n"

        # المميزات
        features = project.get("features", [])
        if features:
            text += f"✨ *المميزات الرئيسية:*\n"
            for feature in features:
                text += f"• {feature}\n"
            text += "\n"
        
        # روابط الديمو
        demo = project.get("demo", {})
        if demo:
            text += f"🌐 *روابط الديمو والاختبار:*\n\n"

            # الموقع الرئيسي
            website = demo.get("website")
            if website:
                if isinstance(website, dict):
                    text += f"🔗 *الموقع الرئيسي:*\n"
                    text += f"   {website.get('link', 'غير متاح')}\n"
                    if website.get('email'):
                        text += f"   📧 Email: `{website['email']}`\n"
                    if website.get('password'):
                        text += f"   🔑 Password: `{website['password']}`\n"
                    text += "\n"
                else:
                    text += f"🔗 *الموقع الرئيسي:*\n   {website}\n\n"

            # لوحة الإدارة
            admin_panel = demo.get("admin_panel")
            if admin_panel:
                text += f"⚙️ *لوحة الإدارة:*\n"
                text += f"   {admin_panel.get('link', 'غير متاح')}\n"
                if admin_panel.get('email'):
                    text += f"   📧 Email: `{admin_panel['email']}`\n"
                if admin_panel.get('password'):
                    text += f"   🔑 Password: `{admin_panel['password']}`\n"
                text += "\n"
            
            # لوحة التاجر
            vendor_panel = demo.get("vendor_panel")
            if vendor_panel:
                text += f"🏪 *لوحة التاجر:*\n"
                text += f"   {vendor_panel.get('link', 'غير متاح')}\n"
                if vendor_panel.get('email'):
                    text += f"   📧 Email: `{vendor_panel['email']}`\n"
                if vendor_panel.get('password'):
                    text += f"   🔑 Password: `{vendor_panel['password']}`\n"

                # حسابات متعددة
                accounts = vendor_panel.get('accounts', [])
                for i, account in enumerate(accounts, 1):
                    text += f"   📧 Account {i}: `{account.get('email', '')}`\n"
                    text += f"   🔑 Password: `{account.get('password', '')}`\n"
                text += "\n"
            
            # لوحة المدرب
            instructor_panel = demo.get("instructor_panel")
            if instructor_panel:
                text += f"👨‍🏫 *لوحة المدرب:*\n"
                text += f"   {instructor_panel.get('link', 'غير متاح')}\n"
                if instructor_panel.get('email'):
                    text += f"   📧 Email: `{instructor_panel['email']}`\n"
                if instructor_panel.get('password'):
                    text += f"   🔑 Password: `{instructor_panel['password']}`\n"
                text += "\n"

            # لوحة الطالب
            student_panel = demo.get("student_panel")
            if student_panel:
                text += f"👨‍🎓 *لوحة الطالب:*\n"
                text += f"   {student_panel.get('link', 'غير متاح')}\n"
                if student_panel.get('email'):
                    text += f"   📧 Email: `{student_panel['email']}`\n"
                if student_panel.get('password'):
                    text += f"   🔑 Password: `{student_panel['password']}`\n"
                text += "\n"

            # لوحة المنظمة
            organization_panel = demo.get("organization_panel")
            if organization_panel:
                text += f"🏢 *لوحة المنظمة:*\n"
                text += f"   {organization_panel.get('link', 'غير متاح')}\n"
                if organization_panel.get('email'):
                    text += f"   📧 Email: `{organization_panel['email']}`\n"
                if organization_panel.get('password'):
                    text += f"   🔑 Password: `{organization_panel['password']}`\n"
                text += "\n"

            # لوحة المستخدم
            user_panel = demo.get("user_panel")
            if user_panel:
                text += f"👤 *لوحة المستخدم:*\n"
                text += f"   {user_panel.get('link', 'غير متاح')}\n"
                if user_panel.get('email'):
                    text += f"   📧 Email: `{user_panel['email']}`\n"
                if user_panel.get('password'):
                    text += f"   🔑 Password: `{user_panel['password']}`\n"
                text += "\n"

            # لوحة الدليفري
            delivery_panel = demo.get("delivery_panel")
            if delivery_panel:
                text += f"🚛 *لوحة الدليفري:*\n"
                text += f"   {delivery_panel.get('link', 'غير متاح')}\n"
                if delivery_panel.get('email'):
                    text += f"   📧 Email: `{delivery_panel['email']}`\n"
                if delivery_panel.get('password'):
                    text += f"   🔑 Password: `{delivery_panel['password']}`\n"
                text += "\n"

            # تطبيق المستخدم
            user_app = demo.get("user_app")
            if user_app:
                text += f"📱 *تطبيق المستخدم:*\n"
                text += f"   [تحميل APK]({user_app.get('link', '#')})\n"
                if user_app.get('email'):
                    text += f"   📧 Email: `{user_app['email']}`\n"
                if user_app.get('password'):
                    text += f"   🔑 Password: `{user_app['password']}`\n"
                if user_app.get('phone'):
                    text += f"   📱 Phone: `{user_app['phone']}`\n"
                text += "\n"

            # تطبيق التاجر
            vendor_app = demo.get("vendor_app")
            if vendor_app:
                text += f"🏪 *تطبيق التاجر:*\n"
                text += f"   [تحميل APK]({vendor_app.get('link', '#')})\n"
                if vendor_app.get('email'):
                    text += f"   📧 Email: `{vendor_app['email']}`\n"
                if vendor_app.get('password'):
                    text += f"   🔑 Password: `{vendor_app['password']}`\n"
                text += "\n"

            # تطبيق الدليفري
            delivery_app = demo.get("delivery_app")
            if delivery_app:
                text += f"🚚 *تطبيق الدليفري:*\n"
                text += f"   [تحميل APK]({delivery_app.get('link', '#')})\n"
                if delivery_app.get('email'):
                    text += f"   📧 Email: `{delivery_app['email']}`\n"
                if delivery_app.get('password'):
                    text += f"   🔑 Password: `{delivery_app['password']}`\n"
                text += "\n"
        
        # إضافة خط فاصل بعد روابط الديمو
        if demo:
            text += "─" * 30 + "\n\n"

        # ملاحظات
        notes = project.get("notes")
        if notes:
            text += f"📝 *ملاحظات إضافية:*\n{notes}\n\n"
        
        return text
    
    @staticmethod
    def format_search_results(results: List[Dict[str, Any]], query: str) -> str:
        """تنسيق نتائج البحث"""
        if not results:
            return f"🔍 *نتائج البحث عن '{query}'*\n\n❌ لم يتم العثور على مشاريع مطابقة."
        
        text = f"🔍 *نتائج البحث عن '{query}'*\n"
        text += f"تم العثور على {len(results)} مشروع:\n\n"
        
        for i, project in enumerate(results[:MAX_PROJECTS_PER_MESSAGE], 1):
            price = project.get("price", {}).get("text", "غير محدد")
            category = project.get("category_id", "غير محدد")
            text += f"{i}️⃣ *{project.get('name', 'مشروع')}*\n"
            text += f"   💰 {price} | 📁 {category}\n"
            text += f"   {project.get('description', '')[:100]}...\n\n"
        
        if len(results) > MAX_PROJECTS_PER_MESSAGE:
            text += f"... و {len(results) - MAX_PROJECTS_PER_MESSAGE} نتيجة أخرى"
        
        return text
    
    @staticmethod
    def format_project_with_versions(project: Dict[str, Any]) -> str:
        """تنسيق المشروع مع إصداراته"""
        text = f"🛠️ *{project.get('name', 'مشروع')}*\n"
        text += f"— {project.get('description', 'لا يوجد وصف')}\n\n"
        
        # التقنيات
        technologies = project.get("technologies", [])
        if technologies:
            text += f"🧪 *التقنيات المستخدمة:*\n"
            for tech in technologies:
                text += f"• {tech}\n"
        
        # المميزات الأساسية
        features = project.get("features", [])
        if features:
            text += f"\n✨ *المميزات الأساسية:*\n"
            for feature in features:
                text += f"• {feature}\n"
        
        text += f"\n📋 *اختر الإصدار المناسب لك:*\n"
        
        return text
    
    @staticmethod
    def clean_text_for_markdown(text: str) -> str:
        """تنظيف النص من الرموز الخاصة التي تسبب مشاكل في Markdown"""
        if not text:
            return ""
        
        # إزالة الرموز الخاصة التي تسبب مشاكل في Markdown
        special_chars = ['_', '*', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        
        # إزالة أي رموز أخرى قد تسبب مشاكل
        text = text.replace('\\', '\\\\')
        return text

    @staticmethod
    def format_version_details(project: Dict[str, Any], version: Dict[str, Any]) -> str:
        """تنسيق تفاصيل الإصدار"""
        project_name = project.get('name', 'مشروع')
        version_name = version.get('name', 'إصدار')
        description = version.get('description', 'لا يوجد وصف')

        text = f"🛠️ *{project_name}*\n\n"
        text += f"📋 *الإصدار:* {version_name}\n\n"

        text += f"📝 *وصف الإصدار:*\n{description}\n\n"

        # السعر والوقت
        price = version.get("price", {})
        delivery_time = version.get("delivery_time")

        if price or delivery_time:
            text += "💼 *معلومات الطلب:*\n"
            if price:
                text += f"💰 السعر: {price.get('text', 'غير محدد')}\n"
            if delivery_time:
                text += f"⏰ مدة التسليم: {delivery_time}\n"
            text += "\n"
        
        # المميزات
        features = version.get("features", [])
        if features:
            text += f"\n✨ المميزات:\n"
            for feature in features:
                text += f"• {feature}\n"
        
        # إضافة روابط الديمو حسب نوع الإصدار
        demo = project.get("demo", {})
        if demo:
            text += f"🌐 *روابط الديمو والاختبار:*\n\n"

            # الموقع الرئيسي - متاح في جميع الإصدارات
            website = demo.get("website")
            if website:
                text += f"🔗 *الموقع الرئيسي:*\n   {website}\n\n"

            # لوحة الإدارة - متاحة في جميع الإصدارات
            admin_panel = demo.get("admin_panel")
            if admin_panel:
                text += f"⚙️ *لوحة الإدارة:*\n"
                text += f"   {admin_panel.get('link', 'غير متاح')}\n"
                if admin_panel.get('email'):
                    text += f"   📧 Email: `{admin_panel['email']}`\n"
                if admin_panel.get('password'):
                    text += f"   🔑 Password: `{admin_panel['password']}`\n"
                text += "\n"

            # لوحة التاجر - متاحة في Multi Vendor و Ready و 6Valley و MartVill
            vendor_panel = demo.get("vendor_panel")
            project_id = project.get("id", "")
            if vendor_panel and ("multi_vendor" in project_id or "ready" in project_id or "6valley" in project_id or "martvill" in project_id):
                text += f"🏪 *لوحة التاجر:*\n"
                text += f"   {vendor_panel.get('link', 'غير متاح')}\n"
                if vendor_panel.get('email'):
                    text += f"   📧 Email: `{vendor_panel['email']}`\n"
                if vendor_panel.get('password'):
                    text += f"   🔑 Password: `{vendor_panel['password']}`\n"
                text += "\n"

            # لوحة المستخدم - متاحة في MartVill
            user_panel = demo.get("user_panel")
            if user_panel and "martvill" in project_id:
                text += f"👤 *لوحة المستخدم:*\n"
                text += f"   {user_panel.get('link', 'غير متاح')}\n"
                if user_panel.get('email'):
                    text += f"   📧 Email: `{user_panel['email']}`\n"
                if user_panel.get('password'):
                    text += f"   🔑 Password: `{user_panel['password']}`\n"
                text += "\n"

            # لوحة الدليفري - متاحة في MartVill مع إدارة الدليفري
            delivery_panel = demo.get("delivery_panel")
            version_id = version.get("id", "")
            if delivery_panel and "martvill" in project_id and "with_delivery" in version_id:
                text += f"🚛 *لوحة الدليفري:*\n"
                text += f"   {delivery_panel.get('link', 'غير متاح')}\n"
                if delivery_panel.get('email'):
                    text += f"   📧 Email: `{delivery_panel['email']}`\n"
                if delivery_panel.get('password'):
                    text += f"   🔑 Password: `{delivery_panel['password']}`\n"
                text += "\n"
            
            # تطبيق المستخدم - متاح في الإصدارات التي تحتوي على تطبيق أو مشروع 6amMart
            user_app = demo.get("user_app")
            if user_app and ("with_user_app" in version.get("id", "") or "with_delivery" in version.get("id", "") or project_id == "6ammart"):
                text += f"📱 *تطبيق المستخدم:*\n"
                text += f"   {user_app.get('link', 'غير متاح')}\n"
                if user_app.get('email'):
                    text += f"   📧 Email: `{user_app['email']}`\n"
                if user_app.get('password'):
                    text += f"   🔑 Password: `{user_app['password']}`\n"
                text += "\n"
            
            # تطبيق التاجر - متاح في Multi Vendor و Ready مع تطبيق
            vendor_app = demo.get("vendor_app")
            project_id = project.get("id", "")
            version_id = version.get("id", "")

            # شروط عرض تطبيق التاجر
            show_vendor_app = (
                vendor_app and
                ("active_multi" in project_id or "multi_vendor" in project_id or "ready" in project_id or "6valley" in project_id or "martvill" in project_id or "6ammart" in project_id) and
                ("with_user_app" in version_id or "with_delivery" in version_id or project_id == "6ammart")
            )

            if show_vendor_app:
                text += f"🏪 *تطبيق التاجر:*\n"
                text += f"   {vendor_app.get('link', 'غير متاح')}\n"
                if vendor_app.get('email'):
                    text += f"   📧 Email: `{vendor_app['email']}`\n"
                if vendor_app.get('password'):
                    text += f"   🔑 Password: `{vendor_app['password']}`\n"
                text += "\n"

            # تطبيق الدليفري - متاح في الإصدارات التي تحتوي على نظام التوصيل أو مشروع 6amMart
            delivery_app = demo.get("delivery_app")
            if delivery_app and ("with_delivery" in version.get("id", "") or project_id == "6ammart"):
                text += f"🚚 *تطبيق الدليفري:*\n"
                text += f"   {delivery_app.get('link', 'غير متاح')}\n"
                if delivery_app.get('email'):
                    text += f"   📧 Email: `{delivery_app['email']}`\n"
                if delivery_app.get('password'):
                    text += f"   🔑 Password: `{delivery_app['password']}`\n"
                text += "\n"

            # إضافة خط فاصل بعد روابط الديمو
            text += "─" * 30 + "\n\n"
        
        return text
    
    @staticmethod
    def format_stats(stats: Dict[str, Any]) -> str:
        """تنسيق الإحصائيات"""
        text = "📊 *إحصائيات المشاريع*\n\n"
        
        text += f"📁 *الأقسام الرئيسية:* {stats.get('total_categories', 0)}\n"
        text += f"📂 *الأقسام الفرعية:* {stats.get('total_subcategories', 0)}\n"
        text += f"🛠️ *إجمالي المشاريع:* {stats.get('total_projects', 0)}\n\n"
        
        # المشاريع حسب القسم
        projects_by_category = stats.get("projects_by_category", {})
        if projects_by_category:
            text += "*المشاريع حسب القسم:*\n"
            for category, count in projects_by_category.items():
                text += f"• {category}: {count} مشروع\n"
        
        # نطاق الأسعار
        price_range = stats.get("price_range", {})
        if price_range.get("min") != float('inf'):
            text += f"\n💰 *نطاق الأسعار:*\n"
            text += f"• الأدنى: ${price_range.get('min', 0):,.0f}\n"
            text += f"• الأعلى: ${price_range.get('max', 0):,.0f}\n"
        
        # التقنيات المستخدمة
        technologies = stats.get("technologies", [])
        if technologies:
            text += f"\n🧪 *التقنيات المستخدمة:*\n"
            for tech in sorted(technologies):
                text += f"• {tech}\n"
        
        return text 