# Language Routing

Use this reference when the repository stack is not obvious, the repository is mixed-language, or the user asks for a change that could affect several modules.

## Routing principles

- Route by the files and behavior that must change, not by the repository's largest language.
- Prefer the most specific available skill or profile that matches the requested task.
- When a repository has multiple build systems, identify the owning module before running commands.
- When signals conflict, inspect nearby source, tests, package manifests, and CI workflows before editing.
- When no language-specific profile exists, follow `change-code` and local repository conventions without inventing unsupported language rules.

## Strong signals

### Java

Use `java-change-code` when available if the relevant module contains Java source and Maven or Gradle build files.

Common signals:

- `pom.xml`
- `build.gradle` or `build.gradle.kts`
- `settings.gradle` or `settings.gradle.kts`
- `src/main/java`, `src/test/java`
- `mvnw`, `gradlew`

Do not route Kotlin-only modules to `java-change-code` unless the task also changes Java Maven/Gradle code.

### JavaScript and TypeScript

Read `references/js-ts-quality-rules.md` for JS/TS changes.

Common signals:

- `package.json`
- `package-lock.json`, `npm-shrinkwrap.json`
- `pnpm-lock.yaml`, `pnpm-workspace.yaml`
- `yarn.lock`
- `bun.lockb`, `bun.lock`
- `tsconfig.json`, `jsconfig.json`
- `eslint.config.*`, `.eslintrc*`, `prettier.config.*`, `.prettierrc*`
- `src/**/*.ts`, `src/**/*.tsx`, `src/**/*.js`, `src/**/*.jsx`

Pick the package manager from the lockfile when one is present. Prefer package scripts over invented commands.

### Bash and shell scripts

Read `references/bash-quality-rules.md` for shell script, Makefile shell, and CI shell-step changes.

Common signals:

- `*.sh`
- shebangs such as `#!/usr/bin/env bash`, `#!/bin/sh`, or `#!/bin/zsh`
- `scripts/`, `bin/`, `Makefile`, `justfile`
- ShellCheck or shfmt configuration

Before editing, determine whether the script is POSIX `sh`, Bash, Zsh, or another shell. Do not use Bash-only features in POSIX scripts.

## Mixed-language repositories

For monorepos and mixed modules:

1. Identify the file or module that owns the requested behavior.
2. Read local instructions closest to that path.
3. Use the available language profile for the changed files when one exists.
4. Run checks scoped to that module first.
5. Run broader checks only when shared contracts or generated artifacts are affected.

Examples:

- Java backend plus React frontend: route API implementation to Java; route UI changes to JS/TS; route API contract changes through both sides if needed.
- Shell script that invokes a Java service: route script-only fixes to shell; route service behavior changes to Java.
- Generated client from OpenAPI: edit the OpenAPI source when appropriate, not generated output, and verify both generator and affected consumer when practical.

## Ambiguous cases

If the language or module is still ambiguous after targeted inspection, ask one clarifying question only when the choice would materially change behavior, compatibility, or verification. Otherwise make a reasonable assumption, state it in the final response, and continue.
