# Java Quality Rules

Read this file when a Java change is non-trivial, touches business logic, error handling, persistence, transactions, integration boundaries, concurrency, security, serialization, public contracts, or shared architecture.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Contents

- Design
- Complexity
- Method-level code
- Domain and business logic
- Persistence and transactions
- Spring and framework code
- Integration boundaries
- Testing
- Security
- Observability and operations
- Public contracts and compatibility

## Design

- Prefer simple classes with clear responsibilities.
- Keep business rules in the domain/application layer used by the repository.
- Keep controllers, transport adapters, repositories, and framework glue thin.
- Prefer composition over inheritance.
- Avoid anemic utility dumping grounds.
- Avoid speculative abstractions.
- Use existing abstractions before introducing new ones.
- Introduce new interfaces only when they reduce real coupling, support a real boundary, enable testability for a side-effect boundary, or match an existing project pattern.
- Prefer immutable value objects where practical.
- Use records only if the project Java version and local style allow them.
- Do not introduce DDD patterns unless the module already uses them or the domain complexity justifies them.
- Keep invariants in one place when possible.

## Complexity

- Keep cyclomatic and cognitive complexity low.
- Prefer guard clauses when they make the happy path clearer.
- Split methods that mix validation, mapping, persistence, branching, and side effects.
- Extract intention-revealing private methods when they improve readability or testability.
- Do not extract methods mechanically if it only scatters simple logic across the class.
- Avoid clever streams when a clear loop is easier to read.
- Avoid reflection, dynamic dispatch tricks, generic frameworks, and inheritance-heavy designs unless the project already uses them and they solve a real problem.

## Method-level code

- Name methods by business intent, not implementation detail.
- Keep parameters understandable.
- Introduce a value object or command object when a parameter list becomes error-prone.
- Avoid ambiguous `null` returns.
- Use `Optional` for return values only when local style supports it.
- Do not use `Optional` for fields or parameters unless the project already does so intentionally.
- Preserve root causes when wrapping exceptions.
- Do not catch broad exceptions unless the boundary requires it.
- Do not swallow exceptions silently.
- Do not log and rethrow the same exception unless the project intentionally does this.
- Keep user-facing errors safe and useful.
- Do not expose secrets, tokens, stack traces, SQL, internal class names, or sensitive payloads in user-facing errors.

## Domain and business logic

- Make important business rules visible in code, not hidden in incidental conditionals.
- Prefer explicit domain names over vague primitives when they improve correctness.
- Keep side effects at system boundaries.
- Preserve existing consistency and transaction boundaries.
- Make write operations idempotent when retries, duplicate requests, or message redelivery are possible.
- Consider ordering, duplicate events, stale state, and partial failure when changing business flows.
- Avoid global mutable state.
- Avoid time-dependent logic without an injectable clock or existing project equivalent when tests need determinism.

## Persistence and transactions

- Follow existing repository, DAO, JPA, JDBC, MyBatis, jOOQ, or migration patterns.
- Avoid N+1 queries.
- Be careful with lazy loading outside transactions.
- Keep transaction boundaries consistent with nearby code.
- Do not widen transactions without a clear reason.
- Do not perform slow external calls inside transactions unless the existing architecture intentionally does this.
- Preserve optimistic/pessimistic locking behavior.
- Do not change schema, migration order, indexes, constraints, or data migration behavior without an explicit requirement.
- When schema changes are explicitly required, consider backward compatibility, rollout order, rollback, data backfill, and old application versions.
- Keep repository queries covered by tests when behavior is non-obvious or database-specific.

## Spring and framework code

- Follow the project’s existing Spring style if present.
- Prefer constructor injection when dependency injection is used.
- Keep controllers thin.
- Put validation at request/input boundaries.
- Keep mapping logic in existing mappers/converters if the project has them.
- Avoid full Spring context tests for logic that can be tested with focused unit tests.
- Use framework annotations consistently with nearby code.
- Do not introduce framework magic when plain Java is clearer.
- Be careful with proxy-based behavior such as `@Transactional`, `@Async`, caching, validation, and security annotations.
- Do not move methods across classes in a way that accidentally disables proxy-based behavior.
- Keep configuration properties backward compatible unless explicitly requested.

## Integration boundaries

For external HTTP, messaging, filesystem, cache, search, object storage, or database boundaries:

- Consider timeouts, retries, backoff, idempotency, and partial failures.
- Keep serialization and deserialization behavior backward compatible unless the user explicitly asked to change the contract.
- Preserve existing error mapping and observability patterns.
- Avoid leaking internal exception details to external callers.
- Keep message/event consumers safe for duplicate delivery when applicable.
- Do not change topic names, queue names, routing keys, event types, or payload fields without explicit requirement.
- Avoid logging sensitive request/response bodies.

## Testing

- Prefer focused unit tests for business rules.
- Use integration tests for wiring, persistence, transactions, serialization, framework behavior, and cross-component business flows.
- Integration tests must verify meaningful business behavior, not only application startup, bean creation, or mock interactions.
- Test observable behavior, not implementation details.
- Prefer real value objects and simple fakes over deep mock chains.
- Use Mockito only for stable collaborators, side-effect boundaries, or slow/external dependencies.
- Avoid verifying every internal call unless the interaction itself is the observable behavior.
- Keep fixtures small and readable.
- Test names and display names should describe business behavior.
- Keep test method names consistent with local style.
- Add regression tests for fixed bugs.
- Add boundary tests for validation, dates, numbers, state transitions, and collection sizes when relevant.
- Add serialization/deserialization tests when changing DTOs, JSON annotations, event payloads, or API contracts.
- Add repository/integration tests when query behavior, constraints, transactions, or DB-specific behavior matter.

## Security

When the change touches input, auth, files, SQL, serialization, HTML, shell, external calls, secrets, or sensitive data:

- Validate untrusted input at boundaries.
- Prefer allow-lists over block-lists.
- Use parameterized queries or the project’s safe ORM/query APIs.
- Avoid dynamic execution of user-controlled data.
- Do not build shell commands from untrusted input.
- Prevent path traversal for file paths.
- Do not log secrets, tokens, credentials, personal data, or sensitive payloads.
- Check authorization, not only authentication.
- Preserve tenant/account/user isolation.
- Use existing crypto/security utilities.
- Do not invent custom crypto.
- Consider race conditions, replay, duplicate requests, and idempotency.
- Keep error messages safe: useful for diagnosis, but not revealing internals.

## Observability and operations

- Preserve existing logging, metrics, tracing, and audit patterns.
- Do not add noisy logs.
- Do not log sensitive values.
- Keep log levels consistent with nearby code.
- Prefer structured logging if the project uses it.
- Add metrics or audit events only when the existing architecture expects them for this behavior.
- Preserve backward compatibility for dashboards, alerts, and operational scripts when relevant.

## Public contracts and compatibility

Treat these as public contracts unless proven otherwise:

- REST/GraphQL/gRPC APIs;
- DTO fields and JSON names;
- event payloads;
- database schemas and migration order;
- configuration property names and meanings;
- command-line flags;
- scheduled job names and behavior;
- external file formats;
- error codes used by clients;
- security roles and permissions.

When contract changes are explicitly required:

- call out compatibility impact;
- preserve backward compatibility where practical;
- consider feature flags or additive changes;
- consider migration and rollback;
- update tests and documentation near the changed contract.
