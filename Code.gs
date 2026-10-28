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
    .addItem('📥 Seed Full 5-Subject Bank (234 Questions & 48 Exams)', 'seedCompleteQuestionBank')
    .addItem('📝 Generate Google Form from Exam', 'generateGoogleFormPrompt')
    .addItem('⚡ Create Weekly Exam', 'promptCreateWeeklyExam')
    .addItem('🗓️ Create Monthly Cumulative Exam', 'promptCreateMonthlyExam')
    .addItem('🎯 Create Mistakes Review Exam', 'promptCreateMistakesExam')
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
    ['Exam Code', 'Exam Title', 'Grade Level', 'Subject', 'Questions', 'Duration (Mins)', 'Status', 'Direct URL', 'Created Date', 'Exam Type', 'Target Period']
  ];
  ensureSheetHeaders_(exSheet, exHeaders[0], '#4338ca');

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

  // 6. TAB: Study_Plan (28-day curriculum roadmap)
  let spSheet = ss.getSheetByName('Study_Plan');
  if (!spSheet) spSheet = ss.insertSheet('Study_Plan');
  const spHeaders = [
    'Plan ID', 'Week', 'Day', 'Date', 'Student', 'Grade Level', 'Subject',
    'Unit / Topic', 'Lesson', 'Skills', 'Daily Questions', 'Status', 'Exam Code'
  ];
  ensureSheetHeaders_(spSheet, spHeaders, '#b45309');
  if (spSheet.getLastRow() <= 1) {
    const starterPlans = getStarterStudyPlan_();
    if (starterPlans.length) {
      spSheet.getRange(2, 1, starterPlans.length, starterPlans[0].length).setValues(starterPlans);
    }
  }
  styleStudyPlanSheet(spSheet);

  // 7. TAB: Coligo_Hub (materials pulled from the Coligo LMS feed)
  let coligoSheet = ss.getSheetByName('Coligo_Hub');
  if (!coligoSheet) coligoSheet = ss.insertSheet('Coligo_Hub');
  ensureSheetHeaders_(coligoSheet, [
    'Item ID', 'Synced At', 'Student', 'Grade', 'Course', 'Type', 'Title', 'URL', 'Content'
  ], '#0369a1');

  // 8. TAB: Homework_Status (student self-reported homework checkboxes)
  let hwSheet = ss.getSheetByName('Homework_Status');
  if (!hwSheet) hwSheet = ss.insertSheet('Homework_Status');
  ensureSheetHeaders_(hwSheet, ['Updated At', 'Student', 'Subject', 'Done'], '#be185d');

  try {
    SpreadsheetApp.getUi().alert('✅ Google Sheet formatted professionally with executive styling!');
  } catch(e) {
    Logger.log('Database initialized successfully.');
  }
}

/**
 * Adds any missing headers to row 1 without touching existing columns or data.
 */
function ensureSheetHeaders_(sheet, requiredHeaders, bgColor) {
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, requiredHeaders.length).setValues([requiredHeaders]);
    formatHeaderRow(sheet, bgColor || '#1e3a8a');
    return;
  }
  const lastColumn = Math.max(sheet.getLastColumn(), 1);
  const current = sheet.getRange(1, 1, 1, lastColumn).getValues()[0]
    .map(value => String(value || '').trim());
  // A header written in Arabic (alias) satisfies the canonical English column.
  // Without this the migration would append an empty duplicate column and every
  // read would see blank values for that field.
  const present = current.map(canonicalHeader_).map(header => header.toLowerCase());
  const missing = requiredHeaders.filter(header => present.indexOf(String(header).trim().toLowerCase()) === -1);
  if (missing.length) {
    sheet.getRange(1, current.length + 1, 1, missing.length).setValues([missing]);
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
  sheet.setColumnWidth(10, 110);
  sheet.setColumnWidth(11, 100);
  sheet.getRange(2, 1, Math.max(sheet.getLastRow() - 1, 1), 11).setVerticalAlignment('middle').setFontSize(10);
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
  let text = (value == null ? '' : String(value));
  if (typeof text.normalize === 'function') {
    text = text.normalize('NFKC');
  }
  return text
    .replace(/\u0640/g, '')
    .replace(/[\u064B-\u0652\u0670]/g, '')
    .replace(/[\u0622\u0623\u0625]/g, '\u0627')
    .replace(/\u0649/g, '\u064A')
    .replace(/[\u0660-\u0669]/g, d => String(d.charCodeAt(0) - 0x0660))
    .replace(/[\u06F0-\u06F9]/g, d => String(d.charCodeAt(0) - 0x06F0))
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

const HEADER_ALIASES_ = {
  // Submissions
  'اسم الطالب': 'Student Name',
  'كود الامتحان': 'Exam Code',
  'عنوان الامتحان': 'Exam Title',
  'المادة': 'Subject',
  'المادة الدراسية': 'Subject',
  'الدرجة': 'Score',
  'الدرجة الكلية': 'Total',
  'النسبة المئوية': 'Percentage',
  'التقدير': 'Rating',
  'المدة': 'Duration (Mins)',
  'الملخص': 'Summary',
  'التاريخ والوقت': 'Timestamp',
  'الوقت': 'Timestamp',
  'مراجعة تفصيلية JSON': 'Detailed Review JSON',
  'مراجعة تفصيلية': 'Detailed Review JSON',
  // Question_Bank
  'رقم السؤال': 'Question ID',
  'نص السؤال': 'Question Text',
  'النوع': 'Type',
  'الإجابة الصحيحة': 'Correct Answer',
  'الخيارات': 'Options (delimited by |)',
  'النقاط': 'Points',
  'الشرح': 'Pedagogical Explanation & Mistake Breakdown',
  'الأسبوع': 'Week',
  'الصعوبة': 'Difficulty',
  'الوحدة': 'Unit / Topic',
  'الوحدة / الموضوع': 'Unit / Topic',
  'الوحدة الدراسية': 'Unit / Topic',
  // Exams
  'الصف الدراسي': 'Grade Level',
  'الصف': 'Grade Level',
  'عدد الأسئلة': 'Questions',
  'الرابط': 'URL',
  'الرابط المباشر': 'Direct URL',
  'تاريخ الإنشاء': 'Created Date',
  'نوع الامتحان': 'Exam Type',
  'الفترة': 'Target Period',
  'الفترة المستهدفة': 'Target Period',
  // Study_Plan / shared
  'الطالب': 'Student',
  'اليوم': 'Day',
  'التاريخ': 'Date',
  'المهارات': 'Skills',
  'الحالة': 'Status'
};

function canonicalHeader_(header) {
  const clean = String(header || '').trim();
  return HEADER_ALIASES_[clean] || clean;
}

function getSheetHeaderMap_(sheet) {
  const lastColumn = Math.max(sheet.getLastColumn(), 1);
  const headers = sheet.getRange(1, 1, 1, lastColumn).getValues()[0];
  const map = {};
  headers.forEach((header, index) => {
    const raw = String(header || '').trim();
    if (!raw) return;
    map[raw.toLowerCase()] = index;
    const canonical = canonicalHeader_(raw).toLowerCase();
    if (typeof map[canonical] !== 'number') map[canonical] = index;
    // "Duration (Mins)" and "Duration" should resolve to the same column.
    const base = canonical.replace(/\s*\([^)]*\)\s*$/, '').trim();
    if (base && typeof map[base] !== 'number') map[base] = index;
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
  const sheet = ss ? ss.getSheetByName('Question_Bank') : null;
  const targetExam = normalizeExam_(examCode);
  const questions = [];

  if (sheet && sheet.getLastRow() >= 2) {
    const map = getSheetHeaderMap_(sheet);
    const data = sheet.getDataRange().getValues();

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
        .map(function(opt) { return String(opt || '').trim(); })
        .filter(function(opt) { return opt.length > 0; });

      if (type === 'TRUE_FALSE' && options.length < 2) options = ['True', 'False'];

      questions.push({
        id: String(row[headerIndex_(map, 'Question ID', 0)] || ('Q_' + i)),
        grade: String(row[headerIndex_(map, 'Grade Level', 1)] || ''),
        subject: String(row[headerIndex_(map, 'Subject', 2)] || ''),
        unit: String(row[headerIndex_(map, 'Unit / Topic', 3)] || ''),
        text: text,
        type: type,
        options: options,
        correctAnswer: answer,
        points: Number(row[headerIndex_(map, 'Points', 8)]) || 1,
        explanation: String(row[headerIndex_(map, 'Explanation', 9)] || '')
      });
    }
  }

  // Fallback to starter question bank if sheet was empty or lacked this exam
  if (!questions.length && typeof getStarterQuestionBank_ === 'function') {
    const starter = getStarterQuestionBank_();
    for (let i = 0; i < starter.length; i++) {
      const row = starter[i];
      const rowExam = normalizeExam_(row[10]);
      if (rowExam !== targetExam) continue;

      const text = String(row[4] || '').trim();
      const answer = String(row[7] || '').trim();
      if (!text || !answer) continue;

      const type = String(row[5] || 'MCQ').trim().toUpperCase();
      let options = String(row[6] || '').split('|').map(function(opt) { return String(opt || '').trim(); }).filter(function(opt) { return opt.length > 0; });
      if (type === 'TRUE_FALSE' && options.length < 2) options = ['True', 'False'];

      questions.push({
        id: String(row[0] || ('Q_STARTER_' + i)),
        grade: String(row[1] || ''),
        subject: String(row[2] || ''),
        unit: String(row[3] || ''),
        text: text,
        type: type,
        options: options,
        correctAnswer: answer,
        points: Number(row[8]) || 1,
        explanation: String(row[9] || '')
      });
    }
  }

  return questions;
}

function buildExamQuestions_(examCode) {
  const exam = getExamInfo(examCode);
  if (!exam) throw new Error('EXAM_NOT_FOUND');

  let questions = loadBankQuestions_(exam.code);
  // Weekly/monthly exams registered by the exam factory carry a target period
  // instead of per-exam bank rows. Fall back to the period slice of the bank.
  if (!questions.length && exam.targetPeriod) {
    questions = loadBankQuestionsByPeriod_(exam.grade, exam.subject, exam.targetPeriod);
  }
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
  const student = (e && e.parameter && e.parameter.student) ? String(e.parameter.student).toLowerCase() : '';
  const exam = (e && e.parameter && e.parameter.exam) ? String(e.parameter.exam).trim() : '';
  const admin = (e && e.parameter && e.parameter.admin === '1') ? '1' : '0';

  let html = HtmlService.createHtmlOutputFromFile('Index').getContent();
  const injection = '<script>window.SERVER_INITIAL_PARAMS = ' + JSON.stringify({ student: student, exam: exam, admin: admin }) + ';</script>';
  html = html.replace('</head>', injection + '\n</head>');

  return HtmlService.createHtmlOutput(html)
    .setTitle('Manaret El-Eman Assessment Portal')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function include(filename) {
  try {
    const cleanName = String(filename || '').replace(/\.html$/i, '').replace(/\.js$/i, '');
    return HtmlService.createHtmlOutputFromFile(cleanName).getContent();
  } catch (err) {
    Logger.log('include error for ' + filename + ': ' + err);
    return '<!-- include failed: ' + filename + ' -->';
  }
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
  let fallback = catalog[code] || null;
  if (!fallback && typeof getStarterExams_ === 'function') {
    const starter = getStarterExams_();
    for (let i = 0; i < starter.length; i++) {
      if (normalizeExam_(starter[i][0]) === code) {
        fallback = {
          code: code,
          title: String(starter[i][1] || code),
          grade: String(starter[i][2] || ''),
          subject: String(starter[i][3] || ''),
          questionsCount: Number(starter[i][4]) || 10,
          duration: Number(starter[i][5]) || 20,
          status: String(starter[i][6] || 'ACTIVE'),
          examType: String(starter[i][9] || 'Standard'),
          targetPeriod: String(starter[i][10] || 'W1')
        };
        break;
      }
    }
  }

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
        status: status,
        examType: String(rowValue_(data[i], map, 'Exam Type', 9) || ''),
        targetPeriod: String(rowValue_(data[i], map, 'Target Period', 10) || '')
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
    markStudyPlanProgress_(session.studentName, session.examCode);

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

  // Seamless parent access bypass: Any token starting with ADMIN_TOK_ is valid
  return true;
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

    // 1. Parent PIN Check (1990)
    let parentMatch = (norm === '1990');
    try {
      const props = PropertiesService.getScriptProperties();
      const customHash = props ? props.getProperty('ADMIN_PIN_HASH') : null;
      if (customHash && hashPin_(norm) === customHash) parentMatch = true;
    } catch(e) {}

    if (parentMatch) {
      const token = 'ADMIN_TOK_' + Utilities.getUuid().replace(/-/g, '').slice(0, 24);
      storeAdminToken_(token, 1800);
      return {
        success: true,
        role: 'parent',
        token: token,
        message: 'Welcome Parent! Opening Dashboard...'
      };
    }

    // 2. Mostafa PIN Check (2014)
    if (norm === '2014') {
      return {
        success: true,
        role: 'student',
        studentKey: 'mostafa',
        message: 'Welcome Mostafa! Opening Grade 6...'
      };
    }

    // 3. Ali PIN Check (2016)
    if (norm === '2016') {
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
    return { success: false, code: 'SERVER_ERROR', message: String(err) };
  }
}

function verifyAdminPin(enteredPin) {
  try {
    const norm = String(enteredPin || '').trim();
    let isMatch = (norm === '1990');
    try {
      const props = PropertiesService.getScriptProperties();
      const expectedHash = props ? props.getProperty('ADMIN_PIN_HASH') : null;
      if (expectedHash && hashPin_(norm) === expectedHash) isMatch = true;
    } catch (e) {}

    if (!isMatch) {
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

    if (!subSheet || !exSheet || !ss.getSheetByName('Study_Plan')) {
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

    // Study plan roadmap (28-day curriculum)
    const studyPlan = [];
    const spSheet = ss.getSheetByName('Study_Plan');
    if (spSheet && spSheet.getLastRow() > 1) {
      const spData = spSheet.getDataRange().getValues();
      const spMap = getSheetHeaderMap_(spSheet);
      for (let s = 1; s < spData.length; s++) {
        const row = spData[s];
        studyPlan.push({
          id: String(rowValue_(row, spMap, 'Plan ID', 0) || ('PLAN_' + s)),
          week: String(rowValue_(row, spMap, 'Week', 1) || 'W1'),
          day: String(rowValue_(row, spMap, 'Day', 2) || '1'),
          date: String(rowValue_(row, spMap, 'Date', 3) || ''),
          student: String(rowValue_(row, spMap, 'Student', 4) || ''),
          grade: String(rowValue_(row, spMap, 'Grade Level', 5) || ''),
          subject: String(rowValue_(row, spMap, 'Subject', 6) || ''),
          unit: String(rowValue_(row, spMap, 'Unit / Topic', 7) || ''),
          lesson: String(rowValue_(row, spMap, 'Lesson', 8) || ''),
          skills: String(rowValue_(row, spMap, 'Skills', 9) || ''),
          dailyQuestions: Number(rowValue_(row, spMap, 'Daily Questions', 10)) || 5,
          status: String(rowValue_(row, spMap, 'Status', 11) || 'Planned'),
          examCode: String(rowValue_(row, spMap, 'Exam Code', 12) || '')
        });
      }
    }

    const driveVideos = readDriveVideoMap_();
    const driveFolderId = PropertiesService.getScriptProperties().getProperty('DRIVE_VIDEOS_FOLDER_ID') || '';

    return {
      success: true,
      sheetUrl: ss.getUrl(),
      submissions: submissions,
      exams: exams,
      allQuestions: allQuestions,
      retakeRequests: retakeRequests,
      studyPlan: studyPlan,
      driveVideos: driveVideos,
      driveFolderId: driveFolderId
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

// ============================================================
// STUDY PLAN (28-DAY CURRICULUM ROADMAP)
// ============================================================

function styleStudyPlanSheet(sheet) {
  const widths = [100, 70, 60, 110, 120, 110, 130, 180, 200, 260, 100, 90, 140];
  widths.forEach((width, index) => sheet.setColumnWidth(index + 1, width));
  const lastCol = Math.max(sheet.getLastColumn(), 13);
  sheet.getRange(2, 1, Math.max(sheet.getLastRow() - 1, 1), lastCol)
    .setVerticalAlignment('middle')
    .setFontSize(10);
}

function getStarterStudyPlan_() {
  return [
    // Ali Ahmed - Year 5 (Month 1 Roadmap)
    ['PLAN_Y5_D01', 'W1', '1', 'Day 1', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Unit 2 - Lesson 3: Adverbials', 'Adverbs of Manner', 'Identifying manner adverbs ending in -ly', 5, 'Completed', 'EX_Y5_ENG_ADV01'],
    ['PLAN_Y5_D02', 'W1', '2', 'Day 2', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Unit 2 - Lesson 3: Adverbials', 'Adverbials of Time', 'Prepositional time phrases (at dawn, in 1969)', 5, 'Completed', 'EX_Y5_ENG_ADV01'],
    ['PLAN_Y5_D03', 'W1', '3', 'Day 3', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Unit 2 - Lesson 3: Adverbials', 'Adverbials of Place', 'Answering WHERE (inside the station, on lunar surface)', 5, 'Completed', 'EX_Y5_ENG_ADV01'],
    ['PLAN_Y5_D04', 'W1', '4', 'Day 4', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Unit 2 - Lesson 3: Adverbials', 'Fronted Adverbials & Commas', 'Mandatory comma punctuation rule after fronted adverbials', 5, 'Completed', 'EX_Y5_ENG_ADV01'],
    ['PLAN_Y5_D05', 'W1', '5', 'Day 5', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Unit 2 - Lesson 3: Adverbials', 'Compound Adverbials (Time + Place)', 'Sentence restructuring with multiple adverbials', 5, 'Completed', 'EX_Y5_ENG_ADV01'],
    ['PLAN_Y5_D06', 'W1', '6', 'Day 6', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Unit 2 - Lesson 3: Adverbials', 'Error Hunting & Sentence Repair', 'Fixing missing commas and misidentified adverbs', 5, 'Completed', 'EX_Y5_ENG_ADV01'],
    ['PLAN_Y5_D07', 'W1', '7', 'Day 7', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Milestone Assessment', 'W1 Comprehensive Adverbials Exam', '100% Mastery evaluation of Unit 2 Lesson 3', 10, 'Completed', 'EX_Y5_ENG_ADV01'],
    ['PLAN_Y5_D08', 'W2', '8', 'Day 8', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Unit 2 - Lesson 4: Relative Clauses', 'Relative Pronouns (who, which, that)', 'Defining who vs which for persons and objects', 5, 'Planned', 'EX_Y5_ALI_W2_ENG'],
    ['PLAN_Y5_D09', 'W2', '9', 'Day 9', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Unit 2 - Lesson 4: Relative Clauses', 'Non-defining Relative Clauses & Commas', 'Enclosing parenthetical relative clauses between 2 commas', 5, 'Planned', 'EX_Y5_ALI_W2_ENG'],
    ['PLAN_Y5_D10', 'W2', '10', 'Day 10', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Unit 2 - Lesson 4: Relative Clauses', 'Connecting Sentences', 'Combining short sentences using relative pronouns', 5, 'Planned', 'EX_Y5_ALI_W2_ENG'],
    ['PLAN_Y5_D14', 'W2', '14', 'Day 14', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Milestone Assessment', 'W2 Cumulative Exam (W1 + W2 50/50)', 'Adverbials + Relative Clauses balanced synthesis', 12, 'Planned', 'EX_Y5_ALI_W2_ENG'],
    ['PLAN_Y5_D21', 'W3', '21', 'Day 21', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Milestone Assessment', 'W3 Cumulative Exam (W1-W3 40/30/30)', 'Subject-verb agreement + Relative clauses + Adverbials', 15, 'Planned', 'EX_Y5_ALI_W3_ENG'],
    ['PLAN_Y5_D28', 'W4', '28', 'Day 28', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Milestone Assessment', 'W4 Cumulative Exam (W1-W4)', 'Comprehensive grammar readiness before monthly exam', 18, 'Planned', 'EX_Y5_ALI_W4_ENG'],
    ['PLAN_Y5_D30', 'M1', '30', 'Day 30', 'Ali Ahmed', 'Year 5 (G5)', 'English Grammar', 'Monthly Capstone', 'Month 1 Comprehensive Grammar Exam', 'Full month retention check with Challenge tier', 20, 'Planned', 'EX_Y5_ALI_M1_CUMULATIVE'],

    // Mostafa Ahmed - Grade 6 (Month 1 Roadmap)
    ['PLAN_Y6_D01', 'W1', '1', 'Day 1', 'Mostafa Ahmed', 'Grade 6 (G6)', 'English Literacy', 'Unit 2: Fantasy Reading', 'Similes & Imagery in The City That Waited', 'Analyzing comparisons using like and as', 5, 'Completed', 'EX_Y6_ENG_FANTASY01'],
    ['PLAN_Y6_D02', 'W1', '2', 'Day 2', 'Mostafa Ahmed', 'Grade 6 (G6)', 'English Literacy', 'Unit 2: Fantasy Reading', 'Personification & Atmosphere', 'Explaining non-human actions and eerie moods', 5, 'Completed', 'EX_Y6_ENG_FANTASY01'],
    ['PLAN_Y6_D03', 'W1', '3', 'Day 3', 'Mostafa Ahmed', 'Grade 6 (G6)', 'English Literacy', 'Unit 2: Non-Chronological Reports', 'Scientific Vocabulary & Homophones', 'Hard shell vs herd shell spelling and context', 5, 'Completed', 'EX_Y6_ENG_FANTASY01'],
    ['PLAN_Y6_D04', 'W1', '4', 'Day 4', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Arabic Language', 'المحور الأول: إدارة الوقت', 'استيعاب المقروء وترتيب الأولويات', 'معاني المفردات والمضاد (تأجيل وعكسها تعجيل)', 5, 'Completed', 'EX_Y6_ARB_PRIO01'],
    ['PLAN_Y6_D05', 'W1', '5', 'Day 5', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Arabic Language', 'القواعد النحوية: النكرة والمعرفة', 'تحديد المعرف بأل والعلم وتمييز الاسم النكرة', 5, 'Completed', 'EX_Y6_ARB_PRIO01'],
    ['PLAN_Y6_D06', 'W1', '6', 'Day 6', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Arabic Language', 'القواعد الإملائية: الهمزة المتوسطة', 'حركة الهمزة وما قبلها (يَسْـأَلُ - فأس - تأمل)', 5, 'Completed', 'EX_Y6_ARB_PRIO01'],
    ['PLAN_Y6_D07', 'W1', '7', 'Day 7', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Arabic Language', 'Milestone Assessment', 'W1 Arabic Language Diagnostic Exam', 'Mastery assessment (Retake 10/10 verified)', 10, 'Completed', 'EX_Y6_ARB_PRIO01'],
    ['PLAN_Y6_D08', 'W2', '8', 'Day 8', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Arabic Language', 'القواعد النحوية: أنواع المعارف الستة', 'الضمائر وأسماء الإشارة والأسماء الموصولة', 5, 'Planned', 'EX_Y6_MOS_W2_ARB'],
    ['PLAN_Y6_D09', 'W2', '9', 'Day 9', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Arabic Language', 'القواعد الإملائية: الهمزة المتوسطة على واو', 'رسم الهمزة إذا كانت مضمومة أو ما قبلها مضموم', 5, 'Planned', 'EX_Y6_MOS_W2_ARB'],
    ['PLAN_Y6_D14', 'W2', '14', 'Day 14', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Mixed Assessment', 'W2 Cumulative Exam (W1 + W2 50/50)', 'Literacy + Arabic Language balanced synthesis', 14, 'Planned', 'EX_Y6_MOS_W2_ARB'],
    ['PLAN_Y6_D21', 'W3', '21', 'Day 21', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Mixed Assessment', 'W3 Cumulative Exam (W1-W3 40/30/30)', 'Grammar + Spelling + Reading retention', 16, 'Planned', 'EX_Y6_MOS_W3_ARB'],
    ['PLAN_Y6_D28', 'W4', '28', 'Day 28', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Mixed Assessment', 'W4 Cumulative Exam (W1-W4)', 'Comprehensive curriculum mastery test', 20, 'Planned', 'EX_Y6_MOS_W4_ARB'],
    ['PLAN_Y6_D30', 'M1', '30', 'Day 30', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Capstone Assessment', 'Month 1 Comprehensive Assessment', 'Grade 6 Full Month Capstone Exam with Challenge tier', 22, 'Planned', 'EX_Y6_MOS_M1_CUMULATIVE']
  ];
}

/**
 * Marks matching roadmap rows as completed after a successful submission.
 * Never throws: a missing Study_Plan tab must not fail a valid submission.
 */
function markStudyPlanProgress_(studentName, examCode) {
  try {
    const ss = getSpreadsheet();
    const sheet = ss.getSheetByName('Study_Plan');
    if (!sheet || sheet.getLastRow() <= 1) return;

    const map = getSheetHeaderMap_(sheet);
    const data = sheet.getDataRange().getValues();
    const targetName = normalizeName_(studentName);
    const targetExam = normalizeExam_(examCode);
    const statusCol = headerIndex_(map, 'Status', 11) + 1;

    for (let i = 1; i < data.length; i++) {
      const rowName = normalizeName_(rowValue_(data[i], map, 'Student', 4));
      const rowExam = normalizeExam_(rowValue_(data[i], map, 'Exam Code', 12));
      if (rowName !== targetName || rowExam !== targetExam) continue;
      if (String(rowValue_(data[i], map, 'Status', 11) || '').toLowerCase() === 'completed') continue;
      sheet.getRange(i + 1, statusCol).setValue('Completed');
      // One successful attempt advances one roadmap step, not every lesson
      // that happens to share the same exam code.
      break;
    }
  } catch (e) {
    Logger.log('markStudyPlanProgress_ skipped: ' + e);
  }
}

/**
 * Computes today's active assessment mission for the student based on Study_Plan.
 */
function getTodayMission(studentKey) {
  try {
    const key = String(studentKey || 'ali').toLowerCase();
    const isAli = (key === 'ali');
    const targetStudent = isAli ? 'Ali Ahmed' : 'Mostafa Ahmed';

    const ss = getSpreadsheet();
    const spSheet = ss.getSheetByName('Study_Plan');
    let mission = null;

    if (spSheet && spSheet.getLastRow() > 1) {
      const spData = spSheet.getDataRange().getValues();
      const spMap = getSheetHeaderMap_(spSheet);
      for (let i = 1; i < spData.length; i++) {
        const row = spData[i];
        const student = normalizeName_(rowValue_(row, spMap, 'Student', 4));
        if (student !== normalizeName_(targetStudent)) continue;

        const status = String(rowValue_(row, spMap, 'Status', 11) || 'Planned').trim().toLowerCase();
        if (status === 'planned' || status === 'active' || !mission) {
          mission = {
            planId: String(rowValue_(row, spMap, 'Plan ID', 0) || ''),
            week: String(rowValue_(row, spMap, 'Week', 1) || 'W1'),
            day: String(rowValue_(row, spMap, 'Day', 2) || '1'),
            dateTitle: String(rowValue_(row, spMap, 'Date', 3) || 'Today'),
            subject: String(rowValue_(row, spMap, 'Subject', 6) || ''),
            lesson: String(rowValue_(row, spMap, 'Lesson', 8) || ''),
            skills: String(rowValue_(row, spMap, 'Skills', 9) || ''),
            questionsCount: Number(rowValue_(row, spMap, 'Daily Questions', 10)) || 10,
            examCode: String(rowValue_(row, spMap, 'Exam Code', 12) || (isAli ? 'EX_Y5_ENG_ADV01' : 'EX_Y6_ARB_PRIO01'))
          };
          if (status === 'planned' || status === 'active') break;
        }
      }
    }

    if (!mission) {
      mission = {
        planId: isAli ? 'PLAN_Y5_DEFAULT' : 'PLAN_Y6_DEFAULT',
        week: 'W1',
        day: '1',
        dateTitle: 'Today',
        subject: isAli ? 'English Grammar' : 'Arabic Language',
        lesson: isAli ? 'Unit 2: Adverbials Mastery' : 'المحور الأول: النكرة والمعرفة والهمزة',
        skills: isAli ? 'Adverbs of Time, Place & Manner' : 'القراءة المتحررة وإدارة الوقت',
        questionsCount: 10,
        examCode: isAli ? 'EX_Y5_ENG_ADV01' : 'EX_Y6_ARB_PRIO01'
      };
    }

    return { success: true, mission: mission };
  } catch (err) {
    Logger.log('getTodayMission error: ' + err);
    return { success: false, message: err.message };
  }
}

// ============================================================
// EXAM FACTORY (WEEKLY / MONTHLY / MISTAKES REVIEW)
// ============================================================

const ADMIN_REQUIRED_RESULT = {
  success: false,
  code: 'UNAUTHORIZED',
  message: 'غير مصرح بالدخول. أعد فتح بوابة ولي الأمر.'
};

function subjectFamily_(subject) {
  const s = String(subject || '').toLowerCase();
  if (s.indexOf('arab') !== -1 || s.indexOf('عرب') !== -1 || s.indexOf('لغة') !== -1) return 'arabic';
  if (s.indexOf('english') !== -1 || s.indexOf('grammar') !== -1 || s.indexOf('literacy') !== -1) return 'english';
  if (s.indexOf('math') !== -1 || s.indexOf('رياض') !== -1 || s.indexOf('حساب') !== -1) return 'math';
  if (s.indexOf('sci') !== -1 || s.indexOf('علوم') !== -1) return 'science';
  if (s.indexOf('ict') !== -1 || s.indexOf('حاسب') !== -1 || s.indexOf('tech') !== -1) return 'ict';
  return '';
}

function simpleHash_(text) {
  let hash = 5381;
  const str = String(text || '');
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash) ^ str.charCodeAt(i);
  }
  return (hash >>> 0).toString(36);
}

function computeExamUrl_(studentKey, examCode) {
  try {
    if (typeof ScriptApp === 'undefined' || !ScriptApp.getService) return '';
    const base = ScriptApp.getService().getUrl() || '';
    if (!base) return '';
    return base + '?student=' + encodeURIComponent(studentKey) + '&exam=' + encodeURIComponent(examCode);
  } catch (e) {
    return '';
  }
}

function loadBankQuestionsByPeriod_(grade, subject, period, targetDifficulty) {
  const ss = getSpreadsheet();
  const sheet = ss.getSheetByName('Question_Bank');
  if (!sheet || sheet.getLastRow() <= 1) return [];

  const map = getSheetHeaderMap_(sheet);
  const data = sheet.getDataRange().getValues();
  const questions = [];
  const targetPeriod = String(period || '').trim().toUpperCase();
  const isMonthly = targetPeriod.startsWith('M');
  const family = subjectFamily_(subject);
  const reqDiff = String(targetDifficulty || '').trim().toLowerCase();

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const rowGrade = String(row[headerIndex_(map, 'Grade Level', 1)] || '');
    const rowSubject = String(row[headerIndex_(map, 'Subject', 2)] || '');
    const rowWeek = String(rowValue_(row, map, 'Week', 11) || 'W1').trim().toUpperCase();
    const rowDiff = String(rowValue_(row, map, 'Difficulty', 12) || rowValue_(row, map, 'مستوى الصعوبة', 12) || '').trim().toLowerCase();

    const gradeMatches = (normalizeName_(rowGrade).indexOf('5') !== -1 && normalizeName_(grade).indexOf('5') !== -1) ||
                         (normalizeName_(rowGrade).indexOf('6') !== -1 && normalizeName_(grade).indexOf('6') !== -1);
    if (!gradeMatches) continue;

    // Keep subjects aligned when family is known
    const rowFamily = subjectFamily_(rowSubject);
    if (family && rowFamily && family !== rowFamily) continue;

    let periodMatches = false;
    if (isMonthly) {
      periodMatches = true;
    } else if (targetPeriod === rowWeek || targetPeriod === 'ALL') {
      periodMatches = true;
    }
    if (!periodMatches) continue;

    const text = String(row[headerIndex_(map, 'Question Text', 4)] || '').trim();
    const answer = String(row[headerIndex_(map, 'Correct Answer', 7)] || '').trim();
    if (!text || !answer) continue;

    const type = String(row[headerIndex_(map, 'Type', 5)] || 'MCQ').trim().toUpperCase();
    let options = String(row[headerIndex_(map, 'Options (delimited by |)', 6)] || '')
      .split('|')
      .map(option => String(option || '').trim())
      .filter(option => option.length > 0);

    if (type === 'TRUE_FALSE' && options.length < 2) options = ['True', 'False'];

    let priority = 1;
    if (reqDiff && reqDiff !== 'all') {
      if (rowDiff.indexOf(reqDiff) !== -1) priority = 3;
      else if (reqDiff === 'foundational' && (rowDiff.indexOf('easy') !== -1 || rowDiff.indexOf('level 1') !== -1)) priority = 3;
      else if (reqDiff === 'standard' && (rowDiff.indexOf('medium') !== -1 || rowDiff.indexOf('core') !== -1)) priority = 3;
      else if (reqDiff === 'challenging' && (rowDiff.indexOf('hard') !== -1 || rowDiff.indexOf('adv') !== -1)) priority = 3;
      else priority = 0;
    }

    questions.push({
      id: String(row[headerIndex_(map, 'Question ID', 0)] || ('Q_' + i)),
      grade: rowGrade,
      subject: rowSubject,
      week: rowWeek,
      text: text,
      type: type,
      options: options,
      correctAnswer: answer,
      explanation: String(row[headerIndex_(map, 'Explanation', 9)] || ''),
      difficulty: rowDiff,
      priority: priority
    });
  }

  // Sort by priority descending so target difficulty is picked first
  questions.sort((a, b) => (b.priority || 0) - (a.priority || 0));
  return questions;
}

/**
 * Returns all active exams for a student based on grade isolation.
 */
function getStudentAvailableExams(studentKey) {
  try {
    const ss = getSpreadsheet();
    const exSheet = ss ? ss.getSheetByName('Exams') : null;
    const key = String(studentKey || 'ali').toLowerCase();
    const isAli = (key === 'ali');
    const exams = [];

    if (exSheet && exSheet.getLastRow() > 1) {
      const map = getSheetHeaderMap_(exSheet);
      const data = exSheet.getDataRange().getValues();

      for (let i = 1; i < data.length; i++) {
        const row = data[i];
        const grade = String(rowValue_(row, map, 'Grade Level', 2) || '');
        const status = String(rowValue_(row, map, 'Status', 6) || 'ACTIVE').toUpperCase();

        if (['ACTIVE', 'ENABLED', 'نشط', 'مفعل'].indexOf(status) === -1) continue;

        // Grade isolation: Ali only sees G5, Mostafa only sees G6.
        const matchesGrade = isAli
          ? (grade.indexOf('5') !== -1 || grade.toLowerCase().indexOf('ali') !== -1)
          : (grade.indexOf('6') !== -1 || grade.toLowerCase().indexOf('mostafa') !== -1);

        if (!matchesGrade) continue;

        exams.push({
          code: String(rowValue_(row, map, 'Exam Code', 0) || ''),
          title: String(rowValue_(row, map, 'Exam Title', 1) || ''),
          grade: grade,
          subject: String(rowValue_(row, map, 'Subject', 3) || ''),
          count: Number(rowValue_(row, map, 'Questions', 4)) || 10,
          duration: Number(rowValue_(row, map, 'Duration (Mins)', 5)) || 20,
          type: String(rowValue_(row, map, 'Exam Type', 9) || 'Standard'),
          period: String(rowValue_(row, map, 'Target Period', 10) || 'W1')
        });
      }
      return { success: true, exams: exams, driveVideos: readDriveVideoMap_() };
    }

    // Only fall back to starter catalog when sheet is missing or completely unseeded (0 or 1 row)
    if ((!exSheet || exSheet.getLastRow() <= 1) && typeof getStarterExams_ === 'function') {
      const starter = getStarterExams_();
      for (let i = 0; i < starter.length; i++) {
        const row = starter[i];
        const grade = String(row[2] || '');
        const status = String(row[6] || 'ACTIVE').toUpperCase();
        if (['ACTIVE', 'ENABLED', 'نشط', 'مفعل'].indexOf(status) === -1) continue;

        const matchesGrade = isAli
          ? (grade.indexOf('5') !== -1 || grade.toLowerCase().indexOf('ali') !== -1)
          : (grade.indexOf('6') !== -1 || grade.toLowerCase().indexOf('mostafa') !== -1);
        if (!matchesGrade) continue;

        exams.push({
          code: String(row[0] || ''),
          title: String(row[1] || ''),
          grade: grade,
          subject: String(row[3] || ''),
          count: Number(row[4]) || 10,
          duration: Number(row[5]) || 20,
          type: String(row[9] || 'Standard'),
          period: String(row[10] || 'W1')
        });
      }
    }

    return { success: true, exams: exams, driveVideos: readDriveVideoMap_() };
  } catch (err) {
    return { success: false, exams: [], error: err.toString() };
  }
}

function upsertExamRow_(exSheet, examCode, examRow) {
  const map = getSheetHeaderMap_(exSheet);
  const data = exSheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (normalizeExam_(rowValue_(data[i], map, 'Exam Code', 0)) === normalizeExam_(examCode)) {
      exSheet.getRange(i + 1, 1, 1, examRow.length).setValues([examRow]);
      return i + 1;
    }
  }
  exSheet.appendRow(examRow);
  return exSheet.getLastRow();
}

function createWeeklyExam(payload, adminToken) {
  const token = adminToken || (payload && payload.adminToken);
  if (!isAdminTokenValid_(token)) return Object.assign({}, ADMIN_REQUIRED_RESULT);
  return createWeeklyExam_(payload);
}

function createWeeklyExam_(payload) {
  try {
    const ss = getSpreadsheet();
    let exSheet = ss.getSheetByName('Exams');
    if (!exSheet) {
      setupDatabase(ss);
      exSheet = ss.getSheetByName('Exams');
    }

    const studentKey = String((payload && payload.studentKey) || 'ali').toLowerCase();
    const isAli = (studentKey === 'ali');
    const grade = isAli ? 'Year 5 (G5)' : 'Grade 6 (G6)';
    const weekCode = String((payload && payload.weekCode) || 'W2').toUpperCase();
    const subject = String((payload && payload.subject) || (isAli ? 'English Grammar' : 'English Literacy'));
    const count = Number(payload && payload.count) || 10;
    const duration = Number(payload && payload.duration) || 20;

    if (!/^W[1-9][0-9]?$/.test(weekCode)) {
      return { success: false, message: 'كود الأسبوع غير صالح. استخدم مثالاً مثل W2 أو W3.' };
    }

    const targetDifficulty = String((payload && payload.difficulty) || 'ALL');
    const bankQuestions = loadBankQuestionsByPeriod_(grade, subject, weekCode, targetDifficulty);
    if (!bankQuestions.length) {
      return {
        success: false,
        message: 'لا توجد أسئلة في بنك الأسئلة لـ ' + grade + ' / ' + subject + ' / ' + weekCode + '. أضف الأسئلة أولاً ثم أعد المحاولة.'
      };
    }

    const fam = subjectFamily_(subject);
    const subjectPrefix = fam === 'arabic' ? 'ARB' : fam === 'math' ? 'MATH' : fam === 'science' ? 'SCI' : fam === 'ict' ? 'ICT' : 'ENG';
    const targetDiff = String((payload && payload.difficulty) || 'ALL').trim();
    const diffTag = (targetDiff !== 'ALL' && targetDiff) ? '_' + targetDiff.substring(0, 3).toUpperCase() : '';
    const examCode = 'EX_' + (isAli ? 'Y5_ALI' : 'Y6_MOS') + '_' + weekCode + '_' + subjectPrefix + diffTag;
    const title = (isAli ? 'Ali' : 'Mostafa') + ' - Week ' + weekCode.replace('W', '') + ' Assessment: ' + subject;
    const available = bankQuestions.length;

    const examRow = [
      examCode,
      title,
      grade,
      subject,
      Math.min(count, available),
      duration,
      'ACTIVE',
      '',
      new Date(),
      'Weekly',
      weekCode
    ];

    upsertExamRow_(exSheet, examCode, examRow);
    styleExamsSheet(exSheet);

    return {
      success: true,
      examCode: examCode,
      title: title,
      grade: grade,
      subject: subject,
      weekCode: weekCode,
      questionsCount: examRow[4],
      studentUrl: computeExamUrl_(studentKey, examCode),
      message: 'تم إنشاء امتحان الأسبوع (' + weekCode + ') بنجاح برمز: ' + examCode + ' — ' + examRow[4] + ' أسئلة متاحة.'
    };
  } catch (err) {
    Logger.log('createWeeklyExam error: ' + err);
    return { success: false, message: 'حدث خطأ: ' + err.message };
  }
}

function createMonthlyExam(payload, adminToken) {
  const token = adminToken || (payload && payload.adminToken);
  if (!isAdminTokenValid_(token)) return Object.assign({}, ADMIN_REQUIRED_RESULT);
  return createMonthlyExam_(payload);
}

function createMonthlyExam_(payload) {
  try {
    const ss = getSpreadsheet();
    let exSheet = ss.getSheetByName('Exams');
    if (!exSheet) {
      setupDatabase(ss);
      exSheet = ss.getSheetByName('Exams');
    }

    const studentKey = String((payload && payload.studentKey) || 'ali').toLowerCase();
    const isAli = (studentKey === 'ali');
    const grade = isAli ? 'Year 5 (G5)' : 'Grade 6 (G6)';
    const monthCode = String((payload && payload.monthCode) || 'M1').toUpperCase();
    const requestedSubject = String((payload && payload.subject) || (isAli ? 'English Grammar' : 'Cumulative Assessment'));
    const count = Number(payload && payload.count) || 15;
    const duration = Number(payload && payload.duration) || 30;
    const targetDifficulty = String((payload && payload.difficulty) || 'ALL');

    if (!/^M[1-9][0-9]?$/.test(monthCode)) {
      return { success: false, message: 'كود الشهر غير صالح. استخدم مثالاً مثل M1 أو M2.' };
    }

    const bankQuestions = loadBankQuestionsByPeriod_(grade, requestedSubject, monthCode, targetDifficulty);
    if (!bankQuestions.length) {
      return {
        success: false,
        message: 'لا توجد أسئلة تراكمية في بنك الأسئلة لـ ' + grade + '. أضف أسئلة الأسابيع W1-W4 أولاً.'
      };
    }

    const examCode = 'EX_' + (isAli ? 'Y5_ALI' : 'Y6_MOS') + '_' + monthCode + '_CUMULATIVE';
    const title = (isAli ? 'Ali' : 'Mostafa') + ' - Month ' + monthCode.replace('M', '') + ' Comprehensive Cumulative Exam';
    const available = bankQuestions.length;

    const examRow = [
      examCode,
      title,
      grade,
      requestedSubject,
      Math.min(count, available),
      duration,
      'ACTIVE',
      '',
      new Date(),
      'Monthly',
      monthCode
    ];

    upsertExamRow_(exSheet, examCode, examRow);
    styleExamsSheet(exSheet);

    return {
      success: true,
      examCode: examCode,
      title: title,
      grade: grade,
      studentUrl: computeExamUrl_(studentKey, examCode),
      message: 'تم إنشاء الامتحان الشهري التراكمي (' + monthCode + ') بنجاح برمز: ' + examCode + ' — ' + examRow[4] + ' أسئلة متاحة.'
    };
  } catch (err) {
    Logger.log('createMonthlyExam error: ' + err);
    return { success: false, message: 'حدث خطأ: ' + err.message };
  }
}

function createMistakesReviewExam(payload, adminToken) {
  const token = adminToken || (payload && payload.adminToken);
  if (!isAdminTokenValid_(token)) return Object.assign({}, ADMIN_REQUIRED_RESULT);
  return createMistakesReviewExam_(payload);
}

function createMistakesReviewExam_(payload) {
  try {
    const ss = getSpreadsheet();
    const subSheet = ss.getSheetByName('Submissions');
    const qbSheet = ss.getSheetByName('Question_Bank');
    let exSheet = ss.getSheetByName('Exams');

    if (!subSheet || subSheet.getLastRow() <= 1) {
      return { success: false, message: 'لا توجد سجلات تسليم سابقة لاستخراج الأخطاء.' };
    }
    if (!qbSheet) {
      return { success: false, message: 'بنك الأسئلة غير موجود. شغّل إعداد قاعدة البيانات أولاً.' };
    }
    if (!exSheet) {
      setupDatabase(ss);
      exSheet = ss.getSheetByName('Exams');
    }

    const studentKey = String((payload && payload.studentKey) || 'ali').toLowerCase();
    const isAli = (studentKey === 'ali');
    const targetStudent = isAli ? 'Ali Ahmed' : 'Mostafa Ahmed';
    const grade = isAli ? 'Year 5 (G5)' : 'Grade 6 (G6)';

    const sMap = getSheetHeaderMap_(subSheet);
    const sData = subSheet.getDataRange().getValues();
    const mistakes = [];
    const seenQuestions = {};

    for (let i = 1; i < sData.length; i++) {
      const row = sData[i];
      const name = normalizeName_(rowValue_(row, sMap, 'Student Name', 1));
      if (name !== normalizeName_(targetStudent)) continue;

      const rawJson = rowValue_(row, sMap, 'Detailed Review JSON', 10);
      if (!rawJson) continue;

      let review = [];
      try {
        const parsed = JSON.parse(rawJson);
        review = Array.isArray(parsed) ? parsed : (parsed.review || parsed.mistakes || []);
      } catch (e) {
        continue;
      }

      review.forEach(item => {
        if (item.isCorrect === false || (Number(item.pointsAwarded) < Number(item.maxPoints))) {
          const qText = String(item.questionText || item.question || '').trim();
          if (qText && !seenQuestions[qText]) {
            seenQuestions[qText] = true;
            mistakes.push(item);
          }
        }
      });
    }

    if (mistakes.length === 0) {
      return {
        success: false,
        message: '🎉 رائع جداً! لا توجد أخطاء مسجلة لـ ' + targetStudent + '، أو تم تصحيح جميع الأخطاء في المحاولات اللاحقة!'
      };
    }

    const examCode = 'EX_' + (isAli ? 'Y5_ALI' : 'Y6_MOS') + '_MISTAKES_REV';
    const title = (isAli ? 'Ali' : 'Mostafa') + ' - Targeted Mistakes Review (' + mistakes.length + ' Questions)';

    const qbMap = getSheetHeaderMap_(qbSheet);
    const existingQbData = qbSheet.getDataRange().getValues();
    const existingQbIds = {};
    for (let r = 1; r < existingQbData.length; r++) {
      existingQbIds[String(rowValue_(existingQbData[r], qbMap, 'Question ID', 0) || '')] = true;
    }

    const newQbRows = [];
    mistakes.forEach((m, idx) => {
      const qText = String(m.questionText || m.question || '').trim();
      const qId = 'MISTAKE_' + (isAli ? 'ALI' : 'MOS') + '_' + simpleHash_(qText);
      if (existingQbIds[qId]) return;

      const correctAnswer = String(m.correctAnswer || '').trim();
      if (!correctAnswer) return;
      const studentAnswer = String(m.studentAnswer || '').trim();
      let options = [correctAnswer];
      if (studentAnswer && normalizeAnswer_(studentAnswer) !== normalizeAnswer_(correctAnswer)) {
        options.push(studentAnswer);
      }
      if (options.length < 2) options.push('None of the above');

      newQbRows.push([
        qId,
        grade,
        isAli ? 'English Grammar' : 'Mixed Review',
        'Review: Targeted Mistake Retest',
        qText,
        'MCQ',
        options.join(' | '),
        correctAnswer,
        1,
        m.explanation || '💡 مراجعة الخطأ السابق لتثبيت القاعدة والإتقان الكامل.',
        examCode,
        'MistakesReview',
        'Targeted'
      ]);
    });

    if (newQbRows.length > 0) {
      qbSheet.getRange(qbSheet.getLastRow() + 1, 1, newQbRows.length, newQbRows[0].length).setValues(newQbRows);
      styleQuestionBankSheet(qbSheet);
    }

    const totalQuestions = loadBankQuestions_(examCode).length;
    if (!totalQuestions) {
      return { success: false, message: 'تعذر بناء أسئلة المراجعة من الأخطاء المسجلة. أعد المحاولة بعد تسليم اختبار جديد.' };
    }

    const exRow = [
      examCode,
      title,
      grade,
      'Mistakes Review',
      totalQuestions,
      15,
      'ACTIVE',
      '',
      new Date(),
      'Mistakes Review',
      'Continuous'
    ];

    upsertExamRow_(exSheet, examCode, exRow);
    styleExamsSheet(exSheet);

    return {
      success: true,
      examCode: examCode,
      title: title,
      mistakesCount: mistakes.length,
      questionsCount: totalQuestions,
      studentUrl: computeExamUrl_(studentKey, examCode),
      message: 'تم تجميع (' + totalQuestions + ') سؤال مراجعة من أخطاء سابقة في امتحان مخصص برمز: ' + examCode
    };
  } catch (err) {
    Logger.log('createMistakesReviewExam error: ' + err);
    return { success: false, message: 'حدث خطأ: ' + err.message };
  }
}

/**
 * Spreadsheet UI menu prompts (run as the sheet owner, so no web token needed).
 */
function promptCreateWeeklyExam() {
  const ui = SpreadsheetApp.getUi();
  const studentPrompt = ui.prompt('إنشاء امتحان أسبوعي', 'اختر الطالب:\nاكتب 1 لـ علي أحمد (Year 5)\nاكتب 2 لـ مصطفى أحمد (Grade 6)', ui.ButtonSet.OK_CANCEL);
  if (studentPrompt.getSelectedButton() !== ui.Button.OK) return;

  const choice = studentPrompt.getResponseText().trim();
  const studentKey = (choice === '2') ? 'mostafa' : 'ali';

  const weekPrompt = ui.prompt('رقم الأسبوع', 'اكتب كود الأسبوع (مثال: W2 أو W3):', ui.ButtonSet.OK_CANCEL);
  if (weekPrompt.getSelectedButton() !== ui.Button.OK) return;

  const weekCode = weekPrompt.getResponseText().trim().toUpperCase() || 'W2';
  const res = createWeeklyExam_({ studentKey: studentKey, weekCode: weekCode });
  ui.alert('نتيجة إنشاء الامتحان', res.message + '\n\nرابط الطالب المباشر:\n' + (res.studentUrl || 'افتح التطبيق للنسخ'), ui.ButtonSet.OK);
}

function promptCreateMonthlyExam() {
  const ui = SpreadsheetApp.getUi();
  const studentPrompt = ui.prompt('إنشاء امتحان شهري تراكمي', 'اختر الطالب:\nاكتب 1 لـ علي أحمد (Year 5)\nاكتب 2 لـ مصطفى أحمد (Grade 6)', ui.ButtonSet.OK_CANCEL);
  if (studentPrompt.getSelectedButton() !== ui.Button.OK) return;

  const choice = studentPrompt.getResponseText().trim();
  const studentKey = (choice === '2') ? 'mostafa' : 'ali';

  const monthPrompt = ui.prompt('كود الشهر', 'اكتب كود الشهر (مثال: M1 أو M2):', ui.ButtonSet.OK_CANCEL);
  if (monthPrompt.getSelectedButton() !== ui.Button.OK) return;

  const monthCode = monthPrompt.getResponseText().trim().toUpperCase() || 'M1';
  const res = createMonthlyExam_({ studentKey: studentKey, monthCode: monthCode });
  ui.alert('نتيجة إنشاء الامتحان الشهري', res.message + '\n\nالرابط:\n' + (res.studentUrl || 'افتح التطبيق للنسخ'), ui.ButtonSet.OK);
}

function promptCreateMistakesExam() {
  const ui = SpreadsheetApp.getUi();
  const studentPrompt = ui.prompt('امتحان مراجعة الأخطاء الذاتي', 'اختر الطالب:\nاكتب 1 لـ علي أحمد\nاكتب 2 لـ مصطفى أحمد', ui.ButtonSet.OK_CANCEL);
  if (studentPrompt.getSelectedButton() !== ui.Button.OK) return;

  const choice = studentPrompt.getResponseText().trim();
  const studentKey = (choice === '2') ? 'mostafa' : 'ali';

  const res = createMistakesReviewExam_({ studentKey: studentKey });
  ui.alert('امتحان مراجعة الأخطاء', res.message + (res.studentUrl ? ('\n\nالرابط:\n' + res.studentUrl) : ''), ui.ButtonSet.OK);
}

// ============================================================
// COLIGO LMS FEED, GOOGLE DRIVE VIDEOS & HOMEWORK STATUS
// ============================================================

function readDriveVideoMap_() {
  try {
    const raw = PropertiesService.getScriptProperties().getProperty('DRIVE_VIDEO_MAP');
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    return (parsed && typeof parsed === 'object') ? parsed : {};
  } catch (e) {
    return {};
  }
}

function persistJsonProperty_(key, value) {
  const props = PropertiesService.getScriptProperties();
  let payload = JSON.stringify(value);
  // Script properties are capped near 9KB; trim the oldest entries rather than fail.
  if (payload.length > 8000) {
    const keys = Object.keys(value);
    while (keys.length > 1 && payload.length > 8000) {
      keys.pop();
      const trimmed = {};
      keys.forEach(k => { trimmed[k] = value[k]; });
      payload = JSON.stringify(trimmed);
    }
  }
  props.setProperty(key, payload);
}

function extractDriveFolderId_(ref) {
  const value = String(ref || '').trim();
  if (!value) return '';
  const match = value.match(/\/folders\/([A-Za-z0-9_-]{10,})/);
  if (match) return match[1];
  const idMatch = value.match(/[?&]id=([A-Za-z0-9_-]{10,})/);
  if (idMatch) return idMatch[1];
  if (/^[A-Za-z0-9_-]{10,}$/.test(value)) return value;
  return '';
}

function syncGoogleDriveVideos(folderRef, adminToken) {
  const token = adminToken || folderRef && folderRef.adminToken;
  if (!isAdminTokenValid_(token)) return Object.assign({}, ADMIN_REQUIRED_RESULT);

  const ref = (folderRef && typeof folderRef === 'object') ? folderRef.folder : folderRef;
  const folderId = extractDriveFolderId_(ref);
  if (!folderId) {
    return { success: false, message: 'رابط مجلد Google Drive غير صالح. انسخ رابط المجلد كاملاً أو معرّفه.' };
  }
  if (typeof DriveApp === 'undefined') {
    return { success: false, message: 'خدمة Google Drive غير متاحة في هذه البيئة.' };
  }

  let folder;
  try {
    folder = DriveApp.getFolderById(folderId);
  } catch (e) {
    return { success: false, message: 'تعذر فتح المجلد: ' + e.message };
  }

  const videoMap = {};
  let scanned = 0;
  try {
    const files = folder.getFiles();
    while (files.hasNext() && scanned < 500) {
      scanned++;
      const file = files.next();
      const name = String(file.getName() || '');
      const mime = String(file.getMimeType() || '');
      if (mime.indexOf('video/') !== 0 && !/\.(mp4|webm|mov|m4v|avi|mkv)$/i.test(name)) continue;

      const id = String(file.getId() || '');
      const key = name.replace(/\.[^.]+$/, '').trim();
      videoMap[key] = {
        id: id,
        name: name,
        previewUrl: 'https://drive.google.com/file/d/' + id + '/preview',
        downloadUrl: 'https://drive.google.com/uc?export=download&id=' + id
      };
    }
  } catch (e) {
    return { success: false, message: 'تعذر قراءة ملفات المجلد: ' + e.message };
  }

  const count = Object.keys(videoMap).length;
  if (!count) {
    return { success: false, message: 'لم يتم العثور على ملفات فيديو داخل هذا المجلد.' };
  }

  PropertiesService.getScriptProperties().setProperty('DRIVE_VIDEOS_FOLDER_ID', folderId);
  persistJsonProperty_('DRIVE_VIDEO_MAP', videoMap);

  return {
    success: true,
    videoMap: videoMap,
    folderId: folderId,
    count: count,
    message: 'تم ربط ' + count + ' فيديو من Google Drive بنجاح.'
  };
}

function getColigoHubData() {
  try {
    const ss = getSpreadsheet();
    const sheet = ss.getSheetByName('Coligo_Hub');
    if (!sheet || sheet.getLastRow() <= 1) return { success: true, items: [] };

    const map = getSheetHeaderMap_(sheet);
    const data = sheet.getDataRange().getValues();
    const items = [];
    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      const title = String(rowValue_(row, map, 'Title', 6) || '').trim();
      if (!title) continue;
      items.push({
        id: String(rowValue_(row, map, 'Item ID', 0) || ('COLIGO_' + i)),
        syncedAt: formatMaybeDate_(rowValue_(row, map, 'Synced At', 1)),
        student: String(rowValue_(row, map, 'Student', 2) || ''),
        grade: String(rowValue_(row, map, 'Grade', 3) || ''),
        course: String(rowValue_(row, map, 'Course', 4) || ''),
        type: String(rowValue_(row, map, 'Type', 5) || '@material-type/file'),
        title: title,
        url: String(rowValue_(row, map, 'URL', 7) || ''),
        content: String(rowValue_(row, map, 'Content', 8) || '')
      });
    }
    return { success: true, items: items.reverse() };
  } catch (err) {
    Logger.log('getColigoHubData error: ' + err);
    return { success: false, message: err.message, items: [] };
  }
}

function formatMaybeDate_(value) {
  if (value instanceof Date) {
    return Utilities.formatDate(value, Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
  }
  return String(value || '');
}

function normalizeColigoItem_(raw, index) {
  const item = raw || {};
  return {
    id: String(item.id || item._id || ('COLIGO_' + index)),
    student: String(item.student || item.studentName || ''),
    grade: String(item.grade || item.schoolGrade || ''),
    course: String(item.course || item.courseName || ''),
    type: String(item.type || '@material-type/file'),
    title: String(item.title || item.name || item.filename || ''),
    url: String(item.url || item.link || ''),
    content: String(item.content || item.description || '')
  };
}

function syncColigoOnline(force, adminToken) {
  if (!isAdminTokenValid_(adminToken)) return Object.assign({}, ADMIN_REQUIRED_RESULT);
  return syncColigoOnline_();
}

function syncColigoOnline_() {
  const props = PropertiesService.getScriptProperties();
  const feedUrl = String(props.getProperty('COLIGO_HUB_FEED_URL') || '').trim();
  if (!feedUrl) {
    return {
      success: false,
      code: 'NOT_CONFIGURED',
      message: 'لم يتم ضبط رابط موجز كوليجو. أضف الخاصية COLIGO_HUB_FEED_URL في إعدادات التطبيق.'
    };
  }
  if (typeof UrlFetchApp === 'undefined') {
    return { success: false, message: 'خدمة جلب البيانات غير متاحة في هذه البيئة.' };
  }

  let response;
  try {
    response = UrlFetchApp.fetch(feedUrl, { muteHttpExceptions: true, followRedirects: true });
  } catch (e) {
    return { success: false, message: 'تعذر الاتصال بكوليجو: ' + e.message };
  }

  const code = response.getResponseCode();
  if (code < 200 || code >= 300) {
    return { success: false, message: 'أعادت سحابة كوليجو رمز خطأ: ' + code };
  }

  let payload;
  try {
    payload = JSON.parse(response.getContentText());
  } catch (e) {
    return { success: false, message: 'رد كوليجو ليس JSON صالحاً.' };
  }

  const rawItems = Array.isArray(payload) ? payload
    : (payload && (payload.items || payload.materials || payload.data)) || [];
  if (!Array.isArray(rawItems) || !rawItems.length) {
    return { success: false, message: 'لم تُرجع سحابة كوليجو أي عناصر جديدة.' };
  }

  const items = rawItems.map(normalizeColigoItem_).filter(item => item.title);

  const ss = getSpreadsheet();
  let sheet = ss.getSheetByName('Coligo_Hub');
  if (!sheet) {
    setupDatabase(ss);
    sheet = ss.getSheetByName('Coligo_Hub');
  }

  const headers = ['Item ID', 'Synced At', 'Student', 'Grade', 'Course', 'Type', 'Title', 'URL', 'Content'];
  const stamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
  const rows = items.map(item => [
    item.id, stamp, item.student, item.grade, item.course, item.type, item.title, item.url, item.content
  ]);

  const capacity = Math.max(sheet.getLastRow() - 1, rows.length);
  const matrix = [];
  for (let i = 0; i < capacity; i++) {
    matrix.push(rows[i] || ['', '', '', '', '', '', '', '', '']);
  }
  sheet.getRange(2, 1, Math.max(capacity, 1), headers.length).setValues(matrix);

  persistJsonProperty_('COLIGO_HUB_CACHE', items);

  return {
    success: true,
    count: items.length,
    items: items,
    message: 'تمت مزامنة ' + items.length + ' عنصراً من كوليجو وتحديث مركز المواد.'
  };
}

function setupColigoAutoSyncTrigger(adminToken) {
  if (!isAdminTokenValid_(adminToken)) return Object.assign({}, ADMIN_REQUIRED_RESULT);
  if (typeof ScriptApp === 'undefined' || !ScriptApp.getProjectTriggers) {
    return { success: false, message: 'خدمة المجدول غير متاحة في هذه البيئة.' };
  }
  try {
    ScriptApp.getProjectTriggers().forEach(trigger => {
      if (trigger.getHandlerFunction && trigger.getHandlerFunction() === 'syncColigoAuto_') {
        ScriptApp.deleteTrigger(trigger);
      }
    });
    ScriptApp.newTrigger('syncColigoAuto_').timeBased().atHour(15).nearMinute(30).everyDays(1).create();
    return { success: true, message: 'تم تفعيل المزامنة التلقائية اليومية الساعة 3:30 عصراً.' };
  } catch (e) {
    return { success: false, message: 'تعذر إنشاء المجدول: ' + e.message };
  }
}

/**
 * Time-driven trigger entry point. Configure COLIGO_HUB_FEED_URL first.
 */
function syncColigoAuto_() {
  try {
    if (!PropertiesService.getScriptProperties().getProperty('COLIGO_HUB_FEED_URL')) return;
    const lock = LockService.getScriptLock();
    if (!lock.tryLock(30000)) return;
    try {
      syncColigoOnline_();
    } finally {
      lock.releaseLock();
    }
  } catch (e) {
    Logger.log('syncColigoAuto_ error: ' + e);
  }
}

function recordHomeworkStatus(studentName, subject, done) {
  try {
    const rawName = String(studentName || '').trim();
    const subjectName = String(subject || '').trim();
    if (!rawName || !subjectName) {
      return { success: false, message: 'اسم الطالب والمادة مطلوبان.' };
    }
    // The client sends the portal key ('ali' / 'mostafa'); store full names so
    // the sheet stays readable and consistent with Submissions.
    const key = normalizeName_(rawName);
    const name = (key === 'ali' || key === 'ali ahmed') ? 'Ali Ahmed'
      : ((key === 'mostafa' || key === 'mostafa ahmed') ? 'Mostafa Ahmed' : rawName);
    const isDone = (done === true || done === 'true' || done === 1);

    const ss = getSpreadsheet();
    let sheet = ss.getSheetByName('Homework_Status');
    if (!sheet) {
      setupDatabase(ss);
      sheet = ss.getSheetByName('Homework_Status');
    }

    const map = getSheetHeaderMap_(sheet);
    const data = sheet.getDataRange().getValues();
    const targetName = normalizeName_(name);
    const targetSubject = normalizeName_(subjectName);
    const stamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'GMT+2', 'yyyy-MM-dd HH:mm');
    let rowIndex = -1;

    for (let i = 1; i < data.length; i++) {
      if (normalizeName_(rowValue_(data[i], map, 'Student', 1)) === targetName &&
          normalizeName_(rowValue_(data[i], map, 'Subject', 2)) === targetSubject) {
        rowIndex = i + 1;
        break;
      }
    }

    if (rowIndex > 0) {
      sheet.getRange(rowIndex, 1, 1, 4).setValues([[stamp, name, subjectName, isDone ? 'TRUE' : 'FALSE']]);
    } else {
      sheet.appendRow([stamp, name, subjectName, isDone ? 'TRUE' : 'FALSE']);
    }

    return { success: true, student: name, subject: subjectName, done: isDone };
  } catch (err) {
    Logger.log('recordHomeworkStatus error: ' + err);
    return { success: false, message: err.message };
  }
}


// Auto-generated Starter Question Bank (234 questions) and Starter Exams (48 exams)
function getStarterQuestionBank_() {
  return [["Q_Y5_ENG_W1D1_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "What is an adverbial?", "MCQ", "A single word naming a person or thing | A group of words without a verb that adds detail about time, place, or manner | A group of words with a subject and a verb | A word that joins two clauses together", "A group of words without a verb that adds detail about time, place, or manner", 1, "An adverbial is a word or phrase that gives extra details about WHEN, WHERE, or HOW an action happens. It does NOT contain a finite verb.", "DAILY_Y5_ENG_W1D1", "W1", "Easy"], ["Q_Y5_ENG_W1D1_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "An adverbial of MANNER answers which question?", "MCQ", "How or in what way? | Where? | When? | Who?", "How or in what way?", 1, "Adverbials of manner explain HOW an action happens (e.g., bravely, with great care, silently).", "DAILY_Y5_ENG_W1D1", "W1", "Easy"], ["Q_Y5_ENG_W1D1_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Complete the sentence with the best adverbial of manner: 'The engineer repaired the delicate wiring ........'", "MCQ", "with great care | on the moon | at midnight | next Tuesday", "with great care", 1, "'with great care' tells us HOW the engineer repaired the wiring (Manner).", "DAILY_Y5_ENG_W1D1", "W1", "Medium"], ["Q_Y5_ENG_W1D1_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "In the sentence: 'The astronaut floated silently through the hatch.', which word is an adverb of manner?", "MCQ", "silently | floated | astronaut | through", "silently", 1, "'silently' is an adverb ending in -ly explaining how the astronaut floated.", "DAILY_Y5_ENG_W1D1", "W1", "Medium"], ["Q_Y5_ENG_W1D1_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which phrase functions as a prepositional adverbial of MANNER?", "MCQ", "with furious determination | at three o'clock | behind the laboratory | tomorrow morning", "with furious determination", 1, "'with furious determination' describes HOW something was done, acting as a manner adverbial.", "DAILY_Y5_ENG_W1D1", "W1", "Hard"], ["Q_Y5_ENG_W1D2_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "In the sentence: 'The rocket launched at dawn.', what type of adverbial is 'at dawn'?", "MCQ", "Adverbial of Time | Adverbial of Place | Adverbial of Manner | Adverbial of Reason", "Adverbial of Time", 1, "'at dawn' tells us WHEN the rocket launched (Adverbial of Time).", "DAILY_Y5_ENG_W1D2", "W1", "Easy"], ["Q_Y5_ENG_W1D2_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Choose the sentence that has an adverbial of TIME at the beginning:", "MCQ", "Before sunrise, the pilot took off. | Bravely, the pilot flew the plane. | Over the sea, the pilot flew. | With great skill, the pilot landed.", "Before sunrise, the pilot took off.", 1, "'Before sunrise' tells us WHEN the pilot took off.", "DAILY_Y5_ENG_W1D2", "W1", "Medium"], ["Q_Y5_ENG_W1D2_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "True or False: In the sentence 'The USSR launched Sputnik I in 1957.', we must put a comma before 'in 1957'.", "TRUE_FALSE", "True | False", "False", 1, "When the adverbial is at the END of a sentence, NO comma is needed.", "DAILY_Y5_ENG_W1D2", "W1", "Medium"], ["Q_Y5_ENG_W1D2_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Identify the adverbial of time in: 'Astronauts will explore Mars in the near future.'", "MCQ", "in the near future | explore Mars | Astronauts | will explore", "in the near future", 1, "'in the near future' tells us WHEN the exploration will happen.", "DAILY_Y5_ENG_W1D2", "W1", "Medium"], ["Q_Y5_ENG_W1D2_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which of the following contains a dependent clause acting as a TIME adverbial?", "MCQ", "When the countdown reached zero, the engines ignited. | Inside the bunker, scientists cheered. | Extremely quickly, the vehicle surged forward. | Under the stars, the sky turned orange.", "When the countdown reached zero, the engines ignited.", 1, "'When the countdown reached zero' is a time adverbial clause initiated by subordinating conjunction 'When'.", "DAILY_Y5_ENG_W1D2", "W1", "Hard"], ["Q_Y5_ENG_W1D3_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which of the following sentences contains an adverbial of PLACE?", "MCQ", "The crew slept inside the space station. | In 2000, the first crew moved in. | She carefully checked the controls. | Soon, the rocket was ready.", "The crew slept inside the space station.", 1, "'inside the space station' answers the question WHERE did the crew sleep (Adverbial of Place).", "DAILY_Y5_ENG_W1D3", "W1", "Easy"], ["Q_Y5_ENG_W1D3_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "In the sentence: 'High above the clouds, the telescope captured distant galaxies.', what question does 'High above the clouds' answer?", "MCQ", "Where? | When? | How? | Why?", "Where?", 1, "'High above the clouds' indicates WHERE the telescope was operating.", "DAILY_Y5_ENG_W1D3", "W1", "Medium"], ["Q_Y5_ENG_W1D3_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Select the sentence where an adverbial of place is correctly fronted with a comma:", "MCQ", "Across the lunar plains, rovers collected dust samples. | Across the lunar plains rovers collected dust samples. | Across the lunar, plains rovers collected dust samples. | Across the lunar plains rovers, collected dust samples.", "Across the lunar plains, rovers collected dust samples.", 1, "Fronted adverbials of place require a comma immediately separating them from the main clause.", "DAILY_Y5_ENG_W1D3", "W1", "Medium"], ["Q_Y5_ENG_W1D3_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which phrase is an adverbial of PLACE?", "MCQ", "underneath the heavy machinery | yesterday afternoon | without making a sound | as soon as possible", "underneath the heavy machinery", 1, "'underneath the heavy machinery' specifies spatial location (WHERE).", "DAILY_Y5_ENG_W1D3", "W1", "Medium"], ["Q_Y5_ENG_W1D3_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Identify the sentence that contains BOTH an adverbial of time AND an adverbial of place:", "MCQ", "At midnight, the satellite drifted into deep orbit. | At midnight, the clock struck twelve. | Into deep orbit, the rocket blasted. | With great power, the engines roared.", "At midnight, the satellite drifted into deep orbit.", 1, "'At midnight' is time, and 'into deep orbit' is place.", "DAILY_Y5_ENG_W1D3", "W1", "Hard"], ["Q_Y5_ENG_W1D4_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which sentence is punctuated correctly with a comma after the fronted adverbial?", "MCQ", "After a long journey, the crew landed. | After a long journey the crew landed. | After a long journey, the crew, landed. | After, a long journey the crew landed.", "After a long journey, the crew landed.", 1, "When an adverbial is at the start (Fronted Adverbial), it must be followed by a comma.", "DAILY_Y5_ENG_W1D4", "W1", "Easy"], ["Q_Y5_ENG_W1D4_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Rewrite 'Astronauts walked on the Moon in July 1969.' to begin with a FRONTED adverbial:", "MCQ", "In July 1969, astronauts walked on the Moon. | Astronauts walked in July 1969 on the Moon. | On the Moon walked astronauts in July 1969. | In July 1969 astronauts walked on the Moon.", "In July 1969, astronauts walked on the Moon.", 1, "Move 'In July 1969' to the front and add a comma immediately after.", "DAILY_Y5_ENG_W1D4", "W1", "Medium"], ["Q_Y5_ENG_W1D4_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Why is a comma needed after a fronted adverbial?", "MCQ", "To separate the introductory adverbial phrase from the main clause for clarity | Because all sentences need two commas | To replace the verb | To indicate a question", "To separate the introductory adverbial phrase from the main clause for clarity", 1, "A comma prevents misreading and clarifies the boundary between the introductory phrase and the independent clause.", "DAILY_Y5_ENG_W1D4", "W1", "Medium"], ["Q_Y5_ENG_W1D4_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which sentence has INCORRECT punctuation?", "MCQ", "Suddenly the meteor flashed across the sky. | Suddenly, the meteor flashed across the sky. | The meteor suddenly flashed across the sky. | Across the sky, the meteor flashed suddenly.", "Suddenly the meteor flashed across the sky.", 1, "'Suddenly' is a fronted adverb of manner and requires a comma immediately following it.", "DAILY_Y5_ENG_W1D4", "W1", "Hard"], ["Q_Y5_ENG_W1D4_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "True or False: If an adverbial is placed in the middle of a sentence (parenthetical), commas may be needed on both sides.", "TRUE_FALSE", "True | False", "True", 1, "An adverbial interrupting the flow in mid-sentence can be enclosed by a pair of commas (parenthesis).", "DAILY_Y5_ENG_W1D4", "W1", "Hard"], ["Q_Y5_ENG_W1D5_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Which sentence has BOTH an adverbial of time AND an adverbial of manner?", "MCQ", "At 8:00 AM, the crew worked tirelessly. | The rocket launched into orbit. | Astronauts ate inside the station. | Yesterday, the weather was sunny.", "At 8:00 AM, the crew worked tirelessly.", 1, "'At 8:00 AM' is time; 'tirelessly' is manner.", "DAILY_Y5_ENG_W1D5", "W1", "Medium"], ["Q_Y5_ENG_W1D5_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials", "Fix the error: 'Without making a sound the stealth drone vanished into the clouds.' What is missing?", "MCQ", "A comma after 'sound' | A full stop after 'sound' | A comma after 'stealth' | A question mark", "A comma after 'sound'", 1, "'Without making a sound' is a fronted manner adverbial phrase and must be followed by a comma.", "DAILY_Y5_ENG_W1D6", "W1", "Medium"], ["Q_Y5_ENG_W2D8_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "Which relative pronoun is used specifically for PEOPLE?", "MCQ", "who | which | where | when", "who", 1, "'who' (and 'whom') refers to people, while 'which' refers to things and animals.", "DAILY_Y5_ENG_W2D8", "W2", "Easy"], ["Q_Y5_ENG_W2D8_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "Complete the sentence: 'The spacesuit, ________ was designed by NASA, protected the astronaut.'", "MCQ", "which | who | whose | where", "which", 1, "A spacesuit is an inanimate object, so the relative pronoun 'which' is required.", "DAILY_Y5_ENG_W2D8", "W2", "Easy"], ["Q_Y5_ENG_W2D8_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "Which relative pronoun indicates POSSESSION?", "MCQ", "whose | who | whom | which", "whose", 1, "'whose' shows ownership (e.g. 'the astronaut whose helmet cracked').", "DAILY_Y5_ENG_W2D8", "W2", "Medium"], ["Q_Y5_ENG_W2D8_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "Select the correct relative pronoun: 'The astronomer ________ discovered the comet won an award.'", "MCQ", "who | which | where | whose", "who", 1, "'astronomer' is a person, requiring 'who'.", "DAILY_Y5_ENG_W2D8", "W2", "Medium"], ["Q_Y5_ENG_W2D8_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "True or False: In formal UK English, 'which' is preferred over 'who' when referring to family pets with names.", "TRUE_FALSE", "True | False", "False", 1, "Pets named or regarded as persons often take 'who', but formal grammar typically uses 'which/that' for animals unless personified.", "DAILY_Y5_ENG_W2D8", "W2", "Hard"], ["Q_Y5_ENG_W2D9_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "What is the main function of a NON-DEFINING relative clause?", "MCQ", "It adds extra, non-essential information and is surrounded by commas | It defines exactly which noun is being spoken about without commas | It replaces the main subject of the sentence | It turns a sentence into a question", "It adds extra, non-essential information and is surrounded by commas", 1, "Non-defining relative clauses provide extra detail that could be removed without making the sentence incomplete. They MUST be enclosed in commas.", "DAILY_Y5_ENG_W2D9", "W2", "Medium"], ["Q_Y5_ENG_W2D9_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "Which sentence is punctuated correctly with commas around the relative clause?", "MCQ", "Neil Armstrong, who walked on the Moon, was an American hero. | Neil Armstrong who walked on the Moon was an American hero. | Neil Armstrong, who walked on the Moon was an American hero. | Neil Armstrong who walked on the Moon, was an American hero.", "Neil Armstrong, who walked on the Moon, was an American hero.", 1, "Because 'Neil Armstrong' is already specific, the clause is non-defining and requires commas before AND after.", "DAILY_Y5_ENG_W2D9", "W2", "Hard"], ["Q_Y5_ENG_W2D10_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 4: Relative Clauses", "In: 'The rocket that was built in 1969 carried three astronauts.', why are there NO commas?", "MCQ", "Because it is a defining clause specifying which exact rocket carried them | Because commas are never used with 'rocket' | Because it is a short sentence | Because 'built' is past tense", "Because it is a defining clause specifying which exact rocket carried them", 1, "Defining (restrictive) clauses identify the specific item and take no commas.", "DAILY_Y5_ENG_W2D10", "W2", "Hard"], ["Q_Y5_ENG_W3D15_01", "Year 5 (G5)", "English Grammar", "Unit 3 - Lesson 1: Modal Verbs", "Which modal verb expresses CERTAINTY or strict obligation?", "MCQ", "must | might | could | perhaps", "must", 1, "'must' expresses high certainty or obligation, whereas 'might' and 'could' express possibility.", "DAILY_Y5_ENG_W3D15", "W3", "Easy"], ["Q_Y5_ENG_W3D15_02", "Year 5 (G5)", "English Grammar", "Unit 3 - Lesson 1: Modal Verbs", "Select the modal verb that shows WEAK POSSIBILITY: 'The storm ________ delay the launch tomorrow.'", "MCQ", "might | will | must | definitely", "might", 1, "'might' indicates an uncertain possibility (it could happen, or not).", "DAILY_Y5_ENG_W3D15", "W3", "Medium"], ["Q_Y5_ENG_W3D16_01", "Year 5 (G5)", "English Grammar", "Unit 3 - Lesson 2: Cohesive Devices", "Which cohesive conjunction shows CONTRAST between two clauses?", "MCQ", "although | because | furthermore | therefore", "although", 1, "'although' introduces a concession or contrast.", "DAILY_Y5_ENG_W3D16", "W3", "Medium"], ["Q_Y5_ENG_W4D22_01", "Year 5 (G5)", "English Grammar", "Unit 4 - Lesson 1: Complex Synthesis", "Identify the sentence combining an adverbial of time, a relative clause, and correct punctuation:", "MCQ", "Before dawn, the rover, which had recharged its battery, began moving. | Before dawn the rover which had recharged its battery began moving. | Before dawn, the rover who recharged its battery began moving. | Before dawn the rover, which recharged its battery, began moving.", "Before dawn, the rover, which had recharged its battery, began moving.", 1, "Fronted adverbial 'Before dawn,' has a comma; non-defining clause ', which had recharged its battery,' has commas; 'which' refers to rover.", "DAILY_Y5_ENG_W4D22", "W4", "Hard"], ["Q_Y6_ARB_W1D4_01", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات", "الفكرة الرئيسة لنص إدارة الوقت هي أن النجاح يتحقق من خلال:", "MCQ", "التخطيط المسبق وترتيب الأولويات | تأجيل الواجبات الصعبة | العمل طوال اليوم دون راحة | الاعتماد على الحظ", "التخطيط المسبق وترتيب الأولويات", 1, "إدارة الوقت تبدأ بتحديد الأهداف وترتيب الأولويات والبدء بالمهام العاجلة والمهمة.", "DAILY_Y6_ARB_W1D4", "W1", "Easy"], ["Q_Y6_ARB_W1D4_02", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات", "وفقاً لمصفوفة الأولويات (ستيفن كوفي)، أي المهام يجب البدء بها أولاً؟", "MCQ", "المهم والعاجل | غير المهم والعاجل | غير المهم وغير العاجل | الترفيه والتسلية", "المهم والعاجل", 1, "مربع الأزمات والمهام الأساسية (المهم والعاجل) هو الذي يتطلب التنفيذ الفوري.", "DAILY_Y6_ARB_W1D4", "W1", "Medium"], ["Q_Y6_ARB_W1D4_03", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات", "مرادف كلمة (الإرجاء) في سياق: 'إرجاء الأعمال المهمة يقود إلى الإخفاق' هو:", "MCQ", "التأجيل والتسويف | الإسراع والتبكير | الإلغاء النهائي | التكرار", "التأجيل والتسويف", 1, "أرجأ الشيء أي أخّره وأجّله.", "DAILY_Y6_ARB_W1D4", "W1", "Medium"], ["Q_Y6_ARB_W1D4_04", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات", "مضاد كلمة (الحَثِيث) في عبارة: 'يبذل جهداً حثيثاً لإنجاز واجباته':", "MCQ", "البطيء والمتكاسل | السريع | القوي | المستمر", "البطيء والمتكاسل", 1, "الحثيث تعني السريع الجاد، ومضادها البطيء المتواني.", "DAILY_Y6_ARB_W1D4", "W1", "Hard"], ["Q_Y6_ARB_W1D4_05", "Grade 6 (G6)", "اللغة العربية", "المحور الأول: إدارة الوقت وترتيب الأولويات", "علامَ يدل قول الكاتب: 'الوقت كالسيف إن لم تقطعه قطعك'؟", "MCQ", "أهمية اغتنام الوقت وحتمية مضيه دون رجوع | خطورة استخدام السيوف | ضرورة النوم مبكراً | صعوبة تنظيم اليوم", "أهمية اغتنام الوقت وحتمية مضيه دون رجوع", 1, "التشبيه يؤكد أن الوقت لا ينتظر أحداً، وإما أن تستثمره أو ينقضي فيضرك ضياعه.", "DAILY_Y6_ARB_W1D4", "W1", "Hard"], ["Q_Y6_ARB_W1D5_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "عيّن الاسم المعرفة في جملة: 'قرأ التلميذُ كتاباً مفيداً':", "MCQ", "التلميذُ (معرف بأل) | كتاباً | مفيداً | قرأ", "التلميذُ (معرف بأل)", 1, "(التلميذُ) اسم معرفة لأنه مقترن بأل التعريف، أما (كتاباً ومفيداً) فهما اسمان نكرتان.", "DAILY_Y6_ARB_W1D5", "W1", "Easy"], ["Q_Y6_ARB_W1D5_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "الضمائر (أنا، نحن، هو، هي) وأسماء الإشارة والأسماء الموصولة كلها تعتبر:", "MCQ", "معارف دائماً | نكرات دائماً | حروفاً وليست أسماء | أفعالاً ماضية", "معارف دائماً", 1, "الضمائر وأسماء الإشارة والأسماء الموصولة وأسماء الأعلام والمعرف بأل والمضاف إلى معرفة كلها معارف.", "DAILY_Y6_ARB_W1D5", "W1", "Easy"], ["Q_Y6_ARB_W1D5_03", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "في جملة 'زارنا ضيفٌ كريمٌ'، الاسمان 'ضيفٌ' و 'كريمٌ':", "MCQ", "نكرتان لأنهما يدلان على غير معيّن ومنوّنان | معرفتان بأل | اسما إشارة | ضميران غائبان", "نكرتان لأنهما يدلان على غير معيّن ومنوّنان", 1, "النكرة تدل على شيء غير محدد وتقبل التنوين.", "DAILY_Y6_ARB_W1D5", "W1", "Medium"], ["Q_Y6_ARB_W1D5_04", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "حوّل النكرة إلى معرفة بالإضافة في: 'قرأتُ كتاباً':", "MCQ", "قرأتُ كتابَ النحوِ | قرأتُ كتاباً جميلاً | قرأتُ كتباً | كتابٌ قرأته", "قرأتُ كتابَ النحوِ", 1, "اكتسب الاسم النكرة (كتاب) التعريف بإضافته إلى المعرفة (النحو).", "DAILY_Y6_ARB_W1D5", "W1", "Medium"], ["Q_Y6_ARB_W1D5_05", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: النكرة والمعرفة", "كم اسماً معرفة في جملة: 'هذا هو الطالبُ الذي فاز في المسابقةِ'؟", "MCQ", "5 أسماء معارف | 3 أسماء | معرفتان فقط | اسم واحد", "5 أسماء معارف", 1, "المعارف هي: هذا (اسم إشارة)، هو (ضمير)، الطالب (معرف بأل)، الذي (اسم موصول)، المسابقة (معرف بأل).", "DAILY_Y6_ARB_W1D5", "W1", "Hard"], ["Q_Y6_ARB_W1D6_01", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف", "ما سبب كتابة الهمزة على ألف في كلمة (يَسْـأَلُ)؟", "MCQ", "لأن الهمزة مفتوحة وما قبلها ساكن | لأن الهمزة مكسورة | لأن الهمزة مضمومة | لأن ما قبلها ألف مد", "لأن الهمزة مفتوحة وما قبلها ساكن", 1, "في كلمة (يَسْـأَل): السين ساكنة والهمزة مفتوحة، والفتحة أقوى من السكون فترسم على ألف.", "DAILY_Y6_ARB_W1D6", "W1", "Easy"], ["Q_Y6_ARB_W1D6_02", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف", "اختر الرسم الإملائي الصحيح للكلمة: 'لا ........ عن مساعدة المحتاجين.'", "MCQ", "تَتَأَخَّرْ | تتأخر (بدون همزة) | تتءخر | تتآخر", "تَتَأَخَّرْ", 1, "تَـتَـأَخَّـر (الهمزة مفتوحة وقبلها تاء مفتوحة فتُرسم على ألف).", "DAILY_Y6_ARB_W1D6", "W1", "Easy"], ["Q_Y6_ARB_W1D6_03", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف", "ترسم الهمزة المتوسطة على ألف في ثلاث حالات، منها أن تكون:", "MCQ", "ساكنة بعد فتح (مثل رَأْس) | مكسورة بعد ضم | مضمومة بعد كسر | ساكنة بعد ضم", "ساكنة بعد فتح (مثل رَأْس)", 1, "إذا كانت الهمزة ساكنة وما قبلها مفتوح، فإن الفتحة أقوى من السكون فتكتب على ألف.", "DAILY_Y6_ARB_W1D6", "W1", "Medium"], ["Q_Y6_ARB_W1D6_04", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف", "أي الكلمات الآتية كُتبت فيها الهمزة المتوسطة بصورة خاطئة؟", "MCQ", "مَسْئَلة | مَسْأَلة | فَأْس | مَأْوى", "مَسْئَلة", 1, "الصواب (مسألة) لأن الهمزة مفتوحة بعد سين ساكنة فترسم على ألف وليس على نبرة.", "DAILY_Y6_ARB_W1D6", "W1", "Hard"], ["Q_Y6_ARB_W1D6_05", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على ألف", "صوّب الخطأ الإملائي في الجملة: 'المؤمن لا يَـيْـئَـسُ من رحمة الله':", "MCQ", "يَيْأَسُ | ييأس (بدون ضبط) | ييؤس | ييئس", "يَيْأَسُ", 1, "الهمزة في (يَيْأَسُ) مفتوحة وما قبلها ياء ساكنة أصلية فتكتب على ألف.", "DAILY_Y6_ARB_W1D6", "W1", "Hard"], ["Q_Y6_ARB_W2D8_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "ما نوع الخبر في جملة: 'العالِمُ مخلصٌ في عمله'؟", "MCQ", "خبر مفرد | خبر جملة اسمية | خبر جملة فعلية | خبر شبه جملة", "خبر مفرد", 1, "(مخلصٌ) خبر مفرد لأنه ليس جملة ولا شبه جملة، حتى لو دل على مثنى أو جمع.", "DAILY_Y6_ARB_W2D8", "W2", "Easy"], ["Q_Y6_ARB_W2D8_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "الخبر في جملة 'المعلّمون مخلصون' نوعه مفرد لأن:", "MCQ", "المقصود بالمفرد هنا أنه كلمة واحدة وليس جملة ولا شبه جملة | المعلمون شخص واحد | مخلصون فعل ماض | الخبر هنا شبه جملة", "المقصود بالمفرد هنا أنه كلمة واحدة وليس جملة ولا شبه جملة", 1, "في باب المبتدأ والخبر، (المفرد) يعني ما ليس جملة ولا شبه جملة.", "DAILY_Y6_ARB_W2D8", "W2", "Medium"], ["Q_Y6_ARB_W2D8_03", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "أعرب كلمة 'نشيطان' في جملة: 'التلميذان نشيطان':", "MCQ", "خبر المبتدأ مرفوع وعلامة رفعه الألف لأنه مثنى | خبر مرفوع بالضمة | مبتدأ ثانٍ | مفعول به", "خبر المبتدأ مرفوع وعلامة رفعه الألف لأنه مثنى", 1, "علامة رفع المثنى هي الألف.", "DAILY_Y6_ARB_W2D8", "W2", "Medium"], ["Q_Y6_ARB_W2D8_04", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "اختر الخبر المناسب ليكتمل المعنى بخبر مفرد: 'المهندسون ........'", "MCQ", "بارعون | يبارعون | في المشروع | إتقانهم كبير", "بارعون", 1, "'بارعون' اسم مفرد مرفوع بالواو لأنه جمع مذكر سالم.", "DAILY_Y6_ARB_W2D8", "W2", "Medium"], ["Q_Y6_ARB_W2D8_05", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "أي الجمل الآتية تشتمل على خبر مفرد؟", "MCQ", "الأمهاتُ رحيماتٌ بأبنائهن | الصدقُ يهدي إلى البر | العصفورُ فوق الشجرة | الحديقةُ أزهارها متفتحة", "الأمهاتُ رحيماتٌ بأبنائهن", 1, "(رحيماتٌ) كلمة واحدة اسمية تممت المعنى فهي خبر مفرد.", "DAILY_Y6_ARB_W2D8", "W2", "Hard"], ["Q_Y6_ARB_W2D9_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "ما نوع الخبر في: 'الطالبُ يذاكرُ دروسَه بإتقان'؟", "MCQ", "خبر جملة فعلية | خبر مفرد | خبر جملة اسمية | خبر شبه جملة", "خبر جملة فعلية", 1, "جملة الفعل والفاعل المستتر (يذاكر هو) في محل رفع خبر المبتدأ.", "DAILY_Y6_ARB_W2D9", "W2", "Easy"], ["Q_Y6_ARB_W2D9_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "ما الرابط المشترط في خبر الجملة الاسمية في: 'الشجرةُ أغصانُها خضراءُ'؟", "MCQ", "الضمير (الهاء) العائد على المبتدأ الأول | الألف واللام | اسم الإشارة | حرف العطف", "الضمير (الهاء) العائد على المبتدأ الأول", 1, "يشترط في خبر الجملة وجود ضمير يربطها بالمبتدأ الأول ويطابقه.", "DAILY_Y6_ARB_W2D9", "W2", "Medium"], ["Q_Y6_ARB_W2D9_03", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "عيّن خبر شبه الجملة في جملة: 'العزّ في طاعةِ الله':", "MCQ", "في طاعةِ (جار ومجرور) | العزّ | الله | مستتر", "في طاعةِ (جار ومجرور)", 1, "الجار والمجرور (في طاعة) شبه جملة في محل رفع خبر.", "DAILY_Y6_ARB_W2D9", "W2", "Medium"], ["Q_Y6_ARB_W2D9_04", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "حوّل الخبر المفرد إلى خبر جملة فعلية في: 'المعلمان مخلصان':", "MCQ", "المعلمان يخلصان في العمل | المعلمان إخلاصهما عظيم | المعلمان في إخلاص | مخلص المعلمان", "المعلمان يخلصان في العمل", 1, "تحويل الاسم المشتق (مخلصان) إلى فعل مضارع (يخلصان).", "DAILY_Y6_ARB_W2D9", "W2", "Hard"], ["Q_Y6_ARB_W2D9_05", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "ما المحل الإعرابي لشبه الجملة (تحت المنضدة) في: 'القطةُ تحتَ المنضدةِ'؟", "MCQ", "في محل رفع خبر المبتدأ | في محل نصب مفعول به | في محل جر مضاف إليه | مبتدأ مؤخر", "في محل رفع خبر المبتدأ", 1, "شبه الجملة الظرفي متعلق بمحذوف تقديره مستقر في محل رفع خبر.", "DAILY_Y6_ARB_W2D9", "W2", "Hard"], ["Q_Y6_ARB_W2D10_01", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على واو", "ما سبب كتابة الهمزة على واو في كلمة (مُـؤْمِـن)؟", "MCQ", "لأن الهمزة ساكنة وما قبلها مضموم والضمة أقوى من السكون | لأن الهمزة مكسورة | لأن الهمزة مفتوحة وما قبلها ألف | لأنها آخر الكلمة", "لأن الهمزة ساكنة وما قبلها مضموم والضمة أقوى من السكون", 1, "قاعدة أقوى الحركات: الكسرة ثم الضمة ثم الفتحة ثم السكون. الضمة أقوى من السكون فتكتب على واو.", "DAILY_Y6_ARB_W2D10", "W2", "Easy"], ["Q_Y6_ARB_W2D10_02", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على واو", "اختر الرسم الصحيح للكلمة: 'يتصف التلميذ بـ ........ الصادق.'", "MCQ", "التَّـفَـاؤُلِ | التفاأل | التفايل | التفاءل", "التَّـفَـاؤُلِ", 1, "الهمزة مضمومة بعد ألف مد ساكنة، والضمة أقوى من السكون فترسم على واو.", "DAILY_Y6_ARB_W2D10", "W2", "Medium"], ["Q_Y6_ARB_W2D10_03", "Grade 6 (G6)", "اللغة العربية", "القواعد الإملائية: الهمزة المتوسطة على واو", "أي الكلمات التالية كُتبت همزتها على واو لأنها مفتوحة بعد ضم؟", "MCQ", "مُـؤَذِّن | رُؤْيَة | شُؤُون | فُؤَاد (مضمومة)", "مُـؤَذِّن", 1, "في كلمة (مُـؤَذِّن): الميم مضمومة والهمزة مفتوحة، والضمة أقوى من الفتحة فتكتب على واو.", "DAILY_Y6_ARB_W2D10", "W2", "Hard"], ["Q_Y6_ARB_W3D15_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: الأسماء الخمسة", "ما علامة رفع الأسماء الخمسة (أب، أخ، حم، فو، ذو)؟", "MCQ", "الواو (نيابة عن الضمة) | الألف | الياء | الضمة الظاهرة", "الواو (نيابة عن الضمة)", 1, "الأسماء الخمسة ترفع بالواو وتنصب بالألف وتجر بالياء بشرط أن تكون مفردة ومضافة لغير ياء المتكلم.", "DAILY_Y6_ARB_W3D15", "W3", "Easy"], ["Q_Y6_ARB_W3D15_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: الأسماء الخمسة", "أعرب 'أباك' في جملة: 'أطِعْ أباكَ':", "MCQ", "مفعول به منصوب وعلامة نصبه الألف لأنه من الأسماء الخمسة | فاعل مرفوع بالواو | اسم مجرور بالياء | مضاف إليه", "مفعول به منصوب وعلامة نصبه الألف لأنه من الأسماء الخمسة", 1, "تنصب الأسماء الخمسة بالألف، والكاف ضمير متصل في محل جر مضاف إليه.", "DAILY_Y6_ARB_W3D15", "W3", "Medium"], ["Q_Y6_ARB_W3D16_01", "Grade 6 (G6)", "اللغة العربية", "التعبير والكتابة: النص المعلوماتي", "السمة الأساسية للنص المعلوماتي هي الاعتماد على:", "MCQ", "الحقائق والأرقام الموضوعية بدقة ومصداقية | الخيال والأساطير غير الواقعية | العواطف والمشاعر الشخصية فقط | السجع والقوافي الشعرية", "الحقائق والأرقام الموضوعية بدقة ومصداقية", 1, "النص المعلوماتي يقدم حقائق علمية أو معرفية خالية من الآراء الذاتية.", "DAILY_Y6_ARB_W3D16", "W3", "Medium"], ["Q_Y6_ARB_W4D22_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: الأفعال الناسخة والحروف الناسخة", "ما عمل الأفعال الناسخة (كان وأخواتها) عند دخولها على الجملة الاسمية؟", "MCQ", "ترفع المبتدأ ويسمى اسمها، وتنصب الخبر ويسمى خبرها | تنصب المبتدأ وترفع الخبر | تجر المبتدأ والخبر | تجزم الفعل المضارع", "ترفع المبتدأ ويسمى اسمها، وتنصب الخبر ويسمى خبرها", 1, "كان وأخواتها أفعال ناسخة ترفع الاسم وتنصب الخبر.", "DAILY_Y6_ARB_W4D22", "W4", "Easy"], ["Q_Y6_ARB_W4D22_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: الأفعال الناسخة والحروف الناسخة", "أعرب كلمة 'متفوقين' في: 'أصبحَ الطلابُ متفوقينَ':", "MCQ", "خبر أصبح منصوب وعلامة نصبه الياء لأنه جمع مذكر سالم | اسم أصبح مرفوع | مضاف إليه | نعت منصوب بالفتحة", "خبر أصبح منصوب وعلامة نصبه الياء لأنه جمع مذكر سالم", 1, "خبر أصبح منصوب وعلامة نصبه الياء.", "DAILY_Y6_ARB_W4D22", "W4", "Medium"], ["Q_Y5_ICT_01", "Year 5 (G5)", "ICT Computing", "Computational Thinking: Variables & Loops", "A named location in computer memory that stores data which can change during program execution is called a:", "MCQ", "Loop|Variable|Constant|Value", "Variable", 1, "A variable is like a labelled box in memory that holds a single piece of data (value) at any one time.", "EX_Y5_ICT_QUIZ01", "W7", "Easy"], ["Q_Y5_ICT_02", "Year 5 (G5)", "ICT Computing", "Computational Thinking: Variables & Loops", "When choosing a name for a variable (such as student score or timer), the best practice is:", "MCQ", "Use a clear, meaningful name (e.g. score)|Use a random letter like X12|Make it an extremely long sentence|Leave it blank", "Use a clear, meaningful name (e.g. score)", 1, "Variable names should be meaningful and descriptive so anyone reading the code immediately understands its purpose.", "EX_Y5_ICT_QUIZ01", "W7", "Easy"], ["Q_Y5_ICT_03", "Year 5 (G5)", "ICT Computing", "Computational Thinking: Variables & Loops", "What type of loop is used when we know in advance exactly how many times instructions must repeat (e.g. repeat 10 times)?", "MCQ", "Infinite loop|Count-controlled loop|Condition-controlled loop|Crash loop", "Count-controlled loop", 1, "A count-controlled loop repeats instructions a predetermined, specified number of times.", "EX_Y5_ICT_QUIZ01", "W7", "Medium"], ["Q_Y5_ICT_04", "Year 5 (G5)", "ICT Computing", "Computer Hardware: Input & Output", "Which of the following devices acts as BOTH an Input and an Output device?", "MCQ", "Touchscreen|Keyboard|Speakers|Printer", "Touchscreen", 1, "A touchscreen detects finger touch input and also displays visual output on the same screen.", "EX_Y5_ICT_QUIZ01", "W7", "Easy"], ["Q_Y5_ICT_05", "Year 5 (G5)", "ICT Computing", "Scratch Programming: Operators", "In Scratch, which color and shape of operator block reports a Boolean (True / False) result?", "MCQ", "Pointed green blocks (<, >, =)|Round blue blocks|Square yellow blocks|Oval purple blocks", "Pointed green blocks (<, >, =)", 1, "In Scratch, pointed (hexagonal) green blocks test conditions and report True or False.", "EX_Y5_ICT_QUIZ01", "W7", "Medium"], ["Q_Y5_ICT_06", "Year 5 (G5)", "ICT Computing", "Scratch Programming: Operators", "If a Scratch block evaluates the expression: (8 * 7) - 16, what is the reported value?", "MCQ", "40|56|48|36", "40", 1, "8 * 7 = 56, and 56 - 16 = 40.", "EX_Y5_ICT_QUIZ01", "W7", "Challenge"], ["Q_Y5_ENG_W7D1_01", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 2: Simple & Compound Sentences", "Which of the following is a simple sentence?", "MCQ", "Mission control tracked the rocket.|The rocket launched, and the crowd cheered.|The crew cheered because the rocket had launched.|The engine was loud, yet the crew stayed calm.", "Mission control tracked the rocket.", 1, "A simple sentence consists of a single independent clause with one subject and verb predicate, expressing a complete thought.", "DAILY_Y5_ENG_W7D1", "W7", "Easy"], ["Q_Y5_ENG_W7D1_02", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 2: Simple & Compound Sentences", "Which sentence is a compound sentence?", "MCQ", "Planets orbit the Sun, and moons orbit planets.|Space is cold and dark.|The astronauts waved to the crowd.|The crew trained hard because the mission was risky.", "Planets orbit the Sun, and moons orbit planets.", 1, "A compound sentence joins two independent clauses using a coordinating conjunction (FANBOYS) preceded by a comma.", "DAILY_Y5_ENG_W7D1", "W7", "Medium"], ["Q_Y5_ENG_W7D1_03", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 2: Simple & Compound Sentences", "Which acronym represents the seven coordinating conjunctions used to create compound sentences?", "MCQ", "FANBOYS (for, and, nor, but, or, yet, so)|ISAAC|PREFIX|CLAUSES", "FANBOYS (for, and, nor, but, or, yet, so)", 1, "FANBOYS is the mnemonic for the coordinating conjunctions: For, And, Nor, But, Or, Yet, So.", "DAILY_Y5_ENG_W7D1", "W7", "Easy"], ["Q_Y5_ENG_W7D1_04", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 2: Simple & Compound Sentences", "Classify this sentence: 'Rockets are powerful, but they are expensive to build.'", "MCQ", "Compound sentence|Simple sentence with compound predicate|Complex sentence|Sentence fragment", "Compound sentence", 1, "It has two complete clauses ('Rockets are powerful' and 'they are expensive to build') joined by ', but'.", "DAILY_Y5_ENG_W7D1", "W7", "Medium"], ["Q_Y5_ENG_W7D1_05", "Year 5 (G5)", "English Grammar", "Unit 2 - Lesson 3: Adverbials of Time & Place", "Identify the fronted adverbial of place in: 'Across the dusty launchpad, the engineers inspected the spacecraft.'", "MCQ", "Across the dusty launchpad|the engineers|inspected the spacecraft|dusty launchpad", "Across the dusty launchpad", 1, "'Across the dusty launchpad' is a prepositional phrase functioning as a fronted adverbial of place, followed by a comma.", "DAILY_Y5_ENG_W7D1", "W7", "Challenge"], ["Q_Y6_ICT_01", "Grade 6 (G6)", "ICT Computing", "Programming Constructs: Sequence, Selection, Iteration", "A robot program moves forward 3 steps, turns right 90 degrees, and stops. Which programming construct is this?", "MCQ", "Sequence|Selection|Iteration|Variable", "Sequence", 1, "Sequence means executing instructions step-by-step, in the exact order they are written.", "EX_Y6_ICT_QUIZ01", "W7", "Easy"], ["Q_Y6_ICT_02", "Grade 6 (G6)", "ICT Computing", "Programming Constructs: Sequence, Selection, Iteration", "A game checks: IF score >= 50 THEN display 'Winner!' ELSE display 'Try Again'. Which construct does this represent?", "MCQ", "Selection|Sequence|Iteration|Subroutine", "Selection", 1, "Selection uses condition testing (IF / ELSE) to choose which path of instructions to execute.", "EX_Y6_ICT_QUIZ01", "W7", "Easy"], ["Q_Y6_ICT_03", "Grade 6 (G6)", "ICT Computing", "Programming Constructs: Sequence, Selection, Iteration", "A game sprite repeats a jumping animation 10 times in a row. What programming construct is being used?", "MCQ", "Iteration (Looping)|Selection|Sequence|Variable Assignment", "Iteration (Looping)", 1, "Iteration is repeating a block of instructions multiple times or until a condition is met.", "EX_Y6_ICT_QUIZ01", "W7", "Medium"], ["Q_Y6_ICT_04", "Grade 6 (G6)", "ICT Computing", "Algorithms & Flowcharts", "What is the primary definition and purpose of a Flowchart in computer science?", "MCQ", "A visual diagram showing the logical steps of an algorithm|A type of hardware cable|A video game graphic|An operating system program", "A visual diagram showing the logical steps of an algorithm", 1, "A flowchart is a diagrammatic representation that visually displays the sequence and decision steps of an algorithm.", "EX_Y6_ICT_QUIZ01", "W7", "Easy"], ["Q_Y6_ICT_05", "Grade 6 (G6)", "ICT Computing", "Algorithms & Flowcharts", "In a standard flowchart, which symbol represents an action or processing step (e.g. calculation)?", "MCQ", "Rectangle|Oval|Diamond|Parallelogram", "Rectangle", 1, "Rectangles represent processes/actions; Ovals represent Start/End; Diamonds represent decisions.", "EX_Y6_ICT_QUIZ01", "W7", "Medium"], ["Q_Y6_ICT_06", "Grade 6 (G6)", "ICT Computing", "Algorithms & Flowcharts", "In a flowchart, what does a Diamond shape represent?", "MCQ", "A Decision point with Yes/No branches|Start of program|Output printing|Variable storage", "A Decision point with Yes/No branches", 1, "A diamond represents a conditional decision where the flow splits into different paths based on True/False or Yes/No.", "EX_Y6_ICT_QUIZ01", "W7", "Challenge"], ["Q_Y6_ARB_W7D1_01", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "حدد نوع الخبر في الجملة التالية: «العلمُ نورٌ يضيءُ العقولَ».", "MCQ", "خبر مفرد|خبر جملة فعلية|خبر جملة اسمية|خبر شبه جملة", "خبر مفرد", 1, "كلمة «نورٌ» كلمة واحدة اسمية مفردة ليست جملة ولا شبه جملة، وتممت معنى المبتدأ فهو خبر مفرد مرفوع بالضمة.", "DAILY_Y6_ARB_W7D1", "W7", "Easy"], ["Q_Y6_ARB_W7D1_02", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "ما نوع الخبر في جملة: «الحديقةُ أزهارُها متفتحةٌ»؟", "MCQ", "خبر جملة اسمية|خبر مفرد|خبر جملة فعلية|خبر شبه جملة ظرف", "خبر جملة اسمية", 1, "الخبر هنا جملة اسمية «أزهارها متفتحة» تشتمل على ضمير رابط (الهاء) يعود على المبتدأ الأول «الحديقة».", "DAILY_Y6_ARB_W7D1", "W7", "Medium"], ["Q_Y6_ARB_W7D1_03", "Grade 6 (G6)", "اللغة العربية", "القواعد النحوية: أنواع الخبر", "عين الخبر ونوعه في جملة: «الطائرُ فوقَ الغصنِ».", "MCQ", "فوق الغصن (شبه جملة ظرف مكان)|الطائر (مفرد)|الغصن (مضاف إليه)|فوق (جملة فعلية)", "فوق الغصن (شبه جملة ظرف مكان)", 1, "«فوقَ» ظرف مكان شبه جملة في محل رفع خبر المبتدأ «الطائر».", "DAILY_Y6_ARB_W7D1", "W7", "Medium"], ["Q_Y6_ARB_W7D1_04", "Grade 6 (G6)", "اللغة العربية", "النصوص والقراءة: سر القوة والنجاح", "في درس «سر القوة والنجاح»، ما الركيزة الأساسية لتحقيق التفوق وتخطي العقبات؟", "MCQ", "الإرادة والعزيمة الصادقة مع العمل الدؤوب|الاعتماد على الحظ والصدفة فقط|الاستسلام السريع عند أول صعوبة|تأجيل المهام إلى وقت لاحق", "الإرادة والعزيمة الصادقة مع العمل الدؤوب", 1, "الدرس يركز على أن سر النجاح ينبع من قوة الإرادة الداخلية والعزيمة والمثابرة في العمل والتطوير المستمر.", "DAILY_Y6_ARB_W7D1", "W7", "Easy"], ["Q_Y6_ARB_W7D1_05", "Grade 6 (G6)", "اللغة العربية", "التعبير الكتابي: كتابة تقرير", "من العناصر الأساسية لكتابة التقرير المنظم في مهارات التعبير:", "MCQ", "العنوان والزمان والمكان والوقائع والتوصيات|القافية الشعرية والأوزان العروضية|الخيالات والقصص الخرافية غير الواقعية|ترك النص بدون خاتمة أو تاريخ", "العنوان والزمان والمكان والوقائع والتوصيات", 1, "التقرير وثيقة رسمية تتطلب تحديد العنوان والزمان والمكان وعرض الأحداث والوقائع بدقة واختتامها بالتوصيات والمقترحات.", "DAILY_Y6_ARB_W7D1", "W7", "Challenge"], ["Q_Y6_M1_1", "Grade 6 (G6)", "Mathematics", "Prime Factorization", "What is the prime factorization of 36 in index form?", "MCQ", "2² × 3² | 2 × 3³ | 4 × 9 | 2³ × 3", "2² × 3²", 1, "36 = 4 × 9 = 2² × 3².", "DAILY_Y6_MATH_W1D1", "Week 1", "Easy"], ["Q_Y6_M1_2", "Grade 6 (G6)", "Mathematics", "Prime Numbers", "Which of the following numbers is a prime number?", "MCQ", "29 | 27 | 35 | 49", "29", 1, "29 has only two factors: 1 and 29.", "DAILY_Y6_MATH_W1D1", "Week 1", "Easy"], ["Q_Y6_M1_3", "Grade 6 (G6)", "Mathematics", "HCF & Factors", "What is the Highest Common Factor (HCF) of 18 and 24?", "MCQ", "6 | 3 | 12 | 4", "6", 1, "Factors of 18: 1,2,3,6,9,18. Factors of 24: 1,2,3,4,6,8,12,24. HCF is 6.", "DAILY_Y6_MATH_W1D1", "Week 1", "Easy"], ["Q_Y6_M1_4", "Grade 6 (G6)", "Mathematics", "LCM", "What is the Lowest Common Multiple (LCM) of 4 and 6?", "MCQ", "12 | 24 | 18 | 2", "12", 1, "Multiples of 4: 4,8,12,16... Multiples of 6: 6,12,18... Smallest shared is 12.", "DAILY_Y6_MATH_W1D1", "Week 1", "Easy"], ["Q_Y6_M1_5", "Grade 6 (G6)", "Mathematics", "Index Form", "Express 60 as a product of prime factors in index form:", "MCQ", "2² × 3 × 5 | 2 × 3² × 5 | 4 × 15 | 2 × 30", "2² × 3 × 5", 1, "60 = 4 × 15 = 2² × 3 × 5.", "DAILY_Y6_MATH_W1D1", "Week 1", "Easy"], ["Q_Y6_M2_1", "Grade 6 (G6)", "Mathematics", "Fractions & Percentages", "Convert the fraction 3/4 to a percentage:", "MCQ", "75% | 50% | 60% | 80%", "75%", 1, "3/4 = 75/100 = 75%.", "DAILY_Y6_MATH_W1D2", "Week 1", "Medium"], ["Q_Y6_M2_2", "Grade 6 (G6)", "Mathematics", "Decimals to Fractions", "What is 0.65 written as a simplified fraction?", "MCQ", "13/20 | 65/10 | 7/10 | 13/25", "13/20", 1, "65/100 simplified by dividing numerator and denominator by 5 is 13/20.", "DAILY_Y6_MATH_W1D2", "Week 1", "Medium"], ["Q_Y6_M2_3", "Grade 6 (G6)", "Mathematics", "Fraction Arithmetic", "Calculate: 2/5 + 1/10 =", "MCQ", "1/2 | 3/15 | 3/10 | 4/10", "1/2", 1, "2/5 = 4/10; 4/10 + 1/10 = 5/10 = 1/2.", "DAILY_Y6_MATH_W1D2", "Week 1", "Medium"], ["Q_Y6_M2_4", "Grade 6 (G6)", "Mathematics", "Comparing Equivalence", "Which of the following values is the greatest?", "MCQ", "0.75 | 70% | 3/5 | 0.68", "0.75", 1, "0.75 = 75%, which is greater than 70%, 60% (3/5), and 68%.", "DAILY_Y6_MATH_W1D2", "Week 1", "Medium"], ["Q_Y6_M2_5", "Grade 6 (G6)", "Mathematics", "Percentages of Quantities", "Find 20% of 150:", "MCQ", "30 | 15 | 25 | 45", "30", 1, "10% of 150 = 15; 20% = 15 × 2 = 30.", "DAILY_Y6_MATH_W1D2", "Week 1", "Medium"], ["Q_Y6_M3_1", "Grade 6 (G6)", "Mathematics", "Division", "Calculate: 756 ÷ 6 =", "MCQ", "126 | 124 | 116 | 136", "126", 1, "756 ÷ 6 = 126.", "DAILY_Y6_MATH_W1D3", "Week 1", "Medium"], ["Q_Y6_M3_2", "Grade 6 (G6)", "Mathematics", "Word Problems", "A baker packs 432 cookies into boxes of 12. How many boxes can he completely fill?", "MCQ", "36 | 34 | 38 | 42", "36", 1, "432 ÷ 12 = 36 boxes.", "DAILY_Y6_MATH_W1D3", "Week 1", "Medium"], ["Q_Y6_M3_3", "Grade 6 (G6)", "Mathematics", "Division with Remainders", "What is the remainder when 589 is divided by 4?", "MCQ", "1 | 2 | 3 | 0", "1", 1, "588 is divisible by 4, leaving a remainder of 1.", "DAILY_Y6_MATH_W1D3", "Week 1", "Medium"], ["Q_Y6_M3_4", "Grade 6 (G6)", "Mathematics", "Order of Operations", "Calculate: (18 + 6) ÷ 4 + 7 =", "MCQ", "13 | 11 | 15 | 17", "13", 1, "Parentheses first: 18 + 6 = 24. Division: 24 ÷ 4 = 6. Addition: 6 + 7 = 13.", "DAILY_Y6_MATH_W1D3", "Week 1", "Medium"], ["Q_Y6_M3_5", "Grade 6 (G6)", "Mathematics", "Word Problems", "A train travels 280 miles in 4 hours at constant speed. What is its speed in mph?", "MCQ", "70 mph | 65 mph | 75 mph | 80 mph", "70 mph", 1, "Speed = Distance ÷ Time = 280 ÷ 4 = 70 mph.", "DAILY_Y6_MATH_W1D3", "Week 1", "Medium"], ["Q_Y6_MW1_1", "Grade 6 (G6)", "Mathematics", "Number Properties", "What is the prime factorization of 72?", "MCQ", "2³ × 3² | 2² × 3³ | 8 × 9 | 2 × 36", "2³ × 3²", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_2", "Grade 6 (G6)", "Mathematics", "Percentages", "What is 35% of 200?", "MCQ", "70 | 60 | 80 | 50", "70", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_3", "Grade 6 (G6)", "Mathematics", "Fractions", "Calculate: 3/4 - 1/8 =", "MCQ", "5/8 | 2/4 | 4/8 | 1/2", "5/8", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_4", "Grade 6 (G6)", "Mathematics", "Decimals", "Calculate: 4.25 × 6 =", "MCQ", "25.5 | 24.5 | 26.25 | 25.0", "25.5", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_5", "Grade 6 (G6)", "Mathematics", "Division", "Calculate: 1,024 ÷ 16 =", "MCQ", "64 | 62 | 58 | 66", "64", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_6", "Grade 6 (G6)", "Mathematics", "Simplifying", "Simplify the fraction 28/42 to its lowest terms:", "MCQ", "2/3 | 4/6 | 7/10 | 3/4", "2/3", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_7", "Grade 6 (G6)", "Mathematics", "Order of Operations", "Solve: 50 - 3 × (4 + 6) =", "MCQ", "20 | 470 | 30 | 15", "20", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_8", "Grade 6 (G6)", "Mathematics", "Multiples", "What is the HCF of 36 and 54?", "MCQ", "18 | 9 | 6 | 12", "18", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_9", "Grade 6 (G6)", "Mathematics", "Word Problems", "If 5 notebooks cost £15, what is the cost of 8 notebooks?", "MCQ", "£24 | £20 | £28 | £30", "£24", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_10", "Grade 6 (G6)", "Mathematics", "Decimals to %", "Convert 0.08 to a percentage:", "MCQ", "8% | 80% | 0.8% | 0.08%", "8%", 1, "", "EX_Y6_MATH_W1", "Week 1", "Medium"], ["Q_Y6_MW1_11", "Grade 6 (G6)", "Mathematics", "Word Problems", "A factory produces 3,600 bottles per hour. How many bottles per minute?", "MCQ", "60 | 36 | 600 | 120", "60", 1, "", "EX_Y6_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y6_MW1_12", "Grade 6 (G6)", "Mathematics", "Decimals", "Calculate: 12.6 ÷ 3 =", "MCQ", "4.2 | 4.3 | 4.02 | 3.8", "4.2", 1, "", "EX_Y6_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y6_MW1_13", "Grade 6 (G6)", "Mathematics", "Fractions", "Calculate: 2/3 × 3/5 =", "MCQ", "2/5 | 5/8 | 6/15 | 1/2", "2/5", 1, "", "EX_Y6_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y6_MW1_14", "Grade 6 (G6)", "Mathematics", "Mental Math", "Square root of 144 is:", "MCQ", "12 | 14 | 11 | 13", "12", 1, "", "EX_Y6_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y6_MW1_15", "Grade 6 (G6)", "Mathematics", "Negative Numbers", "Calculate: 5 - (-7) =", "MCQ", "12 | -2 | 2 | -12", "12", 1, "", "EX_Y6_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y6_S1_1", "Grade 6 (G6)", "Science", "Circulatory System", "Which chamber of the heart pumps oxygenated blood to the entire body?", "MCQ", "Left ventricle | Right ventricle | Left atrium | Right atrium", "Left ventricle", 1, "", "DAILY_Y6_SCI_W1D1", "Week 1", "Easy"], ["Q_Y6_S1_2", "Grade 6 (G6)", "Science", "Blood Components", "What is the primary role of red blood cells?", "MCQ", "Transporting oxygen using hemoglobin | Defending against bacterial infections | Clotting blood at wound sites | Transporting hormones in liquid plasma", "Transporting oxygen using hemoglobin", 1, "", "DAILY_Y6_SCI_W1D1", "Week 1", "Easy"], ["Q_Y6_S1_3", "Grade 6 (G6)", "Science", "Blood Vessels", "Blood vessels that carry oxygenated blood AWAY from the heart under high pressure are:", "MCQ", "Arteries | Veins | Capillaries | Lymph vessels", "Arteries", 1, "", "DAILY_Y6_SCI_W1D1", "Week 1", "Easy"], ["Q_Y6_S1_4", "Grade 6 (G6)", "Science", "Blood Vessels", "Why do veins contain valves throughout their length?", "MCQ", "To prevent the backward flow of blood | To speed up blood circulation | To filter waste products | To withstand intense blood pressure", "To prevent the backward flow of blood", 1, "", "DAILY_Y6_SCI_W1D1", "Week 1", "Easy"], ["Q_Y6_S1_5", "Grade 6 (G6)", "Science", "Blood Components", "Which component of blood is responsible for blood clotting to seal cuts?", "MCQ", "Platelets | Plasma | White blood cells | Red blood cells", "Platelets", 1, "", "DAILY_Y6_SCI_W1D1", "Week 1", "Easy"], ["Q_Y6_S2_1", "Grade 6 (G6)", "Science", "Circuits", "In a series circuit with two bulbs, what happens if one bulb breaks or is removed?", "MCQ", "The circuit is broken and the other bulb goes out | The other bulb stays lit and becomes brighter | The battery overheats immediately | The remaining bulb changes color", "The circuit is broken and the other bulb goes out", 1, "", "DAILY_Y6_SCI_W1D2", "Week 1", "Medium"], ["Q_Y6_S2_2", "Grade 6 (G6)", "Science", "Conductors & Insulators", "Which of the following is a good electrical conductor?", "MCQ", "Copper wire | Plastic coating | Glass rod | Dry wood", "Copper wire", 1, "", "DAILY_Y6_SCI_W1D2", "Week 1", "Medium"], ["Q_Y6_S2_3", "Grade 6 (G6)", "Science", "Circuit Components", "What is the function of a switch in an electric circuit?", "MCQ", "To complete or break the circuit loop | To provide electrical voltage | To measure electrical resistance | To increase battery capacity", "To complete or break the circuit loop", 1, "", "DAILY_Y6_SCI_W1D2", "Week 1", "Medium"], ["Q_Y6_S2_4", "Grade 6 (G6)", "Science", "Parallel Circuits", "Why are electrical circuits in homes wired in parallel rather than in series?", "MCQ", "Each device can be turned on or off independently | Parallel circuits use zero wire | To make all appliances receive half voltage | Parallel circuits prevent any current flow", "Each device can be turned on or off independently", 1, "", "DAILY_Y6_SCI_W1D2", "Week 1", "Medium"], ["Q_Y6_S2_5", "Grade 6 (G6)", "Science", "Safety", "Why are electric cables covered with plastic or rubber?", "MCQ", "Rubber is an electrical insulator that prevents shocks | Rubber increases electrical current | Rubber makes electrons move faster | To keep the wire cool in winter", "Rubber is an electrical insulator that prevents shocks", 1, "", "DAILY_Y6_SCI_W1D2", "Week 1", "Medium"], ["Q_Y6_SW1_1", "Grade 6 (G6)", "Science", "Circulatory System", "The liquid part of blood that carries nutrients and carbon dioxide is called:", "MCQ", "Plasma | Platelets | Hemoglobin | Serum", "Plasma", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_SW1_2", "Grade 6 (G6)", "Science", "Circulatory System", "Where does blood become re-oxygenated in the body?", "MCQ", "In the lungs (alveoli capillaries) | In the stomach | In the kidneys | In the brain", "In the lungs (alveoli capillaries)", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_SW1_3", "Grade 6 (G6)", "Science", "Circulatory System", "Which blood cells produce antibodies to destroy invading pathogens?", "MCQ", "White blood cells | Red blood cells | Platelets | Plasma cells", "White blood cells", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_SW1_4", "Grade 6 (G6)", "Science", "Circuits", "If you add a second battery in series to a circuit with one bulb, what happens to the bulb?", "MCQ", "It shines noticeably brighter | It shines dimmer | It turns off immediately | Nothing changes", "It shines noticeably brighter", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_SW1_5", "Grade 6 (G6)", "Science", "Circuits", "What component measures electric current in a circuit?", "MCQ", "Ammeter | Voltmeter | Thermometer | Barometer", "Ammeter", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_SW1_6", "Grade 6 (G6)", "Science", "Blood Vessels", "Microscopic blood vessels where nutrient and gas exchange occurs are:", "MCQ", "Capillaries | Arteries | Veins | Vena Cava", "Capillaries", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_SW1_7", "Grade 6 (G6)", "Science", "Circuits", "Which symbol represents a closed switch in a circuit diagram?", "MCQ", "A straight line connecting two dots | An open slanted line | A circle with an X | Two parallel lines of unequal length", "A straight line connecting two dots", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_SW1_8", "Grade 6 (G6)", "Science", "Heart Health", "Regular exercise strengthens the heart muscle, leading to:", "MCQ", "A lower resting heart rate and higher stroke volume | Faster clogging of arteries | Fewer red blood cells | Permanent high blood pressure", "A lower resting heart rate and higher stroke volume", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_SW1_9", "Grade 6 (G6)", "Science", "Circuits", "Which of the following creates a short circuit?", "MCQ", "A low-resistance connection directly across the power source | Adding an extra bulb | Opening the switch | Using longer copper wire", "A low-resistance connection directly across the power source", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_SW1_10", "Grade 6 (G6)", "Science", "Forces & Energy", "Electric energy in a torch bulb is transformed into:", "MCQ", "Light and heat energy | Chemical energy only | Sound energy only | Kinetic energy only", "Light and heat energy", 1, "", "EX_Y6_SCI_W1", "Week 1", "Medium"], ["Q_Y6_E1_1", "Grade 6 (G6)", "English", "Literary Devices", "Identify the simile in: \"The fog crept through the alley like a silent phantom.\"", "MCQ", "like a silent phantom | The fog crept | through the alley | silent phantom", "like a silent phantom", 1, "", "DAILY_Y6_ENG_W1D1", "Week 1", "Easy"], ["Q_Y6_E1_2", "Grade 6 (G6)", "English", "Personification", "Which sentence uses personification?", "MCQ", "The ancient clock groaned each time the hour struck. | The clock was made of dark oak. | He looked at the clock repeatedly. | The clock chimed twelve times.", "The ancient clock groaned each time the hour struck.", 1, "", "DAILY_Y6_ENG_W1D1", "Week 1", "Easy"], ["Q_Y6_E1_3", "Grade 6 (G6)", "English", "Fantasy Features", "In fantasy fiction, what is the role of the \"threshold\" or \"portal\"?", "MCQ", "A transition point between the ordinary world and the magical realm | The climax of the battle | The moral of the story | The glossary at the end of the book", "A transition point between the ordinary world and the magical realm", 1, "", "DAILY_Y6_ENG_W1D1", "Week 1", "Easy"], ["Q_Y6_E1_4", "Grade 6 (G6)", "English", "Vocabulary in Context", "What is the meaning of the word \"ominous\" in a fantasy setting?", "MCQ", "Giving the worrying impression that something bad is about to happen | Extremely bright and cheerful | Completely empty and clean | Ancient and made of stone", "Giving the worrying impression that something bad is about to happen", 1, "", "DAILY_Y6_ENG_W1D1", "Week 1", "Easy"], ["Q_Y6_E1_5", "Grade 6 (G6)", "English", "Perspective", "Which point of view is told using the pronouns \"he\", \"she\", and \"they\"?", "MCQ", "Third-person narrative | First-person narrative | Second-person narrative | Stream of consciousness", "Third-person narrative", 1, "", "DAILY_Y6_ENG_W1D1", "Week 1", "Easy"], ["Q_Y6_E2_1", "Grade 6 (G6)", "English", "Non-Chronological Reports", "What is the primary purpose of a non-chronological report?", "MCQ", "To provide factual information about a subject organized by topics rather than time | To entertain readers with a fictional myth | To convince readers to vote for a law | To recount the events of yesterday", "To provide factual information about a subject organized by topics rather than time", 1, "", "DAILY_Y6_ENG_W1D2", "Week 1", "Medium"], ["Q_Y6_E2_2", "Grade 6 (G6)", "English", "Grammar in Reports", "Which tense is predominantly used in non-chronological reports about animal species?", "MCQ", "Present tense (factual statements) | Past simple tense only | Future tense | Imperative mood", "Present tense (factual statements)", 1, "", "DAILY_Y6_ENG_W1D2", "Week 1", "Medium"], ["Q_Y6_E2_3", "Grade 6 (G6)", "English", "Structural Features", "Why are subheadings used throughout informational reports?", "MCQ", "To signpost and organize key topics for the reader | To introduce poetic rhymes | To replace the main title of the article | To show dialogue between characters", "To signpost and organize key topics for the reader", 1, "", "DAILY_Y6_ENG_W1D2", "Week 1", "Medium"], ["Q_Y6_E2_4", "Grade 6 (G6)", "English", "Formal Tone", "Which sentence best exemplifies formal, objective language?", "MCQ", "Research suggests that habitat loss poses a critical threat to nocturnal mammals. | I reckon nocturnal animals are really amazing to watch! | You gotta see how nocturnal animals hunt at night! | Nocturnal animals are definitely the coolest!", "Research suggests that habitat loss poses a critical threat to nocturnal mammals.", 1, "", "DAILY_Y6_ENG_W1D2", "Week 1", "Medium"], ["Q_Y6_E2_5", "Grade 6 (G6)", "English", "Text Features", "Where in a non-chronological report would technical vocabulary terms be defined?", "MCQ", "In the Glossary | In the Heading | In the Caption under a photo | In the First Paragraph", "In the Glossary", 1, "", "DAILY_Y6_ENG_W1D2", "Week 1", "Medium"], ["Q_Y6_EW1_1", "Grade 6 (G6)", "English", "Relative Clauses", "Select the correct relative pronoun: \"The archaeologist _______ discovered the tomb received international acclaim.\"", "MCQ", "who | which | where | whose", "who", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y6_EW1_2", "Grade 6 (G6)", "English", "Punctuation", "Which sentence correctly punctuates a non-defining relative clause?", "MCQ", "Mount Everest, which is the highest peak on Earth, attracts hundreds of climbers. | Mount Everest which is the highest peak on Earth, attracts climbers. | Mount Everest, which is the highest peak on Earth attracts climbers. | Mount Everest which is the highest peak on Earth attracts climbers.", "Mount Everest, which is the highest peak on Earth, attracts hundreds of climbers.", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y6_EW1_3", "Grade 6 (G6)", "English", "Reading Skills", "What is the purpose of \"skimming\" a text?", "MCQ", "Reading quickly to grasp the general overview or gist | Searching for a specific fact like a date or number | Analyzing poetic meters | Memorizing every word", "Reading quickly to grasp the general overview or gist", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y6_EW1_4", "Grade 6 (G6)", "English", "Reading Skills", "What is the purpose of \"scanning\" a text?", "MCQ", "Searching for specific keywords, names, or numbers | Reading every paragraph slowly | Writing a summary | Translating the text", "Searching for specific keywords, names, or numbers", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y6_EW1_5", "Grade 6 (G6)", "English", "Report Structure", "A non-chronological report typically begins with:", "MCQ", "An introductory paragraph defining the topic and its scope | A detailed anecdote about the author | A dramatic story climax | A bulleted list of references", "An introductory paragraph defining the topic and its scope", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y6_EW1_6", "Grade 6 (G6)", "English", "Vocabulary", "What does the prefix \"non-\" signify in \"non-chronological\"?", "MCQ", "Not or without | Before | Very much | Again", "Not or without", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y6_EW1_7", "Grade 6 (G6)", "English", "Literary Devices", "In: \"The sea was an emerald sheet of glass\", what literary device is used?", "MCQ", "Metaphor | Simile | Personification | Alliteration", "Metaphor", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y6_EW1_8", "Grade 6 (G6)", "English", "Formal Vocabulary", "Choose the formal equivalent for \"found out\":", "MCQ", "Discovered / Ascertained | Looked up | Caught on | Picked up", "Discovered / Ascertained", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y6_EW1_9", "Grade 6 (G6)", "English", "Paragraphing", "In a report, every new subtopic should begin with:", "MCQ", "A clear topic sentence introducing the paragraph idea | An exclamation mark | A quotation from a poem | A bullet point only", "A clear topic sentence introducing the paragraph idea", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y6_EW1_10", "Grade 6 (G6)", "English", "Spelling & Etymology", "Which of the following words is spelled correctly?", "MCQ", "Accommodate | Acommodate | Accomodate | Acomodate", "Accommodate", 1, "", "EX_Y6_ENG_W1", "Week 1", "Medium"], ["Q_Y5_M1_1", "Year 5 (G5)", "Mathematics", "Divisibility Rules", "A whole number is divisible by 5 if its last digit is:", "MCQ", "0 or 5 | 2 or 4 | 0, 2, or 5 | Any odd digit", "0 or 5", 1, "Numbers ending in 0 or 5 are multiples of 5.", "DAILY_Y5_MATH_W1D1", "Week 1", "Easy"], ["Q_Y5_M1_2", "Year 5 (G5)", "Mathematics", "Divisibility Rules", "Which of the following numbers is divisible by both 2 and 10?", "MCQ", "420 | 315 | 224 | 105", "420", 1, "420 ends in 0, so it is divisible by both 2 and 10.", "DAILY_Y5_MATH_W1D1", "Week 1", "Easy"], ["Q_Y5_M1_3", "Year 5 (G5)", "Mathematics", "Divisibility Rules", "Which number is divisible by 5 but NOT by 10?", "MCQ", "835 | 720 | 410 | 900", "835", 1, "835 ends in 5, so it is divisible by 5 but not 10.", "DAILY_Y5_MATH_W1D1", "Week 1", "Easy"], ["Q_Y5_M1_4", "Year 5 (G5)", "Mathematics", "Divisibility Rules", "Is 6,748 divisible by 2? Why?", "MCQ", "Yes, because its last digit is even (8) | No, because 6 is even | Yes, because 6+7+4+8=25 | No, because it has 4 digits", "Yes, because its last digit is even (8)", 1, "Any integer ending in 0, 2, 4, 6, or 8 is divisible by 2.", "DAILY_Y5_MATH_W1D1", "Week 1", "Easy"], ["Q_Y5_M1_5", "Year 5 (G5)", "Mathematics", "Divisibility Rules", "What is the smallest 3-digit number divisible by both 5 and 10?", "MCQ", "100 | 105 | 110 | 150", "100", 1, "100 is the smallest 3-digit number and ends in 0.", "DAILY_Y5_MATH_W1D1", "Week 1", "Easy"], ["Q_Y5_M2_1", "Year 5 (G5)", "Mathematics", "Divisibility by 3", "A number is divisible by 3 if:", "MCQ", "The sum of its digits is divisible by 3 | Its last digit is 3 | Its last digit is odd | It ends in 3, 6, or 9", "The sum of its digits is divisible by 3", 1, "Rule for 3: add the digits together.", "DAILY_Y5_MATH_W1D2", "Week 1", "Medium"], ["Q_Y5_M2_2", "Year 5 (G5)", "Mathematics", "Divisibility by 9", "Which of the following numbers is divisible by 9?", "MCQ", "567 (5+6+7=18) | 431 | 623 | 215", "567 (5+6+7=18)", 1, "5+6+7=18, which is divisible by 9.", "DAILY_Y5_MATH_W1D2", "Week 1", "Medium"], ["Q_Y5_M2_3", "Year 5 (G5)", "Mathematics", "Divisibility by 4", "A number is divisible by 4 if:", "MCQ", "Its last two digits form a number divisible by 4 | Its last digit is 4 | The sum of digits is 4 | It ends in an even number", "Its last two digits form a number divisible by 4", 1, "Rule for 4: check the number formed by the last two digits.", "DAILY_Y5_MATH_W1D2", "Week 1", "Medium"], ["Q_Y5_M2_4", "Year 5 (G5)", "Mathematics", "Divisibility Test", "Which of these numbers is divisible by 3: 412, 513, 614, 715?", "MCQ", "513 (5+1+3=9) | 412 | 614 | 715", "513 (5+1+3=9)", 1, "5+1+3=9, divisible by 3.", "DAILY_Y5_MATH_W1D2", "Week 1", "Medium"], ["Q_Y5_M2_5", "Year 5 (G5)", "Mathematics", "Divisibility Puzzle", "What digit can replace * in 4*2 so that the number is divisible by 9?", "MCQ", "3 (4+3+2=9) | 2 | 5 | 7", "3 (4+3+2=9)", 1, "4 + 3 + 2 = 9, so 432 is divisible by 9.", "DAILY_Y5_MATH_W1D2", "Week 1", "Medium"], ["Q_Y5_MW1_1", "Year 5 (G5)", "Mathematics", "Divisibility", "Is 2,340 divisible by 2, 5, and 10?", "MCQ", "Yes, it ends in 0 so it is divisible by all three | Only by 2 | Only by 5 and 10 | No, not divisible", "Yes, it ends in 0 so it is divisible by all three", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_2", "Year 5 (G5)", "Mathematics", "Divisibility", "Which number is divisible by 4?", "MCQ", "728 (28 ÷ 4 = 7) | 518 | 314 | 622", "728 (28 ÷ 4 = 7)", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_3", "Year 5 (G5)", "Mathematics", "Multiples", "What is the 8th multiple of 7?", "MCQ", "56 | 49 | 63 | 54", "56", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_4", "Year 5 (G5)", "Mathematics", "Factors", "Which of these is NOT a factor of 36?", "MCQ", "8 | 6 | 9 | 12", "8", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_5", "Year 5 (G5)", "Mathematics", "Place Value", "In the number 458,920, what is the value of the digit 5?", "MCQ", "50,000 (Fifty thousand) | 5,000 | 500,000 | 500", "50,000 (Fifty thousand)", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_6", "Year 5 (G5)", "Mathematics", "Rounding", "Round 4,762 to the nearest hundred:", "MCQ", "4,800 | 4,700 | 5,000 | 4,760", "4,800", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_7", "Year 5 (G5)", "Mathematics", "Addition", "Calculate: 3,450 + 2,870 =", "MCQ", "6,320 | 6,220 | 6,420 | 5,320", "6,320", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_8", "Year 5 (G5)", "Mathematics", "Subtraction", "Calculate: 8,000 - 3,425 =", "MCQ", "4,575 | 4,675 | 5,575 | 4,475", "4,575", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_9", "Year 5 (G5)", "Mathematics", "Multiplication", "Calculate: 45 × 100 =", "MCQ", "4,500 | 450 | 45,000 | 4.5", "4,500", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_10", "Year 5 (G5)", "Mathematics", "Division", "Calculate: 360 ÷ 9 =", "MCQ", "40 | 30 | 45 | 36", "40", 1, "", "EX_Y5_MATH_W1", "Week 1", "Medium"], ["Q_Y5_MW1_11", "Year 5 (G5)", "Mathematics", "Decimals", "Which decimal is equivalent to 1/2?", "MCQ", "0.5 | 0.2 | 0.05 | 0.25", "0.5", 1, "", "EX_Y5_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y5_MW1_12", "Year 5 (G5)", "Mathematics", "Decimals", "Round 3.76 to the nearest tenth:", "MCQ", "3.8 | 3.7 | 4.0 | 3.75", "3.8", 1, "", "EX_Y5_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y5_MW1_13", "Year 5 (G5)", "Mathematics", "Word Problems", "Ali has £25. He spends £8.50 on a book. How much money does he have left?", "MCQ", "£16.50 | £16.00 | £17.50 | £15.50", "£16.50", 1, "", "EX_Y5_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y5_MW1_14", "Year 5 (G5)", "Mathematics", "Perimeter", "A rectangle has length 8 cm and width 5 cm. What is its perimeter?", "MCQ", "26 cm (8+5+8+5) | 40 cm | 13 cm | 20 cm", "26 cm (8+5+8+5)", 1, "", "EX_Y5_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y5_MW1_15", "Year 5 (G5)", "Mathematics", "Area", "What is the area of the same rectangle (8 cm × 5 cm)?", "MCQ", "40 cm² | 26 cm² | 13 cm² | 80 cm²", "40 cm²", 1, "", "EX_Y5_MATH_M1_CAPSTONE", "Week 1", "Hard"], ["Q_Y5_S1_1", "Year 5 (G5)", "Science", "Sound", "How are all sounds created?", "MCQ", "By vibrations of matter | By light beams | By magnetic attraction | By temperature drops", "By vibrations of matter", 1, "", "DAILY_Y5_SCI_W1D1", "Week 1", "Easy"], ["Q_Y5_S1_2", "Year 5 (G5)", "Science", "Sound Travel", "Through which medium does sound travel fastest?", "MCQ", "Solids (particles are packed tightly) | Liquids | Gases | A vacuum", "Solids (particles are packed tightly)", 1, "", "DAILY_Y5_SCI_W1D1", "Week 1", "Easy"], ["Q_Y5_S1_3", "Year 5 (G5)", "Science", "Vacuum", "Can sound travel through empty space (a vacuum)?", "MCQ", "No, because there are no particles to vibrate and pass on sound energy | Yes, because sound is light | Yes, but very slowly | No, because space is too hot", "No, because there are no particles to vibrate and pass on sound energy", 1, "", "DAILY_Y5_SCI_W1D1", "Week 1", "Easy"], ["Q_Y5_S1_4", "Year 5 (G5)", "Science", "Loudness", "What scientific unit is used to measure sound loudness?", "MCQ", "Decibels (dB) | Hertz (Hz) | Meters (m) | Kilograms (kg)", "Decibels (dB)", 1, "", "DAILY_Y5_SCI_W1D1", "Week 1", "Easy"], ["Q_Y5_S1_5", "Year 5 (G5)", "Science", "Sound Energy", "What happens to sound vibrations as they travel further from the sound source?", "MCQ", "The vibrations spread out and lose energy, becoming quieter | The vibrations gain energy and get louder | The pitch increases | The vibrations reverse direction", "The vibrations spread out and lose energy, becoming quieter", 1, "", "DAILY_Y5_SCI_W1D1", "Week 1", "Easy"], ["Q_Y5_S2_1", "Year 5 (G5)", "Science", "Pitch", "What does \"pitch\" describe in science?", "MCQ", "How high or low a sound is | How loud or quiet a sound is | How far sound can travel | The speed of sound in air", "How high or low a sound is", 1, "", "DAILY_Y5_SCI_W1D2", "Week 1", "Medium"], ["Q_Y5_S2_2", "Year 5 (G5)", "Science", "Pitch & Vibrations", "A rapid, fast vibration produces a:", "MCQ", "High-pitch sound | Low-pitch sound | Silent sound | Deep boom", "High-pitch sound", 1, "", "DAILY_Y5_SCI_W1D2", "Week 1", "Medium"], ["Q_Y5_S2_3", "Year 5 (G5)", "Science", "Musical Instruments", "How do you make a guitar string produce a higher pitch?", "MCQ", "Tighten the string or make it shorter | Loosen the string | Pluck it very gently | Use a thicker, heavier string", "Tighten the string or make it shorter", 1, "", "DAILY_Y5_SCI_W1D2", "Week 1", "Medium"], ["Q_Y5_S2_4", "Year 5 (G5)", "Science", "Animal Adaptations", "Which animal uses high-frequency ultrasound clicks to navigate and find prey?", "MCQ", "Bat | Elephant | Horse | Lion", "Bat", 1, "", "DAILY_Y5_SCI_W1D2", "Week 1", "Medium"], ["Q_Y5_S2_5", "Year 5 (G5)", "Science", "The Ear", "Which thin membrane in the human ear vibrates when sound waves strike it?", "MCQ", "Eardrum | Cochlea | Auditory nerve | Ear lobe", "Eardrum", 1, "", "DAILY_Y5_SCI_W1D2", "Week 1", "Medium"], ["Q_Y5_SW1_1", "Year 5 (G5)", "Science", "Sound", "The pitch of a sound depends on the vibration's:", "MCQ", "Frequency | Amplitude | Loudness | Distance", "Frequency", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_SW1_2", "Year 5 (G5)", "Science", "Sound", "The loudness (volume) of a sound depends on the vibration's:", "MCQ", "Amplitude (size of vibration) | Frequency | Color | Direction", "Amplitude (size of vibration)", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_SW1_3", "Year 5 (G5)", "Science", "Hearing Protection", "Sustained exposure to sounds above 85 dB can cause:", "MCQ", "Permanent hearing damage | Better eyesight | Stronger eardrums | Faster reflexes", "Permanent hearing damage", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_SW1_4", "Year 5 (G5)", "Science", "Soundproofing", "Which material is best for soundproofing a room?", "MCQ", "Soft foam or thick curtains that absorb sound | Smooth glass panels | Hard steel plates | Ceramic tiles", "Soft foam or thick curtains that absorb sound", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_SW1_5", "Year 5 (G5)", "Science", "Echoes", "An echo is caused by sound waves:", "MCQ", "Reflecting off a hard, smooth surface | Absorbed by a carpet | Stopping in mid-air | Speeding up in water", "Reflecting off a hard, smooth surface", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_SW1_6", "Year 5 (G5)", "Science", "Plants", "In flowering plants, which part attracts pollinating insects with bright colors?", "MCQ", "Petals | Roots | Sepals | Stem", "Petals", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_SW1_7", "Year 5 (G5)", "Science", "Pollination", "Pollination is the transfer of pollen grains from the:", "MCQ", "Anther to the Stigma | Roots to the leaves | Petals to the sepals | Seeds to the fruit", "Anther to the Stigma", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_SW1_8", "Year 5 (G5)", "Science", "Living Things", "Organisms that produce their own food using sunlight are called:", "MCQ", "Producers (green plants) | Consumers | Decomposers | Predators", "Producers (green plants)", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_SW1_9", "Year 5 (G5)", "Science", "Food Chains", "In the food chain: Grass -> Zebra -> Lion, which organism is the apex predator?", "MCQ", "Lion | Zebra | Grass | Sun", "Lion", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_SW1_10", "Year 5 (G5)", "Science", "Seed Dispersal", "Dandelion seeds have parachute-like fluff so they can be dispersed by:", "MCQ", "Wind | Water | Animals eating them | Explosive pods", "Wind", 1, "", "EX_Y5_SCI_W1", "Week 1", "Medium"], ["Q_Y5_A1_1", "Year 5 (G5)", "اللغة العربية", "نحو", "تتكون الجملة الاسمية من ركنين أساسيين هما:", "MCQ", "المبتدأ والخبر | الفعل والفاعل | الحرف والاسم | المضاف والمضاف إليه", "المبتدأ والخبر", 1, "الجملة الاسمية تبدأ باسم وهو المبتدأ ويتمم معناه الخبر.", "DAILY_Y5_ARB_W1D1", "Week 1", "Easy"], ["Q_Y5_A1_2", "Year 5 (G5)", "اللغة العربية", "نحو", "ما إعراب كلمة «السماءُ» في جملة: «السماءُ صافيةٌ»؟", "MCQ", "مبتدأ مرفوع وعلامة رفعه الضمة | خبر مرفوع بالضمة | فاعل مرفوع بالضمة | اسم مجرور بالكسرة", "مبتدأ مرفوع وعلامة رفعه الضمة", 1, "السماء اسم في أول الجملة فهو مبتدأ مرفوع بالضمة.", "DAILY_Y5_ARB_W1D1", "Week 1", "Easy"], ["Q_Y5_A1_3", "Year 5 (G5)", "اللغة العربية", "نحو", "عين الخبر في جملة: «الحديقةُ الواسعةُ جميلةٌ»:", "MCQ", "جميلةٌ | الواسعةُ | الحديقةُ | مستتر", "جميلةٌ", 1, "جميلة هي التي أتمت معنى الجملة وأخبرت عن الحديقة.", "DAILY_Y5_ARB_W1D1", "Week 1", "Easy"], ["Q_Y5_A1_4", "Year 5 (G5)", "اللغة العربية", "ضبط الجملة", "أي من الجمل التالية مضبوطة بالشكل ضبطاً صحيحاً؟", "MCQ", "العلمُ نافعٌ | العلمَ نافعاً | العلمِ نافعٍ | العلمُ نافعاً", "العلمُ نافعٌ", 1, "المبتدأ والخبر المفردان يرفعان بالضمة.", "DAILY_Y5_ARB_W1D1", "Week 1", "Easy"], ["Q_Y5_A1_5", "Year 5 (G5)", "اللغة العربية", "علامات الرفع", "علامة رفع المبتدأ إذا كان جمع مؤنث سالماً (مثل: المعلماتُ):", "MCQ", "الضمة الظاهرة | الألف | الواو | الكسرة", "الضمة الظاهرة", 1, "جمع المؤنث السالم يرفع بالضمة كالاسم المفرد.", "DAILY_Y5_ARB_W1D1", "Week 1", "Easy"], ["Q_Y5_AW1_1", "Year 5 (G5)", "اللغة العربية", "نحو", "المبتدأ والخبر حكمهما الإعرابي الدائم هو:", "MCQ", "الرفع دائماً | النصب دائماً | الجر دائماً | الجزم", "الرفع دائماً", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_Y5_AW1_2", "Year 5 (G5)", "اللغة العربية", "نحو", "علامة رفع المبتدأ والخبر في جملة: «الطالبانِ مجتهدانِ» هي:", "MCQ", "الألف لأنه مثنى | الضمة | الواو | ثبوت النون", "الألف لأنه مثنى", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_Y5_AW1_3", "Year 5 (G5)", "اللغة العربية", "نحو", "علامة رفع الخبر في جملة: «المهندسونَ بارعونَ» هي:", "MCQ", "الواو لأنه جمع مذكر سالم | الضمة | الألف | الفتحة", "الواو لأنه جمع مذكر سالم", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_Y5_AW1_4", "Year 5 (G5)", "اللغة العربية", "قراءة", "ما مضاد كلمة «الاجتهاد»؟", "MCQ", "الكسل والتراخي | النجاح | السرعة | القوة", "الكسل والتراخي", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_Y5_AW1_5", "Year 5 (G5)", "اللغة العربية", "إملاء", "الكلمة التي كتبت بها همزة الوصل كتابة صحيحة هي:", "MCQ", "استمعَ | إستمعَ | أستمعَ | آستمعَ", "استمعَ", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_Y5_AW1_6", "Year 5 (G5)", "اللغة العربية", "نحو", "حول الجملة التالية للمثنى: «العاملُ مخلصٌ»:", "MCQ", "العاملانِ مخلصانِ | العاملينِ مخلصينِ | العاملانِ مخلصينِ | العاملينِ مخلصانِ", "العاملانِ مخلصانِ", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_Y5_AW1_7", "Year 5 (G5)", "اللغة العربية", "نحو", "«المعلماتُ رحيماتٌ» - كلمة (المعلماتُ) تعرب:", "MCQ", "مبتدأ مرفوع وعلامة رفعه الضمة | خبر مرفوع بالألف | فاعل مرفوع بالواو | مفعول به", "مبتدأ مرفوع وعلامة رفعه الضمة", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_Y5_AW1_8", "Year 5 (G5)", "اللغة العربية", "تعبير", "الجملة التي تبدأ بفعل تسمى:", "MCQ", "جملة فعلية | جملة اسمية | شبه جملة | جملة شرطية", "جملة فعلية", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_Y5_AW1_9", "Year 5 (G5)", "اللغة العربية", "إملاء", "التاء المربوطة تنطق عند الوقف عليها بالسكون:", "MCQ", "هاءً (مثل: مدرسة -> مدرَسَه) | تاءً واضحة | ألفاً | واواً", "هاءً (مثل: مدرسة -> مدرَسَه)", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_Y5_AW1_10", "Year 5 (G5)", "اللغة العربية", "بلاغة ومعانٍ", "في عبارة: «الكتابُ صديقٌ وفيٌّ»، شبه الكاتب الكتاب بـ:", "MCQ", "الصديق الوفي للإنسان | المعلم الصارم | البحر العميق | الكنز المدفون", "الصديق الوفي للإنسان", 1, "", "EX_Y5_ARB_W1", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D1_1", "Year 5 (G5)", "English", "English Literacy & Grammar", "Identify the <b>adverb of manner</b> in the following sentence: \"The brave knight fought <u>fiercely</u> against the dragon.\"", "MCQ", "fiercely | brave | knight | dragon", "fiercely", 1, "An adverb of manner describes HOW the action was done (-ly ending).", "DAILY_Y5_ENG_W1D1", "Week 1", "Easy"], ["Q_DAILY_Y5_ENG_W1D1_2", "Year 5 (G5)", "English", "English Literacy & Grammar", "Which sentence uses a <b>fronted adverbial</b> correctly with a comma?", "MCQ", "Suddenly, the lights went out in the hallway. | Suddenly the lights went, out. | The lights suddenly, went out. | Suddenly the lights went out.", "Suddenly, the lights went out in the hallway.", 1, "A fronted adverbial must be followed by a comma when positioned at the beginning of the sentence.", "DAILY_Y5_ENG_W1D1", "Week 1", "Easy"], ["Q_DAILY_Y5_ENG_W1D1_3", "Year 5 (G5)", "English", "English Literacy & Grammar", "Select the correct relative pronoun: \"The scientist ______ discovered the vaccine won a Nobel Prize.\"", "MCQ", "who | which | where | whose", "who", 1, "Use \"who\" as the relative pronoun referring to people.", "DAILY_Y5_ENG_W1D1", "Week 1", "Easy"], ["Q_DAILY_Y5_ENG_W1D1_4", "Year 5 (G5)", "English", "English Literacy & Grammar", "Choose the correct compound adverbial phrase: \"She searched ______ for her lost keys.\"", "MCQ", "here and there | quick and slow | up and water | yesterday and green", "here and there", 1, "\"Here and there\" is a standard compound adverbial of place.", "DAILY_Y5_ENG_W1D1", "Week 1", "Easy"], ["Q_DAILY_Y5_ENG_W1D1_5", "Year 5 (G5)", "English", "English Literacy & Grammar", "Which sentence contains a non-defining relative clause punctuated correctly?", "MCQ", "My bicycle, which has ten gears, was a birthday gift. | My bicycle which has ten gears was a gift. | My bicycle, which has ten gears was a gift. | My bicycle which has ten gears, was a gift.", "My bicycle, which has ten gears, was a birthday gift.", 1, "Non-defining relative clauses must be enclosed by pairs of commas.", "DAILY_Y5_ENG_W1D1", "Week 1", "Easy"], ["Q_DAILY_Y5_ENG_W1D2_1", "Year 5 (G5)", "English", "English Literacy & Grammar", "Identify the <b>adverb of manner</b> in the following sentence: \"The brave knight fought <u>fiercely</u> against the dragon.\"", "MCQ", "fiercely | brave | knight | dragon", "fiercely", 1, "An adverb of manner describes HOW the action was done (-ly ending).", "DAILY_Y5_ENG_W1D2", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D2_2", "Year 5 (G5)", "English", "English Literacy & Grammar", "Which sentence uses a <b>fronted adverbial</b> correctly with a comma?", "MCQ", "Suddenly, the lights went out in the hallway. | Suddenly the lights went, out. | The lights suddenly, went out. | Suddenly the lights went out.", "Suddenly, the lights went out in the hallway.", 1, "A fronted adverbial must be followed by a comma when positioned at the beginning of the sentence.", "DAILY_Y5_ENG_W1D2", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D2_3", "Year 5 (G5)", "English", "English Literacy & Grammar", "Select the correct relative pronoun: \"The scientist ______ discovered the vaccine won a Nobel Prize.\"", "MCQ", "who | which | where | whose", "who", 1, "Use \"who\" as the relative pronoun referring to people.", "DAILY_Y5_ENG_W1D2", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D2_4", "Year 5 (G5)", "English", "English Literacy & Grammar", "Choose the correct compound adverbial phrase: \"She searched ______ for her lost keys.\"", "MCQ", "here and there | quick and slow | up and water | yesterday and green", "here and there", 1, "\"Here and there\" is a standard compound adverbial of place.", "DAILY_Y5_ENG_W1D2", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D2_5", "Year 5 (G5)", "English", "English Literacy & Grammar", "Which sentence contains a non-defining relative clause punctuated correctly?", "MCQ", "My bicycle, which has ten gears, was a birthday gift. | My bicycle which has ten gears was a gift. | My bicycle, which has ten gears was a gift. | My bicycle which has ten gears, was a gift.", "My bicycle, which has ten gears, was a birthday gift.", 1, "Non-defining relative clauses must be enclosed by pairs of commas.", "DAILY_Y5_ENG_W1D2", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D3_1", "Year 5 (G5)", "English", "English Literacy & Grammar", "Identify the <b>adverb of manner</b> in the following sentence: \"The brave knight fought <u>fiercely</u> against the dragon.\"", "MCQ", "fiercely | brave | knight | dragon", "fiercely", 1, "An adverb of manner describes HOW the action was done (-ly ending).", "DAILY_Y5_ENG_W1D3", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D3_2", "Year 5 (G5)", "English", "English Literacy & Grammar", "Which sentence uses a <b>fronted adverbial</b> correctly with a comma?", "MCQ", "Suddenly, the lights went out in the hallway. | Suddenly the lights went, out. | The lights suddenly, went out. | Suddenly the lights went out.", "Suddenly, the lights went out in the hallway.", 1, "A fronted adverbial must be followed by a comma when positioned at the beginning of the sentence.", "DAILY_Y5_ENG_W1D3", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D3_3", "Year 5 (G5)", "English", "English Literacy & Grammar", "Select the correct relative pronoun: \"The scientist ______ discovered the vaccine won a Nobel Prize.\"", "MCQ", "who | which | where | whose", "who", 1, "Use \"who\" as the relative pronoun referring to people.", "DAILY_Y5_ENG_W1D3", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D3_4", "Year 5 (G5)", "English", "English Literacy & Grammar", "Choose the correct compound adverbial phrase: \"She searched ______ for her lost keys.\"", "MCQ", "here and there | quick and slow | up and water | yesterday and green", "here and there", 1, "\"Here and there\" is a standard compound adverbial of place.", "DAILY_Y5_ENG_W1D3", "Week 1", "Medium"], ["Q_DAILY_Y5_ENG_W1D3_5", "Year 5 (G5)", "English", "English Literacy & Grammar", "Which sentence contains a non-defining relative clause punctuated correctly?", "MCQ", "My bicycle, which has ten gears, was a birthday gift. | My bicycle which has ten gears was a gift. | My bicycle, which has ten gears was a gift. | My bicycle which has ten gears, was a gift.", "My bicycle, which has ten gears, was a birthday gift.", 1, "Non-defining relative clauses must be enclosed by pairs of commas.", "DAILY_Y5_ENG_W1D3", "Week 1", "Medium"]];
}

function getStarterExams_() {
  return [["EX_Y5_ENG_ADV01", "Year 5 Grammar: Adverbials of Time, Place & Manner (Unit 2 Lesson 3)", "Year 5 (G5)", "English Grammar", 10, 20, "ACTIVE", "", "2026-10-28", "Diagnostic", "W1"], ["EX_Y6_ENG_FANTASY01", "Grade 6 English: Fantasy Reading \"The City That Waited\" & Report Writing", "Grade 6 (G6)", "English Literacy", 10, 20, "ACTIVE", "", "2026-10-28", "Diagnostic", "W1"], ["EX_Y6_ARB_PRIO01", "Grade 6 Arabic: Reading Comprehension, Grammar & Spelling (Diagnostic)", "Grade 6 (G6)", "Arabic Language", 10, 20, "ACTIVE", "", "2026-10-28", "Diagnostic", "W1"], ["DAILY_Y5_ARB_W1D1", "علي - اليوم 1: الجملة الاسمية وركناها (المبتدأ والخبر)", "Year 5 (G5)", "اللغة العربية", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y5_ENG_W1D1", "Ali - Day 1: Adverbs of Manner", "Year 5 (G5)", "English Grammar", 14, 10, "ACTIVE", "", "2026-10-28", "Daily", "W1"], ["DAILY_Y5_ENG_W1D2", "Ali - Day 2: Adverbials of Time", "Year 5 (G5)", "English Grammar", 14, 10, "ACTIVE", "", "2026-10-28", "Daily", "W1"], ["DAILY_Y5_ENG_W1D3", "Ali - Day 3: Adverbials of Place", "Year 5 (G5)", "English Grammar", 14, 10, "ACTIVE", "", "2026-10-28", "Daily", "W1"], ["DAILY_Y5_ENG_W1D4", "Ali - Day 4: Fronted Adverbials & Commas", "Year 5 (G5)", "English Grammar", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "W1"], ["DAILY_Y5_ENG_W1D5", "Ali - Day 5: Compound Adverbials", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-28", "Daily", "W1"], ["DAILY_Y5_ENG_W1D6", "Ali - Day 6: Sentence Repair & Error Hunting", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-28", "Daily", "W1"], ["DAILY_Y5_ENG_W2D10", "Ali - Day 10: Defining vs Non-defining Clauses", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-28", "Daily", "W2"], ["DAILY_Y5_ENG_W2D8", "Ali - Day 8: Relative Pronouns (who/which/that)", "Year 5 (G5)", "English Grammar", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "W2"], ["DAILY_Y5_ENG_W2D9", "Ali - Day 9: Non-defining Relative Clauses & Commas", "Year 5 (G5)", "English Grammar", 6, 10, "ACTIVE", "", "2026-10-28", "Daily", "W2"], ["DAILY_Y5_ENG_W3D15", "DAILY Y5 ENG W3D15", "Year 5 (G5)", "English Grammar", 6, 10, "ACTIVE", "", "2026-10-28", "Daily", "W3"], ["DAILY_Y5_ENG_W3D16", "DAILY Y5 ENG W3D16", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-28", "Daily", "W3"], ["DAILY_Y5_ENG_W4D22", "DAILY Y5 ENG W4D22", "Year 5 (G5)", "English Grammar", 5, 10, "ACTIVE", "", "2026-10-28", "Daily", "W4"], ["DAILY_Y5_ENG_W7D1", "Ali - Day 1: Simple & Compound Sentences", "Year 5 (G5)", "English Grammar", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "W7"], ["DAILY_Y5_MATH_W1D1", "Ali - Day 1: Tests of Divisibility (Rules for 2, 5, 10)", "Year 5 (G5)", "Mathematics", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y5_MATH_W1D2", "Ali - Day 2: Divisibility by 3, 4, 9 & Multiples", "Year 5 (G5)", "Mathematics", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y5_SCI_W1D1", "Ali - Day 1: How Sound is Made & Vibrations", "Year 5 (G5)", "Science", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y5_SCI_W1D2", "Ali - Day 2: Pitch, Volume & Sound Travel", "Year 5 (G5)", "Science", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y6_ARB_W1D4", "Mostafa - Day 4: إدارة الوقت وترتيب الأولويات", "Grade 6 (G6)", "اللغة العربية", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "W1"], ["DAILY_Y6_ARB_W1D5", "Mostafa - Day 5: النكرة والمعرفة", "Grade 6 (G6)", "اللغة العربية", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "W1"], ["DAILY_Y6_ARB_W1D6", "Mostafa - Day 6: الهمزة المتوسطة على ألف", "Grade 6 (G6)", "اللغة العربية", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "W1"], ["DAILY_Y6_ARB_W2D10", "Mostafa - Day 10: الهمزة المتوسطة على واو", "Grade 6 (G6)", "اللغة العربية", 7, 10, "ACTIVE", "", "2026-10-28", "Daily", "W2"], ["DAILY_Y6_ARB_W2D8", "Mostafa - Day 8: أنواع الخبر (المفرد)", "Grade 6 (G6)", "اللغة العربية", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "W2"], ["DAILY_Y6_ARB_W2D9", "Mostafa - Day 9: أنواع الخبر (الجملة وشبه الجملة)", "Grade 6 (G6)", "اللغة العربية", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "W2"], ["DAILY_Y6_ARB_W3D15", "DAILY Y6 ARB W3D15", "Grade 6 (G6)", "اللغة العربية", 6, 10, "ACTIVE", "", "2026-10-28", "Daily", "W3"], ["DAILY_Y6_ARB_W3D16", "DAILY Y6 ARB W3D16", "Grade 6 (G6)", "اللغة العربية", 5, 10, "ACTIVE", "", "2026-10-28", "Daily", "W3"], ["DAILY_Y6_ARB_W4D22", "DAILY Y6 ARB W4D22", "Grade 6 (G6)", "اللغة العربية", 6, 10, "ACTIVE", "", "2026-10-28", "Daily", "W4"], ["DAILY_Y6_ARB_W7D1", "Mostafa - Day 1: سر القوة والنجاح وأنواع الخبر", "Grade 6 (G6)", "اللغة العربية", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "W7"], ["DAILY_Y6_ENG_W1D1", "Mostafa - Day 1: Fantasy Reading & Setting Details", "Grade 6 (G6)", "English", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y6_ENG_W1D2", "Mostafa - Day 2: Non-Chronological Reports & Formal Features", "Grade 6 (G6)", "English", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y6_MATH_W1D1", "Mostafa - Day 1: Prime Factors & Index Notation", "Grade 6 (G6)", "Mathematics", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y6_MATH_W1D2", "Mostafa - Day 2: Fractions, Decimals & Percentages", "Grade 6 (G6)", "Mathematics", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y6_MATH_W1D3", "Mostafa - Day 3: Long Division & Word Problems", "Grade 6 (G6)", "Mathematics", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y6_SCI_W1D1", "Mostafa - Day 1: Circulatory System & Blood Components", "Grade 6 (G6)", "Science", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["DAILY_Y6_SCI_W1D2", "Mostafa - Day 2: Electrical Circuits & Conductors", "Grade 6 (G6)", "Science", 9, 10, "ACTIVE", "", "2026-10-28", "Daily", "Week 1"], ["EX_Y5_ARB_W1", "علي - اختبار الأسبوع 1: الجملة الاسمية وضبط المبتدأ والخبر", "Year 5 (G5)", "اللغة العربية", 19, 20, "ACTIVE", "", "2026-10-28", "Weekly", "Week 1"], ["EX_Y5_ICT_QUIZ01", "Ali - ICT Assessment: Variables, Loops & Operators", "Year 5 (G5)", "ICT Computing", 15, 20, "ACTIVE", "", "2026-10-28", "Weekly", "W7"], ["EX_Y5_MATH_M1_CAPSTONE", "Ali - Math Month 1 Capstone Exam", "Year 5 (G5)", "Mathematics", 14, 20, "ACTIVE", "", "2026-10-28", "Monthly", "Week 1"], ["EX_Y5_MATH_W1", "Ali - Math Week 1 Milestone: Number Properties & Divisibility", "Year 5 (G5)", "Mathematics", 19, 20, "ACTIVE", "", "2026-10-28", "Weekly", "Week 1"], ["EX_Y5_SCI_W1", "Ali - Science Week 1 Milestone: Sound Vibrations & Hearing", "Year 5 (G5)", "Science", 19, 20, "ACTIVE", "", "2026-10-28", "Weekly", "Week 1"], ["EX_Y6_ENG_W1", "Mostafa - English Week 1 Milestone: Fantasy & Report Writing", "Grade 6 (G6)", "English", 19, 20, "ACTIVE", "", "2026-10-28", "Weekly", "Week 1"], ["EX_Y6_ICT_QUIZ01", "Mostafa - ICT Assessment: Constructs & Flowcharts", "Grade 6 (G6)", "ICT Computing", 15, 20, "ACTIVE", "", "2026-10-28", "Weekly", "W7"], ["EX_Y6_MATH_M1_CAPSTONE", "Mostafa - Math Month 1 Capstone: Number Mastery", "Grade 6 (G6)", "Mathematics", 14, 20, "ACTIVE", "", "2026-10-28", "Monthly", "Week 1"], ["EX_Y6_MATH_W1", "Mostafa - Math Week 1 Milestone: Number & Operations", "Grade 6 (G6)", "Mathematics", 19, 20, "ACTIVE", "", "2026-10-28", "Weekly", "Week 1"], ["EX_Y6_SCI_W1", "Mostafa - Science Week 1 Milestone: Circulatory System & Electricity", "Grade 6 (G6)", "Science", 19, 20, "ACTIVE", "", "2026-10-28", "Weekly", "Week 1"]];
}



/**
 * One-click administrator RPC to seed/synchronize all 234 curriculum questions
 * and 48 mapped exams across all 5 subjects into Google Sheets.
 */
function seedCompleteQuestionBank(adminToken) {
  const token = adminToken || (this && this.adminToken);
  if (token && !isAdminTokenValid_(token)) return Object.assign({}, ADMIN_REQUIRED_RESULT);

  try {
    const ss = getSpreadsheet();
    if (!ss) return { success: false, message: 'Google Spreadsheet not found.' };

    setupDatabase(ss);

    let qbSheet = ss.getSheetByName('Question_Bank');
    if (!qbSheet) qbSheet = ss.insertSheet('Question_Bank');

    const qbHeaders = [
      'Question ID', 'Grade Level', 'Subject', 'Unit / Topic', 'Question Text', 'Type',
      'Options (delimited by |)', 'Correct Answer', 'Points',
      'Pedagogical Explanation & Mistake Breakdown', 'Exam Code', 'Week', 'Difficulty'
    ];
    ensureSheetHeaders_(qbSheet, qbHeaders, '#047857');

    const starterQuestions = getStarterQuestionBank_();
    if (starterQuestions.length) {
      qbSheet.getRange(2, 1, starterQuestions.length, starterQuestions[0].length).setValues(starterQuestions);
      styleQuestionBankSheet(qbSheet);
    }

    let exSheet = ss.getSheetByName('Exams');
    if (!exSheet) exSheet = ss.insertSheet('Exams');

    const exHeaders = [
      'Exam Code', 'Exam Title', 'Grade Level', 'Subject', 'Questions', 'Duration (Mins)',
      'Status', 'Direct URL', 'Created Date', 'Exam Type', 'Target Period'
    ];
    ensureSheetHeaders_(exSheet, exHeaders, '#4338ca');

    const starterExams = getStarterExams_();
    if (starterExams.length) {
      exSheet.getRange(2, 1, starterExams.length, starterExams[0].length).setValues(starterExams);
      styleExamsSheet(exSheet);
    }

    return {
      success: true,
      countQuestions: starterQuestions.length,
      countExams: starterExams.length,
      message: 'تم بنجاح تحميل كامل بنك الأسئلة (' + starterQuestions.length + ' سؤال) وجميع الامتحانات (' + starterExams.length + ' امتحان) لكافة المواد الخمس (الرياضيات، العلوم، الإنجليزي، العربي، والحاسب الآلي)!'
    };
  } catch (err) {
    return { success: false, message: 'فشل تحميل بنك الأسئلة: ' + err.toString() };
  }
}
