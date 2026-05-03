# React and Next.js Skill Evals

Use these cases when reviewing routing changes for `change-code`, `language-routing.md`, and `react-next-change-code`.

The goal is to keep React/Next work routed to `react-next-change-code` while preventing generic JS/TS, backend Node, and non-React JSX runtimes from over-triggering this skill.

## Positive routing cases

### React component in shared package

- Repository signals: `packages/ui/Button.tsx`, `react` in the owning package, React component imports/hooks nearby.
- User request: "Fix Button disabled state and add a component test."
- Expected routing: `react-next-change-code`.
- References: `react-quality-rules.md`, `frontend-testing-rules.md`.

### React hook behavior

- Repository signals: `packages/ui/useDebouncedValue.ts`, React hook naming and imports, React tests nearby.
- User request: "Fix stale closure behavior in this hook."
- Expected routing: `react-next-change-code`.
- References: `react-quality-rules.md`; generic JS/TS rules from `change-code` if async/timer behavior is involved.

### Next App Router page/layout/component

- Repository signals: `apps/web/app/dashboard/page.tsx`, `next` in the owning package, App Router structure.
- User request: "Add the empty state to the dashboard page."
- Expected routing: `react-next-change-code`.
- References: `react-quality-rules.md`; `nextjs-rules.md` if routing, metadata, server/client boundary, or data fetching changes.

### Next route handler

- Repository signals: `apps/web/app/api/users/route.ts`, `next` in package, `NextRequest`/`NextResponse` imports nearby.
- User request: "Validate query params and return 400 for invalid input."
- Expected routing: `react-next-change-code`.
- References: `nextjs-rules.md`; generic JS/TS rules from `change-code` for validation/async logic when available.

### Next middleware/proxy with Next evidence

- Repository signals: `apps/web/middleware.ts` or `apps/web/proxy.ts`, `next` in package, `next/server` imports, Next route structure nearby.
- User request: "Update auth redirect behavior in middleware."
- Expected routing: `react-next-change-code`.
- References: `nextjs-rules.md`.

## Negative routing cases

### Preact TSX component

- Repository signals: `packages/widgets/Card.tsx`, `preact` dependency, no `react`/`react-dom`/`next` evidence in owning package.
- User request: "Fix Card rendering."
- Expected routing: generic JS/TS via `change-code`, not `react-next-change-code`.
- Reason: `.tsx` alone is not React/Next evidence; Preact has different runtime assumptions.

### Solid TSX component

- Repository signals: `apps/solid/src/Button.tsx`, `solid-js` dependency, Solid component patterns.
- User request: "Fix disabled button behavior."
- Expected routing: generic JS/TS via `change-code`, not `react-next-change-code`.
- Reason: non-React JSX runtime.

### Astro MDX-only content

- Repository signals: `src/content/post.mdx`, Astro project, no React/Next component behavior involved.
- User request: "Fix the MDX frontmatter and copy."
- Expected routing: generic JS/TS/content handling or no React/Next skill.
- Reason: Astro/MDX alone is not React/Next evidence.

### Node worker in Next monorepo

- Repository signals: `apps/web` contains Next, but changed files are `services/worker/src/job.ts` or `packages/worker/src/index.ts` with Node-only runtime.
- User request: "Fix retry logic in the worker."
- Expected routing: generic JS/TS via `change-code`, not `react-next-change-code`.
- Reason: route by changed files and behavior, not by the monorepo's largest framework.

### Package script in React repo

- Repository signals: `react` exists in package, but changed files are `package.json` scripts or `scripts/build.ts`.
- User request: "Fix the build script argument parsing."
- Expected routing: generic JS/TS via `change-code` unless the behavior crosses React/Next boundaries.
- Reason: package tooling is not React/Next-specific.

### Generic backend middleware

- Repository signals: `server/middleware.ts`, Express/Koa/Fastify/Nest backend, no `next` dependency, no `next/server` imports, no Next route structure.
- User request: "Fix auth middleware error handling."
- Expected routing: generic JS/TS via `change-code`, not `react-next-change-code`.
- Reason: `middleware.*` alone is not Next evidence.

### Remix loader/action or routing contract

- Repository signals: Remix route file with loader/action/server runtime behavior.
- User request: "Change loader validation and redirect behavior."
- Expected routing: generic JS/TS via `change-code` unless a dedicated Remix profile exists.
- Reason: `react-next-change-code` applies only to React component, hook, JSX, provider, accessibility, or frontend-test changes in React-based non-Next frameworks.

## Regression checks

When editing routing rules, verify that:

- `.tsx` / `.jsx` alone does not trigger React/Next routing.
- Storybook is a React signal only when configured for React.
- App Router filenames count as Next signals only under `app/` or `src/app/`.
- `middleware.*` / `proxy.*` count as Next signals only with Next-specific evidence.
- Node workers and package tooling in React/Next monorepos route to generic JS/TS unless behavior crosses React/Next boundaries.
