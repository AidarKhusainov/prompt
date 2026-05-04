# Next.js Project Detection Rules

Read this file when a task may be Next.js-specific or when the router/runtime/version is unclear.

## Strong Next.js signals

- `next` in the owning package's `package.json`.
- `next.config.*`.
- App Router files under `app/` or `src/app/`: `layout.*`, `page.*`, `loading.*`, `error.*`, `not-found.*`, `template.*`, `route.*`.
- Pages Router files under `pages/` or `src/pages/`: `_app.*`, `_document.*`, `getServerSideProps`, `getStaticProps`, API routes.
- `middleware.*` or `proxy.*` only when located at the app root or `src` root and paired with `next` dependency, `next/server` imports, or nearby Next route structure.

Do not treat file names alone as Next.js evidence.

## Version-sensitive practice

- Inspect installed `next`, `react`, and `react-dom` versions before using version-sensitive APIs.
- Detect App Router, Pages Router, or mixed migration. Do not migrate router systems unless explicitly requested.
- Use App Router rules for files under `app/` or `src/app/`.
- Use Pages Router rules for files under `pages/` or `src/pages/`.
- Do not assume `next lint` exists. Prefer configured package scripts or ESLint directly when the repo uses that pattern.
- Do not enable Cache Components, PPR, new proxy conventions, route segment config, or runtime changes unless installed versions and local config support them.

## Inspect when relevant

- `package.json`, lockfile, workspace config, and package scripts.
- `next.config.*`, `tsconfig.json`, `jsconfig.json`, ESLint config, env templates, and CI workflows.
- Router directories and route segment files.
- `middleware.*` or `proxy.*` files and matcher config.
- Metadata, sitemap/robots, image/font config, server-only/client-only imports, and deployment runtime hints.

Prefer closest package/module-level config in monorepos.
