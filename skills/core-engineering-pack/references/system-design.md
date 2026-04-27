---
name: system-design
description: 'Designs production system boundaries, components, runtime flows, state ownership, sync and async interactions, scalability, resilience, bottlenecks, and failure behavior.'
---

# System Design

## Description

Designs production system boundaries, components, runtime flows, state ownership, sync and async interactions, scalability, resilience, bottlenecks, and failure behavior.

## Purpose

- Turn a capability into a runtime design with clear components, state ownership, data flow, interactions, and operational behavior.
- Identify bottlenecks, consistency boundaries, failure modes, and scalability limits before implementation.
- Make synchronous, asynchronous, cached, replicated, and degraded paths explicit enough to test and operate.

## When to Use

- Designing a new service, subsystem, workflow engine, integration flow, event pipeline, high-traffic endpoint, or background processing system.
- A system has unclear ownership, excessive coupling, unreliable dependencies, slow workflows, hidden shared state, or hard-to-debug incidents.
- The team needs a design review before committing to implementation or splitting components.
- The design crosses platform concerns such as messaging, caching, background jobs, orchestration, gateway integration, search projections, object storage, monitoring, resilience, or traffic control.

## Responsibilities

- Define component responsibilities, ownership, dependency direction, and deployment boundaries.
- Map request flows, event flows, state transitions, data mutations, retries, timeouts, cancellation, and failure states.
- Identify source of truth, derived state, caches, queues, idempotency keys, and repair workflows.
- Specify scalability constraints: throughput, concurrency, fan-out, queue depth, storage growth, hot partitions, and external quotas.
- Define observability and operational controls for critical workflows.
- Involve related skills such as `messaging-and-eventing`, `background-jobs-and-batch-processing`, `workflow-and-job-orchestration`, `caching-and-distributed-state`, `resilience-and-fault-tolerance`, `logging-metrics-and-tracing`, and `monitoring-alerting-and-slos` when the system depends on those mechanisms.

## Decision Principles

- Keep component boundaries aligned to cohesive responsibilities and data ownership, not folder structure or every domain noun.
- Use synchronous calls when immediate consistency and user feedback matter and dependency latency/availability fit the workflow.
- Use asynchronous processing for long-running work, fan-out, buffering, vendor integration, and resilience when eventual consistency is acceptable.
- Put state in one authoritative place; derived state must have rebuild, reconciliation, and freshness rules.
- Design backpressure and load shedding before adding retries that can amplify outages.
- Prefer deterministic failure behavior over optimistic self-healing that operators cannot understand.
- For banking, insurance, and regulated workflows, model money, claim, policy, document, consent, and audit state transitions with explicit compensation, manual review, and evidence capture.

## Expected Output Style

- Start with the runtime shape and state ownership model.
- Include sequence or flow descriptions for happy path, failure path, retry path, and recovery path.
- Name the bottlenecks and the mitigation for each.
- State consistency, latency, timeout, retry, idempotency, and observability rules.
- Separate first-release design from future scale-out options.

## Architecture / Design Guidance

Describe the system with at least four views:

1. **Context**: users, external systems, trust boundaries, and ownership.
2. **Components**: responsibilities, dependencies, deployment units, and data ownership.
3. **Runtime flow**: request sequence, event sequence, state transitions, retries, and errors.
4. **Operational view**: logs, metrics, traces, dashboards, runbooks, scaling controls, and repair paths.

For asynchronous designs, define producer responsibility, event schema, partition key, ordering scope, consumer idempotency, retry limits, DLQ behavior, replay procedure, poison-message handling, and visibility of stuck work. For caches, define cache key, TTL, invalidation trigger, authorization safety, stampede control, stale-read tolerance, and fallback behavior. For gateway-mediated or partner-facing designs, define auth propagation, rate limits, request shaping, idempotency, partner timeout budgets, and safe error contracts. For object storage and search projections, define ownership, lifecycle, access controls, rebuild, and reconciliation rules.

## Implementation Guidance

- Specify API contracts, event contracts, queue/topic names, idempotency keys, timeout budgets, retry policies, circuit breaker behavior, and error propagation rules.
- Pass cancellation through synchronous call chains so timed-out requests do not continue consuming capacity.
- Use bounded queues, worker concurrency limits, and bulkheads for expensive downstream dependencies.
- Design admin or support workflows for replaying messages, repairing stuck state, reindexing projections, and reconciling derived stores.
- Add correlation IDs across every boundary in the first implementation slice.
- Define SLO-impacting signals separately from raw instrumentation: request success, workflow completion, queue lag, stuck jobs, cache hit rate, projection freshness, dependency saturation, and business-state reconciliation.
- Avoid hidden shared state, implicit global locks, unbounded in-memory queues, and background jobs that cannot be observed or stopped.

## Testing Expectations

- Test happy path, dependency timeout, dependency error, partial write, duplicate request, duplicate event, out-of-order event, poison message, retry exhaustion, and recovery.
- Run load tests for known bottlenecks and soak tests for leaks, queue growth, lock contention, and connection exhaustion.
- Verify idempotency under client retries, message redelivery, worker restart, and replay.
- Test degraded mode and operator repair workflows, not only automated success paths.
- Use chaos or fault injection only after deterministic failure cases are already covered.

## Security / Performance / Reliability Considerations

Security requires identity propagation, resource-level authorization, tenant isolation, sensitive data boundaries, safe operational tools, and secret handling across service, job, and integration boundaries. Performance requires latency budgets per hop, bounded concurrency, query budgets, payload limits, hot-key analysis, queue-lag budgets, and cache effectiveness targets. Reliability requires timeouts, cancellation, retry limits, backpressure, DLQs, replay, reconciliation, manual recovery paths, and evidence that failed regulated workflows can be safely repaired.

## Review Checklist

- Each component has one clear responsibility and owner.
- Source of truth, derived state, cache, queue, and search projection responsibilities are explicit.
- Sync and async choices are justified by consistency, latency, and failure behavior.
- Timeout, retry, cancellation, idempotency, and DLQ rules are defined.
- Bottlenecks and scaling limits are named with mitigations.
- Critical workflows have logs, metrics, traces, alerts, and repair procedures.
- Regulated workflows preserve audit evidence, authorization context, and reconciliation procedures across synchronous, asynchronous, and manual steps.
- The design can be delivered in vertical slices without committing to unnecessary future complexity.

## Anti-Patterns to Avoid

- Drawing boxes before understanding data flow and state transitions.
- Creating a service for every noun or database table.
- Retrying forever, retrying non-idempotent work, or retrying faster than dependencies can recover.
- Using cache, search, or queues as hidden sources of truth.
- Ignoring support workflows needed to repair failed or stuck state.
- Letting fan-out grow without quotas, concurrency limits, or failure isolation.
- Designing only the happy path and calling operational recovery an implementation detail.
- Treating platform services such as gateways, caches, queues, schedulers, and search indexes as magic infrastructure instead of owned parts of the runtime design.

## Gotchas / Common Failure Modes

- Timeouts without cancellation reduce user latency but still waste server and database capacity.
- Async workflows move failures from request time to operations time; operators need visibility and repair tools.
- Fan-out multiplies dependency failure probability and can create retry storms.
- Ordering guarantees are expensive and usually apply only within a partition or key, not globally.
- Caches can leak authorization, serve stale decisions, and hide broken read paths.
- Background jobs often fail silently unless progress, lag, and dead letters are first-class metrics.
- A component split that crosses a transaction boundary creates data reconciliation work.
- Partner APIs, document stores, and search indexes often fail outside the request path; system design must show how operators detect, retry, compensate, and explain those failures.
