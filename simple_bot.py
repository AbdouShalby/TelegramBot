#!/usr/bin/env python3
"""
🤖 Simple Telegram Bot - إصدار مبسط للاختبار
"""

import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
from database import db
from formatters import MessageFormatter

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleBotTest:
    def __init__(self):
        self.formatter = MessageFormatter()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر البداية"""
        await update.message.reply_text(
            "👋 أهلاً! أنا بوت مشاريع الشركة 🚀\n\n"
            "استخدم /menu لعرض القائمة الرئيسية\n"
            "استخدم /stats لعرض الإحصائيات"
        )
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        
        keyboard.append([InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = self.formatter.format_main_menu()
        
        await update.message.reply_text(
            message_text, 
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر الإحصائيات"""
        stats = db.get_project_stats()
        stats_text = self.formatter.format_stats(stats)
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """التعامل مع الأزرار"""
        query = update.callback_query
        choice = query.data
        
        await query.answer()
        
        if choice == "stats":
            stats = db.get_project_stats()
            stats_text = self.formatter.format_stats(stats)
            
            keyboard = [[InlineKeyboardButton("🔙 العودة", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                stats_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif choice == "main_menu":
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
        
        elif choice.startswith("category_"):
            category_id = choice.split("_", 1)[1]
            category = db.get_category(category_id)
            
            if category:
                subcategories = db.get_subcategories(category_id)
                
                keyboard = []
                for subcategory_id, subcategory in subcategories.items():
                    icon = subcategory.get("icon", "📁")
                    name = subcategory.get("name", "قسم فرعي")
                    keyboard.append([InlineKeyboardButton(
                        f"{icon} {name}", 
                        callback_data=f"subcategory_{category_id}_{subcategory_id}"
                    )])
                
                keyboard.append([InlineKeyboardButton("🔙 العودة", callback_data="main_menu")])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                message_text = self.formatter.format_category_menu(category)
                
                await query.edit_message_text(
                    message_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        
        elif choice.startswith("subcategory_"):
            parts = choice.split("_", 2)
            if len(parts) >= 3:
                category_id = parts[1]
                subcategory_id = parts[2]
                
                projects = db.get_projects(category_id, subcategory_id)
                subcategory = db.get_subcategory(category_id, subcategory_id)
                
                if projects and subcategory:
                    keyboard = []
                    
                    for project in projects[:3]:  # أول 3 مشاريع فقط
                        project_name = project.get('name', 'مشروع')
                        if len(project_name) > 25:
                            project_name = project_name[:25]
                        
                        keyboard.append([InlineKeyboardButton(
                            f"🛠️ {project_name}", 
                            callback_data=f"project_{category_id}_{subcategory_id}_{project.get('id', '')}"
                        )])
                    
                    keyboard.append([InlineKeyboardButton("🔙 العودة", callback_data=f"category_{category_id}")])
                    
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    message_text = self.formatter.format_subcategory_menu(subcategory, projects, 0, 1)
                    
                    await query.edit_message_text(
                        message_text,
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )

async def main():
    """تشغيل البوت المبسط"""
    print("🚀 بدء تشغيل البوت المبسط...")
    
    bot = SimpleBotTest()
    
    # بناء التطبيق
    app = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", bot.start_command))
    app.add_handler(CommandHandler("menu", bot.menu_command))
    app.add_handler(CommandHandler("stats", bot.stats_command))
    app.add_handler(CallbackQueryHandler(bot.button_handler))
    
    print("✅ البوت جاهز للعمل!")
    print("📱 جرب الأوامر: /start /menu /stats")
    print("🛑 اضغط Ctrl+C لإيقاف البوت")
    
    # تشغيل البوت
    await app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل البوت: {e}")
        import traceback
        traceback.print_exc()
