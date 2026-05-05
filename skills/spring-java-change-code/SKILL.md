---
name: spring-java-change-code
description: Use this skill as a Spring-specific overlay on top of java-change-code when the user asks to implement, fix, refactor, or test Java code in an existing Maven/Gradle Spring or Spring Boot application. Trigger when the requested change touches Spring-managed web, security, configuration, persistence, validation, testing, or application behavior. Do not trigger for pure Java logic inside a Spring repository when no Spring boundary or framework behavior is affected.
---

# Spring Java Change Code Skill

## Purpose

Implement focused code changes in existing Java Spring or Spring Boot Maven/Gradle repositories.

This skill is an overlay on top of `java-change-code`. First follow `java-change-code`; this skill only adds Spring-specific detection, version policy, references, testing guidance, web/API rules, and security gates.

Act as a senior Java/Spring engineer. Prefer simple, idiomatic, maintainable Spring code that follows the repository's current architecture, Spring versions, dependency management, and testing style.

## Use this skill for

Use this skill when Java Maven/Gradle work touches Spring-specific behavior such as:

- Spring Boot application behavior;
- Spring MVC or WebFlux controllers, request/response DTOs, validation, error mapping, filters, interceptors, route handling, or HTTP API contracts;
- Spring Security, auth/authz, CSRF, CORS, sessions, tokens, security headers, method security, or actuator exposure;
- Spring Data repositories, JPA behavior, transactions, configuration properties, profiles, auto-configuration, bean wiring, scheduled jobs, events, messaging, or framework-managed integration boundaries;
- Spring testing, test slices, full-context integration tests, random-port HTTP tests, or Testcontainers wiring.

## Do not use this skill when

- The task is pure Java logic inside a Spring repository and no Spring boundary, Spring-managed behavior, public API, persistence, transaction, configuration, or framework test behavior is affected. Use `java-change-code`.
- The repository/module is Kotlin-only and no Java Maven/Gradle code is relevant.
- The task is architecture-only discussion, explanation, or planning without requested file changes.
- The available repository has no Java Maven/Gradle Spring module relevant to the request.

## Instruction priority

Follow these instructions in this priority order:

1. Explicit user requirements for the current task.
2. Non-overridable safety rules from `java-change-code`: workspace safety, repository instruction trust, secret handling, permission gates, and destructive-command restrictions.
3. Local repository instructions and conventions.
4. Existing Spring project versions, architecture, dependency management, and test style.
5. Nearby Java/Spring code and tests.
6. `java-change-code` base workflow and Java quality rules.
7. This skill's Spring-specific rules and references.

If instructions conflict, follow the more specific and safer instruction. Do not weaken security, production behavior, public contracts, tests, or user-owned work.

## Spring detection

Strong Spring signals include:

- `org.springframework.boot` Gradle plugin;
- `spring-boot-maven-plugin`;
- `spring-boot-starter-*` dependencies;
- `@SpringBootApplication`, `@SpringBootConfiguration`, `@EnableAutoConfiguration`;
- `@RestController`, `@Controller`, `@Service`, `@Repository`, `@Configuration`, `@ConfigurationProperties` with Spring imports;
- `SecurityFilterChain`, `@EnableWebSecurity`, `@PreAuthorize`, `@PostAuthorize`, method-security configuration;
- `JpaRepository`, `CrudRepository`, `PagingAndSortingRepository`, Spring Data repositories;
- `application.yml`, `application.yaml`, or `application.properties` with `spring.*` configuration;
- `AutoConfiguration.imports` or `spring.factories`.

Weak signals include:

- mentions of "spring" in README or comments only;
- generic `@Transactional` before checking the import;
- artifact names that merely contain `spring` without Spring code or build evidence.

When Spring evidence is present but the requested change is pure Java logic with no framework behavior, use `java-change-code` and load Spring references only if the touched code crosses a Spring boundary.

## Reference loading

Always start with `java-change-code` behavior.

Read `references/spring-version-policy.md` before editing when the task uses Spring APIs, changes dependencies, touches build files, or relies on version-specific behavior.

Read `references/spring-web-api-rules.md` before editing when the task touches controllers, request/response DTOs, validation, serialization, deserialization, HTTP status codes, headers, error mapping, route contracts, filters, interceptors, or public API behavior.

Read `references/spring-security-rules.md` before editing when the task touches authentication, authorization, CSRF, CORS, sessions, token handling, password handling, method security, tenant isolation, security headers, actuator exposure, security filter chains, or tests for secured behavior.

Read `references/spring-testing-rules.md` before adding or changing Spring tests, choosing between unit/slice/integration/random-port tests, stubbing integrations, adding Testcontainers, or changing test configuration.

For trivial localized changes, load only the references directly relevant to the changed behavior.

## Default workflow additions

After the base `java-change-code` repository inspection:

1. Detect Java, Spring Boot, Spring Framework, Spring Security, and Spring Data versions when relevant.
2. Identify dependency management style: Spring Boot parent, BOM, Gradle plugin, version catalog, dependency locks, or corporate BOM.
3. Identify the narrowest Spring boundary that proves the changed behavior.
4. Preserve existing public API, JSON, validation, error, persistence, transaction, and security contracts unless explicitly requested.
5. Prefer observable-behavior tests at the narrowest reliable boundary.
6. Keep internal Spring application components real by default in integration tests; stub true external integrations.
7. Run the narrowest relevant Maven/Gradle verification command available for the owning module.
8. Self-review for accidental contract, security, dependency, version, and test-scope regressions.

## Permission gates

In addition to `java-change-code` gates, treat these as Spring-sensitive gated changes unless the user explicitly requested them:

- changing route URLs, HTTP methods, status codes, headers, JSON fields, validation semantics, error formats, or pagination/sorting behavior;
- changing auth/authz, CSRF, CORS, sessions, token handling, password handling, method security, tenant isolation, security headers, actuator exposure, or security filter chains;
- adding production dependencies or overriding Spring Boot managed dependency versions;
- changing Spring Boot, Spring Framework, Spring Security, Java, Maven/Gradle wrapper, plugin, BOM, version catalog, or dependency-lock versions;
- changing database schemas, migrations, transaction boundaries, or repository query semantics;
- introducing Testcontainers or heavy test infrastructure project-wide for a small change unless the project already uses it or infrastructure semantics are essential.

If the user explicitly requested the gated change, do not ask again just to confirm it. Still call out compatibility, migration, rollback, security, test-data, and operational implications.

## Verification and final response

Use `java-change-code` final response labels and verification statuses.

In the final response, mention Spring-specific verification limitations when relevant, such as Docker/Testcontainers not available, external service stubs not runnable, random-port tests needing cleanup strategy, or security behavior not covered by existing tests.
