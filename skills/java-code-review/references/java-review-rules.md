# Java Review Rules

Read this file when reviewing non-trivial Java changes, especially changes that touch business logic, error handling, validation, persistence, transactions, integration boundaries, concurrency, security, serialization, public contracts, generated code, dependencies, or shared architecture.

Use these rules to form concrete findings. Do not paste this checklist into the final review. Report only issues that are supported by the diff and repository context.

## Contents

- Correctness
- Business logic and domain behavior
- Public contracts and compatibility
- Persistence and transactions
- Spring and framework behavior
- Integration boundaries
- Concurrency and idempotency
- Security and privacy
- Testing
- Observability and operations
- Maintainability and architecture
- Generated code and dependencies

## Correctness

Look for changes that can produce incorrect results, regressions, crashes, data corruption, data loss, or broken workflows.

Check whether:

- the implementation matches the requested behavior and acceptance criteria;
- edge cases are handled intentionally;
- null, empty, missing, duplicate, and malformed inputs are safe;
- boundary values are handled correctly;
- conditionals preserve existing behavior outside the requested change;
- default values, fallbacks, and feature flags behave as expected;
- errors are not accidentally swallowed;
- exceptions preserve useful root causes;
- date, time, timezone, locale, rounding, precision, and ordering logic is deterministic where needed;
- collections are not modified while iterating unless safe;
- object equality, hash codes, and ordering are consistent when changed;
- mutable shared objects are not exposed accidentally.

## Business logic and domain behavior

Check whether business rules are implemented in the appropriate domain or application layer used by the repository.

Look for:

- rules hidden in controllers, transport adapters, repositories, or framework glue when a service/domain layer exists;
- duplicated business logic instead of reuse of existing policy, validator, mapper, or domain method;
- invariants that can be bypassed through constructors, setters, builders, or persistence hydration;
- state transitions that miss invalid, repeated, stale, or out-of-order states;
- partial updates that can leave inconsistent state;
- business decisions based on display labels or localized text instead of stable identifiers;
- time-dependent logic without the repository’s existing clock or testable time abstraction;
- speculative abstractions that hide simple rules.

## Public contracts and compatibility

Treat these as public contracts unless proven otherwise:

- REST, GraphQL, gRPC, RPC, or CLI contracts;
- DTO fields and JSON names;
- event payloads and message headers;
- database schemas, migration order, indexes, and constraints;
- configuration property names, defaults, and meanings;
- security roles, permissions, scopes, and claims;
- scheduled job names and behavior;
- external file formats;
- error codes and user-visible error shapes.

Flag changes that:

- remove, rename, or change the type or meaning of public fields;
- break backward or forward compatibility;
- change serialization/deserialization behavior without tests;
- change validation rules without migration or rollout consideration;
- change configuration defaults in a risky way;
- require data backfill, dual-read/write, feature flags, or staged rollout but do not include them;
- lack compatibility notes, migration notes, or rollback considerations for explicit breaking changes.

Prefer additive, backward-compatible changes when practical.

## Persistence and transactions

For JPA, JDBC, MyBatis, jOOQ, repositories, migrations, and transaction changes, check whether:

- query semantics match the intended behavior;
- N+1 queries are not introduced;
- lazy-loaded data is not accessed outside a transaction;
- transaction boundaries are not widened or narrowed accidentally;
- slow external calls are not added inside transactions;
- write ordering is safe;
- locking behavior is preserved;
- optimistic or pessimistic locking failures are handled intentionally;
- batch updates are safe for large datasets;
- migrations are backward compatible with old and new application versions when needed;
- indexes and constraints support new queries or uniqueness assumptions;
- repository tests cover non-obvious or database-specific behavior.

## Spring and framework behavior

For Spring or similar frameworks, check whether:

- annotations are used consistently with nearby code;
- dependency injection style matches the project;
- controllers remain thin;
- request validation occurs at boundaries;
- mapping logic stays in existing mappers/converters when present;
- proxy-based behavior is preserved for `@Transactional`, `@Async`, caching, validation, and security annotations;
- methods were not moved to a class or visibility where framework proxies no longer apply;
- configuration properties remain backward compatible;
- conditional beans, profiles, and auto-configuration behave as intended;
- tests do not use a full application context when focused unit tests would cover the behavior better.

## Integration boundaries

For external HTTP, messaging, filesystem, cache, search, object storage, database boundaries, or third-party SDKs, check whether:

- timeouts are present or inherited from existing clients;
- retries and backoff do not duplicate unsafe writes;
- operations are idempotent when retried or redelivered;
- partial failures are handled;
- response status and error mapping preserve useful diagnostics;
- serialization and deserialization remain compatible;
- topic names, queue names, routing keys, event types, and payload fields are not changed accidentally;
- sensitive request or response bodies are not logged;
- external calls are not made inside transactions unless the architecture already expects it;
- resource cleanup is handled for streams, files, sockets, and clients.

## Concurrency and idempotency

Check whether the change is safe under duplicate requests, retries, concurrent execution, scheduled jobs, and message redelivery.

Look for:

- non-atomic read-modify-write sequences;
- missing uniqueness constraints or idempotency keys;
- unsafe mutable static or shared state;
- unsynchronized caches or maps;
- order-dependent logic that can receive out-of-order events;
- race conditions around status transitions;
- background jobs that can overlap unexpectedly;
- retry loops without limits or backoff;
- operations that are not safe to repeat after partial success.

## Security and privacy

When code touches input, auth, files, SQL, HTML, shell, serialization, external calls, logs, secrets, or sensitive data, check whether:

- untrusted input is validated at boundaries;
- allow-lists are used where appropriate;
- SQL or query APIs are parameterized;
- shell commands are not built from untrusted input;
- file paths prevent traversal;
- deserialization does not instantiate unsafe types from untrusted data;
- authentication is not confused with authorization;
- tenant, account, organization, and user isolation is preserved;
- roles, scopes, and ownership checks are applied at the right layer;
- secrets, tokens, credentials, personal data, and sensitive payloads are not logged or returned;
- error messages are useful but do not reveal internals;
- existing crypto/security utilities are used instead of custom crypto;
- replay, race, and duplicate-request risks are considered for sensitive operations.

## Testing

Check whether tests cover the changed observable behavior, not only implementation details.

Important missing coverage includes:

- new or changed business rule happy path;
- regression case for the bug being fixed;
- invalid input;
- null, empty, duplicate, and boundary values;
- authorization and tenant isolation;
- transaction, persistence, query, and migration behavior;
- serialization/deserialization compatibility;
- concurrency, idempotency, retry, and ordering behavior;
- error mapping and user-visible errors;
- generated contract or schema changes.

Flag tests that:

- weaken or delete relevant assertions;
- only verify mocks when observable behavior should be asserted;
- mock away the behavior under test;
- rely on overly broad full-context tests for simple business logic;
- add brittle assertions on implementation details;
- hide failures with sleeps, ignored tests, broad exception catches, or excessive leniency;
- lack clear names for the business behavior being verified.

## Observability and operations

Check whether the change preserves or improves operational understanding without leaking sensitive data.

Look for:

- missing logs, metrics, audit events, or traces where the repository already expects them;
- noisy logs added to hot paths;
- log levels inconsistent with nearby code;
- duplicate logging and rethrowing;
- sensitive data in logs or error messages;
- changed job names, metric names, labels, or dashboards without compatibility consideration;
- rollout, rollback, and feature-flag gaps for risky changes;
- missing alerts or metrics for new critical flows when local patterns suggest they are required.

## Maintainability and architecture

Flag maintainability issues only when they create real review value.

Look for:

- unnecessary complexity, nesting, or clever streams;
- broad refactors mixed with behavior changes;
- accidental formatting churn;
- duplicate implementations of existing helpers, validators, mappers, parsers, fixtures, or factories;
- new abstractions with only speculative value;
- public helpers created for private one-off behavior;
- inappropriate inheritance over composition;
- classes or methods with unclear responsibility;
- transport, persistence, and domain concerns mixed together;
- temporary logs, debug prints, commented-out code, unused imports, dead code, draft files, or TODOs without linked follow-up.

## Generated code and dependencies

For generated code, check whether:

- the source schema, IDL, OpenAPI spec, template, annotation, or generator input was changed instead of editing generated output directly;
- generated output matches repository workflow;
- regeneration did not modify unrelated files;
- generated files are not hand-edited without explicit justification.

For dependency or build changes, check whether:

- the dependency is clearly needed;
- existing project utilities or standard library APIs would be sufficient;
- the dependency is production or test-only as appropriate;
- versions, lockfiles, catalogs, and wrappers are changed only when required;
- plugin, wrapper, Java version, formatter, linter, or CI changes are directly related;
- license, security, and maintenance risk are acceptable for the repository context.
