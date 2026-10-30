const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

test('Humanities Studio & Labs (Phase P12 - 013-studio-labs-humanities): 19 Units, 190 Flashcards & Simulations', async (t) => {
  const htmlPath = path.join(__dirname, '..', 'Index.bundle.html');
  const htmlContent = fs.readFileSync(htmlPath, 'utf8');

  const dom = new JSDOM(htmlContent, { runScripts: 'dangerously' });
  const window = dom.window;
  const document = window.document;

  await t.test('1. Data Integrity: Exactly 19 units registered across English, Arabic, ICT, and Social Studies', () => {
    assert.ok(Array.isArray(window.HUMANITIES_STUDIO_DATA), 'window.HUMANITIES_STUDIO_DATA must be an array');
    assert.equal(window.HUMANITIES_STUDIO_DATA.length, 19, 'Must contain exactly 19 Humanities units');

    const expectedUnits = [
      // Mostafa English 106 (3)
      { id: 'eng106_relative_clauses', subject: 'English 106', student: 'Mostafa' },
      { id: 'eng106_connectives', subject: 'English 106', student: 'Mostafa' },
      { id: 'eng106_fiction_nonfiction', subject: 'English 106', student: 'Mostafa' },

      // Ali English 105 (3)
      { id: 'eng105_adverbials', subject: 'English 105', student: 'Ali' },
      { id: 'eng105_direct_speech', subject: 'English 105', student: 'Ali' },
      { id: 'eng105_fables_proverbs', subject: 'English 105', student: 'Ali' },

      // Mostafa Arabic 106 (3)
      { id: 'arb106_five_nouns', subject: 'Arabic 106', student: 'Mostafa' },
      { id: 'arb106_types_of_predicate', subject: 'Arabic 106', student: 'Mostafa' },
      { id: 'arb106_nakira_marifa', subject: 'Arabic 106', student: 'Mostafa' },

      // Ali Arabic 105 (2)
      { id: 'arb105_nominal_sentence', subject: 'Arabic 105', student: 'Ali' },
      { id: 'arb105_object_mafool', subject: 'Arabic 105', student: 'Ali' },

      // Mostafa ICT 106 (2)
      { id: 'ict106_flowcharts', subject: 'ICT 106', student: 'Mostafa' },
      { id: 'ict106_loops_variables', subject: 'ICT 106', student: 'Mostafa' },

      // Ali ICT 105 (2)
      { id: 'ict105_scratch_logic', subject: 'ICT 105', student: 'Ali' },
      { id: 'ict105_cyber_safety', subject: 'ICT 105', student: 'Ali' },

      // Mostafa Social Studies 106 (2)
      { id: 'soc106_arab_geography', subject: 'Social Studies 106', student: 'Mostafa' },
      { id: 'soc106_arab_environment', subject: 'Social Studies 106', student: 'Mostafa' },

      // Ali Social Studies 105 (2)
      { id: 'soc105_egypt_geography', subject: 'Social Studies 105', student: 'Ali' },
      { id: 'soc105_ancient_civilization', subject: 'Social Studies 105', student: 'Ali' }
    ];

    expectedUnits.forEach(expected => {
      const u = window.HUMANITIES_STUDIO_MAP[expected.id];
      assert.ok(u, `Unit ${expected.id} must exist in window.HUMANITIES_STUDIO_MAP`);
      assert.equal(u.subjectCode, expected.subject, `${expected.id} must belong to ${expected.subject}`);
      assert.equal(u.student, expected.student, `${expected.id} must belong to ${expected.student}`);
    });
  });

  await t.test('2. Anti-Placeholder & Pedagogical Completeness: Theory, Rules, Examples, Traps & 10 Flashcards per unit', () => {
    let totalCards = 0;

    window.HUMANITIES_STUDIO_DATA.forEach(u => {
      assert.ok(u.title && u.title.length > 5, `Unit ${u.id} must have a descriptive title`);
      assert.ok(u.theory, `Unit ${u.id} must have theory section`);
      assert.ok(u.theory.concept && u.theory.concept.length > 20, `Unit ${u.id} concept must be substantial`);
      assert.ok(Array.isArray(u.theory.rules) && u.theory.rules.length >= 3, `Unit ${u.id} must have >= 3 detailed rules`);
      assert.ok(Array.isArray(u.theory.examples) && u.theory.examples.length >= 1, `Unit ${u.id} must have real examples`);
      assert.ok(u.theory.traps && u.theory.traps.length > 10, `Unit ${u.id} must document exam traps`);

      // Exactly 10 Flashcards
      assert.ok(Array.isArray(u.flashcards), `Unit ${u.id} flashcards must be an array`);
      assert.equal(u.flashcards.length, 10, `Unit ${u.id} must contain exactly 10 flashcards`);

      u.flashcards.forEach((fc, idx) => {
        assert.ok(fc.q && fc.q.length >= 5, `Unit ${u.id} card #${idx+1} must have a valid question`);
        assert.ok(fc.a && fc.a.length >= 3, `Unit ${u.id} card #${idx+1} must have a valid answer`);
        assert.ok(!fc.q.includes('قيد الإعداد') && !fc.a.includes('قيد الإعداد'), `Card #${idx+1} in ${u.id} must not be a placeholder`);
      });

      totalCards += u.flashcards.length;
    });

    assert.equal(totalCards, 190, 'Total Humanities flashcards across all 19 units must equal exactly 190');
  });

  await t.test('3. Subject Workspace Units Rendering: Correct counts per humanities subject', () => {
    const container = document.getElementById('sw-studio-units-list');
    assert.ok(container, '#sw-studio-units-list must exist');

    // Mostafa English 106 -> 3 units
    window.renderSubjectStudioUnits('English 106', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 3, 'English 106 must display 3 units');

    // Mostafa Arabic 106 -> 3 units
    window.renderSubjectStudioUnits('Arabic 106', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 3, 'Arabic 106 must display 3 units');

    // Mostafa ICT 106 -> 2 units
    window.renderSubjectStudioUnits('ICT 106', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 2, 'ICT 106 must display 2 units');

    // Mostafa Social Studies 106 -> 2 units
    window.renderSubjectStudioUnits('Social Studies 106', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 2, 'Social Studies 106 must display 2 units');

    // Ali English 105 -> 3 units
    window.renderSubjectStudioUnits('English 105', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 3, 'English 105 must display 3 units');

    // Ali Arabic 105 -> 2 units
    window.renderSubjectStudioUnits('Arabic 105', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 2, 'Arabic 105 must display 2 units');

    // Ali ICT 105 -> 2 units
    window.renderSubjectStudioUnits('ICT 105', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 2, 'ICT 105 must display 2 units');

    // Ali Social Studies 105 -> 2 units
    window.renderSubjectStudioUnits('Social Studies 105', 'sw-studio-units-list');
    assert.equal(container.querySelectorAll('.studio-unit-card').length, 2, 'Social Studies 105 must display 2 units');
  });

  await t.test('4. Modal Lifecycle & Flashcard Interaction on Humanities Unit', () => {
    const modal = document.getElementById('unit-studio-modal');

    // Open Arabic Five Nouns Unit
    window.openStudioUnit('arb106_five_nouns');
    assert.ok(modal.classList.contains('active'), 'Modal must become active');
    assert.equal(document.getElementById('studio-modal-title').textContent, 'الأسماء الخمسة وعلامات إعرابها الفرعية');

    // Switch to Flashcards Tab
    window.switchStudioTab('flashcards');
    assert.equal(document.getElementById('studio-tab-pane-flashcards').style.display, 'block');

    const cardBox = document.getElementById('studio-flashcard-box');
    assert.ok(!cardBox.classList.contains('flipped'), 'Card must initially not be flipped');

    // Flip Card
    window.flipFlashcard();
    assert.ok(cardBox.classList.contains('flipped'), 'Card must be flipped after flipFlashcard()');

    // Next Card
    window.nextFlashcard();
    assert.equal(document.getElementById('studio-flashcard-counter').textContent, 'بطاقة 2 من 10');

    // Previous Card
    window.prevFlashcard();
    assert.equal(document.getElementById('studio-flashcard-counter').textContent, 'بطاقة 1 من 10');

    // Close Modal
    window.closeStudioModal();
    assert.ok(!modal.classList.contains('active'), 'Modal must close cleanly');
  });

  await t.test('5. Interactive Simulation Engines: All 19 Humanities Tools Mount and Function Cleanly', () => {
    const labContainer = document.getElementById('studio-lab-container');

    // Verify all 19 units mount non-empty lab content
    window.HUMANITIES_STUDIO_DATA.forEach(u => {
      window.openStudioUnit(u.id);
      window.switchStudioTab('lab');

      assert.ok(labContainer.innerHTML.length > 50, `Lab for ${u.id} must render non-empty content`);
      assert.ok(!labContainer.innerHTML.includes('قيد الإعداد'), `Lab for ${u.id} must be implemented`);
    });

    // Specific tool functional validations:
    // Lab 1: Relative clauses select
    window.openStudioUnit('eng106_relative_clauses');
    window.switchStudioTab('lab');
    const rcSelect = document.getElementById('rc-pair-select');
    rcSelect.value = 'telescope';
    rcSelect.dispatchEvent(new window.Event('change'));
    assert.ok(document.getElementById('rc-result-sentence').textContent.includes('telescope'));

    // Lab 7: Five nouns
    window.openStudioUnit('arb106_five_nouns');
    window.switchStudioTab('lab');
    const fnSelect = document.getElementById('fn-sentence-select');
    fnSelect.value = '2';
    fnSelect.dispatchEvent(new window.Event('change'));
    assert.ok(document.getElementById('fn-result-text').textContent.includes('أباك'));

    // Lab 10: Nominal sentence scale
    window.openStudioUnit('arb105_nominal_sentence');
    window.switchStudioTab('lab');
    document.querySelector('.btn-ns-num[data-n="dual"]').click();
    assert.equal(document.getElementById('ns-sub-box').textContent, 'الطالبانِ');

    // Lab 12: Flowchart execution
    window.openStudioUnit('ict106_flowcharts');
    window.switchStudioTab('lab');
    document.getElementById('fc-score-input').value = '85';
    document.getElementById('btn-fc-run').click();
    assert.ok(document.getElementById('fc-trace-summary').textContent.includes('Pass'));

    // Lab 13: Loop trace table
    window.openStudioUnit('ict106_loops_variables');
    window.switchStudioTab('lab');
    document.getElementById('loop-n-input').value = '5';
    document.getElementById('btn-run-loop-trace').click();
    assert.ok(document.getElementById('loop-final-val').textContent.includes('Total = 15'));

    // Lab 14: Scratch coordinates
    window.openStudioUnit('ict105_scratch_logic');
    window.switchStudioTab('lab');
    document.getElementById('btn-sc-right').click();
    assert.equal(document.getElementById('sc-x-val').textContent, '20');

    // Lab 16: Arab geography straits
    window.openStudioUnit('soc106_arab_geography');
    window.switchStudioTab('lab');
    document.querySelector('.btn-geo-item[data-item="mandab"]').click();
    assert.ok(document.getElementById('geo-title').textContent.includes('باب المندب'));

    // Lab 18: Egypt geography borders
    window.openStudioUnit('soc105_egypt_geography');
    window.switchStudioTab('lab');
    document.querySelector('.btn-eg-border[data-b="suez"]').click();
    assert.ok(document.getElementById('eg-title').textContent.includes('قناة السويس'));

    window.closeStudioModal();
  });

  dom.window.close();
});
