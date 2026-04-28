# Product Engineering Baseline

Use this baseline when drafting `AGENTS.md` coding and testing guidance. Adapt it to repository evidence; do not copy it mechanically when local architecture, tooling, or explicit user instructions say otherwise.

## Principles

- **Repository-first.** Follow the repository's architecture, language/runtime version, style, tooling, tests, CI, and nearby code.
- **Simplicity.** Minimize accidental complexity: needless nesting, broad rewrites, accidental formatting, and speculative abstractions. Keep changes small and cohesive. Model essential domain complexity explicitly when it is real.
- **Functional core, imperative shell.** Keep business logic and data transformations pure where practical: prefer immutable value objects, avoid mutating input parameters without a clear reason, and return new values or explicit results. Keep side effects at boundaries such as persistence, network, filesystem, logging, UI state, and integration adapters.
- **Domain modeling.** Prefer explicit domain concepts over primitive obsession in business logic. Apply DDD in domain and application code: value objects should be immutable, while entities and aggregates may change internal state only through clearly named domain methods that preserve invariants. Do not force DDD patterns into simple scripts, UI glue, generated code, or thin infrastructure adapters.
- **Fail-fast.** Validate inputs at boundaries, reject invalid states early, and return actionable errors. Use fail-safe behavior only when resilience, user safety, compatibility, or graceful degradation is a product requirement.
- **Change hygiene.** Leave no junk behind: temporary files, drafts, debug output, experimental scripts, unused imports, dead code, commented-out old code, unused helpers, or TODOs without linked work. Review the final diff for accidental formatting, duplicate implementations, and weakened tests.
- **No careless duplication.** Do not duplicate an implementation when a suitable helper, abstraction, mapper, validator, parser, factory, fixture, or test utility already exists. Do not add a generic helper for one call site; abstractions should reduce real complexity.
- **Contract-first production code.** Do not change public APIs, wire formats, database schemas, events, CLI flags, configuration semantics, or integration behavior without an explicit requirement. If a contract changes, call out compatibility impact, migration needs, and rollback path.
- **Production readiness.** Consider security, privacy, observability, rollback, feature flags, migrations, idempotency, retries, timeouts, backoff, partial failures, ordering, and concurrency when relevant.
- **Dependencies.** Avoid new dependencies unless there is a strong reason. Prefer the standard library and libraries already used by the project; consider license, security, and maintenance status.

## Testing

- Add or update tests for changed behavior, regressions, and important contracts.
- Test observable behavior rather than implementation details.
- Cover happy paths, edge cases, invalid input, boundary values, empty/null cases where relevant, and concurrency, ordering, or idempotency when they matter.
- Use realistic inputs and small fixtures; generate large fixtures only when size itself is being tested.
- Prefer fakes/stubs over heavy mocks when they make behavior clearer.
- Never make tests pass by weakening assertions, skipping relevant checks, or hiding failures.

## Reference Principles

These rules are inspired by A Philosophy of Software Design, Refactoring, Domain-Driven Design, Google Engineering Practices, The Twelve-Factor App, OWASP Secure Coding Practices, SRE, and DORA. Keep references out of `AGENTS.md` unless they help the repository's contributors.
