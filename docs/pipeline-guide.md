# CE7 Benchmark and Self-Evaluation Pipeline Guide

[English](pipeline-guide.md) | [Tiếng Việt](pipeline-guide.vi-VN.md)

> **You are here.** This is the **canonical guide** for the file-based pipeline end to end.
>
> - If you only need short commands: see `evals/file-based-benchmark-pipeline.md`.
> - If you need to interpret scores and decide what to update: see `docs/evaluation-improvement-playbook.md`.
> - If you only want GPT-vs-Claude comparison for banking/insurance cases: see `evals/model-comparison-runbook.md`.

## 1. What this document owns

This document only covers **pipeline execution**:

1. which benchmark files feed the pipeline;
2. which script runs at each stage;
3. the `runs/<run_id>/` directory structure;
4. the input/output contract between benchmark, model, scorer, and `skill-evaluator`;
5. which artifacts are created after each step.

This document does **not** repeat:

- evaluation policy or fix-target rules → `docs/evaluation-improvement-playbook.md`;
- benchmark-specific GPT/Claude comparison guidance → `evals/model-comparison-runbook.md`;
- short quickstart commands → `evals/file-based-benchmark-pipeline.md`.

## 2. Standard pipeline flow

```text
benchmark case
→ generate prompt files
→ run GPT / Claude
→ save outputs to files
→ deterministic scoring
→ generate skill-evaluator prompts
→ semantic scoring
→ write report / history
```

## 3. Core components

### Benchmark sources

- `evals/banking-insurance-benchmark.jsonl`
- `evals/routing-benchmark.jsonl`

### Orchestration script

- `scripts/benchmark_pipeline.py`

### Scoring / semantic evaluation

- `evals/scoring-rubric.md`
- `evals/scoring-rubric.vi-VN.md`
- `agents/skill-evaluator.agent.md`

### Validation / reports

- `scripts/validate_hybrid_packs.py`
- `reports/README.md`
- `reports/README.vi-VN.md`
- `reports/latest-skill-eval.md`
- `reports/latest-skill-eval.vi-VN.md`
- `reports/skill-eval-history.jsonl`

## 4. Run directory layout

Example with `run_id = 2026-04-27-gpt-claude-v1`:

```text
runs/2026-04-27-gpt-claude-v1/
  manifest.json
  prompts/
    gpt/
      banking-001-payment-idempotency.md
      ...
    claude/
      banking-001-payment-idempotency.md
      ...
  outputs/
    gpt/
      banking-001-payment-idempotency.md
      ...
    claude/
      banking-001-payment-idempotency.md
      ...
  scores.json
  scores.jsonl
  report.json
  summary.md
  evaluator-prompts/
    gpt/
      banking-001-payment-idempotency.md
      ...
    claude/
      banking-001-payment-idempotency.md
      ...
```

### Artifact meaning

- `manifest.json`: run metadata, benchmark source, model list.
- `prompts/`: CE7-wrapped prompt files for each model.
- `outputs/`: raw model answers.
- `scores.json` and `scores.jsonl`: deterministic scoring results.
- `report.json`: machine-readable run-level scorecard and update-target summary.
- `summary.md`: quick run summary.
- `evaluator-prompts/`: packaged prompts for `skill-evaluator`.

## 5. Standard execution steps

### Step 0 — Validate the package first

```bash
python3 scripts/validate_hybrid_packs.py
```

If this fails, fix structure before benchmarking.

### Step 1 — Generate prompt files

```bash
python3 scripts/benchmark_pipeline.py prepare \
  --run-id 2026-04-27-gpt-claude-v1 \
  --models gpt,claude
```

Purpose: make GPT and Claude consume the same wrapper, the same benchmark row, and the same output contract.

### Optional: one-command auto mode (switch model only)

If you want the script to run prepare -> model calls -> score -> history sync -> evaluator-prompts automatically:

```bash
# GPT
export OPENAI_API_KEY="<your_openai_key>"
python3 scripts/benchmark_pipeline.py run \
  --run-id 2026-04-27-gpt-auto \
  --model gpt

# Claude
export ANTHROPIC_API_KEY="<your_anthropic_key>"
python3 scripts/benchmark_pipeline.py run \
  --run-id 2026-04-27-claude-auto \
  --model claude
```

Notes:

- `--model` selects provider (`gpt` or `claude`).
- `--provider-model` can override the default provider model string.
- `--limit` is useful for smoke runs; `--overwrite` regenerates existing outputs.

### Optional: no API keys (Copilot manual mode)

If you do not have provider API keys, use:

```bash
# Prepare prompts + output stubs + worklist
python3 scripts/benchmark_pipeline.py implement \
  --run-id 2026-04-27-gpt-claude-manual \
  --models gpt,claude

# After you paste outputs into files, finalize scoring and evaluator prompts
python3 scripts/benchmark_pipeline.py finalize \
  --run-id 2026-04-27-gpt-claude-manual \
  --models gpt,claude
```

Manual-mode helper artifacts:

- `runs/<run_id>/manual/README.md`
- `runs/<run_id>/manual/worklist.md`

### Step 2 — Run the model and save outputs

Feed each file in:

```text
runs/<run_id>/prompts/<model>/<prompt_id>.md
```

to the corresponding model and save output to:

```text
runs/<run_id>/outputs/<model>/<prompt_id>.md
```

#### Recommended output header

```markdown
- Packs selected: core-engineering-pack, platform-integration-pack
- References selected: api-design, messaging-and-eventing
- Why these packs/references are sufficient: payment idempotency crosses API, data, messaging, security, and observability boundaries.
```

This header makes deterministic parsing more reliable. Without it, the script falls back to scanning the body and becomes less accurate.

### Step 3 — Run deterministic scoring

```bash
python3 scripts/benchmark_pipeline.py score \
  --run-id 2026-04-27-gpt-claude-v1 \
  --append-history
```

The script scores:

- `expected_packs` vs `actual_packs`;
- `expected_references` vs `actual_references`;
- `should_not_activate` violations;
- answer length;
- approximate token count;
- rough token efficiency.

The script does **not** score deep semantic quality. That belongs to `skill-evaluator`.

### Step 4 — Generate `skill-evaluator` prompts

```bash
python3 scripts/benchmark_pipeline.py evaluator-prompts \
  --run-id 2026-04-27-gpt-claude-v1
```

Each file in `runs/<run_id>/evaluator-prompts/<model>/<prompt_id>.md` contains:

- benchmark expectations;
- deterministic findings;
- raw model output;
- a structured response schema for the evaluator.

### Step 5 — Write report / history

When you run `score --append-history`, the pipeline also updates:

- `reports/latest-skill-eval.md`
- `reports/latest-skill-eval.vi-VN.md`
- `reports/skill-eval-history.jsonl`

Important: `skill-eval-history.jsonl` should store **one JSON row per run**, not per prompt. Prompt-level evidence stays in `runs/<run_id>/`.

## 6. Data contracts across steps

### Benchmark input contract

Each benchmark row should include at least:

- `id`
- `prompt`
- `expected_packs`
- `expected_references`
- `should_not_activate`

`evals/banking-insurance-benchmark.jsonl` also includes domain, risk class, and scoring notes.

### Model output contract

At minimum, outputs should contain:

- selected packs;
- selected references;
- the main answer body.

### Evaluator output contract

At minimum, evaluator outputs should contain:

- verdict;
- scorecard;
- routing findings;
- token findings;
- production-risk findings;
- suggested update targets.

## 7. Token strategy inside the pipeline

The pipeline is intentionally split into two phases.

### Phase 1 — deterministic

Cheap and fast rule-based parsing catches simple routing and activation errors first.

### Phase 2 — semantic

Only after a concrete output exists do we package a prompt for `skill-evaluator`.

### Avoid

- injecting the full `skill-eval-history.jsonl` into evaluator prompts;
- evaluating the full benchmark suite in one prompt;
- pasting full references into prompts.

Only include:

- the current benchmark row;
- the current output;
- the current deterministic findings;
- the current rubric.

## 8. Common operational mistakes

| Problem | Symptom | Fix |
|---|---|---|
| Output saved to the wrong path | `score` cannot find files | verify `runs/<run_id>/outputs/<model>/<prompt_id>.md` |
| Missing packs/references header | parsing becomes unreliable | add the standard header at the top of output |
| Inconsistent `run_id` | artifacts split across folders | keep one `run_id` per run |
| Full history injected into evaluator | prompt bloat | include only the current row and current findings |
| Global reports contain prompt-level noise | `reports/` becomes hard to read | keep detail in `runs/<run_id>/` and append only one run row to history |

## 9. What to read next

- Want a shorter quickstart: `evals/file-based-benchmark-pipeline.md`
- Want GPT-vs-Claude comparison: `evals/model-comparison-runbook.md`
- Want fix-target guidance: `docs/evaluation-improvement-playbook.md`
- Want scoring criteria: `evals/scoring-rubric.md`

