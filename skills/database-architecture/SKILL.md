---
name: database-architecture
description: 'Selects and designs database platforms using workload-fit reasoning across OLTP, OLAP, relational, document, key-value, wide-column, graph, time-series, search, warehouse, and lakehouse systems.'
---

# Database Architecture

## Description

Selects and designs database platforms using workload-fit reasoning across OLTP, OLAP, relational, document, key-value, wide-column, graph, time-series, search, warehouse, and lakehouse systems.

## Purpose

- Choose storage technology from access patterns, consistency needs, data shape, scale profile, recovery requirements, and operating model rather than preference.
- Define the canonical store, derived stores, cache layers, search indexes, analytical stores, and event streams without confusing their responsibilities.
- Make indexing, partitioning, sharding, replication, retention, migration, backup, restore, and cost decisions reviewable before production.

## When to Use

- Selecting or reviewing PostgreSQL, MySQL, SQL Server, Oracle, MongoDB, Redis, Cassandra, DynamoDB, Elasticsearch, OpenSearch, Neo4j, ClickHouse, BigQuery, Snowflake, Redshift, Databricks, or Kafka-backed patterns.
- A system needs new scale, availability, search, analytics, graph traversal, time-series ingestion, low-latency reads, multi-region behavior, or lower operational cost.
- Current storage causes slow queries, hot partitions, data drift, weak consistency, painful migrations, unreliable restore, high bills, or unclear source-of-truth ownership.
- Storage choices affect caching, search indexing, event-driven propagation, object storage, retention/legal hold, audit evidence, or data residency.

## Responsibilities

- Capture the workload: read/write ratio, query shapes, point lookups, joins, aggregations, latency targets, throughput, cardinality, skew, growth rate, retention, and freshness.
- Identify correctness needs: transaction scope, uniqueness, referential integrity, conflict handling, isolation level, auditability, history, and repair workflow.
- Compare database families and reject poor fits explicitly, not silently.
- Define physical design: indexes, partition keys, shard keys, sort or clustering keys, TTL, compression, replication, backup, restore, archiving, and capacity alarms.
- Separate canonical OLTP state from caches, search projections, analytics marts, lakehouse raw zones, and event logs.
- Involve `caching-and-distributed-state`, `search-and-indexing`, `messaging-and-eventing`, `file-and-object-storage`, `data-engineering-and-pipelines`, `security-review`, and `database-reliability-and-operations` when those stores or propagation paths are part of the design.

## Decision Principles

- Use relational databases when the workload needs transactions, constraints, joins, flexible operational queries, or strong consistency. PostgreSQL is a strong default for product OLTP; MySQL is common for high-read web workloads; SQL Server and Oracle often fit enterprise ecosystems, tooling, and legacy integration constraints.
- Use document databases when the aggregate is naturally document-shaped, reads usually fetch the whole aggregate, schema variation is real, and cross-document transactions are not central to correctness.
- Use key-value stores such as Redis for cache, session state, rate limits, queues with caution, counters, and ephemeral low-latency access. Do not use a cache as the only durable record.
- Use wide-column or partition-key stores such as Cassandra or DynamoDB when access patterns are known up front, writes are high volume, horizontal scale is mandatory, and denormalized query tables are acceptable.
- Use search stores such as Elasticsearch or OpenSearch for relevance, full-text search, faceting, and log exploration. Do not make them the source of truth for money, permissions, or lifecycle state.
- Use graph databases such as Neo4j when multi-hop relationship traversal is the core query, not when simple joins or adjacency lists are sufficient.
- Use analytical stores such as ClickHouse, BigQuery, Snowflake, Redshift, or Databricks for scans, aggregations, BI, ML, and governed analytical products, not OLTP request serving.
- Use Kafka for durable event transport, replay, and decoupled integration; pair it with state stores when queryable current state is required.
- For regulated workloads, select storage with data classification, retention, legal hold, deletion, residency, auditability, encryption, masking, and privileged-access evidence in mind.

## Expected Output Style

- Start with a clear recommendation and state why the workload fits it.
- Include at least one simpler alternative and one rejected alternative with reasons.
- State assumptions about volume, cardinality, growth, latency, consistency, retention, and team operating capability.
- Separate logical model, physical design, operational design, and migration plan.
- Provide reviewable artifacts: access-pattern table, storage decision matrix, index/partition plan, failure-mode list, and validation checklist.

## Architecture / Design Guidance

A production database architecture must name the system of record. Derived projections are allowed only with explicit freshness, rebuild, reconciliation, and ownership rules.

Use this workload-fit frame:

| Workload need | Strong fit | Poor fit warning |
| --- | --- | --- |
| OLTP with constraints, joins, and transactions | PostgreSQL, MySQL, SQL Server, Oracle | Wide-column or search stores used to avoid modeling |
| Aggregate documents with bounded queries | MongoDB or similar document store | Cross-document invariants and ad hoc joins dominate |
| Sub-millisecond ephemeral lookup | Redis or equivalent key-value store | Durable source of truth or complex query model needed |
| Massive predictable partition-key access | Cassandra, DynamoDB | Unknown query patterns, joins, and hot keys |
| Full-text relevance and faceting | Elasticsearch, OpenSearch | Exact transactional truth or complex authorization filtering |
| Relationship path traversal | Neo4j or graph store | Simple foreign-key relationships only |
| Time-window metrics and retention | Time-series store or partitioned analytical store | Entity-centric OLTP updates dominate |
| BI, aggregations, ML, large scans | BigQuery, Snowflake, Redshift, ClickHouse, Databricks | Low-latency transactional request path |

For multiple stores, define propagation: outbox, CDC, event stream, batch ELT, materialized view, object-storage export, or search indexer. Every propagation path needs ordering assumptions, idempotency, retry behavior, lag monitoring, and rebuild procedure. Derived stores must never silently become the authority for balances, claim status, policy eligibility, permissions, consent, or other regulated decisions without a deliberate source-of-truth change.

Object storage is appropriate for documents, images, statements, exports, and immutable raw data when metadata, access control, malware scanning, lifecycle, retention, and legal hold are designed. Search indexes are appropriate for discovery and faceting when freshness, reindexing, and authorization filtering are explicit. Caches are appropriate for speed when invalidation, staleness tolerance, tenant isolation, and warm-up behavior are explicit.

## Implementation Guidance

- Create an access-pattern inventory before selecting technology: operation, filters, sort order, expected rows, frequency, latency target, consistency expectation, and growth driver.
- Design indexes from query predicates and sort requirements; account for write amplification, storage cost, and online build strategy.
- Choose partition or shard keys from cardinality, distribution, access locality, and hot-key risk. A tenant ID alone is often a hot partition for large tenants.
- Define replication topology and read-routing rules. If replicas serve reads, document staleness tolerance and read-after-write requirements.
- Define backup and restore: schedule, retention, encryption, restore target, point-in-time recovery, drill frequency, and expected recovery time.
- For migrations, require expand-contract sequencing, backfill throttling, validation queries, rollback or roll-forward path, and data reconciliation.
- For managed databases, still define ownership for upgrades, parameter changes, indexes, slow queries, cost, failover testing, and incident response.
- For regulated data, document classification, retention period, masking/tokenization, audit-table strategy, export controls, data-subject handling, and who may approve production data fixes.

## Testing Expectations

- Validate representative read and write paths with production-like cardinality, skew, and worst-case tenants or partitions.
- Inspect query plans, index usage, scan volume, lock behavior, and write amplification before launch.
- Test failover, replica lag, backup restore, point-in-time recovery, migration rollback or roll-forward, and projection rebuilds.
- Reconcile canonical and derived stores after backfills, CDC changes, search indexing, and event replay.
- Run capacity tests that include connection limits, storage growth, compaction/vacuum behavior, and maintenance windows.

## Security / Performance / Reliability Considerations

Security requires network isolation, encryption in transit and at rest, least-privilege roles, audit logs, secret rotation, backup encryption, masking, retention/legal hold, and governed exports. Performance requires query-pattern-aligned indexes, partition pruning, bounded result sets, connection pooling, cache effectiveness, search indexing budgets, and capacity forecasting. Reliability requires tested restore, failover behavior, replication lag monitoring, migration safety, projection rebuilds, corruption detection, and clear ownership for production incidents.

## Review Checklist

- Workload shape and access patterns are documented.
- The recommended database has explicit fit reasoning and rejected alternatives.
- Canonical store, cache, search, analytics, and event-log responsibilities are separated.
- Object storage, retention, legal hold, and document metadata responsibilities are explicit when files or exports are involved.
- Consistency, transaction, isolation, and staleness expectations match business workflows.
- Index, partition, shard, retention, and replication strategies match real access patterns.
- Backup, restore, failover, projection rebuild, and migration procedures are tested.
- Cost model includes storage, compute, I/O, network, license, support, and operational labor.
- Team capability is realistic for the chosen technology.

## Anti-Patterns to Avoid

- Choosing NoSQL because the data model is unclear.
- Using Elasticsearch, OpenSearch, Redis, or Kafka as the canonical transactional database without durability and queryability analysis.
- Introducing polyglot persistence before exhausting a simpler relational or managed option.
- Sharding before measuring single-node, managed scaling, partitioning, or read-replica limits.
- Using tenant ID as a partition key without modeling large-tenant skew.
- Creating secondary indexes in distributed stores as if they behaved like relational indexes.
- Running analytics directly on OLTP tables when workload isolation is required.
- Treating managed database backups as sufficient without restore drills.
- Letting cache, search, analytics, or object storage evolve into unofficial systems of record because they are easier to query.

## Gotchas / Common Failure Modes

- A database can scale writes but still fail from hot keys, unbounded queries, or poor partition distribution.
- Document databases still need schema governance, validation, and migration strategy.
- Search indexes are eventually consistent and may not enforce authorization or exact business truth.
- Read replicas can return stale data and hide inefficient query costs until replication lag rises.
- Warehouse and lakehouse bills often spike from unbounded scans, poor clustering, small files, or uncontrolled BI queries.
- Cross-store consistency failures usually appear during retries, backfills, replays, and partial outages.
- Backup success is not restore success; missing keys, permissions, extensions, or version mismatches can make restores fail.
- Retention, legal hold, masking, and delete requirements often conflict unless modeled before data is copied into caches, indexes, warehouses, exports, and object stores.
