// Server-side regression tests for Code.gs.
// Run with: node --test tests/server.test.js
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const test = require('node:test');
const assert = require('node:assert/strict');

const CODE = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');

const BANK_HEADER = [
  'Question ID', 'Grade Level', 'Subject', 'Unit / Topic', 'Question Text', 'Type',
  'Options (delimited by |)', 'Correct Answer', 'Points',
  'Pedagogical Explanation & Mistake Breakdown', 'Exam Code'
];
const EXAM_HEADER = [
  'Exam Code', 'Exam Title', 'Grade Level', 'Subject', 'Questions',
  'Duration (Mins)', 'Status', 'Direct URL', 'Created Date'
];
const SUB_HEADER = [
  'Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total',
  'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON'
];
const RETAKE_HEADER = [
  'Request ID', 'Timestamp', 'Student Name', 'Exam Code', 'Exam Title',
  'Previous Score', 'Status', 'Reason', 'Decision Timestamp'
];
const SESSION_HEADER = [
  'Session ID', 'Created At', 'Student Name', 'Exam Code', 'School Grade',
  'Started At', 'Expires At', 'Status', 'Questions JSON', 'Result JSON'
];

class FakeSheet {
  constructor(name, rows) {
    this.name = name;
    this.rows = (rows || []).map(row => row.slice());
  }
  getLastRow() { return this.rows.length; }
  getLastColumn() {
    return this.rows.length ? Math.max(...this.rows.map(row => row.length)) : 0;
  }
  getDataRange() {
    return { getValues: () => this.rows.map(row => row.slice()) };
  }
  appendRow(row) { this.rows.push(row.slice()); }
  insertSheet(name) { return new FakeSheet(name, []); }
  setColumnWidth() {}
  setRowHeight() {}
  setFrozenRows() {}
  clear() { this.rows = []; }
  getRange(row, col, numRows, numCols) {
    const self = this;
    const nr = numRows || 1;
    const nc = numCols || 1;
    const chain = {
      getValues() {
        const out = [];
        for (let i = 0; i < nr; i++) {
          const source = self.rows[row - 1 + i] || [];
          const line = [];
          for (let j = 0; j < nc; j++) line.push(source[col - 1 + j]);
          out.push(line);
        }
        return out;
      },
      setValues(values) {
        values.forEach((line, i) => {
          const target = row - 1 + i;
          while (self.rows.length <= target) self.rows.push([]);
          line.forEach((value, j) => { self.rows[target][col - 1 + j] = value; });
        });
        return chain;
      },
      setValue(value) {
        const target = row - 1;
        while (self.rows.length <= target) self.rows.push([]);
        self.rows[target][col - 1] = value;
        return chain;
      },
      setBackground() { return chain; },
      setFontColor() { return chain; },
      setFontWeight() { return chain; },
      setFontSize() { return chain; },
      setHorizontalAlignment() { return chain; },
      setVerticalAlignment() { return chain; },
      setWrapStrategy() { return chain; }
    };
    return chain;
  }
}

function makeBankRows(prefix = 'Q') {
  return [
    [prefix + '1', 'Year 5 (G5)', 'English Grammar', 'Unit 2', 'Question one?', 'MCQ', 'A | B | C | D', 'B', 1, 'Because B.', 'EX_Y5_ENG_ADV01'],
    [prefix + '2', 'Year 5 (G5)', 'English Grammar', 'Unit 2', 'Question two?', 'MCQ', 'Time | Place | Manner | Reason', 'Time', 1, 'Time.', 'EX_Y5_ENG_ADV01'],
    [prefix + '3', 'Year 5 (G5)', 'English Grammar', 'Unit 2', 'Question three?', 'MCQ', 'A. | B. | C. | D.', 'A.', 1, 'A.', 'EX_Y5_ENG_ADV01']
  ];
}

function createApp(options = {}) {
  const sheets = options.empty ? {} : {
    Question_Bank: new FakeSheet('Question_Bank', [BANK_HEADER].concat(options.bank || makeBankRows())),
    Exams: new FakeSheet('Exams', [EXAM_HEADER, [
      'EX_Y5_ENG_ADV01', 'Test Exam', 'Year 5 (G5)', 'English Grammar',
      options.questionCount || 3, 20, 'ACTIVE', '', new Date()
    ]].concat(options.extraExams || [])),
    Submissions: new FakeSheet('Submissions', [SUB_HEADER].concat(options.submissions || [])),
    Retake_Requests: new FakeSheet('Retake_Requests', [RETAKE_HEADER].concat(options.retakes || [])),
    Sessions: new FakeSheet('Sessions', [SESSION_HEADER].concat(options.sessions || []))
  };

  const ss = {
    getSheetByName(name) { return sheets[name] || null; },
    insertSheet(name) {
      const sheet = new FakeSheet(name, []);
      sheets[name] = sheet;
      return sheet;
    },
    getId() { return 'test-sheet-id'; },
    getUrl() { return 'https://example.test/sheet'; }
  };

  const props = {};
  let uuid = 0;
  const sandbox = {
    console,
    SpreadsheetApp: {
      getActiveSpreadsheet: () => ss,
      getUi: () => ({ alert() {} }),
      openById: () => ss,
      create: () => ss,
      WrapStrategy: { WRAP: 'WRAP' }
    },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: key => props[key] || null,
        setProperty: (key, value) => { props[key] = value; }
      }),
      getUserProperties: () => ({ getProperty: () => null })
    },
    CacheService: { getScriptCache: () => ({ put() {}, get() { return null; } }) },
    LockService: { getScriptLock: () => ({ tryLock: () => true, waitLock: () => true, releaseLock() {} }) },
    Utilities: {
      getUuid: () => 'uuid-' + (++uuid),
      formatDate: () => '2026-10-25 00:00'
    },
    Session: { getScriptTimeZone: () => 'GMT+2' },
    Logger: { log() {} },
    FormApp: {}
  };

  vm.createContext(sandbox);
  vm.runInContext(CODE, sandbox, { filename: 'Code.gs' });
  return { sandbox, sheets, ss, props };
}

function start(app, name = 'Ali Ahmed', code = 'EX_Y5_ENG_ADV01') {
  return app.sandbox.getExamData(code, name);
}

function sessionFor(app, sessionKey) {
  const row = app.sheets.Sessions.rows.find(r => String(r[0]) === String(sessionKey));
  assert.ok(row, 'session row should exist');
  return JSON.parse(row[8]);
}

test('getExamData samples from the bank and never exposes the answer', () => {
  const app = createApp();
  const result = start(app);
  assert.equal(result.success, true);
  assert.equal(result.questions.length, 3);
  assert.equal(Object.prototype.hasOwnProperty.call(result.questions[0], 'correctAnswer'), false);
  assert.equal(app.sheets.Sessions.rows.length, 2);
});

test('one correct answer out of the full paper is 1/3, not 100%', () => {
  const app = createApp();
  const data = start(app);
  const questions = sessionFor(app, data.sessionKey);
  const first = questions[0];
  const result = app.sandbox.submitExamAnswers({
    studentName: 'Ali Ahmed',
    examCode: 'EX_Y5_ENG_ADV01',
    sessionKey: data.sessionKey,
    answers: { [first.id]: first.correctAnswer }
  });

  assert.equal(result.success, true);
  assert.equal(result.earnedScore, 1);
  assert.equal(result.totalScore, 3);
  assert.equal(result.percentage, 33);
});

test('fabricated empty answers cannot score and unknown ids are ignored', () => {
  const app = createApp();
  const data = start(app);
  const result = app.sandbox.submitExamAnswers({
    studentName: 'Ali Ahmed',
    examCode: 'EX_Y5_ENG_ADV01',
    sessionKey: data.sessionKey,
    answers: { fake1: '', fake2: '' }
  });

  assert.equal(result.success, true);
  assert.equal(result.earnedScore, 0);
  assert.equal(result.totalScore, 3);
  assert.equal(result.percentage, 0);
});

test('duplicate submission returns the saved result and writes one row', () => {
  const app = createApp();
  const data = start(app);
  const payload = {
    studentName: 'Ali Ahmed',
    examCode: 'EX_Y5_ENG_ADV01',
    sessionKey: data.sessionKey,
    answers: {}
  };

  const first = app.sandbox.submitExamAnswers(payload);
  const second = app.sandbox.submitExamAnswers(payload);

  assert.equal(first.success, true);
  assert.equal(second.success, true);
  assert.equal(second.alreadySubmitted, true);
  assert.equal(app.sheets.Submissions.rows.length, 2); // header + one result
});

test('attempt limit is enforced, then an approved retake unlocks one more attempt', () => {
  const app = createApp();
  for (let i = 0; i < 2; i++) {
    const data = start(app);
    app.sandbox.submitExamAnswers({
      studentName: 'Ali Ahmed',
      examCode: 'EX_Y5_ENG_ADV01',
      sessionKey: data.sessionKey,
      answers: {}
    });
  }

  const blocked = start(app);
  assert.equal(blocked.success, false);
  assert.equal(blocked.code, 'MAX_ATTEMPTS');

  const request = app.sandbox.requestExamRetake({
    studentName: 'Ali Ahmed',
    examCode: 'EX_Y5_ENG_ADV01',
    reason: 'Please allow one more try.'
  });
  assert.equal(request.success, true);

  const pending = start(app);
  assert.equal(pending.success, false);

  const approved = app.sandbox.approveRetakeRequest(request.requestId);
  assert.equal(approved.success, true);

  const allowed = start(app);
  assert.equal(allowed.success, true);
});

test('expired sessions are rejected by the server', () => {
  const app = createApp();
  const data = start(app);
  const row = app.sheets.Sessions.rows.find(r => String(r[0]) === String(data.sessionKey));
  row[6] = new Date(Date.now() - 10 * 60 * 1000).toISOString();

  const result = app.sandbox.submitExamAnswers({
    studentName: 'Ali Ahmed',
    examCode: 'EX_Y5_ENG_ADV01',
    sessionKey: data.sessionKey,
    answers: {}
  });

  assert.equal(result.success, false);
  assert.equal(result.code, 'TIME_EXPIRED');
});

test('a student cannot submit another student session', () => {
  const app = createApp();
  const data = start(app);
  const result = app.sandbox.submitExamAnswers({
    studentName: 'Mostafa Ahmed',
    examCode: 'EX_Y5_ENG_ADV01',
    sessionKey: data.sessionKey,
    answers: {}
  });

  assert.equal(result.success, false);
  assert.equal(result.code, 'STUDENT_MISMATCH');
});

test('setupDatabase is non-destructive and does not seed fake submissions', () => {
  const existingSubmission = [
    '2026-10-01 10:00', 'Ali Ahmed', 'Year 5 (G5)', 'EX_Y5_ENG_ADV01',
    8, 10, '80%', 'Very Good', '6 min', '8/10', '[]'
  ];
  const app = createApp({ submissions: [existingSubmission] });
  const before = app.sheets.Question_Bank.rows.length;

  app.sandbox.setupDatabase(app.ss);

  assert.equal(app.sheets.Question_Bank.rows.length, before);
  assert.equal(app.sheets.Submissions.rows.length, 2); // header + original row
});

test('a fresh setup creates the tables and seeds samples only once', () => {
  const app = createApp({ empty: true });
  app.sandbox.setupDatabase(app.ss);

  assert.ok(app.sheets.Submissions);
  assert.ok(app.sheets.Question_Bank);
  assert.ok(app.sheets.Exams);
  assert.ok(app.sheets.Retake_Requests);
  assert.ok(app.sheets.Sessions);
  assert.equal(app.sheets.Question_Bank.rows.length, 46); // header + 45 samples
  assert.equal(app.sheets.Exams.rows.length, 4); // header + 3 samples
  assert.equal(app.sheets.Submissions.rows.length, 1); // no fake students
});

test('a custom exam added to the sheet is served from the bank', () => {
  const app = createApp({
    extraExams: [[
      'EX_CUSTOM_01', 'Custom Exam', 'Year 5 (G5)', 'English Grammar',
      1, 10, 'ACTIVE', '', new Date()
    ]],
    bank: makeBankRows().concat([
      ['C1', 'Year 5 (G5)', 'English Grammar', 'Custom unit', 'Custom question?', 'MCQ', 'Yes | No', 'Yes', 1, 'Yes.', 'EX_CUSTOM_01']
    ])
  });

  const result = app.sandbox.getExamData('EX_CUSTOM_01', 'Ali Ahmed');
  assert.equal(result.success, true);
  assert.equal(result.questions.length, 1);
  assert.equal(result.questions[0].text, 'Custom question?');
});

test('the exam question count controls how many bank items are sampled', () => {
  const bank = [];
  for (let i = 1; i <= 15; i++) {
    bank.push([
      'Q' + i, 'Year 5 (G5)', 'English Grammar', 'Unit 2',
      'Question ' + i, 'MCQ', 'A | B | C | D', 'B', 1, 'Because B.', 'EX_Y5_ENG_ADV01'
    ]);
  }
  const app = createApp({ bank, questionCount: 10 });
  const result = start(app);
  assert.equal(result.success, true);
  assert.equal(result.questions.length, 10);
});

test('admin dashboard shows the real bank instead of generated samples', () => {
  const app = createApp();
  const result = app.sandbox.getAdminDashboardData();
  assert.equal(result.success, true);
  assert.equal(result.allQuestions.length, 3);
  assert.equal(result.allQuestions[0].examCode, 'EX_Y5_ENG_ADV01');
});
