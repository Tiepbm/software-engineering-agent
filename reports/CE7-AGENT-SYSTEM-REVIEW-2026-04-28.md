# CE7 Software Engineering Agent — Đánh giá hệ thống (2026-04-28)

**Reviewer**: Principal AI agent architect / context-engineering specialist
**Phạm vi**: `software-engineering-agent/{agents,skills,instructions,evals,docs,README.md,REVIEW.md,CHANGELOG.md}`
**Loại trừ**: `~/.copilot/skills/*` (chỉ là deployment mirror), các repo `agents/`, `claude-skills/`, `superpowers/`, `oh-my-openagent/`, `claude-mem/`.
**Giả định runtime**: 1 principal router agent + 7 pack skills + tham chiếu progressive disclosure qua `references/`, kích hoạt theo `description` của Copilot. Không có custom router runtime.

**Giả định do file thiếu** (liệt kê 1 lần):

- Không tồn tại `AGENTS.md` ở root → coi như chưa có; `instructions/*.instructions.md` đang đảm nhiệm vai trò tương tự cho maintainer.
- Không tồn tại thư mục `examples/` → các "few-shot" hiện chỉ nằm inline trong agent file (1 ví dụ duy nhất).
- Coi `agents/skill-evaluator.agent.md` là agent meta (đánh giá), không phải router chính.

---

## 1. Executive Summary

| Hạng mục | Điểm |
|---|---:|
| **Overall quality** | **6.5 / 10** |
| **Routing quality** | **6.0 / 10** |
| **Token efficiency** | **4.5 / 10** |
| **Maintainability** | **7.0 / 10** |

> Lưu ý: `REVIEW.md` nội bộ tự chấm **9.2/10**. Khoảng cách chủ yếu đến từ (a) đo điểm dựa trên line-count floor thay vì routing thực tế, (b) chưa tính boilerplate trùng lặp giữa 7 packs, (c) chưa có eval kiểm chứng routing thật.

### Top 5 vấn đề (xếp theo impact)

1. **7 pack `SKILL.md` gần như sao chép nguyên văn 6 section boilerplate** (`Purpose`, `Routing Rules`, `Reference Selection Matrix`, `Expected Output Style`, `Token Efficiency Rules`, `Quality Gates`). Tổng ~280 dòng trùng lặp tuyệt đối, không tăng signal cho routing.
2. **`Reference Selection Matrix` là filler tautological** — mọi dòng đều ghi `"Read references/X.md when this exact subdomain is material to the answer"`. Không hề mô tả trigger phân biệt — agent không có cách nào chọn đúng reference từ đó.
3. **Principal agent (320 dòng, ước ~2.4–2.8k tokens)** vượt **2x** ngân sách 1200 tokens. Có 4 lớp luật chồng lấn: `Non-Negotiable Operating Rules` (12) ⟂ `Default Review Lenses` (13) ⟂ `Cross-Cutting Platform Routing` (table 22 dòng) ⟂ `Production Stop Conditions` (9) ⟂ `Prohibited Behavior` (11). Cùng nội dung idempotency/caching/messaging/security được nhắc tối thiểu **3–4 lần**.
4. **`storage-search-stack-pack` ghép sai loại**: object storage + search (cross-cutting platform infra) bị buộc cùng 5 framework stacks (.NET, Spring Boot, React, Angular, React Native) — hai trục routing hoàn toàn khác nhau. Hệ quả: prompt "Spring Boot REST" sẽ kéo cả pack có search/storage chẳng liên quan, và prompt "S3 signed URL" có thể **bị bỏ qua** vì description nghe nặng về frameworks.
5. **Eval coverage mỏng và 1 chiều**: 15 routing cases + 9 banking cases, **không có** anti-pattern eval (prompt nên KHÔNG kích hoạt pack X), token-budget eval, regression eval, hoặc ambiguity eval. `should_not_activate` chỉ liệt kê 1 pack lẻ — quá yếu để bắt false-positive.

### Top 5 điểm mạnh

1. **Posture enterprise/regulated rất tốt**: idempotency, audit, reconciliation, expand-contract, signed URL, legal hold đều là first-class. Banking/insurance benchmark thực tế (10 prompts tiếng Việt rất sát ngữ cảnh).
2. **Few-shot example payment idempotency** trong agent là exemplar — đúng shape (decision → packs consulted → assumptions → contract → rejected → tests → ops → open questions). Đây là phần đáng giữ nhất trong agent.
3. **Triage 6-bước bắt buộc** ở đầu agent là cấu trúc routing cứng, ép phân loại role/risk/sensitivity trước khi trả lời.
4. **Pack frontmatter đã có `Use when` triggers** — đúng convention Copilot description-based selection. Không pack nào có description rỗng.
5. **`instructions/*.instructions.md` nghiêm túc**: có rule "5-line duplication threshold" trong agent, có decision-matrix preference, có delegation-skill exception (`observability-and-sre`). Đây là maintenance discipline tốt hiếm thấy.

---

## 2. Critical Problems

### CP-1. Boilerplate trùng lặp 7x giữa các pack

- **Vấn đề**: `Purpose` (4 dòng), `Routing Rules` (4 dòng), `Reference Selection Matrix` (header + N dòng filler), `Expected Output Style` (4 dòng), `Token Efficiency Rules` (4 dòng), `Quality Gates` (4 dòng) — tất cả 7 packs có nội dung gần như identical, chỉ thay tên pack.
- **Tại sao quan trọng**: Khi 1 pack được kích hoạt, ~30 dòng noise được nạp vào context. Khi 3 packs cùng kích hoạt (kịch bản phổ biến cho banking prompts: bằng chứng eval `banking-001` mong đợi 5 packs), Copilot phải nuốt ~150 dòng trùng lặp mà 0 tăng signal.
- **Triệu chứng thực tế**: Agent có xu hướng paste lại "expected output style" hoặc "quality gates" vào response (vì nó được nhắc 5 lần trong context). Token cost tăng cho mỗi multi-pack request.
- **Fix**: Trích boilerplate vào **1 file dùng chung** `skills/_shared/PACK-CONVENTIONS.md` (hoặc `instructions/pack-conventions.instructions.md`), mỗi pack chỉ giữ: `frontmatter` + `When to Use` (triggers) + `Pack Reference Map` + `Reference Selection Matrix` (RIÊNG, không filler) + `Cross-pack handoffs`. Mục tiêu mỗi `SKILL.md` ≤ 35 dòng, ≤ 500 tokens.

### CP-2. `Reference Selection Matrix` là filler tautological

- **Vấn đề**: Cột "Selection rule" của mọi reference chỉ ghi `"Read references/X.md when this exact subdomain is material to the answer."` — không có ngôn ngữ trigger phân biệt.
- **Tại sao quan trọng**: Phần được kỳ vọng là "load reference đúng" trở thành noise. Agent không có heuristic phân biệt giữa `data-modeling` vs `database-architecture` vs `sql-and-query-optimization` — 3 reference rất dễ nhầm.
- **Triệu chứng thực tế**: Hoặc nạp **tất cả** references trong pack ("để chắc"), hoặc nạp **tùy hứng** dựa trên keyword bề mặt, dẫn đến token bloat hoặc miss context.
- **Fix**: Thay mỗi dòng bằng trigger thật, ví dụ:
  - `data-modeling`: "Use when defining aggregates, source-of-truth boundaries, history/SCD, derived state ownership, or domain invariants."
  - `database-architecture`: "Use when SELECTING database family/topology, partitioning, replication, or workload-fit reasoning across access patterns."
  - `sql-and-query-optimization`: "Use when a specific query/ORM call is slow, locking, or has a bad plan — focus on EXPLAIN, indexes, statistics."

### CP-3. Principal agent ~2.4–2.8k tokens, vượt budget 2x, lặp luật 3–4 lần

- **Vấn đề**: Cùng "messaging cần ordering/idempotency/retry/DLQ" được phát biểu trong: Operating Rule #8, Cross-Cutting table dòng 169, Default Review Lens "Messaging", Production Stop Condition #2, Prohibited Behavior #4. Tổng cộng **5 lần**. Caching/security/database/monitoring tương tự.
- **Tại sao quan trọng**: Agent file luôn được nạp đầu mỗi conversation — token cost cao nhất hệ thống. Lặp luật cũng làm Copilot ưu tiên paraphrase luật thay vì trả lời câu hỏi.
- **Triệu chứng thực tế**: Response dài, mở đầu bằng việc liệt kê lại 5–8 nguyên tắc (đặc biệt khi prompt ngắn). "Boilerplate-output bias".
- **Fix**: Gộp thành 1 bảng duy nhất `Production Bar` (1 hàng/concern, 4 cột: Concern | Minimum bar | Stop if missing | Pack/reference). Xóa `Default Review Lenses`, `Production Stop Conditions`, `Prohibited Behavior` (tất cả được suy ra từ bảng đó). Mục tiêu agent ≤ 150 dòng, ≤ 1.2k tokens.

### CP-4. `storage-search-stack-pack` đóng gói 2 domain không liên quan

- **Vấn đề**: Pack chứa: `file-and-object-storage`, `search-and-indexing` (cross-cutting infra) **+** `dotnet-development`, `java-spring-boot-development`, `reactjs-development`, `angular-development`, `react-native-development` (framework-specific). Description: *"object/file storage, search/indexing, or framework-specific implementation for .NET, Spring Boot, React, Angular, or React Native"* — trigger trộn 2 chiều.
- **Tại sao quan trọng**:
  - Routing kém: prompt "Implement Spring Boot REST with JPA" sẽ kích hoạt cả storage/search noise; prompt "S3 upload with virus scan" có nguy cơ Copilot bỏ qua vì description nghe nặng frameworks.
  - Trùng lặp ngữ cảnh: stack files (130–153 dòng mỗi cái × 5) khi pack được kích hoạt vô tình nạp cả search/object-storage detail.
- **Triệu chứng thực tế**: Eval `stack-001` (Spring Boot) có `should_not_activate: ["analytics-and-warehouse-design"]` — nhưng không kiểm tra `should_not_activate: ["file-and-object-storage", "search-and-indexing"]` (cùng pack). Đây là blind spot.
- **Fix**: **Tách thành 2 packs**:
  - `storage-search-pack`: file/object storage + search/indexing (2 references). Đây là cross-cutting infra cùng họ với `platform-integration-pack`.
  - `application-stacks-pack` (hoặc `framework-stacks-pack`): 5 frameworks. Description trigger thuần "Use when implementing in .NET / Spring Boot / React / Angular / React Native".
  - Việc này nâng tổng số packs lên 8 — chấp nhận được (vẫn ≤ 10, không gây quá tải Copilot).

### CP-5. Eval thiếu anti-pattern, token-budget, regression, ambiguity

- **Vấn đề**: `routing-benchmark.jsonl` có 15 cases, mỗi case chỉ liệt kê 1 pack `should_not_activate` (yếu). `banking-insurance-benchmark.jsonl` 9 cases không có `should_not_activate` cụ thể cho **references trong cùng pack**. Không có:
  - Anti-pattern eval (prompt mơ hồ → expect agent ASK clarification, không jump implementation).
  - Token-budget eval (đo `tokens_in` của packs/references, fail nếu > X).
  - Regression eval (comparison run-to-run trên cùng prompt).
  - Ambiguity/boundary eval (prompt nằm giữa 2 packs, ép chọn).
- **Tại sao quan trọng**: Hệ thống không thể tự xác minh routing đúng. Mọi cải thiện sau này dựa vào REVIEW tự chấm → echo chamber.
- **Triệu chứng thực tế**: REVIEW.md tự cho 9.2/10, nhưng không có dữ liệu kiểm chứng routing thật.
- **Fix**: Bổ sung 4 bộ eval (chi tiết Section 8).

---

## 3. Pack-by-Pack Review

> Mọi pack đều **chia sẻ 6 vấn đề**: boilerplate trùng lặp, `Reference Selection Matrix` là filler, `Purpose` lặp, `Token Efficiency Rules` lặp, `Quality Gates` lặp, `Routing Rules` lặp. Section dưới chỉ liệt kê **vấn đề riêng** của từng pack.

### 3.1 `core-engineering-pack`

- **What works**: Triggers trong `When to Use` cụ thể (acceptance criteria, sync/async, idempotency, refactoring order). 6 references cân đối. Description đúng `Use when`.
- **What is weak**:
  - `When to Use` mới mô tả domain, chưa nói **NÊN gọi reference nào trước trong domain đó** (vd: requirements vs system-design vs api-design).
  - Description quá rộng: "shaping solution architecture" + "reviewing/refactoring" cùng trigger → có thể ăn nhầm các prompt review thuần code (nên chuyển cho dedicated review).
- **Overlap risks**: `solution-architecture` ↔ `system-design` ranh giới nội bộ pack mơ hồ (REVIEW thừa nhận "boundary acceptable"). `api-design` ↔ `platform-integration-pack/api-gateway-and-service-integration` cũng dễ chồng.
- **Routing risks**: Prompt "review this PR" có thể kích hoạt pack này thay vì routing tới pack chuyên biệt theo loại change (data, security, release).
- **Token issues**: 63 dòng, ~80% là boilerplate → giảm xuống 30 dòng được.
- **Rewrite**: Trim boilerplate; viết lại `Reference Selection Matrix` với trigger thật cho 6 references; xóa `Purpose` và `Token Efficiency Rules` (chuyển vào file shared).
- **Move to references**: Không có nội dung deep nào nằm sai chỗ ở pack này (deep material đã ở references đúng cấu trúc).

### 3.2 `data-database-analytics-pack`

- **What works**: Coverage rộng (modeling → DB → SQL → DB ops → pipelines → analytics). REVIEW chấm group 9.5 — references thực sự dày.
- **What is weak**: 
  - 6 references rất khó phân biệt từ pack: `data-modeling` vs `database-architecture` vs `database-reliability-and-operations` triggers lẫn lộn trong `When to Use`.
  - Pack đa năng nhất nhưng vẫn dùng template chung — không tận dụng được structure phụ.
- **Overlap risks**:
  - `data-engineering-and-pipelines` (CDC/replay/backfill) ↔ `platform-integration-pack/messaging-and-eventing` (outbox/inbox/replay) — cả hai nói về replay nhưng từ 2 lớp khác nhau, agent hay nhầm.
  - `analytics-and-warehouse-design` ↔ `storage-search-stack-pack/search-and-indexing` (đặc biệt nếu prompt nói "search analytics on customer data").
- **Routing risks**: Prompt "slow report SQL" có thể kích hoạt cả `sql-and-query-optimization` lẫn `analytics-and-warehouse-design` — không có quy tắc tie-break.
- **Token issues**: Như CP-1.
- **Rewrite**: Thêm bảng "Reference disambiguation" 1 cột "If prompt mentions… → load…" với 6–8 cặp keyword↔reference cụ thể.
- **Move to references**: OK.

### 3.3 `security-access-pack`

- **What works**: Chỉ 2 references (`security-review`, `authn-authz-and-secrets`) — ít risk overlap nội bộ. `security-review` được REVIEW chấm 10/10.
- **What is weak**:
  - **Pack có nguy cơ over-activate**: description "PII, payment data, file upload, external callbacks, abuse cases" rất rộng → gần như mọi banking prompt sẽ kéo nó vào.
  - Không có ngôn ngữ "DON'T use this pack when…" để chặn over-activation.
- **Overlap risks**: `security-review` ↔ `observability-release-pack/logging-metrics-and-tracing` (sensitive logging, redaction) — cùng nói về PII trong logs.
- **Routing risks**: Eval `security-001` đã yêu cầu `observability-release-pack` cho admin endpoint logging PII — confirm overlap có thật.
- **Token issues**: Pack chỉ có 2 references nhưng vẫn 54 dòng boilerplate — pack này có thể ngắn nhất hệ thống nếu trim.
- **Rewrite**: Thêm 1 dòng phân biệt `security-review` (cross-surface audit, multi-path) vs `authn-authz-and-secrets` (concrete identity/token/secret design).
- **Move to references**: OK.

### 3.4 `platform-integration-pack`

- **What works**: 5 references rõ ranh giới (messaging / gateway / rate-limit / workflow / batch). Triggers concrete (outbox, DLQ, sagas, BFF).
- **What is weak**:
  - `workflow-and-job-orchestration` (long-running) ↔ `background-jobs-and-batch-processing` (recurring/batch) — ranh giới chỉ "long-running" vs "scheduled", agent dễ chọn sai.
  - Description không phân biệt **inbound** (gateway/BFF) vs **outbound** (partner integration) — 2 luồng có rule khác nhau.
- **Overlap risks**: `messaging-and-eventing` ↔ `data-database-analytics-pack/data-engineering-and-pipelines` (event streaming + CDC); `api-gateway-and-service-integration` ↔ `resilience-performance-pack/resilience-and-fault-tolerance` (timeout/circuit ở gateway).
- **Routing risks**: Eval `platform-001` kỳ vọng CHỈ `platform-integration-pack` cho prompt "Kafka outbox/replay" — nhưng prompt này thực tế cũng cần `data-database-analytics-pack` (outbox table = DB design) và `observability-release-pack` (DLQ alerting). Eval đang **dạy sai routing**.
- **Token issues**: Như CP-1.
- **Rewrite**: Bảng disambiguation cho 5 references; bổ sung `See Also: data → CDC pipelines, observability → DLQ alerts`.
- **Move to references**: OK.

### 3.5 `resilience-performance-pack`

- **What works**: Chỉ 3 references — bound nhỏ, ít confusion. Triggers (p95, stampede, circuit breaker) đủ specific.
- **What is weak**:
  - `caching-and-distributed-state` đặt ở pack này thay vì `data-database-analytics-pack` là quyết định debatable — caching cũng là **stateful storage choice**.
  - `performance-engineering` vs `resilience-and-fault-tolerance` triggers chồng (cả hai dùng "throughput", "queue lag").
- **Overlap risks**: `caching-and-distributed-state` ↔ `security-access-pack/security-review` (cache authorization safety); `resilience-and-fault-tolerance` ↔ `platform-integration-pack/api-gateway-and-service-integration` (gateway-level circuit breaker).
- **Routing risks**: Prompt "Redis session storage" có thể đi sang `data-database-analytics-pack` thay vì pack này.
- **Token issues**: Như CP-1.
- **Rewrite**: Khẳng định caching ở đây = **runtime cache + distributed state** (KHÔNG phải primary storage). Thêm cross-link rõ với data pack.
- **Move to references**: OK.

### 3.6 `observability-release-pack`

- **What works**: 4 references theo chuỗi telemetry → SLO → SRE readiness → release. `observability-and-sre` cố ý là delegation skill — design discipline tốt.
- **What is weak**:
  - Pack ghép **observability** + **release** — 2 lifecycle khác nhau. Một prompt "design canary rollout" và "design dashboards" dùng cùng pack nhưng workflow khác hoàn toàn.
  - Description liệt kê 12 keywords trong 1 câu — quá tải, mất focus.
- **Overlap risks**: `monitoring-alerting-and-slos` ↔ `logging-metrics-and-tracing` (đều nói về metrics) — REVIEW thừa nhận overlap "controlled" nhưng vẫn tồn tại.
- **Routing risks**: Prompt "incident response runbook" — không rõ rơi vào `observability-and-sre` hay `monitoring-alerting-and-slos`.
- **Token issues**: Như CP-1.
- **Rewrite**: Cân nhắc tách `release-pack` riêng (chỉ chứa `devops-and-release` + tương lai `feature-flags`, `progressive-delivery`); giữ `observability-pack` cho 3 references còn lại. Hoặc giữ ghép nhưng viết rõ **"2 trục trong cùng pack: telemetry trục dọc + release trục ngang"**.
- **Move to references**: OK; `devops-and-release.md` (318 dòng) **OK** vì là deep playbook đúng vị trí.

### 3.7 `storage-search-stack-pack` ⚠️ **NÊN TÁCH**

- **What works**: Coverage stack đầy đủ; mỗi reference đạt floor 130 dòng.
- **What is weak**: **CP-4** — 2 trục routing trộn lẫn.
- **Overlap risks**: `search-and-indexing` ↔ `data-database-analytics-pack/analytics-and-warehouse-design`; `file-and-object-storage` ↔ `security-access-pack/security-review` (signed URL auth).
- **Routing risks**: Prompt thuần framework ("React state management") sẽ thừa nạp storage/search; prompt thuần storage ("S3 lifecycle policy") có thể bị bỏ qua vì description nặng về frameworks.
- **Token issues**: Pack có 7 references — nhiều nhất hệ thống. SKILL.md vẫn boilerplate, nhưng nguy cơ thật là **phía references**: nếu Copilot nạp 2–3 stack files cùng lúc (vd: monorepo full-stack), tổng tokens vọt lên ~3k.
- **Rewrite**: **Tách 2 pack** như CP-4. Sau khi tách:
  - `storage-search-pack`: 2 references (storage, search). SKILL.md cực ngắn (~25 dòng).
  - `application-stacks-pack`: 5 references frameworks. Bảng "Use stack X when…" rõ ràng.
- **Move to references**: Không cần move; chỉ cần re-pack.

---

## 4. Agent Review (`agents/ce7-software-engineering.agent.md`)

### Routing quality — 6/10

- **Mạnh**: Mandatory triage 6 bước; bảng `Cross-Cutting Platform Routing` 22 hàng map từ concern → pack/reference.
- **Yếu**:
  - `Mission` list 24 bullet là domain labels — không route đi đâu, chỉ là noise.
  - `Skill Routing` section liệt kê 7 packs với toàn bộ 33 references inline — biến agent thành sitemap, không phải router. Nên giữ MAP từ trigger keyword → pack, không phải liệt kê tất cả references.
  - Không có quy tắc **tie-break** khi 2+ packs match (vd: outbox = data + platform).
  - Không có ngôn ngữ "DO NOT activate pack X when…".

### Role clarity — 7/10

- **Mạnh**: "Panel of senior specialists, not generic coding assistant" — định nghĩa thân phận rõ.
- **Yếu**: Vai trò "router" và "panel reviewer" lẫn nhau — agent vừa route vừa tự đưa luật. Nên CHỌN 1: nếu là router thì để pack tự đưa luật; nếu là panel thì gộp packs và bỏ progressive disclosure.

### Bloat risk — RẤT CAO

- **Số liệu**:
  - 320 dòng / ước ~2.4–2.8k tokens.
  - Lặp 4 lớp luật cho cùng concerns (CP-3).
  - Few-shot example: ~50 dòng (đáng giữ, nhưng đang là 1/6 toàn bộ agent).
- **Khuyến nghị**: Cắt xuống ~150 dòng / ≤ 1.2k tokens.

### Missing review lenses

- **Cost / FinOps**: Có nhắc 1 dòng trong "Default Review Lenses" nhưng không có pack — nên có pack hoặc reference riêng (P4 trong REVIEW đã đề cập).
- **Compliance/regulatory mapping** (PCI, SOX, GDPR, ISO 27001): hoàn toàn implicit. Banking/insurance posture nói "audit" nhưng không gắn mapping rõ.
- **Incident response / postmortem**: REVIEW liệt kê P4 nhưng vẫn chưa có; với hệ regulated đây là gap thật.
- **Architecture Decision Records (ADR)**: chỉ đề cập trong `solution-architecture` reference — nên có lens riêng.
- **AI/ML production** (model serving, drift, eval): hoàn toàn vắng — nếu out-of-scope, cần nói rõ.

### Missing output contracts

- Các "Output Behavior by Task Type" section định nghĩa shape cho 3 task types — tốt, nhưng:
  - Không có **counter-example** (cái không nên trả lời).
  - Không có schema/JSON contract (chỉ là markdown headings) → không testable bằng eval tự động.
  - Không có "minimum acceptable" vs "ideal" — agent có xu hướng luôn xuất full 12-section ngay cả khi prompt nhỏ.

### Recommendations

- **Must change**: Cắt agent xuống ≤ 1.2k tokens (gộp 4 lớp luật → 1 bảng `Production Bar`; xóa `Mission` list; xóa `Prohibited Behavior` (đã suy được từ Operating Rules)).
- **Should change**: Thêm `Tie-Breaking Rules` (3–5 dòng) cho cặp pack hay xung đột.
- **Optional**: Thêm 2 few-shot example ngắn (debugging + review) bên cạnh architecture example đã có.

---

## 5. Token Efficiency Review

| Hạng mục | Tokens hiện tại (ước) | Target | Chênh |
|---|---:|---:|---:|
| Principal agent | ~2.4–2.8k | ≤ 1.2k | **-50–60%** |
| Mỗi pack `SKILL.md` | ~600–700 | ≤ 500 (tốt nhất ≤ 350) | **-30–50%** |
| Mỗi reference (median) | ~1.0–1.5k | ≤ 1.2k | OK với hầu hết, **trim** `devops-and-release` (318 dòng) và `database-architecture` (218) |
| Mỗi pack có 5 references nạp cùng lúc | ~6k | ≤ 4k | -33% |

### Nên GIỮ trong agent

- Mandatory triage 6 bước (signal cao, không trùng).
- Skill Routing **rút gọn**: 7 dòng (1 dòng/pack, không liệt kê references).
- 1 bảng `Production Bar` thay 4 lớp luật.
- 1 few-shot example (giữ payment idempotency, có thể trim 30%).

### Nên CHUYỂN từ agent → packs

- 22-row `Cross-Cutting Platform Routing` table → biến mỗi hàng thành **trigger trong `When to Use` của pack tương ứng**.
- `Default Review Lenses` 13 mục → tự động phát sinh từ packs đã activate, không cần liệt kê tĩnh.

### Nên CHUYỂN từ packs → file shared (hoặc instructions)

- 6 section boilerplate (`Purpose`, `Routing Rules`, `Expected Output Style`, `Token Efficiency Rules`, `Quality Gates`) → 1 file `instructions/pack-conventions.instructions.md` có `applyTo: 'skills/**/SKILL.md'`. Maintainer đọc 1 lần, runtime không cần nạp.

### Nên CHUYỂN từ packs → references

- Hiện tại đã làm tốt — không có deep material kẹt ở pack level.

### Nên CHUYỂN vào instructions

- "Stack-specific must remain framework-focused, route broader concerns out" — đã ở `principal-skills-maintenance.instructions.md`. OK.
- "External research adoption discipline" — đã có. OK.

### Nên XÓA hẳn

- `Reference Selection Matrix` filler (sau khi viết lại với trigger thật, không phải xóa toàn bảng — xóa **format hiện tại**).
- `Prohibited Behavior` trong agent (suy được từ Operating Rules + Production Stop Conditions).
- `Mission` 24-bullet list trong agent (chỉ là domain labels).
- `README.md` 354 dòng — tách thành `README.md` (≤ 100 dòng overview) + `docs/INSTALL.md` + `docs/PIPELINE.md` (đã có 1 phần). Phần "Documentation Map" đang trùng với phần "Installation Map" trùng với "Hybrid Pack Mapping".
- Eval `routing-benchmark.jsonl` line 16 (dòng trống cuối) — minor.

---

## 6. Recommended Structural Changes

### 6.1 Must change now (P0)

1. **Trim agent xuống ≤ 1.2k tokens**: gộp 4 lớp luật, xóa `Mission`, xóa `Prohibited Behavior`, rút `Skill Routing` còn 7 dòng. *(file: `agents/ce7-software-engineering.agent.md`)*
2. **Tách boilerplate 7 packs vào 1 file shared**: tạo `skills/_shared/PACK-CONVENTIONS.md` (hoặc inline vào maintenance instructions) — mỗi pack chỉ giữ frontmatter + `When to Use` + `Pack Reference Map` + `Reference Selection Matrix` (rewritten) + `Cross-pack handoffs`. *(file: 7 × `skills/<pack>/SKILL.md`)*
3. **Viết lại `Reference Selection Matrix` mỗi pack** với trigger thật (1 câu/reference, bắt đầu bằng "Use when…"). *(7 packs)*
4. **Tách `storage-search-stack-pack` thành 2 packs** (`storage-search-pack` + `application-stacks-pack`). Update `validate_hybrid_packs.py` (đang hard-code 7 packs → 8). *(8 file changes: 1 split + script + agent + README + 5 evals)*
5. **Bổ sung anti-pattern + token-budget evals** (Section 8). *(evals/)*

### 6.2 Should change next (P1)

1. **Disambiguation table mỗi pack**: 1 bảng nhỏ "If prompt mentions X → load reference Y" cho ≥ 4 cặp dễ nhầm.
2. **Tie-break rules trong agent**: 3–5 dòng cho các cặp hay xung đột (data ↔ platform về outbox; security ↔ observability về PII logging; storage ↔ stack về storage-in-app-code).
3. **Thêm 2 few-shot example ngắn** (implementation/debug + review) trong agent hoặc `examples/` folder.
4. **Tạo `examples/` folder** với 3 sample outputs (architecture, debugging, review) — đã được REVIEW liệt kê P4.
5. **Bổ sung references còn thiếu**: `incident-response-and-postmortem` (vào `observability-release-pack`), `architecture-decision-records` (vào `core-engineering-pack`), `cost-and-finops` (vào pack mới hoặc `resilience-performance-pack`).

### 6.3 Optional later (P2)

1. **Pack `release-pack` tách khỏi `observability-pack`** (nếu nhu cầu release tăng).
2. **`AGENTS.md` ở root** dành cho human contributors (ngắn, ≤ 80 dòng), thay phần install dài trong README.
3. **Schema JSON cho expected output** (machine-checkable shape).
4. **Rút `README.md` xuống ≤ 100 dòng**, push install/pipeline vào `docs/`.
5. **Cân nhắc xóa `agents/skill-evaluator.agent.md`** nếu đã có script `validate_hybrid_packs.py` + scoring rubric — đang chồng lấn 70%.

---

## 7. Concrete Rewrite Plan (priority-ordered)

| # | File | Reason | Change type | Expected impact |
|---:|---|---|---|---|
| 1 | `agents/ce7-software-engineering.agent.md` | Bloat 2x budget, lặp 4 lớp luật | **Rewrite** xuống ≤ 150 dòng | -55% tokens agent; routing rõ hơn |
| 2 | `skills/<7 packs>/SKILL.md` | Boilerplate 280 dòng trùng | **Trim** + **Move boilerplate to shared** | -50% tokens/pack; eliminate echo |
| 3 | `skills/<7 packs>/SKILL.md` `Reference Selection Matrix` | Filler tautological | **Rewrite** với trigger thật | Reference precision tăng đáng kể |
| 4 | `skills/storage-search-stack-pack/` | Ghép 2 trục routing | **Split** thành 2 packs | False-activation giảm; routing chính xác cho stack prompts |
| 5 | `scripts/validate_hybrid_packs.py` | Hard-code 7 packs | **Edit** thành 8 packs | Validator pass với cấu trúc mới |
| 6 | `evals/routing-benchmark.jsonl` | 1 chiều, thiếu negative | **Add** 10 anti-pattern + 8 ambiguity cases | Routing testable |
| 7 | `evals/token-budget.jsonl` (mới) | Không tồn tại | **Add** | Token bloat detectable |
| 8 | `evals/regression.jsonl` (mới) | Không tồn tại | **Add** | Regression detectable |
| 9 | `agents/ce7-software-engineering.agent.md` | Thiếu tie-break rules | **Add** section 5 dòng | Cross-pack ambiguity giảm |
| 10 | `instructions/pack-conventions.instructions.md` (mới) | Boilerplate cần nơi cư trú | **Add** với `applyTo: 'skills/**/SKILL.md'` | Maintainer 1-source-of-truth |
| 11 | `examples/{architecture,debugging,review}.md` (mới) | Few-shot chỉ có 1 trong agent | **Add** 3 file | Output contract dễ tham chiếu |
| 12 | `agents/skill-evaluator.agent.md` | Trùng 70% với rubric + script | **Merge** vào `docs/skill-pack-quality-rubric.md` hoặc **Delete** | -1 agent file maintain |
| 13 | `README.md` | 354 dòng, trùng nhiều | **Trim** xuống ≤ 100 dòng | Onboarding nhanh hơn |
| 14 | `skills/observability-release-pack/references/devops-and-release.md` | 318 dòng (lớn nhất hệ thống) | **Trim** xuống ≤ 220 dòng (tách "Worked Example" sang file riêng nếu cần) | -30% reference tokens |
| 15 | `REVIEW.md` | Tự chấm 9.2/10 không có evidence | **Rewrite** sau khi chạy eval mới với điểm thực | Trust calibration |

---

## 8. Evals Plan (minimal but strong)

### 8.1 Routing evals (mở rộng từ 15 → ~35 cases)

Thêm:

- **Boundary cases (8 prompts)**:
  - `boundary-001`: "Outbox pattern table schema and consumer dedupe" → expect BOTH `data-database-analytics-pack` (table) + `platform-integration-pack` (consumer) + `observability-release-pack` (DLQ alert). Hiện eval `platform-001` đang sai.
  - `boundary-002`: "Redis cluster sizing for cache + session" → expect `resilience-performance-pack` (cache) + `data-database-analytics-pack` (sizing/storage). Test phân biệt cache vs primary store.
  - `boundary-003`: "S3 signed URL with virus scan callback" → expect `storage-search-pack` + `security-access-pack` + `platform-integration-pack` (callback).
  - `boundary-004`: "Sensitive logs masking in checkout pipeline" → expect `security-access-pack` + `observability-release-pack/logging-metrics-and-tracing`. Bắt overlap có chủ đích.
  - `boundary-005`–`008`: thêm 4 cặp pack hay nhầm.
- **Ambiguity-resolve cases (4 prompts)**: prompt cố tình mơ hồ → expect agent ASK clarification trước khi route.

### 8.2 Anti-pattern evals (10 cases) — MỚI

Mỗi case có `must_not_do`:

- `anti-001`: "Just retry the failed payment" → must_not_do: `["recommend retry without idempotency design"]`.
- `anti-002`: "Add Redis cache to fix latency" → must_not_do: `["recommend cache without staleness/invalidation/auth-safety"]`.
- `anti-003`: "Add monitoring to this endpoint" → must_not_do: `["recommend metrics without owner/runbook/threshold"]`.
- `anti-004`: "Pick MongoDB" → must_not_do: `["recommend DB without workload-fit reasoning"]`.
- `anti-005`: "Deploy this migration tonight" → must_not_do: `["recommend release without rollback/expand-contract/SLO gate"]`.
- `anti-006`: "Build a search-based customer 360" → must_not_do: `["treat search index as source of truth"]`.
- `anti-007`–`010`: thêm 4 anti-pattern phổ biến.

### 8.3 Token-budget evals — MỚI

File `evals/token-budget.jsonl`:

- Mỗi pack: max tokens cho `SKILL.md` (= 500), max khi nạp 3 references (= 4500), max agent context (= 1200).
- Script đo, fail nếu vượt 10%.

### 8.4 Production-readiness evals (5 cases)

Tái dùng banking/insurance prompts, score theo `scoring-rubric.md` nhưng FAIL nếu thiếu:
- migration sequencing,
- idempotency on money movement,
- audit evidence schema,
- rollback path,
- operator repair runbook.

### 8.5 Regression evals — MỚI

- Hash output của 8 "golden prompts" (subset routing + banking).
- Compare run-to-run; flag bất kỳ degradation > 5%.
- Đã có `scripts/regression_check.py` (changelog ghi nhận) — viết test cases cho nó.

---

## 9. Redlines / Draft Improvements

### 9.1 Principal agent — **đề xuất rewrite hoàn toàn xuống ~140 dòng**

Sẽ cung cấp khi user bật Edit mode. Khung gồm:

1. Frontmatter (4 dòng).
2. Identity (3 dòng): "Principal-level engineering panel; routes to packs; never duplicates pack content."
3. Mandatory Triage (giữ nguyên 6 bước, ~12 dòng).
4. **Production Bar** (1 bảng duy nhất, 8 hàng × 4 cột: Concern | Minimum bar | Stop if missing | Pack/reference). Thay thế Operating Rules + Default Review Lenses + Cross-Cutting Routing + Production Stop Conditions + Prohibited Behavior.
5. Skill Routing (7 dòng, 1 dòng/pack, KHÔNG liệt kê references):
   ```
   - core-engineering-pack — requirements, architecture, API, tests, review
   - data-database-analytics-pack — data, DB, SQL, pipelines, analytics
   - security-access-pack — identity, authz, secrets, sensitive data, abuse
   - platform-integration-pack — messaging, gateway, workflow, jobs, batch
   - resilience-performance-pack — caching, distributed state, latency, throughput
   - observability-release-pack — telemetry, SLO, runbook, CI/CD, rollout
   - storage-search-pack — object storage, search/indexing
   - application-stacks-pack — .NET, Spring Boot, React, Angular, RN
   ```
6. **Tie-Break Rules** (5 dòng, MỚI): outbox = data + platform; PII logging = security + obs; cache vs store = resilience (runtime cache) vs data (durable); gateway circuit = platform (policy) vs resilience (pattern); search index ≠ source of truth → data + storage-search both.
7. Output structures (3 task types, 1 dòng each pointing to `examples/<type>.md`).
8. 1 few-shot reference: "See `examples/architecture-payment-idempotency.md`".

### 9.2 Pack `SKILL.md` template — **đề xuất rewrite tất cả 7 (sẽ là 8)**

Template ngắn (~30 dòng/pack):

```markdown
---
name: <pack-name>
description: 'Use when <concrete trigger keywords> — distinct from <neighbor-pack> which owns <X>.'
---
# <Pack Title>

## When to Use
- <concrete trigger 1>
- <concrete trigger 2>
- <concrete trigger 3>

## When NOT to Use
- <anti-trigger 1, points to neighbor pack>
- <anti-trigger 2>

## Pack Reference Map
| Reference | Use when |
|---|---|
| `<ref-1>` | Use when <distinct trigger 1> |
| `<ref-2>` | Use when <distinct trigger 2> |
| ... | ... |

## Cross-Pack Handoffs
- → `<other-pack>` for <concern>
- → `<other-pack>` for <concern>

> Pack conventions (output style, quality gates, token rules) live in `instructions/pack-conventions.instructions.md`.
```

### 9.3 Hai pack yếu nhất cần rewrite full

#### A. `storage-search-stack-pack` → **SPLIT**

**`storage-search-pack/SKILL.md`** (draft):

```markdown
---
name: storage-search-pack
description: 'Use when designing object/file storage (uploads, signed URLs, retention, legal hold, virus scan) or search/indexing (projection sync, relevance, authorization filtering, reindex). NOT for in-application stack code — see application-stacks-pack.'
---
# Storage and Search Pack

## When to Use
- Uploads, downloads, signed URLs, document metadata, retention, legal hold, large files, scanning.
- Search projections, index sync, relevance, filters, eventual consistency, aliases, reindex.

## When NOT to Use
- Implementing storage/search calls inside framework code → application-stacks-pack.
- Choosing the primary OLTP database → data-database-analytics-pack.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `file-and-object-storage` | Use when designing upload/download flow, lifecycle, legal hold, scan, or signed-URL contract. |
| `search-and-indexing` | Use when designing projection from source-of-truth into a search index, or reindex/alias strategy. |

## Cross-Pack Handoffs
- → `security-access-pack` for signed-URL authorization, document-level authz, masking.
- → `data-database-analytics-pack` for source-of-truth boundaries and projection lineage.
- → `platform-integration-pack` for upload event/callback handling.
```

**`application-stacks-pack/SKILL.md`** (draft):

```markdown
---
name: application-stacks-pack
description: 'Use when implementing in a specific framework: ASP.NET Core/EF Core, Spring Boot/JPA, React (Next/Remix), Angular, or React Native. Routes broader platform concerns OUT to other packs.'
---
# Application Stacks Pack

## When to Use
- Framework-specific patterns (DI, middleware, hooks, signals, RxJS, hydration, navigation, state).
- Stack-specific gotchas (N+1, hydration mismatch, NgZone, OTA, Hermes, RSC).
- Stack-specific tests (xUnit, JUnit/Spring Test, Vitest/Jest/Detox/Maestro).

## When NOT to Use
- Cross-cutting platform design (messaging, caching, security, storage, search, observability) → respective platform pack.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `dotnet-development` | Use when writing .NET / ASP.NET Core / EF Core code. |
| `java-spring-boot-development` | Use when writing Spring Boot / JPA / Spring Cloud code. |
| `reactjs-development` | Use when writing React / Next.js / Remix / Vite frontend. |
| `angular-development` | Use when writing Angular (standalone, signals, RxJS). |
| `react-native-development` | Use when writing React Native (Expo or bare, New Architecture). |

## Cross-Pack Handoffs
- → `core-engineering-pack` for API contract / testing strategy.
- → `platform-integration-pack` for messaging / gateway integration in the app.
- → `resilience-performance-pack` for caching / timeouts / circuit in the app.
- → `security-access-pack` for authn/authz wiring in the app.
- → `observability-release-pack` for telemetry wiring in the app.
```

#### B. `data-database-analytics-pack` rewrite (rút gọn boilerplate, viết lại Selection Matrix)

```markdown
---
name: data-database-analytics-pack
description: 'Use when modeling domain data, choosing a database, optimizing SQL/ORM, operating production DBs, building pipelines (ETL/ELT/CDC), or designing analytics/warehouse consumption.'
---
# Data, Database, and Analytics Pack

## When to Use
- Aggregates, source-of-truth, history/SCD, audit, transactional boundaries, derived state.
- DB family/topology selection, partitioning, replication, scaling, retention.
- Slow query, bad plan, lock contention, ORM N+1, pagination at scale.
- Backup/restore, failover drill, schema migration coordination.
- ETL/ELT/CDC, replay, backfill, data quality, lineage.
- Marts, semantic layer, BI cost, governed metrics.

## When NOT to Use
- Runtime cache or distributed state → resilience-performance-pack.
- Search index design (even on top of DB) → storage-search-pack.
- Outbox CONSUMER side / replay protocol → platform-integration-pack.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `data-modeling` | Use when defining aggregates, source-of-truth ownership, SCD/history, derived-state rules, or domain invariants. |
| `database-architecture` | Use when CHOOSING a database family or topology with workload-fit reasoning across access patterns. |
| `sql-and-query-optimization` | Use when a SPECIFIC query/ORM call is slow, locking, or has a bad plan — focus on EXPLAIN, indexes, statistics. |
| `database-reliability-and-operations` | Use when planning backup/restore, failover, schema migration sequencing, or DB incident response. |
| `data-engineering-and-pipelines` | Use when designing ETL/ELT/CDC, replay/backfill, idempotent sinks, or data-quality controls. |
| `analytics-and-warehouse-design` | Use when designing facts/dimensions, semantic layer, governed metrics, or BI consumption. |

## Cross-Pack Handoffs
- → `platform-integration-pack` for outbox consumer / DLQ / replay protocol.
- → `observability-release-pack` for migration release safety + DB SLOs.
- → `security-access-pack` for row-level / tenant authz / sensitive column masking.
```

### 9.4 `instructions/pack-conventions.instructions.md` — **MỚI** (chứa boilerplate đã trích)

```markdown
---
description: 'Shared conventions for all pack SKILL.md files. Maintainer-only; NOT loaded at runtime.'
applyTo: 'skills/**/SKILL.md'
---
# Pack Conventions

## Output Style (applies to all packs)
- Decision first, reasoning second.
- Name references consulted when work is non-trivial.
- Separate immediate action / trade-offs / tests / ops / follow-up.
- Concrete: contracts, schemas, gates, examples — not generic advice.

## Token Efficiency (applies to all packs)
- Pack = metadata + routing. References = progressive disclosure.
- Do not paste large reference content into responses.
- If > 3 references seem necessary, name the primary one and justify each extra.

## Quality Gates (applies to all packs)
- Selected references match user's actual risk and task.
- Security, data, observability, delivery, failure handling addressed when material.
- Recommendations testable; rejected options have a stated reason.
```

---

## 10. Phụ lục: Quan sát phụ

- **Bilingual `.vi-VN.md` cho mọi doc** là điểm cộng cho onboarding VN, nhưng nhân đôi maintenance burden — cân nhắc dịch tự động hoặc giữ chỉ phần "intro + commands" song ngữ.
- **`memory/`, `runs/`, `reports/`** thư mục có nhưng không thấy schema chuẩn ở review này — nếu là sample data, nên có `.gitignore` rule rõ.
- **`scripts/regression_check.py`** đã tồn tại nhưng không có test cases trong eval — phối hợp với P1.5 (regression evals).
- **`docs/skill-pack-quality-rubric.md`** và `agents/skill-evaluator.agent.md` chồng lấn 70%; chọn 1.

---

**Kết luận**: Hệ thống có **posture enterprise rất tốt** và **discipline maintenance trên trung bình**, nhưng đang **vượt 2x token budget ở agent** và **lặp ~280 dòng boilerplate ở packs**. Nếu thực thi đầy đủ P0 (5 việc) trong 1 sprint, có thể đạt:

- Agent: -55% tokens
- Packs: -50% tokens trung bình
- Routing precision: +20–30% (nhờ Selection Matrix có trigger thật + storage/stack tách)
- Eval coverage: từ 15 → ~50 cases với 4 trục mới

Đề nghị **giảm điểm tự đánh giá REVIEW.md** từ 9.2 xuống thực tế ~7.0 cho đến khi có dữ liệu eval mới.

