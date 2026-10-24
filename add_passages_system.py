# -*- coding: utf-8 -*-
"""
Add Reading Passages to Code.gs (procedural generators) and Index.html.
"""

# Read Code.gs
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'r', encoding='utf-8') as f:
    code = f.read()

# Passages
eng_fantasy_passage = "The city was a hush. Pale light crept over the cobbles of the deserted square. In the courtyard, the old stone fountain whispered to itself as thin streams of water trickled into the basin. Its white walls glowed like the inside of a seashell in the twilight. High above, the iron gates closed with a mournful sigh, and shadows stretched along the walls, long and thin as fingers. No one walked the silent streets..."
eng_turtle_passage = "Sea turtles are in danger because people throw plastic and rubbish into the sea. People can stop throwing plastic into the sea and join beach clean-ups. People can also ask boats and ships not to dump rubbish into the ocean. Protecting sea turtles matters because they help keep the ocean healthy. If they disappear, marine ecosystems will suffer greatly."
arb_passage = "الوقتُ كنزٌ ثمينٌ وعطاءٌ إلهي عظيم، والنجاحُ في الحياة لا يتحقق بالأماني، وإنما بحسن إدارة يومنا وترتيب أولوياتنا. يتطلب إنجاز المهام وقتاً محدداً وتركيزاً حثيثاً، والبدء بالأهم قبل المهم. كما يحذر الخبراء من تبديد الوقت في المشتتات وتأجيل عمل اليوم إلى الغد، فالأشخاص الذين ينظمون أوقاتهم هم الأكثر قدرة على تحقيق طموحاتهم وخدمة وطنهم."

# Let's inspect where questions are returned in getExamData
# In Code.gs:
# questions.map(q => ({ id: q.id, grade: q.grade, subject: q.subject, unit: q.unit, text: q.text, type: q.type, options: q.options, points: q.points }))
# We must add passage: q.passage || ''

old_map = "points: q.points"
new_map = "points: q.points,\n      passage: q.passage || ''"
code = code.replace(old_map, new_map)

# In generateMostafaEnglishExam, add passages to questions
# Q1 to Q3 and Q9, Q10 get eng_fantasy_passage
# Q4 to Q8 get eng_turtle_passage
import re

# Update generateMostafaEnglishExam in Code.gs
fantasy_escaped = eng_fantasy_passage.replace('"', '\\"')
turtle_escaped = eng_turtle_passage.replace('"', '\\"')
arb_escaped = arb_passage.replace('"', '\\"')

# Insert constant definitions at the start of engine functions
passage_constants = f"""
const ENG_FANTASY_PASSAGE = "{fantasy_escaped}";
const ENG_TURTLE_PASSAGE = "{turtle_escaped}";
const ARB_READING_PASSAGE = "{arb_escaped}";
"""

code = code.replace('function generateMostafaEnglishExam() {', passage_constants + '\nfunction generateMostafaEnglishExam() {')

# Add passage property in Mostafa English
code = code.replace("unit: 'Unit 2: Fantasy Reading (The City That Waited)',", "unit: 'Unit 2: Fantasy Reading (The City That Waited)',\n    passage: ENG_FANTASY_PASSAGE,")
code = code.replace("unit: 'Unit 2: Report Writing (Sea Turtles)',", "unit: 'Unit 2: Report Writing (Sea Turtles)',\n    passage: ENG_TURTLE_PASSAGE,")

# Add passage property in Mostafa Arabic
code = code.replace("unit: 'القراءة المتحررة: فهم المقروء والمفردات',", "unit: 'القراءة المتحررة: فهم المقروء والمفردات',\n    passage: ARB_READING_PASSAGE,")
code = code.replace("unit: 'القراءة المتحررة: استيعاب المقروء',", "unit: 'القراءة المتحررة: استيعاب المقروء',\n    passage: ARB_READING_PASSAGE,")
code = code.replace("unit: 'القواعد النحوية: النكرة والمعرفة',", "unit: 'القواعد النحوية: النكرة والمعرفة',\n    passage: ARB_READING_PASSAGE,")

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Code.gs updated with passages!")

# Now update Index.html to render passage card
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add CSS for passage-box
passage_css = """
    /* Reading Passage Box */
    .passage-box {
      background: #f8fafc;
      border: 1.5px solid #cbd5e1;
      border-left: 5px solid var(--primary);
      border-radius: 12px;
      padding: 16px 18px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
    }

    .passage-box.rtl-content {
      border-left: 1.5px solid #cbd5e1;
      border-right: 5px solid var(--primary);
      direction: rtl;
      text-align: right;
      font-family: 'Cairo', sans-serif;
    }

    .passage-header {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.84rem;
      font-weight: 800;
      color: var(--primary);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 10px;
    }

    .passage-text {
      font-size: 0.98rem;
      line-height: 1.75;
      color: #1e293b;
      white-space: pre-wrap;
    }
"""

html = html.replace('/* Active Quiz Screen */', passage_css + '\n    /* Active Quiz Screen */')

# In renderQuizQuestion: check if q.passage exists and prepend it!
old_render = "box.innerHTML = `\n        <div class=\"q-meta-tag\">${q.unit || q.lesson || 'Core Curriculum'}</div>"

new_render = """
      let passageHtml = '';
      if (q.passage) {
        passageHtml = `
          <div class="passage-box ${isArabic ? 'rtl-content' : ''}">
            <div class="passage-header">
              <span>📖</span>
              <span>${isArabic ? 'نص القراءة (اقرأ الفقرة بعناية للإجابة عن الأسئلة):' : 'Reading Passage (Read carefully before answering):'}</span>
            </div>
            <div class="passage-text">${q.passage}</div>
          </div>
        `;
      }

      box.innerHTML = `
        ${passageHtml}
        <div class="q-meta-tag">${q.unit || q.lesson || 'Core Curriculum'}</div>"""

html = html.replace(old_render, new_render)

# In Parent Portal inspector: renderInspectQuestions
old_inspect = "<div style=\"font-size: 0.98rem; font-weight: 700; margin: 8px 0; color: var(--text-main);\">${q.text}</div>"
new_inspect = """${q.passage ? `<div class="passage-box ${q.passage.match(/[\\u0600-\\u06FF]/) ? 'rtl-content' : ''}" style="margin: 10px 0; padding: 10px 14px; font-size: 0.86rem;"><div style="font-weight:700; color:var(--primary); margin-bottom:4px;">📖 Reading Passage:</div>${q.passage}</div>` : ''}
          <div style="font-size: 0.98rem; font-weight: 700; margin: 8px 0; color: var(--text-main);">${q.text}</div>"""

html = html.replace(old_inspect, new_inspect)

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Index.html updated with passage rendering!")
