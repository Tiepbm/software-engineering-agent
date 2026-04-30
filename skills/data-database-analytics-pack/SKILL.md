---
name: data-database-analytics-pack
description: 'Use when modeling domain data, choosing a database, optimizing SQL/ORM, operating production DBs, building pipelines (ETL/ELT/CDC), or designing analytics/warehouse consumption.'
---
# Data, Database, and Analytics Pack

## When to Use
- Aggregates, source-of-truth, history/SCD, audit trail, transactional boundaries, derived state ownership.
- DB family/topology selection, partitioning, replication, scaling, retention, recovery model.
- Slow query, bad plan, lock contention, ORM N+1, pagination at scale.
- Backup/restore, failover drill, schema migration sequencing, expand-contract.
- ETL/ELT/CDC, replay, backfill, idempotent sinks, data quality, lineage.
- Marts, semantic layer, governed metrics, BI cost control.

## When NOT to Use
- Runtime cache or distributed locks → `resilience-performance-pack`.
- Search index design (even on top of DB) → `storage-search-pack`.
- Outbox CONSUMER side / replay protocol / DLQ → `platform-integration-pack`.
- File/object storage of documents and assets → `storage-search-pack`.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `data-modeling` | Use when defining aggregates, source-of-truth ownership, SCD/history, derived-state rules, or domain invariants. |
| `database-architecture` | Use when CHOOSING a database family, topology, partitioning/replication/sharding strategy, or doing workload-fit reasoning across access patterns. |
| `sql-and-query-optimization` | Use when a SPECIFIC query/ORM call is slow, locks, or has a bad plan — focus on EXPLAIN, indexes, statistics, rewrites. |
| `database-reliability-and-operations` | Use when planning backup/restore, failover, schema migration sequencing, expand-contract, or DB incident response. |
| `data-engineering-and-pipelines` | Use when designing ETL/ELT/CDC, replay/backfill, idempotent sinks, schema evolution, or data-quality controls. |
| `analytics-and-warehouse-design` | Use when designing facts/dimensions, semantic layer, governed metrics, marts, lineage, or BI consumption. |
| `databricks-lakehouse` | Use when designing Databricks/lakehouse medallion architecture, Delta Lake CDC ingestion from RDBMS, Unity Catalog governance, or insurance/banking analytical models on Databricks. |

## Cross-Pack Handoffs
- → `platform-integration-pack` for outbox consumer / DLQ / replay protocol.
- → `observability-release-pack` for migration release safety + DB SLOs + restore drills.
- → `security-access-pack` for row-level / tenant authz and sensitive-column masking.
- → `storage-search-pack` for projecting OLTP data into a search index.

