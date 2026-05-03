# Frontend Testing Rules

Read this file before adding or changing React, Next.js, browser, component, integration, Storybook, Playwright, Cypress, or frontend data-layer tests.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Test strategy

- Use the repository's existing test stack, helpers, providers, mock servers, fixtures, and naming conventions.
- Prefer the smallest test that proves the changed user-observable behavior.
- Use unit tests for pure functions, formatters, reducers, validators, and state transitions.
- Use component tests for rendering, props, user interaction, forms, accessibility-facing states, and provider wiring.
- Use integration tests for routing, data loading, route handlers, server/client interactions, auth boundaries, cache invalidation, and important cross-component flows.
- Use e2e tests for critical browser workflows, navigation, real form flows, auth flows, and behavior that requires a real browser.
- Do not add a new testing framework when a suitable existing path exists.
- Do not move ordinary component behavior into slow e2e tests when a fast component test is enough.

## User-observable assertions

- Test behavior the user can observe: text, roles, labels, state, validation messages, navigation, enabled/disabled controls, focus, and requests/responses at stable boundaries.
- Prefer Testing Library queries by role, label, placeholder, text, display value, or accessible name.
- Use test IDs only when no semantic query is appropriate or the project standard requires them.
- Avoid testing private component state, hook call counts, implementation-specific class names, DOM structure, or internal helper calls unless they are the public contract.
- Avoid snapshot-only tests for behavior changes. Use snapshots only for stable, reviewable structure or generated output.

## Accessibility coverage

When behavior affects UI, consider tests for:

- accessible names and labels;
- keyboard navigation and activation;
- focus movement and focus restoration;
- error message association;
- modal/dialog/popup behavior;
- live regions or status announcements;
- disabled and pending states.

Do not assert inaccessible behavior as acceptable unless the user explicitly requested a temporary migration path and the limitation is documented.

## Async UI and data loading

- Await the UI update, network result, event, timer, or side effect that matters.
- Prefer `findBy*`, `waitFor`, user-event promises, and framework-specific helpers over arbitrary sleeps.
- Use fake timers only when the code is timer-driven and the repository already uses that style.
- Test loading, empty, success, validation-error, and server-error states when the behavior changes.
- Avoid tests that pass because promises are left unawaited.
- Do not increase timeouts to hide race conditions.

## Mocks and fixtures

- Mock at stable side-effect boundaries: network, storage, browser APIs, dates, randomness, router, auth/session, and external services.
- Prefer MSW or the repository's existing request-mocking layer for browser/API interactions.
- Keep fixtures realistic but small. Include edge cases that triggered the bug or requirement.
- Do not deeply mock component internals just to force an implementation path.
- Reset mocks, timers, local storage, session storage, cookies, DOM state, and module state between tests when they can leak.
- Use deterministic dates, IDs, and random values when assertions depend on them.

## React component tests

- Render with the same providers, theme, router, i18n, data clients, and feature flags that production components require.
- Prefer `userEvent` over low-level fire events when testing user interactions.
- Test controlled/uncontrolled input behavior according to the component contract.
- Verify disabled, pending, validation, and optimistic states where relevant.
- Do not assert hook implementation details when the component behavior is enough.
- For custom hooks, prefer testing through a small component or the repository's hook-testing pattern.

## Next.js tests

- For App Router components, respect Server Component and Client Component boundaries in tests.
- Test route handlers as request/response units when possible: method, URL params, query, headers, cookies, body, status, response shape, and errors.
- For server actions/functions, test validation, authorization, mutation behavior, cache invalidation intent, redirects, and error mapping when local patterns support it.
- For pages/layouts/routes, include build/typecheck verification when tests cannot fully model Next.js behavior.
- Mock Next navigation, headers, cookies, image, font, and router APIs only through existing project helpers or stable test utilities.
- Do not make App Router code pass tests by turning large trees into Client Components.

## E2E tests

- Keep e2e tests focused on critical user journeys and framework/browser behavior.
- Prefer stable user-facing selectors and roles over fragile CSS selectors.
- Avoid fixed sleeps; wait for UI state, route changes, network-idle only when meaningful, or explicit app signals.
- Keep test data isolated and cleanup reliable.
- Do not require external production services or real credentials unless the repository already has a safe test environment.
- For visual assertions, use existing screenshot/visual-regression tooling and thresholds.

## Coverage and regression

- Add regression coverage for fixed bugs.
- Cover boundary values, empty input, invalid input, missing data, and permission failures when relevant.
- Avoid chasing coverage percentage with low-value assertions.
- Do not delete or weaken existing tests unless behavior intentionally changed and the new expectation is covered.

## Verification commands

Prefer package scripts and module-scoped commands. Examples, adapt to the repository:

- `pnpm test -- <path>`
- `pnpm --filter <package> test -- <path>`
- `npm test -- <path>`
- `yarn test <path>`
- `bun test <path>`
- `pnpm exec vitest run <path>`
- `pnpm exec jest <path>`
- `pnpm exec playwright test <spec>`
- `pnpm exec cypress run --spec <spec>`

Run typecheck, lint, and build when the change touches TypeScript contracts, routing, server/client boundaries, framework config, public components, or production behavior.

Do not claim checks passed unless the commands completed successfully.
