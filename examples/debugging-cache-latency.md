# Debugging Example — High p95 Latency After Redis Cache Rollout

> Shape: diagnosis → likely root cause → fix → impact → security/observability impact → tests → residual risk → longer-term improvement.

**Diagnosis**: After rolling out a read-through Redis cache for `/v1/customers/{id}/policies`, p95 latency increased from 180 ms to 540 ms while p50 dropped from 120 ms to 28 ms. Cache-hit rate is 71 %.

**Likely root cause**: Cache-miss path is now serial (Redis GET → DB read → Redis SET) and Redis SET is synchronous on the request path. Under tail-latency conditions (Redis pause / slow DB) the miss penalty stacks. Hot tenants concentrate misses on a handful of keys, triggering thundering-herd.

Packs/refs consulted: `resilience-performance-pack/caching-and-distributed-state`, `resilience-performance-pack/performance-engineering`, `security-access-pack/security-review` (cache key includes `tenant_id`?).

**Recommended fix** (immediate):
1. Add `single-flight` (request coalescing) on cache miss per `(tenant_id, customer_id)` so concurrent misses share one DB call.
2. Make Redis SET fire-and-forget after the response is sent.
3. Cap Redis client timeout at 50 ms; on timeout, bypass cache and read DB directly (degrade gracefully, count as miss).

**Impact**:
- Data: no schema change. Cache key MUST include `tenant_id` — verify before deploy.
- Messaging: none.
- Caching: TTL stays 60 s; add `MAXMEMORY-POLICY allkeys-lru` if not already.
- Integration: none.

**Security / observability impact**:
- Verify cache key composition prevents cross-tenant reads (`security-review`).
- Add metrics: `cache_miss_total`, `cache_singleflight_collapsed_total`, `cache_redis_timeout_total`. Alert when `cache_redis_timeout_total / cache_total > 1 %`.

**Tests**:
- Load test with 200 concurrent requests on same key → expect 1 DB call (not 200).
- Inject 100 ms Redis delay → p95 still ≤ 250 ms (degraded, but bounded).
- Cross-tenant key collision test (negative).

**Residual risk**: Stale reads up to 60 s; acceptable for policy listing but NOT for premium amount. If amount is read-through too, add explicit invalidation on `policy.updated` event (`messaging-and-eventing`).

**Longer-term improvement**: Move from read-through to a CDC-driven cache populated by `policy.updated` events; eliminates miss-storm entirely. Requires `data-engineering-and-pipelines` design.

