# -*- coding: utf-8 -*-
"""
Update Code.gs with Mostafa's full English and Arabic exams.
"""

import json

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'r', encoding='utf-8') as f:
    code = f.read()

# Read questions from add_mostafa_exams.py
from add_mostafa_exams import mostafa_english_questions, mostafa_arabic_questions

formatted_q = []
for q in mostafa_english_questions + mostafa_arabic_questions:
    formatted_q.append(
        f"    [{json.dumps(q['id'], ensure_ascii=False)}, {json.dumps(q['grade'], ensure_ascii=False)}, {json.dumps(q['subject'], ensure_ascii=False)}, {json.dumps(q['unit'], ensure_ascii=False)}, {json.dumps(q['text'], ensure_ascii=False)}, {json.dumps(q['type'], ensure_ascii=False)}, {json.dumps(q['options'], ensure_ascii=False)}, {json.dumps(q['correct'], ensure_ascii=False)}, {q['points']}, {json.dumps(q['explanation'], ensure_ascii=False)}, {json.dumps(q['exam_code'], ensure_ascii=False)}]"
    )

new_questions_str = ",\n\n    // ==========================================\n    // Grade 6 (G6) - English & Arabic - For Mostafa Ahmed\n    // ==========================================\n" + ",\n".join(formatted_q)

# Target insertion before the end of sampleQuestions
old_target = "    ['Q_Y6_SCI_005', 'Grade 6 (G6)', 'Science', 'Unit 1: Cells as Systems', 'The flexible barrier that regulates the entry and exit of substances in and out of the cell is the:', 'MCQ', 'Cell Membrane | Cell Wall | Nuclear Membrane | Endoplasmic Reticulum', 'Cell Membrane', 1, '💡 Rule: The cell membrane is semi-permeable (selective). It allows nutrients and water to enter while blocking harmful waste.\\n\\n🌟 Examples of Selective Transport:\\n• Lets in: Oxygen, water, glucose.\\n• Pumps out: Carbon dioxide and waste products.\\n• Found in: BOTH plant and animal cells!', 'EX_Y6_SCI_CELL01']"

if old_target in code:
    code = code.replace(old_target, old_target + new_questions_str)

old_exams = """  const sampleExams = [
    ['EX_Y5_ENG_ADV01', 'Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)', 'Year 5 (G5)', 'English Grammar', 10, 20, 'نشط', '', new Date()],
    ['EX_Y6_SCI_CELL01', 'Grade 6 Science: Cells as Systems & Organelles (Unit 1)', 'Grade 6 (G6)', 'Science', 5, 15, 'نشط', '', new Date()]
  ];"""

new_exams = """  const sampleExams = [
    ['EX_Y5_ENG_ADV01', 'Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)', 'Year 5 (G5)', 'English Grammar', 10, 20, 'نشط', '', new Date()],
    ['EX_Y6_ENG_FANTASY01', 'Grade 6 English: Fantasy Reading "The City That Waited" & Grammar', 'Grade 6 (G6)', 'English Literacy', 10, 20, 'نشط', '', new Date()],
    ['EX_Y6_ARB_PRIO01', 'الصف السادس - لغة عربية: القراءة المتحررة، النكرة والمعرفة، والهمزة المتوسطة', 'Grade 6 (G6)', 'اللغة العربية', 10, 20, 'نشط', '', new Date()],
    ['EX_Y6_SCI_CELL01', 'Grade 6 Science: Cells as Systems & Organelles (Unit 1)', 'Grade 6 (G6)', 'Science', 5, 15, 'نشط', '', new Date()]
  ];"""

if old_exams in code:
    code = code.replace(old_exams, new_exams)

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully updated Code.gs with Mostafa exams!')
