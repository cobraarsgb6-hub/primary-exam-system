// tests/dynamicLevelBanks.test.js
// Phase P14: 015-dynamic-level-banks
// Verifies bank density (>= 45 questions per core lesson: 15 L1, 15 L2, 15 L3),
// zero placeholders, pedagogical explanation integrity, and level stratification.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

// Read Code.gs and extract getStarterQuestionBank_
const codeGsPath = path.join(__dirname, '..', 'Code.gs');
const codeGsContent = fs.readFileSync(codeGsPath, 'utf8');

const bankMatch = codeGsContent.match(/function getStarterQuestionBank_\(\)\s*\{\s*return\s*(\[[\s\S]*?\]);\s*\}/);
assert.ok(bankMatch, 'getStarterQuestionBank_ must be found and match array syntax');

const rawBank = JSON.parse(bankMatch[1]);

test('P14: Bank Density Threshold (Total Bank >= 500 questions)', () => {
  assert.ok(rawBank.length >= 500, `Question bank must contain at least 500 curated questions (found: ${rawBank.length})`);
});

test('P14: Zero Placeholders Mandate across all items in bank', () => {
  const forbiddenPatterns = [
    /placeholder/i,
    /tbd/i,
    /lorem ipsum/i,
    /سيتم إضافة/,
    /قيد الإعداد/,
    /test question/i
  ];

  rawBank.forEach((row, idx) => {
    const [id, grade, subj, unit, text, qtype, optsStr, correct, pts, exp] = row;
    assert.ok(id && id.trim().length > 3, `Row ${idx} must have valid ID`);
    assert.ok(text && text.trim().length > 8, `Row ${idx} (${id}) must have substantive question text`);
    assert.ok(correct && correct.trim().length > 0, `Row ${idx} (${id}) must have correct answer`);
    assert.ok(exp && exp.trim().length >= 15, `Row ${idx} (${id}) must have detailed pedagogical explanation`);

    forbiddenPatterns.forEach(pattern => {
      assert.ok(!pattern.test(text), `Row ${id} text violates anti-placeholder rule: ${text}`);
      assert.ok(!pattern.test(exp), `Row ${id} explanation violates anti-placeholder rule: ${exp}`);
    });
  });
});

test('P14: Stratification Integrity (15 L1, 15 L2, 15 L3 per core lesson)', () => {
  // Test core lessons that have P14 stratified banks
  const examCodesToTest = [
    'DAILY_Y6_SOC_W1D1',
    'DAILY_Y5_SOC_W1D1',
    'DAILY_Y6_ICT_W1D1',
    'DAILY_Y5_ICT_W1D1',
    'DAILY_Y6_ARB_W1D1',
    'DAILY_Y5_ARB_W1D1'
  ];

  examCodesToTest.forEach(code => {
    const items = rawBank.filter(row => row[10] === code);
    assert.ok(items.length >= 45, `Exam ${code} must contain >= 45 questions (found: ${items.length})`);

    const l1 = items.filter(r => r[12] === 'Easy');
    const l2 = items.filter(r => r[12] === 'Medium');
    const l3 = items.filter(r => r[12] === 'Hard' || r[12] === 'Challenge');

    assert.ok(l1.length >= 15, `Exam ${code} must have >= 15 Level 1 (Easy) questions (found: ${l1.length})`);
    assert.ok(l2.length >= 15, `Exam ${code} must have >= 15 Level 2 (Medium) questions (found: ${l2.length})`);
    assert.ok(l3.length >= 15, `Exam ${code} must have >= 15 Level 3 (Hard) questions (found: ${l3.length})`);
  });
});

test('P14: MCQ Option Consistency & Correct Answer Presence', () => {
  rawBank.forEach(row => {
    const [id, , , , , qtype, optsStr, correct] = row;
    if (qtype === 'MCQ') {
      const opts = optsStr.split(/\s*\|\s*/);
      assert.ok(opts.length >= 2, `MCQ ${id} must have at least 2 options (found: ${opts.length})`);
      assert.ok(opts.includes(correct), `MCQ ${id} options must include the correct answer "${correct}"`);
    }
  });
});
