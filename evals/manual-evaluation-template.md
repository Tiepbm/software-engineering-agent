# Manual Semantic Evaluation Template

[English](manual-evaluation-template.md) | [Tiếng Việt](manual-evaluation-template.vi-VN.md)

> **Purpose**: Paste this template into ChatGPT Plus or Copilot Chat to get structured semantic scoring for a CE7 benchmark output. No API keys needed.

## How to use

1. Run `python3 scripts/benchmark_pipeline.py implement --run-id <your-run-id> --models gpt`
2. Open a prompt file from `runs/<run_id>/prompts/gpt/<prompt_id>.md`
3. Paste it into ChatGPT Plus or Copilot Chat
4. Save the model output to `runs/<run_id>/outputs/gpt/<prompt_id>.md`
5. Run `python3 scripts/benchmark_pipeline.py finalize --run-id <your-run-id> --models gpt`
6. For semantic scoring: paste the evaluator prompt (from `runs/<run_id>/evaluator-prompts/gpt/<prompt_id>.md`) into ChatGPT Plus using the template below

## Semantic Evaluation Prompt (paste into ChatGPT Plus)

```
You are a skill evaluator for the CE7 Software Engineering Agent package.

Score this model output on 5 semantic dimensions (0-5 each):

1. **Output Quality** (20%): Is the answer principal-grade, specific, actionable? Does it include decisions, trade-offs, rejected options?
2. **Evidence / Validation** (15%): Does it require tests, metrics, logs, plans, or threat models? Are validation steps concrete?
3. **Production Safety** (10%): Does it cover security, data correctness, release risk, operational controls when relevant?
4. **Copilot Readiness** (5%): Does it work naturally with pack/reference architecture?
5. **Maintainability** (5%): Is guidance CE7-specific, not generic copied text?

Return this JSON:
```json
{
  "prompt_id": "<from evaluator prompt>",
  "model": "gpt",
  "scores": {
    "output_quality": 0,
    "evidence_validation": 0,
    "production_safety": 0,
    "copilot_readiness": 0,
    "maintainability": 0
  },
  "weighted_score": 0,
  "verdict": "PASS|WARN|FAIL",
  "strengths": ["..."],
  "gaps": ["..."],
  "suggested_fixes": ["..."]
}
```

Then provide a 3-sentence explanation.

Here is the evaluator prompt with benchmark expectations and model output:

<PASTE EVALUATOR PROMPT HERE>
```

## Scoring thresholds

| Weighted score | Verdict |
|---:|---|
| 90-100 | PASS — excellent |
| 80-89 | PASS — production-ready |
| 70-79 | WARN — usable, improve next |
| 60-69 | WARN — risky |
| <60 | FAIL |

## After scoring

1. Save the JSON result to `runs/<run_id>/semantic-scores/<model>/<prompt_id>.json`
2. Run `python3 scripts/regression_check.py` to check for regressions
3. If WARN or FAIL: check `docs/evaluation-improvement-playbook.md` section 4 for fix-target guidance

## Budget-friendly evaluation cadence

| Frequency | What to do | Tool | Cost |
|---|---|---|---|
| Every skill change | `python3 scripts/validate_hybrid_packs.py` | Kiro terminal | $0 |
| Weekly | Run 3-5 benchmark prompts in Copilot Chat, score deterministic | Kiro + Copilot | $0 |
| Bi-weekly | Full 10-prompt banking/insurance benchmark, manual semantic eval for lowest 3 | ChatGPT Plus | $0 |
| Monthly | Compare GPT vs Claude on same 5 prompts, update history | ChatGPT + Copilot | $0 |
| After major changes | Full 25-prompt benchmark + semantic eval for all WARN/FAIL | ChatGPT Plus | $0 |
