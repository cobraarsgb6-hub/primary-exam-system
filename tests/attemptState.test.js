const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

class FakeSheet {
  constructor(name, rows) {
    this.name = name;
    this.rows = (rows || []).map(r => r.slice());
  }
  getLastRow() { return this.rows.length; }
  getLastColumn() { return this.rows.length ? Math.max(...this.rows.map(r => r.length)) : 0; }
  getDataRange() {
    return { getValues: () => this.rows.map(r => r.slice()) };
  }
  appendRow(row) { this.rows.push(row.slice()); }
  getRange(row, col, numRows, numCols) {
    const self = this;
    const nr = numRows || 1;
    const nc = numCols || 1;
    const chain = {
      getValues() {
        const out = [];
        for (let i = 0; i < nr; i++) {
          const src = self.rows[row - 1 + i] || [];
          const line = [];
          for (let j = 0; j < nc; j++) line.push(src[col - 1 + j]);
          out.push(line);
        }
        return out;
      },
      setValues(vals) {
        vals.forEach((line, i) => {
          const target = row - 1 + i;
          while (self.rows.length <= target) self.rows.push([]);
          line.forEach((val, j) => { self.rows[target][col - 1 + j] = val; });
        });
        return chain;
      },
      setValue(val) {
        const target = row - 1;
        while (self.rows.length <= target) self.rows.push([]);
        self.rows[target][col - 1] = val;
        return chain;
      },
      getValue() {
        return (self.rows[row - 1] && self.rows[row - 1][col - 1] !== undefined) ? self.rows[row - 1][col - 1] : '';
      }
    };
    return chain;
  }
}

class FakeSpreadsheet {
  constructor(sheets = {}) {
    this.sheets = sheets;
  }
  getSheetByName(name) { return this.sheets[name] || null; }
  insertSheet(name) {
    const s = new FakeSheet(name, []);
    this.sheets[name] = s;
    return s;
  }
}

function createEnv(submissionsRows = [], retakeRows = []) {
  const code = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');
  const subHeaders = ['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON'];
  const retakeHeaders = ['Request ID', 'Timestamp', 'Student Name', 'Exam Code', 'Exam Title', 'Previous Score', 'Status', 'Reason', 'Decision Timestamp'];

  const subSheet = new FakeSheet('Submissions', [subHeaders, ...submissionsRows]);
  const retakeSheet = new FakeSheet('Retake_Requests', [retakeHeaders, ...retakeRows]);
  const ss = new FakeSpreadsheet({ 'Submissions': subSheet, 'Retake_Requests': retakeSheet });

  const ctx = {
    Logger: { log: () => {} },
    SpreadsheetApp: { getActiveSpreadsheet: () => ss },
    Session: { getScriptTimeZone: () => 'GMT+2' },
    Utilities: { formatDate: (d, tz, fmt) => '2026-10-28 10:00' },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: () => null,
        setProperty: () => {}
      })
    },
    getSpreadsheet: () => ss
  };
  vm.createContext(ctx);
  vm.runInContext(code, ctx);
  return { ctx, subSheet, retakeSheet };
}

test('getAttemptState_: 0 attempts allows exam and indicates no submission', () => {
  const { ctx } = createEnv();
  const state = ctx.getAttemptState_('Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01');
  assert.equal(state.hasSubmitted, false);
  assert.equal(state.attemptsCount, 0);
  assert.equal(state.canAttempt, true);
  assert.equal(state.retakeStatus, 'NONE');
});

test('getAttemptState_: 1 attempt still allows exam (MAX_ATTEMPTS = 2)', () => {
  const subRows = [
    ['2026-10-28 09:00', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 8, 10, '80%', 'Very Good 👍', '5 min', '8/10', '[]']
  ];
  const { ctx } = createEnv(subRows);
  const state = ctx.getAttemptState_('Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01');
  assert.equal(state.hasSubmitted, true);
  assert.equal(state.attemptsCount, 1);
  assert.equal(state.canAttempt, true);
  assert.equal(state.lastScore, '8 / 10 (80%)');
});

test('getAttemptState_: 2 attempts exhausts limit and blocks further attempts', () => {
  const subRows = [
    ['2026-10-28 09:00', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 8, 10, '80%', 'Very Good 👍', '5 min', '8/10', '[]'],
    ['2026-10-28 10:00', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 9, 10, '90%', 'Excellent 🌟', '4 min', '9/10', '[]']
  ];
  const { ctx } = createEnv(subRows);
  const state = ctx.getAttemptState_('Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01');
  assert.equal(state.hasSubmitted, true);
  assert.equal(state.attemptsCount, 2);
  assert.equal(state.canAttempt, false);
});

test('getAttemptState_: pending retake request does NOT unlock exam when limit is exhausted', () => {
  const subRows = [
    ['2026-10-28 09:00', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 8, 10, '80%', 'Very Good 👍', '5 min', '8/10', '[]'],
    ['2026-10-28 10:00', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 9, 10, '90%', 'Excellent 🌟', '4 min', '9/10', '[]']
  ];
  const retakeRows = [
    ['REQ_001', '2026-10-28 10:05', 'Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01', 'Fantasy Story', '9/10', 'PENDING', 'Need to review mistake', '']
  ];
  const { ctx } = createEnv(subRows, retakeRows);
  const state = ctx.getAttemptState_('Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01');
  assert.equal(state.retakeStatus, 'PENDING');
  assert.equal(state.canAttempt, false);
});

test('getAttemptState_: approved retake unlocks an additional attempt', () => {
  const subRows = [
    ['2026-10-28 09:00', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 8, 10, '80%', 'Very Good 👍', '5 min', '8/10', '[]'],
    ['2026-10-28 10:00', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 9, 10, '90%', 'Excellent 🌟', '4 min', '9/10', '[]']
  ];
  const retakeRows = [
    ['REQ_001', '2026-10-28 10:05', 'Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01', 'Fantasy Story', '9/10', 'APPROVED', 'Parent approved', '2026-10-28 10:10']
  ];
  const { ctx } = createEnv(subRows, retakeRows);
  const state = ctx.getAttemptState_('Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01');
  assert.equal(state.retakeStatus, 'APPROVED');
  assert.equal(state.canAttempt, true);
});

test('getAttemptState_: consumed retake does not unlock further attempts', () => {
  const subRows = [
    ['2026-10-28 09:00', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 8, 10, '80%', 'Very Good 👍', '5 min', '8/10', '[]'],
    ['2026-10-28 10:00', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 9, 10, '90%', 'Excellent 🌟', '4 min', '9/10', '[]'],
    ['2026-10-28 10:30', 'Mostafa Ahmed', 'Grade 6', 'EX_Y6_ENG_FANTASY01', 10, 10, '100%', 'Excellent 🌟', '3 min', '10/10', '[]']
  ];
  const retakeRows = [
    ['REQ_001', '2026-10-28 10:05', 'Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01', 'Fantasy Story', '9/10', 'CONSUMED', 'Parent approved', '2026-10-28 10:10']
  ];
  const { ctx } = createEnv(subRows, retakeRows);
  const state = ctx.getAttemptState_('Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01');
  assert.equal(state.retakeStatus, 'CONSUMED');
  assert.equal(state.canAttempt, false);
});

test('getAttemptState_: student and exam matching is exact and isolated', () => {
  const subRows = [
    ['2026-10-28 09:00', 'Ali Ahmed', 'Year 5', 'EX_Y5_ENG_ADV01', 10, 10, '100%', 'Excellent 🌟', '5 min', '10/10', '[]'],
    ['2026-10-28 09:30', 'Ali Ahmed', 'Year 5', 'EX_Y5_ENG_ADV01', 10, 10, '100%', 'Excellent 🌟', '5 min', '10/10', '[]']
  ];
  const { ctx } = createEnv(subRows);

  // Different student
  const mostafaState = ctx.getAttemptState_('Mostafa Ahmed', 'EX_Y5_ENG_ADV01');
  assert.equal(mostafaState.attemptsCount, 0);
  assert.equal(mostafaState.canAttempt, true);

  // Substring name: "Khalid" vs "Ali"
  const khalidState = ctx.getAttemptState_('Khalid Ali', 'EX_Y5_ENG_ADV01');
  assert.equal(khalidState.attemptsCount, 0);

  // Different exam for Ali
  const aliMathState = ctx.getAttemptState_('Ali Ahmed', 'EX_Y5_MTH_UNIT01');
  assert.equal(aliMathState.attemptsCount, 0);
  assert.equal(aliMathState.canAttempt, true);
});

test('getAttemptState_ & findActiveSession_: expired session consumes an attempt', () => {
  const code = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');
  const subHeaders = ['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON'];
  const sessionHeaders = ['Session ID', 'Created At', 'Student Name', 'Exam Code', 'School Grade', 'Started At', 'Expires At', 'Status', 'Questions JSON', 'Result JSON'];

  const subSheet = new FakeSheet('Submissions', [subHeaders]);
  const pastDate = new Date(Date.now() - 30 * 60 * 1000).toISOString();
  const sessionRows = [
    sessionHeaders,
    ['SESS_OLD', pastDate, 'Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01', 'Grade 6', pastDate, pastDate, 'ACTIVE', '[{"id":"Q1"}]', '']
  ];
  const sessionSheet = new FakeSheet('Sessions', sessionRows);
  const ss = new FakeSpreadsheet({ 'Submissions': subSheet, 'Sessions': sessionSheet });

  const ctx = {
    Logger: { log: () => {} },
    SpreadsheetApp: { getActiveSpreadsheet: () => ss },
    Session: { getScriptTimeZone: () => 'GMT+2' },
    Utilities: { formatDate: (d, tz, fmt) => '2026-10-28 10:00' },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: () => null,
        setProperty: () => {}
      })
    },
    getSpreadsheet: () => ss
  };
  vm.createContext(ctx);
  vm.runInContext(code, ctx);

  // Calling findActiveSession_ detects the expired session
  const active = ctx.findActiveSession_('Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01');
  assert.equal(active, null);

  // Verify the attempt was consumed in Submissions
  const state = ctx.getAttemptState_('Mostafa Ahmed', 'EX_Y6_ENG_FANTASY01');
  assert.equal(state.attemptsCount, 1);
  assert.equal(state.hasSubmitted, true);
});
