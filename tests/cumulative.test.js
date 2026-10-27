// Contract tests for the cumulative/weekly bank slices and the exam factory
// fallback. Run with: node --test tests/cumulative.test.js
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
  'Status', 'Direct URL', 'Created Date', 'Exam Type', 'Target Period'
];

function makeSheet(rows) {
  return {
    getLastRow: () => rows.length,
    getLastColumn: () => (rows.length ? Math.max(...rows.map(row => row.length)) : 0),
    getDataRange: () => ({ getValues: () => rows.map(row => row.slice()) }),
    getRange(row, col, numRows, numCols) {
      const nr = numRows || 1;
      const nc = numCols || 1;
      return {
        getValues() {
          const out = [];
          for (let i = 0; i < nr; i++) {
            const source = rows[row - 1 + i] || [];
            const line = [];
            for (let j = 0; j < nc; j++) line.push(source[col - 1 + j]);
            out.push(line);
          }
          return out;
        }
      };
    }
  };
}

function loadCode(sheets) {
  const code = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');
  const sandbox = {
    console,
    Logger: { log: () => {} },
    Utilities: { formatDate: date => date.toISOString() },
    Session: { getScriptTimeZone: () => 'GMT+2' },
    PropertiesService: {
      getScriptProperties: () => ({ getProperty: () => null, setProperty: () => {} })
    },
    SpreadsheetApp: {
      getActiveSpreadsheet: () => ({
        getId: () => 'test-sheet',
        getSheetByName: name => sheets[name] || null
      })
    }
  };
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox, { filename: 'Code.gs' });
  return sandbox;
}

function bankRows() {
  return [
    ['Q1', 'Year 5 (G5)', 'English Grammar', 'Unit 2', 'English W1 question?', 'MCQ', 'A | B', 'A', 1, 'Because A.', '', 'W1', 'Standard'],
    ['Q2', 'Year 5 (G5)', 'English Grammar', 'Unit 2', 'English W2 question?', 'MCQ', 'A | B', 'B', 1, 'Because B.', '', 'W2', 'Standard'],
    ['Q3', 'Year 5 (G5)', 'Arabic Language', 'Unit 1', 'Arabic W2 question?', 'MCQ', 'أ | ب', 'أ', 1, 'لأن أ.', '', 'W2', 'Standard'],
    ['Q4', 'Grade 6 (G6)', 'English Grammar', 'Unit 2', 'Grade 6 W2 question?', 'MCQ', 'A | B', 'A', 1, 'Because A.', '', 'W2', 'Standard']
  ];
}

test('loadBankQuestionsByPeriod_ isolates grade/subject and expands monthly slices', () => {
  const sandbox = loadCode({
    Question_Bank: makeSheet([BANK_HEADER].concat(bankRows()))
  });

  const weekly = sandbox.loadBankQuestionsByPeriod_('Year 5 (G5)', 'English Grammar', 'W2');
  assert.equal(weekly.length, 1, 'only the Year 5 English W2 row');
  assert.equal(weekly[0].id, 'Q2');

  const monthly = sandbox.loadBankQuestionsByPeriod_('Year 5 (G5)', 'English Grammar', 'M1');
  assert.equal(monthly.map(question => question.id).sort().join(','), 'Q1,Q2',
    'monthly slices include every week but never Arabic or G6 rows');
});

test('buildExamQuestions_ serves generated exams from their target period', () => {
  const sandbox = loadCode({
    Question_Bank: makeSheet([BANK_HEADER].concat(bankRows())),
    Exams: makeSheet([
      EXAM_HEADER,
      ['EX_Y5_ALI_M1_CUMULATIVE', 'Ali - Month 1 Cumulative', 'Year 5 (G5)', 'English Grammar',
        10, 30, 'ACTIVE', '', new Date(), 'Monthly', 'M1']
    ])
  });

  const built = sandbox.buildExamQuestions_('EX_Y5_ALI_M1_CUMULATIVE');
  assert.equal(built.exam.targetPeriod, 'M1');
  assert.equal(built.questions.map(question => question.id).sort().join(','), 'Q1,Q2');
  assert.equal(built.questions.every(question => question.options.length >= 2), true);
});
