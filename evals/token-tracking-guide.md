# Token Tracking Guide

## Purpose

Track token consumption per eval task to:
1. Identify expensive tasks that need optimization
2. Enforce token budgets (see `token-budget.jsonl`)
3. Compute cost-efficiency score: `quality_score / tokens_used`
4. Detect regressions in token efficiency across versions

## How to Track

### In eval responses JSONL

Add these fields to each response line:

```json
{
  "id": "route-001",
  "response": "...",
  "packs_activated": ["core-engineering-pack"],
  "references_activated": ["solution-architecture"],
  "tokens": {
    "input": 8500,
    "output": 650,
    "total": 9150
  },
  "latency_ms": 2300,
  "model": "claude-sonnet-4-20250514"
}
```

### In report JSON

Aggregate metrics:

```json
{
  "token_summary": {
    "total_input": 125000,
    "total_output": 18000,
    "avg_input_per_task": 8333,
    "avg_output_per_task": 1200,
    "max_input_task": "route-007",
    "max_output_task": "route-003",
    "budget_violations": ["route-007 exceeded budget-multi-pack by 3000 tokens"]
  }
}
```

## Budget Enforcement

From `token-budget.jsonl`:

| Scope | Max input | Max output |
|---|---|---|
| Agent-only | 2000 | — |
| Single-pack task | 8000 | 1500 |
| Multi-pack task | 14000 | 3000 |
| Banking/insurance task | 16000 | 3000 |

Tasks exceeding budget by >20% are flagged as WARN.
Tasks exceeding budget by >50% are flagged as FAIL (token efficiency dimension).

## Cost-Efficiency Score

```
efficiency = (weighted_score / 100) / (total_tokens / budget_tokens)
```

- efficiency > 1.0 = good (high quality, within budget)
- efficiency 0.7-1.0 = acceptable
- efficiency < 0.7 = needs optimization (verbose output or unnecessary pack activation)

## Integration with `benchmark_pipeline.py`

```python
# After scoring, compute token metrics
for result in results:
    budget = get_budget_for_scope(result["packs_activated"])
    result["token_efficiency"] = compute_efficiency(result["weighted_score"], result["tokens"]["total"], budget)
    if result["tokens"]["total"] > budget * 1.5:
        result["token_verdict"] = "FAIL"
    elif result["tokens"]["total"] > budget * 1.2:
        result["token_verdict"] = "WARN"
    else:
        result["token_verdict"] = "PASS"
```

## Reporting

Add to `reports/latest-skill-eval.md`:

```markdown
## Token Efficiency

| Metric | Value |
|---|---|
| Avg tokens/task | 9,150 |
| Budget violations | 1/10 |
| Cost-efficiency score | 0.92 |
| Most expensive task | route-007 (14,200 tokens) |
| Most efficient task | route-002 (3,100 tokens, score 95) |
```
