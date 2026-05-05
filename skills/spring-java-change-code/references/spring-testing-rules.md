# Spring Testing Rules

Use this reference before adding or changing Spring tests, choosing between unit/slice/integration/random-port tests, stubbing integrations, adding Testcontainers, or changing test configuration.

## Default testing philosophy

Prefer observable behavior over implementation details.

For Spring web applications, prefer black-box or near-black-box tests for externally observable application behavior, using the narrowest reliable Spring test boundary.

Use fast unit tests for pure business rules, edge cases, branching-heavy logic, validation helpers, mappers/converters, calculations, state transitions, deterministic domain logic, and time-dependent logic with injectable `Clock`.

Use Spring integration or slice tests for behavior that depends on Spring boundaries: HTTP routing and status codes, validation and error mapping, JSON serialization/deserialization, security behavior, persistence and repository queries, transactions, configuration properties, framework wiring, and cross-component application flows.

Keep application internals real by default in integration tests.

Do not mock internal services, repositories, mappers, validators, or Spring components unless the project already has that pattern, the dependency is genuinely outside the behavior under test, or the test is intentionally a narrow slice test and the collaborator is outside that slice.

Stub/mock mainly true external integrations: third-party HTTP APIs, external auth providers, independently deployed message brokers outside the current test scope, email/SMS providers, payment providers, cloud object storage, search services, and other independently deployed systems.

## Choosing test scope

Use the narrowest test that proves the changed behavior:

- unit test: pure logic and edge cases;
- slice test: MVC, JSON, validation, JPA, security slice, REST client, WebClient, or another framework slice;
- full-context integration test: behavior depends on multiple Spring-managed components working together;
- random-port black-box test: real HTTP/server behavior matters;
- Testcontainers: behavior depends on real infrastructure semantics.

Do not use `@SpringBootTest` for pure business logic that can be tested without Spring.

Do not replace fast unit tests with slow full-context tests when a focused unit test is the reliable boundary.

Do not introduce Testcontainers as a new project-wide testing dependency for a small change unless infrastructure semantics are essential or the project already uses Testcontainers.

## Black-box API tests

For API features, prefer tests that:

1. send a request as a client would;
2. assert status, headers, response body, persisted state, emitted events, or observable side effects;
3. avoid verifying internal method calls;
4. use realistic fixtures;
5. cover happy path, invalid input, authorization/security, and important edge cases.

A test that only verifies `service.create(...)` was called from a controller is usually too implementation-focused when the observable API behavior can be asserted.

## Slice tests

Use slice tests when the slice is the behavior boundary.

Examples:

- web/controller mapping, validation, JSON, and error mapping through MVC/WebFlux test support;
- repository query behavior through data-slice tests;
- serialization/deserialization contracts through JSON tests;
- security behavior through a security-enabled slice or full-context test when the endpoint boundary matters.

Mock collaborators only when they are outside the slice and the test still asserts observable behavior at that slice boundary.

## Full-context integration tests

Use full-context integration tests when behavior depends on multiple Spring-managed components working together.

Keep internal Spring components real by default: services, repositories, mappers, validators, transaction configuration, serialization and error mapping, and security configuration when security behavior is relevant.

Stub true external integrations through established project patterns such as test configuration, fake clients, WireMock/MockWebServer, embedded brokers, contract stubs, or containerized services.

## Transaction note for random-port tests

When using `@SpringBootTest(webEnvironment = RANDOM_PORT)` or `DEFINED_PORT`, do not assume server-side database changes are rolled back by a transactional test method.

Client and server run in separate threads and separate transactions.

Use explicit cleanup, isolated test data, rollback through application behavior, database cleanup utilities, or container lifecycle according to the project style.

## Testcontainers

Use Testcontainers when behavior depends on real infrastructure semantics: PostgreSQL/MySQL-specific SQL, constraints and indexes, JSON/array/db-specific column types, transaction behavior, Kafka/Rabbit/Redis/etc. behavior, or compatibility with production-like services.

When Spring Boot supports it for the project version, prefer `@ServiceConnection` or existing project conventions for wiring container connection details.

Do not start Testcontainers for pure business logic.

Avoid silently replacing the production database with H2 when database-specific behavior matters.

## Security testing

Security behavior must be tested through the security boundary.

Do not disable filters in tests unless the test explicitly is not about security, the project already uses this pattern, and the change does not weaken production security behavior.

For secured endpoints, include unauthorized, forbidden, and allowed cases when behavior changes.

Never make tests pass by disabling CSRF, CORS, authentication, authorization, method security, or security filters.

## Avoid

Avoid testing only that the context loads, replacing fast unit tests with `@SpringBootTest`, using mocks for repository behavior that depends on real SQL/JPA semantics, mocking internal Spring services in full-flow tests, deep Mockito chains for business behavior, verifying every internal call when observable behavior is enough, weakening assertions to make tests pass, disabling security filters to simplify tests, and skipping failing tests caused by the change.

## Self-review

Before finishing, check that tests cover the changed observable behavior, use the narrowest reliable boundary, keep Spring internals real where framework/application behavior is under test, stub true external integrations rather than internal services, include unit edge cases for pure logic, include security cases for secured behavior, do not require unnecessary infrastructure for simple logic, and follow existing project naming, fixtures, profiles, and cleanup style.
