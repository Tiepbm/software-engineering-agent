---
name: observability-release-pack
description: 'Use when designing logs, metrics, traces, SLIs, SLOs, dashboards, alerts, runbooks, production readiness, CI/CD, rollout, feature flags, rollback, or migration release safety.'
---
# Observability and Release Pack

## Description
This is a Copilot-first hybrid pack skill for logging, metrics, tracing, SLOs, alerting, SRE readiness, CI/CD, deployment, release, and rollback safety. It is intentionally a routing and synthesis layer. Load only the referenced leaf document needed for the specific subdomain instead of expanding every topic by default.

## Purpose
- Provide one high-signal activation surface for a related engineering domain.
- Keep token usage low by using this pack as the default context and loading `references/*.md` only when the task requires deeper guidance.
- Preserve principal-level enterprise guidance from the previous leaf skills without keeping 33 peer skills in the Copilot skill namespace.

## When to Use
- Structured logs, metrics, traces, correlation IDs, redaction, telemetry cardinality, or trace propagation.
- SLIs, SLOs, burn-rate alerts, dashboards, severity, ownership, runbooks, incident readiness, or game days.
- CI/CD, environment promotion, config, secrets in pipelines, feature flags, canary/blue-green, migration sequencing, rollback, or release gates.

## Pack Reference Map
- `references/logging-metrics-and-tracing.md` — `logging-metrics-and-tracing`
- `references/monitoring-alerting-and-slos.md` — `monitoring-alerting-and-slos`
- `references/observability-and-sre.md` — `observability-and-sre`
- `references/devops-and-release.md` — `devops-and-release`

## Routing Rules
- Start with this pack's summary guidance for broad or ambiguous requests.
- Read a reference file only when its subdomain affects the recommendation, implementation, review, or validation plan.
- If more than three references appear necessary, state the primary reference first and summarize why each additional reference is required.
- For cross-domain work, combine this pack with the adjacent pack named by `ce7-software-engineering.agent.md` instead of copying unrelated guidance here.

## Reference Selection Matrix
| Reference | Selection rule |
|---|---|
| `logging-metrics-and-tracing` | Read `references/logging-metrics-and-tracing.md` when this exact subdomain is material to the answer. |
| `monitoring-alerting-and-slos` | Read `references/monitoring-alerting-and-slos.md` when this exact subdomain is material to the answer. |
| `observability-and-sre` | Read `references/observability-and-sre.md` when this exact subdomain is material to the answer. |
| `devops-and-release` | Read `references/devops-and-release.md` when this exact subdomain is material to the answer. |

## Expected Output Style
- Start with the decision or finding before the reasoning.
- Name the reference documents consulted when the work is non-trivial.
- Separate immediate action, design trade-offs, tests, operational checks, and follow-up work.
- Keep the answer concrete: include contracts, schemas, rollout gates, checklists, or examples when they reduce ambiguity.

## Token Efficiency Rules
- Do not paste large portions of reference files into the response.
- Prefer a short synthesized rule plus a pointer to the exact reference when more depth is needed.
- Avoid activating unrelated packs just because their concerns are generally useful.
- Treat the pack as metadata + routing; treat `references/` as progressive disclosure.

## Quality Gates
Before finalizing work using this pack, verify:
- The selected references match the user's actual risk and task type.
- Security, data correctness, observability, delivery, and failure behavior are covered when they materially affect production risk.
- Recommendations are testable and include validation evidence.
- Any rejected option includes the reason it was rejected.
