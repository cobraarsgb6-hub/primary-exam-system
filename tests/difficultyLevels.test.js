// Contract tests for P4: Exam Engine Adaptive Difficulty Levels & 5-Subject Factory
// Run with: node --test tests/difficultyLevels.test.js
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const BANK_HEADER = [
  'Question ID', 'Grade Level', 'Subject', 'Unit / Topic', 'Question Text', 'Type',
  'Options (delimited by |)', 'Correct Answer', 'Points',
  'Pedagogical Explanation & Mistake Breakdown', 'Exam Code', 'Week', 'Difficulty'
];
const EXAM_HEADER = [
  'Exam Code', 'Exam Title', 'Grade Level', 'Subject', 'Questions', 'Duration (Mins)',
  'Status', 'Direct URL', 'Created Date', 'Exam Type', 'Target Period', 'Difficulty'
];

function makeSheet(rows) {
  const self = {
    rows: rows,
    getLastRow: () => rows.length,
    getLastColumn: () => (rows.length ? Math.max(...rows.map(row => row.length)) : 0),
    getDataRange: () => ({ getValues: () => rows.map(row => row.slice()) }),
    setColumnWidth: () => {},
    getRange(row, col, numRows, numCols) {
      const nr = numRows || 1;
      const nc = numCols || 1;
      const chain = {
        getValues() {
          const out = [];
          for (let i = 0; i < nr; i++) {
            const source = rows[row - 1 + i] || [];
            const line = [];
            for (let j = 0; j < nc; j++) line.push(source[col - 1 + j]);
            out.push(line);
          }
          return out;
        },
        setValues(newVals) {
          for (let i = 0; i < newVals.length; i++) {
            const rIdx = row - 1 + i;
            while (rows.length <= rIdx) rows.push([]);
            for (let j = 0; j < newVals[i].length; j++) {
              rows[rIdx][col - 1 + j] = newVals[i][j];
            }
          }
          return chain;
        },
        setValue(val) {
          const rIdx = row - 1;
          while (rows.length <= rIdx) rows.push([]);
          rows[rIdx][col - 1] = val;
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
    },
    appendRow(rowValues) {
      rows.push(rowValues.slice());
    }
  };
  return self;
}

function loadCode(sheets) {
  const code = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');
  const props = {
    ADMIN_PIN_HASH: 'FALLBACK_HASH_1450536879',
    ALI_PIN_HASH: 'FALLBACK_HASH_1450515979',
    MOSTAFA_PIN_HASH: 'FALLBACK_HASH_1450515981'
  };
  let uuid = 0;
  const sandbox = {
    console,
    Logger: { log: () => {} },
    Utilities: { formatDate: date => date.toISOString(), getUuid: () => 'uuid-' + (++uuid) },
    Session: { getScriptTimeZone: () => 'GMT+2' },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: key => props[key] || null,
        setProperty: (key, value) => { props[key] = value; }
      }),
      getUserProperties: () => ({ getProperty: () => null })
    },
    CacheService: { getScriptCache: () => ({ put() {}, get() { return null; } }) },
    LockService: { getScriptLock: () => ({ tryLock: () => true, waitLock: () => true, releaseLock() {} }) },
    SpreadsheetApp: {
      getActiveSpreadsheet: () => ({
        getId: () => 'test-sheet',
        getSheetByName: name => sheets[name] || null,
        insertSheet: name => {
          sheets[name] = makeSheet([]);
          return sheets[name];
        }
      })
    }
  };
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox, { filename: 'Code.gs' });
  return sandbox;
}

function sampleBankWithLevels() {
  return [
    BANK_HEADER,
    ['Q_EAS_1', 'Year 5 (G5)', 'Mathematics', 'Unit 1', 'Math Easy Q1', 'MCQ', 'A|B', 'A', 1, 'Exp', '', 'W1', 'Easy'],
    ['Q_EAS_2', 'Year 5 (G5)', 'Mathematics', 'Unit 1', 'Math Easy Q2', 'MCQ', 'A|B', 'B', 1, 'Exp', '', 'W1', 'Foundational'],
    ['Q_MED_1', 'Year 5 (G5)', 'Mathematics', 'Unit 1', 'Math Medium Q1', 'MCQ', 'A|B', 'A', 1, 'Exp', '', 'W1', 'Medium'],
    ['Q_MED_2', 'Year 5 (G5)', 'Mathematics', 'Unit 1', 'Math Medium Q2', 'MCQ', 'A|B', 'B', 1, 'Exp', '', 'W1', 'Standard'],
    ['Q_HAR_1', 'Year 5 (G5)', 'Mathematics', 'Unit 1', 'Math Hard Q1', 'MCQ', 'A|B', 'A', 1, 'Exp', '', 'W1', 'Hard'],
    ['Q_HAR_2', 'Year 5 (G5)', 'Mathematics', 'Unit 1', 'Math Hard Q2', 'MCQ', 'A|B', 'B', 1, 'Exp', '', 'W1', 'Challenging'],
    ['Q_SCI_1', 'Year 5 (G5)', 'Science', 'Unit 1', 'Sci Q1', 'MCQ', 'A|B', 'A', 1, 'Exp', '', 'W1', 'Challenging'],
    ['Q_ICT_1', 'Year 5 (G5)', 'ICT Computing', 'Unit 1', 'ICT Q1', 'MCQ', 'A|B', 'A', 1, 'Exp', '', 'W1', 'Standard'],
    ['Q_SOC_1', 'Year 5 (G5)', 'Social Studies', 'Unit 1', 'Soc Q1', 'MCQ', 'A|B', 'A', 1, 'Exp', '', 'W1', 'Standard'],
    ['Q_SOC_2', 'Grade 6 (G6)', 'الدراسات الاجتماعية', 'الوحدة 1', 'Soc G6 Q1', 'MCQ', 'A|B', 'A', 1, 'Exp', '', 'W1', 'Challenging']
  ];
}

test('matchDifficultyLevel_ canonical matching', () => {
  const sandbox = loadCode({});
  assert.equal(sandbox.matchDifficultyLevel_('Easy', 'Foundational'), true);
  assert.equal(sandbox.matchDifficultyLevel_('Foundational', '1'), true);
  assert.equal(sandbox.matchDifficultyLevel_('Medium', 'Standard'), true);
  assert.equal(sandbox.matchDifficultyLevel_('Core', '2'), true);
  assert.equal(sandbox.matchDifficultyLevel_('Hard', 'Challenging'), true);
  assert.equal(sandbox.matchDifficultyLevel_('Adv Challenge', '3'), true);
  assert.equal(sandbox.matchDifficultyLevel_('Easy', 'Challenging'), false);
  assert.equal(sandbox.matchDifficultyLevel_('Hard', 'Foundational'), false);
  assert.equal(sandbox.matchDifficultyLevel_('Any', 'ALL'), true);
});

test('loadBankQuestionsByPeriod_ strictly filters by specified difficulty', () => {
  const sandbox = loadCode({
    Question_Bank: makeSheet(sampleBankWithLevels())
  });

  const challenging = sandbox.loadBankQuestionsByPeriod_('Year 5 (G5)', 'Mathematics', 'W1', 'Challenging');
  assert.equal(challenging.length, 2);
  assert.equal(challenging.every(q => q.id === 'Q_HAR_1' || q.id === 'Q_HAR_2'), true);

  const foundational = sandbox.loadBankQuestionsByPeriod_('Year 5 (G5)', 'Mathematics', 'W1', 'Foundational');
  assert.equal(foundational.length, 2);
  assert.equal(foundational.every(q => q.id === 'Q_EAS_1' || q.id === 'Q_EAS_2'), true);

  const standard = sandbox.loadBankQuestionsByPeriod_('Year 5 (G5)', 'Mathematics', 'W1', 'Standard');
  assert.equal(standard.length, 2);
  assert.equal(standard.every(q => q.id === 'Q_MED_1' || q.id === 'Q_MED_2'), true);

  const allLevels = sandbox.loadBankQuestionsByPeriod_('Year 5 (G5)', 'Mathematics', 'W1', 'ALL');
  assert.equal(allLevels.length, 6);
});

test('createWeeklyExam_ generates unique code with difficulty and custom count/duration', () => {
  const sheets = {
    Question_Bank: makeSheet(sampleBankWithLevels()),
    Exams: makeSheet([EXAM_HEADER])
  };
  const sandbox = loadCode(sheets);
  const token = sandbox.verifyAdminPin('1990').token;

  const result = sandbox.createWeeklyExam({
    studentKey: 'ali',
    weekCode: 'W1',
    subject: 'Mathematics',
    difficulty: 'Challenging',
    count: 2,
    duration: 15
  }, token);

  assert.equal(result.success, true);
  assert.equal(result.examCode, 'EX_Y5_ALI_W1_MATH_CHA');
  assert.equal(result.questionsCount, 2);
  assert.equal(result.difficulty, 'Challenging');

  // Verify that building questions for this exam returns ONLY Level 3 / Challenging questions!
  const built = sandbox.buildExamQuestions_('EX_Y5_ALI_W1_MATH_CHA');
  assert.equal(built.questions.length, 2);
  assert.equal(built.questions.every(q => q.id === 'Q_HAR_1' || q.id === 'Q_HAR_2'), true);
});

test('createMonthlyExam_ with custom subject and difficulty generates unique code and questions', () => {
  const sheets = {
    Question_Bank: makeSheet(sampleBankWithLevels()),
    Exams: makeSheet([EXAM_HEADER])
  };
  const sandbox = loadCode(sheets);
  const token = sandbox.verifyAdminPin('1990').token;

  const res = sandbox.createMonthlyExam({
    studentKey: 'ali',
    monthCode: 'M1',
    subject: 'Mathematics',
    difficulty: 'Foundational',
    count: 2,
    duration: 25
  }, token);

  assert.equal(res.success, true);
  assert.equal(res.examCode, 'EX_Y5_ALI_M1_MATH_FOU_CUMULATIVE');
  assert.equal(res.questionsCount, 2);
  assert.equal(res.difficulty, 'Foundational');

  // Verify that building questions returns only Foundational questions
  const built = sandbox.buildExamQuestions_('EX_Y5_ALI_M1_MATH_FOU_CUMULATIVE');
  assert.equal(built.questions.length, 2);
  assert.equal(built.questions.every(q => q.id === 'Q_EAS_1' || q.id === 'Q_EAS_2'), true);
});

test('createWeeklyExam_ supports Science and ICT subjects', () => {
  const sheets = {
    Question_Bank: makeSheet(sampleBankWithLevels()),
    Exams: makeSheet([EXAM_HEADER])
  };
  const sandbox = loadCode(sheets);
  const token = sandbox.verifyAdminPin('1990').token;

  const sciRes = sandbox.createWeeklyExam({
    studentKey: 'ali',
    weekCode: 'W1',
    subject: 'Science',
    difficulty: 'Challenging'
  }, token);
  assert.equal(sciRes.success, true);
  assert.equal(sciRes.examCode, 'EX_Y5_ALI_W1_SCI_CHA');

  const ictRes = sandbox.createWeeklyExam({
    studentKey: 'ali',
    weekCode: 'W1',
    subject: 'ICT Computing',
    difficulty: 'Standard'
  }, token);
  assert.equal(ictRes.success, true);
  assert.equal(ictRes.examCode, 'EX_Y5_ALI_W1_ICT_STA');

  const socRes = sandbox.createWeeklyExam({
    studentKey: 'mostafa',
    weekCode: 'W1',
    subject: 'الدراسات الاجتماعية',
    difficulty: 'Challenging'
  }, token);
  assert.equal(socRes.success, true);
  assert.equal(socRes.examCode, 'EX_Y6_MOS_W1_SOC_CHA');
});
