# Documentation Index

[English](README.md) | [Tiếng Việt](README.vi-VN.md)

This folder is grouped by **audience**, not by document type. Pick the row that matches who you are.

## User (you want to use the agent)

| Doc | Purpose |
|---|---|
| [`GETTING-STARTED.md`](GETTING-STARTED.md) / [`.vi-VN.md`](GETTING-STARTED.vi-VN.md) | 5-minute walkthrough — install, first prompt, what to expect. |
| [`INSTALL.md`](INSTALL.md) / [`.vi-VN.md`](INSTALL.vi-VN.md) | Three install modes (global / workspace / per-project) + post-install checks. |

## Evaluator (you score model outputs)

| Doc | Purpose |
|---|---|
| [`pipeline-guide.md`](pipeline-guide.md) / [`.vi-VN.md`](pipeline-guide.vi-VN.md) | End-to-end benchmark execution (prepare → output → score → evaluator → report). |
| `../evals/scoring-rubric.md` / `.vi-VN.md` | Per-prompt scoring rubric (paired with the pipeline guide). |
| `../evals/file-based-benchmark-pipeline.md` / `.vi-VN.md` | Quickstart commands for the file-based pipeline. |
| `../evals/model-comparison-runbook.md` / `.vi-VN.md` | GPT vs Claude comparison runbook for banking / non-life insurance prompts. |

## Maintainer (you change packs, references, agent, or eval rules)

| Doc | Purpose | Bilingual? |
|---|---|---|
| [`evaluation-improvement-playbook.md`](evaluation-improvement-playbook.md) / [`.vi-VN.md`](evaluation-improvement-playbook.vi-VN.md) | When and how to improve packs/references after a benchmark run. | Yes |
| [`skill-pack-quality-rubric.md`](skill-pack-quality-rubric.md) | CI-relevant quality gates each pack PR must clear. | EN-only |
| [`external-skill-research.md`](external-skill-research.md) | Patterns reviewed from sibling projects + originality notes. | EN-only |

> **Bilingual policy.** User-facing docs (README, GETTING-STARTED, INSTALL) and evaluator artifacts that are paired with execution scripts are kept bilingual (`.md` + `.vi-VN.md`). Maintainer-only docs that drive CI rules or technical research are EN-only to avoid translation drift. The rule lives in `AGENTS.md`.

## Where the rest lives

- `../AGENTS.md` — contributor & maintainer entry point (editing rules, sync workflow, bilingual policy).
- `../instructions/` — instruction files inherited by packs and the principal agent.
- `../reports/` — run-level reports and history (e.g. `latest-skill-eval.md`, `skill-eval-history.jsonl`).
- `../examples/` — output-shape templates referenced by the agent.

