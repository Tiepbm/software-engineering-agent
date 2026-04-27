#!/usr/bin/env python3
"""Validate the CE7 Copilot-first hybrid skill-pack layout."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "core-engineering-pack": [
        "requirements-analysis",
        "solution-architecture",
        "system-design",
        "api-design",
        "testing-strategy",
        "code-review-and-refactoring",
    ],
    "data-database-analytics-pack": [
        "data-modeling",
        "database-architecture",
        "sql-and-query-optimization",
        "database-reliability-and-operations",
        "data-engineering-and-pipelines",
        "analytics-and-warehouse-design",
    ],
    "security-access-pack": ["security-review", "authn-authz-and-secrets"],
    "platform-integration-pack": [
        "messaging-and-eventing",
        "api-gateway-and-service-integration",
        "rate-limiting-and-traffic-control",
        "workflow-and-job-orchestration",
        "background-jobs-and-batch-processing",
    ],
    "resilience-performance-pack": [
        "resilience-and-fault-tolerance",
        "caching-and-distributed-state",
        "performance-engineering",
    ],
    "observability-release-pack": [
        "logging-metrics-and-tracing",
        "monitoring-alerting-and-slos",
        "observability-and-sre",
        "devops-and-release",
    ],
    "storage-search-stack-pack": [
        "file-and-object-storage",
        "search-and-indexing",
        "dotnet-development",
        "java-spring-boot-development",
        "reactjs-development",
        "angular-development",
        "react-native-development",
    ],
}
DEFERRED_AGENTS = {"architecture-reviewer.agent.md", "delivery-risk-reviewer.agent.md"}
RESEARCH_SOURCES = ["agents", "claude-skills", "superpowers", "oh-my-openagent", "claude-mem"]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def count_lines(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def check_markdown_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if not target or "://" in target or target.startswith("#") or target.startswith("mailto:"):
            continue
        target_path = (path.parent / target.split("#", 1)[0]).resolve()
        if not target_path.exists():
            fail(errors, f"dead markdown link in {path.relative_to(ROOT)} -> {target}")


def check_skill_tree(base: Path, label: str, errors: list[str]) -> None:
    peer_skills = sorted(p.parent.name for p in base.glob("*/SKILL.md"))
    expected_packs = sorted(EXPECTED)
    if peer_skills != expected_packs:
        fail(errors, f"{label}: expected peer skills {expected_packs}, found {peer_skills}")

    for pack, refs in EXPECTED.items():
        skill = base / pack / "SKILL.md"
        if not skill.exists():
            fail(errors, f"{label}: missing {skill.relative_to(ROOT)}")
            continue
        text = skill.read_text(encoding="utf-8")
        if f"name: {pack}" not in text:
            fail(errors, f"{label}: {skill.relative_to(ROOT)} frontmatter name mismatch")
        if "description: 'Use when" not in text:
            fail(errors, f"{label}: {skill.relative_to(ROOT)} description must use trigger-first 'Use when' phrasing")
        if count_lines(skill) > 220:
            fail(errors, f"{label}: {skill.relative_to(ROOT)} exceeds 220-line pack budget")
        check_markdown_links(skill, errors)
        for ref in refs:
            ref_path = base / pack / "references" / f"{ref}.md"
            if not ref_path.exists():
                fail(errors, f"{label}: missing reference {ref_path.relative_to(ROOT)}")

    all_refs = list(base.glob("*/references/*.md"))
    if len(all_refs) != 33:
        fail(errors, f"{label}: expected 33 references, found {len(all_refs)}")

    leaf_peer_names = {ref for refs in EXPECTED.values() for ref in refs}
    bad_peer_leafs = sorted(name for name in peer_skills if name in leaf_peer_names)
    if bad_peer_leafs:
        fail(errors, f"{label}: former leaf skills are still peers: {bad_peer_leafs}")


def check_agents(errors: list[str]) -> None:
    root_agents = sorted(p.name for p in (ROOT / "agents").glob("*.md"))
    github_agents = sorted(p.name for p in (ROOT / ".github" / "agents").glob("*.md"))
    expected_agents = ["ce7-software-engineering.agent.md", "skill-evaluator.agent.md"]
    if root_agents != expected_agents:
        fail(errors, f"agents/: expected {expected_agents}, found {root_agents}")
    if github_agents != expected_agents:
        fail(errors, f".github/agents/: expected {expected_agents}, found {github_agents}")
    deferred = sorted(set(root_agents + github_agents) & DEFERRED_AGENTS)
    if deferred:
        fail(errors, f"Deferred agents must not exist yet: {deferred}")


def check_copilot(errors: list[str]) -> None:
    path = ROOT / ".github" / "copilot-instructions.md"
    if not path.exists():
        fail(errors, "Missing .github/copilot-instructions.md")
        return
    text = path.read_text(encoding="utf-8")
    for pack in EXPECTED:
        if pack not in text:
            fail(errors, f"copilot-instructions missing pack route: {pack}")


def check_benchmark(errors: list[str]) -> None:
    path = ROOT / "evals" / "routing-benchmark.jsonl"
    if not path.exists():
        fail(errors, "Missing evals/routing-benchmark.jsonl")
        return
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(errors, f"routing-benchmark.jsonl:{line_no}: invalid JSON: {exc}")
            continue
        rows.append(row)
        for pack in row.get("expected_packs", []):
            if pack not in EXPECTED:
                fail(errors, f"routing-benchmark.jsonl:{line_no}: unknown expected pack {pack}")
    if len(rows) < 14:
        fail(errors, f"Expected at least 14 routing benchmark rows, found {len(rows)}")


def check_banking_insurance_benchmark(errors: list[str]) -> None:
    path = ROOT / "evals" / "banking-insurance-benchmark.jsonl"
    if not path.exists():
        fail(errors, "Missing evals/banking-insurance-benchmark.jsonl")
        return
    required_fields = {
        "id",
        "domain",
        "business_context",
        "prompt",
        "expected_packs",
        "expected_references",
        "should_not_activate",
        "model_targets",
        "risk_class",
        "scoring_notes",
    }
    rows = []
    domains = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(errors, f"banking-insurance-benchmark.jsonl:{line_no}: invalid JSON: {exc}")
            continue
        rows.append(row)
        missing = sorted(required_fields - set(row))
        if missing:
            fail(errors, f"banking-insurance-benchmark.jsonl:{line_no}: missing fields {missing}")
        domains.add(row.get("domain"))
        if "gpt" not in row.get("model_targets", []) or "claude" not in row.get("model_targets", []):
            fail(errors, f"banking-insurance-benchmark.jsonl:{line_no}: model_targets must include gpt and claude")
        for pack in row.get("expected_packs", []):
            if pack not in EXPECTED:
                fail(errors, f"banking-insurance-benchmark.jsonl:{line_no}: unknown expected pack {pack}")
        if len(row.get("prompt", "")) < 80:
            fail(errors, f"banking-insurance-benchmark.jsonl:{line_no}: prompt is too short for realistic benchmark")
    if len(rows) != 10:
        fail(errors, f"Expected exactly 10 banking/insurance benchmark rows, found {len(rows)}")
    required_domains = {"banking", "non-life-insurance", "banking-and-non-life-insurance"}
    if not required_domains.issubset(domains):
        fail(errors, f"banking-insurance benchmark missing required domains: {sorted(required_domains - domains)}")


def check_research_artifact(errors: list[str]) -> None:
    path = ROOT / "docs" / "external-skill-research.md"
    if not path.exists():
        fail(errors, "Missing docs/external-skill-research.md")
        return
    text = path.read_text(encoding="utf-8")
    for source in RESEARCH_SOURCES:
        if source not in text:
            fail(errors, f"external-skill-research.md missing source project: {source}")
    required_sections = ["Sources Reviewed", "Adopted Design Principles", "Rejected / Deferred Patterns", "Originality Notes"]
    for section in required_sections:
        if section not in text:
            fail(errors, f"external-skill-research.md missing section: {section}")


def check_quality_rubric(errors: list[str]) -> None:
    path = ROOT / "docs" / "skill-pack-quality-rubric.md"
    if not path.exists():
        fail(errors, "Missing docs/skill-pack-quality-rubric.md")
        return
    text = path.read_text(encoding="utf-8")
    required_terms = ["Trigger accuracy", "Reference precision", "Progressive disclosure", "Benchmark coverage", "Originality", "Copilot readiness"]
    for term in required_terms:
        if term not in text:
            fail(errors, f"skill-pack-quality-rubric.md missing rubric term: {term}")


def check_evaluation_workflow_artifacts(errors: list[str]) -> None:
    required_files = [
        ROOT / "docs" / "evaluation-improvement-playbook.md",
        ROOT / "docs" / "evaluation-improvement-playbook.vi-VN.md",
        ROOT / "docs" / "pipeline-guide.md",
        ROOT / "docs" / "pipeline-guide.vi-VN.md",
        ROOT / "evals" / "scoring-rubric.md",
        ROOT / "evals" / "scoring-rubric.vi-VN.md",
        ROOT / "evals" / "model-comparison-runbook.md",
        ROOT / "evals" / "model-comparison-runbook.vi-VN.md",
        ROOT / "evals" / "file-based-benchmark-pipeline.md",
        ROOT / "evals" / "file-based-benchmark-pipeline.vi-VN.md",
        ROOT / "reports" / "README.md",
        ROOT / "reports" / "README.vi-VN.md",
        ROOT / "reports" / "latest-skill-eval.md",
        ROOT / "reports" / "latest-skill-eval.vi-VN.md",
        ROOT / "reports" / "skill-eval-history.jsonl",
        ROOT / "scripts" / "benchmark_pipeline.py",
    ]
    for path in required_files:
        if not path.exists():
            fail(errors, f"Missing evaluation workflow artifact: {path.relative_to(ROOT)}")
    rubric = ROOT / "evals" / "scoring-rubric.md"
    if rubric.exists():
        text = rubric.read_text(encoding="utf-8")
        for term in ["Trigger accuracy", "Reference precision", "Token efficiency", "Regression Rule"]:
            if term not in text:
                fail(errors, f"scoring-rubric.md missing term: {term}")

    latest_en = ROOT / "reports" / "latest-skill-eval.md"
    if latest_en.exists():
        text = latest_en.read_text(encoding="utf-8")
        for term in ["Latest CE7 Skill Evaluation", "Current snapshot", "Rules"]:
            if term not in text:
                fail(errors, f"reports/latest-skill-eval.md missing section: {term}")

    latest_vi = ROOT / "reports" / "latest-skill-eval.vi-VN.md"
    if latest_vi.exists():
        text = latest_vi.read_text(encoding="utf-8")
        for term in ["Báo cáo CE7 mới nhất", "Snapshot hiện tại", "Quy tắc"]:
            if term not in text:
                fail(errors, f"reports/latest-skill-eval.vi-VN.md missing section: {term}")

    history = ROOT / "reports" / "skill-eval-history.jsonl"
    if history.exists():
        required_history_keys = {
            "timestamp",
            "run_id",
            "benchmark",
            "outputs_scored",
            "models",
            "semantic_status",
            "deterministic",
            "per_model",
            "issue_counts",
            "hotspots",
            "lowest_scoring_cases",
            "likely_update_targets",
            "artifacts",
        }
        for line_no, line in enumerate(history.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(errors, f"skill-eval-history.jsonl:{line_no}: invalid JSON: {exc}")
                continue
            missing = sorted(required_history_keys - set(row))
            if missing:
                fail(errors, f"skill-eval-history.jsonl:{line_no}: missing keys {missing}")
            deterministic = row.get("deterministic", {})
            for key in ["average_score", "pass", "warn", "fail"]:
                if key not in deterministic:
                    fail(errors, f"skill-eval-history.jsonl:{line_no}: deterministic missing key {key}")


def main() -> int:
    errors: list[str] = []
    check_skill_tree(ROOT / "skills", "skills", errors)
    check_skill_tree(ROOT / ".github" / "skills", ".github/skills", errors)
    check_agents(errors)
    check_copilot(errors)
    check_benchmark(errors)
    check_banking_insurance_benchmark(errors)
    check_research_artifact(errors)
    check_quality_rubric(errors)
    check_evaluation_workflow_artifacts(errors)

    if errors:
        print("FAIL: hybrid pack validation found issues:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: hybrid pack layout is valid")
    print("- peer pack skills: 7")
    print("- leaf references: 33")
    print("- agents: ce7-software-engineering, skill-evaluator")
    print("- deferred agents absent")
    print("- routing benchmark present")
    print("- banking/insurance benchmark present")
    print("- external skill research artifact present")
    print("- skill pack quality rubric present")
    print("- evaluation workflow artifacts present")
    return 0


if __name__ == "__main__":
    sys.exit(main())

