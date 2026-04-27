---
name: react-native-development
description: 'Guides React Native delivery across screen architecture, navigation, Android and iOS differences, native modules, permissions, network state, offline behavior, performance, and production debugging.'
---

# React Native Development

## Description

Guides React Native delivery across screen architecture, navigation, iOS/Android differences, the New Architecture (Fabric/TurboModules/Hermes), Expo vs bare workflow, native modules, permissions, network state, offline behavior, performance, OTA updates, and production debugging.

## Purpose

- Build React Native apps that behave correctly across iOS and Android, unreliable networks, permissions, and native build constraints.
- Separate JavaScript-layer problems from native configuration, linking, build, and platform issues.
- Prepare mobile features for production conditions — devices, release builds, store policies — not simulator-only success.
- Choose deliberately between Expo (managed/dev-client) and bare RN, and between Old vs New Architecture.

## When to Use

- Implementing or reviewing React Native screens, navigation, native modules, permissions, offline flows, API integration, rendering performance, or release readiness.
- A bug appears only on one platform, physical devices, release builds, or poor networks.
- A feature touches camera, location, push notifications, secure storage, deep links, biometrics, background tasks, file uploads, or Bluetooth.
- The mobile flow handles regulated data, secure storage, offline writes, gateway/rate-limit errors, document capture/upload, search, push/deep links, OTA updates, or production telemetry.
- Planning migration to the New Architecture (Fabric + TurboModules + Hermes) or upgrading across major RN versions.

## Responsibilities

- Design screen boundaries, navigation params (typed, serializable, small), state ownership, data fetching, offline handling, permissions, and native capability usage.
- Account for iOS and Android lifecycle (`AppState`, background modes, foreground services, app suspension), platform APIs, build config (Xcode signing, Gradle), and store requirements (privacy manifests, permission strings).
- Review FlatList/SectionList performance, image handling, startup cost, JS thread vs UI thread cost, and memory.
- Plan debugging across JS logs, native logs (Xcode console, `adb logcat`), crash reports (Crashlytics, Sentry, Bugsnag), and release builds (no Metro, no React DevTools).
- Decide between Expo managed (no native code), Expo dev client (custom native modules + Expo conveniences), or bare RN (full native control, more upgrade work).
- Involve `api-design`, `authn-authz-and-secrets`, `security-review`, `file-and-object-storage`, `rate-limiting-and-traffic-control`, `logging-metrics-and-tracing`, `performance-engineering`, `resilience-and-fault-tolerance` when mobile code depends on platform contracts.

## Decision Principles

- Treat platform differences as **design constraints**, not late bugs.
- Keep navigation params small and serializable; pass IDs, fetch full data in the destination screen — large objects break deep linking, state restoration, and serialization warnings.
- Request permissions just-in-time with clear fallback UX (denied, limited, restricted on iOS); never request on app launch.
- Use offline queues only with **idempotent operations and conflict strategy**; otherwise queued writes corrupt server state on retry.
- Treat local checks, biometrics, and device state as UX and risk controls — **not replacements** for backend authorization.
- Choose **Expo with dev client** as the default for new projects (best DX, EAS Build, EAS Update, native module support); fall back to bare RN only when build-time native customization Expo can't express is needed.
- Choose the **New Architecture** (Fabric + TurboModules + Hermes + JSI) for new apps on RN 0.74+; migrate existing apps when third-party libraries support it.
- Choose **TanStack Query** or **RTK Query** for server state; avoid hand-rolled `useEffect` data fetching.

## Expected Output Style

- Start with the decision or finding, then the reasoning needed to trust it.
- Show concrete TS/JS snippets for screen, navigation typing, native module bridge, permission flow, or list optimization when they reduce ambiguity.
- Separate immediate fixes from longer-term improvements (New Architecture migration, Expo migration, OTA strategy).
- State assumptions about RN version, Expo SDK version, target iOS/Android versions, Hermes on/off, and Old vs New Architecture.
- Avoid generic advice unless followed by an enforceable rule, code shape, or verification step.

## Architecture / Design Guidance

Mobile architecture should separate screens, components, hooks, API clients (centralized with auth/refresh/correlation/abort), storage (secure for tokens/PII, regular `AsyncStorage` for non-sensitive cache), native adapters (one wrapper per native module), telemetry, and navigation. Native modules require version compatibility, autolinking awareness, permission manifests (`Info.plist`, `AndroidManifest.xml`), and release-build validation.

Offline flows require local state (SQLite via `op-sqlite` / `expo-sqlite`, or MMKV for KV), sync status (`pending|syncing|synced|error|conflict`), retries with exponential backoff, idempotency keys per operation, and conflict UX. Background sync on iOS is severely constrained — use `BGTaskScheduler` (iOS) / `WorkManager` (Android via native module or `expo-background-fetch`); never rely on it for time-critical operations.

For banking/insurance apps, design secure document capture/upload (camera + signed URL upload + scan status polling), masked data display with reveal-on-tap + audit event, session timeout with biometric step-up UX (`expo-local-authentication` / `react-native-keychain`), push/deep-link safety (validate payloads, never trust deep-link params for authorization, handle cold-start vs warm-start), and recovery UX for interrupted payments, claims, quotes, and policy changes.

For OTA updates (Expo Updates / CodePush): version JS bundle compatibility with native binary; use staged rollouts; have rollback ready; treat OTA as JS-only — never push native module changes via OTA (will crash at runtime).

## Implementation Guidance

- **Navigation**: React Navigation with typed `RootStackParamList`; native stack (`@react-navigation/native-stack`) for performance; deep link config schema with explicit param parsing. Expo Router for file-based routing in Expo projects.
- **State**: Zustand for shared client state, TanStack Query / RTK Query for server state.
- **API client**: centralized fetch wrapper with `AbortController`, auth header injection, refresh token handling, correlation IDs (`x-request-id`), retry only on safe verbs with backoff, rate-limit (429 + Retry-After) handling.
- **Secure storage**: `expo-secure-store` (Keychain/Keystore) or `react-native-keychain` for tokens, PII, biometric-protected secrets; never `AsyncStorage` for tokens in regulated apps.
- **Forms**: `react-hook-form` + `zod`; handle keyboard avoidance (`KeyboardAvoidingView`, platform-specific `behavior`).
- **Lists**: `FlatList` with stable `keyExtractor`, `getItemLayout` when item height is fixed, `removeClippedSubviews` for very long lists, `windowSize`/`maxToRenderPerBatch` tuning, `memo`-wrapped row components; consider `FlashList` (Shopify) for large heterogeneous lists.
- **Images**: `expo-image` or `react-native-fast-image` for caching, placeholder, transitions; size images server-side, never load full-resolution into list rows.
- **Permissions**: `react-native-permissions` (bare) or `expo-*` libraries; request just-in-time; handle "ask again" denial flow (iOS: send to Settings, Android: rationale dialog).
- **Network state**: `@react-native-community/netinfo` for online/offline detection; show offline banner; queue writes; auto-retry on reconnect.
- **Push notifications**: `expo-notifications` (Expo) or `@react-native-firebase/messaging` (bare); handle foreground/background/quit states differently; deep-link from notification tap with auth context check.
- **Biometrics**: `expo-local-authentication` / `react-native-biometrics`; use as UX gate over secure storage, never as sole auth proof to backend.
- **Telemetry**: Sentry / Bugsnag / Datadog RUM with native crash reporting (must include native dSYMs/Proguard mappings); custom business events; redact PII before send.
- **Testing**: Jest + `@testing-library/react-native` for unit/component; Detox or Maestro for E2E (Maestro is YAML-based and simpler; Detox is JS-based and more powerful).
- **Build/release**: EAS Build for Expo; Fastlane for bare RN; staged rollouts via App Store/Play Console; OTA via EAS Update / CodePush with rollback plan.

## Testing Expectations

- Test hooks and business logic with unit tests (Jest).
- Component tests for critical screen states (loading, error, empty, success, permission denied, offline).
- Run E2E tests (Detox/Maestro) on at least one iOS and one Android target for critical flows; in CI use simulators/emulators, in pre-release use physical devices.
- Validate permissions, deep links (cold start + warm start), offline/reconnect flows, release builds (Hermes-enabled, minified, signed), and crash reporting (force a crash and verify the report appears with symbols).
- Test secure storage behavior (token retrieval after app restart, biometric fallback, key invalidation on biometric change), token expiry + silent refresh, duplicate offline writes, document upload failures (network drop mid-upload), push/deep-link authorization context, and telemetry redaction.
- Test on **low-end devices** (e.g., 2GB RAM Android) — performance issues are hidden on flagship devices.
- Test on **iOS limited Photo Library access** and **Android scoped storage** — modern OS versions changed semantics.

## Security / Performance / Reliability Considerations

Security requires secure storage (Keychain/Keystore), certificate pinning only when operationally justified, no secrets in JS bundle (it's reverse-engineerable), data masking, safe deep links (validate origin, never trust params for auth), platform permission discipline, Android `android:exported` audit for receivers/services/activities, iOS App Transport Security (ATS) compliance, and privacy manifest (iOS 17+) declaring data collection.

Performance requires startup profiling (Flipper / React Native Performance Monitor), JS thread vs UI thread separation, bridge minimization (New Architecture removes the bridge but TurboModule call cost is non-zero), rendering profiling (Hermes profiler, Systrace on Android, Instruments on iOS), list optimization, image optimization, file-transfer streaming (no full file in memory), and low-end-device testing.

Reliability requires network-state handling, crash reporting with native symbols/mappings, safe retry/idempotency, offline reconciliation with conflict UX, release-build observability, and OTA rollback capability.

## Review Checklist

- Screens have clear ownership; navigation params are small and serializable.
- Typed navigation (`RootStackParamList`) covers all routes.
- Permissions include denial, limited, and restricted state UX.
- Offline behavior is explicit (queued writes, conflict UX, auto-retry on reconnect).
- Platform differences are tested (iOS + Android, multiple OS versions).
- Lists and images are optimized.
- Release builds are validated (Hermes, minification, signed) — not just debug.
- Crash reporting works in release with native symbols.
- Tokens stored in Keychain/Keystore, never `AsyncStorage` for regulated apps.
- Deep links validated; auth context checked before acting on payload.
- OTA updates have rollback plan and don't ship native changes.
- Regulated data display, local storage, crash logs, push/deep links, and document capture are intentionally reviewed.
- Privacy manifest (iOS) and Android permissions audit completed for store submission.

## Anti-Patterns to Avoid

- Assuming simulator behavior matches physical devices (perf, permissions, push, biometrics all differ).
- Storing tokens / PII in `AsyncStorage` (it's plaintext on disk).
- Passing large objects through navigation params (breaks state restoration, deep links).
- Ignoring Android back button behavior (`BackHandler`).
- Testing only debug builds (Hermes, minification, OTA can break release-only).
- Adding native modules without an upgrade plan (they pin you to RN versions).
- Treating offline queues, biometrics, or push/deep links as trusted authorization mechanisms without backend validation.
- Pushing native module changes via OTA (will crash; OTA is JS-only).
- `console.log` everywhere in production builds (kept in JS bundle, slow on Hermes).
- Catching errors silently in async code; crash reporters won't see them.
- Ignoring iOS App Tracking Transparency and Privacy Manifest requirements.

## Gotchas / Common Failure Modes

- **Native dependency versions** can break builds without JS changes; lock peer deps and upgrade in coordinated PRs.
- **Release minification** (Hermes bytecode + Metro minify) can expose hidden assumptions (relying on function names, prop key strings).
- **Permissions differ by OS version**: iOS 14+ added "Limited Photo Library", Android 13+ added per-media permissions, Android 14 added partial photo access; older code requesting `READ_EXTERNAL_STORAGE` is broken.
- **Background execution is platform-constrained**: iOS allows ~30s of background time + special background modes; Android has Doze + battery optimizations + foreground service requirements.
- **Network retries can duplicate writes** unless idempotent (especially after backgrounding mid-request).
- **Crash reporters, screenshots (iOS app switcher snapshot), OS backups (iCloud/Google), notification previews, and local files** can leak sensitive claim, policy, account, or payment data if not configured deliberately.
- **iOS app switcher snapshot** captures the screen including sensitive data — blank it on backgrounding.
- **Hermes** changes JS engine semantics: `eval`, `Function` constructor, and some RegExp features differ from JSC; test in Hermes-enabled release.
- **OTA updates** can ship JS that's incompatible with the installed native binary — version your bundle against native, gate by build number.
- **Deep link cold start vs warm start**: `Linking.getInitialURL()` for cold, `Linking.addEventListener('url')` for warm — must handle both.
- **Push notification handlers** behave differently in foreground (custom UI), background (system notification + tap → deep link), and quit (cold start with notification payload).
- **Keychain/Keystore** entries persist across app uninstalls on iOS; clear on first launch if that's not desired.
- **Biometric changes** (new fingerprint enrolled) invalidate biometric-protected Keychain entries — handle the re-auth flow.
- **`react-native-reanimated`** runs on UI thread; `console.log` inside worklets can crash; use `runOnJS` to log.
- **FlatList with variable item heights** without `getItemLayout` causes scroll jank and incorrect `scrollTo` behavior.
- **Image memory**: loading full-resolution camera photos (10MB+) into list rows OOMs the app on low-RAM devices.
- **App Store / Play Store rejections**: missing permission usage strings (iOS `NSCameraUsageDescription` etc.), missing privacy manifest, undeclared encryption export — surface in store review weeks after build.

## Code Examples

### Secure Storage + Biometric Gate

```typescript
// services/secureAuth.ts
import * as SecureStore from 'expo-secure-store';
import * as LocalAuthentication from 'expo-local-authentication';

const TOKEN_KEY = 'auth_refresh_token';

export async function storeToken(token: string): Promise<void> {
  await SecureStore.setItemAsync(TOKEN_KEY, token, {
    keychainAccessible: SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
    requireAuthentication: true, // biometric required to read
  });
}

export async function getTokenWithBiometric(): Promise<string | null> {
  const { success } = await LocalAuthentication.authenticateAsync({
    promptMessage: 'Xác thực để tiếp tục',
    fallbackLabel: 'Dùng mã PIN',
    disableDeviceFallback: false,
  });
  if (!success) return null;
  return SecureStore.getItemAsync(TOKEN_KEY);
}

// NEVER use AsyncStorage for tokens in regulated apps
// AsyncStorage is plaintext on disk — readable with device access
```

### Offline Queue with Idempotency

```typescript
// services/offlineQueue.ts
import { MMKV } from 'react-native-mmkv';
import NetInfo from '@react-native-community/netinfo';

interface QueuedOperation {
  id: string; // idempotency key
  endpoint: string;
  method: 'POST' | 'PUT';
  body: object;
  createdAt: number;
  retryCount: number;
  status: 'pending' | 'syncing' | 'failed';
}

const storage = new MMKV({ id: 'offline-queue' });

export function enqueue(op: Omit<QueuedOperation, 'id' | 'createdAt' | 'retryCount' | 'status'>): string {
  const id = crypto.randomUUID();
  const operation: QueuedOperation = {
    ...op, id, createdAt: Date.now(), retryCount: 0, status: 'pending',
  };
  const queue = getQueue();
  queue.push(operation);
  storage.set('queue', JSON.stringify(queue));
  return id;
}

export async function syncQueue(): Promise<void> {
  const isConnected = (await NetInfo.fetch()).isConnected;
  if (!isConnected) return;

  const queue = getQueue().filter(op => op.status === 'pending');
  for (const op of queue) {
    try {
      op.status = 'syncing';
      await apiClient.fetch(op.endpoint, {
        method: op.method,
        headers: { 'Idempotency-Key': op.id }, // safe retry
        body: JSON.stringify(op.body),
      });
      removeFromQueue(op.id);
    } catch (error) {
      op.retryCount++;
      op.status = op.retryCount >= 3 ? 'failed' : 'pending';
      updateInQueue(op);
    }
  }
}

// Auto-sync on reconnect
NetInfo.addEventListener(state => {
  if (state.isConnected) syncQueue();
});
```

### Signed URL Document Upload

```typescript
// hooks/useDocumentUpload.ts
export function useDocumentUpload(claimId: string) {
  return useMutation({
    mutationFn: async (file: { uri: string; type: string; name: string }) => {
      // 1. Get signed URL from backend (authorized, short-lived)
      const { uploadUrl, documentId } = await apiClient.fetch<SignedUrlResponse>(
        `/v1/claims/${claimId}/documents/upload-url`,
        { method: 'POST', body: JSON.stringify({ contentType: file.type, fileName: file.name }) }
      );

      // 2. Upload directly to S3 (bypasses API server for large files)
      const response = await fetch(uploadUrl, {
        method: 'PUT',
        headers: { 'Content-Type': file.type },
        body: await fetch(file.uri).then(r => r.blob()),
      });
      if (!response.ok) throw new Error('Upload failed');

      // 3. Confirm upload to backend (triggers malware scan)
      await apiClient.fetch(`/v1/claims/${claimId}/documents/${documentId}/confirm`, {
        method: 'POST',
      });
      return documentId;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['claims', claimId, 'documents'] }),
  });
}
```

### Deep Link with Auth Validation

```typescript
// navigation/deepLinkHandler.ts
import * as Linking from 'expo-linking';
import { useEffect } from 'react';

export function useDeepLinkHandler(navigation: NavigationProp) {
  useEffect(() => {
    // Handle cold start
    Linking.getInitialURL().then(url => { if (url) handleDeepLink(url); });

    // Handle warm start
    const sub = Linking.addEventListener('url', ({ url }) => handleDeepLink(url));
    return () => sub.remove();
  }, []);

  function handleDeepLink(url: string) {
    const parsed = Linking.parse(url);

    // NEVER trust deep link params for authorization
    // Always verify server-side before showing sensitive data
    switch (parsed.path) {
      case 'claims/:id':
        // Navigate to claim — screen will verify access via API
        navigation.navigate('ClaimDetail', { claimId: parsed.queryParams?.id });
        break;
      case 'payments/confirm':
        // Verify payment status server-side, don't trust link params
        navigation.navigate('PaymentConfirm', { paymentId: parsed.queryParams?.id });
        break;
      default:
        navigation.navigate('Home');
    }
  }
}
```

