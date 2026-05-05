# Spring Security Rules

Use this reference before editing authentication, authorization, CSRF, CORS, sessions, token handling, password handling, method security, tenant isolation, security headers, actuator exposure, security filter chains, or tests for secured behavior.

## Security-impacting changes are gated

Treat these as permission-gated changes unless the user explicitly requested them:

- authentication flows;
- authorization rules;
- `SecurityFilterChain` configuration;
- `permitAll`, `authenticated`, role, authority, matcher, or method-security changes;
- CSRF configuration;
- CORS configuration;
- session management;
- remember-me configuration;
- OAuth2/OIDC/resource-server configuration;
- JWT or opaque-token handling;
- password storage and encoders;
- tenant isolation;
- security headers;
- actuator endpoint exposure;
- security test configuration that changes production-equivalent behavior.

If the user did not explicitly request the security-impacting change, stop before editing that behavior, explain the risk, and propose a safer alternative.

## Never weaken security to make code or tests pass

Never disable CSRF, CORS, authentication, authorization, method security, security headers, or security filters only to make tests pass.

Do not broaden `permitAll` or path matchers as an incidental fix.

Do not replace production-like security behavior with `@WithMockUser`, disabled filters, or test-only shortcuts unless the test is explicitly not about security and the project already uses that pattern safely.

## Authorization

Preserve existing authorization semantics unless explicitly requested.

Be careful with:

- matcher ordering;
- path pattern changes;
- HTTP method-specific access rules;
- default deny vs default allow behavior;
- role prefix conventions;
- authorities vs roles;
- method security annotations;
- ownership checks;
- tenant isolation;
- admin vs user flows.

For secured endpoints whose behavior changes, include unauthorized, forbidden, and allowed cases when practical.

## CSRF and browser-facing endpoints

Do not disable CSRF globally without an explicit security requirement.

For unsafe HTTP methods, tests should account for CSRF requirements when the application uses browser/session-based security.

For stateless APIs, follow the project's existing CSRF and token strategy. Do not infer statelessness from a single endpoint.

## CORS

Do not add broad CORS such as wildcard origins, wildcard methods, or credentials with permissive origins unless explicitly required and safe.

Prefer existing central CORS configuration. Avoid scattering CORS annotations across controllers unless the project already uses that style.

## Tokens, sessions, and secrets

Do not log or expose:

- `Authorization` headers;
- cookies;
- refresh tokens;
- access tokens;
- session IDs;
- password hashes;
- API keys;
- private keys;
- OAuth/OIDC claims containing sensitive user data.

Do not parse JWTs manually when the project already uses Spring Security resource-server support or another established library.

Do not change token validation, issuer, audience, clock skew, or key material handling without explicit scope.

## Passwords

Do not store plaintext passwords.

Do not introduce reversible encryption for passwords.

Use the project's existing `PasswordEncoder` strategy. If adding password handling, prefer Spring Security password encoding patterns compatible with the project's version.

Do not log passwords, password reset tokens, or password validation details.

## Actuator and management endpoints

Treat actuator exposure changes as security-sensitive.

Do not expose management endpoints broadly or include sensitive health/details output unless explicitly required and reviewed.

Preserve existing management port, base path, exposure include/exclude, and health details settings unless the task requires changing them.

## Security testing

Security behavior must be tested through the security boundary.

For secured endpoints, prefer tests that assert externally observable security outcomes:

- unauthenticated request is rejected appropriately;
- authenticated but unauthorized request is forbidden appropriately;
- authorized request succeeds;
- CSRF behavior is respected when relevant;
- tenant or ownership isolation is enforced when relevant.

Do not consider a controller test sufficient if security filters are disabled and the change affects security behavior.

## Self-review

Before finishing security-related changes, check:

- no rule was broadened accidentally;
- matcher ordering remains safe;
- default access behavior is still intentional;
- no security filters were disabled in production-equivalent paths;
- no sensitive values are logged or returned;
- tests cover the changed security behavior;
- the final response calls out any security assumptions or limitations.
