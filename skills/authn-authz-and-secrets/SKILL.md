---
name: authn-authz-and-secrets
description: 'Designs authentication, authorization, identity propagation, RBAC, permission boundaries, service-to-service auth, secret storage, rotation, and least privilege.'
---

# Authn Authz and Secrets

## Description

Designs authentication, authorization, identity propagation, RBAC, permission boundaries, service-to-service auth, secret storage, rotation, and least privilege.

## Purpose

- Protect users, tenants, services, secrets, and regulated data with explicit identity and access controls.
- Prevent route-only authorization, privilege escalation, token leakage, stale permissions, and secret sprawl.
- Support enterprise, banking, and insurance systems where auditability and least privilege are mandatory.

## When to Use

- Designing OAuth2, OIDC, session models, token models, RBAC, ABAC, permissions, service-to-service auth, API scopes, or secrets handling.
- A change touches login, user roles, admin operations, customer data, policy/claim/billing state, payments, documents, or partner access.
- Existing systems have unclear permission boundaries, hardcoded secrets, broad service credentials, or missing audit trails.

## Responsibilities

- Define authentication model, trust boundaries, identity provider integration, token/session lifetime, and identity propagation.
- Design resource-level authorization, roles, permissions, tenant isolation, delegated access, and privileged operations.
- Specify secret storage, rotation, access policy, injection method, and incident response for leakage.
- Ensure audit events capture security-sensitive decisions and administrative actions.

## Decision Principles

- Authentication proves identity; authorization decides whether that identity can act on a specific resource.
- Prefer centralized policy decisions with local enforcement close to the protected operation.
- Use least privilege for users, services, pipelines, and jobs.
- Keep secrets out of code, logs, images, test fixtures, and client bundles.
- Short-lived credentials and rotation are safer than long-lived shared secrets.
- Deny by default when identity, tenant, scope, or policy is unclear.

## Expected Output Style

- State the identity model, access model, trust boundaries, and enforcement points.
- Include token/session lifetime, scopes, roles, permissions, and tenant isolation rules.
- Specify secret storage, rotation, and audit behavior.
- Identify abuse cases and expected denial behavior.
- Provide tests for same-role cross-resource access and privilege boundaries.

## Architecture / Design Guidance

Use OIDC for user authentication when federating enterprise identity. Use OAuth2 access tokens for delegated API access, with scopes that are meaningful but not a substitute for resource-level checks. Use service-to-service authentication with workload identity, mTLS, signed tokens, or managed identity where available.

Authorization architecture should protect domain actions, not just endpoints. Banking and insurance systems need checks such as user can view this account, adjust this claim, approve this payment, or access this document based on role, tenant, ownership, workflow state, and separation-of-duties rules.

### Authorization Model Selection

| Model | Strong fit | Avoid when |
|---|---|---|
| RBAC (roles → permissions) | Stable orgs, small role count, coarse-grained back-office tools | Roles explode (>50), per-resource ownership rules, dynamic conditions |
| ABAC (policy over attributes: user, resource, env, action) | Conditional rules ("agent can edit claims in own region during business hours"), regulated approvals, separation-of-duties | Hard-to-audit rule sprawl without a policy engine + tests |
| ReBAC (relationships: user → group → resource) | Hierarchical ownership (account → sub-account → policy), sharing/delegation, multi-level org trees, document/folder ACLs | Pure role-driven enterprise apps with no sharing |
| Hybrid (RBAC for coarse + ABAC/ReBAC for fine) | Most enterprise + banking + insurance systems in practice | When you cannot draw the boundary; default to RBAC + per-resource check |

Implementation hints:
- **OPA / Rego** — externalize ABAC policy from services; bundle policies; decision logging for audit; good for cross-service consistency.
- **AWS Cedar** — typed policy language with formal analysis; strong for ABAC with reasoning ("does any policy allow X?").
- **Google Zanzibar / SpiceDB / OpenFGA / Permify** — ReBAC at scale; consistency tokens (zookies) for read-after-write authorization correctness.
- **Casbin** — embedded RBAC/ABAC in app code; lighter weight, fewer guarantees than OPA.

### Token & Session Defaults
| Surface | Token type | Lifetime | Rotation |
|---|---|---|---|
| Browser SPA | Short access token + refresh via httpOnly cookie or BFF session | 5–15 min access, sliding session | On every refresh |
| Mobile | Access + refresh token, secure storage (Keychain / Keystore) | 15–60 min access, 14–90 d refresh | Refresh rotation, revoke on logout |
| Service-to-service | mTLS or workload identity (SPIFFE / managed identity) | ≤ 1 h | Automatic via platform |
| Partner / B2B | OAuth2 client credentials, signed JWT assertions, mTLS optional | ≤ 1 h | Per-partner rotation policy + revocation list |
| Admin / privileged | Step-up auth + short-lived elevated token | ≤ 15 min | Per-action; never persistent |

## Implementation Guidance

- Validate issuer, audience, signature, expiry, not-before, token type, and required claims.
- Enforce resource-level authorization in application services or policy handlers, not only in UI or gateway layers.
- Use separate privileges for read, create, update, approve, export, administer, and impersonate actions.
- Store secrets in managed secret stores or vaults; inject at runtime; rotate without redeploy where practical.
- Never log tokens, API keys, passwords, private keys, refresh tokens, or full authorization headers.
- Add audit events for login anomalies, privileged actions, permission changes, secret access, exports, and administrative overrides.

## Testing Expectations

- Test unauthenticated, expired token, invalid audience, invalid issuer, missing scope, wrong tenant, and insufficient role cases.
- Test same-role different-resource access to catch horizontal authorization bugs.
- Test privilege escalation attempts, admin-only actions, impersonation, and separation-of-duties constraints.
- Test secret rotation and revocation without downtime.
- Test audit event creation for security-sensitive actions.

## Security / Performance / Reliability Considerations

Security requires least privilege, deny-by-default, token validation, secret rotation, audit, and sensitive log controls. Performance requires caching policy data only with safe invalidation and staleness rules. Reliability requires identity provider outage behavior, key rollover handling, service credential renewal, and clear break-glass procedures.

## Review Checklist

- Authentication and authorization are separated and both are explicit.
- Resource-level and tenant-level checks protect sensitive actions.
- Token validation is complete.
- Secrets are stored and rotated safely.
- Service accounts have least privilege.
- Audit covers privileged and regulated actions.
- UI checks are not treated as security enforcement.
- Authorization tests cover negative and cross-tenant cases.

## Anti-Patterns to Avoid

- Route-level authorization only for resource-specific actions.
- Trusting client-provided tenant, role, or user identifiers.
- Using one shared service credential for many systems.
- Long-lived secrets in environment files, source code, containers, or CI logs.
- Treating OAuth scopes as complete business authorization.
- Caching permissions without invalidation after role changes.

## Gotchas / Common Failure Modes

- Horizontal authorization bugs often appear in list, search, export, and background-job paths.
- Token validation mistakes can accept tokens from the wrong issuer or audience.
- Role names rarely capture workflow-specific approval constraints.
- Secret rotation breaks systems that cache credentials indefinitely.
- Service-to-service calls can lose user context needed for audit and authorization.
- Emergency access without audit becomes a compliance finding.

