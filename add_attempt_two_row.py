# -*- coding: utf-8 -*-
"""
Add Mostafa's Attempt 2 (10/10) for Arabic exam in Code.gs
so both attempts appear under each other in Submissions tab!
"""
import re

code_path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(code_path, "r", encoding="utf-8") as f:
    code = f.read()

# Build Mostafa Arabic Attempt 2 Review (10/10 - All Correct!)
attempt2_review_js = """
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
"""

# Replace in getHistoricalSubmissionsData
old_return = """  return {
    ali: aliReview,
    mostafaEng: mostafaEngReview,
    mostafaArb: mostafaArbReview
  };"""

new_return = attempt2_review_js + """
  return {
    ali: aliReview,
    mostafaEng: mostafaEngReview,
    mostafaArb: mostafaArbReview,
    mostafaArbAttempt2: mostafaArbAttempt2Review
  };"""

code = code.replace(old_return, new_return, 1)

# Now update restoreAllHistoricalSubmissions to append Attempt 2
old_restore_func = code[code.find("function restoreAllHistoricalSubmissions() {"):]

new_restore_func = """function restoreAllHistoricalSubmissions() {
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
}"""

code = code[:code.find("function restoreAllHistoricalSubmissions() {")] + new_restore_func

with open(code_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Code.gs updated with Attempt 1 and Attempt 2 under each other.")
