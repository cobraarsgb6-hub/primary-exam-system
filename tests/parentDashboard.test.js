// Contract and Unit tests for Phase 8: Parent Command Dashboard & Multi-Subject Analytics
// Run with: node --test tests/parentDashboard.test.js
const test = require('node:test');
const assert = require('node:assert/strict');

function computeScoreTrend(subs) {
  if (!subs || subs.length < 2) {
    return { trend: 'stable', label: '⚖️ مستقر / Stable', diff: 0 };
  }
  const chronSubs = subs.slice().reverse();
  const firstScore = Number(String(chronSubs[0].percentage || '').replace('%', '')) || 0;
  const lastScore = Number(String(chronSubs[chronSubs.length - 1].percentage || '').replace('%', '')) || 0;
  const diff = lastScore - firstScore;

  if (diff >= 5) {
    return { trend: 'improving', label: `📈 تصاعدي (+${diff}%) / Improving`, diff: diff };
  } else if (diff <= -5) {
    return { trend: 'declining', label: `📉 تراجع (${diff}%) / Needs Attention`, diff: diff };
  }
  return { trend: 'stable', label: '⚖️ مستقر / Stable', diff: diff };
}

function getPedagogicalPolicy(avgPercentage) {
  if (avgPercentage >= 85) {
    return { tier: 'challenge', name: 'خطة الإثراء والتحدي', minScore: 85 };
  } else if (avgPercentage >= 70) {
    return { tier: 'practice', name: 'خطة التثبيت والممارسة', minScore: 70 };
  } else if (avgPercentage >= 50) {
    return { tier: 'reteach', name: 'خطة إعادة شرح المفهوم', minScore: 50 };
  }
  return { tier: 'intervention', name: 'خطة التدخل المشترك مع ولي الأمر', minScore: 0 };
}

function identifyRecurrentWeaknesses(reviewItems) {
  const stats = {};
  (reviewItems || []).forEach(item => {
    const key = item.unit || item.skill || item.questionText || item.id || 'Unknown';
    if (!stats[key]) {
      stats[key] = { key: key, wrongCount: 0, totalCount: 0 };
    }
    stats[key].totalCount++;
    if (item.isCorrect === false) {
      stats[key].wrongCount++;
    }
  });

  return Object.values(stats).filter(s => s.wrongCount >= 2 || (s.totalCount >= 2 && (s.wrongCount / s.totalCount) >= 0.3));
}

function generateSubmissionsCsv(subs) {
  let csvContent = '\uFEFF'; // UTF-8 BOM
  csvContent += 'Timestamp,Student,Grade,Exam Code,Earned,Total,Percentage,Rating,Duration\n';

  subs.forEach(s => {
    const clean = (val) => '"' + String(val == null ? '' : val).replace(/"/g, '""') + '"';
    csvContent += [
      clean(s.timestamp),
      clean(s.studentName),
      clean(s.schoolGroup),
      clean(s.examCode),
      clean(s.earnedScore),
      clean(s.totalScore),
      clean(s.percentage),
      clean(s.rating),
      clean(s.durationSpent)
    ].join(',') + '\n';
  });

  return csvContent;
}

test('P8 Test 1: computeScoreTrend accurately classifies improving, declining, and stable trajectories', () => {
  // Improving: oldest is 60%, newest is 90% (reverse of recent-first order)
  const improvingSubs = [{ percentage: '90%' }, { percentage: '75%' }, { percentage: '60%' }];
  const resImp = computeScoreTrend(improvingSubs);
  assert.equal(resImp.trend, 'improving');
  assert.equal(resImp.diff, 30);
  assert.match(resImp.label, /تصاعدي/);

  // Declining: oldest is 90%, newest is 60%
  const decliningSubs = [{ percentage: '60%' }, { percentage: '75%' }, { percentage: '90%' }];
  const resDec = computeScoreTrend(decliningSubs);
  assert.equal(resDec.trend, 'declining');
  assert.equal(resDec.diff, -30);
  assert.match(resDec.label, /تراجع/);

  // Stable: difference < 5%
  const stableSubs = [{ percentage: '80%' }, { percentage: '82%' }];
  const resStb = computeScoreTrend(stableSubs);
  assert.equal(resStb.trend, 'stable');
  assert.equal(resStb.diff, -2);
});

test('P8 Test 2: getPedagogicalPolicy maps score brackets to 4-tier pedagogical policies', () => {
  assert.equal(getPedagogicalPolicy(95).tier, 'challenge');
  assert.equal(getPedagogicalPolicy(85).tier, 'challenge');
  assert.equal(getPedagogicalPolicy(84).tier, 'practice');
  assert.equal(getPedagogicalPolicy(70).tier, 'practice');
  assert.equal(getPedagogicalPolicy(69).tier, 'reteach');
  assert.equal(getPedagogicalPolicy(50).tier, 'reteach');
  assert.equal(getPedagogicalPolicy(49).tier, 'intervention');
  assert.equal(getPedagogicalPolicy(20).tier, 'intervention');
});

test('P8 Test 3: identifyRecurrentWeaknesses flags skills with repeated errors (>= 2 mistakes)', () => {
  const reviews = [
    { unit: 'Adverbials', isCorrect: false },
    { unit: 'Adverbials', isCorrect: false }, // 2 errors -> flag!
    { unit: 'Divisibility by 3', isCorrect: true },
    { unit: 'Divisibility by 3', isCorrect: true }, // 0 errors -> clear
    { unit: 'Fractions', isCorrect: false },
    { unit: 'Fractions', isCorrect: true } // 1 error out of 2 (50%) -> flag
  ];

  const weak = identifyRecurrentWeaknesses(reviews);
  assert.equal(weak.length, 2);
  const keys = weak.map(w => w.key);
  assert.ok(keys.includes('Adverbials'));
  assert.ok(keys.includes('Fractions'));
  assert.ok(!keys.includes('Divisibility by 3'));
});

test('P8 Test 4: generateSubmissionsCsv encodes RFC 4180 CSV with UTF-8 BOM for Arabic support', () => {
  const subs = [
    {
      timestamp: '2026-10-30 10:00',
      studentName: 'Ali Ahmed',
      schoolGroup: 'Year 5 (G5)',
      examCode: 'DAILY_Y5_MATH_W1D1',
      earnedScore: 5,
      totalScore: 5,
      percentage: '100%',
      rating: 'Mastery (100%)',
      durationSpent: '5 Mins'
    },
    {
      timestamp: '2026-10-30 11:00',
      studentName: 'مصطفى أحمد',
      schoolGroup: 'Grade 6 (G6)',
      examCode: 'DAILY_Y6_SCI_W1D1',
      earnedScore: 4,
      totalScore: 5,
      percentage: '80%',
      rating: 'Very Good 👏',
      durationSpent: '6 Mins'
    }
  ];

  const csv = generateSubmissionsCsv(subs);
  assert.ok(csv.startsWith('\uFEFF'), 'CSV must start with UTF-8 BOM');
  assert.ok(csv.includes('Timestamp,Student,Grade,Exam Code'));
  assert.ok(csv.includes('"Ali Ahmed"'));
  assert.ok(csv.includes('"مصطفى أحمد"'));
  assert.ok(csv.includes('"DAILY_Y5_MATH_W1D1"'));
});
