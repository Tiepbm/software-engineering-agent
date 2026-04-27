# Latest CE7 Skill Evaluation Snapshot

[English](latest-skill-eval.md) | [Tiếng Việt](latest-skill-eval.vi-VN.md)

> **You are here.** This is the latest **short run-level snapshot** synced into `reports/`.
>
> - Per-prompt details stay under `runs/<run_id>/`.
> - Long-term history stays in `reports/skill-eval-history.jsonl` with **one row per run**.
> - This file does not replace `summary.md`; it only keeps the highest-signal findings.

## Current snapshot

- **Run ID:** `2026-04-27-baseline-v1`
- **Generated:** 2026-04-27T15:07:18.188614+00:00
- **Benchmark:** `evals/banking-insurance-benchmark.jsonl`
- **Models:** `gpt`
- **Outputs scored:** 10
- **Semantic status:** `pending_skill_evaluator`

## Deterministic scorecard

| Metric | Value |
|---|---:|
| Average deterministic score | 100.0 |
| PASS | 10 |
| WARN | 0 |
| FAIL | 0 |

## Model scorecard

| Model | Outputs | Avg score | PASS | WARN | FAIL | Avg words |
|---|---:|---:|---:|---:|---:|---:|
| gpt | 10 | 100.0 | 10 | 0 | 0 | 999.7 |

## Highest-signal findings

- Missing expected packs: 0 output(s). Hotspots: -
- Missing expected references: 0 output(s). Hotspots: -
- Unexpected/prohibited activations: 0 output(s). Hotspots: -
- Header/parser confidence issues: scanned=0, missing=0
- Long outputs: 0 | bloated outputs: 0

## Likely update targets

| Target | Why | Evidence |
|---|---|---|
| - | No strong deterministic signal suggests an update yet. | - |

## Lowest-scoring cases

| Model | Prompt | Score | Verdict | Main issue |
|---|---|---:|---|---|
| gpt | insurance-002-policy-endorsement-midterm-adjustment | 100 | PASS | no major deterministic issue |
| gpt | insurance-001-claim-fnol-to-settlement | 100 | PASS | no major deterministic issue |
| gpt | insurance-004-reinsurance-bordereaux-analytics | 100 | PASS | no major deterministic issue |
| gpt | cross-001-bancassurance-quote-bind | 100 | PASS | no major deterministic issue |
| gpt | insurance-003-catastrophe-claims-surge | 100 | PASS | no major deterministic issue |

## Artifacts

- `runs/<run_id>/report.json`: `runs/2026-04-27-baseline-v1/report.json`
- `runs/<run_id>/summary.md`: `runs/2026-04-27-baseline-v1/summary.md`
- `runs/<run_id>/scores.jsonl`: `runs/2026-04-27-baseline-v1/scores.jsonl`
- `runs/<run_id>/evaluator-prompts/`: `runs/2026-04-27-baseline-v1/evaluator-prompts`
- Global history: `reports/skill-eval-history.jsonl`

## Rules for this report

- Do not duplicate full prompt-level findings here; keep them in `runs/<run_id>/`.
- Treat this as the latest snapshot only; use `skill-eval-history.jsonl` for trends and regression checks.
- After semantic evaluation, add details to run-local artifacts or a semantic artifact instead of bloating this file.

