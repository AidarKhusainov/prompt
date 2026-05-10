# Spring Integration Boundary Rules

Use this reference before changing Spring-managed outbound integrations, Spring-managed external API clients, external API clients participating in Spring bean wiring/configuration/testing boundaries, scheduled ingestion jobs, retries, timeouts, idempotency, message publishing, or integration tests for external systems.

Examples include third-party HTTP APIs, Telegram bots or clients, RSS/news providers, payment providers, email/SMS providers, external auth providers, search services, object storage, independently deployed message brokers, LLM providers, and other systems outside the current application boundary.

## External systems are unreliable

For every external integration, consider:

- connection, read, and total timeouts;
- retry policy, max attempts, retry budget, backoff, jitter, and retryable error classification;
- provider throttling signals such as `Retry-After`;
- idempotency and duplicate delivery;
- rate limits, quotas, and provider throttling;
- authentication, token refresh, and secret handling;
- provider-specific error mapping;
- fallback behavior and data-loss risk;
- partial failure and recovery behavior;
- observability: logs, metrics, correlation ids, and provider outcome;
- test doubles, contract fixtures, or containers according to project style.

Do not add infinite retries, unbounded queues, silent fallbacks, swallowed provider errors, or blocking calls inside reactive flows.

Do not retry non-repeatable write-like operations without an idempotency key, deduplication marker, or provider-supported replay protection.

Do not combine retry and fallback in a way that makes provider failure invisible or turns a failed integration into a misleading successful application result.

In reactive code paths, treat these as red flags unless the project already isolates them safely:

- `.block()` inside a reactive chain or event-loop path;
- `.toFuture().get()` or other blocking future waits;
- `Thread.sleep(...)`;
- blocking provider SDK calls in reactive handlers, filters, controllers, schedulers, or operators;
- wrapping blocking work in reactive code without following the project's scheduler/bounded-elastic/offloading pattern.

If a blocking provider SDK is unavoidable, isolate it according to the project convention and make the blocking boundary explicit. Do not silently mix blocking provider calls into a reactive pipeline.

## Client style

Use the project's existing integration style first:

- `RestClient` when supported by the project Spring version and already used or appropriate for the local style;
- `WebClient` when the project is reactive or already uses it for outbound clients;
- `RestTemplate` when it is the existing project style or legacy convention;
- OpenFeign or another existing declarative client;
- Spring HTTP Service Clients when supported by the project Spring version and local conventions;
- generated OpenAPI clients;
- a project-specific adapter/gateway abstraction.

Do not choose `WebClient` only because it is newer, and do not introduce `RestClient` into Spring generations that do not support it. Detect the project Spring version and follow `spring-version-policy.md` before changing client APIs.

Do not introduce a new HTTP client library for a small integration change.

Keep integration configuration centralized according to project conventions: base URL, timeouts, auth, default headers, serialization, error handling, retry policy, and observability.

Keep base URL, timeout, retry, auth, and provider options in the project's existing configuration style. Prefer validated `@ConfigurationProperties` when the project uses it. Read `spring-configuration-rules.md` before adding or changing Spring configuration for external clients.

Do not hard-code provider URLs, credentials, timeout values, retry counts, or magic constants inside client code.

Do not build URLs through unsafe string concatenation when user-controlled or provider-controlled values are involved. Prefer URI builders, encoded path/query parameters, or existing client helpers.

## Boundary models

Keep provider DTOs and wire models at the integration boundary.

Do not leak third-party request/response DTOs into domain models, persistence models, or public API response models unless the project already intentionally uses that pattern.

Map external provider responses, errors, and statuses into application-level concepts deliberately.

Do not persist raw provider payloads by default when they may contain secrets, PII, large content, unstable schemas, or irrelevant fields. If raw payload retention is required, sanitize and document the reason.

## Resilience and idempotency

Before adding retries or scheduled ingestion, identify whether the operation is safe to repeat.

For write-like external operations, prefer explicit idempotency keys or deduplication markers when the provider supports them.

For polling/ingestion jobs, preserve checkpoints carefully and make processing resilient to:

- duplicate items;
- out-of-order items;
- provider pagination changes;
- partial page failures;
- interrupted runs;
- overlapping scheduler executions;
- provider rate limiting.

Advance checkpoints only after durable and transactionally consistent processing.

When ingestion combines database writes with message publishing or external side effects, look for existing outbox, after-commit, transactional event, or idempotent publisher patterns.

Do not publish events or call external side-effecting APIs before the related database transaction is committed unless the project intentionally uses that pattern and the failure semantics are explicit.

Do not hide failed ingestion with a successful application result unless the user explicitly requested best-effort behavior and the behavior is observable.

## Testing external integrations

Stub or fake true external systems; keep internal Spring application components real by default in full-flow integration tests.

Prefer the project's existing approach for external test doubles, such as:

- WireMock;
- MockWebServer;
- local fake adapters;
- contract fixtures;
- provider sandbox containers;
- Testcontainers when infrastructure semantics are essential and already supported by the project.

Integration tests should assert observable application behavior: status, response body, persisted state, emitted events, scheduled job results, retry/error handling, and provider request shape when relevant.

Do not replace a meaningful integration test with a Mockito verification that an internal service method was called.

## Security and secrets

Never log tokens, API keys, Authorization headers, cookies, full signed URLs, raw webhook secrets, or provider credentials.

Do not commit sample real credentials in configuration, fixtures, docs, or tests.

For webhook or callback handlers, validate signatures, timestamps, replay protections, and content type according to project/provider conventions.

When provider signatures depend on request bytes or canonical requests, verify the signature against the raw body or provider-specific canonical request before trusting deserialized DTOs.

Use a timing-safe comparison for signatures or MACs when the project/platform provides one.

Reject stale timestamps and replayed delivery ids/nonces when the provider supplies timestamp or replay-protection data.

Treat provider allowlists, callback URLs, redirect URLs, and webhook exposure as security-sensitive changes.

## Operational visibility

For important integration flows, consider existing logging, metrics, and tracing conventions:

- provider name;
- operation name;
- sanitized external status/error class;
- duration;
- retry count;
- rate-limit response;
- skipped, duplicate, accepted, and failed item counts;
- checkpoint progress for ingestion jobs.

Avoid high-cardinality metric tags such as raw URLs, user ids, message text, titles, provider payloads, exception messages, or arbitrary external ids.

## Permission gates

Ask before adding a production dependency, changing provider-facing contracts, changing webhook exposure, changing scheduler cadence, changing retry/backoff semantics broadly, introducing Spring Retry, Resilience4j, a new HTTP client, a scheduler/retry framework, a message broker/client framework, persisting raw provider payloads, or changing token/secret handling unless the user explicitly requested that change.
