# Template Đánh giá Semantic Thủ công

[English](manual-evaluation-template.md) | [Tiếng Việt](manual-evaluation-template.vi-VN.md)

> **Mục đích**: Paste template này vào ChatGPT Plus hoặc Copilot Chat để nhận structured semantic scoring cho CE7 benchmark output. Không cần API keys.

## Cách sử dụng

1. Chạy `python3 scripts/benchmark_pipeline.py implement --run-id <your-run-id> --models gpt`
2. Mở prompt file từ `runs/<run_id>/prompts/gpt/<prompt_id>.md`
3. Paste vào ChatGPT Plus hoặc Copilot Chat
4. Lưu model output vào `runs/<run_id>/outputs/gpt/<prompt_id>.md`
5. Chạy `python3 scripts/benchmark_pipeline.py finalize --run-id <your-run-id> --models gpt`
6. Để chấm semantic: paste evaluator prompt (từ `runs/<run_id>/evaluator-prompts/gpt/<prompt_id>.md`) vào ChatGPT Plus dùng template bên dưới

## Prompt đánh giá Semantic (paste vào ChatGPT Plus)

```
You are a skill evaluator for the CE7 Software Engineering Agent package.

Score this model output on 5 semantic dimensions (0-5 each):

1. **Output Quality** (20%): Is the answer principal-grade, specific, actionable? Does it include decisions, trade-offs, rejected options?
2. **Evidence / Validation** (15%): Does it require tests, metrics, logs, plans, or threat models? Are validation steps concrete?
3. **Production Safety** (10%): Does it cover security, data correctness, release risk, operational controls when relevant?
4. **Copilot Readiness** (5%): Does it work naturally with pack/reference architecture?
5. **Maintainability** (5%): Is guidance CE7-specific, not generic copied text?

Return this JSON:
```json
{
  "prompt_id": "<from evaluator prompt>",
  "model": "gpt",
  "scores": {
    "output_quality": 0,
    "evidence_validation": 0,
    "production_safety": 0,
    "copilot_readiness": 0,
    "maintainability": 0
  },
  "weighted_score": 0,
  "verdict": "PASS|WARN|FAIL",
  "strengths": ["..."],
  "gaps": ["..."],
  "suggested_fixes": ["..."]
}
```

Then provide a 3-sentence explanation.

Here is the evaluator prompt with benchmark expectations and model output:

<PASTE EVALUATOR PROMPT HERE>
```

## Ngưỡng chấm điểm

| Weighted score | Verdict |
|---:|---|
| 90-100 | PASS — xuất sắc |
| 80-89 | PASS — dùng production được |
| 70-79 | WARN — dùng được, nên cải tiến |
| 60-69 | WARN — có rủi ro |
| <60 | FAIL |

## Sau khi chấm

1. Lưu JSON result vào `runs/<run_id>/semantic-scores/<model>/<prompt_id>.json`
2. Chạy `python3 scripts/regression_check.py` để kiểm tra regression
3. Nếu WARN hoặc FAIL: xem `docs/evaluation-improvement-playbook.vi-VN.md` mục 4 để biết nên sửa ở đâu

## Chu kỳ đánh giá phù hợp budget

| Tần suất | Làm gì | Tool | Chi phí |
|---|---|---|---|
| Mỗi khi sửa skill | `python3 scripts/validate_hybrid_packs.py` | Kiro terminal | $0 |
| Hàng tuần | Chạy 3-5 benchmark prompts trong Copilot Chat, chấm deterministic | Kiro + Copilot | $0 |
| 2 tuần/lần | Full 10-prompt banking/insurance benchmark, semantic eval cho 3 case thấp nhất | ChatGPT Plus | $0 |
| Hàng tháng | So sánh GPT vs Claude trên 5 prompts, cập nhật history | ChatGPT + Copilot | $0 |
| Sau thay đổi lớn | Full 25-prompt benchmark + semantic eval cho tất cả WARN/FAIL | ChatGPT Plus | $0 |
