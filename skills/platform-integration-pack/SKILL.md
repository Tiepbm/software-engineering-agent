---
name: platform-integration-pack
description: 'Use when designing messaging/events, API gateways, BFFs, partner integrations, rate limits, long-running workflows (sagas), background jobs, batch processing, retries, DLQs, or repair paths.'
---
# Platform Integration Pack

## When to Use
- Queues, topics, pub/sub, outbox/inbox, ordering scope, idempotent consumers, retries, DLQs, replay, poison messages.
- API gateway, BFF, partner integration, protocol transformation, auth propagation, contract isolation.
- Rate limit / quota / throttling / backpressure / fair degradation.
- Long-running workflows, sagas, approvals, compensation, resumability.
- Scheduled / chunked / checkpointed jobs, batch processing, backfills, reconciliation jobs.

## When NOT to Use
- Outbox TABLE design (DDL) → `data-database-analytics-pack` → `data-modeling`.
- Circuit breaker / timeout / fallback PATTERN itself → `resilience-performance-pack`.
- Telemetry/alerting on lag/DLQ → `observability-release-pack`.
- Identity-based throttling policy → `security-access-pack`.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `messaging-and-eventing` | Use when designing event contracts, outbox/inbox, ordering scope, idempotent consumers, DLQ, replay, or operator repair for queues/topics. |
| `api-gateway-and-service-integration` | Use when defining gateway/BFF policy, partner contract isolation, protocol transformation, error mapping, or auth propagation across boundaries. |
| `rate-limiting-and-traffic-control` | Use when designing per-tenant/per-key rate limits, quotas, backpressure, fair degradation, or graceful rejection. |
| `workflow-and-job-orchestration` | Use when designing LONG-RUNNING workflows, sagas, approval steps, compensation, resumable state machines. |
| `background-jobs-and-batch-processing` | Use when designing RECURRING/SCHEDULED jobs, chunked batch processing, checkpointed backfills, idempotent reconciliation. |

## Cross-Pack Handoffs
- → `data-database-analytics-pack` for outbox table DDL, CDC source, and reconciliation queries.
- → `resilience-performance-pack` for retry/backoff/circuit pattern when wiring producers/consumers.
- → `observability-release-pack` for DLQ alerts, lag SLOs, and consumer-restart runbooks.
- → `security-access-pack` for partner-callback auth and privileged operator repair actions.

