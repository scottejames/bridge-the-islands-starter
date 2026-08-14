"""
Test harness for Bridge the Islands.

Run all cases in ../test_data/{simple,medium,hard}/ against your solution
and report PASS/FAIL per case, per tier, and overall, with timing. Exits
with status 1 if any test fails.

Simple and medium cases are small enough to trace by hand; hard cases are
larger generated cases intended to test how your solution scales, not
just whether it's correct. See ../test_data/README.md for details on
every case.
"""

import time

from bridge_islands import count_reachable_queries
from test_data import load_tier

TIERS = ["simple", "medium", "hard"]


def run_tier(tier: str):
    cases = load_tier(tier)
    passed = 0
    failed = 0
    total_ms = 0.0

    for case in cases:
        start = time.perf_counter()
        try:
            actual = count_reachable_queries(case.n, case.events)
        except NotImplementedError:
            actual = "NOT IMPLEMENTED"
        elapsed_ms = (time.perf_counter() - start) * 1000
        total_ms += elapsed_ms

        ok = actual == case.expected
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {tier}/{case.name}: expected={case.expected} actual={actual} ({elapsed_ms:.1f}ms)")

        if ok:
            passed += 1
        else:
            failed += 1

    return passed, failed, total_ms


def efficiency_band(hard_all_passed: bool, hard_total_ms: float) -> str:
    if not hard_all_passed:
        return "N/A -- hard tier did not fully pass"
    if hard_total_ms < 2000:
        return "Efficient (< 2s total)"
    if hard_total_ms < 10000:
        return "Adequate (2-10s total)"
    return "Slow (> 10s total) -- worth revisiting your approach"


def main() -> None:
    total_passed = 0
    total_failed = 0
    tier_stats = {}

    for tier in TIERS:
        print(f"\n--- {tier} ---")
        passed, failed, total_ms = run_tier(tier)
        total_passed += passed
        total_failed += failed
        tier_stats[tier] = (passed, failed, total_ms)
        print(f"{tier}: {passed} passed, {failed} failed, total {total_ms:.1f}ms")

    print(f"\nTOTAL: {total_passed} passed, {total_failed} failed out of {total_passed + total_failed}")

    hard_passed, hard_failed, hard_ms = tier_stats["hard"]
    print(f"Hard tier: {hard_passed}/{hard_passed + hard_failed} passed, {hard_ms:.1f}ms total")
    print(f"Efficiency band: {efficiency_band(hard_failed == 0, hard_ms)}")

    raise SystemExit(1 if total_failed else 0)


if __name__ == "__main__":
    main()
