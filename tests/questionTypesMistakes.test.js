const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function loadCodeContext() {
  const code = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');
  const props = {
    ADMIN_PIN_HASH: 'FALLBACK_HASH_1450536879',
    ALI_PIN_HASH: 'FALLBACK_HASH_1450515979',
    MOSTAFA_PIN_HASH: 'FALLBACK_HASH_1450515981'
  };
  const cacheStore = {};
  let uuid = 0;
  const context = {
    Logger: { log: () => {} },
    console: console,
    Utilities: {
      formatDate: () => '2026-10-25 00:00',
      getUuid: () => 'uuid-' + (++uuid)
    },
    Session: { getScriptTimeZone: () => 'GMT+2' },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: (key) => props[key] || null,
        setProperty: (key, val) => { props[key] = val; },
        setProperties: (obj) => Object.assign(props, obj),
        deleteProperty: (key) => { delete props[key]; }
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
    LockService: {
      getScriptLock: () => ({ tryLock: () => true, waitLock: () => true, releaseLock() {} })
    },
    SpreadsheetApp: {
      WrapStrategy: { WRAP: 'WRAP' }
    }
  };
  vm.createContext(context);
  vm.runInContext(code, context);
  return context;
}

test('Phase 7 Test 1: isAnswerCorrect_ free-text matching with case & whitespace normalization', () => {
  const ctx = loadCodeContext();
  const { isAnswerCorrect_ } = ctx;

  assert.equal(isAnswerCorrect_('Photosynthesis', 'photosynthesis'), true);
  assert.equal(isAnswerCorrect_('  oxygen  ', 'oxygen'), true);
  assert.equal(isAnswerCorrect_('Carbon Dioxide', 'carbon dioxide'), true);
  assert.equal(isAnswerCorrect_('nitrogen', 'oxygen'), false);
  assert.equal(isAnswerCorrect_('', 'oxygen'), false);
  assert.equal(isAnswerCorrect_(null, 'oxygen'), false);
});

test('Phase 7 Test 2: isAnswerCorrect_ pipe-delimited candidate answers', () => {
  const ctx = loadCodeContext();
  const { isAnswerCorrect_ } = ctx;

  const validOptions = '22|twenty two|twenty-two|٢٢';
  assert.equal(isAnswerCorrect_('22', validOptions), true);
  assert.equal(isAnswerCorrect_('twenty two', validOptions), true);
  assert.equal(isAnswerCorrect_('TWENTY TWO', validOptions), true);
  assert.equal(isAnswerCorrect_('٢٢', validOptions), true);
  assert.equal(isAnswerCorrect_('23', validOptions), false);
});

test('Phase 7 Test 3: isAnswerCorrect_ Arabic text normalization with harakat and teh marbuta folding', () => {
  const ctx = loadCodeContext();
  const { isAnswerCorrect_ } = ctx;

  // Harakat stripping
  assert.equal(isAnswerCorrect_('مَفْعُولٌ بِهِ', 'مفعول به'), true);
  assert.equal(isAnswerCorrect_('الْفَاعِلُ', 'الفاعل'), true);

  // Alef folding & teh marbuta / heh
  assert.equal(isAnswerCorrect_('إجابة', 'اجابة'), true);
  assert.equal(isAnswerCorrect_('اجابه', 'إجابة'), true);
  assert.equal(isAnswerCorrect_('مكتبة', 'مكتبه'), true);
});

test('Phase 7 Test 4: gradeAnswers_ scores mixed question types (MCQ, FILL_IN, TRUE_FALSE)', () => {
  const ctx = loadCodeContext();
  const { gradeAnswers_ } = ctx;

  const questions = [
    { id: 'Q1', text: 'Capital of France?', type: 'MCQ', correctAnswer: 'Paris', points: 1 },
    { id: 'Q2', text: 'Define speed formula', type: 'FILL_IN', correctAnswer: 'distance / time|distance divided by time', points: 2 },
    { id: 'Q3', text: 'Sound travels in a vacuum', type: 'TRUE_FALSE', correctAnswer: 'False', points: 1 }
  ];

  const studentAnswers = {
    Q1: 'Paris',
    Q2: 'distance / time',
    Q3: 'False'
  };

  const result = gradeAnswers_(questions, studentAnswers);
  assert.equal(result.earnedScore, 4);
  assert.equal(result.totalScore, 4);
  assert.equal(result.percentage, 100);
  assert.equal(result.reviewDetails.length, 3);
  assert.equal(result.reviewDetails[1].isCorrect, true);
  assert.equal(result.reviewDetails[1].pointsAwarded, 2);
});

test('Phase 7 Test 5: getStudentMistakes enforces strict cross-student data isolation', () => {
  const ctx = loadCodeContext();
  const { getStudentMistakes, verifyGatewayPin } = ctx;

  // Set up mock spreadsheet with Submissions containing Ali's and Mostafa's attempts
  const submissionsData = [
    ['Timestamp', 'Student Name', 'Grade Level', 'Exam Code', 'Earned Score', 'Total Score', 'Percentage', 'Rating', 'Duration', 'Summary', 'Detailed Review JSON'],
    [
      '2026-10-25 10:00',
      'Ali Ahmed',
      'Year 5 (G5)',
      'DAILY_Y5_ENG_W1D1',
      0,
      1,
      '0%',
      'Needs Practice 🌱',
      '2 Mins',
      '0/1',
      JSON.stringify([
        { questionId: 'Q_ALI_01', questionText: 'Ali fronted adverbial question', studentAnswer: 'walked', correctAnswer: 'quickly walked', isCorrect: false, explanation: 'Needs adverb of manner.' }
      ])
    ],
    [
      '2026-10-25 11:00',
      'Mostafa Ahmed',
      'Grade 6 (G6)',
      'DAILY_Y6_SCI_W1D1',
      0,
      1,
      '0%',
      'Needs Practice 🌱',
      '2 Mins',
      '0/1',
      JSON.stringify([
        { questionId: 'Q_MOS_01', questionText: 'Mostafa circulatory question', studentAnswer: 'veins', correctAnswer: 'arteries', isCorrect: false, explanation: 'High pressure.' }
      ])
    ]
  ];

  const makeSheet = (rows) => ({
    getLastRow: () => rows.length,
    getLastColumn: () => rows[0].length,
    getDataRange: () => ({
      getValues: () => rows.map(r => r.slice())
    }),
    getRange: (r, c, nr, nc) => ({
      getValues: () => {
        const out = [];
        for (let i = 0; i < (nr || 1); i++) {
          const rowIdx = (r - 1) + i;
          const line = [];
          for (let j = 0; j < (nc || 1); j++) {
            line.push(rows[rowIdx] ? rows[rowIdx][(c - 1) + j] : '');
          }
          out.push(line);
        }
        return out;
      }
    })
  });

  const ss = {
    getSheetByName: (name) => {
      if (name === 'Submissions') return makeSheet(submissionsData);
      return null;
    }
  };
  ctx.getSpreadsheet_ = () => ss;

  // Authenticate Ali (PIN: 2016)
  const aliTokRes = verifyGatewayPin('2016');
  assert.equal(aliTokRes.success, true);
  const aliToken = aliTokRes.token;

  // Authenticate Mostafa (PIN: 2014)
  const mosTokRes = verifyGatewayPin('2014');
  assert.equal(mosTokRes.success, true);
  const mosToken = mosTokRes.token;

  // Ali requests Ali's mistakes -> gets exactly Ali's question
  const aliMistakes = getStudentMistakes('ali', aliToken);
  assert.equal(aliMistakes.success, true);
  assert.equal(aliMistakes.count, 1);
  assert.equal(aliMistakes.mistakes[0].questionId, 'Q_ALI_01');
  assert.equal(aliMistakes.mistakes[0].questionText, 'Ali fronted adverbial question');

  // Mostafa requests Mostafa's mistakes -> gets exactly Mostafa's question
  const mosMistakes = getStudentMistakes('mostafa', mosToken);
  assert.equal(mosMistakes.success, true);
  assert.equal(mosMistakes.count, 1);
  assert.equal(mosMistakes.mistakes[0].questionId, 'Q_MOS_01');
  assert.equal(mosMistakes.mistakes[0].questionText, 'Mostafa circulatory question');

  // Cross-student forgery attempt: Ali tries to get Mostafa's mistakes with Ali's token -> BLOCKED!
  const forged = getStudentMistakes('mostafa', aliToken);
  assert.equal(forged.success, false);
  assert.equal(forged.code, 'UNAUTHORIZED');
});
