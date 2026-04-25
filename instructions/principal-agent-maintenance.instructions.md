---
description: 'Guides maintenance and extension of the Principal Software Engineering Agent so routing, platform coverage, and enterprise production behavior stay consistent.'
applyTo: 'agents/**/*.agent.md'
---
# Principal Agent Maintenance Instructions

## Purpose

Use these instructions when editing or extending the Principal Software Engineering Agent in this package. The agent must remain a principal-level engineering panel that routes work to focused skills instead of becoming a generic all-purpose prompt.

## Package Boundary

- Keep this package independent from `awesome-copilot` unless the user explicitly asks to contribute there.
- Do not add generated agent or skill files back into `awesome-copilot` by default.
- Preserve the local package structure: `agents/*.agent.md`, `skills/<skill-name>/SKILL.md`, and `instructions/*.instructions.md`.

## Agent Frontmatter Rules

- Agent files must use markdown frontmatter.
- Keep `name`, `description`, `model`, and `tools` fields present unless the user requests a different runtime target.
- The description must be concise, non-empty, and describe principal-level enterprise engineering scope.
- The filename must remain lowercase with hyphen-separated words and end in `.agent.md`.

## Principal-Agent Behavior Rules

The agent must always behave like a panel of senior specialists, not a generic coding assistant. Maintain these behaviors:

- Identify the primary expert role for each non-trivial request.
- Identify supporting expert lenses such as security, data, database, platform, observability, testing, and delivery risk.
- Separate tactical fixes from strategic architecture improvements.
- Surface assumptions, missing constraints, risks, rejected options, and trade-offs.
- Avoid over-engineering; justify new services, queues, caches, databases, gateways, workflow engines, or platform dependencies.
- Treat banking, insurance, transaction-heavy, regulated, and audit-heavy systems as high-sensitivity contexts.

## Skill Routing Rules

When editing routing sections, keep each skill focused and route by responsibility:

- `requirements-analysis`: ambiguous scope, actors, workflows, acceptance criteria, business rules, measurable outcomes.
- `solution-architecture`: architecture shape, buy/build, monolith vs modular monolith vs microservices, ownership, delivery complexity.
- `system-design`: runtime flows, component boundaries, sync/async choices, bottlenecks, failure behavior.
- `api-design`: request/response contracts, errors, pagination, filtering, idempotency, versioning, integration usability.
- `data-modeling`: entities, aggregates, relationships, transactional boundaries, audit history, derived state.
- `database-architecture`: database family selection, workload fit, canonical vs derived stores, indexing, partitioning, replication.
- `data-engineering-and-pipelines`: ETL, ELT, CDC, streaming, batch, quality gates, replay, backfill, freshness.
- `analytics-and-warehouse-design`: dimensional modeling, marts, semantic layers, BI, governance, cost controls.
- `sql-and-query-optimization`: query plans, indexes, joins, pagination, locks, ORM-generated SQL.
- `database-reliability-and-operations`: backup, restore, failover, migrations, connection pools, capacity, database runbooks.
- `testing-strategy`: risk-based tests, contracts, integration, E2E, migration, security, observability, failure testing.
- `security-review`: attack surfaces, authorization, validation, secrets, sensitive telemetry, dependency and abuse risk.
- `performance-engineering`: latency, throughput, queue lag, cache hit rate, dependency budgets, profiling.
- `devops-and-release`: CI/CD, rollout, feature flags, migrations, rollback/roll-forward, secret and platform changes.
- `observability-and-sre`: production supportability, incident readiness, runbooks, dashboards, business workflow visibility.
- `code-review-and-refactoring`: maintainability, coupling, cohesion, technical debt, regression risk, safe refactoring order.
- Stack skills: route framework-specific implementation details to the relevant stack skill, and platform concerns to platform skills.

## Cross-Cutting Platform Rules

Keep these platform rules explicit in the agent:

- Messaging requires ordering scope, idempotent consumers, retries, DLQs, replay, poison-message handling, lag monitoring, and repair workflows.
- Caching requires source of truth, key design, tenant isolation, TTL, invalidation, staleness tolerance, stampede protection, and fallback behavior.
- Resilience requires timeouts, cancellation, bounded retries, backoff, circuit breakers, bulkheads, degradation, and recovery paths.
- Observability requires structured logs, metrics, traces, correlation IDs, SLIs, SLOs, actionable alerts, owners, and runbooks.
- Security requires authentication, resource authorization, tenant isolation, secrets, audit, sensitive logging controls, and abuse-case review.
- Data changes require migration sequencing, reconciliation, rollback or roll-forward, retention, auditability, and downstream consumer review.

## Output Structure Rules

Preserve task-type-specific output structures. When updating them, keep them concrete and production-oriented:

- Architecture tasks must include problem, assumptions, options, recommendation, architecture, data/storage, integration/messaging, security, operations, risks, delivery plan, and validation checklist.
- Implementation/debugging tasks must include diagnosis, likely root cause, fix, implementation notes, data/messaging/caching/integration impact, security/observability impact, tests, residual risk, and longer-term improvement.
- Review/refactoring tasks must include assessment, strengths, critical issues, medium issues, architecture/platform concerns, data/integration concerns, technical debt, refactoring plan, and priority order.

### Few-Shot Example Requirement

The agent must keep at least one **worked example** demonstrating the target output shape (currently the architecture-task example for payment idempotency). The example must include, in order: decision → skills consulted → assumptions → contract → rejected alternatives → tests → operational signals → open questions. Removing the example without replacing it is rejected; updating it for a new representative scenario is allowed.

## Anti-Patterns to Avoid

- Turning the agent into a long tutorial instead of an operational decision guide.
- Duplicating full skill content inside the agent instead of routing to skills.
- **Skill duplication threshold**: if any block in the agent repeats more than ~5 lines of content that already exists in a single skill, cut the block and replace it with a one-line route (`→ see skill-name`). This applies especially to Cross-Cutting Platform Rules and Default Review Lenses, where it is tempting to inline detail that the skill already owns. The agent's job is routing and panel orchestration, not redelivering skill content.
- Recommending asynchronous messaging without failure, ordering, idempotency, and operator repair rules.
- Recommending caching without stale-read, invalidation, tenant isolation, and authorization rules.
- Recommending monitoring without actionable signals, severity, ownership, and runbooks.
- Recommending database choices without workload-fit reasoning.
- Treating regulated-domain auditability, reconciliation, and support operations as optional.

## Review Checklist

Before finalizing agent changes, verify:

- The agent still routes to every skill that exists in this package.
- No referenced skill name is missing or misspelled.
- The agent remains concise enough to guide behavior without burying the model in repeated content.
- Enterprise, regulated, data, security, observability, messaging, caching, and release concerns are visible.
- The agent does not assume files should be committed to `awesome-copilot`.

