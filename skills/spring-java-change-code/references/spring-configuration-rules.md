# Spring Configuration Rules

Use this reference before editing application configuration, profiles, `@Configuration`, `@ConfigurationProperties`, conditional beans, auto-configuration, actuator exposure, management endpoints, or configuration values.

## Configuration is production behavior

Treat configuration as application behavior, not as incidental text.

Before changing configuration, inspect the project's existing style:

- `application.yml`, `application.yaml`, `application.properties`;
- profile-specific files such as `application-dev.yml` or `application-test.properties`;
- environment-variable conventions;
- config import usage;
- Docker, Helm, Compose, CI, deployment, or README guidance;
- tests that bind or override properties.

Do not change defaults, profile behavior, management exposure, or environment-variable names unless the task requires it.

## Secrets and sensitive values

Never commit secrets, tokens, passwords, credentials, private keys, connection strings with credentials, or production service endpoints.

If configuration is relevant, inspect variable names, placeholders, templates, sanitized examples, or documentation rather than secret values.

Prefer placeholders and documented required environment variables over hardcoded sensitive values.

Do not log configuration values that may contain secrets or PII.

## Property precedence and profiles

Consider property source precedence and profile overrides before changing a value.

When adding or changing a property, check whether the same key appears in:

- default application config;
- profile-specific config;
- test config;
- environment variables;
- command-line or deployment config;
- config imports;
- local documentation.

Do not update only one profile when the behavior must stay consistent across profiles.

Do not accidentally change tests or local development behavior by modifying shared defaults.

## Type-safe configuration

Prefer the project's existing configuration style.

If the project uses type-safe configuration, prefer `@ConfigurationProperties` and validation over scattered `@Value` usage.

If the project already uses `@Value`, environment access, or custom config classes consistently, follow the local style for small changes.

When adding `@ConfigurationProperties`, consider:

- prefix naming consistency;
- validation annotations compatible with the project's Spring generation;
- constructor binding vs mutable binding according to project version and style;
- tests for binding and validation when behavior depends on configuration.

## Conditional beans and auto-configuration

Be careful with conditional configuration:

- `@ConditionalOnProperty`;
- `@ConditionalOnClass`;
- `@ConditionalOnMissingBean`;
- `@Profile`;
- auto-configuration imports;
- bean ordering and primary beans.

Do not make a bean conditional in a way that silently disables production behavior.

For starter/auto-configuration style code, preserve backoff behavior and local override hooks.

## Actuator and management endpoints

Treat actuator and management endpoint changes as security/ops-sensitive.

Do not expose management endpoints casually. Management endpoints can contain sensitive information and should be secured according to project policy.

Changes to endpoint exposure, health details, base path, management port, CORS, probes, or security integration are permission-gated unless explicitly requested.

Preserve existing:

- `management.endpoints.web.exposure.include` and `exclude`;
- health details visibility;
- management base path and port;
- liveness/readiness probe behavior;
- security rules for management endpoints.

If the task asks to expose actuator data, prefer the narrowest endpoint exposure that satisfies the requirement and call out security implications.

## Testing configuration changes

Add or update tests when configuration changes affect behavior.

Use the narrowest reliable test boundary:

- configuration properties binding/validation test;
- application context runner or project-specific config test;
- slice/integration test for conditional beans;
- API/integration test when behavior changes externally.

Do not rely only on `contextLoads` for configuration behavior.

## Self-review

Before finishing, check that:

- no secrets or sensitive values were added;
- profile overrides and property precedence were considered;
- property names and prefixes follow project conventions;
- configuration changes are compatible with detected Spring Boot/Spring Framework versions;
- actuator or management exposure changes were gated and explained;
- tests cover meaningful configuration behavior when relevant.
