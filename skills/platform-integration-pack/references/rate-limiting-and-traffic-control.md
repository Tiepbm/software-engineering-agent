---
name: rate-limiting-and-traffic-control
description: 'Designs throttling, quotas, burst control, backpressure, priority traffic, abuse prevention, partner protection, and graceful rejection behavior.'
---

# Rate Limiting and Traffic Control

## Description

Designs throttling, quotas, burst control, backpressure, priority traffic, abuse prevention, partner protection, and graceful rejection behavior.

## Purpose

- Protect systems from overload, abusive clients, noisy tenants, partner bursts, and retry storms.
- Preserve fairness and availability for critical workflows under high demand or dependency degradation.
- Make rejection behavior explicit, observable, and safe for enterprise APIs and regulated workflows.

## When to Use

- Designing public APIs, partner APIs, API gateways, login flows, payment or claim submission, batch ingestion, webhooks, or expensive search endpoints.
- Systems experience traffic spikes, noisy tenants, dependency saturation, queue overload, abuse, scraping, or unfair resource usage.
- A service needs quotas, burst limits, concurrency limits, backpressure, priority lanes, or graceful degradation.

## Responsibilities

- Define limit dimensions: tenant, user, API key, IP, partner, endpoint, operation type, cost unit, or priority class.
- Choose algorithm: token bucket, leaky bucket, fixed window, sliding window, concurrency limit, queue depth limit, or adaptive throttling.
- Design response behavior, retry-after guidance, error contract, observability, and override procedures.
- Protect downstream databases, queues, search clusters, partner APIs, and background workers.

## Decision Principles

- Rate limits should protect scarce resources and fairness, not be arbitrary numbers.
- Limit by business identity where possible; IP-only limits are weak for enterprise clients and NAT scenarios.
- Use burst tolerance for normal traffic shape but enforce sustained quotas.
- Prefer graceful rejection over accepting work that will fail later or overload dependencies.
- Prioritize critical and paid/contracted traffic deliberately during degradation.

## Expected Output Style

- State the protected resource and traffic risk.
- Include limit dimensions, algorithm, thresholds, burst behavior, and error response.
- Define telemetry, dashboards, and alerting for limit hits and saturation.
- Identify bypass, override, and emergency controls.
- Explain trade-offs between fairness, user experience, and protection.

## Architecture / Design Guidance

Traffic control can happen at CDN, WAF, API gateway, service, queue, worker, or database boundary. Edge limits protect broad capacity and abuse. Service-level limits understand business identity and operation cost. Queue and worker limits protect asynchronous processing. Database and search limits protect expensive query paths.

For banking and insurance, design limits carefully around critical workflows. A customer submitting a claim, making a payment, or completing identity verification may require different handling than bulk export, search, or partner polling.

## Implementation Guidance

- Use stable keys such as tenant ID, client ID, API key, user ID, endpoint, and operation cost class.
- Return explicit 429 or agreed error contracts with Retry-After where clients can act on it.
- Add server-side idempotency for retried operations so throttling does not duplicate side effects.
- Apply concurrency limits to expensive operations, not only request-rate limits.
- Add queue backpressure when workers or downstream systems cannot keep up.
- Provide allowlists, emergency overrides, and partner-specific limits with audit.
- Monitor accepted, throttled, rejected, queued, and shed traffic by dimension.

## Testing Expectations

- Test burst traffic, sustained traffic, noisy tenant behavior, retry behavior, and limit reset behavior.
- Test concurrency limits on expensive endpoints and dependency degradation.
- Test 429 responses, Retry-After, client retry compatibility, and idempotency.
- Test priority traffic during overload.
- Test metrics and alerts for throttling spikes and saturation.

## Security / Performance / Reliability Considerations

Security requires abuse prevention, credential-based limits, bot/scraping controls, and no leakage of sensitive quota metadata. Performance requires low-latency limit checks and hot-key-resistant counters. Reliability requires distributed counter consistency, fail-open/fail-closed decisions, override procedures, and protection from retry storms.

## Review Checklist

- Protected resources and failure modes are clear.
- Limit keys match business identity and fairness needs.
- Algorithm and thresholds fit burst and sustained traffic.
- Expensive operations have concurrency or cost-based limits.
- Rejection response is explicit and client-actionable.
- Metrics show accepted, throttled, rejected, and saturated traffic.
- Overrides are audited and time-bound.
- Critical workflows have priority or special handling where justified.

## Anti-Patterns to Avoid

- Using only IP-based limits for enterprise or partner APIs.
- Returning generic errors that cause clients to retry aggressively.
- Applying one global limit to all endpoints regardless of cost.
- Accepting unlimited work into queues during downstream outages.
- Implementing limits without dashboards or override procedures.
- Allowing internal batch jobs to bypass all limits and starve user traffic.

## Gotchas / Common Failure Modes

- NAT and proxies can make IP limits punish many legitimate users.
- Retry storms can turn throttling into more load unless clients get clear retry guidance.
- Distributed counters can become hot keys or inconsistent under high traffic.
- Fail-open protects availability but may overload dependencies; fail-closed protects dependencies but may block users.
- Partner contracts often require quota transparency and advance notice of changes.
- Background jobs can create traffic spikes that look like abuse unless separately classified.

