# CE7 Software Engineering Agent

Principal-level engineering agent for enterprise and regulated systems, with strong coverage for architecture, data, platform, security, observability, integration, delivery, and production operations.

- Agent file: `agents/ce7-software-engineering.agent.md`
- Review baseline: `REVIEW.md`
- Maintenance rules:
  - `instructions/principal-agent-maintenance.instructions.md`
  - `instructions/principal-skills-maintenance.instructions.md`

## What This Package Includes

```text
ce7-software-engineering/
  agents/
    ce7-software-engineering.agent.md
  skills/
    <33 domain skills>
  instructions/
    principal-agent-maintenance.instructions.md
    principal-skills-maintenance.instructions.md
  REVIEW.md
```

## What The Agent Is Optimized For

- Principal-level decision support, not generic coding chat.
- Enterprise constraints: correctness, auditability, security, operability, delivery safety.
- Regulated workloads: banking, insurance, payments, claims, policy/billing, PII-sensitive systems.
- Cross-functional recommendations with explicit trade-offs and verification steps.

## How The Agent Works

For non-trivial requests, the agent performs mandatory triage:

1. Primary expert role
2. Supporting expert lenses
3. Task type (architecture, implementation/debugging, review/refactoring)
4. Risk class
5. Regulatory sensitivity
6. Missing constraints that could change the recommendation

Then it routes to the right skills and returns a production-oriented answer with assumptions, risks, rejected alternatives, and validation steps.

## Skill Routing Model (High Level)

- Core engineering: `requirements-analysis`, `solution-architecture`, `system-design`, `api-design`, `testing-strategy`, `code-review-and-refactoring`
- Data and database: `data-modeling`, `database-architecture`, `sql-and-query-optimization`, `database-reliability-and-operations`, `data-engineering-and-pipelines`, `analytics-and-warehouse-design`, `search-and-indexing`
- Security and identity: `security-review`, `authn-authz-and-secrets`
- Platform and integration: `messaging-and-eventing`, `api-gateway-and-service-integration`, `workflow-and-job-orchestration`, `background-jobs-and-batch-processing`, `rate-limiting-and-traffic-control`
- Reliability and performance: `resilience-and-fault-tolerance`, `caching-and-distributed-state`, `performance-engineering`
- Observability and operations: `logging-metrics-and-tracing`, `monitoring-alerting-and-slos`, `observability-and-sre`, `devops-and-release`
- Stack-specific: `dotnet-development`, `java-spring-boot-development`, `reactjs-development`, `angular-development`, `react-native-development`

## Expected Output Shapes

- Architecture/analysis: problem -> constraints -> options -> recommendation -> architecture/data/integration/security/ops -> risks -> delivery plan -> validation checklist.
- Implementation/debugging: diagnosis -> likely root cause -> fix -> impact -> tests -> residual risk -> longer-term improvement.
- Review/refactoring: assessment -> strengths -> critical issues -> medium issues -> architecture/data concerns -> refactoring plan -> priority order.

## Production Stop Conditions

The agent will escalate or ask for constraints when key safety conditions are missing, such as:

- Data migration without reconciliation and rollback/roll-forward strategy
- Messaging design without ordering, idempotency, retry, DLQ, replay
- Caching design without staleness/invalidation/authorization safety
- Security-sensitive changes without auth/authz/secrets/audit analysis
- Release plan without sequencing, verification, and rollback strategy
- Performance recommendations without baseline evidence

## Quick Prompt Examples

- "Design idempotent payment retry flow for mobile -> API -> PSP in a multi-tenant system."
- "Review this PR for migration and rollback risk before canary release."
- "Propose API + data model changes for claim status transitions with audit trail."
- "Diagnose high p95 latency after introducing Redis cache and async workers."

## Contributor Notes

When editing this package:

- Keep agent as routing/orchestration panel; do not duplicate skill content.
- Keep skills aligned with required structure and quality floors from instruction files.
- Preserve enterprise/regulated-system posture and production safety rules.
- Re-run package review and update `REVIEW.md` after major changes.

## References

- Agent spec: `agents/ce7-software-engineering.agent.md`
- Quality report: `REVIEW.md`
- Agent maintenance: `instructions/principal-agent-maintenance.instructions.md`
- Skills maintenance: `instructions/principal-skills-maintenance.instructions.md`

