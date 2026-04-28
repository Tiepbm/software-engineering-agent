---
name: storage-search-pack
description: 'Use when designing object/file storage flows (uploads, signed URLs, retention, legal hold, virus scan) or search/indexing (projection sync, relevance, authorization filtering, reindex). NOT for in-application framework code.'
---
# Storage and Search Pack

## When to Use
- Uploads, downloads, signed URLs, document metadata, retention/legal hold, large files, malware scanning.
- Search projection from system of record, index sync, relevance/ranking, filters, eventual consistency, aliases, reindex/zero-downtime swap.
- Document or asset lifecycle in a regulated domain (claims, policies, KYC, statements).

## When NOT to Use
- Implementing storage/search calls inside framework code → `application-stacks-pack`.
- Choosing the primary OLTP/OLAP database → `data-database-analytics-pack`.
- Distributed runtime cache (Redis, in-memory) → `resilience-performance-pack`.
- Async upload event processing/DLQ → `platform-integration-pack`.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `file-and-object-storage` | Use when designing the upload/download contract, lifecycle policy, signed-URL flow, scan/quarantine pipeline, retention, or legal hold. |
| `search-and-indexing` | Use when designing a search projection from a source of truth, defining relevance/filters, document/field-level authz, reindex/alias swap, or freshness SLO. |

## Cross-Pack Handoffs
- → `security-access-pack` for signed-URL authorization, document-level authz, masking, abuse review.
- → `data-database-analytics-pack` for source-of-truth boundaries and projection lineage.
- → `platform-integration-pack` for upload event/callback handling, scan workers, DLQ.
- → `observability-release-pack` for index lag, scan-queue, and storage-quota SLOs/alerts.

