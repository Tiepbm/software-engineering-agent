---
name: core-engineering-pack
description: 'Use when clarifying requirements, shaping solution architecture, designing system/API boundaries, defining tests, or reviewing/refactoring software for maintainability and delivery risk.'
---
# Core Engineering Pack

## Description
This is a Copilot-first hybrid pack skill for requirements, solution architecture, system design, API design, testing strategy, code review, and safe refactoring. It is intentionally a routing and synthesis layer. Load only the referenced leaf document needed for the specific subdomain instead of expanding every topic by default.

## Purpose
- Provide one high-signal activation surface for a related engineering domain.
- Keep token usage low by using this pack as the default context and loading `references/*.md` only when the task requires deeper guidance.
- Preserve principal-level enterprise guidance from the previous leaf skills without keeping 33 peer skills in the Copilot skill namespace.

## When to Use
- Ambiguous scope, business rules, actors, acceptance criteria, or measurable outcomes.
- Architecture shape, service boundaries, sync/async decisions, ownership, or delivery complexity.
- API contracts, idempotency, pagination, validation, versioning, or integration usability.
- Risk-based test strategy, contract/E2E scope, or safe refactoring/review order.

## Pack Reference Map
- `references/requirements-analysis.md` — `requirements-analysis`
- `references/solution-architecture.md` — `solution-architecture`
- `references/system-design.md` — `system-design`
- `references/api-design.md` — `api-design`
- `references/testing-strategy.md` — `testing-strategy`
- `references/code-review-and-refactoring.md` — `code-review-and-refactoring`

## Routing Rules
- Start with this pack's summary guidance for broad or ambiguous requests.
- Read a reference file only when its subdomain affects the recommendation, implementation, review, or validation plan.
- If more than three references appear necessary, state the primary reference first and summarize why each additional reference is required.
- For cross-domain work, combine this pack with the adjacent pack named by `ce7-software-engineering.agent.md` instead of copying unrelated guidance here.

## Reference Selection Matrix
| Reference | Selection rule |
|---|---|
| `requirements-analysis` | Read `references/requirements-analysis.md` when this exact subdomain is material to the answer. |
| `solution-architecture` | Read `references/solution-architecture.md` when this exact subdomain is material to the answer. |
| `system-design` | Read `references/system-design.md` when this exact subdomain is material to the answer. |
| `api-design` | Read `references/api-design.md` when this exact subdomain is material to the answer. |
| `testing-strategy` | Read `references/testing-strategy.md` when this exact subdomain is material to the answer. |
| `code-review-and-refactoring` | Read `references/code-review-and-refactoring.md` when this exact subdomain is material to the answer. |

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
