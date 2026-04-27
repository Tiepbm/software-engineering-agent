---
name: resilience-and-fault-tolerance
description: 'Designs resilient systems with timeouts, retries, backoff, circuit breakers, bulkheads, graceful degradation, failover, and failure containment.'
---

# Resilience and Fault Tolerance

## Description

Designs resilient systems with timeouts, retries, backoff, circuit breakers, bulkheads, graceful degradation, failover, and failure containment.

## Purpose

- Keep critical workflows operating predictably when dependencies are slow, unavailable, degraded, or inconsistent.
- Prevent retries, queues, jobs, and external integrations from amplifying failures.
- Define recovery behavior that is safe for transaction-heavy, regulated, banking, and insurance systems.

## When to Use

- A service depends on databases, APIs, queues, caches, file storage, search, partner systems, or third-party platforms.
- Production failures include timeouts, retry storms, cascading outages, stuck jobs, partial writes, or unclear fallback behavior.
- Designing high-value workflows such as payments, policy changes, claim processing, billing, onboarding, or document ingestion.

## Responsibilities

- Define timeout budgets, retry policies, circuit breaker behavior, bulkheads, fallback, degradation, and recovery paths.
- Identify critical dependencies, failure modes, blast radius, and containment boundaries.
- Ensure retry behavior is idempotency-aware and does not duplicate side effects.
- Define operator visibility, runbooks, and manual repair procedures for partial failures.

## Decision Principles

- Set timeouts on every remote call; no dependency call should wait forever.
- Retry only when the operation is safe, idempotent, or protected by an idempotency key.
- Use exponential backoff with jitter to avoid synchronized retry storms.
- Prefer graceful degradation for non-critical features and fail-closed for security or correctness-sensitive paths.
- Isolate dependencies with bulkheads when one slow dependency can exhaust shared resources.

## Expected Output Style

- State the failure mode being addressed and the recommended resilience control.
- Include timeout, retry, fallback, circuit breaker, and observability settings.
- Identify what happens to user-visible state and data consistency during failure.
- Separate automated recovery from manual repair.
- Explain trade-offs between availability, correctness, latency, and cost.

## Architecture / Design Guidance

Resilience architecture starts with dependency mapping. For each dependency, define criticality, expected latency, timeout, retry safety, fallback option, data consistency impact, and owner. Critical workflows need explicit state transitions for pending, failed, compensated, and manually reviewed states.

Circuit breakers protect callers from repeated dependency failure. Bulkheads isolate pools, queues, workers, and connection limits. Fallbacks must be business-safe; for example, cached product text may be acceptable, but cached authorization, account balance, or policy coverage may not be.

### Resilience Pattern Decision Matrix

| Pattern | When to use | Avoid when | Key parameters |
|---|---|---|---|
| **Timeout** | Every remote call (DB, HTTP, queue, cache, partner) — no exceptions | Never avoid; always set a timeout | Connect timeout (1–5s), read timeout (per-SLA), total budget from user request backward |
| **Retry with backoff** | Transient failures on idempotent operations; network blips, 503, connection reset | Non-idempotent operations without idempotency key; 4xx client errors; auth failures | Max attempts (2–4), base delay (100–500ms), jitter (±50%), exponential factor (2x) |
| **Circuit breaker** | Dependency with repeated failures; protect caller from wasting resources on a known-broken path | Single-request failures; very low traffic where the circuit never opens | Error threshold (50%+ in window), window (10–60s), half-open probe (1 req), recovery timeout (30–120s) |
| **Bulkhead** | Isolate expensive or unreliable dependencies from shared resources (thread pools, connection pools, queues) | All dependencies are equally critical and share the same failure mode | Pool size per dependency, queue depth, rejection policy (fail-fast vs queue-and-wait) |
| **Rate limiter (client-side)** | Protect downstream from burst; respect partner quotas; prevent retry storms | Already handled by server-side rate limiting with clear 429 + Retry-After | Permits/second, burst capacity, queue depth |
| **Fallback / degradation** | Non-critical features where stale or partial data is acceptable; read-only mode during write-path failure | Authorization, financial balance, policy coverage, claim status — correctness-critical data | Fallback source (cache, default, empty), staleness tolerance, user notification |
| **Hedging** | Latency-sensitive reads where redundant requests are cheap and safe (e.g., read from 2 replicas, take first) | Write operations; expensive operations; operations with side effects | Delay before hedge (p95 of normal latency), max concurrent hedges (2) |
| **Load shedding** | Protect system capacity under overload; prioritize critical traffic | All traffic is equally important; system is not near capacity | Priority classification, shed threshold (% of capacity), response (503 + Retry-After) |

### Timeout Budget Calculation

Calculate timeouts backward from the user-facing SLA:

```
User SLA: 2000ms (p99)
├── API gateway overhead: 50ms
├── Auth/validation: 50ms
├── Service logic: 100ms
├── Database query: 200ms (timeout = 300ms with margin)
├── External partner call: 800ms (timeout = 1000ms with margin)
├── Message publish: 50ms (timeout = 100ms)
└── Response serialization: 50ms
    Total budget used: 1300ms
    Remaining margin: 700ms (for retries, GC, network jitter)
```

Rules:
- Sum of all dependency timeouts must be **less than** the user-facing SLA.
- If retries are allowed, multiply: `timeout × (1 + max_retries)` must still fit the budget.
- Set `CancellationToken` / `AbortSignal` / deadline propagation so timed-out requests stop consuming downstream resources.

## Implementation Guidance

- Apply timeout budgets from user request deadline backward through all downstream calls.
- Use bounded retries with jitter and maximum attempts; include retry reason and attempt count in telemetry.
- Use idempotency keys for payment, claim, policy, billing, and external side-effect operations.
- Add circuit breakers for dependencies with repeated failures and define half-open probe behavior.
- Use separate worker pools or queues for high-priority and low-priority work.
- Define degraded responses explicitly: stale data, read-only mode, queued work, manual review, or user-facing error.

## Testing Expectations

- Test dependency timeout, connection refusal, partial response, slow response, invalid response, and intermittent failure.
- Test retry exhaustion, circuit open/half-open/closed transitions, and fallback behavior.
- Test duplicate prevention under retries and worker restarts.
- Test queue buildup, backpressure, and recovery after dependency restoration.
- Run game days for production-critical workflows.

## Security / Performance / Reliability Considerations

Security-sensitive operations should fail closed when authorization, identity, or policy checks are unavailable. Performance requires bounded retries, timeouts, and resource isolation. Reliability requires clear degraded modes, observable state transitions, runbooks, and recovery procedures.

## Review Checklist

- Dependencies and failure modes are identified.
- Every remote call has a timeout.
- Retries are bounded, jittered, and idempotency-safe.
- Circuit breakers and bulkheads protect shared resources where needed.
- Fallback behavior is business-safe.
- Operators can detect, mitigate, and repair partial failures.
- Critical workflows preserve auditability and data correctness.

## Anti-Patterns to Avoid

- Retrying non-idempotent operations without idempotency keys.
- Infinite retries or fixed-delay retries across many clients.
- Fallbacks that return incorrect financial, policy, permission, or claim state.
- Sharing one connection pool across critical and non-critical traffic.
- Treating failover as tested because the vendor claims it works.
- Hiding dependency failure behind success responses.

## Gotchas / Common Failure Modes

- Timeouts without cancellation still consume downstream resources.
- Retries can turn a small outage into a full incident.
- Circuit breakers can protect systems but also hide recovery if probe behavior is wrong.
- Fallback data can become a correctness bug when users make decisions from it.
- Partial writes require reconciliation and compensation, not just exception handling.
- Failover can expose DNS, connection pooling, and transaction replay issues.

