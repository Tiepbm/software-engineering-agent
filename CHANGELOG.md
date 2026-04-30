# Changelog

## 2026-04-28 — Caveman-inspired output optimization (P1-P4)

### Added
- **Output Compression rules** (P1) in agent: drop filler/pleasantries/hedging, lead with decision, tables over prose, code blocks over descriptions. Inspired by caveman project's token reduction approach (~30-40% output token savings).
- **Auto-Verbose safety valve** (P3) in agent: 6 conditions where agent must use full prose (security findings, irreversible actions, compliance, rollback decisions, production stops, user confusion). Prevents compression from hiding critical information.
- **Output Verbosity levels** (P2) in agent: Quick (50-150 tokens) / Standard (300-800) / Deep (800-1500). Auto-detected from risk class and question scope. User can override with "/quick" or "/deep".
- **Terse Review Format** (P4) in `code-review-and-refactoring.md`: one-line-per-finding format (`L42: 🔴 bug: user null. Add guard.`) with severity emoji, category, and summary line. For quick reviews and large PRs.
- `docs/PLAN-automatic-memory.md` — plan for MCP-based automatic memory system (Phase 1-4, not yet implemented).

### Changed
- Agent file: 108 → 122 lines (added 4 sections, still well under 150-line budget).
- `docs/external-skill-research.md` updated with caveman project patterns.
- `memory/learned-patterns.md` fixed stale pack name (`storage-search-stack-pack` → `storage-search-pack`).

## 2026-04-28 — P1/P2 follow-ups (3 new references, AGENTS.md, README trim, evaluator scope split)

### Added
- 3 new reference playbooks (33 → 36 references):
  - `core-engineering-pack/references/architecture-decision-records.md` — ADR template, lifecycle, decision-quality checklist, common failure modes.
  - `observability-release-pack/references/incident-response-and-postmortem.md` — severity matrix, IC/Ops/Comms/Scribe roles, mitigation-first discipline, blameless postmortem template, action-item discipline, regulated-domain additions.
  - `resilience-performance-pack/references/cost-and-finops.md` — FinOps loop, unit economics, attribution, pricing models, high-impact cost traps, denial-of-wallet protection, regulated retention rules.
- `AGENTS.md` at repo root — short editing rules and workflow for human contributors.
- `docs/INSTALL.md` — install modes (global / workspace / per-project) extracted from old README.

### Changed
- `README.md` trimmed from 353 → 84 lines (-76%). Install detail moved to `docs/INSTALL.md`. Added documentation map and CI-enforced quality gates summary.
- `scripts/validate_hybrid_packs.py` updated for 36 references and the 3 new reference names.
- 3 pack `SKILL.md` extended with one new row each in their `Pack Reference Map`.
- `agents/skill-evaluator.agent.md` — added scope-split note pointing at `docs/skill-pack-quality-rubric.md` as canonical; eliminates the previous 70 % overlap by making evaluator agent purely interactive and deferring criteria to the rubric.
- `docs/skill-pack-quality-rubric.md` — header updated to mark itself canonical and reference the evaluator agent + scoring-rubric consumers.

### Notes for the maintainer
- `.github/skills/` mirror not yet synced for the 3 new references and the updated 3 pack SKILL.md (per agreed split of responsibility — user syncs `.github/` manually).
- `evals/banking-insurance-benchmark.jsonl` row count unchanged (10); rubric coverage still applies to new references.

## 2026-04-28 — P0 review fixes (agent trim, pack split, pack-trim, evals expansion)

### Changed (BREAKING for runtime layout)
- **Split `storage-search-stack-pack` → `storage-search-pack` + `application-stacks-pack`** (8 packs total). Storage/search infra is now decoupled from framework-specific stacks; routing precision should improve for both axes. Eval files updated; references moved (no content change).
- **Rewrote principal agent** (`agents/ce7-software-engineering.agent.md`) from 320 → ~110 lines (~-60% tokens). Replaced 4 overlapping rule layers (Operating Rules + Default Review Lenses + Cross-Cutting Routing + Stop Conditions + Prohibited Behavior) with a single `Production Bar` table. Added `Tie-Break Rules` for cross-pack ambiguity. Few-shot moved to `examples/`.
- **Trimmed all 8 pack `SKILL.md`** to a uniform short template (frontmatter + `When to Use` + `When NOT to Use` + `Pack Reference Map` + `Cross-Pack Handoffs`). Removed boilerplate sections (`Purpose`, `Routing Rules`, `Reference Selection Matrix`, `Expected Output Style`, `Token Efficiency Rules`, `Quality Gates`) — now owned by the new shared instructions file. Reference selection rules now carry **distinct `Use when` triggers** instead of tautological filler. Estimated ~50% token reduction per pack.
- **Updated `scripts/validate_hybrid_packs.py`** for 8 packs and a 100-line pack budget.
- **Updated `.github/copilot-instructions.md`** and `instructions/principal-{agent,skills}-maintenance.instructions.md` for the new pack layout.

### Added
- `instructions/pack-conventions.instructions.md` — single source of truth for pack output style / token rules / quality gates / structure. Replaces 6 boilerplate sections previously duplicated across 7 packs.
- `examples/architecture-payment-idempotency.md`, `examples/debugging-cache-latency.md`, `examples/review-pr-checklist.md` — three task-type output shapes referenced by the agent.
- `evals/anti-pattern-benchmark.jsonl` — 10 prompts that test what the agent must NOT do (retry without idempotency, cache without invalidation, monitoring without runbook, DB without workload-fit, deploy without rollback, search-as-source-of-truth, async without DLQ, PII in logs, route-level-authz only, perf fix without profile).
- `evals/token-budget.jsonl` — agent and pack token budgets and 1-pack / 3-pack context-load scenarios.
- `evals/routing-benchmark.jsonl` — added 8 boundary cases (outbox, redis-session-vs-store, signed-URL+callback, PII logging, gateway+circuit, CDC pipeline, stack+platform, search projection) and 2 ambiguity cases (must ASK_FOR_CONSTRAINTS instead of activating a pack). Total: 25 cases.
- `reports/CE7-AGENT-SYSTEM-REVIEW-2026-04-28.md` — brutal review report driving these P0 changes.

### Migration notes
- The user will manually sync `.github/skills/` and `.github/agents/` mirrors after this commit.
- `REVIEW.md` self-rating of 9.2 is no longer valid; rerun benchmarks before re-scoring.
- `agents/skill-evaluator.agent.md` and `docs/skill-pack-quality-rubric.md` overlap ~70%; consolidating one is a follow-up (P2, optional later).

## 2026-04-27 — Self-evaluation automation and budget-friendly workflow

### Added
- Added `scripts/regression_check.py` — stdlib-only regression detection comparing latest vs previous runs in history. Flags score drops, new failures, issue count increases, and trend decline.
- Added `evals/manual-evaluation-template.md` and `evals/manual-evaluation-template.vi-VN.md` — structured template for semantic scoring via ChatGPT Plus or Copilot Chat without API keys. Includes budget-friendly evaluation cadence.
- Added `docs/GETTING-STARTED.md` and `docs/GETTING-STARTED.vi-VN.md` — 5-minute entry point for new users.
- Added Documentation Map to README.md and README.vi-VN.md classifying docs by audience (user/evaluator/maintainer).
- Added Kiro hook `validate-skill-changes` — auto-runs `validate_hybrid_packs.py` when skill/agent files are edited.

### Changed
- Updated `REVIEW.md` with P1/P2/P3 content improvements completed (10 reference files enhanced with decision matrices, templates, and worked examples).

## 2026-04-27 — P1/P2/P3 content improvements

### Changed
- `testing-strategy.md`: Added Test Type Decision Matrix (10 test types with selection rules).
- `resilience-and-fault-tolerance.md`: Added Resilience Pattern Decision Matrix (8 patterns) + Timeout Budget Calculation example.
- `caching-and-distributed-state.md`: Added Cache Pattern Decision Matrix (5 patterns) + Redis-Specific Guidance table.
- `monitoring-alerting-and-slos.md`: Added SLI/SLO Definition Template + Burn-Rate Alert Calculation with examples.
- `messaging-and-eventing.md`: Added Transactional Outbox Worked Example (schema, write path, relay, consumer inbox, alternatives, operational controls).
- `devops-and-release.md`: Added Canary Rollout with SLO Gates Worked Example (Argo Rollouts YAML, analysis template, pre/post checklists).
- `observability-and-sre.md`: Added Production Readiness Checklist Template (copy-paste ready with BLOCK/P1 items).
- `logging-metrics-and-tracing.md`: Added Structured Log Field Schema (20 fields) + Metric Naming Convention guide.
- `security-review.md`: Added Cross-Surface Security Review Worked Example (4 paths: request, async, derived-state, operator).
- `database-architecture.md`: Added Workload-Fit Decision Worked Example (Insurance Claims System with access patterns, decision matrix, physical design).

## 2026-04-27 — Reports optimization and run-level scorecards

### Changed
- Reworked `reports/` so global reporting is now run-level instead of noisy prompt-level duplication.
- Updated `scripts/benchmark_pipeline.py` to generate `runs/<run_id>/report.json`, write concise run summaries, and append only one history row per run.
- `score --append-history` now syncs bilingual latest snapshots to `reports/latest-skill-eval.md` and `reports/latest-skill-eval.vi-VN.md`.
- Updated README and evaluation docs to clarify that prompt-level evidence stays under `runs/<run_id>/`.

### Added
- Added `reports/README.md` and `reports/README.vi-VN.md` to define reports ownership and the history schema.
- Added `reports/latest-skill-eval.vi-VN.md` as the Vietnamese counterpart of the latest snapshot.
- Extended `scripts/validate_hybrid_packs.py` to require the new reports artifacts and validate the run-level history schema when present.
- Added `benchmark_pipeline.py run` for one-command end-to-end execution by provider switch (`--model gpt|claude`) with API-based output generation, scoring, history sync, and evaluator prompt generation.
- Added `benchmark_pipeline.py implement` and `benchmark_pipeline.py finalize` for no-API Copilot workflows: prepare prompts/output stubs/worklist first, then finalize scoring/evaluator prompts after manual paste.

## 2026-04-27 — Evaluation docs cleanup and bilingual guide pairs

### Changed
- Reduced overlap across evaluation guidance by assigning clear ownership:
  - `docs/pipeline-guide*` now owns canonical end-to-end pipeline execution.
  - `docs/evaluation-improvement-playbook*` now owns evaluation policy, fix-target logic, and improvement cadence.
  - `evals/file-based-benchmark-pipeline*` is now a short quickstart only.
  - `evals/model-comparison-runbook*` is now benchmark-specific for GPT vs Claude on banking/non-life insurance prompts.

### Added
- Added English counterparts for the evaluation docs:
  - `docs/pipeline-guide.md`
  - `docs/evaluation-improvement-playbook.md`
  - `evals/file-based-benchmark-pipeline.md`
  - `evals/model-comparison-runbook.md`
- Added Vietnamese scoring rubric at `evals/scoring-rubric.vi-VN.md`.
- Extended `scripts/validate_hybrid_packs.py` to require the bilingual evaluation docs.

## 2026-04-26 — Copilot-first hybrid skill packs

### Changed
- Reworked the package to prioritize GitHub Copilot output via `.github/copilot-instructions.md` and `.github/skills/`.
- Replaced 33 peer skills with 7 peer pack skills:
  - `core-engineering-pack`
  - `data-database-analytics-pack`
  - `security-access-pack`
  - `platform-integration-pack`
  - `resilience-performance-pack`
  - `observability-release-pack`
  - `storage-search-stack-pack`
- Preserved the former 33 leaf skills as progressive-disclosure `references/*.md` files under the relevant pack.
- Updated `ce7-software-engineering.agent.md` to route pack-first and reference-second.

### Added
- Added `agents/skill-evaluator.agent.md` for trigger accuracy, reference precision, overlap, token efficiency, and Copilot readiness evaluation.
- Added `.github/agents/` mirrors for the two current agents.
- Added `evals/routing-benchmark.jsonl` with routing and negative-activation benchmark prompts.
- Added `scripts/validate_hybrid_packs.py` to validate the hybrid pack layout.
- Added `docs/external-skill-research.md` to record patterns reviewed from sibling workspace projects (`agents`, `claude-skills`, `superpowers`, `oh-my-openagent`, `claude-mem`).
- Added `docs/skill-pack-quality-rubric.md` to convert those patterns into quality gates for CE7 pack skills.
- Extended validation and evaluator rules to check external research coverage, originality, and pack quality rubric presence.
- Added `docs/evaluation-improvement-playbook.vi-VN.md` with the 5-layer evaluation workflow and token-efficiency improvement loop.
- Added `evals/scoring-rubric.md` plus `reports/latest-skill-eval.md` and `reports/skill-eval-history.jsonl` for repeatable score tracking.
- Added `evals/banking-insurance-benchmark.jsonl` with 10 realistic benchmark prompts for Banking, Non-life Insurance, and Bancassurance.
- Added `evals/model-comparison-runbook.vi-VN.md` to compare GPT and Claude outputs on the same benchmark cases.
- Extended the validator and scoring rubric to recognize the banking/insurance benchmark and regulated-domain scoring expectations.
- Added `scripts/benchmark_pipeline.py` and `evals/file-based-benchmark-pipeline.vi-VN.md` for file-based model output capture, deterministic routing/reference/token scoring, and `skill-evaluator` prompt generation.
- Added `docs/pipeline-guide.vi-VN.md` as the canonical end-to-end pipeline guide.

### Deferred
- `architecture-reviewer` and `delivery-risk-reviewer` are intentionally deferred until benchmark results justify them.

