import os
import shutil

src = r'C:\Users\co0ob\.gemini\antigravity\brain\54d05bb7-093a-4520-bc55-e8fbc272480c\nagwa_portal_preview.html'
dest = r'C:\Users\co0ob\Projects\primary-exam-system\index.html'
legacy_dest = r'C:\Users\co0ob\Projects\primary-exam-system\legacy_index.html'

# Backup current index.html to legacy_index.html
if not os.path.exists(legacy_dest):
    shutil.copy2(dest, legacy_dest)
    print('Backed up to legacy_index.html')

with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. In Hero Banner: Add direct prominent link to Electricity Lab
old_hero_btn = '<button onclick="openSubjectModal(\'science\')" class="bg-white text-indigo-800 hover:bg-indigo-50 font-black text-sm px-6 py-3 rounded-xl shadow-lg transition-transform active:scale-95 flex items-center gap-2">'
new_hero_btn = '''<a href="resources/coligo/Mostafa/Science 106/Electricity_Mastery_Guide_Stage6.html" class="bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-sm px-6 py-3 rounded-xl shadow-lg transition-transform active:scale-95 flex items-center gap-2">
            <span>⚡ Launch Precision Circuit Lab</span>
            <span>&rarr;</span>
          </a>
          <button onclick="openSubjectModal('science')" class="bg-white/10 hover:bg-white/20 text-white font-bold text-sm px-4 py-3 rounded-xl border border-white/20 transition-all">'''

if old_hero_btn in content:
    content = content.replace(old_hero_btn, new_hero_btn, 1)
    print('Enhanced Hero button!')

# 2. In Science Card: Add Direct Lab Launch Pill
old_sc_p = '<p class="text-xs text-slate-500 font-medium mt-0.5">Electricity_(1).pptx (36 Slides) &bull; Series vs Parallel</p>'
new_sc_p = '''<p class="text-xs text-slate-500 font-medium mt-0.5">Electricity_(1).pptx (36 Slides) &bull; Series vs Parallel</p>
              <div class="mt-2">
                <a href="resources/coligo/Mostafa/Science 106/Electricity_Mastery_Guide_Stage6.html" onclick="event.stopPropagation()" class="inline-flex items-center gap-1.5 bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-300 px-3 py-1 rounded-lg text-xs font-black transition-colors">
                  <span>⚡</span>
                  <span>Open Interactive Physics Workbench</span>
                  <span>&rarr;</span>
                </a>
              </div>'''

if old_sc_p in content:
    content = content.replace(old_sc_p, new_sc_p, 1)
    print('Enhanced Science Card!')

# 3. In Top Bar: Add Link to Legacy Portal / Parent Portal
old_hdr_end = '<!-- Student Switcher -->'
new_hdr_btn = '''<div class="flex items-center gap-2 mr-2">
        <a href="legacy_index.html" class="text-xs font-bold text-slate-600 hover:text-indigo-600 bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-xl transition-colors flex items-center gap-1.5">
          <span>🔐</span>
          <span>Legacy Exams &amp; Parent Portal</span>
        </a>
      </div>
      <!-- Student Switcher -->'''

if old_hdr_end in content:
    content = content.replace(old_hdr_end, new_hdr_btn, 1)
    print('Enhanced Top Bar!')

with open(dest, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated index.html with Nagwa Calm Hub successfully!')
