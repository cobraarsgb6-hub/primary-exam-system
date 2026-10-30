// Contract and unit tests for P6: Cumulative Multi-Subject Exam Schedule & Adaptive Engine
// Run with: node --test tests/scheduleCumulative.test.js
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const BANK_HEADERS = [
  'Question ID', 'Grade Level', 'Subject', 'Unit / Topic', 'Question Text', 'Type',
  'Options (delimited by |)', 'Correct Answer', 'Points',
  'Pedagogical Explanation & Mistake Breakdown', 'Exam Code', 'Week', 'Difficulty'
];

const EXAM_HEADERS = [
  'Exam Code', 'Exam Title', 'Grade Level', 'Subject', 'Questions', 'Duration (Mins)',
  'Status', 'Direct URL', 'Created Date', 'Exam Type', 'Target Period'
];

const SCHED_HEADERS = [
  'Schedule ID', 'Date', 'Student', 'Grade Level', 'Subject', 'Exam Code',
  'Exam Title', 'Exam Type', 'Period', 'Questions', 'Duration (Mins)',
  'Difficulty', 'Status', 'Daily Pair Code'
];

function makeSheet(name, rows) {
  const store = rows.map(r => r.slice());
  return {
    name: name,
    rows: store,
    getLastRow: () => store.length,
    getLastColumn: () => (store.length ? Math.max(...store.map(r => r.length)) : 0),
    getDataRange: () => ({ getValues: () => store.map(r => r.slice()) }),
    appendRow: (row) => store.push(row.slice()),
    getRange(row, col, numRows, numCols) {
      const nr = numRows || 1;
      const nc = numCols || 1;
      const range = {
        getValues() {
          const out = [];
          for (let i = 0; i < nr; i++) {
            const line = [];
            const src = store[row - 1 + i] || [];
            for (let j = 0; j < nc; j++) line.push(src[col - 1 + j]);
            out.push(line);
          }
          return out;
        },
        setValues(vals) {
          vals.forEach((line, i) => {
            const target = row - 1 + i;
            while (store.length <= target) store.push([]);
            line.forEach((val, j) => { store[target][col - 1 + j] = val; });
          });
          return range;
        },
        setValue(val) {
          const target = row - 1;
          while (store.length <= target) store.push([]);
          store[target][col - 1] = val;
          return range;
        },
        getValue() {
          return (store[row - 1] && store[row - 1][col - 1] !== undefined) ? store[row - 1][col - 1] : '';
        },
        setVerticalAlignment: () => range,
        setHorizontalAlignment: () => range,
        setFontSize: () => range,
        setFontWeight: () => range,
        setBackground: () => range,
        setFontColor: () => range,
        setBorder: () => range,
        setWrap: () => range,
        setWrapStrategy: () => range,
        setNumberFormat: () => range
      };
      return range;
    },
    setColumnWidth: () => {},
    setRowHeight: () => {},
    setFrozenRows: () => {}
  };
}

function loadCode(sheets) {
  const code = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');
  const store = { ...sheets };
  const ss = {
    getId: () => 'test-sheet-id',
    getUrl: () => 'https://example.test/sheet',
    getSheetByName: (name) => store[name] || null,
    insertSheet: (name) => {
      const s = makeSheet(name, []);
      store[name] = s;
      return s;
    }
  };
  const props = {
    ADMIN_PIN_HASH: 'FALLBACK_HASH_1450536879',
    ALI_PIN_HASH: 'FALLBACK_HASH_1450515979',
    MOSTAFA_PIN_HASH: 'FALLBACK_HASH_1450515981'
  };
  const sandbox = {
    console,
    Logger: { log: () => {} },
    Utilities: {
      formatDate: d => d.toISOString(),
      getUuid: () => 'MOCK_UUID_' + Math.random().toString(36).substring(2, 8)
    },
    Session: { getScriptTimeZone: () => 'GMT+2' },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: (k) => props[k] || null,
        setProperty: (k, v) => { props[k] = v; },
        setProperties: (obj) => Object.assign(props, obj)
      })
    },
    SpreadsheetApp: {
      getActiveSpreadsheet: () => ss,
      getUi: () => ({ alert: () => {} }),
      WrapStrategy: { WRAP: 'WRAP' }
    },
    getSpreadsheet_: () => ss
  };
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox, { filename: 'Code.gs' });
  return { sandbox, sheets: store, ss };
}

function sampleCumulativeBank() {
  return [
    BANK_HEADERS,
    ['Q_M_W1_1', 'Year 5 (G5)', 'Mathematics', 'Lesson 1: Divisibility', 'Divisible by 2?', 'MCQ', 'Yes | No', 'Yes', 1, 'Ends in even digit', 'EX_Y5_MATH_W1', 'W1', 'Easy'],
    ['Q_M_W1_2', 'Year 5 (G5)', 'Mathematics', 'Lesson 2: Factors', 'Factors of 12?', 'MCQ', '1,2,3,4,6,12 | 1,2', '1,2,3,4,6,12', 1, 'All divisors', 'EX_Y5_MATH_W1', 'W1', 'Medium'],
    ['Q_M_W1_3', 'Year 5 (G5)', 'Mathematics', 'Lesson 2: Factors', 'Prime factors of 24?', 'MCQ', '2^3 x 3 | 4 x 6', '2^3 x 3', 1, 'Index form', 'EX_Y5_MATH_W1', 'W1', 'Challenge'],
    ['Q_M_W2_1', 'Year 5 (G5)', 'Mathematics', 'Lesson 3: Fractions', 'Simplify 4/8?', 'MCQ', '1/2 | 2/3', '1/2', 1, 'Divide by 4', 'EX_Y5_ALI_W2_MATH', 'W2', 'Easy'],
    ['Q_M_W2_2', 'Year 5 (G5)', 'Mathematics', 'Lesson 4: Decimals', '0.25 as fraction?', 'MCQ', '1/4 | 1/2', '1/4', 1, '25/100', 'EX_Y5_ALI_W2_MATH', 'W2', 'Medium'],
    ['Q_M_W3_1', 'Year 5 (G5)', 'Mathematics', 'Lesson 5: Percentages', '50% of 80?', 'MCQ', '40 | 30', '40', 1, 'Half of 80', 'EX_Y5_ALI_W3_MATH', 'W3', 'Easy'],
    ['Q_M_W4_1', 'Year 5 (G5)', 'Mathematics', 'Lesson 6: Word Problems', 'Train 120km in 2h?', 'MCQ', '60 km/h | 50 km/h', '60 km/h', 1, '120/2', 'EX_Y5_ALI_W4_MATH', 'W4', 'Challenge']
  ];
}

test('P6-1: setupDatabase creates Exam_Schedule and 5-subject Study_Plan', () => {
  const env = loadCode({
    Question_Bank: makeSheet('Question_Bank', sampleCumulativeBank()),
    Exams: makeSheet('Exams', [EXAM_HEADERS]),
    Submissions: makeSheet('Submissions', [['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON']])
  });

  env.sandbox.setupDatabase_(env.ss);

  // Check Exam_Schedule
  assert.ok(env.sheets.Exam_Schedule, 'Exam_Schedule tab exists');
  assert.ok(env.sheets.Exam_Schedule.rows.length >= 2, 'Exam_Schedule has rows');
  assert.equal(env.sheets.Exam_Schedule.rows[0].length, 14, 'Exam_Schedule has 14 canonical columns');

  // Check 5-subject Study_Plan
  assert.ok(env.sheets.Study_Plan, 'Study_Plan tab exists');
  const spRows = env.sheets.Study_Plan.rows;
  const subjects = spRows.slice(1).map(r => r[6]); // Subject is col index 6
  assert.ok(subjects.some(s => s.includes('Math')), 'Study_Plan includes Mathematics');
  assert.ok(subjects.some(s => s.includes('Science')), 'Study_Plan includes Science');
  assert.ok(subjects.some(s => s.includes('Grammar') || s.includes('English') || s.includes('Literacy')), 'Study_Plan includes English');
  assert.ok(subjects.some(s => s.includes('العربية') || s.includes('Arabic')), 'Study_Plan includes Arabic');
  assert.ok(subjects.some(s => s.includes('ICT')), 'Study_Plan includes ICT');
});

test('P6-2: loadCumulativeBankQuestionsByPeriod_ coverage-first synthesis and difficulty ordering', () => {
  const env = loadCode({
    Question_Bank: makeSheet('Question_Bank', sampleCumulativeBank()),
    Exams: makeSheet('Exams', [EXAM_HEADERS])
  });

  // W2 cumulative should pull from W1 and W2
  const resW2 = env.sandbox.loadCumulativeBankQuestionsByPeriod_('Year 5 (G5)', 'Mathematics', 'W2');
  assert.ok(resW2.questions.length >= 4, 'W2 includes questions from W1 and W2');
  assert.ok(resW2.coveredWeeks.includes('W1') && resW2.coveredWeeks.includes('W2'), 'Covered weeks are W1 and W2');

  // Check coverage-first: lessons from both W1 and W2 are represented
  const lessons = resW2.questions.map(q => q.lesson);
  assert.ok(lessons.some(l => l.includes('Divisibility') || l.includes('Factors')), 'W1 lesson represented');
  assert.ok(lessons.some(l => l.includes('Fractions') || l.includes('Decimals')), 'W2 lesson represented');

  // Check difficulty ordering: Easy -> Medium -> Challenge
  const diffs = resW2.questions.map(q => q.difficulty.toLowerCase());
  const diffRank = { 'easy': 1, 'foundational': 1, 'medium': 2, 'standard': 2, 'challenge': 3, 'hard': 3 };
  for (let i = 0; i < diffs.length - 1; i++) {
    const rCurrent = diffRank[diffs[i]] || 2;
    const rNext = diffRank[diffs[i + 1]] || 2;
    assert.ok(rCurrent <= rNext, `Questions should be sorted by difficulty: ${diffs[i]} <= ${diffs[i+1]}`);
  }
});

test('P6-3: Same-day non-duplication excludes milestone question IDs from paired daily quiz', () => {
  const env = loadCode({
    Question_Bank: makeSheet('Question_Bank', sampleCumulativeBank()),
    Exams: makeSheet('Exams', [EXAM_HEADERS])
  });

  // Suppose W1 milestone exam uses Q_M_W1_1 and Q_M_W1_2
  const usedInMilestone = ['Q_M_W1_1', 'Q_M_W1_2'];
  const resDaily = env.sandbox.loadCumulativeBankQuestionsByPeriod_('Year 5 (G5)', 'Mathematics', 'W1', 'ALL', usedInMilestone);

  const dailyIds = resDaily.questions.map(q => q.id);
  assert.ok(!dailyIds.includes('Q_M_W1_1'), 'Daily quiz must not contain Q_M_W1_1');
  assert.ok(!dailyIds.includes('Q_M_W1_2'), 'Daily quiz must not contain Q_M_W1_2');
  assert.ok(dailyIds.includes('Q_M_W1_3'), 'Daily quiz picks available non-overlapping question');
});

test('P6-4: getAdaptiveQuestionRecommendations_ responds accurately to student score history', () => {
  // Low score case (<70%)
  const envLow = loadCode({
    Submissions: makeSheet('Submissions', [
      ['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON'],
      ['2026-10-28 10:00', 'Ali Ahmed', 'Year 5 (G5)', 'DAILY_Y5_MATH_W1D1', 3, 5, '60%', 'Developing', '4 min', '3/5', '[]']
    ])
  });
  const recLow = envLow.sandbox.getAdaptiveQuestionRecommendations_('Ali Ahmed', 'Mathematics');
  assert.equal(recLow.adaptiveMode, 'REINFORCEMENT');
  assert.equal(recLow.reinforcementCount, 2);
  assert.equal(recLow.challengeBonus, false);

  // High score case (>=85%)
  const envHigh = loadCode({
    Submissions: makeSheet('Submissions', [
      ['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON'],
      ['2026-10-28 10:00', 'Ali Ahmed', 'Year 5 (G5)', 'DAILY_Y5_MATH_W1D1', 5, 5, '100%', 'Mastery', '3 min', '5/5', '[]']
    ])
  });
  const recHigh = envHigh.sandbox.getAdaptiveQuestionRecommendations_('Ali Ahmed', 'Mathematics');
  assert.equal(recHigh.adaptiveMode, 'CHALLENGE');
  assert.equal(recHigh.challengeBonus, true);
});

test('P6-5: getExamSchedule RPC returns student-isolated schedule and active today exam', () => {
  const schedRows = [
    SCHED_HEADERS,
    ['SCHED_01', '2026-10-30', 'Ali Ahmed', 'Year 5 (G5)', 'Mathematics', 'DAILY_Y5_MATH_W1D1', 'Ali - Math Day 1', 'Daily', 'W1', 5, 10, 'Easy', 'Active', ''],
    ['SCHED_02', '2026-10-30', 'Mostafa Ahmed', 'Grade 6 (G6)', 'Mathematics', 'DAILY_Y6_MATH_W1D1', 'Mostafa - Math Day 1', 'Daily', 'W1', 9, 10, 'Easy', 'Active', '']
  ];
  const env = loadCode({
    Exam_Schedule: makeSheet('Exam_Schedule', schedRows)
  });

  // Verify Ali student token
  const aliTokRes = env.sandbox.verifyGatewayPin('2016');
  assert.ok(aliTokRes.success);

  const resAli = env.sandbox.getExamSchedule('ali', aliTokRes.token);
  assert.equal(resAli.success, true);
  assert.equal(resAli.student, 'Ali Ahmed');
  assert.equal(resAli.schedule.length, 1);
  assert.equal(resAli.todayExam.examCode, 'DAILY_Y5_MATH_W1D1');
});
