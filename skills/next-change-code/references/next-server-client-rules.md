# Next.js Server and Client Rules

Read this file when a change touches Server Components, Client Components, Server Functions, Server Actions, forms, server-only code, client-only code, or serialization boundaries.

## Server and Client Components

- In App Router, keep components server-side by default.
- Add `'use client'` only when the file needs state, effects, event handlers, refs tied to browser behavior, browser APIs, client-only libraries, context providers using client state, or React client hooks.
- Keep client boundaries small and close to the interactive leaf component.
- Once a module is marked `'use client'`, its imports are part of the client module graph.
- Do not import server-only code into Client Components.
- Do not pass non-serializable props from Server Components to Client Components.
- Do not import database clients, filesystem access, private environment variables, auth server helpers, or server-only modules into Client Components.
- Wrap third-party browser-only components in small Client Components instead of marking a whole route or layout as client.
- Do not add hooks such as `useState`, `useEffect`, `useReducer`, `useRef`, `useSearchParams`, or client router hooks to Server Components.
- Avoid hydration mismatches from browser-only values, random IDs, dates, time zones, locale formatting, media queries, and storage reads during server render.

## Data fetching and server work

- Prefer server-side data fetching in Server Components when data is needed for initial render and does not require client interactivity.
- Keep secrets and privileged operations on the server.
- Validate untrusted input from params, search params, cookies, headers, forms, route handlers, webhooks, and third-party callbacks.
- Preserve existing auth/session and tenant-isolation checks.
- Use existing project data libraries and request helpers before adding new ones.
- Preserve redirect and not-found behavior when changing data loading.
- Do not fetch sensitive data in Client Components just to avoid server/client boundaries.

## Server Functions, Server Actions, and forms

- Use Server Functions only when supported by installed Next.js and React versions and consistent with the repository.
- Use Server Actions for mutation/action flows, especially forms, only when installed stack and local conventions support them.
- Keep mutation code server-side and validate all input on the server.
- Ensure mutations have authorization checks, idempotency or double-submit safeguards where relevant, and safe error handling.
- Revalidate or update cache entries after mutations when the UI depends on cached data.
- Use redirects intentionally after successful mutations when that matches user flow.
- Do not pass secrets or privileged objects through action arguments or serialized props.
- Preserve progressive enhancement when the app relies on it.
- Model pending, optimistic, success, validation-error, and server-error states explicitly.

## TypeScript boundaries

- Preserve route param types, search param types, generated route types, and public exported types unless explicitly requested.
- Do not weaken `tsconfig`, disable strictness, or add broad assertions to bypass framework type errors.
- Follow local path aliases and module boundaries.
