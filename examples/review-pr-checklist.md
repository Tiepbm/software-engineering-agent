# Review Example — PR Adding Migration + Canary Rollout

> Shape: assessment → strengths → critical issues → medium issues → architecture/data concerns → technical debt → refactoring plan → priority order.

**Overall assessment**: PR introduces a new `policy_endorsement` table and a backfill script for in-flight policies, with a 10% canary rollout behind feature flag `policy_endorsement_v2`. Direction is correct but rollout safety is **not yet production-ready**.

Packs/refs consulted: `core-engineering-pack/code-review-and-refactoring`, `data-database-analytics-pack/database-reliability-and-operations`, `observability-release-pack/devops-and-release`, `security-access-pack/security-review`.

## Strengths
- Schema change is additive (expand-contract, phase 1).
- Feature flag gates new write path.
- Backfill script supports `--resume-from <checkpoint>`.

## Critical issues (block merge)
1. **No tested rollback**: PR description says "rollback = revert flag", but the new code writes to BOTH old and new tables in shadow mode — reverting the flag does NOT clean up partial writes. Must add a `cleanup_orphan_endorsements` reconciliation job and run a rollback drill in staging.
2. **Backfill is not idempotent**: Re-running on the same range double-inserts. Add `ON CONFLICT (policy_id, effective_date) DO UPDATE` and a unit test that re-runs the same chunk.
3. **Sensitive data in logs**: `logger.info("endorsing policy", policy)` logs the full row including `customer_dob`. Add field-level redaction (see `logging-metrics-and-tracing`).
4. **Canary has no abort gate**: 10% rollout has no SLO check. Add an automated abort on `endorsement_error_rate > 1 %` for 5 min (see `devops-and-release`).

## Medium issues
- `policy_endorsement.id` uses `BIGSERIAL` — fine, but include creation in migration with explicit `START WITH` to avoid collisions across regions.
- Index `idx_policy_endorsement_effective_date` is missing partial predicate; will scan superseded rows. Add `WHERE superseded_at IS NULL`.
- No load test on backfill — estimate row count and projected runtime.

## Architecture / data concerns
- Endorsement effective-dating logic lives partly in the service and partly in the DB — pick one source. Recommend service-side with DB-level invariants only.
- Downstream `billing-service` is not informed of new endorsement events. Add an outbox event (`platform-integration-pack/messaging-and-eventing`).

## Technical debt introduced
- Two write paths (old + new) — must be removed in phase 3 within 4 weeks; track in tech-debt board with explicit removal date.

## Refactoring plan
1. Extract effective-dating to a single `EndorsementService` (testable, replaces in-DB triggers).
2. Add outbox publisher in same transaction.
3. Remove old write path after canary 100 % + 7 days.

## Priority order
1. Critical issue #1 (rollback drill) — required for production-critical merge.
2. Critical issue #2 (backfill idempotency) — required.
3. Critical issue #3 (PII redaction) — required, regulated.
4. Critical issue #4 (canary abort gate) — required.
5. Medium issues — within same PR or follow-up within sprint.
6. Refactoring plan — sprint+1.

