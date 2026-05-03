# JavaScript and TypeScript Skill Evals

Use these cases when reviewing routing changes for `change-code`, `language-routing.md`, and `js-ts-change-code`.

## Positive routing cases

### Node worker in a Next monorepo

- Repository signals: `apps/web` contains Next, changed file is `services/worker/src/job.ts` with Node-only runtime.
- User request: "Fix retry logic in the worker."
- Expected routing: `js-ts-change-code`.
- Expected references: `js-ts-quality-rules.md`.
- Not expected: `react-change-code`, `next-change-code`.

### Package script in a React package

- Repository signals: `react` dependency exists, changed files are `package.json` scripts and `scripts/build.ts`.
- User request: "Fix build script argument parsing."
- Expected routing: `js-ts-change-code`.
- Expected references: `js-ts-quality-rules.md`.
- Not expected: React/Next references unless behavior crosses framework boundaries.

### Shared TypeScript utility

- Repository signals: `packages/shared/src/date.ts`, used by several packages.
- User request: "Fix timezone formatting edge case and add tests."
- Expected routing: `js-ts-change-code`.
- Expected references: `js-ts-quality-rules.md`.

### Preact TSX component

- Repository signals: `preact` dependency, no React/Next evidence in owning package.
- User request: "Fix Card rendering."
- Expected routing: `js-ts-change-code` or a future Preact-specific skill.
- Not expected: `react-change-code`.

## Negative routing cases

### React hook

- Repository signals: `react` dependency, custom hook uses React APIs.
- User request: "Fix stale closure behavior."
- Expected routing: `react-change-code`.
- Not expected as final layer: `js-ts-change-code` only.

### Next route handler

- Repository signals: `app/api/users/route.ts`, `next` dependency.
- User request: "Validate query params and return 400 for invalid input."
- Expected routing: `next-change-code` plus generic JS/TS rules when useful.
- Not expected as final layer: `js-ts-change-code` only.
