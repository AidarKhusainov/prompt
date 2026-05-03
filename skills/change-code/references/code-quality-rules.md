# Code Quality Rules

Read this file when a change is non-trivial, touches business logic, error handling, validation, persistence or state, integration boundaries, async/concurrency, security, serialization, public contracts, shell execution, filesystem operations, or shared architecture.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Contents

- Design
- Complexity
- Method-level code
- Domain and business logic
- State, persistence, and transactions
- Integration boundaries
- Shell and filesystem safety
- Testing
- Security
- Observability and operations
- Public contracts and compatibility

## Design

- Prefer simple modules, functions, classes, scripts, and commands with clear responsibilities.
- Keep business rules in the domain or application layer used by the repository.
- Keep transport adapters, controllers, CLI wrappers, framework glue, scripts, and repositories thin when the architecture supports it.
- Prefer composition and explicit data flow over inheritance-heavy or hidden global behavior.
- Avoid speculative abstractions.
- Use existing abstractions before introducing new ones.
- Introduce new interfaces, protocols, or adapter layers only when they reduce real coupling, support a real boundary, enable testability for a side-effect boundary, or match an existing project pattern.
- Keep invariants in one place when possible.

## Complexity

- Keep cyclomatic and cognitive complexity low.
- Prefer guard clauses when they make the happy path clearer.
- Split code that mixes validation, mapping, persistence, branching, and side effects.
- Extract intention-revealing helpers when they improve readability or testability.
- Do not extract helpers mechanically if it only scatters simple logic.
- Avoid clever language features when straightforward code is easier to read.
- Avoid reflection, dynamic execution, metaprogramming, generic frameworks, and inheritance-heavy designs unless the project already uses them and they solve a real problem.

## Method-level code

- Name functions, methods, variables, scripts, and commands by intent, not implementation detail.
- Keep parameters understandable.
- Introduce a value object, options object, or command object when a parameter list becomes error-prone and the local style supports it.
- Avoid ambiguous `null`, `undefined`, empty-string, or sentinel returns.
- Preserve root causes when wrapping errors.
- Do not catch broad errors unless the boundary requires it.
- Do not swallow errors silently.
- Do not log and rethrow the same error unless the project intentionally does this.
- Keep user-facing errors safe and useful.
- Do not expose secrets, tokens, stack traces, SQL, internal class names, server paths, shell commands with sensitive args, or sensitive payloads in user-facing errors.

## Domain and business logic

- Make important business rules visible in code, not hidden in incidental conditionals.
- Prefer explicit domain names over vague primitives when they improve correctness.
- Keep side effects at system boundaries.
- Preserve existing consistency, transaction, async, and retry boundaries.
- Make write operations idempotent when retries, duplicate requests, message redelivery, or repeated CLI/script execution are possible.
- Consider ordering, duplicate events, stale state, partial failure, and rollback when changing business flows.
- Avoid global mutable state.
- Avoid time-dependent logic without an injectable clock, fakeable time source, or existing project equivalent when tests need determinism.

## State, persistence, and transactions

- Follow existing repository, DAO, ORM, query, migration, cache, or file-state patterns.
- Avoid N+1 queries and unnecessary repeated IO.
- Keep transaction or consistency boundaries aligned with nearby code.
- Do not widen transactions, locks, critical sections, or long-running operations without a clear reason.
- Do not perform slow external calls inside transactions or locks unless the existing architecture intentionally does this.
- Preserve optimistic/pessimistic locking, cache invalidation, and retry behavior.
- Do not change schema, migration order, indexes, constraints, persisted file formats, or data migration behavior without an explicit requirement.
- When schema or persisted-format changes are explicitly required, consider backward compatibility, rollout order, rollback, data backfill, and old application versions.

## Integration boundaries

For external HTTP, messaging, filesystem, shell commands, cache, search, object storage, databases, queues, browsers, or third-party SDKs:

- Consider timeouts, retries, backoff, cancellation, idempotency, and partial failures.
- Keep serialization and deserialization behavior backward compatible unless the user explicitly asked to change the contract.
- Preserve existing error mapping and observability patterns.
- Avoid leaking internal exception details to external callers.
- Keep message/event consumers safe for duplicate delivery when applicable.
- Do not change endpoint paths, topic names, queue names, routing keys, event types, payload fields, CLI flags, file formats, or environment variable semantics without explicit requirement.
- Avoid logging sensitive request/response bodies.

## Shell and filesystem safety

When editing shell scripts, CLI code, build scripts, filesystem utilities, or code that executes commands:

- Determine the intended shell before using shell-specific features.
- Quote variables and paths unless the script intentionally needs word splitting or globbing.
- Prefer arrays for command arguments in Bash and similar shells.
- Do not build shell commands from untrusted input.
- Avoid `eval` and dynamic execution.
- Validate and normalize user-controlled paths.
- Prevent path traversal and accidental writes outside intended directories.
- Treat filenames as arbitrary strings; handle spaces, newlines, leading dashes, and glob characters when practical.
- Use temporary files and directories safely.
- Do not delete, overwrite, or recursively change files without tight scoping and explicit user intent.
- Preserve exit codes and useful stderr when wrapping commands.
- Prefer documented project scripts over invented command lines.

## Testing

- Prefer focused unit tests for business rules.
- Use integration tests for wiring, persistence, serialization, framework behavior, CLI behavior, external process boundaries, and important cross-component flows.
- Integration tests must verify meaningful behavior, not only startup, object creation, or mock interactions.
- Test observable behavior, not implementation details.
- Prefer real value objects and simple fakes over deep mock chains.
- Use mocks only for stable collaborators, side-effect boundaries, or slow/external dependencies.
- Avoid verifying every internal call unless the interaction itself is the observable behavior.
- Keep fixtures small and readable.
- Test names should describe behavior.
- Keep test naming consistent with local style.
- Add regression tests for fixed bugs.
- Add boundary tests for validation, dates, numbers, state transitions, collection sizes, parsing, escaping, filesystem paths, and error handling when relevant.
- Add serialization/deserialization tests when changing DTOs, JSON annotations, event payloads, API contracts, config formats, or file formats.
- Add integration tests when query behavior, constraints, transactions, shell boundaries, or platform behavior matter.

## Security

When the change touches input, auth, files, SQL, serialization, HTML, shell, external calls, secrets, personal data, or sensitive data:

- Validate untrusted input at boundaries.
- Prefer allow-lists over block-lists.
- Use parameterized queries or the project's safe ORM/query APIs.
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
- Preserve backward compatibility for dashboards, alerts, scheduled jobs, operational scripts, and runbooks when relevant.

## Public contracts and compatibility

Treat these as public contracts unless proven otherwise:

- REST, GraphQL, gRPC, RPC, WebSocket, and webhook APIs;
- DTO fields and JSON names;
- event payloads;
- database schemas and migration order;
- configuration property names and meanings;
- environment variables;
- command-line flags and exit codes;
- scheduled job names and behavior;
- external file formats;
- error codes used by clients;
- security roles and permissions;
- package or module public APIs.

When contract changes are explicitly required:

- call out compatibility impact;
- preserve backward compatibility where practical;
- consider feature flags or additive changes;
- consider migration and rollback;
- update tests and documentation near the changed contract.
