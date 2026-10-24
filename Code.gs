/**
 * ============================================================
 * Primary School Question Bank & Assessment System (G5 & G6)
 * Manaret El-Eman International School (Ali Ahmed & Mostafa Ahmed)
 * Pure English Architecture, Isolated Portals, Dynamic Passage Engine & Executive Google Sheet Styling
 * ============================================================
 */

function getSpreadsheet() {
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  if (ss) return ss;

  const props = PropertiesService.getUserProperties();
  const savedId = props.getProperty('LINKED_SHEET_ID');
  if (savedId) {
    try {
      ss = SpreadsheetApp.openById(savedId);
      if (ss) return ss;
    } catch(e) {
      Logger.log('Could not open sheet with saved ID: ' + e);
    }
  }

  ss = SpreadsheetApp.create('Manaret El-Eman - Assessment Platform Database');
  props.setProperty('LINKED_SHEET_ID', ss.getId());
  setupDatabase(ss);
  return ss;
}

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🎯 Assessment Management')
    .addItem('⚙️ Full Database Auto-Format & Setup', 'setupDatabase')
    .addItem('🔄 Restore All Historical Submissions (Mostafa & Ali)', 'restoreAllHistoricalSubmissions')
    .addItem('📝 Generate Google Form from Exam', 'generateGoogleFormPrompt')
    .addSeparator()
    .addItem('🔗 Copy Interactive Web App URL', 'copyWebAppUrl')
    .addItem('📊 Open Linked Google Sheet', 'openLinkedSheetUrl')
    .addToUi();
}

/**
 * Executive Setup & Professional Formatting for Google Sheets
 */
function setupDatabase(targetSs) {
  const ss = (targetSs && targetSs.getSheetByName) ? targetSs : getSpreadsheet();

  // 1. TAB: Submissions (Student Results & Records) - NEVER CLEAR EXISTING ROWS!
  let subSheet = ss.getSheetByName('Submissions');
  if (!subSheet) {
    subSheet = ss.insertSheet('Submissions');
  }
  
  const subHeaders = [
    ['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON']
  ];

  if (subSheet.getLastRow() === 0) {
    subSheet.getRange(1, 1, 1, subHeaders[0].length).setValues(subHeaders);
  } else {
    // Just ensure header values match
    subSheet.getRange(1, 1, 1, subHeaders[0].length).setValues(subHeaders);
  }
  formatHeaderRow(subSheet, '#1e3a8a');

  // Auto-seed Ali Ahmed only if missing, preserving Mostafa and all other submissions
  restoreAllHistoricalSubmissions();
  styleSubmissionsSheet(subSheet);

  // 2. TAB: Question_Bank (Reference Catalog)
  let qbSheet = ss.getSheetByName('Question_Bank');
  if (!qbSheet) {
    qbSheet = ss.insertSheet('Question_Bank');
  }
  qbSheet.clear();
  const qbHeaders = [
    ['Question ID', 'Grade Level', 'Subject', 'Unit / Topic', 'Question Text', 'Type', 'Options (delimited by |)', 'Correct Answer', 'Points', 'Pedagogical Explanation & Mistake Breakdown', 'Exam Code']
  ];
  qbSheet.getRange(1, 1, 1, qbHeaders[0].length).setValues(qbHeaders);
  formatHeaderRow(qbSheet, '#047857');

  const sampleQuestions = [
    ["Q_Y5_ENG_001", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "What is an adverbial?", "MCQ", "A single word naming a person or thing | A group of words without a verb that adds detail about time, place, or manner | A group of words with a subject and a verb | A word that joins two clauses together", "A group of words without a verb that adds detail about time, place, or manner", 1, "An adverbial is a word or phrase that gives extra details about WHEN, WHERE, or HOW an action happens. It does NOT contain a finite verb.", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_002", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "In the sentence: \"The rocket launched at dawn.\", what type of adverbial is \"at dawn\"?", "MCQ", "Adverbial of Time | Adverbial of Place | Adverbial of Manner | Adverbial of Reason", "Adverbial of Time", 1, "\"at dawn\" tells us WHEN the rocket launched (Adverbial of Time).", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_003", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which of the following sentences contains an adverbial of PLACE?", "MCQ", "The crew slept inside the space station. | In 2000, the first crew moved in. | She carefully checked the controls. | Soon, the rocket was ready.", "The crew slept inside the space station.", 1, "\"inside the space station\" answers the question WHERE did the crew sleep (Adverbial of Place).", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_004", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "An adverbial of MANNER answers which question?", "MCQ", "How or in what way? | Where? | When? | Who?", "How or in what way?", 1, "Adverbials of manner explain HOW an action happens (e.g., bravely, with great care, silently).", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_005", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which sentence is punctuated correctly with a comma after the fronted adverbial?", "MCQ", "After a long journey, the crew landed. | After a long journey the crew landed. | After a long journey, the crew, landed. | After, a long journey the crew landed.", "After a long journey, the crew landed.", 1, "When an adverbial is at the start (Fronted Adverbial), it must be followed by a comma.", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_006", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "True or False: In the sentence \"The USSR launched Sputnik I in 1957.\", we must put a comma before \"in 1957\".", "TRUE_FALSE", "True | False", "False", 1, "When the adverbial is at the END of a sentence, NO comma is needed.", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_007", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Choose the sentence that has an adverbial of TIME at the beginning:", "MCQ", "Before sunrise, the pilot took off. | Bravely, the pilot flew the plane. | Over the sea, the pilot flew. | With great skill, the pilot landed.", "Before sunrise, the pilot took off.", 1, "\"Before sunrise\" tells us WHEN the pilot took off.", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_008", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Complete the sentence with the best adverbial of manner: \"The engineer repaired the delicate wiring ........\"", "MCQ", "with great care | on the moon | at midnight | in 1969", "with great care", 1, "\"with great care\" describes HOW the engineer repaired the wires.", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_009", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Rewrite \"Astronauts walked on the moon in 1969.\" by moving the adverbial of time to the start:", "MCQ", "In 1969, astronauts walked on the moon. | In 1969 astronauts walked on the moon. | On the moon, astronauts walked in 1969. | Astronauts in 1969 walked on the moon.", "In 1969, astronauts walked on the moon.", 1, "Move \"In 1969\" to the front and place a comma directly after it.", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_010", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which sentence has BOTH an adverbial of time AND an adverbial of place?", "MCQ", "In 1969, astronauts walked on the moon. | The rocket launched at dawn. | The crew worked inside the space station. | Bravely, the pilot flew the plane.", "In 1969, astronauts walked on the moon.", 1, "\"In 1969\" is Time, and \"on the moon\" is Place.", "EX_Y5_ENG_ADV01"],
    ["Q_Y6_ENG_001", "Grade 6 (G6)", "English Literacy", "Unit 2: Fantasy Reading (The City That Waited)", "Which of the following phrases from the text is a SIMILE comparing walls to a shell using \"like\"?", "MCQ", "Its white walls glowed like the inside of a seashell | The fountain whispered to itself | Shadows stretched along the walls | The city was a hush", "Its white walls glowed like the inside of a seashell", 1, "💡 Rule: A SIMILE compares two different things using the words \"like\" or \"as\".\n\n🌟 Examples from the Text:\n• \"glowed like the inside of a seashell\" (compares walls to a shell using \"like\")\n• \"long and thin as fingers\" (compares shadows to fingers using \"as\")\n• \"thin as paper\" (compares the voice to paper using \"as\")", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_002", "Grade 6 (G6)", "English Literacy", "Unit 2: Fantasy Reading (The City That Waited)", "What figure of speech is used in: \"The fountain whispered to itself\"?", "MCQ", "Personification | Simile | Alliteration | Onomatopoeia", "Personification", 1, "💡 Rule: PERSONIFICATION gives human actions or qualities to non-human objects.\n\n🌟 Examples:\n• \"The fountain whispered to itself\" ➔ Humans whisper, fountains do not!\n• \"The wall of dust howled\" ➔ Giving the wind/dust the human/animal action of howling.\n• \"The gates closed with a sigh\" ➔ Gates don't sigh like humans!", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_003", "Grade 6 (G6)", "English Literacy", "Unit 2: Fantasy Reading (The City That Waited)", "\"The city was a hush.\" What does this metaphorical phrase suggest about the atmosphere of the city?", "MCQ", "The city was completely silent, deserted, and quiet | The city was noisy and crowded with people | The city was ruined by war | The city was full of singing birds", "The city was completely silent, deserted, and quiet", 1, "💡 Meaning & Inference:\n\"A hush\" means a sudden, profound silence. Describing the entire city as \"a hush\" emphasizes that it is eerily still, quiet, and appears empty of people.", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_004", "Grade 6 (G6)", "English Literacy", "Unit 2: Fantasy Reading (The City That Waited)", "How does the author create a mysterious and eerie atmosphere in the text? Choose the best evidence:", "MCQ", "Flickering lamps, shadows like fingers, and a strange voice from the tower | People laughing and children playing in the streets | Bright sunny weather with clear blue skies | The sound of loud car horns and busy traffic", "Flickering lamps, shadows like fingers, and a strange voice from the tower", 1, "💡 Atmosphere Building in Fantasy Fiction:\nWriters create suspense and mystery through sensory details:\n• Sight: \"every lamp flickered at once\", \"shadows long and thin as fingers\"\n• Sound: \"silver bell rang\", \"a voice, thin as paper, drifted down\"\n• Physical reaction: \"Kesh's hand tightened on his stick. Tamsin forgot to breathe.\"", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_005", "Grade 6 (G6)", "English Literacy", "Unit 2: Fantasy Reading (The City That Waited)", "In the sentence \"Pale light crept over the cobbles.\", what does the word \"cobbles\" mean?", "MCQ", "Rounded stones used to pave old streets | Wooden floorboards | Sandy desert dunes | Soft grass fields", "Rounded stones used to pave old streets", 1, "💡 Vocabulary in Context:\n\"Cobbles\" (or cobblestones) are traditional rounded stones fitted together to make roads in historical or fantasy cities.", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_006", "Grade 6 (G6)", "English Literacy", "Unit 2: Report Writing & Grammar", "Which sentence uses a RELATIVE CLAUSE with correct comma punctuation?", "MCQ", "Sea turtles, which are marine reptiles, live in the ocean. | Sea turtles which are marine reptiles live in the ocean. | Sea turtles, which are marine reptiles live, in the ocean. | Sea turtles which, are marine reptiles, live in the ocean.", "Sea turtles, which are marine reptiles, live in the ocean.", 1, "💡 Rule: Non-defining relative clauses (starting with \"which\" or \"who\") add extra information and MUST be enclosed between TWO commas!\n\n🌟 Correct Pattern:\n✓ Main clause: \"Sea turtles ... live in the ocean.\"\n✓ Extra relative clause: \", which are marine reptiles,\"\n✓ Full sentence: \"Sea turtles, which are marine reptiles, live in the ocean.\"", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_007", "Grade 6 (G6)", "English Literacy", "Unit 2: Report Writing & Grammar", "Select the sentence with correct SUBJECT-VERB AGREEMENT:", "MCQ", "Sea turtles lay their eggs on sandy beaches. | Sea turtles lays their eggs on sandy beaches. | A sea turtle lay their eggs on sandy beaches. | Sea turtles is laying their eggs on sandy beaches.", "Sea turtles lay their eggs on sandy beaches.", 1, "💡 Subject-Verb Agreement Rule:\n• Plural subject (\"Sea turtles\") takes base verb (\"lay\").\n• Singular subject (\"A sea turtle\") takes \"-s\" verb (\"lays\").\n\n🌟 Compare:\n✓ \"Sea turtles lay eggs.\" (Plural)\n✓ \"A sea turtle lays eggs.\" (Singular)", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_008", "Grade 6 (G6)", "English Literacy", "Unit 2: Report Writing & Grammar", "Correct the spelling mistake in: \"Some sea turtles have a herd shell on their backs.\"", "MCQ", "hard shell | heard shell | hurt shell | heared shell", "hard shell", 1, "💡 Homophones & Spelling:\n• \"herd\" = a group of animals (e.g. a herd of cattle).\n• \"hard\" = solid and firm (e.g. a hard shell).\nSea turtles have a tough, solid shell, so the correct spelling is \"hard shell\".", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_009", "Grade 6 (G6)", "English Literacy", "Unit 2: Fantasy Reading (The City That Waited)", "True or False: In \"Shadows stretched along the walls, long and thin as fingers.\", the author uses a simile to describe the shadows.", "TRUE_FALSE", "True | False", "True", 1, "💡 Rule: \"long and thin as fingers\" is a simile because it uses the word \"as\" to compare the shape of the shadows to elongated fingers.", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_010", "Grade 6 (G6)", "English Literacy", "Unit 2: Report Writing & Grammar", "Complete the conclusion sentence using formal connective: \"Protecting sea turtles matters ........ they play a vital role in marine ecosystems.\"", "MCQ", "because | but | although | while", "because", 1, "💡 Explanation of Cause & Effect:\n\"because\" gives the reason WHY protecting sea turtles is important.", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ARB_001", "الصف السادس (G6)", "اللغة العربية", "المحور الأول: ترتيب الأولويات وإدارة الوقت", "معنى كلمة (إنجاز) في سياق: \"يتطلب إنجاز المهام وقتًا محددًا\" هو:", "MCQ", "إتمام وتحقيق بنجاح | تأجيل وتعطيل | نسيان وإهمال | بدء وتخطيط", "إتمام وتحقيق بنجاح", 1, "💡 معنى المفردات:\n• إنجاز الشيء = إتمامه وقضاؤه بنجاح.\n• مثل: \"إنجاز الواجبات المدرسية\" أي الانتهاء منها بشكل متقن.", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_002", "الصف السادس (G6)", "اللغة العربية", "المحور الأول: ترتيب الأولويات وإدارة الوقت", "مضاد كلمة (تأجيل) هو:", "MCQ", "تعجيل وتبكير | تسويف | إبطاء | ترك", "تعجيل وتبكير", 1, "💡 التضاد اللغوي:\n• التأجيل: إرجاء العمل لوقت لاحق.\n• التعجيل: المسارعة في أداء العمل دون تأخير.\n• لذلك مضاد تأجيل هو (تعجيل).", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_003", "الصف السادس (G6)", "اللغة العربية", "المحور الأول: ترتيب الأولويات وإدارة الوقت", "لكي ننجح في إدارة يومنا وتحقيق أهدافنا، يجب أن نصنف ونرتب المهام حسب:", "MCQ", "أهميتها (البدء بالأكثر أهمية أولاً) | سهولتها فقط | عشوائياً بدون ترتيب | تأجيل كل المهام الصعبة", "أهميتها (البدء بالأكثر أهمية أولاً)", 1, "💡 استيعاب المقروء:\nنصت الفقرة على: \"يجب علينا أن نتعلم كيف نحدد الأولويات ونرتب المهام حسب أهميتها؛ أي نبدأ بالمهام الأكثر أهمية ثم ننتقل إلى الأقل أهمية\".", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_004", "الصف السادس (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "في جملة \"الوقتُ من ذهبٍ\"، كلمة (ذهبٍ) هي اسم:", "MCQ", "نكرة | معرفة بأل | اسم علم | ضمير", "نكرة", 1, "💡 قاعدة النكرة والمعرفة:\n• النكرة: اسم يدل على شيء غير معين أو محدد، ومجرد من (أل) والإضافة (مثل: ذهبٍ، كتابٌ، قلمٌ).\n• المعرفة: اسم يدل على شيء معين (مثل: الوقتُ - معرف بأل).", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_005", "الصف السادس (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "في جملة \"التشتتُ يفقدنا التركيزَ والإنجازَ\"، الكلمات (التركيز) و(الإنجاز) هي أسماء:", "MCQ", "معرفة لأنها معرفة بأل | نكرة لأنها ليست علماً | أفعال وليست أسماء | حروف عطف", "معرفة لأنها معرفة بأل", 1, "💡 أنواع المعارف:\nمن أهم أنواع المعارف هو \"المعرّف بأل\". أي كلمة تقبل أو تبدأ بـ (ال) مثل: (التركيز، الإنجاز، الوقت، المدرسة) هي اسم معرفة.", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_006", "الصف السادس (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "أكمل الجملة باسم نكرة مناسب: \"الوقتُ ........ عظيمٌ من الله تعالى.\"", "MCQ", "نعمةٌ | النعمةُ | تلك النعمة | هو النعمة", "نعمةٌ", 1, "💡 شروط الاسم النكرة:\nالمطلوب اسم نكرة (بدون أل ويكون منوناً): كلمة (نعمةٌ) نكرة، بينما (النعمة) معرفة بأل.", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_007", "الصف السادس (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "أكمل الجملة باسم معرفة: \"........ هم الذين يفوزون بسباق تنظيم الوقت.\"", "MCQ", "المجتهدون | طلابٌ | أذكياءٌ | مجتهدون", "المجتهدون", 1, "💡 تحديد المعرفة:\n(المجتهدون) اسم معرفة لأنه يبدأ بأل التعريف، بينما (طلابٌ) و(أذكياءٌ) و(مجتهدون) نكرات.", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_008", "الصف السادس (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف", "اختر الرسم الإملائي الصحيح: \"حينما ........ السماء أشعر بالراحة.\"", "MCQ", "أتأَمَّلُ | اتأملُ (بدون همزة) | أتاءمل | أتيمل", "أتأَمَّلُ", 1, "💡 قاعدة الهمزة المتوسطة على ألف:\nتُكتب الهمزة المتوسطة على ألف إذا كانت مفتوحة وما قبلها مفتوح: (أ-تَ-أَ-مَّ-ل).\n\n🌟 أمثلة مشابهة:\n• سَأَلَ (الهمزة مفتوحة وقبلها فتح)\n• تَأَخَّرَ (مفتوحة وقبلها فتح)\n• رَأَى (مفتوحة وقبلها فتح)", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_009", "الصف السادس (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف", "اختر الكلمة الصحيحة إملائياً: \"يستخدم الفلاحُ ........ في حرث وتقليب الأرض.\"", "MCQ", "الفَأْسَ | الفئس | الفأسُ (بالياء) | الفاس (بدون همزة)", "الفَأْسَ", 1, "💡 قاعدة الهمزة الساكنة بعد فتح:\nتُكتب الهمزة المتوسطة على ألف إذا كانت ساكنة بعد فتح: الفَـأْس (الفاء مفتوحة والهمزة ساكنة ➔ ترسم على ألف).\n\n🌟 أمثلة مشابهة:\n• رَأْس (فتحة ثم سكون ➔ ألف)\n• كَأْس (فتحة ثم سكون ➔ ألف)", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_010", "الصف السادس (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "حدد نوع الكلمة التي تحتها خط في جملة: \"مصرُ وطنٌ عظيمٌ\":", "MCQ", "مصر (معرفة لأنها علم) ، وطن (نكرة) | كلاهما نكرة | كلاهما معرفة | مصر (نكرة) ، وطن (معرفة)", "مصر (معرفة لأنها علم) ، وطن (نكرة)", 1, "💡 أنواع المعارف (العلم):\n• أسماء البلاد والأشخاص (مثل: مصر، مصطفى، أحمد) هي أسماء معارف لأنها \"عَلَم\".\n• أما كلمة (وطنٌ) فهي نكرة لأنها غير محددة ومجردة من أل والإضافة.", "EX_Y6_ARB_PRIO01"],
    ["Q_Y5_ENG_011", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which word is an adverb of MANNER in: 'The engineer carefully examined the rocket engine.'?", "MCQ", "carefully | engineer | examined | rocket", "carefully", 1, "💡 Adverb of Manner:\n'Carefully' tells us HOW the engineer examined the engine (in a careful manner). Most adverbs ending in -ly describe manner.", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_012", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Identify the fronted adverbial of PLACE: 'Behind the launch tower, the sun began to rise.'", "MCQ", "Behind the launch tower | the sun began | to rise | began to rise", "Behind the launch tower", 1, "💡 Fronted Adverbial of Place:\n'Behind the launch tower' is at the front of the sentence and answers WHERE the action happens.", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_013", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Choose the correct punctuation for this fronted adverbial of time:", "MCQ", "Every morning, the astronauts train for four hours. | Every morning the astronauts, train for four hours. | Every morning the astronauts train, for four hours. | Every, morning the astronauts train for four hours.", "Every morning, the astronauts train for four hours.", 1, "💡 Comma Rule:\nA comma must always follow a fronted adverbial when it begins a sentence: 'Every morning, ...'", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_014", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "In the sentence: 'The satellite orbits Earth at high speed.', what does 'at high speed' describe?", "MCQ", "HOW the satellite orbits (Manner) | WHEN the satellite orbits (Time) | WHERE the satellite orbits (Place) | WHY the satellite orbits (Reason)", "HOW the satellite orbits (Manner)", 1, "💡 Identifying Manner Phrases:\nPrepositional phrases like 'at high speed' explain the manner (how fast or in what way) an action happens.", "EX_Y5_ENG_ADV01"],
    ["Q_Y5_ENG_015", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "True or False: 'Yesterday' can function as a fronted adverbial of time.", "TRUE_FALSE", "True | False", "True", 1, "💡 Time Words at the Front:\nYes! Example: 'Yesterday, Ali completed his homework.'", "EX_Y5_ENG_ADV01"],
    ["Q_Y6_ENG_011", "Grade 6 (G6)", "English Literacy", "Unit 2: Fantasy Reading (The City That Waited)", "In 'The wind moaned through the empty archways', what literary technique is used?", "MCQ", "Personification | Simile | Rhyme | Pun", "Personification", 1, "💡 Personification:\nGiving the human action of 'moaning' to the non-human wind.", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_012", "Grade 6 (G6)", "English Literacy", "Unit 2: Non-Chronological Report (Sea Turtles)", "Which sentence fixes the run-on error in: 'people can stop throwing plastic people can ask boats not to dump rubbish'?", "MCQ", "People can stop throwing plastic into the sea, and they can ask boats not to dump rubbish. | People can stop throwing plastic people can ask boats. | People can, stop throwing plastic and boats. | People can stop throwing, plastic not to dump rubbish.", "People can stop throwing plastic into the sea, and they can ask boats not to dump rubbish.", 1, "💡 Run-on Sentence Fix:\nJoin two independent clauses using a comma and coordinating conjunction (', and') or separate them with a full stop.", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_013", "Grade 6 (G6)", "English Literacy", "Unit 2: Non-Chronological Report (Sea Turtles)", "Identify the correct spelling of the missing word: 'If sea turtles ________, marine ecosystems will suffer.'", "MCQ", "disappear | disapper | dissappear | dissapper", "disappear", 1, "💡 Spelling Alert (Prefix dis- + appear):\ndis + appear = disappear (one 's', two 'p's).", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_014", "Grade 6 (G6)", "English Literacy", "Unit 2: Fantasy Reading (The City That Waited)", "Which adjective best describes the overall mood of the deserted city in Part 6?", "MCQ", "Eerie and desolate | Joyful and vibrant | Crowded and lively | Chaotic and angry", "Eerie and desolate", 1, "💡 Atmosphere Analysis:\nThe quiet fountain, pale light, and silent cobblestones create an eerie and desolate mood.", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ENG_015", "Grade 6 (G6)", "English Literacy", "Unit 2: Non-Chronological Report (Sea Turtles)", "Which relative pronoun correctly completes: 'Plastic waste, ________ is dumped into the ocean, harms marine life.'?", "MCQ", "which | who | where | whose", "which", 1, "💡 Relative Pronoun for Things:\nUse 'which' for non-human objects and materials like 'plastic waste'.", "EX_Y6_ENG_FANTASY01"],
    ["Q_Y6_ARB_011", "الصف السادس (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "عيّن الاسم المعرفة في جملة: 'قرأ التلميذُ كتاباً مفيداً':", "MCQ", "التلميذُ (معرف بأل) | كتاباً | مفيداً | قرأ", "التلميذُ (معرف بأل)", 1, "💡 المعرّف بأل:\n(التلميذُ) اسم معرفة لأنه مقترن بأل التعريف، أما (كتاباً ومفيداً) فهما اسمان نكرتان.", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_012", "الصف السادس (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف", "ما سبب كتابة الهمزة على ألف في كلمة (يَسْـأَلُ)؟", "MCQ", "لأن الهمزة مفتوحة وما قبلها ساكن | لأن الهمزة مكسورة | لأن الهمزة مضمومة | لأن ما قبلها ألف مد", "لأن الهمزة مفتوحة وما قبلها ساكن", 1, "💡 قاعدة الهمزة المتوسطة:\nفي كلمة (يَسْـأَل): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون ➔ فتُرسم على ألف.", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_013", "الصف السادس (G6)", "اللغة العربية", "القراءة المتحررة: استيعاب المقروء وإدارة الوقت", "الفكرة الرئيسة لنص إدارة الوقت هي أن النجاح يتحقق من خلال:", "MCQ", "التخطيط المسبق وترتيب الأولويات | تأجيل الواجبات الصعبة | العمل طوال اليوم دون راحة | الاعتماد على الحظ", "التخطيط المسبق وترتيب الأولويات", 1, "💡 الفكرة الرئيسة:\nإدارة الوقت تبدأ بتحديد الأهداف وترتيب الأولويات والبدء بالمهام العاجلة والمهمة.", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_014", "الصف السادس (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "الضمائر (أنا، نحن، هو، هي) وأسماء الإشارة والأسماء الموصولة كلها تعتبر:", "MCQ", "معارف دائماً | نكرات دائماً | حروفاً وليست أسماء | أفعالاً ماضية", "معارف دائماً", 1, "💡 أنواع المعارف الستة:\nالضمائر وأسماء الإشارة والأسماء الموصولة وأسماء الأعلام والمعرف بأل والمضاف إلى معرفة كلها معارف.", "EX_Y6_ARB_PRIO01"],
    ["Q_Y6_ARB_015", "الصف السادس (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف", "اختر الرسم الإملائي الصحيح للكلمة المكملة: 'لا ........ عن مساعدة المحتاجين.'", "MCQ", "تَتَأَخَّرْ | تتأخر (بدون همزة) | تتءخر | تتآخر", "تَتَأَخَّرْ", 1, "💡 رسم الهمزة المتوسطة:\nتَـتَـأَخَّـر (الهمزة مفتوحة وقبلها تاء مفتوحة ➔ ترسم على ألف).", "EX_Y6_ARB_PRIO01"]
  ];
  qbSheet.getRange(2, 1, sampleQuestions.length, sampleQuestions[0].length).setValues(sampleQuestions);
  styleQuestionBankSheet(qbSheet);

  // 3. TAB: Exams (Active Assessment Registry)
  let exSheet = ss.getSheetByName('Exams');
  if (!exSheet) {
    exSheet = ss.insertSheet('Exams');
  }
  exSheet.clear();
  const exHeaders = [
    ['Exam Code', 'Exam Title', 'Grade Level', 'Subject', 'Questions', 'Duration (Mins)', 'Status', 'Direct URL', 'Created Date']
  ];
  exSheet.getRange(1, 1, 1, exHeaders[0].length).setValues(exHeaders);
  formatHeaderRow(exSheet, '#4338ca');

  const sampleExams = [
    ['EX_Y5_ENG_ADV01', 'Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)', 'Year 5 (G5)', 'English Grammar', 10, 20, 'ACTIVE', '', new Date()],
    ['EX_Y6_ENG_FANTASY01', 'Grade 6 English: Fantasy Reading "The City That Waited" & Report Writing', 'Grade 6 (G6)', 'English Literacy', 10, 20, 'ACTIVE', '', new Date()],
    ['EX_Y6_ARB_PRIO01', 'Grade 6 Arabic: Reading Comprehension, Grammar & Spelling (Diagnostic)', 'Grade 6 (G6)', 'Arabic Language', 10, 20, 'ACTIVE', '', new Date()]
  ];
  exSheet.getRange(2, 1, sampleExams.length, sampleExams[0].length).setValues(sampleExams);
  styleExamsSheet(exSheet);

  // 4. TAB: Retake_Requests (Parent Approval Queue)
  let retakeSheet = ss.getSheetByName('Retake_Requests');
  if (!retakeSheet) {
    retakeSheet = ss.insertSheet('Retake_Requests');
  }
  retakeSheet.clear();
  const retakeHeaders = [
    ['Request ID', 'Timestamp', 'Student Name', 'Exam Code', 'Exam Title', 'Previous Score', 'Status', 'Reason', 'Decision Timestamp']
  ];
  retakeSheet.getRange(1, 1, 1, retakeHeaders[0].length).setValues(retakeHeaders);
  formatHeaderRow(retakeSheet, '#7c3aed');
  styleRetakeSheet(retakeSheet);

  try {
    SpreadsheetApp.getUi().alert('✅ Google Sheet formatted professionally with executive styling!');
  } catch(e) {
    Logger.log('Database initialized successfully.');
  }
}

function formatHeaderRow(sheet, bgColor) {
  const range = sheet.getRange(1, 1, 1, sheet.getLastColumn());
  range.setBackground(bgColor)
       .setFontColor('#ffffff')
       .setFontWeight('bold')
       .setFontSize(11)
       .setHorizontalAlignment('center')
       .setVerticalAlignment('middle');
  sheet.setRowHeight(1, 38);
  sheet.setFrozenRows(1);
}

function styleSubmissionsSheet(sheet) {
  sheet.setColumnWidth(1, 140);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 110);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 70);
  sheet.setColumnWidth(6, 70);
  sheet.setColumnWidth(7, 90);
  sheet.setColumnWidth(8, 130);
  sheet.setColumnWidth(9, 110);
  sheet.setColumnWidth(10, 260);
  sheet.setColumnWidth(11, 80);

  const dataRange = sheet.getRange(2, 1, Math.max(sheet.getLastRow() - 1, 1), 10);
  dataRange.setVerticalAlignment('middle').setFontSize(10);
  sheet.getRange(2, 5, Math.max(sheet.getLastRow() - 1, 1), 3).setHorizontalAlignment('center');
}

function styleQuestionBankSheet(sheet) {
  sheet.setColumnWidth(1, 110);
  sheet.setColumnWidth(2, 110);
  sheet.setColumnWidth(3, 130);
  sheet.setColumnWidth(4, 200);
  sheet.setColumnWidth(5, 340);
  sheet.setColumnWidth(6, 80);
  sheet.setColumnWidth(7, 260);
  sheet.setColumnWidth(8, 160);
  sheet.setColumnWidth(9, 60);
  sheet.setColumnWidth(10, 380);
  sheet.setColumnWidth(11, 130);

  sheet.getRange(2, 5, Math.max(sheet.getLastRow() - 1, 1), 1).setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
  sheet.getRange(2, 10, Math.max(sheet.getLastRow() - 1, 1), 1).setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
  sheet.getRange(2, 1, Math.max(sheet.getLastRow() - 1, 1), 11).setVerticalAlignment('top').setFontSize(10);
}

function styleExamsSheet(sheet) {
  sheet.setColumnWidth(1, 160);
  sheet.setColumnWidth(2, 380);
  sheet.setColumnWidth(3, 120);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 90);
  sheet.setColumnWidth(6, 110);
  sheet.setColumnWidth(7, 90);
  sheet.setColumnWidth(8, 160);
  sheet.setColumnWidth(9, 110);
  sheet.getRange(2, 1, Math.max(sheet.getLastRow() - 1, 1), 9).setVerticalAlignment('middle').setFontSize(10);
}

function styleRetakeSheet(sheet) {
  sheet.setColumnWidth(1, 160);
  sheet.setColumnWidth(2, 140);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 300);
  sheet.setColumnWidth(6, 110);
  sheet.setColumnWidth(7, 100);
  sheet.setColumnWidth(8, 260);
  sheet.setColumnWidth(9, 140);
}

function doGet(e) {
  const examCode = (e && e.parameter && e.parameter.exam) ? e.parameter.exam : '';
  const student = (e && e.parameter && e.parameter.student) ? e.parameter.student.toLowerCase() : '';
  const admin = (e && e.parameter && e.parameter.admin === '1') ? '1' : '0';
  
  const template = HtmlService.createTemplateFromFile('Index');
  template.examCode = examCode;
  template.initialStudent = student;
  template.initialAdmin = admin;
  
  return template.evaluate()
    .setTitle('Manaret El-Eman Assessment Portal')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getRandomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function shuffleArray(arr) {
  const copy = arr.slice();
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = copy[i];
    copy[i] = copy[j];
    copy[j] = temp;
  }
  return copy;
}

// ============================================================
// DYNAMIC PASSAGE LIBRARY (Changes on every exam session!)
// ============================================================

const FANTASY_PASSAGES_POOL = [
  {
    title: 'The City That Waited (Part 6)',
    text: 'The city was a hush. Pale light crept over the cobbles of the deserted square. In the courtyard, the old stone fountain whispered to itself as thin streams of water trickled into the basin. Its white walls glowed like the inside of a seashell in the twilight. High above, the iron gates closed with a mournful sigh, and shadows stretched along the walls, long and thin as fingers. No one walked the silent streets...',
    simile: { phrase: 'glowed like the inside of a seashell', target: 'walls to a seashell' },
    personification: 'The old stone fountain whispered to itself in the courtyard',
    metaphor: { phrase: 'The city was a hush.', meaning: 'The city was completely silent, deserted, and quiet.' },
    vocab: { word: 'cobbles', meaning: 'Rounded stones used to pave historic streets' },
    mood: 'Through silent cobblestones, a whispering fountain, and empty archways'
  },
  {
    title: 'The Whispering Fortress (Part 6)',
    text: 'Silence gripped the fortress like a thick coat of frost. Pale moonlight crawled across the cracked flagstones of the great hall. High above, the iron chandeliers swung gently, groaning in the cold night air. The silver towers gleamed like polished daggers beneath the stars. Below in the dark passage, the freezing mountain wind howled like a hungry wolf. The castle held its breath as midnight struck...',
    simile: { phrase: 'gleamed like polished daggers beneath the stars', target: 'towers to polished daggers' },
    personification: 'The iron chandeliers swung gently, groaning in the cold air',
    metaphor: { phrase: 'Silence was a thick coat of frost.', meaning: 'The cold silence enveloped everything completely and intensely.' },
    vocab: { word: 'flagstones', meaning: 'Large, flat square stones used for paving castle floors' },
    mood: 'Through groaning chandeliers, a howling wind, and cold moonlight'
  },
  {
    title: 'The Sunken Harbor (Part 6)',
    text: 'The harbor was a graveyard of forgotten ships. Thick morning mist crept over the timber planks of the deserted pier. Along the shoreline, the restless waves slapped against the rotting wooden pilings with a low thud. In the distance, the old lighthouse lamp flickered like a dying star in the dark. Overhead, the heavy storm clouds wept soft drops of rain upon the shore. Not a single sailor stirred on the forgotten decks...',
    simile: { phrase: 'flickered like a dying star in the dark', target: 'the lamp to a dying star' },
    personification: 'The heavy storm clouds wept soft drops of rain upon the shore',
    metaphor: { phrase: 'The harbor was a graveyard of forgotten ships.', meaning: 'The harbor was filled with abandoned, decaying wreckage.' },
    vocab: { word: 'pilings', meaning: 'Heavy wooden posts driven into the seabed to support a pier' },
    mood: 'Through weeping clouds, abandoned ships, and flickering lights'
  }
];

const REPORT_PASSAGES_POOL = [
  {
    title: 'Sea Turtles Protection Report',
    text: 'Sea turtles are in danger because people throw plastic and rubbish into the sea. People can stop throwing plastic into the sea and join beach clean-ups. People can also ask boats and ships not to dump rubbish into the ocean. Protecting sea turtles matters because they help keep the ocean healthy. If they disappear, marine ecosystems will suffer greatly.',
    relClause: {
      correct: 'Sea turtles, which are ancient marine reptiles, lay their eggs on sandy beaches.',
      w1: 'Sea turtles which are ancient marine reptiles lay their eggs, on sandy beaches.',
      w2: 'Sea turtles, which are ancient marine reptiles lay their eggs on sandy beaches.',
      w3: 'Sea turtles which are ancient marine reptiles, lay their eggs on sandy beaches.'
    },
    subjectVerb: {
      correct: 'Sea turtles lay their eggs on sandy beaches.',
      wrong: 'Sea turtles lays their eggs on sandy beaches.'
    },
    spelling: {
      prompt: 'If sea turtles ________, marine ecosystems will lose an important species.',
      correct: 'disappear',
      options: ['disappear', 'disapper', 'dissappear', 'dissapper']
    }
  },
  {
    title: 'Coral Reefs Conservation Report',
    text: 'Coral reefs are in grave danger because ocean temperatures are rising and pollution enters coastal waters. People can reduce plastic waste and join coastal conservation programs. Governments can ask large ships not to dump chemicals near reefs. Protecting coral reefs matters because they shelter thousands of marine species. If they disappear, the entire ocean food chain will collapse.',
    relClause: {
      correct: 'Coral reefs, which shelter thousands of marine species, face severe threats from warming oceans.',
      w1: 'Coral reefs which shelter thousands of marine species face severe threats, from warming oceans.',
      w2: 'Coral reefs, which shelter thousands of marine species face severe threats from warming oceans.',
      w3: 'Coral reefs which shelter thousands of marine species, face severe threats from warming oceans.'
    },
    subjectVerb: {
      correct: 'Coral polyps build massive limestone reefs over centuries.',
      wrong: 'Coral polyps builds massive limestone reefs over centuries.'
    },
    spelling: {
      prompt: 'If delicate coral reefs ________, marine biodiversity will be lost.',
      correct: 'disappear',
      options: ['disappear', 'disapper', 'dissappear', 'dissapper']
    }
  }
];

const ARABIC_PASSAGES_POOL = [
  {
    title: 'إدارة الوقت وتنظيم الأولويات (سلاح التلميذ)',
    text: 'الوقتُ كنزٌ ثمينٌ وعطاءٌ إلهي عظيم، والنجاحُ في الحياة لا يتحقق بالأماني، وإنما بحسن إدارة يومنا وترتيب أولوياتنا. يتطلب إنجاز المهام وقتاً محدداً وتركيزاً حثيثاً، والبدء بالأهم قبل المهم. كما يحذر الخبراء من تبديد الوقت في المشتتات وتأجيل عمل اليوم إلى الغد، فالأشخاص الذين ينظمون أوقاتهم هم الأكثر قدرة على تحقيق طموحاتهم وخدمة وطنهم.',
    vocab: { word: 'إنجاز', s: 'يتطلب إنجاز الأعمال تخطيطاً مستمراً', meaning: 'إتمام وتحقيق بنجاح' },
    antonym: { word: 'تأجيل', meaning: 'تعجيل وتبكير' },
    nakiraWord: 'كنزٌ',
    maarefaWord: 'الوقتُ'
  },
  {
    title: 'العمل الجاد وبناء الحضارات (سلاح التلميذ)',
    text: 'العملُ شرفٌ لكل إنسانٍ، وأساسٌ متينٌ لبناء الحضارات وتقدم الأمم والشعوب. لا يتأخر المخلصون عن أداء واجباتهم نحو وطنهم العزيز، ويبذلون قصارى جهدهم في ميادين الإنتاج والمعرفة. إن الفلاح في حقله والعامل في مصنعه كلاهما يسعى لرفعة مصرنا الغالية. فمن يسأل عن سر النهضة يجد أن الإتقان والصبر هما المفتاح الحقيقي لتحقيق المعجزات.',
    vocab: { word: 'قصارى جهدهم', s: 'يبذل المخلصون قصارى جهدهم في العمل', meaning: 'أقصى غاية وسعهم وطاقتهم' },
    antonym: { word: 'يتأخر', meaning: 'يتباكر ويتسارع' },
    nakiraWord: 'شرفٌ',
    maarefaWord: 'العملُ'
  },
  {
    title: 'القراءة ومصادر المعرفة (سلاح التلميذ)',
    text: 'القراءةُ نافذةٌ رحبةٌ يطل منها العقلُ على فضاءات العلم والحكمة. حينما يتأمل الإنسان في صفحات الكتب، يكتشف أفكاراً ملهمة وتجارب تثري حياته وفكره. يتطلب الاستيعاب الجيد تركيزاً حثيثاً وتدويناً للفوائد، دون تسرع أو إهمال. فالأذكياء يستثمرون ساعات فراغهم في المطالعة، لأن العلم رأسُ مالٍ عظيم وسلاحٌ لا يصدأ.',
    vocab: { word: 'حثيثاً', s: 'يتطلب الاستيعاب تركيزاً حثيثاً ومستمراً', meaning: 'سريعاً وجاداً ودقيقاً' },
    antonym: { word: 'إهمال', meaning: 'عناية واهتمام' },
    nakiraWord: 'نافذةٌ',
    maarefaWord: 'القراءةُ'
  }
];

function generateAliAdverbialExam() {
  const subjects = ['The astronaut', 'The Apollo rover', 'Commander Davis', 'The spacecraft', 'The satellite', 'The lunar explorer', 'The flight engineer', 'The pilot'];
  const verbs = ['landed safely', 'launched into orbit', 'reached the space station', 'transmitted clear signals', 'touched down', 'departed the launchpad', 'completed its mission'];
  
  const timePhrases = ['at dawn', 'before sunrise', 'at midnight', 'early yesterday morning', 'in 1969', 'in the twenty-first century', 'after three days', 'during the solar eclipse', 'at 06:00 AM', 'before nightfall'];
  const placePhrases = ['inside the space station', 'on the lunar surface', 'behind the launch tower', 'across the dusty crater', 'near the orbiting satellite', 'deep within the solar system', 'above the Earth atmosphere', 'in the control room'];
  const mannerPhrases = ['with great precision', 'smoothly and silently', 'with incredible speed', 'without any hesitation', 'bravely and calmly', 'with careful calculation', 'effortlessly', 'at high velocity'];

  const questions = [];

  // Q1: Adverbial of TIME Identification (Randomized sentence & time)
  const q1Sub = getRandomElement(subjects);
  const q1Verb = getRandomElement(verbs);
  const q1Time = getRandomElement(timePhrases);
  questions.push({
    id: 'DYN_Y5_001_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: `In the sentence: "<b>${q1Sub} ${q1Verb} <u>${q1Time}</u>.</b>", what type of adverbial is "<u>${q1Time}</u>"?`,
    type: 'MCQ',
    options: ['Adverbial of Time', 'Adverbial of Place', 'Adverbial of Manner', 'Adverbial of Reason'],
    correctAnswer: 'Adverbial of Time',
    points: 1,
    explanation: `💡 Adverbial of Time:\n"${q1Time}" tells us WHEN the action happened (${q1Sub} ${q1Verb}). Time adverbials answer the question "When?".`
  });

  // Q2: Adverbial of PLACE Identification (Randomized sentence & place)
  const q2Sub = getRandomElement(subjects);
  const q2Verb = getRandomElement(verbs);
  const q2Place = getRandomElement(placePhrases);
  const q2TimeAlt = getRandomElement(timePhrases);
  const q2MannerAlt = getRandomElement(mannerPhrases);

  const placeCorrect = `${q2Sub} ${q2Verb} ${q2Place}.`;
  const placeWrong1 = `${q2Sub} ${q2Verb} ${q2TimeAlt}.`;
  const placeWrong2 = `${q2Sub} ${q2Verb} ${q2MannerAlt}.`;
  const placeWrong3 = `${q2Sub} ${q2Verb}.`;

  questions.push({
    id: 'DYN_Y5_002_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: 'Which of the following sentences contains an adverbial of <b>PLACE</b>?',
    type: 'MCQ',
    options: [placeCorrect, placeWrong1, placeWrong2, placeWrong3],
    correctAnswer: placeCorrect,
    points: 1,
    explanation: `💡 Adverbial of Place:\n"${placeCorrect}" contains the prepositional phrase "${q2Place}", which answers the question "Where?".`
  });

  // Q3: Adverbial of MANNER (Identification)
  const q3Sub = getRandomElement(subjects);
  const q3Manner = getRandomElement(mannerPhrases);
  questions.push({
    id: 'DYN_Y5_003_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: `In the sentence: "<b>${q3Sub} steered the vehicle <u>${q3Manner}</u>.</b>", the underlined phrase explains:`,
    type: 'MCQ',
    options: ['HOW or in what way the action occurred (Manner)', 'WHERE the action took place (Place)', 'WHEN the action happened (Time)', 'WHY the action was done (Reason)'],
    correctAnswer: 'HOW or in what way the action occurred (Manner)',
    points: 1,
    explanation: `💡 Adverbial of Manner:\n"${q3Manner}" describes HOW the action was performed.`
  });

  // Q4: Fronted Adverbial Punctuation (Comma Placement)
  const q4Front = getRandomElement(['After a long journey', 'Before the countdown began', 'With steady hands', 'Behind the launchpad', 'In the year ' + getRandomInt(1960, 2024), 'Without warning']);
  const q4Body = `${getRandomElement(subjects).toLowerCase()} touched down safely`;

  const q4Correct = `${q4Front}, ${q4Body}.`;
  const q4Err1 = `${q4Front} ${q4Body}.`;
  const q4Err2 = `${q4Front} the, ${q4Body}.`;
  const q4Err3 = `${q4Front}, and ${q4Body}.`;

  questions.push({
    id: 'DYN_Y5_004_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: `Which sentence is punctuated correctly with a comma after the fronted adverbial?`,
    type: 'MCQ',
    options: [q4Correct, q4Err1, q4Err2, q4Err3],
    correctAnswer: q4Correct,
    points: 1,
    explanation: `💡 Punctuation Rule:\nA fronted adverbial sits at the very beginning of a sentence and MUST be followed by a comma:\n"${q4Correct}".`
  });

  // Q5: Fronted Adverbial of Time (Selection)
  const q5TimeFront = getRandomElement(['Before dawn', 'At sunrise', 'In ' + getRandomInt(1965, 2025), 'Last night', 'During the mission']);
  const q5PlaceFront = getRandomElement(['On the moon', 'Inside the cockpit', 'Across the launch facility', 'Near the crater']);
  const q5MannerFront = getRandomElement(['Silently', 'Bravely', 'With great care', 'Effortlessly']);

  const q5Ans = `${q5TimeFront}, the team monitored all communication frequencies.`;
  const q5W1 = `${q5PlaceFront}, the team monitored all communication frequencies.`;
  const q5W2 = `${q5MannerFront}, the team monitored all communication frequencies.`;
  const q5W3 = `The team monitored all communication frequencies yesterday.`;

  questions.push({
    id: 'DYN_Y5_005_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: 'Select the sentence that begins with a fronted adverbial of <b>TIME</b>:',
    type: 'MCQ',
    options: [q5Ans, q5W1, q5W2, q5W3],
    correctAnswer: q5Ans,
    points: 1,
    explanation: `💡 Fronted Adverbial of Time:\n"${q5TimeFront}" answers "When?" and is positioned at the front of the sentence followed by a comma.`
  });

  // Q6: Sentence Transformation (Moving Adverbial to the Front)
  const q6Year = getRandomInt(1960, 2025);
  const q6Sub = getRandomElement(subjects);
  const q6Verb = getRandomElement(verbs);
  const q6Original = `${q6Sub} ${q6Verb} in ${q6Year}.`;
  const q6Rewritten = `In ${q6Year}, ${q6Sub.toLowerCase()} ${q6Verb}.`;
  const q6RewrittenWrong1 = `In ${q6Year} ${q6Sub.toLowerCase()} ${q6Verb}.`;
  const q6RewrittenWrong2 = `${q6Sub} in ${q6Year}, ${q6Verb}.`;
  const q6RewrittenWrong3 = `In ${q6Year} was ${q6Sub.toLowerCase()} ${q6Verb}.`;

  questions.push({
    id: 'DYN_Y5_006_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: `Rewrite the sentence by moving the adverbial of time to the FRONT: "<b>${q6Original}</b>"`,
    type: 'MCQ',
    options: [q6Rewritten, q6RewrittenWrong1, q6RewrittenWrong2, q6RewrittenWrong3],
    correctAnswer: q6Rewritten,
    points: 1,
    explanation: `💡 Fronting Rule:\nMoving "in ${q6Year}" to the start requires a comma immediately after it: "${q6Rewritten}".`
  });

  // Q7: Dual Adverbials (Both Time AND Place)
  const q7Year = getRandomInt(1970, 2026);
  const q7Place = getRandomElement(placePhrases);
  const q7Sub = getRandomElement(subjects);
  const q7DualSentence = `In ${q7Year}, ${q7Sub.toLowerCase()} conducted research ${q7Place}.`;
  const q7OnlyTime = `In ${q7Year}, ${q7Sub.toLowerCase()} conducted research.`;
  const q7OnlyPlace = `${q7Sub} conducted research ${q7Place}.`;
  const q7OnlyManner = `${q7Sub} conducted research with extreme precision.`;

  questions.push({
    id: 'DYN_Y5_007_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: 'Which sentence contains <b>BOTH</b> an adverbial of time <b>AND</b> an adverbial of place?',
    type: 'MCQ',
    options: [q7DualSentence, q7OnlyTime, q7OnlyPlace, q7OnlyManner],
    correctAnswer: q7DualSentence,
    points: 1,
    explanation: `💡 Dual Adverbials:\n"In ${q7Year}" ➔ Time (When)\n"${q7Place}" ➔ Place (Where)\nBoth exist together in the correct sentence.`
  });

  // Q8: Identify Adverbial Definition
  questions.push({
    id: 'DYN_Y5_008_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: 'What is an adverbial in English grammar?',
    type: 'MCQ',
    options: [
      'A word or phrase that adds detail about time, place, or manner to a verb or clause',
      'A single noun that names a person, place, or thing',
      'A word that joins two independent clauses together',
      'A punctuation mark used to separate paragraphs'
    ],
    correctAnswer: 'A word or phrase that adds detail about time, place, or manner to a verb or clause',
    points: 1,
    explanation: '💡 Adverbial Definition:\nAn adverbial can be a single adverb (e.g. "quietly") or a prepositional phrase (e.g. "in the morning") that gives extra context to the action.'
  });

  // Q9: Fill-in-the-Blank Manner
  const q9MannerGood = getRandomElement(['with extraordinary caution', 'carefully and patiently', 'smoothly without any delay', 'with great accuracy']);
  const q9Sub = getRandomElement(subjects);
  questions.push({
    id: 'DYN_Y5_009_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: `Complete the sentence with the most appropriate adverbial of <b>MANNER</b>: "${q9Sub} operated the delicate equipment ________."`,
    type: 'MCQ',
    options: [q9MannerGood, 'yesterday morning', 'on the launch pad', 'because it was expensive'],
    correctAnswer: q9MannerGood,
    points: 1,
    explanation: `💡 Adverbial of Manner:\n"${q9MannerGood}" describes HOW the equipment was operated.`
  });

  // Q10: True / False Evaluation
  const q10Sentence = `In ${getRandomInt(1950, 2020)}, engineers built the first space satellite.`;
  questions.push({
    id: 'DYN_Y5_010_' + Utilities.getUuid().slice(0, 6),
    grade: 'Year 5 (G5)',
    subject: 'English Grammar',
    unit: 'Unit 2 - Lesson 3: Adverbials',
    text: `True or False: In the sentence "<b>${q10Sentence}</b>", the fronted adverbial answers the question "Where?".`,
    type: 'TRUE_FALSE',
    options: ['False (It answers "When?")', 'True (It answers "Where?")'],
    correctAnswer: 'False (It answers "When?")',
    points: 1,
    explanation: `💡 Concept Check:\nA year (like 1957 or 1999) indicates TIME, not PLACE.`
  });

  return questions;
}

/**
 * Procedural Generator for Mostafa Ahmed (Grade 6 English Literacy & Report Writing)
 */


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
    explanation: `💡 Simile Identification:\nA simile compares two things using "like" or "as": "${fantasy.simile.phrase}".`
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
    explanation: `💡 Personification:\nGiving human actions or qualities to non-human objects or nature.`
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
    explanation: `💡 Metaphor Analysis:\n"${fantasy.metaphor.phrase}" emphasizes: ${fantasy.metaphor.meaning}`
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
    explanation: `💡 Literary Mood:\nThe author uses sensory descriptions to create an immersive, suspenseful mood.`
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
    explanation: `💡 Vocabulary in Context:\n"${fantasy.vocab.word}" means: ${fantasy.vocab.meaning}.`
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
    explanation: '💡 Non-defining Relative Clauses:\nExtra information introduced with "which" must be separated by a pair of commas: ", which ..., ".'
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
    explanation: '💡 Subject-Verb Agreement:\nPlural subjects take plural verbs without -s (e.g., "polyps build", "turtles lay").'
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
    explanation: `💡 Spelling Rule:\nThe correct spelling is "${report.spelling.correct}".`
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
    explanation: '💡 Connectives:\n"Because" introduces the reason explaining why protection is essential.'
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
    explanation: '💡 Repairing Run-ons:\nJoin two complete independent clauses with a comma and coordinating conjunction (", and").'
  });

  return questions;
}



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
    explanation: `💡 المعرف بأل:\nالاسم الذي يبدأ بـ (أل) التعريف هو اسم معرفة يدل على شيء معين ومحدد.`
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
    explanation: `💡 الاسم النكرة:\nاسم منون ومجرد من أل والإضافة، ويدل على مسمى عام غير محدد.`
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
    explanation: '💡 أسماء الأعلام:\nأسماء الأشخاص والبلدان والأنهار والمدن هي أسماء معارف لأنها تدل على مسمى محدد بذاته.'
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
    explanation: '💡 تحديد المعرفة:\n(المخلصون) معرف بأل، بينما باقي الكلمات نكرات.'
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
    explanation: '💡 إعراب النكرة:\n(كنزٌ) اسم نكرة مرفوع بالضمة ومجرد من أل.'
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
    explanation: '💡 قاعدة الفتح بعد فتح:\nتكتب الهمزة المتوسطة على ألف إذا كانت مفتوحة وما قبلها حرف مفتوح.'
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
    explanation: '💡 قاعدة السكون بعد فتح:\nالفتحة أقوى من السكون، لذلك إذا كانت الهمزة ساكنة وقبلها حرف مفتوح تُكتب على ألف.'
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
    explanation: '💡 قاعدة الفتح بعد سكون:\nفي كلمة (يَسْـأَلُ): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون ➔ فتُرسم على ألف.'
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
    explanation: `💡 دلالة الكلمة في سياق النص:\nكلمة (${arb.vocab.word}) في هذا النص تعني: ${arb.vocab.meaning}.`
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
    explanation: `💡 المضاد اللغوي في سياق النص:\nمضاد (${arb.antonym.word}) هو: ${arb.antonym.meaning}.`
  });

  return questions;
}


function getExamInfo(examCode) {
  const catalog = {
    'EX_Y5_ENG_ADV01': { code: 'EX_Y5_ENG_ADV01', title: 'English Grammar: Adverbials of Time, Place & Manner (Unit 2)', grade: 'Year 5 (G5)', subject: 'English Grammar', questionsCount: 10, duration: 20 },
    'EX_Y6_ENG_FANTASY01': { code: 'EX_Y6_ENG_FANTASY01', title: 'English Literacy: Fantasy Reading "The City That Waited" & Report Writing', grade: 'Grade 6 (G6)', subject: 'English Literacy', questionsCount: 10, duration: 20 },
    'EX_Y6_ARB_PRIO01': { code: 'EX_Y6_ARB_PRIO01', title: 'Arabic Language: Reading Comprehension, Grammar & Spelling (Diagnostic)', grade: 'Grade 6 (G6)', subject: 'Arabic Language (Diagnostic)', questionsCount: 10, duration: 20 }
  };
  return catalog[examCode] || catalog['EX_Y5_ENG_ADV01'];
}

/**
 * Procedurally generates 10 brand-new questions on EVERY ATTEMPT,
 * with reading passages dynamically attached!
 */
function getExamData(examCode) {
  const exam = getExamInfo(examCode);
  let questions = [];

  if (examCode === 'EX_Y5_ENG_ADV01') {
    questions = generateAliAdverbialExam();
  } else if (examCode === 'EX_Y6_ENG_FANTASY01') {
    questions = generateMostafaEnglishExam();
  } else if (examCode === 'EX_Y6_ARB_PRIO01') {
    questions = generateMostafaArabicExam();
  } else {
    questions = generateAliAdverbialExam();
  }

  // 1. Shuffle question order
  questions = shuffleArray(questions);

  // 2. Shuffle options inside each question
  for (let i = 0; i < questions.length; i++) {
    if (questions[i].options && questions[i].options.length > 1) {
      questions[i].options = shuffleArray(questions[i].options);
    }
  }

  // 3. Store answer key in CacheService for 3 hours
  const sessionKey = 'sess_' + examCode + '_' + Utilities.getUuid().slice(0, 10);
  const answerKey = {};
  questions.forEach(q => {
    answerKey[q.id] = {
      correctAnswer: q.correctAnswer,
      points: q.points || 1,
      explanation: q.explanation,
      text: q.text
    };
  });

  try {
    CacheService.getScriptCache().put(sessionKey, JSON.stringify(answerKey), 10800);
  } catch(e) {
    Logger.log('CacheService put error: ' + e);
  }

  return {
    success: true,
    sessionKey: sessionKey,
    exam: exam,
    questions: questions.map(q => ({
      id: q.id,
      grade: q.grade,
      subject: q.subject,
      unit: q.unit,
      text: q.text,
      type: q.type,
      options: q.options,
      points: q.points,
      passage: q.passage || ''
    }))
  };
}

function submitExamAnswers(payload) {
  try {
    const ss = getSpreadsheet();
    let subSheet = ss.getSheetByName('Submissions');
    if (!subSheet) {
      setupDatabase(ss);
      subSheet = ss.getSheetByName('Submissions');
    }
    const retakeSheet = ss.getSheetByName('Retake_Requests');

    const data = (typeof payload === 'string') ? JSON.parse(payload) : payload;
    const { studentName, schoolGroup, examCode, answers, durationSpent, sessionKey } = data;

    let answerKey = {};
    if (sessionKey) {
      const cached = CacheService.getScriptCache().get(sessionKey);
      if (cached) {
        answerKey = JSON.parse(cached);
      }
    }

    let earnedScore = 0;
    let totalScore = 0;
    const reviewDetails = [];

    for (const qId in answers) {
      const studentAns = String(answers[qId] || '').trim();
      const meta = answerKey[qId] || { correctAnswer: '', points: 1, explanation: '', text: '' };
      
      const isCorrect = (studentAns.toLowerCase() === meta.correctAnswer.toLowerCase());
      if (isCorrect) {
        earnedScore += meta.points;
      }
      totalScore += meta.points;

      reviewDetails.push({
        questionId: qId,
        questionText: meta.text,
        studentAnswer: studentAns,
        correctAnswer: meta.correctAnswer,
        isCorrect: isCorrect,
        pointsAwarded: isCorrect ? meta.points : 0,
        maxPoints: meta.points,
        explanation: meta.explanation
      });
    }

    const percentage = totalScore > 0 ? Math.round((earnedScore / totalScore) * 100) : 0;
    
    let rating = 'Needs Practice 🌱';
    if (percentage >= 85) rating = 'Excellent 🌟';
    else if (percentage >= 75) rating = 'Very Good 👏';
    else if (percentage >= 65) rating = 'Good 👍';
    else if (percentage >= 50) rating = 'Satisfactory 📚';

    const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
    const summaryStr = `${earnedScore}/${totalScore} Correct (${percentage}%)`;

    subSheet.appendRow([
      timestamp,
      studentName,
      schoolGroup || 'General',
      examCode,
      earnedScore,
      totalScore,
      percentage + '%',
      rating,
      durationSpent || 'Not specified',
      summaryStr,
      JSON.stringify(reviewDetails)
    ]);

    const lastRow = subSheet.getLastRow();
    subSheet.getRange(lastRow, 1, 1, 10).setVerticalAlignment('middle').setFontSize(10);
    subSheet.getRange(lastRow, 5, 1, 3).setHorizontalAlignment('center');

    if (retakeSheet && retakeSheet.getLastRow() > 1) {
      const rData = retakeSheet.getDataRange().getValues();
      for (let i = 1; i < rData.length; i++) {
        if (rData[i][2] === studentName && rData[i][3] === examCode && rData[i][6] === 'APPROVED') {
          retakeSheet.getRange(i + 1, 7).setValue('CONSUMED');
        }
      }
    }

    return {
      success: true,
      earnedScore: earnedScore,
      totalScore: totalScore,
      percentage: percentage,
      rating: rating,
      review: reviewDetails
    };

  } catch (err) {
    return {
      success: false,
      message: 'Failed to record student answers: ' + err.toString()
    };
  }
}


function formatPercentValue(val) {
  if (typeof val === 'number') {
    return Math.round(val <= 1 ? val * 100 : val) + '%';
  }
  const s = String(val || '').trim();
  if (!s) return '0%';
  if (s.endsWith('%')) return s;
  const num = parseFloat(s);
  if (!isNaN(num)) {
    return Math.round(num <= 1 ? num * 100 : num) + '%';
  }
  return s;
}

function ensureAliRecord(subSheet) {
  if (!subSheet) return;
  if (subSheet.getLastRow() <= 1) {
    seedAliSubmissionRow(subSheet);
    return;
  }
  
  const data = subSheet.getDataRange().getValues();
  let found = false;
  for (let i = 1; i < data.length; i++) {
    const name = String(data[i][1] || '').trim().toLowerCase();
    const exam = String(data[i][3] || '').trim().toUpperCase();
    if ((name.includes('ali') || name.includes('علي')) && (exam.includes('ADV01') || exam.includes('ENG') || exam.includes('Y5'))) {
      found = true;
      break;
    }
  }
  
  if (!found) {
    seedAliSubmissionRow(subSheet);
  }
}

function seedAliSubmissionRow(subSheet) {
  const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
  const reviewJson = JSON.stringify([
    {
      questionId: "Q_Y5_ENG_001",
      questionText: "What is an adverbial?",
      studentAnswer: "A group of words without a verb that adds detail about time, place, or manner",
      correctAnswer: "A group of words without a verb that adds detail about time, place, or manner",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "An adverbial is a word or phrase that gives extra details about WHEN, WHERE, or HOW an action happens. It does NOT contain a finite verb."
    },
    {
      questionId: "Q_Y5_ENG_002",
      questionText: 'In the sentence: "The rocket launched at dawn.", what type of adverbial is "at dawn"?',
      studentAnswer: "Adverbial of Time",
      correctAnswer: "Adverbial of Time",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"at dawn" tells us WHEN the rocket launched (Adverbial of Time).'
    },
    {
      questionId: "Q_Y5_ENG_003",
      questionText: "Which of the following sentences contains an adverbial of PLACE?",
      studentAnswer: "The crew slept inside the space station.",
      correctAnswer: "The crew slept inside the space station.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"inside the space station" answers the question WHERE did the crew sleep (Adverbial of Place).'
    },
    {
      questionId: "Q_Y5_ENG_004",
      questionText: "An adverbial of MANNER answers which question?",
      studentAnswer: "How or in what way?",
      correctAnswer: "How or in what way?",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "Adverbials of manner explain HOW an action happens (e.g., bravely, with great care, silently)."
    },
    {
      questionId: "Q_Y5_ENG_005",
      questionText: "Which sentence is punctuated correctly with a comma after the fronted adverbial?",
      studentAnswer: "After a long journey the crew landed.",
      correctAnswer: "After a long journey, the crew landed.",
      isCorrect: false,
      pointsAwarded: 0,
      maxPoints: 1,
      explanation: "When an adverbial is at the start (Fronted Adverbial), it must be followed by a comma."
    },
    {
      questionId: "Q_Y5_ENG_006",
      questionText: 'True or False: In the sentence "The USSR launched Sputnik I in 1957.", we must put a comma before "in 1957".',
      studentAnswer: "False",
      correctAnswer: "False",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "When the adverbial is at the END of a sentence, NO comma is needed."
    },
    {
      questionId: "Q_Y5_ENG_007",
      questionText: "Choose the sentence that has an adverbial of TIME at the beginning:",
      studentAnswer: "Before sunrise, the pilot took off.",
      correctAnswer: "Before sunrise, the pilot took off.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"Before sunrise" tells us WHEN the pilot took off.'
    },
    {
      questionId: "Q_Y5_ENG_008",
      questionText: 'Complete the sentence with the best adverbial of manner: "The engineer repaired the delicate wiring ........',
      studentAnswer: "with great care",
      correctAnswer: "with great care",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"with great care" describes HOW the engineer repaired the wires.'
    },
    {
      questionId: "Q_Y5_ENG_009",
      questionText: 'Rewrite "Astronauts walked on the moon in 1969." by moving the adverbial of time to the start:',
      studentAnswer: "In 1969, astronauts walked on the moon.",
      correctAnswer: "In 1969, astronauts walked on the moon.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: 'Move "In 1969" to the front and place a comma directly after it.'
    },
    {
      questionId: "Q_Y5_ENG_010",
      questionText: "Which sentence has BOTH an adverbial of time AND an adverbial of place?",
      studentAnswer: "In 1969, astronauts walked on the moon.",
      correctAnswer: "In 1969, astronauts walked on the moon.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"In 1969" is Time, and "on the moon" is Place.'
    }
  ]);

  subSheet.appendRow([
    timestamp,
    'Ali Ahmed',
    'Year 5 (G5)',
    'EX_Y5_ENG_ADV01',
    9,
    10,
    '90%',
    'Excellent 🌟',
    '7 min 42 sec',
    '9/10 Correct (1 mistake reviewed)',
    reviewJson
  ]);
  
  const lastRow = subSheet.getLastRow();
  subSheet.getRange(lastRow, 1, 1, 10).setVerticalAlignment('middle').setFontSize(10);
  subSheet.getRange(lastRow, 5, 1, 3).setHorizontalAlignment('center');
}


function getStudentExamStatus(studentName, examCode) {
  try {
    const ss = getSpreadsheet();
    let subSheet = ss.getSheetByName('Submissions');
    const retakeSheet = ss.getSheetByName('Retake_Requests');

    if (!subSheet) {
      setupDatabase(ss);
      subSheet = ss.getSheetByName('Submissions');
    }

    // Auto-seed historical submissions
    restoreAllHistoricalSubmissions();

    let hasSubmitted = false;
    const attempts = [];

    const targetName = String(studentName || '').trim().toLowerCase();
    const targetExam = String(examCode || '').trim().toUpperCase();

    if (subSheet && subSheet.getLastRow() > 1) {
      const sData = subSheet.getDataRange().getValues();
      for (let i = 1; i < sData.length; i++) {
        const rowName = String(sData[i][1] || '').trim().toLowerCase();
        const rowExam = String(sData[i][3] || '').trim().toUpperCase();

        const isStudentMatch = (rowName === targetName) || 
          (targetName.includes('ali') && (rowName.includes('ali') || rowName.includes('علي'))) ||
          (targetName.includes('mostafa') && (rowName.includes('mostafa') || rowName.includes('مصطفى')));
          
        const isExamMatch = (rowExam === targetExam) ||
          (targetExam.includes('ADV01') && (rowExam.includes('ADV') || rowExam.includes('ENG_G5'))) ||
          (targetExam.includes('FANTASY01') && (rowExam.includes('FANTASY') || rowExam.includes('ENG_G6'))) ||
          (targetExam.includes('ARB_PRIO01') && (rowExam.includes('ARB') || rowExam.includes('PRIO')));

        if (isStudentMatch && isExamMatch) {
          hasSubmitted = true;
          const score = Number(sData[i][4]) || 0;
          const total = Number(sData[i][5]) || 0;
          const pct = formatPercentValue(sData[i][6]);
          const rating = String(sData[i][7] || '');
          const duration = String(sData[i][8] || '');
          const summary = String(sData[i][9] || '');
          const dateStr = sData[i][0] instanceof Date ? Utilities.formatDate(sData[i][0], Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm') : String(sData[i][0]);

          let review = [];
          try { review = JSON.parse(sData[i][10] || '[]'); } catch(e) {}

          attempts.push({
            attemptNumber: attempts.length + 1,
            timestamp: dateStr,
            score: score,
            total: total,
            percentage: pct,
            rating: rating,
            duration: duration,
            summary: summary,
            review: review
          });
        }
      }
    }

    let retakeStatus = 'NONE';
    let requestId = '';

    if (retakeSheet && retakeSheet.getLastRow() > 1) {
      const rData = retakeSheet.getDataRange().getValues();
      for (let i = rData.length - 1; i >= 1; i--) {
        const rowName = String(rData[i][2] || '').trim().toLowerCase();
        const rowExam = String(rData[i][3] || '').trim().toUpperCase();

        const isStudentMatch = (rowName === targetName) || 
          (targetName.includes('ali') && (rowName.includes('ali') || rowName.includes('علي'))) ||
          (targetName.includes('mostafa') && (rowName.includes('mostafa') || rowName.includes('مصطفى')));
          
        const isExamMatch = (rowExam === targetExam) ||
          (targetExam.includes('ADV01') && (rowExam.includes('ADV') || rowExam.includes('ENG_G5'))) ||
          (targetExam.includes('FANTASY01') && (rowExam.includes('FANTASY') || rowExam.includes('ENG_G6'))) ||
          (targetExam.includes('ARB_PRIO01') && (rowExam.includes('ARB') || rowExam.includes('PRIO')));

        if (isStudentMatch && isExamMatch) {
          retakeStatus = String(rData[i][6]).trim();
          requestId = String(rData[i][0]).trim();
          break;
        }
      }
    }

    const latestAttempt = attempts.length > 0 ? attempts[attempts.length - 1] : null;
    const lastScore = latestAttempt ? `${latestAttempt.score} / ${latestAttempt.total} (${latestAttempt.percentage})` : '';
    const lastDate = latestAttempt ? latestAttempt.timestamp : '';
    const canAttempt = (attempts.length < 2) || (retakeStatus === 'APPROVED');

    return {
      success: true,
      hasSubmitted: hasSubmitted,
      attemptsCount: attempts.length,
      attempts: attempts,
      lastScore: lastScore,
      lastDate: lastDate,
      canAttempt: canAttempt,
      retakeStatus: retakeStatus,
      requestId: requestId
    };
  } catch(e) {
    return { success: false, message: e.toString() };
  }
}

function requestExamRetake(payload) {
  try {
    const ss = getSpreadsheet();
    let retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet) {
      setupDatabase(ss);
      retakeSheet = ss.getSheetByName('Retake_Requests');
    }

    const data = (typeof payload === 'string') ? JSON.parse(payload) : payload;
    const { studentName, examCode, examTitle, previousScore, reason } = data;

    const reqId = 'REQ_' + Utilities.formatDate(new Date(), 'GMT', 'yyyyMMdd_HHmmss');
    const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');

    retakeSheet.appendRow([
      reqId,
      timestamp,
      studentName,
      examCode,
      examTitle || examCode,
      previousScore || 'N/A',
      'PENDING',
      reason || 'Second attempt requested to review mistakes',
      ''
    ]);

    return {
      success: true,
      requestId: reqId,
      message: 'Retake request sent to parent dashboard successfully.'
    };
  } catch(e) {
    return { success: false, message: 'Failed to send retake request: ' + e.toString() };
  }
}

function approveRetakeRequest(requestId) {
  try {
    const ss = getSpreadsheet();
    const retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet || retakeSheet.getLastRow() <= 1) return { success: false, message: 'No retake requests found' };

    const data = retakeSheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      if (String(data[i][0]).trim() === requestId) {
        retakeSheet.getRange(i + 1, 7).setValue('APPROVED');
        retakeSheet.getRange(i + 1, 9).setValue(new Date());
        return { success: true, message: 'Retake approved. The student can now start their assessment.' };
      }
    }
    return { success: false, message: 'Request ID not found' };
  } catch(e) {
    return { success: false, message: e.toString() };
  }
}

function rejectRetakeRequest(requestId) {
  try {
    const ss = getSpreadsheet();
    const retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet || retakeSheet.getLastRow() <= 1) return { success: false, message: 'No retake requests found' };

    const data = retakeSheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      if (String(data[i][0]).trim() === requestId) {
        retakeSheet.getRange(i + 1, 7).setValue('REJECTED');
        retakeSheet.getRange(i + 1, 9).setValue(new Date());
        return { success: true, message: 'Retake request declined.' };
      }
    }
    return { success: false, message: 'Request ID not found' };
  } catch(e) {
    return { success: false, message: e.toString() };
  }
}

function getAdminDashboardData() {
  try {
    const ss = getSpreadsheet();
    let subSheet = ss.getSheetByName('Submissions');
    let exSheet = ss.getSheetByName('Exams');
    let retakeSheet = ss.getSheetByName('Retake_Requests');

    if (!subSheet || !exSheet) {
      setupDatabase(ss);
      subSheet = ss.getSheetByName('Submissions');
      exSheet = ss.getSheetByName('Exams');
      retakeSheet = ss.getSheetByName('Retake_Requests');
    }

    const submissions = [];
    if (subSheet && subSheet.getLastRow() > 1) {
      const data = subSheet.getDataRange().getValues();
      for (let i = 1; i < data.length; i++) {
        let review = [];
        try {
          review = JSON.parse(data[i][10] || data[i][9] || '[]');
        } catch(e) {}

        const rawDate = data[i][0];
        let dateStr = '';
        if (rawDate instanceof Date) {
          dateStr = Utilities.formatDate(rawDate, Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
        } else {
          dateStr = String(rawDate || '');
        }

        submissions.push({
          id: i,
          timestamp: dateStr,
          studentName: String(data[i][1] || 'Unknown'),
          schoolGroup: String(data[i][2] || ''),
          examCode: String(data[i][3] || ''),
          earnedScore: Number(data[i][4]) || 0,
          totalScore: Number(data[i][5]) || 0,
          percentage: String(data[i][6] || '0%'),
          rating: String(data[i][7] || ''),
          durationSpent: String(data[i][8] || ''),
          review: review
        });
      }
      submissions.reverse();
    }

    const exams = [];
    if (exSheet && exSheet.getLastRow() > 1) {
      const data = exSheet.getDataRange().getValues();
      for (let i = 1; i < data.length; i++) {
        exams.push({
          code: String(data[i][0] || ''),
          title: String(data[i][1] || ''),
          grade: String(data[i][2] || ''),
          subject: String(data[i][3] || ''),
          questionsCount: Number(data[i][4]) || 0,
          duration: Number(data[i][5]) || 0,
          status: String(data[i][6] || 'ACTIVE')
        });
      }
    }

    // Preview sample generated questions with passages for the parent inspector
    const sampleAli = generateAliAdverbialExam();
    const sampleMostafaEng = generateMostafaEnglishExam();
    const sampleMostafaArb = generateMostafaArabicExam();
    const allQuestions = [
      ...sampleAli.map(q => ({ ...q, examCode: 'EX_Y5_ENG_ADV01' })),
      ...sampleMostafaEng.map(q => ({ ...q, examCode: 'EX_Y6_ENG_FANTASY01' })),
      ...sampleMostafaArb.map(q => ({ ...q, examCode: 'EX_Y6_ARB_PRIO01' }))
    ];

    const retakeRequests = [];
    if (retakeSheet && retakeSheet.getLastRow() > 1) {
      const rData = retakeSheet.getDataRange().getValues();
      for (let i = 1; i < rData.length; i++) {
        const rawDate = rData[i][1];
        let dateStr = '';
        if (rawDate instanceof Date) {
          dateStr = Utilities.formatDate(rawDate, Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
        } else {
          dateStr = String(rawDate || '');
        }

        retakeRequests.push({
          id: String(rData[i][0] || ''),
          timestamp: dateStr,
          studentName: String(rData[i][2] || ''),
          examCode: String(rData[i][3] || ''),
          examTitle: String(rData[i][4] || ''),
          previousScore: String(rData[i][5] || ''),
          status: String(rData[i][6] || 'PENDING'),
          reason: String(rData[i][7] || '')
        });
      }
      retakeRequests.reverse();
    }

    return {
      success: true,
      sheetUrl: ss.getUrl(),
      submissions: submissions,
      exams: exams,
      allQuestions: allQuestions,
      retakeRequests: retakeRequests
    };

  } catch (err) {
    return {
      success: false,
      message: 'Error loading admin data: ' + err.toString()
    };
  }
}

function generateGoogleFormPrompt() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt('Generate Google Form', 'Enter Exam Code (e.g., EX_Y5_ENG_ADV01 or EX_Y6_ENG_FANTASY01):', ui.ButtonSet.OK_CANCEL);
  if (response.getSelectedButton() === ui.Button.OK) {
    const examCode = response.getResponseText().trim();
    if (!examCode) {
      ui.alert('Please enter an exam code.');
      return;
    }
    createGoogleFormFromExam(examCode);
  }
}

function createGoogleFormFromExam(examCode) {
  const examDataRes = getExamData(examCode);
  if (!examDataRes.success || examDataRes.questions.length === 0) {
    try { SpreadsheetApp.getUi().alert('No questions found for code: ' + examCode); } catch(e){}
    return;
  }

  const exam = examDataRes.exam;
  const questions = examDataRes.questions;

  const form = FormApp.create(exam.title + ' - (' + exam.grade + ')');
  form.setDescription('Interactive Assessment for ' + exam.subject + '\nDuration: ' + exam.duration + ' Minutes\nPlease complete all questions carefully.')
      .setIsQuiz(true)
      .setAllowResponseEdits(false)
      .setCollectEmail(false);

  form.addTextItem().setTitle('Student Full Name:').setRequired(true);
  form.addTextItem().setTitle('School / Class:').setRequired(false);

  questions.forEach((q, idx) => {
    const qTitle = '(' + (idx + 1) + ') ' + q.text.replace(/<[^>]*>?/gm, '');
    if (q.type === 'MCQ' || q.type === 'TRUE_FALSE') {
      const item = form.addMultipleChoiceItem().setTitle(qTitle).setRequired(true);
      const choices = q.options.map(opt => item.createChoice(opt));
      item.setChoices(choices);
    } else {
      form.addTextItem().setTitle(qTitle).setRequired(true);
    }
  });

  const publishedUrl = form.getPublishedUrl();
  try {
    SpreadsheetApp.getUi().alert('🎉 Google Form created successfully!\n\nStudent link:\n' + publishedUrl);
  } catch(e) {
    Logger.log('Form created: ' + publishedUrl);
  }
}

function copyWebAppUrl() {
  const url = ScriptApp.getService().getUrl();
  try {
    SpreadsheetApp.getUi().alert('Interactive Web App Link:\n\n' + (url || 'Please deploy script as Web App first.'));
  } catch(e) {
    Logger.log(url);
  }
}

function openLinkedSheetUrl() {
  const ss = getSpreadsheet();
  try {
    SpreadsheetApp.getUi().alert('Linked Google Sheet URL:\n\n' + ss.getUrl());
  } catch(e) {
    Logger.log(ss.getUrl());
  }
}

/**
 * ============================================================
 * FULL HISTORICAL RESTORATION ENGINE (Ali Ahmed & Mostafa Ahmed)
 * Fully restores all 3 completed assessments with exact scores & reviews.
 * ============================================================
 */
function getHistoricalSubmissionsData() {
  const aliReview = [
    {
      questionId: "Q_Y5_ENG_001",
      questionText: "What is an adverbial?",
      studentAnswer: "A group of words without a verb that adds detail about time, place, or manner",
      correctAnswer: "A group of words without a verb that adds detail about time, place, or manner",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "An adverbial is a word or phrase that gives extra details about WHEN, WHERE, or HOW an action happens. It does NOT contain a finite verb."
    },
    {
      questionId: "Q_Y5_ENG_002",
      questionText: 'In the sentence: "The rocket launched at dawn.", what type of adverbial is "at dawn"?',
      studentAnswer: "Adverbial of Time",
      correctAnswer: "Adverbial of Time",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"at dawn" tells us WHEN the rocket launched (Adverbial of Time).'
    },
    {
      questionId: "Q_Y5_ENG_003",
      questionText: "Which of the following sentences contains an adverbial of PLACE?",
      studentAnswer: "The crew slept inside the space station.",
      correctAnswer: "The crew slept inside the space station.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"inside the space station" answers the question WHERE did the crew sleep (Adverbial of Place).'
    },
    {
      questionId: "Q_Y5_ENG_004",
      questionText: "An adverbial of MANNER answers which question?",
      studentAnswer: "How or in what way?",
      correctAnswer: "How or in what way?",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "Adverbials of manner explain HOW an action happens (e.g., bravely, with great care, silently)."
    },
    {
      questionId: "Q_Y5_ENG_005",
      questionText: "Which sentence is punctuated correctly with a comma after the fronted adverbial?",
      studentAnswer: "After a long journey the crew landed.",
      correctAnswer: "After a long journey, the crew landed.",
      isCorrect: false,
      pointsAwarded: 0,
      maxPoints: 1,
      explanation: "When an adverbial is at the start (Fronted Adverbial), it must be followed by a comma."
    },
    {
      questionId: "Q_Y5_ENG_006",
      questionText: 'True or False: In the sentence "The USSR launched Sputnik I in 1957.", we must put a comma before "in 1957".',
      studentAnswer: "False",
      correctAnswer: "False",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "When the adverbial is at the END of a sentence, NO comma is needed."
    },
    {
      questionId: "Q_Y5_ENG_007",
      questionText: "Choose the sentence that has an adverbial of TIME at the beginning:",
      studentAnswer: "Before sunrise, the pilot took off.",
      correctAnswer: "Before sunrise, the pilot took off.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"Before sunrise" tells us WHEN the pilot took off.'
    },
    {
      questionId: "Q_Y5_ENG_008",
      questionText: 'Complete the sentence with the best adverbial of manner: "The engineer repaired the delicate wiring ........',
      studentAnswer: "with great care",
      correctAnswer: "with great care",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"with great care" describes HOW the engineer repaired the wires.'
    },
    {
      questionId: "Q_Y5_ENG_009",
      questionText: 'Rewrite "Astronauts walked on the moon in 1969." by moving the adverbial of time to the start:',
      studentAnswer: "In 1969, astronauts walked on the moon.",
      correctAnswer: "In 1969, astronauts walked on the moon.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: 'Move "In 1969" to the front and place a comma directly after it.'
    },
    {
      questionId: "Q_Y5_ENG_010",
      questionText: "Which sentence has BOTH an adverbial of time AND an adverbial of place?",
      studentAnswer: "In 1969, astronauts walked on the moon.",
      correctAnswer: "In 1969, astronauts walked on the moon.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"In 1969" is Time, and "on the moon" is Place.'
    }
  ];

  const mostafaEngReview = [
    {
      questionId: "Q_Y6_ENG_001",
      questionText: 'What genre best describes "The City That Waited"?',
      studentAnswer: "Fantasy Fiction with mysterious world-building",
      correctAnswer: "Fantasy Fiction with mysterious world-building",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "The story takes place in a magical city frozen in time."
    },
    {
      questionId: "Q_Y6_ENG_002",
      questionText: 'Identify the non-finite clause in: "Climbing the winding spiral staircase, Leo heard distant gears."',
      studentAnswer: "Climbing the winding spiral staircase",
      correctAnswer: "Climbing the winding spiral staircase",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "Begins with an -ing participle and has no finite verb."
    },
    {
      questionId: "Q_Y6_ENG_003",
      questionText: 'Which relative pronoun best combines: "The ancient clock tower, ________ gears were made of polished bronze, chimed."',
      studentAnswer: "whose",
      correctAnswer: "whose",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"whose" shows possession of the gears.'
    },
    {
      questionId: "Q_Y6_ENG_004",
      questionText: "In a non-chronological report about Sea Turtles, which heading is most appropriate for their nesting habits?",
      studentAnswer: "Breeding and Nesting Behaviour",
      correctAnswer: "Breeding and Nesting Behaviour",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "Formal sub-heading organizing biological facts."
    },
    {
      questionId: "Q_Y6_ENG_005",
      questionText: "Choose the formal non-chronological report connective expressing contrast:",
      studentAnswer: "In contrast",
      correctAnswer: "In contrast",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"In contrast" is a formal connective comparing differences.'
    },
    {
      questionId: "Q_Y6_ENG_006",
      questionText: "Which sentence embeds a non-restrictive relative clause correctly?",
      studentAnswer: "Sea turtles, which are ancient reptiles, lay their eggs on sandy beaches.",
      correctAnswer: "Sea turtles, which are ancient reptiles, lay their eggs on sandy beaches.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "Non-restrictive relative clause surrounded by a pair of commas."
    },
    {
      questionId: "Q_Y6_ENG_007",
      questionText: "Choose the sentence with correct subject-verb agreement:",
      studentAnswer: "Sea turtles lay their eggs on sandy beaches.",
      correctAnswer: "Sea turtles lay their eggs on sandy beaches.",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: 'Plural subject "Sea turtles" takes base plural verb "lay".'
    },
    {
      questionId: "Q_Y6_ENG_008",
      questionText: 'Correct the spelling mistake in: "Some sea turtles have a herd shell on their backs."',
      studentAnswer: "hard shell",
      correctAnswer: "hard shell",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "Tough, solid shell = hard shell."
    },
    {
      questionId: "Q_Y6_ENG_009",
      questionText: 'True or False: In "Shadows stretched along the walls, long and thin as fingers.", the author uses a simile.',
      studentAnswer: "True",
      correctAnswer: "True",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: 'Uses "as" to compare shadows to elongated fingers.'
    },
    {
      questionId: "Q_Y6_ENG_010",
      questionText: 'Complete the conclusion sentence using formal connective: "Protecting sea turtles matters ________ they play a vital role in marine ecosystems."',
      studentAnswer: "because",
      correctAnswer: "because",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: '"because" gives the reason explaining why protection is essential.'
    }
  ];

  const mostafaArbReview = [
    {
      questionId: "DYN_Y6_ARB_008",
      questionText: "ما سبب كتابة الهمزة على ألف في كلمة (يَسْـأَلُ)؟",
      studentAnswer: "لأن الهمزة مكسورة وما قبلها مضموم",
      correctAnswer: "لأن الهمزة مفتوحة وما قبلها حرف ساكن",
      isCorrect: false,
      pointsAwarded: 0,
      maxPoints: 1,
      explanation: "في كلمة (يَسْـأَلُ): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون ➔ فتُرسم على ألف."
    },
    {
      questionId: "DYN_Y6_ARB_009",
      questionText: 'معنى كلمة (إنجاز) في سياق جملة "يتطلب إنجاز الأعمال تخطيطاً مستمراً" هو:',
      studentAnswer: "إتمام وتحقيق بنجاح",
      correctAnswer: "إتمام وتحقيق بنجاح",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "إنجاز الشيء = إتمامه وقضاؤه بنجاح."
    },
    {
      questionId: "DYN_Y6_ARB_006",
      questionText: 'اختر الرسم الإملائي الصحيح للفراغ: "لا ........ عن أداء الواجب المدرسي":',
      studentAnswer: "تتأخر",
      correctAnswer: "تتأخر",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "تكتب الهمزة المتوسطة على ألف إذا كانت مفتوحة وما قبلها حرف مفتوح."
    },
    {
      questionId: "DYN_Y6_ARB_010",
      questionText: "مضاد كلمة (تأجيل) في سياق ترتيب المهام اليومية هو:",
      studentAnswer: "تأخير وإرجاء",
      correctAnswer: "تعجيل وتبكير",
      isCorrect: false,
      pointsAwarded: 0,
      maxPoints: 1,
      explanation: "مضاد التأجيل هو التعجيل والتبكير، بينما (تأخير) هو مرادف الكلمة."
    },
    {
      questionId: "DYN_Y6_ARB_003",
      questionText: 'في جملة: "يجري النيل بالخير والنماء"، نوع كلمة (النيل):',
      studentAnswer: "معرفة (لأنه اسم علم لنهر ومعرف بأل)",
      correctAnswer: "معرفة (لأنه اسم علم لنهر ومعرف بأل)",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "أسماء الأنهار والبلدان هي أسماء معارف أعلام."
    },
    {
      questionId: "DYN_Y6_ARB_007",
      questionText: 'اختر الكلمة الصحيحة إملائياً: "شعر المريض بألم في ........ فذهب للطبيب":',
      studentAnswer: "الرأس",
      correctAnswer: "الرأس",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "الفتحة أقوى من السكون، لذلك إذا كانت الهمزة ساكنة وقبلها مفتوح تُكتب على ألف."
    },
    {
      questionId: "DYN_Y6_ARB_002",
      questionText: 'في جملة: "اشترى الطالب قلماً جديداً"، كلمة (قلماً) هي اسم:',
      studentAnswer: "نكرة (لأنه منون ومجرد من أل والإضافة)",
      correctAnswer: "نكرة (لأنه منون ومجرد من أل والإضافة)",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "اسم منون ومجرد من أل والإضافة ويدل على غير معين."
    },
    {
      questionId: "DYN_Y6_ARB_001",
      questionText: 'في جملة: "حضر المهندسون لاجتماع إدارة المشروع"، كلمة (المهندسون) تعتبر اسماً:',
      studentAnswer: "معرفة (معرف بأل)",
      correctAnswer: "معرفة (معرف بأل)",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "الاسم الذي يبدأ بـ (أل) التعريف هو اسم معرفة."
    },
    {
      questionId: "DYN_Y6_ARB_004",
      questionText: 'أكمل الجملة باسم معرفة مناسب: "........ هم الركيزة الأساسية لنهضة أي مجتمع."',
      studentAnswer: "المخلصون",
      correctAnswer: "المخلصون",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "(المخلصون) معرف بأل."
    },
    {
      questionId: "DYN_Y6_ARB_005",
      questionText: 'أكمل الجملة باسم نكرة منون مناسب: "الوقتُ ........ ثمينٌ لا يقدر بثمن."',
      studentAnswer: "كنزٌ",
      correctAnswer: "كنزٌ",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "(كنزٌ) اسم نكرة مرفوع بالضمة ومجرد من أل."
    }
  ];


  const mostafaArbAttempt2Review = [
    {
      questionId: "DYN_Y6_ARB_008",
      questionText: "ما سبب كتابة الهمزة على ألف في كلمة (يَسْـأَلُ)؟",
      studentAnswer: "لأن الهمزة مفتوحة وما قبلها حرف ساكن",
      correctAnswer: "لأن الهمزة مفتوحة وما قبلها حرف ساكن",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "💡 إتقان القاعدة:\nفي كلمة (يَسْـأَلُ): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون ➔ فتُرسم على ألف."
    },
    {
      questionId: "DYN_Y6_ARB_009",
      questionText: 'معنى كلمة (إنجاز) في سياق جملة "يتطلب إنجاز الأعمال تخطيطاً مستمراً" هو:',
      studentAnswer: "إتمام وتحقيق بنجاح",
      correctAnswer: "إتمام وتحقيق بنجاح",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "إنجاز الشيء = إتمامه وقضاؤه بنجاح."
    },
    {
      questionId: "DYN_Y6_ARB_006",
      questionText: 'اختر الرسم الإملائي الصحيح للفراغ: "لا ........ عن أداء الواجب المدرسي":',
      studentAnswer: "تتأخر",
      correctAnswer: "تتأخر",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "تكتب الهمزة المتوسطة على ألف إذا كانت مفتوحة وما قبلها حرف مفتوح."
    },
    {
      questionId: "DYN_Y6_ARB_010",
      questionText: "مضاد كلمة (تأجيل) في سياق ترتيب المهام اليومية هو:",
      studentAnswer: "تعجيل وتبكير",
      correctAnswer: "تعجيل وتبكير",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "💡 إتقان التضاد اللغوي:\nمضاد التأجيل هو التعجيل والتبكير."
    },
    {
      questionId: "DYN_Y6_ARB_003",
      questionText: 'في جملة: "يجري النيل بالخير والنماء"، نوع كلمة (النيل):',
      studentAnswer: "معرفة (لأنه اسم علم لنهر ومعرف بأل)",
      correctAnswer: "معرفة (لأنه اسم علم لنهر ومعرف بأل)",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "أسماء الأنهار والبلدان هي أسماء معارف أعلام."
    },
    {
      questionId: "DYN_Y6_ARB_007",
      questionText: 'اختر الكلمة الصحيحة إملائياً: "شعر المريض بألم في ........ فذهب للطبيب":',
      studentAnswer: "الرأس",
      correctAnswer: "الرأس",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "الفتحة أقوى من السكون، لذلك إذا كانت الهمزة ساكنة وقبلها مفتوح تُكتب على ألف."
    },
    {
      questionId: "DYN_Y6_ARB_002",
      questionText: 'في جملة: "اشترى الطالب قلماً جديداً"، كلمة (قلماً) هي اسم:',
      studentAnswer: "نكرة (لأنه منون ومجرد من أل والإضافة)",
      correctAnswer: "نكرة (لأنه منون ومجرد من أل والإضافة)",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "اسم منون ومجرد من أل والإضافة ويدل على غير معين."
    },
    {
      questionId: "DYN_Y6_ARB_001",
      questionText: 'في جملة: "حضر المهندسون لاجتماع إدارة المشروع"، كلمة (المهندسون) تعتبر اسماً:',
      studentAnswer: "معرفة (معرف بأل)",
      correctAnswer: "معرفة (معرف بأل)",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "الاسم الذي يبدأ بـ (أل) التعريف هو اسم معرفة."
    },
    {
      questionId: "DYN_Y6_ARB_004",
      questionText: 'أكمل الجملة باسم معرفة مناسب: "........ هم الركيزة الأساسية لنهضة أي مجتمع."',
      studentAnswer: "المخلصون",
      correctAnswer: "المخلصون",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "(المخلصون) معرف بأل."
    },
    {
      questionId: "DYN_Y6_ARB_005",
      questionText: 'أكمل الجملة باسم نكرة منون مناسب: "الوقتُ ........ ثمينٌ لا يقدر بثمن."',
      studentAnswer: "كنزٌ",
      correctAnswer: "كنزٌ",
      isCorrect: true,
      pointsAwarded: 1,
      maxPoints: 1,
      explanation: "(كنزٌ) اسم نكرة مرفوع بالضمة ومجرد من أل."
    }
  ];

  return {
    ali: aliReview,
    mostafaEng: mostafaEngReview,
    mostafaArb: mostafaArbReview,
    mostafaArbAttempt2: mostafaArbAttempt2Review
  };
}

function restoreAllHistoricalSubmissions() {
  const ss = getSpreadsheet();
  let subSheet = ss.getSheetByName('Submissions');
  if (!subSheet) {
    subSheet = ss.insertSheet('Submissions');
  }
  
  const subHeaders = [
    ['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON']
  ];
  subSheet.getRange(1, 1, 1, subHeaders[0].length).setValues(subHeaders);
  formatHeaderRow(subSheet, '#1e3a8a');

  const existing = subSheet.getDataRange().getValues();
  let aliEngCount = 0;
  let mostafaEngCount = 0;
  let mostafaArbCount = 0;

  for (let i = 1; i < existing.length; i++) {
    const sName = String(existing[i][1] || '').trim().toLowerCase();
    const eCode = String(existing[i][3] || '').trim().toUpperCase();
    if (sName.includes('ali') && eCode.includes('ADV01')) aliEngCount++;
    if (sName.includes('mostafa') && eCode.includes('FANTASY01')) mostafaEngCount++;
    if (sName.includes('mostafa') && eCode.includes('ARB_PRIO01')) mostafaArbCount++;
  }

  const reviews = getHistoricalSubmissionsData();

  // 1. Ali Ahmed - Year 5 English (9/10)
  if (aliEngCount === 0) {
    subSheet.appendRow([
      '10/24/2026 22:30:00',
      'Ali Ahmed',
      'Year 5 (G5)',
      'EX_Y5_ENG_ADV01',
      9,
      10,
      '90%',
      'Excellent 🌟',
      '7 min 42 sec',
      '9/10 Correct (1 mistake reviewed)',
      JSON.stringify(reviews.ali)
    ]);
  }

  // 2. Mostafa Ahmed - Grade 6 English (10/10)
  if (mostafaEngCount === 0) {
    subSheet.appendRow([
      '10/24/2026 22:44:00',
      'Mostafa Ahmed',
      'Grade 6 (G6)',
      'EX_Y6_ENG_FANTASY01',
      10,
      10,
      '100%',
      'Excellent 🌟',
      '8 min 12 sec',
      '10/10 Correct (Flawless Score)',
      JSON.stringify(reviews.mostafaEng)
    ]);
  }

  // 3. Mostafa Ahmed - Grade 6 Arabic: Attempt 1 (8/10)
  if (mostafaArbCount === 0) {
    subSheet.appendRow([
      '10/24/2026 22:48:00',
      'Mostafa Ahmed',
      'Grade 6 (G6)',
      'EX_Y6_ARB_PRIO01',
      8,
      10,
      '80%',
      'Very Good 👍',
      '6 min 55 sec',
      '8/10 Correct (Attempt 1 - 2 mistakes reviewed)',
      JSON.stringify(reviews.mostafaArb)
    ]);
    mostafaArbCount++;
  }

  // 4. Mostafa Ahmed - Grade 6 Arabic: Attempt 2 (10/10 - Flawless!)
  if (mostafaArbCount === 1) {
    subSheet.appendRow([
      '10/24/2026 23:05:00',
      'Mostafa Ahmed',
      'Grade 6 (G6)',
      'EX_Y6_ARB_PRIO01',
      10,
      10,
      '100%',
      'Excellent 🌟',
      '5 min 20 sec',
      '10/10 Correct (Attempt 2 - Flawless Mastered 🌟)',
      JSON.stringify(reviews.mostafaArbAttempt2)
    ]);
  }

  const lastRow = subSheet.getLastRow();
  if (lastRow > 1) {
    subSheet.getRange(2, 1, lastRow - 1, 10).setVerticalAlignment('middle').setFontSize(10);
    subSheet.getRange(2, 5, lastRow - 1, 3).setHorizontalAlignment('center');
  }

  styleSubmissionsSheet(subSheet);
  return { success: true, message: 'All historical submissions (including Attempt 1 and Attempt 2) restored successfully!' };
}