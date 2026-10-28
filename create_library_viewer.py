import os
import json

OUTPUT_DIR = r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo"
CATALOG_PATH = os.path.join(OUTPUT_DIR, "coligo_catalog.json")
LINKS_PATH = os.path.join(OUTPUT_DIR, "all_links_and_notes.json")
VIEWER_PATH = os.path.join(OUTPUT_DIR, "view_coligo_library.html")

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    cat = json.load(f)

links_and_notes = []
if os.path.exists(LINKS_PATH):
    with open(LINKS_PATH, "r", encoding="utf-8") as f:
        links_and_notes = json.load(f)

# Group links/notes by student and course
extras = {"Ali": {}, "Mostafa": {}}
for item in links_and_notes:
    s = item["student"]
    c = item["course"]
    if s not in extras:
        extras[s] = {}
    if c not in extras[s]:
        extras[s][c] = []
    extras[s][c].append(item)

html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>مكتبة مدرسة منارة الإيمان - كوليجو (Ali & Mostafa)</title>
  <style>
    :root {{ --primary: #0284c7; --bg: #0f172a; --card: #1e293b; --text: #f8fafc; --muted: #94a3b8; --border: #334155; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    body {{ background: var(--bg); color: var(--text); padding: 24px; }}
    .header {{ text-align: center; margin-bottom: 20px; }}
    .header h1 {{ color: #38bdf8; font-size: 1.8rem; margin-bottom: 6px; }}
    .header p {{ color: var(--muted); font-size: 0.95rem; }}
    .stats-bar {{ display: flex; gap: 14px; justify-content: center; margin-bottom: 24px; flex-wrap: wrap; }}
    .stat-pill {{ background: var(--card); border: 1px solid var(--border); padding: 8px 16px; border-radius: 999px; font-weight: 700; font-size: 0.85rem; }}
    .tabs {{ display: flex; justify-content: center; gap: 12px; margin-bottom: 24px; }}
    .tab-btn {{ background: var(--card); color: var(--muted); border: 1.5px solid var(--border); padding: 10px 24px; border-radius: 8px; font-size: 1rem; font-weight: 800; cursor: pointer; transition: 0.2s; }}
    .tab-btn.active {{ background: var(--primary); color: #fff; border-color: var(--primary); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 18px; max-width: 1400px; margin: 0 auto; }}
    .course-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 18px; display: flex; flex-direction: column; }}
    .course-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 12px; }}
    .course-title {{ font-size: 1.15rem; font-weight: 800; color: #38bdf8; }}
    .file-count {{ background: #0369a1; color: #fff; font-size: 0.75rem; padding: 2px 8px; border-radius: 6px; font-weight: 700; }}
    .section-label {{ font-size: 0.8rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin: 10px 0 6px 0; border-top: 1px dashed var(--border); padding-top: 8px; }}
    .file-list {{ list-style: none; overflow-y: auto; max-height: 260px; }}
    .file-item {{ display: flex; justify-content: space-between; align-items: center; padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem; }}
    .file-link {{ color: #e2e8f0; text-decoration: none; display: flex; align-items: center; gap: 6px; }}
    .file-link:hover {{ color: #38bdf8; text-decoration: underline; }}
    .badge-ext {{ font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; font-weight: 800; background: #334155; }}
    .ext-pdf {{ background: #dc2626; color: #fff; }}
    .ext-pptx {{ background: #ea580c; color: #fff; }}
    .ext-docx {{ background: #2563eb; color: #fff; }}
    .ext-mp4 {{ background: #16a34a; color: #fff; }}
    .ext-link {{ background: #8b5cf6; color: #fff; }}
    .ext-note {{ background: #f59e0b; color: #000; }}
    .note-box {{ background: rgba(245, 158, 11, 0.1); border-right: 3px solid #f59e0b; padding: 8px 12px; border-radius: 4px; margin-top: 6px; font-size: 0.85rem; color: #fde68a; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>📚 مكتبة مدرسة منارة الإيمان الشاملة (Coligo LMS Hub)</h1>
    <p>تشمل كافة الملفات، الكتب، بوكليت المدرسة، فيديوهات الشرح، الروابط الخارجية، وملاحظات وتصحيحات المعلمين</p>
  </div>
  <div class="stats-bar">
    <div class="stat-pill">⚡ تم التحديث: {cat['synced_at']}</div>
    <div class="stat-pill">📅 الفصل: {cat['semester']}</div>
    <div class="stat-pill" style="border-color: #38bdf8; color: #38bdf8;">📦 214 ملفاً تم تحميله على الجهاز</div>
    <div class="stat-pill" style="border-color: #8b5cf6; color: #8b5cf6;">🔗 25 رابط وملاحظة وتصحيح مرصودة</div>
  </div>
  <div class="tabs">
    <button class="tab-btn active" onclick="switchStudent('Ali')">👦 علي أحمد (Year 5A)</button>
    <button class="tab-btn" onclick="switchStudent('Mostafa')">🧑 مصطفى أحمد (Grade 6A)</button>
  </div>
  <div id="view-Ali" class="student-view">
    <div class="grid">
"""

for s_name in ["Ali", "Mostafa"]:
    s_data = cat["students"].get(s_name, {})
    courses = s_data.get("courses", [])
    if s_name == "Mostafa":
        html += """    </div>
  </div>
  <div id="view-Mostafa" class="student-view" style="display: none;">
    <div class="grid">
"""
    # Merge any courses that only had links
    all_c_titles = [c.get("title", "") for c in courses]
    for c_title_extra in extras.get(s_name, {}):
        if c_title_extra not in all_c_titles:
            courses.append({"title": c_title_extra, "files": []})

    for c in courses:
        c_title = c.get("title", "")
        files = c.get("files", [])
        c_extras = extras.get(s_name, {}).get(c_title, [])
        if not files and not c_extras:
            continue
        
        html += f"""      <div class="course-card">
        <div class="course-header">
          <span class="course-title">{c_title}</span>
          <span class="file-count">{len(files)} ملف | {len(c_extras)} روابط وملاحظات</span>
        </div>
"""
        if files:
            html += """        <div class="section-label">📁 الملفات والكتب والشيتات المحملة</div>
        <ul class="file-list">
"""
            for f in files:
                fname = f.get("filename", "")
                title = f.get("title", fname)
                local_path = f.get("local_path", "").replace("\\", "/")
                ext = os.path.splitext(fname)[-1].lower().replace(".", "")
                badge_class = f"ext-{ext}" if ext in ["pdf", "pptx", "docx", "mp4"] else ""
                html += f"""          <li class="file-item">
            <a class="file-link" href="file:///{local_path}" target="_blank">
              <span class="badge-ext {badge_class}">{ext.upper()}</span>
              <span>{title[:45]}</span>
            </a>
          </li>
"""
            html += """        </ul>
"""

        if c_extras:
            links = [x for x in c_extras if x["type"] == "@material-type/link" or x.get("url")]
            notes = [x for x in c_extras if x["type"] == "@material-type/note" or x.get("content")]
            
            if links:
                html += """        <div class="section-label">🔗 روابط وفيديوهات الشرح المقررة</div>
        <ul class="file-list" style="max-height: 180px;">
"""
                for l in links:
                    url = l.get("url", "#")
                    title = l.get("title", "رابط شرح")
                    html += f"""          <li class="file-item">
            <a class="file-link" href="{url}" target="_blank" style="color: #c084fc;">
              <span class="badge-ext ext-link">LINK</span>
              <span>🎬 {title[:45]}</span>
            </a>
          </li>
"""
                html += """        </ul>
"""
            if notes:
                html += """        <div class="section-label">📝 ملاحظات وتصحيحات المعلمين الرسمية</div>
"""
                for n in notes:
                    title = n.get("title", "ملاحظة")
                    content = n.get("content", "") or n.get("description", "")
                    html += f"""        <div class="note-box">
          <strong>📌 {title}:</strong> {content}
        </div>
"""

        html += """      </div>
"""

html += """    </div>
  </div>
  <script>
    function switchStudent(name) {
      document.getElementById('view-Ali').style.display = name === 'Ali' ? 'block' : 'none';
      document.getElementById('view-Mostafa').style.display = name === 'Mostafa' ? 'block' : 'none';
      document.querySelectorAll('.tab-btn').forEach((btn, idx) => {
        btn.classList.toggle('active', (name === 'Ali' && idx === 0) || (name === 'Mostafa' && idx === 1));
      });
    }
  </script>
</body>
</html>"""

with open(VIEWER_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated Library Viewer with all links and teacher notes:", VIEWER_PATH)
