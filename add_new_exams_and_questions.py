import csv
import json
import os
import re

EXAMS_CSV = r"primary-exam-system\Exams.csv"
BANK_CSV = r"primary-exam-system\Question_Bank.csv"
INDEX_HTML = r"primary-exam-system\Index.html"

# ==============================================================================
# 1. NEW EXAMS DATA
# ==============================================================================
new_exams = [
    # Foundational exams (ensuring complete 28 -> 32 sync)
    {
        "code": "EX_Y5_ENG_ADV01",
        "title": "English Grammar: Adverbials Mastery & Sentence Expansion (Diagnostic)",
        "grade": "Year 5 (G5)",
        "subject": "English Grammar",
        "count": "10",
        "duration": "20",
        "status": "ACTIVE",
        "form_url": "",
        "date": "2026-10-25",
        "type": "Diagnostic",
        "period": "W1"
    },
    {
        "code": "EX_Y6_ARB_PRIO01",
        "title": "Arabic Grammar: الأولويات والنكرة والمعرفة (Diagnostic)",
        "grade": "Grade 6 (G6)",
        "subject": "اللغة العربية",
        "count": "10",
        "duration": "20",
        "status": "ACTIVE",
        "form_url": "",
        "date": "2026-10-25",
        "type": "Diagnostic",
        "period": "W1"
    },
    {
        "code": "EX_Y6_ENG_FANTASY01",
        "title": "English Literature: Fantasy Genre & Reading Comprehension (Diagnostic)",
        "grade": "Grade 6 (G6)",
        "subject": "English Literature",
        "count": "10",
        "duration": "20",
        "status": "ACTIVE",
        "form_url": "",
        "date": "2026-10-25",
        "type": "Diagnostic",
        "period": "W1"
    },
    # BRAND NEW WEEK 7 & ICT EXAMS (Coligo live alignment)
    {
        "code": "EX_Y5_ICT_QUIZ01",
        "title": "Ali - ICT Assessment: Variables, Loops, Input/Output & Operators",
        "grade": "Year 5 (G5)",
        "subject": "ICT Computing",
        "count": "6",
        "duration": "12",
        "status": "ACTIVE",
        "form_url": "",
        "date": "2026-10-26",
        "type": "Milestone",
        "period": "W7"
    },
    {
        "code": "DAILY_Y5_ENG_W7D1",
        "title": "Ali - Day 1: Simple & Compound Sentences",
        "grade": "Year 5 (G5)",
        "subject": "English Grammar",
        "count": "5",
        "duration": "10",
        "status": "ACTIVE",
        "form_url": "",
        "date": "2026-10-26",
        "type": "Daily",
        "period": "W7"
    },
    {
        "code": "EX_Y6_ICT_QUIZ01",
        "title": "Mostafa - ICT Assessment: Programming Constructs & Flowcharts",
        "grade": "Grade 6 (G6)",
        "subject": "ICT Computing",
        "count": "6",
        "duration": "12",
        "status": "ACTIVE",
        "form_url": "",
        "date": "2026-10-26",
        "type": "Milestone",
        "period": "W7"
    },
    {
        "code": "DAILY_Y6_ARB_W7D1",
        "title": "Mostafa - Day 1: سر القوة والنجاح وأنواع الخبر",
        "grade": "Grade 6 (G6)",
        "subject": "اللغة العربية",
        "count": "5",
        "duration": "10",
        "status": "ACTIVE",
        "form_url": "",
        "date": "2026-10-26",
        "type": "Daily",
        "period": "W7"
    }
]

# ==============================================================================
# 2. NEW QUESTIONS DATA
# ==============================================================================
new_questions = [
    # --- Ali ICT (EX_Y5_ICT_QUIZ01) ---
    {
        "id": "Q_Y5_ICT_01",
        "grade": "Year 5 (G5)",
        "subject": "ICT Computing",
        "topic": "Computational Thinking: Variables & Loops",
        "text": "A named location in computer memory that stores data which can change during program execution is called a:",
        "type": "MCQ",
        "options": "Loop|Variable|Constant|Value",
        "correct": "Variable",
        "points": "1",
        "explanation": "A variable is like a labelled box in memory that holds a single piece of data (value) at any one time.",
        "exam_code": "EX_Y5_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y5_ICT_02",
        "grade": "Year 5 (G5)",
        "subject": "ICT Computing",
        "topic": "Computational Thinking: Variables & Loops",
        "text": "When choosing a name for a variable (such as student score or timer), the best practice is:",
        "type": "MCQ",
        "options": "Use a clear, meaningful name (e.g. score)|Use a random letter like X12|Make it an extremely long sentence|Leave it blank",
        "correct": "Use a clear, meaningful name (e.g. score)",
        "points": "1",
        "explanation": "Variable names should be meaningful and descriptive so anyone reading the code immediately understands its purpose.",
        "exam_code": "EX_Y5_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y5_ICT_03",
        "grade": "Year 5 (G5)",
        "subject": "ICT Computing",
        "topic": "Computational Thinking: Variables & Loops",
        "text": "What type of loop is used when we know in advance exactly how many times instructions must repeat (e.g. repeat 10 times)?",
        "type": "MCQ",
        "options": "Infinite loop|Count-controlled loop|Condition-controlled loop|Crash loop",
        "correct": "Count-controlled loop",
        "points": "1",
        "explanation": "A count-controlled loop repeats instructions a predetermined, specified number of times.",
        "exam_code": "EX_Y5_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Medium"
    },
    {
        "id": "Q_Y5_ICT_04",
        "grade": "Year 5 (G5)",
        "subject": "ICT Computing",
        "topic": "Computer Hardware: Input & Output",
        "text": "Which of the following devices acts as BOTH an Input and an Output device?",
        "type": "MCQ",
        "options": "Touchscreen|Keyboard|Speakers|Printer",
        "correct": "Touchscreen",
        "points": "1",
        "explanation": "A touchscreen detects finger touch input and also displays visual output on the same screen.",
        "exam_code": "EX_Y5_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y5_ICT_05",
        "grade": "Year 5 (G5)",
        "subject": "ICT Computing",
        "topic": "Scratch Programming: Operators",
        "text": "In Scratch, which color and shape of operator block reports a Boolean (True / False) result?",
        "type": "MCQ",
        "options": "Pointed green blocks (<, >, =)|Round blue blocks|Square yellow blocks|Oval purple blocks",
        "correct": "Pointed green blocks (<, >, =)",
        "points": "1",
        "explanation": "In Scratch, pointed (hexagonal) green blocks test conditions and report True or False.",
        "exam_code": "EX_Y5_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Medium"
    },
    {
        "id": "Q_Y5_ICT_06",
        "grade": "Year 5 (G5)",
        "subject": "ICT Computing",
        "topic": "Scratch Programming: Operators",
        "text": "If a Scratch block evaluates the expression: (8 * 7) - 16, what is the reported value?",
        "type": "MCQ",
        "options": "40|56|48|36",
        "correct": "40",
        "points": "1",
        "explanation": "8 * 7 = 56, and 56 - 16 = 40.",
        "exam_code": "EX_Y5_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Challenge"
    },

    # --- Ali English (DAILY_Y5_ENG_W7D1) ---
    {
        "id": "Q_Y5_ENG_W7D1_01",
        "grade": "Year 5 (G5)",
        "subject": "English Grammar",
        "topic": "Unit 2 - Lesson 2: Simple & Compound Sentences",
        "text": "Which of the following is a simple sentence?",
        "type": "MCQ",
        "options": "Mission control tracked the rocket.|The rocket launched, and the crowd cheered.|The crew cheered because the rocket had launched.|The engine was loud, yet the crew stayed calm.",
        "correct": "Mission control tracked the rocket.",
        "points": "1",
        "explanation": "A simple sentence consists of a single independent clause with one subject and verb predicate, expressing a complete thought.",
        "exam_code": "DAILY_Y5_ENG_W7D1",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y5_ENG_W7D1_02",
        "grade": "Year 5 (G5)",
        "subject": "English Grammar",
        "topic": "Unit 2 - Lesson 2: Simple & Compound Sentences",
        "text": "Which sentence is a compound sentence?",
        "type": "MCQ",
        "options": "Planets orbit the Sun, and moons orbit planets.|Space is cold and dark.|The astronauts waved to the crowd.|The crew trained hard because the mission was risky.",
        "correct": "Planets orbit the Sun, and moons orbit planets.",
        "points": "1",
        "explanation": "A compound sentence joins two independent clauses using a coordinating conjunction (FANBOYS) preceded by a comma.",
        "exam_code": "DAILY_Y5_ENG_W7D1",
        "week": "W7",
        "difficulty": "Medium"
    },
    {
        "id": "Q_Y5_ENG_W7D1_03",
        "grade": "Year 5 (G5)",
        "subject": "English Grammar",
        "topic": "Unit 2 - Lesson 2: Simple & Compound Sentences",
        "text": "Which acronym represents the seven coordinating conjunctions used to create compound sentences?",
        "type": "MCQ",
        "options": "FANBOYS (for, and, nor, but, or, yet, so)|ISAAC|PREFIX|CLAUSES",
        "correct": "FANBOYS (for, and, nor, but, or, yet, so)",
        "points": "1",
        "explanation": "FANBOYS is the mnemonic for the coordinating conjunctions: For, And, Nor, But, Or, Yet, So.",
        "exam_code": "DAILY_Y5_ENG_W7D1",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y5_ENG_W7D1_04",
        "grade": "Year 5 (G5)",
        "subject": "English Grammar",
        "topic": "Unit 2 - Lesson 2: Simple & Compound Sentences",
        "text": "Classify this sentence: 'Rockets are powerful, but they are expensive to build.'",
        "type": "MCQ",
        "options": "Compound sentence|Simple sentence with compound predicate|Complex sentence|Sentence fragment",
        "correct": "Compound sentence",
        "points": "1",
        "explanation": "It has two complete clauses ('Rockets are powerful' and 'they are expensive to build') joined by ', but'.",
        "exam_code": "DAILY_Y5_ENG_W7D1",
        "week": "W7",
        "difficulty": "Medium"
    },
    {
        "id": "Q_Y5_ENG_W7D1_05",
        "grade": "Year 5 (G5)",
        "subject": "English Grammar",
        "topic": "Unit 2 - Lesson 3: Adverbials of Time & Place",
        "text": "Identify the fronted adverbial of place in: 'Across the dusty launchpad, the engineers inspected the spacecraft.'",
        "type": "MCQ",
        "options": "Across the dusty launchpad|the engineers|inspected the spacecraft|dusty launchpad",
        "correct": "Across the dusty launchpad",
        "points": "1",
        "explanation": "'Across the dusty launchpad' is a prepositional phrase functioning as a fronted adverbial of place, followed by a comma.",
        "exam_code": "DAILY_Y5_ENG_W7D1",
        "week": "W7",
        "difficulty": "Challenge"
    },

    # --- Mostafa ICT (EX_Y6_ICT_QUIZ01) ---
    {
        "id": "Q_Y6_ICT_01",
        "grade": "Grade 6 (G6)",
        "subject": "ICT Computing",
        "topic": "Programming Constructs: Sequence, Selection, Iteration",
        "text": "A robot program moves forward 3 steps, turns right 90 degrees, and stops. Which programming construct is this?",
        "type": "MCQ",
        "options": "Sequence|Selection|Iteration|Variable",
        "correct": "Sequence",
        "points": "1",
        "explanation": "Sequence means executing instructions step-by-step, in the exact order they are written.",
        "exam_code": "EX_Y6_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y6_ICT_02",
        "grade": "Grade 6 (G6)",
        "subject": "ICT Computing",
        "topic": "Programming Constructs: Sequence, Selection, Iteration",
        "text": "A game checks: IF score >= 50 THEN display 'Winner!' ELSE display 'Try Again'. Which construct does this represent?",
        "type": "MCQ",
        "options": "Selection|Sequence|Iteration|Subroutine",
        "correct": "Selection",
        "points": "1",
        "explanation": "Selection uses condition testing (IF / ELSE) to choose which path of instructions to execute.",
        "exam_code": "EX_Y6_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y6_ICT_03",
        "grade": "Grade 6 (G6)",
        "subject": "ICT Computing",
        "topic": "Programming Constructs: Sequence, Selection, Iteration",
        "text": "A game sprite repeats a jumping animation 10 times in a row. What programming construct is being used?",
        "type": "MCQ",
        "options": "Iteration (Looping)|Selection|Sequence|Variable Assignment",
        "correct": "Iteration (Looping)",
        "points": "1",
        "explanation": "Iteration is repeating a block of instructions multiple times or until a condition is met.",
        "exam_code": "EX_Y6_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Medium"
    },
    {
        "id": "Q_Y6_ICT_04",
        "grade": "Grade 6 (G6)",
        "subject": "ICT Computing",
        "topic": "Algorithms & Flowcharts",
        "text": "What is the primary definition and purpose of a Flowchart in computer science?",
        "type": "MCQ",
        "options": "A visual diagram showing the logical steps of an algorithm|A type of hardware cable|A video game graphic|An operating system program",
        "correct": "A visual diagram showing the logical steps of an algorithm",
        "points": "1",
        "explanation": "A flowchart is a diagrammatic representation that visually displays the sequence and decision steps of an algorithm.",
        "exam_code": "EX_Y6_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y6_ICT_05",
        "grade": "Grade 6 (G6)",
        "subject": "ICT Computing",
        "topic": "Algorithms & Flowcharts",
        "text": "In a standard flowchart, which symbol represents an action or processing step (e.g. calculation)?",
        "type": "MCQ",
        "options": "Rectangle|Oval|Diamond|Parallelogram",
        "correct": "Rectangle",
        "points": "1",
        "explanation": "Rectangles represent processes/actions; Ovals represent Start/End; Diamonds represent decisions.",
        "exam_code": "EX_Y6_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Medium"
    },
    {
        "id": "Q_Y6_ICT_06",
        "grade": "Grade 6 (G6)",
        "subject": "ICT Computing",
        "topic": "Algorithms & Flowcharts",
        "text": "In a flowchart, what does a Diamond shape represent?",
        "type": "MCQ",
        "options": "A Decision point with Yes/No branches|Start of program|Output printing|Variable storage",
        "correct": "A Decision point with Yes/No branches",
        "points": "1",
        "explanation": "A diamond represents a conditional decision where the flow splits into different paths based on True/False or Yes/No.",
        "exam_code": "EX_Y6_ICT_QUIZ01",
        "week": "W7",
        "difficulty": "Challenge"
    },

    # --- Mostafa Arabic (DAILY_Y6_ARB_W7D1) ---
    {
        "id": "Q_Y6_ARB_W7D1_01",
        "grade": "Grade 6 (G6)",
        "subject": "اللغة العربية",
        "topic": "القواعد النحوية: أنواع الخبر",
        "text": "حدد نوع الخبر في الجملة التالية: «العلمُ نورٌ يضيءُ العقولَ».",
        "type": "MCQ",
        "options": "خبر مفرد|خبر جملة فعلية|خبر جملة اسمية|خبر شبه جملة",
        "correct": "خبر مفرد",
        "points": "1",
        "explanation": "كلمة «نورٌ» كلمة واحدة اسمية مفردة ليست جملة ولا شبه جملة، وتممت معنى المبتدأ فهو خبر مفرد مرفوع بالضمة.",
        "exam_code": "DAILY_Y6_ARB_W7D1",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y6_ARB_W7D1_02",
        "grade": "Grade 6 (G6)",
        "subject": "اللغة العربية",
        "topic": "القواعد النحوية: أنواع الخبر",
        "text": "ما نوع الخبر في جملة: «الحديقةُ أزهارُها متفتحةٌ»؟",
        "type": "MCQ",
        "options": "خبر جملة اسمية|خبر مفرد|خبر جملة فعلية|خبر شبه جملة ظرف",
        "correct": "خبر جملة اسمية",
        "points": "1",
        "explanation": "الخبر هنا جملة اسمية «أزهارها متفتحة» تشتمل على ضمير رابط (الهاء) يعود على المبتدأ الأول «الحديقة».",
        "exam_code": "DAILY_Y6_ARB_W7D1",
        "week": "W7",
        "difficulty": "Medium"
    },
    {
        "id": "Q_Y6_ARB_W7D1_03",
        "grade": "Grade 6 (G6)",
        "subject": "اللغة العربية",
        "topic": "القواعد النحوية: أنواع الخبر",
        "text": "عين الخبر ونوعه في جملة: «الطائرُ فوقَ الغصنِ».",
        "type": "MCQ",
        "options": "فوق الغصن (شبه جملة ظرف مكان)|الطائر (مفرد)|الغصن (مضاف إليه)|فوق (جملة فعلية)",
        "correct": "فوق الغصن (شبه جملة ظرف مكان)",
        "points": "1",
        "explanation": "«فوقَ» ظرف مكان شبه جملة في محل رفع خبر المبتدأ «الطائر».",
        "exam_code": "DAILY_Y6_ARB_W7D1",
        "week": "W7",
        "difficulty": "Medium"
    },
    {
        "id": "Q_Y6_ARB_W7D1_04",
        "grade": "Grade 6 (G6)",
        "subject": "اللغة العربية",
        "topic": "النصوص والقراءة: سر القوة والنجاح",
        "text": "في درس «سر القوة والنجاح»، ما الركيزة الأساسية لتحقيق التفوق وتخطي العقبات؟",
        "type": "MCQ",
        "options": "الإرادة والعزيمة الصادقة مع العمل الدؤوب|الاعتماد على الحظ والصدفة فقط|الاستسلام السريع عند أول صعوبة|تأجيل المهام إلى وقت لاحق",
        "correct": "الإرادة والعزيمة الصادقة مع العمل الدؤوب",
        "points": "1",
        "explanation": "الدرس يركز على أن سر النجاح ينبع من قوة الإرادة الداخلية والعزيمة والمثابرة في العمل والتطوير المستمر.",
        "exam_code": "DAILY_Y6_ARB_W7D1",
        "week": "W7",
        "difficulty": "Easy"
    },
    {
        "id": "Q_Y6_ARB_W7D1_05",
        "grade": "Grade 6 (G6)",
        "subject": "اللغة العربية",
        "topic": "التعبير الكتابي: كتابة تقرير",
        "text": "من العناصر الأساسية لكتابة التقرير المنظم في مهارات التعبير:",
        "type": "MCQ",
        "options": "العنوان والزمان والمكان والوقائع والتوصيات|القافية الشعرية والأوزان العروضية|الخيالات والقصص الخرافية غير الواقعية|ترك النص بدون خاتمة أو تاريخ",
        "correct": "العنوان والزمان والمكان والوقائع والتوصيات",
        "points": "1",
        "explanation": "التقرير وثيقة رسمية تتطلب تحديد العنوان والزمان والمكان وعرض الأحداث والوقائع بدقة واختتامها بالتوصيات والمقترحات.",
        "exam_code": "DAILY_Y6_ARB_W7D1",
        "week": "W7",
        "difficulty": "Challenge"
    }
]

print("Script template ready.")
