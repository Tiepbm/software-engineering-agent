---
name: java-spring-boot-development
description: 'Guides Spring Boot REST services with layering, JPA, validation, transactions, exception handling, security, DTO mapping, integration tests, and N+1 avoidance.'
---
> **SCOPE NOTE (v1.x):** This reference is now a **stack-level decision matrix** (versions, AOT/RSC/virtual-thread, Modulith, Expo-vs-bare, RxJS-vs-signals trade-offs). For *implementation* (writing handlers, components, hooks, queries, tests, migrations), hand off to **`coding-assistant-agent`** per `HANDOFF-PROTOCOL.md`. Pre-existing implementation snippets below are kept only as reference for the trade-off discussion — they are not the canonical place to copy code from.


# Java Spring Boot Development

## Description

Guides Spring Boot REST services with layering, JPA, validation, transactions, exception handling, security, DTO mapping, integration tests, and N+1 avoidance.

## Purpose

- Build Spring Boot services with clear controller/service/repository boundaries, safe transactions, and predictable persistence.
- Avoid common JPA traps such as lazy-loading surprises, N+1 queries, and transaction leakage across `@Async` / `@Transactional` boundaries.
- Make APIs secure, testable, and operationally clear under Spring Boot 3, Jakarta EE namespace, virtual threads, and AOT/Native compilation.

## When to Use

- Implementing or reviewing Spring Boot REST APIs (Spring MVC or WebFlux), services, repositories, JPA entities, transactions, validation, security, scheduled jobs, Kafka/RabbitMQ listeners, or integration tests.
- A service has fat controllers, unclear transactions, exposed entities, lazy loading errors, inconsistent error handling, or N+1 queries discovered only at production cardinality.
- Adding features that change persistence, authorization, external integrations, or messaging.
- The service uses messaging, caching, scheduled jobs, gateway integration, object storage, search, secrets, or resilience libraries that should follow platform guidance.

## Responsibilities

- Keep controllers focused on HTTP, validation, and response mapping.
- Put use-case orchestration and transaction boundaries in services.
- Use repositories (Spring Data) for persistence access; add `@Query` / Querydsl / native SQL for explicit read paths.
- Define DTOs (records or classes), `@ControllerAdvice` exception handlers, Bean Validation, Spring Security policies, and integration tests with Testcontainers.
- Choose between Spring MVC (servlet, blocking, virtual threads in Boot 3.2+) and WebFlux (reactive, Project Reactor) by workload shape, team familiarity, and downstream client model.
- Call related skills: `api-design`, `authn-authz-and-secrets`, `messaging-and-eventing`, `caching-and-distributed-state`, `background-jobs-and-batch-processing`, `logging-metrics-and-tracing`, `resilience-and-fault-tolerance`, `database-reliability-and-operations`.

## Decision Principles

- Do not expose JPA entities as API contracts; use records / DTOs and explicit mappers (MapStruct or hand-written).
- Place `@Transactional` at service boundaries, not randomly across helpers; default isolation is engine-dependent — be explicit when it matters.
- Prefer explicit fetch plans (`@EntityGraph`, JOIN FETCH, projection interfaces, DTO projections) over default lazy loading for known read paths.
- Use Bean Validation (`jakarta.validation`) for input shape; enforce business invariants in domain code, not annotations.
- Spring MVC + virtual threads (Boot 3.2+ / Java 21) is usually the right default for new blocking-style services; choose WebFlux only when the entire call chain (DB driver, HTTP clients, downstream APIs) is reactive and high-concurrency I/O is the bottleneck.
- For cross-module monoliths, consider Spring Modulith to enforce module boundaries at compile/test time before splitting into microservices.
- Keep Spring Security, transaction, retry, cache, and async annotations aligned with use-case semantics; annotations must not hide unsafe side effects, authorization gaps, or proxy limitations (no self-invocation).

## Expected Output Style

- Start with the decision or finding, then the reasoning needed to trust it.
- Show concrete Java/Kotlin snippets for controller signature, service boundary, JPA fetch plan, exception handler, or `RestClient`/`WebClient` config when they reduce ambiguity.
- Separate immediate fixes from longer-term improvements (Modulith, Native, virtual threads migration).
- State assumptions about Spring Boot version, Java version, JPA provider (Hibernate version), DB engine, and target SLO.
- Avoid generic advice unless followed by an enforceable rule, code shape, or verification step.

## Architecture / Design Guidance

Architecture should separate REST contracts (controllers + DTOs), application services (use cases + transaction boundaries), domain behavior (entities + value objects + domain services), persistence (repositories + custom queries), integration clients (typed `RestClient` / `WebClient` / Feign), messaging adapters (Kafka/RabbitMQ listeners + producers), schedulers, and configuration. Persistence model **must not** dictate API model.

Spring Security rules must align with method-level (`@PreAuthorize`) or resource-level authorization implemented in services. Endpoint-level `.requestMatchers(...)` is necessary but not sufficient for resource ownership checks.

For banking/insurance workloads, carry audit context, tenant context, idempotency keys, and safe error codes through controllers, services, transactions, outbox publishers, and partner clients. Use `@ConfigurationProperties` + `@Validated` for fail-fast startup; avoid scattered `@Value` lookups.

Spring Modulith is the recommended path before microservices: define modules with package-level boundaries, verify with `ApplicationModules.of(App.class).verify()` in tests, and emit `ApplicationEventPublisher` events between modules with transactional event listeners.

For long-running or async work, prefer Spring Batch (chunked jobs with checkpointing) over hand-rolled `@Scheduled` loops; prefer `@KafkaListener` with manual ack and `DefaultErrorHandler` over fire-and-forget consumers.

## Implementation Guidance

- **Controllers**: thin; use records as DTOs; return `ResponseEntity<T>` or domain DTO directly; never return `Entity` types.
- **Errors**: `@RestControllerAdvice` with `ProblemDetail` (Spring 6+) for stable error contracts; map domain exceptions to error codes; never leak stack traces.
- **Validation**: `@Valid` on `@RequestBody`; group validations for create vs update; custom `ConstraintValidator` for business rules at the boundary only.
- **Persistence**: prefer `JpaRepository` + `@Query`/`@EntityGraph` over derived method names for non-trivial queries; use DTO projections (`interface` or `record`) for read endpoints to avoid loading full entities; use Hibernate `@BatchSize` or `@Fetch(SUBSELECT)` to mitigate N+1 in known paths.
- **Transactions**: `@Transactional` on service methods; `readOnly = true` for reads (enables Hibernate optimizations); be explicit about propagation for nested calls; understand that **self-invocation bypasses the proxy** (call goes through `this`, no transaction starts).
- **HTTP clients**: `RestClient` (Spring 6.1+) for synchronous calls; `WebClient` for reactive or high-concurrency I/O; configure timeouts (`connect`, `read`, `write`, `response`) per client; wrap with Resilience4j (`@Retry`, `@CircuitBreaker`, `@TimeLimiter`, `@Bulkhead`).
- **Migrations**: Flyway or Liquibase; expand-contract sequencing; large data migrations use `@Procedure` or raw SQL with batching, not entity-level loops.
- **Concurrency**: optimistic locking with `@Version` for contested entities; Hibernate `LockModeType.PESSIMISTIC_WRITE` only for short critical sections.
- **Messaging**: transactional outbox (`spring-modulith-events` jdbc/jpa publisher, or hand-rolled outbox table); `@KafkaListener` with `@Transactional` + manual ack; idempotent consumers using business key or event ID with a processed-events table.
- **Scheduling**: `@Scheduled` for simple cron; Spring Batch or Quartz for restartable, chunked, monitored jobs.
- **Caching**: `@Cacheable` only with explicit cache name, key, TTL, and `unless` conditions; never cache permissions/balances without invalidation hooks.
- **Secrets**: Spring Cloud Config + Vault, AWS Secrets Manager, GCP Secret Manager via `spring-cloud-*-bootstrap`; never `application.yml` for prod secrets.
- **Telemetry**: Micrometer + OpenTelemetry exporter (`io.micrometer:micrometer-tracing-bridge-otel`); Spring Boot Actuator endpoints scoped behind security; structured JSON logs via Logback encoder.
- **Native / AOT**: Spring Boot 3 supports GraalVM Native Image via `spring-boot-starter-parent`; audit reflection, runtime hints, dynamic proxies, and `@ConditionalOnClass` chains; test in Native, not just JVM.
- **Virtual threads** (Java 21 + Boot 3.2+): enable via `spring.threads.virtual.enabled=true`; **do not pin virtual threads** with `synchronized` blocks holding I/O — use `ReentrantLock` instead.

## Testing Expectations

- Unit test domain and service logic without Spring context.
- Use `@WebMvcTest`, `@DataJpaTest`, `@JsonTest` for slice tests; full `@SpringBootTest` only when integration boundaries matter.
- Use **Testcontainers** with the real database engine for JPA behavior — never H2 for query-shape tests (different SQL dialect, different lazy semantics).
- Test transactions, validation, authorization, N+1-sensitive endpoints (assert query count with `datasource-proxy` or Hibernate statistics), and migrations against a production-like schema.
- Test idempotent retries, outbox/message redelivery, scheduled-job restart, cache authorization safety, and telemetry redaction when those features are present.
- Performance: JMH for hot-path microbenchmarks; load tests (`Gatling`, `k6`) for endpoint-level SLO validation.

## Security / Performance / Reliability Considerations

Security requires authentication (OAuth2 Resource Server with JWT validation: issuer, audience, expiry, signature), resource authorization (`@PreAuthorize` + service-level checks), CSRF discipline (disable for stateless JWT APIs only), CORS configuration via `CorsConfigurationSource`, safe deserialization (avoid polymorphic Jackson without `@JsonTypeInfo` allowlists), managed secrets, and audit-safe logs. Spring Security filter chain ordering matters — verify with `SecurityFilterChain` debug logs.

Performance requires query inspection (Hibernate SQL logging or `p6spy` in dev), batching (`hibernate.jdbc.batch_size`, `order_inserts`, `order_updates`), pagination (`Pageable`, prefer keyset over offset), HikariCP pool tuning matching DB capacity (not per-instance defaults), cache discipline, and avoiding lazy loading during JSON serialization (use DTO projections or `@JsonIgnoreProperties({"hibernateLazyInitializer"})`).

Reliability requires timeouts on every external call, bounded retries around safe operations only (Resilience4j `@Retry` + `@CircuitBreaker` composition), idempotent message handlers, durable outbox, graceful shutdown (`server.shutdown=graceful` + `spring.lifecycle.timeout-per-shutdown-phase`), and observable integration failures.

## Review Checklist

- Layers are clear; controllers do not call repositories.
- DTO mapping is explicit; entities are not exposed.
- Transaction boundaries are intentional; `readOnly` set for reads.
- JPA fetch strategy is reviewed; N+1 is verified with query counts in tests.
- Validation and errors are consistent; `ProblemDetail` returned uniformly.
- Security rules protect resources at both endpoint and service level.
- Testcontainers used for JPA tests; H2 banned for query-shape tests.
- HTTP clients have per-client timeouts and resilience policies.
- Outbox / idempotency present when publishing messages or calling external side effects.
- Migrations follow expand-contract; large backfills batched outside JPA.
- Virtual threads enabled (where appropriate) with no `synchronized`-pinning hot paths.
- Platform concerns are routed to the appropriate skill instead of being hidden behind annotations.

## Anti-Patterns to Avoid

- Business logic in controllers.
- Open Session in View (`spring.jpa.open-in-view=true`) — silently hides lazy-loading problems and leaks transactions into HTTP rendering. **Disable in production.**
- Exposing JPA entities directly in REST responses.
- `@Transactional` on every method (defeats explicit boundaries; obscures self-invocation issues).
- Self-invocation of `@Transactional` / `@Async` / `@Cacheable` / `@Retryable` methods (bypasses the proxy — annotation does nothing).
- Ignoring N+1 because tests use tiny data; only production cardinality reveals it.
- `catch (Exception e) { return null; }` swallowing failures.
- Combining `@Transactional` + `@Async` on the same method (transaction context does **not** propagate across thread switch).
- Combining `@Transactional` + Kafka publish without outbox — message can be sent then transaction rollback leaves an orphan event.
- Using H2 in tests when production is PostgreSQL/MySQL/Oracle.
- Hand-rolled HMAC, JWT validation, or password hashing instead of Spring Security primitives.
- Pinning virtual threads with `synchronized` blocks that perform I/O (use `ReentrantLock`).

## Gotchas / Common Failure Modes

- Lazy loading throws `LazyInitializationException` outside transactions or, with OSIV enabled, silently runs N+1 queries during JSON serialization.
- `equals` / `hashCode` on JPA entities using auto-generated IDs causes set/map bugs before persist; use business key or `@NaturalId` instead.
- Cascade settings (`CascadeType.ALL`, `orphanRemoval=true`) can delete more than intended on detached entity merges.
- Default Jackson serialization can leak fields not annotated `@JsonIgnore`; use DTOs or explicit views.
- Connection pool exhaustion shows as application slowness, not DB errors — usually HikariCP `maximumPoolSize` × replicas exceeds DB max connections.
- Scheduler overlap: `@Scheduled` with overlapping execution times runs concurrently unless `fixedDelay` or distributed lock (ShedLock) is used.
- Kafka consumer redelivery on poison messages causes infinite reprocessing without `DefaultErrorHandler` + DLQ.
- Spring proxy-based annotations (`@Transactional`, `@Async`, `@Cacheable`, `@Retryable`) do not work on `private`/`final` methods or self-invocation.
- Secret rotation breaks long-running instances if Spring Cloud Config refresh / `@RefreshScope` is not configured.
- AOT/Native: missing reflection/serialization hints fail at runtime in Native binary but pass in JVM tests; verify with native build CI step.
- Virtual thread pinning via `synchronized` reduces concurrency to platform-thread count — invisible until load testing.
- `@Transactional(readOnly = true)` on Hibernate enables flush-mode skip; accidental writes inside read-only TX silently fail at flush.

## Code Examples

### Transactional Outbox Pattern

```java
// 1. Outbox entity
@Entity
@Table(name = "outbox_events")
public class OutboxEvent {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private UUID aggregateId;
    private String eventType;
    @Column(unique = true) private UUID eventId;
    @JdbcTypeCode(SqlTypes.JSON) private String payload;
    private UUID correlationId;
    private Instant createdAt;
    private Instant publishedAt; // null = not yet published
    private int retryCount;
}

// 2. Service writes state + outbox in one transaction
@Service
@RequiredArgsConstructor
public class PaymentService {
    private final PaymentRepository payments;
    private final OutboxRepository outbox;

    @Transactional
    public Payment capturePayment(CaptureCommand cmd) {
        Payment payment = payments.findByIdAndVersion(cmd.paymentId(), cmd.expectedVersion())
            .orElseThrow(() -> new OptimisticLockException("Payment modified"));
        payment.capture(cmd.pspReference());
        payments.save(payment);

        outbox.save(OutboxEvent.builder()
            .aggregateId(payment.getId())
            .eventType("payment.captured")
            .eventId(UUID.randomUUID())
            .payload(toJson(new PaymentCapturedEvent(payment)))
            .correlationId(cmd.correlationId())
            .createdAt(Instant.now())
            .build());
        return payment;
    }
}

// 3. Relay worker publishes and marks as sent
@Component @RequiredArgsConstructor
public class OutboxRelay {
    private final OutboxRepository outbox;
    private final KafkaTemplate<String, String> kafka;

    @Scheduled(fixedDelay = 500)
    @Transactional
    public void relay() {
        List<OutboxEvent> pending = outbox.findTop100ByPublishedAtIsNullOrderByCreatedAt();
        for (OutboxEvent event : pending) {
            try {
                kafka.send("payments.events", event.getAggregateId().toString(), event.getPayload()).get();
                event.setPublishedAt(Instant.now());
            } catch (Exception e) {
                event.setRetryCount(event.getRetryCount() + 1);
                log.warn("Outbox relay failed for event {}: {}", event.getEventId(), e.getMessage());
            }
        }
    }
}
```

### Idempotent Kafka Consumer

```java
@Component @RequiredArgsConstructor
public class ClaimEventConsumer {
    private final ProcessedEventRepository processedEvents;
    private final ClaimService claimService;

    @KafkaListener(topics = "claims.events", groupId = "claim-processor")
    @Transactional
    public void handle(ConsumerRecord<String, String> record) {
        ClaimEvent event = parse(record.value());

        // Idempotency check: skip if already processed
        if (processedEvents.existsByEventId(event.eventId())) {
            log.info("Skipping duplicate event: {}", event.eventId());
            return;
        }

        // Process
        claimService.applyEvent(event);

        // Mark as processed (in same transaction)
        processedEvents.save(new ProcessedEvent(event.eventId(), Instant.now()));
    }
}
```

### Resource-Level Authorization

```java
@Component
public class ClaimOwnershipChecker implements PermissionEvaluator {
    private final ClaimRepository claims;

    @Override
    public boolean hasPermission(Authentication auth, Object target, Object permission) {
        if (target instanceof UUID claimId) {
            Claim claim = claims.findById(claimId).orElse(null);
            if (claim == null) return false;

            UserPrincipal user = (UserPrincipal) auth.getPrincipal();
            return switch (permission.toString()) {
                case "VIEW" -> claim.getAssigneeId().equals(user.getId())
                    || user.getRoles().contains("ADMIN");
                case "APPROVE" -> user.getRoles().contains("SENIOR_ADJUSTER")
                    && !claim.getAssigneeId().equals(user.getId()); // separation of duties
                default -> false;
            };
        }
        return false;
    }
}

// Usage in service
@PreAuthorize("hasPermission(#claimId, 'APPROVE')")
public Claim approveClaim(UUID claimId, ApprovalCommand cmd) { ... }
```

### Resilience4j Circuit Breaker + Retry

```java
@Configuration
public class ResilienceConfig {
    @Bean
    public CircuitBreakerConfig cbConfig() {
        return CircuitBreakerConfig.custom()
            .failureRateThreshold(50)
            .waitDurationInOpenState(Duration.ofSeconds(30))
            .slidingWindowSize(10)
            .permittedNumberOfCallsInHalfOpenState(2)
            .build();
    }
}

@Service @RequiredArgsConstructor
public class PspClient {
    private final RestClient restClient;

    @CircuitBreaker(name = "psp", fallbackMethod = "pspFallback")
    @Retry(name = "psp", fallbackMethod = "pspFallback")
    @TimeLimiter(name = "psp")
    public PspResponse submitPayment(PspRequest request) {
        return restClient.post()
            .uri("/v1/payments")
            .header("Idempotency-Key", request.idempotencyKey().toString())
            .body(request)
            .retrieve()
            .body(PspResponse.class);
    }

    private PspResponse pspFallback(PspRequest request, Exception ex) {
        log.error("PSP unavailable for payment {}: {}", request.paymentId(), ex.getMessage());
        // Return pending status — reconciliation job will resolve later
        return PspResponse.pending(request.paymentId(), "PSP_UNAVAILABLE");
    }
}
```

