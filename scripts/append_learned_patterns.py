#!/usr/bin/env python3
"""Append learned patterns from eval run results to memory/learned-patterns.md.

Usage:
    python3 scripts/append_learned_patterns.py --report runs/2026-04-28-8pack-baseline/report.json

Reads the eval report, identifies:
- Tasks that scored below threshold — logs the failure pattern
- Routing corrections (wrong pack activated) — logs the correction
- Production Bar violations — logs the gap

Appends entries to memory/learned-patterns.md (capped at 50 lines of actionable patterns).

Related (runtime, not eval): `mcp-memory/memory_cli.py promote` appends a deduped
`## PROPOSED` block to the same file from real interaction memory (the Memory MCP DB).
Run both before the weekly synthesis PR — they are complementary sources.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY_FILE = ROOT / "memory" / "learned-patterns.md"
ROUTING_CORRECTIONS_FILE = ROOT / "memory" / "routing-corrections.jsonl"
MAX_MEMORY_LINES = 50


def load_report(report_path: Path) -> dict:
    return json.loads(report_path.read_text(encoding="utf-8"))


def extract_patterns(report: dict) -> list[dict]:
    """Extract actionable patterns from eval report."""
    patterns = []
    today = date.today().isoformat()

    results = report.get("results", report.get("scores", []))
    for result in results:
        task_id = result.get("id", "unknown")
        score = result.get("weighted_score", result.get("score", 100))
        verdict = result.get("verdict", "PASS")

        # Failed or warned task
        if verdict in ("FAIL", "WARN") or score < 70:
            expected_packs = result.get("expected_packs", [])
            actual_packs = result.get("packs_activated", [])
            missing_packs = set(expected_packs) - set(actual_packs)
            unexpected_packs = set(actual_packs) - set(expected_packs)

            if missing_packs or unexpected_packs:
                patterns.append({
                    "date": today,
                    "type": "routing_correction",
                    "task_id": task_id,
                    "expected": list(expected_packs),
                    "missing": list(missing_packs),
                    "unexpected": list(unexpected_packs),
                    "summary": f"Routing issue on {task_id}: missing={list(missing_packs)}, unexpected={list(unexpected_packs)}",
                })
            else:
                patterns.append({
                    "date": today,
                    "type": "quality_gap",
                    "task_id": task_id,
                    "score": score,
                    "verdict": verdict,
                    "summary": f"Task {task_id} scored {score} ({verdict})",
                })

    return patterns


def append_to_memory(patterns: list[dict]) -> int:
    """Append patterns to learned-patterns.md. Respects 50-line cap."""
    if not patterns:
        return 0

    existing = MEMORY_FILE.read_text(encoding="utf-8") if MEMORY_FILE.exists() else ""
    existing_lines = existing.splitlines()

    # Count current actionable lines (non-header, non-blank)
    actionable_lines = [l for l in existing_lines if l.strip() and not l.startswith("#") and not l.startswith(">")]
    remaining_budget = MAX_MEMORY_LINES - len(actionable_lines)

    if remaining_budget <= 0:
        print(f"WARN: memory/learned-patterns.md at {len(actionable_lines)} actionable lines (cap: {MAX_MEMORY_LINES}). Skipping append.")
        return 0

    new_entries = []
    for p in patterns[:remaining_budget]:
        dedup_key = p["task_id"]
        if dedup_key in existing:
            continue

        if p["type"] == "routing_correction":
            entry = f"\n{len(actionable_lines) + len(new_entries) + 1}. **Routing fix ({p['task_id']})**: missing={p.get('missing', [])}, unexpected={p.get('unexpected', [])}. Update tie-break rules.\n"
        else:
            entry = f"\n{len(actionable_lines) + len(new_entries) + 1}. **Quality gap ({p['task_id']})**: scored {p.get('score', '?')} ({p.get('verdict', '?')}). Review reference depth.\n"

        new_entries.append(entry)

    if new_entries:
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            for entry in new_entries:
                f.write(entry)

    return len(new_entries)


def append_routing_corrections(patterns: list[dict]) -> int:
    """Append routing corrections to routing-corrections.jsonl."""
    corrections = [p for p in patterns if p["type"] == "routing_correction"]
    if not corrections:
        return 0

    with open(ROUTING_CORRECTIONS_FILE, "a", encoding="utf-8") as f:
        for c in corrections:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    return len(corrections)


def main() -> int:
    parser = argparse.ArgumentParser(description="Append learned patterns from eval report")
    parser.add_argument("--report", required=True, help="Path to eval report JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print patterns without appending")
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        print(f"ERROR: report not found: {report_path}")
        return 1

    report = load_report(report_path)
    patterns = extract_patterns(report)

    if args.dry_run:
        print(f"Found {len(patterns)} patterns:")
        for p in patterns:
            print(f"  [{p['type']}] {p['summary']}")
        return 0

    n_memory = append_to_memory(patterns)
    n_routing = append_routing_corrections(patterns)

    print(f"Appended {n_memory} entries to memory/learned-patterns.md")
    print(f"Appended {n_routing} entries to memory/routing-corrections.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
