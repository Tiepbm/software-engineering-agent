---
name: data-modeling
description: 'Models entities, aggregates, relationships, transactions, history, auditability, consistency, query patterns, derived state, and reporting implications.'
---
# Data Modeling
## Description
Models entities, aggregates, relationships, transactions, history, auditability, consistency, query patterns, derived state, and reporting implications.
## Purpose
- Create data models that preserve business meaning, transactional integrity, query efficiency, and future reporting needs.
- Identify aggregates, relationships, lifecycle states, ownership, history, and correction behavior.
- Balance normalization, denormalization, derived projections, and operational simplicity using actual access patterns.
- Prevent caches, search indexes, event payloads, reports, and object metadata from becoming accidental sources of truth.
## When to Use
- Designing new persisted data, changing schema, migrating data, adding reporting needs, or introducing a new source of truth.
- A model has duplicated meanings, unclear ownership, missing history, slow queries, or difficult data correction.
- The team must decide aggregate boundaries, relationship cardinality, audit strategy, or denormalization.
- The data model feeds events, caches, search indexes, analytics, object-storage metadata, workflows, or regulated reporting.
## Responsibilities
- Identify entities, value objects, aggregates, reference data, lifecycle states, invariants, and transactional boundaries.
- Define cardinality, nullability, uniqueness, constraints, retention, history, and audit needs.
- Map write paths and read paths separately, then choose where denormalization is justified.
- Make reporting, analytics, and downstream data contracts visible during model design.
- Define source-of-truth ownership, derived-state refresh rules, event payload boundaries, search/index fields, cacheable values, and object metadata when those consumers exist.
- Involve `database-architecture`, `messaging-and-eventing`, `caching-and-distributed-state`, `search-and-indexing`, `file-and-object-storage`, `analytics-and-warehouse-design`, and `security-review` when the model crosses those concerns.
## Decision Principles
- Normalize core OLTP facts that require integrity; denormalize read models only for measured query or ownership reasons.
- Put invariants close to the data with constraints when correctness matters.
- Use surrogate keys for internal identity and natural keys for uniqueness when business identity exists.
- Model history explicitly when decisions, compliance, billing, or audit depend on past truth.
- Treat lifecycle state as a domain concept with allowed transitions, actors, timestamps, and reasons; avoid one overloaded status field for unrelated workflows.
- Store object bytes, search projections, analytics facts, and cache entries outside the core model only when their ownership, rebuild, retention, and authorization behavior are defined.
- For banking, insurance, and regulated workloads, prefer traceable corrections and immutable business history over destructive updates that erase decision evidence.
## Expected Output Style
- Start with the decision or finding, then provide the reasoning needed to trust it.
- Separate immediate actions from longer-term improvements.
- State assumptions, constraints, trade-offs, risks, and missing information explicitly.
- Use concrete examples, acceptance criteria, contracts, schemas, queries, or checklists when they reduce ambiguity.
- Avoid generic advice unless it is followed by an enforceable rule or verification step.
## Architecture / Design Guidance
Data modeling must define the system of record, aggregate boundaries, consistency expectations, and downstream consumers. For every important fact, name where it is authored, where it is copied, who may correct it, how history is retained, and how consumers learn about changes.

Model write-side truth separately from read-side convenience:

- **Canonical state**: the authoritative OLTP record with constraints, ownership, correction rules, and audit history.
- **Derived read models**: denormalized tables, cached values, search documents, and API projections with freshness and rebuild rules.
- **Event contracts**: stable facts emitted for integration; they should not expose internal persistence noise or unbounded object graphs.
- **Analytical facts**: governed reporting grain, slowly changing dimensions, and late-data behavior.
- **Object metadata**: document ownership, scan status, retention class, legal hold, checksum, and object version; never rely on object path alone for authorization.

For event-driven systems, model both current state and event history, including replay behavior, schema evolution, idempotency keys, and correction events. For search and cache consumers, model permission changes and invalidation as first-class changes, not background implementation details.
## Implementation Guidance
Specify table or collection names, fields, types, constraints, indexes, foreign keys, document shape, partition keys, and migration path. Document derived fields and their refresh semantics. Avoid broad JSON blobs unless schema variability is real, validation is explicit, and query patterns support it.

Include for each important entity:

- business identifier and internal identifier;
- owner and lifecycle states;
- required invariants and database constraints;
- audit fields and correction path;
- retention, deletion, legal hold, and masking behavior;
- events emitted when it changes;
- cache/search/analytics/object-storage projections that must be updated or rebuilt.

Use uniqueness constraints for idempotency keys, external references, natural keys, and duplicate prevention where correctness depends on them. Use version columns, optimistic concurrency, or explicit transition guards for contested updates such as payments, claims, approvals, policy changes, and document review.
## Testing Expectations
- Test uniqueness, nullability, referential integrity, lifecycle transitions, invalid states, and historical queries.
- Add migration tests with representative dirty production data.
- Verify read patterns use intended indexes and do not require full scans at expected volume.
- Test correction flows, permission changes, soft deletes, retention boundaries, and legal hold conflicts.
- Reconcile canonical records against cache entries, search documents, event consumers, analytical tables, and object metadata after migration, replay, or backfill.
## Security / Performance / Reliability Considerations
Sensitive fields require classification, encryption choices, retention, deletion, masking, export controls, and audit rules. Performance depends on query-pattern-driven indexes, partitioning, bounded relationships, and avoiding unbounded aggregate loading. Reliability depends on constraints, backups, migration reversibility, correction tooling, derived-state rebuilds, and reconciliation jobs that prove copies match the source of truth.
## Review Checklist
- Entities and aggregates match business language.
- Transactional boundaries are explicit.
- Constraints protect critical invariants.
- History and audit are modeled where needed.
- Indexes match query patterns.
- Reporting impact is considered.
- Migration and backfill plan exists.
- Derived state, events, caches, search indexes, analytics, and object metadata have ownership and rebuild rules.
- Permission, tenant, retention, and deletion behavior are modeled across every copy of the data.
## Anti-Patterns to Avoid
- Using one generic status field for unrelated lifecycle states.
- Storing important queryable data only inside opaque JSON.
- Skipping constraints because validation exists in application code.
- Creating many-to-many relationships without ownership or lifecycle rules.
- Ignoring deleted, corrected, merged, and duplicated records.
- Treating cache keys, search documents, event payloads, object paths, or analytics tables as undocumented extensions of the data model.
- Publishing internal entity schemas directly as API or event contracts.
## Gotchas / Common Failure Modes
- Names like customer, user, account, and member often hide different concepts.
- Soft deletes break uniqueness and reporting unless modeled deliberately.
- Denormalized snapshots need refresh and reconciliation rules.
- Audit logs are not a replacement for queryable business history.
- Changing cardinality later is often more expensive than adding a field.
- Permission and tenant changes are easy to update in the canonical store but miss caches, search indexes, exports, and downstream marts.
- Backfills can create historically impossible states unless lifecycle transitions and effective dates are modeled.
- Event replay can resurrect old meanings if schema versions and correction events are not explicit.

## Worked Example: Tracking Policy Holder Address Changes (SCD Type 2)

**Problem**: Insurance policies must be priced and audited against the address that was in effect at the time of each renewal, claim, or premium calculation — not today's address. A single mutable `customer.address` column loses history; an append-only audit log is queryable only with effort. SCD (Slowly Changing Dimension) Type 2 is the standard pattern.

**Schema**:

```sql
CREATE TABLE customer_address_history (
  customer_id        BIGINT       NOT NULL,
  address_line1      TEXT         NOT NULL,
  address_line2      TEXT,
  city               TEXT         NOT NULL,
  region             TEXT         NOT NULL,
  postal_code        TEXT         NOT NULL,
  country_code       CHAR(2)      NOT NULL,
  valid_from         TIMESTAMPTZ  NOT NULL,
  valid_to           TIMESTAMPTZ  NOT NULL DEFAULT 'infinity',
  is_current         BOOLEAN      GENERATED ALWAYS AS (valid_to = 'infinity') STORED,
  recorded_at        TIMESTAMPTZ  NOT NULL DEFAULT now(),
  recorded_by        TEXT         NOT NULL,            -- user / system / migration
  source_event_id    UUID,                              -- audit trace to triggering event
  correction_of      BIGINT,                            -- self-FK if this row corrects an earlier one
  PRIMARY KEY (customer_id, valid_from),
  EXCLUDE USING gist (
    customer_id WITH =,
    tstzrange(valid_from, valid_to, '[)') WITH &&
  )                                                    -- no overlapping validity windows
);

CREATE UNIQUE INDEX one_current_per_customer
  ON customer_address_history (customer_id) WHERE is_current;
```

**Write path (apply a change)** — single transaction:
1. `UPDATE ... SET valid_to = :now WHERE customer_id = :id AND is_current` (close current row).
2. `INSERT` new row with `valid_from = :now`, `valid_to = 'infinity'`.
3. Emit `customer.address_changed` outbox event with both old and new snapshots.

**Read patterns**:
- Current address: `WHERE is_current` (covered by partial unique index).
- Address as-of a date: `WHERE valid_from <= :asof AND valid_to > :asof`.
- Used by claim adjudication: `JOIN ... ON valid_from <= claim.event_date AND valid_to > claim.event_date`.

**Why not the alternatives**:
- **SCD Type 1 (overwrite)**: loses history; cannot reprice or audit retroactively.
- **SCD Type 3 (previous-value column)**: only keeps one prior value; insufficient for multi-year history.
- **Append-only event log only**: requires snapshot rebuilds for every read; not a query primitive.
- **Soft delete + new row**: ambiguous current-state without the validity range; breaks the EXCLUDE constraint guarantee.

**Gotchas**:
- Corrections (data-fix) need `correction_of` + a new validity row, not an `UPDATE` of historical rows — historical truth must be immutable for audit.
- Time zones: `valid_from`/`valid_to` are `TIMESTAMPTZ`; downstream marts must convert to business calendar consistently.
- Downstream (search index, BI, CDC) must understand "current row" semantics to avoid showing every historical row in dashboards.

