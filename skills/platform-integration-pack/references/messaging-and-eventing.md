---
name: messaging-and-eventing
description: 'Designs production messaging and event-driven systems with ordering, idempotency, retries, dead-letter handling, replay, contracts, and consumer operations.'
---

# Messaging and Eventing

## Description

Designs production messaging and event-driven systems with ordering, idempotency, retries, dead-letter handling, replay, contracts, and consumer operations.

## Purpose

- Choose queues, topics, pub/sub, event streams, and asynchronous integration patterns based on workload and failure behavior.
- Make event-driven designs reliable enough for enterprise workflows, banking transactions, insurance claims, billing, notifications, and integration pipelines.
- Prevent hidden data loss, duplicate side effects, poison-message loops, and unobservable consumer failures.

## When to Use

- Designing Kafka-style streams, RabbitMQ-style brokers, SQS-style queues, pub/sub systems, outbox/inbox patterns, or event-driven integrations.
- A workflow needs buffering, fan-out, decoupling, long-running processing, partner integration, or resilience to dependency outages.
- Existing consumers have lag, duplicates, reprocessing failures, missing events, dead-letter growth, or unclear event ownership.

## Responsibilities

- Define producer ownership, event source of truth, event schema, topic or queue strategy, delivery guarantees, and consumer ownership.
- Specify ordering scope, partition key, deduplication, idempotency, retry policy, backoff, dead-letter handling, and replay procedure.
- Design event contract versioning, compatibility, retention, compaction, correlation IDs, and audit traceability.
- Make asynchronous failure modes visible and repairable by operators.

## Decision Principles

- Use messaging to decouple time, ownership, fan-out, or availability; do not use it to avoid modeling consistency.
- Prefer commands for directed work and events for facts that already happened.
- Require idempotent consumers for at-least-once delivery; assume duplicates will happen.
- Define ordering per aggregate or partition where possible; global ordering is expensive and rarely justified.
- Keep event contracts stable and additive; breaking changes require versioning and consumer migration.

## Expected Output Style

- State the recommended messaging pattern and why synchronous communication is insufficient.
- Include producer, consumer, topic/queue, schema, ordering, retry, DLQ, replay, and observability decisions.
- Separate business event semantics from broker mechanics.
- Identify failure modes and operator repair paths.
- Call out consistency trade-offs and user-visible effects.

## Architecture / Design Guidance

Use queues for work distribution, topics for fan-out, streams for ordered replayable event logs, and pub/sub for decoupled notifications. For transactional systems, use the outbox pattern when publishing events must be atomic with database state. Use an inbox or processed-message table when consumers must prevent duplicate side effects.

A complete event design defines topic naming, event ownership, schema ownership, partition key, retention, compaction, consumer groups, replay rules, DLQ routing, poison-message handling, correlation IDs, and audit requirements. In regulated domains, every event that changes money, policy, claim, customer communication, or compliance state must be traceable to the initiating actor and business transaction.

## Implementation Guidance

- Publish immutable facts with event IDs, aggregate IDs, schema version, event time, producer, correlation ID, causation ID, and tenant or business context where safe.
- Use transactional outbox for database-backed producers; do not publish to the broker before the database transaction commits.
- Make consumers idempotent using event ID, business key, or operation key; store processed markers where side effects matter.
- Use bounded retries with exponential backoff and jitter; route exhausted messages to a DLQ with reason metadata.
- Provide controlled replay tooling with filters, dry-run mode, rate limits, and audit logging.
- Monitor consumer lag, processing rate, error rate, retry rate, DLQ depth, and oldest unprocessed message age.

## Testing Expectations

- Test duplicate delivery, out-of-order delivery, retry exhaustion, poison messages, broker outage, consumer restart, and replay.
- Test event schema compatibility with old and new consumers.
- Test outbox publication after transaction commit and failure before publication.
- Test idempotency for externally visible side effects such as payments, emails, policy updates, or claim status changes.
- Test DLQ alerting and operator replay workflow.

## Security / Performance / Reliability Considerations

Security requires broker authentication, topic authorization, encrypted transport, safe payloads, and no secrets or unnecessary PII in events. Performance depends on partition keys, payload size, consumer concurrency, batching, broker quotas, retention, and hot-key avoidance. Reliability requires idempotency, bounded retries, DLQs, replay, lag monitoring, schema compatibility, and operational ownership.

## Review Checklist

- Producer, consumer, event owner, and source of truth are explicit.
- Topic or queue choice fits the workflow.
- Ordering scope and partition key are defined.
- Consumers are idempotent and deduplicate side effects.
- Retry, backoff, DLQ, replay, and poison-message rules are documented.
- Event schema versioning and compatibility are defined.
- Lag, error, retry, and DLQ metrics are monitored.
- Business-critical events are auditable and traceable.

## Anti-Patterns to Avoid

- Using messaging to hide unclear ownership or consistency requirements.
- Assuming exactly-once delivery removes the need for idempotent consumers.
- Putting secrets, tokens, or excessive PII in event payloads.
- Retrying forever without backoff or DLQ.
- Using one catch-all topic with unrelated event types and owners.
- Replaying production events without rate limits, audit, or downstream impact analysis.
- Treating CDC records as clean business events without transformation.

## Gotchas / Common Failure Modes

- Duplicate messages appear during producer retries, consumer restarts, broker failover, and replay.
- Ordering is usually scoped to a key or partition, not the whole system.
- DLQs become graveyards when ownership and replay rules are unclear.
- Consumer lag can hide a production outage while producers appear healthy.
- Schema changes break consumers when optional fields become required in practice.
- Replay can duplicate external side effects unless consumers are idempotent.
- Eventual consistency creates support issues when users expect immediate state changes.

## Worked Example: Transactional Outbox for Payment Events

**Problem**: A payment service must update the payment record in PostgreSQL AND publish a `payment.captured` event to Kafka. Publishing directly to Kafka inside the DB transaction is unsafe — if the transaction commits but Kafka publish fails, the event is lost; if Kafka publish succeeds but the transaction rolls back, a phantom event exists.

**Solution**: Transactional Outbox — write the event to an `outbox` table in the same DB transaction as the business state change. A separate relay process reads the outbox and publishes to Kafka.

**Schema**:

```sql
CREATE TABLE payment_outbox (
  id              BIGSERIAL    PRIMARY KEY,
  aggregate_id    UUID         NOT NULL,          -- payment ID
  aggregate_type  TEXT         NOT NULL DEFAULT 'Payment',
  event_type      TEXT         NOT NULL,          -- e.g., 'payment.captured'
  event_id        UUID         NOT NULL UNIQUE,   -- idempotency key for consumers
  payload         JSONB        NOT NULL,          -- event body (no secrets, minimal PII)
  correlation_id  UUID,                            -- trace to originating request
  tenant_id       UUID         NOT NULL,
  created_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
  published_at    TIMESTAMPTZ,                     -- NULL = not yet published
  retry_count     INT          NOT NULL DEFAULT 0,
  last_error      TEXT
);

CREATE INDEX ix_outbox_unpublished
  ON payment_outbox (created_at)
  WHERE published_at IS NULL;
```

**Write path** (single transaction):

```sql
BEGIN;
  -- 1. Update payment state
  UPDATE payments SET status = 'CAPTURED', captured_at = now(), version = version + 1
  WHERE id = :payment_id AND version = :expected_version;

  -- 2. Write outbox event in same transaction
  INSERT INTO payment_outbox (aggregate_id, event_type, event_id, payload, correlation_id, tenant_id)
  VALUES (:payment_id, 'payment.captured', gen_random_uuid(),
          jsonb_build_object('payment_id', :payment_id, 'amount', :amount, 'currency', :currency,
                             'captured_at', now(), 'psp_reference', :psp_ref),
          :correlation_id, :tenant_id);
COMMIT;
```

**Relay process** (separate worker, polling or CDC-based):

```
Every 500ms (or via CDC on outbox table):
  1. SELECT * FROM payment_outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 100 FOR UPDATE SKIP LOCKED;
  2. For each row:
     a. Publish to Kafka topic `payments.events` with key = aggregate_id (ordering per payment)
     b. On success: UPDATE payment_outbox SET published_at = now() WHERE id = :id;
     c. On failure: UPDATE payment_outbox SET retry_count = retry_count + 1, last_error = :error WHERE id = :id;
  3. Alert if any row has retry_count > 5 or created_at < now() - interval '5 minutes' AND published_at IS NULL.
```

**Consumer idempotency** (inbox pattern):

```sql
CREATE TABLE processed_events (
  event_id    UUID         PRIMARY KEY,
  processed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Consumer logic:
BEGIN;
  INSERT INTO processed_events (event_id) VALUES (:event_id) ON CONFLICT DO NOTHING;
  -- If inserted (not duplicate): execute side effect
  -- If conflict (duplicate): skip
COMMIT;
```

**Why not alternatives**:
- **Publish then commit**: Kafka gets the event but DB might rollback → phantom event.
- **Commit then publish**: DB commits but Kafka might fail → lost event.
- **Distributed transaction (2PC)**: Complex, slow, most brokers don't support XA.
- **CDC-only (Debezium on payments table)**: Captures DB changes but emits technical change events, not clean business events with the right schema and context.

**Operational controls**:
- Metric: `outbox_unpublished_age_seconds` (oldest unpublished row age) — alert if > 30s.
- Metric: `outbox_publish_total{result="success|failure"}` — alert on sustained failures.
- Metric: `outbox_retry_exhausted_total` — alert immediately; requires manual investigation.
- Cleanup: archive or delete published rows older than 7 days (configurable retention).
- Replay: re-publish specific events by resetting `published_at = NULL` with audit log entry.

