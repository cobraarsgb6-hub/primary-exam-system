# Feature Specification: P5 — Test Suite Harmonization & Autonomous Release Gate

**Feature Directory:** `specs/006-test-release-gate`  
**Status:** In Progress / Verifying  
**Author:** Antigravity Architect (for Ahmed Ibrahim)  
**Date:** October 30, 2026  

---

## 1. Executive Summary & Problem Statement
Prior to Phase 5, the testing ecosystem across `primary-exam-system` suffered from count discrepancies (documentation variously citing 43, 48, 51, or 53 tests) and lacked an enforced CI/CD release gate. In addition, browser-level end-to-end tests were blocked after the Phase 2 introduction of the SHA-256 PIN gateway dialog because headless automation lacked simulated credential resolution.

Phase 5 harmonizes all test suites, establishes an authoritative truth ledger of test execution counts, guarantees automated PIN resolution in E2E testing environments, and adds a pre-deployment verification gate to `.github/workflows/deploy-pages.yml` so that broken builds or failing tests strictly block GitHub Pages deployment.

---

## 2. Harmonized Test Architecture & Counts
The test suite is canonically structured into three distinct layers executed from exact source `HEAD`:

| Test Suite | Runner | Test Count | Scope |
|---|---|---|---|
| **Server & Node Unit Tests** | `npm test` (`node --test`) | **53 Tests** | Session isolation, answer normalization, scoring integrity, rate limiting, token security, difficulty levels, Arabic headers. |
| **Playwright Master E2E Suite** | `python tests/e2e/run_all_e2e.py` | **51 Tests** | 4-Tier Opaque Box browser testing: Core coverage (25), Boundary & corner cases (20), Cross-feature scenarios (4), Real-world workflows (2). |
| **Interactive Multi-Subject Browser Test** | `python tests/test_multisubject_navigation.py` | **End-to-End** | Live interactive browser test verifying PIN gateway unlocking (`2014` / `2016`), subject filters (Math, Science, Arabic), and full quiz lifecycle with 0 console errors. |

**Total Canonical Automated Checks:** **104 passing tests** (53 unit/server + 51 E2E) + 1 interactive multi-subject browser suite.

---

## 3. Acceptance Criteria
1. **Zero Failing Tests:** Both `npm test` (53 tests) and `python tests/e2e/run_all_e2e.py` (51 tests) pass with 100% success rate.
2. **Interactive UI Verification:** `python tests/test_multisubject_navigation.py` executes without hanging or timeouts and outputs zero console errors.
3. **CI/CD Quality Gate:** `.github/workflows/deploy-pages.yml` incorporates a required `test` job running `npm test` that prevents deployment if any test fails.
4. **Single Source of Truth:** `CURRENT_STATUS_AR.md` explicitly documents the exact counts and execution commands.
