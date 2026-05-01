# Example: CE7 -> Coding Handoff — Idempotent Payment Capture

This is the **CE7-side** of the handoff demonstrated in `coding-assistant-agent/examples/expert-payment-idempotency.md`. Together they show one full cycle.

## Scenario

> "We need an idempotent payment-capture endpoint. Multi-tenant. Postgres. Spring Boot 3. Goes live next sprint."

## CE7 Triage

1. **Primary expert role** — Data architect (idempotency table) + integration lead (PSP + outbox).
2. **Supporting lenses** — security (multi-tenant, PCI scope), observability (SLO + runbook), release (rollout + flag).
3. **Task type** — architecture/analysis (decision); implementation -> Coding.
4. **Risk class** — production-critical (money path).
5. **Regulatory sensitivity** — money + audit.
6. **Missing constraints** — apply Clarify-First.

## Clarify-First Pass

| Lens | Asked? | Answer (assumed if not provided) |
|---|---|---|
| Data lifecycle | YES — confirm 24h dedup window acceptable for FX correction workflow? | Assume 24h pending answer |
| Regulator / compliance | NO — already in PCI scope per existing system |
| SLO / capacity | YES — what is the target p99? | 300ms (set by product) |
| Tenant model | NO — pooled-DB with `tenant_id` discriminator (existing) |
| Rollout window | YES — 1%->10%->50%->100% over 5d acceptable? | Yes |
| On-call ownership | NO — payments-team owns existing capture flow |

3 clarifying questions, 1 round, all resolved.

## Decision (compressed)

**Use idempotency-table pattern with `(tenant_id, idempotency_key)` unique constraint.** Reject:

- *Idempotency in URL path* — leaks key in access logs.
- *Skip dedup for replay safety* — PSP charges twice on retry.
- *PSP-side idempotency only* — PSP timeout produces unknown state on our side.

Production Bar rows touched:
- `data-database-analytics-pack/data-modeling`: idempotency table is system of record for dedup; 24h retention with cleanup job; audit row in `payments_audit` per capture.
- `platform-integration-pack/messaging-and-eventing`: outbox-based `payment.captured` event for downstream (deferred to follow-up ADR — call out as residual risk).
- `security-access-pack/authn-authz-and-secrets`: `tenant_id` predicate on every read/write; PSP credentials via vault, 90d rotation.
- `observability-release-pack/devops-and-release`: flag + SLO gate per rollout step; rollback = flip flag.

## Self-Critique Pass

1. **Reversibility** — yes; flag flip + additive table.
2. **Rejected alternatives** — named (3 above).
3. **Open questions / owner** — 24h dedup window confirmation; outbox follow-up ADR; reconciliation cadence (open).

## Implementation Input Package (handed to Coding)

```yaml
adr_id: ADR-2026-04-payment-idempotency
title: Idempotent payment capture endpoint
risk_class: production-critical
regulatory: money,audit
contract:
  format: openapi
  snippet: |
    POST /v1/payments/capture
    headers: { Idempotency-Key: uuid }
    body: { amount, currency, customer_id }
    responses: { 200: PaymentCaptured, 409: ConflictDifferentBody }
idempotency:
  key_shape: "(tenant_id, idempotency_key)"
  storage: "payments_idempotency table, 24h dedup window"
  retry_semantics: "same key + same body -> 200 cached; same key + different body -> 409"
slo:
  latency_p99_ms: 300
  availability_pct: 99.9
  error_budget_pct: 0.1
data_lifecycle:
  source_of_truth: "payments table (Postgres)"
  history: "payments_audit (append-only, 7y retention)"
  derived_state: "balances projection (eventual, lag SLO < 30s) - DEFERRED to follow-up ADR"
security:
  authz: "resource-level: payment.tenant_id == caller.tenant_id"
  pii: "customer_id is internal id; no PAN/PII in logs"
  secrets: "PSP credentials via vault, rotated 90d"
rollout:
  feature_flag: "payments.idempotent_v2"
  steps: ["1%", "10%", "50%", "100%"]
  duration_days: 5
  slo_gate: "abort if p99 > 350ms or error_rate > 0.5% over 30m"
  rollback: "flip flag; expand-contract migration safe to leave forward"
runbook_stub:
  log_fields: ["correlation_id", "idempotency_key", "tenant_id", "psp_request_id"]
  metric_to_watch: "payments_capture_total{result=}, payments_capture_duration_seconds"
  dashboard: "grafana://payments/capture-v2"
  replay_command: "psql -c 'select * from payments_outbox where status=failed and created_at > now()-1h'"
on_call_owner: "payments-team (PagerDuty: payments-primary)"
rejected_alternatives:
  - "Idempotency key in URL path: rejected - leaks key in access logs"
  - "Skip dedup for replay safety: rejected - PSP charges twice on retry"
  - "PSP-side idempotency only: rejected - PSP timeout produces unknown state on our side"
open_questions:
  - "Confirm 24h dedup window is acceptable for FX correction workflow"
  - "Reconciliation cadence (hourly vs daily)?"
```

## Hand-off

CE7 stops here. The package goes to `coding-assistant-agent` (per `HANDOFF-PROTOCOL.md`). CE7 re-engages only if Coding's Self-Review Block surfaces an architecture/governance question (HANDOFF-PROTOCOL Section 5).

See `coding-assistant-agent/examples/expert-payment-idempotency.md` for the implementation side of the same example.
