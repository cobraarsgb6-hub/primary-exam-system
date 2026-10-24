# -*- coding: utf-8 -*-
"""
Procedural Question Generation Engine for Code.gs.
Every single time an exam is started, 10 brand-new questions are mathematically
and contextually generated with different numbers, sentences, names, and variations.
"""

engine_js = """
// ============================================================
// DYNAMIC PROCEDURAL QUESTION GENERATORS
// Every exam attempt generates brand-new sentences, names & numbers!
// ============================================================

function getRandomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Procedural Generator for Ali Ahmed (Year 5 Grammar - Adverbials)
 */
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
    explanation: `💡 Adverbial of Time:\\n"${q1Time}" tells us WHEN the action happened (${q1Sub} ${q1Verb}). Time adverbials answer the question "When?".`
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
    explanation: `💡 Adverbial of Place:\\n"${placeCorrect}" contains the prepositional phrase "${q2Place}", which answers the question "Where?".`
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
    explanation: `💡 Adverbial of Manner:\\n"${q3Manner}" describes HOW the action was performed.`
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
    explanation: `💡 Punctuation Rule:\\nA fronted adverbial sits at the very beginning of a sentence and MUST be followed by a comma:\\n"${q4Correct}".`
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
    explanation: `💡 Fronted Adverbial of Time:\\n"${q5TimeFront}" answers "When?" and is positioned at the front of the sentence followed by a comma.`
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
    explanation: `💡 Fronting Rule:\\nMoving "in ${q6Year}" to the start requires a comma immediately after it: "${q6Rewritten}".`
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
    explanation: `💡 Dual Adverbials:\\n"In ${q7Year}" ➔ Time (When)\\n"${q7Place}" ➔ Place (Where)\\nBoth exist together in the correct sentence.`
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
    explanation: '💡 Adverbial Definition:\\nAn adverbial can be a single adverb (e.g. "quietly") or a prepositional phrase (e.g. "in the morning") that gives extra context to the action.'
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
    explanation: `💡 Adverbial of Manner:\\n"${q9MannerGood}" describes HOW the equipment was operated.`
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
    explanation: `💡 Concept Check:\\nA year (like 1957 or 1999) indicates TIME, not PLACE.`
  });

  return questions;
}

/**
 * Procedural Generator for Mostafa Ahmed (Grade 6 English Literacy & Report Writing)
 */
function generateMostafaEnglishExam() {
  const questions = [];

  // Q1: Simile Generator (Dynamic comparisons)
  const similes = [
    { text: 'Its white walls glowed like the inside of a seashell', target: 'walls to a seashell' },
    { text: 'The ancient stone towers rose like giant spears against the sky', target: 'towers to spears' },
    { text: 'Shadows stretched along the cobbles, long and thin as fingers', target: 'shadows to fingers' },
    { text: 'The dry desert wind whistled sharp as a knife through the gates', target: 'wind to a knife' },
    { text: 'Her ancient voice sounded as thin as parchment paper', target: 'voice to paper' }
  ];
  const chosenSimile = getRandomElement(similes);
  questions.push({
    id: 'DYN_Y6_ENG_001_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (The City That Waited)',
    text: `Which of the following phrases is a <b>SIMILE</b> comparing ${chosenSimile.target}?`,
    type: 'MCQ',
    options: [
      chosenSimile.text,
      'The fountain whispered softly to itself',
      'The city was a complete and eerie hush',
      'Cobblestones lined the silent marketplace'
    ],
    correctAnswer: chosenSimile.text,
    points: 1,
    explanation: `💡 Simile Definition:\\nA simile compares two distinct things using "like" or "as": "${chosenSimile.text}".`
  });

  // Q2: Personification Generator
  const personifications = [
    'The abandoned fountain whispered softly to itself in the courtyard',
    'The rusty iron gates groaned under the heavy desert wind',
    'Pale moonlight crept slowly over the silent cobblestones',
    'The old clock tower watched over the deserted square',
    'The desert dust howled angrily against the marble columns'
  ];
  const chosenPerson = getRandomElement(personifications);
  questions.push({
    id: 'DYN_Y6_ENG_002_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (The City That Waited)',
    text: `What figure of speech is used in: "<b>${chosenPerson}</b>"?`,
    type: 'MCQ',
    options: ['Personification', 'Simile', 'Alliteration', 'Hyperbole'],
    correctAnswer: 'Personification',
    points: 1,
    explanation: `💡 Personification:\\nGiving human traits or actions (whispering, groaning, creeping, watching) to non-human objects.`
  });

  // Q3: Metaphor & Atmosphere
  const metaphors = [
    { phrase: 'The city was a hush.', meaning: 'The city was completely silent, deserted, and quiet.' },
    { phrase: 'The desert was an endless ocean of golden sand.', meaning: 'The desert appeared vast and boundless like the sea.' },
    { phrase: 'The night was a heavy dark blanket.', meaning: 'The darkness covered everything completely and intensely.' }
  ];
  const chosenMeta = getRandomElement(metaphors);
  questions.push({
    id: 'DYN_Y6_ENG_003_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (The City That Waited)',
    text: `In the metaphorical phrase: "<b>${chosenMeta.phrase}</b>", what does the author imply?`,
    type: 'MCQ',
    options: [
      chosenMeta.meaning,
      'The city was crowded with celebrations',
      'The weather was stormy and loud',
      'People were singing in the streets'
    ],
    correctAnswer: chosenMeta.meaning,
    points: 1,
    explanation: `💡 Metaphor Analysis:\\nA metaphor states that one thing IS another to create vivid imagery without using "like" or "as".`
  });

  // Q4: Relative Clause (Sea Turtles Report Writing)
  const relClauses = [
    {
      correct: 'Sea turtles, which are ancient marine reptiles, lay their eggs on sandy beaches.',
      w1: 'Sea turtles which are ancient marine reptiles lay their eggs, on sandy beaches.',
      w2: 'Sea turtles, which are ancient marine reptiles lay their eggs on sandy beaches.',
      w3: 'Sea turtles which are ancient marine reptiles, lay their eggs on sandy beaches.'
    },
    {
      correct: 'Plastic waste, which is dumped into oceans, poses a severe hazard to wildlife.',
      w1: 'Plastic waste which is dumped into oceans poses a severe hazard, to wildlife.',
      w2: 'Plastic waste, which is dumped into oceans poses a severe hazard to wildlife.',
      w3: 'Plastic waste which is dumped into oceans, poses a severe hazard to wildlife.'
    }
  ];
  const chosenRel = getRandomElement(relClauses);
  questions.push({
    id: 'DYN_Y6_ENG_004_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (Sea Turtles)',
    text: 'Which sentence correctly punctuates the non-defining <b>RELATIVE CLAUSE</b> with commas?',
    type: 'MCQ',
    options: [chosenRel.correct, chosenRel.w1, chosenRel.w2, chosenRel.w3],
    correctAnswer: chosenRel.correct,
    points: 1,
    explanation: '💡 Non-defining Relative Clauses:\\nWhen extra information is inserted with "which", it must be enclosed with a pair of commas: ", which ..., ".'
  });

  // Q5: Subject-Verb Agreement (Dynamic Sea Life)
  const svPairs = [
    { correct: 'Sea turtles lay their eggs on land.', wrong: 'Sea turtles lays their eggs on land.' },
    { correct: 'The female turtle crawls up the beach at night.', wrong: 'The female turtle crawl up the beach at night.' },
    { correct: 'Marine biologists study the migration habits of ocean animals.', wrong: 'Marine biologists studies the migration habits of ocean animals.' },
    { correct: 'Floating plastic rubbish harms marine animals.', wrong: 'Floating plastic rubbish harm marine animals.' }
  ];
  const chosenSV = getRandomElement(svPairs);
  questions.push({
    id: 'DYN_Y6_ENG_005_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (Sea Turtles)',
    text: 'Select the sentence with correct <b>SUBJECT-VERB AGREEMENT</b>:',
    type: 'MCQ',
    options: [
      chosenSV.correct,
      chosenSV.wrong,
      'They was swimming across the reef.',
      'The eggs is buried under the sand.'
    ],
    correctAnswer: chosenSV.correct,
    points: 1,
    explanation: '💡 Subject-Verb Agreement Rule:\\nA plural subject takes a plural verb (e.g. "Turtles lay", "Biologists study"), while a singular subject takes a singular verb ending in -s.'
  });

  // Q6: Spelling Trap (From Homework Draft)
  const spellingTraps = [
    { prompt: 'If sea turtles ________, ocean ecosystems will lose a vital species.', correct: 'disappear', options: ['disappear', 'disapper', 'dissappear', 'dissapper'] },
    { prompt: 'Adult turtles possess a protective ________ that shields their bodies.', correct: 'hard shell', options: ['hard shell', 'hard shel', 'hard shill', 'hard shull'] },
    { prompt: 'People must stop dumping ________ into coastal waters.', correct: 'rubbish', options: ['rubbish', 'rubish', 'rubbsh', 'roubish'] }
  ];
  const chosenSpell = getRandomElement(spellingTraps);
  questions.push({
    id: 'DYN_Y6_ENG_006_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (Sea Turtles)',
    text: `Identify the correctly spelled word to complete: "<b>${chosenSpell.prompt}</b>"`,
    type: 'MCQ',
    options: chosenSpell.options,
    correctAnswer: chosenSpell.correct,
    points: 1,
    explanation: `💡 Spelling Rule:\\nThe correct standard spelling is "${chosenSpell.correct}".`
  });

  // Q7: Connectives for Formal Cause & Effect
  questions.push({
    id: 'DYN_Y6_ENG_007_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (Sea Turtles)',
    text: 'Complete the conclusion sentence with the best causal connective: "Protecting marine habitats is vital ________ sea turtles maintain healthy seagrass beds."',
    type: 'MCQ',
    options: ['because', 'although', 'unless', 'despite'],
    correctAnswer: 'because',
    points: 1,
    explanation: '💡 Causal Connectives:\\n"Because" introduces the reason or explanation why protecting marine habitats is vital.'
  });

  // Q8: Run-on Sentence Correction
  questions.push({
    id: 'DYN_Y6_ENG_008_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Report Writing (Sea Turtles)',
    text: 'Which sentence correctly repairs the run-on error in: "People can join beach clean-ups they can ask boats not to dump waste"?',
    type: 'MCQ',
    options: [
      'People can join beach clean-ups, and they can ask boats not to dump waste.',
      'People can join beach clean-ups they can, ask boats not to dump waste.',
      'People can join, beach clean-ups and they can ask boats.',
      'People can join beach clean-ups they, can ask boats not to dump waste.'
    ],
    correctAnswer: 'People can join beach clean-ups, and they can ask boats not to dump waste.',
    points: 1,
    explanation: '💡 Repairing Run-ons:\\nSeparate two independent clauses with a comma followed by a coordinating conjunction (", and") or a full stop.'
  });

  // Q9: Vocabulary in Context (Cobbles / Deserted)
  questions.push({
    id: 'DYN_Y6_ENG_009_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (The City That Waited)',
    text: 'In the phrase "Pale light crept over the <b>cobbles</b>", what does the word "cobbles" refer to?',
    type: 'MCQ',
    options: [
      'Rounded stones used to pave historic streets',
      'Small wooden boats in a harbor',
      'Tall stone statues of ancient rulers',
      'Glass lanterns hanging from doorways'
    ],
    correctAnswer: 'Rounded stones used to pave historic streets',
    points: 1,
    explanation: '💡 Vocabulary Meaning:\\n"Cobbles" (cobblestones) are smooth, rounded stones historically used for paving roads and pathways.'
  });

  // Q10: Atmosphere & Setting Analysis
  questions.push({
    id: 'DYN_Y6_ENG_010_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'English Literacy',
    unit: 'Unit 2: Fantasy Reading (The City That Waited)',
    text: 'How does the author convey a mysterious and desolate atmosphere in Part 6?',
    type: 'MCQ',
    options: [
      'Through silent cobblestones, a whispering fountain, and empty archways',
      'By describing a crowded festival with loud cheering crowds',
      'By narrating a fast-paced chariot race across the dunes',
      'By presenting a comical dialogue between market merchants'
    ],
    correctAnswer: 'Through silent cobblestones, a whispering fountain, and empty archways',
    points: 1,
    explanation: '💡 Literary Mood:\\nThe author uses sensory descriptions of silence, empty spaces, and faint sounds to build an eerie and desolate tone.'
  });

  return questions;
}

/**
 * Procedural Generator for Mostafa Ahmed (Grade 6 Arabic - سلاح التلميذ)
 */
function generateMostafaArabicExam() {
  const questions = [];

  // Q1: النكرة والمعرفة (المعرف بأل)
  const nakiraSentences = [
    { s: 'قرأ التلميذُ كتاباً مفيداً عن تاريخ وطنه.', word: 'التلميذُ', type: 'معرفة (لأنه معرف بأل)' },
    { s: 'حقق المهندسُ إنجازاً باهراً في المشروع.', word: 'المهندسُ', type: 'معرفة (لأنه معرف بأل)' },
    { s: 'شاهد الأطفالُ فيلماً وثائقياً عن الحياة البحرية.', word: 'الأطفالُ', type: 'معرفة (لأنه معرف بأل)' },
    { s: 'يساعد الوقتُ الإنسانَ على تنظيم حياته.', word: 'الوقتُ', type: 'معرفة (لأنه معرف بأل)' }
  ];
  const chosenN1 = getRandomElement(nakiraSentences);
  questions.push({
    id: 'DYN_Y6_ARB_001_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة',
    text: `في جملة: "<b>${chosenN1.s}</b>"، كلمة (<b>${chosenN1.word}</b>) تعتبر اسماً:`,
    type: 'MCQ',
    options: [
      chosenN1.type,
      'نكرة (لأنه يدل على غير معين)',
      'فعلاً ماضياً مبنياً على الفتح',
      'حرف جر يفيد الظرفية'
    ],
    correctAnswer: chosenN1.type,
    points: 1,
    explanation: `💡 المعرف بأل:\\nالاسم الذي يبدأ بـ (أل) التعريف هو اسم معرفة لأنه يدل على معين ومحدد.`
  });

  // Q2: النكرة والمعرفة (العَلَم)
  const alamSentences = [
    { s: 'مصرُ مهدُ الحضارةِ والتاريخِ.', word: 'مصرُ', reason: 'معرفة (لأنه اسم عَلَم لبلد)' },
    { s: 'سافر أحمدُ في رحلةٍ تعليميةٍ.', word: 'أحمدُ', reason: 'معرفة (لأنه اسم عَلَم لشخص)' },
    { s: 'يجري النيلُ بالخير والنماء.', word: 'النيلُ', reason: 'معرفة (لأنه اسم عَلَم لنهر ومعرف بأل)' }
  ];
  const chosenAlam = getRandomElement(alamSentences);
  questions.push({
    id: 'DYN_Y6_ARB_002_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة',
    text: `في جملة: "<b>${chosenAlam.s}</b>"، نوع كلمة (<b>${chosenAlam.word}</b>):`,
    type: 'MCQ',
    options: [
      chosenAlam.reason,
      'نكرة (لأنه مجرد من أل)',
      'فعل مضارع مرفوع',
      'حرف عطف'
    ],
    correctAnswer: chosenAlam.reason,
    points: 1,
    explanation: '💡 أسماء الأعلام:\\nأسماء الأشخاص والبلدان والأنهار هي من أقوى أنواع المعارف لأنها تدل على مسمى محدد بذاته.'
  });

  // Q3: النكرة الخالصة
  const pureNakira = [
    { s: 'اشترى الطالبُ قلماً جديداً.', word: 'قلماً' },
    { s: 'نظّم المعلمُ مسابقةً ثقافيةً.', word: 'مسابقةً' },
    { s: 'قرأتُ قصةً رائعةً في المكتبة.', word: 'قصةً' }
  ];
  const chosenPure = getRandomElement(pureNakira);
  questions.push({
    id: 'DYN_Y6_ARB_003_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة',
    text: `في جملة: "<b>${chosenPure.s}</b>"، كلمة (<b>${chosenPure.word}</b>) هي اسم:`,
    type: 'MCQ',
    options: ['نكرة (لأنه منون ومجرد من أل والإضافة)', 'معرفة بأل', 'اسم إشارة', 'ضمير غائب'],
    correctAnswer: 'نكرة (لأنه منون ومجرد من أل والإضافة)',
    points: 1,
    explanation: '💡 الاسم النكرة:\\nاسم يدل على شيء غير محدد، ويقبل التنوين ومجرد من (أل) وغير مضاف لمعرفة.'
  });

  // Q4: إكمال الفراغ باسم معرفة
  questions.push({
    id: 'DYN_Y6_ARB_004_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة',
    text: 'أكمل الجملة التالية باسم <b>معرفة</b> مناسب: "........ يبذلون جهدهم لرفعة الوطن."',
    type: 'MCQ',
    options: ['المخلصون', 'رجالٌ', 'أوفياءٌ', 'مواطنونَ'],
    correctAnswer: 'المخلصون',
    points: 1,
    explanation: '💡 تحديد المعرفة:\\n(المخلصون) معرف بأل، بينما باقي الخيارات نكرات.'
  });

  // Q5: إكمال الفراغ باسم نكرة
  questions.push({
    id: 'DYN_Y6_ARB_005_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد النحوية: النكرة والمعرفة',
    text: 'أكمل الجملة التالية باسم <b>نكرة</b> منون: "الوقتُ ........ ثمينٌ لا يُعوّض."',
    type: 'MCQ',
    options: ['كنزٌ', 'الكنزُ', 'ذلك الكنز', 'هذا كنز'],
    correctAnswer: 'كنزٌ',
    points: 1,
    explanation: '💡 إعراب النكرة:\\n(كنزٌ) اسم نكرة مرفوع بالضمة ومجرد من أل.'
  });

  // Q6: الهمزة المتوسطة على ألف (مفتوحة بعد فتح)
  const hamzaFatha = [
    { word: 'سَـأَلَ', sentence: '........ التلميذُ معلمه عن مسألة صعبة.', correct: 'سَأَلَ', wrong: ['سئل', 'ساأل', 'سألَ (بالياء)'] },
    { word: 'تَـأَخَّـرَ', sentence: 'لا ........ عن أداء الواجب المدرسي.', correct: 'تَتَأَخَّرْ', wrong: ['تتأخر (بدون همزة)', 'تتءخر', 'تتآخر'] },
    { word: 'رَأَى', sentence: 'حينما ........ القائدُ جنوده شجعهم.', correct: 'رَأَى', wrong: ['رءى', 'راأى', 'ريى'] }
  ];
  const chosenHF = getRandomElement(hamzaFatha);
  questions.push({
    id: 'DYN_Y6_ARB_006_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد الإملائية: الهمزة المتوسطة على ألف',
    text: `اختر الرسم الإملائي الصحيح للفراغ: "<b>${chosenHF.sentence}</b>"`,
    type: 'MCQ',
    options: [chosenHF.correct, ...chosenHF.wrong],
    correctAnswer: chosenHF.correct,
    points: 1,
    explanation: '💡 قاعدة الهمزة المفتوحة بعد فتح:\\nتكتب الهمزة المتوسطة على ألف إذا كانت مفتوحة وما قبلها حرف مفتوح.'
  });

  // Q7: الهمزة المتوسطة على ألف (ساكنة بعد فتح)
  const hamzaSukoon = [
    { word: 'الفَـأْس', s: 'يستخدم الفلاحُ ........ في حرث الحقل.', correct: 'الفَأْسَ', wrong: ['الفئس', 'الفاس', 'الفاءس'] },
    { word: 'الرَّأْس', s: 'شعر المريض بألم في ........ فذهب للطبيب.', correct: 'الرَّأْسِ', wrong: ['الرئس', 'الراس', 'الراءس'] },
    { word: 'الكـأْس', s: 'رفع الفريق الفائز ........ عالياً.', correct: 'الكَأْسَ', wrong: ['الكئس', 'الكاس', 'الكاءس'] }
  ];
  const chosenHS = getRandomElement(hamzaSukoon);
  questions.push({
    id: 'DYN_Y6_ARB_007_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد الإملائية: الهمزة المتوسطة على ألف',
    text: `اختر الكلمة الصحيحة إملائياً: "<b>${chosenHS.s}</b>"`,
    type: 'MCQ',
    options: [chosenHS.correct, ...chosenHS.wrong],
    correctAnswer: chosenHS.correct,
    points: 1,
    explanation: '💡 قاعدة الهمزة الساكنة بعد فتح:\\nالفتحة أقوى من السكون، لذلك إذا كانت الهمزة ساكنة وقبلها حرف مفتوح تُكتب على ألف.'
  });

  // Q8: الهمزة المتوسطة على ألف (مفتوحة بعد ساكن)
  questions.push({
    id: 'DYN_Y6_ARB_008_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القواعد الإملائية: الهمزة المتوسطة على ألف',
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

  // Q9: القراءة المتحررة (معاني المفردات)
  const vocabItems = [
    { word: 'إنجاز', s: 'يتطلب إنجاز الأعمال تخطيطاً مستمراً', meaning: 'إتمام وتحقيق بنجاح' },
    { word: 'تبديد', s: 'حذر المعلم من تبديد الوقت في المشتتات', meaning: 'تضييع وإهدار دون فائدة' },
    { word: 'الحثيث', s: 'يسعى الطالب الحثيث نحو التفوق', meaning: 'السريع والجاد والمستمر' }
  ];
  const chosenVocab = getRandomElement(vocabItems);
  questions.push({
    id: 'DYN_Y6_ARB_009_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القراءة المتحررة: فهم المقروء والمفردات',
    text: `معنى كلمة (<b>${chosenVocab.word}</b>) في سياق جملة: "<b>${chosenVocab.s}</b>" هو:`,
    type: 'MCQ',
    options: [chosenVocab.meaning, 'نسيان وإهمال', 'تأخير وتعطيل', 'خوف وتردد'],
    correctAnswer: chosenVocab.meaning,
    points: 1,
    explanation: `💡 دلالة الكلمة في السياق:\\nكلمة (${chosenVocab.word}) في هذا الموضع تعني: ${chosenVocab.meaning}.`
  });

  // Q10: القراءة المتحررة (المضاد وإدارة الأولويات)
  questions.push({
    id: 'DYN_Y6_ARB_010_' + Utilities.getUuid().slice(0, 6),
    grade: 'Grade 6 (G6)',
    subject: 'Arabic Language',
    unit: 'القراءة المتحررة: استيعاب المقروء',
    text: 'مضاد كلمة (<b>تأجيل</b>) في سياق ترتيب المهام اليومية هو:',
    type: 'MCQ',
    options: ['تعجيل وتبكير', 'تأخير وإرجاء', 'كسل وتراخٍ', 'إهمال وتفريط'],
    correctAnswer: 'تعجيل وتبكير',
    points: 1,
    explanation: '💡 المضاد اللغوي:\\nمضاد التأجيل هو التعجيل والتبكير بالعمل.'
  });

  return questions;
}
"""

with open(r'C:\Users\co0ob\Projects\primary-exam-system\procedural_engine.js', 'w', encoding='utf-8') as f:
    f.write(engine_js)

print("Procedural engine written successfully.")
