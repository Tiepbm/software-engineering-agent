# External Skill Research for CE7 Software Engineering Agent

**Date:** 2026-04-27  
**Purpose:** Capture reusable patterns from sibling workspace projects to improve the CE7 Copilot-first hybrid software-engineering skill packs without copying external skill text verbatim.

## Scope

This research informs:

- `.github/copilot-instructions.md`
- `agents/ce7-software-engineering.agent.md`
- `agents/skill-evaluator.agent.md`
- `skills/*/SKILL.md`
- `skills/*/references/*.md`
- `evals/routing-benchmark.jsonl`
- `scripts/validate_hybrid_packs.py`
- maintenance instructions under `instructions/`

The repository remains original: external projects provide design patterns, evaluation ideas, and structural heuristics; they are not copied as source text into CE7 references.

## Sources Reviewed

| Workspace project | Files / areas inspected | Transferable pattern | Applied in CE7 |
|---|---|---|---|
| `agents` | `README.md`, `docs/plugin-eval.md`, `plugins/plugin-eval`, selected workflow/security/CI skills | Three-layer evaluation, quality dimensions, anti-patterns, badges, progressive disclosure, plugin granularity | `skill-evaluator`, `validate_hybrid_packs.py`, benchmark corpus, pack/reference architecture |
| `agents/plugins/tdd-workflows` | `agents/tdd-orchestrator.md` | Test-first discipline, regression safety nets, mutation/property/contract thinking, TDD governance | Adds expectation that pack changes include routing/eval cases before claiming quality improvement |
| `agents/plugins/git-pr-workflows` | `agents/code-reviewer.md` | Severity-based review, static analysis + manual reasoning, security/performance/config review lenses | Reinforces CE7 review outputs and evaluator risk ranking |
| `agents/plugins/conductor` | `skills/context-driven-development/SKILL.md` | Context as first-class artifact, context → spec → plan → implement flow, artifact synchronization | Informs docs-as-contract and README/instructions synchronization rules |
| `agents/plugins/cicd-automation` | `skills/deployment-pipeline-design/SKILL.md` | Input/output sections, rollout strategy matrices, metric gates, rollback planning | Feeds release-quality expectations for `observability-release-pack` |
| `agents/plugins/security-scanning` | `skills/stride-analysis-patterns/SKILL.md` | Systematic threat modeling with explicit threat categories and mitigations | Feeds security evaluation scenarios and `security-access-pack` expectations |
| `claude-skills` | `README.md`, `INSTALLATION.md`, `skill-tester`, `self-eval`, `spec-driven-workflow`, `skill-security-auditor`, engineering skill catalog | Multi-tool target layouts, structural validation, scorecards, self-eval anti-inflation, spec-first workflow, skill security audit | `.github/skills` target, validator, scorecard dimensions, escalation and spec-quality expectations |
| `superpowers` | `writing-skills`, `using-superpowers`, `test-driven-development`, `systematic-debugging` | Trigger-only descriptions, skill TDD, pressure scenarios, root-cause-before-fix, evidence-before-claims | `Use when` descriptions, benchmark-first improvement discipline, debug/implementation response expectations |
| `oh-my-openagent` | README orchestration sections, Copilot/rules discovery tests | Copilot `.github/copilot-instructions.md` discovery, rules injection, context-lean background/specialist routing | Copilot-first target, `.github/agents`, `.github/skills`, pack-first routing |
| `claude-mem` | README progressive disclosure and memory search workflow | Multi-layer retrieval: compact index → contextual timeline → full details only when selected | Pack → reference progressive disclosure and token-budget rules |
| `caveman` | `SKILL.md`, `caveman-review/SKILL.md`, `caveman-compress/SKILL.md`, `evals/README.md`, `hooks/` | Output compression rules (drop filler/hedging/pleasantries), intensity levels (lite/full/ultra), auto-clarity (verbose for critical content), terse review format (1-line per finding), 3-arm eval harness (baseline vs terse vs skill), multi-agent distribution via `npx skills` | Output Compression + Auto-Verbose in agent, Verbosity Levels (Quick/Standard/Deep), Terse Review Format in `code-review-and-refactoring.md`, future: compress tool for memory files |

## Adopted Design Principles

### 1. Trigger-first discovery

Pack frontmatter must answer: “Should Copilot load this pack for this task?” It should not summarize the full workflow. This reduces accidental activation and prevents Copilot from treating metadata as a substitute for the skill body.

**CE7 rule:** all pack descriptions start with `Use when` and describe task triggers, not implementation steps.

### 2. Pack-first, reference-second progressive disclosure

The pack skill is the compact routing layer. Former leaf skills are full reference material. This mirrors progressive disclosure from plugin systems and layered memory retrieval.

**CE7 rule:** load one pack by default, then only exact references needed for the task. Loading more than three references requires an explicit reason.

### 3. Evidence before claims

Debugging, performance, migration, release, and security recommendations must be grounded in evidence: reproduction, baseline, traces/logs/metrics, execution plan, threat model, or rollback gate.

**CE7 rule:** output shapes must include validation evidence, not only recommended actions.

### 4. Skill changes need tests

A skill pack improvement is not complete because the prose sounds better. It needs pressure prompts and a validator or benchmark row that would catch regressions.

**CE7 rule:** meaningful pack changes should update `evals/routing-benchmark.jsonl` or explain why existing prompts already cover the change.

### 5. Separate static checks from semantic judgment

Static validators catch structure and dead links quickly. Semantic evaluation catches trigger ambiguity, scope overlap, and answer quality.

**CE7 rule:** `validate_hybrid_packs.py` handles deterministic checks; `skill-evaluator` handles qualitative review.

### 6. Security-sensitive skills require abuse cases

Security guidance must consider identity spoofing, tampering, repudiation, information disclosure, denial of service, and privilege escalation where relevant.

**CE7 rule:** `security-access-pack` evaluations should ask whether threat categories and mitigations are explicit enough for the risk class.

### 7. Release guidance requires operational gates

Release advice is weak without metrics, smoke tests, rollback/roll-forward paths, owners, and environment gates.

**CE7 rule:** `observability-release-pack` should require rollout gates and post-deploy verification for production-impacting work.

### 8. Context is a maintained artifact

Agent behavior degrades when README, instructions, packs, `.github` mirrors, and evals drift apart.

**CE7 rule:** repository updates must keep docs, instructions, `.github` mirrors, root skills, and validator expectations synchronized.

### 9. Compress output, not substance (from caveman)

Output tokens can be reduced ~30-40% by dropping filler, hedging, and pleasantries without losing technical accuracy. Lead with decision, use tables over prose, code blocks over descriptions.

**CE7 rule:** agent has explicit Output Compression rules. Pattern: `[decision]. [reasoning]. [next step].` Drop filler/hedging/pleasantries. Tables for comparisons.

### 10. Auto-verbose for critical content (from caveman)

Compression must never hide security warnings, irreversible actions, compliance implications, or rollback decisions. Agent must automatically switch to full prose for these.

**CE7 rule:** agent has Auto-Verbose section listing 6 conditions that override compression. Resume compressed style after critical section.

### 11. User-controlled output depth (from caveman)

Different questions need different output lengths. A lookup question should not produce an 800-word analysis.

**CE7 rule:** agent supports Quick/Standard/Deep verbosity levels. Auto-detected from risk class and question scope. User can override.

## Rejected / Deferred Patterns

| Pattern | Decision | Reason |
|---|---|---|
| Importing full external skills into CE7 references | Rejected | Would bloat token usage and blur ownership/originality. |
| Adding many specialist agents now | Deferred | User explicitly chose only `skill-evaluator` before benchmark evidence. |
| Full marketplace/plugin packaging | Deferred | Current phase is Copilot-first, not Claude marketplace-first. |
| Heavy runtime dependencies for validation | Rejected for now | Validator should stay stdlib-only and fast. |
| Auto-running LLM Monte Carlo evaluation | Deferred | Valuable later, but current workflow needs deterministic local checks first. |

## Improvement Backlog

| Priority | Improvement | Target |
|---|---|---|
| P1 | Add pack-level scorecard reports generated from benchmark results | `reports/` or `evals/` |
| P1 | Expand benchmark prompts to include should-not-trigger cases per pack pair | `evals/routing-benchmark.jsonl` |
| P1 | Add dead cross-reference scan for `references/*.md` links | `scripts/validate_hybrid_packs.py` |
| P2 | Add security-abuse prompt set for regulated domains | `evals/security-abuse-benchmark.jsonl` |
| P2 | Add release/migration operational-gate prompt set | `evals/release-risk-benchmark.jsonl` |
| P2 | Add score history to detect self-eval inflation over time | `reports/skill-eval-history.jsonl` |
| P3 | Consider `architecture-reviewer` only if routing benchmark shows repeated architecture quality misses | `agents/` |
| P3 | Consider `delivery-risk-reviewer` only if release/migration prompts fail repeatedly | `agents/` |

## Originality Notes

- External project content was used as inspiration for structure and quality criteria only.
- CE7 pack text and evaluator rules are synthesized for this project’s enterprise/regulated software-engineering scope.
- Former CE7 leaf skills remain the authoritative detailed domain references.
- Future changes should cite source projects in this file when they adopt a new pattern.

