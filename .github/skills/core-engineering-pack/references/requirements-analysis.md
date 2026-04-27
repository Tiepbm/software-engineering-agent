---
name: requirements-analysis
description: 'Clarifies ambiguous business and technical requests into measurable requirements, acceptance criteria, constraints, risks, and validation-ready delivery scope.'
---
# Requirements Analysis
## Description
Clarifies ambiguous business and technical requests into measurable requirements, acceptance criteria, constraints, risks, and validation-ready delivery scope.
## Purpose
- Turn vague requests into testable scope with actors, workflows, business rules, constraints, and measurable outcomes.
- Separate business requirements from proposed technical solutions so implementation choices remain open until trade-offs are understood.
- Expose missing assumptions early enough to prevent rework, invalid acceptance criteria, and hidden delivery risk.
## When to Use
- A request contains words like improve, support, automate, integrate, migrate, optimize, dashboard, workflow, or make it easier without measurable success criteria.
- Stakeholders disagree on behavior, priority, workflow ownership, compliance needs, or acceptable trade-offs.
- The team needs acceptance criteria, edge cases, story slicing, or business-rule clarification before design or coding.
## Responsibilities
- Identify actors, triggers, happy paths, alternate paths, failure paths, permissions, and decision points.
- Convert business rules into explicit examples and acceptance criteria that QA and developers can verify.
- Call out missing non-functional requirements such as latency, retention, auditability, accessibility, compliance, and reporting.
- Challenge technical prescriptions that are disguised as requirements, such as use Kafka or add MongoDB, until the workload need is clear.
## Decision Principles
- Require every requirement to answer who benefits, what changes, why it matters, and how success is measured.
- Prefer examples over abstract wording: given a policy is expired, when renewal is attempted, then the system blocks payment and explains why.
- Treat edge cases as scope, not polish, when they affect money, compliance, security, data correctness, or user trust.
- Defer implementation choices until constraints such as volume, freshness, consistency, integration ownership, and operational support are known.
- A requirement is not ready until it names the actor, trigger, business rule, exception behavior, data touched, owner, measurable outcome, and validation evidence.
- Classify ambiguity explicitly: terminology ambiguity, policy ambiguity, data ambiguity, ownership ambiguity, priority ambiguity, compliance ambiguity, or technical-prescription ambiguity.
- Resolve high-risk ambiguity before estimation when it changes authorization, money movement, policy/claim/billing state, audit evidence, migration scope, integration ownership, or operational support.
## Expected Output Style
- Start with the decision or finding, then provide the reasoning needed to trust it.
- Separate immediate actions from longer-term improvements.
- State assumptions, constraints, trade-offs, risks, and missing information explicitly.
- Use concrete examples, acceptance criteria, contracts, schemas, queries, or checklists when they reduce ambiguity.
- Avoid generic advice unless it is followed by an enforceable rule or verification step.
## Architecture / Design Guidance
Model the business process before modeling software. Identify bounded workflows, source systems, consuming systems, ownership boundaries, and data lifecycle. If requirements imply new data capture, define retention, audit, correction, reporting, and deletion expectations before choosing storage or APIs.

Separate **constraints** (non-negotiable: regulatory, SLA, data-residency, existing integration contracts) from **preferences** (stakeholder-selected technology, implementation opinions). Constraints drive architecture; preferences are negotiable. A requirement saying "use Kafka" is a preference until the workload need for async decoupling, fan-out, ordering, replay, or resilience is confirmed.

For domain events and state changes, identify: who triggers, what state is affected, what downstream systems must react, what audit evidence is required, and what happens when the trigger fails halfway. These questions surface integration contracts before any API or schema is designed.

### NFR Capture Template
For every requirement that touches production behavior, capture each NFR explicitly with a number, not adjectives. Missing rows = open question, not "default":

| Category | Question to answer | Example target |
|---|---|---|
| Latency | P50 / P95 / P99 for each user-visible operation | P95 ≤ 400 ms for policy lookup |
| Throughput | Sustained req/s, peak req/s, burst window | 200 rps sustained, 800 rps for 60 s |
| Concurrency | Concurrent users, concurrent in-flight workflows, lock contention windows | 5,000 concurrent agents at 09:00 open |
| Volume | Records today, growth/year, retention horizon | 12 M policies, +18 %/yr, retain 10 yr |
| Availability | Uptime target, allowed degraded modes, maintenance window | 99.9 % core, 99.5 % reporting |
| Recovery | RPO / RTO per data class, restore drill cadence | RPO 5 min, RTO 30 min for payments |
| Consistency | Strong / read-your-writes / eventual per workflow | Strong for balance, eventual for search |
| Freshness | Acceptable staleness for caches, replicas, indexes, marts | Search ≤ 30 s lag, BI ≤ 1 h |
| Auditability | Who/what/when/why must be reconstructable, retention, immutability | 7-yr immutable for claim decisions |
| Compliance | Data residency, regulatory regimes, lawful basis, masking | EU residency, GDPR, PCI scope minimised |
| Accessibility | WCAG level, assistive-tech support, language coverage | WCAG 2.2 AA, en + vi, screen reader |
| Observability | SLIs, alerting threshold, business-event visibility | Burn-rate alert at 2 %/h on payment SLO |
| Cost | Unit economics ceiling, peak-cost guardrail | ≤ $0.002 per quote computed |

### Scenario Template

Use scenarios for any workflow with business rules, permissions, regulated data, or failure paths:

| Field | Required content |
|---|---|
| Context | Product area, actor, tenant/customer segment, source system, consuming system |
| Given | Starting state, permissions, data quality assumptions, feature flags |
| When | Trigger, user action, job/event/callback, external dependency behavior |
| Then | Expected state change, response, notification, audit entry, event/report emitted |
| Failure path | Validation failure, duplicate submission, timeout, authorization denial, downstream outage |
| Evidence | Test, metric, log/event, report, audit record, UAT sign-off artifact |

Scenario sets must include at least one happy path, one permission failure, one data-quality failure, one duplicate/retry case, and one operational failure for business-critical flows.
## Implementation Guidance

Produce user stories or requirement slices small enough to build and verify in one sprint. Each slice must include: actor, trigger, happy path, at least one failure path, permission rules, data inputs/outputs, and definition of done. Include field-level validation rules, error states, and migration needs when the slice touches existing data.

Slice strategies for large requirements:
- **Vertical slice**: UI/API/state/test/telemetry for one end-to-end path before expanding variants.
- **CRUD slice**: one entity lifecycle per slice (create → read → update → delete), not the whole entity at once.
- **Role slice**: one actor's view of a workflow before adding a second actor.
- **Workflow-state slice**: one state transition at a time (draft → submitted, submitted → approved, approved → paid).
- **Migration/backfill slice**: schema/data capture first, compatibility period second, backfill/reconciliation third, removal last.
- **Risk-first slice**: prove the hardest dependency, authorization rule, data migration, or SLA before filling in low-risk screens.
- **Error-path first** for regulated flows: implement the rejection / guard / audit path before the happy path when the failure case affects money, compliance, or security.
- **Notification/reporting last**: decouple downstream consumers (emails, reports, audit exports) from the core state change.

The slice is too large if it changes more than one bounded workflow, requires multiple unrelated approvals, cannot be demonstrated with one scenario set, or cannot be rolled back without data correction.

Mark open questions with: *impact if unresolved*, *safe default assumption*, and *owner*. Never leave a TODO without these three fields — unowned ambiguity becomes a defect.
## Testing Expectations

- Each acceptance criterion must be testable by a human or automated test without interpreting intent.
- Include positive, negative, boundary, permission, concurrency, and data-quality examples for critical flows.
- Define business validation evidence: metric, report, audit entry, event, or observable user outcome.
- For regulated flows, define the **UAT sign-off criteria** explicitly: who signs off, what data set, what environment, and what audit trail proves the test occurred.
- Acceptance criteria written as scenarios (given/when/then) are directly executable with Cucumber, SpecFlow, Behave, or equivalent; prefer this format for business-critical and compliance-sensitive flows to close the gap between specification and test suite.
## Security / Performance / Reliability Considerations
Security-sensitive requirements must define actors, permissions, sensitive data handling, audit events, and abuse cases. Performance requirements must include measurable targets and expected load. Reliability requirements must define acceptable failure behavior, recovery expectations, and manual workaround tolerance.
## Review Checklist
- Actors and workflows are explicit.
- Business rules include examples and edge cases.
- Success criteria are measurable.
- Assumptions are marked and owned.
- Technical choices are not mistaken for business needs.
- NFRs that affect architecture are captured.
- Acceptance criteria can be tested without guesswork.
- Ambiguity is classified and either resolved, explicitly assumed, or assigned to an owner with impact.
- Each high-risk scenario includes permission, duplicate/retry, data-quality, and operational-failure behavior.
- Story slices are vertical, demonstrable, and reversible without hidden data repair.
## Anti-Patterns to Avoid
- Accepting vague goals such as make it scalable or user friendly without metrics.
- Letting a stakeholder-selected technology define the problem.
- Writing acceptance criteria that restate the implementation task.
- Ignoring unhappy paths because they are uncommon.
- Treating reporting, audit, migration, and support needs as later work.
- Treating stakeholder consensus as requirements quality when scenarios, data ownership, and evidence are still missing.
- Estimating a story before resolving ambiguity that could change architecture, authorization, migration, or operational ownership.
## Gotchas / Common Failure Modes
- Different actors often use the same word for different workflow states.
- Missing data correction rules create production support load.
- A feature can satisfy the UI request while failing the business process.
- Compliance and audit needs frequently appear after design unless asked explicitly.
- Edge cases around time zones, retries, and duplicate submissions often become defects.
- “Same as existing flow” often hides a legacy exception, manual workaround, or undocumented support process.
- A technically small requirement can be delivery-large when it changes audit evidence, customer communication, downstream reports, or migration/reconciliation scope.
