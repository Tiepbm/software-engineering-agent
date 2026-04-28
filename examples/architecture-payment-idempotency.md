# Architecture Example — Idempotent Payment Retries

> Shape: decision → packs/refs consulted → assumptions → contract → rejected alternatives → tests → operational signals → open questions.

**Decision**: Introduce a client-generated `Idempotency-Key` (UUIDv4, scoped per logical payment attempt) on `POST /v1/payments`, stored server-side with request hash + final response for 24 h.

**Packs / references consulted**:
- `core-engineering-pack/api-design` — idempotency contract, error model.
- `platform-integration-pack/messaging-and-eventing` — outbox dedupe to PSP / downstream.
- `resilience-performance-pack/caching-and-distributed-state` — Redis NX lock store.
- `data-database-analytics-pack/database-reliability-and-operations` — durable record growth.
- `security-access-pack/security-review` — cross-tenant key reuse.

**Constraints assumed (please confirm)**:
- Payment service is system of record for charge state.
- Mobile clients can be offline up to N minutes and may retry.
- Downstream PSP supports its own idempotency window (typically 24 h).

**Contract** (additive, non-breaking):
- Header `Idempotency-Key: <uuid>` REQUIRED for `POST /v1/payments`; reject `400 idempotency_key_required` (gated by feature flag during rollout).
- Server stores `(tenant_id, idempotency_key) → request_hash + response_snapshot + status` with 24 h TTL.
- Same key + same hash → return stored response (`200/201`, original body).
- Same key + different hash → `409 idempotency_key_conflict`.
- Same key while in-flight → `409 idempotency_in_progress`; client backs off.

**Storage**: Redis `SET NX PX` for in-flight lock; Postgres `payment_idempotency` table for the durable record (Redis is cache, Postgres is truth — see `caching-and-distributed-state`). Composite key includes `tenant_id` (see `security-review`).

**Downstream**: PSP call passes a derived idempotency token (NOT the raw client key). Outbox event for `payment.captured` deduped on the same logical key (see `messaging-and-eventing`).

**Rejected alternatives**:
1. Server-generated key in response — fails offline retry.
2. Hash of request body as key — false dedupes when user legitimately retries same amount.
3. No idempotency, rely on PSP — DB charges twice while PSP dedupes once.

**Tests required**:
- Same key + same body → one charge, identical response twice.
- Same key + different body → `409`, no second charge.
- Network failure mid-call → retry succeeds, one charge total.
- Two concurrent requests, same key → exactly one wins, the other gets `409 in_progress`.
- Cross-tenant key reuse → treated as new key (no leak).
- 24 h after expiry → key reusable; window does not extend silently.

**Operational**:
- Metric: `idempotency_replay_total{result="hit|conflict|in_progress"}`.
- Alert: replay-hit rate > 5 % sustained = client retry storm or upstream timeout misconfigured.
- Storage growth budget: ~2 KB × peak rps × 86 400 s.

**Open questions**:
1. Cross-region idempotency (active-active) or per-region sufficient?
2. PSP's own idempotency window — must align with ours.
3. Archive expired keys for audit/reconciliation beyond 24 h?

