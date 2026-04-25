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
