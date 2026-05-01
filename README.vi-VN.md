# CE7 Software Engineering Agent

[English](README.md) | [Tiếng Việt](README.vi-VN.md)

Một **agent kỹ thuật cấp principal** cho hệ thống enterprise và regulated (banking, insurance, payments, claims, billing). Định tuyến công việc tới các pack skill chuyên biệt và reference progressive-disclosure; **không bao giờ duplicate** nội dung pack vào agent.

## Bạn nhận được gì

- **2 agent** — `agents/ce7-software-engineering.agent.md` (router; entry point bắt buộc, ~125 dòng, table-driven) và `agents/skill-evaluator.agent.md` (tool benchmark/đánh giá tuỳ chọn dùng bởi `scripts/benchmark_pipeline.py`).
- **8 pack skills** — trigger `Use when` cụ thể, ranh giới `When NOT to Use` rõ ràng, cross-pack handoff tường minh.
- **39 reference playbook** — chỉ load khi task thật sự cần (đã bao gồm `aws-cloud-architecture` trong `core-engineering-pack`).
- **3 ví dụ output-shape** — architecture, debugging, review.
- **Eval harness** — routing, anti-pattern, token-budget, banking/insurance benchmark + scoring rubric.
- **Triển khai Copilot-first** qua `.github/copilot-instructions.md` + `.github/skills/`.

## Pack skills (8)

| Pack | Use when |
|---|---|
| `core-engineering-pack` | Requirements, architecture, system design, API contracts, testing, review, refactoring, ADR, AWS cloud architecture. |
| `data-database-analytics-pack` | Data modeling, lựa chọn/vận hành DB, tuning SQL/ORM, pipeline, analytics/warehouse. |
| `security-access-pack` | Identity, authz, tenant isolation, secrets, audit, sensitive data, abuse case. |
| `platform-integration-pack` | Messaging, gateway/BFF, partner integration, rate limit, workflow, job, batch. |
| `resilience-performance-pack` | Cache runtime, distributed state, timeout/retry/circuit, latency, capacity, cost/FinOps. |
| `observability-release-pack` | Logs/metrics/traces, SLO, alert, runbook, CI/CD, rollout, rollback, incident response. |
| `storage-search-pack` | Object/file storage, signed URL, retention, search/indexing, projection, reindex. |
| `application-stacks-pack` | Code framework: ASP.NET Core/EF, Spring Boot/JPA, React, Angular, React Native. |

## Quick start

```bash
# 1. Cài đặt (chọn 1 chế độ — xem docs/INSTALL.vi-VN.md)
cp -R .github/skills/                  ~/.copilot/skills/   # global
# HOẶC mở folder này trong IDE; Copilot tự đọc .github/

# 2. Validate
python3 scripts/validate_hybrid_packs.py

# 3. Thử một prompt
# "Act as the CE7 Software Engineering Agent. Design idempotent payment retries
#  with reconciliation and audit for a multi-tenant banking flow."
```

## Bản đồ tài liệu

Xem [`docs/README.vi-VN.md`](docs/README.vi-VN.md) để có index nhóm theo đối tượng người đọc. Tra nhanh:

| File | Đối tượng | Mục đích |
|---|---|---|
| `AGENTS.md` | Maintainer / contributor | Quy tắc edit, chính sách song ngữ, workflow sync. |
| `docs/INSTALL.md` / `.vi-VN.md` | User | Các chế độ cài đặt và kiểm tra sau cài. |
| `docs/GETTING-STARTED.md` / `.vi-VN.md` | User | Walkthrough 5 phút cho prompt đầu tiên. |
| `docs/pipeline-guide.md` / `.vi-VN.md` | Evaluator | Pipeline benchmark end-to-end. |
| `docs/evaluation-improvement-playbook.md` / `.vi-VN.md` | Maintainer | Khi nào và làm thế nào cải tiến pack. |
| `docs/skill-pack-quality-rubric.md` | Maintainer (chỉ EN) | Quality gate mà PR phải pass. |
| `docs/external-skill-research.md` | Maintainer (chỉ EN) | Pattern từ project khác + ghi chú originality. |
| `instructions/pack-conventions.instructions.md` | Maintainer | Single source of truth về structure / output style / token rules của pack. |
| `instructions/principal-agent-maintenance.instructions.md` | Maintainer | Quy tắc bảo trì agent. |
| `instructions/principal-skills-maintenance.instructions.md` | Maintainer | Quy tắc bảo trì reference. |
| `evals/scoring-rubric.md` / `.vi-VN.md` | Evaluator | Rubric chấm điểm theo từng prompt. |
| `examples/` | User / agent | Template output-shape mà agent tham chiếu. |
| `reports/CE7-AGENT-SYSTEM-REVIEW-2026-04-28.md` | Maintainer | Review nghiêm khắc dẫn tới kiến trúc hiện tại. |
| `reports/PLAN-automatic-memory.md` | Maintainer | Plan thiết kế deferred (memory dựa MCP). |
| `CHANGELOG.md` | Tất cả | Release log. |

## Quality gate (CI-enforceable)

`python3 scripts/validate_hybrid_packs.py` enforce:

- 8 peer pack skills (`skills/<pack>/SKILL.md`).
- 39 leaf references (`skills/<pack>/references/*.md`).
- Pack frontmatter `description` bắt đầu bằng `'Use when'`.
- Pack `SKILL.md` ≤ 100 dòng.
- Routing benchmark chỉ dùng tên pack đã biết.
- Banking/insurance benchmark = đúng 10 dòng; các domain bắt buộc phải có mặt.
- Các artifact của workflow đánh giá phải tồn tại.

Thêm `CHECK_GITHUB_MIRROR=1` để validate luôn cả mirror `.github/`.

## Status

- Layout: 8 pack / 39 reference / 2 agent / 3 example / 4 file eval.
- Review gần nhất: `reports/CE7-AGENT-SYSTEM-REVIEW-2026-04-28.md`.

## Contributing

Đọc `AGENTS.md` trước. Tóm tắt: giữ pack ≤ 100 dòng, giữ agent ở dạng table-driven, ưu tiên thêm reference thay vì thêm pack mới, và luôn cập nhật `evals/` khi đổi routing.

