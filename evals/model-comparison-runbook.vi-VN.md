# Runbook so sánh GPT / Claude cho Banking & Non-life Insurance Benchmark

[English](model-comparison-runbook.md) | [Tiếng Việt](model-comparison-runbook.vi-VN.md)

> **Bạn đang ở đâu?** Đây là runbook **benchmark-specific** cho bộ case `evals/banking-insurance-benchmark.jsonl`.
>
> - Nếu bạn cần cách chạy pipeline nói chung: xem `docs/pipeline-guide.vi-VN.md`.
> - Nếu bạn chỉ cần quickstart lệnh: xem `evals/file-based-benchmark-pipeline.vi-VN.md`.
> - Nếu bạn cần biết cách diễn giải kết quả và update target: xem `docs/evaluation-improvement-playbook.vi-VN.md`.

Dùng runbook này để chạy 10 case thực tế trong `evals/banking-insurance-benchmark.jsonl` với các model GPT và Claude.

## 1. Mục tiêu

So sánh model theo 4 câu hỏi:

1. Model có chọn đúng pack/reference không?
2. Model có đưa ra answer principal-grade cho nghiệp vụ ngân hàng / bảo hiểm phi nhân thọ không?
3. Model có đủ production safety: security, data correctness, audit, observability, release, rollback không?
4. Model có tiết kiệm token, không mở quá nhiều pack/reference và không trả lời lan man không?

## 2. Chuẩn bị tối thiểu

Đọc các file:

- `evals/banking-insurance-benchmark.jsonl`
- `evals/scoring-rubric.md`
- `evals/scoring-rubric.vi-VN.md`

Nếu chạy qua pipeline file-based, dùng thêm:

- `docs/pipeline-guide.vi-VN.md`
- `scripts/benchmark_pipeline.py`

## 3. Prompt wrapper chuẩn

Để giảm sai khác giữa GPT và Claude, dùng wrapper này:

```text
Act as CE7 Software Engineering Agent.
Use the Copilot-first hybrid pack architecture.
Before answering, state:
- Packs selected
- References selected
- Why these packs/references are sufficient
Do not load more than 3 references unless required by production risk.
Then answer the business prompt with principal-level engineering guidance.

Business prompt:
<PASTE_PROMPT_HERE>
```

## 4. Cách chạy từng case

Với mỗi dòng trong `evals/banking-insurance-benchmark.jsonl`:

1. lấy trường `prompt`;
2. chạy cùng một wrapper cho GPT và Claude;
3. ghi lại actual packs/references;
4. so với `expected_packs`, `expected_references`, `should_not_activate`;
5. chấm theo rubric;
6. lưu kết quả vào report/history hoặc vào `runs/<run_id>/...` nếu dùng pipeline file-based.

## 5. Score sheet per model

| Field | GPT | Claude |
|---|---|---|
| Prompt ID |  |  |
| Packs selected |  |  |
| References selected |  |  |
| Unexpected packs |  |  |
| Missing packs |  |  |
| Unexpected references |  |  |
| Missing references |  |  |
| Weighted score |  |  |
| Verdict |  |  |
| Token notes |  |  |
| Main strengths |  |  |
| Main weaknesses |  |  |

## 6. What good looks like cho benchmark này

Một câu trả lời mạnh nên:

- nêu assumptions rõ ràng;
- tách architecture, data, integration, security, observability, testing, release;
- có failure paths và operator repair paths;
- định nghĩa audit evidence cho regulated workflows;
- có idempotency/reconciliation khi liên quan đến money hoặc claims;
- có rollback/roll-forward cho migration/release;
- tránh mở stack references không liên quan;
- tránh generic advice kiểu “use best practices”.

## 7. Chọn model thắng như thế nào?

Ưu tiên model:

- thiếu ít critical risk hơn;
- mở ít pack/reference thừa hơn;
- có validation evidence cụ thể hơn;
- xử lý regulated-domain detail tốt hơn;
- ngắn hơn nhưng vẫn đầy đủ;
- ổn định hơn trên toàn bộ 10 prompts.

**Không chọn winner từ một prompt.** Dùng average score + regression count trên toàn bộ suite.

## 8. Sau khi so sánh xong, làm gì tiếp?

- Nếu cả hai model cùng fail một pattern → sửa agent/pack/reference.
- Nếu chỉ một model fail → ghi history, quan sát thêm trước khi sửa instruction.
- Nếu benchmark chưa bắt được một kiểu sai mới → thêm benchmark row hoặc cập nhật scoring notes.

