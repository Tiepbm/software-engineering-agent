---
name: reactjs-development
description: 'Guides React application design across components, hooks, state, forms, API integration, loading and error states, performance, accessibility, and tests.'
---

# ReactJS Development

## Description

Guides React application design across components, hooks, state, forms, API integration, loading and error states, performance, accessibility, and tests across React 18/19, server components, Suspense, and modern data libraries.

## Purpose

- Build React interfaces that are understandable, accessible, performant, and maintainable under product change.
- Keep UI state, server state, forms, and effects separated by responsibility.
- Use React 18/19 features (Suspense, transitions, Server Components, Actions, `use` hook) deliberately rather than retrofitting old `useEffect` patterns onto them.
- Prevent bloated components, scattered API calls, and security gaps in regulated frontends.

## When to Use

- Implementing or reviewing React components, hooks, pages, forms, API integration, state management, accessibility, performance, or SSR/SSG/RSC architecture.
- The UI has too many `useEffect` calls, inconsistent loading/error states, rerender storms, hydration mismatches, or duplicated form logic.
- A feature must support complex flows, async data, optimistic updates, file uploads, or reusable component patterns.
- The frontend handles regulated data, token/session behavior, gateway errors, rate limits, file uploads/downloads, search experiences, or telemetry for critical journeys.
- Choosing between Vite SPA, Next.js (App Router with RSC), Remix, TanStack Start, or another React meta-framework.

## Responsibilities

- Design component boundaries, state ownership, data fetching pattern, form validation, error/loading/empty states, and accessibility behavior.
- Choose state location: local (`useState`/`useReducer`), URL, server state (TanStack Query / SWR / RTK Query), client state (Zustand / Jotai / Redux Toolkit), or React context — by scope, mutation frequency, and shareability.
- Decide rendering model: client-only SPA, SSR with hydration, RSC + client islands, or static — based on SEO, TTFB, data freshness, and team capability.
- Review hooks dependencies, memoization, rendering cost, bundle size, and test coverage.
- Keep components cohesive and small enough to reason about.
- Involve `api-design`, `authn-authz-and-secrets`, `security-review`, `rate-limiting-and-traffic-control`, `file-and-object-storage`, `search-and-indexing`, `logging-metrics-and-tracing`, `performance-engineering` when UI behavior depends on those platform contracts.

## Decision Principles

- Use `useEffect` for synchronization with **external systems** only (browser APIs, subscriptions, manual DOM), not for deriving render state from props/state — derive during render or with `useMemo`.
- Keep server data in a server-state library (TanStack Query / SWR / RSC fetch); avoid copying it into local state unless editing drafts.
- Prefer composition and component slots over prop drilling or large global stores.
- Make accessibility part of component contracts (keyboard, focus, ARIA, screen reader); audit with `eslint-plugin-jsx-a11y` and `axe`.
- Treat client-side checks as UX only; regulated decisions (payment, claim, policy, eligibility, account access) **must** be enforced by backend APIs.
- For state libraries: `useState` first → URL/search params next → server state for remote data → client store only when truly cross-component shared mutable state exists.
- For meta-frameworks: choose Next.js App Router when SEO + RSC + edge rendering matter; choose Vite SPA when the app is behind auth and SEO is irrelevant; choose Remix/TanStack Start when nested routing + data loaders fit the mental model.

## Expected Output Style

- Start with the decision or finding, then the reasoning needed to trust it.
- Show concrete React snippets for component shape, hook composition, query setup, form handler, or Suspense boundary when they reduce ambiguity.
- Separate immediate fixes (component refactor) from longer-term improvements (state architecture, RSC migration, framework choice).
- State assumptions about React version (18 vs 19), router (React Router / Next.js / Remix), bundler (Vite / Webpack / Turbopack), TypeScript usage, and target browsers/devices.
- Avoid generic advice unless followed by an enforceable rule, code shape, or verification step.

## Architecture / Design Guidance

Frontend architecture should group by **feature** (`features/billing/`, `features/claims/`) where product behavior changes together, not by type (`components/`, `hooks/`, `utils/`). Shared components must have stable, documented APIs and accessibility guarantees.

API integration should centralize: one HTTP client (fetch wrapper or `axios` instance) with auth header injection, refresh token handling, error mapping, retry policy for safe verbs only, correlation IDs (`x-request-id`), and `AbortSignal` propagation. Wrap calls in TanStack Query / SWR for caching, dedup, background refresh, and optimistic updates — do not re-implement these in `useEffect`.

For React 19 + Next.js App Router with RSC: keep server components for data fetching and static rendering; move interactivity to leaf client components (`"use client"`); use Server Actions for mutations with progressive enhancement; do not pass non-serializable props from server to client.

For Suspense and streaming: wrap data-fetching boundaries with `<Suspense fallback={...}>` + error boundaries; React 19 `use()` hook lets components await promises directly (only inside transitions or Suspense). Stream large pages with `loading.tsx` (Next App Router) or `defer` (Remix) to ship above-the-fold first.

For banking/insurance screens, design safe rendering, masking (PAN, account, claim numbers), copy/download behavior with audit, idempotent submission UX (disable + idempotency key), and recovery UX for interrupted payments, claims, policy changes, document uploads, and quote flows.

## Implementation Guidance

- **Forms**: `react-hook-form` + `zod`/`yup` schema, or framework-native (Next.js Server Actions, Remix `useFetcher`). Model loading, empty, error, stale, rate-limited, offline/retry, validation-error, and success states explicitly — not as an afterthought.
- **Server state**: TanStack Query v5 with `queryKey` discipline (tenant + entity + filters), `staleTime` matching freshness tolerance, `gcTime` for memory, `select` for projection, `placeholderData` for keepPreviousData pattern; mutations with `onMutate` for optimistic updates + `onError` rollback + `onSettled` invalidation.
- **Client state**: Zustand for simple shared state, Jotai for atom-based fine-grained state, Redux Toolkit when middleware/devtools/time-travel matter. Avoid Redux for simple cases.
- **Memoization**: `React.memo`, `useMemo`, `useCallback` only when profiler shows wasted renders or stable identity is required for downstream `useEffect`/`useMemo`. React 19 compiler (when enabled) memoizes automatically — avoid manual memoization in compiler-on projects.
- **Performance**: `React.lazy` + Suspense for route-level code splitting; `react-window` / `react-virtuoso` for large lists; `next/image` or equivalent for image optimization; bundle analyzer in CI; monitor Core Web Vitals (LCP, INP, CLS).
- **Accessibility**: semantic HTML first, ARIA only when semantic HTML can't express it; manage focus on route change and modal open; trap focus in modals; respect `prefers-reduced-motion`.
- **Auth / tokens**: never store long-lived tokens in `localStorage` for regulated apps — use httpOnly cookies for session, in-memory for short-lived access tokens with silent refresh; protect against XSS as the primary threat.
- **Error boundaries**: one per route + one per significant async region; log to telemetry with correlation ID; show actionable recovery UX, not raw stack traces.
- **Telemetry**: web vitals + error tracking (Sentry / Datadog RUM); custom business events (payment_started, claim_submitted) with safe metadata only; respect Do-Not-Track and consent.
- **Testing tools**: Vitest (Vite) or Jest, `@testing-library/react`, `@testing-library/user-event`, MSW for network mocking at the boundary, Playwright/Cypress for E2E.

## Testing Expectations

- Test pure utilities and hooks with focused unit tests (`renderHook` from Testing Library).
- Use component tests for rendering, user events, validation, accessibility states, and error/empty/loading branches — query by accessible role, not test IDs.
- Mock network at the boundary with MSW using realistic responses (success, 4xx, 5xx, slow, abort).
- Use E2E tests for critical journeys only (login → key workflow → confirmation); not every edge case.
- Test masked regulated data display, authorization failure UX (401/403 → redirect or message), expired sessions (silent refresh + retry), rate limits (429 + Retry-After), duplicate submissions (idempotency key reuse), file upload/download errors, and accessibility for critical journeys (axe in CI).
- Visual regression for design-system components only; full-app visual diffs are noisy.

## Security / Performance / Reliability Considerations

Security requires safe rendering (no `dangerouslySetInnerHTML` on untrusted content; sanitize with DOMPurify if unavoidable), CSP headers from the server, protected tokens (httpOnly cookies preferred), data masking, server-side authorization (client checks are UX only), and secure cookie flags (`Secure`, `HttpOnly`, `SameSite=Lax/Strict`). Audit third-party scripts and supply chain (npm audit, Renovate/Dependabot).

Performance requires bundle budgets enforced in CI (`size-limit`, `bundlewatch`), render profiling (React DevTools Profiler), image optimization, list virtualization, search/list result bounding, code splitting, prefetching critical routes, and avoiding context churn (split contexts by update frequency).

Reliability requires error boundaries, resilient API state handling (retry safe verbs only with backoff, circuit-break on dependency failure), duplicate-submit prevention (button disable + idempotency key), offline detection (`navigator.onLine` + service worker if PWA), and user-visible recovery for partial failures.

## Review Checklist

- Components have clear single responsibilities; no 500-line components.
- `useEffect` count per component is low; each effect synchronizes with an external system, not derives state.
- All async states (loading, empty, error, stale, rate-limited, success) are represented in UI.
- Forms validate accessibly with clear error messages tied to inputs.
- Server data lives in server-state library, not duplicated into local state.
- API errors are user-actionable, not raw status codes.
- Large lists are virtualized; large pages are code-split.
- Tests use accessible queries (`getByRole`) and simulate user behavior, not implementation details.
- No long-lived tokens in `localStorage` for regulated apps.
- Regulated data display, downloads, telemetry events, and client storage are intentionally designed and reviewed.
- Bundle size budgets are set and enforced.
- Accessibility audited automatically (axe) and manually (keyboard, screen reader) for critical flows.

## Anti-Patterns to Avoid

- Overusing `useEffect` for derived data (compute during render or with `useMemo`).
- Putting all app state in one global store ("Redux for everything").
- Bloated page components mixing data fetching, business logic, and presentation.
- Scattered `fetch` calls without a centralized client (no auth refresh, no correlation, no error mapping).
- Ignoring keyboard and screen reader behavior; ARIA misuse where semantic HTML would suffice.
- Memoizing everything (`useMemo` / `useCallback` everywhere) without profiling.
- Hiding backend authorization, rate-limit, or idempotency problems behind optimistic UI without a reconciliation path.
- `dangerouslySetInnerHTML` with user-supplied or third-party content without sanitization.
- Storing JWTs / refresh tokens in `localStorage` for regulated workflows.
- Mixing server components and client components incorrectly (passing functions, dates, or class instances from server to client without serialization).
- Building custom data-fetching hooks instead of using TanStack Query / SWR / RSC fetch.

## Gotchas / Common Failure Modes

- **Stale closures**: `useEffect`/`useCallback` capturing old state when dependency array is wrong; ESLint `react-hooks/exhaustive-deps` catches most cases.
- **Strict Mode** (React 18+) double-invokes effects in development to expose unsafe effects — design effects to be idempotent.
- **Hydration mismatches**: SSR output differs from client render (e.g., `Date.now()`, `Math.random()`, `window` access without guard); only visible in production unless tested with SSR.
- **Rerender cascades from context**: any context value change re-renders all consumers; split contexts by update frequency.
- **TanStack Query gotchas**: `queryKey` must be serializable + stable; mutation `onSuccess` invalidation can trigger refetch storms — use targeted `setQueryData` updates.
- **React 19 `use()` hook**: must be inside a Suspense boundary; can't be in regular event handlers.
- **Server Components**: cannot use hooks or browser APIs; passing event handlers to client components requires `"use client"` boundary.
- **Browser caches, logs, analytics events, screenshots, and downloads** can leak sensitive claim, policy, account, or payment information if not designed explicitly (no PII in URLs, no PII in `console.log`, no PII in error tracker payloads).
- **Bundle bloat**: importing entire libraries (`import _ from 'lodash'`) instead of named imports; check with bundle analyzer.
- **Accessibility regressions**: focus lost on route change unless explicitly managed; modal focus trap broken when content changes.
- **Date/timezone bugs**: `new Date(string)` parses inconsistently across browsers — always use ISO 8601 + `date-fns-tz` or `Temporal` (when available).
- **Service worker** caching old bundles after deploy unless cache-busting + skipWaiting strategy is correct.

## Code Examples

### TanStack Query with Auth Refresh

```tsx
// api/client.ts — centralized HTTP client
const apiClient = {
  async fetch<T>(url: string, options?: RequestInit): Promise<T> {
    const token = await getAccessToken(); // from auth store
    const res = await fetch(`${BASE_URL}${url}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'X-Correlation-Id': crypto.randomUUID(),
        ...options?.headers,
      },
      signal: options?.signal ?? AbortSignal.timeout(30_000),
    });
    if (res.status === 401) {
      await refreshToken(); // silent refresh
      return apiClient.fetch(url, options); // retry once
    }
    if (!res.ok) throw new ApiError(res.status, await res.json());
    return res.json();
  }
};

// hooks/useClaims.ts — query with proper key discipline
export function useClaims(filters: ClaimFilters) {
  return useQuery({
    queryKey: ['claims', filters.tenantId, filters.status, filters.page],
    queryFn: ({ signal }) => apiClient.fetch<ClaimList>(
      `/v1/claims?${new URLSearchParams(filters)}`, { signal }
    ),
    staleTime: 30_000, // 30s freshness tolerance
    placeholderData: keepPreviousData, // smooth pagination
  });
}
```

### Idempotent Form Submission

```tsx
function PaymentForm() {
  const [idempotencyKey] = useState(() => crypto.randomUUID()); // stable per mount
  const mutation = useMutation({
    mutationFn: (data: PaymentInput) => apiClient.fetch('/v1/payments', {
      method: 'POST',
      headers: { 'Idempotency-Key': idempotencyKey },
      body: JSON.stringify(data),
    }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['payments'] }),
  });

  return (
    <form onSubmit={handleSubmit(data => mutation.mutate(data))}>
      {/* form fields */}
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Processing...' : 'Submit Payment'}
      </button>
      {mutation.isError && <ErrorMessage error={mutation.error} />}
    </form>
  );
}
```

### Error Boundary with Telemetry

```tsx
class AppErrorBoundary extends Component<PropsWithChildren, { error?: Error }> {
  state: { error?: Error } = {};

  static getDerivedStateFromError(error: Error) { return { error }; }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // Report to telemetry with correlation context
    reportError({
      error,
      componentStack: info.componentStack,
      correlationId: getCurrentCorrelationId(),
      userId: getCurrentUserId(), // safe reference, not PII
      route: window.location.pathname,
    });
  }

  render() {
    if (this.state.error) {
      return (
        <div role="alert">
          <h2>Something went wrong</h2>
          <p>Our team has been notified. Please try again.</p>
          <button onClick={() => this.setState({ error: undefined })}>Retry</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

### Masked Data Display (Regulated)

```tsx
function MaskedField({ value, label, onReveal }: {
  value: string; label: string; onReveal: () => void;
}) {
  const [revealed, setRevealed] = useState(false);
  const masked = value.replace(/.(?=.{4})/g, '*'); // show last 4

  const handleReveal = () => {
    setRevealed(true);
    onReveal(); // triggers audit event via API
    setTimeout(() => setRevealed(false), 30_000); // auto-hide after 30s
  };

  return (
    <div>
      <label>{label}</label>
      <span aria-live="polite">{revealed ? value : masked}</span>
      {!revealed && (
        <button onClick={handleReveal} aria-label={`Reveal ${label}`}>
          Show
        </button>
      )}
    </div>
  );
}
```

