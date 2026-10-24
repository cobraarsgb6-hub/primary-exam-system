# -*- coding: utf-8 -*-
import csv

questions = [
    {
        'id': 'Q_Y5_ENG_001',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'What is an adverbial?',
        'type': 'MCQ',
        'options': 'A single word naming a person or thing | A group of words without a verb that adds detail about time, place, or manner | A group of words with a subject and a verb | A word that joins two clauses together',
        'correct': 'A group of words without a verb that adds detail about time, place, or manner',
        'points': 1,
        'explanation': 'An adverbial is a word or phrase that gives more information about WHERE (place), WHEN (time), or HOW (manner) an action happens.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_002',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'In the sentence: "The rocket launched at dawn.", what type of adverbial is "at dawn"?',
        'type': 'MCQ',
        'options': 'Adverbial of Time | Adverbial of Place | Adverbial of Manner | Adverbial of Reason',
        'correct': 'Adverbial of Time',
        'points': 1,
        'explanation': '"At dawn" answers the question WHEN? did the rocket launch, so it is an adverbial of time.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_003',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Which of the following sentences contains an adverbial of PLACE?',
        'type': 'MCQ',
        'options': 'The crew slept inside the space station. | In 2000, the first crew moved in. | She carefully checked the controls. | Soon, the rocket was ready.',
        'correct': 'The crew slept inside the space station.',
        'points': 1,
        'explanation': '"Inside the space station" tells us WHERE they slept, making it an adverbial of place.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_004',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'An adverbial of MANNER answers which question?',
        'type': 'MCQ',
        'options': 'How or in what way? | Where? | When? | Who?',
        'correct': 'How or in what way?',
        'points': 1,
        'explanation': 'Adverbials of manner describe HOW something happens (e.g., with great care, bravely, quickly).',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_005',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Which sentence is punctuated correctly with a comma after the fronted adverbial?',
        'type': 'MCQ',
        'options': 'After a long journey, the crew landed. | After a long journey the crew landed. | After a long journey, the crew, landed. | After, a long journey the crew landed.',
        'correct': 'After a long journey, the crew landed.',
        'points': 1,
        'explanation': 'When an adverbial comes at the start of a sentence (fronted adverbial), it must be followed by a comma.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_006',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'True or False: In the sentence "The USSR launched Sputnik I in 1957.", we must put a comma before "in 1957".',
        'type': 'TRUE_FALSE',
        'options': 'True (صح) | False (خطأ)',
        'correct': 'False (خطأ)',
        'points': 1,
        'explanation': 'When the adverbial comes at the END of a sentence, no comma is needed. We only use a comma when it is at the START (fronted).',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_007',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Choose the sentence that has an adverbial of TIME at the beginning:',
        'type': 'MCQ',
        'options': 'Before sunrise, the pilot took off. | Bravely, the pilot flew the plane. | Over the sea, the pilot flew. | With great skill, the pilot landed.',
        'correct': 'Before sunrise, the pilot took off.',
        'points': 1,
        'explanation': '"Before sunrise" tells us WHEN the pilot took off, so it is an adverbial of time.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_008',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Complete the sentence with the best adverbial of manner: "The engineer repaired the delicate wiring ........"',
        'type': 'MCQ',
        'options': 'with great care | on the moon | at midnight | in 1969',
        'correct': 'with great care',
        'points': 1,
        'explanation': 'Delicate wiring needs careful handling, so "with great care" (manner) is the most logical fit.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_009',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Rewrite "Astronauts walked on the moon in 1969." by moving the adverbial of time to the start:',
        'type': 'MCQ',
        'options': 'In 1969, astronauts walked on the moon. | In 1969 astronauts walked on the moon. | On the moon, astronauts walked in 1969. | Astronauts in 1969 walked on the moon.',
        'correct': 'In 1969, astronauts walked on the moon.',
        'points': 1,
        'explanation': 'Moving "In 1969" to the front requires a comma immediately after it: "In 1969, astronauts walked on the moon."',
        'exam_code': 'EX_Y5_ENG_ADV01'
    },
    {
        'id': 'Q_Y5_ENG_010',
        'grade': 'الصف الخامس (Year 5)',
        'subject': 'English Grammar',
        'unit': 'Unit 2 - Lesson 3: Adverbials',
        'text': 'Which sentence has BOTH an adverbial of time AND an adverbial of place?',
        'type': 'MCQ',
        'options': 'In 1969, astronauts walked on the moon. | The rocket launched at dawn. | The crew worked inside the space station. | Bravely, the pilot flew the plane.',
        'correct': 'In 1969, astronauts walked on the moon.',
        'points': 1,
        'explanation': '"In 1969" is an adverbial of TIME, and "on the moon" is an adverbial of PLACE! Both exist in this sentence.',
        'exam_code': 'EX_Y5_ENG_ADV01'
    }
]

qb_path = r'C:\Users\co0ob\Projects\primary-exam-system\Question_Bank.csv'
ex_path = r'C:\Users\co0ob\Projects\primary-exam-system\Exams.csv'

with open(qb_path, 'a', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    for q in questions:
        writer.writerow([
            q['id'], q['grade'], q['subject'], q['unit'],
            q['text'], q['type'], q['options'], q['correct'],
            q['points'], q['explanation'], q['exam_code']
        ])

with open(ex_path, 'a', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'EX_Y5_ENG_ADV01',
        'Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)',
        'الصف الخامس (Year 5)',
        'English Grammar',
        10,
        20,
        'نشط',
        '',
        '2026-10-24'
    ])

print('Successfully appended 10 questions and registered exam EX_Y5_ENG_ADV01!')
