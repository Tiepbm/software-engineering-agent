# Getting Started with CE7 Software Engineering Agent

[English](GETTING-STARTED.md) | [Tiếng Việt](GETTING-STARTED.vi-VN.md)

## What is this?

A principal-level software engineering agent with 7 skill packs covering architecture, data, security, platform integration, resilience, observability, and application stacks. Designed for enterprise and regulated systems (banking, insurance, payments, claims).

## 5-minute setup

1. Clone and open in your IDE workspace.
2. Choose installation mode:
   - **Global** (all projects): `cp -R .github/skills/* ~/.copilot/skills/ && cp agents/*.agent.md ~/.copilot/agents/ && cp .github/copilot-instructions.md ~/.copilot/`
   - **Workspace only**: just open the folder — Copilot reads `.github/` automatically
   - **Add to existing project**: `cp -R .github/ <your-project>/.github/`
3. Verify structure: `python3 scripts/validate_hybrid_packs.py`
4. Start prompting:

```text
Act as CE7 Software Engineering Agent.
Design idempotent payment retries for a multi-tenant mobile flow.
```

## How it works

```text
Your prompt
  → CE7 agent classifies the task (triage)
  → Routes to 1-2 pack skills
  → Loads specific references only when needed
  → Produces principal-grade output with:
      decision, assumptions, trade-offs, rejected options,
      tests, operational controls, and open questions
```

## What you get

| Pack | Covers |
|---|---|
| `core-engineering-pack` | Requirements, architecture, APIs, testing, code review, AWS cloud architecture |
| `data-database-analytics-pack` | Data models, databases, SQL, pipelines, analytics |
| `security-access-pack` | Security review, auth, secrets, tenant isolation |
| `platform-integration-pack` | Messaging, gateways, rate limits, workflows, jobs |
| `resilience-performance-pack` | Resilience, caching, performance, cost/FinOps |
| `observability-release-pack` | Telemetry, SLOs, CI/CD, rollout, rollback, incident response |
| `storage-search-pack` | Object storage, signed URLs, search/indexing |
| `application-stacks-pack` | .NET, Spring Boot, React, Angular, React Native |

## Reading order

| You want to... | Read this |
|---|---|
| Understand the project | `README.md` |
| Start using the agent | This file |
| See quality scores | `REVIEW.md` |
| Run benchmarks | `evals/file-based-benchmark-pipeline.md` |
| Understand the eval pipeline | `docs/pipeline-guide.md` |
| Know when/how to improve skills | `docs/evaluation-improvement-playbook.md` |
| Maintain agent/skills | `instructions/principal-agent-maintenance.instructions.md` |

## Quick prompt examples

- "Design a claims processing workflow with state transitions, audit trail, and compensation."
- "Review this PR for migration and rollback risk before canary release."
- "Diagnose high p95 latency after introducing Redis cache and async workers."
- "Propose API + data model for policy renewal with idempotency and reconciliation."

## Key design principles

- **Pack-first routing**: load one pack, then only the exact references needed.
- **Token efficiency**: never paste full references; synthesize and point.
- **Evidence before claims**: recommendations include validation steps.
- **Enterprise posture**: data correctness, auditability, security, and operability are first-class.
- **Progressive disclosure**: packs are routing layers; depth lives in `references/*.md`.

## When to use this agent

This agent is a **principal-level engineering panel**, not a coding assistant. It adds the most value when you need architectural decisions, trade-off analysis, and production-safety guidance.

### Best for (agent adds significant value)

| Question type | Example |
|---|---|
| System design | "Design payment idempotency for mobile banking" |
| Database selection | "PostgreSQL or MongoDB for claims system?" |
| Architecture review | "Review this PR for migration and rollback risk" |
| Security review | "Review this endpoint for tenant isolation" |
| Data modeling | "Design SCD Type 2 for policy versioning" |
| DevOps / release | "Plan canary rollout with SLO gates" |
| Performance diagnosis | "Diagnose high p95 latency after adding Redis cache" |
| Integration design | "Design outbox pattern for payment events" |

### OK for (agent helps with patterns, not full code)

| Question type | What you get |
|---|---|
| "Write outbox pattern in Spring Boot" | Code pattern from reference + architectural context |
| "Implement idempotency middleware in .NET" | Code example + production checklist |
| "Setup TanStack Query with auth refresh" | Code pattern + security considerations |
| "Fix N+1 query in JPA" | EXPLAIN walkthrough + index recommendation |

### Not designed for (use the model directly)

| Question type | Why |
|---|---|
| "Write a sort function" | Basic coding — model already knows, agent adds no value |
| "Debug CSS layout" | Frontend layout is outside agent scope |
| "Convert Python to Go" | Language translation — no reference coverage |
| "Explain async/await for beginners" | Tutorial content — agent is for decisions, not teaching |

### Recommended workflow

For implementation tasks, combine the agent with direct model usage:

1. **Ask CE7**: "What pattern should I use for payment retry?" → Get architecture decision + trade-offs + checklist
2. **Ask model directly**: "Implement that pattern in Spring Boot" → Get working code
3. **Ask CE7**: "Review this implementation for production risks" → Get security/ops/data review
