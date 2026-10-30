# Implementation Plan: 003-security-privacy

**Branch**: `master` | **Feature Path**: `specs/003-security-privacy`
**Status**: Completed & Verified | **Readiness Gate**: 48/48 Tests PASS

---

## 🛡️ 1. Architecture & Security Invariants

### 1. Unified Token & Claims Architecture
* **Server-Issued Tokens**: All student and administrative operations require short-lived, server-minted tokens (`ACCESS_TOK_*`).
* **Cryptographic Claims**: Each token contains strict role (`student` or `parent`), identity (`ali`, `mostafa`), issue timestamp, and expiration (`expiresAt`).
* **Session sweeps & LockService**: Concurrency and duplicate submissions protected via server-side locking.

### 2. Cross-Student Data Isolation Invariant
* No student can query or submit on behalf of the other student.
* `studentKeyForIdentity_(identity)` resolves canonical keys (`ali`, `mostafa`).
* Requests with mismatched tokens fail immediately with `UNAUTHORIZED` or `STUDENT_MISMATCH`.

### 3. Server-Only Correct Answers & Grading Invariant
* `publicQuestions_` strips `correctAnswer`, `options` solution hints, and pedagogical explanations before returning questions to the client browser.
* Grading is computed exclusively on the server in `gradeSessionAnswers_`.

### 4. PIN Brute-Force Rate Limiting
* Failed PIN attempts tracked in `CacheService`.
* Exceeding 8 failed attempts triggers automatic 10-minute lockout across all roles.

---

## 🧪 2. Security Test Suite (`tests/security.test.js`)
* **Test 1**: Rejection of forged and missing student tokens.
* **Test 2**: Cross-student data isolation (Ali token cannot access Mostafa mission/retake).
* **Test 3**: Rejection of administrative RPCs without valid admin token.
* **Test 4**: `getExamData` strictly strips correct answers and explanations.
* **Test 5**: Gateway PIN rate limiting protects against brute force.
