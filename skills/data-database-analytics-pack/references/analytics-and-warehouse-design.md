---
name: analytics-and-warehouse-design
description: 'Designs governed analytical models, dimensional schemas, marts, semantic layers, warehouse and lakehouse platforms, BI consumption paths, freshness, and cost controls.'
---

# Analytics and Warehouse Design

## Description

Designs governed analytical models, dimensional schemas, marts, semantic layers, warehouse and lakehouse platforms, BI consumption paths, freshness, and cost controls.

## Purpose

- Turn operational data into trustworthy analytical products with explicit grain, lineage, metric ownership, and consumption contracts.
- Choose warehouse, lakehouse, columnar database, data mart, semantic layer, or dashboard dataset patterns based on query workload, governance, cost, and freshness.
- Prevent metric drift, unbounded BI costs, raw-table sprawl, and dashboards that cannot be reconciled to source systems.

## When to Use

- Designing a warehouse, lakehouse, semantic layer, star schema, data mart, dashboard dataset, metric layer, or analytics migration.
- BI users disagree on revenue, churn, conversion, active user, policy count, or other metric definitions.
- Dashboards are slow, warehouse costs are rising, analysts query raw replicas directly, or lakehouse zones have become undocumented dumping grounds.
- Choosing between BigQuery, Snowflake, Redshift, ClickHouse, Databricks, or similar analytical platforms.

## Responsibilities

- Define business process, fact grain, dimensions, slowly changing dimension behavior, conformed dimensions, and metric ownership.
- Separate raw, staged, curated, mart, semantic, and BI presentation layers with clear promotion criteria.
- Decide partitioning, clustering, sort keys, materialization, aggregation, and refresh patterns from query workload and freshness needs.
- Govern PII, row-level access, column masking, exports, lineage, certified datasets, and metric definitions.
- Make analytical outputs reconcilable to source systems and explainable to business owners.

## Decision Principles

- Use star schemas for BI-friendly dimensional analysis unless the engine and workload strongly favor wide denormalized tables.
- Keep fact tables at the lowest useful grain; aggregate in marts, materialized views, or semantic models, not by destroying source detail too early.
- Use conformed dimensions when teams need cross-domain analysis; allow mart-specific dimensions only when the domain meaning is intentionally local.
- Use lakehouse platforms when open storage, raw history, ML/data science, notebooks, and mixed workloads matter.
- Use warehouses when governed SQL analytics, BI concurrency, predictable performance, and managed operations dominate.
- Use ClickHouse-style columnar serving when low-latency analytical queries over high-volume event data matter and the team can design sort/order keys correctly.

## Expected Output Style

- State the analytical grain, primary consumers, freshness target, and metric ownership before proposing tables.
- Include a layer diagram or list: raw, staging, curated, mart, semantic, BI.
- Provide fact/dimension definitions, metric formulas, SCD behavior, partition/clustering choices, and governance controls.
- Call out cost drivers and query anti-patterns explicitly.
- Include validation and reconciliation checks, not just model names.

## Architecture / Design Guidance

Use a layered analytical architecture:

1. **Raw**: immutable source-shaped data with ingestion metadata.
2. **Staging**: standardized types, names, time zones, deduplication, and source corrections.
3. **Curated core**: reusable business entities and conformed dimensions.
4. **Marts**: business-process-specific facts and dimensions optimized for consumption.
5. **Semantic layer**: certified metric definitions, role-based access, and business-friendly names.
6. **BI products**: dashboards, extracts, reverse ETL, notebooks, and ML features with owners.

Platform fit matters. BigQuery favors serverless scale and partition/clustering discipline; Snowflake favors managed warehouse separation and governance features; Redshift favors AWS-integrated warehouse workloads with distribution/sort design; ClickHouse favors fast columnar analytics with careful ordering and ingestion design; Databricks favors lakehouse, Spark, ML, open formats, and mixed batch/streaming workloads. Do not choose a platform without expected concurrency, data volume, latency, governance, ecosystem, and cost model.

## Implementation Guidance

- Document fact grain in the first paragraph of every fact table definition: one row per what, at what time, at what business level.
- Define metric formulas with numerator, denominator, filters, time window, timezone, late-data behavior, and owner.
- Use surrogate keys for dimensions when SCD Type 2 or historical joins are required; do not overwrite history when reports need past truth.
- Partition by common time filters and retention boundaries; cluster, sort, or order by high-selectivity predicates and join keys used by common queries.
- Materialize expensive joins and aggregates only when freshness, rebuild cost, and invalidation behavior are defined.
- Publish certified datasets for BI users; restrict direct access to raw and staging layers unless the user is doing governed exploration.
- Add cost controls: query limits, warehouse sizing rules, scheduled materialization, dashboard cache strategy, and alerts for scan or credit spikes.

## Testing Expectations

- Reconcile row counts and key aggregates from raw to staging to curated to mart outputs.
- Test metric formulas against hand-calculated examples and known business periods.
- Test SCD behavior, late-arriving facts, fiscal calendars, timezone boundaries, null handling, deduplication, and deleted source records.
- Test dashboard performance with realistic filters, concurrency, and worst-case date ranges.
- Monitor freshness, volume anomalies, distribution changes, cost spikes, and failed model builds.

## Security / Performance / Reliability Considerations

Security requires PII classification, row-level and column-level access, masking, export controls, audit logs, and least-privilege BI access. Performance requires partition pruning, clustering/sort keys, pre-aggregation, bounded dashboards, and avoiding full-table scans. Reliability requires freshness SLAs, lineage, reproducible transformations, rollback of bad models, restatement policy, and source-to-report reconciliation.

## Review Checklist

- Fact grain is explicit and matches the business process.
- Metric definitions have owners, formulas, filters, time windows, and examples.
- Dimensions are conformed where cross-domain reporting requires shared meaning.
- SCD behavior and history requirements are documented.
- BI users consume certified marts or semantic models, not raw OLTP replicas.
- Partitioning, clustering, sorting, and materialization match actual query patterns.
- Freshness, quality, lineage, access control, and cost targets are monitored.
- Reports can be reconciled to source systems or known financial/control totals.

## Anti-Patterns to Avoid

- Building dashboards directly on source application tables or raw CDC replicas.
- Creating one giant table without declared grain, owner, or refresh semantics.
- Letting each dashboard define revenue, active user, or churn differently.
- Partitioning on low-selectivity columns or ignoring common date filters.
- Hiding expensive transformations inside BI tools where they cannot be tested or governed.
- Treating a lakehouse as cheap storage without contracts, compaction, retention, or ownership.
- Using extracts to bypass access controls or semantic consistency.

## Gotchas / Common Failure Modes

- Revenue, churn, active-user, conversion, and retention metrics usually hide policy decisions, not just SQL formulas.
- Time zones, fiscal calendars, daylight saving changes, and late-arriving data silently change trends.
- Slowly changing dimensions can make historical reports wrong if overwritten attributes are joined to old facts.
- BI tools can generate expensive SQL and bypass intended pruning.
- Freshness promises create operational obligations; late but correct may be better than fast and wrong.
- Data marts become untrusted when reconciliation failures are not visible and owned.
- Cost controls added after dashboard rollout are harder because users already depend on expensive behavior.
