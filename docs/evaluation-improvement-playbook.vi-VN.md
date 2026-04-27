# Playbook đánh giá và cải tiến CE7 Agent / Skill Packs

**Mục tiêu:** giúp bạn đánh giá chất lượng agent + skills một cách lặp lại được, biết nên cải tiến chỗ nào, và tránh làm hệ thống phình token.

## 1. Nguyên tắc vận hành

CE7 hiện dùng kiến trúc **Copilot-first hybrid packs**:

- Copilot thấy **7 pack skills** ở `.github/skills/*/SKILL.md`.
- 33 leaf skills cũ nằm trong `references/*.md`.
- Agent chính `ce7-software-engineering` route theo pack trước, reference sau.
- `skill-evaluator` đánh giá trigger, routing, overlap, token efficiency, output quality và originality.

Điểm quan trọng: **không cải tiến bằng cách thêm thật nhiều nội dung vào pack**. Cải tiến tốt thường là:

1. trigger rõ hơn;
2. route đúng hơn;
3. benchmark bắt lỗi tốt hơn;
4. reference được chọn chính xác hơn;
5. output có evidence/test/operation checklist tốt hơn;
6. token ít hơn cho cùng chất lượng.

## 2. 5 lớp đánh giá

### Layer 1 — Structural validation

Chạy deterministic checks trước mọi review:

```bash
python3 scripts/validate_hybrid_packs.py
```

Validator kiểm tra:

- đúng 7 peer pack skills;
- đúng 33 references;
- chỉ có 2 agents hiện tại;
- chưa thêm deferred agents;
- `.github/skills` và root `skills` đúng cấu trúc;
- benchmark corpus tồn tại;
- external research/rubric tồn tại;
- pack descriptions dùng `Use when`;
- pack không vượt line budget.

**Fail ở layer này thì chưa review semantic.** Sửa cấu trúc trước.

### Layer 2 — Routing benchmark

Dùng `evals/routing-benchmark.jsonl` để kiểm tra:

- prompt nên activate pack nào;
- reference nào cần mở;
- pack/reference nào không nên activate;
- prompt cross-domain có route hợp lý không.

Mỗi benchmark row nên có:

```json
{
  "id": "security-001",
  "prompt": "Review an admin endpoint that changes customer email and logs PII.",
  "expected_packs": ["security-access-pack", "observability-release-pack"],
  "expected_references": ["security-review", "authn-authz-and-secrets", "logging-metrics-and-tracing"],
  "should_not_activate": ["data-database-analytics-pack"]
}
```

Mục tiêu:

- giảm false positive: pack bị mở sai;
- giảm false negative: pack cần mà không mở;
- giảm reference bloat: mở quá nhiều references.

### Layer 3 — Semantic answer quality

Cho `skill-evaluator` chấm output trên cùng benchmark prompt.

Score 0–5 cho các chiều:

| Dimension | Câu hỏi đánh giá |
|---|---|
| Correctness | Câu trả lời có đúng vấn đề và domain không? |
| Principal judgment | Có nêu trade-off, rejected options, rủi ro không? |
| Evidence discipline | Có yêu cầu baseline, logs, metrics, tests, threat model, execution plan không? |
| Production readiness | Có migration, rollback, observability, owner, runbook không? |
| Security/data safety | Có authz, tenant isolation, audit, sensitive logging, PII không? |
| Testability | Acceptance criteria/test cases có kiểm chứng được không? |
| Actionability | Team có thể làm theo ngay không? |
| Brevity | Có đủ nhưng không dài lan man không? |

### Layer 4 — Token efficiency

Đánh giá token theo hành vi, không chỉ line count.

| Metric | Good | Bad |
|---|---|---|
| Pack activation count | 1 pack mặc định, 2–3 nếu cross-domain | 4+ packs cho prompt bình thường |
| Reference count | 0–2 references thường, 3 khi phức tạp | mở toàn bộ references |
| Pack body size | dưới 220 lines | pack biến thành tutorial |
| Answer style | synthesized rules + exact references | paste nguyên đoạn reference |
| Repetition | route ngắn, không lặp platform rules | cùng một paragraph xuất hiện nhiều pack |

### Layer 5 — Regression history

Sau mỗi lần benchmark, ghi lại vào:

```text
reports/latest-skill-eval.md
reports/skill-eval-history.jsonl
```

Bạn cần biết chất lượng đang tăng thật hay chỉ “cảm giác tốt hơn”.

## 3. Scorecard đề xuất

Dùng trọng số này cho mỗi pack hoặc toàn package:

| Dimension | Weight |
|---|---:|
| Trigger accuracy | 20% |
| Reference precision | 15% |
| Output quality | 20% |
| Evidence / validation quality | 15% |
| Production safety | 10% |
| Token efficiency | 10% |
| Copilot readiness | 5% |
| Originality / maintainability | 5% |

Cách tính đơn giản:

```text
weighted_score = Σ(score_0_to_5 × weight) × 20
```

Thang điểm:

| Score | Meaning |
|---:|---|
| 90–100 | Excellent / reference-grade |
| 80–89 | Production-ready |
| 70–79 | Usable but needs improvement |
| 60–69 | Risky / needs focused fixes |
| <60 | Not acceptable |

## 4. Quy trình cải tiến chuẩn

### Bước 1 — Chạy validation

```bash
python3 scripts/validate_hybrid_packs.py
```

Nếu fail, sửa cấu trúc trước.

### Bước 2 — Chọn benchmark prompt

Chọn 5–10 prompt đại diện:

- 2 prompt single-pack;
- 2 prompt cross-domain;
- 2 prompt high-risk security/data/release;
- 1 prompt negative activation;
- 1 prompt stack-specific.

### Bước 3 — Chạy qua CE7 agent

Với mỗi prompt, ghi lại:

- pack được route;
- references được mở;
- output cuối;
- số pack/reference bị mở sai;
- thiếu gì trong output.

### Bước 4 — Chấm bằng `skill-evaluator`

Dùng output format của `skill-evaluator`:

1. Verdict: PASS / WARN / FAIL.
2. Scorecard.
3. Structural checks.
4. Routing findings.
5. Token findings.
6. External research findings.
7. Risk-ranked fixes.
8. Regression additions.

### Bước 5 — Chỉ sửa chỗ có evidence

Không sửa pack chỉ vì “có thể hay hơn”. Sửa khi benchmark cho thấy:

- prompt route sai;
- pack description mơ hồ;
- reference thiếu trigger;
- output thiếu evidence/test/rollback/security;
- token bị bloat;
- overlap giữa packs.

### Bước 6 — Re-run validation + benchmark

Sau patch:

```bash
python3 scripts/validate_hybrid_packs.py
```

Sau đó chạy lại prompt đã fail để xác nhận regression được sửa.

## 5. Cách làm skills thông minh hơn mà không tốn token hơn

### Nên làm

- Viết trigger cụ thể hơn trong pack description.
- Thêm decision matrix ngắn thay vì prose dài.
- Thêm benchmark prompt để bắt lỗi routing.
- Đưa chi tiết dài vào `references/`, không đưa vào pack.
- Tách “minimum bar” và “deep guidance”.
- Thêm examples ngắn ở reference nếu giúp model chọn đúng.
- Dùng negative activation: ghi rõ khi nào không dùng pack.

### Không nên làm

- Thêm nhiều agents khi chưa có benchmark chứng minh cần.
- Copy skill từ project khác vào CE7.
- Nhồi tất cả security/performance/ops rules vào mọi pack.
- Mở nhiều pack “cho chắc”.
- Tăng line count để tạo cảm giác chuyên sâu.
- Viết description kiểu tóm tắt workflow thay vì trigger.

## 6. Khi nào nên thêm agent mới?

Hiện tại chỉ nên có:

- `ce7-software-engineering`
- `skill-evaluator`

Chỉ thêm `architecture-reviewer` nếu benchmark cho thấy lặp lại lỗi như:

- kiến trúc thiếu trade-off;
- boundary sai;
- over-engineering;
- không xét ownership/team topology;
- recommendation quá tactical.

Chỉ thêm `delivery-risk-reviewer` nếu benchmark cho thấy lặp lại lỗi như:

- migration thiếu rollback;
- release thiếu rollout gates;
- không có SLO/alert/runbook;
- thiếu feature flag hoặc compatibility plan;
- production support path mơ hồ.

Nếu lỗi chỉ là trigger/reference sai, sửa pack trước, chưa thêm agent.

## 7. Chu kỳ cải tiến khuyến nghị

### Hàng tuần hoặc sau mỗi thay đổi lớn

1. Chạy validator.
2. Chạy 10 benchmark prompts.
3. Ghi report vào `reports/latest-skill-eval.md`.
4. Thêm một dòng vào `reports/skill-eval-history.jsonl`.
5. Patch tối đa 1–2 pack có điểm thấp nhất.
6. Re-run benchmark fail cases.

### Hàng tháng

1. Review `docs/external-skill-research.md`.
2. Tìm thêm pattern tốt từ workspace.
3. Cập nhật `docs/skill-pack-quality-rubric.md` nếu quality bar thay đổi.
4. Quyết định có cần agent mới không dựa trên benchmark history.

## 8. Definition of Done cho cải tiến pack

Một cải tiến pack hoàn tất khi:

- validator pass;
- benchmark fail case trước đó pass lại;
- không tăng số pack/reference cần mở cho prompt bình thường;
- `.github/skills` sync với root `skills`;
- README/instructions nếu bị ảnh hưởng đã cập nhật;
- nếu học pattern từ project khác thì `external-skill-research.md` đã ghi nhận;
- report mới được ghi vào `reports/latest-skill-eval.md`.

