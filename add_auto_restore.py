# -*- coding: utf-8 -*-
import json
import re

code_path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(code_path, "r", encoding="utf-8") as f:
    code = f.read()

# Exact review for Mostafa's Arabic exam (from screenshot)
mostafa_arb_review = [
    {
        "questionId": "DYN_Y6_ARB_008",
        "questionText": "ما سبب كتابة الهمزة على ألف في كلمة (يَسْـأَلُ)؟",
        "studentAnswer": "لأن الهمزة مكسورة وما قبلها مضموم",
        "correctAnswer": "لأن الهمزة مفتوحة وما قبلها حرف ساكن",
        "isCorrect": False,
        "pointsAwarded": 0,
        "maxPoints": 1,
        "explanation": "في كلمة (يَسْـأَلُ): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون ➔ فتُرسم على ألف."
    },
    {
        "questionId": "DYN_Y6_ARB_009",
        "questionText": "معنى كلمة (إنجاز) في سياق جملة \"يتطلب إنجاز الأعمال تخطيطاً مستمراً\" هو:",
        "studentAnswer": "إتمام وتحقيق بنجاح",
        "correctAnswer": "إتمام وتحقيق بنجاح",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "إنجاز الشيء = إتمامه وقضاؤه بنجاح."
    },
    {
        "questionId": "DYN_Y6_ARB_006",
        "questionText": "اختر الرسم الإملائي الصحيح للفراغ: \"لا ........ عن أداء الواجب المدرسي\":",
        "studentAnswer": "تتأخر",
        "correctAnswer": "تتأخر",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "تكتب الهمزة المتوسطة على ألف إذا كانت مفتوحة وما قبلها حرف مفتوح."
    },
    {
        "questionId": "DYN_Y6_ARB_010",
        "questionText": "مضاد كلمة (تأجيل) في سياق ترتيب المهام اليومية هو:",
        "studentAnswer": "تأخير وإرجاء",
        "correctAnswer": "تعجيل وتبكير",
        "isCorrect": False,
        "pointsAwarded": 0,
        "maxPoints": 1,
        "explanation": "مضاد التأجيل هو التعجيل والتبكير، بينما (تأخير) هو مرادف الكلمة."
    },
    {
        "questionId": "DYN_Y6_ARB_003",
        "questionText": "في جملة: \"يجري النيل بالخير والنماء\"، نوع كلمة (النيل):",
        "studentAnswer": "معرفة (لأنه اسم علم لنهر ومعرف بأل)",
        "correctAnswer": "معرفة (لأنه اسم علم لنهر ومعرف بأل)",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "أسماء الأنهار والبلدان هي أسماء معارف أعلام."
    },
    {
        "questionId": "DYN_Y6_ARB_007",
        "questionText": "اختر الكلمة الصحيحة إملائياً: \"شعر المريض بألم في ........ فذهب للطبيب\":",
        "studentAnswer": "الرأس",
        "correctAnswer": "الرأس",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "الفتحة أقوى من السكون، لذلك إذا كانت الهمزة ساكنة وقبلها مفتوح تُكتب على ألف."
    },
    {
        "questionId": "DYN_Y6_ARB_002",
        "questionText": "في جملة: \"اشترى الطالب قلماً جديداً\"، كلمة (قلماً) هي اسم:",
        "studentAnswer": "نكرة (لأنه منون ومجرد من أل والإضافة)",
        "correctAnswer": "نكرة (لأنه منون ومجرد من أل والإضافة)",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "اسم منون ومجرد من أل والإضافة ويدل على غير معين."
    },
    {
        "questionId": "DYN_Y6_ARB_001",
        "questionText": "في جملة: \"حضر المهندسون لاجتماع إدارة المشروع\"، كلمة (المهندسون) تعتبر اسماً:",
        "studentAnswer": "معرفة (معرف بأل)",
        "correctAnswer": "معرفة (معرف بأل)",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "الاسم الذي يبدأ بـ (أل) التعريف هو اسم معرفة."
    },
    {
        "questionId": "DYN_Y6_ARB_004",
        "questionText": "أكمل الجملة باسم معرفة مناسب: \"........ هم الركيزة الأساسية لنهضة أي مجتمع.\"",
        "studentAnswer": "المخلصون",
        "correctAnswer": "المخلصون",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "(المخلصون) معرف بأل."
    },
    {
        "questionId": "DYN_Y6_ARB_005",
        "questionText": "أكمل الجملة باسم نكرة منون مناسب: \"الوقتُ ........ ثمينٌ لا يقدر بثمن.\"",
        "studentAnswer": "كنزٌ",
        "correctAnswer": "كنزٌ",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "(كنزٌ) اسم نكرة مرفوع بالضمة ومجرد من أل."
    }
]

# Exact review for Mostafa's English exam: 10/10
mostafa_eng_review = [
    {
        "questionId": "Q_Y6_ENG_001",
        "questionText": "What genre best describes \"The City That Waited\"?",
        "studentAnswer": "Fantasy Fiction with mysterious world-building",
        "correctAnswer": "Fantasy Fiction with mysterious world-building",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "The story takes place in a magical city frozen in time."
    },
    {
        "questionId": "Q_Y6_ENG_002",
        "questionText": "Identify the non-finite clause in: \"Climbing the winding spiral staircase, Leo heard distant gears.\"",
        "studentAnswer": "Climbing the winding spiral staircase",
        "correctAnswer": "Climbing the winding spiral staircase",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "Begins with an -ing participle and has no finite verb."
    },
    {
        "questionId": "Q_Y6_ENG_003",
        "questionText": "Which relative pronoun best combines: \"The ancient clock tower, ________ gears were made of polished bronze, chimed.\"",
        "studentAnswer": "whose",
        "correctAnswer": "whose",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "\"whose\" shows possession of the gears."
    },
    {
        "questionId": "Q_Y6_ENG_004",
        "questionText": "In a non-chronological report about Sea Turtles, which heading is most appropriate for their nesting habits?",
        "studentAnswer": "Breeding and Nesting Behaviour",
        "correctAnswer": "Breeding and Nesting Behaviour",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "Formal sub-heading organizing biological facts."
    },
    {
        "questionId": "Q_Y6_ENG_005",
        "questionText": "Choose the formal non-chronological report connective expressing contrast:",
        "studentAnswer": "In contrast",
        "correctAnswer": "In contrast",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "\"In contrast\" is a formal connective comparing differences."
    },
    {
        "questionId": "Q_Y6_ENG_006",
        "questionText": "Which sentence embeds a non-restrictive relative clause correctly?",
        "studentAnswer": "Sea turtles, which are ancient reptiles, lay their eggs on sandy beaches.",
        "correctAnswer": "Sea turtles, which are ancient reptiles, lay their eggs on sandy beaches.",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "Non-restrictive relative clause surrounded by a pair of commas."
    },
    {
        "questionId": "Q_Y6_ENG_007",
        "questionText": "Choose the sentence with correct subject-verb agreement:",
        "studentAnswer": "Sea turtles lay their eggs on sandy beaches.",
        "correctAnswer": "Sea turtles lay their eggs on sandy beaches.",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "Plural subject \"Sea turtles\" takes base plural verb \"lay\"."
    },
    {
        "questionId": "Q_Y6_ENG_008",
        "questionText": "Correct the spelling mistake in: \"Some sea turtles have a herd shell on their backs.\"",
        "studentAnswer": "hard shell",
        "correctAnswer": "hard shell",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "Tough, solid shell = hard shell."
    },
    {
        "questionId": "Q_Y6_ENG_009",
        "questionText": "True or False: In \"Shadows stretched along the walls, long and thin as fingers.\", the author uses a simile.",
        "studentAnswer": "True",
        "correctAnswer": "True",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "Uses \"as\" to compare shadows to elongated fingers."
    },
    {
        "questionId": "Q_Y6_ENG_010",
        "questionText": "Complete the conclusion sentence using formal connective: \"Protecting sea turtles matters ________ they play a vital role in marine ecosystems.\"",
        "studentAnswer": "because",
        "correctAnswer": "because",
        "isCorrect": True,
        "pointsAwarded": 1,
        "maxPoints": 1,
        "explanation": "\"because\" gives the reason explaining why protection is essential."
    }
]

arb_json_str = json.dumps(mostafa_arb_review).replace('"', '\\"')
eng_json_str = json.dumps(mostafa_eng_review).replace('"', '\\"')

# Function to add all historical submissions safely
restore_func = f"""
function restoreAllHistoricalSubmissions() {{
  const ss = getSpreadsheet();
  let subSheet = ss.getSheetByName('Submissions');
  if (!subSheet) {{
    subSheet = ss.insertSheet('Submissions');
  }}
  
  const subHeaders = [
    ['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON']
  ];
  subSheet.getRange(1, 1, 1, subHeaders[0].length).setValues(subHeaders);
  formatHeaderRow(subSheet, '#1e3a8a');

  // Check which submissions exist
  const existing = subSheet.getDataRange().getValues();
  const keys = new Set();
  for (let i = 1; i < existing.length; i++) {{
    const sName = String(existing[i][1] || '').trim().toLowerCase();
    const eCode = String(existing[i][3] || '').trim().toUpperCase();
    keys.add(sName + '___' + eCode);
  }}

  const targetSubmissions = [
    // 1. Mostafa Ahmed - English Literacy (10/10)
    {{
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
        "{eng_json_str}"
      ]
    }},
    // 2. Mostafa Ahmed - Arabic Diagnostic (8/10)
    {{
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
        "{arb_json_str}"
      ]
    }}
  ];

  targetSubmissions.forEach(item => {{
    if (!keys.has(item.key)) {{
      subSheet.appendRow(item.row);
      const lastRow = subSheet.getLastRow();
      subSheet.getRange(lastRow, 1, 1, 10).setVerticalAlignment('middle').setFontSize(10);
      subSheet.getRange(lastRow, 5, 1, 3).setHorizontalAlignment('center');
      keys.add(item.key);
    }}
  }});

  // Also ensure Ali Ahmed is present
  ensureAliRecord(subSheet);
  styleSubmissionsSheet(subSheet);

  return 'All historical submissions restored successfully! Total rows: ' + subSheet.getLastRow();
}}
"""

# Append restoreAllHistoricalSubmissions to Code.gs
code += "\n\n" + restore_func

# Also in onOpen, add a menu item for it
code = code.replace(
    ".addItem('⚙️ Full Database Auto-Format & Setup', 'setupDatabase')",
    ".addItem('⚙️ Full Database Auto-Format & Setup', 'setupDatabase')\n    .addItem('🔄 Restore All Historical Submissions (Mostafa & Ali)', 'restoreAllHistoricalSubmissions')"
)

# Also ensure restoreAllHistoricalSubmissions is automatically called in getAdminDashboardData() so the parent portal immediately sees all historical submissions!
code = code.replace(
    "ensureAliRecord(subSheet);",
    "restoreAllHistoricalSubmissions();"
)

with open(code_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Code.gs updated with restoreAllHistoricalSubmissions.")
