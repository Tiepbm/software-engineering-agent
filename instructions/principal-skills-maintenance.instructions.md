---
description: 'Guides maintenance and extension of the Principal Software Engineering skill set so each skill remains focused, production-grade, and compatible with the package.'
applyTo: 'skills/**/SKILL.md'
---
# Principal Skills Maintenance Instructions

## Purpose

Use these instructions when editing or adding `skills/<pack-name>/SKILL.md` files in this package. Each top-level skill is now a **hybrid pack skill**: a focused routing and synthesis layer with detailed former leaf skills stored under `references/*.md`.

## Package Boundary

- Keep these skills in this standalone package unless the user explicitly asks to contribute to another repository.
- Do not place generated skills back into `awesome-copilot` by default.
- Preserve the path convention: `skills/<pack-name>/SKILL.md` plus `skills/<pack-name>/references/<leaf-skill>.md`.
- Keep `.github/skills/` as the primary GitHub Copilot output mirror.
- When adopting patterns from sibling workspace projects, update `docs/external-skill-research.md` and apply `docs/skill-pack-quality-rubric.md`. Do not copy external skill text verbatim.

## Required Skill Frontmatter

Every `SKILL.md` must start with markdown frontmatter:

- `name`: lowercase, hyphen-separated, and exactly matching the pack folder name.
- `description`: concise, non-empty, wrapped in single quotes, between 10 and 1024 characters, and beginning with trigger-style `Use when` wording.

Example:

```markdown
---
name: example-skill
description: 'Clear description of the focused skill purpose.'
---
```

## Pack Skill Structure

Every top-level pack `SKILL.md` must keep these sections in this order:

1. Title
2. Description
3. Purpose
4. When to Use
5. Pack Reference Map
6. Routing Rules
7. Reference Selection Matrix
8. Expected Output Style
9. Token Efficiency Rules
10. Quality Gates

Former leaf references under `references/*.md` may retain their previous detailed 14-section playbook structure. Do not force leaf references into the short pack structure.

### Optional Trailing Sections

After the 14 required sections, a skill may append any of the following — but only after all 14, never interleaved:

- `See Also` — at most 4 cross-links to genuinely adjacent skills (not a catalog of every skill in the package).
- `Worked Example` / `Worked Example: <topic>` — a concrete, end-to-end illustration (DDL, query plan, contract, decision walk-through). Prefer this over abstract advice when the skill teaches a pattern.
- `<Name> Template` — a reusable template (e.g. ADR Template, NFR Capture Template, Runbook Template). Must be self-contained and copyable.

Subsections (`###`) inside a required section are allowed and encouraged for decision matrices, templates, and worked examples that belong to that section's topic (e.g. NFR table inside Architecture / Design Guidance).

## Skill Quality Bar

Each pack must be written like a senior/principal routing layer:

- Use concrete, enforceable rules.
- Explain trade-offs and rejected shortcuts.
- Include failure modes that actually happen in production.
- Separate tactical implementation guidance from architecture or operational guidance.
- Include test expectations and review checklists that a team can apply during PR review.
- Avoid vague phrases such as “follow best practices” unless followed by specific verification rules.
- Keep guidance useful for enterprise systems, especially banking, insurance, transaction-heavy, regulated, and audit-heavy workloads.
- Keep detailed domain instruction in `references/*.md`; the pack owns discovery, routing, and synthesis.

### Pack Size and Reference Rules

- Top-level pack skills must stay **≤ 100 lines** (CI-enforced). Detail belongs in `references/`.
- The package must expose exactly **8 peer pack skills** in both `skills/` and `.github/skills/`.
- The package must preserve exactly **33 former leaf references** across pack `references/` directories unless a deliberate migration updates `scripts/validate_hybrid_packs.py` and `evals/routing-benchmark.jsonl`.
- Former stack-specific references (`*-development`) should retain their detailed implementation depth inside `references/`, not as peer skills.

### Decision Matrix Preference

When a skill describes choices among multiple options (algorithm, model, framework style, storage engine, authorization model, pagination strategy, etc.), prefer a **comparison table** with at minimum the columns *Option*, *Strong fit*, *Avoid when* — instead of paragraph prose. Tables make trade-offs reviewable in PRs and are easier for the model to follow at runtime.

## Focus and Boundary Rules

Do not turn every pack into a giant platform document. Keep packs as routing and synthesis layers, then route deeper concerns to references:

- Use `security-access-pack` references for attack surfaces, identity, resource authorization, tenant isolation, secrets, sensitive data, and abuse cases.
- Use `platform-integration-pack` references for queues, topics, gateways, workflows, background jobs, rate limiting, retries, DLQs, replay, and consumer operations.
- Use `resilience-performance-pack` references for TTLs, invalidation, stale reads, locks, timeouts, retries, circuit breakers, performance, and profiling.
- Use `observability-release-pack` references for logs, metrics, traces, SLIs, SLOs, dashboards, alerts, runbooks, CI/CD, rollout, and release safety.
- Use `storage-search-pack` references for object storage, search projections, authorization filtering, and reindexing.
- Use `application-stacks-pack` references for framework-specific implementation (.NET, Spring Boot, React, Angular, React Native).
- Use `data-database-analytics-pack` references for data models, database decisions, SQL/ORM tuning, DB operations, pipelines, warehouses, and analytics.
- Use `core-engineering-pack` references for requirements, architecture, system design, APIs, testing, review, and refactoring.

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

Before finalizing a skill-pack change, verify:

- The `name` field exactly matches the skill folder.
- The `description` is clear, validation-friendly, and starts with `Use when`.
- All pack sections exist in the correct order.
- Former leaf content lives under `references/`, not as a peer skill.
- Root `skills/` and `.github/skills/` stay synchronized.
- `scripts/validate_hybrid_packs.py` passes.
- `docs/external-skill-research.md` records any newly adopted external pattern.
- `docs/skill-pack-quality-rubric.md` still reflects the current quality gate.
- Choice-among-options content uses a decision matrix, not prose.
- The pack remains focused on routing and synthesis.
- Cross-cutting concerns are referenced only where they affect the skill’s domain.
- Gotchas and anti-patterns are concrete enough to catch production defects.
- Testing expectations include failure paths, not only happy paths.
- Security, performance, and reliability considerations are specific and reviewable.

