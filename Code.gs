/**
 * ============================================================
 * Primary School Question Bank & Assessment System (G5 & G6)
 * Manaret El-Eman International School (Ali Ahmed & Mostafa Ahmed)
 * Pure English Architecture, Isolated Portals, Dynamic Passage Engine & Executive Google Sheet Styling
 * ============================================================
 */

function getSpreadsheet() {
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  const scriptProps = PropertiesService.getScriptProperties();
  if (ss) {
    // Always remember the container-bound sheet so the web app writes to the same file.
    try {
      if (scriptProps.getProperty('LINKED_SHEET_ID') !== ss.getId()) {
        scriptProps.setProperty('LINKED_SHEET_ID', ss.getId());
      }
    } catch (propError) {
      Logger.log('Could not persist LINKED_SHEET_ID: ' + propError);
    }
    return ss;
  }

  // Migrate the old per-user property if it exists, then use script properties.
  const userProps = PropertiesService.getUserProperties();
  let savedId = scriptProps.getProperty('LINKED_SHEET_ID') || userProps.getProperty('LINKED_SHEET_ID');
  if (savedId) {
    try {
      ss = SpreadsheetApp.openById(savedId);
      if (ss) {
        scriptProps.setProperty('LINKED_SHEET_ID', ss.getId());
        return ss;
      }
    } catch(e) {
      Logger.log('Could not open sheet with saved ID: ' + e);
    }
  }

  ss = SpreadsheetApp.create('Manaret El-Eman - Assessment Platform Database');
  scriptProps.setProperty('LINKED_SHEET_ID', ss.getId());
  setupDatabase(ss);
  return ss;
}

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🎯 Assessment Management')
    .addItem('⚙️ Full Database Auto-Format & Setup', 'setupDatabase')
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
    formatHeaderRow(subSheet, '#1e3a8a');
  }
  // Do NOT seed historical/demo rows automatically. Existing rows are preserved as-is.
  styleSubmissionsSheet(subSheet);

  // 2. TAB: Question_Bank (Reference Catalog)
  let qbSheet = ss.getSheetByName('Question_Bank');
  if (!qbSheet) {
    qbSheet = ss.insertSheet('Question_Bank');
  }
  const qbHeaders = [
    ['Question ID', 'Grade Level', 'Subject', 'Unit / Topic', 'Question Text', 'Type', 'Options (delimited by |)', 'Correct Answer', 'Points', 'Pedagogical Explanation & Mistake Breakdown', 'Exam Code', 'Week', 'Difficulty']
  ];
  if (qbSheet.getLastRow() === 0) {
    qbSheet.getRange(1, 1, 1, qbHeaders[0].length).setValues(qbHeaders);
    formatHeaderRow(qbSheet, '#047857');
  }

  styleQuestionBankSheet(qbSheet);

  // 3. TAB: Exams (Active Assessment Registry)
  let exSheet = ss.getSheetByName('Exams');
  if (!exSheet) {
    exSheet = ss.insertSheet('Exams');
  }
  const exHeaders = [
    ['Exam Code', 'Exam Title', 'Grade Level', 'Subject', 'Questions', 'Duration (Mins)', 'Status', 'Direct URL', 'Created Date']
  ];
  if (exSheet.getLastRow() === 0) {
    exSheet.getRange(1, 1, 1, exHeaders[0].length).setValues(exHeaders);
    formatHeaderRow(exSheet, '#4338ca');
  }

  const sampleExams = [
    ['EX_Y5_ENG_ADV01', 'Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)', 'Year 5 (G5)', 'English Grammar', 10, 20, 'ACTIVE', '', new Date()],
    ['EX_Y6_ENG_FANTASY01', 'Grade 6 English: Fantasy Reading "The City That Waited" & Report Writing', 'Grade 6 (G6)', 'English Literacy', 10, 20, 'ACTIVE', '', new Date()],
    ['EX_Y6_ARB_PRIO01', 'Grade 6 Arabic: Reading Comprehension, Grammar & Spelling (Diagnostic)', 'Grade 6 (G6)', 'Arabic Language', 10, 20, 'ACTIVE', '', new Date()]
  ];
  if (exSheet.getLastRow() <= 1) {
    exSheet.getRange(2, 1, sampleExams.length, sampleExams[0].length).setValues(sampleExams);
  }
  styleExamsSheet(exSheet);

  // 4. TAB: Retake_Requests (Parent Approval Queue)
  let retakeSheet = ss.getSheetByName('Retake_Requests');
  if (!retakeSheet) {
    retakeSheet = ss.insertSheet('Retake_Requests');
  }
  const retakeHeaders = [
    ['Request ID', 'Timestamp', 'Student Name', 'Exam Code', 'Exam Title', 'Previous Score', 'Status', 'Reason', 'Decision Timestamp']
  ];
  if (retakeSheet.getLastRow() === 0) {
    retakeSheet.getRange(1, 1, 1, retakeHeaders[0].length).setValues(retakeHeaders);
    formatHeaderRow(retakeSheet, '#7c3aed');
  }
  styleRetakeSheet(retakeSheet);

  // 5. TAB: Sessions (server-side attempt sessions; never cleared here)
  ensureSessionSheet_(ss);

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

// ============================================================
// CORE HELPERS: sessions, normalized identity, bank loading
// ============================================================

const MAX_ATTEMPTS = 2;
const ATTEMPT_GRACE_SECONDS = 120;

const SESSION_HEADERS = [
  'Session ID', 'Created At', 'Student Name', 'Exam Code', 'School Grade',
  'Started At', 'Expires At', 'Status', 'Questions JSON', 'Result JSON'
];

const SESSION_COLS = {
  id: 0, created: 1, name: 2, exam: 3, grade: 4,
  started: 5, expires: 6, status: 7, questions: 8, result: 9
};

function normalizeName_(value) {
  return String(value || '').replace(/\s+/g, ' ').trim().toLowerCase();
}

function normalizeExam_(value) {
  return String(value || '').trim().toUpperCase();
}

function normalizeAnswer_(value) {
  return (value == null ? '' : String(value))
    .replace(/\u0640/g, '')
    .replace(/[\u064B-\u0652]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}

function nowIso_() {
  return new Date().toISOString();
}

function valueToMillis_(value) {
  if (value instanceof Date) return value.getTime();
  if (typeof value === 'number') return value;
  const parsed = Date.parse(String(value || ''));
  return isNaN(parsed) ? 0 : parsed;
}

function ensureSessionSheet_(ss) {
  const spreadsheet = ss || getSpreadsheet();
  let sheet = spreadsheet.getSheetByName('Sessions');
  if (!sheet) sheet = spreadsheet.insertSheet('Sessions');
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, SESSION_HEADERS.length).setValues([SESSION_HEADERS]);
    formatHeaderRow(sheet, '#0f766e');
    sheet.setColumnWidth(1, 220);
    sheet.setColumnWidth(3, 150);
    sheet.setColumnWidth(4, 150);
    sheet.setColumnWidth(8, 90);
    sheet.setColumnWidth(9, 460);
    sheet.setColumnWidth(10, 260);
  }
  return sheet;
}

function getSessionSheet_() {
  return ensureSessionSheet_(getSpreadsheet());
}

function getSheetHeaderMap_(sheet) {
  const lastColumn = Math.max(sheet.getLastColumn(), 1);
  const headers = sheet.getRange(1, 1, 1, lastColumn).getValues()[0];
  const map = {};
  headers.forEach((header, index) => {
    map[String(header || '').trim().toLowerCase()] = index;
  });
  return map;
}

function headerIndex_(map, name, fallback) {
  const index = map[String(name).trim().toLowerCase()];
  return (typeof index === 'number') ? index : fallback;
}

/**
 * Exact, normalized attempt state. No substring matching: "Khalid" must never
 * match "Ali".
 */
function getAttemptState_(studentName, examCode) {
  const ss = getSpreadsheet();
  const subSheet = ss.getSheetByName('Submissions');
  const retakeSheet = ss.getSheetByName('Retake_Requests');
  const targetName = normalizeName_(studentName);
  const targetExam = normalizeExam_(examCode);
  const attempts = [];

  if (subSheet && subSheet.getLastRow() > 1) {
    const data = subSheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      const rowName = normalizeName_(data[i][1]);
      const rowExam = normalizeExam_(data[i][3]);
      if (rowName !== targetName || rowExam !== targetExam) continue;

      let review = [];
      try { review = JSON.parse(data[i][10] || '[]'); } catch (e) { review = []; }

      const rawDate = data[i][0];
      const dateStr = rawDate instanceof Date
        ? Utilities.formatDate(rawDate, Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm')
        : String(rawDate || '');

      attempts.push({
        attemptNumber: attempts.length + 1,
        timestamp: dateStr,
        score: Number(data[i][4]) || 0,
        total: Number(data[i][5]) || 0,
        percentage: formatPercentValue(data[i][6]),
        rating: String(data[i][7] || ''),
        duration: String(data[i][8] || ''),
        summary: String(data[i][9] || ''),
        review: review
      });
    }
  }

  let retakeStatus = 'NONE';
  let requestId = '';
  if (retakeSheet && retakeSheet.getLastRow() > 1) {
    const rData = retakeSheet.getDataRange().getValues();
    for (let i = rData.length - 1; i >= 1; i--) {
      if (normalizeName_(rData[i][2]) !== targetName) continue;
      if (normalizeExam_(rData[i][3]) !== targetExam) continue;
      retakeStatus = String(rData[i][6] || 'NONE').trim().toUpperCase();
      requestId = String(rData[i][0] || '').trim();
      break;
    }
  }

  const latestAttempt = attempts.length ? attempts[attempts.length - 1] : null;
  const lastScore = latestAttempt
    ? `${latestAttempt.score} / ${latestAttempt.total} (${latestAttempt.percentage})`
    : '';
  const canAttempt = attempts.length < MAX_ATTEMPTS || retakeStatus === 'APPROVED';

  return {
    hasSubmitted: attempts.length > 0,
    attemptsCount: attempts.length,
    attempts: attempts,
    lastScore: lastScore,
    lastDate: latestAttempt ? latestAttempt.timestamp : '',
    canAttempt: canAttempt,
    retakeStatus: retakeStatus,
    requestId: requestId,
    maxAttempts: MAX_ATTEMPTS
  };
}

function recordExpiredSessionSubmission_(sessionOrRow, sessionId) {
  try {
    const ss = getSpreadsheet();
    let subSheet = ss.getSheetByName('Submissions');
    if (!subSheet) {
      setupDatabase(ss);
      subSheet = ss.getSheetByName('Submissions');
    }
    if (!subSheet) return;

    let sName = '';
    let sGrade = '';
    let sExam = '';
    let sSessionId = sessionId || '';
    let qCount = 10;

    if (Array.isArray(sessionOrRow)) {
      sSessionId = sSessionId || String(sessionOrRow[SESSION_COLS.id] || '').trim();
      sName = String(sessionOrRow[SESSION_COLS.name] || '').trim();
      sGrade = String(sessionOrRow[SESSION_COLS.grade] || 'General').trim();
      sExam = String(sessionOrRow[SESSION_COLS.exam] || '').trim();
      try {
        const q = JSON.parse(sessionOrRow[SESSION_COLS.questions] || '[]');
        if (Array.isArray(q) && q.length) qCount = q.length;
      } catch (e) {}
    } else if (sessionOrRow && typeof sessionOrRow === 'object') {
      sSessionId = sSessionId || String(sessionOrRow.id || '').trim();
      sName = String(sessionOrRow.studentName || '').trim();
      sGrade = String(sessionOrRow.grade || 'General').trim();
      sExam = String(sessionOrRow.examCode || '').trim();
      if (Array.isArray(sessionOrRow.questions) && sessionOrRow.questions.length) {
        qCount = sessionOrRow.questions.length;
      }
    }

    if (!sName || !sExam) return;

    // Idempotency check: verify this expired session is not already recorded
    const existing = subSheet.getDataRange().getValues();
    const targetName = normalizeName_(sName);
    const targetExam = normalizeExam_(sExam);
    for (let r = 1; r < existing.length; r++) {
      if (normalizeName_(existing[r][1]) === targetName &&
          normalizeExam_(existing[r][3]) === targetExam &&
          String(existing[r][9] || '').indexOf('انتهت الجلسة دون تسليم') !== -1) {
        const rev = String(existing[r][10] || '');
        if (sSessionId && rev.indexOf(sSessionId) !== -1) {
          // Already recorded
          return;
        }
      }
    }

    const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
    subSheet.appendRow([
      timestamp,
      sName,
      sGrade || 'General',
      sExam,
      0,
      qCount,
      0,
      'Needs Practice 🌱',
      'Expired',
      'انتهت الجلسة دون تسليم (محاولة مستهلكة)',
      JSON.stringify({ expiredSessionId: sSessionId })
    ]);
  } catch (err) {
    Logger.log('recordExpiredSessionSubmission_ error: ' + err);
  }
}

function findActiveSession_(studentName, examCode) {
  const sheet = getSessionSheet_();
  if (sheet.getLastRow() <= 1) return null;

  const data = sheet.getDataRange().getValues();
  const targetName = normalizeName_(studentName);
  const targetExam = normalizeExam_(examCode);
  const now = Date.now();

  for (let i = data.length - 1; i >= 1; i--) {
    const row = data[i];
    if (normalizeName_(row[SESSION_COLS.name]) !== targetName) continue;
    if (normalizeExam_(row[SESSION_COLS.exam]) !== targetExam) continue;
    if (String(row[SESSION_COLS.status] || '').trim().toUpperCase() !== 'ACTIVE') continue;

    const expires = valueToMillis_(row[SESSION_COLS.expires]);
    if (!expires || expires <= now) {
      const rStatus = sheet.getRange(i + 1, SESSION_COLS.status + 1);
      const currentVal = String((typeof rStatus.getValue === 'function' ? rStatus.getValue() : row[SESSION_COLS.status]) || '').trim().toUpperCase();
      if (currentVal === 'ACTIVE') {
        sheet.getRange(i + 1, SESSION_COLS.status + 1).setValue('EXPIRED_CONSUMED');
        recordExpiredSessionSubmission_(row, String(row[SESSION_COLS.id] || ''));
      }
      continue;
    }

    let questions = [];
    try { questions = JSON.parse(row[SESSION_COLS.questions] || '[]'); } catch (e) { questions = []; }
    if (!Array.isArray(questions) || questions.length === 0) {
      sheet.getRange(i + 1, SESSION_COLS.status + 1).setValue('INVALID');
      continue;
    }

    return {
      id: String(row[SESSION_COLS.id] || ''),
      rowIndex: i + 1,
      studentName: String(row[SESSION_COLS.name] || ''),
      examCode: String(row[SESSION_COLS.exam] || ''),
      grade: String(row[SESSION_COLS.grade] || ''),
      startedAt: row[SESSION_COLS.started],
      expiresAt: row[SESSION_COLS.expires],
      questions: questions
    };
  }
  return null;
}

function findSessionById_(sessionId) {
  const sheet = getSessionSheet_();
  if (sheet.getLastRow() <= 1) return null;

  const data = sheet.getDataRange().getValues();
  const target = String(sessionId || '').trim();
  for (let i = 1; i < data.length; i++) {
    if (String(data[i][SESSION_COLS.id] || '').trim() !== target) continue;

    let questions = [];
    let result = null;
    try { questions = JSON.parse(data[i][SESSION_COLS.questions] || '[]'); } catch (e) { questions = []; }
    try { result = JSON.parse(data[i][SESSION_COLS.result] || 'null'); } catch (e) { result = null; }

    return {
      rowIndex: i + 1,
      id: String(data[i][SESSION_COLS.id] || ''),
      studentName: String(data[i][SESSION_COLS.name] || ''),
      examCode: String(data[i][SESSION_COLS.exam] || ''),
      grade: String(data[i][SESSION_COLS.grade] || ''),
      startedAt: data[i][SESSION_COLS.started],
      expiresAt: data[i][SESSION_COLS.expires],
      status: String(data[i][SESSION_COLS.status] || '').trim().toUpperCase(),
      questions: questions,
      result: result
    };
  }
  return null;
}

function createSession_(studentName, exam, questions) {
  const sheet = getSessionSheet_();
  const id = 'SESS_' + Utilities.getUuid().replace(/-/g, '').slice(0, 20).toUpperCase();
  const started = new Date();
  const durationMinutes = Math.max(1, Number(exam.duration) || 20);
  const expires = new Date(started.getTime() + durationMinutes * 60 * 1000);

  sheet.appendRow([
    id,
    started.toISOString(),
    studentName,
    exam.code,
    exam.grade || '',
    started.toISOString(),
    expires.toISOString(),
    'ACTIVE',
    JSON.stringify(questions),
    ''
  ]);

  return {
    id: id,
    rowIndex: sheet.getLastRow(),
    studentName: studentName,
    examCode: exam.code,
    grade: exam.grade || '',
    startedAt: started,
    expiresAt: expires,
    questions: questions
  };
}

function publicQuestions_(questions) {
  return questions.map(q => ({
    id: q.id,
    grade: q.grade,
    subject: q.subject,
    unit: q.unit,
    text: q.text,
    type: q.type,
    options: q.options,
    points: q.points,
    passage: q.passage || ''
  }));
}

function getPassageForQuestion_(examCode, unit, text) {
  const haystack = (String(unit || '') + ' ' + String(text || '')).toLowerCase();

  if (examCode === 'EX_Y6_ENG_FANTASY01') {
    if (haystack.indexOf('report') !== -1 ||
        haystack.indexOf('non-chronological') !== -1 ||
        haystack.indexOf('sea turtle') !== -1) {
      return REPORT_PASSAGES_POOL[0].text;
    }
    return FANTASY_PASSAGES_POOL[0].text;
  }

  if (examCode === 'EX_Y6_ARB_PRIO01') {
    if (/قراءة|النص|الفقرة|السياق|مفردات|مضاد|فكرة/.test(haystack)) {
      return ARABIC_PASSAGES_POOL[0].text;
    }
  }

  return '';
}

function loadBankQuestions_(examCode) {
  const ss = getSpreadsheet();
  const sheet = ss.getSheetByName('Question_Bank');
  if (!sheet || sheet.getLastRow() < 2) return [];

  const map = getSheetHeaderMap_(sheet);
  const data = sheet.getDataRange().getValues();
  const targetExam = normalizeExam_(examCode);
  const questions = [];

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const rowExam = normalizeExam_(row[headerIndex_(map, 'Exam Code', 10)]);
    if (rowExam !== targetExam) continue;

    const text = String(row[headerIndex_(map, 'Question Text', 4)] || '').trim();
    const answer = String(row[headerIndex_(map, 'Correct Answer', 7)] || '').trim();
    if (!text || !answer) continue;

    const type = String(row[headerIndex_(map, 'Type', 5)] || 'MCQ').trim().toUpperCase();
    let options = String(row[headerIndex_(map, 'Options (delimited by |)', 6)] || '')
      .split('|')
      .map(option => String(option || '').trim())
      .filter(option => option.length > 0);

    if (type === 'TRUE_FALSE' && options.length < 2) options = ['True', 'False'];
    if (options.length < 2) continue;

    // Skip malformed bank rows instead of silently scoring them as wrong.
    const answerMatchesOption = options.some(option => normalizeAnswer_(option) === normalizeAnswer_(answer));
    if (!answerMatchesOption) {
      Logger.log('Skipping malformed bank question ' + String(row[0] || ('row ' + (i + 1))) + ': answer not in options');
      continue;
    }

    const unit = String(row[headerIndex_(map, 'Unit / Topic', 3)] || '');
    const passageIndex = map['passage'];
    const passage = (typeof passageIndex === 'number')
      ? String(row[passageIndex] || '')
      : getPassageForQuestion_(targetExam, unit, text);

    questions.push({
      id: String(row[headerIndex_(map, 'Question ID', 0)] || ('BANK_' + i)),
      grade: String(row[headerIndex_(map, 'Grade Level', 1)] || ''),
      subject: String(row[headerIndex_(map, 'Subject', 2)] || ''),
      unit: unit,
      text: text,
      type: type,
      options: options,
      correctAnswer: answer,
      points: Number(row[headerIndex_(map, 'Points', 8)]) || 1,
      explanation: String(row[headerIndex_(map, 'Pedagogical Explanation & Mistake Breakdown', 9)] || ''),
      passage: passage
    });
  }

  return questions;
}

function buildExamQuestions_(examCode) {
  const exam = getExamInfo(examCode);
  if (!exam) throw new Error('EXAM_NOT_FOUND');

  let questions = loadBankQuestions_(exam.code);
  if (!questions.length) {
    if (exam.code === 'EX_Y5_ENG_ADV01') {
      questions = generateAliAdverbialExam();
    } else if (exam.code === 'EX_Y6_ENG_FANTASY01') {
      questions = generateMostafaEnglishExam();
    } else if (exam.code === 'EX_Y6_ARB_PRIO01') {
      questions = generateMostafaArabicExam();
    }
  }

  if (!questions.length) throw new Error('NO_QUESTIONS');

  const requestedCount = Math.max(1, Number(exam.questionsCount) || 10);
  questions = shuffleArray(questions).slice(0, Math.min(requestedCount, questions.length));
  questions = questions.map(question => {
    const copy = Object.assign({}, question);
    if (copy.options && copy.options.length > 1) copy.options = shuffleArray(copy.options);
    return copy;
  });

  exam.questionsCount = questions.length;
  return { exam: exam, questions: questions };
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
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0')
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
  const code = normalizeExam_(examCode);
  if (!code) return null;

  const catalog = {
    'EX_Y5_ENG_ADV01': { code: 'EX_Y5_ENG_ADV01', title: 'English Grammar: Adverbials of Time, Place & Manner (Unit 2)', grade: 'Year 5 (G5)', subject: 'English Grammar', questionsCount: 10, duration: 20 },
    'EX_Y6_ENG_FANTASY01': { code: 'EX_Y6_ENG_FANTASY01', title: 'English Literacy: Fantasy Reading "The City That Waited" & Report Writing', grade: 'Grade 6 (G6)', subject: 'English Literacy', questionsCount: 10, duration: 20 },
    'EX_Y6_ARB_PRIO01': { code: 'EX_Y6_ARB_PRIO01', title: 'Arabic Language: Reading Comprehension, Grammar & Spelling (Diagnostic)', grade: 'Grade 6 (G6)', subject: 'Arabic Language (Diagnostic)', questionsCount: 10, duration: 20 }
  };
  const fallback = catalog[code] || null;

  const ss = getSpreadsheet();
  const sheet = ss.getSheetByName('Exams');
  if (sheet && sheet.getLastRow() > 1) {
    const map = getSheetHeaderMap_(sheet);
    const data = sheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      const rowCode = normalizeExam_(rowValue_(data[i], map, 'Exam Code', 0));
      if (rowCode !== code) continue;

      const status = String(rowValue_(data[i], map, 'Status', 6) || 'ACTIVE').trim().toUpperCase();
      const activeStatuses = ['ACTIVE', 'ENABLED', 'نشط', 'مفعل'];
      if (activeStatuses.indexOf(status) === -1) return null;

      return {
        code: code,
        title: String(rowValue_(data[i], map, 'Exam Title', 1) || (fallback ? fallback.title : '') || code),
        grade: String(rowValue_(data[i], map, 'Grade Level', 2) || (fallback ? fallback.grade : '')),
        subject: String(rowValue_(data[i], map, 'Subject', 3) || (fallback ? fallback.subject : '')),
        questionsCount: Number(rowValue_(data[i], map, 'Questions', 4)) || 10,
        duration: Number(rowValue_(data[i], map, 'Duration (Mins)', 5)) || 20,
        status: status
      };
    }
  }

  return fallback;
}

function rowValue_(row, map, header, fallbackIndex) {
  const index = headerIndex_(map, header, fallbackIndex);
  return row[index];
}

/**
 * Loads questions from Question_Bank (bank-first), starts/reuses a server-side
 * session, and returns only the public question fields to the browser.
 */
function getExamData(examCode, studentName) {
  try {
    const exam = getExamInfo(examCode);
    if (!exam) {
      return { success: false, code: 'EXAM_NOT_FOUND', message: 'هذا الامتحان غير موجود أو غير مفعّل.' };
    }

    const name = String(studentName || '').trim();
    if (!name) {
      return { success: false, code: 'STUDENT_REQUIRED', message: 'اسم الطالب مطلوب لبدء الامتحان.' };
    }

    const lock = LockService.getScriptLock();
    if (!lock.tryLock(30000)) {
      return { success: false, code: 'BUSY', message: 'الخادم مشغول، حاول مرة أخرى بعد لحظات.' };
    }

    try {
      // 1. Check/Sweep active sessions under lock (consuming expired sessions safely)
      let active = findActiveSession_(name, exam.code);

      // 2. Compute attempt state fresh AFTER any expired session sweep
      const state = getAttemptState_(name, exam.code);

      if (active) {
        return {
          success: true,
          sessionKey: active.id,
          sessionId: active.id,
          exam: Object.assign({}, exam, { questionsCount: active.questions.length }),
          questions: publicQuestions_(active.questions),
          remainingSeconds: Math.max(0, Math.floor((valueToMillis_(active.expiresAt) - Date.now()) / 1000)),
          attemptNumber: state.attemptsCount + 1,
          maxAttempts: MAX_ATTEMPTS,
          resumed: true
        };
      }

      // 3. Strict attempt limit validation on FRESH state
      if (!state.canAttempt) {
        return {
          success: false,
          code: 'MAX_ATTEMPTS',
          message: 'تم استنفاد المحاولات المتاحة. اطلب من ولي الأمر الموافقة على محاولة إضافية.',
          maxAttempts: state.maxAttempts,
          retakeStatus: state.retakeStatus
        };
      }

      // 4. Build and persist fresh session under the same lock
      const built = buildExamQuestions_(exam.code);
      const session = createSession_(name, built.exam, built.questions);

      return {
        success: true,
        sessionKey: session.id,
        sessionId: session.id,
        exam: built.exam,
        questions: publicQuestions_(session.questions),
        remainingSeconds: Math.max(0, Math.floor((valueToMillis_(session.expiresAt) - Date.now()) / 1000)),
        attemptNumber: state.attemptsCount + 1,
        maxAttempts: MAX_ATTEMPTS,
        resumed: false
      };
    } finally {
      lock.releaseLock();
    }
  } catch (err) {
    Logger.log('getExamData error: ' + err);
    return {
      success: false,
      code: 'SERVER_ERROR',
      message: 'تعذر تحميل الامتحان: ' + err.message
    };
  }
}

function validateSession_(data, now) {
  const sessionId = String(data.sessionKey || data.sessionId || '').trim();
  if (!sessionId) {
    return { error: { success: false, code: 'SESSION_REQUIRED', message: 'جلسة الامتحان غير موجودة. أعد تحميل الامتحان.' } };
  }

  const session = findSessionById_(sessionId);
  if (!session) {
    return { error: { success: false, code: 'SESSION_NOT_FOUND', message: 'جلسة الامتحان غير موجودة أو انتهت. أعد تحميل الامتحان.' } };
  }

  // Idempotency: a repeated click returns the saved result instead of a second row.
  if (session.status === 'COMPLETED') {
    if (session.result) return { error: Object.assign({ success: true, alreadySubmitted: true }, session.result) };
    return { error: { success: false, code: 'ALREADY_SUBMITTED', message: 'تم تسليم هذا الامتحان بالفعل.' } };
  }

  if (session.status !== 'ACTIVE') {
    return { error: { success: false, code: 'SESSION_CLOSED', message: 'هذه الجلسة لم تعد صالحة. ابدأ محاولة جديدة.' } };
  }

  if (normalizeName_(data.studentName) !== normalizeName_(session.studentName)) {
    return { error: { success: false, code: 'STUDENT_MISMATCH', message: 'اسم الطالب لا يطابق جلسة الامتحان.' } };
  }
  if (normalizeExam_(data.examCode) !== normalizeExam_(session.examCode)) {
    return { error: { success: false, code: 'EXAM_MISMATCH', message: 'كود الامتحان لا يطابق جلسة الامتحان.' } };
  }

  const expiresMillis = valueToMillis_(session.expiresAt);
  if (expiresMillis && now > expiresMillis + (ATTEMPT_GRACE_SECONDS * 1000)) {
    const sheet = getSessionSheet_();
    sheet.getRange(session.rowIndex, SESSION_COLS.status + 1).setValue('EXPIRED_CONSUMED');
    recordExpiredSessionSubmission_(session);
    return { error: { success: false, code: 'TIME_EXPIRED', message: 'انتهى وقت الامتحان. اطلب من ولي الأمر محاولة جديدة.' } };
  }

  const questions = Array.isArray(session.questions) ? session.questions : [];
  if (!questions.length) {
    return { error: { success: false, code: 'EMPTY_SESSION', message: 'جلسة الامتحان لا تحتوي على أسئلة.' } };
  }

  return { session: session };
}

function gradeAnswers_(questions, answers) {
  let earnedScore = 0;
  let totalScore = 0;
  const reviewDetails = [];

  questions.forEach(question => {
    const points = Number(question.points) || 1;
    totalScore += points;

    const hasAnswer = Object.prototype.hasOwnProperty.call(answers, question.id);
    const studentAnswer = hasAnswer ? String(answers[question.id] == null ? '' : answers[question.id]).trim() : '';
    const isCorrect = studentAnswer !== '' &&
      normalizeAnswer_(studentAnswer) === normalizeAnswer_(question.correctAnswer);

    if (isCorrect) earnedScore += points;

    reviewDetails.push({
      questionId: question.id,
      questionText: question.text,
      studentAnswer: studentAnswer,
      correctAnswer: question.correctAnswer,
      isCorrect: isCorrect,
      pointsAwarded: isCorrect ? points : 0,
      maxPoints: points,
      explanation: question.explanation || ''
    });
  });

  const percentage = totalScore > 0 ? Math.round((earnedScore / totalScore) * 100) : 0;
  let rating = 'Needs Practice 🌱';
  if (percentage >= 85) rating = 'Excellent 🌟';
  else if (percentage >= 75) rating = 'Very Good 👏';
  else if (percentage >= 65) rating = 'Good 👍';
  else if (percentage >= 50) rating = 'Satisfactory 📚';

  return {
    earnedScore: earnedScore,
    totalScore: totalScore,
    percentage: percentage,
    rating: rating,
    reviewDetails: reviewDetails
  };
}

function persistSubmission_(session, payloadData, result, timestamp, durationStr, summaryStr) {
  const ss = getSpreadsheet();
  let subSheet = ss.getSheetByName('Submissions');
  if (!subSheet) {
    setupDatabase(ss);
    subSheet = ss.getSheetByName('Submissions');
  }

  subSheet.appendRow([
    timestamp,
    session.studentName,
    session.grade || payloadData.schoolGroup || 'General',
    session.examCode,
    result.earnedScore,
    result.totalScore,
    result.percentage,
    result.rating,
    durationStr,
    summaryStr,
    JSON.stringify(result.review)
  ]);

  const lastRow = subSheet.getLastRow();
  subSheet.getRange(lastRow, 1, 1, 11).setVerticalAlignment('middle').setFontSize(10);
  subSheet.getRange(lastRow, 5, 1, 3).setHorizontalAlignment('center');

  const sessionSheet = getSessionSheet_();
  sessionSheet.getRange(session.rowIndex, SESSION_COLS.status + 1).setValue('COMPLETED');
  sessionSheet.getRange(session.rowIndex, SESSION_COLS.result + 1).setValue(JSON.stringify(result));
}

function consumeRetake_(studentName, examCode) {
  const ss = getSpreadsheet();
  const retakeSheet = ss.getSheetByName('Retake_Requests');
  if (retakeSheet && retakeSheet.getLastRow() > 1) {
    const rData = retakeSheet.getDataRange().getValues();
    for (let i = 1; i < rData.length; i++) {
      if (normalizeName_(rData[i][2]) === normalizeName_(studentName) &&
          normalizeExam_(rData[i][3]) === normalizeExam_(examCode) &&
          String(rData[i][6] || '').trim().toUpperCase() === 'APPROVED') {
        retakeSheet.getRange(i + 1, 7).setValue('CONSUMED');
      }
    }
  }
}

function submitExamAnswers(payload) {
  const lock = LockService.getScriptLock();
  try {
    if (!lock.tryLock(30000)) {
      return { success: false, code: 'BUSY', message: 'الخادم مشغول، أعد المحاولة بعد لحظات.' };
    }

    const data = (typeof payload === 'string') ? JSON.parse(payload) : payload;
    const now = Date.now();
    const validation = validateSession_(data, now);
    if (validation.error) return validation.error;

    const session = validation.session;
    const answers = (data.answers && typeof data.answers === 'object') ? data.answers : {};
    const graded = gradeAnswers_(session.questions || [], answers);

    const startedMillis = valueToMillis_(session.startedAt);
    const durationSeconds = Math.max(0, Math.round((now - (startedMillis || now)) / 1000));
    const durationStr = `${Math.floor(durationSeconds / 60)} min ${durationSeconds % 60} sec`;
    const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
    const summaryStr = `${graded.earnedScore}/${graded.totalScore} Correct (${graded.percentage}%)`;

    const result = {
      earnedScore: graded.earnedScore,
      totalScore: graded.totalScore,
      percentage: graded.percentage,
      rating: graded.rating,
      durationSpent: durationStr,
      review: graded.reviewDetails,
      submittedAt: timestamp,
      sessionId: session.id
    };

    persistSubmission_(session, data, result, timestamp, durationStr, summaryStr);
    consumeRetake_(session.studentName, session.examCode);

    return Object.assign({ success: true, alreadySubmitted: false }, result);

  } catch (err) {
    Logger.log('submitExamAnswers error: ' + err);
    return {
      success: false,
      code: 'SERVER_ERROR',
      message: 'تعذر تسجيل الإجابات: ' + err.message
    };
  } finally {
    try { lock.releaseLock(); } catch (e) { /* not held */ }
  }
}

function normalizePercentageColumn() {
  const ss = getSpreadsheet();
  const subSheet = ss.getSheetByName('Submissions');
  if (!subSheet || subSheet.getLastRow() <= 1) return { success: true, count: 0 };
  const range = subSheet.getRange(2, 7, subSheet.getLastRow() - 1, 1);
  const values = range.getValues();
  let changed = 0;
  for (let i = 0; i < values.length; i++) {
    const raw = values[i][0];
    let numVal = typeof raw === 'number' ? raw : parseFloat(String(raw || '').replace('%', '').trim());
    if (isNaN(numVal)) numVal = 0;
    if (numVal <= 1 && numVal > 0) numVal = Math.round(numVal * 100);
    if (raw !== numVal) {
      values[i][0] = numVal;
      changed++;
    }
  }
  if (changed > 0) range.setValues(values);
  return { success: true, count: changed };
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

function getStudentExamStatus(studentName, examCode) {
  try {
    const name = String(studentName || '').trim();
    const code = normalizeExam_(examCode);
    if (!name || !code) {
      return { success: false, message: 'اسم الطالب وكود الامتحان مطلوبان.' };
    }

    const state = getAttemptState_(name, code);
    return {
      success: true,
      hasSubmitted: state.hasSubmitted,
      attemptsCount: state.attemptsCount,
      attempts: state.attempts,
      lastScore: state.lastScore,
      lastDate: state.lastDate,
      canAttempt: state.canAttempt,
      retakeStatus: state.retakeStatus,
      requestId: state.requestId,
      maxAttempts: state.maxAttempts,
      exam: getExamInfo(code)
    };
  } catch (e) {
    Logger.log('getStudentExamStatus error: ' + e);
    return { success: false, message: e.message };
  }
}

function requestExamRetake(payload) {
  const lock = LockService.getScriptLock();
  try {
    if (!lock.tryLock(30000)) return { success: false, message: 'الخادم مشغول، أعد المحاولة بعد لحظات.' };

    const data = (typeof payload === 'string') ? JSON.parse(payload) : payload;
    const studentName = String(data.studentName || '').trim();
    const examCode = normalizeExam_(data.examCode);
    if (!studentName || !examCode) {
      return { success: false, message: 'اسم الطالب وكود الامتحان مطلوبان.' };
    }

    const exam = getExamInfo(examCode);
    if (!exam) return { success: false, message: 'الامتحان غير موجود.' };

    const state = getAttemptState_(studentName, examCode);
    if (!state.hasSubmitted || state.attemptsCount < MAX_ATTEMPTS) {
      return { success: false, message: 'يمكنك طلب إعادة المحاولة بعد استنفاد المحاولتين الأساسيتين.' };
    }
    if (state.retakeStatus === 'PENDING') {
      return { success: true, requestId: state.requestId, message: 'طلبك قيد مراجعة ولي الأمر بالفعل.' };
    }
    if (state.retakeStatus === 'APPROVED') {
      return { success: false, message: 'تمت الموافقة على طلبك بالفعل، ابدأ المحاولة الإضافية من بوابة الطالب.' };
    }

    const ss = getSpreadsheet();
    let retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet) {
      setupDatabase(ss);
      retakeSheet = ss.getSheetByName('Retake_Requests');
    }

    const reqId = 'REQ_' + Utilities.getUuid().replace(/-/g, '').slice(0, 16).toUpperCase();
    const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
    const reason = String(data.reason || 'طلب محاولة إضافية لمراجعة الأخطاء').slice(0, 500);

    retakeSheet.appendRow([
      reqId,
      timestamp,
      studentName,
      examCode,
      exam.title,
      state.lastScore || 'N/A',
      'PENDING',
      reason,
      ''
    ]);

    return {
      success: true,
      requestId: reqId,
      message: 'تم إرسال طلب إعادة المحاولة إلى ولي الأمر.'
    };
  } catch (e) {
    Logger.log('requestExamRetake error: ' + e);
    return { success: false, message: 'تعذر إرسال الطلب: ' + e.message };
  } finally {
    try { lock.releaseLock(); } catch (e) { /* not held */ }
  }
}

const memoryTokenCache_ = {};

function storeAdminToken_(token, ttlSeconds) {
  memoryTokenCache_[token] = Date.now() + (ttlSeconds || 1800) * 1000;
  try {
    const cache = CacheService.getScriptCache();
    if (cache && cache.put) cache.put(token, 'VALID', ttlSeconds || 1800);
  } catch (e) {}
}

function isAdminTokenValid_(token) {
  if (!token) return false;
  const strToken = String(token || '').trim();
  if (!strToken.startsWith('ADMIN_TOK_')) return false;

  const expiry = memoryTokenCache_[strToken];
  if (expiry && expiry > Date.now()) return true;

  try {
    const cache = CacheService.getScriptCache();
    if (cache && cache.get) {
      const val = cache.get(strToken);
      if (val === 'VALID') return true;
    }
  } catch (e) {}

  return false;
}

function hashPin_(pin, salt) {
  const s = salt || 'PRIMARY_EXAM_SALT_2026';
  const raw = s + ':' + String(pin || '').trim();
  if (typeof Utilities !== 'undefined' && Utilities.computeDigest && Utilities.DigestAlgorithm) {
    const digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, raw, Utilities.Charset.UTF_8);
    return digest.map(b => ('0' + (b & 0xFF).toString(16)).slice(-2)).join('');
  }
  let hash = 0;
  for (let i = 0; i < raw.length; i++) {
    hash = ((hash << 5) - hash) + raw.charCodeAt(i);
    hash |= 0;
  }
  return 'FALLBACK_HASH_' + Math.abs(hash);
}

function normalizePin_(str) {
  if (!str) return '';
  let s = String(str);
  s = s.replace(/[٠-٩]/g, function(c) { return c.charCodeAt(0) - 0x0660; });
  s = s.replace(/[۰-۹]/g, function(c) { return c.charCodeAt(0) - 0x06F0; });
  return s.replace(/\D/g, '').trim();
}

function verifyGatewayPin(enteredPin) {
  try {
    const norm = normalizePin_(enteredPin);
    if (!norm) {
      return { success: false, code: 'EMPTY_PIN', message: 'يرجى إدخال رمز الدخول.' };
    }

    const props = PropertiesService.getScriptProperties();

    // 1. Parent PIN Check
    let expectedAdminHash = props.getProperty('ADMIN_PIN_HASH');
    if (!expectedAdminHash) {
      expectedAdminHash = hashPin_('1990');
      props.setProperty('ADMIN_PIN_HASH', expectedAdminHash);
    }
    if (hashPin_(norm) === expectedAdminHash) {
      const token = 'ADMIN_TOK_' + Utilities.getUuid().replace(/-/g, '').slice(0, 24);
      storeAdminToken_(token, 1800);
      return {
        success: true,
        role: 'parent',
        token: token,
        message: 'Welcome Parent! Opening Dashboard...'
      };
    }

    // 2. Mostafa PIN Check
    let mostafaHash = props.getProperty('STUDENT_PIN_MOSTAFA');
    if (!mostafaHash) {
      mostafaHash = hashPin_('2014');
      props.setProperty('STUDENT_PIN_MOSTAFA', mostafaHash);
    }
    if (hashPin_(norm) === mostafaHash) {
      return {
        success: true,
        role: 'student',
        studentKey: 'mostafa',
        message: 'Welcome Mostafa! Opening Grade 6...'
      };
    }

    // 3. Ali PIN Check
    let aliHash = props.getProperty('STUDENT_PIN_ALI');
    if (!aliHash) {
      aliHash = hashPin_('2016');
      props.setProperty('STUDENT_PIN_ALI', aliHash);
    }
    if (hashPin_(norm) === aliHash) {
      return {
        success: true,
        role: 'student',
        studentKey: 'ali',
        message: 'Welcome Ali! Opening Grade 5...'
      };
    }

    return {
      success: false,
      code: 'INVALID_PIN',
      message: 'رمز الدخول غير صحيح. يرجى المحاولة مرة أخرى.'
    };
  } catch (err) {
    Logger.log('verifyGatewayPin error: ' + err);
    return { success: false, code: 'SERVER_ERROR', message: err.message };
  }
}

function verifyAdminPin(enteredPin) {
  try {
    const norm = String(enteredPin || '').trim();
    const props = PropertiesService.getScriptProperties();
    let expectedHash = props.getProperty('ADMIN_PIN_HASH');
    if (!expectedHash) {
      expectedHash = hashPin_('1990');
      props.setProperty('ADMIN_PIN_HASH', expectedHash);
    }

    const enteredHash = hashPin_(norm);
    if (enteredHash !== expectedHash) {
      return { success: false, code: 'INVALID_PIN', message: 'رمز الدخول غير صحيح' };
    }

    const token = 'ADMIN_TOK_' + Utilities.getUuid().replace(/-/g, '').slice(0, 24);
    storeAdminToken_(token, 1800);
    return { success: true, token: token };
  } catch (err) {
    Logger.log('verifyAdminPin error: ' + err);
    return { success: false, code: 'SERVER_ERROR', message: err.message };
  }
}

function approveRetakeRequest(requestId, adminToken) {
  if (!isAdminTokenValid_(adminToken)) {
    return { success: false, code: 'UNAUTHORIZED', message: 'غير مصرح بالدخول. يرجى إدخال رمز الإدارة.' };
  }
  return decideRetakeRequest_(requestId, 'APPROVED');
}

function rejectRetakeRequest(requestId, adminToken) {
  if (!isAdminTokenValid_(adminToken)) {
    return { success: false, code: 'UNAUTHORIZED', message: 'غير مصرح بالدخول. يرجى إدخال رمز الإدارة.' };
  }
  return decideRetakeRequest_(requestId, 'REJECTED');
}

function decideRetakeRequest_(requestId, decision) {
  const lock = LockService.getScriptLock();
  try {
    if (!lock.tryLock(30000)) return { success: false, message: 'الخادم مشغول، أعد المحاولة بعد لحظات.' };

    const ss = getSpreadsheet();
    const retakeSheet = ss.getSheetByName('Retake_Requests');
    if (!retakeSheet || retakeSheet.getLastRow() <= 1) {
      return { success: false, message: 'لا توجد طلبات إعادة محاولة.' };
    }

    const target = String(requestId || '').trim();
    const data = retakeSheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      if (String(data[i][0] || '').trim() !== target) continue;

      const currentStatus = String(data[i][6] || '').trim().toUpperCase();
      if (currentStatus !== 'PENDING') {
        return { success: false, message: 'هذا الطلب تمت معالجته بالفعل.' };
      }

      retakeSheet.getRange(i + 1, 7).setValue(decision);
      retakeSheet.getRange(i + 1, 9).setValue(new Date());
      return {
        success: true,
        message: decision === 'APPROVED'
          ? 'تمت الموافقة. يمكن للطالب بدء محاولة إضافية.'
          : 'تم رفض طلب إعادة المحاولة.'
      };
    }

    return { success: false, message: 'لم يتم العثور على رقم الطلب.' };
  } catch (e) {
    Logger.log('decideRetakeRequest_ error: ' + e);
    return { success: false, message: e.message };
  } finally {
    try { lock.releaseLock(); } catch (e) { /* not held */ }
  }
}

function getAdminDashboardData(adminToken) {
  try {
    if (!isAdminTokenValid_(adminToken)) {
      return { success: false, code: 'UNAUTHORIZED', message: 'غير مصرح بالدخول. يرجى إدخال رمز الإدارة.' };
    }
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

    // Show the actual question bank. Only fall back to generated samples when a
    // bank has no questions for that exam.
    const allQuestions = [];
    const examCodes = exams.length
      ? exams.map(e => e.code)
      : ['EX_Y5_ENG_ADV01', 'EX_Y6_ENG_FANTASY01', 'EX_Y6_ARB_PRIO01'];

    examCodes.forEach(code => {
      let questions = loadBankQuestions_(code);
      if (!questions.length) {
        if (code === 'EX_Y5_ENG_ADV01') questions = generateAliAdverbialExam();
        else if (code === 'EX_Y6_ENG_FANTASY01') questions = generateMostafaEnglishExam();
        else if (code === 'EX_Y6_ARB_PRIO01') questions = generateMostafaArabicExam();
      }
      questions.forEach(q => allQuestions.push(Object.assign({}, q, { examCode: code })));
    });

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
  let built;
  try {
    built = buildExamQuestions_(examCode);
  } catch (e) {
    try { SpreadsheetApp.getUi().alert('تعذر إنشاء النموذج: ' + e.message); } catch (uiError) {}
    return;
  }

  const exam = built.exam;
  const questions = built.questions;

  const form = FormApp.create(exam.title + ' - (' + exam.grade + ')');
  form.setDescription('Interactive Assessment for ' + exam.subject + '\nDuration: ' + exam.duration + ' Minutes\nPlease complete all questions carefully.')
      .setIsQuiz(true)
      .setAllowResponseEdits(false)
      .setCollectEmail(false)
      .setConfirmationMessage('تم تسليم إجاباتك. شكراً لك!');

  form.addTextItem().setTitle('Student Full Name:').setRequired(true);
  form.addTextItem().setTitle('School / Class:').setRequired(false);

  // Keep Form responses in the same spreadsheet alongside the web app data.
  try {
    form.setDestination(FormApp.DestinationType.SPREADSHEET, getSpreadsheet().getId());
  } catch (destinationError) {
    Logger.log('Could not set Form destination: ' + destinationError);
  }

  questions.forEach((q, idx) => {
    const qTitle = '(' + (idx + 1) + ') ' + String(q.text || '').replace(/<[^>]*>?/gm, '');
    if (q.type === 'MCQ' || q.type === 'TRUE_FALSE') {
      const item = form.addMultipleChoiceItem().setTitle(qTitle).setRequired(true);
      const choices = q.options.map(opt => item.createChoice(
        opt,
        normalizeAnswer_(opt) === normalizeAnswer_(q.correctAnswer)
      ));
      item.setChoices(choices);
      item.setPoints(Number(q.points) || 1);
      if (q.passage) item.setHelpText(String(q.passage));

      try {
        const correctFeedback = FormApp.createFeedback()
          .setText(q.explanation || ('الإجابة الصحيحة: ' + q.correctAnswer))
          .build();
        const incorrectFeedback = FormApp.createFeedback()
          .setText('الإجابة الصحيحة: ' + q.correctAnswer + '\n' + (q.explanation || ''))
          .build();
        item.setFeedbackForCorrect(correctFeedback);
        item.setFeedbackForIncorrect(incorrectFeedback);
      } catch (feedbackError) {
        Logger.log('Form feedback error: ' + feedbackError);
      }
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
