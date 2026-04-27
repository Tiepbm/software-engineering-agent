---
name: api-gateway-and-service-integration
description: 'Designs API gateways, BFFs, partner integrations, service routing, auth propagation, transformation, rate limits, resilience, and external dependency handling.'
---

# API Gateway and Service Integration

## Description

Designs API gateways, BFFs, partner integrations, service routing, auth propagation, transformation, rate limits, resilience, and external dependency handling.

## Purpose

- Integrate services, clients, and partners through controlled, observable, secure, and evolvable boundaries.
- Decide when to use API gateways, BFFs, direct service calls, adapters, anti-corruption layers, or integration services.
- Protect internal systems from partner instability, abusive traffic, protocol mismatch, and contract drift.

## When to Use

- Designing API gateway policies, BFFs, partner APIs, service-to-service calls, request transformation, routing, or protocol translation.
- Integrations need auth propagation, throttling, retries, circuit boundaries, versioning, auditing, or partner-specific handling.
- Existing integrations are brittle, hard to observe, over-coupled, or leak internal models.

## Responsibilities

- Define gateway responsibilities, backend ownership, routing, authentication, authorization propagation, and contract boundaries.
- Design partner integration policies: rate limits, timeouts, retries, idempotency, error mapping, versioning, and support contacts.
- Prevent API gateways from accumulating business logic that belongs in domain services.
- Ensure integrations are observable, testable, and recoverable.

## Decision Principles

- Use gateways for cross-cutting edge concerns: routing, auth enforcement, TLS, throttling, request limits, observability, and coarse transformations.
- Use BFFs when client-specific aggregation or experience shaping is needed and should not pollute core APIs.
- Use anti-corruption layers when external partner models differ from internal domain models.
- Keep business decisions in services, not in gateway scripts or policy fragments.
- Treat external APIs as unreliable dependencies with contracts, timeouts, retries, and fallback behavior.

## Expected Output Style

- State the integration boundary and why the chosen pattern fits.
- Include auth propagation, contract, timeout, retry, rate limit, error mapping, and observability rules.
- Identify what logic belongs at the gateway vs backend services.
- Include partner failure and versioning scenarios.
- Provide reviewable endpoint and policy decisions.

## Architecture / Design Guidance

A gateway should protect and standardize ingress without becoming a distributed monolith. It can terminate TLS, verify tokens, enforce coarse policies, route traffic, apply quotas, add correlation IDs, and normalize errors. A BFF can aggregate and shape responses for a specific web, mobile, or partner experience, but it must not become the canonical source of business rules.

Partner integrations should isolate external contracts behind adapters. Internal services should depend on stable internal models, not partner payloads or error codes.

## Implementation Guidance

- Propagate identity, tenant, scopes, correlation IDs, and trace context safely.
- Set request size limits, timeout budgets, retry policies, circuit breakers, and rate limits per route or partner.
- Map external errors to stable internal error contracts without losing diagnostic detail.
- Version public and partner APIs deliberately; support compatibility windows.
- Use idempotency keys for partner operations with side effects.
- Log integration attempts with safe metadata, not full sensitive payloads.
- Create contract tests and sandbox verification for partner APIs.

## Testing Expectations

- Test auth propagation, authorization failures, token expiry, invalid scopes, and tenant isolation.
- Test gateway routing, transformation, size limits, rate limits, timeout, retry, and circuit behavior.
- Test partner error mapping, version compatibility, idempotency, and duplicate requests.
- Test BFF aggregation when one downstream dependency is slow or unavailable.
- Test trace propagation from client through gateway to backend and partner adapter.

## Security / Performance / Reliability Considerations

Security requires token validation, scope enforcement, mTLS where needed, input validation, request limits, and safe logging. Performance requires bounded aggregation, payload control, connection reuse, and avoiding gateway bottlenecks. Reliability requires timeouts, circuit breakers, rate limits, fallback behavior, partner SLAs, and operational dashboards.

## Review Checklist

- Gateway, BFF, adapter, and backend responsibilities are separated.
- Auth and tenant context propagate correctly.
- Rate limits, quotas, timeouts, and retries are defined per integration risk.
- External contracts are isolated from internal domain models.
- Error mapping is stable and useful.
- Observability covers gateway, backend, and partner boundaries.
- Versioning and compatibility windows are documented.

## Anti-Patterns to Avoid

- Putting business logic in gateway policies.
- Letting BFFs become unowned backend services with duplicated rules.
- Passing partner payloads directly into core domain models.
- Retrying unsafe partner operations without idempotency.
- Using one global timeout and rate limit for all routes.
- Logging full partner payloads that contain PII or secrets.

## Gotchas / Common Failure Modes

- Gateways can become single points of failure or bottlenecks.
- Partner APIs often have undocumented rate limits and inconsistent error formats.
- Auth propagation bugs can become cross-tenant data exposure.
- BFF aggregation multiplies downstream failure probability.
- Request transformation can hide breaking changes until a partner upgrades.
- Circuit breakers at the gateway can protect services but must expose clear client behavior.

