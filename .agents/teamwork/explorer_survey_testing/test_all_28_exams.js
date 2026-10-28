const fs = require('fs');
const path = require('path');
const vm = require('vm');

const CODE = fs.readFileSync(path.join(__dirname, '..', '..', '..', 'Code.gs'), 'utf8');

function parseCsv(content) {
  const lines = content.trim().split(/\r?\n/);
  return lines.map(line => {
    const row = [];
    let inside = false;
    let token = '';
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (c === '"') {
        if (inside && line[i+1] === '"') {
          token += '"';
          i++;
        } else {
          inside = !inside;
        }
      } else if (c === ',' && !inside) {
        row.push(token);
        token = '';
      } else {
        token += c;
      }
    }
    row.push(token);
    return row;
  });
}

const exCsv = parseCsv(fs.readFileSync(path.join(__dirname, '..', '..', '..', 'Exams.csv'), 'utf8'));
const qbCsv = parseCsv(fs.readFileSync(path.join(__dirname, '..', '..', '..', 'Question_Bank.csv'), 'utf8'));

class FakeSheet {
  constructor(name, rows) {
    this.name = name;
    this.rows = (rows || []).map(r => r.slice());
  }
  getLastRow() { return this.rows.length; }
  getLastColumn() { return this.rows.length ? Math.max(...this.rows.map(r => r.length)) : 0; }
  getDataRange() { return { getValues: () => this.rows.map(r => r.slice()) }; }
  appendRow(row) { this.rows.push(row.slice()); }
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

const englishExamHeader = [
  'Exam Code', 'Exam Title', 'Grade Level', 'Subject', 'Questions',
  'Duration (Mins)', 'Status', 'Direct URL', 'Created Date', 'Exam Type', 'Target Period'
];
const examsSheetRows = [englishExamHeader].concat(exCsv.slice(1));

const englishQbHeader = [
  'Question ID', 'Grade Level', 'Subject', 'Unit / Topic', 'Question Text', 'Type',
  'Options (delimited by |)', 'Correct Answer', 'Points',
  'Pedagogical Explanation & Mistake Breakdown', 'Exam Code', 'Week', 'Difficulty'
];
const qbSheetRows = [englishQbHeader].concat(qbCsv.slice(1));

const sheets = {
  Question_Bank: new FakeSheet('Question_Bank', qbSheetRows),
  Exams: new FakeSheet('Exams', examsSheetRows),
  Submissions: new FakeSheet('Submissions', [['Timestamp', 'Student Name', 'School Grade', 'Exam Code', 'Score', 'Total', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON']]),
  Retake_Requests: new FakeSheet('Retake_Requests', [['Request ID', 'Timestamp', 'Student Name', 'Exam Code', 'Exam Title', 'Previous Score', 'Status', 'Reason', 'Decision Timestamp']]),
  Sessions: new FakeSheet('Sessions', [['Session ID', 'Created At', 'Student Name', 'Exam Code', 'School Grade', 'Started At', 'Expires At', 'Status', 'Questions JSON', 'Result JSON']]),
  Study_Plan: new FakeSheet('Study_Plan', [['Plan ID', 'Week', 'Day', 'Day Label', 'Student Name', 'Grade Level', 'Subject', 'Unit / Topic', 'Lesson Title', 'Skills', 'Questions Count', 'Status', 'Exam Code']])
};

const ss = {
  getSheetByName(name) { return sheets[name] || null; },
  insertSheet(name) {
    const s = new FakeSheet(name, []);
    sheets[name] = s;
    return s;
  },
  getId() { return 'test-id'; },
  getUrl() { return 'https://test'; }
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
      setProperty: (k, v) => { props[k] = v; }
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

// Initialize database
sandbox.setupDatabase(ss);

const all_28 = [
  'DAILY_Y5_ENG_W1D1', 'DAILY_Y5_ENG_W1D2', 'DAILY_Y5_ENG_W1D3', 'DAILY_Y5_ENG_W1D4',
  'DAILY_Y5_ENG_W1D5', 'DAILY_Y5_ENG_W1D6', 'DAILY_Y5_ENG_W2D8', 'DAILY_Y5_ENG_W2D9',
  'DAILY_Y5_ENG_W2D10', 'EX_Y5_ENG_W1', 'EX_Y5_ENG_W2_CUMULATIVE', 'EX_Y5_ENG_W3_CUMULATIVE',
  'EX_Y5_ENG_W4_CUMULATIVE', 'EX_Y5_ENG_M1_CAPSTONE', 'EX_Y5_ENG_ADV01',
  'DAILY_Y6_ARB_W1D4', 'DAILY_Y6_ARB_W1D5', 'DAILY_Y6_ARB_W1D6', 'DAILY_Y6_ARB_W2D8',
  'DAILY_Y6_ARB_W2D9', 'DAILY_Y6_ARB_W2D10', 'EX_Y6_ARB_W1', 'EX_Y6_ARB_W2_CUMULATIVE',
  'EX_Y6_ARB_W3_CUMULATIVE', 'EX_Y6_ARB_W4_CUMULATIVE', 'EX_Y6_ARB_M1_CAPSTONE',
  'EX_Y6_ARB_PRIO01', 'EX_Y6_ENG_FANTASY01'
];

console.log('Testing full E2E lifecycle (getExamData -> answer all correctly -> submitExamAnswers) for all 28 exams:');
let submitSuccess = 0;

for (const code of all_28) {
  const student = code.includes('Y5') ? 'Ali Ahmed' : 'Mostafa Ahmed';
  const examData = sandbox.getExamData(code, student);
  if (!examData || !examData.success) {
    console.log(`[GET FAIL] ${code}`);
    continue;
  }
  
  // Find secret answers stored in Sessions sheet
  const sessRow = sheets.Sessions.rows.find(r => String(r[0]) === String(examData.sessionKey));
  const fullQuestions = JSON.parse(sessRow[8]);
  const answers = {};
  fullQuestions.forEach(q => {
    answers[q.id] = q.correctAnswer;
  });

  const subRes = sandbox.submitExamAnswers({
    studentName: student,
    examCode: code,
    sessionKey: examData.sessionKey,
    answers: answers
  });

  if (subRes && subRes.success && subRes.percentage === 100) {
    console.log(`[PASS 100%] ${code}: Scored ${subRes.earnedScore}/${subRes.totalScore} points`);
    submitSuccess++;
  } else {
    console.log(`[SUBMIT FAIL] ${code}:`, subRes);
  }
}

console.log(`\nSubmissions result: ${submitSuccess}/28 successfully scored 100%!`);
console.log(`Submissions sheet total rows: ${sheets.Submissions.rows.length} (1 header + ${sheets.Submissions.rows.length - 1} submissions)`);
