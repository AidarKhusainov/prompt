# Language Routing

Use this reference when the repository stack is not obvious, the repository is mixed-language, or the user asks for a change that could affect several modules.

## Routing principles

- Route by the files and behavior that must change, not by the repository's largest language.
- Prefer the most specific available skill or profile that matches the requested task.
- When a repository has multiple build systems, identify the owning module before running commands.
- When signals conflict, inspect nearby source, tests, package manifests, and CI workflows before editing.
- When no language-specific or framework-specific profile exists, follow `change-code` and local repository conventions without inventing unsupported language rules.

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

### React and Next.js

Use `react-next-change-code` when available if the changed files or requested behavior involve React or Next.js UI, components, hooks, providers, forms, routes, layouts, Server Components, Client Components, server/client boundaries, route handlers, Server Functions, Server Actions, metadata, caching/revalidation, middleware/proxy, images/fonts, accessibility, or React/Next frontend tests.

Common React signals:

- `react` or `react-dom` in `package.json`
- React components, hooks, providers, UI tests, JSX/TSX using React APIs, React Testing Library, Storybook configured for React, Vite React, CRA, Remix routes using React, or framework-specific React entry points
- Storybook only when configured for React, for example `@storybook/react*`, React stories/components, or React dependencies nearby
- files such as `*.tsx` or `*.jsx` only when paired with React-specific imports, package dependencies, or local conventions

Do not treat `.tsx` or `.jsx` alone as React/Next.js evidence.

Common Next.js signals:

- `next` in `package.json`
- `next.config.*`
- App Router files under `app/` or `src/app/`: `layout.*`, `page.*`, `loading.*`, `error.*`, `not-found.*`, `route.*`
- Pages Router files: `pages/`, `src/pages/`, `_app.*`, `_document.*`, `getServerSideProps`, `getStaticProps`, API routes
- `middleware.*` or `proxy.*` only when located at the Next.js app root or `src` root and paired with `next` in `package.json`, `next/server` imports, or nearby Next.js route structure

For React/Next.js tasks, also read `references/js-ts-quality-rules.md` when the change touches general JavaScript/TypeScript concerns such as package scripts, type declarations, async logic, Node/server utilities, package tooling, build scripts, or shared JS/TS code.

Do not use React/Next.js rules only because a monorepo package contains React or Next.js somewhere. Route worker-only code, package scripts, config tooling, codegen, backend JS/TS, and shared non-UI utilities to the generic JS/TS profile unless the requested behavior crosses into React/Next.js.

Do not use React/Next.js rules for non-React frameworks such as Vue, Svelte, Angular, Astro-only, Preact, Solid, MDX-only, or plain Node.js unless the changed files actually contain React/Next.js code or the repository explicitly treats that area as React/Next.js.

### JavaScript and TypeScript

Read `references/js-ts-quality-rules.md` for JS/TS changes that are not better handled by `react-next-change-code`.

Common signals:

- `package.json`
- `package-lock.json`, `npm-shrinkwrap.json`
- `pnpm-lock.yaml`, `pnpm-workspace.yaml`
- `yarn.lock`
- `bun.lockb`, `bun.lock`
- `tsconfig.json`, `jsconfig.json`
- `eslint.config.*`, `.eslintrc*`, `prettier.config.*`, `.prettierrc*`
- `src/**/*.ts`, `src/**/*.tsx`, `src/**/*.js`, `src/**/*.jsx`, config scripts, CLIs, backend JS/TS, or shared libraries

If JSX/TSX is present without React or Next.js evidence, route to generic JS/TS first and follow the repository's local JSX runtime conventions.

Choose the package manager from consistent repository evidence: `packageManager`, Corepack usage, lockfiles, workspace config, README, CI, and package scripts. If signals conflict, inspect nearby module docs before choosing commands.

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
3. Use the available language/framework profile for the changed files and behavior when one exists.
4. Run checks scoped to that module first.
5. Run broader checks only when shared contracts or generated artifacts are affected.

Examples:

- Java backend plus React frontend: route API implementation to Java; route UI changes to React/Next.js; route API contract changes through both sides if needed.
- Next.js frontend plus Node worker: route app route/component/server-action changes to React/Next.js; route worker-only changes to JS/TS.
- React package plus shared TypeScript utilities: route component or hook changes to React/Next.js; route utility-only changes to JS/TS unless the utility's contract is React-specific.
- Shell script that invokes a Java service: route script-only fixes to shell; route service behavior changes to Java.
- Generated client from OpenAPI: edit the OpenAPI source when appropriate, not generated output, and verify both generator and affected consumer when practical.

## Ambiguous cases

If the language or module is still ambiguous after targeted inspection, ask one clarifying question only when the choice would materially change behavior, compatibility, or verification. Otherwise make a reasonable assumption, state it in the final response, and continue.
