# CE7 Software Engineering Agent

[English](README.md) | [Tiếng Việt](README.vi-VN.md)

## Tổng quan

Đây là agent kỹ thuật ở cấp principal dành cho hệ thống enterprise và regulated, với phạm vi mạnh về architecture, data, platform, security, observability, integration, delivery và production operations.

- Tệp agent: `agents/ce7-software-engineering.agent.md`
- Mốc đánh giá: `REVIEW.md`
- Quy tắc bảo trì:
  - `instructions/principal-agent-maintenance.instructions.md`
  - `instructions/principal-skills-maintenance.instructions.md`

## Cấu trúc package

```text
ce7-software-engineering/
  agents/
    ce7-software-engineering.agent.md
  skills/
    <33 domain skills>
  instructions/
    principal-agent-maintenance.instructions.md
    principal-skills-maintenance.instructions.md
  REVIEW.md
```

## Mục tiêu tối ưu

- Hỗ trợ ra quyết định ở mức principal, không trả lời kiểu chat chung chung.
- Ưu tiên data correctness, auditability, security, operability và delivery safety.
- Tối ưu cho domain nhạy cảm như banking, insurance, payments, claims, policy/billing và PII.
- Luôn nêu rõ assumptions, trade-offs, risks, rejected options và validation steps.

## Cơ chế trả lời

Với yêu cầu không tầm thường, agent thực hiện triage 6 bước bắt buộc: primary role, supporting lenses, task type, risk class, regulatory sensitivity và missing constraints.

## Bảng mapping đầy đủ 33 skills

| # | Skill slug | Nhóm | Khi nào dùng | Tác nhân kích hoạt chính | Skill file |
|---:|---|---|---|---|---|
| 1 | `requirements-analysis` | Core Engineering | Làm rõ yêu cầu mơ hồ, acceptance criteria, scope/risk | Ambiguous scope, actors, workflows, measurable outcomes | [SKILL.md](skills/requirements-analysis/SKILL.md) |
| 2 | `solution-architecture` | Core Engineering | Chọn hình dáng kiến trúc, buy-vs-build, ownership | Architecture shape, boundaries, complexity, team fit | [SKILL.md](skills/solution-architecture/SKILL.md) |
| 3 | `system-design` | Core Engineering | Thiết kế runtime flow, component boundaries, failure modes | Runtime flows, sync/async, scalability, bottlenecks | [SKILL.md](skills/system-design/SKILL.md) |
| 4 | `api-design` | Core Engineering | Thiết kế contract API, versioning, idempotency, errors | API boundaries, request/response contracts, compatibility | [SKILL.md](skills/api-design/SKILL.md) |
| 5 | `testing-strategy` | Core Engineering | Xây dựng chiến lược test theo rủi ro, test pyramid, migration tests | Risk-based testing, integration/contract/E2E scope | [SKILL.md](skills/testing-strategy/SKILL.md) |
| 6 | `code-review-and-refactoring` | Core Engineering | Review maintainability và kế hoạch refactor an toàn | Coupling/cohesion, debt, regression risk, safe sequence | [SKILL.md](skills/code-review-and-refactoring/SKILL.md) |
| 7 | `data-modeling` | Data and Database | Mô hình hóa entity/aggregate, history, auditability | Entities, relationships, transactional boundaries | [SKILL.md](skills/data-modeling/SKILL.md) |
| 8 | `database-architecture` | Data and Database | Chọn loại database theo workload-fit | OLTP/OLAP fit, consistency, scaling, retention | [SKILL.md](skills/database-architecture/SKILL.md) |
| 9 | `sql-and-query-optimization` | Data and Database | Tối ưu SQL/ORM dựa trên execution plan | Query plans, indexes, joins, lock/contention | [SKILL.md](skills/sql-and-query-optimization/SKILL.md) |
| 10 | `database-reliability-and-operations` | Data and Database | Vận hành database production: backup/restore/failover/migration | Replication, restore drills, migration safety | [SKILL.md](skills/database-reliability-and-operations/SKILL.md) |
| 11 | `data-engineering-and-pipelines` | Data and Database | Thiết kế ETL/ELT/CDC, replay, backfill, data quality | Pipelines, schema evolution, idempotency, recovery | [SKILL.md](skills/data-engineering-and-pipelines/SKILL.md) |
| 12 | `analytics-and-warehouse-design` | Data and Database | Thiết kế DWH/lakehouse, marts, semantic layer, governance | Dimensional models, BI consumption, freshness/cost | [SKILL.md](skills/analytics-and-warehouse-design/SKILL.md) |
| 13 | `search-and-indexing` | Data and Database | Thiết kế search/indexing, relevance, reindex, auth filtering | Index sync, relevance tuning, eventual consistency | [SKILL.md](skills/search-and-indexing/SKILL.md) |
| 14 | `security-review` | Security and Access | Đánh giá attack surface và abuse paths | Authz gaps, validation, secrets, dependency risk | [SKILL.md](skills/security-review/SKILL.md) |
| 15 | `authn-authz-and-secrets` | Security and Access | Thiết kế authn/authz, identity propagation, secret rotation | Identity, RBAC/ABAC, least privilege, secret lifecycle | [SKILL.md](skills/authn-authz-and-secrets/SKILL.md) |
| 16 | `messaging-and-eventing` | Messaging and Platform | Thiết kế queue/topic/event, ordering, DLQ, replay | Events, pub/sub, outbox/inbox, idempotent consumers | [SKILL.md](skills/messaging-and-eventing/SKILL.md) |
| 17 | `api-gateway-and-service-integration` | Messaging and Platform | Thiết kế gateway/BFF, routing policy, service integration | API gateway, protocol translation, auth propagation | [SKILL.md](skills/api-gateway-and-service-integration/SKILL.md) |
| 18 | `rate-limiting-and-traffic-control` | Messaging and Platform | Thiết kế throttling, quota, fairness, abuse prevention | Rate limiting, backpressure, graceful rejection | [SKILL.md](skills/rate-limiting-and-traffic-control/SKILL.md) |
| 19 | `workflow-and-job-orchestration` | Messaging and Platform | Orchestrate workflow dài hạn, saga, compensation | Workflow state, approvals, compensation, resumability | [SKILL.md](skills/workflow-and-job-orchestration/SKILL.md) |
| 20 | `background-jobs-and-batch-processing` | Messaging and Platform | Thiết kế job schedule/batch có checkpoint và retry | Chunking, retries, duplicate prevention, observability | [SKILL.md](skills/background-jobs-and-batch-processing/SKILL.md) |
| 21 | `resilience-and-fault-tolerance` | Resilience and Performance | Áp dụng timeouts/retries/circuit breakers/degradation | Failure containment, failover, recovery patterns | [SKILL.md](skills/resilience-and-fault-tolerance/SKILL.md) |
| 22 | `caching-and-distributed-state` | Resilience and Performance | Thiết kế cache correctness, TTL, invalidation, distributed locks | Staleness rules, key scope, stampede controls | [SKILL.md](skills/caching-and-distributed-state/SKILL.md) |
| 23 | `performance-engineering` | Resilience and Performance | Cải thiện latency/throughput dựa trên profiling evidence | Profiling, capacity, concurrency, cost-aware tuning | [SKILL.md](skills/performance-engineering/SKILL.md) |
| 24 | `logging-metrics-and-tracing` | Observability and Ops | Thiết kế telemetry có cấu trúc và redaction | Structured logs, metrics, traces, correlation IDs | [SKILL.md](skills/logging-metrics-and-tracing/SKILL.md) |
| 25 | `monitoring-alerting-and-slos` | Observability and Ops | Thiết kế SLI/SLO, alert actionable, runbook ownership | Alert quality, burn rates, error budgets | [SKILL.md](skills/monitoring-alerting-and-slos/SKILL.md) |
| 26 | `observability-and-sre` | Observability and Ops | Bảo đảm production readiness và operational ownership | Supportability, runbooks, game-day readiness | [SKILL.md](skills/observability-and-sre/SKILL.md) |
| 27 | `devops-and-release` | Observability and Ops | Thiết kế CI/CD, rollout, feature flags, rollback safety | Release orchestration, migration coordination | [SKILL.md](skills/devops-and-release/SKILL.md) |
| 28 | `file-and-object-storage` | Storage and Search | Thiết kế lưu trữ file/object, signed URL, retention, scanning | Upload/download flows, metadata, legal hold | [SKILL.md](skills/file-and-object-storage/SKILL.md) |
| 29 | `dotnet-development` | Stack Specific | Hướng dẫn triển khai ASP.NET Core/EF Core production | Layering, middleware, async/cancellation, DTOs | [SKILL.md](skills/dotnet-development/SKILL.md) |
| 30 | `java-spring-boot-development` | Stack Specific | Hướng dẫn triển khai Spring Boot service architecture | Controllers/services/repos, JPA, transactions | [SKILL.md](skills/java-spring-boot-development/SKILL.md) |
| 31 | `reactjs-development` | Stack Specific | Hướng dẫn triển khai React web app architecture | Components/hooks/state/forms/API integration | [SKILL.md](skills/reactjs-development/SKILL.md) |
| 32 | `angular-development` | Stack Specific | Hướng dẫn Angular structure, RxJS, forms, guards | Feature modules, services, interceptors, testability | [SKILL.md](skills/angular-development/SKILL.md) |
| 33 | `react-native-development` | Stack Specific | Hướng dẫn mobile RN iOS/Android production | Navigation, permissions, offline, performance | [SKILL.md](skills/react-native-development/SKILL.md) |

## Định dạng output mặc định

- Kiến trúc/phân tích: bài toán -> ràng buộc -> phương án -> khuyến nghị -> kiến trúc/dữ liệu/tích hợp/bảo mật/vận hành -> rủi ro -> kế hoạch triển khai -> checklist xác thực.
- Triển khai/gỡ lỗi: chẩn đoán -> nguyên nhân gốc khả dĩ -> cách sửa -> tác động -> kiểm thử -> rủi ro còn lại -> cải tiến dài hạn.
- Rà soát/tái cấu trúc: đánh giá tổng thể -> điểm mạnh -> vấn đề nghiêm trọng -> vấn đề trung bình -> quan ngại kiến trúc/dữ liệu -> kế hoạch refactor -> thứ tự ưu tiên.

## Điều kiện dừng để làm rõ thêm

Agent sẽ dừng để hỏi thêm ràng buộc khi thiếu điều kiện an toàn quan trọng, ví dụ:

- Di chuyển dữ liệu thiếu chiến lược reconciliation và rollback/roll-forward
- Thiết kế messaging thiếu ordering, idempotency, retry, DLQ và replay
- Thiết kế cache thiếu staleness, invalidation và an toàn phân quyền
- Thay đổi nhạy cảm bảo mật thiếu phân tích auth/authz/secrets/audit
- Kế hoạch phát hành thiếu sequencing, verification và rollback
- Khuyến nghị hiệu năng thiếu baseline làm bằng chứng

## Prompt mẫu

- "Thiết kế luồng retry thanh toán có idempotency từ mobile -> API -> PSP trong hệ thống multi-tenant."
- "Rà soát PR này về rủi ro migration và rollback trước khi canary release."
- "Đề xuất thay đổi API + data model cho luồng chuyển trạng thái claim có audit trail."
- "Chẩn đoán p95 latency cao sau khi thêm Redis cache và async workers."

## Lưu ý khi đóng góp

- Giữ agent như routing/orchestration panel; không duplicate nội dung skills.
- Giữ skills theo đúng structure và quality floor trong instructions.
- Bảo toàn enterprise/regulated posture và production safety rules.
- Re-run review và cập nhật `REVIEW.md` sau khi thay đổi lớn.

## Tài liệu tham chiếu

- Đặc tả agent: `agents/ce7-software-engineering.agent.md`
- Báo cáo chất lượng: `REVIEW.md`
- Hướng dẫn bảo trì agent: `instructions/principal-agent-maintenance.instructions.md`
- Hướng dẫn bảo trì skills: `instructions/principal-skills-maintenance.instructions.md`

