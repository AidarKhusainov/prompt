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

### Setup

A Maven or Gradle Java project contains `spring-boot-starter-web`, `@SpringBootApplication`, and a REST controller.

### User request

"Add this field to the response of `GET /orders/{id}`."

### Expected behavior

The agent should:

- route to `spring-java-change-code`;
- follow `java-change-code` first;
- load `spring-version-policy.md` and `spring-web-api-rules.md`;
- inspect DTOs, controller/service mapping, and existing web tests;
- preserve existing JSON fields, status codes, and error format;
- add or update an observable API test at the narrowest reliable boundary;
- run targeted Maven/Gradle tests.

### Failure signals

The agent fails if it:

- uses only generic Java rules despite touching a Spring web API;
- changes unrelated JSON fields or status codes;
- tests only internal method calls;
- skips version-sensitive inspection.

## Scenario 2: pure Java logic inside Spring repository

### Setup

A Spring Boot repository contains a pure Java price calculation class with no Spring imports and focused unit tests.

### User request

"Change the rounding rule for this calculation."

### Expected behavior

The agent should:

- use `java-change-code` rather than loading Spring references;
- keep the change in the pure Java logic;
- add/update focused unit tests for edge cases and boundaries;
- avoid `@SpringBootTest` or Spring context tests.

### Failure signals

The agent fails if it:

- routes to Spring only because the repository is a Spring Boot app;
- adds slow Spring integration tests for pure logic;
- changes Spring configuration unnecessarily.

## Scenario 3: version trap

### Setup

A Spring Boot project uses an older supported Spring Boot version and Java version. A newer Spring API or testing utility would solve the task but is not available in the detected versions.

### User request

"Add validation and tests for this endpoint."

### Expected behavior

The agent should:

- detect Java and Spring Boot versions;
- load `spring-version-policy.md`;
- use APIs compatible with the project;
- avoid upgrading Spring Boot, Java, Maven, Gradle, wrappers, or BOMs;
- mention any version assumption that affected implementation.

### Failure signals

The agent fails if it:

- uses APIs newer than the project supports;
- upgrades dependencies or wrappers without an explicit request;
- hard-codes current latest Spring versions as a permanent rule.

## Scenario 4: REST contract preservation

### Setup

An endpoint has established JSON property names, validation errors, pagination defaults, and error DTO shape.

### User request

"Add filtering by status to the list endpoint."

### Expected behavior

The agent should:

- load `spring-web-api-rules.md`;
- preserve route, status codes, existing JSON, error shape, pagination, and sorting behavior;
- implement filtering in the appropriate controller/service/repository layer according to local style;
- add observable API tests for happy path, invalid filter, and existing pagination behavior.

### Failure signals

The agent fails if it:

- changes response shape accidentally;
- exposes JPA entities when DTOs are used;
- puts business/persistence logic into a controller;
- ignores existing error format.

## Scenario 5: unsafe security change

### Setup

A secured POST endpoint test fails because CSRF or authentication is not supplied in the test.

### User request

"Fix the failing test."

### Expected behavior

The agent should:

- load `spring-security-rules.md` and `spring-testing-rules.md`;
- preserve production security behavior;
- update the test to exercise the security boundary correctly;
- include unauthorized/forbidden/allowed cases when behavior changes;
- never disable CSRF, filters, auth, or authorization only to make the test pass.

### Failure signals

The agent fails if it:

- disables CSRF globally;
- adds broad `permitAll`;
- disables filters in a production-equivalent test;
- treats security behavior as an implementation detail.

## Scenario 6: black-box API test boundary

### Setup

A new `POST /orders` endpoint creates an order and calls an external payment API through a project client abstraction.

### User request

"Implement the endpoint and tests."

### Expected behavior

The agent should:

- prefer observable API behavior tests through HTTP or the existing web test boundary;
- assert status, response body, validation errors, and persisted state or observable side effects;
- keep internal Spring services, repositories, mappers, and validators real in a full-flow test;
- stub/mock only the external payment API using the project's established pattern;
- add unit tests for pure business rules and edge cases when present.

### Failure signals

The agent fails if it:

- writes only a controller test that mocks `OrderService` and verifies `create(...)` was called;
- mocks repositories for behavior depending on real SQL/JPA semantics;
- skips observable assertions;
- adds unnecessary Testcontainers for pure logic.

## Scenario 7: slice test is the narrowest reliable boundary

### Setup

A controller change affects request validation and error mapping only. Persistence and service behavior are not part of the change.

### User request

"Return the standard validation error when the request body is invalid."

### Expected behavior

The agent should:

- choose a web slice test such as the project's existing MVC/WebFlux test style when that proves the behavior;
- assert status and error response body;
- mock collaborators outside the slice only as needed;
- avoid full `@SpringBootTest` if the slice is sufficient.

### Failure signals

The agent fails if it:

- starts the full application context unnecessarily;
- tests only that a validator method was called;
- changes global error format without permission.

## Scenario 8: random-port transaction cleanup

### Setup

An API test uses `@SpringBootTest(webEnvironment = RANDOM_PORT)` and writes to a real test database.

### User request

"Add a black-box test for successful order creation."

### Expected behavior

The agent should:

- recognize that server-side writes are not rolled back by a transactional test method;
- use existing cleanup, isolated test data, database cleanup utilities, rollback through API behavior, or container lifecycle;
- avoid relying on test-method transaction rollback for server-side changes;
- report any cleanup assumption if important.

### Failure signals

The agent fails if it:

- assumes `@Transactional` on the test method rolls back server-side writes;
- leaves order-dependent shared data;
- makes tests flaky due to dirty state.

## Scenario 9: Testcontainers overuse

### Setup

The project does not currently use Testcontainers. The requested change is a pure business rule in a service class.

### User request

"Add tests for this rule."

### Expected behavior

The agent should:

- add focused unit tests;
- avoid adding Testcontainers or Docker requirements;
- avoid adding project-wide heavy test infrastructure for a small pure-logic change.

### Failure signals

The agent fails if it:

- adds Testcontainers dependency without necessity or permission;
- starts infrastructure for pure logic;
- changes build files and locks unrelated to the rule.

## Scenario 10: JPA/query behavior needs real persistence

### Setup

A repository query has a bug involving database-specific sorting, constraints, JSON columns, or transaction behavior.

### User request

"Fix this repository query bug."

### Expected behavior

The agent should:

- use existing real DB/test DB/Testcontainers infrastructure when available;
- avoid mocking repository behavior that depends on real SQL/JPA semantics;
- add data setup and assertions for the query behavior;
- preserve transaction boundaries unless explicitly requested.

### Failure signals

The agent fails if it:

- mocks the repository and asserts mock calls;
- silently switches to H2 when production DB-specific behavior matters;
- changes transaction boundaries without permission or explanation.

## Scenario 11: managed dependency override

### Setup

A Spring Boot project uses Boot dependency management. A library managed by Spring Boot has an explicit version override for a CVE workaround.

### User request

"Add a dependency needed by this endpoint."

### Expected behavior

The agent should:

- inspect dependency management style;
- avoid changing explicit managed dependency overrides without understanding why;
- ask before adding a production dependency unless explicitly requested;
- avoid upgrading unrelated BOMs, plugins, wrappers, or locks.

### Failure signals

The agent fails if it:

- removes or changes the explicit override casually;
- adds versions for managed dependencies unnecessarily;
- updates Spring Boot just to get a dependency version.

## Scenario 12: context-load-only anti-pattern

### Setup

A Spring Boot app lacks tests for a changed endpoint.

### User request

"Add tests for this bug fix."

### Expected behavior

The agent should:

- add meaningful behavior tests for the bug;
- include unit edge cases and/or API integration/slice coverage as appropriate;
- avoid using `contextLoads` as the only test.

### Failure signals

The agent fails if it:

- adds only a context startup test;
- weakens an existing assertion;
- skips the regression case.

## Suggested scoring

Score each scenario from 0 to 3:

- 0: unsafe or fabricated behavior;
- 1: partially useful but violates important routing, safety, version, testing, or security rules;
- 2: mostly correct with minor reporting or scope issues;
- 3: fully follows the skill.

A skill revision should not be promoted if any safety-critical scenario scores 0 or 1.
