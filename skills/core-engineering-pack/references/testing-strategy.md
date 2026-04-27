---
name: testing-strategy
description: 'Designs risk-based testing across unit, integration, contract, end-to-end, test data, automation, architecture for testability, confidence, and fast feedback.'
---
# Testing Strategy
## Description
Designs risk-based testing across unit, integration, contract, end-to-end, test data, automation, architecture for testability, confidence, and fast feedback.
## Purpose
- Build a testing strategy that gives fast feedback and credible release confidence without turning the suite into a slow brittle gate.
- Match test types to risk: business rules, integration boundaries, contracts, data correctness, security, and user-critical workflows.
- Design systems so they can be tested deterministically.
- Cover platform failure modes such as duplicate messages, cache staleness, gateway retries, secret rotation, object scanning, search lag, queue backlog, and degraded dependencies before production.
## When to Use
- Planning quality for a feature, service, migration, API, frontend, mobile app, or release.
- The current suite is flaky, slow, shallow, over-reliant on E2E tests, or missing integration confidence.
- A production defect indicates coverage is aimed at lines rather than risks.
- A change touches regulated workflows, messaging, caching, background jobs, orchestration, API gateways, object storage, search indexes, rate limits, observability, or deployment/migration safety.
## Responsibilities
- Define the test pyramid for the context, not as dogma.
- Choose unit tests for pure logic, integration tests for real boundaries, contract tests for provider/consumer compatibility, and E2E tests for critical journeys.
- Specify test data strategy, environment strategy, automation ownership, and failure triage.
- Make acceptance criteria executable where practical.
- Map each production risk to the cheapest reliable test type and identify which risks require staging, fault injection, load tests, game days, or manual operational drills.
- Involve `messaging-and-eventing`, `caching-and-distributed-state`, `resilience-and-fault-tolerance`, `logging-metrics-and-tracing`, `monitoring-alerting-and-slos`, `security-review`, `database-reliability-and-operations`, and `devops-and-release` when the testing scope depends on those concerns.
## Decision Principles
- Prefer many fast deterministic tests and a small number of high-value end-to-end tests.
- Test contracts at service boundaries before relying on full-stack tests.
- Use production-like dependencies for critical integration behavior, but isolate tests enough to run reliably.
- Every flaky test is either fixed, quarantined with owner/date, or deleted.
- Test behavior and externally visible contracts before implementation details.
- Use real databases, brokers, caches, object stores, and identity flows for risks that mocks cannot represent accurately.
- For banking, insurance, and regulated systems, release confidence must include authorization, audit evidence, reconciliation, rollback/roll-forward, and support recovery tests.
## Expected Output Style
- Start with the decision or finding, then provide the reasoning needed to trust it.
- Separate immediate actions from longer-term improvements.
- State assumptions, constraints, trade-offs, risks, and missing information explicitly.
- Use concrete examples, acceptance criteria, contracts, schemas, queries, or checklists when they reduce ambiguity.
- Avoid generic advice unless it is followed by an enforceable rule or verification step.
## Architecture / Design Guidance
Architecture must expose seams for testing without weakening production design. Avoid static global state, hidden time dependencies, random IDs without injection, and direct external calls in domain logic. For data systems, test migrations, backfills, schema compatibility, and reconciliation.

Design the test strategy by risk category:

- **Business correctness**: unit and scenario tests for rules, workflow states, edge cases, and concurrency.
- **API and integration contracts**: provider/consumer contract tests, schema compatibility, error contracts, idempotency, and versioning.
- **Messaging and jobs**: duplicate delivery, out-of-order events, retries, DLQs, replay, stuck jobs, missed schedules, and resumable backfills.
- **Caching and search**: stale reads, invalidation, permission changes, reindexing, source-of-truth verification, and cache outage fallback.
- **Security**: resource authorization, same-role different-resource access, secrets, signed URLs, unsafe files, webhook signatures, and tenant isolation.
- **Observability and operations**: telemetry emission, alert routing, dashboard usefulness, runbook execution, and incident timeline reconstruction.
- **Release safety**: feature flags, expand-contract migrations, rollback or roll-forward, secret rotation, and platform compatibility windows.

### Test Type Decision Matrix

Use this matrix to select the cheapest reliable test type for each risk. Start from the top; move down only when the cheaper type cannot cover the risk.

| Test type | Strong fit | Avoid when | Typical cost |
|---|---|---|---|
| **Unit** (pure logic, no I/O) | Business rules, calculations, state machines, validators, mappers, domain invariants | Behavior depends on real DB, broker, cache, or network | Fast; seconds |
| **Scenario / BDD** (given-when-then) | Acceptance criteria, regulated workflows, multi-step business flows with edge cases | Only happy path exists; no business rules to verify | Fast; seconds |
| **Integration** (real DB, real broker, test containers) | Repository queries, migration correctness, transaction isolation, message delivery, cache TTL, search indexing | Pure logic with no I/O dependency | Medium; seconds to minutes |
| **Contract** (provider/consumer, Pact-style) | Multi-team APIs, partner webhooks, event schemas, mobile/BFF contracts, public APIs | Single-team internal calls where integration tests already cover the boundary | Medium; seconds |
| **Component / slice** (one service, mocked external deps) | Service-level behavior including auth, validation, error mapping, and middleware | Cross-service consistency or real dependency behavior matters | Medium; seconds |
| **E2E / journey** (full stack, real or staging deps) | Critical user journeys (login → payment → confirmation), smoke tests post-deploy | Every edge case; flaky environments; slow feedback | High; minutes |
| **Performance / load** (k6, Gatling, locust) | Latency SLOs, throughput limits, connection pool sizing, queue lag under load, capacity planning | Functional correctness (use other types first) | High; minutes to hours |
| **Chaos / fault injection** (Chaos Monkey, Litmus, toxiproxy) | Failover, circuit breaker, timeout, retry storm, partial write recovery | Deterministic failure cases not yet covered by integration tests | High; requires operational maturity |
| **Security** (SAST, DAST, dependency scan, pen test) | Injection, auth bypass, dependency CVEs, secrets in code, abuse cases | Replacing business-logic authorization tests | Varies |
| **Migration / rollback** (expand-contract, backfill, restore) | Schema changes, data backfills, CDC consumer compatibility, restore drills | No data shape or downstream consumer changes | Medium to high |

**Selection rules**:
1. Cover business rules with unit/scenario tests first — they are the fastest feedback.
2. Cover boundaries (DB, broker, cache, partner) with integration or contract tests — mocks hide real behavior.
3. Cover critical journeys with a small E2E suite — not every permutation.
4. Cover performance and resilience only after functional correctness is solid.
5. For regulated flows (payments, claims, policies, billing), require at least: unit for rules, integration for persistence, contract for external APIs, and one E2E for the critical journey.
## Implementation Guidance
Add tests in the same delivery slice as implementation. Use builders or fixtures that express business meaning. Keep mocks at process boundaries, not for every collaborator. Include observability assertions when workflows require audit events, metrics, traces, alerts, or emitted messages.

Use test doubles deliberately:

- Use mocks for pure domain collaborators and rare error paths where the contract is already tested elsewhere.
- Use real database engines for SQL behavior, migrations, constraints, isolation, and query plans.
- Use broker/cache/object-store/search test containers or controlled integration environments when delivery, TTL, indexing, or signed URL behavior matters.
- Use contract tests for partner APIs, webhooks, mobile clients, BFFs, and public APIs that cannot be verified by one repository alone.

Make failure tests repeatable: inject clock, IDs, dependency responses, retry counters, queue messages, and feature flag state. Keep test data synthetic, classified, and safe for logs.
## Testing Expectations
- Run unit tests on each change and integration/contract tests before merge.
- Run E2E tests on critical release paths and after environment changes.
- Include negative, boundary, permission, concurrency, migration, and rollback tests where relevant.
- Test idempotency for retried API calls, message redelivery, mobile duplicate submits, job restarts, and partner callbacks.
- Test degraded behavior for dependency timeout, cache outage, queue backlog, rate limiting, expired credentials, object scan failure, search lag, and partial writes.
- Verify logs, metrics, traces, audit events, dashboards, and alerts for critical workflows before launch.
## Security / Performance / Reliability Considerations
Tests must avoid real secrets and sensitive production data. Performance tests should measure meaningful latency, throughput, queue lag, cache hit rate, dependency saturation, and user-visible percentiles. Reliability tests must include retry, timeout, duplicate event, stale cache, partial failure, failover, replay, backfill, and recovery behavior for critical flows. Security tests must verify denial paths, tenant boundaries, redaction, and secret rotation without leaking credentials into artifacts.
## Review Checklist
- Risks are mapped to test types.
- Critical business rules have fast tests.
- Boundaries have integration or contract coverage.
- E2E scope is small and valuable.
- Test data is deterministic and safe.
- Flaky tests have owners.
- CI time remains acceptable.
- Messaging, cache, search, object storage, gateway, and job behavior are covered where present.
- Observability and alert behavior are tested for production-critical workflows.
- Migration, rollback/roll-forward, and reconciliation tests exist when data shape or downstream consumers change.
## Anti-Patterns to Avoid
- Counting coverage percentage as confidence.
- Mocking the database for repository behavior that depends on SQL.
- Testing implementation details instead of observable behavior.
- Creating E2E tests for every edge case.
- Ignoring migration and rollback tests.
- Mocking brokers, caches, identity providers, or object storage for production-critical behavior and then claiming integration confidence.
- Testing only happy-path synchronous requests while async consumers, jobs, DLQs, search projections, and cache invalidation remain untested.
- Treating telemetry, runbooks, and alerts as operational documentation instead of testable release criteria.
## Gotchas / Common Failure Modes
- Test environments often differ from production in data volume, permissions, network, and time zones.
- Mocks can preserve wrong assumptions.
- UI tests fail from timing unless designed around user-observable state.
- Contract tests need versioning discipline.
- Slow suites get bypassed.
- Idempotency bugs usually appear only under retries, duplicate messages, mobile reconnect, gateway retries, and job restarts.
- Cache, search, and analytics copies can pass functional tests while leaking stale permissions or deleted regulated data.
- Alerts that were never fired in staging often page the wrong team or lack the missing context during the first incident.

## Test Plan Template

Copy this template when planning tests for a new feature or story. Fill relevant rows; mark N/A for inapplicable categories.

```markdown
# Test Plan: <Feature Name>

**Story/Ticket:** <link>
**Risk class:** low | medium | high | production-critical
**Packs involved:** <list>

## Coverage Matrix

| Category | Test cases | Type | Priority |
|---|---|---|---|
| Happy path | <main success scenario> | Unit + Integration | Must |
| Validation/input | Invalid input, missing fields, boundary values | Unit | Must |
| Authorization | Unauthorized, wrong tenant, wrong role, same-role-different-resource | Integration | Must (if auth) |
| Error handling | Dependency timeout, 5xx, invalid response, partial failure | Integration | Must |
| Idempotency | Duplicate request, retry after timeout, concurrent same-key | Integration | Must (if mutating) |
| Concurrency | Optimistic lock conflict, race condition, double-submit | Integration | High risk only |
| Data correctness | Constraint violation, state transition guard, audit trail | Integration | Must (regulated) |
| Migration/rollback | Schema compat, backfill, rollback, dual-write | Migration test | Must (if schema change) |
| Performance | Latency p95, throughput, query plan, N+1 | Load test | If SLO-bound |
| Security | Injection, XSS, CSRF, secret exposure, PII in logs | Security scan + manual | Must (if user input) |
| Observability | Metrics emitted, logs structured, traces propagated, alerts fire | Integration | Must (production-critical) |
| Degraded mode | Cache outage, queue backlog, dependency down, rate limited | Integration | High risk only |

## Test Data Requirements
- [ ] Synthetic data (no production PII)
- [ ] Representative volume for performance tests
- [ ] Edge cases: empty, max-size, unicode, timezone boundary
- [ ] Multi-tenant: at least 2 tenants in test data

## Definition of Done (Testing)
- [ ] All "Must" rows have passing tests
- [ ] No test uses real secrets or production data
- [ ] CI runs in < X minutes
- [ ] Coverage for changed code ≥ 80%
- [ ] Flaky tests: 0 new, existing quarantined with owner
```

## Coverage Checklist by Feature Type

### API Endpoint (REST/GraphQL/gRPC)

| Must test | Example |
|---|---|
| Request validation | Missing required field → 400 with details |
| Authorization per resource | User A cannot access User B's resource → 403 |
| Idempotency (if POST/mutation) | Same idempotency key → same response, no duplicate side effect |
| Error contract | Dependency timeout → 503 with retry-after; validation → 400 with field errors |
| Pagination boundary | Empty result, last page, concurrent insert during pagination |
| Rate limit behavior | Exceed limit → 429 with Retry-After header |
| Contract compatibility | Old client still works after field addition |
| Observability | Request logged with correlation_id; metrics emitted; trace spans present |

### Messaging Consumer (Kafka/RabbitMQ/SQS)

| Must test | Example |
|---|---|
| Duplicate message | Same event_id delivered twice → side effect happens once |
| Out-of-order delivery | Event B arrives before Event A → correct final state |
| Poison message | Malformed payload → DLQ, not infinite retry |
| Retry exhaustion | 3 failures → DLQ with error metadata |
| Schema evolution | Old schema message still processable by new consumer |
| Lag recovery | Consumer restarts → resumes from checkpoint, no data loss |
| Idempotent side effects | Payment/email/notification not duplicated on redelivery |

### Database Migration

| Must test | Example |
|---|---|
| Forward migration | Clean apply on empty + production-like schema |
| Backward compatibility | Old code still works with new schema (expand phase) |
| Backfill correctness | All existing rows transformed correctly |
| Rollback/roll-forward | Revert migration without data loss |
| Constraint safety | New constraint doesn't reject valid existing data |
| Performance impact | Migration completes within maintenance window; no lock timeout |
| Downstream consumers | CDC, search index, cache still work after schema change |

### Background Job / Batch

| Must test | Example |
|---|---|
| Idempotent rerun | Same job with same input → same result, no duplicates |
| Partial failure + resume | Crash at row 5000 → restart processes from 5001 |
| Overlapping prevention | Two instances don't run simultaneously |
| Empty input | No work to do → completes successfully, no error |
| Dirty data | Null fields, invalid references, duplicate keys handled |
| Throttling | Doesn't overload downstream DB/API/queue |
| Completion proof | Metric/log confirms all expected records processed |

### UI Component (React/Angular/Mobile)

| Must test | Example |
|---|---|
| All async states | Loading, success, error, empty, stale, rate-limited |
| Form validation | Required fields, format, boundary, cross-field |
| Accessibility | Keyboard navigation, screen reader, focus management |
| Authorization UX | Forbidden action → clear message (not broken UI) |
| Duplicate submit prevention | Double-click → one request (disable + idempotency key) |
| Offline/reconnect | Network drop → queue or clear error; reconnect → retry |
| Sensitive data masking | PII masked by default; reveal requires action + audit |
