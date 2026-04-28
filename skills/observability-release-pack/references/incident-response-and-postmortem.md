---
name: incident-response-and-postmortem
description: 'Use when designing on-call response, severity classification, comms protocol, blameless postmortem, action-item tracking, and learning loops for production incidents in regulated systems.'
---

# Incident Response and Postmortem

## Description

Production incidents are inevitable; *unmanaged* incidents are the failure. This reference covers the operational discipline of detecting, declaring, mitigating, communicating, and learning from incidents — including the blameless postmortem that turns each incident into durable improvement. For regulated systems (banking, insurance, payments) the postmortem is also part of the audit surface.

## Purpose

- Reduce mean time to mitigate (MTTM) by making roles, decisions, and comms scripted instead of improvised.
- Ensure customer-affecting incidents are detected and declared, not silently waited out.
- Create durable learning by separating *what happened* (timeline) from *why it happened* (contributing factors) and from *what we will change* (action items with owners).
- Give regulators and auditors traceable evidence of what was affected, who was notified, what was done, and when.

## When to Use

- Designing or revising on-call rotation, escalation, runbooks, or severity classification.
- Standing up an incident-management process from scratch.
- After a customer-affecting outage, money-movement defect, regulated data exposure, or sustained SLO burn.
- Designing the integration between alerts, on-call paging, comms channels, status page, and incident tracker.
- Defining KPIs that measure operational health beyond uptime (MTTD, MTTM, repeat-incident rate, action-item completion).

## Severity Matrix

| Severity | Customer impact | Examples | Page on-call? | Exec / regulator notify? |
|---|---|---|---|---|
| **SEV-1** | Major outage / money-movement defect / regulated-data exposure | Payments down for all tenants; PII leak; ledger desync; auth fully broken | Immediate, page primary + secondary | Yes — exec channel within 15 min; regulator within contractual SLA |
| **SEV-2** | Significant degradation for a class of customers | One region down; one product offline; SLO burn > 4× for > 30 min | Immediate, page primary | Exec channel notify; regulator only if customer-affecting > threshold |
| **SEV-3** | Minor user-visible defect or near-miss | Slow page on one route; partial degradation auto-mitigated | During business hours | Internal only |
| **SEV-4** | No customer impact but operationally notable | Failed deploy auto-rolled back; latent bug found in tests | None (next business day) | Internal note |

Severity must be **declared explicitly**, recorded, and re-evaluated at least every 30 minutes during the incident.

## Roles (must be named, not implicit)

- **Incident Commander (IC)** — owns the incident, makes decisions, controls comms cadence. Does NOT debug. Hands off if shift expires or fatigue sets in.
- **Operations Lead (Ops)** — drives the technical investigation and remediation; reports to IC.
- **Communications Lead (Comms)** — owns external (status page, customer email, regulator) and internal (exec channel, support) updates. Frees IC from typing.
- **Scribe** — keeps the timeline (UTC, with source) in real time. Without a scribe, the postmortem fabricates the timeline.
- **Subject-matter experts (SMEs)** — pulled in by IC as needed; released when no longer required. Avoid the "everyone watching" anti-pattern.

For SEV-3+, the IC and Ops can be the same person; for SEV-1/2 they MUST be different.

## Lifecycle

1. **Detect** — alert fires, customer reports, or operator observes. MTTD = detect minus first symptom.
2. **Declare** — open the incident channel/ticket, assign IC, set initial severity. Declaration starts the clock for SLAs and comms.
3. **Triage** — Ops forms the leading hypothesis; IC decides whether to mitigate or investigate first. Default: **mitigate first** (rollback, flag off, drain traffic) and investigate after stability.
4. **Mitigate** — restore customer service even if root cause is unknown. Acceptable mitigations include rollback, feature flag off, traffic shed, failover, manual intervention. MTTM = mitigation minus declaration.
5. **Communicate** — Comms updates internal + external on a fixed cadence (every 30 min for SEV-1, every 60 min for SEV-2) even if the message is "no change yet". Silence is worse than no progress.
6. **Resolve** — declare the customer-visible incident over; downgrade severity. Post a final external update.
7. **Postmortem** — schedule within 5 business days; publish within 10. Owner = IC unless reassigned.

## Comms Protocol

- **Internal channel** (Slack/Teams): one channel per incident, never reused. Pin the IC, severity, and current hypothesis at the top.
- **Status page**: required for SEV-1/2. Publish within 15 min of declaration with what is known. Update on cadence. Resolve when customer impact ends, not when ticket closes.
- **Customer comms**: scripted templates per severity; legal/compliance approval path defined in advance (not negotiated during the incident).
- **Regulator**: SLA-driven; templates and contacts pre-loaded. For payments and PII-bearing incidents this is non-negotiable.
- **Exec / leadership**: separate channel; updates from Comms (NOT from IC). Execs do NOT debug.

## Mitigation-First Discipline

The following are valid mitigations even before root cause is known:

- Rollback to last known-good build (single click; pre-tested).
- Feature flag OFF for the affected code path.
- Traffic shedding / rate-limit hardening.
- Region failover or DNS cutover (only if drilled).
- Manual data correction with audit trail (financial systems; requires authorized operator).
- Read-only mode (regulated systems may degrade to read-only rather than corrupt write state).

If mitigation is not available, the incident has a *latent process defect* — log it as an action item.

## Postmortem Discipline (Blameless)

The postmortem is **about systems, not people**. Names appear only in the timeline (who did what when), never in the analysis ("operator X made a mistake"). The right framing is "the system permitted this mistake".

### Postmortem Template

```markdown
# Postmortem: <incident-id> — <one-line summary>

- **Date / duration**: YYYY-MM-DD HH:MM UTC, lasted X min
- **Severity**: SEV-N
- **Customer impact**: who, how many, what they saw, money/data implications
- **Detection**: alert / customer report / operator. MTTD = X min
- **Mitigation**: what restored service. MTTM = X min
- **Status**: Mitigated | Resolved | Action items in progress

## Timeline (UTC)
- HH:MM — first symptom (source: metric / log / report)
- HH:MM — alert fired
- HH:MM — incident declared, IC = <name>
- HH:MM — hypothesis 1: …
- HH:MM — mitigation A applied: <effect>
- HH:MM — service restored
- HH:MM — incident resolved

## Contributing Factors
Distinguish trigger (what fired the failure today) from latent conditions (what made the system fragile).
- Trigger: …
- Latent: missing alert, missing rollback, missing test, missing runbook, missing capacity, brittle dependency, etc.

## What Went Well
Genuine positives — alert worked, runbook was correct, comms cadence held. Reinforces good behaviour.

## What Went Poorly
- Detection gap (e.g. SLO did not trigger because cardinality was wrong).
- Comms gap.
- Mitigation gap (e.g. rollback untested).
- Decision gap (e.g. waited too long to declare).

## Action Items (owners + due dates required)
| ID | Type | Action | Owner | Due | Tracking |
|---|---|---|---|---|---|
| AI-1 | detect | Add SLO burn-rate alert on X | @sre-team | YYYY-MM-DD | JIRA-… |
| AI-2 | mitigate | Drill the failover quarterly | @ops | YYYY-MM-DD | JIRA-… |
| AI-3 | prevent | Make schema migration expand-contract by default | @platform | YYYY-MM-DD | JIRA-… |

Action items WITHOUT an owner and a due date do not exist.
```

### Action-Item Discipline

- Every action item has a single owner (a person, not a team) and a due date.
- Action items are tracked in the same backlog as feature work and prioritized accordingly. "Postmortem backlog" that lives in a doc no one reads is an anti-pattern.
- Repeat incidents are tagged; if the same contributing factor appears twice, the corresponding action item is escalated as P0.
- Quarterly review of completed vs aged-out action items; aged-out items either get re-prioritized or are explicitly closed with rationale.

## Operational Metrics

- **MTTD** (mean time to detect) — gap between first symptom and alert.
- **MTTM** (mean time to mitigate) — gap between declaration and customer impact ending.
- **MTTR** (mean time to resolve) — declaration to incident closure.
- **Repeat-incident rate** — % of incidents whose contributing factors match a previous incident.
- **Action-item completion within SLA** — % of postmortem actions closed by due date.
- **% of SEV-1/2 with completed postmortem within 10 business days**.

Report these monthly to engineering leadership; they are leading indicators of operational maturity.

## Common Failure Modes

- **No declared severity** — team debates urgency while customers suffer. Fix: severity is declared on first message in the channel.
- **IC also debugging** — quality of decisions collapses. Fix: hand off Ops role.
- **Mitigation skipped in favour of root cause** — extends customer impact for engineering curiosity. Fix: mitigation-first norm.
- **Postmortem becomes finger-pointing** — destroys the learning loop. Fix: blameless framing enforced by the IC; postmortem reviewer rejects person-blame language.
- **Action items without owners / due dates** — nothing changes. Fix: review template and reject incomplete entries.
- **Comms gap** — customers hear from Twitter before the status page. Fix: status page within 15 min of SEV-1/2 declaration, hard rule.

## Regulated-Domain Additions

For banking, insurance, payments, PII-bearing systems:

- Regulator notification SLA is contractual; templates and contacts are pre-loaded.
- Money-movement incidents require a reconciliation step in the postmortem (what was paid/reversed/duplicated, evidence query attached).
- Data-exposure incidents require DPO/legal involvement from declaration; comms approval path is mandatory, not optional.
- Postmortem is part of the audit trail and retained per regulator requirement (typically 7 years).
- Preserve forensic evidence: do NOT delete logs, snapshots, or message traces during mitigation; capture them.

## See Also

- `monitoring-alerting-and-slos` — SLO burn-rate alerts that drive timely detection.
- `observability-and-sre` — production-readiness that prevents incidents.
- `devops-and-release` — release safety and tested rollback as primary mitigation.
- `security-review` — required for any incident with security or PII implications.

