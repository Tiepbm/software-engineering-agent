# CE7 Skill Pack Quality Rubric

Use this rubric when improving or reviewing the 7 Copilot-first hybrid pack skills.

## Score Scale

| Score | Meaning |
|---:|---|
| 5 | Excellent; production-ready and benchmark-backed. |
| 4 | Strong; minor gaps or missing edge-case coverage. |
| 3 | Adequate; usable but needs clearer triggers, validation, or boundaries. |
| 2 | Weak; likely to misroute or produce generic guidance. |
| 1 | Poor; structurally incomplete or unsafe for production guidance. |
| 0 | Missing or invalid. |

## Dimensions

| Dimension | Excellent looks like | Common failure |
|---|---|---|
| Trigger accuracy | Description starts with `Use when`, names concrete symptoms/tasks, and avoids workflow summary. | Generic description causes wrong pack activation. |
| Reference precision | Pack points to exact `references/*.md` files and discourages loading unrelated references. | Pack asks Copilot to load all references by default. |
| Scope calibration | Pack is broad enough to replace peer leaf skills but narrow enough to avoid becoming a general software-engineering bucket. | Multiple packs overlap heavily or one pack absorbs unrelated domains. |
| Progressive disclosure | Pack stays concise; deep guidance lives in references. | Pack becomes a long tutorial duplicating references. |
| Evidence discipline | Debugging, performance, release, migration, security, and data claims require observable evidence. | Recommendations are asserted without reproduction, baseline, logs, metrics, plans, or tests. |
| Spec/test discipline | Requirements and implementation work trace to acceptance criteria and tests. | Code or design proceeds before ambiguity and validation are handled. |
| Security realism | Sensitive changes include abuse cases, authorization boundaries, secrets, audit, and data handling. | Security is reduced to generic validation or dependency advice. |
| Release operability | Production changes include rollout gates, monitoring, rollback/roll-forward, owners, and support path. | Release advice ends at “deploy and monitor.” |
| Token efficiency | Pack normally stays under 220 lines and references are opened selectively. | Pack or answer pastes large reference sections. |
| Benchmark coverage | Meaningful behavior changes add or update benchmark prompts. | Skill changes are prose-only and cannot be regression tested. |
| Originality | External patterns are summarized, adapted, and cited in `external-skill-research.md`. | External skill text is copied or adopted without attribution. |
| Copilot readiness | `.github/copilot-instructions.md`, `.github/skills`, root `skills`, and instructions stay synchronized. | Root and `.github` mirrors drift. |

## Required Review Output

When using `skill-evaluator`, report:

1. Overall verdict: PASS / WARN / FAIL.
2. Score table across the dimensions above.
3. Structural validation results from `scripts/validate_hybrid_packs.py`.
4. Routing and reference-loading risks.
5. Token and duplication risks.
6. External research/originality risks.
7. Required benchmark additions.
8. Risk-ranked fixes.

## Minimum Release Gate

A pack change is ready when:

- `python3 scripts/validate_hybrid_packs.py` passes;
- no pack exceeds the line budget;
- no former leaf skill is reintroduced as a peer skill;
- `.github/skills` mirrors root `skills`;
- relevant benchmark rows exist or a clear reason says existing rows cover the change;
- external inspiration, if any, is recorded in `docs/external-skill-research.md`.

