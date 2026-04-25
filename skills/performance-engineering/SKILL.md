---
name: performance-engineering
description: 'Improves latency, throughput, resource usage, caching, concurrency, database cost, network cost, rendering cost, and profiling discipline before optimization.'
---

# Performance Engineering

## Description

Improves latency, throughput, resource usage, caching, concurrency, database cost, network cost, rendering cost, and profiling discipline before optimization. Applies queueing theory and measurement before making changes.

## Purpose

- Improve performance using measurements, bottleneck analysis, and workload fit instead of guesses.
- Balance latency, throughput, cost, correctness, and maintainability.
- Prevent premature optimization while addressing real user or system constraints.
- Use profiling tools and queueing math to predict impact before shipping changes.

## When to Use

- A workflow is slow, expensive, timing out, saturating CPU, memory, I/O, database, network, or UI rendering.
- Designing high-traffic APIs, data flows, frontend pages, mobile screens, or background jobs.
- Performance targets are part of acceptance criteria or SLOs.
- Symptoms involve queue lag, cache hit rate, retry storms, partner quotas, gateway limits, search latency, object-storage throughput, or tenant fairness.
- Capacity planning before a launch, marketing event, regulatory deadline, or seasonal peak.

## Responsibilities

- Define workload, target latency (p50/p95/p99), throughput, concurrency, payload size, data volume, and measurement method.
- Identify bottlenecks across application, database, cache, network, queue, browser, and mobile rendering layers using **profiling tools**, not guesses.
- Recommend changes with **expected impact** (calculated where possible) and **validation metrics** to prove improvement.
- Avoid optimizations that damage correctness, security, or operability.
- Apply queueing theory (Little's Law, USL/Universal Scalability Law) to predict bottleneck behavior under load.
- Involve `caching-and-distributed-state`, `rate-limiting-and-traffic-control`, `resilience-and-fault-tolerance`, `monitoring-alerting-and-slos`, `background-jobs-and-batch-processing`, `search-and-indexing`, `sql-and-query-optimization`, `api-gateway-and-service-integration` when tuning depends on those platform behaviors.

## Decision Principles

- **Profile before optimizing** unless the defect is obvious and local. Most "obvious" bottleneck guesses are wrong.
- **Optimize the bottleneck**, not the most familiar code. A 10x improvement in non-bottleneck code does nothing.
- **Cache only when** invalidation, freshness, memory, and stampede behavior are defined (delegate detail to `caching-and-distributed-state`).
- **Prefer reducing work** (eliminate, batch, defer, cache) over making unnecessary work faster.
- Optimize against **user-visible and SLO-relevant percentiles** (p95/p99), not averages — averages hide the worst experiences.
- Protect regulated workflows from tenant starvation and noisy-neighbor effects.
- **Measure baseline → change one variable → measure again**. Multiple changes confound results.
- **Little's Law** (`L = λ × W`): concurrent requests = arrival rate × response time. If response time doubles under load, in-flight work doubles, exhausting threads/connections.
- **USL** explains why throughput doesn't scale linearly: contention (α) and coherency (β) cap scale even when adding more capacity.

## Expected Output Style

- Start with the bottleneck hypothesis, the evidence (profiler output, query plan, metric), and the proposed change.
- Show concrete before/after numbers (or the measurement plan if not yet measured).
- Separate immediate fixes (query, index, cache, payload reduction) from longer-term improvements (architecture, workload separation, rewrite).
- State assumptions about load shape, concurrency, payload size, and target percentile.
- Include validation steps: how to confirm the change worked in staging and production.
- Avoid generic advice ("add a cache") unless followed by an enforceable rule, key design, and invalidation plan.

## Architecture / Design Guidance

Performance architecture defines **budgets** before design:

- **Request budget**: total time from user click to response, broken down per hop (API, auth, DB, cache, downstream).
- **Database query budget**: rows scanned, locks held, transaction duration, connection time.
- **Caching strategy**: what is cached, key design, TTL, invalidation, fallback (delegate to `caching-and-distributed-state`).
- **Concurrency model**: thread/connection pool sizing matching downstream capacity (Little's Law); bounded queues; bulkheads.
- **Queue capacity**: arrival rate, processing rate, max queue depth before backpressure (`messaging-and-eventing`, `background-jobs-and-batch-processing`).
- **Backpressure**: explicit rejection (429) over silent acceptance and later failure.
- **Dependency budgets**: per-partner timeout, retry, and quota allocation.
- **Gateway limits**: payload size, rate limit, timeout (`rate-limiting-and-traffic-control`, `api-gateway-and-service-integration`).
- **Client rendering budget** (frontend/mobile): bundle size, time-to-interactive (TTI), input latency (INP), frame budget (16.6ms for 60fps).

For banking and insurance workflows, budgets should explicitly cover payment authorization, claim submission, quote generation, document upload/download, and policy changes — with **fairness across tenants and branches** (one large customer should not starve others).

## Implementation Guidance

**Profiling tools** (use the right one for the layer):

| Layer | Tools |
|---|---|
| Linux process / system | `perf`, `bpftrace`, `eBPF`, `htop`, `iostat`, `vmstat`, `pidstat` |
| .NET | `dotnet-trace`, `dotnet-counters`, `PerfView`, `BenchmarkDotNet`, MiniProfiler, EF Core query logging |
| Java/JVM | `async-profiler`, JFR (Java Flight Recorder) + JMC, `jstack`, `jcmd`, JMH for microbenchmarks |
| Node.js | `--prof` + `node --prof-process`, `clinic.js`, Chrome DevTools CPU profiler |
| Python | `py-spy`, `cProfile`, `scalene`, `memory_profiler` |
| Go | `pprof` (CPU, heap, goroutine, block, mutex), `trace` |
| Database (PostgreSQL) | `EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_statements`, `auto_explain`, `pgBadger` |
| Database (MySQL) | `EXPLAIN ANALYZE`, performance schema, slow query log |
| Database (SQL Server) | Actual execution plans, Extended Events, Query Store |
| Browser | Chrome DevTools Performance + Lighthouse + Web Vitals |
| Mobile (iOS) | Instruments (Time Profiler, Allocations, Leaks) |
| Mobile (Android) | Android Studio Profiler, Systrace, Perfetto |
| React Native | Hermes profiler, Flipper, React DevTools Profiler |
| Distributed tracing | Jaeger, Tempo, Zipkin, Datadog APM |
| Load testing | `k6`, `Gatling`, `wrk`, `vegeta`, `locust`, `JMeter` |

**Common optimizations** (apply only after profiling confirms the bottleneck):

- **Pagination**: keyset over offset for deep/mutable lists (delegate to `sql-and-query-optimization`).
- **Projection**: select only needed columns; avoid loading object graphs.
- **Batching**: combine N small calls into one (DB `IN` clauses with bounds, HTTP batch endpoints, message batching with order awareness).
- **Compression**: `gzip`/`brotli` for HTTP, column compression for warehouses.
- **Async I/O**: free threads while waiting on I/O; respect cancellation.
- **Bounded concurrency**: parallel-fan-out with semaphore; never unbounded `Promise.all` / `Task.WhenAll`.
- **Caching**: with full design (delegate to `caching-and-distributed-state`).
- **Connection pooling**: size pool to total DB capacity (not per-instance default × replicas).
- **N+1 elimination**: prefetch, JOIN FETCH, projection (delegate to `sql-and-query-optimization`).
- **Hot-path allocation**: object pooling, `ArrayPool<T>`, struct-based parsing for high-throughput.

**Capacity planning math**:

- **Little's Law**: required threads = arrival_rate × avg_response_time. 1000 RPS × 50ms = 50 threads. If response time triples (slow downstream), need 150 threads or you queue.
- **Threadpool sizing**: for I/O-bound work, size = cores × (1 + wait_time / compute_time). For CPU-bound, size ≈ cores.
- **Connection pool**: pool_size × replicas ≤ DB max_connections × 0.8 (leave headroom for admin / migrations).
- **Queue depth**: at steady state, depth = arrival_rate × queue_time. Set max queue based on max acceptable queue_time, then reject (backpressure) beyond that.

## Testing Expectations

- **Microbenchmarks** only for isolated hot paths (BenchmarkDotNet, JMH); never for system-level decisions.
- **Load tests** for system behavior under realistic workload shape (think ramp-up, soak, spike, stress).
- **Soak tests** (hours) for memory leaks, connection leaks, file descriptor leaks, queue accumulation.
- **Inspect query plans** for data-bound work; verify index usage, scan size, lock duration.
- **Browser/mobile profilers** for rendering, startup, and memory.
- **Test cold cache, cache stampede, dependency throttling, retry exhaustion, queue backlog drain, and worst-case tenant or data-partition behavior** — these only appear under realistic concurrency and skew.
- **Regression tests**: keep a small suite of perf tests in CI that fails if p95 increases beyond budget.

## Security / Performance / Reliability Considerations

Security controls (auth, encryption, audit logging, rate limiting) **must stay intact** under optimization. A faster system that bypasses authorization is broken, not optimized.

Reliability requires timeouts, backpressure, circuit breakers, bounded retries, graceful degradation, and overload protection (delegate to `resilience-and-fault-tolerance`). Performance changes must not compromise data correctness or create stale decisions without explicit tolerance — especially for balances, eligibility, claim status, policy coverage, and authorization decisions.

## Review Checklist

- Targets and baseline are documented (p50/p95/p99 + throughput + concurrency).
- Bottleneck is **proven by profiling**, not guessed.
- Database cost (rows, plans, locks) is measured.
- Cache behavior is safe (invalidation, staleness, authorization).
- Concurrency is bounded; thread/connection pool sizing matches downstream capacity (Little's Law).
- Queue lag, retry rate, dependency quotas, and cache hit/miss behavior are measured when relevant.
- Client rendering cost (bundle, TTI, INP) is measured for frontend changes.
- After-change metrics prove improvement against the same workload.
- Regression test or alert exists to catch future regressions.
- Optimization does not reduce security, audit, or correctness guarantees.

## Anti-Patterns to Avoid

- Optimizing without measurements ("this loop looks slow").
- Adding cache to hide a bad query, broken data model, or missing source-of-truth decision.
- Unbounded parallelism (`Promise.all` over arbitrary input, `Parallel.ForEach` without `MaxDegreeOfParallelism`).
- Returning huge payloads "because the client might need it".
- Ignoring slow mobile devices and poor networks.
- Treating average latency as sufficient when SLOs measure p95/p99.
- Solving latency by increasing retries, fan-out, or cache staleness without checking failure amplification and correctness.
- Microbenchmarking in isolation and assuming the result holds under real load.
- Capacity planning by linear extrapolation — USL says throughput plateaus or regresses past a point.
- Increasing thread pool / connection pool to "fix" slowness — usually exhausts the downstream and makes it worse.

## Gotchas / Common Failure Modes

- **p95 and p99 latency** reveal issues hidden by averages — a 10ms average can hide a 2-second p99.
- **Cold starts and cache misses** are user-visible and dominate after deploys, failovers, or autoscaling.
- **Fast local tests** can hide production cardinality, skew, and concurrency issues.
- **Caching permissioned data** can leak access if invalidation lags role changes.
- **Network round trips** dominate many UI flows; one waterfall of 5 sequential requests at 100ms each = 500ms before render.
- **Retry storms** turn a small dependency hiccup into a cascading outage; bounded retries with jitter are mandatory.
- **Cold starts on serverless** (Lambda, Functions, Cloud Run) can add seconds; provisioned concurrency or warm-up needed for SLO-sensitive paths.
- **Hot partitions** in distributed databases (Cassandra, DynamoDB) cap throughput at single-partition limit even with many partitions overall.
- **Shared gateway / cache / queue limits** create per-tenant noisy-neighbor problems invisible until production scale.
- **GC pauses** (JVM, .NET, Node) can cause p99 spikes invisible in average metrics; tune GC for tail latency, not throughput.
- **Connection pool exhaustion** appears as request timeouts, not DB errors.
- **Database statistics drift**: query plans regress after large data loads or version upgrades; refresh stats explicitly.
- **Optimization at the wrong layer**: spending a week optimizing a JS function that runs in 5ms while the API call takes 800ms.
- **Little's Law violation**: assuming a thread pool of 100 can handle 100 concurrent requests when downstream takes 500ms — actual capacity is 100/0.5 = 200 RPS, not 100 × any number.

