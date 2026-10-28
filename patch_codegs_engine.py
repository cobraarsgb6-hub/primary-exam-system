# -*- coding: utf-8 -*-
import json
import re

print("Patching Code.gs with authentic Question Bank, Cumulative Generator, and Security...")

with open(r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs", "r", encoding="utf-8") as f:
    code = f.read()

# 1. REMOVE HARDCODED TOKEN
code = re.sub(
    r"defaultToken:\s*'eyJhbGciOiJIUzI1Ni[^\']*'",
    "defaultToken: ''",
    code
)

# Ensure getColigoToken_ only uses Script Properties
old_get_token = """function getColigoToken_() {
  var prop = PropertiesService.getScriptProperties().getProperty('COLIGO_JWT_TOKEN');
  return prop || COLIGO_CONFIG_DEFAULT.defaultToken;
}"""

new_get_token = """function getColigoToken_() {
  var prop = PropertiesService.getScriptProperties().getProperty('COLIGO_JWT_TOKEN');
  return (prop && prop.trim()) ? prop.trim() : '';
}"""

if old_get_token in code:
    code = code.replace(old_get_token, new_get_token)

# 2. UPDATE getStarterStudyPlan_
from build_full_dataset import generate_study_plan, generate_questions, generate_exams

starter_plan = generate_study_plan()
plan_json_lines = []
for p in starter_plan:
    escaped_items = [json.dumps(item, ensure_ascii=False) for item in p]
    plan_json_lines.append("    [" + ", ".join(escaped_items) + "]")

plan_replacement = "function getStarterStudyPlan_() {\n  return [\n" + ",\n".join(plan_json_lines) + "\n  ];\n}"

code = re.sub(
    r"function getStarterStudyPlan_\(\)\s*\{[\s\S]*?\n\}",
    plan_replacement,
    code,
    count=1
)

# 3. UPDATE loadBankQuestionsByPeriod_ and buildExamQuestions_
new_generator_code = """function loadBankQuestionsByPeriod_(grade, subject, period) {
  const ss = getSpreadsheet();
  const sheet = ss.getSheetByName('Question_Bank');
  if (!sheet || sheet.getLastRow() <= 1) return [];

  const map = getSheetHeaderMap_(sheet);
  const data = sheet.getDataRange().getValues();
  const targetPeriod = String(period || '').trim().toUpperCase();
  const targetSubject = String(subject || '').trim().toLowerCase();
  const isGrade5 = normalizeName_(grade).includes('5');

  // Determine allowed weeks for cumulative exams (W2 = W1+W2, W3 = W1+W2+W3, W4/M1 = W1..W4)
  let allowedWeeks = ['W1'];
  if (targetPeriod === 'W2') {
    allowedWeeks = ['W1', 'W2'];
  } else if (targetPeriod === 'W3') {
    allowedWeeks = ['W1', 'W2', 'W3'];
  } else if (targetPeriod === 'W4' || targetPeriod.startsWith('M')) {
    allowedWeeks = ['W1', 'W2', 'W3', 'W4'];
  }

  // 1. Gather all matching questions partitioned by lesson
  const poolByLesson = {};
  const allMatching = [];

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const rowGrade = String(row[headerIndex_(map, 'Grade Level', 1)] || '');
    const rowSubject = String(row[headerIndex_(map, 'Subject', 2)] || '').toLowerCase();
    const rowWeek = String(row[headerIndex_(map, 'Week', 11)] || 'W1').trim().toUpperCase();

    // Grade filter
    const rowIsG5 = normalizeName_(rowGrade).includes('5');
    if (isGrade5 !== rowIsG5) continue;

    // Strict Subject filter: Never mix Arabic and English
    if (targetSubject.includes('arab') || targetSubject.includes('عرب')) {
      if (!rowSubject.includes('arab') && !rowSubject.includes('عرب')) continue;
    } else if (targetSubject.includes('gramm') || targetSubject.includes('eng')) {
      if (!rowSubject.includes('gramm') && !rowSubject.includes('eng')) continue;
    }

    // Cumulative week check
    if (allowedWeeks.indexOf(rowWeek) === -1) continue;

    const text = String(row[headerIndex_(map, 'Question Text', 4)] || '').trim();
    const answer = String(row[headerIndex_(map, 'Correct Answer', 7)] || '').trim();
    if (!text || !answer) continue;

    const type = String(row[headerIndex_(map, 'Type', 5)] || 'MCQ').trim().toUpperCase();
    let options = String(row[headerIndex_(map, 'Options (delimited by |)', 6)] || '')
      .split('|')
      .map(function(opt) { return String(opt || '').trim(); })
      .filter(Boolean);

    if (type === 'TRUE_FALSE' && options.length < 2) options = ['True', 'False'];
    if (options.length < 2) continue;

    const lesson = String(row[headerIndex_(map, 'Unit / Topic', 3)] || 'General');
    const qObj = {
      id: String(row[headerIndex_(map, 'Question ID', 0)] || ('BANK_' + i)),
      grade: rowGrade,
      subject: rowSubject,
      unit: lesson,
      lesson: lesson,
      text: text,
      type: type,
      options: options,
      correctAnswer: answer,
      points: Number(row[headerIndex_(map, 'Points', 8)]) || 1,
      explanation: String(row[headerIndex_(map, 'Pedagogical Explanation & Mistake Breakdown', 9)] || ''),
      passage: getPassageForQuestion_(row[headerIndex_(map, 'Exam Code', 10)], lesson, text),
      week: rowWeek,
      difficulty: String(row[headerIndex_(map, 'Difficulty', 12)] || 'Standard')
    };

    if (!poolByLesson[lesson]) poolByLesson[lesson] = [];
    poolByLesson[lesson].push(qObj);
    allMatching.push(qObj);
  }

  // 2. Balanced distribution: Ensure at least 1 question per covered lesson!
  const selected = [];
  const selectedIds = {};

  const lessons = Object.keys(poolByLesson);
  for (let l = 0; l < lessons.length; l++) {
    const lessonQs = poolByLesson[lessons[l]];
    const picked = getRandomElement(lessonQs);
    if (picked && !selectedIds[picked.id]) {
      selected.push(picked);
      selectedIds[picked.id] = true;
    }
  }

  // Fill remaining slots from allMatching shuffled
  const shuffledRemaining = shuffleArray(allMatching);
  for (let r = 0; r < shuffledRemaining.length; r++) {
    const q = shuffledRemaining[r];
    if (!selectedIds[q.id]) {
      selected.push(q);
      selectedIds[q.id] = true;
    }
  }

  return selected;
}

function buildExamQuestions_(examCode) {
  const exam = getExamInfo(examCode);
  if (!exam) throw new Error('EXAM_NOT_FOUND');

  let questions = loadBankQuestions_(exam.code);
  const requestedCount = Math.max(1, Number(exam.questionsCount) || 10);

  // If questions directly assigned to this examCode are fewer than requestedCount
  // or if this is a cumulative/weekly/monthly exam:
  if (questions.length < requestedCount) {
    const period = exam.period || exam.targetPeriod || (exam.code.includes('W2') ? 'W2' : exam.code.includes('W3') ? 'W3' : exam.code.includes('W4') ? 'W4' : exam.code.includes('M1') ? 'M1' : 'W1');
    const pool = loadBankQuestionsByPeriod_(exam.grade, exam.subject, period);
    if (pool && pool.length > 0) {
      const existingIds = {};
      questions.forEach(function(q) { existingIds[q.id] = true; });
      pool.forEach(function(pq) {
        if (!existingIds[pq.id]) {
          questions.push(pq);
          existingIds[pq.id] = true;
        }
      });
    }
  }

  // Fallbacks if bank is somehow completely empty
  if (!questions.length) {
    if (exam.grade && exam.grade.includes('5')) {
      questions = generateAliAdverbialExam();
    } else if (exam.subject && exam.subject.includes('Arab')) {
      questions = generateMostafaArabicExam();
    } else {
      questions = generateMostafaEnglishExam();
    }
  }

  if (!questions.length) throw new Error('NO_QUESTIONS');

  // Slice to requested count
  questions = questions.slice(0, Math.min(requestedCount, questions.length));
  
  // Shuffle options for each question
  questions = questions.map(function(question) {
    const copy = Object.assign({}, question);
    if (copy.options && copy.options.length > 1) copy.options = shuffleArray(copy.options);
    return copy;
  });

  exam.questionsCount = questions.length;
  return { exam: exam, questions: questions };
}"""

# Replace old loadBankQuestionsByPeriod_
code = re.sub(
    r"function loadBankQuestionsByPeriod_[\s\S]*?return questions;\s*\}",
    "",
    code
)

# Replace old buildExamQuestions_
code = re.sub(
    r"function buildExamQuestions_[\s\S]*?return \{\s*exam:\s*exam,\s*questions:\s*questions\s*\};\s*\}",
    new_generator_code,
    code,
    count=1
)

# 4. UPDATE STUDY PLAN ON SUBMISSION
study_plan_updater = """
function updateStudyPlanOnSubmission_(studentName, examCode, earnedScore, totalScore, percentage) {
  try {
    const ss = getSpreadsheet();
    const spSheet = ss.getSheetByName('Study_Plan');
    if (!spSheet || spSheet.getLastRow() <= 1) return;

    const map = getSheetHeaderMap_(spSheet);
    const data = spSheet.getDataRange().getValues();
    const targetStudent = normalizeName_(studentName);
    const targetExam = normalizeExam_(examCode);

    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      const rowStudent = normalizeName_(rowValue_(row, map, 'Student', 4));
      const rowExam = normalizeExam_(rowValue_(row, map, 'Exam Code', 12));

      if (rowStudent === targetStudent && rowExam === targetExam) {
        const statusCol = headerIndex_(map, 'Status', 11) + 1;
        spSheet.getRange(i + 1, statusCol).setValue('Completed');
        break;
      }
    }
  } catch (err) {
    Logger.log('updateStudyPlanOnSubmission_ error: ' + err);
  }
}
"""

if "updateStudyPlanOnSubmission_" not in code:
    code += "\n" + study_plan_updater

# Ensure updateStudyPlanOnSubmission_ is called in submitExamAnswers
if "updateStudyPlanOnSubmission_" not in code.split("function submitExamAnswers")[1].split("return Object.assign")[0]:
    code = code.replace(
        "return Object.assign({ success: true, alreadySubmitted: false }, result);",
        "updateStudyPlanOnSubmission_(session.studentName, session.examCode, earnedScore, totalScore, percentage);\n    return Object.assign({ success: true, alreadySubmitted: false }, result);"
    )

# 5. UPDATE setupDatabase TO SEED COMPLETE QUESTION BANK AND EXAMS
all_qs = generate_questions()
qb_rows_code = []
for q in all_qs:
    escaped_q = [json.dumps(col, ensure_ascii=False) for col in q]
    qb_rows_code.append("    [" + ", ".join(escaped_q) + "]")

new_qb_seeder = "const sampleQuestions = [\n" + ",\n".join(qb_rows_code) + "\n  ];"

code = re.sub(
    r"const sampleQuestions = \[\s*\[[\s\S]*?EX_Y6_ARB_PRIO01\"\]\s*\];",
    new_qb_seeder,
    code,
    count=1
)

all_exams = generate_exams()
ex_rows_code = []
for ex in all_exams:
    escaped_ex = [json.dumps(col, ensure_ascii=False) for col in ex]
    ex_rows_code.append("    [" + ", ".join(escaped_ex) + "]")

new_ex_seeder = "const starterExams = [\n" + ",\n".join(ex_rows_code) + "\n  ];"

code = re.sub(
    r"const starterExams = \[\s*\[[\s\S]*?EX_Y6_MOS_W2_ARB\"\]\s*\];",
    new_ex_seeder,
    code,
    count=1
)

with open(r"C:\Users\co0ob\Projects\primary-exam-system\Code.gs", "w", encoding="utf-8") as f:
    f.write(code)

print("Code.gs successfully patched and saved!")
