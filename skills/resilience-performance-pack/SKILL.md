---
name: resilience-performance-pack
description: 'Use when improving latency, throughput, resource usage, cache correctness, distributed state, timeouts, retries, circuit breakers, bulkheads, graceful degradation, or failure containment.'
---
# Resilience and Performance Pack

## Description
This is a Copilot-first hybrid pack skill for resilience, fault tolerance, caching, distributed state, performance engineering, profiling, and capacity reasoning. It is intentionally a routing and synthesis layer. Load only the referenced leaf document needed for the specific subdomain instead of expanding every topic by default.

## Purpose
- Provide one high-signal activation surface for a related engineering domain.
- Keep token usage low by using this pack as the default context and loading `references/*.md` only when the task requires deeper guidance.
- Preserve principal-level enterprise guidance from the previous leaf skills without keeping 33 peer skills in the Copilot skill namespace.

## When to Use
- Timeouts, retries, backoff, circuit breakers, bulkheads, failover, degradation, failure testing, or recovery behavior.
- Cache TTLs, invalidation, staleness, distributed locks, sessions, hot keys, stampedes, or cache authorization safety.
- Latency budgets, p95/p99, throughput, profiling evidence, capacity, concurrency, queue lag, rendering cost, or unit economics.

## Pack Reference Map
- `references/resilience-and-fault-tolerance.md` — `resilience-and-fault-tolerance`
- `references/caching-and-distributed-state.md` — `caching-and-distributed-state`
- `references/performance-engineering.md` — `performance-engineering`

## Routing Rules
- Start with this pack's summary guidance for broad or ambiguous requests.
- Read a reference file only when its subdomain affects the recommendation, implementation, review, or validation plan.
- If more than three references appear necessary, state the primary reference first and summarize why each additional reference is required.
- For cross-domain work, combine this pack with the adjacent pack named by `ce7-software-engineering.agent.md` instead of copying unrelated guidance here.

## Reference Selection Matrix
| Reference | Selection rule |
|---|---|
| `resilience-and-fault-tolerance` | Read `references/resilience-and-fault-tolerance.md` when this exact subdomain is material to the answer. |
| `caching-and-distributed-state` | Read `references/caching-and-distributed-state.md` when this exact subdomain is material to the answer. |
| `performance-engineering` | Read `references/performance-engineering.md` when this exact subdomain is material to the answer. |

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
