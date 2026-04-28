---
name: security-access-pack
description: 'Use when reviewing attack surfaces or designing authentication, authorization, tenant isolation, identity propagation, secrets, audit controls, abuse cases, or sensitive data handling.'
---
# Security and Access Pack

## When to Use
- Identity, sessions, tokens, RBAC/ABAC/ReBAC, resource-level authorization, tenant isolation, admin access.
- PII / payment / financial / policy / claim / billing data, secrets, file uploads, external callbacks, sensitive telemetry.
- Dependency risk, input validation, abuse paths, privilege boundaries, cross-surface security audit.

## When NOT to Use
- Pure transport telemetry / SLOs (no PII concern) → `observability-release-pack`.
- Pure framework auth wiring without policy decisions → `application-stacks-pack`.
- Network rate-limiting/throttling (not identity-based) → `platform-integration-pack` → `rate-limiting-and-traffic-control`.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `security-review` | Use when AUDITING an existing change/system across the 4 paths (request, async, derived state, operator) for cross-surface risks. |
| `authn-authz-and-secrets` | Use when DESIGNING identity/token/session, choosing an authorization model (RBAC/ABAC/ReBAC), or planning secret storage/rotation. |

## Cross-Pack Handoffs
- → `observability-release-pack` for sensitive logging, masking, and audit-event schema.
- → `data-database-analytics-pack` for row-level/tenant authz and column-level masking in the DB.
- → `storage-search-pack` for signed-URL authz and document/field-level filtering.
- → `platform-integration-pack` for partner-callback identity propagation and gateway policy.

