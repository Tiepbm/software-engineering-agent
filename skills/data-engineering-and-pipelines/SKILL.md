---
name: data-engineering-and-pipelines
description: 'Designs resilient ETL, ELT, batch, streaming, CDC, and event-driven pipelines with schema evolution, data quality, idempotency, replay, backfill, and failure recovery.'
---

# Data Engineering and Pipelines

## Description

Designs resilient ETL, ELT, batch, streaming, CDC, and event-driven pipelines with schema evolution, data quality, idempotency, replay, backfill, and failure recovery.

## Purpose

- Move data between systems with correctness, lineage, observability, and recovery instead of fragile scheduled scripts.
- Choose batch, streaming, CDC, event-driven integration, ETL, or ELT based on freshness, volume, transformation complexity, cost, and operating capability.
- Make duplicates, deletes, updates, late-arriving data, schema drift, replay, and backfill explicit design concerns.

## When to Use

- Building or reviewing ingestion, transformation, warehouse loading, lakehouse loading, event integration, CDC replication, streaming processing, or batch orchestration.
- Pipelines produce duplicate records, missing records, stale dashboards, broken schemas, silent data quality regressions, painful reruns, or unsafe backfills.
- Teams need freshness SLAs, lineage, schema contracts, replay strategy, data quality gates, orchestration, or operational runbooks.
- Data movement touches regulated datasets, object storage zones, search projections, event streams, workflow orchestration, monitoring/SLOs, or downstream operational systems.

## Responsibilities

- Define source systems, sink systems, data contracts, extraction method, transformation stages, orchestration, ownership, freshness targets, and failure behavior.
- Specify idempotency keys, deduplication logic, watermarking, ordering assumptions, late-data handling, retry policy, dead-letter handling, and reprocessing rules.
- Govern schema evolution for additive, breaking, nullable, renamed, and removed fields.
- Design data quality checks at ingestion, transformation, publication, and consumption boundaries.
- Provide replay, backfill, rollback, and reconciliation procedures before production.
- Involve `workflow-and-job-orchestration`, `background-jobs-and-batch-processing`, `messaging-and-eventing`, `file-and-object-storage`, `search-and-indexing`, `monitoring-alerting-and-slos`, and `security-review` when pipeline correctness depends on those concerns.

## Decision Principles

- Use batch when freshness tolerance is minutes to hours and simpler reruns, lower cost, and easier reconciliation are more valuable than low latency.
- Use streaming when business action requires low latency and the team can operate state, watermarks, ordering, checkpointing, replay, and exactly-once illusions responsibly.
- Use CDC when database changes must feed downstream systems with minimal application changes, but treat CDC records as technical change events, not clean business events.
- Use event-driven ingestion when the source application can publish domain events with stable contracts and idempotent consumers.
- Use ELT when a warehouse or lakehouse can perform transformations with lineage, scalable compute, and governed SQL or notebook workflows.
- Use ETL when data must be filtered, masked, validated, enriched, or reshaped before landing due to security, cost, or downstream compatibility.
- For banking, insurance, and regulated datasets, prefer designs that preserve lineage, reconciliation evidence, approval records, field classification, and reproducible backfills over opaque ad hoc extracts.

## Expected Output Style

- Start with the recommended pipeline pattern and why the freshness and correctness requirements fit it.
- State source-of-truth, data contract, grain, key strategy, freshness SLA, and failure recovery model.
- Separate ingestion, raw landing, validation, transformation, publication, and consumption stages.
- Include operational controls: retries, DLQ, replay, backfill, reconciliation, alerting, and runbooks.
- Prefer tables, checklists, and example failure scenarios over abstract pipeline advice.

## Architecture / Design Guidance

Design pipelines as explicit stages:

1. **Ingest**: pull, push, event, CDC, file drop, API extraction, or stream subscription.
2. **Land raw**: immutable source-shaped data with metadata such as source offset, extraction time, load time, schema version, and run ID.
3. **Validate**: schema checks, required fields, type checks, duplicate detection, referential checks, and business rule thresholds.
4. **Transform**: deterministic logic with versioned code and repeatable inputs.
5. **Publish**: curated tables, marts, topics, search projections, or APIs with documented contracts.
6. **Consume**: BI, ML, operational services, reverse ETL, downstream applications, or external partners.

For Kafka-based or streaming designs, define partition key, ordering scope, consumer group ownership, retention period, compaction behavior, checkpoint storage, poison-message handling, and replay procedure. For CDC, define snapshot strategy, delete semantics, transaction ordering, schema change behavior, and downstream compaction or merge logic. For object-storage landing zones, define immutability, encryption, partitioning, lifecycle, retention/legal hold, file sizing, manifest/checksum behavior, and access controls.

Operational and analytical pipelines must distinguish freshness, completeness, correctness, and publication readiness. A dashboard can be fresh and wrong; a claims, billing, fraud, or regulatory report needs reconciliation and sign-off evidence when it drives decisions or external submissions.

## Implementation Guidance

- Use immutable raw zones where possible so failed transformations can be replayed without re-extracting from source systems.
- Store operational metadata: source system, source primary key, source offset or LSN, event ID, schema version, ingestion timestamp, processing timestamp, run ID, and checksum where useful.
- Make every load idempotent. Re-running the same file, batch, event, or CDC window must not duplicate facts or corrupt aggregates.
- Use merge/upsert logic only with clear natural keys, delete handling, and update timestamp rules.
- Isolate backfills from incremental pipelines with separate run IDs, throttling, monitoring, and rollback or replacement strategy.
- Define quarantine rules for bad records: what is rejected, where it is stored, who owns remediation, and whether publication is blocked.
- Keep transformation code deterministic; avoid hidden dependencies on wall-clock time except through explicit business dates or run parameters.
- Capture lineage and approval metadata for regulated backfills: source snapshot, code version, parameters, approver, run ID, validation results, and downstream consumers notified.

## Testing Expectations

- Test initial load, incremental load, duplicate delivery, missing fields, schema additions, schema removals, renamed fields, deletes, updates, late arrivals, and out-of-order records.
- Test replay from raw data, CDC offsets, Kafka retention, and checkpoint reset without data loss or duplication.
- Test backfills on representative historical data, including high-volume partitions and dirty source records.
- Validate record counts, checksums, uniqueness, referential integrity, accepted/rejected counts, freshness, and business aggregates.
- Run failure tests for source outage, sink outage, partial writes, orchestration retry, poison message, and credential expiration.

## Security / Performance / Reliability Considerations

Security requires classification of fields, PII minimization, masking/tokenization where needed, encrypted storage, least-privilege access, safe logs, retention/legal hold, and governed exports. Performance requires partitioning, file sizing, clustering, compaction, avoiding small-file explosions, controlling source extraction load, bounding streaming state, and planning warehouse/query cost. Reliability requires replayable inputs, durable checkpoints, idempotent writes, freshness alerts, quality alerts, lag alerts, DLQs, backfill controls, and documented recovery steps.

## Review Checklist

- Source, sink, owner, data contract, grain, key strategy, and freshness SLA are explicit.
- Pipeline stages are separated and observable.
- Schema evolution rules cover additive and breaking changes.
- Idempotency, deduplication, ordering, watermarks, and late data handling are defined.
- Bad-record quarantine and data quality gates are actionable.
- Replay and backfill procedures are tested and throttled.
- Reconciliation exists between source, raw, curated, and published outputs.
- Operational alerts cover freshness, volume anomalies, error rate, lag, and quality failures.
- Regulated outputs include lineage, masking, approval, retention, and consumer notification rules.

## Anti-Patterns to Avoid

- Using streaming because it sounds modern when hourly batch satisfies the business SLA.
- Treating CDC rows as business events without reconstructing business meaning.
- Dropping malformed records silently or burying them in logs.
- Running destructive backfills through the same path as incremental loads without isolation.
- Building transformations that depend on current time, mutable reference data, or manual spreadsheet fixes without versioning.
- Letting dashboards consume raw source replicas directly.
- Assuming exactly-once semantics remove the need for idempotent sinks.
- Running regulated backfills or report restatements without approval evidence, consumer communication, and reconciliation sign-off.

## Gotchas / Common Failure Modes

- Deletes and updates are harder than inserts; they must be modeled explicitly in CDC and analytical tables.
- Late-arriving facts break daily aggregates, windowed joins, and SLA dashboards unless watermarks and restatement rules exist.
- Kafka retention shorter than recovery needs makes replay impossible during incidents.
- Backfills can overload source databases, object storage, warehouses, and downstream consumers unless throttled.
- Schema drift often begins as optional fields and becomes a breaking contract when consumers depend on them.
- Duplicate events usually appear during retries, consumer restarts, replay, and producer timeouts.
- Freshness alerts without quality checks can publish wrong data quickly.
- Object storage, search indexes, BI extracts, and reverse ETL copies can retain sensitive data beyond the source retention policy unless lifecycle and deletion propagation are designed.
