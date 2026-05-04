# Next.js Cache and Runtime Rules

Read this file when a change touches caching, revalidation, static/dynamic rendering, route segment config, runtime target, deployment behavior, or performance-sensitive data loading.

## Caching and rendering mode

- Treat caching and rendering mode as public behavior. Do not change them casually.
- Before editing, identify whether the route is static, dynamic, partially prerendered, cache-component based, or legacy cache-model based.
- Preserve existing `fetch` cache options, `next.revalidate`, `next.tags`, route segment config, `dynamic`, `revalidate`, `fetchCache`, `runtime`, and `preferredRegion` unless the task requires a change.
- Use newer cache APIs only when installed Next.js version, config, and local patterns support them.
- Do not force a Cache Components migration when the app uses the previous cache model.
- Prefer tag-based revalidation over path-based revalidation when cache ownership is clear.
- Avoid over-invalidating broad paths or root layouts unless the task requires it.
- Consider `cookies`, `headers`, `searchParams`, and request-specific APIs rendering-mode-sensitive.

## Revalidation

- Choose revalidation APIs and signatures supported by the installed Next.js version.
- Do not add deprecated or version-incompatible `revalidateTag` calls.
- Use `updateTag` only when the installed version supports it and the local codebase uses that model.
- Never use Server Action-only APIs from Route Handlers.
- Revalidate only after successful mutations when cached UI depends on changed data.

## Runtime and deployment

- Do not switch Node.js/Edge runtime unless explicitly required and verified.
- Keep runtime compatibility in mind: Node.js APIs are not available in Edge runtime.
- Preserve deployment hints, region preferences, route segment config, and environment assumptions unless the task requires a change.
- Do not introduce filesystem, database, crypto, streaming, or dependency behavior unsupported by the selected runtime.

## Verification

For cache/runtime changes, prefer typecheck plus build or the closest configured Next.js framework check. Add targeted tests when local patterns support them.
