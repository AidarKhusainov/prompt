# JavaScript and TypeScript Quality Rules

Read this file when a non-trivial change touches JavaScript, TypeScript, Node.js, browser utilities, package tooling, build scripts, shared JS/TS code, or JS/TS tests.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Stack detection

Before editing, inspect the relevant module for:

- package manager: `packageManager`, Corepack usage, `package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`/`bun.lockb`;
- workspace config: `pnpm-workspace.yaml`, npm/yarn workspaces, Turborepo, Nx, Lerna;
- runtime and module system: `engines`, `type`, `.mjs`, `.cjs`, `.mts`, `.cts`, bundler config;
- TypeScript config: `tsconfig.json`, inherited configs, project references;
- test framework: Jest, Vitest, Mocha, Playwright, Cypress, Testing Library, Node test runner;
- formatter/linter: ESLint flat config, `.eslintrc*`, Prettier, Biome;
- framework signals that may require a narrower framework skill.

Use package scripts and documented commands before inventing commands.

## Package manager and dependencies

- Use the package manager indicated by consistent repository evidence.
- Do not mix lockfiles or package managers.
- Do not edit lockfiles manually.
- Do not add dependencies unless clearly necessary and permitted.
- Prefer existing utilities and framework patterns before adding packages.
- Do not upgrade Node, TypeScript, bundlers, framework versions, package managers, lockfiles, or toolchain config unless directly required.
- Preserve workspace boundaries and package ownership in monorepos.

## TypeScript

- Prefer strong, local, understandable types over broad `any`.
- Do not introduce `any`, non-null assertions, type assertions, or `// @ts-ignore` unless there is a narrow, justified reason.
- Prefer `unknown` plus validation for untrusted input.
- Preserve public exported types unless a contract change was requested.
- Respect the project's strictness settings instead of weakening `tsconfig`.
- Avoid duplicating runtime schemas and TypeScript types when the repository already has a schema/type pattern.

## JavaScript

- Follow the project's existing JS style and module system.
- Avoid implicit globals and mutation of shared objects.
- Prefer `const` by default and `let` when reassignment is needed.
- Avoid changing CommonJS/ESM boundaries unless explicitly required.
- Preserve runtime compatibility with configured Node or browser targets.

## Async and error handling

- Await promises that must complete before continuing.
- Return promises from async test helpers and lifecycle hooks.
- Do not fire-and-forget async work unless it is intentional, observable, and failure-safe.
- Do not swallow promise rejections.
- Preserve cancellation, timeout, retry, and abort behavior when present.
- Preserve root causes when wrapping errors.
- Keep user-facing errors safe and useful.
- In Node services, avoid blocking the event loop with expensive synchronous IO or CPU work unless existing code intentionally does it.

## Frontend-neutral browser code

- Keep UI state minimal and derived state explicit.
- Preserve accessibility semantics and browser behavior when touching DOM-facing utilities.
- Avoid direct DOM manipulation when the owning framework provides a safer pattern.
- Do not add broad rerenders, polling, or expensive computations without considering performance.

For React or Next-specific UI behavior, route to the narrower framework skill.

## Node.js, backend, and CLI code

- Validate external input at boundaries: HTTP, CLI args, env vars, files, queues, and third-party callbacks.
- Preserve API response shapes, status codes, headers, exit codes, stderr behavior, and error codes unless explicitly requested.
- Do not expose stack traces, internal paths, tokens, SQL, or sensitive payloads to clients.
- Use parameterized queries or the project's safe query APIs.
- Avoid building shell commands from untrusted input. Prefer argument arrays with `spawn`/`execFile` over string commands.
- Handle filesystem paths safely; prevent path traversal and accidental writes outside intended directories.

## Testing

- Add or update tests for changed behavior when a suitable test path exists.
- Prefer focused unit tests for pure logic and integration/e2e tests for routing, rendering, persistence, browser behavior, or external boundaries.
- Use the existing framework and assertion style.
- Do not weaken assertions, delete coverage, increase timeouts without reason, or skip tests to make them pass.
- For async tests, await the relevant UI update, promise, event, or side effect.
- Keep mocks close to stable side-effect boundaries.
- Add regression tests for fixed bugs.

## Build and verification

Prefer the narrowest relevant command first. Adapt examples to the repository:

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
