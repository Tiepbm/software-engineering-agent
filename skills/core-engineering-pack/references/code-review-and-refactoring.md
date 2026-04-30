---
name: code-review-and-refactoring
description: 'Reviews maintainability, clarity, coupling, cohesion, hidden complexity, technical debt, regression risk, safe refactoring order, and issue prioritization.'
---
# Code Review and Refactoring
## Description
Reviews maintainability, clarity, coupling, cohesion, hidden complexity, technical debt, regression risk, safe refactoring order, and issue prioritization.
## Purpose
- Improve code quality while protecting delivery, behavior, and production stability.
- Distinguish critical design and correctness issues from style-only comments.
- Plan refactoring in safe increments with tests and rollback awareness.
- Surface hidden platform risk in code changes: unsafe retries, stale caches, unbounded queries, missing authorization, weak telemetry, brittle jobs, and data-copy drift.
## When to Use
- Reviewing pull requests, legacy modules, complex changes, or refactoring proposals.
- Code is hard to understand, test, extend, or operate.
- The team needs a priority order for technical debt.
- A change touches persistence, APIs, events, caches, background jobs, search, object storage, gateway policies, secrets, observability, or regulated workflows.
## Responsibilities
- Assess correctness, readability, coupling, cohesion, abstraction quality, error handling, data access, security, performance, and test coverage.
- Identify hidden complexity, duplicated business rules, leaky boundaries, and risky dependencies.
- Recommend refactoring sequence that reduces risk instead of rewriting everything.
- Separate blocking issues from suggestions.
- Identify when concerns belong to specialized skills such as `security-review`, `api-design`, `database-architecture`, `messaging-and-eventing`, `caching-and-distributed-state`, `logging-metrics-and-tracing`, `resilience-and-fault-tolerance`, or `testing-strategy` instead of being solved ad hoc in local code.
## Decision Principles
- Block changes for correctness, security, data loss, compatibility, or severe operability risk.
- Prefer simple explicit code over clever abstractions.
- Refactor behind tests and stable interfaces.
- Do not request style churn that obscures review of behavior.
- Review failure behavior as carefully as happy-path structure: timeouts, cancellation, retry limits, idempotency, compensation, and operator visibility.
- In regulated systems, prioritize data correctness, audit trail continuity, resource authorization, and rollback/roll-forward safety over cosmetic cleanup.

Use severity consistently:

| Severity | Meaning | Reviewer action |
|---|---|---|
| Blocker | Can cause data loss, auth bypass, financial/policy/claim/billing corruption, outage, irreversible migration, or broken public contract | Must fix before merge |
| High | Likely production defect, severe operability gap, unbounded cost/performance risk, missing rollback, or unsafe side effect | Fix before release; usually before merge |
| Medium | Maintainability, testability, coupling, or localized correctness issue with bounded blast radius | Fix in this PR or create tracked follow-up |
| Low | Readability, naming, small duplication, local simplification | Suggest; do not block unless pattern repeats |
| Nit | Formatting or preference with no behavior/risk impact | Optional; avoid noise during risky reviews |

Escalate one level when the change touches regulated data, tenant isolation, privileged operations, migration/backfill, external callbacks, payments, claims, policies, billing, or customer communications.
## Expected Output Style
- Start with the decision or finding, then provide the reasoning needed to trust it.
- Separate immediate actions from longer-term improvements.
- State assumptions, constraints, trade-offs, risks, and missing information explicitly.
- Use concrete examples, acceptance criteria, contracts, schemas, queries, or checklists when they reduce ambiguity.
- Avoid generic advice unless it is followed by an enforceable rule or verification step.
## Architecture / Design Guidance
Good design has cohesive modules, clear dependency direction, domain rules outside transport/controllers, explicit data boundaries, and observable failure behavior. Refactoring should preserve public contracts unless compatibility changes are deliberate and planned.

Review code at three levels:

1. **Local correctness**: simple logic, clear names, edge cases, validation, nullability, concurrency, and error handling.
2. **Boundary correctness**: API contracts, DTOs, persistence queries, transactions, event publication, cache access, file handling, search indexing, and external calls.
3. **Operational correctness**: logs, metrics, traces, alerts, retries, timeouts, backpressure, migrations, rollback/roll-forward, and support repair paths.

Refactoring should reduce one kind of risk at a time. If a module mixes domain rules, persistence, HTTP concerns, message publishing, cache invalidation, and telemetry, extract boundaries in an order that preserves behavior and adds tests before moving side effects.

Review priorities by change type:

| Change type | Review first | Specialist skill to involve |
|---|---|---|
| API/controller/route | Contract compatibility, validation, idempotency, resource authorization, error shape | `api-design`, `authn-authz-and-secrets` |
| Persistence/query | Transaction boundary, migration safety, query plan, locks, N+1, data correction path | `data-modeling`, `sql-and-query-optimization`, `database-reliability-and-operations` |
| Event/queue/worker | Ordering key, idempotency, retry/DLQ/replay, poison handling, lag metrics | `messaging-and-eventing`, `background-jobs-and-batch-processing` |
| Cache/session/lock | Source of truth, key scope, tenant isolation, TTL, invalidation, stampede behavior | `caching-and-distributed-state` |
| UI/mobile screen | Authorization UX vs backend enforcement, loading/error states, accessibility, telemetry, duplicate submit | relevant stack skill, `security-review` |
| Release/config/infra | Rollback, feature flag, secret exposure, environment drift, SLO gate | `devops-and-release`, `monitoring-alerting-and-slos` |
| Security-sensitive code | Trust boundary, authn/authz, secret handling, sensitive telemetry, abuse case | `security-review`, `authn-authz-and-secrets` |
## Implementation Guidance
Use characterization tests before changing legacy behavior. Extract pure functions, isolate side effects, introduce DTO boundaries, remove duplication around business rules, and narrow public APIs. Refactor one axis at a time: structure, naming, behavior, or performance.

Safe refactoring sequence:

1. **Freeze behavior**: characterize current behavior, public contracts, events, queries, logs, and dashboards before moving code.
2. **Add seams**: introduce interfaces/adapters or pure functions without changing behavior.
3. **Move one responsibility**: extract validation, mapping, query, side effect, or domain rule separately.
4. **Verify compatibility**: run tests, compare contract snapshots, inspect query plans, check emitted events/log fields.
5. **Remove old path** only after both paths are observed or feature-flagged safely.
6. **Document residual risk**: known debt, follow-up owner, rollback or roll-forward path.

During review, require explicit fixes for:

- business logic embedded in controllers, UI components, gateway scripts, schedulers, or message handlers;
- database calls hidden inside loops, serializers, or template rendering;
- message publishing inside transactions without outbox/idempotency design;
- cache writes without invalidation, tenant keying, or stale-read rules;
- external calls without timeout, cancellation, retry classification, and safe error mapping;
- logs or errors that leak tokens, PII, claim/policy/account/payment data, or signed URLs;
- background jobs without checkpointing, duplicate prevention, progress metrics, or stop/resume behavior.
- public DTO/event/schema changes without compatibility window, versioning, or consumer migration plan;
- support/admin scripts that bypass authorization, validation, audit, or reconciliation rules used by the main app.
## Testing Expectations
- Run existing tests before and after refactoring.
- Add tests around current behavior before risky changes.
- Use mutation or edge-case tests for critical rules where useful.
- Validate performance and query behavior after data-access refactors.
- Add or update contract tests when public APIs, event payloads, webhooks, or partner adapters change.
- Add idempotency, retry, authorization, migration, cache invalidation, and observability tests when refactoring side-effecting workflows.
- For broad refactors, add a review harness: golden master outputs, snapshot contracts, query-count assertions, event payload snapshots, or approval tests where appropriate.
- Test both old and new paths during feature-flagged refactors, including flag rollback and mixed-version deployment behavior.
## Security / Performance / Reliability Considerations
Security review must catch authorization bypasses, unsafe input, secrets, sensitive logs, cross-tenant access, unsafe file handling, stale permission caches, and privileged support paths. Performance review must catch N+1, unbounded loops, allocations, large payloads, inefficient queries, unbounded fan-out, cache stampedes, and retry storms. Reliability review must catch swallowed exceptions, missing cancellation, unsafe retries, non-idempotent operations, hidden background failures, and recovery paths that require manual database edits.

Platform risk checks are mandatory when a refactor changes where side effects happen. Moving code across boundaries can silently change transaction duration, retry scope, cancellation behavior, auth context propagation, cache invalidation timing, event ordering, connection usage, telemetry fields, or release rollback safety.
## Review Checklist
- Code intent is clear.
- Business logic is not duplicated.
- Dependencies point inward or toward stable abstractions.
- Error handling is explicit.
- Tests protect risky behavior.
- Data access is bounded.
- Refactoring plan is incremental.
- Severity is assigned consistently; blockers and high-risk issues are not hidden among nits.
- Review priority matches the change type; specialist skills are involved when platform or security risk appears.
- Old/new behavior compatibility is verified when public contracts, storage, events, jobs, or release behavior change.
- Authorization, data consistency, idempotency, and audit behavior are preserved across refactoring.
- Messaging, caching, search, object storage, gateway, and job side effects are explicit and observable when present.
- Public contracts and downstream consumers are protected by compatibility checks or migration plans.
## Anti-Patterns to Avoid
- Rewriting working systems without tests.
- Commenting on formatting while missing data loss.
- Introducing abstractions for one implementation.
- Moving code without reducing coupling.
- Mixing behavior changes with broad cleanup.
- Treating platform concerns as incidental library calls instead of owned design decisions.
- Hiding failures by catching broad exceptions, logging them, and continuing as if the workflow succeeded.
- Refactoring code that emits events, updates caches, writes files, or changes schemas without a compatibility and rollback plan.
- Blocking on subjective style while accepting untested side effects, missing authorization, or broken rollback.
- Splitting one messy module into many files without reducing coupling, clarifying ownership, or adding tests.
## Gotchas / Common Failure Modes
- Large refactors hide regressions in review.
- Dead code may be used by reflection or configuration.
- Renaming public contracts can break clients.
- Performance can regress from cleaner but chatty code.
- Technical debt priority should follow risk and change frequency.
- Moving authorization or validation code can protect the main request path but miss background jobs, message consumers, search exports, or admin tools.
- Cleaner abstractions can accidentally change transaction boundaries, retry behavior, lazy loading, or event ordering.
- Removing “duplicate” fields or logs can break audit, reconciliation, support tooling, dashboards, or downstream reports.
- A refactor can pass unit tests while breaking observability because metric names, log fields, trace attributes, or alert dimensions changed.
- Mixed-version deployments expose compatibility bugs that local refactors miss: old producer/new consumer, new API/old mobile client, old job/new schema.

## Terse Review Format

Use this format for quick reviews, large PRs (> 20 findings), or when user requests "terse review" / "quick review". One line per finding.

**Format:** `<file>:L<line>: <severity> <category>: <problem>. <fix>.`

**Severity:**
- `🔴 blocker` — data loss, auth bypass, financial corruption, broken public contract
- `🟠 high` — likely production defect, missing rollback, unsafe side effect
- `🟡 medium` — maintainability, testability, bounded correctness issue
- `🔵 low` — readability, naming, small duplication
- `⚪ nit` — formatting, preference, no behavior impact

**Category:** `bug` | `security` | `auth` | `data` | `perf` | `test` | `migration` | `ops` | `style`

**Example terse review:**

```
PaymentService.java:L42:  🔴 bug: user null after .findById(). Guard before .email access.
PaymentService.java:L67:  🟠 security: idempotency key from client not tenant-scoped. Add (tenant_id, key) composite.
PaymentService.java:L88:  🟠 data: outbox INSERT outside @Transactional boundary. Move into same TX as payment UPDATE.
PaymentService.java:L120: 🟡 perf: N+1 query in loop. Use @EntityGraph or batch IN clause.
PaymentService.java:L155: 🟡 ops: no correlation_id in log. Add MDC.put("correlation_id", ctx.correlationId()).
PaymentService.java:L180: 🔵 test: no test for duplicate callback. Add: same psp_reference twice → no state change.
PaymentService.java:L200: ⚪ nit: unused import. Remove.

Summary: 1 blocker, 2 high, 2 medium, 1 low, 1 nit. Block on L42 + L67 + L88.
```

**Rules:**
- Always include `Summary` line at the end with counts per severity.
- Always state which findings block merge.
- Use Standard (prose) format for: security findings with exploit path, architecture disagreements, onboarding contexts where author needs the "why".
- Escalate severity one level when change touches regulated data, tenant isolation, money, or customer communications.
