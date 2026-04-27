---
name: logging-metrics-and-tracing
description: 'Designs production telemetry with structured logs, useful metrics, trace propagation, correlation IDs, safe redaction, and business-event observability.'
---

# Logging Metrics and Tracing

## Description

Designs production telemetry with structured logs, useful metrics, trace propagation, correlation IDs, safe redaction, and business-event observability.

## Purpose

- Make systems diagnosable across services, databases, queues, jobs, mobile clients, frontends, and partner integrations.
- Capture enough evidence to explain incidents without leaking secrets, regulated data, or customer-sensitive information.
- Connect technical telemetry to business workflows such as payments, claims, policies, onboarding, billing, and document processing.

## When to Use

- Adding or reviewing logs, metrics, traces, correlation IDs, telemetry conventions, error reporting, or business events.
- A system is hard to debug across service boundaries, async consumers, jobs, API gateways, or external integrations.
- Incidents lack evidence, logs contain PII, metrics are noisy, traces have useless spans, or business workflow health is invisible.

## Responsibilities

- Define telemetry boundaries at APIs, service calls, database calls, queue publish/consume, background jobs, cache calls, and external integrations.
- Standardize correlation IDs, causation IDs, request IDs, tenant-safe identifiers, operation names, and error codes.
- Design metrics with clear units, labels, aggregation behavior, and cardinality limits.
- Ensure logs and traces are useful, sampled appropriately, and safe for enterprise retention policies.

## Decision Principles

- Log business decisions and state transitions, not every line of execution.
- Use structured logs with stable fields; avoid parsing free-text messages for operations.
- Metrics should describe rate, errors, duration, saturation, freshness, lag, and business outcomes.
- Traces should explain cross-boundary latency and failure, not duplicate every log line.
- Redact secrets and sensitive data by default; allowlist fields rather than blocklisting known bad fields.

## Expected Output Style

- Specify telemetry events, fields, metric names, labels, spans, and propagation rules.
- State what an operator can diagnose from the telemetry.
- Include redaction and cardinality rules.
- Separate technical signals from business workflow signals.
- Provide review checklists that can be applied to code and dashboards.

## Architecture / Design Guidance

Telemetry architecture must define how context flows across HTTP, messaging, scheduled jobs, mobile calls, browser calls, and database operations. Correlation IDs should follow a transaction across synchronous and asynchronous boundaries. Trace spans should mark meaningful boundaries: inbound request, authorization decision, validation, database query class, external call, message publish, message consume, job execution, retry, and business completion.

For banking and insurance workflows, emit business-safe events for state transitions such as payment authorized, claim received, document scanned, policy changed, and billing adjustment queued. These events should be safe for logs and analytics without exposing regulated data.

## Implementation Guidance

- Use structured logging with fields such as timestamp, level, service, environment, operation, correlation_id, trace_id, tenant_id or safe tenant hash, user class, status, duration, and error_code.
- Define log levels: debug for local detail, info for lifecycle events, warn for recoverable abnormal behavior, error for failed operations requiring investigation.
- Avoid high-cardinality metric labels such as raw user ID, account number, claim number, policy number, email, URL with IDs, or free-form error text.
- Add trace propagation through API gateway, service calls, message headers, and job metadata.
- Capture retry count, queue lag, cache hit/miss, external dependency latency, and database operation class.
- Use consistent error codes that support alerting, search, support workflows, and incident timelines.

### Structured Log Field Schema

Use this schema as the baseline for all services. Fields marked `required` must appear on every log line; `recommended` should appear when available; `conditional` appears only for specific event types.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `timestamp` | ISO 8601 UTC | required | Event time | `2026-04-27T10:15:30.123Z` |
| `level` | enum | required | `debug`, `info`, `warn`, `error`, `fatal` | `error` |
| `service` | string | required | Service name (matches deployment) | `claims-api` |
| `environment` | string | required | `dev`, `staging`, `prod` | `prod` |
| `operation` | string | required | Logical operation name (stable, not URL) | `submitClaim`, `processPayment` |
| `correlation_id` | UUID | required | Request-scoped ID propagated across boundaries | `a1b2c3d4-...` |
| `trace_id` | string | recommended | OpenTelemetry trace ID | `4bf92f3577b34da6a3ce929d0e0e4736` |
| `span_id` | string | recommended | OpenTelemetry span ID | `00f067aa0ba902b7` |
| `tenant_id` | string | recommended | Tenant identifier (safe hash if PII risk) | `tenant_abc123` |
| `user_class` | string | recommended | User type without PII | `agent`, `customer`, `system`, `admin` |
| `status` | enum | required | `success`, `failure`, `partial`, `skipped` | `failure` |
| `duration_ms` | number | recommended | Operation duration in milliseconds | `342` |
| `error_code` | string | conditional | Stable machine-readable error code | `CLAIM_DUPLICATE_SUBMISSION` |
| `error_message` | string | conditional | Human-readable (no PII, no secrets) | `Duplicate claim for policy P-123` |
| `dependency` | string | conditional | External dependency name | `payment-gateway`, `postgres-primary` |
| `dependency_status` | string | conditional | Dependency call result | `success`, `timeout`, `error` |
| `dependency_duration_ms` | number | conditional | Dependency call duration | `180` |
| `retry_attempt` | number | conditional | Current retry attempt (0-based) | `2` |
| `queue_name` | string | conditional | Queue/topic for async operations | `claims.submitted` |
| `job_id` | string | conditional | Background job run identifier | `job_run_20260427_001` |
| `http_method` | string | conditional | HTTP method for API requests | `POST` |
| `http_path` | string | conditional | URL path template (no IDs) | `/v1/claims/{id}/submit` |
| `http_status` | number | conditional | HTTP response status code | `409` |

### Metric Naming Convention

Follow OpenTelemetry semantic conventions with these rules:

```
<namespace>_<subsystem>_<metric_name>_<unit>

Examples:
  claims_api_request_duration_seconds        (histogram)
  claims_api_request_total                   (counter, labels: method, path_template, status)
  claims_processing_queue_depth              (gauge)
  claims_processing_duration_seconds         (histogram)
  payments_settlement_total                  (counter, labels: result, currency)
  cache_operations_total                     (counter, labels: cache_name, operation, result)
  db_query_duration_seconds                  (histogram, labels: operation_class)
```

**Label rules**:
- Use `_total` suffix for counters, `_seconds` for duration histograms, no suffix for gauges.
- Labels must be low-cardinality: use `path_template` not `path_with_ids`, `operation_class` not `full_query`, `tenant_tier` not `tenant_id`.
- Maximum 5-7 labels per metric; each additional label multiplies cardinality.
- Never use: raw user ID, email, account number, claim number, full URL, full error message, or request body hash as labels.

## Testing Expectations

- Test correlation propagation across API calls, messages, and background jobs.
- Verify logs redact secrets, tokens, credentials, PII, payment data, claim details, and policy identifiers.
- Test metric label cardinality with realistic tenant and user volumes.
- Verify traces include meaningful spans for slow dependencies and async processing.
- Validate that business workflow events appear for success, failure, cancellation, and compensation paths.

## Security / Performance / Reliability Considerations

Security requires redaction, access control, retention policy, auditability, and no sensitive payload dumps. Performance requires bounded log volume, metric cardinality control, trace sampling, and avoiding telemetry on hot loops. Reliability requires telemetry pipelines that fail safely, preserve critical incident evidence, and do not block user workflows when collectors are unavailable.

## Review Checklist

- Correlation and trace context crosses service, message, and job boundaries.
- Logs are structured and include stable operation and error fields.
- Metrics have clear units, labels, and cardinality limits.
- Traces identify slow or failing dependencies.
- Sensitive fields are redacted or never emitted.
- Business-critical workflows have observable start, completion, failure, and compensation events.
- Operators can answer what failed, who was affected, when it started, and what dependency was involved.

## Anti-Patterns to Avoid

- Logging full request or response bodies in production.
- Using raw customer identifiers, account numbers, claim IDs, policy numbers, or emails as metric labels.
- Creating traces with many tiny spans that do not explain latency or failure.
- Logging errors without operation, correlation ID, or error code.
- Treating telemetry as optional after feature implementation.
- Emitting business events that contain regulated data when a safe reference is enough.

## Gotchas / Common Failure Modes

- Missing correlation IDs make async and partner failures expensive to investigate.
- Debug logs enabled in production can leak sensitive data and overwhelm storage.
- High-cardinality labels can break metrics systems or create runaway cost.
- Trace sampling may hide rare but critical regulated workflow failures.
- Logs without retention and access controls can become compliance liabilities.
- Telemetry added after incidents often misses the decision point that caused the failure.

