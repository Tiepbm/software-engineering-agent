# Contract cho thư mục Reports của CE7

[English](README.md) | [Tiếng Việt](README.vi-VN.md)

## `reports/` sở hữu phần gì?

`reports/` chỉ giữ các artifacts tín hiệu cao ở mức cross-run:

- `latest-skill-eval.md` → snapshot run mới nhất bằng tiếng Anh.
- `latest-skill-eval.vi-VN.md` → snapshot run mới nhất bằng tiếng Việt.
- `skill-eval-history.jsonl` → lịch sử machine-readable dạng append-only với **1 JSON object cho mỗi run**.

Chi tiết ở mức prompt **không** nên để ở đây. Hãy giữ chúng trong `runs/<run_id>/`.

## Những gì nên nằm trong `runs/<run_id>/`

Artifacts chi tiết theo từng run vẫn ở thư mục run:

- `manifest.json`
- `report.json`
- `summary.md`
- `scores.json`
- `scores.jsonl`
- `evaluator-prompts/`
- `outputs/` gốc

## Vì sao phải tách như vậy?

Cách tách này giúp `reports/` hữu ích cho regression tracking mà không biến nó thành bản sao đầy nhiễu của `runs/`.

Nên làm:

- 1 dòng cho mỗi run trong history;
- latest snapshot ngắn gọn;
- trỏ ngược về artifacts đầy đủ của run.

Không nên:

- append per-prompt rows vào history toàn cục;
- copy toàn bộ findings từng prompt vào `latest-skill-eval*`;
- lưu full model outputs trong `reports/`.

## Schema của `skill-eval-history.jsonl`

Mỗi dòng nên là JSON object ở mức run với tối thiểu các trường:

- `timestamp`
- `run_id`
- `benchmark`
- `outputs_scored`
- `models`
- `semantic_status`
- `deterministic.average_score`
- `deterministic.pass`
- `deterministic.warn`
- `deterministic.fail`
- `per_model`
- `issue_counts`
- `hotspots`
- `lowest_scoring_cases`
- `likely_update_targets`
- `artifacts`

## Luồng cập nhật chuẩn

```bash
python3 scripts/benchmark_pipeline.py score \
  --run-id <run-id> \
  --append-history
```

Lệnh này nên:

1. ghi `report.json` và `summary.md` trong thư mục run;
2. ghi đè `latest-skill-eval.md` và `latest-skill-eval.vi-VN.md`;
3. thêm đúng một dòng JSON vào `skill-eval-history.jsonl`.

## Thứ tự nên đọc

- Cần execution steps: `docs/pipeline-guide.vi-VN.md`
- Cần scoring policy và logic cải tiến: `docs/evaluation-improvement-playbook.vi-VN.md`
- Cần quick commands: `evals/file-based-benchmark-pipeline.vi-VN.md`

