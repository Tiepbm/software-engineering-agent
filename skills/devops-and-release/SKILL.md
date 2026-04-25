---
name: devops-and-release
description: 'Designs CI/CD, environment promotion, configuration, feature flags, rollback, migration coordination, secrets handling, and safe delivery practices.'
---

# DevOps and Release

## Description

Designs CI/CD, environment promotion, configuration, feature flags, rollback, migration coordination, secrets handling, deployment topologies (rolling, blue-green, canary, progressive delivery), GitOps, and safe delivery practices for enterprise and regulated systems.

## Purpose

- Deliver changes safely, repeatably, and quickly with clear gates, rollback paths, and environment discipline.
- Reduce release risk from manual steps, configuration drift, migration mistakes, and missing observability.
- Coordinate application, database, infrastructure, messaging, and dependency changes so that no single change can take down the system without an undo path.

## When to Use

- Creating or reviewing CI/CD pipelines, deployment topologies, release plans, environment promotion, feature flags, configuration, rollback, or migration coordination.
- A release has high blast radius, multi-service dependencies, database changes, external integrations, or compliance requirements.
- Teams experience failed deployments, unclear rollback, manual release checklists, configuration drift between environments, or "it worked in staging" failures.
- Releases include object-storage migrations, messaging/topic changes, gateway policy changes, secret rotation, cache/search rebuilds, orchestration changes, or SLO-based rollout gates.
- Adopting GitOps, progressive delivery, trunk-based development, or release-train models.

## Responsibilities

- Define build, test, scan, package, deploy, promote, verify, and rollback stages for the pipeline.
- Separate **configuration from code** and **secrets from configuration**.
- Plan feature flags, canaries, blue-green, rolling deploys, and migration sequencing where appropriate.
- Coordinate **application + database + infrastructure + messaging + secrets** changes so each change is independently reversible.
- Ensure release evidence (who approved, what artifact, what checks passed) and ownership are clear.
- Involve `authn-authz-and-secrets`, `database-reliability-and-operations`, `messaging-and-eventing`, `file-and-object-storage`, `api-gateway-and-service-integration`, `monitoring-alerting-and-slos`, `resilience-and-fault-tolerance`, `caching-and-distributed-state`, `search-and-indexing` when release safety depends on those platforms.

## Decision Principles

- **Automate repeatable steps** and make manual approvals explicit risk gates with audit evidence.
- Prefer **small reversible releases** over large batch deployments — small changes have small blast radius and fast rollback.
- Use **feature flags** for runtime behavior rollout, not as permanent branching logic; every flag has an owner and an expiry date.
- **Coordinate schema changes with compatible application versions** using expand-contract — never deploy a destructive schema change in the same release as the code that depends on it.
- **Test rollback** before relying on it. An untested rollback is not a rollback plan.
- For banking, insurance, and regulated systems, release evidence must show: who approved, what artifact was deployed, what checks passed, what data or secret changed, and how rollback or compensation would work — and this evidence must survive incidents and audits.
- **GitOps** (declarative config in git, controllers reconcile state) is the recommended model for Kubernetes / cloud-native systems; **imperative scripts** are acceptable for simpler topologies but require equally rigorous audit and rollback.

## Expected Output Style

- Start with the deployment topology and rollout strategy decision.
- Show the pipeline stages, gates, and rollback path explicitly.
- Separate immediate fixes (one release) from longer-term improvements (pipeline design, GitOps adoption).
- State assumptions about deployment target (k8s, serverless, VM, on-prem), traffic profile, regulated approval requirements, and team release cadence.
- Include validation checklist for the release: pre-deploy, deploy, post-deploy, and rollback drill.
- Avoid generic advice ("use canaries") unless followed by concrete percentages, gating signals, and abort criteria.

## Architecture / Design Guidance

Release architecture covers:

- **Artifact immutability**: build once, promote the same artifact across environments. Never rebuild for prod.
- **Environment parity**: dev/staging/prod use the same artifact, the same infrastructure-as-code, and only differ in configuration. Drift is a defect.
- **Infrastructure as code**: Terraform / Pulumi / CloudFormation / Bicep / Crossplane for cloud resources; Helm / Kustomize / Argo CD ApplicationSets for Kubernetes.
- **Secret management**: external secret stores (Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault) with managed identity / workload identity injection — never in artifacts, env files, or git.
- **Deployment topology**: rolling, blue-green, canary, or progressive delivery, chosen by traffic profile and risk:

  | Strategy | When | Trade-offs |
  |---|---|---|
  | **Rolling** | Default for stateless services | Brief mixed-version state during deploy; works with k8s defaults |
  | **Blue-green** | Need instant cutover and instant rollback; can afford 2x capacity briefly | DB schema must support both versions; DNS or load-balancer cutover |
  | **Canary** | High-risk change, need to observe before full rollout | Needs traffic-splitting (Istio, Linkerd, AWS ALB weighted, Cloudflare); needs SLO-based abort |
  | **Progressive delivery** (Argo Rollouts, Flagger) | Want automated canary with metric-based promotion | Requires reliable SLI metrics and an automated abort path |
  | **Shadow / mirror traffic** | Validate new version with real traffic without user impact | No write-side validation; cost of running parallel |
  | **Feature flag rollout** | Decouple deploy from release; per-tenant/segment rollout | Flag accumulation debt; needs flag governance |

- **Health checks**: liveness (restart if dead), readiness (route traffic when ready), startup (longer grace for slow boot). Misconfigured readiness causes traffic to a non-ready pod.
- **Rollout gates**: SLO burn-rate, error rate, latency p99, queue lag, dependency health — automated abort if breached.
- **Rollback strategy**: app rollback (redeploy previous artifact), config rollback (revert flag/setting), data rollback (rare, usually roll-forward with compensation). **Schema rollback is often impossible** — design schema changes as expand-contract so old code continues to work.

Releases that modify topics, queues, gateway routes, cache namespaces, search indexes, object-storage buckets, job schedules, or secrets need compatibility and migration sequencing **just like database schema changes**. Deploy compatible producers/consumers/clients first, verify lag and error rates, only then remove old contracts/routes/indexes/buckets/policies.

For regulated systems, the pipeline itself is part of the audit surface: who can trigger, who approves, what artifacts are signed (Sigstore/Cosign), what scans were run (SAST/DAST/dependency/license/secret), and what evidence is retained.

## Implementation Guidance

- **CI**: fast (<10 min) unit + static checks on every PR; longer integration / contract / security / migration checks before merge or before promotion.
- **Build**: pinned dependency versions (lockfiles), reproducible builds (`SOURCE_DATE_EPOCH`, deterministic ordering), least-privilege pipeline credentials (OIDC to cloud, no long-lived secrets in CI).
- **Artifact signing**: Sigstore / Cosign for container images; verify signature before deploy.
- **Image scanning**: Trivy, Grype, or Snyk in CI; fail on high/critical CVEs in runtime layers; re-scan promoted artifacts.
- **Configuration**: environment-specific via external config service or git overlay (Kustomize), validated at startup.
- **Secrets**: managed secret references with workload identity; rotate without redeploy where practical (apps re-fetch on TTL or signal).
- **Database changes**: expand-contract with explicit phases — (1) add new column nullable, (2) deploy code that writes both old and new, (3) backfill, (4) deploy code that reads new only, (5) deploy code that stops writing old, (6) drop old column. Each phase is independently deployable and rollback-safe (delegate detail to `database-reliability-and-operations`).
- **Messaging changes**: deploy compatible consumer first (handles old + new schema), then deploy producer with new schema, then remove old schema after consumer lag drains and no replay is needed.
- **Object storage / search / cache changes**: deploy reader of new + old format first, then writer, then deprecate old. Reindex search aliases for zero-downtime.
- **Feature flags**: every flag has owner, default, expiry, and removal PR linked. Use percentage rollout + tenant/user targeting; never use flags as permanent branching logic.
- **Canary specifics**: start at 1-5% of traffic for 10-30 min, observe SLO burn-rate and error rate, promote to 25%, 50%, 100% with validation gates between each. Automated abort on SLO breach.
- **Blue-green DNS cutover**: TTL must be short (< 1 min) before cutover, otherwise some clients hold old IPs for hours. Application Load Balancer / target group switching is faster and safer than DNS for many cases.
- **Smoke tests**: a small suite (1-5 critical paths) running immediately after deploy, before declaring success. Failure aborts the rollout.
- **Post-deploy verification**: SLO burn-rate window (30 min - 2 hours) before declaring stable; alerts on regression to previous baseline.
- **GitOps**: Argo CD or Flux reconciles desired state from git; manual `kubectl apply` is forbidden in prod. Drift detection alerts on out-of-band changes.
- **Trunk-based development**: short-lived branches, merge to main daily; feature flags hide incomplete work; release any commit on main without long stabilization.
- **Release trains** (alternative): scheduled cadence (weekly/biweekly), branch cut + stabilization + ship; useful when downstream coordination is heavy.

## Testing Expectations

- CI must run **fast unit and static checks** (lint, type, format, license, secret scan) on every change.
- Run **integration, contract, security, and migration checks** before promotion to staging.
- Run **smoke tests and health probes** after deploy to verify basic functionality before promoting traffic.
- **Practice rollback** for critical systems quarterly (game day): deploy a known-bad change, verify rollback path works, measure time to recovery.
- Validate rollout gates with **logs, metrics, traces, alerts, queue lag, cache/search health, secret access, and object-storage permissions** where relevant.
- Test **canary abort**: deploy a canary, manually trigger SLO breach, verify automated abort.
- Test **secret rotation** in non-prod first: rotate a secret, verify all consumers (app, jobs, replicas, CI) refresh without downtime.

## Security / Performance / Reliability Considerations

Security requires protected secrets (no secrets in CI logs, container layers, env files, or git), signed or traceable artifacts (Sigstore/Cosign), dependency scanning (SBOM, CVE), restricted deploy permissions (production deploy = explicit approval + audit), secret rotation plans, and audit evidence retention.

Performance requires deploys that **do not overload services** with cold starts, migrations, cache rebuilds, reindexing, or backfills. Stagger replicas during rolling deploy. Pre-warm caches if cold-start latency violates SLO. Throttle backfills to leave headroom for live traffic.

Reliability requires canaries with **automated SLO-based abort**, health checks (liveness + readiness + startup), graceful shutdown (SIGTERM handler, drain in-flight requests, deregister from load balancer before killing the process), **rollback or roll-forward with documented procedure**, deployment telemetry (deploy markers in dashboards), and explicit compensation when rollback cannot undo side effects (sent emails, published events, charged payments).

## Review Checklist

- Pipeline stages are explicit and automated; manual gates are intentional risk controls.
- Artifacts are immutable; same artifact across environments.
- Secrets are not exposed in CI logs, container layers, env files, or git.
- Configuration drift between environments is monitored and alerted.
- Rollback path is **tested**, not just documented.
- Migration order is safe (expand-contract); each phase independently deployable and rollback-safe.
- Post-deploy verification (smoke tests + SLO window) before declaring stable.
- Platform changes cover queues/topics, object storage, search, gateway policy, cache, jobs, and secrets when applicable.
- Feature flags have owner, default, expiry, removal plan.
- Canary has automated SLO-based abort; thresholds documented.
- Health checks (liveness, readiness, startup) are correctly configured.
- Graceful shutdown drains in-flight work and deregisters from load balancer.
- Audit evidence (who approved, what artifact, what scans) is retained per regulatory requirement.

## Anti-Patterns to Avoid

- Deploying from developer machines (no audit, no reproducibility, no rollback evidence).
- Changing production config manually (`kubectl edit`, console clicks) without git or audit.
- Combining risky schema changes with broad feature changes in the same release.
- Leaving stale feature flags forever ("we'll clean up later" = never).
- Assuming rollback works without testing it.
- Rotating secrets, changing gateway policy, or deleting old event/file/index contracts before all clients and jobs have moved.
- Deploying to production without canary or staged rollout for high-risk changes.
- Long-lived service account keys / API tokens in CI (use OIDC + workload identity).
- Building artifacts per environment (build for prod, rebuild for staging) — defeats artifact immutability.
- Using `latest` tag in production manifests — pin to immutable digest or version.
- Trusting `kubectl rollout undo` without verifying the previous state is still healthy and compatible with current data/dependencies.
- Skipping smoke tests because "it worked in staging".

## Gotchas / Common Failure Modes

- **Rollback may not undo data writes**: events sent, files written, payments charged, emails dispatched. Requires compensation, not rollback.
- **Canaries need representative traffic**: routing 1% of low-traffic endpoints proves nothing; weight by request volume or use shadow traffic.
- **Environment parity gaps** (different DB version, different cache, different upstream) cause release-only failures invisible in staging.
- **Secret rotation can break old running instances** if they cache credentials and don't re-fetch on rotation; design for rotation from the start.
- **Long migrations** can outlive deployment windows; chunk and resume; never block the deploy on full backfill.
- **Successful deployment ≠ safe release** if queue lag, error budgets, fraud/claims/payment workflows, or downstream reconciliations degrade after the smoke test passes. Watch SLOs for hours, not minutes.
- **Health check misconfiguration**: liveness with too-aggressive threshold restarts pods during slow GC pauses; readiness without startup probe routes traffic to non-ready pods during long boot.
- **Graceful shutdown not honored**: process killed before in-flight requests complete causes 502s and dropped messages.
- **GitOps drift**: manual changes outside git get reverted by the controller, sometimes mid-incident — make sure the team understands.
- **DNS TTL** during blue-green cutover: clients with cached DNS hit the old environment for the TTL duration; keep TTL low or use load-balancer-level cutover.
- **Container image OS layer CVEs**: re-scanning shows new CVEs even on unchanged code; have a base-image refresh cadence.
- **CI secrets in PR forks**: GitHub Actions / GitLab CI may expose secrets to fork PRs unless explicitly restricted; audit.
- **Sigstore / Cosign verification skipped**: signed artifacts are pointless if verification is not enforced at deploy time.
- **Database connection pool × replicas**: a rolling deploy briefly doubles pool count (old + new replicas alive); can exceed DB max connections and outage during the deploy itself.
- **Feature flag debt**: 100+ stale flags make code unreadable and hide dead paths. Enforce expiry with automated reports.
- **Scheduled jobs running during deploy**: a job started on the old code path may complete on the new code path with incompatible state; stop schedulers during high-risk deploys.

## See Also

- `database-reliability-and-operations` — expand-contract migrations, online DDL, replica-aware deploys, and restore drills that the release pipeline must coordinate with.
- `monitoring-alerting-and-slos` — SLO gates, burn-rate alerting, and post-deploy verification windows referenced by progressive delivery.
- `messaging-and-eventing` — consumer compatibility, schema evolution, and replay safety during rolling deploys.
- `authn-authz-and-secrets` — secret rotation, workload identity, and signed-artifact verification at deploy time.

