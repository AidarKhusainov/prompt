# Language Routing

Use this reference when the repository stack is not obvious, the repository is mixed-language, or the user asks for a change that could affect several modules.

## Routing principles

- Route by the files and behavior that must change, not by the repository's largest language.
- Prefer the most specific available skill or profile that matches the requested task.
- Use language skills for generic language behavior and framework skills only for framework-specific behavior.
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

### JavaScript and TypeScript

Use `js-ts-change-code` for JS/TS changes that are not better handled by a more specific framework skill.

Common signals:

- `package.json`
- JS package-manager lockfiles and workspace files
- `tsconfig.json`, `jsconfig.json`
- ESLint, Prettier, Biome, bundler, or test config
- `src/**/*.ts`, `src/**/*.js`, config scripts, CLIs, backend JS/TS, workers, or shared libraries

Route generic package scripts, build tooling, Node workers, shared utilities, backend JS/TS, codegen, and non-framework tests to `js-ts-change-code` even if the monorepo also contains React or Next.js.

If JSX/TSX is present without framework evidence, route to `js-ts-change-code` first and follow local JSX runtime conventions.

### React

Use `react-change-code` when the changed files or requested behavior involve React UI, components, hooks, providers, forms, JSX rendering, accessibility, state, refs, effects, or React frontend tests.

Common React signals:

- `react` or `react-dom` in the owning package's `package.json`
- React imports, hooks, providers, component tests, React Testing Library, Storybook configured for React, Vite React, CRA, or framework-specific React entry points
- `*.tsx` or `*.jsx` only when paired with React-specific imports, package dependencies, or local conventions

Do not treat `.tsx` or `.jsx` alone as React evidence.

For non-Next React frameworks such as Remix, use `react-change-code` only for component, hook, JSX, provider, accessibility, or frontend-test changes. Route framework-specific loaders, actions, server runtime, routing contracts, and build tooling to `js-ts-change-code` unless a dedicated framework profile exists.

Do not use React rules for Preact, Solid, Vue, Svelte, Angular, Astro-only, MDX-only, or plain Node.js unless the changed files actually contain React code or the repository explicitly treats that area as React.

### Next.js

Use `next-change-code` when the changed files or requested behavior involve Next.js routing, App Router, Pages Router, layouts, route handlers, API routes, Server Components, Client Components, server/client boundaries, Server Functions, Server Actions, metadata, caching/revalidation, middleware/proxy, images/fonts, runtime, or framework build behavior.

Common Next.js signals:

- `next` in the owning package's `package.json`
- `next.config.*`
- App Router files under `app/` or `src/app/`: `layout.*`, `page.*`, `loading.*`, `error.*`, `not-found.*`, `template.*`, `route.*`
- Pages Router files: `pages/`, `src/pages/`, `_app.*`, `_document.*`, `getServerSideProps`, `getStaticProps`, API routes
- `middleware.*` or `proxy.*` only when located at the Next.js app root or `src` root and paired with `next` in `package.json`, `next/server` imports, or nearby Next.js route structure

For ordinary React component changes inside a Next app, prefer `react-change-code` unless the change touches Next-specific routing, runtime, cache, metadata, server/client, or framework behavior.

For Next.js tasks, also apply `react-change-code` when the task changes React UI behavior, and apply `js-ts-change-code` when it changes generic JS/TS utilities or package tooling.

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

- Java backend plus React frontend: route API implementation to Java; route UI changes to React; route API contract changes through both sides if needed.
- Next.js frontend plus Node worker: route app route/component/server-action changes to Next.js or React as appropriate; route worker-only changes to JS/TS.
- React package plus shared TypeScript utilities: route component or hook changes to React; route utility-only changes to JS/TS unless the utility's contract is React-specific.
- Shell script that invokes a Java service: route script-only fixes to shell; route service behavior changes to Java.
- Generated client from OpenAPI: edit the OpenAPI source when appropriate, not generated output, and verify both generator and affected consumer when practical.

## Compatibility routers

`react-next-change-code` remains a compatibility router for older integrations. Prefer `react-change-code` and `next-change-code` for new rules and evals.

## Ambiguous cases

If the language or module is still ambiguous after targeted inspection, ask one clarifying question only when the choice would materially change behavior, compatibility, or verification. Otherwise make a reasonable assumption, state it in the final response, and continue.
