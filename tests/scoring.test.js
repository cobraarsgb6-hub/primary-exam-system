const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const code = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');
const context = {};
vm.createContext(context);
vm.runInContext(code, context);
const { formatPercentValue, normalizeAnswer_ } = context;

function calculateRating(percentage) {
  if (percentage >= 85) return 'Excellent 🌟';
  if (percentage >= 75) return 'Very Good 👏';
  if (percentage >= 65) return 'Good 👍';
  if (percentage >= 50) return 'Satisfactory 📚';
  return 'Needs Practice 🌱';
}

function calculateScore(questions, answers) {
  let earnedScore = 0;
  let totalScore = 0;
  const reviewDetails = [];

  questions.forEach(question => {
    const points = Number(question.points) || 1;
    totalScore += points;

    const hasAnswer = Object.prototype.hasOwnProperty.call(answers, question.id);
    const studentAnswer = hasAnswer ? String(answers[question.id] == null ? '' : answers[question.id]).trim() : '';
    const isCorrect = studentAnswer !== '' &&
      normalizeAnswer_(studentAnswer) === normalizeAnswer_(question.correctAnswer);

    if (isCorrect) earnedScore += points;

    reviewDetails.push({
      questionId: question.id,
      isCorrect: isCorrect,
      pointsAwarded: isCorrect ? points : 0,
      maxPoints: points
    });
  });

  const percentage = totalScore > 0 ? Math.round((earnedScore / totalScore) * 100) : 0;
  const rating = calculateRating(percentage);

  return {
    earnedScore,
    totalScore,
    percentage,
    rating,
    review: reviewDetails
  };
}

test('calculateRating: strictly tests all rating thresholds', () => {
  // 85%+ -> Excellent 🌟
  assert.equal(calculateRating(100), 'Excellent 🌟');
  assert.equal(calculateRating(85), 'Excellent 🌟');

  // 75% - 84% -> Very Good 👏
  assert.equal(calculateRating(84), 'Very Good 👏');
  assert.equal(calculateRating(75), 'Very Good 👏');

  // 65% - 74% -> Good 👍
  assert.equal(calculateRating(74), 'Good 👍');
  assert.equal(calculateRating(65), 'Good 👍');

  // 50% - 64% -> Satisfactory 📚
  assert.equal(calculateRating(64), 'Satisfactory 📚');
  assert.equal(calculateRating(50), 'Satisfactory 📚');

  // < 50% -> Needs Practice 🌱
  assert.equal(calculateRating(49), 'Needs Practice 🌱');
  assert.equal(calculateRating(0), 'Needs Practice 🌱');
});

test('calculateScore: handles totalScore = 0 gracefully', () => {
  const result = calculateScore([], {});
  assert.equal(result.totalScore, 0);
  assert.equal(result.earnedScore, 0);
  assert.equal(result.percentage, 0);
  assert.equal(result.rating, 'Needs Practice 🌱');
});

test('calculateScore: handles numeric answers vs text answers', () => {
  const questions = [
    { id: 'Q1', points: 1, correctAnswer: '10' },
    { id: 'Q2', points: 2, correctAnswer: 'Time' },
    { id: 'Q3', points: 1, correctAnswer: '0' }
  ];

  // Number 10 passed as number, 'time' with different casing, 0 as number
  const answers = {
    Q1: 10,
    Q2: 'time',
    Q3: 0
  };

  const result = calculateScore(questions, answers);
  assert.equal(result.totalScore, 4);
  assert.equal(result.earnedScore, 4);
  assert.equal(result.percentage, 100);
  assert.equal(result.rating, 'Excellent 🌟');
});

test('calculateScore: empty or missing answers earn zero points', () => {
  const questions = [
    { id: 'Q1', points: 2, correctAnswer: 'Yes' },
    { id: 'Q2', points: 3, correctAnswer: 'No' }
  ];

  const answers = {
    Q1: '   ',
    Q2: null
  };

  const result = calculateScore(questions, answers);
  assert.equal(result.totalScore, 5);
  assert.equal(result.earnedScore, 0);
  assert.equal(result.percentage, 0);
  assert.equal(result.rating, 'Needs Practice 🌱');
});

test('formatPercentValue: normalizes numbers and strings consistently', () => {
  // Numeric values
  assert.equal(formatPercentValue(1), '100%');
  assert.equal(formatPercentValue(0.85), '85%');
  assert.equal(formatPercentValue(85), '85%');
  assert.equal(formatPercentValue(0), '0%');

  // String values
  assert.equal(formatPercentValue('90%'), '90%');
  assert.equal(formatPercentValue('75'), '75%');
  assert.equal(formatPercentValue(''), '0%');
  assert.equal(formatPercentValue(null), '0%');
});
