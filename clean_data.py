# -*- coding: utf-8 -*-
import csv

qb_path = r'C:\Users\co0ob\Projects\primary-exam-system\Question_Bank.csv'
ex_path = r'C:\Users\co0ob\Projects\primary-exam-system\Exams.csv'

questions = [
    # Year 5 - Ali Ahmed
    {
        'id': 'Q_Y5_ENG_001', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'What is an adverbial?', 'type': 'MCQ',
        'options': 'A single word naming a person or thing | A group of words without a verb that adds detail about time, place, or manner | A group of words with a subject and a verb | A word that joins two clauses together',
        'correct': 'A group of words without a verb that adds detail about time, place, or manner', 'points': 1,
        'explanation': 'An adverbial is a word or phrase that gives extra details about WHEN, WHERE, or HOW an action happens. It does NOT contain a finite verb.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_002', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'In the sentence: "The rocket launched at dawn.", what type of adverbial is "at dawn"?', 'type': 'MCQ',
        'options': 'Adverbial of Time | Adverbial of Place | Adverbial of Manner | Adverbial of Reason',
        'correct': 'Adverbial of Time', 'points': 1,
        'explanation': '"at dawn" tells us WHEN the rocket launched (Adverbial of Time).',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_003', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Which of the following sentences contains an adverbial of PLACE?', 'type': 'MCQ',
        'options': 'The crew slept inside the space station. | In 2000, the first crew moved in. | She carefully checked the controls. | Soon, the rocket was ready.',
        'correct': 'The crew slept inside the space station.', 'points': 1,
        'explanation': '"inside the space station" answers the question WHERE did the crew sleep (Adverbial of Place).',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_004', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'An adverbial of MANNER answers which question?', 'type': 'MCQ',
        'options': 'How or in what way? | Where? | When? | Who?',
        'correct': 'How or in what way?', 'points': 1,
        'explanation': 'Adverbials of manner explain HOW an action happens (e.g., bravely, with great care, silently).',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_005', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Which sentence is punctuated correctly with a comma after the fronted adverbial?', 'type': 'MCQ',
        'options': 'After a long journey, the crew landed. | After a long journey the crew landed. | After a long journey, the crew, landed. | After, a long journey the crew landed.',
        'correct': 'After a long journey, the crew landed.', 'points': 1,
        'explanation': 'When an adverbial is at the start (Fronted Adverbial), it must be followed by a comma.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_006', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'True or False: In the sentence "The USSR launched Sputnik I in 1957.", we must put a comma before "in 1957".', 'type': 'TRUE_FALSE',
        'options': 'True | False',
        'correct': 'False', 'points': 1,
        'explanation': 'When the adverbial is at the END of a sentence, NO comma is needed.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_007', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Choose the sentence that has an adverbial of TIME at the beginning:', 'type': 'MCQ',
        'options': 'Before sunrise, the pilot took off. | Bravely, the pilot flew the plane. | Over the sea, the pilot flew. | With great skill, the pilot landed.',
        'correct': 'Before sunrise, the pilot took off.', 'points': 1,
        'explanation': '"Before sunrise" tells us WHEN the pilot took off.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_008', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Complete the sentence with the best adverbial of manner: "The engineer repaired the delicate wiring ........"', 'type': 'MCQ',
        'options': 'with great care | on the moon | at midnight | in 1969',
        'correct': 'with great care', 'points': 1,
        'explanation': '"with great care" describes HOW the engineer repaired the wires.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_009', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Rewrite "Astronauts walked on the moon in 1969." by moving the adverbial of time to the start:', 'type': 'MCQ',
        'options': 'In 1969, astronauts walked on the moon. | In 1969 astronauts walked on the moon. | On the moon, astronauts walked in 1969. | Astronauts in 1969 walked on the moon.',
        'correct': 'In 1969, astronauts walked on the moon.', 'points': 1,
        'explanation': 'Move "In 1969" to the front and place a comma directly after it.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_010', 'grade': 'Year 5 (G5)', 'subject': 'English Grammar', 'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Which sentence has BOTH an adverbial of time AND an adverbial of place?', 'type': 'MCQ',
        'options': 'In 1969, astronauts walked on the moon. | The rocket launched at dawn. | The crew worked inside the space station. | Bravely, the pilot flew the plane.',
        'correct': 'In 1969, astronauts walked on the moon.', 'points': 1,
        'explanation': '"In 1969" is Time, and "on the moon" is Place.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },

    # Grade 6 Science - Mostafa Ahmed
    {
        'id': 'Q_Y6_SCI_001', 'grade': 'Grade 6 (G6)', 'subject': 'Science', 'unit': 'Unit 1: Cells as Systems',
        'text': 'Which organelle acts as the control center of the cell and directs all cell activities?', 'type': 'MCQ',
        'options': 'Nucleus | Mitochondria | Cell Membrane | Cytoplasm',
        'correct': 'Nucleus', 'points': 1,
        'explanation': 'The nucleus contains DNA and directs all activities of the cell.',
        'exam_code': 'EX_Y6_SCI_CELL01'
    },
    {
        'id': 'Q_Y6_SCI_002', 'grade': 'Grade 6 (G6)', 'subject': 'Science', 'unit': 'Unit 1: Cells as Systems',
        'text': 'The "powerhouse" of the cell responsible for producing energy through cellular respiration is the:', 'type': 'MCQ',
        'options': 'Mitochondria | Ribosome | Vacuole | Chloroplast',
        'correct': 'Mitochondria', 'points': 1,
        'explanation': 'Mitochondria produce cellular energy (ATP) by converting glucose and oxygen.',
        'exam_code': 'EX_Y6_SCI_CELL01'
    },
    {
        'id': 'Q_Y6_SCI_003', 'grade': 'Grade 6 (G6)', 'subject': 'Science', 'unit': 'Unit 1: Cells as Systems',
        'text': 'True or False: Plant cells have a rigid cell wall and chloroplasts, whereas animal cells do not.', 'type': 'TRUE_FALSE',
        'options': 'True | False',
        'correct': 'True', 'points': 1,
        'explanation': 'Plant cells have a cell wall and chloroplasts, while animal cells do not.',
        'exam_code': 'EX_Y6_SCI_CELL01'
    },
    {
        'id': 'Q_Y6_SCI_004', 'grade': 'Grade 6 (G6)', 'subject': 'Science', 'unit': 'Unit 1: Cells as Systems',
        'text': 'Which jelly-like substance fills the cell and holds the organelles in place?', 'type': 'MCQ',
        'options': 'Cytoplasm | Cell wall | Chlorophyll | Nucleus',
        'correct': 'Cytoplasm', 'points': 1,
        'explanation': 'Cytoplasm is the gel-like fluid that suspends cellular organelles.',
        'exam_code': 'EX_Y6_SCI_CELL01'
    },
    {
        'id': 'Q_Y6_SCI_005', 'grade': 'Grade 6 (G6)', 'subject': 'Science', 'unit': 'Unit 1: Cells as Systems',
        'text': 'The flexible barrier that regulates the entry and exit of substances in and out of the cell is the:', 'type': 'MCQ',
        'options': 'Cell Membrane | Cell Wall | Nuclear Membrane | Endoplasmic Reticulum',
        'correct': 'Cell Membrane', 'points': 1,
        'explanation': 'The cell membrane is semi-permeable and controls what enters and exits the cell.',
        'exam_code': 'EX_Y6_SCI_CELL01'
    }
]

headers = [
    'معرف السؤال', 'الصف الدراسي', 'المادة', 'الوحدة / الدرس',
    'نص السؤال', 'نوع السؤال', 'الخيارات (مفصولة بـ |)',
    'الإجابة الصحيحة', 'الدرجة', 'الشرح والتوضيح', 'كود الامتحان'
]

with open(qb_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for q in questions:
        writer.writerow([
            q['id'], q['grade'], q['subject'], q['unit'],
            q['text'], q['type'], q['options'], q['correct'],
            q['points'], q['explanation'], q['exam_code']
        ])

ex_headers = [
    'كود الامتحان', 'عنوان الامتحان', 'الصف الدراسي', 'المادة',
    'عدد الأسئلة', 'المدة (دقائق)', 'الحالة', 'رابط الحل للطلاب', 'تاريخ الإنشاء'
]

exams = [
    ['EX_Y5_ENG_ADV01', 'Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)', 'Year 5 (G5)', 'English Grammar', 10, 20, 'نشط', '', '2026-10-24'],
    ['EX_Y6_SCI_CELL01', 'Grade 6 Science: Cells as Systems & Organelles (Unit 1)', 'Grade 6 (G6)', 'Science', 5, 15, 'نشط', '', '2026-10-24']
]

with open(ex_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(ex_headers)
    for row in exams:
        writer.writerow(row)

print('Cleaned Question_Bank.csv and Exams.csv - 100% International English!')
