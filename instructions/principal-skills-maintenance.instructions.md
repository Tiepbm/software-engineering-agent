---
description: 'Guides maintenance and extension of the Principal Software Engineering skill set so each skill remains focused, production-grade, and compatible with the package.'
applyTo: 'skills/**/SKILL.md'
---
# Principal Skills Maintenance Instructions

## Purpose

Use these instructions when editing or adding `skills/<skill-name>/SKILL.md` files in this package. Each skill must remain a focused expert playbook with concrete production guidance, not a generic best-practices article.

## Package Boundary

- Keep these skills in this standalone package unless the user explicitly asks to contribute to another repository.
- Do not place generated skills back into `awesome-copilot` by default.
- Preserve the path convention: `skills/<skill-name>/SKILL.md`.

## Required Skill Frontmatter

Every `SKILL.md` must start with markdown frontmatter:

- `name`: lowercase, hyphen-separated, and exactly matching the folder name.
- `description`: concise, non-empty, wrapped in single quotes, and between 10 and 1024 characters.

Example:

```markdown
---
name: example-skill
description: 'Clear description of the focused skill purpose.'
---
```

## Required Section Order

Every skill must keep these sections in this order:

1. Title
2. Description
3. Purpose
4. When to Use
5. Responsibilities
6. Decision Principles
7. Expected Output Style
8. Architecture / Design Guidance
9. Implementation Guidance
10. Testing Expectations
11. Security / Performance / Reliability Considerations
12. Review Checklist
13. Anti-Patterns to Avoid
14. Gotchas / Common Failure Modes

### Optional Trailing Sections

After the 14 required sections, a skill may append any of the following — but only after all 14, never interleaved:

- `See Also` — at most 4 cross-links to genuinely adjacent skills (not a catalog of every skill in the package).
- `Worked Example` / `Worked Example: <topic>` — a concrete, end-to-end illustration (DDL, query plan, contract, decision walk-through). Prefer this over abstract advice when the skill teaches a pattern.
- `<Name> Template` — a reusable template (e.g. ADR Template, NFR Capture Template, Runbook Template). Must be self-contained and copyable.

Subsections (`###`) inside a required section are allowed and encouraged for decision matrices, templates, and worked examples that belong to that section's topic (e.g. NFR table inside Architecture / Design Guidance).

## Skill Quality Bar

Each skill must be written like a senior/principal engineer playbook:

- Use concrete, enforceable rules.
- Explain trade-offs and rejected shortcuts.
- Include failure modes that actually happen in production.
- Separate tactical implementation guidance from architecture or operational guidance.
- Include test expectations and review checklists that a team can apply during PR review.
- Avoid vague phrases such as “follow best practices” unless followed by specific verification rules.
- Keep guidance useful for enterprise systems, especially banking, insurance, transaction-heavy, regulated, and audit-heavy workloads.

### Minimum Depth Floor

- Stack-specific skills (`*-development`: dotnet, java-spring-boot, reactjs, angular, react-native) must be **≥ 130 lines**. Below this floor a stack skill cannot reliably cover framework version, ecosystem libraries, decision matrices, and gotchas at principal grade.
- All other skills must be **≥ 90 lines**, unless explicitly marked as a delegation skill (see Focus and Boundary Rules).
- Length is a sanity floor, not a target — bloat is still rejected by the Anti-Patterns rules. Prefer adding a worked example or decision matrix over restating prose.

### Decision Matrix Preference

When a skill describes choices among multiple options (algorithm, model, framework style, storage engine, authorization model, pagination strategy, etc.), prefer a **comparison table** with at minimum the columns *Option*, *Strong fit*, *Avoid when* — instead of paragraph prose. Tables make trade-offs reviewable in PRs and are easier for the model to follow at runtime.

## Focus and Boundary Rules

Do not turn every skill into a giant platform document. Keep the skill’s original purpose and route deeper concerns to related skills:

- Use `security-review` for attack surfaces, sensitive data, dependency risk, and abuse cases.
- Use `authn-authz-and-secrets` for identity, resource authorization, tenant isolation, secrets, and credential rotation.
- Use `messaging-and-eventing` for queues, topics, events, ordering, idempotency, retries, DLQs, replay, and consumer operations.
- Use `caching-and-distributed-state` for TTLs, invalidation, stale reads, distributed locks, sessions, and cache authorization safety.
- Use `resilience-and-fault-tolerance` for timeouts, retries, circuit breakers, bulkheads, degradation, and failure containment.
- Use `logging-metrics-and-tracing` for structured logs, metrics, traces, correlation IDs, redaction, and telemetry fields.
- Use `monitoring-alerting-and-slos` for SLIs, SLOs, dashboards, alert thresholds, severity, ownership, and runbooks.
- Use `background-jobs-and-batch-processing` for scheduled work, workers, chunking, checkpointing, duplicate prevention, and resumability.
- Use `workflow-and-job-orchestration` for long-running workflows, state machines, approvals, compensation, and manual repair.
- Use `api-gateway-and-service-integration` for gateways, BFFs, partner integration, auth propagation, transformation, and external dependency boundaries.
- Use `file-and-object-storage` for uploads, downloads, signed URLs, retention, malware scanning, metadata, and large-file behavior.
- Use `search-and-indexing` for search projections, relevance, filtering, authorization, reindexing, and source-of-truth synchronization.
- Use `rate-limiting-and-traffic-control` for quotas, throttling, backpressure, priority traffic, partner protection, and graceful rejection.

### Delegation Skills

A skill may be intentionally short ("delegation map") when its domain is fully owned by sibling skills. Current example: `observability-and-sre` delegates detail to `logging-metrics-and-tracing` and `monitoring-alerting-and-slos`. For a delegation skill:

- The Architecture / Design Guidance and Implementation Guidance sections must explicitly name **which sibling skills own the detail** and what each owns.
- Do not duplicate signal lists, alert thresholds, log field schemas, or runbook templates that already exist in the sibling skills.
- The skill should still describe the integration story (how the pieces compose) and any responsibility that does not fit cleanly inside one sibling.
- The Minimum Depth Floor does not apply; instead the skill must be reviewed for "no duplicated detail" on every change.

## Enterprise Production Rules

When a skill touches regulated or business-critical systems, require explicit handling of:

- data correctness and source of truth;
- resource-level authorization and tenant isolation;
- idempotency for retries, duplicate submissions, jobs, messages, and external callbacks;
- audit evidence for privileged, financial, policy, claim, billing, document, and support operations;
- migration, backfill, rollback or roll-forward, and reconciliation;
- observability that can answer what failed, who or what was affected, and what operator action is safe;
- operational ownership, runbooks, dashboards, and support repair paths.

## Stack-Specific Skill Rules

Stack skills such as `.NET`, Spring Boot, React, Angular, and React Native must remain framework-focused:

- Explain framework-specific patterns, APIs, pitfalls, and tests.
- Do not hide platform concerns inside controllers, annotations, hooks, interceptors, services, or mobile screens.
- Route broader concerns to platform skills when the design involves messaging, caching, security, identity, object storage, search, rate limiting, resilience, observability, jobs, or release safety.

## Anti-Patterns to Avoid

- Repeating the same generic platform paragraph in every skill.
- Adding tool names, databases, queues, or frameworks without workload-fit reasoning.
- Recommending messaging without ordering, retry, idempotency, DLQ, replay, and operator repair rules.
- Recommending caching without staleness, invalidation, tenant isolation, stampede protection, and fallback behavior.
- Recommending monitoring without actionable signals, severity, owner, and runbook.
- Recommending security-sensitive changes without authn, authz, secrets, audit, sensitive telemetry, and abuse-case review.
- Treating analytics, search, cache, object storage, or event logs as accidental systems of record.
- Adding a `See Also` block that lists more than 4 skills, or links to skills that are not genuinely adjacent — `See Also` is a routing aid, not a sitemap.
- Letting a stack skill drift below the 130-line floor without a delegation-skill justification recorded in the PR.
- Replacing a decision matrix with paragraph prose during "cleanup" — the matrix is the contract.

## Review Checklist

Before finalizing a skill change, verify:

- The `name` field exactly matches the skill folder.
- The `description` is clear and validation-friendly.
- All required sections exist in the correct order.
- Any optional trailing section (`See Also`, `Worked Example`, `<Name> Template`) appears only after the 14 required sections.
- Stack skills meet the 130-line floor; other skills meet the 90-line floor (or are explicitly delegation skills).
- Choice-among-options content uses a decision matrix, not prose.
- The skill remains focused on its domain.
- Cross-cutting concerns are referenced only where they affect the skill’s domain.
- Gotchas and anti-patterns are concrete enough to catch production defects.
- Testing expectations include failure paths, not only happy paths.
- Security, performance, and reliability considerations are specific and reviewable.

