# CE7 Software Engineering Agent

[English](README.md) | [Vietnamese](README.vi-VN.md)

## Overview

This is a principal-level engineering agent for enterprise and regulated systems, with strong coverage across architecture, data, platform, security, observability, integration, delivery, and production operations.

- Agent file: `agents/ce7-software-engineering.agent.md`
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
ce7-software-engineering/
  agents/
    ce7-software-engineering.agent.md
  skills/
    <33 domain skills>
  instructions/
    principal-agent-maintenance.instructions.md
    principal-skills-maintenance.instructions.md
  REVIEW.md
```

## Optimization Goals

- Principal-level decision support, not generic coding chat.
- Enterprise posture: correctness, auditability, security, operability, and delivery safety.
- Regulated workloads: banking, insurance, payments, claims, policy/billing, and PII-sensitive systems.
- Explicit assumptions, trade-offs, risks, rejected options, and validation steps.

## Response Model

For non-trivial requests, the agent runs mandatory 6-step triage: primary role, supporting lenses, task type, risk class, regulatory sensitivity, and missing constraints.

## Installation and Setup

This package is documentation-first and file-based. Based on the current repository structure (`agents/`, `skills/`, `instructions/`), use the steps below to install and start using it in your workspace.

### 1) Clone the repository

```bash
git clone <your-repo-url>
cd ce7-software-engineering
```

### 2) Keep the package structure intact

Required paths:

- `agents/ce7-software-engineering.agent.md`
- `skills/<skill-name>/SKILL.md` (33 skills)
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
- Ensure all skill links still resolve to `skills/<skill>/SKILL.md`.
- Update `REVIEW.md` after major changes.

## Full 33-Skill Mapping

| # | Skill slug | Group | When to use | Primary triggers | Skill file |
|---:|---|---|---|---|---|
| 1 | `requirements-analysis` | Core Engineering | Clarify ambiguous requirements, acceptance criteria, and scope/risk | Ambiguous scope, actors, workflows, measurable outcomes | [SKILL.md](skills/requirements-analysis/SKILL.md) |
| 2 | `solution-architecture` | Core Engineering | Select architecture shape, buy-vs-build, and ownership model | Architecture shape, boundaries, complexity, team fit | [SKILL.md](skills/solution-architecture/SKILL.md) |
| 3 | `system-design` | Core Engineering | Design runtime flow, component boundaries, and failure behavior | Runtime flows, sync/async, scalability, bottlenecks | [SKILL.md](skills/system-design/SKILL.md) |
| 4 | `api-design` | Core Engineering | Define API contracts, versioning, idempotency, and errors | API boundaries, request/response contracts, compatibility | [SKILL.md](skills/api-design/SKILL.md) |
| 5 | `testing-strategy` | Core Engineering | Define risk-based tests, test pyramid, and migration tests | Risk-based testing, integration/contract/E2E scope | [SKILL.md](skills/testing-strategy/SKILL.md) |
| 6 | `code-review-and-refactoring` | Core Engineering | Review maintainability and safe refactoring plan | Coupling/cohesion, debt, regression risk, safe sequence | [SKILL.md](skills/code-review-and-refactoring/SKILL.md) |
| 7 | `data-modeling` | Data and Database | Model entities/aggregates, history, and auditability | Entities, relationships, transactional boundaries | [SKILL.md](skills/data-modeling/SKILL.md) |
| 8 | `database-architecture` | Data and Database | Choose database type using workload-fit reasoning | OLTP/OLAP fit, consistency, scaling, retention | [SKILL.md](skills/database-architecture/SKILL.md) |
| 9 | `sql-and-query-optimization` | Data and Database | Optimize SQL/ORM using execution plans | Query plans, indexes, joins, lock/contention | [SKILL.md](skills/sql-and-query-optimization/SKILL.md) |
| 10 | `database-reliability-and-operations` | Data and Database | Run production DB safely: backup/restore/failover/migrations | Replication, restore drills, migration safety | [SKILL.md](skills/database-reliability-and-operations/SKILL.md) |
| 11 | `data-engineering-and-pipelines` | Data and Database | Build ETL/ELT/CDC with replay, backfill, and data quality | Pipelines, schema evolution, idempotency, recovery | [SKILL.md](skills/data-engineering-and-pipelines/SKILL.md) |
| 12 | `analytics-and-warehouse-design` | Data and Database | Design DWH/lakehouse, marts, semantic layer, governance | Dimensional models, BI consumption, freshness/cost | [SKILL.md](skills/analytics-and-warehouse-design/SKILL.md) |
| 13 | `search-and-indexing` | Data and Database | Design search/indexing relevance, reindex, auth filtering | Index sync, relevance tuning, eventual consistency | [SKILL.md](skills/search-and-indexing/SKILL.md) |
| 14 | `security-review` | Security and Access | Review attack surfaces and abuse paths | Authz gaps, validation, secrets, dependency risk | [SKILL.md](skills/security-review/SKILL.md) |
| 15 | `authn-authz-and-secrets` | Security and Access | Design authn/authz, identity propagation, secret rotation | Identity, RBAC/ABAC, least privilege, secret lifecycle | [SKILL.md](skills/authn-authz-and-secrets/SKILL.md) |
| 16 | `messaging-and-eventing` | Messaging and Platform | Design queues/topics/events, ordering, DLQ, replay | Events, pub/sub, outbox/inbox, idempotent consumers | [SKILL.md](skills/messaging-and-eventing/SKILL.md) |
| 17 | `api-gateway-and-service-integration` | Messaging and Platform | Design gateway/BFF routing and service integrations | API gateway, protocol translation, auth propagation | [SKILL.md](skills/api-gateway-and-service-integration/SKILL.md) |
| 18 | `rate-limiting-and-traffic-control` | Messaging and Platform | Design throttling, quotas, fairness, abuse protection | Rate limiting, backpressure, graceful rejection | [SKILL.md](skills/rate-limiting-and-traffic-control/SKILL.md) |
| 19 | `workflow-and-job-orchestration` | Messaging and Platform | Orchestrate long-running workflows, saga, compensation | Workflow state, approvals, compensation, resumability | [SKILL.md](skills/workflow-and-job-orchestration/SKILL.md) |
| 20 | `background-jobs-and-batch-processing` | Messaging and Platform | Design scheduled jobs/batches with checkpoint and retry | Chunking, retries, duplicate prevention, observability | [SKILL.md](skills/background-jobs-and-batch-processing/SKILL.md) |
| 21 | `resilience-and-fault-tolerance` | Resilience and Performance | Apply timeouts/retries/circuit breakers/degradation | Failure containment, failover, recovery patterns | [SKILL.md](skills/resilience-and-fault-tolerance/SKILL.md) |
| 22 | `caching-and-distributed-state` | Resilience and Performance | Design cache correctness, TTL, invalidation, locks | Staleness rules, key scope, stampede controls | [SKILL.md](skills/caching-and-distributed-state/SKILL.md) |
| 23 | `performance-engineering` | Resilience and Performance | Improve latency/throughput based on profiling evidence | Profiling, capacity, concurrency, cost-aware tuning | [SKILL.md](skills/performance-engineering/SKILL.md) |
| 24 | `logging-metrics-and-tracing` | Observability and Ops | Design structured telemetry and redaction | Structured logs, metrics, traces, correlation IDs | [SKILL.md](skills/logging-metrics-and-tracing/SKILL.md) |
| 25 | `monitoring-alerting-and-slos` | Observability and Ops | Define SLI/SLO, actionable alerts, runbook ownership | Alert quality, burn rates, error budgets | [SKILL.md](skills/monitoring-alerting-and-slos/SKILL.md) |
| 26 | `observability-and-sre` | Observability and Ops | Drive production readiness and operational ownership | Supportability, runbooks, game-day readiness | [SKILL.md](skills/observability-and-sre/SKILL.md) |
| 27 | `devops-and-release` | Observability and Ops | Design CI/CD, rollout, feature flags, rollback safety | Release orchestration, migration coordination | [SKILL.md](skills/devops-and-release/SKILL.md) |
| 28 | `file-and-object-storage` | Storage and Search | Design file/object storage, signed URLs, retention, scanning | Upload/download flows, metadata, legal hold | [SKILL.md](skills/file-and-object-storage/SKILL.md) |
| 29 | `dotnet-development` | Stack Specific | ASP.NET Core/EF Core implementation guidance | Layering, middleware, async/cancellation, DTOs | [SKILL.md](skills/dotnet-development/SKILL.md) |
| 30 | `java-spring-boot-development` | Stack Specific | Spring Boot service implementation guidance | Controllers/services/repos, JPA, transactions | [SKILL.md](skills/java-spring-boot-development/SKILL.md) |
| 31 | `reactjs-development` | Stack Specific | React web app implementation guidance | Components/hooks/state/forms/API integration | [SKILL.md](skills/reactjs-development/SKILL.md) |
| 32 | `angular-development` | Stack Specific | Angular structure, RxJS, forms, guards guidance | Feature modules, services, interceptors, testability | [SKILL.md](skills/angular-development/SKILL.md) |
| 33 | `react-native-development` | Stack Specific | React Native iOS/Android implementation guidance | Navigation, permissions, offline, performance | [SKILL.md](skills/react-native-development/SKILL.md) |

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

