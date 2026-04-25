---
name: observability-and-sre
description: 'Coordinates production supportability, ownership, runbooks, game days, and business workflow visibility while delegating telemetry, alerting, and resilience detail to specialist skills.'
---

# Observability and SRE

## Description

Orchestrator skill for **production supportability**: who owns what when it breaks, whether the system is launch-ready, and whether business workflows are visible to operators. **Intentionally lean** — all technical detail lives in specialist skills.

## When to Use

- Designing or reviewing the **overall production support story** for a service, integration, pipeline, or high-risk feature.
- Operability readiness gate before launch, or after repeated incidents detected by users instead of alerts.
- Deciding ownership across telemetry, alerts, dashboards, runbooks, and on-call.
- Post-incident review that needs to translate findings into telemetry / alert / test backlog.

If the question is **"what to instrument / alert / fall back to / how to log"** — route to the specialist below. If it is **"is this system production-ready and who owns what when it breaks"** — stay here.

## Skill Routing — Where Detail Lives

| Concern | Owning skill |
|---|---|
| Log fields, metric names, trace spans, correlation IDs, cardinality, redaction, propagation | `logging-metrics-and-tracing` |
| SLI formulas, SLO targets, alert rules, burn-rate, dashboards, runbook content, severity policy | `monitoring-alerting-and-slos` |
| Timeouts, retries, circuit breakers, bulkheads, fallback, graceful degradation | `resilience-and-fault-tolerance` |
| Messaging lag, DLQ depth, replay tooling | `messaging-and-eventing` |
| Job duration, missed schedules, checkpoint age | `background-jobs-and-batch-processing` |
| Pipeline freshness, data quality alerts | `data-engineering-and-pipelines` |
| Gateway error mapping, partner timeout budgets | `api-gateway-and-service-integration` |
| Sensitive telemetry redaction, audit events | `security-review`, `authn-authz-and-secrets` |

## Decision Principles

- Production readiness is a **set of owned commitments**, not a tool checklist.
- Every page must have an owner, severity, runbook, and expected human action.
- SLOs must tie to user-visible or business-critical outcomes; vanity SLOs waste error budget.
- Operability is a **launch gate**, not a post-launch upgrade.
- For banking, insurance, claims, policy, billing, payments: incident timelines must be reconstructable from telemetry **without leaking regulated data** and must answer — what failed, which segment was affected, is data correctness at risk, what repair is safe.

## Production-Ready Definition

A service is production-ready when it has:

1. Named **critical user journeys and business workflows** with owners.
2. SLI coverage per journey (spec → `monitoring-alerting-and-slos`).
3. Telemetry that propagates correlation across boundaries (spec → `logging-metrics-and-tracing`).
4. Alerts with owner + severity + runbook + expected action — no orphan pages.
5. Dashboards that answer "what changed, who is affected, what dependency is failing".
6. Runbooks **executed at least once** (game day or real incident), not only written.
7. On-call rotation with explicit handoff and escalation policy.
8. Failure-mode behavior designed in (spec → `resilience-and-fault-tolerance`).
9. Platform-dependency signals owned by the right team (queues, jobs, caches, search, storage, gateway, pipelines).
10. Post-incident learning loop that produces backlog items with owners.

## Expected Output Style

Produce **operability plans and gap reports**, not telemetry code. Typical shape:

- **Service / scope**
- **Critical journeys** (with owners)
- **Coverage matrix**: journey → SLI status / alert owner / runbook status / game-day status
- **Launch blockers** vs **post-launch improvements** (separated)
- **Specialist follow-ups**: which skill owns each technical decision

## Review Checklist

- Critical journeys named with owners.
- Each journey has SLI/SLO coverage (delegate spec).
- Every alert has owner, severity, runbook, expected action.
- Runbooks executed at least once.
- On-call + escalation policy exist.
- Telemetry correlation propagates across services, messaging, jobs (delegate spec).
- Platform-dependency signals owned by the right team.
- Post-incident actions tracked as backlog with owners.
- Regulated incidents reconstructable without leaking protected data.

## Anti-Patterns to Avoid

- Treating "we have logs / a dashboard / an alert" as observability.
- Alerts without owners, runbooks, or expected actions (orphan pages).
- Launching without production-readiness review and at least one game day.
- **Duplicating detail that belongs in `logging-metrics-and-tracing`, `monitoring-alerting-and-slos`, or `resilience-and-fault-tolerance`** — keep this skill focused on ownership and readiness.
- Building post-incident dashboards that still miss the signal that made the incident invisible.

## Gotchas / Common Failure Modes

- Operability gaps are usually **ownership gaps**, not tooling gaps — a perfect alert that pages nobody is worse than a manual check.
- Game days surface unowned alerts, broken runbook links, and missing escalation paths far cheaper than real incidents.
- Missing business workflow signals make payment / claim / policy / billing incidents invisible until customers or regulators report them.
- Telemetry pipeline outages hide the very evidence needed to debug — monitor the monitor.
- Runbooks that look complete but have never been executed usually fail at the first unfamiliar dependency or expired credential.

