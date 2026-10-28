# Forensic Investigation & Implementation Design Report
## Defect 3 (Deep-Linking Parameter Precedence) & Defect 4 (SafeStorage Sandbox Resilience)

**Target**: `Index.html`  
**Milestone**: Milestone 1 (Frontend Defect Remediation)  
**Author**: Explorer M1-2  
**Integrity Mode**: Read-Only Audit & Verification  
**Date**: 2026-10-25T16:08:00Z  

---

## 1. Observation

### 1.1 Context and Scope
The primary assessment portal (`Index.html`) runs both as a standalone web application and embedded inside Google Apps Script (GAS) HTML Service iframes (`https://script.google.com` and `https://*.googleusercontent.com`).
Two critical client-side defects affect user access and storage reliability:
1. **Defect 3**: URL deep-linking parameter precedence at `Index.html:2787-2800` (`preferredExamCode` vs default `activeExamCode`).
2. **Defect 4**: Direct access to `window.localStorage` at `Index.html:2708, 2719, 2731, 2911, 3388, 3712-3713` triggering fatal `SecurityError` / `DOMException` under GAS iframe sandbox restrictions and strict third-party cookie blocking.

---

### 1.2 Direct Codebase Observations & Exact Locations

#### A. URL Deep-Linking & Portal Initial Selection (`Index.html:2773-2816`)
Inspection of lines 2773 to 2816 of `Index.html`:
```javascript
2773:     function openStudentPortal(studentKey, preferredExamCode) {
2774:       // 1. INSTANT SCREEN SWITCH: Switch to student portal immediately on click
2775:       showScreen('screen-student');
2776:       currentStudentKey = studentKey;
2777: 
2778:       const student = STUDENT_DATA[studentKey];
2779:       if (!student) return;
2780: 
2781:       try {
2782:         const titleEl = document.getElementById('sp-student-title');
2783:         const gradeEl = document.getElementById('sp-student-grade');
2784:         if (titleEl) titleEl.innerText = `${student.name}'s Assessment Portal`;
2785:         if (gradeEl) gradeEl.innerText = `${student.grade} • International School`;
2786: 
2787:       // Determine initial selection: keep activeExamCode if already valid for this student, else preferred, else first
2788:       let selectedCode = (preferredExamCode && student.exams.some(ex => ex.code === preferredExamCode))
2789:         ? preferredExamCode
2790:         : (student.exams.some(ex => ex.code === activeExamCode) ? activeExamCode : (student.exams[0] ? student.exams[0].code : ''));
2791: 
2792:       function renderExamCards() {
2793:         const listEl = document.getElementById('sp-exams-list');
2794:         if (!listEl) return;
2795:         listEl.innerHTML = '';
2796:         student.exams.forEach((ex) => {
2797:           const card = document.createElement('button');
2798:           card.type = 'button';
2799:           card.className = 'exam-item-card' + (ex.code === activeExamCode ? ' active' : '');
2800:           card.id = 'exam-item-' + ex.code;
...
2815:       renderExamCards();
2816:       selectStudentExam(selectedCode);
```

**Verbatim Discrepancies Observed**:
1. At line 2787, the developer comment states:  
   `// Determine initial selection: keep activeExamCode if already valid for this student, else preferred, else first`  
   This comment misstates the precedence: `preferredExamCode` is the explicit URL query parameter intention (`?exam=...`) and must take absolute precedence over any default or stale session variable `activeExamCode`.
2. Notice line 2799 in `renderExamCards()`:  
   `card.className = 'exam-item-card' + (ex.code === activeExamCode ? ' active' : '');`  
   Because `activeExamCode` has NOT yet been updated to `selectedCode` at line 2815 when `renderExamCards()` is called, the exam card rendered with `.active` class will initially be `activeExamCode` (e.g. `'EX_Y5_ENG_ADV01'`), NOT the deep-linked exam (`selectedCode`). Then at line 2816, `selectStudentExam(selectedCode)` executes, updating `activeExamCode` and toggling the `.active` class on DOM elements. This causes an optical jump / flicker.
3. Synchronizing `activeExamCode = selectedCode;` before calling `renderExamCards()`, and using `ex.code === selectedCode` inside `renderExamCards()`, guarantees atomic rendering on the very first paint.

---

#### B. Complete Inventory of `localStorage` Invocations in `Index.html`
A search across all 4,406 lines of `Index.html` identified exactly 6 locations referencing `localStorage`:

1. **`Index.html:2708`** (in `saveProgress()`):
   ```javascript
   2706:     function saveProgress() {
   2707:       try {
   2708:         localStorage.setItem(progressKey(), JSON.stringify({
   2709:           sessionKey: currentSessionKey,
   2710:           answers: studentAnswers,
   2711:           currentIdx: currentIdx,
   2712:           savedAt: Date.now()
   2713:         }));
   2714:       } catch (e) { /* storage may be unavailable */ }
   2715:     }
   ```
2. **`Index.html:2719`** (in `loadProgress()`):
   ```javascript
   2717:     function loadProgress(sessionKey) {
   2718:       try {
   2719:         const raw = localStorage.getItem(progressKey());
   2720:         if (!raw) return null;
   ...
   2727:       }
   2728:     }
   ```
3. **`Index.html:2731`** (in `clearProgress()`):
   ```javascript
   2730:     function clearProgress() {
   2731:       try { localStorage.removeItem(progressKey()); } catch (e) { /* ignore */ }
   2732:     }
   ```
4. **`Index.html:2911`** (in `checkExamStatus()` offline simulation fallback):
   ```javascript
   2908:         const student = STUDENT_DATA[currentStudentKey];
   2909:         const lockKey = 'lock_' + examCode + '_' + student.name.replace(/\s+/g, '_');
   2910:         let localLock = null;
   2911:         try { localLock = localStorage.getItem(lockKey); } catch (e) {}
   2912:         const fallback = localLock
   2913:           ? { hasSubmitted: true, attempts: [], lastScore: '', canAttempt: false, retakeStatus: 'NONE', maxAttempts: 2 }
   2914:           : { hasSubmitted: false, attempts: [], canAttempt: true, retakeStatus: 'NONE', maxAttempts: 2 };
   ```
5. **`Index.html:3388`** (in `onSubmissionSuccess()` offline simulation locking):
   ```javascript
   3385:       const student = STUDENT_DATA[currentStudentKey];
   3386:       const lockKey = 'lock_' + activeExamCode + '_' + student.name.replace(/\s+/g, '_');
   3387:       try {
   3388:         localStorage.setItem(lockKey, JSON.stringify({
   3389:           date: new Date().toLocaleDateString(),
   3390:           score: `${res.earnedScore}/${res.totalScore} (${res.percentage}%)`
   3391:         }));
   3392:       } catch (e) { /* ignore */ }
   ```
6. **`Index.html:3712-3713`** (in `clearDeviceLocks()` parent device reset action):
   ```javascript
   3709:     function clearDeviceLocks() {
   3710:       if (confirm('Reset local device locks and saved in-progress answers for all exams on this browser?')) {
   3711:         try {
   3712:           Object.keys(localStorage).forEach(k => {
   3713:             if (k.startsWith('lock_') || k.startsWith('progress_')) localStorage.removeItem(k);
   3714:           });
   3715:           alert('Device data reset successfully.');
   3716:         } catch (e) {
   3717:           alert('Unable to access device storage: ' + e.message);
   3718:         }
   3719:       }
   3720:     }
   ```

---

## 2. Logic Chain

1. **Storage Sandboxing Vulnerability in Google Apps Script**:
   - Google Apps Script web apps embedded in iframes run on `script.googleusercontent.com` across cross-origin boundaries.
   - When users browse with Chrome/Edge/Safari default settings blocking third-party storage, merely referencing `window.localStorage` throws an unhandled DOMException:  
     `DOMException: Failed to read the 'localStorage' property from 'Window': Access is denied for this document.`
   - In `clearDeviceLocks()` (`Index.html:3712`), `Object.keys(localStorage)` is evaluated. If `localStorage` is blocked, this throws immediately, popping up `alert('Unable to access device storage: ...')` and failing the device reset action.
   - Furthermore, if `localStorage` is blocked, `saveProgress()` and `loadProgress()` fail silently to retain any in-progress answers if the user navigates back and forth between questions or modals.

2. **In-Memory Dual-Layer Fallback Architecture**:
   - To make the client 100% resilient, storage operations must never touch `window.localStorage` without an active probe check.
   - A probe test (`window.localStorage.setItem('__probe__', '1'); window.localStorage.removeItem('__probe__')`) safely determines availability once and caches the boolean result.
   - If `window.localStorage` throws `SecurityError` or `QuotaExceededError`, `safeStorage` transparently delegates to an internal `memoryStore = {}` dictionary.
   - In-memory operations allow the active session to save progress, load progress, lock exams locally, and enumerate keys via `safeStorage.keys()` without any exception.

3. **URL Parameter Precedence Logic**:
   - Navigation via URL query parameters (`?student=ali&exam=DAILY_Y5_ENG_W1D3` or `?student=mostafa&exam=DAILY_Y6_ARB_W1D4`) is the primary deep-linking contract for automated homework assignments and parental notifications.
   - When `preferredExamCode` is passed:
     - Check: Is `preferredExamCode` present in `student.exams`?
     - If `true` -> `selectedCode = preferredExamCode` (Top Priority).
     - If `false` -> Fall back to `activeExamCode` (if valid for this student), else `student.exams[0].code`.
   - Before invoking `renderExamCards()`, set `activeExamCode = selectedCode`. This ensures that when the card buttons are generated, the targeted card immediately possesses the `active` CSS class, avoiding repaint artifacts and guaranteeing synchronous UI state.

---

## 3. Caveats

1. **Cross-Session Persistence in Sandboxed Mode**:  
   If a user's browser completely blocks third-party iframe storage (`SecurityError`), `safeStorage` falls back to `memoryStore`. In this fallback state, saved quiz progress is preserved during the active tab session, but will not survive a hard browser page refresh (F5). This is an inherent browser sandbox security constraint, not an application defect.
2. **Read-Only Scope Compliance**:  
   This explorer report is strictly read-only. No edits have been made to `Index.html` or `Code.gs`. The code blocks in Section 4 are formatted as exact, drop-in replacement chunks ready for Worker M1.

---

## 4. Conclusion & Precise Implementation Plan for Worker M1

### Fix 1: Deep-Linking Parameter Precedence & Initial Card Activation
**File**: `C:\Users\co0ob\Projects\primary-exam-system\Index.html`  
**Target Lines**: 2787–2801

#### Exact BEFORE Code Chunk (`Index.html:2787-2801`):
```javascript
      // Determine initial selection: keep activeExamCode if already valid for this student, else preferred, else first
      let selectedCode = (preferredExamCode && student.exams.some(ex => ex.code === preferredExamCode))
        ? preferredExamCode
        : (student.exams.some(ex => ex.code === activeExamCode) ? activeExamCode : (student.exams[0] ? student.exams[0].code : ''));

      function renderExamCards() {
        const listEl = document.getElementById('sp-exams-list');
        if (!listEl) return;
        listEl.innerHTML = '';
        student.exams.forEach((ex) => {
          const card = document.createElement('button');
          card.type = 'button';
          card.className = 'exam-item-card' + (ex.code === activeExamCode ? ' active' : '');
          card.id = 'exam-item-' + ex.code;
```

#### Exact AFTER Drop-in Replacement Chunk:
```javascript
      // Determine initial selection: prioritize preferredExamCode when valid, else activeExamCode if already valid for this student, else first
      let selectedCode = (preferredExamCode && student.exams.some(ex => ex.code === preferredExamCode))
        ? preferredExamCode
        : (activeExamCode && student.exams.some(ex => ex.code === activeExamCode))
          ? activeExamCode
          : (student.exams[0] ? student.exams[0].code : '');

      activeExamCode = selectedCode;

      function renderExamCards() {
        const listEl = document.getElementById('sp-exams-list');
        if (!listEl) return;
        listEl.innerHTML = '';
        student.exams.forEach((ex) => {
          const card = document.createElement('button');
          card.type = 'button';
          card.className = 'exam-item-card' + (ex.code === selectedCode ? ' active' : '');
          card.id = 'exam-item-' + ex.code;
```

---

### Fix 2: Define `safeStorage` Resilient Storage Module
**File**: `C:\Users\co0ob\Projects\primary-exam-system\Index.html`  
**Target Location**: Immediately before `function progressKey()` at Line 2700.

#### Exact Code to Insert:
```javascript
    /**
     * Resilient safeStorage wrapper for Google Apps Script iframe sandbox & strict storage policies.
     * Automatically falls back to an in-memory store if localStorage throws SecurityError or QuotaExceededError.
     */
    const safeStorage = (function () {
      const memoryStore = {};

      function getStorage() {
        try {
          if (typeof window !== 'undefined' && 'localStorage' in window && window.localStorage !== null) {
            const testKey = '__storage_probe__';
            window.localStorage.setItem(testKey, '1');
            window.localStorage.removeItem(testKey);
            return window.localStorage;
          }
        } catch (e) {
          // localStorage inaccessible (GAS iframe sandbox SecurityError / disabled third-party cookies)
        }
        return null;
      }

      let storageInstance = undefined;
      function storage() {
        if (storageInstance === undefined) {
          storageInstance = getStorage();
        }
        return storageInstance;
      }

      return {
        getItem: function (key) {
          try {
            const s = storage();
            if (s) {
              const val = s.getItem(key);
              if (val !== null) return val;
            }
          } catch (e) { /* fallback to memory */ }
          return Object.prototype.hasOwnProperty.call(memoryStore, key) ? memoryStore[key] : null;
        },
        setItem: function (key, value) {
          const strVal = String(value);
          try {
            const s = storage();
            if (s) {
              s.setItem(key, strVal);
            }
          } catch (e) { /* ignore quota/sandbox errors */ }
          memoryStore[key] = strVal;
        },
        removeItem: function (key) {
          try {
            const s = storage();
            if (s) {
              s.removeItem(key);
            }
          } catch (e) { /* ignore */ }
          delete memoryStore[key];
        },
        keys: function () {
          const keySet = new Set();
          try {
            const s = storage();
            if (s) {
              for (let i = 0; i < s.length; i++) {
                const k = s.key(i);
                if (k) keySet.add(k);
              }
            }
          } catch (e) { /* ignore */ }
          Object.keys(memoryStore).forEach(k => keySet.add(k));
          return Array.from(keySet);
        },
        // Convenience method aliases
        get: function (key) { return this.getItem(key); },
        set: function (key, val) { return this.setItem(key, val); },
        remove: function (key) { return this.removeItem(key); }
      };
    })();
```

Also, in the bottom global exports block (around line 4340), expose `safeStorage` for testing and console inspection:
```javascript
window.safeStorage = safeStorage;
```

---

### Fix 3: Replace Unshielded `localStorage` Invocations with `safeStorage`

#### 3A. `Index.html:2706-2733` (`saveProgress`, `loadProgress`, `clearProgress`)

**BEFORE**:
```javascript
    function saveProgress() {
      try {
        localStorage.setItem(progressKey(), JSON.stringify({
          sessionKey: currentSessionKey,
          answers: studentAnswers,
          currentIdx: currentIdx,
          savedAt: Date.now()
        }));
      } catch (e) { /* storage may be unavailable */ }
    }

    function loadProgress(sessionKey) {
      try {
        const raw = localStorage.getItem(progressKey());
        if (!raw) return null;
        const saved = JSON.parse(raw);
        if (saved.sessionKey !== sessionKey) return null;
        if (!saved.savedAt || Date.now() - saved.savedAt > 3 * 60 * 60 * 1000) return null;
        return saved;
      } catch (e) {
        return null;
      }
    }

    function clearProgress() {
      try { localStorage.removeItem(progressKey()); } catch (e) { /* ignore */ }
    }
```

**AFTER**:
```javascript
    function saveProgress() {
      try {
        safeStorage.setItem(progressKey(), JSON.stringify({
          sessionKey: currentSessionKey,
          answers: studentAnswers,
          currentIdx: currentIdx,
          savedAt: Date.now()
        }));
      } catch (e) { /* storage may be unavailable */ }
    }

    function loadProgress(sessionKey) {
      try {
        const raw = safeStorage.getItem(progressKey());
        if (!raw) return null;
        const saved = JSON.parse(raw);
        if (saved.sessionKey !== sessionKey) return null;
        if (!saved.savedAt || Date.now() - saved.savedAt > 3 * 60 * 60 * 1000) return null;
        return saved;
      } catch (e) {
        return null;
      }
    }

    function clearProgress() {
      try { safeStorage.removeItem(progressKey()); } catch (e) { /* ignore */ }
    }
```

---

#### 3B. `Index.html:2908-2916` (`checkExamStatus` simulation fallback)

**BEFORE**:
```javascript
        const student = STUDENT_DATA[currentStudentKey];
        const lockKey = 'lock_' + examCode + '_' + student.name.replace(/\s+/g, '_');
        let localLock = null;
        try { localLock = localStorage.getItem(lockKey); } catch (e) {}
        const fallback = localLock
          ? { hasSubmitted: true, attempts: [], lastScore: '', canAttempt: false, retakeStatus: 'NONE', maxAttempts: 2 }
          : { hasSubmitted: false, attempts: [], canAttempt: true, retakeStatus: 'NONE', maxAttempts: 2 };
        setTimeout(() => renderStudentStatus(fallback, studentName, examCode), 200);
```

**AFTER**:
```javascript
        const student = STUDENT_DATA[currentStudentKey];
        const lockKey = 'lock_' + examCode + '_' + student.name.replace(/\s+/g, '_');
        let localLock = null;
        try { localLock = safeStorage.getItem(lockKey); } catch (e) {}
        const fallback = localLock
          ? { hasSubmitted: true, attempts: [], lastScore: '', canAttempt: false, retakeStatus: 'NONE', maxAttempts: 2 }
          : { hasSubmitted: false, attempts: [], canAttempt: true, retakeStatus: 'NONE', maxAttempts: 2 };
        setTimeout(() => renderStudentStatus(fallback, studentName, examCode), 200);
```

---

#### 3C. `Index.html:3385-3393` (`onSubmissionSuccess` local locking)

**BEFORE**:
```javascript
      const student = STUDENT_DATA[currentStudentKey];
      const lockKey = 'lock_' + activeExamCode + '_' + student.name.replace(/\s+/g, '_');
      try {
        localStorage.setItem(lockKey, JSON.stringify({
          date: new Date().toLocaleDateString(),
          score: `${res.earnedScore}/${res.totalScore} (${res.percentage}%)`
        }));
      } catch (e) { /* ignore */ }
```

**AFTER**:
```javascript
      const student = STUDENT_DATA[currentStudentKey];
      const lockKey = 'lock_' + activeExamCode + '_' + student.name.replace(/\s+/g, '_');
      try {
        safeStorage.setItem(lockKey, JSON.stringify({
          date: new Date().toLocaleDateString(),
          score: `${res.earnedScore}/${res.totalScore} (${res.percentage}%)`
        }));
      } catch (e) { /* ignore */ }
```

---

#### 3D. `Index.html:3709-3720` (`clearDeviceLocks`)

**BEFORE**:
```javascript
    function clearDeviceLocks() {
      if (confirm('Reset local device locks and saved in-progress answers for all exams on this browser?')) {
        try {
          Object.keys(localStorage).forEach(k => {
            if (k.startsWith('lock_') || k.startsWith('progress_')) localStorage.removeItem(k);
          });
          alert('Device data reset successfully.');
        } catch (e) {
          alert('Unable to access device storage: ' + e.message);
        }
      }
    }
```

**AFTER**:
```javascript
    function clearDeviceLocks() {
      if (confirm('Reset local device locks and saved in-progress answers for all exams on this browser?')) {
        try {
          safeStorage.keys().forEach(k => {
            if (k.startsWith('lock_') || k.startsWith('progress_')) safeStorage.removeItem(k);
          });
          alert('Device data reset successfully.');
        } catch (e) {
          alert('Unable to access device storage: ' + (e && e.message ? e.message : e));
        }
      }
    }
```

---

## 5. Verification Method

To independently verify the investigation findings and validate the implementation:

### 1. AST Syntax Validation
Run Node.js syntax verification against the `<script>` tag inside `Index.html`:
```powershell
python -c "import re, subprocess; c = open('Index.html', encoding='utf-8').read(); m = re.search(r'<script\b[^>]*>(.*?)</script>', c, re.DOTALL); subprocess.run(['node', '--check'], input=m.group(1), text=True, check=True)"
```
**Expected Output**: Exit code `0` with zero syntax warnings.

### 2. Deep-Linking Verification Test
Run Playwright against URL parameters for both Ali and Mostafa:
```powershell
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html?student=ali&exam=DAILY_Y5_ENG_W1D3')
    page.wait_for_timeout(800)
    card_id = page.evaluate('() => document.querySelector(\".exam-item-card.active\")?.id')
    print('Ali deep link active card:', card_id)
    assert card_id == 'exam-item-DAILY_Y5_ENG_W1D3', f'Expected exam-item-DAILY_Y5_ENG_W1D3, got {card_id}'

    page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html?student=mostafa&exam=DAILY_Y6_ARB_W1D4')
    page.wait_for_timeout(800)
    card_id_m = page.evaluate('() => document.querySelector(\".exam-item-card.active\")?.id')
    print('Mostafa deep link active card:', card_id_m)
    assert card_id_m == 'exam-item-DAILY_Y6_ARB_W1D4', f'Expected exam-item-DAILY_Y6_ARB_W1D4, got {card_id_m}'
    browser.close()
    print('ALL DEEP LINK TESTS PASSED!')
"
```

### 3. Sandbox Storage Resilience Under Simulated `SecurityError`
Run Playwright with `localStorage` explicitly throwing a DOMException:
```powershell
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.add_init_script('''
        Object.defineProperty(window, 'localStorage', {
            get: () => { throw new DOMException('Access is denied for this document.', 'SecurityError'); }
        });
    ''')
    errors = []
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto('file:///C:/Users/co0ob/Projects/primary-exam-system/Index.html?student=ali&exam=DAILY_Y5_ENG_W1D3')
    page.wait_for_timeout(1000)
    res = page.evaluate('''() => {
        window.safeStorage.setItem('test_k', '123');
        return { val: window.safeStorage.getItem('test_k'), keys: window.safeStorage.keys() };
    }''')
    print('Resilience probe result:', res)
    assert len(errors) == 0, f'Page errors encountered: {errors}'
    assert res['val'] == '123'
    browser.close()
    print('SANDBOX RESILIENCE VERIFIED!')
"
```

### 4. Invalidation Conditions
- If `document.querySelector('.exam-item-card.active')` resolves to `exam-item-EX_Y5_ENG_ADV01` when deep-linking to `DAILY_Y5_ENG_W1D3`, Defect 3 is NOT remediated.
- If accessing or resetting storage throws `SecurityError: Failed to read the 'localStorage' property from 'Window'`, Defect 4 is NOT remediated.
