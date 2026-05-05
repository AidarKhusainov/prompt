# Spring Web API Rules

Use this reference before editing Spring MVC/WebFlux controllers, request/response DTOs, validation, serialization, HTTP status codes, headers, error mapping, filters, interceptors, or public API behavior.

## Preserve public contracts

Do not accidentally change public API behavior.

Preserve existing:

- route paths and HTTP methods;
- request and response DTO fields;
- JSON property names and formats;
- HTTP status codes;
- headers;
- validation semantics and validation messages when they are part of the contract;
- error response shape and error codes;
- pagination, sorting, filtering, and default limits;
- content types;
- backwards compatibility for clients.

Changing a public contract is a permission-gated change unless the user explicitly requested that exact contract change.

## Controllers and boundaries

Keep controllers thin.

Controllers should usually handle:

- request mapping;
- authentication principal extraction when needed;
- input validation boundary;
- request-to-command/query mapping;
- response mapping;
- status codes and headers.

Avoid putting business rules, persistence logic, transaction orchestration, external integration details, or large conditionals directly in controllers when the project has service/application/domain layers.

Follow the repository's current architecture: package-by-feature, layered, hexagonal, clean architecture, or a simpler local convention. Do not introduce a new architecture for a small endpoint change.

## DTOs and serialization

Prefer explicit request/response DTOs for external APIs when the project already uses DTOs.

Do not return JPA entities directly from controllers if the project uses DTOs or if entity exposure would leak persistence details, lazy-loaded relationships, internal fields, or sensitive data.

Be careful with:

- `@JsonProperty`, `@JsonFormat`, `@JsonIgnore`, `@JsonInclude`;
- enum serialization;
- date/time/timezone handling;
- null vs empty collection semantics;
- backward-compatible field additions;
- validation groups;
- records vs classes based on project Java version and style.

## Validation

Validate external input at the boundary using the project's existing style.

Common patterns:

- Bean Validation annotations on request DTOs;
- `@Valid` or `@Validated` on controller parameters;
- custom validators when declarative validation is not expressive enough;
- service-layer validation for business invariants that are not transport-specific.

Do not rely only on database constraints or downstream exceptions for user-facing validation.

Do not expose raw validation internals if the project has a standard error format.

## Error handling

Prefer the existing error handling style:

- `@ControllerAdvice`;
- `ProblemDetail`;
- custom error DTOs;
- project-specific exception mappers;
- framework defaults only when the project already uses them intentionally.

Do not leak:

- stack traces;
- SQL;
- table or column names;
- internal class names;
- raw exception messages containing sensitive details;
- tokens, credentials, session identifiers, PII, or secrets.

Preserve useful root causes in logs or exception chains when wrapping errors.

## HTTP semantics

Use status codes deliberately and consistently with existing endpoints.

Avoid changing semantics such as:

- `200` vs `201` vs `204`;
- `400` vs `422` when the project distinguishes them;
- `401` vs `403`;
- `404` vs empty result;
- idempotency behavior for PUT/PATCH/DELETE;
- retryable vs non-retryable errors.

For list endpoints, consider existing conventions for pagination, sorting, filtering, maximum limits, and deterministic ordering.

## Security and privacy at the web boundary

Do not log full request bodies, authorization headers, cookies, tokens, passwords, API keys, or PII.

If adding logs for API behavior, log stable identifiers and high-level outcomes only, following the project's logging style.

Do not add permissive CORS, disabled CSRF, broad `permitAll`, or disabled security filters as part of a web change. Load `spring-security-rules.md` for security-impacting work.

## Web API tests

For API behavior, prefer tests that assert externally observable behavior through the narrowest reliable boundary:

- status codes;
- headers;
- response body;
- validation and error format;
- security outcomes;
- persisted state or emitted side effects when relevant.

Avoid tests that only verify a controller called an internal service method when observable API behavior can be asserted.
