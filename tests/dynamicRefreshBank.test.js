// tests/dynamicRefreshBank.test.js
// Phase P13: 014-full-refresh-question-bank
// Rigorous verification of dynamic question synthesizer, mathematical correctness,
// full refresh uniqueness, and client refresh controls.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

// Read Code.gs and extract the dynamic generator engine
const codeGsPath = path.join(__dirname, '..', 'Code.gs');
const codeGsContent = fs.readFileSync(codeGsPath, 'utf8');

// Provide mock environment to execute Code.gs dynamic synthesizer in Node
const mockContext = {
  Math: Math,
  String: String,
  Number: Number,
  Object: Object,
  Array: Array,
  Date: Date,
  JSON: JSON,
  shuffleArray: function (arr) {
    const copy = arr.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const t = copy[i];
      copy[i] = copy[j];
      copy[j] = t;
    }
    return copy;
  },
  subjectFamily_: function (subj) {
    const s = String(subj || '').toLowerCase();
    if (s.indexOf('math') !== -1 || s.indexOf('رياضيات') !== -1) return 'math';
    if (s.indexOf('sci') !== -1 || s.indexOf('علوم') !== -1) return 'science';
    return 'other';
  }
};

// Evaluate synthesizer functions inside mock context
const scriptToEval = `
  (function(ctx) {
    const Math = ctx.Math;
    const shuffleArray = ctx.shuffleArray;
    const subjectFamily_ = ctx.subjectFamily_;

    ${codeGsContent.slice(codeGsContent.indexOf('function generatePrimeFactorQuestion_('))}
  })(mockContext);
`;

// Helper sandbox runner
const fnHolder = {};
const evalRunner = new Function('holder', 'ctx', `
  const Math = ctx.Math;
  const shuffleArray = ctx.shuffleArray;
  const subjectFamily_ = ctx.subjectFamily_;

  ${codeGsContent.slice(codeGsContent.indexOf('function generatePrimeFactorQuestion_('))}

  holder.generatePrimeFactorQuestion_ = generatePrimeFactorQuestion_;
  holder.generateFDPQuestion_ = generateFDPQuestion_;
  holder.generateDivisionQuestion_ = generateDivisionQuestion_;
  holder.generateBODMASQuestion_ = generateBODMASQuestion_;
  holder.generatePlaceValueQuestion_ = generatePlaceValueQuestion_;
  holder.generateDivisibilityQuestion_ = generateDivisibilityQuestion_;
  holder.generateRoundingQuestion_ = generateRoundingQuestion_;
  holder.generateCircuitsDynamicQuestion_ = generateCircuitsDynamicQuestion_;
  holder.synthesizeDynamicQuestions_ = synthesizeDynamicQuestions_;
`);

evalRunner(fnHolder, mockContext);

test('P13: Prime Factorization question produces mathematically sound prime powers', () => {
  for (let i = 0; i < 20; i++) {
    const q = fnHolder.generatePrimeFactorQuestion_(2, 1000 + i);
    assert.ok(q.id.startsWith('DYN_MATH_PRIME_'), 'ID format matches dynamic prime');
    assert.ok(q.correctAnswer, 'Correct answer must be defined');

    // Parse the powers and verify the product equals the number in the question
    const numMatch = q.text.match(/<b>(\d+)<\/b>/);
    assert.ok(numMatch, 'Question text contains target number');
    const targetNum = Number(numMatch[1]);

    const factors = q.correctAnswer.split(' × ');
    let product = 1;
    factors.forEach(f => {
      if (f.includes('^')) {
        const [base, exp] = f.split('^').map(Number);
        product *= Math.pow(base, exp);
      } else {
        product *= Number(f);
      }
    });

    assert.equal(product, targetNum, `Prime factor product (${product}) must equal target number (${targetNum})`);
    assert.equal(q.options.length, 4, 'Must have exactly 4 MCQ options');
    assert.ok(q.options.includes(q.correctAnswer), 'Options must include the correct answer');
  }
});

test('P13: Long Division Bus Stop generator verifies dividend = divisor * quotient + remainder', () => {
  for (let i = 0; i < 20; i++) {
    const q = fnHolder.generateDivisionQuestion_(2, 2000 + i);
    const divMatch = q.text.match(/<b>(\d+)\s*÷\s*(\d+)<\/b>/);
    assert.ok(divMatch, 'Division expression captured');
    const dividend = Number(divMatch[1]);
    const divisor = Number(divMatch[2]);

    let quotient, remainder;
    if (q.correctAnswer.includes(' r ')) {
      const parts = q.correctAnswer.split(' r ').map(Number);
      quotient = parts[0];
      remainder = parts[1];
    } else {
      quotient = Number(q.correctAnswer);
      remainder = 0;
    }

    assert.equal(divisor * quotient + remainder, dividend, 'Division identity must strictly hold');
    assert.ok(remainder < divisor, 'Remainder must be strictly less than divisor');
  }
});

test('P13: Tests of Divisibility generator evaluates exact mathematical truth', () => {
  for (let i = 0; i < 20; i++) {
    const q = fnHolder.generateDivisibilityQuestion_(1, 3000 + i);
    const match = q.text.match(/<b>([\d,]+)<\/b>.*<b>(\d+)<\/b>/);
    assert.ok(match, 'Captured number and divisor');
    const n = Number(match[1].replace(/,/g, ''));
    const k = Number(match[2]);

    const actuallyDivisible = (n % k === 0);
    const expectedAnswer = actuallyDivisible ? 'Yes (يقبل القسمة)' : 'No (لا يقبل القسمة)';
    assert.equal(q.correctAnswer, expectedAnswer, `Divisibility test for ${n} by ${k} must match`);
  }
});

test('P13: Rounding generator matches nearest scale', () => {
  for (let i = 0; i < 20; i++) {
    const q = fnHolder.generateRoundingQuestion_(2, 4000 + i);
    const match = q.text.match(/<b>([\d,]+)<\/b>.*<b>([\d,]+)<\/b>/);
    assert.ok(match, 'Captured number and rounding scale');
    const n = Number(match[1].replace(/,/g, ''));
    const scale = Number(match[2].replace(/,/g, ''));

    const expectedRounded = Math.round(n / scale) * scale;
    assert.equal(Number(q.correctAnswer.replace(/,/g, '')), expectedRounded, 'Rounded value must be exact');
  }
});

test('P13: Full Refresh produces non-identical question sets across consecutive calls', () => {
  const set1 = fnHolder.synthesizeDynamicQuestions_('Grade 6 (G6)', 'Mathematics', 10, 'ALL', 1111);
  const set2 = fnHolder.synthesizeDynamicQuestions_('Grade 6 (G6)', 'Mathematics', 10, 'ALL', 9999);

  assert.equal(set1.length, 10, 'Set 1 must contain 10 questions');
  assert.equal(set2.length, 10, 'Set 2 must contain 10 questions');

  // Compare IDs or texts to ensure non-identical dynamic synthesis
  const ids1 = set1.map(q => q.id).join(',');
  const ids2 = set2.map(q => q.id).join(',');
  assert.notEqual(ids1, ids2, 'Subsequent dynamic refreshes must produce distinct questions');
});

test('P13: Question Synthesizer balances across L1, L2, L3 tiers', () => {
  const questions = fnHolder.synthesizeDynamicQuestions_('Grade 6 (G6)', 'Mathematics', 15, 'ALL', 12345);
  const levels = questions.map(q => q.difficulty);

  const easyCount = levels.filter(d => d === 'Easy').length;
  const medCount = levels.filter(d => d === 'Medium').length;
  const hardCount = levels.filter(d => d === 'Hard').length;

  assert.ok(easyCount > 0, 'Must contain Easy (L1) questions');
  assert.ok(medCount > 0, 'Must contain Medium (L2) questions');
  assert.ok(hardCount > 0, 'Must contain Hard (L3) questions');
});

test('P13: Client Quiz UI contains Dynamic Refresh Bank button and handler', () => {
  const quizAppHtml = fs.readFileSync(path.join(__dirname, '..', 'QuizApp.js.html'), 'utf8');

  assert.ok(quizAppHtml.includes('btn-quiz-refresh-bank'), 'Must contain #btn-quiz-refresh-bank button');
  assert.ok(quizAppHtml.includes('refreshQuizQuestions'), 'Must declare refreshQuizQuestions handler');
  assert.ok(quizAppHtml.includes('window.refreshQuizQuestions'), 'Must export refreshQuizQuestions to window');
});
