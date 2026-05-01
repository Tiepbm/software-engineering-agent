# Cài đặt

Package này theo hướng tài liệu + file. Chọn 1 trong 3 chế độ:

## Option A — Global (mọi workspace)

Copy vào `~/.copilot` để agent dùng được ở mọi project:

```bash
# Agent + instructions
cp agents/ce7-software-engineering.agent.md ~/.copilot/agents/
cp instructions/*.instructions.md           ~/.copilot/instructions/
cp .github/copilot-instructions.md          ~/.copilot/copilot-instructions.md

# Skills (8 pack + 39 reference)
rm -rf ~/.copilot/skills/*
cp -R .github/skills/* ~/.copilot/skills/
```

Cấu trúc sau khi cài:

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
    core-engineering-pack/references/*.md          # bao gồm aws-cloud-architecture.md
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

## Option B — Chỉ workspace

Mở folder này trong IDE. Copilot tự đọc `.github/copilot-instructions.md` và `.github/skills/`. Không cần copy.

## Option C — Thêm vào project hiện có

```bash
cp -R .github/copilot-instructions.md  <your-project>/.github/
cp -R .github/skills/                  <your-project>/.github/skills/
cp -R .github/agents/                  <your-project>/.github/agents/
```

## Sau khi cài — kiểm tra nhanh

- Mở IDE và verify Copilot Chat thấy đủ 8 pack skill.
- Thử prompt routing-first:
  - *"Act as CE7 Software Engineering Agent. Design idempotent payment retries for a multi-tenant mobile flow."*
  - *"Review this PR for migration and rollback risk before canary release."*

## Cập nhật package

Khi pull update mới, re-sync mirror `.github/skills/` từ `skills/` (xem workflow trong `AGENTS.md`), rồi chạy lại:

```bash
python3 scripts/validate_hybrid_packs.py
CHECK_GITHUB_MIRROR=1 python3 scripts/validate_hybrid_packs.py
```

