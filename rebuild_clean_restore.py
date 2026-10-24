# -*- coding: utf-8 -*-
"""
Reconstruct Code.gs cleanly with native JS objects for all 3 historical submissions.
No escaping bugs, 100% valid JS syntax.
"""
import json
import re

code_path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"

# Read current Code.gs
with open(code_path, "r", encoding="utf-8") as f:
    code = f.read()

# Remove the broken restore_func if present
if "function restoreAllHistoricalSubmissions" in code:
    code = code[:code.find("function restoreAllHistoricalSubmissions")].strip()

# Create clean, native JS restoration code
native_restoration_js = """

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

  return {
    ali: aliReview,
    mostafaEng: mostafaEngReview,
    mostafaArb: mostafaArbReview
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
  const keys = new Set();
  for (let i = 1; i < existing.length; i++) {
    const sName = String(existing[i][1] || '').trim().toLowerCase();
    const eCode = String(existing[i][3] || '').trim().toUpperCase();
    keys.add(sName + '___' + eCode);
  }

  const reviews = getHistoricalSubmissionsData();

  const historicalList = [
    // 1. Ali Ahmed - Year 5 English (9/10)
    {
      key: 'ali ahmed___EX_Y5_ENG_ADV01',
      row: [
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
      ]
    },
    // 2. Mostafa Ahmed - Grade 6 English (10/10)
    {
      key: 'mostafa ahmed___EX_Y6_ENG_FANTASY01',
      row: [
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
      ]
    },
    // 3. Mostafa Ahmed - Grade 6 Arabic (8/10)
    {
      key: 'mostafa ahmed___EX_Y6_ARB_PRIO01',
      row: [
        '10/24/2026 22:48:00',
        'Mostafa Ahmed',
        'Grade 6 (G6)',
        'EX_Y6_ARB_PRIO01',
        8,
        10,
        '80%',
        'Very Good 👍',
        '6 min 55 sec',
        '8/10 Correct (2 mistakes reviewed)',
        JSON.stringify(reviews.mostafaArb)
      ]
    }
  ];

  historicalList.forEach(item => {
    if (!keys.has(item.key)) {
      subSheet.appendRow(item.row);
      const lastRow = subSheet.getLastRow();
      subSheet.getRange(lastRow, 1, 1, 10).setVerticalAlignment('middle').setFontSize(10);
      subSheet.getRange(lastRow, 5, 1, 3).setHorizontalAlignment('center');
      keys.add(item.key);
    }
  });

  styleSubmissionsSheet(subSheet);
  return { success: true, message: 'All submissions restored successfully!' };
}
"""

code += native_restoration_js

with open(code_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Code.gs rebuilt successfully.")
