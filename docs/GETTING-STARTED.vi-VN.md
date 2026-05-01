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
| `core-engineering-pack` | Requirements, architecture, APIs, testing, code review, AWS cloud architecture |
| `data-database-analytics-pack` | Data models, databases, SQL, pipelines, analytics |
| `security-access-pack` | Security review, auth, secrets, tenant isolation |
| `platform-integration-pack` | Messaging, gateways, rate limits, workflows, jobs |
| `resilience-performance-pack` | Resilience, caching, performance, cost/FinOps |
| `observability-release-pack` | Telemetry, SLOs, CI/CD, rollout, rollback, incident response |
| `storage-search-pack` | Object storage, signed URLs, search/indexing |
| `application-stacks-pack` | .NET, Spring Boot, React, Angular, React Native |

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

## Khi nào nên dùng agent này

Agent này là **principal-level engineering panel**, không phải coding assistant. Nó mang lại giá trị cao nhất khi bạn cần quyết định kiến trúc, phân tích trade-offs, và hướng dẫn production-safety.

### Rất phù hợp (agent thêm giá trị đáng kể)

| Loại câu hỏi | Ví dụ |
|---|---|
| Thiết kế hệ thống | "Thiết kế payment idempotency cho mobile banking" |
| Chọn database | "PostgreSQL hay MongoDB cho claims system?" |
| Review kiến trúc | "Review PR này về rủi ro migration và rollback" |
| Review bảo mật | "Review endpoint này về tenant isolation" |
| Data modeling | "Thiết kế SCD Type 2 cho policy versioning" |
| DevOps / release | "Lập kế hoạch canary rollout với SLO gates" |
| Chẩn đoán performance | "Chẩn đoán p95 latency cao sau khi thêm Redis cache" |
| Thiết kế integration | "Thiết kế outbox pattern cho payment events" |

### Khá phù hợp (agent hỗ trợ patterns, không viết full code)

| Loại câu hỏi | Bạn nhận được gì |
|---|---|
| "Viết outbox pattern bằng Spring Boot" | Code pattern từ reference + architectural context |
| "Implement idempotency middleware .NET" | Code example + production checklist |
| "Setup TanStack Query với auth refresh" | Code pattern + security considerations |
| "Fix N+1 query trong JPA" | EXPLAIN walkthrough + index recommendation |

### Không phù hợp (dùng model trực tiếp)

| Loại câu hỏi | Lý do |
|---|---|
| "Viết function sort array" | Coding cơ bản — model đã biết, agent không thêm giá trị |
| "Debug lỗi CSS layout" | Frontend layout ngoài scope agent |
| "Convert code Python sang Go" | Dịch ngôn ngữ — không có reference coverage |
| "Giải thích async/await cho người mới" | Nội dung tutorial — agent dành cho decisions, không phải dạy học |

### Workflow khuyến nghị

Với các task implementation, kết hợp agent với model trực tiếp:

1. **Hỏi CE7**: "Nên dùng pattern nào cho payment retry?" → Nhận quyết định kiến trúc + trade-offs + checklist
2. **Hỏi model trực tiếp**: "Implement pattern đó bằng Spring Boot" → Nhận code hoạt động
3. **Hỏi CE7**: "Review implementation này về production risks" → Nhận review security/ops/data
