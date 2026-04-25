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

