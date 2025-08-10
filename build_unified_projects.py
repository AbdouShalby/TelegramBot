#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
إنشاء ملف مشاريع موحّد projects_new.json يحتوي جميع الأقسام المتاحة
بالاعتماد على أكثر ملف شامل أولاً، مع استخراج الأقسام حتى لو كان JSON جزئياً.

أولوية المصادر:
  1) projects_old_broken.json (غالباً يشمل كل الأقسام)
  2) projects_new_fixed.json
  3) projects_backup.json
  4) projects_broken_again.json
  5) projects_broken.json
  6) projects_new.json (الحالي)

نأخذ أول نسخة صالحة لكل قسم من قائمة المصادر بدون دمج معقّد لتسريع البناء.
"""

from __future__ import annotations

import json
import os
from typing import Dict, Any, Optional


SOURCES = [
    "projects_old_broken.json",
    "projects_new_fixed.json",
    "projects_backup.json",
    "projects_broken_again.json",
    "projects_broken.json",
    "projects_new.json",
]

TARGET = "projects_new.json"

KNOWN_CATEGORIES = ["stores", "education", "delivery", "business", "mobile"]


def try_load(path: str) -> Optional[Dict[str, Any]]:
    # محاولة تحميل JSON كامل
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        pass

    # محاولة استخراج بلوكات أقسام معروفة من ملف نصي جزئي
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lstrip("\ufeff")
        categories: Dict[str, Any] = {}
        for cat in KNOWN_CATEGORIES:
            key = f'"{cat}"'
            i = content.find(key)
            if i == -1:
                continue
            # ابحث عن أول '{' بعد المفتاح
            j = content.find("{", i)
            if j == -1:
                continue
            depth = 0
            end = None
            for k in range(j, len(content)):
                ch = content[k]
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        end = k
                        break
            if end is None:
                continue
            block = content[j:end+1]
            try:
                categories[cat] = json.loads(block)
            except Exception:
                continue
        if categories:
            return {"categories": categories}
    except Exception:
        pass
    return None


def main() -> None:
    # جمع أفضل نسخة لكل قسم حسب أولوية المصادر
    unified: Dict[str, Any] = {"categories": {}}

    for cat in KNOWN_CATEGORIES:
        # اختر أول ظهور للقسم
        chosen = None
        for src in SOURCES:
            if not os.path.exists(src):
                continue
            data = try_load(src)
            if not data or "categories" not in data:
                continue
            section = data["categories"].get(cat)
            if section:
                chosen = section
                break
        if chosen:
            unified["categories"][cat] = chosen

    # لو لم نجد أي قسم، لا نكتب شيئاً
    if not unified["categories"]:
        raise SystemExit("No categories could be extracted from sources")

    # كتابة الملف الموحّد
    with open(TARGET, "w", encoding="utf-8") as f:
        json.dump(unified, f, ensure_ascii=False, indent=2)

    # ملخّص
    print("✅ Unified projects written to", TARGET)
    print("📁 الأقسام:", ", ".join(unified["categories"].keys()))


if __name__ == "__main__":
    main()


