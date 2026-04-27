# Bắt đầu với CE7 Software Engineering Agent

[English](GETTING-STARTED.md) | [Tiếng Việt](GETTING-STARTED.vi-VN.md)

## Đây là gì?

Một agent kỹ thuật cấp principal với 7 skill packs bao phủ architecture, data, security, platform integration, resilience, observability, và application stacks. Thiết kế cho hệ thống enterprise và regulated (ngân hàng, bảo hiểm, thanh toán, bồi thường).

## Thiết lập trong 5 phút

1. Clone và mở trong IDE workspace.
2. Chọn chế độ cài đặt:
   - **Global** (tất cả project): `cp -R .github/skills/* ~/.copilot/skills/ && cp agents/*.agent.md ~/.copilot/agents/ && cp .github/copilot-instructions.md ~/.copilot/`
   - **Chỉ workspace**: mở folder — Copilot tự đọc `.github/`
   - **Thêm vào project có sẵn**: `cp -R .github/ <your-project>/.github/`
3. Kiểm tra cấu trúc: `python3 scripts/validate_hybrid_packs.py`
4. Bắt đầu prompt:

```text
Act as CE7 Software Engineering Agent.
Thiết kế luồng retry thanh toán có idempotency cho hệ thống multi-tenant.
```

## Cách hoạt động

```text
Prompt của bạn
  → CE7 agent phân loại task (triage)
  → Route đến 1-2 pack skills
  → Load references cụ thể chỉ khi cần
  → Trả về output principal-grade với:
      quyết định, giả định, trade-offs, phương án bị loại,
      tests, operational controls, và câu hỏi mở
```

## Bạn nhận được gì

| Pack | Bao phủ |
|---|---|
| `core-engineering-pack` | Requirements, architecture, APIs, testing, code review |
| `data-database-analytics-pack` | Data models, databases, SQL, pipelines, analytics |
| `security-access-pack` | Security review, auth, secrets, tenant isolation |
| `platform-integration-pack` | Messaging, gateways, rate limits, workflows, jobs |
| `resilience-performance-pack` | Resilience, caching, performance engineering |
| `observability-release-pack` | Telemetry, SLOs, CI/CD, rollout, rollback |
| `storage-search-stack-pack` | Object storage, search, .NET, Spring Boot, React, Angular, React Native |

## Thứ tự đọc tài liệu

| Bạn muốn... | Đọc file này |
|---|---|
| Hiểu tổng quan project | `README.md` |
| Bắt đầu sử dụng agent | File này |
| Xem điểm chất lượng | `REVIEW.md` |
| Chạy benchmark | `evals/file-based-benchmark-pipeline.vi-VN.md` |
| Hiểu pipeline đánh giá | `docs/pipeline-guide.vi-VN.md` |
| Biết khi nào/cách cải tiến skills | `docs/evaluation-improvement-playbook.vi-VN.md` |
| Bảo trì agent/skills | `instructions/principal-agent-maintenance.instructions.md` |

## Prompt mẫu

- "Thiết kế workflow xử lý bồi thường với state transitions, audit trail, và compensation."
- "Rà soát PR này về rủi ro migration và rollback trước khi canary release."
- "Chẩn đoán p95 latency cao sau khi thêm Redis cache và async workers."
- "Đề xuất API + data model cho gia hạn hợp đồng bảo hiểm với idempotency và reconciliation."

## Nguyên tắc thiết kế chính

- **Pack-first routing**: load một pack, sau đó chỉ load references cần thiết.
- **Token efficiency**: không paste toàn bộ references; tổng hợp và trỏ.
- **Evidence before claims**: khuyến nghị phải kèm validation steps.
- **Enterprise posture**: data correctness, auditability, security, operability là ưu tiên hàng đầu.
- **Progressive disclosure**: packs là routing layers; chi tiết nằm trong `references/*.md`.
