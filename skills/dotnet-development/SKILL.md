---
name: dotnet-development
description: 'Guides ASP.NET Core development with layered architecture, dependency injection, middleware, EF Core, validation, async, cancellation, DTOs, exceptions, logging, and tests.'
---

# Dotnet Development

## Description

Guides ASP.NET Core development with layered architecture, dependency injection, middleware, EF Core, validation, async, cancellation, DTOs, exceptions, logging, and tests.

## Purpose

- Build maintainable ASP.NET Core services with clear boundaries, safe data access, and production-grade behavior.
- Keep business rules out of controllers and persistence details out of application contracts.
- Use .NET platform features (DI, middleware, hosted services, channels, source generators, AOT, gRPC, SignalR) deliberately rather than accidentally.

## When to Use

- Implementing or reviewing ASP.NET Core APIs (MVC controllers or Minimal APIs), gRPC services, SignalR hubs, BackgroundService/IHostedService, EF Core data access, middleware, validation, logging, or tests.
- A .NET service has fat controllers, weak DTO boundaries, sync-over-async, poor exception handling, inefficient EF queries, or unsafe HttpClient usage.
- Adding features that touch transactions, integration, scheduled jobs, real-time push, or production operations.
- The implementation uses messaging, caching, background workers, gateway policies, object storage, search, secrets, or resilience patterns that should be aligned with platform skills.

## Responsibilities

- Define controller / Minimal API endpoint, application service, domain, infrastructure, and persistence responsibilities.
- Use DI with correct lifetimes (`Singleton` / `Scoped` / `Transient`) and avoid captive dependencies.
- Design DTOs, validation, exception mapping (`ProblemDetails` / `IExceptionHandler`), logging scopes, async flows, and `CancellationToken` propagation.
- Inspect EF Core query translation, change tracking, migrations, and connection-pool behavior.
- Choose between MVC controllers and Minimal APIs by team size, OpenAPI tooling needs, filters/conventions, and testability.
- Call related skills: `api-design`, `authn-authz-and-secrets`, `messaging-and-eventing`, `caching-and-distributed-state`, `background-jobs-and-batch-processing`, `logging-metrics-and-tracing`, `resilience-and-fault-tolerance`, `database-reliability-and-operations`.

## Decision Principles

- Controllers/endpoints orchestrate transport concerns; services own use cases; domain code owns rules.
- Use `async`/`await` end-to-end and pass `CancellationToken` to every I/O call. Never `.Result` / `.Wait()`.
- Use DTOs for API contracts; never serialize EF entities directly.
- Prefer explicit `Select` projections and `AsNoTracking()` for read paths; avoid lazy loading entirely in API code.
- Use `IHttpClientFactory` (typed clients) — never `new HttpClient()` per request (socket exhaustion) and never one static `HttpClient` without DNS handling.
- Choose Minimal API for small/internal services and contract-first scenarios; choose MVC controllers for complex filters, conventions, model binding hooks, and large teams used to attribute routing.
- Use `Channel<T>` / `System.IO.Pipelines` for in-process producer-consumer; use a real broker (queue/topic) for cross-process work.
- Source generators (`System.Text.Json`, `[LoggerMessage]`, gRPC, regex) and AOT are first-class for cold-start-sensitive services; they restrict reflection — design for it from the start.

## Expected Output Style

- Start with the decision or finding, then provide the reasoning needed to trust it.
- Show concrete C# snippets for DI registration, endpoint shape, EF projection, exception handler, or `HttpClient` config when they reduce ambiguity.
- Separate immediate fixes (controller/service refactor) from longer-term improvements (architecture, source generators, AOT migration).
- State assumptions about .NET version, hosting model (Kestrel/IIS/containerized), EF provider, and target SLO.
- Avoid generic advice unless followed by an enforceable rule, code shape, or verification step.

## Architecture / Design Guidance

Architecture should use clear layers or vertical slices with explicit dependency direction (transport → application → domain ← infrastructure). Middleware handles cross-cutting HTTP concerns: correlation, exception mapping, authentication, rate-limit headers, response compression. **Resource-level authorization** belongs near the use case (policy handlers or explicit checks in services), not only as `[Authorize]` on endpoints.

EF Core placement:
- Simple CRUD: application services may use `DbContext` directly with discipline (no `DbContext` in controllers, no leakage of `IQueryable` across boundaries).
- Complex domain: repositories or query services hide EF specifics; commands use unit-of-work boundaries.
- Reporting/analytics queries: separate read-side (Dapper, raw SQL, or `FromSqlRaw`) from write-side EF model.

For real-time features, prefer SignalR for browser/mobile push with auth integration; use gRPC streaming for service-to-service. For batch/queue-style in-process work, use `BackgroundService` + `Channel<T>` with bounded capacity and graceful shutdown via `IHostApplicationLifetime`.

For banking/insurance workloads, preserve audit fields, authorization context, idempotency keys, and safe error mapping across controllers, services, outbox publishers, and integration clients. Use `IOptions<T>` + `IValidateOptions<T>` to fail fast on misconfiguration at startup.

## Implementation Guidance

- **Validation**: `DataAnnotations`, `FluentValidation`, or Minimal API endpoint filters. Validate DTOs at the boundary; enforce domain invariants inside aggregates.
- **Errors**: standard `ProblemDetails` via `IExceptionHandler` (.NET 8+) or middleware. Map domain exceptions to stable error codes; never leak stack traces in production.
- **Logging**: `ILogger<T>` with **logging source generators** (`[LoggerMessage]`) for hot paths to avoid boxing/allocation; structured fields, no PII.
- **HTTP clients**: `IHttpClientFactory` + typed clients + `Microsoft.Extensions.Http.Resilience` (.NET 8+) or Polly for timeout / retry / circuit breaker / hedging. Configure per-named-client timeouts, not one global `HttpClient.Timeout`.
- **EF Core**: `AsNoTracking()` for reads, explicit `Select` projections, `AsSplitQuery()` for cartesian-explosion joins, compiled queries for hot paths, connection resiliency only with idempotent operations.
- **Migrations**: EF migrations with **expand-contract** sequencing; for large data changes use raw SQL migrations with chunking, not EF `SaveChanges` loops.
- **Background work**: `BackgroundService` + `IServiceScopeFactory` to create scoped services per work item; respect `stoppingToken`; checkpoint progress.
- **Outbox / messaging**: write outbox row in same transaction as state change; relay process publishes asynchronously; consumers are idempotent (use `MediatR` pipeline behavior or explicit dispatcher).
- **Secrets**: managed identities (Azure/AWS), `Microsoft.Extensions.Configuration` providers (Key Vault / Secrets Manager / Parameter Store), never `appsettings.json` for prod secrets.
- **Telemetry**: OpenTelemetry SDK (`OpenTelemetry.Extensions.Hosting`), exporters for OTLP; instrument HTTP, EF Core (`OpenTelemetry.Instrumentation.EntityFrameworkCore`), runtime metrics.
- **AOT / Trimming**: enable for cold-start-sensitive services (Lambdas, Functions, K8s scale-to-zero); audit reflection use, switch to source-generated JSON, verify all DI factories.

## Testing Expectations

- Unit test domain and application services with no DI container; inject fakes/mocks for I/O.
- Integration test APIs with `WebApplicationFactory<TProgram>` + Testcontainers (real DB) for data behavior; avoid `Microsoft.EntityFrameworkCore.InMemory` for query-shape tests.
- Test EF migrations against a fresh DB and against a migrated copy of production-like data.
- Test cancellation and timeout: client disconnects must propagate `OperationCanceledException` and free DB/HTTP resources.
- Test idempotent retries, outbox publishing on commit/rollback, BackgroundService restart safety, cache authorization safety, and PII redaction in logs.
- Performance: `BenchmarkDotNet` for hot paths only; load tests (`k6`, `NBomber`) for endpoint-level SLO validation.

## Security / Performance / Reliability Considerations

Security requires authentication middleware ordering (UseRouting → UseAuthentication → UseAuthorization → endpoints), policy- or resource-based authorization (`IAuthorizationHandler`), safe model binding (avoid over-posting via DTOs), antiforgery for cookie-auth MVC apps, managed secrets, and audit-safe logs. Never log JWTs, refresh tokens, connection strings, or full request bodies.

Performance requires `Select` projections, `AsNoTracking`, no N+1 (verify with EF Core logging or MiniProfiler), bounded result sets, connection pool sizing matching DB capacity (not per-instance defaults), `HttpClient` reuse via factory, `ArrayPool<T>` / `Memory<T>` for high-throughput allocations, and response compression for large payloads.

Reliability requires `CancellationToken` everywhere, request timeouts (`RequestTimeouts` middleware in .NET 8+), bounded retries only around safe operations, idempotent message handlers, durable outbox, `IHostApplicationLifetime` for graceful shutdown, and traceable failures via correlation IDs.

## Review Checklist

- Controllers / Minimal API endpoints are thin (no business logic, no direct DB calls).
- DTOs protect API boundaries; no EF entities exposed.
- DI lifetimes are correct; no scoped-into-singleton captures.
- `CancellationToken` flows from endpoint to every I/O call.
- EF queries use `Select` projections, `AsNoTracking` for reads, no lazy loading.
- `HttpClient` always via `IHttpClientFactory` with timeouts and resilience policies.
- Errors map to consistent `ProblemDetails` with stable error codes.
- Logs use structured fields and source generators on hot paths; no sensitive data.
- Outbox / idempotency present when publishing messages or calling external side effects.
- Migrations follow expand-contract; large backfills are chunked outside EF.
- Platform concerns are delegated to the relevant skill instead of being solved ad hoc.

## Anti-Patterns to Avoid

- Business logic in controllers or Minimal API lambdas.
- Returning EF entities directly (over-posting, lazy-loading explosions, leak of internal shape).
- `async void`, `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` on async code.
- Injecting `Scoped` services into `Singleton` services (captive dependency).
- Lazy loading inside JSON serialization (turn off lazy loading in API projects).
- `catch (Exception) { return Ok(); }` swallowing failures.
- `new HttpClient()` per request, or one static `HttpClient` without `SocketsHttpHandler.PooledConnectionLifetime`.
- Publishing messages, writing files, or calling partners inside an EF transaction without idempotency, outbox, timeout, and compensation design.
- Using `appsettings.json` for production secrets or committing them to source.
- Enabling AOT/trimming without auditing reflection, JSON serialization, and DI factories.

## Gotchas / Common Failure Modes

- EF Core LINQ can translate unexpectedly or silently fall back to client evaluation in older versions; .NET 6+ throws — but only at runtime.
- `DbContext` is **not thread-safe** — never share across parallel `Task.WhenAll` operations.
- `IHttpClientFactory`'s default handler lifetime (2 min) recycles sockets; static `HttpClient` ignores DNS changes for the process lifetime.
- Automatic retries (resilience pipelines, EF connection resiliency, broker redelivery) duplicate non-idempotent side effects unless explicitly protected.
- Middleware order changes security: misplacing `UseAuthentication` after `UseEndpoints` silently disables auth.
- Configuration values not validated at startup (`IValidateOptions<T>`) cause runtime crashes far from the source.
- `BackgroundService` exceptions in .NET 6+ crash the host by default unless `BackgroundServiceExceptionBehavior.Ignore` is set; in .NET 5- they were silently swallowed — both are dangerous defaults to know.
- `HttpClient.Timeout` is per-call total; per-attempt timeouts in resilience pipelines must be strictly less to allow retries.
- AOT-compiled apps fail at runtime on reflection-heavy libraries (older `Newtonsoft.Json`, AutoMapper without source generator, some DI containers); test in Release+AOT, not Debug.
- Connection pool exhaustion shows as request timeouts, not DB errors — usually caused by leaked `DbContext`s or over-large per-instance pool × autoscaled replicas.
- Source-generated JSON (`JsonSerializerContext`) can't serialize types it wasn't told about — runtime `NotSupportedException` in production only.

