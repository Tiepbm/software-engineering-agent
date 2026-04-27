---
name: solution-architecture
description: 'Designs pragmatic solution architecture across application, integration, data, delivery, team ownership, cost, and operations while controlling complexity and trade-offs.'
---

# Solution Architecture

## Description

Designs pragmatic solution architecture across application, integration, data, delivery, team ownership, cost, and operations while controlling complexity and trade-offs.

## Purpose

- Choose an architecture shape that fits business goals, constraints, team capability, data ownership, and time-to-market.
- Make trade-offs explicit across monolith, modular monolith, microservices, managed services, vendor products, integration platforms, buy, and build.
- Prevent architecture from becoming either vague diagrams or unnecessary distributed systems work.

## When to Use

- A capability spans multiple systems, teams, vendors, databases, compliance boundaries, or deployment units.
- The team must decide between monolith vs modular monolith vs microservices, build vs buy, sync vs async integration, or managed vs self-operated platforms.
- The decision affects maintainability, operability, cost, security, scalability, delivery sequencing, or long-term ownership.
- The architecture needs explicit involvement from platform skills for messaging, caching, gateway integration, resilience, monitoring, object storage, search, or rate limiting.

## Responsibilities

- Define business capabilities, system context, ownership boundaries, integration contracts, data ownership, and delivery increments.
- Compare options against known constraints rather than architectural fashion.
- Identify the source of truth, consistency requirements, migration path, operational support model, and failure behavior.
- Control complexity by naming what is deliberately not being built in version 1.
- Produce decisions that can be implemented, tested, monitored, and revisited.
- Route deep reviews to related skills such as `messaging-and-eventing`, `caching-and-distributed-state`, `api-gateway-and-service-integration`, `resilience-and-fault-tolerance`, `monitoring-alerting-and-slos`, `security-review`, and `authn-authz-and-secrets` when those concerns drive the architecture.

## Decision Principles

- Prefer a modular monolith when one team owns the product, transactional consistency matters, independent deployment is not required, and scale is within one deployable's capacity.
- Use microservices only when independent ownership, independent scaling, deployment isolation, regulatory isolation, or fault isolation outweighs distributed-system cost.
- Prefer synchronous integration for request/response workflows that require immediate consistency and have reliable latency budgets.
- Prefer asynchronous integration for long-running work, fan-out, decoupled vendor interaction, buffering, or resilience when eventual consistency is acceptable.
- Buy commodity capabilities unless differentiation, data control, compliance, integration constraints, or total cost justify building.
- Use managed services when they reduce undifferentiated operations, but account for lock-in, pricing model, regional availability, quotas, and failure modes.
- For banking, insurance, and regulated workloads, treat auditability, data residency, segregation of duties, retention, vendor risk, and operational evidence as architecture constraints rather than after-the-fact compliance tasks.

## Expected Output Style

- Start with the recommended architecture shape and the constraints that drive it.
- Include at least three options: simplest viable option, recommended option, and one rejected higher-complexity option.
- Separate tactical release architecture from strategic target architecture.
- State data ownership, integration contracts, failure behavior, operating model, and cost implications.
- Provide a delivery sequence that proves the riskiest assumptions early.

## Architecture / Design Guidance

A useful architecture decision explains boundaries. Valid boundary reasons include business capability ownership, data consistency, security isolation, independent deployment, independent scaling, regulatory constraints, and team ownership. Invalid boundary reasons include matching every noun to a service, copying an org chart blindly, or hiding unclear requirements behind infrastructure.

For each option, evaluate:

- Business fit: user value, workflow coverage, time-to-market.
- Technical fit: coupling, cohesion, consistency, scale, latency, integration complexity.
- Data fit: source of truth, migration, audit, reporting, retention, privacy.
- Operational fit: monitoring, on-call, runbooks, backup/restore, failover, cost.
- Team fit: ownership, skills, cognitive load, release coordination.
- Change fit: likely future changes and what the design makes easy or hard.

For cross-cutting platform decisions, state whether the design needs eventing, orchestration, background jobs, gateway mediation, traffic shaping, shared cache, object storage, search indexing, or managed identity and secrets. Keep the solution architecture decision focused on boundaries and trade-offs, then call the specialized skill for detailed implementation rules.

## Implementation Guidance

- Start with a walking skeleton that exercises auth, one critical workflow, one persistence path, one integration path, deployment, logging, metrics, and rollback.
- Use ADRs for decisions with meaningful alternatives; include context, decision, rejected options, consequences, and revisit triggers.
- Define integration contracts before implementation: API schema, event schema, error behavior, retry policy, idempotency, and versioning.
- Define platform contracts early for cache invalidation, message ordering, gateway policies, object-storage lifecycle, search projection rebuilds, and SLO ownership when they affect the business capability.
- Put migration, observability, and release strategy in the first implementation slice, not after feature completion.
- Keep platform abstractions thin until two real use cases prove the abstraction shape.
- Define ownership for every runtime component and every data store before production.

## Testing Expectations

- Validate architecture with thin vertical slices before broad implementation.
- Use contract tests for service, vendor, and event boundaries.
- Run failure-mode tests for timeouts, retries, duplicate messages, unavailable dependencies, partial writes, and degraded modes.
- Prove migration, rollback or roll-forward, backup/restore, and operational dashboards before production cutover.
- Test non-functional assumptions: latency, throughput, concurrency, data volume, and deployment frequency.

## Security / Performance / Reliability Considerations

Security requires trust boundaries, identity propagation, resource-level authorization, secret handling, audit events, data classification, and evidence suitable for regulated change control. Performance requires latency budgets, bounded payloads, query budgets, cache rules, queue-lag budgets, dependency quotas, and capacity assumptions. Reliability requires failure-mode design, idempotency, retries with limits, backpressure, alerting, runbooks, disaster recovery expectations, and repair paths for asynchronous or externally visible side effects.

## Review Checklist

- The recommended architecture maps to business capabilities and team ownership.
- At least one simpler option and one rejected option are documented.
- Data ownership, consistency, retention, migration, and reporting impacts are explicit.
- Integration boundaries include contracts, retries, idempotency, versioning, and observability.
- Cross-cutting concerns identify which specialist skills must be involved and what decision remains owned by solution architecture.
- Operational ownership, cost model, and support burden are realistic.
- Delivery can proceed in increments that reduce risk early.
- The architecture avoids distributed complexity unless justified by concrete constraints.

## Anti-Patterns to Avoid

- Choosing microservices to appear modern without independent ownership or deployment need.
- Using a queue to avoid defining consistency, ordering, retry, or ownership.
- Sharing a database between services as an integration shortcut.
- Buying a platform without checking data export, rate limits, failure behavior, pricing, and support model.
- Building a generic platform before product workflows prove repeated needs.
- Designing for hypothetical global scale while ignoring today's team and operational maturity.
- Producing diagrams without rollout, monitoring, migration, and incident-response plans.
- Treating compliance, audit, resilience, observability, and secret handling as implementation details delegated after architecture approval.

## Gotchas / Common Failure Modes

- Service boundaries that split a transaction often create reconciliation and support workload.
- Vendor APIs become product dependencies; quotas, outages, data ownership, and contract changes matter.
- Managed services reduce some toil but add regional, quota, pricing, and lock-in constraints.
- A target architecture without an incremental path becomes shelfware.
- Platform teams can become bottlenecks when ownership and self-service boundaries are unclear.
- Event-driven designs move failures from user requests to operations; they still need repair workflows.
- Gateway, cache, and queue choices can become shared production choke points if quotas, ownership, and failure behavior are not agreed up front.
- The simplest architecture is not always the smallest codebase; it is the design with the lowest total delivery and operating risk for the constraints.

## ADR Template

Every non-reversible architecture decision should ship with a short ADR (Architecture Decision Record). Keep ≤ 1 page; one decision per ADR; immutable once accepted (supersede with a new ADR, do not edit history).

```markdown
# ADR-NNNN: <short imperative title, e.g. "Use Outbox Pattern for Payment Events">

- Status: Proposed | Accepted | Superseded by ADR-XXXX | Deprecated
- Date: YYYY-MM-DD
- Deciders: <names / roles>
- Consulted: <skills, teams>
- Stakeholders affected: <product, ops, security, data, partners>

## Context
What problem are we solving? What constraints (regulatory, performance, team, cost, time) are non-negotiable?
What forces are in tension (e.g. consistency vs availability, build vs buy, time-to-market vs operability)?

## Decision
We will <do X> because <Y>. State it as a single sentence a new engineer can understand in 30 seconds.

## Options Considered
| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| A. <chosen> | … | … | (selected) |
| B. … | … | … | … |
| C. Do nothing | … | … | … |

(At least 3 options including "do nothing" / status quo. No option = no decision.)

## Consequences
- Positive: what becomes easier, cheaper, safer.
- Negative: what becomes harder, more expensive, what we now own operationally.
- Neutral: what changes shape but is roughly equivalent.

## Compliance / Security / Data Impact
Audit, retention, residency, PII, regulated workflows touched. Owner of each control.

## Rollout & Reversal
- How we ship it (walking skeleton → expand-contract → cutover).
- How we reverse it if it fails (kill switch, feature flag, fallback path, time-to-reverse).
- Time horizon after which reversal becomes prohibitively expensive.

## Follow-ups
- Linked tickets, future ADRs, monitoring/SLOs to add, tech-debt acknowledged.
```

