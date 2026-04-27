---
name: workflow-and-job-orchestration
description: 'Designs multi-step workflows and job orchestration with state transitions, approvals, compensation, resumability, visibility, and failure recovery.'
---

# Workflow and Job Orchestration

## Description

Designs multi-step workflows and job orchestration with state transitions, approvals, compensation, resumability, visibility, and failure recovery.

## Purpose

- Coordinate long-running business processes without losing state, duplicating actions, or hiding failures.
- Decide when orchestration, choreography, state machines, schedulers, or workflow engines are appropriate.
- Make approvals, compensation, manual intervention, audit, and recovery first-class in enterprise workflows.

## When to Use

- Designing claim processing, policy issuance, loan or account onboarding, payment workflows, document review, partner onboarding, or multi-step operational jobs.
- A process spans services, human approvals, external systems, timers, retries, documents, or compensation steps.
- Existing workflows get stuck, cannot resume, lack visibility, or require manual database edits to repair.

## Responsibilities

- Define workflow states, transitions, triggers, owners, timers, approval points, compensation, and terminal outcomes.
- Choose orchestration vs choreography based on visibility, coupling, ownership, and failure handling.
- Ensure every step is idempotent or protected by a workflow execution key.
- Provide operator views, audit trail, replay, retry, cancellation, and manual repair controls.

## Decision Principles

- Use orchestration when central visibility, human approvals, timers, and explicit recovery matter.
- Use choreography when services own independent reactions and global process visibility is less critical.
- Model workflow state explicitly; do not infer critical state from scattered logs or messages.
- Prefer compensation for completed side effects that cannot be rolled back transactionally.
- Require manual review states for regulated exceptions instead of forcing unsafe automation.

## Expected Output Style

- State workflow boundaries, state model, trigger model, and ownership.
- Include step list, transition rules, retry/compensation behavior, and operator actions.
- Identify which steps are synchronous, asynchronous, manual, timed, or external.
- Call out audit, compliance, and data consistency implications.
- Provide validation scenarios for happy path and stuck path.

## Architecture / Design Guidance

Workflow architecture needs a durable state store, transition rules, execution history, idempotency controls, timeout handling, and visibility. Workflow engines are justified when process complexity includes timers, retries, compensation, human tasks, or long-running state. A simple database-backed state machine is often enough for smaller bounded workflows.

Sagas should define each local transaction, emitted event or command, compensation action, retry behavior, and terminal state. In regulated systems, every state transition should be attributable to an actor, system, rule, or timer.

## Implementation Guidance

- Define allowed state transitions and reject invalid transitions at the domain layer.
- Store workflow instance ID, business key, current state, version, timestamps, actor, correlation ID, and transition history.
- Use optimistic concurrency or explicit locks to prevent double transitions.
- Make each step idempotent and record external side-effect references.
- Add timers for stuck states and escalation paths for manual intervention.
- Expose operator actions such as retry step, skip with approval, cancel, compensate, and mark for manual review.

## Testing Expectations

- Test happy path, each failure path, timeout, retry, compensation, cancellation, duplicate event, and concurrent transition.
- Test manual approval and rejection paths.
- Test workflow resume after process restart and dependency outage.
- Test audit trail completeness for regulated transitions.
- Test operator repair actions with authorization controls.

## Security / Performance / Reliability Considerations

Security requires authorization for workflow actions, audit of manual intervention, and protection of sensitive workflow metadata. Performance requires bounded polling, worker concurrency, and partitioning for large workflow volumes. Reliability requires durable state, idempotent steps, timeout escalation, compensation, and dashboards for stuck or aging workflows.

## Review Checklist

- Workflow boundaries and owner are clear.
- States and allowed transitions are explicit.
- Orchestration vs choreography choice is justified.
- Compensation and manual intervention are defined.
- Steps are idempotent and recoverable.
- Stuck states have timers and alerts.
- Audit trail covers automated and human actions.
- Operators can inspect and repair workflow instances safely.

## Anti-Patterns to Avoid

- Encoding workflow state only in comments, logs, or UI flags.
- Using choreography when operators need one authoritative workflow view.
- Using a heavy workflow engine for a simple two-step process.
- Retrying completed external side effects without idempotency.
- Allowing manual database updates to repair workflow state.
- Ignoring compensation until the first production incident.

## Gotchas / Common Failure Modes

- Human approval steps create long-lived state and permission complexity.
- Compensation is not rollback; it is new business behavior that must be tested.
- Duplicate messages can advance workflows twice without concurrency control.
- Workflow engines still require domain modeling and operational ownership.
- Stuck workflows become invisible unless age and state metrics are monitored.
- External systems may complete work after your timeout, requiring reconciliation.

