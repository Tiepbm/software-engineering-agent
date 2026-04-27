---
name: sql-and-query-optimization
description: 'Optimizes SQL and ORM-generated queries through execution plans, indexing, join strategy, selectivity, pagination, locks, statistics, schema alignment, and write-cost trade-offs.'
---

# SQL and Query Optimization

## Description

Optimizes SQL and ORM-generated queries through execution plans, indexing, join strategy, selectivity, pagination, locks, statistics, schema alignment, and write-cost trade-offs.

## Purpose

- Fix query performance by identifying root causes in plans, schema, statistics, indexes, data distribution, and access patterns.
- Reduce latency, resource usage, blocking, lock contention, and write amplification without changing business results.
- Make database performance work reviewable, measurable, and safe to deploy.

## When to Use

- Queries are slow, expensive, blocking writes, timing out, spilling memory, scanning too many rows, or causing CPU, I/O, lock, or replica-lag pressure.
- Adding list endpoints, dashboards, reports, search filters, migrations, backfills, or ORM query paths that may hit production data.
- Reviewing indexes, pagination, joins, aggregations, sorting, filtering, locking, or generated SQL from EF Core, JPA/Hibernate, ActiveRecord, Django ORM, or similar tools.

## Responsibilities

- Capture query text, bind parameters, frequency, caller, expected row count, actual row count, latency target, and production cardinality.
- Inspect actual execution plans, row estimates, join order, join method, index usage, scans, sort operations, memory spills, waits, locks, and buffer/logical reads.
- Align indexes with predicates, joins, ordering, grouping, and selectivity while accounting for write cost.
- Identify non-sargable predicates, stale statistics, parameter-sensitive plans, N+1 queries, unbounded lists, and schema-query mismatch.
- Provide before/after measurements and deployment safety notes for index or query changes.

## Decision Principles

- Measure with representative data and parameters before optimizing; averages are not enough for skewed tenants or customers.
- Prefer query and schema alignment over optimizer hints. Use hints only when engine behavior is understood, documented, and tested against upgrades.
- Use keyset pagination for large or mutable result sets; use offset pagination only for small stable lists or administrative use.
- Add indexes only when they serve real access patterns and their read benefit exceeds write, storage, maintenance, and migration cost.
- Fix N+1 and chatty access patterns before adding hardware or read replicas.
- Do not move OLAP-style scans onto OLTP systems when a warehouse, mart, replica, or pre-aggregation is the correct workload separation.

## Expected Output Style

- Start with the likely bottleneck and the evidence from the plan or measurements.
- Show the specific query, access pattern, index or rewrite recommendation, and expected effect.
- State risks: write amplification, lock duration, index build impact, plan regression, stale statistics, and rollback approach.
- Separate tactical query fix from longer-term schema or workload-separation changes.
- Include validation commands or metrics to compare before and after.

## Architecture / Design Guidance

Query performance is a contract between schema, data distribution, access patterns, and the optimizer. OLTP paths need narrow predicates, bounded results, selective indexes, and short transactions. Analytical paths need columnar storage, partition pruning, clustering/sort keys, pre-aggregation, or workload isolation.

Plan inspection must account for engine differences: PostgreSQL buffers and row estimates, MySQL EXPLAIN and index choice, SQL Server actual execution plans and parameter sniffing, Oracle optimizer statistics and hints, and distributed warehouses where scan bytes and shuffle dominate cost. ORM convenience does not remove the need to inspect generated SQL.

## Implementation Guidance

- Make predicates sargable: avoid functions on indexed columns, leading wildcard searches, implicit casts, mismatched collations, and expression patterns that prevent index use unless expression indexes exist.
- Use composite indexes in an order that matches equality filters, range filters, join keys, and sort/group needs for the specific engine.
- Consider covering indexes for hot reads, partial/filtered indexes for selective subsets, and expression indexes only when the expression is stable and frequently used.
- Replace SELECT * with required columns in hot paths and avoid loading object graphs that the caller does not need.
- Batch or prefetch to eliminate N+1 queries; use projections instead of serializing lazy-loaded entities.
- Keep transactions short and avoid user interaction, network calls, or large loops inside open transactions.
- Build large indexes using online/concurrent mechanisms where available and plan disk, lock, replica, and rollback impact.

## Testing Expectations

- Compare before and after execution plans, wall-clock time, rows scanned, rows returned, logical reads/buffers, memory spills, lock waits, and CPU/I/O indicators.
- Test common, worst-case, and skewed parameter values, including large tenants or high-cardinality filters.
- Verify new indexes do not materially harm write throughput, storage budget, replication lag, or migration duration.
- Test pagination under concurrent inserts, deletes, and updates.
- Test ORM changes against generated SQL, not only repository method behavior.

## Security / Performance / Reliability Considerations

Security requires parameterized queries, least-privilege roles, safe dynamic SQL construction, and no sensitive data leakage through diagnostic logs. Performance requires actual plans, accurate statistics, bounded result sets, workload isolation, and index discipline. Reliability requires avoiding long transactions, blocking DDL, lock escalation, retry storms, and production index builds without an operational plan.

## Review Checklist

- Actual execution plan or equivalent engine evidence is reviewed.
- Query predicates are sargable and data types match indexed columns.
- Index recommendation maps to a real access pattern and includes write-cost analysis.
- Pagination is bounded and stable for mutable datasets.
- Join order, join method, and cardinality estimates are plausible.
- Aggregations, sorts, and DISTINCT operations do not hide unnecessary scans or spills.
- ORM-generated SQL is inspected for hot paths.
- Deployment plan covers index build safety, monitoring, and rollback.

## Anti-Patterns to Avoid

- Adding indexes without reading the actual plan.
- Using SELECT * or loading full entity graphs in hot paths.
- Offset pagination for deep, high-traffic, or mutable lists.
- Applying functions, casts, or transformations to indexed columns in filters without expression indexes.
- Trusting ORM method names while ignoring generated SQL and lazy loading.
- Using hints to hide bad schema, stale statistics, or wrong access patterns.
- Sending analytical dashboards to primary OLTP databases.

## Gotchas / Common Failure Modes

- An index can improve one read path while degrading writes, storage, vacuum/maintenance, and replication.
- Parameter sniffing or parameter-sensitive plans can make one tenant fast and another slow.
- Low-cardinality indexes often disappoint unless combined, filtered, or used for covering/sort purposes.
- Sorts and hash aggregations can dominate cost even when filters are indexed.
- Read replicas spread inefficient query cost and can add stale-read correctness problems.
- ORM lazy loading can turn one endpoint into hundreds of queries only at production cardinality.
- Query plans can regress after statistics changes, upgrades, data growth, or tenant skew.

## Worked Example: Reading `EXPLAIN ANALYZE` (PostgreSQL)

**Query**:
```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT c.id, c.policy_number, p.holder_name
FROM   claims c
JOIN   policies p ON p.id = c.policy_id
WHERE  c.tenant_id = $1
  AND  c.status    = 'OPEN'
  AND  c.created_at >= now() - interval '30 days'
ORDER  BY c.created_at DESC
LIMIT  50;
```

**Sample plan (problematic)**:
```
Limit  (cost=15234.10..15234.22 rows=50 width=64) (actual time=812.4..812.6 rows=50 loops=1)
  Buffers: shared hit=812 read=4231
  ->  Sort  (cost=15234.10..15301.55 rows=26980 width=64) (actual time=812.4..812.5 rows=50 loops=1)
        Sort Key: c.created_at DESC
        Sort Method: top-N heapsort  Memory: 32kB
        ->  Hash Join  (cost=412.00..14123.40 rows=26980 width=64) (actual time=12.1..801.2 rows=27034 loops=1)
              Hash Cond: (c.policy_id = p.id)
              ->  Seq Scan on claims c  (cost=0.00..13200.00 rows=26980 width=40)
                    (actual time=0.4..720.1 rows=27034 loops=1)
                    Filter: ((tenant_id = $1) AND (status = 'OPEN')
                             AND (created_at >= (now() - '30 days'::interval)))
                    Rows Removed by Filter: 1972966
                    Buffers: shared read=4100
              ->  Hash  (cost=290.00..290.00 rows=9760 width=32)
                    ->  Seq Scan on policies p ...
Planning Time: 0.42 ms
Execution Time: 812.9 ms
```

**How to read it**:
1. **Bottom-up**: `Seq Scan on claims` reads 2 M rows, filter discards 98.6 % (`Rows Removed by Filter: 1972966`) → no usable index for the predicate.
2. **`actual time=0.4..720.1`** — this single node owns ~720 ms of the 813 ms total. Optimization target = this node.
3. **`Buffers: shared read=4100`** — physical reads (cold cache); after warmup these become `hit`. Use `BUFFERS` to distinguish I/O cost from CPU cost.
4. **Estimated vs actual rows**: `rows=26980 (actual rows=27034)` → estimate is accurate, so this is not a statistics problem; it is an indexing/access-path problem.
5. **Top-N heapsort** with 32 kB is fine; not the bottleneck. `LIMIT 50` after sort means the planner cannot push the limit down because it must sort the full filtered set first.
6. **Hash Join** is appropriate for 27 k × 9 760 rows; do not "fix" it without addressing the seq scan first.

**Fix**: composite index aligned with the filter + sort:
```sql
CREATE INDEX CONCURRENTLY ix_claims_tenant_status_created
  ON claims (tenant_id, status, created_at DESC)
  INCLUDE (policy_id)
  WHERE status IN ('OPEN','PENDING');     -- partial index keeps it small
```
Why this shape: leading equality columns (`tenant_id`, `status`), then range/sort column (`created_at DESC`) so the planner can do an **Index Scan Backward** + **Limit** without a Sort node. `INCLUDE (policy_id)` makes it covering for the join. Partial `WHERE` keeps the index small if `OPEN` is < 5 % of rows.

**Expected new plan shape**:
```
Limit  ...  (actual time=0.3..1.2 rows=50 loops=1)
  ->  Nested Loop  ...
        ->  Index Scan Backward using ix_claims_tenant_status_created on claims c
              Index Cond: ((tenant_id = $1) AND (status = 'OPEN')
                           AND (created_at >= now() - '30 days'::interval))
              Buffers: shared hit=53
        ->  Index Scan using policies_pkey on policies p
              Index Cond: (id = c.policy_id)
Execution Time: 1.5 ms
```

**Verification checklist before merging the index**:
- [ ] `EXPLAIN ANALYZE` shows Index Scan, no Sort node, `Rows Removed by Filter` is small.
- [ ] `pg_stat_user_indexes.idx_scan` increases for the new index after deploy.
- [ ] Write benchmark: insert/update on `claims` is not regressed beyond budget (every index has write cost).
- [ ] Index size acceptable (`\di+` or `pg_relation_size`); partial predicate keeps it tight.
- [ ] Plan stable for both small tenants and the largest tenant (parameter sniffing check) — re-run with the worst-case `$1`.

