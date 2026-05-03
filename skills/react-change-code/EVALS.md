# React Skill Evals

Use these cases when reviewing routing and reference-loading changes for `react-change-code`.

## Positive routing cases

### React component in shared package

- Repository signals: `packages/ui/Button.tsx`, `react` in owning package, React component imports nearby.
- User request: "Fix Button disabled state and add a component test."
- Expected routing: `react-change-code`.
- Expected references: `react-quality-rules.md`, `frontend-testing-rules.md`.
- Not expected: Next.js references.

### React hook behavior

- Repository signals: custom hook with React APIs and tests nearby.
- User request: "Fix stale closure behavior in this hook."
- Expected routing: `react-change-code`.
- Expected references: `react-quality-rules.md`.
- Optional: `js-ts-change-code` for async/timer behavior.

### Ordinary UI in Next app

- Repository signals: `apps/web/components/EmptyState.tsx`, `next` dependency exists, no routing/cache/server-client behavior changed.
- User request: "Update empty state copy and disabled button behavior."
- Expected routing: `react-change-code`.
- Expected references: `react-quality-rules.md` for behavior changes; none for pure copy.
- Not expected: `next-change-code` unless Next-specific behavior is touched.

## Negative routing cases

### Next route handler

- Repository signals: `apps/web/app/api/users/route.ts`.
- User request: "Validate query params and return 400."
- Expected routing: `next-change-code`.
- Not expected as final layer: `react-change-code`.

### Package script in React repo

- Repository signals: `react` dependency exists, changed files are `package.json` scripts or `scripts/build.ts`.
- User request: "Fix build script argument parsing."
- Expected routing: `js-ts-change-code`.
- Not expected: `react-change-code`.

### Non-React JSX runtime

- Repository signals: Preact, Solid, Vue, Svelte, Astro-only, or MDX-only.
- User request: "Fix component rendering."
- Expected routing: generic JS/TS or a future dedicated framework skill.
- Not expected: `react-change-code`.

## Reference-loading regression checks

- Trivial copy or import cleanup should not load React references unless code is accessibility-, security-, contract-, or routing-sensitive.
- Component behavior changes load `react-quality-rules.md`.
- Frontend tests load `frontend-testing-rules.md`.
- Next-specific behavior routes to `next-change-code` instead of loading Next rules here.
