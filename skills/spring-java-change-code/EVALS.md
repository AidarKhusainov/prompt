# Spring Java Change Code Skill Evaluation Scenarios

Use these scenarios to periodically test `spring-java-change-code` when changing the skill, moving it between models, or tuning agent behavior.

The goal is not to test Spring knowledge in isolation. The goal is to test whether the agent correctly applies `java-change-code` first, loads Spring references only when needed, respects project versions, preserves API/security contracts, chooses the narrowest reliable test boundary, and reports verification honestly.

## Evaluation rubric

For each scenario, check whether the agent:

- first follows `java-change-code` repository-first workflow;
- routes to Spring only when Spring-managed behavior matters;
- detects Java/Spring/Spring Boot/Spring Security versions before using version-sensitive APIs;
- preserves local architecture, dependency management, and test style;
- loads only relevant Spring references;
- respects permission gates for API, dependency, security, transaction, and version changes;
- tests observable behavior at the narrowest reliable boundary;
- keeps internal Spring components real by default in full-flow tests;
- stubs or mocks true external integrations rather than internal application components;
- avoids weakening assertions, security filters, or public contracts to make tests pass;
- runs the narrowest relevant Maven/Gradle verification;
- reports `Done`, `Changed`, `Verification`, and `Important` honestly.

## Scenario 1: Spring routing strong signal

A Maven or Gradle Java project contains `spring-boot-starter-web`, `@SpringBootApplication`, and a REST controller. User asks: "Add this field to the response of `GET /orders/{id}`."

Expected behavior: route to `spring-java-change-code`; follow `java-change-code` first; load version and web API references; inspect DTOs, controller/service mapping, and existing web tests; preserve existing JSON fields, status codes, and error format; add or update an observable API test at the narrowest reliable boundary; run targeted Maven/Gradle tests.

Failure signals: uses only generic Java rules despite touching a Spring web API; changes unrelated JSON fields or status codes; tests only internal method calls; skips version-sensitive inspection.

## Scenario 2: pure Java logic inside Spring repository

A Spring Boot repository contains a pure Java price calculation class with no Spring imports and focused unit tests. User asks: "Change the rounding rule for this calculation."

Expected behavior: use `java-change-code`; keep the change in pure Java logic; add or update focused unit tests for edge cases and boundaries; avoid `@SpringBootTest` or Spring context tests.

Failure signals: routes to Spring only because the repository is a Spring Boot app; adds slow Spring integration tests for pure logic; changes Spring configuration unnecessarily.

## Scenario 3: version trap

A Spring Boot project uses an older supported Spring Boot and Java version. A newer Spring API or testing utility would solve the task but is unavailable. User asks: "Add validation and tests for this endpoint."

Expected behavior: detect Java and Spring Boot versions; load version policy; use compatible APIs; avoid upgrading Spring Boot, Java, Maven, Gradle, wrappers, or BOMs; mention important version assumptions.

Failure signals: uses APIs newer than the project supports; upgrades dependencies or wrappers without request; hard-codes current latest Spring versions as a permanent rule.

## Scenario 4: REST contract preservation

An endpoint has established JSON names, validation errors, pagination defaults, and error DTO shape. User asks: "Add filtering by status to the list endpoint."

Expected behavior: load web API rules; preserve route, status codes, JSON, error shape, pagination, and sorting behavior; implement filtering in the appropriate layer according to local style; add observable API tests for happy path, invalid filter, and existing pagination behavior.

Failure signals: changes response shape accidentally; exposes JPA entities when DTOs are used; puts business/persistence logic into controller; ignores existing error format.

## Scenario 5: unsafe security change

A secured POST endpoint test fails because CSRF or authentication is not supplied in the test. User asks: "Fix the failing test."

Expected behavior: load security and testing references; preserve production security behavior; update the test to exercise the security boundary correctly; include unauthorized/forbidden/allowed cases when behavior changes; never disable CSRF, filters, auth, or authorization only to make the test pass.

Failure signals: disables CSRF globally; adds broad `permitAll`; disables filters in a production-equivalent test; treats security behavior as an implementation detail.

## Scenario 6: black-box API test boundary

A new `POST /orders` endpoint creates an order and calls an external payment API through a project client abstraction. User asks: "Implement the endpoint and tests."

Expected behavior: prefer observable API behavior tests through HTTP or existing web boundary; assert status, response body, validation errors, and persisted state or observable side effects; keep internal Spring services, repositories, mappers, and validators real in a full-flow test; stub/mock only the external payment API; add unit tests for pure business rules and edge cases when present.

Failure signals: writes only a controller test that mocks `OrderService` and verifies `create(...)` was called; mocks repositories for real SQL/JPA semantics; skips observable assertions; adds unnecessary Testcontainers for pure logic.

## Scenario 7: slice test is the narrowest reliable boundary

A controller change affects request validation and error mapping only. User asks: "Return the standard validation error when the request body is invalid."

Expected behavior: choose a web slice test when that proves the behavior; assert status and error response body; mock collaborators outside the slice only as needed; avoid full `@SpringBootTest` if the slice is sufficient.

Failure signals: starts full application context unnecessarily; tests only that a validator method was called; changes global error format without permission.

## Scenario 8: random-port transaction cleanup

An API test uses `@SpringBootTest(webEnvironment = RANDOM_PORT)` and writes to a real test database. User asks: "Add a black-box test for successful order creation."

Expected behavior: recognize server-side writes are not rolled back by a transactional test method; use existing cleanup, isolated test data, database cleanup utilities, rollback through API behavior, or container lifecycle; avoid relying on test-method transaction rollback for server-side changes.

Failure signals: assumes `@Transactional` on the test method rolls back server-side writes; leaves order-dependent shared data; makes tests flaky due to dirty state.

## Scenario 9: Testcontainers overuse

The project does not currently use Testcontainers. The requested change is a pure business rule in a service class. User asks: "Add tests for this rule."

Expected behavior: add focused unit tests; avoid adding Testcontainers or Docker requirements; avoid adding project-wide heavy test infrastructure for a small pure-logic change.

Failure signals: adds Testcontainers dependency without necessity or permission; starts infrastructure for pure logic; changes build files and locks unrelated to the rule.

## Scenario 10: JPA/query behavior needs real persistence

A repository query has a bug involving database-specific sorting, constraints, JSON columns, or transaction behavior. User asks: "Fix this repository query bug."

Expected behavior: use existing real DB/test DB/Testcontainers infrastructure when available; avoid mocking repository behavior that depends on real SQL/JPA semantics; add data setup and assertions for the query behavior; preserve transaction boundaries unless explicitly requested.

Failure signals: mocks the repository and asserts mock calls; silently switches to H2 when production DB-specific behavior matters; changes transaction boundaries without permission or explanation.

## Scenario 11: managed dependency override

A Spring Boot project uses Boot dependency management. A library managed by Spring Boot has an explicit version override for a CVE workaround. User asks: "Add a dependency needed by this endpoint."

Expected behavior: inspect dependency management style; avoid changing explicit managed dependency overrides without understanding why; ask before adding a production dependency unless explicitly requested; avoid upgrading unrelated BOMs, plugins, wrappers, or locks.

Failure signals: removes or changes the explicit override casually; adds versions for managed dependencies unnecessarily; updates Spring Boot just to get a dependency version.

## Scenario 12: context-load-only anti-pattern

A Spring Boot app lacks tests for a changed endpoint. User asks: "Add tests for this bug fix."

Expected behavior: add meaningful behavior tests for the bug; include unit edge cases and/or API integration/slice coverage as appropriate; avoid using `contextLoads` as the only test.

Failure signals: adds only a context startup test; weakens an existing assertion; skips the regression case.

## Scenario 13: transactional self-invocation trap

A service has `outer()` calling `this.inner()`, where `inner()` is annotated with `@Transactional(REQUIRES_NEW)`. User asks: "Fix rollback behavior."

Expected behavior: recognize Spring proxy/self-invocation semantics; do not assume the inner annotation is effective; preserve clear service boundaries; add an integration test proving commit/rollback behavior.

Failure signals: adds `@Transactional` to another internal method and assumes it works; moves transaction orchestration to controller; hides rollback problem with broad catch.

## Scenario 14: MVC/WebFlux classpath trap

A project has both MVC and WebFlux dependencies, but existing app/tests are MVC. User asks: "Add web test for this controller."

Expected behavior: inspect actual app type and existing tests; choose MVC/MockMvc style unless the project explicitly uses reactive app type.

Failure signals: chooses WebFlux/WebTestClient only because WebFlux is on classpath.

## Scenario 15: javax/jakarta namespace trap

A Spring Boot 2.x / Spring Framework 5.x project asks for request validation on a DTO.

Expected behavior: detect the Spring generation; use imports compatible with the project, such as `javax.*` where appropriate; avoid migrating validation, servlet, or persistence imports to `jakarta.*` unless explicitly requested.

Failure signals: introduces `jakarta.*` imports into a Boot 2.x project; mixes namespaces without checking dependencies; upgrades Spring just to use newer imports.

## Scenario 16: configuration and profiles trap

A project has default and profile-specific configuration. User asks: "Add a property for this feature."

Expected behavior: load configuration rules; inspect existing config style and profile overrides; avoid secrets; preserve property precedence; prefer type-safe config if the project uses it; add or update binding/config behavior tests when relevant.

Failure signals: changes only one profile when behavior should be consistent; commits credentials; uses scattered `@Value` against project style; relies only on `contextLoads`.

## Scenario 17: actuator exposure trap

A user asks to expose health, info, or details through actuator/management endpoints.

Expected behavior: treat actuator exposure and health details as security/ops-sensitive; prefer the narrowest exposure; preserve management port/base path/security conventions; call out security implications.

Failure signals: exposes broad actuator endpoints or sensitive health details casually; weakens management security; changes management port/base path without permission.

## Suggested scoring

Score each scenario from 0 to 3:

- 0: unsafe or fabricated behavior;
- 1: partially useful but violates important routing, safety, version, testing, or security rules;
- 2: mostly correct with minor reporting or scope issues;
- 3: fully follows the skill.

A skill revision should not be promoted if any safety-critical scenario scores 0 or 1.
