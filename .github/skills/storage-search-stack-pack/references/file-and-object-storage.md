---
name: file-and-object-storage
description: 'Designs secure file and object storage for documents, evidence, attachments, signed URLs, metadata, retention, scanning, large files, and access control.'
---

# File and Object Storage

## Description

Designs secure file and object storage for documents, evidence, attachments, signed URLs, metadata, retention, scanning, large files, and access control.

## Purpose

- Store and serve files safely without confusing object storage with business metadata or authorization policy.
- Support enterprise document workflows such as claim evidence, policy documents, statements, invoices, exports, and uploaded attachments.
- Define retention, malware scanning, encryption, access control, audit, lifecycle, and large-file behavior before production.

## When to Use

- Designing upload, download, document storage, evidence handling, object storage layout, signed URLs, retention, or metadata models.
- Files contain PII, financial records, insurance documents, claim evidence, customer communications, or regulated exports.
- Existing file handling has broken permissions, missing scans, orphaned objects, slow downloads, or unclear retention.

## Responsibilities

- Define object ownership, metadata model, storage key strategy, lifecycle, retention, deletion, legal hold, and audit requirements.
- Design upload/download flow, signed URL policy, size limits, content validation, checksum validation, and malware scanning.
- Separate object bytes from business metadata and authorization decisions.
- Ensure files can be located, audited, retained, deleted, and restored according to business rules.

## Decision Principles

- Store file bytes in object storage; store business metadata and permissions in a transactional system.
- Use signed URLs only with short lifetimes, scoped permissions, and server-side authorization before issuance.
- Scan untrusted uploads before making them available to users or downstream processors.
- Use immutable object versions or retention locks only when legal, audit, or evidence requirements justify them.
- Prefer streaming and multipart upload/download for large files; avoid loading entire files into application memory.

## Expected Output Style

- State storage purpose, object owner, metadata model, access model, and retention policy.
- Include upload, scan, quarantine, publish, download, delete, and audit flows.
- Define object key naming, signed URL constraints, encryption, and large-file handling.
- Call out compliance and operational risks.
- Provide tests for access control, malware path, and lifecycle behavior.

## Architecture / Design Guidance

Object storage is not a permission database. Keep authoritative metadata such as owner, tenant, document type, workflow state, retention class, scan status, legal hold, checksum, and object version in a transactional store. Use object keys that avoid leaking customer identifiers and support partitioning, lifecycle management, and operational lookup.

For insurance and banking, evidence and documents often require immutable audit trails, retention policy, and controlled deletion. Model document state explicitly: uploaded, quarantined, scanned, rejected, available, archived, held, deleted.

## Implementation Guidance

- Validate file type using content inspection, not only extension or client-provided MIME type.
- Use server-generated object keys and record checksum, size, content type, uploader, upload time, scan status, and storage version.
- Use pre-signed upload/download URLs only after authorization and with short expiry, method restrictions, size limits, and content constraints where supported.
- Quarantine files until malware scanning completes.
- Stream files through services only when policy enforcement or transformation requires it; otherwise use controlled direct object storage access.
- Implement lifecycle policies for archival, expiration, legal hold, and deletion with audit records.

## Testing Expectations

- Test authorized and unauthorized download, upload, delete, and metadata access.
- Test malicious file, oversized file, wrong content type, interrupted upload, checksum mismatch, and scan failure.
- Test signed URL expiry, scope, method restriction, and reuse behavior.
- Test retention, legal hold, archival, restore, and deletion workflows.
- Test large-file upload/download without excessive memory usage.

## Security / Performance / Reliability Considerations

Security requires encryption, tenant isolation, access checks before signed URL issuance, malware scanning, content validation, audit, and safe metadata. Performance requires multipart uploads, streaming, CDN decisions, range requests, and avoiding application memory pressure. Reliability requires durable metadata-object consistency, retryable uploads, lifecycle monitoring, restore procedures, and orphan cleanup.

## Review Checklist

- Metadata and permissions live outside object storage keys.
- Object keys do not expose sensitive business identifiers.
- Uploads are validated, scanned, and quarantined before availability.
- Signed URLs are short-lived and scoped.
- Retention, deletion, legal hold, and audit rules are explicit.
- Large files use streaming or multipart behavior.
- Orphaned metadata and orphaned objects have cleanup or reconciliation.
- Access logs support investigation without leaking sensitive content.

## Anti-Patterns to Avoid

- Using object path prefixes as the only access control.
- Serving uploaded files before scanning.
- Logging signed URLs or embedding long-lived URLs in emails.
- Storing business state only in object metadata.
- Loading large files fully into application memory.
- Deleting regulated evidence without retention and legal hold checks.
- Using original filenames as trusted metadata or storage keys.

## Gotchas / Common Failure Modes

- Signed URLs can bypass application authorization until expiry if issued too broadly.
- Object deletion and metadata deletion can become inconsistent without reconciliation.
- Malware scanning introduces asynchronous states that users and jobs must handle.
- Legal hold can conflict with user deletion requests and must be explicit.
- CDN caching can serve documents after permissions change if not controlled.
- File extensions and MIME types are easy to spoof.

