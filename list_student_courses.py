import json, os

base = os.path.dirname(__file__)
path_cat = os.path.join(base, 'resources', 'coligo', 'coligo_catalog.json')
with open(path_cat, 'r', encoding='utf-8') as f:
    cat = json.load(f)

for st_id, st_data in cat.get('students', {}).items():
    print(f"=== STUDENT {st_id} ===")
    for c in st_data.get('courses', []):
        files_count = len(c.get('downloaded_files', []))
        links_count = len(c.get('links', []))
        print(f"  * {c.get('title')}: {c.get('total_items')} items ({files_count} files, {links_count} links)")
