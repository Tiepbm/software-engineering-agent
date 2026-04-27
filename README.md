# CE7 Software Engineering Agent

[English](README.md) | [Vietnamese](README.vi-VN.md)

## Overview

This is a principal-level engineering agent for enterprise and regulated systems, with strong coverage across architecture, data, platform, security, observability, integration, delivery, and production operations.

- Primary Copilot target: `.github/copilot-instructions.md` and `.github/skills/`
- Agent files: `agents/ce7-software-engineering.agent.md`, `agents/skill-evaluator.agent.md`
- Review baseline: `REVIEW.md`
- Maintenance rules:
  - `instructions/principal-agent-maintenance.instructions.md`
  - `instructions/principal-skills-maintenance.instructions.md`

## Recommended GitHub Topics

Use these repository topics on GitHub for discoverability:

- `copilot-agent`
- `github-copilot`
- `prompt-engineering`
- `software-engineering`
- `enterprise-architecture`
- `system-design`
- `api-design`
- `data-engineering`
- `database-architecture`
- `security-review`
- `observability`
- `sre`
- `devops`
- `performance-engineering`
- `refactoring`
- `regulated-systems`
- `banking`
- `insurance`

Quick set from GitHub UI: Repository -> Settings -> General -> Topics.

Optional via GitHub CLI:

```bash
gh repo edit <owner>/<repo> --add-topic copilot-agent --add-topic github-copilot --add-topic prompt-engineering --add-topic software-engineering --add-topic enterprise-architecture --add-topic system-design --add-topic api-design --add-topic data-engineering --add-topic database-architecture --add-topic security-review --add-topic observability --add-topic sre --add-topic devops --add-topic performance-engineering --add-topic refactoring --add-topic regulated-systems --add-topic banking --add-topic insurance
```

## Package Structure

```text
software-engineering-agent/
  .github/
    copilot-instructions.md
    agents/
      ce7-software-engineering.agent.md
      skill-evaluator.agent.md
    skills/
      <7 pack skills>/SKILL.md
      <7 pack skills>/references/*.md
  agents/
    ce7-software-engineering.agent.md
    skill-evaluator.agent.md
  skills/
    <7 pack skills>/SKILL.md
    <7 pack skills>/references/*.md
  evals/
    banking-insurance-benchmark.jsonl
    file-based-benchmark-pipeline.md
    file-based-benchmark-pipeline.vi-VN.md
    model-comparison-runbook.md
    model-comparison-runbook.vi-VN.md
    routing-benchmark.jsonl
    scoring-rubric.md
    scoring-rubric.vi-VN.md
  docs/
    evaluation-improvement-playbook.md
    external-skill-research.md
    evaluation-improvement-playbook.vi-VN.md
    pipeline-guide.md
    pipeline-guide.vi-VN.md
    skill-pack-quality-rubric.md
  reports/
    README.md
    README.vi-VN.md
    latest-skill-eval.md
    latest-skill-eval.vi-VN.md
    skill-eval-history.jsonl
  scripts/
    benchmark_pipeline.py
    validate_hybrid_packs.py
  instructions/
    principal-agent-maintenance.instructions.md
    principal-skills-maintenance.instructions.md
  REVIEW.md
```

### Copilot-First Hybrid Skill Design

- **7 peer pack skills** are exposed to GitHub Copilot.
- The previous **33 leaf skills** are preserved as `references/*.md` under the relevant pack.
- Copilot should load a pack first, then load only the exact reference files needed for the task.
- `.github/skills/` is the primary runtime target; root `skills/` mirrors the pack structure for repository maintenance.
- `docs/external-skill-research.md` records patterns reviewed from sibling workspace projects.
- `docs/skill-pack-quality-rubric.md` turns those patterns into reviewable quality gates.
- `docs/evaluation-improvement-playbook.md` / `docs/evaluation-improvement-playbook.vi-VN.md` explain the recurring evaluation and improvement workflow.

### Evaluation Documentation Map

To reduce overlap, evaluation docs now have explicit ownership:

- `docs/pipeline-guide.md` / `docs/pipeline-guide.vi-VN.md` → canonical end-to-end pipeline execution guide.
- `docs/evaluation-improvement-playbook.md` / `docs/evaluation-improvement-playbook.vi-VN.md` → evaluation policy, fix-target logic, improvement cadence, and Definition of Done.
- `evals/file-based-benchmark-pipeline.md` / `evals/file-based-benchmark-pipeline.vi-VN.md` → short quickstart commands only.
- `evals/model-comparison-runbook.md` / `evals/model-comparison-runbook.vi-VN.md` → GPT-vs-Claude benchmarking for the banking/non-life insurance suite.
- `evals/scoring-rubric.md` / `evals/scoring-rubric.vi-VN.md` → scoring criteria only.

### Reports Map

`reports/` now has explicit ownership too:

- `reports/latest-skill-eval.md` / `reports/latest-skill-eval.vi-VN.md` → latest short run-level snapshot only.
- `reports/skill-eval-history.jsonl` → append-only machine-readable history with **one row per run**.
- `reports/README.md` / `reports/README.vi-VN.md` → schema and ownership contract.

Detailed prompt-by-prompt findings should stay under `runs/<run_id>/`, especially `report.json`, `summary.md`, and `scores.jsonl`.

## Optimization Goals

- Principal-level decision support, not generic coding chat.
- Enterprise posture: correctness, auditability, security, operability, and delivery safety.
- Regulated workloads: banking, insurance, payments, claims, policy/billing, and PII-sensitive systems.
- Explicit assumptions, trade-offs, risks, rejected options, and validation steps.

## Response Model

For non-trivial requests, the agent runs mandatory 6-step triage: primary role, supporting lenses, task type, risk class, regulatory sensitivity, and missing constraints.

## Installation and Setup

This package is documentation-first and file-based. Based on the current repository structure (`.github/`, `agents/`, `skills/`, `instructions/`), use the steps below to install and start using it in your workspace.

> **New here?** Start with `docs/GETTING-STARTED.md` for a 5-minute overview.

### Documentation Map

| Audience | Document | Purpose |
|---|---|---|
| **New users** | `docs/GETTING-STARTED.md` | 5-minute setup and first prompt |
| **All users** | `README.md` | Full project overview, structure, and commands |
| **All users** | `REVIEW.md` | Quality scores and improvement history |
| **Evaluators** | `evals/file-based-benchmark-pipeline.md` | Quickstart commands for benchmarking |
| **Evaluators** | `docs/pipeline-guide.md` | Full pipeline execution guide |
| **Evaluators** | `docs/evaluation-improvement-playbook.md` | When and how to improve skills |
| **Evaluators** | `evals/model-comparison-runbook.md` | GPT vs Claude comparison |
| **Evaluators** | `evals/scoring-rubric.md` | Scoring criteria |
| **Maintainers** | `instructions/principal-agent-maintenance.instructions.md` | Agent editing rules |
| **Maintainers** | `instructions/principal-skills-maintenance.instructions.md` | Skill editing rules |
| **Maintainers** | `docs/external-skill-research.md` | Patterns from sibling projects |
| **Maintainers** | `docs/skill-pack-quality-rubric.md` | Quality gates for pack changes |
| **Reports** | `reports/README.md` | Reports schema and ownership |

All documents are available in English and Vietnamese (`.vi-VN.md` suffix).

### 1) Clone the repository

```bash
git clone <your-repo-url>
cd software-engineering-agent
```

### 2) Choose installation mode

#### Option A: Global installation (all workspaces)

Copy to `~/.copilot` so the agent is available in every project:

```bash
# Agent + instructions
cp agents/ce7-software-engineering.agent.md ~/.copilot/agents/
cp instructions/*.instructions.md ~/.copilot/instructions/
cp .github/copilot-instructions.md ~/.copilot/copilot-instructions.md

# Skills (7 packs + 33 references)
rm -rf ~/.copilot/skills/*
cp -R .github/skills/* ~/.copilot/skills/
```

Structure after install:

```text
~/.copilot/
  copilot-instructions.md
  agents/
    ce7-software-engineering.agent.md
  instructions/
    principal-agent-maintenance.instructions.md
    principal-skills-maintenance.instructions.md
  skills/
    core-engineering-pack/SKILL.md
    core-engineering-pack/references/*.md
    data-database-analytics-pack/SKILL.md
    data-database-analytics-pack/references/*.md
    security-access-pack/SKILL.md
    security-access-pack/references/*.md
    platform-integration-pack/SKILL.md
    platform-integration-pack/references/*.md
    resilience-performance-pack/SKILL.md
    resilience-performance-pack/references/*.md
    observability-release-pack/SKILL.md
    observability-release-pack/references/*.md
    storage-search-stack-pack/SKILL.md
    storage-search-stack-pack/references/*.md
```

#### Option B: Workspace-only installation

Keep the repo as a workspace folder. Copilot reads from `.github/` automatically:

```bash
# Just open the folder in your IDE — no copy needed
# Copilot discovers .github/copilot-instructions.md and .github/skills/ automatically
```

#### Option C: Add to existing project

Copy `.github/` contents into your project:

```bash
cp .github/copilot-instructions.md <your-project>/.github/
cp -R .github/skills/ <your-project>/.github/skills/
cp -R .github/agents/ <your-project>/.github/agents/
```

### 3) Open in your IDE workspace

Open this folder as part of your workspace so Copilot can read agent + skill markdown files.

### 4) Start with a routing-first prompt

Ask the assistant with a clear task and constraints, for example:

- "Act as CE7 Software Engineering Agent. Design idempotent payment retries for a multi-tenant mobile flow."
- "Review this change using security, data, and release-risk lenses."

### 5) Verify package health after updates

- Ensure both `README.md` and `README.vi-VN.md` stay aligned.
- Ensure all pack links still resolve to `skills/<pack>/SKILL.md` and `.github/skills/<pack>/SKILL.md`.
- Update `docs/external-skill-research.md` when adopting patterns from sibling projects.
- Review `docs/skill-pack-quality-rubric.md` when changing pack triggers, references, or evaluator rules.
- Run `python3 scripts/validate_hybrid_packs.py`.
- Update `REVIEW.md` after major changes.

## Hybrid Pack Mapping

| # | Pack skill | Former leaf references | Primary triggers |
|---:|---|---|---|
| 1 | `core-engineering-pack` | `requirements-analysis`, `solution-architecture`, `system-design`, `api-design`, `testing-strategy`, `code-review-and-refactoring` | Requirements, architecture, APIs, tests, review, refactoring |
| 2 | `data-database-analytics-pack` | `data-modeling`, `database-architecture`, `sql-and-query-optimization`, `database-reliability-and-operations`, `data-engineering-and-pipelines`, `analytics-and-warehouse-design` | Data models, databases, SQL/ORM, DB ops, pipelines, analytics |
| 3 | `security-access-pack` | `security-review`, `authn-authz-and-secrets` | Security review, identity, authorization, tenant isolation, secrets, sensitive data |
| 4 | `platform-integration-pack` | `messaging-and-eventing`, `api-gateway-and-service-integration`, `rate-limiting-and-traffic-control`, `workflow-and-job-orchestration`, `background-jobs-and-batch-processing` | Messaging, gateways, integrations, rate limits, workflows, jobs, batch |
| 5 | `resilience-performance-pack` | `resilience-and-fault-tolerance`, `caching-and-distributed-state`, `performance-engineering` | Resilience, caching, distributed state, latency, throughput, profiling |
| 6 | `observability-release-pack` | `logging-metrics-and-tracing`, `monitoring-alerting-and-slos`, `observability-and-sre`, `devops-and-release` | Telemetry, SLOs, alerts, runbooks, release, rollout, rollback |
| 7 | `storage-search-stack-pack` | `file-and-object-storage`, `search-and-indexing`, `dotnet-development`, `java-spring-boot-development`, `reactjs-development`, `angular-development`, `react-native-development` | Object storage, search, .NET, Spring Boot, React, Angular, React Native |

### Validation

```bash
python3 scripts/validate_hybrid_packs.py
```

The validator checks exactly 7 peer pack skills, 33 references, 2 agents, no deferred reviewer agents, complete Copilot routes, and a valid routing benchmark corpus.

## Next Steps for Evaluation and Improvement

1. Read `docs/evaluation-improvement-playbook.md` or `docs/evaluation-improvement-playbook.vi-VN.md` for the evaluation policy and improvement loop.
2. Run structural validation:

   ```bash
   python3 scripts/validate_hybrid_packs.py
   ```

3. Select 5–10 prompts from `evals/routing-benchmark.jsonl`.
4. Run those prompts through `ce7-software-engineering` and record activated packs/references.
5. Use `agents/skill-evaluator.agent.md` to score outputs with `evals/scoring-rubric.md`.
6. Sync the latest snapshot to `reports/latest-skill-eval.md` / `reports/latest-skill-eval.vi-VN.md` and append **one run-level row** to `reports/skill-eval-history.jsonl`.
7. Patch packs/references only when benchmark evidence shows routing, reference precision, output quality, or token-bloat issues.

### Banking and Non-Life Insurance Benchmark

- `evals/banking-insurance-benchmark.jsonl` contains 10 realistic banking, non-life insurance, and bancassurance cases.
- `evals/model-comparison-runbook.md` / `evals/model-comparison-runbook.vi-VN.md` explain how to replay the same cases on GPT and Claude models.
- `evals/file-based-benchmark-pipeline.md` / `evals/file-based-benchmark-pipeline.vi-VN.md` provide the short quickstart for file-based execution.
- `docs/pipeline-guide.md` / `docs/pipeline-guide.vi-VN.md` are the canonical guides for prepare → output → score → evaluator → report/history.
- Use `evals/scoring-rubric.md` or `evals/scoring-rubric.vi-VN.md` to score both models consistently.
- Use `reports/README.md` / `reports/README.vi-VN.md` to keep global reports concise and run-level.

### File-Based Benchmark Pipeline

```bash
python3 scripts/benchmark_pipeline.py prepare --run-id 2026-04-27-gpt-claude-v1 --models gpt,claude
python3 scripts/benchmark_pipeline.py score --run-id 2026-04-27-gpt-claude-v1 --append-history
python3 scripts/benchmark_pipeline.py evaluator-prompts --run-id 2026-04-27-gpt-claude-v1
```

Save model outputs to `runs/<run_id>/outputs/<model>/<prompt_id>.md` before running `score`.

### One-command Auto Run (switch model only)

If you want the pipeline to run automatically end-to-end for one provider in one command:

```bash
# GPT
export OPENAI_API_KEY="<your_openai_key>"
python3 scripts/benchmark_pipeline.py run --run-id 2026-04-27-gpt-auto --model gpt

# Claude
export ANTHROPIC_API_KEY="<your_anthropic_key>"
python3 scripts/benchmark_pipeline.py run --run-id 2026-04-27-claude-auto --model claude
```

What `run` does automatically:

1. prepare prompts for the selected model;
2. call the provider API for each prompt and save outputs;
3. run deterministic scoring with `--append-history`;
4. sync `reports/latest-skill-eval*` and append one run row to history;
5. generate `evaluator-prompts/` for semantic scoring.

### No API keys (Copilot chat windows) — recommended manual automation

If you do not have API keys and want a Copilot-friendly flow:

```bash
# 1) Prepare prompts + output stubs + worklist for GPT and Claude
python3 scripts/benchmark_pipeline.py implement \
  --run-id 2026-04-27-gpt-claude-manual \
  --models gpt,claude

# 2) After pasting model outputs into files, finalize scoring and evaluator prompts
python3 scripts/benchmark_pipeline.py finalize \
  --run-id 2026-04-27-gpt-claude-manual \
  --models gpt,claude
```

`implement` creates run-local guidance under `runs/<run_id>/manual/README.md` and `runs/<run_id>/manual/worklist.md`.

## Expected Output Shapes

- Architecture/analysis: problem -> constraints -> options -> recommendation -> architecture/data/integration/security/ops -> risks -> delivery plan -> validation checklist.
- Implementation/debugging: diagnosis -> likely root cause -> fix -> impact -> tests -> residual risk -> longer-term improvement.
- Review/refactoring: assessment -> strengths -> critical issues -> medium issues -> architecture/data concerns -> refactoring plan -> priority order.

## Production Stop Conditions

The agent escalates or asks for constraints when key safety conditions are missing, such as:

- Data migration without reconciliation and rollback/roll-forward strategy
- Messaging design without ordering, idempotency, retry, DLQ, and replay
- Caching design without staleness, invalidation, and authorization safety
- Security-sensitive changes without auth/authz/secrets/audit analysis
- Release plan without sequencing, verification, and rollback strategy
- Performance recommendations without baseline evidence

## Quick Prompt Examples

- "Design idempotent payment retry flow for mobile -> API -> PSP in a multi-tenant system."
- "Review this PR for migration and rollback risk before canary release."
- "Propose API + data model changes for claim status transitions with audit trail."
- "Diagnose high p95 latency after introducing Redis cache and async workers."

## Contributor Notes

- Keep the agent as a routing/orchestration panel; do not duplicate skill content.
- Keep all skills aligned with required structure and quality floors in the instructions.
- Preserve enterprise/regulated posture and production safety rules.
- Re-run the package review and update `REVIEW.md` after major changes.

## References

- Agent spec: `agents/ce7-software-engineering.agent.md`
- Quality report: `REVIEW.md`
- Agent maintenance: `instructions/principal-agent-maintenance.instructions.md`
- Skills maintenance: `instructions/principal-skills-maintenance.instructions.md`

