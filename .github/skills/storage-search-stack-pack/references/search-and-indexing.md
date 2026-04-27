---
name: search-and-indexing
description: 'Designs search and indexing systems with source-of-truth synchronization, relevance, filters, authorization, eventual consistency, reindexing, and operational controls.'
---

# Search and Indexing

## Description

Designs search and indexing systems with source-of-truth synchronization, relevance, filters, authorization, eventual consistency, reindexing, and operational controls.

## Purpose

- Provide reliable full-text, faceted, filtered, and relevance-ranked search without confusing indexes with transactional truth.
- Design synchronization from source-of-truth systems to search indexes with freshness, rebuild, and reconciliation controls.
- Make search safe for regulated data such as documents, claims, policies, customers, transactions, and evidence.

## When to Use

- Designing OpenSearch/Elasticsearch-style indexing, full-text search, faceted search, document search, autocomplete, relevance tuning, or search projections.
- Search results are stale, incomplete, unauthorized, slow, irrelevant, or hard to rebuild.
- Systems need searchable documents, evidence, customer records, claims, policies, or transaction histories.

## Responsibilities

- Define source of truth, index purpose, searchable fields, filterable fields, ranking signals, analyzers, and access controls.
- Design indexing pipeline, freshness targets, retry behavior, dead-letter handling, reindexing, and reconciliation.
- Model eventual consistency and user experience when index state lags source state.
- Monitor indexing lag, query latency, errors, zero-result rate, relevance quality, and authorization failures.

## Decision Principles

- Use search indexes for discovery and retrieval, not as canonical stores for financial, policy, claim, or permission truth.
- Keep authorization enforceable at query time or through safe pre-filtered indexes; never rely on UI filtering.
- Design reindexing before launch; every index will need rebuilds.
- Prefer explicit searchable/filterable fields over dumping entire source objects into the index.
- Treat relevance as a product feature with feedback loops, not a one-time technical setting.

## Expected Output Style

- State source of truth, index consumers, searchable fields, filter fields, and freshness target.
- Include indexing pipeline, consistency model, reindex strategy, and failure handling.
- Define authorization filtering and sensitive field handling.
- Explain relevance and ranking trade-offs.
- Provide operational metrics and validation checks.

## Architecture / Design Guidance

Search architecture should separate source-of-truth storage from search projections. Indexing can use CDC, outbox events, batch rebuilds, or application-published events. Each path needs idempotency, retry, DLQ, lag monitoring, and rebuild procedure.

For regulated systems, index only fields needed for search. Sensitive documents and evidence should use metadata plus secure object storage references; avoid indexing full sensitive text unless access controls, retention, masking, and audit requirements are satisfied.

### Relevance and Ranking Strategy

| Approach | Strong fit | Weakness |
|---|---|---|
| BM25 / TF-IDF (lexical) | Exact terms, IDs, codes, names, structured product/policy/claim search | Synonyms, paraphrases, multilingual recall |
| Vector / dense embeddings (kNN, HNSW) | Semantic similarity, "find similar claims/incidents/policies", FAQ retrieval | Exact identifiers, numeric filters, regulated explainability |
| Hybrid (BM25 + vector, rank fusion) | Default when both keyword precision and semantic recall matter; document/knowledge search | Higher cost, two pipelines to maintain, requires tuning weights |
| Learning-to-rank (LTR) | Mature search with click/conversion telemetry and labeled judgments | Cold start; needs feedback loop and offline evaluation harness |
| Cross-encoder rerank (top-K rerank after retrieval) | High-value top-N (e.g. first page); knowledge agents | Latency cost; only rerank top 50–200, not the whole corpus |

Rules: pick lexical first for regulated identifier-heavy workflows (policy number, claim ID, account, tax code); add vector recall when users describe intent in natural language; use Reciprocal Rank Fusion (RRF) as the default hybrid combiner before tuning weighted scores; reranker latency budget belongs in the API contract.

### Vector Search Specifics

- Embedding model is part of the index contract; rotating it = full reindex with dual-write window.
- Choose distance metric (cosine / dot / L2) consistent with how the embedding was trained.
- HNSW parameters (`M`, `efConstruction`, `efSearch`) trade recall vs latency vs memory; benchmark with representative queries, not synthetic ones.
- Authorization filtering on vector indexes must happen at query time via pre-filters or post-filters; "trust the embedding" is not authorization.
- Store the embedding model version + content hash with each vector so reindex/diff is auditable.

### Reindex and Alias Pattern (zero-downtime)

1. Create `index_v(N+1)` with new mapping/analyzers/embedding.
2. Backfill from source-of-truth (paged, idempotent, rate-limited).
3. Dual-write live updates to both `vN` and `v(N+1)` from the indexing pipeline.
4. Verify counts, sample queries, relevance regression set, and authorization filters.
5. Atomically swap the read alias to `v(N+1)`.
6. Keep `vN` for rollback window (24–72 h), then delete.

## Implementation Guidance

- Define index schema with field types, analyzers, normalizers, filter fields, sort fields, nested fields, and language handling.
- Include source record ID, version, update timestamp, tenant boundary, visibility markers, and index build version.
- Use aliases or versioned indexes for zero-downtime reindexing.
- Implement partial updates carefully; full reindex may be safer when derived fields change.
- Add query limits, pagination strategy, highlighting controls, and timeout behavior.
- Provide fallback behavior when search is unavailable, such as exact ID lookup or degraded browsing.

## Testing Expectations

- Test indexing create, update, delete, permission change, tenant move, and document redaction.
- Test stale index behavior and source-of-truth verification for critical actions.
- Test authorization filters for same-role cross-resource access.
- Test reindexing with production-like volume and zero-downtime alias switch.
- Test relevance with representative queries, misspellings, synonyms, and edge cases.

## Security / Performance / Reliability Considerations

Security requires tenant isolation, field-level sensitivity review, authorization filtering, audit for document access, and no unauthorized cached search results. Performance requires index design, shard sizing, query limits, pagination, and avoiding expensive wildcard or regex patterns. Reliability requires indexing retries, DLQs, lag alerts, snapshots, reindex runbooks, and source-to-index reconciliation.

## Review Checklist

- Source of truth and index purpose are explicit.
- Searchable, filterable, sortable, and sensitive fields are reviewed.
- Authorization is enforced server-side.
- Freshness target and stale behavior are documented.
- Reindex and rebuild procedure exists.
- Indexing failures are visible and repairable.
- Search quality has test queries and feedback signals.
- Critical actions verify source-of-truth state, not only index state.

## Anti-Patterns to Avoid

- Using the search index as the canonical database.
- Indexing all source fields by default.
- Filtering unauthorized results only in the frontend.
- Launching without a reindex strategy.
- Ignoring deletes, permission changes, and document retention.
- Allowing unbounded wildcard queries on public or partner APIs.

## Gotchas / Common Failure Modes

- Permission changes are often harder to index correctly than content changes.
- Eventual consistency can show deleted or unauthorized results unless handled deliberately.
- Relevance tuning can harm exact-match workflows if not tested.
- Reindexing can overload source systems and search clusters.
- An index schema that works for English may fail for names, codes, or multilingual content.
- Search outages need graceful behavior for support and operations teams.

