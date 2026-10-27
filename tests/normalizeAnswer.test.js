const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Extract normalizeAnswer_ from Code.gs
const code = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');
const context = {};
vm.createContext(context);
vm.runInContext(code, context);
const { normalizeAnswer_, normalizeName_, normalizeExam_ } = context;

test('normalizeAnswer_: handles empty, null, undefined and numbers', () => {
  assert.equal(normalizeAnswer_(''), '');
  assert.equal(normalizeAnswer_(null), '');
  assert.equal(normalizeAnswer_(undefined), '');
  assert.equal(normalizeAnswer_(123), '123');
  assert.equal(normalizeAnswer_(0), '0');
});

test('normalizeAnswer_: strips Arabic diacritics / harakat', () => {
  // Fatha, Damma, Kasra, Sukun, Tanween
  const withHarakat = 'مَفْعُولٌ بِهِ';
  const withoutHarakat = 'مفعول به';
  assert.equal(normalizeAnswer_(withHarakat), normalizeAnswer_(withoutHarakat));
});

test('normalizeAnswer_: strips Arabic tatweel / kashida', () => {
  const withTatweel = 'المــــــبتدأ';
  const withoutTatweel = 'المبتدأ';
  assert.equal(normalizeAnswer_(withTatweel), normalizeAnswer_(withoutTatweel));
});

test('normalizeAnswer_: collapses multiple spaces and trims edges', () => {
  const messy = '   Adverbial    of     Time   ';
  assert.equal(normalizeAnswer_(messy), 'adverbial of time');
});

test('normalizeAnswer_: lowercases Latin characters', () => {
  assert.equal(normalizeAnswer_('Present PERFECT Continuous'), 'present perfect continuous');
});

test('normalizeAnswer_: combined real-world Arabic test case', () => {
  const student = '   ظَـرْفُ   زَمَـــانٍ   ';
  const expected = 'ظرف زمان';
  assert.equal(normalizeAnswer_(student), normalizeAnswer_(expected));
});

test('normalizeAnswer_: folds alef forms and alef maqsura', () => {
  assert.equal(normalizeAnswer_('أحمد'), normalizeAnswer_('احمد'));
  assert.equal(normalizeAnswer_('إجابة'), normalizeAnswer_('اجابة'));
  assert.equal(normalizeAnswer_('آمن'), normalizeAnswer_('امن'));
  assert.equal(normalizeAnswer_('مصطفى'), normalizeAnswer_('مصطفي'));
});

test('normalizeAnswer_: converts Arabic-Indic digits', () => {
  assert.equal(normalizeAnswer_('١٢٣'), '123');
  assert.equal(normalizeAnswer_('۴۵۶'), '456');
});

test('normalizeName_: normalizes student names cleanly and collapses spaces', () => {
  assert.equal(normalizeName_('  Mostafa   Ahmed  '), 'mostafa ahmed');
  assert.equal(normalizeName_('علي   أحمد'), 'علي أحمد');
  assert.equal(normalizeName_(''), '');
});

test('normalizeExam_: uppercases and trims exam codes', () => {
  assert.equal(normalizeExam_('  ex_y5_eng_adv01  '), 'EX_Y5_ENG_ADV01');
  assert.equal(normalizeExam_(''), '');
});
