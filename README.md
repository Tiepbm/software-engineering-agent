# CE7 Software Engineering Agent

[English](README.md) | [Tiếng Việt](README.vi-VN.md)

A **principal-level engineering agent** for enterprise and regulated systems (banking, insurance, payments, claims, billing). Routes work to focused pack skills and progressive-disclosure references; never duplicates pack content in the agent.

## What you get

- **1 router agent** — `agents/ce7-software-engineering.agent.md` (~110 lines, table-driven).
- **8 pack skills** — concrete `Use when` triggers, distinct `When NOT to Use` boundaries, explicit cross-pack handoffs.
- **36 reference playbooks** — loaded only when a task needs them.
- **3 output-shape examples** — architecture, debugging, review.
- **Eval harness** — routing, anti-pattern, token-budget, banking/insurance benchmarks + scoring rubric.
- **Copilot-first deployment** via `.github/copilot-instructions.md` + `.github/skills/`.

## Pack skills (8)

| Pack | Use when |
|---|---|
| `core-engineering-pack` | Requirements, architecture, system design, API contracts, testing, review, refactoring, ADRs. |
| `data-database-analytics-pack` | Data modeling, DB selection/ops, SQL/ORM tuning, pipelines, analytics/warehouse. |
| `security-access-pack` | Identity, authz, tenant isolation, secrets, audit, sensitive data, abuse cases. |
| `platform-integration-pack` | Messaging, gateways/BFFs, partner integrations, rate limits, workflows, jobs, batch. |
| `resilience-performance-pack` | Runtime cache, distributed state, timeouts/retries/circuits, latency, capacity, cost/FinOps. |
| `observability-release-pack` | Logs/metrics/traces, SLOs, alerts, runbooks, CI/CD, rollout, rollback, incident response. |
| `storage-search-pack` | Object/file storage, signed URLs, retention, search/indexing, projection, reindex. |
| `application-stacks-pack` | Framework code: ASP.NET Core/EF, Spring Boot/JPA, React, Angular, React Native. |

## Quick start

```bash
# 1. Install (pick one mode — see docs/INSTALL.md)
cp -R .github/skills/                  ~/.copilot/skills/   # global
# OR open this folder in your IDE; Copilot reads .github/ automatically

# 2. Validate
python3 scripts/validate_hybrid_packs.py

# 3. Try a prompt
# "Act as the CE7 Software Engineering Agent. Design idempotent payment retries
#  with reconciliation and audit for a multi-tenant banking flow."
```

## Documentation map

| File | Audience | Purpose |
|---|---|---|
| `AGENTS.md` | Maintainer / contributor | Short editing rules and workflow. |
| `docs/INSTALL.md` | User | Install modes and post-install checks. |
| `docs/GETTING-STARTED.md` | User | 5-minute first-prompt walkthrough. |
| `docs/pipeline-guide.md` | Evaluator | End-to-end benchmark execution. |
| `docs/evaluation-improvement-playbook.md` | Maintainer | When and how to improve packs. |
| `docs/skill-pack-quality-rubric.md` | Maintainer | Quality gates a PR must clear. |
| `docs/external-skill-research.md` | Maintainer | Patterns from sibling projects + originality notes. |
| `instructions/pack-conventions.instructions.md` | Maintainer | Single source of truth for pack structure / output style / token rules. |
| `instructions/principal-agent-maintenance.instructions.md` | Maintainer | Agent maintenance rules. |
| `instructions/principal-skills-maintenance.instructions.md` | Maintainer | Reference maintenance rules. |
| `evals/scoring-rubric.md` | Evaluator | Per-prompt scoring rubric. |
| `examples/` | User / agent | Output-shape templates referenced by the agent. |
| `reports/CE7-AGENT-SYSTEM-REVIEW-2026-04-28.md` | Maintainer | Brutal review that drives the current architecture. |
| `CHANGELOG.md` | All | Release log. |

## Quality gates (CI-enforceable)

`python3 scripts/validate_hybrid_packs.py` enforces:

- 8 peer pack skills (`skills/<pack>/SKILL.md`).
- 36 leaf references (`skills/<pack>/references/*.md`).
- Pack frontmatter `description` starts with `'Use when'`.
- Pack `SKILL.md` ≤ 100 lines.
- Routing benchmark uses only known pack names.
- Banking/insurance benchmark = exactly 10 rows; required domains present.
- Required evaluation workflow artifacts exist.

Add `CHECK_GITHUB_MIRROR=1` to also validate the `.github/` mirror.

## Status

- Layout: 8 packs / 39 references / 2 agents / 3 examples / 4 eval files.
- Last review: `reports/CE7-AGENT-SYSTEM-REVIEW-2026-04-28.md`.

## Contributing

Read `AGENTS.md` first. The short version: keep packs ≤ 100 lines, keep the agent table-driven, prefer adding a reference over adding a pack, and always update `evals/` when you change routing.
