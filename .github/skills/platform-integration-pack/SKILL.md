---
name: platform-integration-pack
description: 'Use when designing messaging, events, gateways, BFFs, partner integrations, rate limits, long-running workflows, background jobs, batch processing, retries, DLQs, or repair paths.'
---
# Platform Integration Pack

## Description
This is a Copilot-first hybrid pack skill for messaging/eventing, gateway and service integration, rate limiting, workflow orchestration, background jobs, and batch processing. It is intentionally a routing and synthesis layer. Load only the referenced leaf document needed for the specific subdomain instead of expanding every topic by default.

## Purpose
- Provide one high-signal activation surface for a related engineering domain.
- Keep token usage low by using this pack as the default context and loading `references/*.md` only when the task requires deeper guidance.
- Preserve principal-level enterprise guidance from the previous leaf skills without keeping 33 peer skills in the Copilot skill namespace.

## When to Use
- Queues, topics, pub/sub, outbox/inbox, ordering, idempotent consumers, retries, DLQs, replay, or poison messages.
- API gateway, BFF, partner integration, protocol transformation, auth propagation, quotas, backpressure, or graceful rejection.
- Long-running workflows, sagas, approvals, compensation, resumability, scheduled workers, chunking, checkpointing, or backfills.

## Pack Reference Map
- `references/messaging-and-eventing.md` — `messaging-and-eventing`
- `references/api-gateway-and-service-integration.md` — `api-gateway-and-service-integration`
- `references/rate-limiting-and-traffic-control.md` — `rate-limiting-and-traffic-control`
- `references/workflow-and-job-orchestration.md` — `workflow-and-job-orchestration`
- `references/background-jobs-and-batch-processing.md` — `background-jobs-and-batch-processing`

## Routing Rules
- Start with this pack's summary guidance for broad or ambiguous requests.
- Read a reference file only when its subdomain affects the recommendation, implementation, review, or validation plan.
- If more than three references appear necessary, state the primary reference first and summarize why each additional reference is required.
- For cross-domain work, combine this pack with the adjacent pack named by `ce7-software-engineering.agent.md` instead of copying unrelated guidance here.

## Reference Selection Matrix
| Reference | Selection rule |
|---|---|
| `messaging-and-eventing` | Read `references/messaging-and-eventing.md` when this exact subdomain is material to the answer. |
| `api-gateway-and-service-integration` | Read `references/api-gateway-and-service-integration.md` when this exact subdomain is material to the answer. |
| `rate-limiting-and-traffic-control` | Read `references/rate-limiting-and-traffic-control.md` when this exact subdomain is material to the answer. |
| `workflow-and-job-orchestration` | Read `references/workflow-and-job-orchestration.md` when this exact subdomain is material to the answer. |
| `background-jobs-and-batch-processing` | Read `references/background-jobs-and-batch-processing.md` when this exact subdomain is material to the answer. |

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
