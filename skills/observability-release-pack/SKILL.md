---
name: observability-release-pack
description: 'Use when designing logs/metrics/traces, SLIs/SLOs, dashboards, alerts, runbooks, production readiness, CI/CD, rollouts, feature flags, rollback, or migration release safety.'
---
# Observability and Release Pack

This pack carries TWO orthogonal axes — **telemetry/SRE** (vertical) and **release/delivery** (horizontal). Pick references along the axis the prompt is on.

## When to Use
- Structured logs, metrics, traces, correlation IDs, redaction, telemetry cardinality, trace propagation.
- SLIs, SLOs, burn-rate alerts, dashboards, severity, ownership, runbooks, on-call readiness, game days.
- CI/CD, environment promotion, secrets in pipelines, feature flags, canary/blue-green/progressive delivery, migration sequencing, rollback, SLO-gated rollout.

## When NOT to Use
- DB-specific migration mechanics (expand-contract DDL, restore drill) → `data-database-analytics-pack` → `database-reliability-and-operations`.
- Identity/secret design itself → `security-access-pack` → `authn-authz-and-secrets`.
- Resilience PATTERNS (timeouts, circuit breaker) → `resilience-performance-pack`.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `logging-metrics-and-tracing` | Use when defining structured log fields, metric names/cardinality, trace span model, redaction rules, or correlation-ID propagation. |
| `monitoring-alerting-and-slos` | Use when defining SLIs/SLOs, burn-rate alerts, severity, ownership, runbook links, or alert routing. |
| `observability-and-sre` | Use when planning production readiness, on-call ownership, game day, or end-to-end observability story across owners. Delegates detail to the two siblings above. |
| `devops-and-release` | Use when designing CI/CD stages, deployment topology (rolling/blue-green/canary/progressive), feature flags, GitOps, signing, rollout gates, or rollback drills. |
| `incident-response-and-postmortem` | Use when designing on-call response, severity classification, comms protocol, blameless postmortem, action-item tracking, or learning loops for production incidents. |

## Cross-Pack Handoffs
- → `core-engineering-pack` for cloud architecture / AWS service selection / Well-Architected reviews (`aws-cloud-architecture`).
- → `data-database-analytics-pack` for migration sequencing and restore drills.
- → `platform-integration-pack` for DLQ/lag dashboards and consumer-repair runbooks.
- → `resilience-performance-pack` for SLO-driven degradation and capacity gates.
- → `security-access-pack` for sensitive-log masking, audit events, and secret rotation in pipelines.

