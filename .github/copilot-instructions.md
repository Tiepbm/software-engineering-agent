# GitHub Copilot Instructions — CE7 Software Engineering Agent

Use this repository as a Copilot-first software-engineering agent package.

## Operating Mode
- Treat `agents/ce7-software-engineering.agent.md` as the principal routing agent.
- Prefer the 7 pack skills in `.github/skills/*/SKILL.md` over the old 33 leaf-skill layout.
- Treat `.github/skills/<pack>/references/*.md` as progressive-disclosure reference material; load only the exact reference needed for the task.
- When a task is high-risk, state the pack and references consulted before giving the recommendation.
- Read `memory/learned-patterns.md` for routing corrections and quality patterns learned from previous interactions.

## Memory and Continuous Improvement
- Before routing, check if `memory/learned-patterns.md` contains a relevant pattern for this type of task.
- After completing a significant response, the user may ask you to log the interaction to `memory/interaction-log.jsonl` for future reference.
- If you notice a routing mistake (wrong pack activated, missing critical reference), suggest adding it to `memory/routing-corrections.jsonl`.
- Do NOT read `memory/interaction-log.jsonl` during normal prompts — it may be large. Only read `memory/learned-patterns.md` (kept short).

## Token Rules
- Do not load multiple packs by default. Start from the pack whose trigger best matches the request.
- Load more than one pack only when the user's task crosses domain boundaries such as security + data migration + release.
- Do not paste reference text verbatim unless the user asks for a template or checklist.
- Prefer concise decisions, explicit assumptions, rejected options, validation steps, and production risks.

## Default Pack Routing
- Requirements, architecture, API, testing, review/refactoring → `core-engineering-pack`.
- Data modeling, database, SQL, DB ops, pipelines, analytics → `data-database-analytics-pack`.
- Security, auth, authorization, secrets, sensitive data → `security-access-pack`.
- Messaging, gateways, rate limits, workflows, jobs, batch → `platform-integration-pack`.
- Resilience, caching, distributed state, performance → `resilience-performance-pack`.
- Logs, metrics, traces, SLOs, runbooks, CI/CD, rollout → `observability-release-pack`.
- File/object storage, search/indexing, .NET, Spring Boot, React, Angular, React Native → `storage-search-stack-pack`.

## Evaluation
Use `agents/skill-evaluator.agent.md` for package quality review, trigger accuracy, overlap, progressive disclosure, and token-budget checks.
