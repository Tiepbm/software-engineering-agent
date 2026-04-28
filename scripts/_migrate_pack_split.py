#!/usr/bin/env python3
"""One-off migration script: rename storage-search-stack-pack into storage-search-pack
or application-stacks-pack inside eval files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# routing-benchmark
p = ROOT / "evals" / "routing-benchmark.jsonl"
text = p.read_text(encoding="utf-8")
text = text.replace(
    '"id":"stack-001","prompt":"Implement a Spring Boot REST service with JPA transactions, DTO mapping, validation, and N+1 avoidance.","expected_packs":["storage-search-stack-pack"]',
    '"id":"stack-001","prompt":"Implement a Spring Boot REST service with JPA transactions, DTO mapping, validation, and N+1 avoidance.","expected_packs":["application-stacks-pack"]',
)
text = text.replace(
    '"id":"stack-002","prompt":"Design object storage upload flow with signed URLs, metadata, malware scanning, and retention.","expected_packs":["storage-search-stack-pack","security-access-pack"]',
    '"id":"stack-002","prompt":"Design object storage upload flow with signed URLs, metadata, malware scanning, and retention.","expected_packs":["storage-search-pack","security-access-pack"]',
)
text = text.replace(
    '"id":"stack-003","prompt":"Design search indexing with authorization filtering, freshness, relevance, and reindex strategy.","expected_packs":["storage-search-stack-pack","data-database-analytics-pack"]',
    '"id":"stack-003","prompt":"Design search indexing with authorization filtering, freshness, relevance, and reindex strategy.","expected_packs":["storage-search-pack","data-database-analytics-pack"]',
)
text = text.replace(
    '"should_not_activate":["storage-search-stack-pack"]',
    '"should_not_activate":["application-stacks-pack"]',
)
p.write_text(text, encoding="utf-8")
print("routing-benchmark.jsonl: done")

# banking benchmark: every prior storage-search-stack-pack usage was about documents/objects
b = ROOT / "evals" / "banking-insurance-benchmark.jsonl"
btext = b.read_text(encoding="utf-8")
btext = btext.replace('"storage-search-stack-pack"', '"storage-search-pack"')
b.write_text(btext, encoding="utf-8")
print("banking-insurance-benchmark.jsonl: done")

