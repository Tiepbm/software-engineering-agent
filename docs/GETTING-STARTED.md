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
| `core-engineering-pack` | Requirements, architecture, APIs, testing, code review |
| `data-database-analytics-pack` | Data models, databases, SQL, pipelines, analytics |
| `security-access-pack` | Security review, auth, secrets, tenant isolation |
| `platform-integration-pack` | Messaging, gateways, rate limits, workflows, jobs |
| `resilience-performance-pack` | Resilience, caching, performance engineering |
| `observability-release-pack` | Telemetry, SLOs, CI/CD, rollout, rollback |
| `storage-search-stack-pack` | Object storage, search, .NET, Spring Boot, React, Angular, React Native |

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
