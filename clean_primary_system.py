import csv

# Clean Question_Bank.csv
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Question_Bank.csv', encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))
header = rows[0]

seen = set()
clean_qb = [header]
for r in rows[1:]:
    if not r or not r[0]:
        continue
    qid = r[0].strip()
    if qid and qid not in seen and not qid.startswith('Q_Y6_SCI'):
        seen.add(qid)
        clean_qb.append(r)

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Question_Bank.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(clean_qb)

print('Cleaned Question_Bank rows:', len(clean_qb) - 1)

# Clean Exams.csv
exams_data = [
    ['كود الامتحان', 'عنوان الامتحان', 'الصف الدراسي', 'المادة', 'عدد الأسئلة', 'المدة (دقائق)', 'الحالة', 'رابط الحل للطلاب', 'تاريخ الإنشاء'],
    ['EX_Y5_ENG_ADV01', 'Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)', 'Year 5 (G5)', 'English Grammar', '10', '20', 'نشط', '', '2026-10-24'],
    ['EX_Y6_ENG_FANTASY01', "Grade 6 English: Fantasy Reading 'The City That Waited' & Grammar", 'Grade 6 (G6)', 'English Literacy', '10', '20', 'نشط', '', '2026-10-24'],
    ['EX_Y6_ARB_PRIO01', 'الصف السادس - لغة عربية: القراءة المتحررة، النكرة والمعرفة، والهمزة المتوسطة', 'Grade 6 (G6)', 'اللغة العربية', '10', '20', 'نشط', '', '2026-10-24']
]
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Exams.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(exams_data)

print('Cleaned Exams count:', len(exams_data) - 1)
