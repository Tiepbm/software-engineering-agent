# CE7 Agent / Skill Pack Evaluation and Improvement Playbook

[English](evaluation-improvement-playbook.md) | [Tiếng Việt](evaluation-improvement-playbook.vi-VN.md)

> **You are here.** This is the canonical document for **evaluation policy** and **improvement decisions**.
>
> - If you need pipeline commands: see `docs/pipeline-guide.md`.
> - If you only need short commands: see `evals/file-based-benchmark-pipeline.md`.
> - If you want GPT-vs-Claude comparison on banking/insurance cases: see `evals/model-comparison-runbook.md`.

**Goal:** make agent + skill quality review repeatable, decide exactly what to improve, and avoid token bloat.

## 1. Operating principles

CE7 uses a **Copilot-first hybrid pack** design:

- GitHub Copilot sees **8 pack skills** under `.github/skills/*/SKILL.md`.
- The previous 33 leaf skills live under `references/*.md`.
- `ce7-software-engineering` routes pack first, reference second.
- `skill-evaluator` reviews triggers, routing, overlap, token efficiency, output quality, and originality.

The key rule: **do not improve quality by stuffing more text into pack files**. Good improvement usually means:

1. clearer triggers;
2. better routing;
3. better benchmark coverage;
4. more precise reference selection;
5. stronger evidence / testing / operational guidance;
6. fewer tokens for the same outcome.

## 2. Five evaluation layers

### Layer 1 — Structural validation

Run `python3 scripts/validate_hybrid_packs.py` before any review.

If this fails, **do not do semantic review yet**. Fix structure first.

### Layer 2 — Routing benchmark

Use benchmarks to verify correct pack/reference activation and avoid false activation.

### Layer 3 — Semantic answer quality

Let `skill-evaluator` score output for correctness, principal judgment, evidence discipline, production readiness, security/data safety, testability, actionability, and brevity.

### Layer 4 — Token efficiency

Evaluate behavior, not just line count:

- pack activation count;
- reference activation count;
- whether answers paste reference content;
- repeated rules across packs.

### Layer 5 — Regression history

Record runs in:

```text
reports/latest-skill-eval.md
reports/latest-skill-eval.vi-VN.md
reports/skill-eval-history.jsonl
```

The goal is real regression detection, not “this feels better.” Keep global history at **one row per run** and keep prompt-level detail under `runs/<run_id>/`.

## 3. Scorecard and grading

Detailed scoring lives in:

- `evals/scoring-rubric.md`
- `evals/scoring-rubric.vi-VN.md`

Keep these 8 score groups:

- trigger accuracy;
- reference precision;
- output quality;
- evidence / validation quality;
- production safety;
- token efficiency;
- Copilot readiness;
- originality / maintainability.

## 4. How to decide what to update

| Failure pattern | Update target |
|---|---|
| Repeated missing expected pack | `agents/ce7-software-engineering.agent.md` or `.github/copilot-instructions.md` |
| Correct pack but missing reference | `skills/<pack>/SKILL.md` |
| Correct reference but shallow output | `skills/<pack>/references/<reference>.md` |
| Too many packs/references opened | token rules in pack `SKILL.md` or `.github/copilot-instructions.md` |
| GPT and Claude both fail | package instructions are unclear; update agent/skill |
| Only one model fails | record history, observe further before editing instructions |
| Benchmark missed a new failure type | add a benchmark row or update scoring notes |

### Golden rule

**Do not edit a skill because an answer merely sounds suboptimal.**

Only edit when benchmark + score + history show a repeated error or a clear production risk.

## 5. Standard improvement loop

1. run structural validation;
2. run representative benchmark prompts;
3. score deterministic + semantic results;
4. classify failures using the table above;
5. patch only the top 1–2 targets;
6. re-run the failing cases to confirm the regression is fixed.

## 6. How to make skills smarter without spending more tokens

### Good changes

- tighten pack descriptions with more explicit triggers;
- add short decision matrices instead of long prose;
- move deep guidance into `references/` instead of packs;
- add negative activation rules when a pack is over-triggered;
- add benchmark prompts that catch routing or production-risk misses.

### Bad changes

- adding more agents without benchmark evidence;
- copying skills from other projects into CE7;
- pushing all security/performance/ops rules into every pack;
- opening many packs “just to be safe”;
- inflating line count to look more advanced.

## 7. When should you add a new agent?

For now, CE7 should stay with:

- `ce7-software-engineering`
- `skill-evaluator`

Add a new agent only when benchmark history shows a **repeated judgment gap** that pack/reference edits cannot solve cleanly.

## 8. Recommended cadence

### Weekly or after major changes

1. run validator;
2. run benchmark;
3. write the report;
4. append history;
5. patch up to 1–2 targets;
6. re-run failed cases.

### Monthly

1. review `docs/external-skill-research.md`;
2. update `docs/skill-pack-quality-rubric.md` if the quality bar changes;
3. decide whether new benchmark suites or new agents are justified.

## 9. Definition of Done for a pack improvement

A pack improvement is done when:

- validator passes;
- the previous failing benchmark case now passes;
- normal prompts do not require more pack/reference activations;
- `.github/skills` stays in sync with root `skills`;
- affected README/instructions are updated;
- `external-skill-research.md` is updated if a new external pattern was adopted;
- the new report is recorded in `reports/latest-skill-eval.md` / `reports/latest-skill-eval.vi-VN.md`.

## 10. What to read next

- Want to run the pipeline: `docs/pipeline-guide.md`
- Want a quickstart: `evals/file-based-benchmark-pipeline.md`
- Want GPT-vs-Claude comparison: `evals/model-comparison-runbook.md`
- Want the detailed rubric: `evals/scoring-rubric.md`

