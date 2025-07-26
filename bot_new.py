import json
import logging
import asyncio
import time
import pytz
import sys
import os
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import JobQueue
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.error import Conflict, NetworkError, TimedOut

# Import our modules
from config import BOT_TOKEN, TRIGGER_WORDS, MESSAGE_DELAY
from database import db
from formatters import MessageFormatter

# Setup logging for server
log_filename = f"bot_log_{datetime.now().strftime('%Y%m%d')}.txt"
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProjectBot:
    """بوت مشاريع الشركة مع نظام أقسام متدرج"""
    
    def __init__(self):
        self.formatter = MessageFormatter()
        # تخزين رسائل البوت لكل جروب
        self.group_messages = {}
        # حماية من الطلبات المتكررة
        self.processing_groups = set()
        # إحصائيات البوت
        self.stats = {
            'start_time': datetime.now(),
            'total_requests': 0,
            'group_requests': 0,
            'private_requests': 0
        }
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر البداية"""
        self.stats['total_requests'] += 1
        if update.message.chat.type == 'private':
            self.stats['private_requests'] += 1
        else:
            self.stats['group_requests'] += 1
            
        await update.message.reply_text(
            "👋 أهلاً! أنا بوت مشاريع الشركة 🚀\n\n"
            "في الجروبات، قم بعمل منشن لي واكتب كلمة من الكلمات التالية:\n"
            f"• {' • '.join(TRIGGER_WORDS)}\n\n"
            "مثال: `@ProjectsDetailsBot ديموز`"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر المساعدة"""
        self.stats['total_requests'] += 1
        help_text = """🔧 *مساعدة بوت مشاريع الشركة*

*كيفية الاستخدام:*
1️⃣ في الجروبات: منشن البوت + كلمة مفتاحية
2️⃣ في الخاص: اكتب كلمة مفتاحية مباشرة

*الكلمات المفتاحية:*
• ديموز / demos
• مشاريع / projects
• بحث / search

*الأوامر المتاحة:*
/start - بدء البوت
/help - هذه الرسالة
/stats - إحصائيات المشاريع
/search - البحث في المشاريع

*مثال:* `@ProjectsDetailsBot ديموز`"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر الإحصائيات"""
        self.stats['total_requests'] += 1
        stats = db.get_project_stats()
        stats_text = self.formatter.format_stats(stats)
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر البحث"""
        self.stats['total_requests'] += 1
        query = ' '.join(context.args) if context.args else ''
        if not query:
            await update.message.reply_text(
                "🔍 *البحث في المشاريع*\n\n"
                "اكتب: `/search كلمة البحث`\n"
                "مثال: `/search Laravel`",
                parse_mode='Markdown'
            )
            return
        
        results = db.search_projects(query)
        results_text = self.formatter.format_search_results(results, query)
        await update.message.reply_text(results_text, parse_mode='Markdown')
    
    async def handle_mentions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """التعامل مع المنشن في الجروبات"""
        self.stats['total_requests'] += 1
        self.stats['group_requests'] += 1
        
        message = update.message
        text = message.text.lower()
        bot_username = (await context.bot.get_me()).username.lower()
        
        # التحقق من منشن البوت وكلمة مفتاحية
        if f"@{bot_username}" in text and any(word in text for word in TRIGGER_WORDS):
            # حماية من الطلبات المتكررة
            chat_id = message.chat_id
            if chat_id in self.processing_groups:
                await message.reply_text("⏳ جاري معالجة طلب سابق، يرجى الانتظار...")
                return
            
            self.processing_groups.add(chat_id)
            try:
                await self.show_main_menu(update, context, is_group=True)
            finally:
                # إزالة من قائمة المعالجة بعد ثانيتين
                asyncio.create_task(self.remove_from_processing(chat_id, 2))
    
    async def remove_from_processing(self, chat_id: int, delay: int):
        """إزالة الجروب من قائمة المعالجة بعد فترة"""
        await asyncio.sleep(delay)
        self.processing_groups.discard(chat_id)
    
    async def handle_private_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """التعامل مع الرسائل في الخاص"""
        self.stats['total_requests'] += 1
        self.stats['private_requests'] += 1
        
        message = update.message
        text = message.text.lower()
        
        # التحقق من الكلمات المفتاحية
        if any(word in text for word in TRIGGER_WORDS):
            await self.show_main_menu(update, context, is_group=False)
        else:
            # البحث المباشر
            results = db.search_projects(text)
            if results:
                results_text = self.formatter.format_search_results(results, text)
                await message.reply_text(results_text, parse_mode='Markdown')
            else:
                await message.reply_text(
                    "🔍 *البحث في المشاريع*\n\n"
                    "اكتب كلمة للبحث أو استخدم الكلمات المفتاحية:\n"
                    f"• {' • '.join(TRIGGER_WORDS)}",
                    parse_mode='Markdown'
                )
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, is_group: bool = False):
        """عرض القائمة الرئيسية"""
        categories = db.get_categories()
        
        keyboard = []
        for category_id, category in categories.items():
            icon = category.get("icon", "📁")
            name = category.get("name", "قسم")
            keyboard.append([InlineKeyboardButton(
                f"{icon} {name}", 
                callback_data=f"category_{category_id}"
            )])
        
        # إضافة زر الإحصائيات
        keyboard.append([InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = self.formatter.format_main_menu()
        
        if is_group:
            # في الجروبات: تحديث الرسالة الموجودة أو إنشاء رسالة جديدة
            chat_id = update.message.chat_id
            if chat_id in self.group_messages:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=self.group_messages[chat_id],
                        text=message_text,
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
                    return
                except Exception as e:
                    logger.warning(f"Failed to edit message: {e}")
                    # إذا فشل التحديث، احذف الرسالة القديمة
                    try:
                        await context.bot.delete_message(chat_id, self.group_messages[chat_id])
                    except:
                        pass
            
            # إرسال رسالة جديدة
            sent_message = await update.message.reply_text(
                message_text, 
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            # حفظ معرف الرسالة
            self.group_messages[chat_id] = sent_message.message_id
            
            # حذف الرسالة بعد 10 دقائق بدلاً من 5
            asyncio.create_task(self.delete_message_later(context, chat_id, sent_message.message_id, 600))
        else:
            # في الخاص: إرسال رسالة عادية
            sent_message = await update.message.reply_text(
                message_text, 
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def delete_message_later(self, context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, delay: int):
        """حذف الرسالة بعد فترة زمنية"""
        await asyncio.sleep(delay)
        try:
            await context.bot.delete_message(chat_id, message_id)
            # حذف من القاموس
            if chat_id in self.group_messages and self.group_messages[chat_id] == message_id:
                del self.group_messages[chat_id]
        except Exception as e:
            logger.warning(f"Failed to delete message: {e}")
    
    async def show_category_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, category_id: str):
        """عرض قائمة الأقسام الفرعية"""
        category = db.get_category(category_id)
        if not category:
            await update.callback_query.answer("❌ القسم غير موجود")
            return
        
        subcategories = db.get_subcategories(category_id)
        
        keyboard = []
        for subcategory_id, subcategory in subcategories.items():
            icon = subcategory.get("icon", "📁")
            name = subcategory.get("name", "قسم فرعي")
            keyboard.append([InlineKeyboardButton(
                f"{icon} {name}", 
                callback_data=f"subcategory_{category_id}_{subcategory_id}"
            )])
        
        # زر العودة للقائمة الرئيسية
        keyboard.append([InlineKeyboardButton("🔙 العودة", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = self.formatter.format_category_menu(category)
        
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_subcategory_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                  category_id: str, subcategory_id: str, page: int = 0):
        """عرض قائمة المشاريع مع pagination"""
        subcategory = db.get_subcategory(category_id, subcategory_id)
        if not subcategory:
            await update.callback_query.answer("❌ القسم الفرعي غير موجود")
            return
        
        projects = db.get_projects(category_id, subcategory_id)
        
        if not projects:
            await update.callback_query.answer("❌ لا توجد مشاريع")
            return
        
        # إعدادات Pagination
        projects_per_page = 3
        total_pages = (len(projects) + projects_per_page - 1) // projects_per_page
        start_index = page * projects_per_page
        end_index = min(start_index + projects_per_page, len(projects))
        current_projects = projects[start_index:end_index]
        
        keyboard = []
        
        # إضافة المشاريع للصفحة الحالية
        for i, project in enumerate(current_projects, start_index + 1):
            # تقصير اسم المشروع إذا كان طويلاً
            project_name = project.get('name', 'مشروع')
            if len(project_name) > 25:
                project_name = project_name[:25]
            
            keyboard.append([InlineKeyboardButton(
                f"🛠️ {project_name}", 
                callback_data=f"project_{category_id}_{subcategory_id}_{project.get('id', '')}"
            )])
        
        # أزرار التنقل
        nav_buttons = []
        
        # أزرار Pagination
        if total_pages > 1:
            pagination_row = []
            
            # زر السابق
            if page > 0:
                pagination_row.append(InlineKeyboardButton("⬅️ السابق", 
                    callback_data=f"page_{category_id}_{subcategory_id}_{page-1}"))
            
            # رقم الصفحة
            pagination_row.append(InlineKeyboardButton(f"📄 {page+1}/{total_pages}", 
                callback_data="no_action"))
            
            # زر التالي
            if page < total_pages - 1:
                pagination_row.append(InlineKeyboardButton("➡️ التالي", 
                    callback_data=f"page_{category_id}_{subcategory_id}_{page+1}"))
            
            keyboard.append(pagination_row)
        
        # أزرار إضافية
        nav_buttons.append(InlineKeyboardButton("🔙 العودة", 
            callback_data=f"category_{category_id}"))
        keyboard.append(nav_buttons)
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = self.formatter.format_subcategory_menu(subcategory, projects, page, total_pages)
        
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_project_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                 category_id: str, subcategory_id: str, project_id: str):
        """عرض تفاصيل المشروع مع إصداراته"""
        logger.info(f"Attempting to show project: {category_id}/{subcategory_id}/{project_id}")
        
        project = db.get_project(category_id, subcategory_id, project_id)
        if not project:
            logger.warning(f"Project not found: {category_id}/{subcategory_id}/{project_id}")
            await update.callback_query.answer("❌ المشروع غير موجود")
            return
        
        logger.info(f"Found project: {project.get('name', 'Unknown')}")
        
        # التحقق من وجود إصدارات
        versions = project.get("versions", [])
        if versions:
            # عرض إصدارات المشروع
            await self.show_project_versions(update, context, category_id, subcategory_id, project_id)
        else:
            # عرض تفاصيل المشروع العادية
            project_text = self.formatter.format_project_details(project)
            
            keyboard = [
                [InlineKeyboardButton("🔙 العودة", callback_data=f"subcategory_{category_id}_{subcategory_id}")],
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                await update.callback_query.edit_message_text(
                    project_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                logger.info(f"Successfully sent project details for: {project.get('name', 'Unknown')}")
            except Exception as e:
                logger.error(f"Error sending project details: {e}")
                await update.callback_query.answer("❌ حدث خطأ في إرسال التفاصيل")
    
    async def show_project_versions(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                  category_id: str, subcategory_id: str, project_id: str):
        """عرض إصدارات المشروع"""
        project = db.get_project(category_id, subcategory_id, project_id)
        versions = project.get("versions", [])
        
        if not versions:
            await update.callback_query.answer("❌ لا توجد إصدارات متاحة")
            return
        
        # تنسيق رسالة المشروع مع إصداراته
        project_text = self.formatter.format_project_with_versions(project)
        
        # إنشاء أزرار الإصدارات
        keyboard = []
        for version in versions:
            version_name = version.get('name', 'إصدار')
            price = version.get('price', {}).get('text', 'غير محدد')
            keyboard.append([InlineKeyboardButton(
                f"🛠️ {version_name} - {price}", 
                callback_data=f"version_{category_id}_{subcategory_id}_{project_id}_{version.get('id', '')}"
            )])
        
        # أزرار التنقل
        keyboard.append([
            InlineKeyboardButton("🔙 العودة", callback_data=f"subcategory_{category_id}_{subcategory_id}"),
            InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await update.callback_query.edit_message_text(
                project_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            logger.info(f"Successfully sent project versions for: {project.get('name', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error sending project versions: {e}")
            await update.callback_query.answer("❌ حدث خطأ في إرسال التفاصيل")
    
    async def show_version_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                 category_id: str, subcategory_id: str, project_id: str, version_id: str):
        """عرض تفاصيل إصدار محدد"""
        logger.info(f"Attempting to show version: {category_id}/{subcategory_id}/{project_id}/{version_id}")
        
        project = db.get_project(category_id, subcategory_id, project_id)
        version = db.get_project_version(category_id, subcategory_id, project_id, version_id)
        
        if not project or not version:
            logger.warning(f"Version not found: {category_id}/{subcategory_id}/{project_id}/{version_id}")
            await update.callback_query.answer("❌ الإصدار غير موجود")
            return
        
        logger.info(f"Found version: {version.get('name', 'Unknown')}")
        
        # تنسيق تفاصيل الإصدار
        version_text = self.formatter.format_version_details(project, version)
        
        keyboard = [
            [InlineKeyboardButton("🔙 العودة", callback_data=f"project_{category_id}_{subcategory_id}_{project_id}")],
            [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            # إضافة تأخير صغير لتجنب Flood control
            import asyncio
            await asyncio.sleep(0.5)
            
            await update.callback_query.edit_message_text(
                version_text,
                reply_markup=reply_markup,
                parse_mode=None
            )
            logger.info(f"Successfully sent version details for: {version.get('name', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error sending version details: {e}")
            await update.callback_query.answer("❌ حدث خطأ في إرسال التفاصيل")
    
    async def show_all_projects(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                               category_id: str, subcategory_id: str):
        """عرض جميع تفاصيل المشاريع"""
        projects = db.get_projects(category_id, subcategory_id)
        
        if not projects:
            await update.callback_query.answer("❌ لا توجد مشاريع")
            return
        
        # تجميع تفاصيل جميع المشاريع في رسالة واحدة
        all_projects_text = ""
        for i, project in enumerate(projects, 1):
            project_text = self.formatter.format_project_details(project)
            all_projects_text += f"📋 *المشروع {i} من {len(projects)}*\n\n{project_text}\n\n{'─' * 30}\n\n"
        
        # زر العودة
        keyboard = [
            [InlineKeyboardButton("🔙 العودة", callback_data=f"subcategory_{category_id}_{subcategory_id}")],
            [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await update.callback_query.edit_message_text(
                all_projects_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error sending all projects: {e}")
            await update.callback_query.answer("❌ حدث خطأ في إرسال التفاصيل")
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """التعامل مع الأزرار"""
        query = update.callback_query
        choice = query.data
        
        logger.info(f"Button pressed: {choice}")
        
        try:
            # الرد على callback query مع معالجة الأخطاء
            try:
                await query.answer()
            except Exception as e:
                logger.warning(f"Could not answer callback query: {e}")
                # تجاهل الخطأ والمتابعة
            if choice == "main_menu":
                # إعادة إنشاء القائمة الرئيسية
                categories = db.get_categories()
                
                keyboard = []
                for category_id, category in categories.items():
                    icon = category.get("icon", "📁")
                    name = category.get("name", "قسم")
                    keyboard.append([InlineKeyboardButton(
                        f"{icon} {name}", 
                        callback_data=f"category_{category_id}"
                    )])
                
                keyboard.append([InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                message_text = self.formatter.format_main_menu()
                
                await query.edit_message_text(
                    message_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif choice == "stats":
                stats = db.get_project_stats()
                stats_text = self.formatter.format_stats(stats)
                
                # إضافة زر العودة
                keyboard = [[InlineKeyboardButton("🔙 العودة", callback_data="main_menu")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    stats_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif choice.startswith("category_"):
                category_id = choice.split("_", 1)[1]
                await self.show_category_menu(update, context, category_id)
            
            elif choice.startswith("subcategory_"):
                parts = choice.split("_", 2)
                if len(parts) >= 3:
                    category_id = parts[1]
                    subcategory_id = parts[2]
                    await self.show_subcategory_menu(update, context, category_id, subcategory_id, 0)
            
            elif choice.startswith("page_"):
                parts = choice.split("_", 3)
                if len(parts) >= 4:
                    category_id = parts[1]
                    subcategory_id = parts[2]
                    page = int(parts[3])
                    await self.show_subcategory_menu(update, context, category_id, subcategory_id, page)
            
            elif choice.startswith("project_"):
                # تقسيم الـ callback data بشكل صحيح
                parts = choice.split("_", 1)  # تقسيم مرة واحدة فقط
                if len(parts) >= 2:
                    # استخراج باقي البيانات
                    remaining = parts[1]  # stores_single_vendor_active
                    remaining_parts = remaining.split("_")
                    
                    if len(remaining_parts) >= 3:
                        category_id = remaining_parts[0]  # stores
                        subcategory_id = remaining_parts[1] + "_" + remaining_parts[2]  # single_vendor
                        project_id = "_".join(remaining_parts[3:])  # active
                        
                        logger.info(f"Processing project request: {category_id}/{subcategory_id}/{project_id}")
                        await self.show_project_details(update, context, category_id, subcategory_id, project_id)
                    else:
                        logger.warning(f"Invalid project callback data structure: {choice}")
                        await query.answer("❌ بيانات غير صحيحة")
                else:
                    logger.warning(f"Invalid project callback data: {choice}")
                    await query.answer("❌ بيانات غير صحيحة")
            
            elif choice.startswith("version_"):
                # بنية بسيطة وثابتة للـ callback data
                parts = choice.split("_", 1)
                if len(parts) >= 2:
                    remaining = parts[1]  # stores_multi_vendor_martfury_website_only
                    remaining_parts = remaining.split("_")
                    
                    if len(remaining_parts) >= 4:
                        category_id = remaining_parts[0]  # stores
                        subcategory_id = remaining_parts[1] + "_" + remaining_parts[2]  # multi_vendor
                        
                        # بنية ثابتة: تحديد project_id و version_id بشكل صحيح
                        if len(remaining_parts) >= 5:
                            # تحديد version_id أولاً
                            version_id = None
                            project_id = None
                            
                            # البحث عن version_id من النهاية
                            if remaining_parts[-1] == "only" and remaining_parts[-2] == "website":
                                version_id = "website_only"
                                project_id = "_".join(remaining_parts[3:-2])
                            elif remaining_parts[-1] == "app" and remaining_parts[-2] == "user" and remaining_parts[-3] == "with":
                                version_id = "with_user_app"
                                project_id = "_".join(remaining_parts[3:-3])
                            elif remaining_parts[-1] == "delivery" and remaining_parts[-2] == "with":
                                version_id = "with_delivery"
                                project_id = "_".join(remaining_parts[3:-2])
                            else:
                                # محاولة عامة
                                project_id = remaining_parts[3]
                                version_id = "_".join(remaining_parts[4:])
                            
                            logger.info(f"Fixed parsing: project_id={project_id}, version_id={version_id}")
                            await self.show_version_details(update, context, category_id, subcategory_id, project_id, version_id)
                        else:
                            logger.warning(f"Invalid version callback data structure: {choice}")
                            await query.answer("❌ بيانات غير صحيحة")
                    else:
                        logger.warning(f"Invalid version callback data structure: {choice}")
                        await query.answer("❌ بيانات غير صحيحة")
                else:
                    logger.warning(f"Invalid version callback data: {choice}")
                    await query.answer("❌ بيانات غير صحيحة")
            
            elif choice.startswith("show_all_"):
                parts = choice.split("_", 3)
                if len(parts) >= 4:
                    category_id = parts[2]
                    subcategory_id = parts[3]
                    await self.show_all_projects(update, context, category_id, subcategory_id)
            
            elif choice == "no_action":
                # لا تفعل شيئاً للزر
                try:
                    await query.answer()
                except:
                    pass  # تجاهل الأخطاء للزر غير الفعال
            
            else:
                await query.answer("❌ خيار غير صحيح")
        
        except Exception as e:
            logger.error(f"Error in button handler: {e}")
            await query.answer("❌ حدث خطأ، حاول مرة أخرى")

async def main():
    """تشغيل البوت"""
    print("🚀 بدء تشغيل بوت مشاريع الشركة على السيرفر...")
    print(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 مجلد العمل: {os.getcwd()}")
    print(f"📝 ملف السجل: {log_filename}")
    
    try:
        bot = ProjectBot()
        
        # إعداد المجدول
        scheduler = AsyncIOScheduler(timezone=pytz.timezone("Africa/Cairo"))
        scheduler.start()
        
        # بناء التطبيق مع إعدادات الشبكة
        app = ApplicationBuilder().token(BOT_TOKEN).connect_timeout(30.0).read_timeout(30.0).write_timeout(30.0).build()
        
        # إضافة المعالجات
        app.add_handler(CommandHandler("start", bot.start_command))
        app.add_handler(CommandHandler("help", bot.help_command))
        app.add_handler(CommandHandler("stats", bot.stats_command))
        app.add_handler(CommandHandler("search", bot.search_command))
        
        # معالجات الرسائل
        bot_info = await app.bot.get_me()
        print(f"🤖 البوت: @{bot_info.username}")
        print(f"🆔 معرف البوت: {bot_info.id}")
        
        app.add_handler(MessageHandler(
            filters.TEXT & filters.ChatType.GROUPS & filters.Mention(bot_info.username),
            bot.handle_mentions
        ))
        app.add_handler(MessageHandler(
            filters.TEXT & filters.ChatType.PRIVATE,
            bot.handle_private_messages
        ))
        
        # معالج الأزرار
        app.add_handler(CallbackQueryHandler(bot.button_handler))
        
        print("✅ البوت جاهز للعمل على السيرفر!")
        print("📱 يمكنك الآن استخدام البوت في الجروبات أو الخاص")
        print("📊 السجل يتم حفظه في:", log_filename)
        print("🛑 اضغط Ctrl+C لإيقاف البوت")
        
        await app.run_polling(drop_pending_updates=True)
        
    except Conflict as e:
        print("❌ خطأ: هناك نسخة أخرى من البوت شغالة بالفعل!")
        print("💡 الحلول:")
        print("   1. استخدم stop_bot_server.bat لإيقاف النسخة الأخرى")
        print("   2. استخدم run_bot_server.bat لتشغيل نسخة جديدة")
        print("   3. انتظر دقيقة ثم حاول مرة أخرى")
        sys.exit(1)
        
    except NetworkError as e:
        print(f"❌ خطأ في الشبكة: {e}")
        print("💡 الحلول:")
        print("   1. تأكد من اتصال الإنترنت")
        print("   2. انتظر دقيقة ثم حاول مرة أخرى")
        print("   3. جرب استخدام VPN إذا كنت في منطقة محظورة")
        sys.exit(1)
    
    except TimedOut as e:
        print(f"❌ انتهت مهلة الاتصال: {e}")
        print("💡 الحلول:")
        print("   1. تأكد من سرعة الإنترنت")
        print("   2. انتظر دقيقة ثم حاول مرة أخرى")
        print("   3. جرب استخدام شبكة أخرى")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        print("💡 تأكد من صحة التوكن والإعدادات")
        print(f"📍 نوع الخطأ: {type(e).__name__}")
        import traceback
        print("📋 تفاصيل الخطأ:")
        traceback.print_exc()
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    import platform
    import nest_asyncio

    # تطبيق nest_asyncio للتوافق مع Windows
    nest_asyncio.apply()

    # إعداد event loop للـ Windows
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # إنشاء event loop جديد
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل البوت: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            loop.close()
        except:
            pass