# File-Based Benchmark Pipeline — Quickstart

[English](file-based-benchmark-pipeline.md) | [Tiếng Việt](file-based-benchmark-pipeline.vi-VN.md)

> **You are here.** This is the **short quickstart** for running the file-based benchmark pipeline.
>
> - Full execution guide: `docs/pipeline-guide.md`
> - Scoring and improvement logic: `docs/evaluation-improvement-playbook.md`
> - Banking/insurance GPT-vs-Claude comparison: `evals/model-comparison-runbook.md`

This pipeline lets AI run and self-evaluate mostly through files instead of manual copying.

## Short flow

```text
benchmark JSONL
→ prepare prompt files
→ run GPT/Claude and save outputs
→ deterministic routing/reference/token scoring
→ generate skill-evaluator prompts
→ skill-evaluator performs semantic scoring
→ save report/history
```

Main script:

```text
scripts/benchmark_pipeline.py
```

## 1. Prepare prompt files

```bash
python3 scripts/validate_hybrid_packs.py

python3 scripts/benchmark_pipeline.py prepare \
  --run-id 2026-04-27-gpt-claude-v1 \
  --models gpt,claude
```

## 2. Run models and save outputs

Read prompts from:

```text
runs/<run_id>/prompts/<model>/<prompt_id>.md
```

Save outputs to:

```text
runs/<run_id>/outputs/<model>/<prompt_id>.md
```

Recommended output header:

```markdown
- Packs selected: core-engineering-pack, platform-integration-pack
- References selected: api-design, messaging-and-eventing
- Why these packs/references are sufficient: ...
```

## 3. Run deterministic scoring

```bash
python3 scripts/benchmark_pipeline.py score \
  --run-id 2026-04-27-gpt-claude-v1 \
  --append-history
```

Main artifacts:

```text
runs/<run_id>/report.json
runs/<run_id>/scores.json
runs/<run_id>/scores.jsonl
runs/<run_id>/summary.md
reports/latest-skill-eval.md
reports/latest-skill-eval.vi-VN.md
reports/skill-eval-history.jsonl
```

`reports/skill-eval-history.jsonl` should append **one row per run**, not one row per prompt.

## 4. Generate `skill-evaluator` prompts

```bash
python3 scripts/benchmark_pipeline.py evaluator-prompts \
  --run-id 2026-04-27-gpt-claude-v1
```

Main artifacts:

```text
runs/<run_id>/evaluator-prompts/<model>/<prompt_id>.md
```

## 5. What should you read next?

- Want artifact meanings and data contracts: `docs/pipeline-guide.md`
- Want to decide whether to update agent, pack, or reference: `docs/evaluation-improvement-playbook.md`
- Want detailed scoring criteria: `evals/scoring-rubric.md`

## Optional one-command auto run

```bash
# GPT
export OPENAI_API_KEY="<your_openai_key>"
python3 scripts/benchmark_pipeline.py run --run-id 2026-04-27-gpt-auto --model gpt

# Claude
export ANTHROPIC_API_KEY="<your_anthropic_key>"
python3 scripts/benchmark_pipeline.py run --run-id 2026-04-27-claude-auto --model claude
```

## Optional no-API manual mode

```bash
python3 scripts/benchmark_pipeline.py implement --run-id 2026-04-27-gpt-claude-manual --models gpt,claude
python3 scripts/benchmark_pipeline.py finalize --run-id 2026-04-27-gpt-claude-manual --models gpt,claude
```

