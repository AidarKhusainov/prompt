# React and Next.js Compatibility Router Evals

Use these cases when reviewing the compatibility behavior of `react-next-change-code`.

The goal is to keep older integrations working while routing new work to narrower skills.

## Positive compatibility cases

### React component in shared package

- Repository signals: `packages/ui/Button.tsx`, `react` in owning package, React component imports/hooks nearby.
- User request: "Fix Button disabled state and add a component test."
- Expected compatibility routing: `react-next-change-code` -> `react-change-code`.
- Expected references after routing: `react-quality-rules.md`, `frontend-testing-rules.md`.

### Next route handler

- Repository signals: `apps/web/app/api/users/route.ts`, `next` in package, `NextRequest`/`NextResponse` imports nearby.
- User request: "Validate query params and return 400 for invalid input."
- Expected compatibility routing: `react-next-change-code` -> `next-change-code`.
- Expected references after routing: `next-routing-api-rules.md`; optionally JS/TS validation rules.

### Next middleware/proxy with Next evidence

- Repository signals: `apps/web/middleware.ts` or `apps/web/proxy.ts`, `next` in package, `next/server` imports, Next route structure nearby.
- User request: "Update auth redirect behavior in middleware."
- Expected compatibility routing: `react-next-change-code` -> `next-change-code`.
- Expected references after routing: `next-middleware-proxy-rules.md`, `next-project-detection-rules.md`.

## Negative compatibility cases

### Generic JS/TS in React or Next repo

- Repository signals: React or Next exists somewhere, but changed files are package scripts, Node workers, backend JS/TS, codegen, or shared non-React utilities.
- User request: "Fix build script argument parsing" or "Fix worker retry logic."
- Expected routing: `js-ts-change-code`, not React/Next final-layer behavior.

### Non-React JSX runtime

- Repository signals: Preact, Solid, Vue, Svelte, Angular, Astro-only, or MDX-only.
- User request: "Fix component rendering."
- Expected routing: generic JS/TS or a future dedicated framework skill, not React/Next behavior.

## Regression checks

- `react-next-change-code` remains short and does not accumulate new detailed framework rules.
- New React rules go to `react-change-code`.
- New Next rules go to `next-change-code`.
- `.tsx` / `.jsx` alone does not trigger React/Next routing.
- `middleware.*` / `proxy.*` count as Next signals only with Next-specific evidence.
