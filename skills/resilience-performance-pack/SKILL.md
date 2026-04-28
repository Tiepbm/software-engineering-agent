---
name: resilience-performance-pack
description: 'Use when improving latency/throughput, designing runtime cache and distributed state, or applying timeouts, retries, circuit breakers, bulkheads, graceful degradation, and failure containment.'
---
# Resilience and Performance Pack

## When to Use
- Timeouts, cancellations, bounded retries, backoff, circuit breakers, bulkheads, failover, graceful degradation, fault-injection.
- Runtime cache (Redis/in-memory): TTL, invalidation, staleness, distributed locks, sessions, hot keys, stampedes, cache authorization safety.
- Latency budgets, p95/p99, throughput, profiling evidence, queueing math, capacity planning, concurrency limits, queue lag, rendering cost.

## When NOT to Use
- Choosing the PRIMARY storage / source of truth → `data-database-analytics-pack`.
- Search index correctness/freshness → `storage-search-pack`.
- DLQ/retry behaviour at the message-broker layer → `platform-integration-pack` → `messaging-and-eventing`.
- Rate-limit policy at the edge → `platform-integration-pack` → `rate-limiting-and-traffic-control`.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `resilience-and-fault-tolerance` | Use when designing timeout/retry/circuit/bulkhead/fallback policy for a specific dependency, or when planning fault-injection tests. |
| `caching-and-distributed-state` | Use when adding a runtime cache, distributed lock, session store, or any shared in-memory state — including staleness, invalidation, tenant isolation, stampede protection. |
| `performance-engineering` | Use when investigating a SPECIFIC latency/throughput/capacity problem with profiling evidence, queueing math, or capacity planning. |
| `cost-and-finops` | Use when reasoning about cloud/runtime cost, unit economics, attribution, savings plans, denial-of-wallet protection, or architectural trade-offs that move money — not only latency. |

## Cross-Pack Handoffs
- → `data-database-analytics-pack` when the bottleneck is the DB itself (plan, indexes, hot rows).
- → `platform-integration-pack` when retries/queues/DLQs are at the broker layer.
- → `observability-release-pack` for SLO-based degradation triggers and runbooks.
- → `security-access-pack` for cache authorization safety (tenant isolation, key design).

