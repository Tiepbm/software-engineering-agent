---
name: aws-cloud-architecture
description: 'Use when selecting AWS services, designing multi-AZ/region architecture, applying Well-Architected principles, managing IAM/networking, or optimizing AWS cost for enterprise workloads.'
---
# AWS Cloud Architecture

## Description

Guides AWS service selection, Well-Architected design, networking, IAM, cost optimization, and operational patterns for enterprise and regulated systems.

## When to Use

- Selecting between AWS compute (ECS, EKS, Lambda, EC2), database (RDS, Aurora, DynamoDB), messaging (SQS, SNS, EventBridge, MSK), or storage (S3, EFS) services.
- Designing multi-AZ, multi-region, or disaster recovery architecture.
- Applying Well-Architected Framework pillars to a design review.
- Planning IAM, VPC, security groups, or network architecture.
- Optimizing AWS cost (Reserved Instances, Savings Plans, right-sizing, spot).

## AWS Service Selection Matrix

### Compute

| Service | Strong fit | Avoid when |
|---|---|---|
| **ECS Fargate** | Containerized services, no cluster management, predictable workloads | Need GPU, need OS-level control, very cost-sensitive long-running |
| **EKS** | K8s ecosystem, multi-cloud portability, complex scheduling, service mesh | Small team without K8s expertise, simple services |
| **Lambda** | Event-driven, short-lived (< 15 min), spiky traffic, glue logic | Long-running processes, consistent high throughput, cold-start-sensitive SLOs |
| **EC2** | Full OS control, GPU, HPC, legacy apps, license-bound software | Undifferentiated container workloads (use ECS/EKS) |
| **App Runner** | Simple container deploy, no infra management, low-traffic APIs | Complex networking, service mesh, fine-grained scaling |

### Database

| Service | Strong fit | Avoid when |
|---|---|---|
| **RDS PostgreSQL/MySQL** | OLTP with joins, constraints, transactions, familiar SQL | Need horizontal write scaling beyond read replicas |
| **Aurora** | RDS workloads needing better HA (multi-AZ failover < 30s), read scaling (15 replicas), serverless v2 for spiky | Cost-sensitive small workloads (Aurora minimum is higher than RDS) |
| **DynamoDB** | Known access patterns, massive scale, single-digit ms latency, serverless | Ad-hoc queries, joins, complex transactions, unknown access patterns |
| **ElastiCache Redis** | Cache, session, rate limit, pub/sub, leaderboard | Primary durable storage (use RDS/DynamoDB) |
| **DocumentDB** | MongoDB-compatible API on AWS managed infra | Need full MongoDB features (DocumentDB is not 100% compatible) |
| **Redshift/Athena** | Analytics, BI, large scans | OLTP request serving |

### Messaging

| Service | Strong fit | Avoid when |
|---|---|---|
| **SQS** | Simple queue, decoupling, at-least-once, no ordering needed | Strict ordering (use SQS FIFO), fan-out (use SNS+SQS), event replay |
| **SQS FIFO** | Ordered processing per message group, exactly-once | High throughput > 3000 msg/s per queue, need replay |
| **SNS** | Fan-out to multiple subscribers, push notifications | Need message persistence or replay (use SNS+SQS or EventBridge) |
| **EventBridge** | Event routing with rules, schema registry, cross-account, SaaS integration | Simple point-to-point queue (use SQS), high-throughput streaming |
| **MSK (Kafka)** | Event streaming, replay, ordering, high throughput, consumer groups | Simple queue workloads (over-engineering), team has no Kafka expertise |
| **Kinesis** | Real-time streaming, analytics, short retention | Long retention + replay (use MSK), simple queue (use SQS) |

### Storage

| Service | Strong fit | Avoid when |
|---|---|---|
| **S3** | Object storage, documents, backups, data lake, static hosting | File system semantics needed (use EFS), low-latency block storage (use EBS) |
| **EFS** | Shared file system across containers/instances, POSIX compatible | Object storage workloads (use S3), high IOPS (use EBS) |
| **EBS** | Block storage for EC2, database volumes | Shared access across instances (use EFS), object storage (use S3) |

## Well-Architected Pillars (Decision Checklist)

| Pillar | Key questions for every design |
|---|---|
| **Operational Excellence** | How do we deploy? How do we detect failures? Who owns on-call? Runbooks exist? |
| **Security** | IAM least privilege? Encryption at rest + transit? VPC isolation? Secrets in Secrets Manager? Audit via CloudTrail? |
| **Reliability** | Multi-AZ? Auto-scaling? Health checks? Backup + restore tested? Failover tested? |
| **Performance** | Right-sized? Caching (ElastiCache/CloudFront)? Read replicas? Connection pooling? |
| **Cost Optimization** | Reserved/Savings Plans for baseline? Spot for fault-tolerant? Right-sized? Lifecycle policies on S3? Unused resources cleaned? |
| **Sustainability** | Right-sized (not over-provisioned)? Serverless where appropriate? Data lifecycle managed? |

## IAM Patterns

| Pattern | Rule |
|---|---|
| **Service roles** | Each ECS task / Lambda function gets its own IAM role. Never share roles across services. |
| **Least privilege** | Start with zero permissions, add only what's needed. Use IAM Access Analyzer to find unused permissions. |
| **No long-lived keys** | Use IAM roles (not access keys) for services. Use OIDC federation for CI/CD (GitHub Actions → AWS). |
| **Secrets** | Secrets Manager or SSM Parameter Store (SecureString). Never environment variables for sensitive values in Lambda/ECS task definitions. |
| **Cross-account** | Use AssumeRole with external ID. Never share root credentials. |
| **MFA** | Required for console access and destructive API calls (S3 delete, RDS delete). |

## Networking Patterns

| Pattern | When |
|---|---|
| **VPC with public + private subnets** | Default for most workloads. Public: ALB, NAT Gateway. Private: ECS tasks, RDS, ElastiCache. |
| **VPC endpoints** | S3, DynamoDB, SQS, SNS, Secrets Manager — avoid NAT Gateway cost and latency for AWS service calls. |
| **Security groups** | Allow only required ports. Reference other security groups (not CIDR) for service-to-service. |
| **NACLs** | Stateless, use only for broad deny rules. Security groups are primary. |
| **PrivateLink** | Cross-account or cross-VPC service access without internet exposure. |
| **Transit Gateway** | Multi-VPC, multi-account networking hub. |

## Cost Optimization Patterns

| Pattern | Savings |
|---|---|
| **Savings Plans (Compute)** | 30-40% for predictable baseline compute (ECS, Lambda, EC2) |
| **Reserved Instances (RDS/ElastiCache)** | 30-60% for stable database workloads |
| **Spot Instances** | 60-90% for fault-tolerant batch, CI/CD runners, dev/test |
| **S3 Intelligent-Tiering** | Auto-moves objects between access tiers. No retrieval fees. |
| **S3 Lifecycle policies** | Archive to Glacier after 90d, delete after retention period |
| **Right-sizing** | Use Compute Optimizer recommendations. Over-provisioned = wasted money. |
| **NAT Gateway alternatives** | VPC endpoints for AWS services (S3, DynamoDB, SQS) save NAT cost |
| **Lambda right-sizing** | Use Power Tuning to find optimal memory/cost ratio |

## Multi-AZ and Disaster Recovery

| Strategy | RPO | RTO | Cost | Use when |
|---|---|---|---|---|
| **Multi-AZ (active-active)** | 0 | < 1 min | Baseline | Default for production |
| **Pilot light** | Minutes | 10-30 min | Low | DR for non-critical systems |
| **Warm standby** | Seconds | < 10 min | Medium | DR for important systems |
| **Multi-region active-active** | 0 | 0 | High | Global users, regulatory data residency |

## Anti-Patterns

- Using EC2 for stateless container workloads (use ECS Fargate or EKS).
- DynamoDB for unknown or ad-hoc query patterns (use RDS).
- Lambda for consistent high-throughput APIs (use ECS — Lambda cold starts + per-invocation cost).
- Single-AZ for production databases (always Multi-AZ for RDS/Aurora).
- Long-lived IAM access keys for services (use IAM roles).
- NAT Gateway for all AWS service traffic (use VPC endpoints).
- Over-provisioned instances "just in case" (use auto-scaling + right-sizing).
- Storing secrets in environment variables or SSM plain-text parameters.
- S3 bucket policies with `*` principal (public access by accident).

## Gotchas

- **Lambda cold starts**: 100ms-2s depending on runtime and VPC. Use provisioned concurrency for SLO-sensitive paths.
- **DynamoDB throttling**: hot partition keys cause throttling even with provisioned capacity. Design partition keys for even distribution.
- **SQS visibility timeout**: must be longer than consumer processing time, or message reappears and gets processed twice.
- **RDS connection limits**: each instance has a max connection count. Use RDS Proxy for Lambda or high-connection workloads.
- **S3 eventual consistency**: S3 is now strongly consistent for PUTs, but CloudFront caching can serve stale content.
- **ECS task role vs execution role**: task role = what the app can do. Execution role = what ECS agent can do (pull images, write logs).
- **Aurora Serverless v2 scaling**: scales in 0.5 ACU increments, but scaling up takes seconds — not instant for traffic spikes.
- **EventBridge rule limits**: 300 rules per bus by default. Request increase early for event-heavy architectures.
- **Cross-region replication cost**: S3 CRR, DynamoDB Global Tables, Aurora Global Database all add transfer + storage cost.

## Review Checklist

- [ ] Service selection has workload-fit reasoning (not "we always use X").
- [ ] Multi-AZ enabled for all production stateful services.
- [ ] IAM roles per service, least privilege, no long-lived keys.
- [ ] Secrets in Secrets Manager or SSM SecureString.
- [ ] VPC endpoints for high-traffic AWS service calls.
- [ ] Auto-scaling configured with appropriate min/max/target.
- [ ] Backup + restore tested (not just enabled).
- [ ] Cost baseline established; Savings Plans for predictable workloads.
- [ ] CloudTrail enabled for audit; CloudWatch alarms for critical metrics.
- [ ] S3 lifecycle policies and encryption configured.
