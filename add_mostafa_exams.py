# -*- coding: utf-8 -*-
"""
Add Mostafa Ahmed (Grade 6) Exams:
1. English: Fantasy Reading "The City That Waited" & Grammar (EX_Y6_ENG_FANTASY01)
2. Arabic: القراءة المتحررة، النكرة والمعرفة، والهمزة المتوسطة (EX_Y6_ARB_PRIO01)
"""

import csv

qb_path = r'C:\Users\co0ob\Projects\primary-exam-system\Question_Bank.csv'
ex_path = r'C:\Users\co0ob\Projects\primary-exam-system\Exams.csv'

mostafa_english_questions = [
    {
        'id': 'Q_Y6_ENG_001', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Fantasy Reading (The City That Waited)',
        'text': 'Which of the following phrases from the text is a SIMILE comparing walls to a shell using "like"?',
        'type': 'MCQ',
        'options': 'Its white walls glowed like the inside of a seashell | The fountain whispered to itself | Shadows stretched along the walls | The city was a hush',
        'correct': 'Its white walls glowed like the inside of a seashell', 'points': 1,
        'explanation': '💡 Rule: A SIMILE compares two different things using the words "like" or "as".\n\n🌟 Examples from the Text:\n• "glowed like the inside of a seashell" (compares walls to a shell using "like")\n• "long and thin as fingers" (compares shadows to fingers using "as")\n• "thin as paper" (compares the voice to paper using "as")',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    },
    {
        'id': 'Q_Y6_ENG_002', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Fantasy Reading (The City That Waited)',
        'text': 'What figure of speech is used in: "The fountain whispered to itself"?',
        'type': 'MCQ',
        'options': 'Personification | Simile | Alliteration | Onomatopoeia',
        'correct': 'Personification', 'points': 1,
        'explanation': '💡 Rule: PERSONIFICATION gives human actions or qualities to non-human objects.\n\n🌟 Examples:\n• "The fountain whispered to itself" ➔ Humans whisper, fountains do not!\n• "The wall of dust howled" ➔ Giving the wind/dust the human/animal action of howling.\n• "The gates closed with a sigh" ➔ Gates don\'t sigh like humans!',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    },
    {
        'id': 'Q_Y6_ENG_003', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Fantasy Reading (The City That Waited)',
        'text': '"The city was a hush." What does this metaphorical phrase suggest about the atmosphere of the city?',
        'type': 'MCQ',
        'options': 'The city was completely silent, deserted, and quiet | The city was noisy and crowded with people | The city was ruined by war | The city was full of singing birds',
        'correct': 'The city was completely silent, deserted, and quiet', 'points': 1,
        'explanation': '💡 Meaning & Inference:\n"A hush" means a sudden, profound silence. Describing the entire city as "a hush" emphasizes that it is eerily still, quiet, and appears empty of people.',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    },
    {
        'id': 'Q_Y6_ENG_004', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Fantasy Reading (The City That Waited)',
        'text': 'How does the author create a mysterious and eerie atmosphere in the text? Choose the best evidence:',
        'type': 'MCQ',
        'options': 'Flickering lamps, shadows like fingers, and a strange voice from the tower | People laughing and children playing in the streets | Bright sunny weather with clear blue skies | The sound of loud car horns and busy traffic',
        'correct': 'Flickering lamps, shadows like fingers, and a strange voice from the tower', 'points': 1,
        'explanation': '💡 Atmosphere Building in Fantasy Fiction:\nWriters create suspense and mystery through sensory details:\n• Sight: "every lamp flickered at once", "shadows long and thin as fingers"\n• Sound: "silver bell rang", "a voice, thin as paper, drifted down"\n• Physical reaction: "Kesh\'s hand tightened on his stick. Tamsin forgot to breathe."',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    },
    {
        'id': 'Q_Y6_ENG_005', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Fantasy Reading (The City That Waited)',
        'text': 'In the sentence "Pale light crept over the cobbles.", what does the word "cobbles" mean?',
        'type': 'MCQ',
        'options': 'Rounded stones used to pave old streets | Wooden floorboards | Sandy desert dunes | Soft grass fields',
        'correct': 'Rounded stones used to pave old streets', 'points': 1,
        'explanation': '💡 Vocabulary in Context:\n"Cobbles" (or cobblestones) are traditional rounded stones fitted together to make roads in historical or fantasy cities.',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    },
    {
        'id': 'Q_Y6_ENG_006', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Report Writing & Grammar',
        'text': 'Which sentence uses a RELATIVE CLAUSE with correct comma punctuation?',
        'type': 'MCQ',
        'options': 'Sea turtles, which are marine reptiles, live in the ocean. | Sea turtles which are marine reptiles live in the ocean. | Sea turtles, which are marine reptiles live, in the ocean. | Sea turtles which, are marine reptiles, live in the ocean.',
        'correct': 'Sea turtles, which are marine reptiles, live in the ocean.', 'points': 1,
        'explanation': '💡 Rule: Non-defining relative clauses (starting with "which" or "who") add extra information and MUST be enclosed between TWO commas!\n\n🌟 Correct Pattern:\n✓ Main clause: "Sea turtles ... live in the ocean."\n✓ Extra relative clause: ", which are marine reptiles,"\n✓ Full sentence: "Sea turtles, which are marine reptiles, live in the ocean."',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    },
    {
        'id': 'Q_Y6_ENG_007', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Report Writing & Grammar',
        'text': 'Select the sentence with correct SUBJECT-VERB AGREEMENT:',
        'type': 'MCQ',
        'options': 'Sea turtles lay their eggs on sandy beaches. | Sea turtles lays their eggs on sandy beaches. | A sea turtle lay their eggs on sandy beaches. | Sea turtles is laying their eggs on sandy beaches.',
        'correct': 'Sea turtles lay their eggs on sandy beaches.', 'points': 1,
        'explanation': '💡 Subject-Verb Agreement Rule:\n• Plural subject ("Sea turtles") takes base verb ("lay").\n• Singular subject ("A sea turtle") takes "-s" verb ("lays").\n\n🌟 Compare:\n✓ "Sea turtles lay eggs." (Plural)\n✓ "A sea turtle lays eggs." (Singular)',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    },
    {
        'id': 'Q_Y6_ENG_008', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Report Writing & Grammar',
        'text': 'Correct the spelling mistake in: "Some sea turtles have a herd shell on their backs."',
        'type': 'MCQ',
        'options': 'hard shell | heard shell | hurt shell | heared shell',
        'correct': 'hard shell', 'points': 1,
        'explanation': '💡 Homophones & Spelling:\n• "herd" = a group of animals (e.g. a herd of cattle).\n• "hard" = solid and firm (e.g. a hard shell).\nSea turtles have a tough, solid shell, so the correct spelling is "hard shell".',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    },
    {
        'id': 'Q_Y6_ENG_009', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Fantasy Reading (The City That Waited)',
        'text': 'True or False: In "Shadows stretched along the walls, long and thin as fingers.", the author uses a simile to describe the shadows.',
        'type': 'TRUE_FALSE',
        'options': 'True | False',
        'correct': 'True', 'points': 1,
        'explanation': '💡 Rule: "long and thin as fingers" is a simile because it uses the word "as" to compare the shape of the shadows to elongated fingers.',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    },
    {
        'id': 'Q_Y6_ENG_010', 'grade': 'Grade 6 (G6)', 'subject': 'English Literacy', 'unit': 'Unit 2: Report Writing & Grammar',
        'text': 'Complete the conclusion sentence using formal connective: "Protecting sea turtles matters ........ they play a vital role in marine ecosystems."',
        'type': 'MCQ',
        'options': 'because | but | although | while',
        'correct': 'because', 'points': 1,
        'explanation': '💡 Explanation of Cause & Effect:\n"because" gives the reason WHY protecting sea turtles is important.',
        'exam_code': 'EX_Y6_ENG_FANTASY01'
    }
]

mostafa_arabic_questions = [
    {
        'id': 'Q_Y6_ARB_001', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'المحور الأول: ترتيب الأولويات وإدارة الوقت',
        'text': 'معنى كلمة (إنجاز) في سياق: "يتطلب إنجاز المهام وقتًا محددًا" هو:',
        'type': 'MCQ',
        'options': 'إتمام وتحقيق بنجاح | تأجيل وتعطيل | نسيان وإهمال | بدء وتخطيط',
        'correct': 'إتمام وتحقيق بنجاح', 'points': 1,
        'explanation': '💡 معنى المفردات:\n• إنجاز الشيء = إتمامه وقضاؤه بنجاح.\n• مثل: "إنجاز الواجبات المدرسية" أي الانتهاء منها بشكل متقن.',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    },
    {
        'id': 'Q_Y6_ARB_002', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'المحور الأول: ترتيب الأولويات وإدارة الوقت',
        'text': 'مضاد كلمة (تأجيل) هو:',
        'type': 'MCQ',
        'options': 'تعجيل وتبكير | تسويف | إبطاء | ترك',
        'correct': 'تعجيل وتبكير', 'points': 1,
        'explanation': '💡 التضاد اللغوي:\n• التأجيل: إرجاء العمل لوقت لاحق.\n• التعجيل: المسارعة في أداء العمل دون تأخير.\n• لذلك مضاد تأجيل هو (تعجيل).',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    },
    {
        'id': 'Q_Y6_ARB_003', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'المحور الأول: ترتيب الأولويات وإدارة الوقت',
        'text': 'لكي ننجح في إدارة يومنا وتحقيق أهدافنا، يجب أن نصنف ونرتب المهام حسب:',
        'type': 'MCQ',
        'options': 'أهميتها (البدء بالأكثر أهمية أولاً) | سهولتها فقط | عشوائياً بدون ترتيب | تأجيل كل المهام الصعبة',
        'correct': 'أهميتها (البدء بالأكثر أهمية أولاً)', 'points': 1,
        'explanation': '💡 استيعاب المقروء:\nنصت الفقرة على: "يجب علينا أن نتعلم كيف نحدد الأولويات ونرتب المهام حسب أهميتها؛ أي نبدأ بالمهام الأكثر أهمية ثم ننتقل إلى الأقل أهمية".',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    },
    {
        'id': 'Q_Y6_ARB_004', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'القواعد النحوية: النكرة والمعرفة',
        'text': 'في جملة "الوقتُ من ذهبٍ"، كلمة (ذهبٍ) هي اسم:',
        'type': 'MCQ',
        'options': 'نكرة | معرفة بأل | اسم علم | ضمير',
        'correct': 'نكرة', 'points': 1,
        'explanation': '💡 قاعدة النكرة والمعرفة:\n• النكرة: اسم يدل على شيء غير معين أو محدد، ومجرد من (أل) والإضافة (مثل: ذهبٍ، كتابٌ، قلمٌ).\n• المعرفة: اسم يدل على شيء معين (مثل: الوقتُ - معرف بأل).',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    },
    {
        'id': 'Q_Y6_ARB_005', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'القواعد النحوية: النكرة والمعرفة',
        'text': 'في جملة "التشتتُ يفقدنا التركيزَ والإنجازَ"، الكلمات (التركيز) و(الإنجاز) هي أسماء:',
        'type': 'MCQ',
        'options': 'معرفة لأنها معرفة بأل | نكرة لأنها ليست علماً | أفعال وليست أسماء | حروف عطف',
        'correct': 'معرفة لأنها معرفة بأل', 'points': 1,
        'explanation': '💡 أنواع المعارف:\nمن أهم أنواع المعارف هو "المعرّف بأل". أي كلمة تقبل أو تبدأ بـ (ال) مثل: (التركيز، الإنجاز، الوقت، المدرسة) هي اسم معرفة.',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    },
    {
        'id': 'Q_Y6_ARB_006', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'القواعد النحوية: النكرة والمعرفة',
        'text': 'أكمل الجملة باسم نكرة مناسب: "الوقتُ ........ عظيمٌ من الله تعالى."',
        'type': 'MCQ',
        'options': 'نعمةٌ | النعمةُ | تلك النعمة | هو النعمة',
        'correct': 'نعمةٌ', 'points': 1,
        'explanation': '💡 شروط الاسم النكرة:\nالمطلوب اسم نكرة (بدون أل ويكون منوناً): كلمة (نعمةٌ) نكرة، بينما (النعمة) معرفة بأل.',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    },
    {
        'id': 'Q_Y6_ARB_007', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'القواعد النحوية: النكرة والمعرفة',
        'text': 'أكمل الجملة باسم معرفة: "........ هم الذين يفوزون بسباق تنظيم الوقت."',
        'type': 'MCQ',
        'options': 'المجتهدون | طلابٌ | أذكياءٌ | مجتهدون',
        'correct': 'المجتهدون', 'points': 1,
        'explanation': '💡 تحديد المعرفة:\n(المجتهدون) اسم معرفة لأنه يبدأ بأل التعريف، بينما (طلابٌ) و(أذكياءٌ) و(مجتهدون) نكرات.',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    },
    {
        'id': 'Q_Y6_ARB_008', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'القواعد الإملائية: الهمزة المتوسطة على ألف',
        'text': 'اختر الرسم الإملائي الصحيح: "حينما ........ السماء أشعر بالراحة."',
        'type': 'MCQ',
        'options': 'أتأَمَّلُ | اتأملُ (بدون همزة) | أتاءمل | أتيمل',
        'correct': 'أتأَمَّلُ', 'points': 1,
        'explanation': '💡 قاعدة الهمزة المتوسطة على ألف:\nتُكتب الهمزة المتوسطة على ألف إذا كانت مفتوحة وما قبلها مفتوح: (أ-تَ-أَ-مَّ-ل).\n\n🌟 أمثلة مشابهة:\n• سَأَلَ (الهمزة مفتوحة وقبلها فتح)\n• تَأَخَّرَ (مفتوحة وقبلها فتح)\n• رَأَى (مفتوحة وقبلها فتح)',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    },
    {
        'id': 'Q_Y6_ARB_009', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'القواعد الإملائية: الهمزة المتوسطة على ألف',
        'text': 'اختر الكلمة الصحيحة إملائياً: "يستخدم الفلاحُ ........ في حرث وتقليب الأرض."',
        'type': 'MCQ',
        'options': 'الفَأْسَ | الفئس | الفأسُ (بالياء) | الفاس (بدون همزة)',
        'correct': 'الفَأْسَ', 'points': 1,
        'explanation': '💡 قاعدة الهمزة الساكنة بعد فتح:\nتُكتب الهمزة المتوسطة على ألف إذا كانت ساكنة بعد فتح: الفَـأْس (الفاء مفتوحة والهمزة ساكنة ➔ ترسم على ألف).\n\n🌟 أمثلة مشابهة:\n• رَأْس (فتحة ثم سكون ➔ ألف)\n• كَأْس (فتحة ثم سكون ➔ ألف)',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    },
    {
        'id': 'Q_Y6_ARB_010', 'grade': 'الصف السادس (G6)', 'subject': 'اللغة العربية', 'unit': 'القواعد النحوية: النكرة والمعرفة',
        'text': 'حدد نوع الكلمة التي تحتها خط في جملة: "مصرُ وطنٌ عظيمٌ":',
        'type': 'MCQ',
        'options': 'مصر (معرفة لأنها علم) ، وطن (نكرة) | كلاهما نكرة | كلاهما معرفة | مصر (نكرة) ، وطن (معرفة)',
        'correct': 'مصر (معرفة لأنها علم) ، وطن (نكرة)', 'points': 1,
        'explanation': '💡 أنواع المعارف (العلم):\n• أسماء البلاد والأشخاص (مثل: مصر، مصطفى، أحمد) هي أسماء معارف لأنها "عَلَم".\n• أما كلمة (وطنٌ) فهي نكرة لأنها غير محددة ومجردة من أل والإضافة.',
        'exam_code': 'EX_Y6_ARB_PRIO01'
    }
]

# Write all questions to CSV
with open(qb_path, 'a', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    for q in mostafa_english_questions + mostafa_arabic_questions:
        writer.writerow([
            q['id'], q['grade'], q['subject'], q['unit'],
            q['text'], q['type'], q['options'], q['correct'],
            q['points'], q['explanation'], q['exam_code']
        ])

# Write exams to CSV
with open(ex_path, 'a', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'EX_Y6_ENG_FANTASY01',
        'Grade 6 English: Fantasy Reading "The City That Waited" & Grammar',
        'Grade 6 (G6)',
        'English Literacy',
        10,
        20,
        'نشط',
        '',
        '2026-10-24'
    ])
    writer.writerow([
        'EX_Y6_ARB_PRIO01',
        'الصف السادس - لغة عربية: القراءة المتحررة، النكرة والمعرفة، والهمزة المتوسطة',
        'Grade 6 (G6)',
        'اللغة العربية',
        10,
        20,
        'نشط',
        '',
        '2026-10-24'
    ])

print('Successfully added 20 questions (English & Arabic) for Mostafa Ahmed (G6)!')
