---
name: architecture-decision-records
description: 'Use when capturing an architectural decision, its alternatives, trade-offs, and the consequences future readers (and your future self) need to understand without rerunning the analysis.'
---

# Architecture Decision Records (ADRs)

## Description

An ADR captures a single significant architectural decision: the context that forced it, the options considered, the choice made, and the consequences. ADRs are immutable; they are not design docs and not roadmaps. They exist so that 6 months from now no one re-litigates a decision without new evidence, and so that new joiners can read why the system looks the way it does.

## Purpose

- Make architectural intent durable; recover the *why*, not only the *what*.
- Force explicit option comparison and rejected alternatives at decision time.
- Reduce hallway-decision drift (the "Slack thread is the architecture" failure mode).
- Give code reviewers a reference to point at when a PR violates an established decision.

## When to Use

- A choice will be expensive to reverse (DB family, language, framework, identity model, messaging fabric, multi-tenancy model).
- A choice has cross-team consequences (event contracts, shared schemas, gateway policy).
- A choice is contested in code review or in design discussion and "we agreed verbally" is insufficient.
- A regulated decision needs an audit trail (data residency, key management, retention policy).
- A NON-decision is being recorded ("we deliberately did not adopt X because Y") — these are equally valuable.

When NOT to write an ADR: trivial implementation choices, easily reversible code patterns, and decisions a single team owner can change without coordination.

## ADR Lifecycle

| State | Meaning |
|---|---|
| `Proposed` | Draft open for comment; not authoritative. |
| `Accepted` | Decision in force. |
| `Superseded by ADR-NNNN` | Still readable, but a newer ADR overrides it. Never edit the superseded body — link forward. |
| `Deprecated` | Decision intentionally retired without a replacement (rare). |
| `Rejected` | Considered and explicitly turned down — keep for the audit trail. |

ADRs are **append-only**. To change a decision, write a new ADR that supersedes the old one and link both ways. Never rewrite an `Accepted` ADR's content; add a `Superseded by` note at the top.

## ADR Template

```markdown
# ADR-NNNN: <Short title in present tense>

- **Status**: Proposed | Accepted | Superseded by ADR-MMMM | Deprecated | Rejected
- **Date**: YYYY-MM-DD
- **Deciders**: <names / roles>
- **Consulted**: <SMEs, security, SRE, DBA, compliance>
- **Informed**: <stakeholders notified after the fact>

## Context

What forces this decision now? Business driver, technical driver, regulatory driver, deadline. State the problem in one paragraph. Reference the relevant requirements / NFRs / SLOs.

## Decision

We will <do X>. State the decision in one sentence, present tense, active voice.

## Options Considered

### Option 1: <name>
- **How it works**: 2–4 sentences.
- **Pros**: bullets.
- **Cons**: bullets.
- **Reversal cost**: low / medium / high.

### Option 2: <name>
… same shape …

(Include at least one rejected alternative. "We didn't think of any" is not credible.)

## Consequences

- **Positive**: outcomes we expect.
- **Negative**: costs we accept; technical debt incurred.
- **Operational**: new on-call surface, new metrics, new runbooks.
- **Security / compliance**: new authz/audit obligations.
- **Reversal plan**: if we wanted to undo this in 12 months, what is the path?

## Validation

How will we know the decision was correct? Concrete signals (SLO, error rate, ramp-up time, customer feedback) and a checkpoint date.

## References

- Related ADRs (link both ways).
- Tickets, design docs, benchmarks.
```

## Decision Quality Checklist

A reviewable ADR shows:

- A real problem with a concrete trigger, not "best practice".
- ≥ 2 options with honest pros/cons (the "do nothing" option counts).
- An explicit decision sentence (not "we will explore").
- Consequences that include cost and reversal path, not only benefits.
- A validation criterion that could later prove the decision wrong.
- Named deciders and consulted parties (avoid anonymous mandates).

## Operational Rules

- Store ADRs in `docs/adr/NNNN-<slug>.md` with zero-padded sequential numbers.
- ADR numbers are global and never reused even when an ADR is rejected.
- Link ADRs from the relevant code path (`README.md`, package doc, or top of the affected module) so readers find them at the point of use.
- Open ADRs are reviewed in the same forum that approves architecture changes; reject silently-merged ADRs.
- For regulated systems, capture ADRs that affect data residency, key custody, retention, and audit logging — these are part of the audit surface.

## Common Failure Modes

- ADR written after the code shipped — captures a justification, not a decision. Mitigate by requiring the ADR before the implementation PR is merged for in-scope decisions.
- ADRs that are 80 % background — readers stop at "Decision". Trim background to the minimum that frames the choice.
- Updating an Accepted ADR in place when the decision actually changed — this destroys the audit trail. Always write a successor.
- ADRs that describe how to implement, not what was decided — that belongs in the design doc.
- Treating ADRs as project status — they are timeless decisions, not sprint artifacts.

## Anti-Patterns

- Decision: "We will use microservices." → vacuous; pick the bounded context boundaries instead.
- Options section listing only the chosen option ("alternatives: none considered").
- Status `Accepted` with no deciders named.
- "Consequences: TBD" — if consequences are unknown, the decision is not ready.

## See Also

- `solution-architecture` — the design analysis that often precedes an ADR.
- `code-review-and-refactoring` — reviewers should cite ADRs when blocking conflicting changes.
- `devops-and-release` — release plans should reference the ADRs that motivated them.

