---
name: security-access-pack
description: 'Use when reviewing attack surfaces or designing authentication, authorization, tenant isolation, identity propagation, secrets, audit controls, abuse cases, or sensitive data handling.'
---
# Security and Access Pack

## Description
This is a Copilot-first hybrid pack skill for security review, authn/authz, tenant isolation, identity propagation, secrets, audit, dependency risk, and abuse-case analysis. It is intentionally a routing and synthesis layer. Load only the referenced leaf document needed for the specific subdomain instead of expanding every topic by default.

## Purpose
- Provide one high-signal activation surface for a related engineering domain.
- Keep token usage low by using this pack as the default context and loading `references/*.md` only when the task requires deeper guidance.
- Preserve principal-level enterprise guidance from the previous leaf skills without keeping 33 peer skills in the Copilot skill namespace.

## When to Use
- Identity, permissions, RBAC/ABAC/ReBAC, resource authorization, tenant isolation, sessions, tokens, or admin access.
- PII, payment/financial data, policy/claim/billing state, secrets, external callbacks, file uploads, or sensitive telemetry.
- Dependency risk, input validation, abuse paths, privilege boundaries, or cross-surface security review.

## Pack Reference Map
- `references/security-review.md` — `security-review`
- `references/authn-authz-and-secrets.md` — `authn-authz-and-secrets`

## Routing Rules
- Start with this pack's summary guidance for broad or ambiguous requests.
- Read a reference file only when its subdomain affects the recommendation, implementation, review, or validation plan.
- If more than three references appear necessary, state the primary reference first and summarize why each additional reference is required.
- For cross-domain work, combine this pack with the adjacent pack named by `ce7-software-engineering.agent.md` instead of copying unrelated guidance here.

## Reference Selection Matrix
| Reference | Selection rule |
|---|---|
| `security-review` | Read `references/security-review.md` when this exact subdomain is material to the answer. |
| `authn-authz-and-secrets` | Read `references/authn-authz-and-secrets.md` when this exact subdomain is material to the answer. |

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
