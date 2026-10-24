# -*- coding: utf-8 -*-
"""
Inject Dynamic Passages and Coordinated Question Generation into Code.gs.
"""

with open(r'C:\Users\co0ob\Projects\primary-exam-system\dynamic_passages_pool.js', 'r', encoding='utf-8') as f:
    passages_pool_code = f.read()

# Read current Code.gs
with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace generateMostafaEnglishExam with dynamic passage-aware version
new_mostafa_eng = """
/**
 * Procedural Generator for Mostafa Ahmed (Grade 6 English Literacy & Report Writing)
 * Randomly selects a unique passage from the pool on every attempt and generates matched questions!
 */
function generateMostafaEnglishExam() {
  const fantasy = getRandomElement(FANTASY_PASSAGES_POOL);
  const report = getRandomElement(REPORT_PASSAGES_POOL);
  const questions = [];

  // Q1: Simile (Matched to the active passage)
  questions.push({
    id: 'DYN_Y6_ENG_001_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (' + fantasy.title + ')',
    passage: fantasy.text,
    text: `From the reading passage, which phrase is a <b>SIMILE</b> comparing ${fantasy.simile.target}?`,
    type: 'MCQ',
    options: [
      fantasy.simile.phrase,
      fantasy.personification,
      fantasy.metaphor.phrase,
      'Cobblestones lined the silent marketplace'
    ],
    correctAnswer: fantasy.simile.phrase,
    points: 1,
    explanation: `💡 Simile Identification:\\nA simile compares two things using "like" or "as": "${fantasy.simile.phrase}".`
  });

  // Q2: Personification (Matched to the active passage)
  questions.push({
    id: 'DYN_Y6_ENG_002_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (' + fantasy.title + ')',
    passage: fantasy.text,
    text: `What figure of speech is demonstrated in this sentence from the passage: "<b>${fantasy.personification}</b>"?`,
    type: 'MCQ',
    options: ['Personification', 'Simile', 'Alliteration', 'Hyperbole'],
    correctAnswer: 'Personification',
    points: 1,
    explanation: `💡 Personification:\\nGiving human actions or qualities to non-human objects or nature.`
  });

  // Q3: Metaphor & Atmospheric Inference
  questions.push({
    id: 'DYN_Y6_ENG_003_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (' + fantasy.title + ')',
    passage: fantasy.text,
    text: `In the passage, the author writes: "<b>${fantasy.metaphor.phrase}</b>" What does this metaphorical description suggest?`,
    type: 'MCQ',
    options: [
      fantasy.metaphor.meaning,
      'The place was bustling with vibrant festivals and music',
      'The weather was stormy and violent',
      'Crowds were cheering in the streets'
    ],
    correctAnswer: fantasy.metaphor.meaning,
    points: 1,
    explanation: `💡 Metaphor Analysis:\\n"${fantasy.metaphor.phrase}" emphasizes: ${fantasy.metaphor.meaning}`
  });

  // Q4: Atmosphere & Sensory Details
  questions.push({
    id: 'DYN_Y6_ENG_004_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (' + fantasy.title + ')',
    passage: fantasy.text,
    text: `How does the author establish a mysterious and atmospheric tone in <i>${fantasy.title}</i>?`,
    type: 'MCQ',
    options: [
      fantasy.mood,
      'Through loud cheering crowds and busy street vendors',
      'By narrating a comical argument between characters',
      'By describing a peaceful sunny morning garden'
    ],
    correctAnswer: fantasy.mood,
    points: 1,
    explanation: `💡 Literary Mood:\\nThe author uses sensory descriptions to create an immersive, suspenseful mood.`
  });

  // Q5: Vocabulary in Context
  questions.push({
    id: 'DYN_Y6_ENG_005_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (' + fantasy.title + ')',
    passage: fantasy.text,
    text: `In the passage, what is the meaning of the word "<b>${fantasy.vocab.word}</b>"?`,
    type: 'MCQ',
    options: [
      fantasy.vocab.meaning,
      'Delicate glassware imported from afar',
      'Heavy wooden shields used in battle',
      'Small sailing boats anchored near shore'
    ],
    correctAnswer: fantasy.vocab.meaning,
    points: 1,
    explanation: `💡 Vocabulary in Context:\\n"${fantasy.vocab.word}" means: ${fantasy.vocab.meaning}.`
  });

  // Q6: Relative Clause (Matched to active report passage)
  questions.push({
    id: 'DYN_Y6_ENG_006_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (' + report.title + ')',
    passage: report.text,
    text: `From the report passage, which sentence correctly punctuates the non-defining <b>RELATIVE CLAUSE</b> with commas?`,
    type: 'MCQ',
    options: [
      report.relClause.correct,
      report.relClause.w1,
      report.relClause.w2,
      report.relClause.w3
    ],
    correctAnswer: report.relClause.correct,
    points: 1,
    explanation: '💡 Non-defining Relative Clauses:\\nExtra information introduced with "which" must be separated by a pair of commas: ", which ..., ".'
  });

  // Q7: Subject-Verb Agreement (Matched to report passage)
  questions.push({
    id: 'DYN_Y6_ENG_007_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (' + report.title + ')',
    passage: report.text,
    text: 'Select the sentence with correct <b>SUBJECT-VERB AGREEMENT</b> from the report context:',
    type: 'MCQ',
    options: [
      report.subjectVerb.correct,
      report.subjectVerb.wrong,
      'They was swimming across the coral reef.',
      'The animals travels together in winter.'
    ],
    correctAnswer: report.subjectVerb.correct,
    points: 1,
    explanation: '💡 Subject-Verb Agreement:\\nPlural subjects take plural verbs without -s (e.g., "polyps build", "turtles lay").'
  });

  // Q8: Spelling Trap (From active report passage)
  questions.push({
    id: 'DYN_Y6_ENG_008_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (' + report.title + ')',
    passage: report.text,
    text: `Identify the correct standard spelling to complete the sentence: "<b>${report.spelling.prompt}</b>"`,
    type: 'MCQ',
    options: report.spelling.options,
    correctAnswer: report.spelling.correct,
    points: 1,
    explanation: `💡 Spelling Rule:\\nThe correct spelling is "${report.spelling.correct}".`
  });

  // Q9: Causal Connectives
  questions.push({
    id: 'DYN_Y6_ENG_009_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (' + report.title + ')',
    passage: report.text,
    text: 'Complete the conclusion sentence using formal cause-and-effect connective: "Protecting endangered marine life is essential ________ healthy ecosystems sustain our planet."',
    type: 'MCQ',
    options: ['because', 'although', 'unless', 'despite'],
    correctAnswer: 'because',
    points: 1,
    explanation: '💡 Connectives:\\n"Because" introduces the reason explaining why protection is essential.'
  });

  // Q10: Run-on Sentence Repair
  questions.push({
    id: 'DYN_Y6_ENG_010_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (' + report.title + ')',
    passage: report.text,
    text: 'Which sentence correctly repairs the run-on sentence error from the student report draft?',
    type: 'MCQ',
    options: [
      'Communities can organize coastal clean-ups, and people must stop dumping plastic into the sea.',
      'Communities can organize coastal clean-ups people must, stop dumping plastic.',
      'Communities can organize coastal clean-ups and people must, stop dumping.',
      'Communities can, organize coastal clean-ups people must stop.'
    ],
    correctAnswer: 'Communities can organize coastal clean-ups, and people must stop dumping plastic into the sea.',
    points: 1,
    explanation: '💡 Repairing Run-ons:\\nJoin two complete independent clauses with a comma and coordinating conjunction (", and").'
  });

  return questions;
}
"""

# Replace generateMostafaArabicExam with dynamic passage-aware version
new_mostafa_arb = """
/**
 * Procedural Generator for Mostafa Ahmed (Grade 6 Arabic - سلاح التلميذ)
 * Randomly selects a unique authentic textbook passage from the pool on every attempt and generates matched questions!
 */
function generateMostafaArabicExam() {
  const arb = getRandomElement(ARABIC_PASSAGES_POOL);
  const questions = [];

  // Q1: استخراج المعرفة من النص المحدد
  questions.push({
    id: 'DYN_Y6_ARB_001_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة (' + arb.title + ')',
    passage: arb.text,
    text: `من خلال قراءتك للفقرة السابقة، كلمة (<b>${arb.maarefaWord}</b>) تعتبر اسماً:`,
    type: 'MCQ',
    options: [
      'معرفة (لأنه معرف بأل)',
      'نكرة (لأنه يدل على غير معين)',
      'فعلاً ماضياً مبنياً على الفتح',
      'حرف جر يفيد الظرفية'
    ],
    correctAnswer: 'معرفة (لأنه معرف بأل)',
    points: 1,
    explanation: `💡 المعرف بأل:\\nالاسم الذي يبدأ بـ (أل) التعريف هو اسم معرفة يدل على شيء معين ومحدد.`
  });

  // Q2: استخراج النكرة من النص المحدد
  questions.push({
    id: 'DYN_Y6_ARB_002_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة (' + arb.title + ')',
    passage: arb.text,
    text: `في سياق الفقرة السابقة، كلمة (<b>${arb.nakiraWord}</b>) هي اسم:`,
    type: 'MCQ',
    options: [
      'نكرة (لأنه منون ومجرد من أل والإضافة)',
      'معرفة بأل',
      'اسم إشارة للقريب',
      'ضمير متكلم'
    ],
    correctAnswer: 'نكرة (لأنه منون ومجرد من أل والإضافة)',
    points: 1,
    explanation: `💡 الاسم النكرة:\\nاسم منون ومجرد من أل والإضافة، ويدل على مسمى عام غير محدد.`
  });

  // Q3: أنواع المعارف (العَلَم)
  const alamItems = [
    { s: 'مصرُ وطنٌ عظيمٌ يحتضن أبناءه المخلصين.', word: 'مصرُ' },
    { s: 'يجري نهرُ النيلِ بالخير العميم لأرض الكنانة.', word: 'النيلُ' },
    { s: 'حقق مصطفى المركز الأول بفضل تنظيمه للوقت.', word: 'مصطفى' }
  ];
  const chosenAlam = getRandomElement(alamItems);
  questions.push({
    id: 'DYN_Y6_ARB_003_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة',
    passage: arb.text,
    text: `في جملة: "<b>${chosenAlam.s}</b>"، كلمة (<b>${chosenAlam.word}</b>) اسم معرفة لأنه:`,
    type: 'MCQ',
    options: ['اسم عَلَم', 'معرف بالإضافة فقط', 'ضمير منفصل', 'اسم موصول'],
    correctAnswer: 'اسم عَلَم',
    points: 1,
    explanation: '💡 أسماء الأعلام:\\nأسماء الأشخاص والبلدان والأنهار والمدن هي أسماء معارف لأنها تدل على مسمى محدد بذاته.'
  });

  // Q4: إكمال الفراغ باسم معرفة
  questions.push({
    id: 'DYN_Y6_ARB_004_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة',
    passage: arb.text,
    text: 'أكمل الجملة التالية باسم <b>معرفة</b> مناسب: "........ هم الركيزة الأساسية لنهضة أي مجتمع."',
    type: 'MCQ',
    options: ['المخلصون', 'رجالٌ', 'أوفياءٌ', 'مواطنونَ'],
    correctAnswer: 'المخلصون',
    points: 1,
    explanation: '💡 تحديد المعرفة:\\n(المخلصون) معرف بأل، بينما باقي الكلمات نكرات.'
  });

  // Q5: إكمال الفراغ باسم نكرة
  questions.push({
    id: 'DYN_Y6_ARB_005_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة',
    passage: arb.text,
    text: 'أكمل الجملة التالية باسم <b>نكرة</b> منون مناسب: "الوقتُ ........ ثمينٌ لا يقدر بثمن."',
    type: 'MCQ',
    options: ['كنزٌ', 'الكنزُ', 'ذلك الكنز', 'هذا كنز'],
    correctAnswer: 'كنزٌ',
    points: 1,
    explanation: '💡 إعراب النكرة:\\n(كنزٌ) اسم نكرة مرفوع بالضمة ومجرد من أل.'
  });

  // Q6: الهمزة المتوسطة على ألف (مفتوحة بعد فتح)
  const hamzaFatha = [
    { word: 'سَـأَلَ', s: '........ الطالبُ أستاذه عن المسألة.', correct: 'سَأَلَ', wrong: ['سئل', 'ساأل', 'سألَ (بالياء)'] },
    { word: 'تَـأَخَّـرَ', s: 'لا ........ عن مساعدة المحتاجين وخدمة الوطن.', correct: 'تَتَأَخَّرْ', wrong: ['تتأخر (بدون همزة)', 'تتءخر', 'تتآخر'] },
    { word: 'تَـأَمَّـلَ', s: 'حينما ........ المفكرُ في الكون أدرك عظمة الخالق.', correct: 'تَأَمَّلَ', wrong: ['تءمل', 'تأملَ (بالياء)', 'تاأمل'] }
  ];
  const chosenHF = getRandomElement(hamzaFatha);
  questions.push({
    id: 'DYN_Y6_ARB_006_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد الإملائية: الهمزة المتوسطة على ألف',
    passage: arb.text,
    text: `اختر الرسم الإملائي الصحيح للفراغ: "<b>${chosenHF.s}</b>"`,
    type: 'MCQ',
    options: [chosenHF.correct, ...chosenHF.wrong],
    correctAnswer: chosenHF.correct,
    points: 1,
    explanation: '💡 قاعدة الفتح بعد فتح:\\nتكتب الهمزة المتوسطة على ألف إذا كانت مفتوحة وما قبلها حرف مفتوح.'
  });

  // Q7: الهمزة المتوسطة على ألف (ساكنة بعد فتح)
  const hamzaSukoon = [
    { s: 'يستخدم الفلاحُ ........ في تقليب وحرث الأرض.', correct: 'الفَأْسَ', wrong: ['الفئس', 'الفاس', 'الفاءس'] },
    { s: 'شعر الطالب بألم خفيف في ........ بعد يوم حافل.', correct: 'الرَّأْسِ', wrong: ['الرئس', 'الراس', 'الراءس'] },
    { s: 'حمل قائد الفريق ........ الذهبي بعد الفوز المستحق.', correct: 'الكَأْسَ', wrong: ['الكئس', 'الكاس', 'الكاءس'] }
  ];
  const chosenHS = getRandomElement(hamzaSukoon);
  questions.push({
    id: 'DYN_Y6_ARB_007_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد الإملائية: الهمزة المتوسطة على ألف',
    passage: arb.text,
    text: `اختر الكلمة الصحيحة إملائياً لإكمال الفراغ: "<b>${chosenHS.s}</b>"`,
    type: 'MCQ',
    options: [chosenHS.correct, ...chosenHS.wrong],
    correctAnswer: chosenHS.correct,
    points: 1,
    explanation: '💡 قاعدة السكون بعد فتح:\\nالفتحة أقوى من السكون، لذلك إذا كانت الهمزة ساكنة وقبلها حرف مفتوح تُكتب على ألف.'
  });

  // Q8: الهمزة المتوسطة على ألف (مفتوحة بعد ساكن)
  questions.push({
    id: 'DYN_Y6_ARB_008_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد الإملائية: الهمزة المتوسطة على ألف',
    passage: arb.text,
    text: 'ما سبب كتابة الهمزة على ألف في كلمة (<b>يَسْـأَلُ</b>)؟',
    type: 'MCQ',
    options: [
      'لأن الهمزة مفتوحة وما قبلها حرف ساكن',
      'لأن الهمزة مكسورة وما قبلها مضموم',
      'لأن ما قبلها ألف مد ساكنة',
      'لأنها همزة متطرفة وليست متوسطة'
    ],
    correctAnswer: 'لأن الهمزة مفتوحة وما قبلها حرف ساكن',
    points: 1,
    explanation: '💡 قاعدة الفتح بعد سكون:\\nفي كلمة (يَسْـأَلُ): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون ➔ فتُرسم على ألف.'
  });

  // Q9: معاني المفردات من النص المختار تحديداً
  questions.push({
    id: 'DYN_Y6_ARB_009_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القراءة المتحررة: فهم المقروء والمفردات (' + arb.title + ')',
    passage: arb.text,
    text: `معنى كلمة (<b>${arb.vocab.word}</b>) في سياق النص السابق هو:`,
    type: 'MCQ',
    options: [arb.vocab.meaning, 'نسيان وإهمال', 'تأخير وتعطيل', 'خوف وتردد'],
    correctAnswer: arb.vocab.meaning,
    points: 1,
    explanation: `💡 دلالة الكلمة في سياق النص:\\nكلمة (${arb.vocab.word}) في هذا النص تعني: ${arb.vocab.meaning}.`
  });

  // Q10: المضاد اللغوي من النص المختار تحديداً
  questions.push({
    id: 'DYN_Y6_ARB_010_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القراءة المتحررة: استيعاب المقروء (' + arb.title + ')',
    passage: arb.text,
    text: `مضاد كلمة (<b>${arb.antonym.word}</b>) في سياق النص السابق هو:`,
    type: 'MCQ',
    options: [arb.antonym.meaning, 'تأخير وتأجيل', 'كسل وتراخٍ', 'إهمال وتفريط'],
    correctAnswer: arb.antonym.meaning,
    points: 1,
    explanation: `💡 المضاد اللغوي في سياق النص:\\nمضاد (${arb.antonym.word}) هو: ${arb.antonym.meaning}.`
  });

  return questions;
}
"""

# Let's replace generateMostafaEnglishExam and generateMostafaArabicExam in Code.gs
import re

# Insert passages_pool_code before generateMostafaEnglishExam
pattern_eng = r"function generateMostafaEnglishExam\(\) \{[\s\S]*?return questions;\s*\}"
pattern_arb = r"function generateMostafaArabicExam\(\) \{[\s\S]*?return questions;\s*\}"

code = re.sub(pattern_eng, new_mostafa_eng.strip(), code)
code = re.sub(pattern_arb, new_mostafa_arb.strip(), code)

# Insert the pools before generateMostafaEnglishExam
code = code.replace("/**\n * Procedural Generator for Mostafa Ahmed", passages_pool_code + "\n/**\n * Procedural Generator for Mostafa Ahmed")

with open(r'C:\Users\co0ob\Projects\primary-exam-system\Code.gs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Code.gs successfully updated with dynamic passages pool!")
