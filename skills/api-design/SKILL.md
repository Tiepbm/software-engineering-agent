---
name: api-design
description: 'Designs durable API boundaries, request and response contracts, errors, pagination, filtering, idempotency, versioning, and integration usability.'
---
# API Design
## Description
Designs durable API boundaries, request and response contracts, errors, pagination, filtering, idempotency, versioning, and integration usability.
## Purpose
- Create APIs that are predictable for consumers, evolvable for providers, and explicit about errors, compatibility, and data semantics.
- Make integration behavior testable before implementation.
- Prevent endpoint-by-endpoint drift in naming, validation, pagination, status codes, and error payloads.
## When to Use
- Creating or reviewing REST, GraphQL, RPC, webhook, event, or internal service contracts.
- Consumers need stable contracts across teams, products, mobile clients, partners, or long-lived integrations.
- An API has inconsistent errors, breaking changes, inefficient list endpoints, duplicate submissions, or unclear validation behavior.
- API behavior depends on gateway routing, auth propagation, rate limiting, idempotency, async callbacks, partner integration, object download/upload, or search/list semantics.
## Responsibilities
- Define resources, commands, query patterns, lifecycle states, and ownership boundaries.
- Specify request, response, error, validation, authentication, authorization, pagination, filtering, sorting, and idempotency contracts.
- Protect backward compatibility and define versioning or evolution policy.
- Design for consumer usability without exposing internal persistence models.
- Involve `api-gateway-and-service-integration`, `authn-authz-and-secrets`, `rate-limiting-and-traffic-control`, `security-review`, `messaging-and-eventing`, or `file-and-object-storage` when those concerns shape the API contract.
## Decision Principles
- Use resource-oriented endpoints for CRUD-like domains and command endpoints for business actions with side effects.
- Require cursor pagination for large or mutable lists; offset pagination is acceptable only for small stable datasets.
- Use idempotency keys for retried creates, payments, external calls, and mobile unreliable networks.
- Return stable error codes with human messages and machine-actionable details.
- Propagate authorization, tenant, trace, and idempotency context explicitly across service and partner boundaries; never rely on client-side checks for regulated decisions.
## Expected Output Style
- Start with the decision or finding, then provide the reasoning needed to trust it.
- Separate immediate actions from longer-term improvements.
- State assumptions, constraints, trade-offs, risks, and missing information explicitly.
- Use concrete examples, acceptance criteria, contracts, schemas, queries, or checklists when they reduce ambiguity.
- Avoid generic advice unless it is followed by an enforceable rule or verification step.
## Architecture / Design Guidance
API boundaries should reflect product capabilities and ownership boundaries. Avoid leaking table names, ORM entity graphs, internal enum churn, or workflow implementation details. For events and webhooks, define schema version, ordering expectations, delivery retry policy, duplicate handling, replay support, and signature or authentication rules. For banking and insurance APIs, contract errors must be audit-safe: enough for support and reconciliation without exposing account, claim, policy, payment, or regulated personal data.

Gateway-facing APIs must define route ownership, authentication mode, authorization context, rate limits, quota headers, timeout behavior, body limits, correlation IDs, and dependency failure mapping. File and object workflows should prefer pre-signed or mediated upload/download contracts with content validation, malware scanning, lifecycle rules, and access revocation. Search/list APIs must define freshness expectations and authorization filtering rather than pretending search indexes are transactional truth.

### Style Selection (REST vs GraphQL vs gRPC vs Async)
| Style | Strong fit | Avoid when |
|---|---|---|
| REST + JSON | Public, partner, mobile, long-lived integrations; cache-friendly reads; broad tooling | Many tiny chained calls per screen, or strongly typed binary contracts needed |
| GraphQL | One BFF aggregating many backends for a UI client with varied selection sets | Public/partner API where query cost is hard to bound; write-heavy or transactional workflows; clients that need stable cacheable URLs |
| gRPC / protobuf | Internal service-to-service, low-latency, schema-first, polyglot, streaming | Browser-direct without a gateway, partner integrations without tooling, ad-hoc inspection-heavy workflows |
| Webhooks / Events | Push notifications, partner callbacks, eventual workflows | Synchronous request/response semantics, ordered transactional state changes |

GraphQL specifics: enforce persisted queries or query allow-lists for partner/public surfaces; cap depth, breadth, and complexity per operation; require dataloader-style batching to avoid N+1; authorize at field/resolver level, not only at schema entry; design error model as `data` + `errors` semantics, not HTTP status codes; mutations should still be idempotent for retry safety.

gRPC specifics: version via package name (`v1`, `v2`); never reuse field numbers; only add optional fields for backward-compatible evolution; use `Status` codes consistently across services; configure deadlines on every call; expose gRPC-Gateway or Connect when browsers need access.

### Versioning Strategy
| Approach | When acceptable | Trade-off |
|---|---|---|
| URI version (`/v1/...`) | Public + partner APIs, mobile clients with long upgrade tail | Forces new path on every breaking change; encourages "v2 rewrites" |
| Header version (`Api-Version: 2026-04-01`) | Internal or controlled-consumer APIs needing fine-grained dated revisions | Harder to inspect; cache keys must include header |
| Field-level evolution (additive only) | Default for all APIs between breaking versions | Requires discipline: never remove or repurpose fields silently |
| Capability negotiation (Accept-Version, feature flags) | Multi-tenant SaaS where tenants opt-in to behavior | Adds matrix of supported combinations; must be tested |

Rules: breaking changes ship as a new version with overlap window covering the slowest mobile/partner upgrade tail; deprecation requires `Deprecation` + `Sunset` headers, changelog entry, and proactive consumer migration tracking; never repurpose an existing field's meaning, units, enum, or nullability — add a new field instead.

### Pagination Algorithms
| Algorithm | Use when | Avoid when |
|---|---|---|
| Cursor (opaque, monotonic key) | Default for any list that can grow, mutate, or be exported | — |
| Keyset / seek (`WHERE id > :last AND ...`) | High-traffic feeds, infinite scroll, mutable lists | Sort by non-unique field without composite tiebreaker |
| Offset / limit | Small (< 1000), stable, admin-only datasets | Deep pages, concurrent writes, mobile lists |
| Token + total count | When UI must show total; total is approximate or capped | Per-tenant dataset > 100k where COUNT cost dominates |

Always cap `limit` server-side; return `next_cursor` (and `prev_cursor` only if needed); make cursors opaque (base64) to allow internal evolution; signed cursors prevent tampering on partner APIs.
## Implementation Guidance
Write contracts before code where integration risk is high. Include examples for success, validation failure, authorization failure, not found, conflict, rate limit, timeout, duplicate idempotency key, and dependency failure. Enforce DTO boundaries and map explicitly between domain and wire formats. Specify whether mutating endpoints are synchronous, accepted for asynchronous processing, or split into command plus status/query endpoints.
## Testing Expectations
- Contract tests must verify request and response shapes, required fields, error payloads, status codes, and compatibility.
- Consumer-driven tests are required for multi-team or partner APIs.
- Add idempotency, retry, duplicate submission, timeout, and gateway rate-limit tests for mutating endpoints.
- Include pagination, filtering, sorting, and boundary validation tests.
## Security / Performance / Reliability Considerations
Do not expose sensitive fields by default. Authenticate every non-public endpoint and authorize per resource, not only per route. Performance requirements must cover list limits, N+1 serialization, payload size, compression, rate limiting, cache headers, and gateway/body-size limits. Reliability requires timeouts, retry guidance, idempotency persistence, async status visibility, and trace IDs.
## Review Checklist
- Resources and actions are named consistently.
- Contracts include examples and error shapes.
- Pagination and filtering are bounded.
- Mutating retries are safe.
- Backward compatibility is protected.
- Authorization semantics are explicit.
- Rate limits, idempotency rules, auth propagation, and gateway behavior are explicit.
- Internal models are not leaked.
## Anti-Patterns to Avoid
- Returning raw database entities.
- Using 200 OK for every outcome.
- Adding unbounded list endpoints.
- Changing response fields without compatibility analysis.
- Making clients parse human-readable error text for control flow.
- Ignoring webhook duplicate delivery.
- Returning sensitive business details in errors, URLs, logs, or cacheable responses.
## Gotchas / Common Failure Modes
- Mobile clients may run old API versions for months.
- Optional fields become required in practice when clients depend on them.
- Offset pagination can skip or duplicate records under concurrent writes.
- Partial update semantics are often ambiguous.
- Idempotency storage must expire safely without allowing duplicate side effects.
- Gateway retries, mobile retries, and partner retries can duplicate payments, claims submissions, document uploads, or policy changes unless the API contract makes side effects idempotent.
