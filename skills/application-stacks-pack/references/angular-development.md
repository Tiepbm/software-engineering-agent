---
name: angular-development
description: 'Guides Angular applications with feature structure, services, RxJS, reactive forms, guards, interceptors, state handling, testability, and scalable frontend design.'
---
> **SCOPE NOTE (v1.x):** This reference is now a **stack-level decision matrix** (versions, AOT/RSC/virtual-thread, Modulith, Expo-vs-bare, RxJS-vs-signals trade-offs). For *implementation* (writing handlers, components, hooks, queries, tests, migrations), hand off to **`coding-assistant-agent`** per `HANDOFF-PROTOCOL.md`. Pre-existing implementation snippets below are kept only as reference for the trade-off discussion — they are not the canonical place to copy code from.


# Angular Development

## Description

Guides Angular applications with feature structure, standalone components, signals, RxJS, reactive forms, guards, interceptors, state handling, testability, and scalable frontend design across Angular 16/17/18+.

## Purpose

- Build Angular applications with clear feature boundaries, predictable reactive flows, and maintainable components.
- Use RxJS deliberately without creating nested subscriptions, leaky abstractions, or over-engineered streams when signals suffice.
- Adopt modern Angular: standalone components, signals, the new control flow (`@if`/`@for`/`@switch`), `inject()`, and SSR with hydration.
- Keep components focused on presentation and interaction orchestration.

## When to Use

- Implementing or reviewing Angular features, services, reactive forms, route guards, interceptors, state, API integration, signals, SSR, or tests.
- The app has overloaded components, nested subscriptions, duplicated service logic, memory leaks, OnPush rendering issues, or unclear state ownership.
- A frontend needs scalable feature organization, signals migration, NgModule → standalone migration, or production readiness.
- The app handles regulated data, token/session behavior, gateway errors, rate limits, file transfer, search/list UX, or telemetry for critical workflows.
- Choosing between RxJS-based services, signals, NgRx (Store / Signals / Component Store), Akita, or simple service streams.

## Responsibilities

- Define feature areas (standalone-first; NgModules only for legacy or library packaging), smart/presentational components where useful, services, state boundaries, forms, guards, and interceptors.
- Design observable streams with cancellation, error handling, and lifecycle management (`takeUntilDestroyed`, async pipe).
- Choose between signals (synchronous derived state, fine-grained change detection) and RxJS (async streams, time-based composition, multi-source merging).
- Review accessibility, performance, change detection strategy, and testability.
- Keep API clients and mapping logic out of templates.
- Involve `api-design`, `authn-authz-and-secrets`, `security-review`, `rate-limiting-and-traffic-control`, `file-and-object-storage`, `search-and-indexing`, `logging-metrics-and-tracing`, `performance-engineering` when Angular code depends on platform contracts.

## Decision Principles

- Prefer **standalone components** for new code (Angular 15+); migrate NgModules incrementally.
- Use **reactive forms** for complex validation and dynamic behavior; template-driven forms only for trivial inputs.
- Use **signals** for synchronous state derivation, computed values, and template binding with fine-grained change detection (Angular 16+); use **RxJS** for async/time/multi-source streams (HTTP, websockets, debounced inputs).
- Avoid nested subscriptions; compose streams with `switchMap`, `mergeMap`, `concatMap`, or `exhaustMap` based on concurrency semantics — see Gotchas for the choice rules.
- Use `async` pipe (auto-unsubscribes on destroy) or `takeUntilDestroyed()` (Angular 16+ injection-context-aware) for lifecycle safety; never manually subscribe in components without unsubscribe management.
- Put cross-cutting HTTP behavior (auth, correlation, gateway error mapping, retry policy, rate-limit handling) in **functional interceptors** (`HttpInterceptorFn`, Angular 15+).
- Treat guards (`CanActivate`, `CanMatch`) and client-side permissions as **navigation UX**; backend APIs remain authoritative for regulated resource access and business decisions.
- For state management: service streams + signals first → Component Store for complex local state → NgRx Store only for true global, time-traveled, devtools-debugged shared state.

## Expected Output Style

- Start with the decision or finding, then the reasoning needed to trust it.
- Show concrete TypeScript snippets for component shape, service stream, interceptor, signal/computed, RxJS operator chain, or form group when they reduce ambiguity.
- Separate immediate fixes from longer-term improvements (standalone migration, signals adoption, SSR, NgRx → signal store).
- State assumptions about Angular version (≥16 for signals, ≥17 for new control flow + SSR with hydration, ≥18 for zoneless preview), Angular Material/CDK usage, and target browsers.
- Avoid generic advice unless followed by an enforceable rule, code shape, or verification step.

## Architecture / Design Guidance

Architecture should be **feature-based**, not type-folder-only at scale: `features/billing/`, `features/claims/` each owns components, services, routes, and state. Shared concerns go to `core/` (singleton services, guards, interceptors) and `shared/` (presentational components, pipes, directives).

Services own data access and reusable workflows; components consume signals/observables exposed by services. Functional interceptors centralize auth/session, correlation IDs, gateway error mapping (4xx → user-actionable, 5xx → retry/circuit-break), rate-limit handling (429 + Retry-After), and safe retry policy (only on idempotent verbs).

Guards protect navigation UX but **backend authorization remains authoritative**. Use `CanMatch` over `CanActivate` for route-level lazy loading + permission checks (avoids loading the chunk if denied).

State management progression:
1. Local component state with signals.
2. Feature service exposing signals + observables; components subscribe via `async` pipe or signal binding.
3. Component Store (`@ngrx/component-store`) for complex local state with derived selectors.
4. NgRx Store / Signal Store (`@ngrx/signals`) for global state shared across unrelated features.

For SSR (Angular Universal in 16-, native SSR with hydration in 17+): use `provideClientHydration()`, avoid `window`/`document` access in components (use `isPlatformBrowser`), defer non-critical work with `afterNextRender`/`afterRender` (Angular 16+).

For banking/insurance screens, design masking, confirmation dialogs, duplicate-submit protection (disable button + idempotency key), accessible forms, and recovery UX for payments, claims, policy changes, document uploads, and quote flows.

## Implementation Guidance

- **Components**: standalone with `imports: [...]`; use `ChangeDetectionStrategy.OnPush`; bind via signals or `async` pipe; use new control flow `@if/@for/@switch` (Angular 17+) for better type narrowing and performance.
- **Services**: `providedIn: 'root'` for app-wide singletons; `providedIn: 'any'` rarely; feature services provided in route data for lazy isolation.
- **DI**: use `inject()` function over constructor injection in modern code (works in factories, route resolvers, interceptors, guards).
- **HTTP**: `HttpClient` with typed responses; functional interceptors registered via `provideHttpClient(withInterceptors([...]))`; use `HttpParams`/`HttpHeaders` builders, never string concatenation.
- **Forms**: typed `FormGroup`/`FormControl` (Angular 14+); custom `Validator` + `AsyncValidator`; track touched/dirty/valid for UX; cross-field validators on `FormGroup` level.
- **RxJS operators**: `switchMap` for cancel-previous (typeahead), `mergeMap` for parallel (file uploads with concurrency), `concatMap` for ordered serial (form submits), `exhaustMap` for ignore-while-busy (login/save buttons). See Gotchas for safety rules.
- **Signals** (Angular 16+): `signal()`, `computed()`, `effect()` for reactive primitives; use `toSignal()` to bridge observables; use `toObservable()` to bridge back when needed.
- **Lifecycle**: `takeUntilDestroyed()` (Angular 16+) over manual `Subject` + `takeUntil` pattern; works only in injection context (constructor or with explicit `DestroyRef`).
- **Routing**: lazy-load feature routes via `loadComponent`/`loadChildren`; use route resolvers sparingly (often a service signal/observable in the component is simpler); preloading strategies for next-likely routes.
- **Performance**: `OnPush` everywhere by default; `trackBy` (or `track` in `@for`) for lists; defer non-critical content with `@defer` (Angular 17+) for code-splitting at the template level.
- **Telemetry**: integrate Sentry / Datadog RUM via `ErrorHandler` and HTTP interceptor; emit business events with safe metadata; respect consent.
- **Testing tools**: Jest (recommended over Karma) with `@testing-library/angular`, Cypress/Playwright for E2E, MSW or Angular's `HttpTestingController` for HTTP mocking.

## Testing Expectations

- Unit test validators, pipes, services, signals, and reducers/stores.
- Component tests with `@testing-library/angular` for forms, validation messages, accessibility, async states; query by accessible role.
- HTTP tests verify request shape, headers, error handling, and retry behavior using `HttpTestingController` or MSW.
- E2E tests cover critical journeys (login → key workflow → confirmation), not every form permutation.
- Test masked regulated data, authorization failure UX, expired sessions (silent refresh + retry), rate limits, duplicate submits, file upload/download errors, and accessibility (axe-core in CI) for critical journeys.
- Test lifecycle safety: ensure no subscriptions leak after component destroy (test via memory profile or explicit count).

## Security / Performance / Reliability Considerations

Security requires Angular's built-in sanitizer (do not use `bypassSecurityTrust*` without justification + review), CSP headers from server, CSRF token handling for cookie-auth (`HttpClientXsrfModule`), CORS discipline, safe token storage (httpOnly cookies preferred for regulated apps; in-memory for SPAs), data masking at display, and server-side authorization. Never store tokens in `localStorage` for regulated workloads.

Performance requires lazy loading of routes and heavy components (`@defer`), `OnPush` change detection (consider zoneless in Angular 18+ preview), signal-based fine-grained updates, list virtualization (`@angular/cdk/scrolling`), `trackBy`/`track` for `*ngFor`/`@for`, search/list bounding, image optimization (`NgOptimizedImage`), and bundle budgets (`angular.json` `budgets` config) enforced in CI.

Reliability requires global `ErrorHandler` for uncaught errors, retry discipline (only safe verbs, with backoff), cancellation via `switchMap` for typeahead/navigation, user-visible recovery for partial failures, and offline detection where relevant.

## Review Checklist

- Feature boundaries are clear; standalone components used for new code.
- Subscriptions are lifecycle-safe (`async` pipe or `takeUntilDestroyed`).
- RxJS operator choice matches concurrency semantics (see Gotchas).
- Forms are typed (`FormGroup<T>`) and validated.
- Functional interceptors handle auth, correlation, error mapping, rate limits.
- Components use `OnPush` and signals or async pipe (no manual `markForCheck` scattered around).
- Tests cover behavior, async states, and accessibility — not implementation details.
- No `bypassSecurityTrust*` without security review.
- Regulated data display, downloads, telemetry, and client storage are intentionally designed and reviewed.
- Bundle budgets are configured and enforced.
- Lazy loading + `CanMatch` guards prevent loading code for forbidden routes.

## Anti-Patterns to Avoid

- Nested `.subscribe()` calls inside other subscriptions.
- Business logic in templates or in inline arrow functions in `*ngFor` (causes change-detection thrash).
- Overloaded components mixing data fetching, state, and presentation.
- Leaky services with mutable public state arrays/objects (mutate them and OnPush components miss updates).
- Bypassing Angular sanitization casually (`bypassSecurityTrustHtml` on user content).
- Adding global state (NgRx) for local form state.
- Hiding backend authorization, rate-limit, or idempotency problems behind optimistic UI without a reconciliation path.
- `mergeMap` for write operations with no concurrency cap (can fire unbounded parallel requests on rapid user input).
- `switchMap` for write operations (cancels in-flight save when user clicks again — partial state risk).
- Manual subscriptions in components without unsubscribe management (memory leaks).
- Storing JWTs in `localStorage` for regulated workflows.
- Mixing NgRx, Akita, Component Store, and bare RxJS streams in the same feature without a written rule.

## Gotchas / Common Failure Modes

- **RxJS operator selection** is a frequent source of bugs:
  - `switchMap` cancels the prior inner observable — wrong for writes/saves (silent data loss).
  - `mergeMap` runs all in parallel with no order guarantee — can flood backend on rapid user input; cap with `mergeMap(fn, concurrent)`.
  - `concatMap` runs serially in order — correct for ordered writes but accumulates a queue under load.
  - `exhaustMap` ignores new emissions while inner is active — correct for "ignore double-clicks on submit button".
- **OnPush requires immutable input discipline**: mutating an input array/object instead of replacing it causes the child to miss updates.
- **Signals and RxJS bridging**: `toSignal()` requires an initial value or `requireSync: true`; without it, the signal returns `undefined` until first emission — breaks template typing.
- **Route guards do not secure APIs**: `CanActivate` returning `false` only blocks navigation; the API still must enforce authorization.
- **Subscriptions in services** can leak for the app lifetime if the service is `providedIn: 'root'` and subscribes to an external long-lived stream.
- **Hydration mismatches** in SSR: any `Math.random()`, `Date.now()`, or DOM access during initial render breaks hydration silently in Angular 17+ (warnings in dev, broken UI in prod).
- **Change detection cycles**: signals updating during `effect()` can cause `ExpressionChangedAfterItHasBeenCheckedError` — restructure to avoid sync writes during render.
- **`inject()` outside injection context** throws — must be called in constructors, factories, or within `runInInjectionContext()`.
- **Browser caches, logs, analytics events, and downloaded files** can leak sensitive claim, policy, account, or payment information if not designed explicitly.
- **`@defer` blocks** require the deferred component to be standalone; can break SSR if conditions reference browser-only APIs.
- **NgRx store updates** triggering view changes outside the component tree can bypass `OnPush` if not selecting properly with `select()`.
- **Bundle bloat from Angular Material**: importing entire modules instead of standalone-component imports inflates bundle 100KB+ unnecessarily.
- **Zoneless mode** (Angular 18+ preview): breaks libraries that rely on `Zone.js` patching (e.g., some RxJS schedulers, third-party widgets) — verify compatibility before enabling.

## Code Examples

### Functional Interceptor (Auth + Correlation + Error Mapping)

```typescript
// interceptors/auth-correlation.interceptor.ts
export const authCorrelationInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const correlationId = crypto.randomUUID();

  const authReq = req.clone({
    setHeaders: {
      'Authorization': `Bearer ${auth.accessToken()}`,
      'X-Correlation-Id': correlationId,
      'X-Tenant-Id': auth.tenantId(),
    },
  });

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        return auth.refreshToken$().pipe(
          switchMap(() => next(authReq.clone({
            setHeaders: { 'Authorization': `Bearer ${auth.accessToken()}` }
          }))),
        );
      }
      if (error.status === 429) {
        const retryAfter = parseInt(error.headers.get('Retry-After') ?? '5', 10);
        return timer(retryAfter * 1000).pipe(switchMap(() => next(authReq)));
      }
      return throwError(() => mapToAppError(error, correlationId));
    }),
  );
};

// Register in app.config.ts
provideHttpClient(withInterceptors([authCorrelationInterceptor]))
```

### ExhaustMap for Idempotent Submit

```typescript
// components/payment-form.component.ts
@Component({
  template: `
    <form [formGroup]="form" (ngSubmit)="submit$.next()">
      <!-- form fields -->
      <button type="submit" [disabled]="submitting()">
        @if (submitting()) { Processing... } @else { Submit Payment }
      </button>
    </form>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PaymentFormComponent {
  private http = inject(HttpClient);
  private idempotencyKey = crypto.randomUUID(); // stable per component instance

  form = new FormGroup({ amount: new FormControl(0, [Validators.required, Validators.min(1)]) });
  submit$ = new Subject<void>();
  submitting = signal(false);

  constructor() {
    this.submit$.pipe(
      filter(() => this.form.valid),
      tap(() => this.submitting.set(true)),
      exhaustMap(() => this.http.post('/v1/payments', this.form.value, {
        headers: { 'Idempotency-Key': this.idempotencyKey }
      })),
      takeUntilDestroyed(),
    ).subscribe({
      next: () => { this.submitting.set(false); /* navigate to success */ },
      error: (err) => { this.submitting.set(false); /* show error */ },
    });
  }
}
```

### Signal-Based Feature Service

```typescript
// services/claims.service.ts
@Injectable({ providedIn: 'root' })
export class ClaimsService {
  private http = inject(HttpClient);

  // State as signals
  private _claims = signal<Claim[]>([]);
  private _loading = signal(false);
  private _error = signal<AppError | null>(null);

  // Public read-only signals
  readonly claims = this._claims.asReadonly();
  readonly loading = this._loading.asReadonly();
  readonly error = this._error.asReadonly();

  // Derived
  readonly openClaims = computed(() => this._claims().filter(c => c.status === 'OPEN'));
  readonly claimCount = computed(() => this._claims().length);

  loadClaims(filters: ClaimFilters): void {
    this._loading.set(true);
    this._error.set(null);

    this.http.get<Claim[]>('/v1/claims', { params: filters as any }).pipe(
      finalize(() => this._loading.set(false)),
    ).subscribe({
      next: (claims) => this._claims.set(claims),
      error: (err) => this._error.set(mapToAppError(err)),
    });
  }
}

// Usage in component — no subscription management needed
@Component({
  template: `
    @if (claims.loading()) { <spinner /> }
    @else if (claims.error(); as err) { <error-message [error]="err" /> }
    @else {
      @for (claim of claims.openClaims(); track claim.id) {
        <claim-card [claim]="claim" />
      }
    }
  `
})
export class ClaimListComponent {
  claims = inject(ClaimsService);
  constructor() { this.claims.loadClaims({ status: 'OPEN' }); }
}
```

### Typed Reactive Form with Cross-Field Validation

```typescript
interface EndorsementForm {
  endorsementType: FormControl<string>;
  effectiveDate: FormControl<string>;
  changes: FormGroup<{ vehiclePlate: FormControl<string>; newValue: FormControl<string> }>;
  reason: FormControl<string>;
}

@Component({ /* ... */ })
export class EndorsementFormComponent {
  form = new FormGroup<EndorsementForm>({
    endorsementType: new FormControl('', { nonNullable: true, validators: [Validators.required] }),
    effectiveDate: new FormControl('', { nonNullable: true, validators: [Validators.required, this.futureDateValidator] }),
    changes: new FormGroup({
      vehiclePlate: new FormControl('', { nonNullable: true }),
      newValue: new FormControl('', { nonNullable: true, validators: [Validators.required] }),
    }),
    reason: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.minLength(10)] }),
  }, { validators: [this.effectiveDateAfterTodayValidator] });

  private futureDateValidator(control: AbstractControl): ValidationErrors | null {
    const date = new Date(control.value);
    return date > new Date() ? null : { futureDate: true };
  }

  private effectiveDateAfterTodayValidator(group: AbstractControl): ValidationErrors | null {
    const type = group.get('endorsementType')?.value;
    const date = group.get('effectiveDate')?.value;
    if (type === 'CANCELLATION' && new Date(date) < new Date()) {
      return { cancellationMustBeFuture: true };
    }
    return null;
  }
}
```

