# Installation

This package is documentation-first and file-based. Pick one mode:

## Option A — Global (all workspaces)

Copy into `~/.copilot` so the agent is available in every project:

```bash
# Agent + instructions
cp agents/ce7-software-engineering.agent.md ~/.copilot/agents/
cp instructions/*.instructions.md           ~/.copilot/instructions/
cp .github/copilot-instructions.md          ~/.copilot/copilot-instructions.md

# Skills (8 packs + 39 references)
rm -rf ~/.copilot/skills/*
cp -R .github/skills/* ~/.copilot/skills/
```

Resulting layout:

```
~/.copilot/
  copilot-instructions.md
  agents/ce7-software-engineering.agent.md
  instructions/
    pack-conventions.instructions.md
    principal-agent-maintenance.instructions.md
    principal-skills-maintenance.instructions.md
  skills/
    core-engineering-pack/SKILL.md
    core-engineering-pack/references/*.md
    data-database-analytics-pack/SKILL.md
    data-database-analytics-pack/references/*.md
    security-access-pack/SKILL.md
    security-access-pack/references/*.md
    platform-integration-pack/SKILL.md
    platform-integration-pack/references/*.md
    resilience-performance-pack/SKILL.md
    resilience-performance-pack/references/*.md
    observability-release-pack/SKILL.md
    observability-release-pack/references/*.md
    storage-search-pack/SKILL.md
    storage-search-pack/references/*.md
    application-stacks-pack/SKILL.md
    application-stacks-pack/references/*.md
```

## Option B — Workspace-only

Open this folder in your IDE. Copilot reads `.github/copilot-instructions.md` and `.github/skills/` automatically. No copy needed.

## Option C — Add to an existing project

```bash
cp -R .github/copilot-instructions.md  <your-project>/.github/
cp -R .github/skills/                  <your-project>/.github/skills/
cp -R .github/agents/                  <your-project>/.github/agents/
```

## After install — quick checks

- Open the IDE and verify Copilot Chat sees the 8 pack skills.
- Try a routing-first prompt:
  - *"Act as CE7 Software Engineering Agent. Design idempotent payment retries for a multi-tenant mobile flow."*
  - *"Review this PR for migration and rollback risk before canary release."*

## Updating the package

When you pull updates, re-sync `.github/skills/` mirror from `skills/` (see `AGENTS.md` workflow), then re-run:

```bash
python3 scripts/validate_hybrid_packs.py
CHECK_GITHUB_MIRROR=1 python3 scripts/validate_hybrid_packs.py
```

