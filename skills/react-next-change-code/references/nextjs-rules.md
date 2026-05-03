# Next.js Rules

Read this file when a change touches a Next.js application, including App Router, Pages Router, route handlers, API routes, Server Components, Client Components, Server Functions, Server Actions, forms, metadata, caching, revalidation, images, fonts, middleware/proxy, runtime config, or build/deployment behavior.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Version-sensitive practice

- Inspect the installed `next`, `react`, and `react-dom` versions before using version-sensitive APIs.
- Detect whether the app uses App Router, Pages Router, or a mixed migration. Do not migrate router systems unless explicitly requested.
- Use App Router rules for files under `app/` or `src/app/`.
- Use Pages Router rules for files under `pages/` or `src/pages/` and preserve legacy data fetching methods when present.
- Use the term Server Functions for general server-executed functions. Use Server Actions for mutation/action flows, especially forms.
- For Next.js 16+ projects, account for Cache Components and the `proxy.ts` rename only when the repository has adopted those patterns.
- Do not rename `middleware.ts` to `proxy.ts`, enable `cacheComponents`, add PPR, change route segment config, or alter runtime target unless the task explicitly requires it.
- In Next.js 16+ projects that already use `proxy.ts`, remember that proxy runs on the Node.js runtime. Do not assume Edge runtime behavior for proxy code.
- Do not assume `next lint` exists. Prefer the repository's configured ESLint/package script because newer Next.js versions use ESLint directly.

## Project and router detection

Before editing, inspect relevant:

- `package.json`, lockfile, workspace config, and package scripts;
- `next.config.*`, `tsconfig.json`, `jsconfig.json`, ESLint config, env templates, and CI workflows;
- `app/` or `src/app/` route segments, `layout.*`, `page.*`, `loading.*`, `error.*`, `not-found.*`, `template.*`, `route.*`, and route groups;
- `pages/` or `src/pages/`, `_app.*`, `_document.*`, API routes, and legacy data fetching;
- `middleware.*` or `proxy.*` files and matcher config;
- metadata usage, sitemap/robots files, image/font config, server-only/client-only imports, and deployment runtime hints.

Prefer the closest package/module-level config and scripts in monorepos.

## Server and Client Components

- In App Router, keep components server-side by default.
- Add `'use client'` only when the file needs state, effects, event handlers, refs tied to browser behavior, browser APIs, client-only libraries, context providers that use client state, or React client hooks.
- Keep client boundaries small and close to the interactive leaf component.
- Once a module is marked `'use client'`, its imports are part of the client module graph. Do not import server-only code into it.
- Do not pass non-serializable props from Server Components to Client Components.
- Do not import database clients, filesystem access, private environment variables, auth server helpers, or server-only modules into Client Components.
- Use `server-only` and `client-only` package patterns when the repository already uses them or when adding a small boundary guard is appropriate.
- Wrap third-party browser-only components in small Client Components instead of marking a whole route or layout as client.
- Do not add hooks such as `useState`, `useEffect`, `useReducer`, `useRef`, `useSearchParams`, or client router hooks to Server Components.
- Avoid hydration mismatches from browser-only values, random IDs, dates, time zones, locale formatting, media queries, and storage reads during server render.

## Data fetching and server work

- Prefer server-side data fetching in Server Components when data is needed for initial render and does not require client interactivity.
- Do not duplicate server data into client state unless the UI needs optimistic, draft, staged, or client-only state.
- Keep secrets and privileged operations on the server.
- Validate untrusted input from params, search params, cookies, headers, forms, route handlers, webhooks, and third-party callbacks.
- Preserve existing auth/session and tenant-isolation checks.
- Use existing project data libraries and request helpers before adding new ones.
- Preserve redirect and not-found behavior when changing data loading.
- Do not fetch sensitive data in Client Components just to avoid server/client boundaries.

## Caching, revalidation, and rendering mode

- Treat caching and rendering mode as public behavior. Do not change them casually.
- Before editing, identify whether the route is static, dynamic, partially prerendered, cache-component based, or legacy cache-model based.
- Preserve existing `fetch` cache options, `next.revalidate`, `next.tags`, route segment config, `dynamic`, `revalidate`, `fetchCache`, `runtime`, and `preferredRegion` unless the task requires a change.
- Do not use Cache Components APIs unless `cacheComponents: true` is enabled or the repository already has a local pattern for them.
- In modern Next.js projects using Cache Components, use `use cache`, `cacheTag`, `cacheLife`, `revalidateTag`, `updateTag`, and `revalidatePath` only when enabled and consistent with local patterns.
- In Next.js 16+ projects, do not add single-argument `revalidateTag(tag)` calls. Prefer `revalidateTag(tag, "max")` for stale-while-revalidate behavior, or `updateTag(tag)` only in Server Actions when read-your-own-writes semantics are required.
- Use `updateTag` for read-your-own-writes only in Server Actions where supported.
- Use `revalidateTag` for tag-based stale-while-revalidate invalidation when supported and appropriate.
- Prefer tag-based revalidation over path-based revalidation when the cache ownership is clear.
- Avoid over-invalidating broad paths or root layouts unless the task requires it.
- Do not use deprecated or legacy cache behavior when the repository has already migrated to a newer model.
- If the app uses the previous cache model, preserve it instead of forcing a Cache Components migration.
- Consider request-specific APIs such as `cookies`, `headers`, `searchParams`, and `connection` as rendering-mode-sensitive.

## Server Functions, Server Actions, and forms

- Use Server Functions only when supported by the installed Next.js and React versions and consistent with the repository.
- Use Server Actions for mutation/action flows, especially forms, only when the installed stack and local conventions support them.
- Keep mutation code server-side and validate all input on the server.
- Ensure mutations have authorization checks, idempotency or double-submit safeguards where relevant, and safe error handling.
- Revalidate or update cache entries after mutations when the UI depends on cached data.
- Use redirects intentionally after successful mutations when that matches user flow.
- Do not pass secrets or privileged objects through action arguments or serialized props.
- For forms, preserve progressive enhancement when the app relies on it.
- Model pending, optimistic, success, validation-error, and server-error states explicitly.
- For React 19+ stacks, use action-aware APIs such as `useActionState`, `useOptimistic`, and `useFormStatus` only when the installed stack and project patterns support them.

## Route handlers, API routes, and webhooks

- Preserve HTTP methods, status codes, headers, response shapes, streaming behavior, and cache headers unless explicitly requested.
- Validate params, query strings, headers, cookies, body payloads, and webhook signatures.
- Do not expose stack traces, internal paths, SQL, tokens, cookies, or sensitive payloads to clients.
- Keep runtime compatibility in mind: Node.js APIs are not available in Edge runtime.
- Do not switch runtime between Node.js and Edge unless explicitly required and verified.
- Use `NextRequest`/`NextResponse` patterns consistently with nearby handlers.
- Avoid reading large request bodies unnecessarily.

## Routing, navigation, and metadata

- Preserve public URLs, route groups, dynamic segment names, catch-all behavior, search params, redirects, rewrites, and canonical URLs unless explicitly requested.
- Use Next.js navigation APIs appropriate to the router type.
- Use `Link` for navigation and preserve prefetch behavior unless there is a reason to change it.
- Use Metadata APIs in App Router where appropriate; do not manually duplicate head tags when Metadata APIs are already used.
- Preserve title, description, Open Graph, Twitter metadata, alternates, robots, sitemap, and structured data behavior unless the task targets SEO.
- Treat metadata changes as public/SEO behavior and verify carefully.

## Images, fonts, and assets

- Prefer `next/image` for local or remote images when the project uses it and configuration supports the source.
- Preserve image dimensions, aspect ratio, priority/loading behavior, alt text, and remote image config.
- Do not set meaningless alt text. Use empty `alt=""` only for decorative images.
- Prefer `next/font` when the project uses it. Do not add external font requests or broad global font changes without need.
- Avoid adding large assets or unoptimized images unless explicitly required.

## Styling and CSS boundaries

- Preserve global CSS import constraints and route/layout ownership.
- Use existing styling systems: CSS Modules, Tailwind, Sass, CSS-in-JS, component libraries, or design tokens.
- Avoid global CSS changes for local component fixes.
- Preserve theme, responsive behavior, dark/light mode, and reduced-motion behavior.

## Middleware and proxy

- Treat middleware/proxy as security- and routing-sensitive.
- Preserve matcher patterns, auth checks, redirects, rewrites, headers, cookies, locale handling, and URL normalization unless explicitly requested.
- For Next.js 16+ projects that already use `proxy.ts`, follow proxy naming and Node.js runtime constraints.
- Do not rename middleware/proxy files or change skip flags just for style.
- Do not add heavy work, database calls, or unsupported runtime APIs to middleware/proxy.

## TypeScript and generated types

- Preserve route param types, search param types, generated route types, and public exported types unless explicitly requested.
- Do not weaken `tsconfig`, disable strictness, or add broad assertions to bypass framework type errors.
- For current App Router examples, account for async `params`/`searchParams` patterns when the installed Next.js version and local codebase use them.
- Follow local path aliases and module boundaries.

## Testing and verification

Run checks based on what changed:

- Component-only UI changes: focused component tests, typecheck, lint when relevant.
- Route/page/layout changes: route-level tests or build, plus typecheck.
- Server/client boundary changes: typecheck and build.
- Metadata, image/font, config, cache, runtime, middleware/proxy changes: build and targeted tests where available.
- Route handlers/API routes: unit/integration tests for status, headers, body, auth, validation, and error cases.
- Critical navigation/form flows: Playwright/Cypress when the repository uses e2e tests.

Prefer package scripts and configured commands. Examples, adapt to the repository:

- `pnpm --filter web test -- <path>`
- `pnpm --filter web typecheck`
- `pnpm --filter web lint`
- `pnpm --filter web build`
- `pnpm exec playwright test <spec>`

Do not claim a Next.js build passed unless the build command completed successfully.
