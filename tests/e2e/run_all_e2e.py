"""
Master E2E Test Runner for primary-exam-system
Executes all 4 Tiers of the Opaque-Box E2E Testing Suite:
  - Tier 1: Core Feature Coverage (25 tests)
  - Tier 2: Boundary & Corner Cases (20 tests)
  - Tier 3: Cross-Feature Integration Scenarios (4 scenarios)
  - Tier 4: Real-World Application Scenarios (2 scenarios)
Produces structured pass/fail metrics and returns clean exit codes.
"""

import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from tests.e2e.harness import E2EHarness
from tests.e2e import tier1_core_coverage
from tests.e2e import tier2_boundary_corner
from tests.e2e import tier3_cross_feature
from tests.e2e import tier4_real_world

def main():
    print("================================================================================")
    print("       PRIMARY-EXAM-SYSTEM COMPREHENSIVE 4-TIER E2E TEST RUNNER")
    print("================================================================================")
    total_start = time.perf_counter()

    all_results = {}
    total_passed = 0
    total_failed = 0

    with E2EHarness(headless=True) as h:
        # Tier 1
        t1_start = time.perf_counter()
        t1_res = tier1_core_coverage.run_all(harness=h)
        all_results['Tier 1: Core Feature Coverage'] = {
            'results': t1_res,
            'duration': (time.perf_counter() - t1_start) * 1000
        }

        # Tier 2
        t2_start = time.perf_counter()
        t2_res = tier2_boundary_corner.run_all(harness=h)
        all_results['Tier 2: Boundary & Corner Cases'] = {
            'results': t2_res,
            'duration': (time.perf_counter() - t2_start) * 1000
        }

        # Tier 3
        t3_start = time.perf_counter()
        t3_res = tier3_cross_feature.run_all(harness=h)
        all_results['Tier 3: Cross-Feature Integration'] = {
            'results': t3_res,
            'duration': (time.perf_counter() - t3_start) * 1000
        }

        # Tier 4
        t4_start = time.perf_counter()
        t4_res = tier4_real_world.run_all(harness=h)
        all_results['Tier 4: Real-World Scenarios'] = {
            'results': t4_res,
            'duration': (time.perf_counter() - t4_start) * 1000
        }

    total_duration = (time.perf_counter() - total_start) * 1000

    print("\n" + "=" * 80)
    print("                      GRAND E2E TEST EXECUTION SUMMARY")
    print("=" * 80)
    print(f"{'Tier Name':<42} | {'Count':<6} | {'Passed':<7} | {'Failed':<7} | {'Duration (s)':<12}")
    print("-" * 80)

    for tier_name, data in all_results.items():
        res_list = data['results']
        count = len(res_list)
        passed = sum(1 for r in res_list if r['status'] == 'PASS')
        failed = sum(1 for r in res_list if r['status'] == 'FAIL')
        total_passed += passed
        total_failed += failed
        dur_sec = data['duration'] / 1000.0
        print(f"{tier_name:<42} | {count:<6} | {passed:<7} | {failed:<7} | {dur_sec:>10.2f}s")

    print("-" * 80)
    total_tests = total_passed + total_failed
    pass_rate = (total_passed / total_tests * 100.0) if total_tests > 0 else 0.0
    print(f"{'TOTAL / OVERALL':<42} | {total_tests:<6} | {total_passed:<7} | {total_failed:<7} | {(total_duration/1000.0):>10.2f}s")
    print("=" * 80)
    print(f"OVERALL STATUS: {'PASS' if total_failed == 0 else 'FAIL'} (Pass Rate: {pass_rate:.1f}%)")
    print(f"Total Execution Time: {total_duration/1000.0:.2f} seconds")
    print("=" * 80)

    if total_failed > 0:
        print("\nFAILED TESTS BREAKDOWN:")
        for tier_name, data in all_results.items():
            for r in data['results']:
                if r['status'] == 'FAIL':
                    print(f"  [{tier_name}] {r['name']} -> {r['error']}")
        sys.exit(1)
    else:
        print("\nALL 51 TESTS PASSED WITH 100% SUCCESS!")
        sys.exit(0)

if __name__ == '__main__':
    main()
