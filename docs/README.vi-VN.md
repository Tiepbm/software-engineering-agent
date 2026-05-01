# Index tài liệu

[English](README.md) | [Tiếng Việt](README.vi-VN.md)

Folder này được nhóm theo **đối tượng người đọc**, không theo loại tài liệu. Chọn dòng tương ứng với vai trò của bạn.

## Người dùng (bạn muốn dùng agent)

| Doc | Mục đích |
|---|---|
| [`GETTING-STARTED.vi-VN.md`](GETTING-STARTED.vi-VN.md) / [`.md`](GETTING-STARTED.md) | Walkthrough 5 phút — cài đặt, prompt đầu tiên, kỳ vọng output. |
| [`INSTALL.vi-VN.md`](INSTALL.vi-VN.md) / [`.md`](INSTALL.md) | Ba chế độ cài đặt (global / workspace / per-project) + kiểm tra sau cài. |

## Evaluator (bạn chấm điểm output model)

| Doc | Mục đích |
|---|---|
| [`pipeline-guide.vi-VN.md`](pipeline-guide.vi-VN.md) / [`.md`](pipeline-guide.md) | Pipeline benchmark end-to-end (prepare → output → score → evaluator → report). |
| `../evals/scoring-rubric.vi-VN.md` / `.md` | Rubric chấm điểm theo từng prompt (đi cùng pipeline guide). |
| `../evals/file-based-benchmark-pipeline.vi-VN.md` / `.md` | Quickstart lệnh cho pipeline file-based. |
| `../evals/model-comparison-runbook.vi-VN.md` / `.md` | Runbook so sánh GPT vs Claude cho prompt banking / non-life insurance. |

## Maintainer (bạn sửa pack, reference, agent hoặc eval rules)

| Doc | Mục đích | Song ngữ? |
|---|---|---|
| [`evaluation-improvement-playbook.vi-VN.md`](evaluation-improvement-playbook.vi-VN.md) / [`.md`](evaluation-improvement-playbook.md) | Khi nào và cách cải tiến pack/reference sau benchmark run. | Có |
| [`skill-pack-quality-rubric.md`](skill-pack-quality-rubric.md) | Quality gate liên quan CI mà mỗi PR pack phải pass. | Chỉ EN |
| [`external-skill-research.md`](external-skill-research.md) | Pattern tham khảo từ project khác + ghi chú originality. | Chỉ EN |

> **Chính sách song ngữ.** Tài liệu user-facing (README, GETTING-STARTED, INSTALL) và artifact evaluator gắn với script thực thi giữ song ngữ (`.md` + `.vi-VN.md`). Tài liệu chỉ dành maintainer — driving CI rule hoặc technical research — chỉ dùng EN để tránh translation drift. Quy tắc nằm trong `AGENTS.md`.

## Phần còn lại nằm ở đâu

- `../AGENTS.md` — entry point cho contributor & maintainer (quy tắc edit, sync workflow, bilingual policy).
- `../instructions/` — file instruction được pack và principal agent kế thừa.
- `../reports/` — report ở mức run, history, và plan thiết kế deferred (vd `PLAN-automatic-memory.md`).
- `../examples/` — template output-shape mà agent tham chiếu.

