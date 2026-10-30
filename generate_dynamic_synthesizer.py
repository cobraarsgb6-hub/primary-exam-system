# -*- coding: utf-8 -*-
"""
Generates Dynamic Question Synthesizer logic for Code.gs and client runtime.
Phase P13: 014-full-refresh-question-bank
"""

dynamic_code = r'''
// =========================================================================
// PHASE P13: DYNAMIC QUESTION SYNTHESIZER & FULL REFRESH ENGINE
// =========================================================================

function generatePrimeFactorQuestion_(level, seed) {
  var pool = [24, 36, 40, 48, 54, 60, 72, 80, 84, 90, 96, 108, 120, 144, 150, 180];
  var n = pool[Math.floor(Math.random() * pool.length)];
  var temp = n;
  var factors = {};
  var primes = [2, 3, 5, 7, 11, 13];
  for (var i = 0; i < primes.length; i++) {
    var p = primes[i];
    while (temp % p === 0) {
      factors[p] = (factors[p] || 0) + 1;
      temp = Math.floor(temp / p);
    }
  }
  if (temp > 1) factors[temp] = 1;

  var parts = [];
  var sortedPrimes = Object.keys(factors).map(Number).sort(function(a, b) { return a - b; });
  sortedPrimes.forEach(function(p) {
    var exp = factors[p];
    parts.push(exp > 1 ? (p + '^' + exp) : String(p));
  });
  var correctAns = parts.join(' × ');

  // Generate 3 intelligent distractors
  var distractors = [];
  distractors.push(parts.slice().reverse().join(' × '));
  // Mutate an exponent
  var mutParts = sortedPrimes.map(function(p) {
    var exp = factors[p];
    return (exp > 1 ? (p + '^' + (exp + 1)) : (p + '^2'));
  });
  distractors.push(mutParts.join(' × '));
  // Add an off-by-one prime
  distractors.push(sortedPrimes.join(' × '));

  var options = [correctAns];
  distractors.forEach(function(d) {
    if (d !== correctAns && options.indexOf(d) === -1 && options.length < 4) {
      options.push(d);
    }
  });
  while (options.length < 4) {
    options.push(n + ' × 1');
  }

  var diffTag = (level === 1 ? 'Easy' : (level === 2 ? 'Medium' : 'Hard'));
  return {
    id: 'DYN_MATH_PRIME_' + n + '_' + Math.floor(Math.random() * 10000),
    grade: 'Grade 6 (G6)',
    subject: 'Mathematics',
    unit: 'Unit 1: Prime Factors & Index Notation',
    text: 'What is the prime factorization of <b>' + n + '</b> written in index notation?',
    type: 'MCQ',
    options: shuffleArray(options),
    correctAnswer: correctAns,
    points: 1,
    explanation: 'Decompose ' + n + ' by repeated division using prime numbers. The prime powers are: ' + correctAns + '.',
    examCode: 'PRACTICE_Y6_MATH',
    week: 'W1',
    difficulty: diffTag
  };
}

function generateFDPQuestion_(level, seed) {
  var fdpPool = [
    { frac: '1/4', dec: '0.25', pct: '25%' },
    { frac: '3/4', dec: '0.75', pct: '75%' },
    { frac: '1/5', dec: '0.2', pct: '20%' },
    { frac: '2/5', dec: '0.4', pct: '40%' },
    { frac: '3/5', dec: '0.6', pct: '60%' },
    { frac: '4/5', dec: '0.8', pct: '80%' },
    { frac: '1/8', dec: '0.125', pct: '12.5%' },
    { frac: '3/8', dec: '0.375', pct: '37.5%' },
    { frac: '5/8', dec: '0.625', pct: '62.5%' },
    { frac: '7/8', dec: '0.875', pct: '87.5%' },
    { frac: '7/10', dec: '0.7', pct: '70%' },
    { frac: '9/20', dec: '0.45', pct: '45%' },
    { frac: '13/20', dec: '0.65', pct: '65%' },
    { frac: '17/20', dec: '0.85', pct: '85%' }
  ];

  var item = fdpPool[Math.floor(Math.random() * fdpPool.length)];
  var isToPct = Math.random() > 0.5;

  var qText = isToPct
    ? 'Convert the fraction <b>' + item.frac + '</b> into an equivalent percentage:'
    : 'Convert the decimal <b>' + item.dec + '</b> into its simplest fraction form:';
  var correctAns = isToPct ? item.pct : item.frac;

  var options = [correctAns];
  fdpPool.forEach(function(other) {
    var candidate = isToPct ? other.pct : other.frac;
    if (candidate !== correctAns && options.indexOf(candidate) === -1 && options.length < 4) {
      options.push(candidate);
    }
  });

  var diffTag = (level === 1 ? 'Easy' : (level === 2 ? 'Medium' : 'Hard'));
  return {
    id: 'DYN_MATH_FDP_' + Math.floor(Math.random() * 10000),
    grade: 'Grade 6 (G6)',
    subject: 'Mathematics',
    unit: 'Unit 2: Fractions, Decimals & Percentages',
    text: qText,
    type: 'MCQ',
    options: shuffleArray(options),
    correctAnswer: correctAns,
    points: 1,
    explanation: 'Equivalent FDP identity: ' + item.frac + ' = ' + item.dec + ' = ' + item.pct + '.',
    examCode: 'PRACTICE_Y6_MATH',
    week: 'W1',
    difficulty: diffTag
  };
}

function generateDivisionQuestion_(level, seed) {
  var divisor = Math.floor(Math.random() * 8) + 4; // 4 to 11
  var quotient = Math.floor(Math.random() * 40) + 15; // 15 to 54
  var remainder = (level === 1) ? 0 : Math.floor(Math.random() * divisor);
  var dividend = (divisor * quotient) + remainder;

  var correctAns = (remainder === 0) ? String(quotient) : (quotient + ' r ' + remainder);
  var options = [
    correctAns,
    (quotient - 1) + (remainder > 0 ? (' r ' + remainder) : ''),
    quotient + (remainder > 0 ? (' r ' + (remainder + 1)) : ' r 1'),
    (quotient + 1) + (remainder > 0 ? (' r ' + remainder) : '')
  ];

  var diffTag = (level === 1 ? 'Easy' : (level === 2 ? 'Medium' : 'Hard'));
  return {
    id: 'DYN_MATH_DIV_' + dividend + '_' + Math.floor(Math.random() * 10000),
    grade: 'Grade 6 (G6)',
    subject: 'Mathematics',
    unit: 'Unit 3: Long Division (Bus Stop Method)',
    text: 'Calculate <b>' + dividend + ' ÷ ' + divisor + '</b> using the Bus Stop division method:',
    type: 'MCQ',
    options: shuffleArray(options),
    correctAnswer: correctAns,
    points: 1,
    explanation: 'Using the bus stop method: ' + dividend + ' ÷ ' + divisor + ' = ' + quotient + (remainder > 0 ? (' with a remainder of ' + remainder) : ' exactly') + '.',
    examCode: 'PRACTICE_Y6_MATH',
    week: 'W1',
    difficulty: diffTag
  };
}

function generateBODMASQuestion_(level, seed) {
  var a = Math.floor(Math.random() * 10) + 2;
  var b = Math.floor(Math.random() * 8) + 2;
  var c = Math.floor(Math.random() * 6) + 2;
  var d = Math.floor(Math.random() * 5) + 1;

  var text, correctAns, trapAns;
  if (level === 1) {
    // a + b * c
    text = 'Evaluate: <b>' + a + ' + ' + b + ' × ' + c + '</b>';
    correctAns = a + (b * c);
    trapAns = (a + b) * c; // Trap: adding before multiplying
  } else if (level === 2) {
    // (a + b) * c - d
    text = 'Evaluate: <b>(' + a + ' + ' + b + ') × ' + c + ' - ' + d + '</b>';
    correctAns = ((a + b) * c) - d;
    trapAns = a + (b * c) - d;
  } else {
    // a * b - (c + d)^2 or a * b + c * d
    text = 'Evaluate: <b>' + a + ' × ' + b + ' - (' + c + ' + ' + d + ')</b>';
    correctAns = (a * b) - (c + d);
    trapAns = (a * b) - c + d; // Trap: forgetting brackets distributing minus
  }

  var options = [
    String(correctAns),
    String(trapAns),
    String(correctAns + 2),
    String(Math.abs(correctAns - 3))
  ];

  var diffTag = (level === 1 ? 'Easy' : (level === 2 ? 'Medium' : 'Hard'));
  return {
    id: 'DYN_MATH_BODMAS_' + Math.floor(Math.random() * 10000),
    grade: 'Grade 6 (G6)',
    subject: 'Mathematics',
    unit: 'Unit 4: Order of Operations (BODMAS)',
    text: text,
    type: 'MCQ',
    options: shuffleArray(options),
    correctAnswer: String(correctAns),
    points: 1,
    explanation: 'Follow BODMAS rule: Brackets first, then Orders (powers), then Division & Multiplication, and finally Addition & Subtraction. Correct value = ' + correctAns + '.',
    examCode: 'PRACTICE_Y6_MATH',
    week: 'W1',
    difficulty: diffTag
  };
}

function generatePlaceValueQuestion_(level, seed) {
  var places = [
    { name: 'Hundred Thousands', mul: 100000 },
    { name: 'Ten Thousands', mul: 10000 },
    { name: 'Thousands', mul: 1000 },
    { name: 'Hundreds', mul: 100 },
    { name: 'Tens', mul: 10 },
    { name: 'Millions', mul: 1000000 }
  ];
  var pObj = places[Math.floor(Math.random() * places.length)];
  var digit = Math.floor(Math.random() * 8) + 2; // 2 to 9
  var numBase = 4000000 + (digit * pObj.mul) + Math.floor(Math.random() * 9999);
  var correctVal = digit * pObj.mul;

  var options = [
    correctVal.toLocaleString('en-US'),
    (digit * (pObj.mul * 10)).toLocaleString('en-US'),
    (digit * Math.max(1, Math.floor(pObj.mul / 10))).toLocaleString('en-US'),
    String(digit)
  ];

  var diffTag = (level === 1 ? 'Easy' : (level === 2 ? 'Medium' : 'Hard'));
  return {
    id: 'DYN_MATH_PV_' + Math.floor(Math.random() * 10000),
    grade: 'Grade 6 (G6)',
    subject: 'Mathematics',
    unit: 'Unit 5: Place Value to 10,000,000',
    text: 'In the number <b>' + numBase.toLocaleString('en-US') + '</b>, what is the value of the digit <u>' + digit + '</u> in the ' + pObj.name + ' column?',
    type: 'MCQ',
    options: shuffleArray(options),
    correctAnswer: correctVal.toLocaleString('en-US'),
    points: 1,
    explanation: 'The digit ' + digit + ' sits in the ' + pObj.name + ' position, so its value is ' + digit + ' × ' + pObj.mul.toLocaleString('en-US') + ' = ' + correctVal.toLocaleString('en-US') + '.',
    examCode: 'PRACTICE_Y6_MATH',
    week: 'W1',
    difficulty: diffTag
  };
}

function generateDivisibilityQuestion_(level, seed) {
  var divisors = [2, 3, 4, 5, 6, 9, 10, 25, 100];
  var k = divisors[Math.floor(Math.random() * divisors.length)];
  var isDivisible = Math.random() > 0.5;
  var base = Math.floor(Math.random() * 200) + 15;
  var n = isDivisible ? (base * k) : ((base * k) + (Math.floor(Math.random() * (k - 1)) + 1));

  var actuallyDivisible = (n % k === 0);
  var correctAns = actuallyDivisible ? 'Yes (يقبل القسمة)' : 'No (لا يقبل القسمة)';
  var options = ['Yes (يقبل القسمة)', 'No (لا يقبل القسمة)'];

  var ruleNote = '';
  if (k === 2) ruleNote = 'ends in an even digit (0, 2, 4, 6, 8).';
  else if (k === 3) ruleNote = 'the sum of its digits is divisible by 3.';
  else if (k === 4) ruleNote = 'the last two digits form a multiple of 4.';
  else if (k === 5) ruleNote = 'the last digit is 0 or 5.';
  else if (k === 9) ruleNote = 'the sum of its digits is a multiple of 9.';
  else if (k === 10) ruleNote = 'the last digit is 0.';
  else if (k === 25) ruleNote = 'the last two digits are 00, 25, 50, or 75.';
  else ruleNote = 'it meets the divisibility condition for ' + k + '.';

  var diffTag = (level === 1 ? 'Easy' : (level === 2 ? 'Medium' : 'Hard'));
  return {
    id: 'DYN_MATH_DIVTEST_' + n + '_' + Math.floor(Math.random() * 10000),
    grade: 'Year 5 (G5)',
    subject: 'Mathematics',
    unit: 'Unit 1: Tests of Divisibility',
    text: 'Is the number <b>' + n.toLocaleString('en-US') + '</b> divisible by <b>' + k + '</b> without remainder?',
    type: 'MCQ',
    options: options,
    correctAnswer: correctAns,
    points: 1,
    explanation: 'A number is divisible by ' + k + ' when ' + ruleNote + ' For ' + n + ', ' + n + ' ÷ ' + k + ' = ' + (n / k).toFixed(2) + ' -> ' + correctAns + '.',
    examCode: 'PRACTICE_Y5_MATH',
    week: 'W1',
    difficulty: diffTag
  };
}

function generateRoundingQuestion_(level, seed) {
  var scales = [
    { name: '10', P: 10 },
    { name: '100', P: 100 },
    { name: '1,000', P: 1000 },
    { name: '10,000', P: 10000 }
  ];
  var scale = scales[Math.floor(Math.random() * scales.length)];
  var n = Math.floor(Math.random() * 85000) + 1200;
  var rounded = Math.round(n / scale.P) * scale.P;

  var lower = Math.floor(n / scale.P) * scale.P;
  var upper = lower + scale.P;
  var options = [
    rounded.toLocaleString('en-US'),
    (lower === rounded ? upper : lower).toLocaleString('en-US'),
    (rounded + (scale.P * 2)).toLocaleString('en-US'),
    (rounded - scale.P).toLocaleString('en-US')
  ];

  var diffTag = (level === 1 ? 'Easy' : (level === 2 ? 'Medium' : 'Hard'));
  return {
    id: 'DYN_MATH_ROUND_' + n + '_' + Math.floor(Math.random() * 10000),
    grade: 'Year 5 (G5)',
    subject: 'Mathematics',
    unit: 'Unit 2: Rounding & Place Value',
    text: 'Round the number <b>' + n.toLocaleString('en-US') + '</b> to the nearest <b>' + scale.name + '</b>:',
    type: 'MCQ',
    options: shuffleArray(options),
    correctAnswer: rounded.toLocaleString('en-US'),
    points: 1,
    explanation: 'Look at the digit to the right of the rounding place. If it is 5 or greater, round up; otherwise round down. ' + n.toLocaleString('en-US') + ' rounded to the nearest ' + scale.name + ' = ' + rounded.toLocaleString('en-US') + '.',
    examCode: 'PRACTICE_Y5_MATH',
    week: 'W1',
    difficulty: diffTag
  };
}

function generateCircuitsDynamicQuestion_(level, seed) {
  var cells = Math.floor(Math.random() * 3) + 1; // 1 to 3
  var lamps = Math.floor(Math.random() * 3) + 1; // 1 to 3
  var voltage = (cells * 1.5).toFixed(1);

  var correctAns = 'Voltage is ' + voltage + 'V; ' + (cells > lamps ? 'lamps shine very brightly.' : (cells === lamps ? 'lamps shine with normal brightness.' : 'lamps are dim.'));
  var options = [
    correctAns,
    'Voltage is ' + (voltage * 2) + 'V; lamps burn out immediately.',
    'Voltage is 0V; the circuit is broken.',
    'Voltage is ' + voltage + 'V; adding more lamps in series increases brightness.'
  ];

  var diffTag = (level === 1 ? 'Easy' : (level === 2 ? 'Medium' : 'Hard'));
  return {
    id: 'DYN_SCI_CIRCUIT_' + Math.floor(Math.random() * 10000),
    grade: 'Grade 6 (G6)',
    subject: 'Science',
    unit: 'Unit 3: Electric Circuits & Conductivity',
    text: 'A series circuit contains <b>' + cells + ' cell(s)</b> (1.5V each) and <b>' + lamps + ' identical lamp(s)</b>. What is the total voltage and effect on brightness?',
    type: 'MCQ',
    options: shuffleArray(options),
    correctAnswer: correctAns,
    points: 1,
    explanation: 'Each cell in series adds 1.5V, giving a total of ' + voltage + 'V. More cells increase current and brightness, while adding lamps in series increases resistance and dims the bulbs.',
    examCode: 'PRACTICE_Y6_SCI',
    week: 'W1',
    difficulty: diffTag
  };
}

function synthesizeDynamicQuestions_(grade, subject, count, difficulty, salt) {
  var isG6 = (String(grade || '').indexOf('6') !== -1);
  var fam = subjectFamily_(subject);
  var targetCount = Math.max(3, Math.min(30, Number(count) || 10));
  var questions = [];

  var generators = [];
  if (fam === 'math') {
    if (isG6) {
      generators = [
        generatePrimeFactorQuestion_,
        generateFDPQuestion_,
        generateDivisionQuestion_,
        generateBODMASQuestion_,
        generatePlaceValueQuestion_
      ];
    } else {
      generators = [
        generateDivisibilityQuestion_,
        generateRoundingQuestion_,
        generateDivisionQuestion_
      ];
    }
  } else if (fam === 'science') {
    generators = [
      generateCircuitsDynamicQuestion_
    ];
  }

  if (!generators.length) {
    return [];
  }

  // Generate requested count evenly balanced across L1, L2, L3
  for (var i = 0; i < targetCount; i++) {
    var gen = generators[i % generators.length];
    var level = (i % 3) + 1; // 1, 2, 3
    var q = gen(level, (salt || Date.now()) + i);
    questions.push(q);
  }

  return shuffleArray(questions);
}
'''

with open("dynamic_question_engine.py", "w", encoding="utf-8") as f:
    f.write(dynamic_code)

print("Saved dynamic_question_engine.py template successfully")
