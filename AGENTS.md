# AGENTS.md — Contributor & Maintainer Guide

> Short, opinionated entry point for **humans** editing this repo. For full feature docs see `README.md`. For runtime behaviour see `agents/ce7-software-engineering.agent.md`.

## What this repo is

A Copilot-first principal-engineering agent package:

- **1 router agent** — `agents/ce7-software-engineering.agent.md`. Trim, table-driven, no knowledge dump.
- **8 pack skills** — `skills/<pack>/SKILL.md`. Each one routes to its own deep references.
- **39 references** — `skills/<pack>/references/*.md`. Progressive disclosure; loaded on demand.
- **3 examples** — `examples/`. Output shapes for architecture / debugging / review tasks.
- **2 maintenance instruction files** — `instructions/principal-{agent,skills}-maintenance.instructions.md`.
- **1 shared pack-conventions file** — `instructions/pack-conventions.instructions.md` (single source of truth for pack output style / token rules / quality gates).
- **Eval harness** — `evals/{routing,banking-insurance,anti-pattern}-benchmark.jsonl`, `evals/token-budget.jsonl`, `evals/scoring-rubric.md`.
- **Validator** — `scripts/validate_hybrid_packs.py` (CI-enforceable).

## Repo layout (only what you need to know)

```
agents/                 ce7-software-engineering.agent.md  ← router; KEEP SHORT
                        skill-evaluator.agent.md           ← package self-evaluator
skills/<pack>/SKILL.md  ← 8 packs; ≤ 100 lines each (CI-enforced)
skills/<pack>/references/*.md  ← 36 deep playbooks
instructions/           pack-conventions.instructions.md         ← inherited by every pack
                        principal-agent-maintenance.instructions.md
                        principal-skills-maintenance.instructions.md
examples/               architecture-, debugging-, review- shapes
evals/                  routing, anti-pattern, token-budget, banking-insurance, scoring
scripts/validate_hybrid_packs.py
docs/                   pipeline, evaluation playbook, external research, quality rubric
.github/                Copilot mirror (kept in sync with skills/ + agents/)
```

## Editing rules (the short version)

### Pack `SKILL.md` (the trim ones, ≤ 100 lines)

A pack `SKILL.md` MUST contain — in this order — and NOTHING ELSE:

1. Frontmatter with `name` matching folder, `description` starting with `'Use when …'`.
2. `# <Pack Title>`.
3. `## When to Use` (3–6 concrete trigger bullets).
4. `## When NOT to Use` (2–4 anti-triggers pointing at neighbour packs).
5. `## Pack Reference Map` (table; one row per reference; **distinct** `Use when` per row).
6. `## Cross-Pack Handoffs` (`→ <other-pack> for <concern>` bullets).
7. *(Optional)* `## Worked Example` or `## Notes` — only if it removes routing ambiguity.

DO NOT add `Purpose`, `Routing Rules`, `Reference Selection Matrix`, `Expected Output Style`, `Token Efficiency Rules`, or `Quality Gates` sections. Those live in `instructions/pack-conventions.instructions.md`.

### Reference (`references/*.md`)

- Frontmatter (`name`, `description` starting with `'Use when …'`).
- Body in the existing 14-section playbook style; ≤ 250 lines (warn at 220).
- Decision matrices, templates, and worked examples are encouraged. Avoid generic prose.

### Principal agent (`ce7-software-engineering.agent.md`)

- KEEP UNDER ~150 lines. The agent is a router, not a knowledge dump.
- Do NOT inline rules already covered by a pack/reference. If you write > 5 lines that duplicate a pack, replace it with `→ <pack-name>/<reference-name>`.
- Update the `Skill Routing` table and `Production Bar` table when you add/remove a pack or reference; update `Tie-Break Rules` when a new ambiguity is identified.

### Eval files

- `evals/routing-benchmark.jsonl` — every prompt has `expected_packs`, `expected_references`, `should_not_activate`. Negative tests are required.
- `evals/anti-pattern-benchmark.jsonl` — every prompt has `must_not_do` and `must_do`.
- `evals/token-budget.jsonl` — agent + per-pack + multi-pack scenario budgets. Update if you intentionally relax a budget.
- `evals/banking-insurance-benchmark.jsonl` — exactly 10 rows; if you add one, retire one with rationale in the PR.

## Workflow

```bash
# 1. Make your changes in skills/, agents/, instructions/, evals/, examples/, docs/.

# 2. Run the validator before committing.
python3 scripts/validate_hybrid_packs.py

# 3. (When ready) sync the Copilot mirror.
for pack in core-engineering-pack data-database-analytics-pack security-access-pack \
            platform-integration-pack resilience-performance-pack observability-release-pack \
            storage-search-pack application-stacks-pack; do
  cp -R skills/$pack/SKILL.md  .github/skills/$pack/SKILL.md
  cp -R skills/$pack/references .github/skills/$pack/
done
cp agents/*.agent.md .github/agents/

# 4. Run the mirror-aware validator.
CHECK_GITHUB_MIRROR=1 python3 scripts/validate_hybrid_packs.py

# 5. (Optional) re-run benchmarks; see docs/pipeline-guide.md.
```

## Common edits — quick recipes

| You want to… | Touch these files |
|---|---|
| Add a new pack | `skills/<pack>/SKILL.md` + add EXPECTED entry in `scripts/validate_hybrid_packs.py` + agent `Skill Routing` + `instructions/principal-{agent,skills}-maintenance` |
| Add a reference inside an existing pack | new `skills/<pack>/references/<ref>.md` + add row to that pack's `Pack Reference Map` + EXPECTED entry in validator + (optional) routing-benchmark case |
| Change a pack's trigger | update `description`, `When to Use`, and `When NOT to Use` together — they must agree |
| Add a tie-break rule | edit agent `Tie-Break Rules` (one line) + add a `boundary-*` case to `routing-benchmark.jsonl` |
| Add a "must not do" pattern | edit one or more pack `When NOT to Use` + add an `anti-*` case to `anti-pattern-benchmark.jsonl` |
| Trim something bloated | the validator caps pack `SKILL.md` at 100 lines; references warn at 220, fail at 250 |

## Bilingual policy

Two tiers, enforced by review (not by the validator yet):

- **Bilingual (`.md` + `.vi-VN.md`)** — user-facing docs and evaluator artifacts paired with execution scripts: `README`, `docs/README`, `docs/GETTING-STARTED`, `docs/INSTALL`, `docs/pipeline-guide`, `docs/evaluation-improvement-playbook`, `evals/scoring-rubric`, `evals/file-based-benchmark-pipeline`, `evals/model-comparison-runbook`, `evals/manual-evaluation-template`, `reports/README`, `reports/latest-skill-eval`.
- **EN-only** — maintainer-only docs that drive CI rules or technical research and would suffer from translation drift: `docs/skill-pack-quality-rubric.md`, `docs/external-skill-research.md`, `instructions/*.instructions.md`, `agents/*.agent.md`, `examples/*`, `reports/CE7-AGENT-SYSTEM-REVIEW-*.md`, `reports/PLAN-*.md`, `CHANGELOG.md`, `REVIEW.md`, this file.

When in doubt: if the doc is read by a runtime consumer (Copilot, validator, pipeline script) or describes pack/agent internals, keep it EN-only. If it is a human entry point or paired with a script the user runs, keep it bilingual.

## What NOT to do

- Do not paste reference content into the agent or into another pack. Use `→` routing.
- Do not rewrite an `Accepted` ADR — write a successor (see `core-engineering-pack/references/architecture-decision-records.md`).
- Do not add a pack just because a topic feels important. Add a reference inside an existing pack first; only split when the pack outgrows its scope.
- Do not edit `.github/skills/` or `.github/agents/` directly — they are mirrors, regenerated from `skills/` and `agents/`.
- Do not modify `evals/banking-insurance-benchmark.jsonl` row count without explicit rationale; the validator enforces 10.
- Do not commit the validator failing. CI rejects it; humans should too.

## Where to read next

- `README.md` — full project overview, install modes, pipeline.
- `docs/pipeline-guide.md` — end-to-end benchmark execution.
- `docs/evaluation-improvement-playbook.md` — when and how to improve packs.
- `docs/skill-pack-quality-rubric.md` — quality gates a PR must clear.
- `reports/CE7-AGENT-SYSTEM-REVIEW-2026-04-28.md` — the brutal review that drove the current architecture.

