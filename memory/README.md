# CE7 Agent Memory

This directory stores interaction history that the CE7 agent can reference to improve routing accuracy and output quality over time.

## How it works

1. After each significant interaction, append a privacy-safe summary to `interaction-log.jsonl` manually or via the optional `memory-save` hook
2. Periodically (weekly), review the log and update `learned-patterns.md`
3. The agent reads `learned-patterns.md` via instructions to improve future responses

## Files

| File | Purpose | Updated |
|---|---|---|
| `interaction-log.jsonl` | Raw log of questions, routing decisions, and feedback | After each interaction |
| `learned-patterns.md` | Synthesized patterns from history (top routing rules, common mistakes, domain preferences) | Weekly review |
| `routing-corrections.jsonl` | Cases where routing was wrong and the correct routing | When errors found |

## Schema: interaction-log.jsonl

```json
{
  "timestamp": "2026-04-28T10:00:00Z",
  "prompt_summary": "Design payment idempotency for mobile banking",
  "domain": "banking",
  "risk_class": "production-critical",
  "packs_activated": ["core-engineering-pack", "platform-integration-pack"],
  "references_used": ["api-design", "messaging-and-eventing"],
  "output_quality": "good|acceptable|poor",
  "feedback": "User accepted without changes",
  "routing_correct": true,
  "notes": ""
}
```

## Schema: routing-corrections.jsonl

```json
{
  "timestamp": "2026-04-28T10:00:00Z",
  "prompt_summary": "Review PR for migration risk",
  "expected_packs": ["observability-release-pack", "data-database-analytics-pack"],
  "actual_packs": ["core-engineering-pack"],
  "correction": "Should have routed to devops-and-release + database-reliability-and-operations",
  "root_cause": "Agent treated migration as generic code review instead of release-risk task"
}
```

## How the agent uses this

The agent's instructions reference `memory/learned-patterns.md`. This file is kept short (< 50 lines) and contains only high-signal patterns that materially affect routing or output quality.

The agent does NOT read `interaction-log.jsonl` directly during prompts (too large). Instead, patterns are synthesized into `learned-patterns.md` during periodic review.

Runtime hook entries must remain privacy-safe metadata only: file paths, likely packs/references, active ADR id, handoff status, and coarse quality labels. Do not store prompt bodies, code contents, tool output bodies, secrets, or real customer data.

