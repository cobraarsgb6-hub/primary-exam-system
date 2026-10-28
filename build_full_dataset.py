# -*- coding: utf-8 -*-
"""
Generates the pedagogical question bank, study plan, and exams catalog
with authentic Week, Lesson, Skill, and Difficulty distributions.
"""
import csv

def generate_questions():
    questions = []

    # =========================================================================
    # ALI AHMED - YEAR 5 (G5) - ENGLISH GRAMMAR
    # =========================================================================
    
    # --- WEEK 1: ADVERBIALS ---
    # Day 1: Adverbs of Manner
    questions.append([
        "Q_Y5_ENG_W1D1_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "What is an adverbial?", "MCQ",
        "A single word naming a person or thing | A group of words without a verb that adds detail about time, place, or manner | A group of words with a subject and a verb | A word that joins two clauses together",
        "A group of words without a verb that adds detail about time, place, or manner",
        1, "An adverbial is a word or phrase that gives extra details about WHEN, WHERE, or HOW an action happens. It does NOT contain a finite verb.",
        "DAILY_Y5_ENG_W1D1", "W1", "Easy", "Adverbs of Manner", "Identifying definition of adverbial"
    ])
    questions.append([
        "Q_Y5_ENG_W1D1_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "An adverbial of MANNER answers which question?", "MCQ",
        "How or in what way? | Where? | When? | Who?",
        "How or in what way?",
        1, "Adverbials of manner explain HOW an action happens (e.g., bravely, with great care, silently).",
        "DAILY_Y5_ENG_W1D1", "W1", "Easy", "Adverbs of Manner", "Purpose of manner adverbials"
    ])
    questions.append([
        "Q_Y5_ENG_W1D1_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Complete the sentence with the best adverbial of manner: 'The engineer repaired the delicate wiring ........'", "MCQ",
        "with great care | on the moon | at midnight | next Tuesday",
        "with great care",
        1, "'with great care' tells us HOW the engineer repaired the wiring (Manner).",
        "DAILY_Y5_ENG_W1D1", "W1", "Medium", "Adverbs of Manner", "Selecting appropriate manner adverbial"
    ])
    questions.append([
        "Q_Y5_ENG_W1D1_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "In the sentence: 'The astronaut floated silently through the hatch.', which word is an adverb of manner?", "MCQ",
        "silently | floated | astronaut | through",
        "silently",
        1, "'silently' is an adverb ending in -ly explaining how the astronaut floated.",
        "DAILY_Y5_ENG_W1D1", "W1", "Medium", "Adverbs of Manner", "Recognizing -ly manner adverbs"
    ])
    questions.append([
        "Q_Y5_ENG_W1D1_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Which phrase functions as a prepositional adverbial of MANNER?", "MCQ",
        "with furious determination | at three o'clock | behind the laboratory | tomorrow morning",
        "with furious determination",
        1, "'with furious determination' describes HOW something was done, acting as a manner adverbial.",
        "DAILY_Y5_ENG_W1D1", "W1", "Hard", "Adverbs of Manner", "Prepositional manner phrases"
    ])

    # Day 2: Adverbials of Time
    questions.append([
        "Q_Y5_ENG_W1D2_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "In the sentence: 'The rocket launched at dawn.', what type of adverbial is 'at dawn'?", "MCQ",
        "Adverbial of Time | Adverbial of Place | Adverbial of Manner | Adverbial of Reason",
        "Adverbial of Time",
        1, "'at dawn' tells us WHEN the rocket launched (Adverbial of Time).",
        "DAILY_Y5_ENG_W1D2", "W1", "Easy", "Adverbials of Time", "Identifying time adverbials"
    ])
    questions.append([
        "Q_Y5_ENG_W1D2_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Choose the sentence that has an adverbial of TIME at the beginning:", "MCQ",
        "Before sunrise, the pilot took off. | Bravely, the pilot flew the plane. | Over the sea, the pilot flew. | With great skill, the pilot landed.",
        "Before sunrise, the pilot took off.",
        1, "'Before sunrise' tells us WHEN the pilot took off.",
        "DAILY_Y5_ENG_W1D2", "W1", "Medium", "Adverbials of Time", "Fronted time adverbials"
    ])
    questions.append([
        "Q_Y5_ENG_W1D2_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "True or False: In the sentence 'The USSR launched Sputnik I in 1957.', we must put a comma before 'in 1957'.", "TRUE_FALSE",
        "True | False",
        "False",
        1, "When the adverbial is at the END of a sentence, NO comma is needed.",
        "DAILY_Y5_ENG_W1D2", "W1", "Medium", "Adverbials of Time", "Comma rules for end-sentence time adverbials"
    ])
    questions.append([
        "Q_Y5_ENG_W1D2_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Identify the adverbial of time in: 'Astronauts will explore Mars in the near future.'", "MCQ",
        "in the near future | explore Mars | Astronauts | will explore",
        "in the near future",
        1, "'in the near future' tells us WHEN the exploration will happen.",
        "DAILY_Y5_ENG_W1D2", "W1", "Medium", "Adverbials of Time", "Locating multi-word time adverbials"
    ])
    questions.append([
        "Q_Y5_ENG_W1D2_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Which of the following contains a dependent clause acting as a TIME adverbial?", "MCQ",
        "When the countdown reached zero, the engines ignited. | Inside the bunker, scientists cheered. | Extremely quickly, the vehicle surged forward. | Under the stars, the sky turned orange.",
        "When the countdown reached zero, the engines ignited.",
        1, "'When the countdown reached zero' is a time adverbial clause initiated by subordinating conjunction 'When'.",
        "DAILY_Y5_ENG_W1D2", "W1", "Hard", "Adverbials of Time", "Adverbial clauses of time"
    ])

    # Day 3: Adverbials of Place
    questions.append([
        "Q_Y5_ENG_W1D3_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Which of the following sentences contains an adverbial of PLACE?", "MCQ",
        "The crew slept inside the space station. | In 2000, the first crew moved in. | She carefully checked the controls. | Soon, the rocket was ready.",
        "The crew slept inside the space station.",
        1, "'inside the space station' answers the question WHERE did the crew sleep (Adverbial of Place).",
        "DAILY_Y5_ENG_W1D3", "W1", "Easy", "Adverbials of Place", "Identifying place adverbials"
    ])
    questions.append([
        "Q_Y5_ENG_W1D3_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "In the sentence: 'High above the clouds, the telescope captured distant galaxies.', what question does 'High above the clouds' answer?", "MCQ",
        "Where? | When? | How? | Why?",
        "Where?",
        1, "'High above the clouds' indicates WHERE the telescope was operating.",
        "DAILY_Y5_ENG_W1D3", "W1", "Medium", "Adverbials of Place", "Determining place function"
    ])
    questions.append([
        "Q_Y5_ENG_W1D3_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Select the sentence where an adverbial of place is correctly fronted with a comma:", "MCQ",
        "Across the lunar plains, rovers collected dust samples. | Across the lunar plains rovers collected dust samples. | Across the lunar, plains rovers collected dust samples. | Across the lunar plains rovers, collected dust samples.",
        "Across the lunar plains, rovers collected dust samples.",
        1, "Fronted adverbials of place require a comma immediately separating them from the main clause.",
        "DAILY_Y5_ENG_W1D3", "W1", "Medium", "Adverbials of Place", "Fronted place adverbials and commas"
    ])
    questions.append([
        "Q_Y5_ENG_W1D3_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Which phrase is an adverbial of PLACE?", "MCQ",
        "underneath the heavy machinery | yesterday afternoon | without making a sound | as soon as possible",
        "underneath the heavy machinery",
        1, "'underneath the heavy machinery' specifies spatial location (WHERE).",
        "DAILY_Y5_ENG_W1D3", "W1", "Medium", "Adverbials of Place", "Prepositional place phrases"
    ])
    questions.append([
        "Q_Y5_ENG_W1D3_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Identify the sentence that contains BOTH an adverbial of time AND an adverbial of place:", "MCQ",
        "At midnight, the satellite drifted into deep orbit. | At midnight, the clock struck twelve. | Into deep orbit, the rocket blasted. | With great power, the engines roared.",
        "At midnight, the satellite drifted into deep orbit.",
        1, "'At midnight' is time, and 'into deep orbit' is place.",
        "DAILY_Y5_ENG_W1D3", "W1", "Hard", "Adverbials of Place", "Compound time and place adverbials"
    ])

    # Day 4: Fronted Adverbials & Commas
    questions.append([
        "Q_Y5_ENG_W1D4_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Which sentence is punctuated correctly with a comma after the fronted adverbial?", "MCQ",
        "After a long journey, the crew landed. | After a long journey the crew landed. | After a long journey, the crew, landed. | After, a long journey the crew landed.",
        "After a long journey, the crew landed.",
        1, "When an adverbial is at the start (Fronted Adverbial), it must be followed by a comma.",
        "DAILY_Y5_ENG_W1D4", "W1", "Easy", "Fronted Adverbials", "Mandatory comma rule"
    ])
    questions.append([
        "Q_Y5_ENG_W1D4_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Rewrite 'Astronauts walked on the Moon in July 1969.' to begin with a FRONTED adverbial:", "MCQ",
        "In July 1969, astronauts walked on the Moon. | Astronauts walked in July 1969 on the Moon. | On the Moon walked astronauts in July 1969. | In July 1969 astronauts walked on the Moon.",
        "In July 1969, astronauts walked on the Moon.",
        1, "Move 'In July 1969' to the front and add a comma immediately after.",
        "DAILY_Y5_ENG_W1D4", "W1", "Medium", "Fronted Adverbials", "Sentence restructuring"
    ])
    questions.append([
        "Q_Y5_ENG_W1D4_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Why is a comma needed after a fronted adverbial?", "MCQ",
        "To separate the introductory adverbial phrase from the main clause for clarity | Because all sentences need two commas | To replace the verb | To indicate a question",
        "To separate the introductory adverbial phrase from the main clause for clarity",
        1, "A comma prevents misreading and clarifies the boundary between the introductory phrase and the independent clause.",
        "DAILY_Y5_ENG_W1D4", "W1", "Medium", "Fronted Adverbials", "Syntactic purpose of comma"
    ])
    questions.append([
        "Q_Y5_ENG_W1D4_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Which sentence has INCORRECT punctuation?", "MCQ",
        "Suddenly the meteor flashed across the sky. | Suddenly, the meteor flashed across the sky. | The meteor suddenly flashed across the sky. | Across the sky, the meteor flashed suddenly.",
        "Suddenly the meteor flashed across the sky.",
        1, "'Suddenly' is a fronted adverb of manner and requires a comma immediately following it.",
        "DAILY_Y5_ENG_W1D4", "W1", "Hard", "Fronted Adverbials", "Detecting missing comma"
    ])
    questions.append([
        "Q_Y5_ENG_W1D4_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "True or False: If an adverbial is placed in the middle of a sentence (parenthetical), commas may be needed on both sides.", "TRUE_FALSE",
        "True | False",
        "True",
        1, "An adverbial interrupting the flow in mid-sentence can be enclosed by a pair of commas (parenthesis).",
        "DAILY_Y5_ENG_W1D4", "W1", "Hard", "Fronted Adverbials", "Parenthetical adverbials"
    ])

    # Day 5 & 6: Synthesis, Compound & Error Hunting (Week 1 Milestone Pool)
    questions.append([
        "Q_Y5_ENG_W1D5_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Which sentence has BOTH an adverbial of time AND an adverbial of manner?", "MCQ",
        "At 8:00 AM, the crew worked tirelessly. | The rocket launched into orbit. | Astronauts ate inside the station. | Yesterday, the weather was sunny.",
        "At 8:00 AM, the crew worked tirelessly.",
        1, "'At 8:00 AM' is time; 'tirelessly' is manner.",
        "DAILY_Y5_ENG_W1D5", "W1", "Medium", "Compound Adverbials", "Recognizing multiple adverbial types"
    ])
    questions.append([
        "Q_Y5_ENG_W1D5_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials",
        "Fix the error: 'Without making a sound the stealth drone vanished into the clouds.' What is missing?", "MCQ",
        "A comma after 'sound' | A full stop after 'sound' | A comma after 'stealth' | A question mark",
        "A comma after 'sound'",
        1, "'Without making a sound' is a fronted manner adverbial phrase and must be followed by a comma.",
        "DAILY_Y5_ENG_W1D6", "W1", "Medium", "Error Hunting", "Repairing missing comma"
    ])

    # --- WEEK 2: RELATIVE CLAUSES ---
    # Day 8: Relative Pronouns (who, which, that, whose)
    questions.append([
        "Q_Y5_ENG_W2D8_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses",
        "Which relative pronoun is used specifically for PEOPLE?", "MCQ",
        "who | which | where | when",
        "who",
        1, "'who' (and 'whom') refers to people, while 'which' refers to things and animals.",
        "DAILY_Y5_ENG_W2D8", "W2", "Easy", "Relative Pronouns", "Pronoun selection for people"
    ])
    questions.append([
        "Q_Y5_ENG_W2D8_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses",
        "Complete the sentence: 'The spacesuit, ________ was designed by NASA, protected the astronaut.'", "MCQ",
        "which | who | whose | where",
        "which",
        1, "A spacesuit is an inanimate object, so the relative pronoun 'which' is required.",
        "DAILY_Y5_ENG_W2D8", "W2", "Easy", "Relative Pronouns", "Pronoun selection for objects"
    ])
    questions.append([
        "Q_Y5_ENG_W2D8_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses",
        "Which relative pronoun indicates POSSESSION?", "MCQ",
        "whose | who | whom | which",
        "whose",
        1, "'whose' shows ownership (e.g. 'the astronaut whose helmet cracked').",
        "DAILY_Y5_ENG_W2D8", "W2", "Medium", "Relative Pronouns", "Possessive relative pronouns"
    ])
    questions.append([
        "Q_Y5_ENG_W2D8_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses",
        "Select the correct relative pronoun: 'The astronomer ________ discovered the comet won an award.'", "MCQ",
        "who | which | where | whose",
        "who",
        1, "'astronomer' is a person, requiring 'who'.",
        "DAILY_Y5_ENG_W2D8", "W2", "Medium", "Relative Pronouns", "Subject relative pronoun"
    ])
    questions.append([
        "Q_Y5_ENG_W2D8_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses",
        "True or False: In formal UK English, 'which' is preferred over 'who' when referring to family pets with names.", "TRUE_FALSE",
        "True | False",
        "False",
        1, "Pets named or regarded as persons often take 'who', but formal grammar typically uses 'which/that' for animals unless personified.",
        "DAILY_Y5_ENG_W2D8", "W2", "Hard", "Relative Pronouns", "Nuances in animate antecedents"
    ])

    # Day 9 & 10: Defining vs Non-Defining Relative Clauses (Commas)
    questions.append([
        "Q_Y5_ENG_W2D9_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses",
        "What is the main function of a NON-DEFINING relative clause?", "MCQ",
        "It adds extra, non-essential information and is surrounded by commas | It defines exactly which noun is being spoken about without commas | It replaces the main subject of the sentence | It turns a sentence into a question",
        "It adds extra, non-essential information and is surrounded by commas",
        1, "Non-defining relative clauses provide extra detail that could be removed without making the sentence incomplete. They MUST be enclosed in commas.",
        "DAILY_Y5_ENG_W2D9", "W2", "Medium", "Non-defining Clauses", "Punctuation and function"
    ])
    questions.append([
        "Q_Y5_ENG_W2D9_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses",
        "Which sentence is punctuated correctly with commas around the relative clause?", "MCQ",
        "Neil Armstrong, who walked on the Moon, was an American hero. | Neil Armstrong who walked on the Moon was an American hero. | Neil Armstrong, who walked on the Moon was an American hero. | Neil Armstrong who walked on the Moon, was an American hero.",
        "Neil Armstrong, who walked on the Moon, was an American hero.",
        1, "Because 'Neil Armstrong' is already specific, the clause is non-defining and requires commas before AND after.",
        "DAILY_Y5_ENG_W2D9", "W2", "Hard", "Non-defining Clauses", "Enclosing comma pair"
    ])
    questions.append([
        "Q_Y5_ENG_W2D10_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses",
        "In: 'The rocket that was built in 1969 carried three astronauts.', why are there NO commas?", "MCQ",
        "Because it is a defining clause specifying which exact rocket carried them | Because commas are never used with 'rocket' | Because it is a short sentence | Because 'built' is past tense",
        "Because it is a defining clause specifying which exact rocket carried them",
        1, "Defining (restrictive) clauses identify the specific item and take no commas.",
        "DAILY_Y5_ENG_W2D10", "W2", "Hard", "Defining Clauses", "Distinguishing restrictive clauses"
    ])

    # --- WEEK 3: MODAL VERBS & COHESIVE DEVICES ---
    questions.append([
        "Q_Y5_ENG_W3D15_01", "Year 5 (G5)", "English Grammar", "Unit 3 - Lesson 1: Modal Verbs",
        "Which modal verb expresses CERTAINTY or strict obligation?", "MCQ",
        "must | might | could | perhaps",
        "must",
        1, "'must' expresses high certainty or obligation, whereas 'might' and 'could' express possibility.",
        "DAILY_Y5_ENG_W3D15", "W3", "Easy", "Modal Verbs", "Degrees of certainty"
    ])
    questions.append([
        "Q_Y5_ENG_W3D15_02", "Year 5 (G5)", "English Grammar", "Unit 3 - Lesson 1: Modal Verbs",
        "Select the modal verb that shows WEAK POSSIBILITY: 'The storm ________ delay the launch tomorrow.'", "MCQ",
        "might | will | must | definitely",
        "might",
        1, "'might' indicates an uncertain possibility (it could happen, or not).",
        "DAILY_Y5_ENG_W3D15", "W3", "Medium", "Modal Verbs", "Expressing possibility"
    ])
    questions.append([
        "Q_Y5_ENG_W3D16_01", "Year 5 (G5)", "English Grammar", "Unit 3 - Lesson 2: Cohesive Devices",
        "Which cohesive conjunction shows CONTRAST between two clauses?", "MCQ",
        "although | because | furthermore | therefore",
        "although",
        1, "'although' introduces a concession or contrast.",
        "DAILY_Y5_ENG_W3D16", "W3", "Medium", "Cohesion", "Contrast conjunctions"
    ])

    # --- WEEK 4: SYNTHESIS & COMPLEX SENTENCES ---
    questions.append([
        "Q_Y5_ENG_W4D22_01", "Year 5 (G5)", "English Grammar", "Unit 4 - Lesson 1: Complex Synthesis",
        "Identify the sentence combining an adverbial of time, a relative clause, and correct punctuation:", "MCQ",
        "Before dawn, the rover, which had recharged its battery, began moving. | Before dawn the rover which had recharged its battery began moving. | Before dawn, the rover who recharged its battery began moving. | Before dawn the rover, which recharged its battery, began moving.",
        "Before dawn, the rover, which had recharged its battery, began moving.",
        1, "Fronted adverbial 'Before dawn,' has a comma; non-defining clause ', which had recharged its battery,' has commas; 'which' refers to rover.",
        "DAILY_Y5_ENG_W4D22", "W4", "Hard", "Complex Synthesis", "Full syntactic integration"
    ])

    # =========================================================================
    # MOSTAFA AHMED - GRADE 6 (G6) - ARABIC LANGUAGE
    # =========================================================================
    
    # --- WEEK 1: النكرة والمعرفة + الهمزة المتوسطة على ألف + إدارة الوقت ---
    # Day 4: إدارة الوقت وترتيب الأولويات
    questions.append([
        "Q_Y6_ARB_W1D4_01", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات",
        "الفكرة الرئيسة لنص إدارة الوقت هي أن النجاح يتحقق من خلال:", "MCQ",
        "التخطيط المسبق وترتيب الأولويات | تأجيل الواجبات الصعبة | العمل طوال اليوم دون راحة | الاعتماد على الحظ",
        "التخطيط المسبق وترتيب الأولويات",
        1, "إدارة الوقت تبدأ بتحديد الأهداف وترتيب الأولويات والبدء بالمهام العاجلة والمهمة.",
        "DAILY_Y6_ARB_W1D4", "W1", "Easy", "استيعاب المقروء", "الفكرة الرئيسة"
    ])
    questions.append([
        "Q_Y6_ARB_W1D4_02", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات",
        "وفقاً لمصفوفة الأولويات (ستيفن كوفي)، أي المهام يجب البدء بها أولاً؟", "MCQ",
        "المهم والعاجل | غير المهم والعاجل | غير المهم وغير العاجل | الترفيه والتسلية",
        "المهم والعاجل",
        1, "مربع الأزمات والمهام الأساسية (المهم والعاجل) هو الذي يتطلب التنفيذ الفوري.",
        "DAILY_Y6_ARB_W1D4", "W1", "Medium", "إدارة الوقت", "مصفوفة الأولويات"
    ])
    questions.append([
        "Q_Y6_ARB_W1D4_03", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات",
        "مرادف كلمة (الإرجاء) في سياق: 'إرجاء الأعمال المهمة يقود إلى الإخفاق' هو:", "MCQ",
        "التأجيل والتسويف | الإسراع والتبكير | الإلغاء النهائي | التكرار",
        "التأجيل والتسويف",
        1, "أرجأ الشيء أي أخّره وأجّله.",
        "DAILY_Y6_ARB_W1D4", "W1", "Medium", "المفردات والدلالة", "معاني المفردات"
    ])
    questions.append([
        "Q_Y6_ARB_W1D4_04", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات",
        "مضاد كلمة (الحَثِيث) في عبارة: 'يبذل جهداً حثيثاً لإنجاز واجباته':", "MCQ",
        "البطيء والمتكاسل | السريع | القوي | المستمر",
        "البطيء والمتكاسل",
        1, "الحثيث تعني السريع الجاد، ومضادها البطيء المتواني.",
        "DAILY_Y6_ARB_W1D4", "W1", "Hard", "المفردات والدلالة", "المضاد اللغوي"
    ])
    questions.append([
        "Q_Y6_ARB_W1D4_05", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات",
        "علامَ يدل قول الكاتب: 'الوقت كالسيف إن لم تقطعه قطعك'؟", "MCQ",
        "أهمية اغتنام الوقت وحتمية مضيه دون رجوع | خطورة استخدام السيوف | ضرورة النوم مبكراً | صعوبة تنظيم اليوم",
        "أهمية اغتنام الوقت وحتمية مضيه دون رجوع",
        1, "التشبيه يؤكد أن الوقت لا ينتظر أحداً، وإما أن تستثمره أو ينقضي فيضرك ضياعه.",
        "DAILY_Y6_ARB_W1D4", "W1", "Hard", "البلاغة والتذوق", "دلالة التشبيه"
    ])

    # Day 5: النكرة والمعرفة
    questions.append([
        "Q_Y6_ARB_W1D5_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة",
        "عيّن الاسم المعرفة في جملة: 'قرأ التلميذُ كتاباً مفيداً':", "MCQ",
        "التلميذُ (معرف بأل) | كتاباً | مفيداً | قرأ",
        "التلميذُ (معرف بأل)",
        1, "(التلميذُ) اسم معرفة لأنه مقترن بأل التعريف، أما (كتاباً ومفيداً) فهما اسمان نكرتان.",
        "DAILY_Y6_ARB_W1D5", "W1", "Easy", "النكرة والمعرفة", "التمييز بين النكرة والمعرفة"
    ])
    questions.append([
        "Q_Y6_ARB_W1D5_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة",
        "الضمائر (أنا، نحن، هو، هي) وأسماء الإشارة والأسماء الموصولة كلها تعتبر:", "MCQ",
        "معارف دائماً | نكرات دائماً | حروفاً وليست أسماء | أفعالاً ماضية",
        "معارف دائماً",
        1, "الضمائر وأسماء الإشارة والأسماء الموصولة وأسماء الأعلام والمعرف بأل والمضاف إلى معرفة كلها معارف.",
        "DAILY_Y6_ARB_W1D5", "W1", "Easy", "النكرة والمعرفة", "أقسام المعارف"
    ])
    questions.append([
        "Q_Y6_ARB_W1D5_03", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة",
        "في جملة 'زارنا ضيفٌ كريمٌ'، الاسمان 'ضيفٌ' و 'كريمٌ':", "MCQ",
        "نكرتان لأنهما يدلان على غير معيّن ومنوّنان | معرفتان بأل | اسما إشارة | ضميران غائبان",
        "نكرتان لأنهما يدلان على غير معيّن ومنوّنان",
        1, "النكرة تدل على شيء غير محدد وتقبل التنوين.",
        "DAILY_Y6_ARB_W1D5", "W1", "Medium", "النكرة والمعرفة", "علامات النكرة"
    ])
    questions.append([
        "Q_Y6_ARB_W1D5_04", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة",
        "حوّل النكرة إلى معرفة بالإضافة في: 'قرأتُ كتاباً':", "MCQ",
        "قرأتُ كتابَ النحوِ | قرأتُ كتاباً جميلاً | قرأتُ كتباً | كتابٌ قرأته",
        "قرأتُ كتابَ النحوِ",
        1, "اكتسب الاسم النكرة (كتاب) التعريف بإضافته إلى المعرفة (النحو).",
        "DAILY_Y6_ARB_W1D5", "W1", "Medium", "النكرة والمعرفة", "المعرف بالإضافة"
    ])
    questions.append([
        "Q_Y6_ARB_W1D5_05", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة",
        "كم اسماً معرفة في جملة: 'هذا هو الطالبُ الذي فاز في المسابقةِ'؟", "MCQ",
        "5 أسماء معارف | 3 أسماء | معرفتان فقط | اسم واحد",
        "5 أسماء معارف",
        1, "المعارف هي: هذا (اسم إشارة)، هو (ضمير)، الطالب (معرف بأل)، الذي (اسم موصول)، المسابقة (معرف بأل).",
        "DAILY_Y6_ARB_W1D5", "W1", "Hard", "النكرة والمعرفة", "تعداد المعارف المتعددة"
    ])

    # Day 6: الهمزة المتوسطة على ألف
    questions.append([
        "Q_Y6_ARB_W1D6_01", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف",
        "ما سبب كتابة الهمزة على ألف في كلمة (يَسْـأَلُ)؟", "MCQ",
        "لأن الهمزة مفتوحة وما قبلها ساكن | لأن الهمزة مكسورة | لأن الهمزة مضمومة | لأن ما قبلها ألف مد",
        "لأن الهمزة مفتوحة وما قبلها ساكن",
        1, "في كلمة (يَسْـأَل): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون فترسم على ألف.",
        "DAILY_Y6_ARB_W1D6", "W1", "Easy", "الهمزة المتوسطة", "الهمزة المفتوحة بعد ساكن"
    ])
    questions.append([
        "Q_Y6_ARB_W1D6_02", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف",
        "اختر الرسم الإملائي الصحيح للكلمة: 'لا ........ عن مساعدة المحتاجين.'", "MCQ",
        "تَتَأَخَّرْ | تتأخر (بدون همزة) | تتءخر | تتآخر",
        "تَتَأَخَّرْ",
        1, "تَـتَـأَخَّـر (الهمزة مفتوحة وقبلها تاء مفتوحة فتُرسم على ألف).",
        "DAILY_Y6_ARB_W1D6", "W1", "Easy", "الهمزة المتوسطة", "الهمزة المفتوحة بعد فتح"
    ])
    questions.append([
        "Q_Y6_ARB_W1D6_03", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف",
        "ترسم الهمزة المتوسطة على ألف في ثلاث حالات، منها أن تكون:", "MCQ",
        "ساكنة بعد فتح (مثل رَأْس) | مكسورة بعد ضم | مضمومة بعد كسر | ساكنة بعد ضم",
        "ساكنة بعد فتح (مثل رَأْس)",
        1, "إذا كانت الهمزة ساكنة وما قبلها مفتوح، فإن الفتحة أقوى من السكون فتكتب على ألف.",
        "DAILY_Y6_ARB_W1D6", "W1", "Medium", "الهمزة المتوسطة", "الهمزة الساكنة بعد فتح"
    ])
    questions.append([
        "Q_Y6_ARB_W1D6_04", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف",
        "أي الكلمات الآتية كُتبت فيها الهمزة المتوسطة بصورة خاطئة؟", "MCQ",
        "مَسْئَلة | مَسْأَلة | فَأْس | مَأْوى",
        "مَسْئَلة",
        1, "الصواب (مسألة) لأن الهمزة مفتوحة بعد سين ساكنة فترسم على ألف وليس على نبرة.",
        "DAILY_Y6_ARB_W1D6", "W1", "Hard", "الهمزة المتوسطة", "اكتشاف الخطأ الإملائي"
    ])
    questions.append([
        "Q_Y6_ARB_W1D6_05", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف",
        "صوّب الخطأ الإملائي في الجملة: 'المؤمن لا يَـيْـئَـسُ من رحمة الله':", "MCQ",
        "يَيْأَسُ | ييأس (بدون ضبط) | ييؤس | ييئس",
        "يَيْأَسُ",
        1, "الهمزة في (يَيْأَسُ) مفتوحة وما قبلها ياء ساكنة أصلية فتكتب على ألف.",
        "DAILY_Y6_ARB_W1D6", "W1", "Hard", "الهمزة المتوسطة", "تصويب الخطأ"
    ])

    # --- WEEK 2: أنواع الخبر (مفرد، جملة، شبه جملة) + الهمزة المتوسطة على واو ---
    # Day 8: أنواع الخبر (الخبر المفرد)
    questions.append([
        "Q_Y6_ARB_W2D8_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "ما نوع الخبر في جملة: 'العالِمُ مخلصٌ في عمله'؟", "MCQ",
        "خبر مفرد | خبر جملة اسمية | خبر جملة فعلية | خبر شبه جملة",
        "خبر مفرد",
        1, "(مخلصٌ) خبر مفرد لأنه ليس جملة ولا شبه جملة، حتى لو دل على مثنى أو جمع.",
        "DAILY_Y6_ARB_W2D8", "W2", "Easy", "أنواع الخبر", "الخبر المفرد"
    ])
    questions.append([
        "Q_Y6_ARB_W2D8_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "الخبر في جملة 'المعلّمون مخلصون' نوعه مفرد لأن:", "MCQ",
        "المقصود بالمفرد هنا أنه كلمة واحدة وليس جملة ولا شبه جملة | المعلمون شخص واحد | مخلصون فعل ماض | الخبر هنا شبه جملة",
        "المقصود بالمفرد هنا أنه كلمة واحدة وليس جملة ولا شبه جملة",
        1, "في باب المبتدأ والخبر، (المفرد) يعني ما ليس جملة ولا شبه جملة.",
        "DAILY_Y6_ARB_W2D8", "W2", "Medium", "أنواع الخبر", "تعريف الخبر المفرد"
    ])
    questions.append([
        "Q_Y6_ARB_W2D8_03", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "أعرب كلمة 'نشيطان' في جملة: 'التلميذان نشيطان':", "MCQ",
        "خبر المبتدأ مرفوع وعلامة رفعه الألف لأنه مثنى | خبر مرفوع بالضمة | مبتدأ ثانٍ | مفعول به",
        "خبر المبتدأ مرفوع وعلامة رفعه الألف لأنه مثنى",
        1, "علامة رفع المثنى هي الألف.",
        "DAILY_Y6_ARB_W2D8", "W2", "Medium", "أنواع الخبر", "إعراب الخبر المفرد المثنى"
    ])
    questions.append([
        "Q_Y6_ARB_W2D8_04", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "اختر الخبر المناسب ليكتمل المعنى بخبر مفرد: 'المهندسون ........'", "MCQ",
        "بارعون | يبارعون | في المشروع | إتقانهم كبير",
        "بارعون",
        1, "'بارعون' اسم مفرد مرفوع بالواو لأنه جمع مذكر سالم.",
        "DAILY_Y6_ARB_W2D8", "W2", "Medium", "أنواع الخبر", "مطابقة الخبر للمبتدأ"
    ])
    questions.append([
        "Q_Y6_ARB_W2D8_05", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "أي الجمل الآتية تشتمل على خبر مفرد؟", "MCQ",
        "الأمهاتُ رحيماتٌ بأبنائهن | الصدقُ يهدي إلى البر | العصفورُ فوق الشجرة | الحديقةُ أزهارها متفتحة",
        "الأمهاتُ رحيماتٌ بأبنائهن",
        1, "(رحيماتٌ) كلمة واحدة اسمية تممت المعنى فهي خبر مفرد.",
        "DAILY_Y6_ARB_W2D8", "W2", "Hard", "أنواع الخبر", "استخراج الخبر المفرد"
    ])

    # Day 9: الخبر الجملة وشبه الجملة
    questions.append([
        "Q_Y6_ARB_W2D9_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "ما نوع الخبر في: 'الطالبُ يذاكرُ دروسَه بإتقان'؟", "MCQ",
        "خبر جملة فعلية | خبر مفرد | خبر جملة اسمية | خبر شبه جملة",
        "خبر جملة فعلية",
        1, "جملة الفعل والفاعل المستتر (يذاكر هو) في محل رفع خبر المبتدأ.",
        "DAILY_Y6_ARB_W2D9", "W2", "Easy", "أنواع الخبر", "الخبر الجملة الفعلية"
    ])
    questions.append([
        "Q_Y6_ARB_W2D9_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "ما الرابط المشترط في خبر الجملة الاسمية في: 'الشجرةُ أغصانُها خضراءُ'؟", "MCQ",
        "الضمير (الهاء) العائد على المبتدأ الأول | الألف واللام | اسم الإشارة | حرف العطف",
        "الضمير (الهاء) العائد على المبتدأ الأول",
        1, "يشترط في خبر الجملة وجود ضمير يربطها بالمبتدأ الأول ويطابقه.",
        "DAILY_Y6_ARB_W2D9", "W2", "Medium", "أنواع الخبر", "الرابط في الجملة الاسمية"
    ])
    questions.append([
        "Q_Y6_ARB_W2D9_03", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "عيّن خبر شبه الجملة في جملة: 'العزّ في طاعةِ الله':", "MCQ",
        "في طاعةِ (جار ومجرور) | العزّ | الله | مستتر",
        "في طاعةِ (جار ومجرور)",
        1, "الجار والمجرور (في طاعة) شبه جملة في محل رفع خبر.",
        "DAILY_Y6_ARB_W2D9", "W2", "Medium", "أنواع الخبر", "الخبر شبه الجملة الجار والمجرور"
    ])
    questions.append([
        "Q_Y6_ARB_W2D9_04", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "حوّل الخبر المفرد إلى خبر جملة فعلية في: 'المعلمان مخلصان':", "MCQ",
        "المعلمان يخلصان في العمل | المعلمان إخلاصهما عظيم | المعلمان في إخلاص | مخلص المعلمان",
        "المعلمان يخلصان في العمل",
        1, "تحويل الاسم المشتق (مخلصان) إلى فعل مضارع (يخلصان).",
        "DAILY_Y6_ARB_W2D9", "W2", "Hard", "أنواع الخبر", "التحويل بين أنواع الخبر"
    ])
    questions.append([
        "Q_Y6_ARB_W2D9_05", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر",
        "ما المحل الإعرابي لشبه الجملة (تحت المنضدة) في: 'القطةُ تحتَ المنضدةِ'؟", "MCQ",
        "في محل رفع خبر المبتدأ | في محل نصب مفعول به | في محل جر مضاف إليه | مبتدأ مؤخر",
        "في محل رفع خبر المبتدأ",
        1, "شبه الجملة الظرفي متعلق بمحذوف تقديره مستقر في محل رفع خبر.",
        "DAILY_Y6_ARB_W2D9", "W2", "Hard", "أنواع الخبر", "إعراب شبه الجملة الظرفي"
    ])

    # Day 10: الهمزة المتوسطة على واو
    questions.append([
        "Q_Y6_ARB_W2D10_01", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على واو",
        "ما سبب كتابة الهمزة على واو في كلمة (مُـؤْمِـن)؟", "MCQ",
        "لأن الهمزة ساكنة وما قبلها مضموم والضمة أقوى من السكون | لأن الهمزة مكسورة | لأن الهمزة مفتوحة وما قبلها ألف | لأنها آخر الكلمة",
        "لأن الهمزة ساكنة وما قبلها مضموم والضمة أقوى من السكون",
        1, "قاعدة أقوى الحركات: الكسرة ثم الضمة ثم الفتحة ثم السكون. الضمة أقوى من السكون فتكتب على واو.",
        "DAILY_Y6_ARB_W2D10", "W2", "Easy", "الهمزة على واو", "الهمزة الساكنة بعد ضم"
    ])
    questions.append([
        "Q_Y6_ARB_W2D10_02", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على واو",
        "اختر الرسم الصحيح للكلمة: 'يتصف التلميذ بـ ........ الصادق.'", "MCQ",
        "التَّـفَـاؤُلِ | التفاأل | التفايل | التفاءل",
        "التَّـفَـاؤُلِ",
        1, "الهمزة مضمومة بعد ألف مد ساكنة، والضمة أقوى من السكون فترسم على واو.",
        "DAILY_Y6_ARB_W2D10", "W2", "Medium", "الهمزة على واو", "الهمزة المضمومة بعد مد"
    ])
    questions.append([
        "Q_Y6_ARB_W2D10_03", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على واو",
        "أي الكلمات التالية كُتبت همزتها على واو لأنها مفتوحة بعد ضم؟", "MCQ",
        "مُـؤَذِّن | رُؤْيَة | شُؤُون | فُؤَاد (مضمومة)",
        "مُـؤَذِّن",
        1, "في كلمة (مُـؤَذِّن): الميم مضمومة والهمزة مفتوحة، والضمة أقوى من الفتحة فتكتب على واو.",
        "DAILY_Y6_ARB_W2D10", "W2", "Hard", "الهمزة على واو", "الهمزة المفتوحة بعد ضم"
    ])

    # --- WEEK 3: الأسماء الخمسة وإعرابها + كتابة نص معلوماتي ---
    questions.append([
        "Q_Y6_ARB_W3D15_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: الأسماء الخمسة",
        "ما علامة رفع الأسماء الخمسة (أب، أخ، حم، فو، ذو)؟", "MCQ",
        "الواو (نيابة عن الضمة) | الألف | الياء | الضمة الظاهرة",
        "الواو (نيابة عن الضمة)",
        1, "الأسماء الخمسة ترفع بالواو وتنصب بالألف وتجر بالياء بشرط أن تكون مفردة ومضافة لغير ياء المتكلم.",
        "DAILY_Y6_ARB_W3D15", "W3", "Easy", "الأسماء الخمسة", "علامات الإعراب الفرعية"
    ])
    questions.append([
        "Q_Y6_ARB_W3D15_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: الأسماء الخمسة",
        "أعرب 'أباك' في جملة: 'أطِعْ أباكَ':", "MCQ",
        "مفعول به منصوب وعلامة نصبه الألف لأنه من الأسماء الخمسة | فاعل مرفوع بالواو | اسم مجرور بالياء | مضاف إليه",
        "مفعول به منصوب وعلامة نصبه الألف لأنه من الأسماء الخمسة",
        1, "تنصب الأسماء الخمسة بالألف، والكاف ضمير متصل في محل جر مضاف إليه.",
        "DAILY_Y6_ARB_W3D15", "W3", "Medium", "الأسماء الخمسة", "إعراب النصب"
    ])
    questions.append([
        "Q_Y6_ARB_W3D16_01", "Grade 6 (G6)", "اللغة العربية", "التعبير والكتابة: النص المعلوماتي",
        "السمة الأساسية للنص المعلوماتي هي الاعتماد على:", "MCQ",
        "الحقائق والأرقام الموضوعية بدقة ومصداقية | الخيال والأساطير غير الواقعية | العواطف والمشاعر الشخصية فقط | السجع والقوافي الشعرية",
        "الحقائق والأرقام الموضوعية بدقة ومصداقية",
        1, "النص المعلوماتي يقدم حقائق علمية أو معرفية خالية من الآراء الذاتية.",
        "DAILY_Y6_ARB_W3D16", "W3", "Medium", "النص المعلوماتي", "خصائص النص المعلوماتي"
    ])

    # --- WEEK 4: كان وأخواتها وإن وأخواتها ---
    questions.append([
        "Q_Y6_ARB_W4D22_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: الأفعال الناسخة والحروف الناسخة",
        "ما عمل الأفعال الناسخة (كان وأخواتها) عند دخولها على الجملة الاسمية؟", "MCQ",
        "ترفع المبتدأ ويسمى اسمها، وتنصب الخبر ويسمى خبرها | تنصب المبتدأ وترفع الخبر | تجر المبتدأ والخبر | تجزم الفعل المضارع",
        "ترفع المبتدأ ويسمى اسمها، وتنصب الخبر ويسمى خبرها",
        1, "كان وأخواتها أفعال ناسخة ترفع الاسم وتنصب الخبر.",
        "DAILY_Y6_ARB_W4D22", "W4", "Easy", "كان وأخواتها", "عمل الأفعال الناسخة"
    ])
    questions.append([
        "Q_Y6_ARB_W4D22_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: الأفعال الناسخة والحروف الناسخة",
        "أعرب كلمة 'متفوقين' في: 'أصبحَ الطلابُ متفوقينَ':", "MCQ",
        "خبر أصبح منصوب وعلامة نصبه الياء لأنه جمع مذكر سالم | اسم أصبح مرفوع | مضاف إليه | نعت منصوب بالفتحة",
        "خبر أصبح منصوب وعلامة نصبه الياء لأنه جمع مذكر سالم",
        1, "خبر أصبح منصوب وعلامة نصبه الياء.",
        "DAILY_Y6_ARB_W4D22", "W4", "Medium", "كان وأخواتها", "إعراب خبر كان"
    ])

    return questions

def generate_exams():
    exams = []
    # Ali Exams
    exams.append(["DAILY_Y5_ENG_W1D1", "Ali - Day 1: Adverbs of Manner", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W1"])
    exams.append(["DAILY_Y5_ENG_W1D2", "Ali - Day 2: Adverbials of Time", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W1"])
    exams.append(["DAILY_Y5_ENG_W1D3", "Ali - Day 3: Adverbials of Place", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W1"])
    exams.append(["DAILY_Y5_ENG_W1D4", "Ali - Day 4: Fronted Adverbials & Commas", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W1"])
    exams.append(["DAILY_Y5_ENG_W1D5", "Ali - Day 5: Compound Adverbials", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W1"])
    exams.append(["DAILY_Y5_ENG_W1D6", "Ali - Day 6: Sentence Repair & Error Hunting", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W1"])
    exams.append(["EX_Y5_ENG_W1", "Ali - Week 1 Milestone: Adverbials Mastery", "Year 5 (G5)", "English Grammar", 10, 20, "ACTIVE", "", "2026-10-25", "Weekly", "W1"])
    exams.append(["DAILY_Y5_ENG_W2D8", "Ali - Day 8: Relative Pronouns (who/which/that)", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W2"])
    exams.append(["DAILY_Y5_ENG_W2D9", "Ali - Day 9: Non-defining Relative Clauses & Commas", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W2"])
    exams.append(["DAILY_Y5_ENG_W2D10", "Ali - Day 10: Defining vs Non-defining Clauses", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W2"])
    exams.append(["EX_Y5_ENG_W2_CUMULATIVE", "Ali - Week 2 Cumulative Exam (W1 + W2 Balanced)", "Year 5 (G5)", "English Grammar", 12, 25, "ACTIVE", "", "2026-10-25", "Cumulative", "W2"])
    exams.append(["EX_Y5_ENG_W3_CUMULATIVE", "Ali - Week 3 Cumulative Exam (W1 + W2 + W3)", "Year 5 (G5)", "English Grammar", 15, 30, "ACTIVE", "", "2026-10-25", "Cumulative", "W3"])
    exams.append(["EX_Y5_ENG_W4_CUMULATIVE", "Ali - Week 4 Milestone Exam (W1 - W4)", "Year 5 (G5)", "English Grammar", 18, 35, "ACTIVE", "", "2026-10-25", "Cumulative", "W4"])
    exams.append(["EX_Y5_ENG_M1_CAPSTONE", "Ali - Month 1 Comprehensive Capstone Exam", "Year 5 (G5)", "English Grammar", 20, 40, "ACTIVE", "", "2026-10-25", "Monthly", "M1"])

    # Mostafa Exams
    exams.append(["DAILY_Y6_ARB_W1D4", "Mostafa - Day 4: إدارة الوقت وترتيب الأولويات", "Grade 6 (G6)", "اللغة العربية", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W1"])
    exams.append(["DAILY_Y6_ARB_W1D5", "Mostafa - Day 5: النكرة والمعرفة", "Grade 6 (G6)", "اللغة العربية", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W1"])
    exams.append(["DAILY_Y6_ARB_W1D6", "Mostafa - Day 6: الهمزة المتوسطة على ألف", "Grade 6 (G6)", "اللغة العربية", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W1"])
    exams.append(["EX_Y6_ARB_W1", "Mostafa - Week 1 Milestone: لغة عربية", "Grade 6 (G6)", "اللغة العربية", 10, 20, "ACTIVE", "", "2026-10-25", "Weekly", "W1"])
    exams.append(["DAILY_Y6_ARB_W2D8", "Mostafa - Day 8: أنواع الخبر (المفرد)", "Grade 6 (G6)", "اللغة العربية", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W2"])
    exams.append(["DAILY_Y6_ARB_W2D9", "Mostafa - Day 9: أنواع الخبر (الجملة وشبه الجملة)", "Grade 6 (G6)", "اللغة العربية", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W2"])
    exams.append(["DAILY_Y6_ARB_W2D10", "Mostafa - Day 10: الهمزة المتوسطة على واو", "Grade 6 (G6)", "اللغة العربية", 5, 10, "ACTIVE", "", "2026-10-25", "Daily", "W2"])
    exams.append(["EX_Y6_ARB_W2_CUMULATIVE", "Mostafa - Week 2 Cumulative Exam (W1 + W2)", "Grade 6 (G6)", "اللغة العربية", 12, 25, "ACTIVE", "", "2026-10-25", "Cumulative", "W2"])
    exams.append(["EX_Y6_ARB_W3_CUMULATIVE", "Mostafa - Week 3 Cumulative Exam (W1 + W2 + W3)", "Grade 6 (G6)", "اللغة العربية", 15, 30, "ACTIVE", "", "2026-10-25", "Cumulative", "W3"])
    exams.append(["EX_Y6_ARB_W4_CUMULATIVE", "Mostafa - Week 4 Milestone Exam (W1 - W4)", "Grade 6 (G6)", "اللغة العربية", 18, 35, "ACTIVE", "", "2026-10-25", "Cumulative", "W4"])
    exams.append(["EX_Y6_ARB_M1_CAPSTONE", "Mostafa - Month 1 Comprehensive Capstone Exam", "Grade 6 (G6)", "اللغة العربية", 20, 40, "ACTIVE", "", "2026-10-25", "Monthly", "M1"])
    return exams

def generate_study_plan():
    plan = []
    # Ali Ahmed
    plan.append(["PLAN_Y5_D01", "W1", "1", "Day 1", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Adverbs of Manner", "Identifying manner adverbs ending in -ly", 5, "Completed", "DAILY_Y5_ENG_W1D1"])
    plan.append(["PLAN_Y5_D02", "W1", "2", "Day 2", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Adverbials of Time", "Prepositional time phrases (at dawn, in 1969)", 5, "Completed", "DAILY_Y5_ENG_W1D2"])
    plan.append(["PLAN_Y5_D03", "W1", "3", "Day 3", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Adverbials of Place", "Answering WHERE (inside the station, on lunar surface)", 5, "Completed", "DAILY_Y5_ENG_W1D3"])
    plan.append(["PLAN_Y5_D04", "W1", "4", "Day 4", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Fronted Adverbials & Commas", "Mandatory comma punctuation rule after fronted adverbials", 5, "Completed", "DAILY_Y5_ENG_W1D4"])
    plan.append(["PLAN_Y5_D05", "W1", "5", "Day 5", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Compound Adverbials (Time + Place)", "Sentence restructuring with multiple adverbials", 5, "Active", "DAILY_Y5_ENG_W1D5"])
    plan.append(["PLAN_Y5_D06", "W1", "6", "Day 6", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Sentence Repair & Error Hunting", "Fixing missing commas and misidentified adverbs", 5, "Planned", "DAILY_Y5_ENG_W1D6"])
    plan.append(["PLAN_Y5_D07", "W1", "7", "Day 7", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Milestone Assessment", "W1 Milestone Exam", "Full mastery of manner, time, and place adverbials", 10, "Planned", "EX_Y5_ENG_W1"])
    
    plan.append(["PLAN_Y5_D08", "W2", "8", "Day 8", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "Relative Pronouns", "Choosing between who, which, and whose", 5, "Planned", "DAILY_Y5_ENG_W2D8"])
    plan.append(["PLAN_Y5_D09", "W2", "9", "Day 9", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "Non-defining Clauses", "Punctuation with commas on both sides", 5, "Planned", "DAILY_Y5_ENG_W2D9"])
    plan.append(["PLAN_Y5_D10", "W2", "10", "Day 10", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "Defining vs Non-defining", "Syntactic distinction and comma omission", 5, "Planned", "DAILY_Y5_ENG_W2D10"])
    plan.append(["PLAN_Y5_D14", "W2", "14", "Day 14", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Milestone Assessment", "W2 Cumulative Exam (W1 + W2)", "Adverbials + Relative Clauses balanced synthesis", 12, "Planned", "EX_Y5_ENG_W2_CUMULATIVE"])
    plan.append(["PLAN_Y5_D21", "W3", "21", "Day 21", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Milestone Assessment", "W3 Cumulative Exam (W1 + W2 + W3)", "Modal verbs + Relative clauses + Adverbials", 15, "Planned", "EX_Y5_ENG_W3_CUMULATIVE"])
    plan.append(["PLAN_Y5_D28", "W4", "28", "Day 28", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Milestone Assessment", "W4 Milestone Exam (W1 - W4)", "Comprehensive grammar synthesis before monthly capstone", 18, "Planned", "EX_Y5_ENG_W4_CUMULATIVE"])
    plan.append(["PLAN_Y5_D30", "M1", "30", "Day 30", "Ali Ahmed", "Year 5 (G5)", "English Grammar", "Monthly Capstone", "Month 1 Comprehensive Exam", "Full Month 1 Cambridge curriculum evaluation", 20, "Planned", "EX_Y5_ENG_M1_CAPSTONE"])

    # Mostafa Ahmed
    plan.append(["PLAN_Y6_D04", "W1", "4", "Day 4", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت", "إدارة الوقت وترتيب الأولويات", "استيعاب المقروء ومصفوفة الأولويات", 5, "Completed", "DAILY_Y6_ARB_W1D4"])
    plan.append(["PLAN_Y6_D05", "W1", "5", "Day 5", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "النكرة والمعرفة", "التمييز بين المعارف الست والنكرات", 5, "Active", "DAILY_Y6_ARB_W1D5"])
    plan.append(["PLAN_Y6_D06", "W1", "6", "Day 6", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة", "الهمزة المتوسطة على ألف", "قاعدة أقوى الحركات ورسم الهمزة", 5, "Planned", "DAILY_Y6_ARB_W1D6"])
    plan.append(["PLAN_Y6_D07", "W1", "7", "Day 7", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "Milestone Assessment", "W1 Milestone Exam", "إتقان النكرة والمعرفة والهمزة المتوسطة والقراءة", 10, "Planned", "EX_Y6_ARB_W1"])
    
    plan.append(["PLAN_Y6_D08", "W2", "8", "Day 8", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "أنواع الخبر (المفرد)", "المطابقة في الإفراد والتثنية والجمع وعلامات الرفع", 5, "Planned", "DAILY_Y6_ARB_W2D8"])
    plan.append(["PLAN_Y6_D09", "W2", "9", "Day 9", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "الخبر الجملة وشبه الجملة", "الرابط وإعراب الجملة وشبه الجملة", 5, "Planned", "DAILY_Y6_ARB_W2D9"])
    plan.append(["PLAN_Y6_D10", "W2", "10", "Day 10", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة", "الهمزة المتوسطة على واو", "الهمزة الساكنة والمفتوحة بعد ضم", 5, "Planned", "DAILY_Y6_ARB_W2D10"])
    plan.append(["PLAN_Y6_D14", "W2", "14", "Day 14", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "Milestone Assessment", "W2 Cumulative Exam (W1 + W2)", "أنواع الخبر + النكرة والمعرفة + الهمزة المتوسطة", 12, "Planned", "EX_Y6_ARB_W2_CUMULATIVE"])
    plan.append(["PLAN_Y6_D21", "W3", "21", "Day 21", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "Milestone Assessment", "W3 Cumulative Exam (W1 + W2 + W3)", "الأسماء الخمسة + أنواع الخبر + الإملاء والقراءة", 15, "Planned", "EX_Y6_ARB_W3_CUMULATIVE"])
    plan.append(["PLAN_Y6_D28", "W4", "28", "Day 28", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "Milestone Assessment", "W4 Milestone Exam (W1 - W4)", "كان وأخواتها + الأسماء الخمسة + أنواع الخبر الشامل", 18, "Planned", "EX_Y6_ARB_W4_CUMULATIVE"])
    plan.append(["PLAN_Y6_D30", "M1", "30", "Day 30", "Mostafa Ahmed", "Grade 6 (G6)", "اللغة العربية", "Monthly Capstone", "Month 1 Comprehensive Exam", "الامتحان الشهري التراكمي الشامل لمنهج الصف السادس", 20, "Planned", "EX_Y6_ARB_M1_CAPSTONE"])

    return plan

if __name__ == "__main__":
    qs = generate_questions()
    print(f"Generated {len(qs)} pedagogical questions.")
    
    # Write Question_Bank.csv
    qb_path = r"C:\Users\co0ob\Projects\primary-exam-system\Question_Bank.csv"
    headers = [
        "معرف السؤال", "الصف الدراسي", "المادة", "الوحدة / الدرس", "نص السؤال",
        "نوع السؤال", "الخيارات (مفصولة بـ |)", "الإجابة الصحيحة", "الدرجة",
        "الشرح والتوضيح", "كود الامتحان", "الأسبوع", "مستوى الصعوبة"
    ]
    with open(qb_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for q in qs:
            # write row with 13 standard columns
            writer.writerow(q[:13])
    print(f"Successfully saved {len(qs)} rows to {qb_path}")

    # Write Exams.csv
    ex_path = r"C:\Users\co0ob\Projects\primary-exam-system\Exams.csv"
    ex_headers = [
        "كود الامتحان", "عنوان الامتحان", "الصف الدراسي", "المادة",
        "عدد الأسئلة", "مدة الامتحان (بالدقائق)", "حالة الامتحان",
        "رابط Google Form", "تاريخ الإنشاء", "نوع الامتحان", "الفترة"
    ]
    exams = generate_exams()
    with open(ex_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(ex_headers)
        for e in exams:
            writer.writerow(e)
    print(f"Successfully saved {len(exams)} exams to {ex_path}")
