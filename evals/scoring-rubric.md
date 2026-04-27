# CE7 Benchmark Scoring Rubric

Use this rubric when scoring benchmark outputs from `ce7-software-engineering` and `skill-evaluator`.

## Per-Prompt Scores

Score each prompt from 0 to 5 on every dimension.

| Dimension | Weight | 5 means | 3 means | 1 means |
|---|---:|---|---|---|
| Trigger accuracy | 20% | Correct pack(s), no unnecessary packs | Mostly correct but one ambiguous route | Wrong pack or missed required pack |
| Reference precision | 15% | Opens only needed references | Opens one extra or misses minor reference | Opens many extras or misses core reference |
| Output quality | 20% | Principal-grade, specific, actionable | Useful but generic in places | Vague or not actionable |
| Evidence / validation | 15% | Requires tests, metrics, logs, plans, or threat model as appropriate | Mentions validation but not concrete | No evidence requirement |
| Production safety | 10% | Covers security/data/release/ops risks when relevant | Covers some risks | Misses critical production risk |
| Token efficiency | 10% | Concise synthesis, no pasted references | Slightly verbose | Bloated or repeats reference text |
| Copilot readiness | 5% | Works naturally with `.github` pack/reference layout | Minor friction | Assumes wrong runtime/layout |
| Maintainability/originality | 5% | CE7-specific, no copied external text, easy to maintain | Some generic phrasing | Duplicative, copied, or hard to evolve |

## Weighted Score

```text
weighted_score = Σ(score_0_to_5 × weight) × 20
```

## Verdict

| Weighted score | Verdict |
|---:|---|
| 90–100 | PASS — excellent |
| 80–89 | PASS — production-ready |
| 70–79 | WARN — usable, improve next |
| 60–69 | WARN — risky, prioritize fixes |
| <60 | FAIL — do not rely on this behavior |

## Token Notes

Record these alongside the score:

- Packs activated: `n`
- References activated: `n`
- Unexpected packs: list
- Unexpected references: list
- Missing packs/references: list
- Answer length: short / medium / long / bloated
- Evidence included: yes / partial / no

## Regression Rule

If a prompt previously scored ≥80 and now scores <80, treat it as a regression even if the average package score remains acceptable.

## Banking / Non-Life Insurance Benchmark Notes

For `evals/banking-insurance-benchmark.jsonl`, raise expectations for regulated workflows:

- Banking prompts involving money movement must address idempotency, duplicate prevention, reconciliation, audit evidence, and operator repair.
- Core banking or ledger migration prompts must include expand-contract migration, reconciliation queries, restore/rollback or roll-forward, and regulator-safe reporting.
- Non-life insurance claim prompts must include state transitions, document retention, role-based access, fraud/assessment paths, payment integration, and appeal/failure paths.
- Bancassurance prompts must define bank/insurer integration boundaries, consent, data sharing, payment/policy issuance consistency, refund/cancellation state, and partner outage behavior.
- Customer 360/search prompts must not treat search indexes as source of truth and must include field/document-level authorization, masking, audit, deletion/correction, and index lag monitoring.

Penalize outputs that are technically plausible but ignore regulated-domain correctness, auditability, support operations, or downstream reporting.

