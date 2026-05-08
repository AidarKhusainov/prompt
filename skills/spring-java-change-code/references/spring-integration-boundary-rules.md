# Spring Integration Boundary Rules

Use this reference before editing outbound HTTP clients, Telegram/API clients, scheduled ingestion jobs, retries, timeouts, idempotency, message publishing, external DTO mapping, or integration tests for external systems.

## External systems are unreliable

For every external integration, consider:

- timeout behavior;
- retry policy and backoff;
- idempotency and duplicate handling;
- rate limits and quota behavior;
- authentication and token handling;
- error classification;
- fallback behavior;
- partial failure behavior;
- observability;
- test stubs, fakes, containers, or contract fixtures.

Do not add infinite retries, unbounded queues, blocking calls in reactive flows, silent data loss, or fallbacks that hide failed ingestion.

## Outbound clients

Use the project's existing client style first:

- `RestClient`;
- `WebClient`;
- `RestTemplate`;
- OpenFeign or another established declarative client;
- generated OpenAPI client;
- project-specific gateway/adapter abstraction.

Do not introduce a new HTTP client library or integration framework for a small change unless the user explicitly asked for it or the existing stack cannot support the requirement.

Configure base URL, timeouts, authentication, default headers, serialization, deserialization, and error handling centrally according to project style.

Do not build URLs by unsafe string concatenation when user-controlled or external values are involved.

Do not log request/response bodies, headers, tokens, cookies, credentials, provider secrets, or raw third-party payloads unless the project has an explicit sanitized debug mechanism.

## Error handling

Classify external failures deliberately:

- validation/client errors from the provider;
- authentication or authorization errors;
- rate limiting;
- timeout;
- transient server errors;
- malformed or incompatible provider responses;
- duplicate or already-processed data;
- permanent unsupported data.

Do not swallow provider errors silently.

When a failure affects user-visible behavior, map it to the existing application error style.

When a failure affects background ingestion, make it observable through logs, metrics, retry state, dead-letter handling, skipped-item reporting, or another project-established mechanism.

## Idempotency and duplicates

For ingestion, polling, scheduled jobs, webhooks, message consumers, and external event processing:

- assume at-least-once delivery unless the provider guarantees otherwise;
- make processing idempotent when feasible;
- define a stable deduplication key;
- preserve checkpoints carefully;
- avoid advancing checkpoints before durable processing succeeds;
- handle replay and retry without corrupting state;
- keep duplicate handling observable when it affects business behavior.

Do not rely only on in-memory state for deduplication or checkpoints unless the project intentionally accepts that limitation.

## External DTOs and mapping

Keep external provider DTOs at the integration boundary.

Do not leak third-party API models into domain models, persistence models, or public API responses unless the project already intentionally does that.

Map provider fields into application-owned models deliberately, including:

- optional/missing fields;
- unexpected enum values;
- timestamp/time zone semantics;
- provider ids;
- pagination cursors;
- localization/encoding quirks;
- backwards-incompatible provider changes.

Do not bind untrusted provider payloads directly to persistence entities.

## Scheduling, polling, and background jobs

For scheduled or background integration flows:

- avoid overlapping executions unless intentional;
- use locking, single-flight execution, or idempotency when concurrent runs can conflict;
- apply bounded retries and backoff;
- avoid tight loops on provider failures;
- make progress and failure states visible;
- preserve last-successful checkpoints carefully;
- avoid losing data when processing partially succeeds.

Do not make a scheduled job depend on wall-clock timing in tests when a fake clock, explicit trigger, or direct application service boundary would be more deterministic.

## Messaging and events

For message publishing or consuming:

- preserve event schema and compatibility unless explicitly requested;
- consider ordering, duplication, retry, and dead-letter behavior;
- make consumers idempotent when practical;
- avoid publishing before the transaction commits unless the project intentionally uses that pattern;
- prefer the project's existing outbox, transaction synchronization, or event publication style when present.

Do not introduce a broker, outbox, or eventing framework for a small local change without explicit scope.

## Testing external integrations

Stub or fake true external systems.

Prefer the project's existing approach:

- WireMock;
- MockWebServer;
- local fake adapter;
- Spring test configuration with a fake gateway;
- contract fixtures;
- Testcontainers for infrastructure semantics;
- provider sandbox only when the project already uses it and credentials are available safely.

In full-flow Spring integration tests, keep internal services, repositories, mappers, validators, and Spring components real by default. Stub only the external integration boundary.

For outbound HTTP behavior, test at least the important observable cases:

- success mapping;
- provider error mapping;
- timeout or transient failure when relevant;
- malformed or missing provider fields when relevant;
- retry/idempotency behavior when the feature depends on it.

Do not require real external credentials or live third-party services for normal automated tests.
