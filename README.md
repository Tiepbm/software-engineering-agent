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
    routing-benchmark.jsonl
  docs/
    external-skill-research.md
    evaluation-improvement-playbook.vi-VN.md
    skill-pack-quality-rubric.md
  reports/
    latest-skill-eval.md
    skill-eval-history.jsonl
  scripts/
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
- `docs/evaluation-improvement-playbook.vi-VN.md` explains the recurring evaluation and improvement workflow.

## Optimization Goals

- Principal-level decision support, not generic coding chat.
- Enterprise posture: correctness, auditability, security, operability, and delivery safety.
- Regulated workloads: banking, insurance, payments, claims, policy/billing, and PII-sensitive systems.
- Explicit assumptions, trade-offs, risks, rejected options, and validation steps.

## Response Model

For non-trivial requests, the agent runs mandatory 6-step triage: primary role, supporting lenses, task type, risk class, regulatory sensitivity, and missing constraints.

## Installation and Setup

This package is documentation-first and file-based. Based on the current repository structure (`.github/`, `agents/`, `skills/`, `instructions/`), use the steps below to install and start using it in your workspace.

### 1) Clone the repository

```bash
git clone <your-repo-url>
cd software-engineering-agent
```

### 2) Keep the package structure intact

Required paths:

- `.github/copilot-instructions.md`
- `.github/skills/<pack-name>/SKILL.md` (7 pack skills)
- `.github/skills/<pack-name>/references/<leaf>.md` (33 former leaf skills)
- `agents/ce7-software-engineering.agent.md`
- `agents/skill-evaluator.agent.md`
- `instructions/principal-agent-maintenance.instructions.md`
- `instructions/principal-skills-maintenance.instructions.md`

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

1. Read `docs/evaluation-improvement-playbook.vi-VN.md` for the 5-layer evaluation workflow.
2. Run structural validation:

   ```bash
   python3 scripts/validate_hybrid_packs.py
   ```

3. Select 5–10 prompts from `evals/routing-benchmark.jsonl`.
4. Run those prompts through `ce7-software-engineering` and record activated packs/references.
5. Use `agents/skill-evaluator.agent.md` to score outputs with `evals/scoring-rubric.md`.
6. Record results in `reports/latest-skill-eval.md` and append history to `reports/skill-eval-history.jsonl`.
7. Patch packs/references only when benchmark evidence shows routing, reference precision, output quality, or token-bloat issues.

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

