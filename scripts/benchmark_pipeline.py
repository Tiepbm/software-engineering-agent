#!/usr/bin/env python3
"""File-based benchmark pipeline for CE7 banking/insurance evaluations.

Workflow:
1. prepare: generate model prompt files from benchmark JSONL.
2. score: read saved model outputs and compute deterministic routing/reference/token scores.
3. evaluator-prompts: generate skill-evaluator prompts for semantic scoring.

The script is stdlib-only and does not call any model API. You can run GPT/Claude in
whatever UI/API you use, save outputs to the expected paths, then score locally.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENCHMARK = ROOT / "evals" / "banking-insurance-benchmark.jsonl"
DEFAULT_RUNS_DIR = ROOT / "runs"
DEFAULT_MODELS = ["gpt", "claude"]
REPORTS_DIR = ROOT / "reports"
LATEST_REPORT_EN = REPORTS_DIR / "latest-skill-eval.md"
LATEST_REPORT_VI = REPORTS_DIR / "latest-skill-eval.vi-VN.md"
HISTORY_PATH = REPORTS_DIR / "skill-eval-history.jsonl"
DEFAULT_PROVIDER_MODELS = {
    "gpt": "gpt-4.1",
    "claude": "claude-sonnet-4-20250514",
}
SUPPORTED_PROVIDERS = ["gpt", "claude"]
OUTPUT_STUB_MARKER = "<!-- CE7_OUTPUT_PENDING -->"
PACKS = [
    "core-engineering-pack",
    "data-database-analytics-pack",
    "security-access-pack",
    "platform-integration-pack",
    "resilience-performance-pack",
    "observability-release-pack",
    "storage-search-stack-pack",
]
REFERENCES = [
    "requirements-analysis",
    "solution-architecture",
    "system-design",
    "api-design",
    "testing-strategy",
    "code-review-and-refactoring",
    "data-modeling",
    "database-architecture",
    "sql-and-query-optimization",
    "database-reliability-and-operations",
    "data-engineering-and-pipelines",
    "analytics-and-warehouse-design",
    "security-review",
    "authn-authz-and-secrets",
    "messaging-and-eventing",
    "api-gateway-and-service-integration",
    "rate-limiting-and-traffic-control",
    "workflow-and-job-orchestration",
    "background-jobs-and-batch-processing",
    "resilience-and-fault-tolerance",
    "caching-and-distributed-state",
    "performance-engineering",
    "logging-metrics-and-tracing",
    "monitoring-alerting-and-slos",
    "observability-and-sre",
    "devops-and-release",
    "file-and-object-storage",
    "search-and-indexing",
    "dotnet-development",
    "java-spring-boot-development",
    "reactjs-development",
    "angular-development",
    "react-native-development",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON in {path}:{line_no}: {exc}") from exc
    return rows


def run_dir(run_id: str, runs_dir: Path = DEFAULT_RUNS_DIR) -> Path:
    return runs_dir / run_id


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def split_csvish(value: str) -> list[str]:
    cleaned = value.replace("`", "").replace("[", "").replace("]", "")
    parts = re.split(r"[,;\n]|\s+and\s+|\s+và\s+", cleaned, flags=re.IGNORECASE)
    return [p.strip(" -*\t\r") for p in parts if p.strip(" -*\t\r")]


def parse_models_csv(value: str) -> list[str]:
    models = [item.strip().lower() for item in value.split(",") if item.strip()]
    if not models:
        raise SystemExit("No models provided.")
    seen: set[str] = set()
    deduped: list[str] = []
    for model in models:
        if model not in SUPPORTED_PROVIDERS:
            raise SystemExit(f"Unsupported model label '{model}'. Supported: {', '.join(SUPPORTED_PROVIDERS)}")
        if model not in seen:
            seen.add(model)
            deduped.append(model)
    return deduped


def output_stub_text(prompt_path: Path) -> str:
    return (
        f"{OUTPUT_STUB_MARKER}\n"
        "<!-- Replace this file with the full model output after running the prompt in chat. -->\n"
        f"<!-- Prompt source: {rel(prompt_path)} -->\n\n"
        "- Packs selected: <comma-separated pack names>\n"
        "- References selected: <comma-separated reference names>\n"
        "- Why these packs/references are sufficient: <short reason>\n\n"
        "<!-- Paste full model answer below and remove the pending marker above. -->\n"
    )


def build_manual_worklist(target: Path, models: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# CE7 Manual Worklist",
        "",
        f"**Run ID:** `{target.name}`",
        f"**Created:** {datetime.now(timezone.utc).isoformat()}",
        "",
        "Use this checklist while running prompts in Copilot/Chat windows and pasting outputs into files.",
        "",
        "Prompts are shared across models — same input, different output files per model.",
        "",
        "| Model | Prompt ID | Prompt file (shared) | Output file |",
        "|---|---|---|---|",
    ]
    for model in models:
        for row in rows:
            prompt_path = target / "prompts" / f"{row['id']}.md"
            output_path = target / "outputs" / model / f"{row['id']}.md"
            lines.append(
                f"| `{model}` | `{row['id']}` | `{rel(prompt_path)}` | `{rel(output_path)}` |"
            )
    lines.extend([
        "",
        "After you fill outputs, run:",
        "",
        "```bash",
        f"python3 scripts/benchmark_pipeline.py finalize --run-id {target.name} --models {','.join(models)}",
        "```",
    ])
    return "\n".join(lines) + "\n"


def build_manual_readme(target: Path, models: list[str]) -> str:
    return "\n".join(
        [
            "# Manual Benchmark Execution (No API)",
            "",
            f"Run ID: `{target.name}`",
            f"Models: {', '.join(f'`{m}`' for m in models)}",
            "",
            "## Steps",
            "",
            "1. Open shared prompts under `prompts/<prompt_id>.md` in your IDE.",
            "2. For each prompt, run it in each model's chat window.",
            "3. Paste the model answer into `outputs/<model>/<prompt_id>.md`.",
            "4. Remove the pending marker line `<!-- CE7_OUTPUT_PENDING -->` from each completed output file.",
            "5. Run finalize to score and generate evaluator prompts.",
            "",
            "## Finalize command",
            "",
            "```bash",
            f"python3 scripts/benchmark_pipeline.py finalize --run-id {target.name} --models {','.join(models)}",
            "```",
            "",
        ]
    )


def extract_declared_items(text: str, label_patterns: list[str], known_items: list[str]) -> list[str]:
    found: list[str] = []
    lower_known = {item.lower(): item for item in known_items}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for pattern in label_patterns:
            if re.search(pattern, line, flags=re.IGNORECASE):
                after = re.split(pattern, line, flags=re.IGNORECASE, maxsplit=1)[-1]
                candidates = split_csvish(after)
                # Also read short bullet/list lines immediately after an empty label.
                if not candidates and i + 1 < len(lines):
                    for next_line in lines[i + 1 : i + 8]:
                        if re.search(r"(references selected|assumptions|why these|business prompt)", next_line, flags=re.IGNORECASE):
                            break
                        candidates.extend(split_csvish(next_line))
                for candidate in candidates:
                    normalized = candidate.lower().strip()
                    if normalized in lower_known and lower_known[normalized] not in found:
                        found.append(lower_known[normalized])
    return found


def scan_known_items(text: str, known_items: list[str]) -> list[str]:
    found = []
    for item in known_items:
        if re.search(rf"(?<![a-z0-9-]){re.escape(item)}(?![a-z0-9-])", text, flags=re.IGNORECASE):
            found.append(item)
    return found


def extract_actuals(output: str) -> tuple[list[str], list[str], str]:
    packs = extract_declared_items(output, [r"\*\*?packs selected\*\*?\s*:?", r"packs selected\s*:", r"pack[s]?\s*:\s*"], PACKS)
    refs = extract_declared_items(output, [r"\*\*?references selected\*\*?\s*:?", r"references selected\s*:", r"reference[s]?\s*:\s*"], REFERENCES)
    source = "declared"
    if not packs:
        packs = scan_known_items(output, PACKS)
        source = "scanned" if packs else "missing"
    if not refs:
        refs = scan_known_items(output, REFERENCES)
        if source == "declared":
            source = "mixed"
        elif refs:
            source = "scanned"
    return packs, refs, source


def list_diff(expected: list[str], actual: list[str]) -> tuple[list[str], list[str], list[str]]:
    expected_set = set(expected)
    actual_set = set(actual)
    missing = sorted(expected_set - actual_set)
    unexpected = sorted(actual_set - expected_set)
    hits = sorted(expected_set & actual_set)
    return missing, unexpected, hits


def score_selection(expected: list[str], actual: list[str], prohibited: list[str] | None = None) -> int:
    prohibited = prohibited or []
    if not expected and not actual:
        return 5
    if not expected and actual:
        base = 1
    else:
        expected_set = set(expected)
        actual_set = set(actual)
        hits = len(expected_set & actual_set)
        recall = hits / len(expected_set) if expected_set else 1.0
        precision = hits / len(actual_set) if actual_set else 0.0
        base = round(5 * ((0.7 * recall) + (0.3 * precision)))
    prohibited_hits = len(set(prohibited) & set(actual))
    return max(0, min(5, base - prohibited_hits))


def token_score(word_count: int, pack_count: int, ref_count: int, expected_ref_count: int) -> int:
    score = 5
    if ref_count > max(expected_ref_count + 2, 4):
        score -= 1
    if pack_count > 6:
        score -= 1
    if word_count > 1800:
        score -= 1
    if word_count > 2800:
        score -= 1
    if word_count < 120:
        score -= 1
    return max(0, score)


def verdict(score: int | float) -> str:
    if score >= 80:
        return "PASS"
    if score >= 60:
        return "WARN"
    return "FAIL"


def count_values(items: list[str]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))


def top_counts(items: list[str], limit: int = 5) -> list[dict[str, Any]]:
    return [{"name": name, "count": count} for name, count in count_values(items)[:limit]]


def format_hotspots(items: list[dict[str, Any]]) -> str:
    if not items:
        return "-"
    return ", ".join(f"`{item['name']}` x{item['count']}" for item in items)


def summarize_result_issue(result: dict[str, Any]) -> str:
    issues: list[str] = []
    if result["missing_packs"]:
        issues.append(f"missing packs: {', '.join(result['missing_packs'])}")
    if result["missing_references"]:
        issues.append(f"missing refs: {', '.join(result['missing_references'])}")
    unexpected = sorted(set(result["unexpected_packs"] + result["unexpected_references"] + result["prohibited_activations"]))
    if unexpected:
        issues.append(f"unexpected/prohibited: {', '.join(unexpected)}")
    if result["extraction_source"] == "missing":
        issues.append("missing standard packs/references header")
    elif result["extraction_source"] == "scanned":
        issues.append("header missing; parser used body scan")
    if result["token_notes"]["answer_length"] in {"long", "bloated"}:
        issues.append(f"answer too {result['token_notes']['answer_length']}")
    return "; ".join(issues[:3]) or "no major deterministic issue"


def build_model_summary(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    models = sorted({result["model"] for result in results})
    summaries: list[dict[str, Any]] = []
    for model in models:
        subset = [result for result in results if result["model"] == model]
        summaries.append(
            {
                "model": model,
                "outputs_scored": len(subset),
                "average_deterministic_score": round(sum(item["deterministic_score"] for item in subset) / len(subset), 1),
                "pass": sum(1 for item in subset if item["deterministic_verdict"] == "PASS"),
                "warn": sum(1 for item in subset if item["deterministic_verdict"] == "WARN"),
                "fail": sum(1 for item in subset if item["deterministic_verdict"] == "FAIL"),
                "average_word_count": round(sum(item["token_notes"]["word_count"] for item in subset) / len(subset), 1),
            }
        )
    return summaries


def build_run_report(target: Path, benchmark_path: Path, results: list[dict[str, Any]]) -> dict[str, Any]:
    generated_at = datetime.now(timezone.utc).isoformat()
    average_score = round(sum(result["deterministic_score"] for result in results) / len(results), 1)
    pass_count = sum(1 for result in results if result["deterministic_verdict"] == "PASS")
    warn_count = sum(1 for result in results if result["deterministic_verdict"] == "WARN")
    fail_count = sum(1 for result in results if result["deterministic_verdict"] == "FAIL")

    missing_pack_items = [item for result in results for item in result["missing_packs"]]
    missing_reference_items = [item for result in results for item in result["missing_references"]]
    unexpected_activation_items = [
        item
        for result in results
        for item in (result["unexpected_packs"] + result["unexpected_references"] + result["prohibited_activations"])
    ]
    scanned_outputs = sum(1 for result in results if result["extraction_source"] == "scanned")
    missing_header_outputs = sum(1 for result in results if result["extraction_source"] == "missing")
    long_outputs = sum(1 for result in results if result["token_notes"]["answer_length"] in {"long", "bloated"})
    bloated_outputs = sum(1 for result in results if result["token_notes"]["answer_length"] == "bloated")

    lowest_scores = sorted(
        results,
        key=lambda result: (
            result["deterministic_score"],
            len(result["missing_packs"]) + len(result["missing_references"]) + len(result["prohibited_activations"]),
            result["token_notes"]["word_count"],
            result["model"],
            result["prompt_id"],
        ),
    )[:5]

    likely_update_targets: list[dict[str, str]] = []
    if missing_pack_items:
        likely_update_targets.append(
            {
                "target": "agents/ce7-software-engineering.agent.md or .github/copilot-instructions.md",
                "reason": f"Missing expected packs in {sum(1 for result in results if result['missing_packs'])} output(s).",
                "evidence": format_hotspots(top_counts(missing_pack_items)),
            }
        )
    if missing_reference_items:
        likely_update_targets.append(
            {
                "target": "skills/<pack>/SKILL.md",
                "reason": f"Missing expected references in {sum(1 for result in results if result['missing_references'])} output(s).",
                "evidence": format_hotspots(top_counts(missing_reference_items)),
            }
        )
    if unexpected_activation_items:
        likely_update_targets.append(
            {
                "target": "pack trigger rules / negative activation guidance",
                "reason": f"Unexpected or prohibited activations appeared in {sum(1 for result in results if result['unexpected_packs'] or result['unexpected_references'] or result['prohibited_activations'])} output(s).",
                "evidence": format_hotspots(top_counts(unexpected_activation_items)),
            }
        )
    if scanned_outputs or missing_header_outputs:
        likely_update_targets.append(
            {
                "target": "benchmark output contract / prompt wrapper",
                "reason": "Some outputs did not use the standard Packs/References header, reducing parser confidence.",
                "evidence": f"scanned={scanned_outputs}, missing={missing_header_outputs}",
            }
        )
    if long_outputs:
        likely_update_targets.append(
            {
                "target": "token budget rules in packs or evaluator guidance",
                "reason": f"Long or bloated answers appeared in {long_outputs} output(s).",
                "evidence": f"bloated={bloated_outputs}",
            }
        )

    return {
        "timestamp": generated_at,
        "run_id": target.name,
        "benchmark": rel(benchmark_path),
        "outputs_scored": len(results),
        "models": sorted({result["model"] for result in results}),
        "semantic_status": "pending_skill_evaluator",
        "deterministic": {
            "average_score": average_score,
            "pass": pass_count,
            "warn": warn_count,
            "fail": fail_count,
        },
        "per_model": build_model_summary(results),
        "issue_counts": {
            "missing_pack_outputs": sum(1 for result in results if result["missing_packs"]),
            "missing_reference_outputs": sum(1 for result in results if result["missing_references"]),
            "unexpected_activation_outputs": sum(
                1 for result in results if result["unexpected_packs"] or result["unexpected_references"] or result["prohibited_activations"]
            ),
            "prohibited_activation_outputs": sum(1 for result in results if result["prohibited_activations"]),
            "long_outputs": long_outputs,
            "bloated_outputs": bloated_outputs,
            "scanned_outputs": scanned_outputs,
            "missing_header_outputs": missing_header_outputs,
        },
        "hotspots": {
            "missing_packs": top_counts(missing_pack_items),
            "missing_references": top_counts(missing_reference_items),
            "unexpected_activations": top_counts(unexpected_activation_items),
        },
        "lowest_scoring_cases": [
            {
                "model": result["model"],
                "prompt_id": result["prompt_id"],
                "deterministic_score": result["deterministic_score"],
                "verdict": result["deterministic_verdict"],
                "main_issue": summarize_result_issue(result),
            }
            for result in lowest_scores
        ],
        "likely_update_targets": likely_update_targets,
        "artifacts": {
            "run_dir": rel(target),
            "summary_md": rel(target / "summary.md"),
            "report_json": rel(target / "report.json"),
            "scores_json": rel(target / "scores.json"),
            "scores_jsonl": rel(target / "scores.jsonl"),
            "evaluator_prompts_dir": rel(target / "evaluator-prompts"),
        },
    }


def deterministic_score(row: dict[str, Any], output: str, model: str, run_id: str) -> dict[str, Any]:
    actual_packs, actual_refs, extraction_source = extract_actuals(output)
    missing_packs, unexpected_packs, hit_packs = list_diff(row.get("expected_packs", []), actual_packs)
    missing_refs, unexpected_refs, hit_refs = list_diff(row.get("expected_references", []), actual_refs)
    prohibited = row.get("should_not_activate", [])
    prohibited_activations = sorted(set(prohibited) & (set(actual_packs) | set(actual_refs)))
    trigger_accuracy = score_selection(row.get("expected_packs", []), actual_packs, prohibited)
    reference_precision = score_selection(row.get("expected_references", []), actual_refs, prohibited)
    words = len(re.findall(r"\S+", output))
    token_efficiency = token_score(words, len(actual_packs), len(actual_refs), len(row.get("expected_references", [])))
    # Deterministic score only covers dimensions that can be checked without semantic judgment.
    deterministic_pct = round(((trigger_accuracy * 20) + (reference_precision * 15) + (token_efficiency * 10)) / 45 * 20)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "prompt_id": row["id"],
        "domain": row.get("domain"),
        "model": model,
        "risk_class": row.get("risk_class"),
        "expected_packs": row.get("expected_packs", []),
        "actual_packs": actual_packs,
        "missing_packs": missing_packs,
        "unexpected_packs": unexpected_packs,
        "expected_references": row.get("expected_references", []),
        "actual_references": actual_refs,
        "missing_references": missing_refs,
        "unexpected_references": unexpected_refs,
        "should_not_activate": prohibited,
        "prohibited_activations": prohibited_activations,
        "scores": {
            "trigger_accuracy": trigger_accuracy,
            "reference_precision": reference_precision,
            "token_efficiency": token_efficiency,
            "semantic_dimensions": "pending_skill_evaluator",
        },
        "deterministic_score": deterministic_pct,
        "deterministic_verdict": verdict(deterministic_pct),
        "token_notes": {
            "word_count": words,
            "approx_tokens": round(words * 1.35),
            "opened_pack_count": len(actual_packs),
            "opened_reference_count": len(actual_refs),
            "answer_length": "bloated" if words > 2800 else "long" if words > 1800 else "medium" if words > 500 else "short",
        },
        "extraction_source": extraction_source,
        "scoring_notes": row.get("scoring_notes"),
    }


def prompt_wrapper(row: dict[str, Any]) -> str:
    return f"""Act as CE7 Software Engineering Agent.
Use the Copilot-first hybrid pack architecture.
Before answering, state exactly:
- Packs selected: <comma-separated pack names>
- References selected: <comma-separated reference names>
- Why these packs/references are sufficient: <short reason>

Do not load more than 3 references unless required by production risk. If you need more than 3 references, explain why.
Then answer the business prompt with principal-level engineering guidance.

Benchmark metadata:
- Prompt ID: {row['id']}
- Domain: {row.get('domain')}
- Risk class: {row.get('risk_class')}
- Business context: {row.get('business_context')}

Business prompt:
{row['prompt']}
"""


def prepare(args: argparse.Namespace) -> int:
    benchmark = load_jsonl(Path(args.benchmark))
    models = parse_models_csv(args.models) if args.models else DEFAULT_MODELS
    target = run_dir(args.run_id, Path(args.runs_dir))
    prompts_dir = target / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    (target / "outputs").mkdir(parents=True, exist_ok=True)
    for model in models:
        (target / "outputs" / model).mkdir(parents=True, exist_ok=True)
    # Shared prompts — same prompt for all models
    for row in benchmark:
        prompt_path = prompts_dir / f"{row['id']}.md"
        prompt_path.write_text(prompt_wrapper(row), encoding="utf-8")
    # Backward compat: also create per-model symlink dirs if needed by older workflows
    for model in models:
        model_prompt_dir = prompts_dir / model
        if not model_prompt_dir.exists():
            model_prompt_dir.mkdir(parents=True, exist_ok=True)
            for row in benchmark:
                src = prompts_dir / f"{row['id']}.md"
                dst = model_prompt_dir / f"{row['id']}.md"
                if not dst.exists():
                    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    manifest = {
        "run_id": args.run_id,
        "benchmark": str(Path(args.benchmark).relative_to(ROOT) if Path(args.benchmark).is_absolute() else args.benchmark),
        "models": models,
        "prompt_count": len(benchmark),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "prompt_layout": "shared",
        "output_contract": "Save model outputs to runs/<run_id>/outputs/<model>/<prompt_id>.md",
    }
    (target / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Prepared {len(benchmark)} shared prompts for {len(models)} model(s) in {target.relative_to(ROOT)}")
    print(f"Prompts: {target.relative_to(ROOT)}/prompts/<prompt_id>.md")
    print(f"Save outputs under: {target.relative_to(ROOT)}/outputs/<model>/<prompt_id>.md")
    return 0


def implement(args: argparse.Namespace) -> int:
    models = parse_models_csv(args.models) if args.models else DEFAULT_MODELS
    prepare_args = argparse.Namespace(
        run_id=args.run_id,
        benchmark=args.benchmark,
        runs_dir=args.runs_dir,
        models=",".join(models),
    )
    prepare(prepare_args)

    benchmark = load_jsonl(Path(args.benchmark))
    target = run_dir(args.run_id, Path(args.runs_dir))
    created_stubs = 0
    for model in models:
        for row in benchmark:
            prompt_path = target / "prompts" / f"{row['id']}.md"
            output_path = target / "outputs" / model / f"{row['id']}.md"
            if output_path.exists() and not args.overwrite_stubs:
                continue
            output_path.write_text(output_stub_text(prompt_path), encoding="utf-8")
            created_stubs += 1

    manual_dir = target / "manual"
    manual_dir.mkdir(parents=True, exist_ok=True)
    (manual_dir / "README.md").write_text(build_manual_readme(target, models), encoding="utf-8")
    (manual_dir / "worklist.md").write_text(build_manual_worklist(target, models, benchmark), encoding="utf-8")

    print(f"Prepared manual run in {rel(target)}")
    print(f"- models: {', '.join(models)}")
    print(f"- shared prompts: {len(benchmark)}")
    print(f"- output stubs written: {created_stubs}")
    print(f"- manual guide: {rel(manual_dir / 'README.md')}")
    print(f"- worklist: {rel(manual_dir / 'worklist.md')}")
    print(f"Next: fill output files, then run `python3 scripts/benchmark_pipeline.py finalize --run-id {args.run_id} --models {','.join(models)}`")
    return 0


def finalize(args: argparse.Namespace) -> int:
    models = parse_models_csv(args.models) if args.models else DEFAULT_MODELS
    benchmark = load_jsonl(Path(args.benchmark))
    target = run_dir(args.run_id, Path(args.runs_dir))

    missing: list[str] = []
    pending: list[str] = []
    for model in models:
        for row in benchmark:
            output_path = target / "outputs" / model / f"{row['id']}.md"
            if not output_path.exists():
                missing.append(rel(output_path))
                continue
            text = output_path.read_text(encoding="utf-8").strip()
            if not text:
                pending.append(rel(output_path))
                continue
            if OUTPUT_STUB_MARKER in text:
                pending.append(rel(output_path))

    if (missing or pending) and not args.allow_partial:
        print("Finalize blocked: some outputs are missing or still pending stubs.")
        if missing:
            print("Missing output files:")
            for item in missing[:20]:
                print(f"- {item}")
            if len(missing) > 20:
                print(f"- ... and {len(missing) - 20} more")
        if pending:
            print("Pending output files (empty or still contains CE7_OUTPUT_PENDING):")
            for item in pending[:20]:
                print(f"- {item}")
            if len(pending) > 20:
                print(f"- ... and {len(pending) - 20} more")
        print("If you intentionally want partial scoring, rerun with --allow-partial.")
        return 2

    score_args = argparse.Namespace(
        run_id=args.run_id,
        benchmark=args.benchmark,
        runs_dir=args.runs_dir,
        append_history=True,
    )
    score(score_args)

    eval_args = argparse.Namespace(
        run_id=args.run_id,
        benchmark=args.benchmark,
        runs_dir=args.runs_dir,
    )
    evaluator_prompts(eval_args)
    return 0


def score(args: argparse.Namespace) -> int:
    benchmark_path = Path(args.benchmark)
    benchmark_rows = {row["id"]: row for row in load_jsonl(benchmark_path)}
    target = run_dir(args.run_id, Path(args.runs_dir))
    outputs_dir = target / "outputs"
    if not outputs_dir.exists():
        raise SystemExit(f"Missing outputs directory: {outputs_dir}")
    results: list[dict[str, Any]] = []
    for model_dir in sorted(p for p in outputs_dir.iterdir() if p.is_dir()):
        model = model_dir.name
        for output_path in sorted(model_dir.glob("*.md")):
            prompt_id = output_path.stem
            if prompt_id not in benchmark_rows:
                print(f"WARN: skipping unknown output {output_path.relative_to(ROOT)}", file=sys.stderr)
                continue
            output = output_path.read_text(encoding="utf-8")
            if OUTPUT_STUB_MARKER in output:
                print(f"WARN: skipping pending output stub {output_path.relative_to(ROOT)}", file=sys.stderr)
                continue
            results.append(deterministic_score(benchmark_rows[prompt_id], output, model, args.run_id))
    if not results:
        raise SystemExit(f"No model outputs found in {outputs_dir}")
    (target / "scores.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    score_jsonl = "\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n"
    (target / "scores.jsonl").write_text(score_jsonl, encoding="utf-8")
    run_report = build_run_report(target, benchmark_path, results)
    (target / "report.json").write_text(json.dumps(run_report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary(target, run_report, results)
    if args.append_history:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        write_latest_report(run_report)
        with HISTORY_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(run_report, ensure_ascii=False) + "\n")
    print(
        f"Scored {len(results)} output(s). See {target.relative_to(ROOT)}/summary.md and report.json"
        + (", plus reports/latest-skill-eval.md" if args.append_history else "")
    )
    return 0


def write_summary(target: Path, run_report: dict[str, Any], results: list[dict[str, Any]]) -> None:
    lines = [
        "# Benchmark Run Summary",
        "",
        f"**Run ID:** `{target.name}`  ",
        f"**Generated:** {run_report['timestamp']}  ",
        f"**Benchmark:** `{run_report['benchmark']}`  ",
        "**Score type:** deterministic routing/reference/token only; semantic scoring still requires `skill-evaluator`.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Outputs scored | {run_report['outputs_scored']} |",
        f"| Average deterministic score | {run_report['deterministic']['average_score']} |",
        f"| PASS | {run_report['deterministic']['pass']} |",
        f"| WARN | {run_report['deterministic']['warn']} |",
        f"| FAIL | {run_report['deterministic']['fail']} |",
        "",
        "## Model Scorecard",
        "",
        "| Model | Outputs | Avg score | PASS | WARN | FAIL | Avg words |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in run_report["per_model"]:
        lines.append(
            f"| {item['model']} | {item['outputs_scored']} | {item['average_deterministic_score']} | {item['pass']} | {item['warn']} | {item['fail']} | {item['average_word_count']} |"
        )
    lines.extend([
        "",
        "## Highest-Signal Findings",
        "",
        f"- Missing expected packs: {run_report['issue_counts']['missing_pack_outputs']} output(s). Hotspots: {format_hotspots(run_report['hotspots']['missing_packs'])}",
        f"- Missing expected references: {run_report['issue_counts']['missing_reference_outputs']} output(s). Hotspots: {format_hotspots(run_report['hotspots']['missing_references'])}",
        f"- Unexpected/prohibited activations: {run_report['issue_counts']['unexpected_activation_outputs']} output(s). Hotspots: {format_hotspots(run_report['hotspots']['unexpected_activations'])}",
        f"- Parser confidence issues: scanned={run_report['issue_counts']['scanned_outputs']}, missing header={run_report['issue_counts']['missing_header_outputs']}",
        f"- Long answers: {run_report['issue_counts']['long_outputs']} output(s); bloated answers: {run_report['issue_counts']['bloated_outputs']} output(s)",
        "",
        "## Lowest-Scoring Cases",
        "",
        "| Model | Prompt | Score | Verdict | Main issue |",
        "|---|---|---:|---|---|",
    ])
    for item in run_report["lowest_scoring_cases"]:
        lines.append(
            f"| {item['model']} | {item['prompt_id']} | {item['deterministic_score']} | {item['verdict']} | {item['main_issue']} |"
        )
    lines.extend([
        "",
        "## Full Deterministic Results",
        "",
        "| Model | Prompt | Score | Verdict | Missing packs | Missing refs | Unexpected/prohibited | Words |",
        "|---|---|---:|---|---|---|---|---:|",
    ])
    for r in sorted(results, key=lambda item: (item["model"], item["prompt_id"])):
        unexpected = sorted(set(r["unexpected_packs"] + r["unexpected_references"] + r["prohibited_activations"]))
        lines.append(
            f"| {r['model']} | {r['prompt_id']} | {r['deterministic_score']} | {r['deterministic_verdict']} | "
            f"{', '.join(r['missing_packs']) or '-'} | {', '.join(r['missing_references']) or '-'} | "
            f"{', '.join(unexpected) or '-'} | {r['token_notes']['word_count']} |"
        )
    lines.extend([
        "",
        "## Likely Update Targets",
        "",
        "| Target | Why | Evidence |",
        "|---|---|---|",
    ])
    if run_report["likely_update_targets"]:
        for item in run_report["likely_update_targets"]:
            lines.append(f"| `{item['target']}` | {item['reason']} | {item['evidence']} |")
    else:
        lines.append("| - | No strong deterministic update target from this run. | - |")
    lines.extend([
        "",
        "## Artifacts",
        "",
        f"- Run report: `{run_report['artifacts']['report_json']}`",
        f"- Deterministic scores: `{run_report['artifacts']['scores_json']}` and `{run_report['artifacts']['scores_jsonl']}`",
        f"- Evaluator prompts directory: `{run_report['artifacts']['evaluator_prompts_dir']}`",
        "",
        "## Next Step",
        "",
        "Run:",
        "",
        "```bash",
        f"python3 scripts/benchmark_pipeline.py evaluator-prompts --run-id {target.name}",
        "```",
        "",
        "Then submit generated prompts under `evaluator-prompts/` to `skill-evaluator` for semantic scoring.",
    ])
    (target / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_latest_report(run_report: dict[str, Any]) -> None:
    LATEST_REPORT_EN.write_text(render_latest_report(run_report, language="en"), encoding="utf-8")
    LATEST_REPORT_VI.write_text(render_latest_report(run_report, language="vi"), encoding="utf-8")


def render_latest_report(run_report: dict[str, Any], language: str) -> str:
    if language == "vi":
        lines = [
            "# Báo cáo CE7 mới nhất",
            "",
            "[English](latest-skill-eval.md) | [Tiếng Việt](latest-skill-eval.vi-VN.md)",
            "",
            "> **Bạn đang ở đâu?** Đây là snapshot **ngắn gọn ở mức run** mới nhất đã được đồng bộ vào `reports/`.",
            ">",
            "> - Chi tiết per-prompt nằm trong `runs/<run_id>/`.",
            "> - Lịch sử dài hạn nằm ở `reports/skill-eval-history.jsonl` với **1 dòng cho mỗi run**.",
            "> - File này không thay thế `summary.md`; nó chỉ giữ lại tín hiệu quan trọng nhất.",
            "",
            "## Snapshot hiện tại",
            "",
            f"- **Run ID:** `{run_report['run_id']}`",
            f"- **Generated:** {run_report['timestamp']}",
            f"- **Benchmark:** `{run_report['benchmark']}`",
            f"- **Models:** {', '.join(f'`{model}`' for model in run_report['models'])}",
            f"- **Outputs scored:** {run_report['outputs_scored']}",
            f"- **Semantic status:** `{run_report['semantic_status']}`",
            "",
            "## Deterministic scorecard",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Average deterministic score | {run_report['deterministic']['average_score']} |",
            f"| PASS | {run_report['deterministic']['pass']} |",
            f"| WARN | {run_report['deterministic']['warn']} |",
            f"| FAIL | {run_report['deterministic']['fail']} |",
            "",
            "## Scorecard theo model",
            "",
            "| Model | Outputs | Avg score | PASS | WARN | FAIL | Avg words |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
        for item in run_report["per_model"]:
            lines.append(
                f"| {item['model']} | {item['outputs_scored']} | {item['average_deterministic_score']} | {item['pass']} | {item['warn']} | {item['fail']} | {item['average_word_count']} |"
            )
        lines.extend([
            "",
            "## Tín hiệu quan trọng nhất",
            "",
            f"- Thiếu expected packs: {run_report['issue_counts']['missing_pack_outputs']} output(s). Hotspots: {format_hotspots(run_report['hotspots']['missing_packs'])}",
            f"- Thiếu expected references: {run_report['issue_counts']['missing_reference_outputs']} output(s). Hotspots: {format_hotspots(run_report['hotspots']['missing_references'])}",
            f"- Unexpected/prohibited activations: {run_report['issue_counts']['unexpected_activation_outputs']} output(s). Hotspots: {format_hotspots(run_report['hotspots']['unexpected_activations'])}",
            f"- Output thiếu header chuẩn hoặc parser phải fallback: scanned={run_report['issue_counts']['scanned_outputs']}, missing={run_report['issue_counts']['missing_header_outputs']}",
            f"- Output dài: {run_report['issue_counts']['long_outputs']} | bloated: {run_report['issue_counts']['bloated_outputs']}",
            "",
            "## Target nên sửa tiếp",
            "",
            "| Target | Lý do | Evidence |",
            "|---|---|---|",
        ])
        if run_report["likely_update_targets"]:
            for item in run_report["likely_update_targets"]:
                lines.append(f"| `{item['target']}` | {item['reason']} | {item['evidence']} |")
        else:
            lines.append("| - | Không có deterministic signal đủ mạnh để đề xuất chỉnh sửa. | - |")
        lines.extend([
            "",
            "## Cases thấp điểm nhất",
            "",
            "| Model | Prompt | Score | Verdict | Main issue |",
            "|---|---|---:|---|---|",
        ])
        for item in run_report["lowest_scoring_cases"]:
            lines.append(
                f"| {item['model']} | {item['prompt_id']} | {item['deterministic_score']} | {item['verdict']} | {item['main_issue']} |"
            )
        lines.extend([
            "",
            "## Artifacts",
            "",
            f"- `runs/<run_id>/report.json`: `{run_report['artifacts']['report_json']}`",
            f"- `runs/<run_id>/summary.md`: `{run_report['artifacts']['summary_md']}`",
            f"- `runs/<run_id>/scores.jsonl`: `{run_report['artifacts']['scores_jsonl']}`",
            f"- `runs/<run_id>/evaluator-prompts/`: `{run_report['artifacts']['evaluator_prompts_dir']}`",
            f"- Lịch sử toàn cục: `{rel(HISTORY_PATH)}`",
            "",
            "## Quy tắc sử dụng report này",
            "",
            "- Không chép toàn bộ prompt-level findings vào đây; giữ chúng ở `runs/<run_id>/`.",
            "- Chỉ xem đây là snapshot gần nhất; dùng `skill-eval-history.jsonl` để xem xu hướng hoặc regression.",
            "- Sau semantic evaluation, nên ghi bổ sung findings ở run folder hoặc tạo artifact semantic riêng thay vì làm file này quá dài.",
            "",
        ])
        return "\n".join(lines) + "\n"

    lines = [
        "# Latest CE7 Skill Evaluation Snapshot",
        "",
        "[English](latest-skill-eval.md) | [Tiếng Việt](latest-skill-eval.vi-VN.md)",
        "",
        "> **You are here.** This is the latest **short run-level snapshot** synced into `reports/`.",
        ">",
        "> - Per-prompt details stay under `runs/<run_id>/`.",
        "> - Long-term history stays in `reports/skill-eval-history.jsonl` with **one row per run**.",
        "> - This file does not replace `summary.md`; it only keeps the highest-signal findings.",
        "",
        "## Current snapshot",
        "",
        f"- **Run ID:** `{run_report['run_id']}`",
        f"- **Generated:** {run_report['timestamp']}",
        f"- **Benchmark:** `{run_report['benchmark']}`",
        f"- **Models:** {', '.join(f'`{model}`' for model in run_report['models'])}",
        f"- **Outputs scored:** {run_report['outputs_scored']}",
        f"- **Semantic status:** `{run_report['semantic_status']}`",
        "",
        "## Deterministic scorecard",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Average deterministic score | {run_report['deterministic']['average_score']} |",
        f"| PASS | {run_report['deterministic']['pass']} |",
        f"| WARN | {run_report['deterministic']['warn']} |",
        f"| FAIL | {run_report['deterministic']['fail']} |",
        "",
        "## Model scorecard",
        "",
        "| Model | Outputs | Avg score | PASS | WARN | FAIL | Avg words |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in run_report["per_model"]:
        lines.append(
            f"| {item['model']} | {item['outputs_scored']} | {item['average_deterministic_score']} | {item['pass']} | {item['warn']} | {item['fail']} | {item['average_word_count']} |"
        )
    lines.extend([
        "",
        "## Highest-signal findings",
        "",
        f"- Missing expected packs: {run_report['issue_counts']['missing_pack_outputs']} output(s). Hotspots: {format_hotspots(run_report['hotspots']['missing_packs'])}",
        f"- Missing expected references: {run_report['issue_counts']['missing_reference_outputs']} output(s). Hotspots: {format_hotspots(run_report['hotspots']['missing_references'])}",
        f"- Unexpected/prohibited activations: {run_report['issue_counts']['unexpected_activation_outputs']} output(s). Hotspots: {format_hotspots(run_report['hotspots']['unexpected_activations'])}",
        f"- Header/parser confidence issues: scanned={run_report['issue_counts']['scanned_outputs']}, missing={run_report['issue_counts']['missing_header_outputs']}",
        f"- Long outputs: {run_report['issue_counts']['long_outputs']} | bloated outputs: {run_report['issue_counts']['bloated_outputs']}",
        "",
        "## Likely update targets",
        "",
        "| Target | Why | Evidence |",
        "|---|---|---|",
    ])
    if run_report["likely_update_targets"]:
        for item in run_report["likely_update_targets"]:
            lines.append(f"| `{item['target']}` | {item['reason']} | {item['evidence']} |")
    else:
        lines.append("| - | No strong deterministic signal suggests an update yet. | - |")
    lines.extend([
        "",
        "## Lowest-scoring cases",
        "",
        "| Model | Prompt | Score | Verdict | Main issue |",
        "|---|---|---:|---|---|",
    ])
    for item in run_report["lowest_scoring_cases"]:
        lines.append(
            f"| {item['model']} | {item['prompt_id']} | {item['deterministic_score']} | {item['verdict']} | {item['main_issue']} |"
        )
    lines.extend([
        "",
        "## Artifacts",
        "",
        f"- `runs/<run_id>/report.json`: `{run_report['artifacts']['report_json']}`",
        f"- `runs/<run_id>/summary.md`: `{run_report['artifacts']['summary_md']}`",
        f"- `runs/<run_id>/scores.jsonl`: `{run_report['artifacts']['scores_jsonl']}`",
        f"- `runs/<run_id>/evaluator-prompts/`: `{run_report['artifacts']['evaluator_prompts_dir']}`",
        f"- Global history: `{rel(HISTORY_PATH)}`",
        "",
        "## Rules for this report",
        "",
        "- Do not duplicate full prompt-level findings here; keep them in `runs/<run_id>/`.",
        "- Treat this as the latest snapshot only; use `skill-eval-history.jsonl` for trends and regression checks.",
        "- After semantic evaluation, add details to run-local artifacts or a semantic artifact instead of bloating this file.",
        "",
    ])
    return "\n".join(lines) + "\n"


def evaluator_prompt_text(row: dict[str, Any], result: dict[str, Any], output: str) -> str:
    return f"""Use `agents/skill-evaluator.agent.md` and `evals/scoring-rubric.md` to semantically evaluate this CE7 model output.

Return machine-readable JSON first, then a short markdown explanation.

Required JSON shape:
```json
{{
  "prompt_id": "{row['id']}",
  "model": "{result['model']}",
  "semantic_scores": {{
    "output_quality": 0,
    "evidence_validation": 0,
    "production_safety": 0,
    "copilot_readiness": 0,
    "maintainability_originality": 0
  }},
  "final_weighted_score": 0,
  "verdict": "PASS|WARN|FAIL",
  "main_gaps": [],
  "suggested_update_targets": []
}}
```

Benchmark expectation:
```json
{json.dumps(row, ensure_ascii=False, indent=2)}
```

Deterministic routing/reference/token score:
```json
{json.dumps(result, ensure_ascii=False, indent=2)}
```

Model output to evaluate:
```markdown
{output}
```
"""


def evaluator_prompts(args: argparse.Namespace) -> int:
    benchmark_rows = {row["id"]: row for row in load_jsonl(Path(args.benchmark))}
    target = run_dir(args.run_id, Path(args.runs_dir))
    scores_path = target / "scores.json"
    if not scores_path.exists():
        raise SystemExit(f"Missing scores.json. Run score first: {scores_path}")
    results = json.loads(scores_path.read_text(encoding="utf-8"))
    created = 0
    for result in results:
        row = benchmark_rows[result["prompt_id"]]
        output_path = target / "outputs" / result["model"] / f"{result['prompt_id']}.md"
        output = output_path.read_text(encoding="utf-8")
        out_dir = target / "evaluator-prompts" / result["model"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{result['prompt_id']}.md").write_text(evaluator_prompt_text(row, result, output), encoding="utf-8")
        created += 1
    print(f"Generated {created} evaluator prompt(s) under {target.relative_to(ROOT)}/evaluator-prompts")
    return 0


def normalize_openai_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts).strip()
    return ""


def http_post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout_sec: int = 120) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} calling {url}: {body[:1200]}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Network error calling {url}: {exc}") from exc


def call_gpt(prompt: str, model_name: str, temperature: float, max_output_tokens: int | None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY for provider 'gpt'.")
    payload: dict[str, Any] = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }
    if max_output_tokens is not None:
        payload["max_tokens"] = max_output_tokens
    response = http_post_json(
        "https://api.openai.com/v1/chat/completions",
        payload,
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise SystemExit(f"Unexpected OpenAI response shape: {json.dumps(response)[:1200]}") from exc
    text = normalize_openai_content(content)
    if not text.strip():
        raise SystemExit("OpenAI returned empty content.")
    return text.strip() + "\n"


def call_claude(prompt: str, model_name: str, temperature: float, max_output_tokens: int | None) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Missing ANTHROPIC_API_KEY for provider 'claude'.")
    payload: dict[str, Any] = {
        "model": model_name,
        "max_tokens": max_output_tokens if max_output_tokens is not None else 2200,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    response = http_post_json(
        "https://api.anthropic.com/v1/messages",
        payload,
        {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
    )
    try:
        chunks = response["content"]
    except KeyError as exc:
        raise SystemExit(f"Unexpected Anthropic response shape: {json.dumps(response)[:1200]}") from exc
    parts: list[str] = []
    if isinstance(chunks, list):
        for chunk in chunks:
            if isinstance(chunk, dict) and chunk.get("type") == "text" and isinstance(chunk.get("text"), str):
                parts.append(chunk["text"])
    text = "\n".join(parts).strip()
    if not text:
        raise SystemExit("Anthropic returned empty content.")
    return text + "\n"


def run_end_to_end(args: argparse.Namespace) -> int:
    model_label = args.model.lower().strip()
    if model_label not in SUPPORTED_PROVIDERS:
        raise SystemExit("--model must be one of: gpt, claude")

    if model_label == "gpt" and not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Missing OPENAI_API_KEY. Export it before running --model gpt.")
    if model_label == "claude" and not os.getenv("ANTHROPIC_API_KEY"):
        raise SystemExit("Missing ANTHROPIC_API_KEY. Export it before running --model claude.")

    prepare_args = argparse.Namespace(
        run_id=args.run_id,
        benchmark=args.benchmark,
        runs_dir=args.runs_dir,
        models=model_label,
    )
    prepare(prepare_args)

    target = run_dir(args.run_id, Path(args.runs_dir))
    # Shared prompts directory (same prompts for all models)
    model_prompt_dir = target / "prompts"
    # Fall back to per-model dir for backward compat with older runs
    if not any(model_prompt_dir.glob("*.md")):
        model_prompt_dir = target / "prompts" / model_label
    model_output_dir = target / "outputs" / model_label
    model_output_dir.mkdir(parents=True, exist_ok=True)

    prompt_paths = sorted(model_prompt_dir.glob("*.md"))
    if args.limit is not None:
        prompt_paths = prompt_paths[: args.limit]
    if not prompt_paths:
        raise SystemExit(f"No prompts found in {model_prompt_dir}")

    provider_model = args.provider_model or DEFAULT_PROVIDER_MODELS[model_label]
    for i, prompt_path in enumerate(prompt_paths, start=1):
        prompt_id = prompt_path.stem
        output_path = model_output_dir / f"{prompt_id}.md"
        if output_path.exists() and not args.overwrite:
            print(f"[{i}/{len(prompt_paths)}] Skip existing output: {rel(output_path)}")
            continue
        prompt_text = prompt_path.read_text(encoding="utf-8")
        print(f"[{i}/{len(prompt_paths)}] Running {model_label} for {prompt_id}...")
        if model_label == "gpt":
            output_text = call_gpt(prompt_text, provider_model, args.temperature, args.max_output_tokens)
        else:
            output_text = call_claude(prompt_text, provider_model, args.temperature, args.max_output_tokens)
        output_path.write_text(output_text, encoding="utf-8")

    score_args = argparse.Namespace(
        run_id=args.run_id,
        benchmark=args.benchmark,
        runs_dir=args.runs_dir,
        append_history=True,
    )
    score(score_args)

    eval_args = argparse.Namespace(
        run_id=args.run_id,
        benchmark=args.benchmark,
        runs_dir=args.runs_dir,
    )
    evaluator_prompts(eval_args)
    print(
        "Auto run complete. Artifacts: "
        f"{rel(target / 'summary.md')}, {rel(target / 'report.json')}, {rel(target / 'evaluator-prompts')}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="CE7 file-based benchmark pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--run-id", required=True, help="Run identifier, e.g. 2026-04-27-gpt-claude-v1")
        p.add_argument("--benchmark", default=str(DEFAULT_BENCHMARK), help="Benchmark JSONL path")
        p.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR), help="Runs output directory")

    p_prepare = sub.add_parser("prepare", help="Generate prompt files for models")
    add_common(p_prepare)
    p_prepare.add_argument("--models", default=",".join(DEFAULT_MODELS), help="Comma-separated model labels")
    p_prepare.set_defaults(func=prepare)

    p_score = sub.add_parser("score", help="Score saved model outputs deterministically")
    add_common(p_score)
    p_score.add_argument(
        "--append-history",
        action="store_true",
        help="Sync latest reports and append one run-level summary to reports/skill-eval-history.jsonl",
    )
    p_score.set_defaults(func=score)

    p_eval = sub.add_parser("evaluator-prompts", help="Generate prompts for skill-evaluator semantic scoring")
    add_common(p_eval)
    p_eval.set_defaults(func=evaluator_prompts)

    p_impl = sub.add_parser("implement", help="Prepare no-API manual run (prompts + output stubs + worklist)")
    add_common(p_impl)
    p_impl.add_argument("--models", default=",".join(DEFAULT_MODELS), help="Comma-separated model labels, e.g. gpt,claude")
    p_impl.add_argument("--overwrite-stubs", action="store_true", help="Overwrite existing output stub files")
    p_impl.set_defaults(func=implement)

    p_finalize = sub.add_parser("finalize", help="Finalize no-API run: validate outputs, score, sync reports, generate evaluator prompts")
    add_common(p_finalize)
    p_finalize.add_argument("--models", default=",".join(DEFAULT_MODELS), help="Comma-separated model labels expected in outputs")
    p_finalize.add_argument("--allow-partial", action="store_true", help="Allow scoring even if some outputs are missing/pending")
    p_finalize.set_defaults(func=finalize)

    p_run = sub.add_parser("run", help="Run end-to-end benchmark automatically for one provider (gpt or claude)")
    add_common(p_run)
    p_run.add_argument("--model", required=True, choices=SUPPORTED_PROVIDERS, help="Provider label to run")
    p_run.add_argument("--provider-model", default=None, help="Provider model name override")
    p_run.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature")
    p_run.add_argument("--max-output-tokens", type=int, default=2200, help="Max generated tokens per output")
    p_run.add_argument("--limit", type=int, default=None, help="Optional cap on prompt count for this run")
    p_run.add_argument("--overwrite", action="store_true", help="Overwrite existing output files")
    p_run.set_defaults(func=run_end_to_end)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

