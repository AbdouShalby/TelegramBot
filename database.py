import json
import logging
from typing import Dict, List, Optional, Any
from config import DATABASE_FILE

logger = logging.getLogger(__name__)

class ProjectDatabase:
    """نظام إدارة قاعدة بيانات المشاريع"""
    
    def __init__(self, database_file: str = DATABASE_FILE):
        self.database_file = database_file
        self.data = self._load_database()
    
    def _load_database(self) -> Dict[str, Any]:
        """تحميل قاعدة البيانات من الملف"""
        try:
            with open(self.database_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Database file {self.database_file} not found")
            return {"categories": {}}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing database file: {e}")
            return {"categories": {}}
    
    def _save_database(self) -> bool:
        """حفظ قاعدة البيانات إلى الملف"""
        try:
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving database: {e}")
            return False
    
    def get_categories(self) -> Dict[str, Any]:
        """الحصول على جميع الأقسام الرئيسية"""
        return self.data.get("categories", {})
    
    def get_category(self, category_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على قسم معين"""
        return self.data.get("categories", {}).get(category_id)
    
    def get_subcategories(self, category_id: str) -> Dict[str, Any]:
        """الحصول على الأقسام الفرعية لقسم معين"""
        category = self.get_category(category_id)
        if category:
            return category.get("subcategories", {})
        return {}
    
    def get_subcategory(self, category_id: str, subcategory_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على قسم فرعي معين"""
        subcategories = self.get_subcategories(category_id)
        return subcategories.get(subcategory_id)
    
    def get_projects(self, category_id: str, subcategory_id: str) -> List[Dict[str, Any]]:
        """الحصول على مشاريع قسم فرعي معين"""
        subcategory = self.get_subcategory(category_id, subcategory_id)
        if subcategory:
            return subcategory.get("projects", [])
        return []
    
    def get_project(self, category_id: str, subcategory_id: str, project_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على مشروع معين"""
        projects = self.get_projects(category_id, subcategory_id)
        for project in projects:
            if project.get("id") == project_id:
                return project
        return None
    
    def get_project_versions(self, category_id: str, subcategory_id: str, project_id: str) -> List[Dict[str, Any]]:
        """الحصول على إصدارات المشروع"""
        project = self.get_project(category_id, subcategory_id, project_id)
        if not project:
            return []
        
        return project.get("versions", [])
    
    def get_project_version(self, category_id: str, subcategory_id: str, project_id: str, version_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على إصدار محدد من المشروع"""
        versions = self.get_project_versions(category_id, subcategory_id, project_id)
        for version in versions:
            if version.get("id") == version_id:
                return version
        
        return None
    
    def search_projects(self, query: str) -> List[Dict[str, Any]]:
        """البحث في المشاريع"""
        results = []
        query = query.lower()
        
        for category_id, category in self.get_categories().items():
            for subcategory_id, subcategory in category.get("subcategories", {}).items():
                for project in subcategory.get("projects", []):
                    # البحث في اسم المشروع
                    if query in project.get("name", "").lower():
                        project["category_id"] = category_id
                        project["subcategory_id"] = subcategory_id
                        results.append(project)
                        continue
                    
                    # البحث في الوصف
                    if query in project.get("description", "").lower():
                        project["category_id"] = category_id
                        project["subcategory_id"] = subcategory_id
                        results.append(project)
                        continue
                    
                    # البحث في التقنيات
                    technologies = project.get("technologies", [])
                    if any(query in tech.lower() for tech in technologies):
                        project["category_id"] = category_id
                        project["subcategory_id"] = subcategory_id
                        results.append(project)
        
        return results
    
    def filter_projects_by_price(self, min_price: float = 0, max_price: float = float('inf')) -> List[Dict[str, Any]]:
        """تصفية المشاريع حسب السعر"""
        results = []
        
        for category_id, category in self.get_categories().items():
            for subcategory_id, subcategory in category.get("subcategories", {}).items():
                for project in subcategory.get("projects", []):
                    price = project.get("price", {}).get("amount", 0)
                    if min_price <= price <= max_price:
                        project["category_id"] = category_id
                        project["subcategory_id"] = subcategory_id
                        results.append(project)
        
        return results
    
    def filter_projects_by_technology(self, technology: str) -> List[Dict[str, Any]]:
        """تصفية المشاريع حسب التقنية"""
        results = []
        technology = technology.lower()
        
        for category_id, category in self.get_categories().items():
            for subcategory_id, subcategory in category.get("subcategories", {}).items():
                for project in subcategory.get("projects", []):
                    technologies = project.get("technologies", [])
                    if any(technology in tech.lower() for tech in technologies):
                        project["category_id"] = category_id
                        project["subcategory_id"] = subcategory_id
                        results.append(project)
        
        return results
    
    def get_project_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المشاريع"""
        stats = {
            "total_projects": 0,
            "total_categories": 0,
            "total_subcategories": 0,
            "projects_by_category": {},
            "price_range": {"min": float('inf'), "max": 0},
            "technologies": set()
        }
        
        categories = self.get_categories()
        stats["total_categories"] = len(categories)
        
        for category_id, category in categories.items():
            subcategories = category.get("subcategories", {})
            stats["total_subcategories"] += len(subcategories)
            category_projects = 0
            
            for subcategory_id, subcategory in subcategories.items():
                projects = subcategory.get("projects", [])
                category_projects += len(projects)
                stats["total_projects"] += len(projects)
                
                for project in projects:
                    # تحديث نطاق الأسعار
                    price = project.get("price", {}).get("amount", 0)
                    if price > 0:
                        stats["price_range"]["min"] = min(stats["price_range"]["min"], price)
                        stats["price_range"]["max"] = max(stats["price_range"]["max"], price)
                    
                    # جمع التقنيات
                    technologies = project.get("technologies", [])
                    stats["technologies"].update(technologies)
            
            stats["projects_by_category"][category.get("name", category_id)] = category_projects
        
        # تحويل set إلى list للـ JSON
        stats["technologies"] = list(stats["technologies"])
        
        return stats

# إنشاء instance عام لقاعدة البيانات
db = ProjectDatabase() 