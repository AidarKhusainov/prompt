# Spring Version Policy

Use this reference before editing Spring Java code when the task uses Spring APIs, changes dependencies, touches build files, or relies on version-specific behavior.

## Core rule

Existing project versions always win.

Never assume that current latest Spring, Java, Maven, Gradle, or plugin versions are appropriate for an existing repository.

Current Spring Boot stable information is lookup-time context, not a permanent skill rule. Never encode a specific `latest` version as a lasting recommendation.

## Authoritative sources

For Spring API behavior, version compatibility, testing support, dependency management, and security defaults, prefer official versioned documentation on `docs.spring.io` that matches the project's detected version.

Use OWASP guidance as a supplemental source for general security practices, threat modeling, and secure design principles.

Do not let blog posts, StackOverflow answers, tutorials, generated examples, or outdated snippets override project versions, official Spring documentation, local repository conventions, or security gates.

When official documentation and common examples differ, follow the project version and official docs first.

## Detect versions first

Before using Spring APIs or changing dependencies, inspect relevant project files for:

- Java version: toolchains, compiler plugins, source/target compatibility, `.java-version`, `.sdkmanrc`, CI images, Dockerfiles, and README guidance;
- Spring Boot version: parent POM, BOM, Gradle plugin, version catalog, dependency management plugin, or corporate BOM;
- Spring Framework, Spring Security, Spring Data, Spring Cloud, and Spring AI versions when directly relevant;
- Maven/Gradle wrapper versions and build plugin versions;
- dependency locks, version catalogs, Renovate/Dependabot rules, platform BOMs, and corporate constraints.

Use APIs compatible with the detected project versions.

## Existing projects

For existing projects:

- Do not upgrade Java, Spring Boot, Spring Framework, Spring Security, Spring Data, Spring Cloud, Maven, Gradle, wrappers, plugins, BOMs, version catalogs, or dependency locks unless directly requested.
- Do not replace the repository's dependency management style.
- Do not add explicit versions for Spring Boot managed dependencies unless the project already requires an override and the reason is understood.
- If a dependency version is explicitly declared for an artifact managed by Spring Boot, treat it as a deliberate override and do not change it without understanding why.
- Check the project Java version before using newer language features.
- Check Spring major-version compatibility before using newer annotations, testing utilities, HTTP clients, security DSL APIs, or problem-detail features.

## New projects or missing versions

Only for new projects or repositories where versions are genuinely absent:

- Determine the current Spring Boot stable baseline from official Spring Boot documentation at lookup time.
- Prefer currently supported Java LTS choices that match Spring's documented support and project deployment constraints.
- Document the assumption in the final response if it materially affects implementation or verification.

## Dependency management

Respect the repository's existing style: Maven Spring Boot parent, imported BOM, Gradle Spring Boot plugin, dependency-management plugin, native BOM support, version catalogs, dependency locking, or corporate platform BOMs.

When adding dependencies:

1. Prefer existing dependencies and framework-provided starters first.
2. Avoid production dependencies for small helpers that are clearer with standard library or existing project utilities.
3. Ask before adding production dependencies unless the user explicitly requested the dependency addition.
4. Do not upgrade unrelated dependencies or plugins.
5. Explain why a new dependency is necessary, what alternatives were considered, and whether it is managed by the existing BOM.

## Version-sensitive self-review

Before finishing, check:

- the code compiles against the detected Java and Spring versions;
- no newer Spring APIs were introduced accidentally;
- no managed dependency version was overridden accidentally;
- no wrapper, plugin, BOM, version catalog, or lockfile changed unless directly required;
- tests use annotations and utilities available in the project's Spring Boot version;
- final response reports any version assumptions.
