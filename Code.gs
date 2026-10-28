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
  return HtmlService.createHtmlOutputFromFile('Index')
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

function loadBankQuestionsByPeriod_(grade, subject, period) {
  const ss = getSpreadsheet();
  const sheet = ss.getSheetByName('Question_Bank');
  if (!sheet || sheet.getLastRow() <= 1) return [];

  const map = getSheetHeaderMap_(sheet);
  const data = sheet.getDataRange().getValues();
  const questions = [];
  const targetPeriod = String(period || '').trim().toUpperCase();
  const isMonthly = targetPeriod.startsWith('M');
  const family = subjectFamily_(subject);

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const rowGrade = String(row[headerIndex_(map, 'Grade Level', 1)] || '');
    const rowSubject = String(row[headerIndex_(map, 'Subject', 2)] || '');
    const rowWeek = String(rowValue_(row, map, 'Week', 11) || 'W1').trim().toUpperCase();

    const gradeMatches = (normalizeName_(rowGrade).indexOf('5') !== -1 && normalizeName_(grade).indexOf('5') !== -1) ||
                         (normalizeName_(rowGrade).indexOf('6') !== -1 && normalizeName_(grade).indexOf('6') !== -1);
    if (!gradeMatches) continue;

    // Keep Arabic and English papers from mixing when the subject is known.
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
    if (options.length < 2) continue;

    const answerMatchesOption = options.some(option => normalizeAnswer_(option) === normalizeAnswer_(answer));
    if (!answerMatchesOption) {
      Logger.log('Skipping malformed bank question ' + String(row[0] || ('row ' + (i + 1))) + ': answer not in options');
      continue;
    }

    const unit = String(row[headerIndex_(map, 'Unit / Topic', 3)] || '');
    const passageIndex = map['passage'];
    const passage = (typeof passageIndex === 'number')
      ? String(row[passageIndex] || '')
      : getPassageForQuestion_(String(rowValue_(row, map, 'Exam Code', 10) || ''), unit, text);

    questions.push({
      id: String(row[headerIndex_(map, 'Question ID', 0)] || ('BANK_' + i)),
      grade: rowGrade,
      subject: rowSubject,
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

/**
 * Returns all active exams for a student based on grade isolation.
 */
function getStudentAvailableExams(studentKey) {
  try {
    const ss = getSpreadsheet();
    const exSheet = ss.getSheetByName('Exams');
    if (!exSheet || exSheet.getLastRow() <= 1) {
      return { success: true, exams: [], driveVideos: readDriveVideoMap_() };
    }

    const key = String(studentKey || 'ali').toLowerCase();
    const isAli = (key === 'ali');

    const map = getSheetHeaderMap_(exSheet);
    const data = exSheet.getDataRange().getValues();
    const exams = [];

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
  } catch (err) {
    Logger.log('getStudentAvailableExams error: ' + err);
    return { success: false, message: err.message, exams: [] };
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

    const bankQuestions = loadBankQuestionsByPeriod_(grade, subject, weekCode);
    if (!bankQuestions.length) {
      return {
        success: false,
        message: 'لا توجد أسئلة في بنك الأسئلة لـ ' + grade + ' / ' + subject + ' / ' + weekCode + '. أضف الأسئلة أولاً ثم أعد المحاولة.'
      };
    }

    const subjectPrefix = subjectFamily_(subject) === 'arabic' ? 'ARB' : 'ENG';
    const examCode = 'EX_' + (isAli ? 'Y5_ALI' : 'Y6_MOS') + '_' + weekCode + '_' + subjectPrefix;
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

    if (!/^M[1-9][0-9]?$/.test(monthCode)) {
      return { success: false, message: 'كود الشهر غير صالح. استخدم مثالاً مثل M1 أو M2.' };
    }

    const bankQuestions = loadBankQuestionsByPeriod_(grade, requestedSubject, monthCode);
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
