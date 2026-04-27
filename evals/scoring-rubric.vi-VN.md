# Rubric chấm điểm Benchmark CE7

[English](scoring-rubric.md) | [Tiếng Việt](scoring-rubric.vi-VN.md)

Dùng rubric này để chấm benchmark outputs từ `ce7-software-engineering` và `skill-evaluator`.

## Điểm cho từng prompt

Chấm mỗi prompt từ 0 đến 5 cho từng chiều.

| Dimension | Trọng số | 5 nghĩa là | 3 nghĩa là | 1 nghĩa là |
|---|---:|---|---|---|
| Trigger accuracy | 20% | Chọn đúng pack, không mở pack thừa | Gần đúng nhưng có 1 route mơ hồ | Sai pack hoặc thiếu pack bắt buộc |
| Reference precision | 15% | Chỉ mở references cần thiết | Mở thừa 1 reference hoặc thiếu reference phụ | Mở nhiều reference thừa hoặc thiếu reference cốt lõi |
| Output quality | 20% | Principal-grade, cụ thể, làm được ngay | Hữu ích nhưng còn generic ở vài chỗ | Mơ hồ hoặc không hành động được |
| Evidence / validation | 15% | Yêu cầu tests, metrics, logs, plans hoặc threat model phù hợp | Có nhắc validation nhưng chưa cụ thể | Không yêu cầu evidence |
| Production safety | 10% | Bao phủ security/data/release/ops risks khi cần | Bao phủ một phần | Bỏ sót critical production risk |
| Token efficiency | 10% | Cô đọng, không paste reference | Hơi dài | Dài dòng hoặc lặp lại nội dung reference |
| Copilot readiness | 5% | Tự nhiên với layout `.github` pack/reference | Có chút friction | Giả định sai runtime/layout |
| Maintainability/originality | 5% | CE7-specific, không copy external text, dễ bảo trì | Còn hơi generic | Duplicative, copied, hoặc khó phát triển |

## Cách tính điểm tổng

```text
weighted_score = Σ(score_0_to_5 × weight) × 20
```

## Verdict

| Weighted score | Verdict |
|---:|---|
| 90–100 | PASS — xuất sắc |
| 80–89 | PASS — dùng production được |
| 70–79 | WARN — dùng được nhưng nên cải tiến |
| 60–69 | WARN — có rủi ro, nên ưu tiên sửa |
| <60 | FAIL — chưa nên tin cậy |

## Ghi chú token

Ghi thêm các điểm sau khi chấm:

- Packs activated: `n`
- References activated: `n`
- Unexpected packs: danh sách
- Unexpected references: danh sách
- Missing packs/references: danh sách
- Answer length: short / medium / long / bloated
- Evidence included: yes / partial / no

## Quy tắc regression

Nếu một prompt trước đây đạt ≥80 mà bây giờ xuống <80, coi đó là regression dù điểm trung bình package vẫn ổn.

## Ghi chú riêng cho benchmark Banking / Non-Life Insurance

Với `evals/banking-insurance-benchmark.jsonl`, nâng chuẩn cho regulated workflows:

- Prompt liên quan đến money movement phải xử lý idempotency, duplicate prevention, reconciliation, audit evidence và operator repair.
- Prompt liên quan core banking hoặc ledger migration phải có expand-contract migration, reconciliation queries, restore/rollback hoặc roll-forward và regulator-safe reporting.
- Prompt claim bảo hiểm phi nhân thọ phải có state transitions, document retention, role-based access, fraud/assessment paths, payment integration và appeal/failure paths.
- Prompt bancassurance phải xác định bank/insurer boundaries, consent, data sharing, payment/policy issuance consistency, refund/cancellation state và partner outage behavior.
- Prompt Customer 360/search không được coi search index là source of truth và phải có field/document-level authorization, masking, audit, deletion/correction và index lag monitoring.

Phạt các output nghe có vẻ hợp lý về mặt kỹ thuật nhưng bỏ qua correctness cho regulated domain, auditability, support operations hoặc downstream reporting.

