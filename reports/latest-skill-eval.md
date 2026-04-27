# Latest CE7 Skill Evaluation Snapshot

[English](latest-skill-eval.md) | [Tiếng Việt](latest-skill-eval.vi-VN.md)

> **You are here.** This is the latest **short run-level snapshot** synced into `reports/`.
>
> - Per-prompt details stay under `runs/<run_id>/`.
> - Long-term history stays in `reports/skill-eval-history.jsonl` with **one row per run**.
> - This file does not replace `summary.md`; it only keeps the highest-signal findings.

## Current snapshot

- **Run ID:** `smoke-reports-2`
- **Generated:** 2026-04-27T13:17:57.938237+00:00
- **Benchmark:** `evals/banking-insurance-benchmark.jsonl`
- **Models:** `gpt`
- **Outputs scored:** 2
- **Semantic status:** `pending_skill_evaluator`

## Deterministic scorecard

| Metric | Value |
|---|---:|
| Average deterministic score | 100.0 |
| PASS | 2 |
| WARN | 0 |
| FAIL | 0 |

## Model scorecard

| Model | Outputs | Avg score | PASS | WARN | FAIL | Avg words |
|---|---:|---:|---:|---:|---:|---:|
| gpt | 2 | 100.0 | 2 | 0 | 0 | 136.5 |

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
| gpt | banking-001-payment-idempotency | 100 | PASS | no major deterministic issue |
| gpt | banking-002-loan-origination-underwriting | 100 | PASS | no major deterministic issue |

## Artifacts

- `runs/<run_id>/report.json`: `runs/smoke-reports-2/report.json`
- `runs/<run_id>/summary.md`: `runs/smoke-reports-2/summary.md`
- `runs/<run_id>/scores.jsonl`: `runs/smoke-reports-2/scores.jsonl`
- `runs/<run_id>/evaluator-prompts/`: `runs/smoke-reports-2/evaluator-prompts`
- Global history: `reports/skill-eval-history.jsonl`

## Rules for this report

- Do not duplicate full prompt-level findings here; keep them in `runs/<run_id>/`.
- Treat this as the latest snapshot only; use `skill-eval-history.jsonl` for trends and regression checks.
- After semantic evaluation, add details to run-local artifacts or a semantic artifact instead of bloating this file.

