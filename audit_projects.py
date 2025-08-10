#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تدقيق المشاريع: يقارن بين جميع ملفات المشاريع المصدر وملف projects_new.json
ويعرض المشاريع المفقودة (غير الموجودة في الملف الموحد) بحسب القسم/القسم الفرعي.
"""

from __future__ import annotations

import json
import os
from typing import Dict, Any, Optional, Tuple, List

SOURCES = [
    "projects_old_broken.json",
    "projects_new_fixed.json",
    "projects_backup.json",
    "projects_broken_again.json",
    "projects_broken.json",
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

    # محاولة استخراج أقسام معروفة من ملف نصي جزئي
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lstrip("\ufeff")
        categories: Dict[str, Any] = {}
        for cat in KNOWN_CATEGORIES:
            key = f'"{cat}"'
            i = content.find(key)
            if i == -1:
                continue
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


def list_projects(data: Dict[str, Any]) -> List[Tuple[str, str, str, str]]:
    """يرجع قائمة (category_id, subcategory_id, project_id, project_name)"""
    out: List[Tuple[str, str, str, str]] = []
    cats = data.get("categories", {}) or {}
    for cat_id, cat in cats.items():
        subs = (cat or {}).get("subcategories", {}) or {}
        for sub_id, sub in subs.items():
            for p in (sub or {}).get("projects", []) or []:
                out.append((cat_id, sub_id, p.get("id", ""), p.get("name", "")))
    return out


def main() -> None:
    # تحميل الهدف
    with open(TARGET, "r", encoding="utf-8") as f:
        target = json.load(f)
    target_list = list_projects(target)
    target_keys = {(c, s, pid) for (c, s, pid, _) in target_list}

    # فحص المصادر وتجميع المشاريع
    missing: Dict[Tuple[str, str], List[Tuple[str, str]]] = {}
    totals_source = 0
    seen_source_keys = set()
    for src in SOURCES:
        if not os.path.exists(src):
            continue
        data = try_load(src)
        if not data:
            continue
        for (c, s, pid, name) in list_projects(data):
            key = (c, s, pid)
            if key in seen_source_keys:
                continue
            seen_source_keys.add(key)
            totals_source += 1
            if key not in target_keys and pid:
                missing.setdefault((c, s), []).append((pid, name))

    print("📊 Source total unique projects:", totals_source)
    print("📊 Target projects:", len(target_list))
    total_missing = sum(len(v) for v in missing.values())
    print("❗ Missing projects to import:", total_missing)
    if not missing:
        print("✅ لا توجد مشاريع ناقصة")
        return
    print("\n=== Missing by subcategory ===")
    for (c, s), plist in sorted(missing.items()):
        print(f"- {c}/{s}: {len(plist)}")
        # اطبع حتى 10 عناصر فقط للاختصار
        for pid, name in plist[:10]:
            print(f"  • {pid} - {name}")
        if len(plist) > 10:
            print(f"  ... +{len(plist)-10} more")


if __name__ == "__main__":
    main()


