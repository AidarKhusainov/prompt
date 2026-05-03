# React Quality Rules

Read this file when a change touches React components, hooks, JSX/TSX, forms, state, context, refs, effects, accessibility, rendering behavior, component libraries, or React tests.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Version-sensitive practice

- Inspect the installed `react` and `react-dom` versions before using modern APIs.
- Do not use React 19+ APIs such as `useActionState`, `useOptimistic`, Action props, or `use` unless the installed version and framework support them.
- Do not use React 19.2+ APIs or tooling such as `<Activity />`, `useEffectEvent`, `cacheSignal`, React Performance Tracks, or `eslint-plugin-react-hooks` v6 unless those versions are installed and the project already uses or accepts those patterns.
- Do not enable React Compiler, change compiler configuration, or add compiler-specific directives unless the project already uses it or the task explicitly requires it.
- Preserve Strict Mode behavior and existing lint rules. Do not weaken `eslint-plugin-react-hooks` or framework lint configuration.
- Prefer repository-local patterns over generic examples when they are safe and current enough.

## Components and rendering

- Keep components pure: do not perform side effects, subscriptions, random value generation, date/time generation, storage access, DOM mutation, navigation, analytics, or network calls during render.
- Treat props, state, hook arguments, and values passed to JSX as immutable snapshots.
- Use components through JSX; do not call component functions directly.
- Keep components focused. Split only when it improves ownership, reuse, readability, testability, or server/client boundaries.
- Preserve public component props, exported names, class names used by tests, data attributes used by tests, and design-system contracts unless explicitly requested.
- Prefer semantic HTML before custom ARIA. Add ARIA only when native semantics are insufficient.
- Preserve loading, empty, disabled, pending, error, and success states when modifying UI flows.
- Avoid hydration mismatches: do not render request-, browser-, random-, date-, or locale-dependent values differently on server and client unless intentionally gated.

## Hooks

- Follow the Rules of Hooks: call hooks only at the top level of React function components or custom hooks.
- Do not call hooks conditionally, in loops, after early returns, in callbacks, in async functions, or at module scope. The React `use` API is an exception only when supported by the installed version and framework.
- Keep custom hooks named with the `use` prefix and make their dependencies explicit.
- Do not pass hooks as values, dynamically wrap hooks, or create higher-order hooks that obscure hook calls.
- Keep dependency arrays correct. Do not silence `exhaustive-deps` by default; restructure code or stabilize values when needed.
- Prefer event handlers for user-triggered side effects and effects for synchronization with external systems.
- Do not use `useEffect` for derived state that can be calculated during render.
- Clean up subscriptions, timers, observers, event listeners, and async work in effects.
- Avoid broad memoization. Use `useMemo`, `useCallback`, and `memo` only when they solve a measured or likely rendering problem, preserve referential stability required by children/hooks, or match local style.

## State and data flow

- Keep local state minimal. Derive values from props/state during render when possible.
- Avoid duplicating server data in local state unless the UI needs optimistic, draft, or staged state.
- Prefer colocated state unless state is shared across distant components or must survive route/layout boundaries.
- Use existing state/data libraries and provider patterns before adding new ones.
- Model meaningful async UI states explicitly: idle, loading, pending, success, empty, error, and optimistic states when relevant.
- Avoid global mutable state, module-level caches, and singleton clients in browser code unless the project already owns that pattern safely.
- For concurrent updates, use functional state updates when next state depends on previous state.

## Forms and mutations

- Use controlled inputs when the current value drives rendering or validation; use uncontrolled inputs when simpler and consistent with the project.
- Preserve labels, descriptions, error messages, focus behavior, disabled state, validation timing, and submit behavior.
- Prevent double-submit bugs with pending state, disabled submit controls, idempotency, or server-side safeguards when relevant.
- Keep validation close to the boundary that owns the data. Validate again on the server for untrusted input.
- For React 19+ forms/actions, prefer `useActionState`, Action props, and `useOptimistic` only when the installed stack supports them and the project uses or accepts that pattern.
- For older React stacks, preserve the existing mutation pattern such as event handlers, React Query/TanStack Query, SWR, Redux, tRPC, or form libraries.

## Accessibility

- Preserve or improve semantic structure, accessible names, labels, headings, landmark regions, focus order, keyboard behavior, and screen-reader feedback.
- Interactive elements must be reachable and operable by keyboard.
- Use buttons for actions and links for navigation unless there is a deliberate accessibility reason.
- Keep focus visible. Manage focus intentionally after modals, popovers, route transitions, validation errors, or async submissions when the UI requires it.
- Associate form controls with labels and errors.
- Announce async status changes when they are not visually obvious.
- Do not rely on color alone to communicate state.
- Respect reduced-motion preferences for non-essential animation.

## Performance

- Avoid unnecessary global providers, broad context values, and expensive computations on every render.
- Split context or memoize provider values when re-render scope matters.
- Prefer stable keys from data IDs; do not use array indexes as keys when order can change.
- Do not generate random keys or IDs during render. Use `useId` for stable accessibility IDs when appropriate.
- Defer heavy work, lazy-load large client-only UI, or move computation/server work out of client components when the repository architecture supports it.
- Avoid unnecessary polling, timers, layout thrashing, and synchronous browser storage access during render.

## Security and privacy

- Treat user input, URL params, search params, form data, browser storage, server payloads, and third-party data as untrusted.
- Do not use `dangerouslySetInnerHTML` unless the content is sanitized by a trusted project-approved path.
- Do not expose secrets, tokens, private environment variables, internal endpoints, or sensitive payloads in browser code.
- Avoid logging personal data, tokens, cookies, session data, or sensitive form payloads.
- Preserve auth, authorization, tenant isolation, CSRF, CORS, CSP, and cookie behavior.

## Styling and design systems

- Follow the project's styling approach: CSS Modules, Tailwind, CSS-in-JS, Sass, design tokens, or component library APIs.
- Prefer existing design-system primitives and tokens over one-off styling.
- Avoid visual regressions from broad class reordering, reset changes, or global CSS changes.
- Keep responsive behavior and dark/light theme support intact when present.

## Testing guidance

- Test user-observable behavior rather than implementation details.
- Prefer queries by role, label, text, placeholder, or accessible name over test IDs when practical.
- Use test IDs only for stable non-accessible elements or when local style already requires them.
- Test loading, error, empty, disabled, pending, keyboard, and form validation states when behavior changes.
- Avoid snapshot-only coverage for behavior changes.

See `frontend-testing-rules.md` for detailed testing rules.
