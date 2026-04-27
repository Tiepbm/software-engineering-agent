# CE7 Reports Contract

[English](README.md) | [Tiếng Việt](README.vi-VN.md)

## What `reports/` owns

`reports/` keeps only the highest-signal cross-run artifacts:

- `latest-skill-eval.md` → latest English run snapshot.
- `latest-skill-eval.vi-VN.md` → latest Vietnamese run snapshot.
- `skill-eval-history.jsonl` → append-only machine-readable history with **one JSON object per run**.

Detailed prompt evidence does **not** belong here. Keep it under `runs/<run_id>/`.

## What stays under `runs/<run_id>/`

Per-run artifacts remain local to the run folder:

- `manifest.json`
- `report.json`
- `summary.md`
- `scores.json`
- `scores.jsonl`
- `evaluator-prompts/`
- raw `outputs/`

## Why this split exists

This keeps `reports/` useful for regression tracking without turning it into a noisy duplicate of `runs/`.

Good:

- one line per run in history;
- short latest snapshot;
- links back to the full run artifacts.

Avoid:

- appending per-prompt rows to global history;
- copying full prompt findings into `latest-skill-eval*`;
- storing full model outputs in `reports/`.

## `skill-eval-history.jsonl` schema

Each line should be a run-level JSON object with at least:

- `timestamp`
- `run_id`
- `benchmark`
- `outputs_scored`
- `models`
- `semantic_status`
- `deterministic.average_score`
- `deterministic.pass`
- `deterministic.warn`
- `deterministic.fail`
- `per_model`
- `issue_counts`
- `hotspots`
- `lowest_scoring_cases`
- `likely_update_targets`
- `artifacts`

## Standard update flow

```bash
python3 scripts/benchmark_pipeline.py score \
  --run-id <run-id> \
  --append-history
```

That command should:

1. write run-local `report.json` and `summary.md`;
2. overwrite `latest-skill-eval.md` and `latest-skill-eval.vi-VN.md`;
3. append one JSON row to `skill-eval-history.jsonl`.

## Reading order

- Need execution steps: `docs/pipeline-guide.md`
- Need scoring and improvement policy: `docs/evaluation-improvement-playbook.md`
- Need quick commands only: `evals/file-based-benchmark-pipeline.md`

