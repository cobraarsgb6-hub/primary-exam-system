// Security and Privacy regression tests for Code.gs.
// Run with: node --test tests/security.test.js
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
const STUDY_PLAN_HEADER = [
  'Plan ID', 'Grade Level', 'Subject', 'Target Period', 'Focus Domain & Pedagogical Objectives', 'Milestone Exam Code', 'Status'
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
      setFontWeight() { return chain; },
      setBackground() { return chain; },
      setFontColor() { return chain; },
      setHorizontalAlignment() { return chain; },
      setVerticalAlignment() { return chain; },
      setBorder() { return chain; },
      setWrap() { return chain; },
      setWrapStrategy() { return chain; },
      setNumberFormat() { return chain; }
    };
    return chain;
  }
}

function makeBankRows() {
  return [
    ['Q1', 'Year 5 (G5)', 'English Grammar', 'Adverbials', 'Identify the adverbial.', 'MCQ', 'Quickly|Slowly|Blue|Car', 'Quickly', 1, 'Quickly is an adverb of manner.', 'EX_Y5_ENG_ADV01'],
    ['Q2', 'Year 5 (G5)', 'English Grammar', 'Adverbials', 'Choose time adverbial.', 'MCQ', 'Yesterday|Loudly|Here|Red', 'Yesterday', 1, 'Yesterday tells when.', 'EX_Y5_ENG_ADV01'],
    ['Q3', 'Year 5 (G5)', 'English Grammar', 'Adverbials', 'Fronted adverbial punctuation?', 'MCQ', 'Comma|Period|Colon|None', 'Comma', 1, 'Fronted adverbials require a comma.', 'EX_Y5_ENG_ADV01']
  ];
}

function createApp() {
  const sheets = {
    Question_Bank: new FakeSheet('Question_Bank', [BANK_HEADER].concat(makeBankRows())),
    Exams: new FakeSheet('Exams', [EXAM_HEADER, [
      'EX_Y5_ENG_ADV01', 'Test Exam', 'Year 5 (G5)', 'English Grammar', 3, 20, 'ACTIVE', '', new Date()
    ]]),
    Submissions: new FakeSheet('Submissions', [SUB_HEADER]),
    Retake_Requests: new FakeSheet('Retake_Requests', [RETAKE_HEADER]),
    Sessions: new FakeSheet('Sessions', [SESSION_HEADER]),
    Study_Plan: new FakeSheet('Study_Plan', [STUDY_PLAN_HEADER, [
      'PLAN_Y5_ENG_W1', 'Year 5 (G5)', 'English Grammar', 'W1', 'Adverbials & Fronted Adverbials', 'EX_Y5_ENG_W1', 'ACTIVE'
    ]])
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

  const props = {
    ADMIN_PIN_HASH: 'FALLBACK_HASH_1450536879',
    ALI_PIN_HASH: 'FALLBACK_HASH_1450515979',
    MOSTAFA_PIN_HASH: 'FALLBACK_HASH_1450515981'
  };
  let uuid = 0;
  const cacheStore = {};
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
    CacheService: {
      getScriptCache: () => ({
        put(k, v) { cacheStore[k] = v; },
        get(k) { return cacheStore[k] || null; },
        remove(k) { delete cacheStore[k]; }
      })
    },
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

test('Security 1: Rejection of forged and missing student tokens', () => {
  const app = createApp();

  // Missing token
  const res1 = app.sandbox.getTodayMission('ali', null);
  assert.equal(res1.success, false);
  assert.equal(res1.code, 'UNAUTHORIZED');

  // Forged token
  const res2 = app.sandbox.getTodayMission('ali', 'ACCESS_TOK_FAKE_SIGNATURE_123');
  assert.equal(res2.success, false);
  assert.equal(res2.code, 'UNAUTHORIZED');

  // Forged exam data access
  const res3 = app.sandbox.getExamData('EX_Y5_ENG_ADV01', 'Ali Ahmed', 'ACCESS_TOK_FAKE');
  assert.equal(res3.success, false);
  assert.equal(res3.code, 'UNAUTHORIZED');
});

test('Security 2: Cross-student data isolation', () => {
  const app = createApp();

  // Mint valid token for Ali
  const aliAuth = app.sandbox.verifyGatewayPin('2016');
  assert.equal(aliAuth.success, true);
  assert.equal(aliAuth.role, 'student');
  assert.equal(aliAuth.studentKey, 'ali');
  const aliToken = aliAuth.token;

  // Mint valid token for Mostafa
  const mostafaAuth = app.sandbox.verifyGatewayPin('2014');
  assert.equal(mostafaAuth.success, true);
  assert.equal(mostafaAuth.role, 'student');
  assert.equal(mostafaAuth.studentKey, 'mostafa');
  const mostafaToken = mostafaAuth.token;

  // Ali token cannot access Mostafa mission
  const resAliAccessMostafa = app.sandbox.getTodayMission('mostafa', aliToken);
  assert.equal(resAliAccessMostafa.success, false);
  assert.equal(resAliAccessMostafa.code, 'UNAUTHORIZED');

  // Mostafa token cannot access Ali mission
  const resMostafaAccessAli = app.sandbox.getTodayMission('ali', mostafaToken);
  assert.equal(resMostafaAccessAli.success, false);
  assert.equal(resMostafaAccessAli.code, 'UNAUTHORIZED');

  // Ali token cannot request retake on behalf of Mostafa
  const resFakeRetake = app.sandbox.requestExamRetake({ studentName: 'Mostafa Ahmed', examCode: 'EX_Y6_ARB_PRIO01' }, aliToken);
  assert.equal(resFakeRetake.success, false);
  assert.equal(resFakeRetake.code, 'UNAUTHORIZED');
});

test('Security 3: Rejection of administrative RPCs without valid admin token', () => {
  const app = createApp();

  // Student token
  const studentToken = app.sandbox.verifyGatewayPin('2016').token;

  // Admin functions called with student token
  assert.equal(app.sandbox.approveRetakeRequest('REQ-1', studentToken).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.rejectRetakeRequest('REQ-1', studentToken).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.createWeeklyExam({}, studentToken).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.createMonthlyExam({}, studentToken).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.createMistakesReviewExam({}, studentToken).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.setupDatabase(null, studentToken).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.seedCompleteQuestionBank(studentToken).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.syncColigoOnline(studentToken).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.syncGoogleDriveVideos('folder-1', studentToken).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.getAdminDashboardData(studentToken).code, 'UNAUTHORIZED');

  // Admin functions called with null token
  assert.equal(app.sandbox.approveRetakeRequest('REQ-1', null).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.rejectRetakeRequest('REQ-1', null).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.createWeeklyExam({}, null).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.createMonthlyExam({}, null).code, 'UNAUTHORIZED');
  assert.equal(app.sandbox.getAdminDashboardData(null).code, 'UNAUTHORIZED');

  // Valid admin token succeeds
  const adminToken = app.sandbox.verifyAdminPin('1990').token;
  assert.ok(adminToken);
  const dashboard = app.sandbox.getAdminDashboardData(adminToken);
  assert.equal(dashboard.success, true);
});

test('Security 4: Student getExamData strictly strips correct answers and pedagogical explanations', () => {
  const app = createApp();
  const aliToken = app.sandbox.verifyGatewayPin('2016').token;

  const examData = app.sandbox.getExamData('EX_Y5_ENG_ADV01', 'Ali Ahmed', aliToken);
  assert.equal(examData.success, true);
  assert.ok(Array.isArray(examData.questions));
  assert.ok(examData.questions.length > 0);

  for (const q of examData.questions) {
    // Assert sensitive fields are completely absent
    assert.equal(q.correctAnswer, undefined, 'correctAnswer must never be sent to student');
    assert.equal(q['Correct Answer'], undefined, 'Correct Answer must never be sent to student');
    assert.equal(q.explanation, undefined, 'explanation must never be sent to student');
    assert.equal(q.pedagogicalExplanation, undefined, 'pedagogicalExplanation must never be sent to student');
    assert.equal(q.mistakeBreakdown, undefined, 'mistakeBreakdown must never be sent to student');

    // Assert only safe public fields exist
    assert.ok(q.id);
    assert.ok(q.text);
    assert.ok(Array.isArray(q.options));
    assert.ok(typeof q.points === 'number');
  }
});

test('Security 5: Gateway PIN rate limiting protects against brute force', () => {
  const app = createApp();

  // Try wrong PIN 8 times to hit threshold
  for (let i = 0; i < 8; i++) {
    const res = app.sandbox.verifyGatewayPin('0000');
    assert.equal(res.success, false);
    assert.equal(res.code, 'INVALID_PIN');
  }

  // 9th attempt is rate-limited
  const blocked = app.sandbox.verifyGatewayPin('0000');
  assert.equal(blocked.success, false);
  assert.equal(blocked.code, 'RATE_LIMITED');

  // Even the correct PIN is blocked during lockout
  const blockedCorrect = app.sandbox.verifyGatewayPin('1990');
  assert.equal(blockedCorrect.success, false);
  assert.equal(blockedCorrect.code, 'RATE_LIMITED');
});
