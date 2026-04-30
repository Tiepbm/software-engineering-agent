---
name: databricks-lakehouse
description: 'Use when designing Databricks/lakehouse architecture: medallion layers, Delta Lake, Unity Catalog, CDC ingestion from RDBMS, notebook vs job pipelines, cost control, or insurance/banking analytical models.'
---
# Databricks and Lakehouse Architecture

## When to Use

- Designing bronze/silver/gold (medallion) data layers on Databricks or similar lakehouse.
- Ingesting data from RDBMS (Oracle, SQL Server, PostgreSQL) via CDC or batch into Delta Lake.
- Choosing between notebooks, jobs, DLT (Delta Live Tables), or Spark Structured Streaming.
- Designing Unity Catalog governance (catalogs, schemas, row/column security, lineage).
- Building insurance/banking analytical models (policy, claims, premium, reserve, bordereaux).
- Controlling Databricks cost (cluster sizing, photon, spot instances, auto-termination).

## Medallion Architecture

| Layer | Purpose | Format | Freshness | Governance |
|---|---|---|---|---|
| **Bronze** | Raw ingestion, immutable, source-shaped | Delta Lake (append-only) | Near-real-time (CDC) or daily (batch) | Minimal — preserve source fidelity |
| **Silver** | Cleaned, deduplicated, standardized types/names/timezones, referential integrity checked | Delta Lake (merge/upsert) | Minutes to hours | Schema enforced, PII tagged |
| **Gold** | Business-ready: facts, dimensions, metrics, marts, semantic layer | Delta Lake (overwrite or merge) | Hours to daily | Certified, row/column security, lineage tracked |

### Rules

- Bronze is **append-only**. Never update or delete bronze records — they are the audit trail.
- Silver handles **deduplication, type casting, null handling, timezone normalization**. One silver table per source entity.
- Gold is **business-grain aligned**. One fact table per business process (policy issuance, claim settlement, premium collection). Dimensions are conformed where cross-domain analysis is needed.
- Each layer has its own **schema** in Unity Catalog: `bronze.policy_raw`, `silver.policy_cleaned`, `gold.fact_premium`.

## CDC Ingestion from Legacy RDBMS

### Pattern: RDBMS → CDC → Bronze

| Source | CDC Tool | Landing |
|---|---|---|
| Oracle | Debezium + Kafka, or Oracle GoldenGate, or Fivetran | Bronze Delta table |
| SQL Server | Debezium + Kafka, or SQL Server CDC + ADF, or Fivetran | Bronze Delta table |
| PostgreSQL | Debezium + Kafka (logical replication), or Fivetran | Bronze Delta table |

### CDC Bronze Table Schema

```sql
-- Bronze: raw CDC events, append-only
CREATE TABLE bronze.policy_cdc (
  _cdc_operation   STRING,        -- INSERT, UPDATE, DELETE
  _cdc_timestamp   TIMESTAMP,     -- When change happened at source
  _cdc_source      STRING,        -- Source system identifier
  _cdc_offset      STRING,        -- Kafka offset or LSN for replay
  _ingested_at     TIMESTAMP,     -- When landed in bronze
  _batch_id        STRING,        -- Pipeline run ID
  payload          STRING         -- Raw JSON from CDC (preserve source schema)
);
```

### Silver Merge (SCD Type 1 or Type 2)

```sql
-- Silver: merge CDC into current-state table
MERGE INTO silver.policies AS target
USING (
  SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (
      PARTITION BY payload:policy_id
      ORDER BY _cdc_timestamp DESC
    ) AS rn
    FROM bronze.policy_cdc
    WHERE _ingested_at > '${last_processed_timestamp}'
  ) WHERE rn = 1
) AS source
ON target.policy_id = source.payload:policy_id
WHEN MATCHED AND source._cdc_operation != 'DELETE' THEN UPDATE SET
  target.policy_number = source.payload:policy_number,
  target.status = source.payload:status,
  target.premium = source.payload:premium,
  target.updated_at = source._cdc_timestamp
WHEN NOT MATCHED AND source._cdc_operation != 'DELETE' THEN INSERT (
  policy_id, policy_number, status, premium, created_at, updated_at
) VALUES (
  source.payload:policy_id, source.payload:policy_number,
  source.payload:status, source.payload:premium,
  source._cdc_timestamp, source._cdc_timestamp
)
WHEN MATCHED AND source._cdc_operation = 'DELETE' THEN UPDATE SET
  target.is_deleted = true, target.deleted_at = source._cdc_timestamp;
```

## Insurance Domain — Gold Layer Models

### Fact Tables

| Fact | Grain | Key measures | Source |
|---|---|---|---|
| `fact_premium` | One row per premium transaction per policy per period | gross_premium, net_premium, tax, commission | Silver: policies + premium_transactions |
| `fact_claim` | One row per claim event (FNOL, assessment, payment, recovery) | claim_amount, paid_amount, reserved_amount, recovery_amount | Silver: claims + claim_payments |
| `fact_policy_movement` | One row per policy state change (new, renewal, endorsement, cancellation) | count, premium_delta | Silver: policies + endorsements |
| `fact_bordereaux` | One row per policy-claim-transaction per reporting month per treaty | gross, ceded, retained, cession_pct | Silver: policies + claims + treaties |

### Conformed Dimensions

| Dimension | SCD Type | Key attributes |
|---|---|---|
| `dim_policy` | Type 2 (versioned) | policy_number, LOB, product, effective_date, expiry_date, status |
| `dim_customer` | Type 2 | customer_id, name (masked), segment, region |
| `dim_date` | Type 1 | calendar_date, fiscal_year, fiscal_quarter, is_business_day |
| `dim_branch` | Type 1 | branch_code, branch_name, region, zone |
| `dim_treaty` | Type 2 | treaty_id, treaty_type, layer, retention, limit |

## Notebook vs Job vs DLT

| Option | Use when | Avoid when |
|---|---|---|
| **Notebook (interactive)** | Exploration, ad-hoc analysis, prototyping, data quality investigation | Production pipelines (no scheduling, no retry, no monitoring) |
| **Job (scheduled)** | Production ETL/ELT, scheduled batch, parameterized runs, CI/CD deployed | Interactive exploration |
| **DLT (Delta Live Tables)** | Declarative pipeline with auto-dependency, expectations (data quality), auto-scaling | Complex custom logic, non-SQL transformations, cost-sensitive (DLT has premium pricing) |
| **Structured Streaming** | Near-real-time CDC processing, event streaming, sub-minute freshness | Batch-only workloads (over-engineering) |

## Unity Catalog Governance

| Concept | Insurance application |
|---|---|
| **Catalog** | One per environment: `dev`, `staging`, `prod` |
| **Schema** | One per layer: `bronze`, `silver`, `gold`, `sandbox` |
| **Table** | Named by entity: `gold.fact_premium`, `silver.policies` |
| **Row-level security** | Filter by branch/region for branch-level analysts |
| **Column masking** | Mask customer PII (name, ID number, phone) for non-privileged users |
| **Lineage** | Auto-tracked by Unity Catalog — shows bronze → silver → gold flow |
| **Data classification** | Tag PII columns, financial columns, regulated columns |

## Cost Control

| Control | Mechanism |
|---|---|
| **Cluster auto-termination** | 10-15 min idle timeout for interactive; jobs terminate on completion |
| **Spot instances** | Use for non-SLA batch jobs (60-90% savings); avoid for streaming |
| **Photon** | Enable for SQL-heavy workloads (2-8x faster, included in some SKUs) |
| **Cluster sizing** | Start small, scale based on Spark UI metrics (shuffle, spill, GC) |
| **Job clusters** | Dedicated per-job clusters (not shared interactive) for production |
| **Delta optimization** | OPTIMIZE + ZORDER on query-heavy tables; VACUUM after 7 days |
| **Serverless SQL warehouse** | For BI/dashboard queries — auto-scales, pay-per-query |

## Anti-Patterns

- Using notebooks as production pipelines (no version control, no retry, no monitoring).
- Skipping bronze layer and transforming directly from source (loses audit trail and replay ability).
- Gold tables without declared grain (one giant denormalized table with no clear "one row per what").
- Unity Catalog not configured (no lineage, no access control, no PII tagging).
- Running OPTIMIZE on every write (expensive; schedule daily or weekly based on table size).
- Streaming for everything when hourly batch satisfies the business SLA.
- Storing secrets in notebooks (use Databricks secret scopes backed by Azure Key Vault or AWS Secrets Manager).

## Gotchas

- **Delta Lake merge performance**: large merges on unpartitioned tables are slow. Partition by date or tenant for large tables.
- **Schema evolution**: Delta supports additive schema evolution (`mergeSchema`), but column renames/type changes require manual migration.
- **CDC delete handling**: Debezium DELETE events need explicit handling in merge logic — don't just ignore them.
- **Timezone**: Bronze preserves source timezone; silver must normalize to UTC; gold converts to business timezone for reporting.
- **Late-arriving data**: Bronze accepts everything; silver/gold must handle late arrivals (reprocess affected partitions).
- **Cost surprise**: Auto-scaling clusters + long-running notebooks = unexpected bills. Set budget alerts.
- **Unity Catalog migration**: Existing hive_metastore tables need migration to Unity Catalog — plan this early.

## Review Checklist

- [ ] Medallion layers defined (bronze/silver/gold) with clear purpose per layer.
- [ ] CDC ingestion preserves source fidelity in bronze (append-only, raw payload).
- [ ] Silver handles dedup, type casting, null handling, timezone normalization.
- [ ] Gold fact tables have declared grain matching business process.
- [ ] Dimensions are conformed where cross-domain analysis is needed.
- [ ] Unity Catalog configured: catalogs, schemas, row/column security, PII tags, lineage.
- [ ] Cost controls: auto-termination, spot for batch, job clusters for production.
- [ ] Data quality checks at silver→gold boundary (expectations or custom validation).
- [ ] Reconciliation between source system totals and gold layer totals.
- [ ] Secrets in Databricks secret scopes, not in notebooks or environment variables.
