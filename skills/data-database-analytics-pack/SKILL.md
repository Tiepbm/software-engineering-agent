---
name: data-database-analytics-pack
description: 'Use when modeling domain data, selecting databases, optimizing SQL/ORM queries, operating production databases, building pipelines, or designing analytics and warehouse consumption paths.'
---
# Data, Database, and Analytics Pack

## Description
This is a Copilot-first hybrid pack skill for data modeling, database architecture, SQL/query optimization, database operations, data pipelines, analytics, and warehouse design. It is intentionally a routing and synthesis layer. Load only the referenced leaf document needed for the specific subdomain instead of expanding every topic by default.

## Purpose
- Provide one high-signal activation surface for a related engineering domain.
- Keep token usage low by using this pack as the default context and loading `references/*.md` only when the task requires deeper guidance.
- Preserve principal-level enterprise guidance from the previous leaf skills without keeping 33 peer skills in the Copilot skill namespace.

## When to Use
- Entities, aggregates, transactional boundaries, history, auditability, or reporting implications.
- Database family selection, source-of-truth choices, indexing, partitioning, scaling, or retention.
- Query plans, ORM-generated SQL, locks, pagination, replication, failover, backup, restore, or migrations.
- ETL/ELT/CDC, streaming, replay, backfill, data quality, marts, metrics, semantic layers, or BI cost controls.

## Pack Reference Map
- `references/data-modeling.md` — `data-modeling`
- `references/database-architecture.md` — `database-architecture`
- `references/sql-and-query-optimization.md` — `sql-and-query-optimization`
- `references/database-reliability-and-operations.md` — `database-reliability-and-operations`
- `references/data-engineering-and-pipelines.md` — `data-engineering-and-pipelines`
- `references/analytics-and-warehouse-design.md` — `analytics-and-warehouse-design`

## Routing Rules
- Start with this pack's summary guidance for broad or ambiguous requests.
- Read a reference file only when its subdomain affects the recommendation, implementation, review, or validation plan.
- If more than three references appear necessary, state the primary reference first and summarize why each additional reference is required.
- For cross-domain work, combine this pack with the adjacent pack named by `ce7-software-engineering.agent.md` instead of copying unrelated guidance here.

## Reference Selection Matrix
| Reference | Selection rule |
|---|---|
| `data-modeling` | Read `references/data-modeling.md` when this exact subdomain is material to the answer. |
| `database-architecture` | Read `references/database-architecture.md` when this exact subdomain is material to the answer. |
| `sql-and-query-optimization` | Read `references/sql-and-query-optimization.md` when this exact subdomain is material to the answer. |
| `database-reliability-and-operations` | Read `references/database-reliability-and-operations.md` when this exact subdomain is material to the answer. |
| `data-engineering-and-pipelines` | Read `references/data-engineering-and-pipelines.md` when this exact subdomain is material to the answer. |
| `analytics-and-warehouse-design` | Read `references/analytics-and-warehouse-design.md` when this exact subdomain is material to the answer. |

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
