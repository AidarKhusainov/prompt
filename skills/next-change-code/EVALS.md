# Next.js Skill Evals

Use these cases when reviewing routing and reference-loading changes for `next-change-code`.

## Positive routing cases

### App Router page with data loading

- Repository signals: `apps/web/app/dashboard/page.tsx`, `next` dependency, App Router structure.
- User request: "Fix dashboard data loading and empty state."
- Expected routing: `next-change-code` for data loading; also apply `react-change-code` for UI state if needed.
- Expected references: `next-project-detection-rules.md`, `next-server-client-rules.md` when server/client boundary is involved.

### Route handler validation

- Repository signals: `apps/web/app/api/users/route.ts`, `NextRequest`/`NextResponse` imports.
- User request: "Validate query params and return 400 for invalid input."
- Expected routing: `next-change-code`.
- Expected references: `next-routing-api-rules.md`; optionally `js-ts-change-code` for validation/async logic.

### Cache invalidation

- Repository signals: App Router, existing cache tags or revalidation APIs.
- User request: "Revalidate the product list after saving a product."
- Expected routing: `next-change-code`.
- Expected references: `next-cache-runtime-rules.md`, `next-server-client-rules.md` if Server Actions are involved.

### Metadata update

- Repository signals: App Router metadata exports or metadata helper.
- User request: "Fix Open Graph metadata for product pages."
- Expected routing: `next-change-code`.
- Expected references: `next-routing-api-rules.md`.

### Middleware/proxy auth redirect

- Repository signals: `middleware.ts` or `proxy.ts` at Next app root, `next/server` imports, `next` dependency.
- User request: "Fix auth redirect behavior in middleware."
- Expected routing: `next-change-code`.
- Expected references: `next-middleware-proxy-rules.md`, `next-project-detection-rules.md`.

## Negative routing cases

### React-only component in Next app

- Repository signals: Next app exists, changed file is `components/Button.tsx` with no routing/cache/server-client behavior.
- User request: "Fix disabled visual state."
- Expected routing: `react-change-code`.
- Not expected: Next references.

### Node worker in Next monorepo

- Repository signals: `apps/web` contains Next, changed file is `services/worker/src/job.ts`.
- User request: "Fix retry logic."
- Expected routing: `js-ts-change-code`.
- Not expected: `next-change-code`.

### Generic backend middleware

- Repository signals: `server/middleware.ts`, Express/Koa/Fastify/Nest backend, no `next` dependency or `next/server` imports.
- User request: "Fix auth middleware error handling."
- Expected routing: `js-ts-change-code`.
- Not expected: `next-change-code`.

## Reference-loading regression checks

- Detection-only ambiguity loads `next-project-detection-rules.md`, not every Next reference.
- Server/client boundary changes load `next-server-client-rules.md`.
- Cache/runtime changes load `next-cache-runtime-rules.md`.
- Route handlers/API/metadata changes load `next-routing-api-rules.md`.
- Middleware/proxy changes load `next-middleware-proxy-rules.md`.
