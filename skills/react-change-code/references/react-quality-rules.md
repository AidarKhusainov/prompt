# React Quality Rules

Read this file when a change touches React components, hooks, JSX/TSX, forms, state, context, refs, effects, accessibility, rendering behavior, component libraries, or React tests.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Version-sensitive practice

- Inspect installed `react` and `react-dom` versions before using modern APIs.
- Do not use newer React APIs unless the installed version and framework support them.
- Preserve Strict Mode behavior and existing hook/lint rules.
- Do not enable React Compiler or add compiler-specific directives unless the project already uses it or the task explicitly requires it.
- Prefer repository-local patterns over generic examples when they are safe and current enough.

## Components and rendering

- Keep components pure; do not perform side effects, subscriptions, random/date generation, storage access, DOM mutation, navigation, analytics, or network calls during render.
- Treat props, state, hook arguments, and JSX values as immutable snapshots.
- Use components through JSX; do not call component functions directly.
- Keep components focused. Split only when it improves ownership, reuse, readability, testability, or server/client boundaries.
- Preserve public props, exported names, class names/data attributes used by tests, and design-system contracts unless explicitly requested.
- Prefer semantic HTML before custom ARIA.
- Preserve loading, empty, disabled, pending, error, and success states.
- Avoid hydration mismatches from request-, browser-, random-, date-, or locale-dependent values.

## Hooks

- Follow the Rules of Hooks.
- Do not call hooks conditionally, in loops, after early returns, in callbacks, in async functions, or at module scope.
- Keep custom hooks named with the `use` prefix and make dependencies explicit.
- Keep dependency arrays correct; do not silence `exhaustive-deps` by default.
- Prefer event handlers for user-triggered side effects and effects for synchronization with external systems.
- Do not use effects for derived state that can be calculated during render.
- Clean up subscriptions, timers, observers, event listeners, and async work.
- Use memoization only when it solves a real stability or performance need or matches local style.

## State and data flow

- Keep local state minimal. Derive values from props/state during render when possible.
- Avoid duplicating server data in local state unless the UI needs optimistic, draft, or staged state.
- Prefer colocated state unless state must be shared or survive route/layout boundaries.
- Use existing state/data libraries and provider patterns before adding new ones.
- Model meaningful async UI states explicitly.
- Avoid global mutable state and unsafe browser singleton caches.
- Use functional state updates when next state depends on previous state.

## Forms and mutations

- Use controlled inputs when value drives rendering or validation; use uncontrolled inputs when simpler and consistent with the project.
- Preserve labels, descriptions, error messages, focus behavior, disabled state, validation timing, and submit behavior.
- Prevent double-submit bugs with pending state, disabled controls, idempotency, or server safeguards when relevant.
- Validate again on the server for untrusted input.
- Preserve existing mutation patterns such as event handlers, React Query/TanStack Query, SWR, Redux, tRPC, or form libraries.

## Accessibility

- Preserve or improve semantic structure, accessible names, labels, headings, landmark regions, focus order, keyboard behavior, and screen-reader feedback.
- Interactive elements must be reachable and operable by keyboard.
- Use buttons for actions and links for navigation unless there is a deliberate accessibility reason.
- Keep focus visible and manage focus intentionally when the UI requires it.
- Associate form controls with labels and errors.
- Announce async status changes when not visually obvious.
- Do not rely on color alone to communicate state.
- Respect reduced-motion preferences for non-essential animation.

## Performance

- Avoid unnecessary global providers, broad context values, and expensive computations on every render.
- Split context or memoize provider values when re-render scope matters.
- Prefer stable keys from data IDs; avoid array indexes when order can change.
- Do not generate random keys or IDs during render. Use `useId` for stable accessibility IDs when appropriate.
- Move heavy work out of client render paths when the repository architecture supports it.

## Security and privacy

- Treat user input, URL params, search params, form data, browser storage, server payloads, and third-party data as untrusted.
- Do not use `dangerouslySetInnerHTML` unless content is sanitized by a trusted project-approved path.
- Do not expose secrets, tokens, private environment variables, internal endpoints, or sensitive payloads in browser code.
- Avoid logging personal data, tokens, cookies, session data, or sensitive form payloads.
- Preserve auth, authorization, tenant isolation, CSRF, CORS, CSP, and cookie behavior.

## Styling and design systems

- Follow the project's styling approach.
- Prefer existing design-system primitives and tokens over one-off styling.
- Avoid visual regressions from broad class reordering, reset changes, or global CSS changes.
- Preserve responsive behavior and dark/light theme support when present.

## Testing guidance

- Test user-observable behavior rather than implementation details.
- Prefer queries by role, label, text, placeholder, or accessible name.
- Use test IDs only for stable non-accessible elements or when local style requires them.
- Test loading, error, empty, disabled, pending, keyboard, and validation states when behavior changes.
- Avoid snapshot-only coverage for behavior changes.

See `frontend-testing-rules.md` for detailed testing rules.
