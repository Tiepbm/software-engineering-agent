---
name: background-jobs-and-batch-processing
description: 'Designs reliable background jobs and batch processing with scheduling, chunking, checkpointing, retries, idempotency, duplicate prevention, and operational visibility.'
---

# Background Jobs and Batch Processing

## Description

Designs reliable background jobs and batch processing with scheduling, chunking, checkpointing, retries, idempotency, duplicate prevention, and operational visibility.

## Purpose

- Make scheduled, asynchronous, and bulk processing safe, resumable, observable, and recoverable.
- Prevent duplicate side effects, missed runs, unbounded retries, silent failures, and unsafe backfills.
- Support enterprise workloads such as billing runs, reconciliations, claim processing, document processing, notifications, and data correction.

## When to Use

- Designing nightly jobs, workers, schedulers, reconciliation jobs, batch imports, exports, backfills, cleanup jobs, or report generation.
- Jobs fail silently, overlap, duplicate work, run too long, overload dependencies, or cannot resume after failure.
- A business workflow needs operational proof that all expected work completed.

## Responsibilities

- Define trigger, schedule, ownership, input set, chunking strategy, checkpointing, concurrency, retries, and completion criteria.
- Ensure jobs are idempotent or protected from duplicate execution.
- Design pause, resume, cancel, rerun, and backfill behavior.
- Provide visibility into progress, failures, lag, duration, and affected business records.

## Decision Principles

- Use chunking and checkpoints for large work; do not rely on one huge transaction or one long process.
- Make reruns safe before production; assume jobs will be restarted.
- Prevent overlapping runs unless explicitly designed for partitioned concurrency.
- Use bounded retries with classification of retryable and non-retryable errors.
- Prefer reconciliation jobs for correctness-critical systems where events or integrations can be missed.

## Expected Output Style

- State job purpose, trigger, input scope, owner, and completion definition.
- Include chunking, checkpointing, idempotency, retry, concurrency, and observability design.
- Identify downstream impact and throttling needs.
- Separate normal operation from backfill and repair operation.
- Include operator controls and runbook expectations.

## Architecture / Design Guidance

Batch architecture should separate scheduler, job definition, work discovery, chunk processing, checkpoint storage, retry state, and result reporting. For transaction-heavy systems, each chunk should have a clear business boundary and idempotency key. For reconciliation jobs, compare independently derived sources and produce actionable discrepancies rather than silently fixing data.

Long-running jobs should expose progress and support safe interruption. High-impact jobs need approval, dry-run, rate limits, and audit logging.

## Implementation Guidance

- Store job run ID, parameters, version, started time, completed time, status, checkpoint, processed count, failed count, and operator identity for manual runs.
- Use deterministic ordering for chunks so resume behavior is predictable.
- Use small transactions per chunk and commit progress only after side effects are safe.
- Add duplicate prevention with uniqueness constraints, idempotency records, or processed markers.
- Throttle calls to databases, search indexes, object stores, and partner APIs.
- Emit metrics for run status, duration, throughput, failures, retries, stuck chunks, and oldest pending item age.

## Testing Expectations

- Test successful run, partial failure, process crash, retry, resume, duplicate trigger, overlapping schedule, and cancellation.
- Test idempotency by running the same job with the same input twice.
- Test chunk boundaries, dirty data, empty input, maximum input, and slow downstream dependencies.
- Test backfills separately from normal incremental runs.
- Test alerting for missed schedule, long duration, repeated failure, and partial completion.

## Security / Performance / Reliability Considerations

Security requires least-privilege job credentials, audited manual execution, safe exports, and no sensitive data in logs. Performance requires chunking, throttling, bounded concurrency, and dependency-aware scheduling. Reliability requires checkpointing, idempotency, resumability, alerting, and reconciliation for critical workflows.

## Review Checklist

- Trigger, owner, input scope, and completion criteria are explicit.
- Job can resume after failure without duplicating side effects.
- Chunking and concurrency are bounded.
- Retries are classified and limited.
- Overlapping runs are prevented or safe.
- Progress, failures, and lag are observable.
- Backfill and repair procedures are separate from normal operation.
- Audit exists for manual or high-impact runs.

## Anti-Patterns to Avoid

- One massive transaction for an entire batch.
- Jobs that only report success or failure at the end after hours of work.
- Retrying non-idempotent side effects blindly.
- Running backfills through production paths without throttling.
- Allowing overlapping scheduled runs by accident.
- Hiding failed records in logs instead of a queryable error store.

## Gotchas / Common Failure Modes

- Jobs often fail at scale because test data lacks dirty records and skew.
- Process restarts create duplicates unless checkpoints and idempotency are correct.
- A job can complete technically while missing business records due to bad input discovery.
- Backfills can overload source systems and downstream consumers.
- Clock changes and time zones can skip or duplicate scheduled windows.
- Operators need dry-run and progress views before trusting high-impact jobs.

