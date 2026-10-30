const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

test('Isolated Video Player (Phase 10): Architecture & YouTube Escape Prevention', async (t) => {
  const htmlPath = path.join(__dirname, '..', 'Index.bundle.html');
  const htmlContent = fs.readFileSync(htmlPath, 'utf8');

  await t.test('1. Structure: Pointer shield, Celebration card, and Custom Controls exist', () => {
    const dom = new JSDOM(htmlContent, { runScripts: 'dangerously' });
    const document = dom.window.document;

    const container = document.getElementById('isolated-video-player-container');
    assert.ok(container, 'isolated-video-player-container must exist');

    const shield = document.getElementById('video-pointer-shield');
    assert.ok(shield, 'video-pointer-shield must exist over iframe');

    const celebration = document.getElementById('video-celebration-screen');
    assert.ok(celebration, 'video-celebration-screen must exist');

    const controls = document.getElementById('isolated-controls-bar');
    assert.ok(controls, 'isolated-controls-bar must exist');

    const btnPlay = document.getElementById('btn-vctrl-play');
    assert.ok(btnPlay, 'btn-vctrl-play must exist');

    const btnMute = document.getElementById('btn-vctrl-mute');
    assert.ok(btnMute, 'btn-vctrl-mute must exist');

    const seek = document.getElementById('vctrl-seek');
    assert.ok(seek, 'vctrl-seek slider must exist');

    const curTime = document.getElementById('vctrl-time-current');
    const totTime = document.getElementById('vctrl-time-total');
    assert.ok(curTime && totTime, 'Time indicators must exist');
  });

  await t.test('2. Security: Cloud player strictly uses youtube-nocookie.com with lockdown params', () => {
    const dom = new JSDOM(htmlContent, { runScripts: 'dangerously' });
    const window = dom.window;

    // Trigger video modal with sample video ID
    window.openVideoModal('FgCBoZxBkDA', 'Circuits Masterclass');

    const iframe = window.document.getElementById('video-iframe');
    assert.ok(iframe, 'video iframe must exist');
    const src = iframe.src;

    assert.ok(src.includes('youtube-nocookie.com/embed/FgCBoZxBkDA'), 'Must use youtube-nocookie.com domain');
    assert.ok(src.includes('rel=0'), 'rel=0 must be enforced');
    assert.ok(src.includes('modestbranding=1'), 'modestbranding=1 must be enforced');
    assert.ok(src.includes('controls=0'), 'controls=0 must disable raw youtube controls');
    assert.ok(src.includes('disablekb=1'), 'disablekb=1 must disable keyboard shortcuts to prevent external popups');
    assert.ok(src.includes('fs=0'), 'fs=0 must disable youtube native fullscreen in favor of in-platform container fullscreen');
    assert.ok(src.includes('playsinline=1'), 'playsinline=1 must force in-page display on mobile');
    assert.ok(src.includes('iv_load_policy=3'), 'iv_load_policy=3 must disable video annotations');
    assert.ok(src.includes('enablejsapi=1'), 'enablejsapi=1 must be enabled for programmatic interception');
  });

  await t.test('3. Early Interception: 2-second lead time triggers celebration screen and hides iframe', () => {
    const dom = new JSDOM(htmlContent, { runScripts: 'dangerously' });
    const window = dom.window;

    window.openVideoModal('FgCBoZxBkDA', 'Circuits Masterclass');
    const iframe = window.document.getElementById('video-iframe');
    const celebration = window.document.getElementById('video-celebration-screen');
    const shield = window.document.getElementById('video-pointer-shield');

    assert.equal(celebration.style.display, 'none', 'Celebration screen starts hidden');

    // Simulate YouTube postMessage API sending time update 1.5s before end (duration: 100, currentTime: 98.5)
    const timeMessage = {
      data: {
        event: 'infoDelivery',
        info: {
          duration: 100,
          currentTime: 98.5,
          playerState: 1
        }
      }
    };
    window.dispatchEvent(new window.MessageEvent('message', timeMessage));

    // After 2s early interception:
    assert.equal(celebration.style.display, 'flex', 'Celebration screen must be displayed');
    assert.equal(iframe.style.display, 'none', 'IFrame must be hidden to block YouTube end screen suggestions');
    assert.equal(shield.style.display, 'none', 'Pointer shield must be hidden so action buttons can be clicked');
    assert.equal(window.isolatedPlayerState.endIntercepted, true, 'endIntercepted state must be true');

    // Action buttons inside celebration
    const labBtn = window.document.getElementById('btn-vcel-lab');
    const practiceBtn = window.document.getElementById('btn-vcel-practice');
    const replayBtn = window.document.getElementById('btn-vcel-replay');
    assert.ok(labBtn && practiceBtn && replayBtn, 'Action buttons must exist inside celebration screen');
  });

  await t.test('4. Empty State: Missing video ID displays curriculum in-production card with NO external links', () => {
    const dom = new JSDOM(htmlContent, { runScripts: 'dangerously' });
    const window = dom.window;

    window.openVideoModal('', 'Unrecorded Lesson');
    const iframe = window.document.getElementById('video-iframe');
    const placeholder = window.document.getElementById('video-placeholder');
    const controls = window.document.getElementById('isolated-controls-bar');

    assert.equal(iframe.style.display, 'none', 'IFrame must not be rendered when video is missing');
    assert.equal(placeholder.style.display, 'flex', 'Placeholder card must be visible');
    assert.equal(controls.style.display, 'none', 'Controls bar must be hidden for empty state');
    assert.ok(placeholder.textContent.includes('قيد الإعداد والمراجعة'), 'Must state in Arabic that video is in production');
  });

  await t.test('5. Pointer Shield Click: Toggles playback in-platform without opening external tabs', () => {
    const dom = new JSDOM(htmlContent, { runScripts: 'dangerously' });
    const window = dom.window;

    window.openVideoModal('FgCBoZxBkDA', 'Circuits Masterclass');
    const shield = window.document.getElementById('video-pointer-shield');
    const btnPlay = window.document.getElementById('btn-vctrl-play');

    assert.ok(shield, 'Pointer shield is present');
    // Initially not playing
    assert.equal(window.isolatedPlayerState.isPlaying, false);

    // Click shield
    shield.click();
    assert.equal(window.isolatedPlayerState.isPlaying, true, 'Clicking shield must toggle to playing');
    assert.equal(btnPlay.innerHTML.includes('إيقاف'), true, 'Play button text must show pause');

    // Click shield again
    shield.click();
    assert.equal(window.isolatedPlayerState.isPlaying, false, 'Clicking shield again must toggle to paused');
    assert.equal(btnPlay.innerHTML.includes('تشغيل'), true, 'Play button text must show play');
  });
});
