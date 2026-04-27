# Hướng dẫn Pipeline Benchmark và Tự Đánh Giá cho CE7

[English](pipeline-guide.md) | [Tiếng Việt](pipeline-guide.vi-VN.md)

> **Bạn đang ở đâu?** Đây là **tài liệu chuẩn** cho cách chạy pipeline file-based end-to-end.
>
> - Nếu bạn chỉ cần lệnh chạy nhanh: xem `evals/file-based-benchmark-pipeline.vi-VN.md`.
> - Nếu bạn cần biết cách diễn giải kết quả và nên sửa agent/skill ở đâu: xem `docs/evaluation-improvement-playbook.vi-VN.md`.
> - Nếu bạn chỉ so sánh GPT và Claude trên bộ case banking/insurance: xem `evals/model-comparison-runbook.vi-VN.md`.

## 1. Tài liệu này sở hữu phần gì?

Tài liệu này chỉ tập trung vào **vận hành pipeline**:

1. benchmark nào đi vào pipeline;
2. script nào chạy ở bước nào;
3. cấu trúc thư mục `runs/<run_id>/`;
4. contract input/output giữa benchmark, model, scorer và `skill-evaluator`;
5. artifacts nào được tạo sau mỗi bước.

Tài liệu này **không lặp lại**:

- chính sách đánh giá nhiều lớp và cách quyết định update → `docs/evaluation-improvement-playbook.vi-VN.md`;
- hướng dẫn benchmark-specific cho GPT/Claude → `evals/model-comparison-runbook.vi-VN.md`;
- quickstart tối giản → `evals/file-based-benchmark-pipeline.vi-VN.md`.

## 2. Luồng chuẩn của pipeline

```text
benchmark case
→ generate prompt files
→ chạy GPT / Claude
→ lưu output vào file
→ chấm deterministic
→ sinh prompt cho skill-evaluator
→ chấm semantic
→ ghi report / history
```

## 3. Thành phần chính

### Nguồn benchmark

- `evals/banking-insurance-benchmark.jsonl`
- `evals/routing-benchmark.jsonl`

### Script điều phối

- `scripts/benchmark_pipeline.py`

### Scoring / semantic evaluation

- `evals/scoring-rubric.md`
- `evals/scoring-rubric.vi-VN.md`
- `agents/skill-evaluator.agent.md`

### Validation / reports

- `scripts/validate_hybrid_packs.py`
- `reports/README.md`
- `reports/README.vi-VN.md`
- `reports/latest-skill-eval.md`
- `reports/latest-skill-eval.vi-VN.md`
- `reports/skill-eval-history.jsonl`

## 4. Cấu trúc thư mục của một run

Ví dụ với `run_id = 2026-04-27-gpt-claude-v1`:

```text
runs/2026-04-27-gpt-claude-v1/
  manifest.json
  prompts/
    gpt/
      banking-001-payment-idempotency.md
      ...
    claude/
      banking-001-payment-idempotency.md
      ...
  outputs/
    gpt/
      banking-001-payment-idempotency.md
      ...
    claude/
      banking-001-payment-idempotency.md
      ...
  scores.json
  scores.jsonl
  report.json
  summary.md
  evaluator-prompts/
    gpt/
      banking-001-payment-idempotency.md
      ...
    claude/
      banking-001-payment-idempotency.md
      ...
```

### Ý nghĩa từng artifact

- `manifest.json`: metadata của run, benchmark source, model list.
- `prompts/`: prompt đã được wrap sẵn theo contract CE7.
- `outputs/`: nơi model ghi câu trả lời gốc.
- `scores.json` và `scores.jsonl`: kết quả deterministic scoring.
- `report.json`: scorecard machine-readable ở mức run và tóm tắt target nên sửa.
- `summary.md`: bảng tóm tắt nhanh cho run.
- `evaluator-prompts/`: prompt đã được đóng gói cho `skill-evaluator`.

## 5. Quy trình chạy chuẩn

### Bước 0 — Validate package trước

```bash
python3 scripts/validate_hybrid_packs.py
```

Nếu fail, sửa cấu trúc trước khi benchmark.

### Bước 1 — Generate prompt files

```bash
python3 scripts/benchmark_pipeline.py prepare \
  --run-id 2026-04-27-gpt-claude-v1 \
  --models gpt,claude
```

Mục tiêu: bảo đảm GPT và Claude nhận cùng wrapper, cùng benchmark row, cùng output contract.

### Tuỳ chọn: chế độ auto 1 lệnh (chỉ switch model)

Nếu bạn muốn script tự chạy prepare -> gọi model -> score -> sync history -> evaluator-prompts:

```bash
# GPT
export OPENAI_API_KEY="<your_openai_key>"
python3 scripts/benchmark_pipeline.py run \
  --run-id 2026-04-27-gpt-auto \
  --model gpt

# Claude
export ANTHROPIC_API_KEY="<your_anthropic_key>"
python3 scripts/benchmark_pipeline.py run \
  --run-id 2026-04-27-claude-auto \
  --model claude
```

Ghi chú:

- `--model` dùng để chọn provider (`gpt` hoặc `claude`).
- `--provider-model` cho phép override tên model mặc định của provider.
- `--limit` hữu ích cho smoke test; `--overwrite` để ghi đè outputs đã có.

### Tuỳ chọn: không có API key (Copilot manual mode)

Nếu bạn không có API key, dùng 2 lệnh này:

```bash
# Chuẩn bị sẵn prompts + output stubs + worklist
python3 scripts/benchmark_pipeline.py implement \
  --run-id 2026-04-27-gpt-claude-manual \
  --models gpt,claude

# Sau khi dán xong output, finalize để chấm + sinh evaluator-prompts
python3 scripts/benchmark_pipeline.py finalize \
  --run-id 2026-04-27-gpt-claude-manual \
  --models gpt,claude
```

Artifacts thêm trong manual mode:

- `runs/<run_id>/manual/README.md`
- `runs/<run_id>/manual/worklist.md`

`finalize` sẽ chặn nếu còn file output thiếu hoặc còn marker `<!-- CE7_OUTPUT_PENDING -->` (trừ khi dùng `--allow-partial`).

### Bước 2 — Chạy model và lưu output vào file

Đưa từng file trong:

```text
runs/<run_id>/prompts/<model>/<prompt_id>.md
```

cho model tương ứng và lưu output vào:

```text
runs/<run_id>/outputs/<model>/<prompt_id>.md
```

#### Header output khuyến nghị

```markdown
- Packs selected: core-engineering-pack, platform-integration-pack
- References selected: api-design, messaging-and-eventing
- Why these packs/references are sufficient: payment idempotency crosses API, data, messaging, security, and observability boundaries.
```

Header này giúp deterministic scorer parse ổn định hơn. Nếu thiếu, script vẫn fallback scan nội dung nhưng độ chính xác thấp hơn.

### Bước 3 — Chấm deterministic

```bash
python3 scripts/benchmark_pipeline.py score \
  --run-id 2026-04-27-gpt-claude-v1 \
  --append-history
```

Script chấm được:

- `expected_packs` vs `actual_packs`;
- `expected_references` vs `actual_references`;
- `should_not_activate` violations;
- answer length;
- approximate token count;
- token efficiency sơ bộ.

Script **không chấm** semantic quality sâu. Phần đó thuộc về `skill-evaluator`.

### Bước 4 — Sinh prompt cho `skill-evaluator`

```bash
python3 scripts/benchmark_pipeline.py evaluator-prompts \
  --run-id 2026-04-27-gpt-claude-v1
```

Mỗi file trong `runs/<run_id>/evaluator-prompts/<model>/<prompt_id>.md` sẽ chứa:

- benchmark expectation;
- deterministic findings;
- model output gốc;
- schema để evaluator trả về structured result.

### Bước 5 — Ghi report / history

Khi chạy `score --append-history`, pipeline cũng cập nhật:

- `reports/latest-skill-eval.md`
- `reports/latest-skill-eval.vi-VN.md`
- `reports/skill-eval-history.jsonl`

Lưu ý quan trọng: `skill-eval-history.jsonl` chỉ nên chứa **1 JSON row cho mỗi run**, không phải cho từng prompt. Bằng chứng chi tiết theo prompt nên giữ trong `runs/<run_id>/`.

## 6. Contract dữ liệu giữa các bước

### Input contract

Mỗi benchmark row cần có:

- `id`
- `prompt`
- `expected_packs`
- `expected_references`
- `should_not_activate`

Riêng `evals/banking-insurance-benchmark.jsonl` còn có thêm domain, risk class và scoring notes.

### Output contract từ model

Tối thiểu nên có:

- packs selected;
- references selected;
- phần trả lời chính.

### Output contract từ evaluator

Tối thiểu nên có:

- verdict;
- scorecard;
- routing findings;
- token findings;
- production-risk findings;
- suggested update targets.

## 7. Chiến lược tiết kiệm token trong pipeline

Pipeline cố ý chia làm 2 pha:

### Pha 1 — deterministic

Nhanh, rẻ, dùng rule-based parsing để lọc những lỗi đơn giản trước.

### Pha 2 — semantic

Chỉ khi đã có output cụ thể mới đóng gói prompt cho `skill-evaluator`.

### Không nên làm

- không inject toàn bộ `skill-eval-history.jsonl` vào prompt evaluator;
- không đưa full benchmark suite vào một lần chấm;
- không paste toàn bộ references vào prompt.

Chỉ nên đưa:

- benchmark row hiện tại;
- output hiện tại;
- deterministic findings hiện tại;
- rubric hiện tại.

## 8. Các lỗi vận hành hay gặp

| Vấn đề | Dấu hiệu | Cách xử lý |
|---|---|---|
| Output lưu sai path | `score` không thấy file | kiểm tra `runs/<run_id>/outputs/<model>/<prompt_id>.md` |
| Thiếu header packs/references | scorer parse sai hoặc thiếu | thêm header chuẩn ở đầu output |
| Dùng sai `run_id` | artifacts nằm ở nhiều thư mục | thống nhất `run_id` từ đầu run |
| Đưa cả history dài vào evaluator | prompt phình to | chỉ đưa row hiện tại + findings hiện tại |
| Reports toàn cục bị nhồi chi tiết từng prompt | `reports/` khó đọc và nhiễu | giữ chi tiết ở `runs/<run_id>/` và chỉ append 1 dòng history cho mỗi run |

## 9. Nên đọc tiếp gì?

- Muốn chạy nhanh ngay: `evals/file-based-benchmark-pipeline.vi-VN.md`
- Muốn so sánh GPT vs Claude: `evals/model-comparison-runbook.vi-VN.md`
- Muốn biết cách chấm và nên sửa file nào: `docs/evaluation-improvement-playbook.vi-VN.md`
- Muốn xem tiêu chí chấm điểm: `evals/scoring-rubric.vi-VN.md`

