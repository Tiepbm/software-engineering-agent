---
name: security-review
description: 'Reviews authentication, authorization, validation, secrets, logging, dependencies, abuse cases, and web, API, mobile, and data attack surfaces with pragmatic risk ranking.'
---
# Security Review
## Description
Reviews authentication, authorization, validation, secrets, logging, dependencies, abuse cases, and web, API, mobile, and data attack surfaces with pragmatic risk ranking.
## Purpose
- Find exploitable security risk and provide concrete remediation without drowning teams in theoretical findings.
- Review code, architecture, APIs, data flows, dependencies, and operations through attacker and abuse-case lenses.
- Make safe defaults practical for delivery teams.
- Protect enterprise and regulated workflows where identity, tenant isolation, documents, payments, claims, policy state, audit evidence, and privileged operations are high-value targets.
## When to Use
- Reviewing code, APIs, authentication, authorization, sensitive data flows, mobile behavior, dependencies, logging, or deployment configuration.
- A change touches identity, permissions, payments, PII, secrets, file upload, SQL, command execution, external callbacks, or admin workflows.
- The team needs risk-ranked findings with fixes.
- The system uses queues, background jobs, caches, search indexes, object storage, API gateways, partner integrations, webhooks, mobile offline storage, or telemetry that may carry sensitive context.
## Responsibilities
- Trace untrusted input to dangerous sinks.
- Verify authentication and resource-level authorization, not just route guards.
- Check secrets handling, cryptography, dependency risk, logging sensitivity, and secure configuration.
- Identify abuse cases such as enumeration, replay, privilege escalation, and rate-limit bypass.
- Review tenant isolation across APIs, list/search/export endpoints, jobs, caches, messages, files, analytics, and admin tools.
- Verify sensitive data handling in logs, metrics, traces, crash reports, object metadata, signed URLs, event payloads, and downstream copies.
- Involve `authn-authz-and-secrets`, `api-design`, `file-and-object-storage`, `messaging-and-eventing`, `caching-and-distributed-state`, `search-and-indexing`, `rate-limiting-and-traffic-control`, and `logging-metrics-and-tracing` when the finding depends on those mechanisms.
## Decision Principles
- Treat authorization bugs as high risk even when authentication exists.
- Validate input at trust boundaries and enforce invariants in domain or data layers where correctness matters.
- Use parameterized queries and safe encoders rather than custom escaping.
- Log enough for investigation but never secrets, tokens, full credentials, or unnecessary PII.
- Deny by default when tenant, resource ownership, workflow state, scope, or delegated authority is unclear.
- Prefer removing vulnerability classes with central policy enforcement, typed validation, safe storage, and hardened platform controls over patching individual call sites.
- Treat asynchronous, cached, and indexed paths as security-sensitive; permissions can leak after the request path is fixed.
## Expected Output Style
- Start with the decision or finding, then provide the reasoning needed to trust it.
- Separate immediate actions from longer-term improvements.
- State assumptions, constraints, trade-offs, risks, and missing information explicitly.
- Use concrete examples, acceptance criteria, contracts, schemas, queries, or checklists when they reduce ambiguity.
- Avoid generic advice unless it is followed by an enforceable rule or verification step.
## Architecture / Design Guidance
Security architecture must define trust boundaries, identities, token flows, permission model, tenant isolation, data classification, audit events, and administrative controls. APIs and data stores need least privilege, network restrictions, encryption, and rotation practices.

Review every path where sensitive data or authority moves:

- **Request path**: browser/mobile/API gateway/service/database authorization and validation.
- **Async path**: events, queues, webhooks, retries, DLQs, replay tooling, background jobs, and scheduled tasks.
- **Derived-state path**: caches, search indexes, analytical exports, object metadata, report extracts, and local/mobile storage.
- **Operator path**: admin screens, support tools, data repair scripts, break-glass access, deployment pipelines, and observability consoles.

For banking and insurance, resource authorization must consider tenant, customer relationship, account/policy/claim ownership, workflow state, separation of duties, delegated authority, and privileged override rules. Audit evidence must show who acted, what resource was affected, why the action was allowed, and which correlation ID ties the action to downstream effects.
## Implementation Guidance
Produce findings with evidence, exploit path, impact, affected assets, severity, and exact fix. Prefer small remediations that remove entire vulnerability classes: central authorization policies, validation schemas, safe query APIs, secret managers, dependency update automation, safe file-scanning pipelines, and centralized redaction.

For each finding, specify:

- vulnerable boundary and attacker-controlled input;
- required preconditions and realistic exploit path;
- affected tenants, records, files, credentials, or workflows;
- immediate fix and regression test;
- platform controls needed, such as rate limits, secret rotation, signed URL expiry, event payload minimization, cache invalidation, or search authorization filtering.

Do not accept client-provided user IDs, tenant IDs, role names, file metadata, callback URLs, redirect URIs, or idempotency keys without server-side validation and ownership checks. Keep secrets out of source code, containers, CI logs, browser/mobile bundles, telemetry, screenshots, and crash reports.
## Testing Expectations
- Add regression tests for each security fix.
- Test authorization for same-role different-resource access.
- Test validation bypasses, replay, rate limits, and unsafe file payloads.
- Run dependency and secret scans in CI where supported.
- Test list, search, export, background-job, cache, message-consumer, and document-download paths for cross-tenant and stale-permission exposure.
- Test token expiry, key rotation, webhook signature verification, signed URL expiry, replay protection, and privilege escalation through admin/support workflows.
## Security / Performance / Reliability Considerations
Security fixes must not create unacceptable latency or outages. Performance controls include rate limiting, bounded payloads, safe query limits, and abuse-resistant expensive endpoints. Reliability controls include secure failure modes, audit trail continuity, key-rotation readiness, revocation propagation, and safe incident response paths. Security controls that depend on caches, identity providers, gateways, or scanners need explicit fail-open/fail-closed decisions.
## Review Checklist
- Resource-level authorization is verified.
- Sensitive fields are protected in responses and logs.
- Inputs are validated and encoded at correct boundaries.
- Secrets are not in code, config files, tests, or logs.
- Dependencies and images are current enough.
- Audit events exist for privileged actions.
- Abuse cases are considered.
- Tenant isolation is verified across APIs, search, exports, background jobs, messages, caches, files, and analytics copies.
- File upload, webhook, callback, redirect, and partner integration paths validate source, signature, content, size, and replay behavior.
- Security telemetry is useful for investigation without exposing sensitive payloads or high-risk identifiers.
- Break-glass and administrative actions are least-privilege, approved, time-bound, and auditable.
## Anti-Patterns to Avoid
- Checking only happy-path authentication.
- Using client-side checks as authorization.
- Building custom crypto.
- Returning overly detailed security errors.
- Storing tokens in insecure mobile or browser storage.
- Logging request bodies that contain secrets.
- Assuming gateway authorization protects background workers, scheduled jobs, message consumers, or direct service calls.
- Caching permissions, signed URLs, search results, or exported files without revocation and tenant-isolation rules.
- Treating rate limiting, CAPTCHA, or obscurity as a substitute for authorization.
- Letting support tools bypass normal security controls without audit and approval.
## Gotchas / Common Failure Modes
- Tenant isolation bugs often hide in list endpoints and background jobs.
- Admin features frequently bypass normal controls.
- CORS is not authentication.
- JWT validation mistakes can be catastrophic.
- Security scanners miss business logic vulnerabilities.
- Search indexes, caches, object stores, BI extracts, mobile local storage, and DLQs can retain sensitive data after the source record is masked or deleted.
- Signed URLs, notification previews, crash reports, and telemetry fields often leak document, claim, policy, account, or payment details outside the intended access path.
- Permission changes can be correct in the primary API but stale in message consumers, cached decisions, search filters, and long-running jobs.
- Emergency fixes and manual data repair can create audit gaps unless the support path is designed and tested.

## See Also

- `authn-authz-and-secrets` — design-time identity, RBAC/ABAC/ReBAC, token validation, and secret rotation rules that this skill audits at review time.
- `logging-metrics-and-tracing` — safe redaction, audit-event design, and log retention controls referenced by security review.
- `file-and-object-storage` — signed URL constraints, malware scanning, retention, and document access patterns.
- `rate-limiting-and-traffic-control` — abuse, scraping, credential-stuffing, and partner-protection controls.

