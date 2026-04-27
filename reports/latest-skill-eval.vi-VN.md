# Báo cáo CE7 mới nhất

[English](latest-skill-eval.md) | [Tiếng Việt](latest-skill-eval.vi-VN.md)

> **Bạn đang ở đâu?** Đây là snapshot **ngắn gọn ở mức run** mới nhất đã được đồng bộ vào `reports/`.
>
> - Chi tiết per-prompt nằm trong `runs/<run_id>/`.
> - Lịch sử dài hạn nằm ở `reports/skill-eval-history.jsonl` với **1 dòng cho mỗi run**.
> - File này không thay thế `summary.md`; nó chỉ giữ lại tín hiệu quan trọng nhất.

## Snapshot hiện tại

- **Run ID:** `smoke-reports-2`
- **Generated:** 2026-04-27T13:17:57.938237+00:00
- **Benchmark:** `evals/banking-insurance-benchmark.jsonl`
- **Models:** `gpt`
- **Outputs scored:** 2
- **Semantic status:** `pending_skill_evaluator`

## Deterministic scorecard

| Metric | Value |
|---|---:|
| Average deterministic score | 100.0 |
| PASS | 2 |
| WARN | 0 |
| FAIL | 0 |

## Scorecard theo model

| Model | Outputs | Avg score | PASS | WARN | FAIL | Avg words |
|---|---:|---:|---:|---:|---:|---:|
| gpt | 2 | 100.0 | 2 | 0 | 0 | 136.5 |

## Tín hiệu quan trọng nhất

- Thiếu expected packs: 0 output(s). Hotspots: -
- Thiếu expected references: 0 output(s). Hotspots: -
- Unexpected/prohibited activations: 0 output(s). Hotspots: -
- Output thiếu header chuẩn hoặc parser phải fallback: scanned=0, missing=0
- Output dài: 0 | bloated: 0

## Target nên sửa tiếp

| Target | Lý do | Evidence |
|---|---|---|
| - | Không có deterministic signal đủ mạnh để đề xuất chỉnh sửa. | - |

## Cases thấp điểm nhất

| Model | Prompt | Score | Verdict | Main issue |
|---|---|---:|---|---|
| gpt | banking-001-payment-idempotency | 100 | PASS | no major deterministic issue |
| gpt | banking-002-loan-origination-underwriting | 100 | PASS | no major deterministic issue |

## Artifacts

- `runs/<run_id>/report.json`: `runs/smoke-reports-2/report.json`
- `runs/<run_id>/summary.md`: `runs/smoke-reports-2/summary.md`
- `runs/<run_id>/scores.jsonl`: `runs/smoke-reports-2/scores.jsonl`
- `runs/<run_id>/evaluator-prompts/`: `runs/smoke-reports-2/evaluator-prompts`
- Lịch sử toàn cục: `reports/skill-eval-history.jsonl`

## Quy tắc sử dụng report này

- Không chép toàn bộ prompt-level findings vào đây; giữ chúng ở `runs/<run_id>/`.
- Chỉ xem đây là snapshot gần nhất; dùng `skill-eval-history.jsonl` để xem xu hướng hoặc regression.
- Sau semantic evaluation, nên ghi bổ sung findings ở run folder hoặc tạo artifact semantic riêng thay vì làm file này quá dài.

