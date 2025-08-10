#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

with open('projects_new.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

categories = data.get('categories', {})
for cat_id, cat in categories.items():
    print(f"[{cat_id}] {cat.get('name','')}")
    subs = (cat or {}).get('subcategories', {})
    for sub_id, sub in subs.items():
        projects = (sub or {}).get('projects', [])
        print(f"  - {sub_id}: {len(projects)} projects")
        for p in projects:
            print(f"    • {p.get('id','')} - {p.get('name','')}")


