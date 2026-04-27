#!/usr/bin/env python3
"""Regression detection for CE7 skill-eval history.

Compares the latest run against previous runs and flags regressions.
Stdlib-only, no API calls, runs locally in < 1 second.

Usage:
    python3 scripts/regression_check.py
    python3 scripts/regression_check.py --threshold 10
    python3 scripts/regression_check.py --last-n 5
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY_PATH = ROOT / "reports" / "skill-eval-history.jsonl"


def load_history() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    rows = []
    for line in HISTORY_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def check_regression(threshold: float = 10.0, last_n: int = 10) -> int:
    history = load_history()

    if len(history) < 2:
        print("INFO: Not enough history for regression check (need >= 2 runs).")
        print(f"  Current runs in history: {len(history)}")
        print("  Run more benchmarks to enable regression detection.")
        return 0

    latest = history[-1]
    previous = history[-2]

    latest_score = latest["deterministic"]["average_score"]
    previous_score = previous["deterministic"]["average_score"]
    delta = latest_score - previous_score

    print(f"Latest run:   {latest['run_id']} (score: {latest_score})")
    print(f"Previous run: {previous['run_id']} (score: {previous_score})")
    print(f"Delta: {delta:+.1f}")

    regressions = []

    # Check 1: Overall score regression
    if delta < -threshold:
        regressions.append(
            f"REGRESSION: Average score dropped {abs(delta):.1f} points "
            f"({previous_score} → {latest_score}), threshold={threshold}"
        )

    # Check 2: New failures that didn't exist before
    latest_fails = latest["deterministic"].get("fail", 0)
    previous_fails = previous["deterministic"].get("fail", 0)
    if latest_fails > previous_fails:
        regressions.append(
            f"REGRESSION: FAIL count increased ({previous_fails} → {latest_fails})"
        )

    # Check 3: New issue types appeared
    latest_issues = latest.get("issue_counts", {})
    previous_issues = previous.get("issue_counts", {})
    for key in latest_issues:
        if latest_issues[key] > previous_issues.get(key, 0):
            regressions.append(
                f"WARNING: '{key}' increased ({previous_issues.get(key, 0)} → {latest_issues[key]})"
            )

    # Check 4: Per-case regression (if lowest_scoring_cases overlap)
    latest_cases = {c["prompt_id"]: c for c in latest.get("lowest_scoring_cases", [])}
    previous_cases = {c["prompt_id"]: c for c in previous.get("lowest_scoring_cases", [])}
    for prompt_id, latest_case in latest_cases.items():
        if prompt_id in previous_cases:
            prev_score = previous_cases[prompt_id]["deterministic_score"]
            curr_score = latest_case["deterministic_score"]
            if curr_score < prev_score - threshold:
                regressions.append(
                    f"REGRESSION: '{prompt_id}' score dropped "
                    f"({prev_score} → {curr_score})"
                )

    # Check 5: Trend analysis (if enough history)
    if len(history) >= last_n:
        recent = history[-last_n:]
        scores = [r["deterministic"]["average_score"] for r in recent]
        trend = scores[-1] - scores[0]
        if trend < -threshold:
            regressions.append(
                f"TREND WARNING: Score declining over last {last_n} runs "
                f"({scores[0]} → {scores[-1]}, delta={trend:+.1f})"
            )

    # Output
    if regressions:
        print("\n⚠️  REGRESSIONS DETECTED:")
        for r in regressions:
            print(f"  - {r}")
        print(f"\nAction: Review docs/evaluation-improvement-playbook.md section 4 for fix-target guidance.")
        return 1
    else:
        print("\n✅ No regression detected.")

    # Summary stats
    print(f"\nHistory depth: {len(history)} runs")
    if len(history) >= 3:
        all_scores = [r["deterministic"]["average_score"] for r in history]
        print(f"Score range: {min(all_scores):.1f} – {max(all_scores):.1f}")
        print(f"Latest 3 runs: {[r['deterministic']['average_score'] for r in history[-3:]]}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="CE7 regression detection")
    parser.add_argument(
        "--threshold", type=float, default=10.0,
        help="Score drop threshold to flag as regression (default: 10)"
    )
    parser.add_argument(
        "--last-n", type=int, default=10,
        help="Number of recent runs for trend analysis (default: 10)"
    )
    args = parser.parse_args()
    return check_regression(threshold=args.threshold, last_n=args.last_n)


if __name__ == "__main__":
    sys.exit(main())
