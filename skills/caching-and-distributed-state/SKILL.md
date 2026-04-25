---
name: caching-and-distributed-state
description: 'Designs safe caching and distributed state with TTLs, invalidation, staleness rules, Redis-style patterns, locks, sessions, hot-key controls, and consistency trade-offs.'
---

# Caching and Distributed State

## Description

Designs safe caching and distributed state with TTLs, invalidation, staleness rules, Redis-style patterns, locks, sessions, hot-key controls, and consistency trade-offs.

## Purpose

- Improve latency, throughput, and dependency protection without weakening correctness or authorization.
- Make cache staleness, invalidation, ownership, and fallback behavior explicit.
- Use distributed state only when it is safer and simpler than recomputing or querying the source of truth.

## When to Use

- Designing cache-aside, read-through, write-through, write-behind, session storage, distributed locks, rate-limit counters, or idempotency records.
- A system has slow reads, repeated expensive queries, hot keys, cache stampedes, stale data bugs, or inconsistent distributed state.
- Banking or insurance workflows need careful handling of customer, policy, claim, payment, document, or entitlement state.

## Responsibilities

- Define what is cached, why it is cached, source of truth, freshness tolerance, invalidation rules, and fallback behavior.
- Choose cache pattern and storage technology based on consistency, latency, durability, and operating requirements.
- Design key structure, tenant isolation, TTLs, serialization, compression, size limits, and eviction behavior.
- Control hot keys, cache stampedes, lock safety, and failure behavior.

## Decision Principles

- Cache derived or expensive-to-read data only when stale behavior is acceptable or controlled.
- Do not cache authorization-sensitive data unless tenant/user isolation and invalidation are explicit.
- Prefer cache-aside for simple read optimization; use write-through or write-behind only when write semantics and failure recovery are clear.
- Use distributed locks sparingly and only with timeouts, ownership tokens, and safe unlock behavior.
- Treat Redis-style stores as operational dependencies with capacity, persistence, failover, and security requirements.

## Expected Output Style

- State the cache purpose, source of truth, staleness tolerance, and invalidation strategy.
- Include key design, TTL, eviction behavior, stampede protection, and fallback behavior.
- Call out consistency and authorization risks.
- Separate caching for performance from distributed state used for coordination.
- Provide reviewable metrics and tests.

## Architecture / Design Guidance

Caching architecture must preserve a clear source of truth. Cache-aside is usually simplest: read from cache, load from source on miss, then populate. Read-through centralizes loading but can hide expensive behavior. Write-through improves consistency but adds write latency and cache dependency. Write-behind can improve write latency but risks data loss and is unsafe for financial or regulated state unless durability and reconciliation are proven.

Distributed locks should protect short critical sections only. For long-running workflows, use database constraints, workflow state, leases, or idempotency records instead of fragile locks.

## Implementation Guidance

- Use namespaced keys that include environment, tenant boundary, entity type, identifier, version, and purpose.
- Define TTL based on business freshness, not arbitrary defaults.
- Add explicit invalidation for updates that affect correctness.
- Use request coalescing, single-flight loading, jittered TTLs, or soft TTLs to prevent stampedes.
- Store idempotency records with request hash, status, result reference, and expiration policy.
- Monitor hit rate, miss rate, latency, evictions, memory, hot keys, errors, and stale-data incidents.
- Encrypt or avoid sensitive values where cache operators or logs could expose data.

## Testing Expectations

- Test cache hit, miss, stale read, invalidation, eviction, cache outage, and source-of-truth fallback.
- Test concurrent requests for stampede behavior and duplicate writes.
- Test tenant/user isolation in cache keys.
- Test distributed lock timeout, owner token mismatch, process crash, and retry behavior.
- Test idempotency record reuse and expiration.

## Security / Performance / Reliability Considerations

Security requires tenant isolation, no secrets in cache values, restricted access, encrypted transport, and safe logs. Performance requires bounded object size, hot-key mitigation, memory planning, and avoiding cache stampedes. Reliability requires fallback behavior, failover awareness, persistence decisions, monitoring, and clear degraded mode when cache is unavailable.

## Review Checklist

- Source of truth is explicit.
- Staleness tolerance and invalidation rules are defined.
- Cache keys enforce tenant and user isolation.
- TTLs match business risk.
- Stampede and hot-key controls exist.
- Cache outage behavior is safe.
- Distributed locks include timeout, owner token, and safe release.
- Metrics expose hit rate, errors, evictions, memory, and stale-data risk.

## Anti-Patterns to Avoid

- Using cache to hide a broken query or data model.
- Caching permission, balance, claim status, or policy coverage without strict invalidation and risk approval.
- Using distributed locks for long-running business workflows.
- Building write-behind for regulated transactions without durable recovery.
- Sharing cache keys across tenants or users.
- Treating Redis persistence as equivalent to a transactional database without analysis.

## Gotchas / Common Failure Modes

- Stale cache entries can become correctness defects, not just UX issues.
- Cache stampedes often appear after deploys, failovers, or mass expiration.
- Hot keys can overload a single shard even when the cluster has spare capacity.
- Distributed locks can expire while work continues, allowing concurrent writers.
- Cache outages can overload the source database if fallback is unbounded.
- Authorization changes must invalidate cached access decisions immediately enough for the risk.

