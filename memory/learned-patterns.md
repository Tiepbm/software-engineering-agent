# CE7 Learned Patterns

> This file is read by the agent to improve routing and output quality.
> Updated from interaction history. Keep under 50 lines of actionable patterns.
> Last updated: 2026-04-28

## Routing Patterns (from benchmark + real usage)

1. **Payment/money movement** → always include: `security-access-pack` (tenant isolation, audit) + `platform-integration-pack` (outbox, idempotency) + `observability-release-pack` (reconciliation metrics). Never skip security for financial flows.

2. **Migration/schema change** → always include: `observability-release-pack` (expand-contract, rollback gates) + `data-database-analytics-pack` (backfill, reconciliation). Migration is a release problem, not just a data problem.

3. **Document upload/storage** → always include: `storage-search-stack-pack` (signed URLs, scan, retention) + `security-access-pack` (access control, malware). Never serve files before scan completes.

4. **Workflow/approval** → prefer orchestration over choreography when audit trail and manual review are required (banking, insurance, regulated).

5. **Search/Customer 360** → search index is NEVER source of truth. Always enforce authorization at query time, not UI only.

## Output Quality Patterns

6. **Regulated domains** (banking, insurance): always include audit trail design, reconciliation, and operator repair paths. Generic "add logging" is insufficient.

7. **Idempotency**: always specify key scope (tenant + key), storage (Redis lock + DB record), expiry, and what happens on conflict. Never just say "use idempotency key."

8. **Rejected alternatives**: always include at least 2-3 rejected options with concrete reasons. This is what makes output principal-grade vs generic.

## Common Mistakes to Avoid

9. Do NOT route `catastrophe/surge` prompts to `core-engineering-pack`. Route to `resilience-performance-pack` first.

10. Do NOT treat CDC records as clean business events. Always note they need transformation before consumption.

11. Do NOT recommend caching for authorization-sensitive data without explicit invalidation design.
