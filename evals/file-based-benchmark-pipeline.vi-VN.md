# File-based Benchmark Pipeline — Quickstart

[English](file-based-benchmark-pipeline.md) | [Tiếng Việt](file-based-benchmark-pipeline.vi-VN.md)

> **Bạn đang ở đâu?** Đây là bản **quickstart ngắn** để chạy pipeline qua file.
>
> - Guide đầy đủ: `docs/pipeline-guide.vi-VN.md`
> - Cách chấm và cải tiến: `docs/evaluation-improvement-playbook.vi-VN.md`
> - So sánh GPT vs Claude cho banking/insurance: `evals/model-comparison-runbook.vi-VN.md`

Pipeline này giúp bạn để AI chạy và tự đánh giá gần như tự động qua file, thay vì copy thủ công từng kết quả.

## Luồng ngắn gọn

```text
benchmark JSONL
→ prepare prompt files
→ chạy GPT/Claude và lưu output vào file
→ deterministic score routing/reference/token
→ sinh prompt cho skill-evaluator
→ skill-evaluator chấm semantic
→ lưu report/history
```

Script chính:

```text
scripts/benchmark_pipeline.py
```

## 1. Chuẩn bị prompt files

```bash
python3 scripts/validate_hybrid_packs.py

python3 scripts/benchmark_pipeline.py prepare \
  --run-id 2026-04-27-gpt-claude-v1 \
  --models gpt,claude
```

## 2. Chạy model và lưu output

Đọc prompt từ:

```text
runs/<run_id>/prompts/<model>/<prompt_id>.md
```

Lưu output vào:

```text
runs/<run_id>/outputs/<model>/<prompt_id>.md
```

Header output khuyến nghị:

```markdown
- Packs selected: core-engineering-pack, platform-integration-pack
- References selected: api-design, messaging-and-eventing
- Why these packs/references are sufficient: ...
```

## 3. Chấm deterministic

```bash
python3 scripts/benchmark_pipeline.py score \
  --run-id 2026-04-27-gpt-claude-v1 \
  --append-history
```

Artifacts chính:

```text
runs/<run_id>/report.json
runs/<run_id>/scores.json
runs/<run_id>/scores.jsonl
runs/<run_id>/summary.md
reports/latest-skill-eval.md
reports/latest-skill-eval.vi-VN.md
reports/skill-eval-history.jsonl
```

`reports/skill-eval-history.jsonl` chỉ nên append **1 dòng cho mỗi run**, không phải 1 dòng cho mỗi prompt.

## 4. Sinh prompt cho `skill-evaluator`

```bash
python3 scripts/benchmark_pipeline.py evaluator-prompts \
  --run-id 2026-04-27-gpt-claude-v1
```

Artifacts chính:

```text
runs/<run_id>/evaluator-prompts/<model>/<prompt_id>.md
```

## 5. Sau quickstart, đọc gì tiếp?

- Muốn hiểu ý nghĩa từng artifact và contract dữ liệu: `docs/pipeline-guide.vi-VN.md`
- Muốn biết nên sửa agent, pack hay reference: `docs/evaluation-improvement-playbook.vi-VN.md`
- Muốn chấm điểm chi tiết: `evals/scoring-rubric.vi-VN.md`

## Tuỳ chọn auto 1 lệnh

```bash
# GPT
export OPENAI_API_KEY="<your_openai_key>"
python3 scripts/benchmark_pipeline.py run --run-id 2026-04-27-gpt-auto --model gpt

# Claude
export ANTHROPIC_API_KEY="<your_anthropic_key>"
python3 scripts/benchmark_pipeline.py run --run-id 2026-04-27-claude-auto --model claude
```

## Tuỳ chọn không API key (manual mode)

```bash
python3 scripts/benchmark_pipeline.py implement --run-id 2026-04-27-gpt-claude-manual --models gpt,claude
python3 scripts/benchmark_pipeline.py finalize --run-id 2026-04-27-gpt-claude-manual --models gpt,claude
```

