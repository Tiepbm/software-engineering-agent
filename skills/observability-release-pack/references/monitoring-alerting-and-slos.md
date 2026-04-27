---
name: monitoring-alerting-and-slos
description: 'Designs actionable monitoring, alerting, SLIs, SLOs, dashboards, error budgets, runbooks, and business workflow signals for production systems.'
---

# Monitoring Alerting and SLOs

## Description

Designs actionable monitoring, alerting, SLIs, SLOs, dashboards, error budgets, runbooks, and business workflow signals for production systems.

## Purpose

- Detect user-visible failures, data correctness issues, and operational risk before customers or regulators do.
- Convert telemetry into actionable alerts with owners, severity, runbooks, and expected response.
- Define SLOs that reflect business-critical workflows, not just infrastructure uptime.

## When to Use

- Designing service health monitoring, dashboards, alerts, SLIs, SLOs, error budgets, or incident readiness.
- Alerts are noisy, dashboards do not help during incidents, or failures are discovered by users.
- Monitoring must cover queues, jobs, data pipelines, partner integrations, banking transactions, claims, billing, policy changes, or document workflows.

## Responsibilities

- Define SLIs for availability, latency, correctness, freshness, durability, workflow completion, queue lag, and external dependency health.
- Create alerts that are actionable, owned, severity-classified, and linked to runbooks.
- Design dashboards for executive health, service health, dependency health, data pipeline health, and incident diagnosis.
- Control alert noise with deduplication, suppression, burn-rate alerts, and escalation policies.

## Decision Principles

- Alert on symptoms and customer or business impact before low-level causes.
- Every page must have an owner, runbook, severity, and expected action.
- Use SLOs for services and workflows that matter to users or operations; do not create vanity SLOs.
- Monitor correctness and freshness for data systems, not just availability.
- Prefer a small number of high-quality alerts over broad noisy coverage.

## Expected Output Style

- Define SLIs, SLO targets, alert rules, dashboards, owners, and runbook actions.
- Include both technical golden signals and business workflow signals.
- State thresholds, measurement windows, severity, and escalation path.
- Identify missing telemetry required before safe launch.
- Separate launch-blocking alerts from informational dashboards.

## Architecture / Design Guidance

Monitoring architecture should map critical user journeys and business workflows to signals. For APIs, track request rate, error rate, latency, saturation, and dependency failures. For messaging, track consumer lag, DLQ depth, retry rate, and oldest message age. For jobs, track schedule adherence, duration, completion, checkpoint age, and failed chunks. For data pipelines, track freshness, volume anomalies, quality failures, and reconciliation gaps.

In banking and insurance systems, monitor workflow correctness: successful payment settlement, claim intake completion, policy update propagation, document scan completion, billing batch completion, and reconciliation differences.

## Implementation Guidance

- Define SLI formulas with numerator, denominator, filters, source metric, window, and owner.
- Use multi-window burn-rate alerts for high-value SLOs where appropriate.
- Use severity levels tied to business impact: customer-impacting, data-loss risk, compliance risk, degraded dependency, or capacity risk.
- Add runbooks with triage steps, dashboards, common causes, rollback/mitigation, escalation, and customer/support communication guidance.
- Include synthetic checks only for critical flows and verify they represent real user behavior.
- Alert on missing data when absence of events is a failure, such as no billing batch completion or no claim ingestion for expected periods.

### SLI/SLO Definition Template

Use this template for every SLO. Missing fields = open question, not "default":

```markdown
## SLO: <Service/Journey Name> — <Signal Name>

**Owner**: <team / individual>
**Stakeholders**: <product, ops, support, compliance>

### SLI Definition
- **What it measures**: <user-visible outcome, e.g., "successful payment settlement">
- **Numerator**: <good events, e.g., "payment requests returning 2xx within 500ms">
- **Denominator**: <total valid events, e.g., "all payment requests excluding health checks">
- **Source metric**: <metric name, e.g., `http_request_duration_seconds{service="payments", status=~"2.."}`>
- **Measurement window**: <rolling 28 days / 7 days / calendar month>
- **Exclusions**: <synthetic checks, internal health probes, known maintenance windows>

### SLO Target
- **Target**: <e.g., 99.9% of requests succeed within 500ms over 28 days>
- **Error budget**: <e.g., 0.1% = ~43 minutes of total failure per 28 days>
- **Budget consumption rate that triggers action**: <e.g., 2% of budget consumed per hour = page>

### Alert Rules
| Alert | Condition | Severity | Owner | Action |
|---|---|---|---|---|
| Fast burn | >2% budget/hour for 5 min AND >5% budget/hour for 1 min | P1 (page) | <on-call team> | Triage → rollback or mitigate within 15 min |
| Slow burn | >1% budget/6h for 30 min | P2 (ticket) | <service owner> | Investigate within 4h; likely capacity or dependency drift |
| Budget exhausted | <10% remaining in window | P2 (ticket) | <service + product owner> | Freeze non-critical releases; prioritize reliability |

### Burn-Rate Alert Calculation

Multi-window burn-rate alerts reduce noise while catching both fast and slow degradation:

- **Fast burn**: burn_rate > (budget × 14.4 / window_hours) sustained for short window (5 min) AND confirmed over longer window (1 hour)
- **Slow burn**: burn_rate > (budget × 6 / window_hours) sustained for 30 min AND confirmed over 6 hours

Example for 99.9% SLO over 28 days (error budget = 0.1%):
- Fast burn threshold: error_rate > 14.4 × 0.1% = 1.44% for 5 min (confirmed over 1h)
- Slow burn threshold: error_rate > 6 × 0.1% = 0.6% for 30 min (confirmed over 6h)

### Dashboard Requirements
- Current SLI value (last 1h, 7d, 28d)
- Error budget remaining (% and absolute time)
- Burn rate trend (last 24h)
- Top error contributors (by endpoint, dependency, tenant)
- Dependency health signals

### Runbook Link
- **Runbook**: <link to runbook>
- **Last executed**: <date of last game day or real incident>
- **Common causes**: <top 3 historical root causes>
```

## Testing Expectations

- Test alert firing and routing before production launch.
- Test runbooks through game days or incident simulations.
- Validate dashboard usefulness during load tests, dependency failures, and deployment smoke tests.
- Verify SLI calculations against known incidents and historical traffic.
- Test alerts for queue lag, DLQ growth, job failure, data freshness, and reconciliation drift.

## Security / Performance / Reliability Considerations

Security requires restricted access to dashboards containing sensitive metadata and no PII in metric labels. Performance requires limiting high-cardinality metrics and dashboard queries that overload telemetry systems. Reliability requires monitoring the monitoring pipeline, alert delivery, escalation paths, and runbook availability.

## Review Checklist

- Critical user journeys and business workflows have SLIs.
- SLOs have owners, targets, windows, and error-budget meaning.
- Alerts are actionable and tied to runbooks.
- Dashboards answer what changed, who is affected, and what dependency is failing.
- Queue, job, pipeline, and integration failures are visible.
- Alert noise controls exist.
- Operators can mitigate before root cause is fully known.

## Anti-Patterns to Avoid

- Alerting on CPU alone while user workflows fail silently.
- Creating dashboards nobody owns or uses during incidents.
- Paging for non-actionable symptoms.
- Ignoring data freshness, queue lag, and batch completion.
- Using raw customer identifiers in metric labels.
- Treating green infrastructure as proof that business workflows are healthy.

## Gotchas / Common Failure Modes

- The most important production signal may be absence of expected events.
- Average latency hides tail latency that affects enterprise users and partners.
- Alert fatigue causes real incidents to be missed.
- Dashboards built after incidents often lack the missing signal from the incident.
- SLOs without ownership become reporting theater.
- Monitoring only the API misses failures in async processing and downstream reconciliation.

