# GPT / Claude Comparison Runbook for Banking & Non-Life Insurance Benchmark

[English](model-comparison-runbook.md) | [Tiếng Việt](model-comparison-runbook.vi-VN.md)

> **You are here.** This is the **benchmark-specific** runbook for `evals/banking-insurance-benchmark.jsonl`.
>
> - If you need the generic pipeline guide: see `docs/pipeline-guide.md`.
> - If you only need quick commands: see `evals/file-based-benchmark-pipeline.md`.
> - If you need fix-target guidance: see `docs/evaluation-improvement-playbook.md`.

Use this runbook to compare GPT and Claude on the 10 realistic cases in `evals/banking-insurance-benchmark.jsonl`.

## 1. Goal

Compare the models on four questions:

1. Do they select the right packs/references?
2. Do they produce principal-grade guidance for banking / non-life insurance tasks?
3. Do they cover production safety: security, data correctness, audit, observability, release, rollback?
4. Do they stay token-efficient without over-activating packs/references or rambling?

## 2. Minimum prep

Read:

- `evals/banking-insurance-benchmark.jsonl`
- `evals/scoring-rubric.md`
- `evals/scoring-rubric.vi-VN.md`

If you run through the file-based pipeline, also use:

- `docs/pipeline-guide.md`
- `scripts/benchmark_pipeline.py`

## 3. Standard prompt wrapper

Use the same wrapper for both GPT and Claude:

```text
Act as CE7 Software Engineering Agent.
Use the Copilot-first hybrid pack architecture.
Before answering, state:
- Packs selected
- References selected
- Why these packs/references are sufficient
Do not load more than 3 references unless required by production risk.
Then answer the business prompt with principal-level engineering guidance.

Business prompt:
<PASTE_PROMPT_HERE>
```

## 4. How to run each case

For each row in `evals/banking-insurance-benchmark.jsonl`:

1. take the `prompt` field;
2. run the same wrapper on GPT and Claude;
3. record actual packs/references;
4. compare against `expected_packs`, `expected_references`, and `should_not_activate`;
5. score the result with the rubric;
6. save the result to report/history or into `runs/<run_id>/...` if using the file pipeline.

## 5. Per-model score sheet

| Field | GPT | Claude |
|---|---|---|
| Prompt ID |  |  |
| Packs selected |  |  |
| References selected |  |  |
| Unexpected packs |  |  |
| Missing packs |  |  |
| Unexpected references |  |  |
| Missing references |  |  |
| Weighted score |  |  |
| Verdict |  |  |
| Token notes |  |  |
| Main strengths |  |  |
| Main weaknesses |  |  |

## 6. What good looks like for this benchmark

A strong answer should:

- state assumptions clearly;
- separate architecture, data, integration, security, observability, testing, and release;
- include failure paths and operator repair paths;
- define audit evidence for regulated workflows;
- include idempotency/reconciliation when money or claims are involved;
- include rollback/roll-forward for migration/release;
- avoid irrelevant stack references;
- avoid generic “use best practices” guidance.

## 7. How to choose the better model

Prefer the model that:

- misses fewer critical risks;
- opens fewer unnecessary packs/references;
- gives more concrete validation evidence;
- handles regulated-domain detail better;
- is shorter while still complete;
- is more consistent across all 10 prompts.

**Do not choose a winner from one prompt.** Use average score plus regression count across the full suite.

## 8. What to do after comparison

- If both models fail the same pattern, update agent/pack/reference guidance.
- If only one model fails, record the trend and observe before editing instructions.
- If the benchmark does not catch a new failure type, add a new benchmark row or extend scoring notes.

