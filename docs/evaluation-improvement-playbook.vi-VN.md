# Playbook đánh giá và cải tiến CE7 Agent / Skill Packs

[English](evaluation-improvement-playbook.md) | [Tiếng Việt](evaluation-improvement-playbook.vi-VN.md)

> **Bạn đang ở đâu?** Đây là tài liệu chuẩn cho **chính sách đánh giá** và **quy tắc cải tiến**.
>
> - Nếu bạn cần cách chạy lệnh pipeline: xem `docs/pipeline-guide.vi-VN.md`.
> - Nếu bạn cần quickstart ngắn: xem `evals/file-based-benchmark-pipeline.vi-VN.md`.
> - Nếu bạn cần so sánh GPT vs Claude trên banking/insurance benchmark: xem `evals/model-comparison-runbook.vi-VN.md`.

**Mục tiêu:** giúp bạn đánh giá chất lượng agent + skills một cách lặp lại được, biết nên cải tiến chỗ nào, và tránh làm hệ thống phình token.

## 1. Nguyên tắc vận hành

CE7 hiện dùng kiến trúc **Copilot-first hybrid packs**:

- Copilot thấy **8 pack skills** ở `.github/skills/*/SKILL.md`.
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

Chạy `python3 scripts/validate_hybrid_packs.py` trước mọi review.

Fail ở layer này thì **chưa review semantic**. Sửa cấu trúc trước.

### Layer 2 — Routing benchmark

Dùng benchmark để xem prompt có activate đúng pack/reference và tránh false activation không.

### Layer 3 — Semantic answer quality

Cho `skill-evaluator` chấm output theo correctness, principal judgment, evidence discipline, production readiness, security/data safety, testability, actionability và brevity.

### Layer 4 — Token efficiency

Đánh giá theo hành vi:

- số pack mở;
- số reference mở;
- answer có paste reference không;
- có lặp rules giữa nhiều packs không.

### Layer 5 — Regression history

Ghi vào:

```text
reports/latest-skill-eval.md
reports/latest-skill-eval.vi-VN.md
reports/skill-eval-history.jsonl
```

Mục tiêu là phát hiện regression thật, không đánh giá theo cảm giác. Giữ history toàn cục ở mức **1 dòng cho mỗi run** và giữ chi tiết từng prompt trong `runs/<run_id>/`.

## 3. Scorecard và thang điểm

Rubric chi tiết nằm ở:

- `evals/scoring-rubric.md`
- `evals/scoring-rubric.vi-VN.md`

Giữ 8 nhóm điểm chính:

- trigger accuracy;
- reference precision;
- output quality;
- evidence / validation quality;
- production safety;
- token efficiency;
- Copilot readiness;
- originality / maintainability.

## 4. Cách quyết định nên sửa ở đâu

| Pattern lỗi | Nên sửa ở đâu |
|---|---|
| Thiếu expected pack lặp lại | `agents/ce7-software-engineering.agent.md` hoặc `.github/copilot-instructions.md` |
| Pack đúng nhưng thiếu reference | `skills/<pack>/SKILL.md` |
| Reference đúng nhưng output nông | `skills/<pack>/references/<reference>.md` |
| Mở quá nhiều pack/reference | token rules trong pack `SKILL.md` hoặc `.github/copilot-instructions.md` |
| GPT và Claude cùng fail | package hiện tại thiếu rõ, nên sửa agent/skill |
| Chỉ một model fail | ghi history, quan sát thêm trước khi sửa instruction |
| Benchmark không bắt được lỗi mới | thêm benchmark row hoặc cập nhật scoring notes |

### Quy tắc vàng

**Không sửa skill chỉ vì câu trả lời “nghe chưa hay”.**

Chỉ sửa khi benchmark + score + history chỉ ra lỗi lặp lại hoặc production risk rõ ràng.

## 5. Chu trình cải tiến chuẩn

1. Chạy structural validation.
2. Chạy benchmark prompt đại diện.
3. Chấm deterministic + semantic.
4. Phân loại lỗi theo bảng ở trên.
5. Chỉ patch 1–2 target quan trọng nhất.
6. Re-run đúng fail cases để xác nhận regression đã được sửa.

## 6. Cách làm skill thông minh hơn mà không tốn token hơn

### Nên làm

- viết trigger cụ thể hơn trong pack description;
- thêm decision matrix ngắn thay vì prose dài;
- đưa chi tiết dài vào `references/`, không đưa vào pack;
- thêm negative activation khi pack dễ bị route sai;
- thêm benchmark prompt để bắt lỗi routing hoặc production-risk gap.

### Không nên làm

- thêm nhiều agents khi chưa có benchmark chứng minh cần;
- copy skill từ project khác vào CE7;
- nhồi tất cả security/performance/ops rules vào mọi pack;
- mở nhiều pack “cho chắc”; 
- tăng line count để tạo cảm giác chuyên sâu.

## 7. Khi nào nên thêm agent mới?

Hiện tại chỉ nên có:

- `ce7-software-engineering`
- `skill-evaluator`

Chỉ thêm agent mới khi benchmark history cho thấy **lỗi lặp lại theo một loại judgment riêng** mà pack/reference sửa mãi không hết.

## 8. Chu kỳ cải tiến khuyến nghị

### Hàng tuần hoặc sau thay đổi lớn

1. chạy validator;
2. chạy benchmark;
3. ghi report;
4. append history;
5. patch tối đa 1–2 target;
6. re-run fail cases.

### Hàng tháng

1. review `docs/external-skill-research.md`;
2. cập nhật `docs/skill-pack-quality-rubric.md` nếu quality bar thay đổi;
3. xem có cần benchmark suite mới hoặc agent mới không.

## 9. Definition of Done cho cải tiến pack

Một cải tiến pack hoàn tất khi:

- validator pass;
- benchmark fail case trước đó pass lại;
- không tăng số pack/reference cần mở cho prompt bình thường;
- `.github/skills` sync với root `skills`;
- README/instructions nếu bị ảnh hưởng đã cập nhật;
- nếu học pattern từ project khác thì `external-skill-research.md` đã ghi nhận;
- report mới được ghi vào `reports/latest-skill-eval.md` / `reports/latest-skill-eval.vi-VN.md`.

## 10. Nên đọc tiếp gì?

- Muốn chạy pipeline: `docs/pipeline-guide.vi-VN.md`
- Muốn quickstart: `evals/file-based-benchmark-pipeline.vi-VN.md`
- Muốn so sánh GPT và Claude: `evals/model-comparison-runbook.vi-VN.md`
- Muốn xem rubric chi tiết: `evals/scoring-rubric.vi-VN.md`

