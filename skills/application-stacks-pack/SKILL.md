---
name: application-stacks-pack
description: 'Use when making stack-LEVEL decisions: framework choice, version/AOT/RSC/virtual-thread/Modulith trade-offs, build/release pipeline architecture for ASP.NET Core, Spring Boot, React, Angular, or React Native. Implementation handoff -> coding-assistant-agent.'
---
# Application Stacks Pack — Stack Decision Lens

> **Scope changed in v1.x:** This pack is now a **stack-level decision lens**, not an implementation playbook. For *writing* handlers, components, hooks, migrations, tests, or instrumentation, hand off to **`coding-assistant-agent`** per `HANDOFF-PROTOCOL.md`.

## When to Use
- Choosing a framework or major version (Spring MVC vs WebFlux; React Next.js vs Remix vs Vite; Angular standalone vs module; .NET MVC vs Minimal API).
- Evaluating runtime/feature-level trade-offs that change architecture: virtual threads, AOT/Native compilation, Spring Modulith, React Server Components, Angular signals, React Native New Architecture, Hermes.
- Stack-level pipeline architecture (NuGet vs source-generators; Gradle vs Maven; Vite vs Metro; EAS vs bare).
- Stack-level dependency upgrade plans (Spring Boot 2 -> 3, .NET LTS jump, React 18 -> 19, Angular major).

## When NOT to Use
- Writing a handler, component, hook, query, migration, or test in a stack -> **`coding-assistant-agent`** (`backend-pack`, `frontend-pack`, `mobile-pack`, `database-pack`).
- Cross-cutting platform design (messaging, caching, security, storage, search, observability) → respective CE7 platform pack.
- API contract design (idempotency, versioning, pagination) → `core-engineering-pack/api-design`.
- Database schema, query plan, or migration design → `data-database-analytics-pack`.

## Pack Reference Map
Each reference is a **decision matrix + version/feature trade-off**, not implementation code. For implementation, follow the handoff link.

| Reference | Use when |
|---|---|
| `dotnet-development` | Decide between .NET versions / Minimal API vs MVC / EF Core vs Dapper / AOT trade-offs. Implementation -> `coding-assistant-agent/skills/backend-pack/dotnet-aspnet-core`. |
| `java-spring-boot-development` | Decide between Spring Boot versions / WebFlux vs MVC / virtual threads / Spring Modulith / JPA vs jOOQ / Kafka vs RabbitMQ. Implementation -> `coding-assistant-agent/skills/backend-pack/java-spring-boot` or `kotlin-spring`. |
| `reactjs-development` | Decide between React 18/19 / RSC adoption / Next.js vs Remix vs Vite / TanStack vs Zustand vs Redux. Implementation -> `coding-assistant-agent/skills/frontend-pack/react-nextjs`. |
| `angular-development` | Decide between Angular standalone / signals adoption / RxJS retention / SSR/hydration / NgRx vs Signals state. Implementation -> `coding-assistant-agent/skills/frontend-pack/angular`. |
| `react-native-development` | Decide on React Native New Architecture / Hermes / Expo vs bare / OTA channel strategy. Implementation -> `coding-assistant-agent/skills/mobile-pack/react-native`. |

## Cross-Pack Handoffs
- → `core-engineering-pack` for API contracts and testing strategy that cross stacks.
- → `platform-integration-pack` for messaging, gateway, or job design that the app will wire into.
- → `resilience-performance-pack` for caching, timeouts, circuit breakers strategy.
- → `security-access-pack` for authn/authz pattern and secret handling policy.
- → `observability-release-pack` for telemetry strategy and release pipeline policy.
- → `storage-search-pack` for object-storage/search projection design.
- → `coding-assistant-agent` (per `HANDOFF-PROTOCOL.md`) for **all implementation** once the stack-level decision is made.

