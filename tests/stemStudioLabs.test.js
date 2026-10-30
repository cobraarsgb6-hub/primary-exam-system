const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

test('STEM Studio & Labs (Phase P11 - 012-studio-labs-stem): 18 Units, 180 Flashcards & Simulations', async (t) => {
  const htmlPath = path.join(__dirname, '..', 'Index.bundle.html');
  const htmlContent = fs.readFileSync(htmlPath, 'utf8');

  const dom = new JSDOM(htmlContent, { runScripts: 'dangerously' });
  const window = dom.window;
  const document = window.document;

  await t.test('1. Data Integrity: Exactly 18 units registered across Science & Math for Mostafa & Ali', () => {
    assert.ok(Array.isArray(window.STEM_STUDIO_DATA), 'window.STEM_STUDIO_DATA must be an array');
    assert.equal(window.STEM_STUDIO_DATA.length, 18, 'Must contain exactly 18 STEM units');

    const expectedUnits = [
      // Mostafa Science 106 (6 units)
      { id: 'sci106_circulatory', subject: 'Science 106', student: 'Mostafa' },
      { id: 'sci106_forces', subject: 'Science 106', student: 'Mostafa' },
      { id: 'sci106_circuits', subject: 'Science 106', student: 'Mostafa' },
      { id: 'sci106_mixtures', subject: 'Science 106', student: 'Mostafa' },
      { id: 'sci106_changes', subject: 'Science 106', student: 'Mostafa' },
      { id: 'sci106_measurements', subject: 'Science 106', student: 'Mostafa' },

      // Mostafa Math 106 (6 units)
      { id: 'math106_place_value', subject: 'Math 106', student: 'Mostafa' },
      { id: 'math106_prime_factors', subject: 'Math 106', student: 'Mostafa' },
      { id: 'math106_multiplication', subject: 'Math 106', student: 'Mostafa' },
      { id: 'math106_division', subject: 'Math 106', student: 'Mostafa' },
      { id: 'math106_fdp', subject: 'Math 106', student: 'Mostafa' },
      { id: 'math106_bodmas', subject: 'Math 106', student: 'Mostafa' },

      // Ali Science 105 (4 units)
      { id: 'sci105_plant_anatomy', subject: 'Science 105', student: 'Ali' },
      { id: 'sci105_pollination', subject: 'Science 105', student: 'Ali' },
      { id: 'sci105_sound_vibrations', subject: 'Science 105', student: 'Ali' },
      { id: 'sci105_pitch_loudness', subject: 'Science 105', student: 'Ali' },

      // Ali Math 105 (2 units)
      { id: 'math105_divisibility', subject: 'Math 105', student: 'Ali' },
      { id: 'math105_rounding_pv', subject: 'Math 105', student: 'Ali' }
    ];

    expectedUnits.forEach(expected => {
      const u = window.STEM_STUDIO_MAP[expected.id];
      assert.ok(u, `Unit ${expected.id} must exist in window.STEM_STUDIO_MAP`);
      assert.equal(u.subjectCode, expected.subject, `${expected.id} must belong to ${expected.subject}`);
      assert.equal(u.student, expected.student, `${expected.id} must belong to ${expected.student}`);
    });
  });

  await t.test('2. Anti-Placeholder & Pedagogical Completeness: Theory, Rules, Examples, Traps & 10 Flashcards per unit', () => {
    let totalFlashcards = 0;

    window.STEM_STUDIO_DATA.forEach(u => {
      // 1. Titles & Metadata
      assert.ok(u.title && u.title.length >= 5, `${u.id} must have a valid Arabic title`);
      assert.ok(u.titleEn && u.titleEn.length >= 5, `${u.id} must have a valid English title`);
      assert.ok(u.icon && u.icon.length >= 1, `${u.id} must have an icon`);

      // 2. Theory components (Nagwa/Cambridge format)
      assert.ok(u.theory, `${u.id} must have theory object`);
      assert.ok(u.theory.overview && u.theory.overview.length >= 100, `${u.id} overview must be substantial (>=100 chars)`);
      assert.ok(!u.theory.overview.includes('سيتم إضافة'), `${u.id} overview must not contain placeholder`);
      assert.ok(!u.theory.overview.includes('قيد الإعداد'), `${u.id} overview must not contain placeholder`);

      assert.ok(Array.isArray(u.theory.goldenRules) && u.theory.goldenRules.length >= 4, `${u.id} must have >= 4 golden rules`);
      assert.ok(Array.isArray(u.theory.workedExamples) && u.theory.workedExamples.length >= 1, `${u.id} must have worked examples`);
      assert.ok(Array.isArray(u.theory.examTraps) && u.theory.examTraps.length >= 1, `${u.id} must have exam traps`);

      // 3. Flashcards (Strictly >= 10 unique interactive cards per unit)
      assert.ok(Array.isArray(u.flashcards), `${u.id} must have flashcards array`);
      assert.ok(u.flashcards.length >= 10, `${u.id} must have at least 10 flashcards (found ${u.flashcards.length})`);
      totalFlashcards += u.flashcards.length;

      u.flashcards.forEach((c, idx) => {
        assert.ok(c.front && c.front.length >= 8, `${u.id} card ${idx + 1} front must be a real question`);
        assert.ok(c.back && c.back.length >= 8, `${u.id} card ${idx + 1} back must be a real answer`);
        assert.ok(c.tip && c.tip.length >= 4, `${u.id} card ${idx + 1} must have a helpful pedagogical tip`);
      });
    });

    assert.equal(totalFlashcards, 180, 'Total flashcards across all 18 units must equal exactly 180');
  });

  await t.test('3. UI Integration: #unit-studio-modal, 4 tabs, and subject workspace integration', () => {
    // 1. Check modal existence
    const modal = document.getElementById('unit-studio-modal');
    assert.ok(modal, '#unit-studio-modal must exist in document');

    // 2. Check 4 Tab buttons
    assert.ok(document.getElementById('studio-tab-btn-theory'), 'Tab button theory must exist');
    assert.ok(document.getElementById('studio-tab-btn-flashcards'), 'Tab button flashcards must exist');
    assert.ok(document.getElementById('studio-tab-btn-lab'), 'Tab button lab must exist');
    assert.ok(document.getElementById('studio-tab-btn-video'), 'Tab button video must exist');

    // 3. Check 4 Tab Panes
    assert.ok(document.getElementById('studio-tab-pane-theory'), 'Tab pane theory must exist');
    assert.ok(document.getElementById('studio-tab-pane-flashcards'), 'Tab pane flashcards must exist');
    assert.ok(document.getElementById('studio-tab-pane-lab'), 'Tab pane lab must exist');
    assert.ok(document.getElementById('studio-tab-pane-video'), 'Tab pane video must exist');

    // 4. Check workspace container
    assert.ok(document.getElementById('sw-studio-units-list'), '#sw-studio-units-list container must exist in workspace');
  });

  await t.test('4. Subject Workspace Units Rendering: Correct unit counts per subject', () => {
    const container = document.getElementById('sw-studio-units-list');

    // Mostafa Science 106 -> 6 units
    window.renderSubjectStudioUnits('Science 106', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 6, 'Science 106 must display 6 units');

    // Mostafa Math 106 -> 6 units
    window.renderSubjectStudioUnits('Math 106', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 6, 'Math 106 must display 6 units');

    // Ali Science 105 -> 4 units
    window.renderSubjectStudioUnits('Science 105', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 4, 'Science 105 must display 4 units');

    // Ali Math 105 -> 2 units
    window.renderSubjectStudioUnits('Math 105', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 2, 'Math 105 must display 2 units');
  });

  await t.test('5. Modal Lifecycle & Flashcard Interaction: Flip, Next, Prev, and Tabs', () => {
    const modal = document.getElementById('unit-studio-modal');

    // Open Circulatory System Unit
    window.openStudioUnit('sci106_circulatory');
    assert.ok(modal.classList.contains('active'), 'Modal must become active');
    assert.equal(document.getElementById('studio-modal-title').textContent, 'الجهاز الدوري والدورة الدموية المزدوجة');

    // Switch to Flashcards Tab
    window.switchStudioTab('flashcards');
    assert.equal(document.getElementById('studio-tab-pane-flashcards').style.display, 'block');

    const cardBox = document.getElementById('studio-flashcard-box');
    assert.ok(!cardBox.classList.contains('flipped'), 'Card must initially not be flipped');

    // Flip Card
    window.flipFlashcard();
    assert.ok(cardBox.classList.contains('flipped'), 'Card must be flipped after flipFlashcard()');

    // Flip back
    window.flipFlashcard();
    assert.ok(!cardBox.classList.contains('flipped'), 'Card must return to front');

    // Advance to next card
    window.nextFlashcard();
    assert.equal(document.getElementById('studio-flashcard-counter').textContent, 'بطاقة 2 من 10');

    // Previous card
    window.prevFlashcard();
    assert.equal(document.getElementById('studio-flashcard-counter').textContent, 'بطاقة 1 من 10');

    // Close modal
    window.closeStudioModal();
    assert.ok(!modal.classList.contains('active'), 'Modal must close on closeStudioModal()');
  });

  await t.test('6. Interactive Simulation Engines: All 18 Labs mount and execute without errors', () => {
    const labContainer = document.getElementById('studio-lab-container');

    // Iterate through all 18 units and verify each simulation mounts and renders real controls
    window.STEM_STUDIO_DATA.forEach(u => {
      window.openStudioUnit(u.id);
      window.switchStudioTab('lab');

      assert.ok(labContainer.innerHTML.length > 50, `Lab for ${u.id} must render non-empty content`);
      assert.ok(!labContainer.innerHTML.includes('قيد الإعداد'), `Lab for ${u.id} must be fully implemented`);
    });

    // Test specific interactive functions across STEM labs
    // Lab 1: Circulatory BPM
    window.openStudioUnit('sci106_circulatory');
    window.switchStudioTab('lab');
    window.updateHeartBPM(140);
    assert.equal(document.getElementById('bpm-val').textContent, '140 BPM');

    // Lab 2: Parachute physics
    window.openStudioUnit('sci106_forces');
    window.switchStudioTab('lab');
    window.updateParachutePhysics();
    assert.ok(document.getElementById('para-terminal-calc').textContent.includes('km/h'));

    // Lab 3: Circuits switch
    window.openStudioUnit('sci106_circuits');
    window.switchStudioTab('lab');
    window.toggleCircuitSwitch();
    assert.ok(document.getElementById('btn-circuit-switch').textContent.includes('OFF'));

    // Lab 4: Mixtures step
    window.openStudioUnit('sci106_mixtures');
    window.switchStudioTab('lab');
    window.execMixtureStep(1);
    assert.ok(document.getElementById('status-iron').textContent.includes('تم الفصل'));

    // Lab 7: Place value
    window.openStudioUnit('math106_place_value');
    window.switchStudioTab('lab');
    window.shiftPlaceValue(10);
    assert.ok(document.getElementById('pv-expanded-readout').textContent.includes('الصيغة الممتدة'));

    // Lab 8: Prime Tree
    window.openStudioUnit('math106_prime_factors');
    window.switchStudioTab('lab');
    window.generatePrimeTree();
    assert.ok(document.getElementById('prime-tree-result').textContent.includes('الصيغة الأسية'));

    // Lab 11: FDP
    window.openStudioUnit('math106_fdp');
    window.switchStudioTab('lab');
    window.setFDP(75);
    assert.equal(document.getElementById('fdp-pct-val').textContent, '75%');
    assert.equal(document.getElementById('fdp-frac-val').textContent, '3/4');

    // Lab 12: BODMAS
    window.openStudioUnit('math106_bodmas');
    window.switchStudioTab('lab');
    window.updateBODMASLine();
    assert.equal(document.getElementById('line-result-val').textContent, '8');

    // Lab 17: Divisibility
    window.openStudioUnit('math105_divisibility');
    window.switchStudioTab('lab');
    window.setDivisibilityVal(7425);
    const matrix = document.getElementById('divisibility-matrix-grid');
    assert.equal(matrix.children.length, 10, 'Divisibility matrix must inspect all 10 divisors');

    // Lab 18: Rounding Hill
    window.openStudioUnit('math105_rounding_pv');
    window.switchStudioTab('lab');
    window.updateRoundingSim();
    assert.ok(document.getElementById('rounding-explanation-readout').textContent.includes('التقريب'));

    window.closeStudioModal();
  });
  dom.window.close();
});
