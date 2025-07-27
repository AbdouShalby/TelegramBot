"""
نظام حفظ السياق والاهتمامات للمستخدمين
يحفظ ما يبحث عنه المستخدم في الجروب لاستخدامه في الخاص
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class UserContextManager:
    """مدير السياق والاهتمامات للمستخدمين"""
    
    def __init__(self, context_file: str = "user_contexts.json"):
        self.context_file = context_file
        self.contexts = self._load_contexts()
        
    def _load_contexts(self) -> Dict[str, Any]:
        """تحميل السياقات المحفوظة"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading contexts: {e}")
        return {}
    
    def _save_contexts(self):
        """حفظ السياقات في الملف"""
        try:
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(self.contexts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving contexts: {e}")
    
    def save_user_interest(self, user_id: int, message_text: str, chat_type: str = "group"):
        """حفظ اهتمام المستخدم من رسالة في الجروب"""
        user_key = str(user_id)
        
        # استخراج الكلمات المفتاحية
        keywords = self._extract_keywords(message_text)
        
        if not keywords:
            return
            
        # إنشاء أو تحديث سياق المستخدم
        if user_key not in self.contexts:
            self.contexts[user_key] = {
                'keywords': [],
                'requests': [],
                'last_activity': None,
                'preferred_categories': []
            }
        
        # إضافة الكلمات الجديدة
        for keyword in keywords:
            if keyword not in self.contexts[user_key]['keywords']:
                self.contexts[user_key]['keywords'].append(keyword)
        
        # حفظ الطلب الأخير
        self.contexts[user_key]['requests'].append({
            'text': message_text,
            'timestamp': datetime.now().isoformat(),
            'chat_type': chat_type
        })
        
        # الاحتفاظ بآخر 5 طلبات فقط
        if len(self.contexts[user_key]['requests']) > 5:
            self.contexts[user_key]['requests'] = self.contexts[user_key]['requests'][-5:]
        
        self.contexts[user_key]['last_activity'] = datetime.now().isoformat()
        
        # حفظ التغييرات
        self._save_contexts()
        
        logger.info(f"Saved interest for user {user_id}: {keywords}")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """استخراج الكلمات المفتاحية من النص"""
        keywords = []
        text_lower = text.lower()
        
        # كلمات مفتاحية للتقنيات
        tech_keywords = {
            'laravel': 'Laravel',
            'php': 'PHP', 
            'flutter': 'Flutter',
            'react': 'React',
            'mysql': 'MySQL',
            'firebase': 'Firebase',
            'tailwind': 'Tailwind'
        }
        
        # كلمات مفتاحية للأقسام
        category_keywords = {
            'متجر': 'متاجر',
            'متاجر': 'متاجر',
            'مول': 'متاجر',
            'تسوق': 'متاجر',
            'توصيل': 'توصيل',
            'دليفري': 'توصيل',
            'طعام': 'توصيل الطعام',
            'مطعم': 'توصيل الطعام',
            'تعليم': 'تعليمية',
            'تعليمي': 'تعليمية',
            'كورس': 'تعليمية',
            'موبايل': 'تطبيقات موبايل',
            'تطبيق': 'تطبيقات موبايل'
        }
        
        # البحث عن التقنيات
        for key, value in tech_keywords.items():
            if key in text_lower:
                keywords.append(value)
        
        # البحث عن الأقسام
        for key, value in category_keywords.items():
            if key in text_lower:
                keywords.append(value)
        
        return list(set(keywords))  # إزالة التكرار
    
    def get_user_context(self, user_id: int) -> Optional[Dict[str, Any]]:
        """الحصول على سياق المستخدم"""
        user_key = str(user_id)
        
        if user_key not in self.contexts:
            return None
            
        context = self.contexts[user_key].copy()
        
        # التحقق من انتهاء صلاحية السياق (24 ساعة)
        if context.get('last_activity'):
            last_activity = datetime.fromisoformat(context['last_activity'])
            if datetime.now() - last_activity > timedelta(hours=24):
                # السياق منتهي الصلاحية
                return None
        
        return context
    
    def clear_user_context(self, user_id: int):
        """مسح سياق المستخدم"""
        user_key = str(user_id)
        if user_key in self.contexts:
            del self.contexts[user_key]
            self._save_contexts()
    
    def get_personalized_welcome(self, user_id: int) -> Optional[str]:
        """إنشاء رسالة ترحيب مخصصة بناءً على اهتمامات المستخدم"""
        context = self.get_user_context(user_id)
        
        if not context or not context.get('keywords'):
            return None
        
        keywords = context['keywords']
        last_request = context['requests'][-1]['text'] if context['requests'] else None
        
        welcome_msg = "🎉 أهلاً وسهلاً!\n\n"
        
        if last_request:
            welcome_msg += f"🔍 شوفت إنك كنت بتدور على: \"{last_request}\"\n\n"
        
        if keywords:
            welcome_msg += f"💡 بناءً على اهتماماتك في: {', '.join(keywords)}\n"
            welcome_msg += "دي أفضل المشاريع اللي ممكن تناسبك:\n\n"
        
        welcome_msg += "📋 اختر القسم اللي يهمك من القائمة أدناه:"
        
        return welcome_msg
    
    def cleanup_old_contexts(self):
        """تنظيف السياقات القديمة (أكثر من أسبوع)"""
        cutoff_date = datetime.now() - timedelta(days=7)
        users_to_remove = []
        
        for user_id, context in self.contexts.items():
            if context.get('last_activity'):
                last_activity = datetime.fromisoformat(context['last_activity'])
                if last_activity < cutoff_date:
                    users_to_remove.append(user_id)
        
        for user_id in users_to_remove:
            del self.contexts[user_id]
        
        if users_to_remove:
            self._save_contexts()
            logger.info(f"Cleaned up {len(users_to_remove)} old contexts")

# إنشاء مثيل عام
context_manager = UserContextManager()
