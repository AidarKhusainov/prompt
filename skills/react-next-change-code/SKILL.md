---
name: react-next-change-code
description: Compatibility router for older integrations that request React or Next.js repository work. Prefer react-change-code for React-specific UI/components/hooks/tests and next-change-code for Next.js-specific routing/runtime/cache/server-client behavior.
---

# React and Next.js Compatibility Router

## Purpose

Keep the old `react-next-change-code` entry point working while the skill tree is split into narrower layers.

Do not add new detailed rules here. Add React-specific rules to `react-change-code` and Next-specific rules to `next-change-code`.

## Route to `react-change-code` when work touches

- React components, hooks, providers, forms, refs, effects, context, state, or JSX rendering.
- Accessibility, keyboard behavior, focus handling, pending/error/empty states.
- React component tests, hook tests, React Testing Library, or Storybook configured for React.
- React UI inside Vite, CRA, Remix UI files, design systems, shared component packages, or ordinary Next.js UI with no Next-specific behavior.

## Route to `next-change-code` when work touches

- App Router or Pages Router files and behavior.
- Layouts, pages, loading/error/not-found/template files, route groups, route handlers, or API routes.
- Server Components, Client Components, server/client boundaries, Server Functions, or Server Actions.
- Next.js caching, revalidation, static/dynamic rendering, metadata, sitemap/robots, images/fonts, middleware/proxy, runtime, redirects, rewrites, or framework build behavior.

## Route to `js-ts-change-code` instead when work touches

- Generic JS/TS utilities.
- Package scripts or build tooling.
- Node.js workers, CLIs, backend services, codegen, or shared non-React utilities.
- JS/TS tests that are not React/Next-specific.

## Negative routing rules

Do not use React/Next rules only because:

- a file extension is `.tsx` or `.jsx`;
- a monorepo contains React or Next somewhere;
- a file is named `middleware.ts` but has no Next evidence;
- the task touches Preact, Solid, Vue, Svelte, Angular, Astro-only, MDX-only, or another non-React JSX runtime.

## Reference loading policy

This compatibility router should not load large reference files itself.

- For React behavior, apply `react-change-code` and its references.
- For Next.js behavior, apply `next-change-code` and its references.
- For generic JS/TS behavior, apply `js-ts-change-code` and its references.

If the platform cannot activate another skill at runtime, use the routing decision above and follow the selected skill by instruction.

## Verification and final response

Use the selected skill's verification and final-response rules.
