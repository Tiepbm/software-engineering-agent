---
name: core-engineering-pack
description: 'Use when clarifying requirements, shaping solution architecture, designing system/API boundaries, defining test strategy, or reviewing/refactoring software for maintainability and delivery risk.'
---
# Core Engineering Pack

## When to Use
- Ambiguous scope, business rules, actors, acceptance criteria, NFRs, or measurable outcomes.
- Architecture shape, service boundaries, sync/async decisions, ownership, deployment boundaries.
- API contracts (REST/GraphQL/gRPC/async), idempotency, pagination, validation, versioning.
- Risk-based test strategy, contract/E2E scope, fault-injection scope.
- Code review severity, safe refactoring sequence, compatibility checks.

## When NOT to Use
- Concrete framework code (handlers, hooks, components, JPA mappings) → `application-stacks-pack`.
- Database schema or query optimization → `data-database-analytics-pack`.
- Messaging/eventing/gateway/workflow design → `platform-integration-pack`.
- Telemetry, SLOs, runbooks, CI/CD design → `observability-release-pack`.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `requirements-analysis` | Use when actors, business rules, acceptance criteria, NFRs, edge cases, or scope slicing are unclear; the team disagrees on the problem. |
| `solution-architecture` | Use when CHOOSING boundaries, ownership, sync vs async, build vs buy, or producing an ADR. |
| `system-design` | Use when describing runtime flow, failure modes, sequence/state diagrams, or component-level behavior of a SELECTED architecture. |
| `api-design` | Use when defining a specific API contract (style, schema, idempotency, versioning, pagination, error model, deprecation). |
| `testing-strategy` | Use when sizing the testing pyramid, picking test types, defining contract/E2E/migration/fault-injection scope, or test data strategy. |
| `code-review-and-refactoring` | Use when reviewing a PR, ranking review severity, planning a multi-step refactor, or assessing compatibility risk. |
| `architecture-decision-records` | Use when capturing or reviewing an architectural decision, its alternatives, trade-offs, and consequences in a durable, append-only ADR. |
| `legacy-modernization` | Use when modernizing a legacy system: strangler fig, anti-corruption layer, dual-write migration, legacy DB integration, or phased cutover for core banking/insurance. |

## Cross-Pack Handoffs
- → `data-database-analytics-pack` when the architecture/API materially changes the data model.
- → `security-access-pack` when boundaries cross trust/tenant lines.
- → `platform-integration-pack` for any sync↔async boundary or external partner contract.
- → `observability-release-pack` for the rollout plan and validation checklist.

