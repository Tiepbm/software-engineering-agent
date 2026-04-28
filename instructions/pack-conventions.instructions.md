---
description: 'Shared conventions for all pack SKILL.md files. Maintainer-only; do not load at runtime — pack SKILL.md files inherit these rules implicitly.'
applyTo: 'skills/**/SKILL.md'
---
# Pack Conventions

These rules apply to **every** pack `SKILL.md`. Packs do NOT repeat them in body text.

## Pack Skill Structure (REQUIRED)

A trimmed pack `SKILL.md` MUST contain, in this order:

1. Frontmatter (`name`, `description` starting with `'Use when …'`).
2. Title (`# <Pack Title>`).
3. `## When to Use` — concrete trigger keywords (3–6 bullets).
4. `## When NOT to Use` — explicit anti-triggers pointing to neighbour packs (2–4 bullets).
5. `## Pack Reference Map` — table with columns `Reference | Use when` (one row per reference, **distinct** trigger per row).
6. `## Cross-Pack Handoffs` — bullets `→ <other-pack> for <concern>` (3–6 bullets).
7. (Optional) `## Worked Example` or `## Notes` — only if a concrete example reduces routing ambiguity.

A pack `SKILL.md` MUST NOT contain `Purpose`, `Routing Rules`, `Reference Selection Matrix` (the matrix is now folded into `Pack Reference Map`), `Expected Output Style`, `Token Efficiency Rules`, or `Quality Gates` sections — those are owned by this file.

## Output Style (applies to every response that activates a pack)

- Decision first, reasoning second.
- Name the pack(s) and reference(s) consulted when work is non-trivial.
- Separate immediate action / trade-offs / tests / ops / follow-up.
- Concrete: contracts, schemas, gates, examples — not generic advice.
- Stop and ask for missing constraints when a recommendation would change with them.

## Token Efficiency (applies to every pack)

- Pack = metadata + routing. References = progressive disclosure.
- Do NOT paste large reference content into responses.
- Default to ONE pack. Activate a second pack only when the task crosses a domain boundary.
- If more than 3 references seem needed, name the primary one and justify each extra.

## Quality Gates (every response that activates a pack)

- Selected references match the user's actual risk and task type.
- Security, data correctness, observability, delivery, and failure handling addressed when material.
- Recommendations are testable; rejected options carry an explicit reason.
- For regulated domains (banking, insurance, payments, claims, billing), audit, idempotency, reconciliation, and operator repair are first-class.

## Pack Size Budget (CI-enforced)

- Pack `SKILL.md` ≤ 100 lines (validator-enforced).
- Description must start with `Use when` and be ≤ 250 characters.
- Each reference file should normally stay ≤ 220 lines; deep playbooks may exceed but should split into a `worked-example` sibling file when > 250 lines.

## Anti-Patterns (forbidden in pack SKILL.md)

- Repeating boilerplate from this file in any pack body.
- Tautological selection rules ("Read X.md when X is material") — every reference row must carry a **distinct** trigger.
- Missing `When NOT to Use` section — packs must claim a boundary, not only a domain.
- Missing `Cross-Pack Handoffs` section — every pack overlaps with at least one other and must say so explicitly.

