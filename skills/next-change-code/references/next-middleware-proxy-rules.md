# Next.js Middleware and Proxy Rules

Read this file when a change touches Next.js `middleware.*`, `proxy.*`, matcher config, auth redirects, rewrites, request headers, cookies, locale handling, or URL normalization at the Next edge/proxy layer.

## Applicability

Use these rules only with Next.js evidence:

- `next` dependency in the owning package;
- `next/server` imports;
- file located at app root or `src` root;
- nearby Next route structure or config.

Do not treat `middleware.*` alone as Next evidence.

## Rules

- Treat middleware/proxy as security- and routing-sensitive.
- Preserve matcher patterns, auth checks, redirects, rewrites, headers, cookies, locale handling, and URL normalization unless explicitly requested.
- For projects that already use `proxy.ts`, follow proxy naming and runtime constraints for the installed Next.js version.
- For older middleware files, inspect installed Next.js version before assuming Edge or Node runtime behavior.
- If existing middleware relies on Edge runtime behavior, do not migrate it to `proxy.ts` unless installed Next.js version and deployment target support the same behavior.
- Do not rename middleware/proxy files or change skip flags just for style.
- Do not add heavy work, database calls, unsupported runtime APIs, or sensitive logging to middleware/proxy.
- Preserve auth/session, tenant isolation, CSRF/CORS/CSP interactions, cookie flags, and security headers.

## Verification

Prefer tests around matcher behavior, redirects, rewrites, headers, cookies, and auth outcomes when local patterns support them. Otherwise run typecheck plus build or the closest configured Next.js check.
