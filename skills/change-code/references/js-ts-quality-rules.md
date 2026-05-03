# JavaScript and TypeScript Quality Rules

Read this file when a change touches JavaScript, TypeScript, Node.js, frontend code, build tooling, package scripts, or JS/TS tests.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Stack detection

Before editing, inspect the relevant module for:

- package manager: `package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`/`bun.lockb`;
- workspace config: `pnpm-workspace.yaml`, Yarn workspaces, npm workspaces, Turborepo, Nx, Lerna;
- runtime and module system: `engines`, `type: "module"`, `.mjs`, `.cjs`, `.mts`, `.cts`, bundler config;
- TypeScript config: `tsconfig.json`, inherited configs, project references;
- test framework: Jest, Vitest, Mocha, Playwright, Cypress, Testing Library, Node test runner;
- formatter/linter: ESLint flat config, `.eslintrc*`, Prettier, Biome, Rome;
- framework conventions: React, Vue, Svelte, Next.js, Express, NestJS, Fastify, CLI tools.

Use package scripts and documented commands before inventing commands.

## Package manager and dependencies

- Use the package manager implied by the lockfile.
- Do not mix lockfiles or package managers.
- Do not edit lockfiles manually.
- Do not add dependencies unless clearly necessary and permitted.
- Prefer existing utilities and framework patterns before adding packages.
- Do not upgrade Node, TypeScript, bundlers, framework versions, package managers, lockfiles, or toolchain config unless directly required by the task.
- Preserve workspace boundaries and package ownership in monorepos.

## TypeScript

- Prefer strong, local, understandable types over broad `any`.
- Do not introduce `any`, non-null assertions, type assertions, or `// @ts-ignore` unless there is a narrow, justified reason.
- Prefer `unknown` plus validation for untrusted input.
- Preserve public exported types unless a contract change was requested.
- Use discriminated unions for meaningful state variants when local style supports them.
- Avoid duplicating runtime schemas and TypeScript types when the repository already has a schema/type pattern.
- Keep generic types readable; avoid clever type-level programming unless the project already uses it and the problem justifies it.
- Respect the project's strictness settings instead of weakening `tsconfig`.

## JavaScript

- Follow the project's existing JS style and module system.
- Avoid implicit globals and mutation of shared objects.
- Prefer `const` by default and `let` when reassignment is needed.
- Avoid changing CommonJS/ESM boundaries unless explicitly required.
- Preserve runtime compatibility with the configured Node or browser targets.
- Do not use syntax unsupported by the configured runtime or transpilation target.

## Async and error handling

- Await promises that must complete before continuing.
- Return promises from async test helpers and lifecycle hooks.
- Do not fire-and-forget async work unless it is intentional, observable, and failure-safe.
- Preserve cancellation, timeout, retry, and abort behavior when present.
- Do not swallow promise rejections.
- Preserve root causes when wrapping errors.
- Keep user-facing errors safe and useful.
- In Node services, avoid blocking the event loop with expensive synchronous IO or CPU work unless existing code intentionally does it.

## Frontend and UI code

- Keep UI state minimal and derived state explicit.
- Avoid unnecessary global state.
- Preserve accessibility semantics, labels, keyboard behavior, and focus handling.
- Avoid direct DOM manipulation when the framework provides a safer pattern.
- Keep components focused; avoid mixing data fetching, formatting, validation, and rendering when the project has clear layering.
- For React, respect hook rules, dependency arrays, memoization patterns, and controlled/uncontrolled component conventions.
- Do not add broad rerenders, polling, or expensive computations without considering performance.
- Test user-observable behavior with the repository's existing testing approach.

## Node.js, backend, and CLI code

- Validate external input at boundaries: HTTP, CLI args, env vars, files, queues, and third-party callbacks.
- Preserve API response shapes, status codes, headers, and error codes unless explicitly requested.
- Do not expose stack traces, internal paths, tokens, SQL, or sensitive payloads to clients.
- Use parameterized queries or the project's safe query APIs.
- Avoid building shell commands from untrusted input. Prefer argument arrays with `spawn`/`execFile` over string commands.
- Handle filesystem paths safely; prevent path traversal and accidental writes outside intended directories.
- Preserve exit codes and stderr behavior for CLI tools when they are part of the contract.

## Testing

- Add or update tests for changed behavior when a suitable test path exists.
- Prefer focused unit tests for pure logic and integration/e2e tests for routing, rendering, persistence, browser behavior, or external boundaries.
- Use the existing framework and assertion style.
- Do not make tests pass by weakening assertions, deleting coverage, increasing timeouts without reason, or skipping tests.
- For frontend tests, prefer user-visible assertions over implementation details.
- For async tests, await the relevant UI update, promise, event, or side effect.
- Keep mocks close to stable side-effect boundaries; avoid deep mock chains.
- Add regression tests for fixed bugs.

## Build and verification

Prefer the narrowest relevant command first.

Examples, adapt to the repository:

- `pnpm test -- <path>`
- `pnpm --filter <package> test`
- `npm test -- <path>`
- `yarn test <path>`
- `bun test <path>`
- `pnpm lint`
- `pnpm typecheck`
- `pnpm build`

Run typecheck, lint, formatting, or build commands when configured and relevant. Do not claim success unless the command completed successfully.

## Security

- Treat browser input, server input, env vars, file contents, URLs, and package metadata as untrusted.
- Avoid `eval`, `new Function`, unsafe template execution, and dynamic code loading.
- Sanitize or encode data at the correct boundary for HTML, URLs, SQL, shell, JSON, and logs.
- Preserve CSRF, CORS, auth, session, cookie, and tenant-isolation behavior.
- Avoid logging secrets, access tokens, refresh tokens, cookies, API keys, personal data, and sensitive payloads.
- Do not weaken dependency integrity, lockfiles, CSP, auth middleware, or validation schemas without explicit requirement.
