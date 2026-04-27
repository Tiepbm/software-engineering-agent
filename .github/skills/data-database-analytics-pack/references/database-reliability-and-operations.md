---
name: database-reliability-and-operations
description: 'Operates production databases safely with replication, failover, backup, restore, migrations, capacity planning, connection management, observability, and risk controls.'
---

# Database Reliability and Operations

## Description

Operates production databases safely with replication, failover, backup, restore, migrations, capacity planning, connection management, observability, and risk controls.

## Purpose

- Keep databases available, recoverable, observable, and safely changeable under production traffic.
- Reduce data loss, downtime, migration failure, restore failure, connection exhaustion, replication lag, and storage-growth risk.
- Make database operations repeatable with runbooks, drills, dashboards, and ownership instead of heroic manual intervention.

## When to Use

- Planning schema changes, large backfills, database upgrades, failover, replication, backup policy, restore drills, DR, partition maintenance, or capacity growth.
- A release includes data changes that can affect correctness, availability, performance, or rollback.
- Production shows connection exhaustion, lock contention, replication lag, slow recovery, storage pressure, failed migrations, or unclear database ownership.
- Database operations affect CDC, event streams, caches, search indexes, object-storage exports, data pipelines, secrets, audit evidence, or regulated maintenance windows.

## Responsibilities

- Define RPO, RTO, availability target, maintenance windows, backup frequency, backup retention, restore process, failover process, and on-call ownership.
- Plan safe schema changes with expand-contract sequencing, compatibility windows, throttled backfills, validation, and rollback or roll-forward paths.
- Monitor latency, throughput, locks, waits, replication lag, connections, storage, cache hit rate, slow queries, index bloat, vacuum/compaction, backup health, and restore readiness.
- Manage connection pools, database users, parameter changes, upgrades, partition lifecycle, archival, and incident runbooks.
- Coordinate database operations with application deployment, feature flags, data pipeline consumers, analytics replicas, and downstream integrations.
- Involve `database-architecture`, `data-engineering-and-pipelines`, `messaging-and-eventing`, `caching-and-distributed-state`, `search-and-indexing`, `file-and-object-storage`, `authn-authz-and-secrets`, and `monitoring-alerting-and-slos` when operations cross those systems.

## Decision Principles

- A backup strategy is not valid until a restore has been tested with the same keys, extensions, permissions, versions, and target environment expected during an incident.
- Prefer expand-contract migrations for production systems: expand schema, deploy compatible code, backfill, verify, switch reads/writes, then contract later.
- Separate application rollback from data rollback; many data changes require roll-forward repair instead of destructive rollback.
- Limit connection pools from total database capacity, not from a single service instance. Autoscaling can multiply connections faster than the database can accept them.
- Treat long-running transactions, blocking DDL, and unbounded backfills as availability risks even when they look like routine maintenance.
- Production data changes in banking, insurance, and regulated systems need peer review, approval evidence, least-privilege access, audit trails, and reconciliation queries before and after execution.

## Expected Output Style

- Start with the production risk and the safest operational sequence.
- Include preflight checks, execution steps, monitoring, rollback or roll-forward, and post-change verification.
- State lock risk, replication impact, connection impact, storage impact, backup/restore impact, and downstream data impact.
- Use explicit runbook-style steps for high-risk operations.
- Mark assumptions about database engine, version, table size, traffic profile, and maintenance window.

## Architecture / Design Guidance

Database reliability architecture includes primary/replica topology, failover mechanism, DNS or endpoint behavior, read-routing rules, backup storage, point-in-time recovery, cross-region replication where required, maintenance automation, and monitoring. Multi-region writes require conflict resolution and data ownership rules; do not add them only for availability optics.

Schema-change architecture must preserve compatibility across multiple deployed application versions. Any change that renames, removes, rewrites, or retypes data must include a compatibility period and consumer inventory. Derived stores, CDC consumers, search indexes, and BI models may break even when the primary application still works.

Operational plans must include cache invalidation or warm-up, search reindexing, CDC lag, queue backlogs, object-storage export/import dependencies, secret rotation, and dashboard/alert changes when those systems depend on database shape or availability. For regulated workloads, maintenance windows, emergency access, and data repair steps should produce evidence that auditors and support teams can later inspect.

## Implementation Guidance

- For additive schema changes, verify default values, nullable behavior, metadata-only behavior, and lock duration for the specific database engine.
- For large backfills, use bounded batches, deterministic ordering, pause/resume state, rate limits, deadlock handling, and dashboards for rows processed, lag, locks, and error rate.
- For index changes, use online/concurrent creation where available and check write amplification, disk usage, build duration, and replica impact.
- For destructive changes, wait until all application versions and downstream consumers no longer read the old shape; then archive or snapshot before removal.
- For failover, verify application reconnection behavior, DNS TTLs, connection pool recovery, replica promotion, read-only windows, and job scheduler behavior.
- For restore, document who can access backups, where secrets/keys live, how to verify integrity, and how to reconcile data after point-in-time recovery.
- For point-in-time restore, plan reconciliation of external side effects: emitted events, queued jobs, payment calls, document writes, search projections, cache state, and downstream analytical loads.

## Testing Expectations

- Run restore drills and record actual recovery time, missing permissions, missing extensions, key access, and data validation results.
- Test failover with application clients, connection pools, background jobs, CDC consumers, and read replicas, not only the database console.
- Test migrations on production-sized copies with dirty data, realistic indexes, constraints, triggers, and concurrent workload.
- Test backfill pause/resume, retry, deadlock handling, throttling, and rollback or compensating repair.
- Verify monitoring and alerts before executing high-risk database changes.

## Security / Performance / Reliability Considerations

Security requires encrypted backups, least-privilege database roles, restricted admin access, audit logging, secret rotation, controlled exports, and governed emergency access. Performance requires capacity forecasting, index and vacuum/compaction maintenance, query-plan monitoring, cache impact, storage headroom, and connection-pool limits. Reliability requires tested restore, failover drills, migration safety, replication lag monitoring, CDC/search/cache recovery, corruption detection, and operational ownership with runbooks.

## Review Checklist

- RPO, RTO, availability target, owner, and escalation path are explicit.
- Backups are encrypted, monitored, retained, and recently restored successfully.
- Schema changes avoid long blocking locks or have an approved maintenance window.
- Migration plan includes expand-contract, compatibility, validation, and rollback or roll-forward.
- Backfills are throttled, resumable, observable, and safe for replicas and downstream consumers.
- Cache, CDC, search, object-storage export, queue, and analytics impacts are included in the operational plan.
- Connection pool totals fit database capacity under autoscaling.
- Replication lag, storage growth, slow queries, locks, waits, and backup health are monitored.
- Runbooks exist for failover, restore, connection exhaustion, slow queries, storage pressure, and failed migrations.

## Anti-Patterns to Avoid

- Assuming managed databases remove the need for restore drills, capacity planning, and query governance.
- Running large DDL or backfills during peak traffic without lock, replica, and storage analysis.
- Keeping backups in the same failure domain or encryption-key dependency path as the primary database.
- Letting every service instance open large connection pools until failover or autoscaling collapses the database.
- Dropping columns immediately after application deployment without waiting for old versions, jobs, reports, and CDC consumers.
- Performing manual production data fixes without audit trail, peer review, and verification queries.
- Treating read replicas as free scale while ignoring lag and stale-read correctness.
- Rotating keys, changing schemas, or restoring data without checking consumers that depend on old credentials, offsets, projections, or exported files.

## Gotchas / Common Failure Modes

- Failover often exposes hardcoded writer endpoints, stale DNS, retry storms, and clients that do not reconnect cleanly.
- Successful backups can be unrestorable because of missing keys, missing extensions, incompatible versions, or insufficient permissions.
- Replication lag can return stale permissions, balances, inventory, or workflow state to critical reads.
- Long transactions can block vacuum, cleanup, DDL, replication, or storage reclamation.
- Backfills can saturate I/O, WAL/binlog generation, replica apply, cache, or downstream CDC pipelines before CPU looks busy.
- Online index builds still consume disk, I/O, locks, and replication bandwidth.
- Point-in-time restore may require reconciling external side effects that the database rollback cannot undo.
- Emergency fixes can solve one account, claim, policy, or payment while corrupting audit history unless corrections are traceable and reversible.

## See Also

- `devops-and-release` — pipeline-side coordination of expand-contract, canary, blue-green, feature flags, and SLO gates.
- `data-engineering-and-pipelines` — backfill, replay, CDC consumer impact, and downstream reconciliation during migrations.
- `sql-and-query-optimization` — index build cost, plan regression, and connection pool sizing that operations must validate.
- `monitoring-alerting-and-slos` — replication lag, restore drill SLI, connection-pool saturation, and long-transaction alerting.

