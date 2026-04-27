# CE7 Software Engineering Agent

[English](README.md) | [Tiếng Việt](README.vi-VN.md)

## Tổng quan

Đây là agent kỹ thuật ở cấp principal dành cho hệ thống enterprise và regulated, với phạm vi mạnh về architecture, data, platform, security, observability, integration, delivery và production operations.

- Target Copilot chính: `.github/copilot-instructions.md` và `.github/skills/`
- Tệp agent: `agents/ce7-software-engineering.agent.md`, `agents/skill-evaluator.agent.md`
- Mốc đánh giá: `REVIEW.md`
- Quy tắc bảo trì:
  - `instructions/principal-agent-maintenance.instructions.md`
  - `instructions/principal-skills-maintenance.instructions.md`

## Chủ đề GitHub đề xuất (Tags/Topics)

Đề xuất gắn các topic sau cho repository trên GitHub để tăng khả năng tìm kiếm:

- `copilot-agent`
- `github-copilot`
- `prompt-engineering`
- `software-engineering`
- `enterprise-architecture`
- `system-design`
- `api-design`
- `data-engineering`
- `database-architecture`
- `security-review`
- `observability`
- `sre`
- `devops`
- `performance-engineering`
- `refactoring`
- `regulated-systems`
- `banking`
- `insurance`

Thiết lập nhanh trên GitHub UI: Repository -> Settings -> General -> Topics.

Tùy chọn với GitHub CLI:

```bash
gh repo edit <owner>/<repo> --add-topic copilot-agent --add-topic github-copilot --add-topic prompt-engineering --add-topic software-engineering --add-topic enterprise-architecture --add-topic system-design --add-topic api-design --add-topic data-engineering --add-topic database-architecture --add-topic security-review --add-topic observability --add-topic sre --add-topic devops --add-topic performance-engineering --add-topic refactoring --add-topic regulated-systems --add-topic banking --add-topic insurance
```

## Cấu trúc package

```text
software-engineering-agent/
  .github/
    copilot-instructions.md
    agents/
      ce7-software-engineering.agent.md
      skill-evaluator.agent.md
    skills/
      <7 pack skills>/SKILL.md
      <7 pack skills>/references/*.md
  agents/
    ce7-software-engineering.agent.md
    skill-evaluator.agent.md
  skills/
    <7 pack skills>/SKILL.md
    <7 pack skills>/references/*.md
  evals/
    banking-insurance-benchmark.jsonl
    file-based-benchmark-pipeline.md
    file-based-benchmark-pipeline.vi-VN.md
    model-comparison-runbook.md
    model-comparison-runbook.vi-VN.md
    routing-benchmark.jsonl
    scoring-rubric.md
    scoring-rubric.vi-VN.md
  docs/
    evaluation-improvement-playbook.md
    external-skill-research.md
    evaluation-improvement-playbook.vi-VN.md
    pipeline-guide.md
    pipeline-guide.vi-VN.md
    skill-pack-quality-rubric.md
  reports/
    README.md
    README.vi-VN.md
    latest-skill-eval.md
    latest-skill-eval.vi-VN.md
    skill-eval-history.jsonl
  scripts/
    benchmark_pipeline.py
    validate_hybrid_packs.py
  instructions/
    principal-agent-maintenance.instructions.md
    principal-skills-maintenance.instructions.md
  REVIEW.md
```

### Thiết kế hybrid skill pack ưu tiên Copilot

- Chỉ có **7 peer pack skills** cho GitHub Copilot.
- **33 leaf skills** trước đây được giữ dưới dạng `references/*.md` trong pack phù hợp.
- Copilot nên load pack trước, sau đó chỉ load reference chính xác cần cho task.
- `.github/skills/` là target runtime chính; `skills/` ở root mirror cùng cấu trúc để bảo trì repository.
- `docs/external-skill-research.md` ghi lại các pattern đã tham khảo từ project khác trong workspace.
- `docs/skill-pack-quality-rubric.md` chuyển các pattern đó thành quality gates có thể review.
- `docs/evaluation-improvement-playbook.md` / `docs/evaluation-improvement-playbook.vi-VN.md` hướng dẫn vòng đánh giá và cải tiến agent/skills.

### Bản đồ tài liệu đánh giá

Để tránh trùng lặp và nhiễu thông tin, các tài liệu đánh giá hiện có ranh giới rõ ràng:

- `docs/pipeline-guide.md` / `docs/pipeline-guide.vi-VN.md` → guide chuẩn cho pipeline end-to-end.
- `docs/evaluation-improvement-playbook.md` / `docs/evaluation-improvement-playbook.vi-VN.md` → chính sách đánh giá, logic quyết định update, cadence cải tiến, Definition of Done.
- `evals/file-based-benchmark-pipeline.md` / `evals/file-based-benchmark-pipeline.vi-VN.md` → quickstart lệnh ngắn.
- `evals/model-comparison-runbook.md` / `evals/model-comparison-runbook.vi-VN.md` → runbook so sánh GPT vs Claude cho bộ case banking / non-life insurance.
- `evals/scoring-rubric.md` / `evals/scoring-rubric.vi-VN.md` → tiêu chí chấm điểm.

### Bản đồ reports

`reports/` giờ cũng có ownership rõ ràng:

- `reports/latest-skill-eval.md` / `reports/latest-skill-eval.vi-VN.md` → snapshot ngắn gọn của run mới nhất.
- `reports/skill-eval-history.jsonl` → lịch sử machine-readable dạng append-only với **1 dòng cho mỗi run**.
- `reports/README.md` / `reports/README.vi-VN.md` → contract và schema của reports.

Các findings chi tiết theo từng prompt nên nằm trong `runs/<run_id>/`, đặc biệt là `report.json`, `summary.md` và `scores.jsonl`.

## Mục tiêu tối ưu

- Hỗ trợ ra quyết định ở mức principal, không trả lời kiểu chat chung chung.
- Ưu tiên data correctness, auditability, security, operability và delivery safety.
- Tối ưu cho domain nhạy cảm như banking, insurance, payments, claims, policy/billing và PII.
- Luôn nêu rõ assumptions, trade-offs, risks, rejected options và validation steps.

## Cơ chế trả lời

Với yêu cầu không tầm thường, agent thực hiện triage 6 bước bắt buộc: primary role, supporting lenses, task type, risk class, regulatory sensitivity và missing constraints.

## Cài đặt và thiết lập

Gói này theo hướng tài liệu + file markdown. Dựa trên cấu trúc hiện tại (`.github/`, `agents/`, `skills/`, `instructions/`), bạn có thể cài đặt nhanh như sau.

### 1) Clone repository

```bash
git clone <your-repo-url>
cd software-engineering-agent
```

### 2) Giữ nguyên cấu trúc package

Các đường dẫn bắt buộc:

- `.github/copilot-instructions.md`
- `.github/skills/<pack-name>/SKILL.md` (7 pack skills)
- `.github/skills/<pack-name>/references/<leaf>.md` (33 leaf references)
- `agents/ce7-software-engineering.agent.md`
- `agents/skill-evaluator.agent.md`
- `instructions/principal-agent-maintenance.instructions.md`
- `instructions/principal-skills-maintenance.instructions.md`

### 3) Mở thư mục trong workspace IDE

Mở thư mục này trong workspace để Copilot có thể đọc đầy đủ agent + skills + instructions.

### 4) Bắt đầu bằng prompt có bối cảnh

Ví dụ:

- "Act as CE7 Software Engineering Agent. Design idempotent payment retries for a multi-tenant mobile flow."
- "Review this change using security, data, and release-risk lenses."

### 5) Kiểm tra sau khi cập nhật

- Đảm bảo `README.md` và `README.vi-VN.md` còn đồng bộ.
- Đảm bảo link pack vẫn trỏ đúng `skills/<pack>/SKILL.md` và `.github/skills/<pack>/SKILL.md`.
- Cập nhật `docs/external-skill-research.md` khi áp dụng pattern mới từ project khác.
- Review `docs/skill-pack-quality-rubric.md` khi đổi trigger, reference hoặc evaluator rules.
- Chạy `python3 scripts/validate_hybrid_packs.py`.
- Cập nhật `REVIEW.md` sau các thay đổi lớn.

## Mapping hybrid pack

| # | Pack skill | Leaf references cũ | Trigger chính |
|---:|---|---|---|
| 1 | `core-engineering-pack` | `requirements-analysis`, `solution-architecture`, `system-design`, `api-design`, `testing-strategy`, `code-review-and-refactoring` | Requirements, architecture, APIs, tests, review, refactoring |
| 2 | `data-database-analytics-pack` | `data-modeling`, `database-architecture`, `sql-and-query-optimization`, `database-reliability-and-operations`, `data-engineering-and-pipelines`, `analytics-and-warehouse-design` | Data models, databases, SQL/ORM, DB ops, pipelines, analytics |
| 3 | `security-access-pack` | `security-review`, `authn-authz-and-secrets` | Security review, identity, authorization, tenant isolation, secrets, sensitive data |
| 4 | `platform-integration-pack` | `messaging-and-eventing`, `api-gateway-and-service-integration`, `rate-limiting-and-traffic-control`, `workflow-and-job-orchestration`, `background-jobs-and-batch-processing` | Messaging, gateways, integrations, rate limits, workflows, jobs, batch |
| 5 | `resilience-performance-pack` | `resilience-and-fault-tolerance`, `caching-and-distributed-state`, `performance-engineering` | Resilience, caching, distributed state, latency, throughput, profiling |
| 6 | `observability-release-pack` | `logging-metrics-and-tracing`, `monitoring-alerting-and-slos`, `observability-and-sre`, `devops-and-release` | Telemetry, SLOs, alerts, runbooks, release, rollout, rollback |
| 7 | `storage-search-stack-pack` | `file-and-object-storage`, `search-and-indexing`, `dotnet-development`, `java-spring-boot-development`, `reactjs-development`, `angular-development`, `react-native-development` | Object storage, search, .NET, Spring Boot, React, Angular, React Native |

### Validation

```bash
python3 scripts/validate_hybrid_packs.py
```

Validator kiểm tra đúng 7 peer pack skills, 33 references, 2 agents, chưa có deferred reviewer agents, route Copilot đầy đủ và corpus benchmark hợp lệ.

## Bước tiếp theo để đánh giá và cải tiến

1. Đọc `docs/evaluation-improvement-playbook.md` hoặc `docs/evaluation-improvement-playbook.vi-VN.md` để hiểu chính sách đánh giá và vòng cải tiến.
2. Chạy structural validation:

   ```bash
   python3 scripts/validate_hybrid_packs.py
   ```

3. Chọn 5–10 prompts từ `evals/routing-benchmark.jsonl`.
4. Chạy các prompt đó với `ce7-software-engineering` và ghi lại pack/reference được kích hoạt.
5. Dùng `agents/skill-evaluator.agent.md` để chấm output theo `evals/scoring-rubric.md`.
6. Đồng bộ snapshot mới nhất vào `reports/latest-skill-eval.md` / `reports/latest-skill-eval.vi-VN.md` và thêm **một dòng ở mức run** vào `reports/skill-eval-history.jsonl`.
7. Chỉ patch pack/reference khi benchmark chỉ ra lỗi cụ thể về routing, reference precision, output quality hoặc token bloat.

### Benchmark nghiệp vụ Ngân hàng và Bảo hiểm phi nhân thọ

- `evals/banking-insurance-benchmark.jsonl` chứa 10 case thực tế cho banking, non-life insurance và bancassurance.
- `evals/model-comparison-runbook.md` / `evals/model-comparison-runbook.vi-VN.md` hướng dẫn chạy cùng một case trên GPT và Claude để so sánh.
- `evals/file-based-benchmark-pipeline.md` / `evals/file-based-benchmark-pipeline.vi-VN.md` là quickstart cho pipeline qua file.
- `docs/pipeline-guide.md` / `docs/pipeline-guide.vi-VN.md` là guide đầy đủ cho prepare → output → score → evaluator → report/history.
- Dùng `evals/scoring-rubric.md` hoặc `evals/scoring-rubric.vi-VN.md` để chấm điểm nhất quán giữa model.
- Dùng `reports/README.md` / `reports/README.vi-VN.md` để giữ reports toàn cục ngắn gọn và đúng mức run.

### Pipeline tự động qua file

```bash
python3 scripts/benchmark_pipeline.py prepare --run-id 2026-04-27-gpt-claude-v1 --models gpt,claude
python3 scripts/benchmark_pipeline.py score --run-id 2026-04-27-gpt-claude-v1 --append-history
python3 scripts/benchmark_pipeline.py evaluator-prompts --run-id 2026-04-27-gpt-claude-v1
```

Model outputs cần được lưu vào `runs/<run_id>/outputs/<model>/<prompt_id>.md` trước khi chạy lệnh `score`.

### Auto end-to-end bằng 1 lệnh (chỉ switch model)

Nếu bạn muốn chạy toàn bộ pipeline tự động và chỉ chọn model:

```bash
# GPT
export OPENAI_API_KEY="<your_openai_key>"
python3 scripts/benchmark_pipeline.py run --run-id 2026-04-27-gpt-auto --model gpt

# Claude
export ANTHROPIC_API_KEY="<your_anthropic_key>"
python3 scripts/benchmark_pipeline.py run --run-id 2026-04-27-claude-auto --model claude
```

Lệnh `run` sẽ tự động:

1. prepare prompts cho model đã chọn;
2. gọi API của provider cho từng prompt và lưu output;
3. chấm deterministic với `--append-history`;
4. sync `reports/latest-skill-eval*` và append 1 dòng history ở mức run;
5. tạo `evaluator-prompts/` cho semantic scoring.

### Không có API key (Copilot chat windows) — chế độ đề xuất

Nếu bạn không có API key và muốn chạy theo kiểu Copilot thủ công nhưng vẫn gần tự động:

```bash
# 1) Chuẩn bị toàn bộ prompts + output stubs + worklist cho cả GPT và Claude
python3 scripts/benchmark_pipeline.py implement \
  --run-id 2026-04-27-gpt-claude-manual \
  --models gpt,claude

# 2) Sau khi dán xong output vào files, finalize để chấm và sinh evaluator-prompts
python3 scripts/benchmark_pipeline.py finalize \
  --run-id 2026-04-27-gpt-claude-manual \
  --models gpt,claude
```

`implement` sẽ tạo:

- `runs/<run_id>/prompts/<model>/*.md`
- `runs/<run_id>/outputs/<model>/*.md` (stub sẵn để bạn paste output)
- `runs/<run_id>/manual/README.md`
- `runs/<run_id>/manual/worklist.md`

`finalize` sẽ:

1. kiểm tra output còn thiếu hoặc còn marker `CE7_OUTPUT_PENDING`;
2. chấm deterministic + sync reports/history;
3. sinh `evaluator-prompts/`.

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

