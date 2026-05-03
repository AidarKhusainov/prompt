# Next.js Routing, API, and Metadata Rules

Read this file when a change touches routes, navigation, redirects, rewrites, route handlers, API routes, webhooks, metadata, sitemap, robots, images, fonts, or public URLs.

## Route handlers, API routes, and webhooks

- Preserve HTTP methods, status codes, headers, response shapes, streaming behavior, and cache headers unless explicitly requested.
- Validate params, query strings, headers, cookies, body payloads, and webhook signatures.
- Do not expose stack traces, internal paths, SQL, tokens, cookies, or sensitive payloads to clients.
- Keep runtime compatibility in mind.
- Use `NextRequest`/`NextResponse` patterns consistently with nearby handlers.
- Avoid reading large request bodies unnecessarily.
- Preserve auth/session and tenant-isolation checks.

## Routing and navigation

- Preserve public URLs, route groups, dynamic segment names, catch-all behavior, search params, redirects, rewrites, canonical URLs, and locale behavior unless explicitly requested.
- Use Next.js navigation APIs appropriate to the router type.
- Use `Link` for navigation and preserve prefetch behavior unless there is a reason to change it.
- Do not migrate App Router/Pages Router structure unless explicitly requested.

## Metadata and SEO

- Use Metadata APIs in App Router where appropriate; do not manually duplicate head tags when Metadata APIs are already used.
- Preserve title, description, Open Graph, Twitter metadata, alternates, robots, sitemap, canonical URLs, and structured data behavior unless the task targets SEO.
- Treat metadata changes as public/SEO behavior and verify carefully.

## Images, fonts, and assets

- Prefer `next/image` for local or remote images when the project uses it and configuration supports the source.
- Preserve image dimensions, aspect ratio, priority/loading behavior, alt text, and remote image config.
- Use empty `alt=""` only for decorative images.
- Prefer `next/font` when the project uses it.
- Do not add external font requests, broad global font changes, large assets, or unoptimized images without need.

## Verification

- Route handlers/API routes: test method, params/query/body validation, status, headers, response shape, auth, and errors when possible.
- Pages/layouts/routes: use route-level tests or build/typecheck when tests cannot model framework behavior.
- Metadata/image/font/config changes: run build or the closest configured framework check.
