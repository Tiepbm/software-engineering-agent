---
name: application-stacks-pack
description: 'Use when implementing in a specific framework: ASP.NET Core/EF Core, Spring Boot/JPA, React (Next/Remix/Vite), Angular, or React Native. Routes broader platform concerns OUT to other packs.'
---
# Application Stacks Pack

## When to Use
- Framework-specific patterns (DI, middleware, hooks, signals, RxJS, hydration, navigation, state, forms).
- Stack-specific gotchas (N+1, hydration mismatch, NgZone, Hermes, OTA, RSC, AOT, virtual threads, Minimal API vs MVC).
- Stack-specific tests (xUnit, JUnit/Spring Test, Vitest/Jest, Detox/Maestro).
- Stack-specific build/release pipelines (NuGet, Maven/Gradle, Vite, Metro, EAS).

## When NOT to Use
- Cross-cutting platform design (messaging, caching, security, storage, search, observability) → respective platform pack.
- API contract design (idempotency, versioning, pagination) → `core-engineering-pack` → `api-design`.
- Database schema, query plan, or migration → `data-database-analytics-pack`.

## Pack Reference Map
| Reference | Use when |
|---|---|
| `dotnet-development` | Use when writing .NET / ASP.NET Core / EF Core / gRPC / SignalR / channels / source-generators / AOT code. |
| `java-spring-boot-development` | Use when writing Spring Boot 3 / WebFlux vs MVC / virtual threads / Spring Modulith / JPA / Kafka-RabbitMQ patterns. |
| `reactjs-development` | Use when writing React 18/19 / RSC / Suspense / TanStack Query / Zustand-Jotai-Redux / Next.js-Remix-Vite. |
| `angular-development` | Use when writing Angular standalone APIs / signals / RxJS decisions / functional interceptors / SSR/hydration / NgRx. |
| `react-native-development` | Use when writing React Native New Architecture / Hermes / Expo vs bare / OTA / iOS-Android production differences. |

## Cross-Pack Handoffs
- → `core-engineering-pack` for API contracts and testing strategy that cross stacks.
- → `platform-integration-pack` for messaging, gateway, or job code wired into the app.
- → `resilience-performance-pack` for caching, timeouts, circuit breakers wired into the app.
- → `security-access-pack` for authn/authz wiring and secret handling in the app.
- → `observability-release-pack` for telemetry instrumentation and release pipelines.
- → `storage-search-pack` for object-storage/search SDK integration in the app.

