---
name: cost-and-finops
description: 'Use when reasoning about cloud and runtime cost: workload sizing, unit economics, cost attribution, savings plans, FinOps governance, and architectural trade-offs that move money — not just latency.'
---

# Cost and FinOps

## Description

Cost is a non-functional requirement. Architecture decisions, query patterns, retention policies, and cache behaviour all change the monthly bill — and many of them silently. This reference covers the FinOps loop (inform → optimize → operate), unit economics, attribution, common cloud cost traps, and the architectural choices where cost should be a first-class trade-off alongside latency, durability, and security.

For regulated systems, cost discipline is also a control: unbounded data growth becomes an audit/retention problem, and unbounded compute becomes a denial-of-wallet attack surface.

## Purpose

- Make cost a visible, reviewable engineering decision rather than a finance surprise.
- Define unit economics (cost per request / per tenant / per transaction) so capacity planning is grounded.
- Catch the small set of architecture patterns that cause 80 % of cloud cost surprises.
- Treat cost as a *correctness* property (e.g. unbounded queues, runaway retries, log cardinality explosions are cost defects, not just performance defects).

## When to Use

- Sizing a new workload or planning growth (5x, 10x, regional expansion).
- Reviewing the monthly cloud bill against forecast; investigating a cost anomaly.
- Proposing a new component that introduces a per-request, per-GB, per-call, or always-on charge.
- Designing data retention, log/metric cardinality, backup, or disaster-recovery posture.
- Deciding between managed vs self-hosted, on-demand vs reserved/savings plan, or single-region vs multi-region.
- Adding a public surface that bills cloud per request without rate-limit / authz protection (denial-of-wallet risk).

## FinOps Loop

| Phase | Question | Output |
|---|---|---|
| **Inform** | Where does the money go? | Cost-per-team / per-service / per-tenant dashboard; tagging coverage; unit economics. |
| **Optimize** | What is the cheapest correct shape? | Right-size, retire, refactor, change pricing model (RI/SP), change architecture. |
| **Operate** | Who owns ongoing discipline? | Budgets, alerts, monthly review, anomaly detection, FinOps champion per team. |

Skipping any phase produces failure modes: Inform alone produces dashboards no one acts on; Optimize alone produces unrepeatable savings; Operate alone produces governance theatre with no cost reduction.

## Unit Economics

Define and publish at least one unit-economic metric per service:

- $ per 1k requests (synchronous APIs).
- $ per active tenant per month (multi-tenant SaaS).
- $ per transaction processed (payments, claims, policies).
- $ per GB stored or per GB egressed (storage / streaming).
- $ per ML inference (model serving).

Unit economics make scaling decisions concrete. "We are at $0.012 per payment, target is $0.005 by Q4" is reviewable. "Reduce cloud cost" is not.

## Attribution and Tagging

- Mandatory tags on every cloud resource: `cost-center`, `team`, `service`, `environment`, `tenant-class` (e.g. `internal`, `paid`, `free`, `partner`).
- Tagging coverage > 95 % is the precondition for everything else; below that, attribution is fiction.
- Untagged spend is owned by the platform team by default — they will police it.
- For multi-tenant systems, attribute shared resources (DB, cache, broker) by usage proxy (CPU-seconds, calls, GB) and publish per-tenant cost; this is also the input to per-tenant pricing.

## Pricing-Model Choices

| Model | When | Risk |
|---|---|---|
| **On-demand** | Bursty, unpredictable, dev/test, < 12-month workloads. | Highest unit cost in steady state. |
| **Reserved Instances / Savings Plans (1y or 3y)** | Steady-state workloads with > 6-month forecast. | Lock-in to instance family / region; under-utilization wastes the commitment. |
| **Spot / preemptible** | Stateless, idempotent, restartable workloads (batch, CI, async workers). | Eviction; do NOT use for stateful or latency-critical paths. |
| **Serverless (Lambda, Cloud Run, Functions)** | Spiky low-RPS, glue, infrequent jobs. | Per-invocation cost dominates above modest steady RPS; cold start. |
| **Provisioned managed services (Aurora I/O-optimized, DynamoDB on-demand vs provisioned)** | Read/write pattern matches the model. | Wrong model can be 2–5× more expensive at the same workload. |

Rule of thumb: **measure first, commit second**. Buy reservations / savings plans only against ≥ 3 months of stable utilization data, never against forecasts.

## High-Impact Cost Traps

These cause most "where did our cloud bill go" incidents:

- **Cross-AZ / cross-region egress** at chatty service-to-service or DB-to-app paths. Co-locate, batch, or compress.
- **NAT gateway data processing** at high egress volumes — VPC endpoints / PrivateLink can be order-of-magnitude cheaper.
- **Unbounded log volume and high-cardinality metrics** (per-user-id labels, per-request-id metrics). Logging and observability bills frequently exceed compute.
- **Overprovisioned databases** with peak-sized always-on capacity for workloads with 10× off-peak. Use serverless DB tiers or scaled read replicas.
- **Snapshot / backup retention** never reviewed; backups silently outgrow primary storage.
- **Old environments** (sandbox, ephemeral, demo) left running 24×7. Auto-shutdown on schedule.
- **Unattached resources** — EBS volumes, ENIs, load balancers, NAT, IPs that survived a teardown. Continuous resource hygiene scan.
- **N+1 over the network** at scale — same anti-pattern as DB N+1 but with per-call API/cloud charges.
- **Object storage class mismatch** — keeping cold data on Standard or hot data on Glacier (retrieval cost is brutal).
- **Retry storms** — unbounded retries multiply both load and per-call cost. Cap and back off.
- **Public endpoints without authz / rate limits** — denial-of-wallet via scraped public APIs, signed URL leakage, or runaway image transformations.

## Architectural Trade-Off Cheat Sheet

| Decision | Cheap option | Expensive option | When the expensive one is correct |
|---|---|---|---|
| Multi-region | Single region with backup | Active-active multi-region | Regulatory / RTO < minutes / global low-latency reads |
| Cache | None / per-instance memory | Distributed cache cluster | Hot reads dominate AND staleness is bounded |
| Streaming | Batch nightly | Real-time stream | Decision latency materially changes business value |
| ML serving | CPU + smaller model | GPU + large model | Quality lift > cost AND latency budget allows |
| DB | Single primary + read replica | Multi-master / global | True multi-region writes required (rare) |
| Compute | Auto-scaled containers | Always-on reserved fleet | Latency-critical with no cold-start tolerance AND high utilization |

For each, force the question: *what changes in customer behaviour or revenue if we pick the cheap option?* If the answer is "nothing measurable", pick the cheap option.

## Cost as a Correctness Property

Several engineering anti-patterns are best caught as **cost defects** because they are silent in correctness:

- A retry loop without a budget burns money proportional to dependency outage length.
- A log statement at high cardinality (e.g. one log per request × per field) inflates ingestion cost linearly with traffic.
- A cache TTL of 0 or a missing cache key turns the cache into a pass-through.
- A search index that re-indexes everything on every change instead of incremental updates.
- A backup job that never deletes; a snapshot job with no retention policy.
- A scheduled job that runs every minute when hourly would suffice.

Treat each as a defect with an owner and a fix, not as "cloud is expensive".

## Governance Operating Model

- **Budgets per cost center** with monthly forecast vs actual; owners notified on > 10 % deviation.
- **Anomaly alerts** on daily spend by service / by tag (cloud-native or third-party FinOps tooling).
- **Monthly cost review** by engineering leadership; standing agenda: top movers, top spenders, action items.
- **Per-team FinOps champion** — engineer who owns cost discipline for their service; rotates quarterly.
- **Pre-merge cost review** for changes that introduce a new managed service, change retention, or change pricing model. The PR description states the expected monthly impact.
- **Pre-launch cost review** for new public surfaces (denial-of-wallet check) — required before exposing a new endpoint that bills per-call.

## Reporting Cadence

| Cadence | Output | Owner |
|---|---|---|
| Daily | Anomaly alerts on > N % daily spend deviation | Platform / FinOps |
| Weekly | Top movers (services with biggest week-over-week change) | Per-team owner |
| Monthly | Forecast vs actual per cost center; unit economics trend | Engineering leadership |
| Quarterly | Reservation / savings plan review; commitment utilization | FinOps lead |

## Regulated-Domain Additions

- **Retention vs cost**: regulators set minimums (often 7 years for financial records); cost optimization must respect these floors. Tier into archive storage classes rather than delete.
- **Audit logs** are NOT optional cost-cutting targets; they are part of the control plane.
- **Cross-border egress** can have legal implications (data residency) in addition to cost; cost optimization must not move regulated data across jurisdictions silently.
- **Disaster recovery** spend (DR site, backups, drills) is part of regulatory requirement; budget separately and protect from cost-cutting reviews that look only at production traffic.

## Common Failure Modes

- "Cost is finance's problem" — engineering owns the levers; finance only sees the bill.
- Unit economics absent — every cost discussion is qualitative and unactionable.
- Tagging coverage < 80 % — attribution is fiction; budgets cannot be enforced.
- Buying reservations on forecasts instead of measured utilization — common cause of wasted commitment.
- One-time savings projects with no operating model — savings regress within 2 quarters.
- FinOps tooling deployed but no human owner — dashboards no one reads.

## Anti-Patterns

- "Cloud is expensive, let's go on-prem" — without measured TCO including operations.
- Cost spike → first reaction is "scale up the team" instead of "find the unit-economic regression".
- Optimizing the smallest cost line while ignoring the largest (premature optimization in cost form).
- Removing observability to save money — observability cost is the cost of being able to operate; cut cardinality, not coverage.

## See Also

- `performance-engineering` — capacity planning and queueing math drive sizing decisions that determine cost.
- `caching-and-distributed-state` — caching is a cost lever as much as a performance lever.
- `database-architecture` — DB family and topology choice is one of the largest cost levers.
- `observability-and-sre` — telemetry cardinality is one of the largest hidden cost lines.

