---
name: legacy-modernization
description: 'Use when modernizing legacy systems: strangler fig pattern, anti-corruption layer, dual-write migration, legacy DB integration, phased cutover, or coexistence strategy for core banking/insurance systems.'
---
# Legacy System Modernization

## When to Use

- Replacing or wrapping a legacy core system (insurance, banking, ERP) while keeping it running.
- Designing coexistence between old and new systems during multi-year migration.
- Building anti-corruption layers to isolate new code from legacy data models.
- Planning phased cutover with rollback capability.
- Integrating new microservices/APIs with legacy databases (Oracle, SQL Server, mainframe).

## Modernization Strategy Selection

| Strategy | When | Risk | Duration |
|---|---|---|---|
| **Strangler Fig** | Legacy has identifiable bounded contexts that can be extracted one at a time | Low-medium per slice | 1-3 years |
| **Big Bang Rewrite** | Legacy is small, well-understood, and team can afford downtime | Very high (usually fails) | 6-18 months |
| **Wrap and Extend** | Legacy works but needs new capabilities (APIs, mobile, analytics) | Low | Ongoing |
| **Lift and Shift** | Move to cloud first, modernize later | Low (infra only) | 1-3 months |
| **Database-First** | Legacy DB is the bottleneck; app layer is acceptable | Medium | 6-12 months |

**Default recommendation for core insurance/banking: Strangler Fig + Anti-Corruption Layer.**

## Strangler Fig Pattern

```
Phase 1: New system handles NEW features only
  Legacy ←→ New (via ACL)
  Users still use legacy for existing features

Phase 2: Migrate feature-by-feature to new system
  Legacy ←→ ACL ←→ New (growing)
  Router directs traffic: old features → legacy, new features → new system

Phase 3: Legacy becomes read-only (reference data, historical queries)
  New system is primary
  Legacy kept for audit/compliance/historical queries

Phase 4: Legacy decommissioned (after data migration + reconciliation)
  All data in new system
  Legacy archived
```

### Implementation Rules

- **One bounded context at a time.** Never migrate "everything" simultaneously.
- **Start with the least risky, most valuable context.** For insurance: start with quote/proposal (new business), not claims (complex, regulated).
- **Router pattern:** API gateway or BFF routes requests to legacy or new system based on feature flag, tenant, or URL path.
- **Data ownership:** During coexistence, ONE system owns each entity. Never dual-master without explicit conflict resolution.
- **Reconciliation:** Daily reconciliation between legacy and new system for shared data during migration.

## Anti-Corruption Layer (ACL)

```
New System → ACL → Legacy System
                    ↓
              Translates:
              - New domain model ↔ Legacy schema
              - New API contracts ↔ Legacy protocols (SOAP, stored procs, flat files)
              - New events ↔ Legacy triggers/batch jobs
              - New auth ↔ Legacy session/token model
```

### ACL Design Rules

| Rule | Reason |
|---|---|
| ACL is a **separate service/module**, not inline code | Isolates legacy coupling; replaceable when legacy dies |
| ACL translates **both directions** | New → Legacy (writes) and Legacy → New (reads/events) |
| ACL owns **no business logic** | Pure translation; business rules live in new system |
| ACL has **its own data model** if needed | Cache/map legacy IDs ↔ new IDs |
| ACL is **tested with contract tests** | Legacy changes must not silently break new system |
| ACL handles **legacy downtime gracefully** | Queue writes, return degraded responses, alert ops |

### ACL for Legacy Database Integration

```
New Service → ACL Service → Legacy DB (Oracle/SQL Server)
                              ↓
                         Read: SQL views or stored procs (read-only)
                         Write: Stored procs or API (never direct INSERT/UPDATE)
                         Events: CDC (Debezium) on legacy tables → Kafka → New System
```

**Rules for legacy DB access:**
- **Read-only** from new system. Never write directly to legacy tables (breaks legacy app's assumptions).
- **Use views or stored procs** that legacy team maintains. New team does not own legacy schema.
- **CDC for events:** Debezium on legacy tables captures changes without modifying legacy code.
- **ID mapping:** Maintain a mapping table `legacy_id ↔ new_id` in the ACL service.

## Dual-Write Migration Pattern

When migrating data ownership from legacy to new system:

```
Phase A: Legacy is master, new system is shadow
  Write → Legacy → CDC → New (shadow copy)
  Read → Legacy
  Reconcile daily: legacy vs new

Phase B: Dual-write (both systems receive writes)
  Write → Legacy + New (in same transaction or via outbox)
  Read → Legacy (primary) + New (for validation)
  Reconcile: compare every write

Phase C: New is master, legacy is shadow
  Write → New → sync → Legacy (for downstream legacy consumers)
  Read → New
  Reconcile: new vs legacy

Phase D: Legacy decommissioned
  Write → New only
  Read → New only
  Legacy archived
```

### Dual-Write Rules

- **Never dual-master without conflict resolution.** One system is always the "source of truth" at any given phase.
- **Outbox pattern for consistency.** Write to primary + outbox in one transaction; relay to secondary async.
- **Reconciliation at every phase.** Compare record counts, checksums, business totals daily.
- **Feature flag per entity.** `policy_master=legacy` or `policy_master=new` — switchable per entity type.
- **Rollback plan per phase.** Phase B → rollback to Phase A by disabling dual-write flag.

## Insurance-Specific Modernization

### Migration Order (recommended)

| Order | Module | Risk | Reason |
|---|---|---|---|
| 1 | **Quote / Proposal** | Low | New business, no legacy data dependency |
| 2 | **Product Catalog** | Low | Reference data, rarely changes |
| 3 | **Policy Issuance** | Medium | Core workflow, but bounded |
| 4 | **Premium / Billing** | Medium-High | Money movement, reconciliation critical |
| 5 | **Claims** | High | Complex workflow, regulated, document-heavy |
| 6 | **Reinsurance** | High | Cross-system, treaty-dependent |
| 7 | **Reporting / Regulatory** | Last | Depends on all other modules being stable |

### Coexistence Challenges

| Challenge | Mitigation |
|---|---|
| **Policy in legacy, claim in new system** | ACL fetches policy data from legacy via read-only API/view. Claim references legacy policy_id via mapping table. |
| **Premium calculated in legacy, billed in new** | ACL translates legacy premium structure to new billing model. Reconcile daily. |
| **Regulatory reports need data from both systems** | Reporting layer queries both via ACL or unified data warehouse (Databricks gold layer). |
| **Users work in both UIs during migration** | Single sign-on (SSO) across both. Deep links from new UI to legacy screens for unmigrated features. |
| **Legacy batch jobs still running** | Coordinate batch windows. New system must not interfere with legacy batch schedules. |

## Anti-Patterns

- Big bang rewrite of core insurance/banking system (almost always fails — too much hidden complexity).
- Direct SQL writes to legacy database from new system (breaks legacy app's invariants).
- Dual-master without conflict resolution (data diverges silently).
- Migrating claims before policy (claims depend on policy data).
- Skipping reconciliation during coexistence ("we'll check later" = never).
- Building the new system without understanding legacy business rules (they're in stored procs, not docs).
- Assuming legacy can be decommissioned on a fixed date (always takes longer).

## Gotchas

- **Legacy stored procedures contain business rules** that are not documented anywhere. Extract and test them before reimplementing.
- **Legacy data quality is worse than expected.** Nulls, duplicates, orphaned records, inconsistent states. Plan data cleansing as a separate workstream.
- **Legacy batch jobs have hidden dependencies.** Job A must complete before Job B starts. Map the full dependency graph before touching anything.
- **Legacy character encoding** (EBCDIC, Windows-1252, mixed encodings) causes data corruption during migration. Test with real production data samples.
- **Legacy date handling** (2-digit years, fiscal calendars, timezone-unaware dates) needs explicit conversion rules.
- **Regulatory reporting** may require data from both systems during coexistence — plan the unified reporting layer early.
- **Team knowledge of legacy system** is often concentrated in 1-2 people. Document before they leave.
- **Performance baseline of legacy** is unknown. Measure before migration so you can prove the new system is at least as fast.

## Review Checklist

- [ ] Modernization strategy chosen with explicit reasoning (not "rewrite because legacy is old").
- [ ] Migration order follows dependency graph (not political priority).
- [ ] Anti-corruption layer designed as separate service with contract tests.
- [ ] Data ownership is clear at every phase (one master per entity).
- [ ] Reconciliation runs daily during coexistence.
- [ ] Rollback plan exists for each migration phase.
- [ ] Legacy business rules extracted and tested before reimplementation.
- [ ] Legacy data quality assessed with real production samples.
- [ ] Regulatory reporting works during coexistence (data from both systems).
- [ ] Legacy team involved in ACL design (they own the legacy schema).
