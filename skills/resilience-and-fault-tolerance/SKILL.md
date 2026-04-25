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

