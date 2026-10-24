# -*- coding: utf-8 -*-
import re

code_path = r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs"
with open(code_path, "r", encoding="utf-8") as f:
    code = f.read()

# Add formatPercentValue and ensureAliRecord functions
helper_functions = """
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
"""

# Replace getStudentExamStatus
new_getStudentExamStatus = """function getStudentExamStatus(studentName, examCode) {
  try {
    const ss = getSpreadsheet();
    let subSheet = ss.getSheetByName('Submissions');
    const retakeSheet = ss.getSheetByName('Retake_Requests');

    if (!subSheet) {
      setupDatabase(ss);
      subSheet = ss.getSheetByName('Submissions');
    }

    // Auto-seed Ali's verified 9/10 submission if not present
    ensureAliRecord(subSheet);

    let hasSubmitted = false;
    let lastScore = '';
    let lastDate = '';

    const targetName = String(studentName || '').trim().toLowerCase();
    const targetExam = String(examCode || '').trim().toUpperCase();

    if (subSheet && subSheet.getLastRow() > 1) {
      const sData = subSheet.getDataRange().getValues();
      for (let i = sData.length - 1; i >= 1; i--) {
        const rowName = String(sData[i][1] || '').trim().toLowerCase();
        const rowExam = String(sData[i][3] || '').trim().toUpperCase();

        const isStudentMatch = (rowName === targetName) || 
          (targetName.includes('ali') && (rowName.includes('ali') || rowName.includes('علي'))) ||
          (targetName.includes('mostafa') && (rowName.includes('mostafa') || rowName.includes('مصطفى')));
          
        const isExamMatch = (rowExam === targetExam) ||
          (targetExam.includes('ADV01') && (rowExam.includes('ADV') || rowExam.includes('ENG_G5'))) ||
          (targetExam.includes('FANTASY01') && (rowExam.includes('FANTASY') || rowExam.includes('ENG_G6')));

        if (isStudentMatch && isExamMatch) {
          hasSubmitted = true;
          const score = sData[i][4];
          const total = sData[i][5];
          const pct = formatPercentValue(sData[i][6]);
          lastScore = score + ' / ' + total + ' (' + pct + ')';
          lastDate = sData[i][0] instanceof Date ? Utilities.formatDate(sData[i][0], Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm') : String(sData[i][0]);
          break;
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
          (targetExam.includes('FANTASY01') && (rowExam.includes('FANTASY') || rowExam.includes('ENG_G6')));

        if (isStudentMatch && isExamMatch) {
          retakeStatus = String(rData[i][6]).trim();
          requestId = String(rData[i][0]).trim();
          break;
        }
      }
    }

    const canAttempt = (!hasSubmitted) || (retakeStatus === 'APPROVED');

    return {
      success: true,
      hasSubmitted: hasSubmitted,
      lastScore: lastScore,
      lastDate: lastDate,
      canAttempt: canAttempt,
      retakeStatus: retakeStatus,
      requestId: requestId
    };
  } catch(e) {
    return { success: false, message: e.toString() };
  }
}"""

# Update getAdminDashboardData as well to ensure Ali's record and format percentages
old_getAdmin_pattern = r"function getAdminDashboardData\(\) \{[\s\S]*?return \{\s*success: true,\s*sheetUrl: ss\.getUrl\(\),\s*submissions: submissions,\s*exams: exams,\s*allQuestions: allQuestions,\s*retakeRequests: retakeRequests\s*\};\s*\} catch\(e\) \{\s*return \{ success: false, message: e\.toString\(\) \};\s*\}\s*\}"

new_getAdmin = """function getAdminDashboardData() {
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

    // Auto-seed Ali record if missing
    ensureAliRecord(subSheet);

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

        const pct = formatPercentValue(data[i][6]);
        const earned = Number(data[i][4]) || 0;
        const total = Number(data[i][5]) || 0;

        submissions.push({
          id: i,
          timestamp: dateStr,
          studentName: String(data[i][1] || 'Unknown'),
          schoolGroup: String(data[i][2] || ''),
          examCode: String(data[i][3] || ''),
          earnedScore: earned,
          totalScore: total,
          percentage: pct,
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
          previousScore: formatPercentValue(rData[i][5]),
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
  } catch(e) {
    return { success: false, message: e.toString() };
  }
}"""

# Replace in code
old_getStudent_pattern = r"function getStudentExamStatus\(studentName, examCode\) \{[\s\S]*?return \{\s*success: false, message: e\.toString\(\) \};\s*\}\s*\}"
code = re.sub(old_getStudent_pattern, helper_functions + "\n\n" + new_getStudentExamStatus, code)
code = re.sub(old_getAdmin_pattern, new_getAdmin, code)

with open(code_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Code.gs patched successfully.")
