# Frontend Testing Rules

Read this file before adding or changing React, browser, component, integration, Storybook, Playwright, Cypress, or frontend data-layer tests.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Test strategy

- Use the repository's existing test stack, helpers, providers, mock servers, fixtures, and naming conventions.
- Prefer the smallest test that proves changed user-observable behavior.
- Use unit tests for pure functions, formatters, reducers, validators, and state transitions.
- Use component tests for rendering, props, user interaction, forms, accessibility-facing states, and provider wiring.
- Use integration tests for routing, data loading, auth boundaries, and important cross-component flows.
- Use e2e tests for critical browser workflows and behavior requiring a real browser.
- Do not add a new testing framework when a suitable path exists.

## User-observable assertions

- Test behavior the user can observe: text, roles, labels, state, validation messages, navigation, enabled/disabled controls, focus, and stable request/response boundaries.
- Prefer Testing Library queries by role, label, placeholder, text, display value, or accessible name.
- Use test IDs only when no semantic query is appropriate or the project standard requires them.
- Avoid testing private state, hook call counts, fragile DOM structure, implementation-specific class names, or internal helper calls unless they are the public contract.
- Avoid snapshot-only tests for behavior changes.

## Accessibility coverage

When behavior affects UI, consider tests for:

- accessible names and labels;
- keyboard navigation and activation;
- focus movement and focus restoration;
- error message association;
- dialog/popup behavior;
- live regions or status announcements;
- disabled and pending states.

## Async UI and data loading

- Await the UI update, network result, event, timer, or side effect that matters.
- Prefer `findBy*`, `waitFor`, user-event promises, and framework helpers over sleeps.
- Use fake timers only when the code is timer-driven and the repository already uses that style.
- Test loading, empty, success, validation-error, and server-error states when behavior changes.
- Avoid tests that pass because promises are left unawaited.
- Do not increase timeouts to hide race conditions.

## Mocks and fixtures

- Mock at stable side-effect boundaries: network, storage, browser APIs, dates, randomness, router, auth/session, and external services.
- Prefer MSW or the repository's existing request-mocking layer for browser/API interactions.
- Keep fixtures realistic but small.
- Reset mocks, timers, storage, cookies, DOM state, and module state between tests when they can leak.
- Use deterministic dates, IDs, and random values when assertions depend on them.

## React component tests

- Render with the same providers, theme, router, i18n, data clients, and feature flags that production components require.
- Prefer `userEvent` over low-level fire events.
- Test controlled/uncontrolled input behavior according to the component contract.
- Verify disabled, pending, validation, and optimistic states where relevant.
- Do not assert hook implementation details when component behavior is enough.
- For custom hooks, prefer testing through a small component or the repository's hook-testing pattern.

## E2E tests

- Keep e2e tests focused on critical user journeys and framework/browser behavior.
- Prefer stable user-facing selectors and roles over fragile CSS selectors.
- Avoid fixed sleeps; wait for UI state, route changes, or explicit app signals.
- Keep test data isolated and cleanup reliable.
- Do not require external production services or real credentials unless the repository already has a safe test environment.

## Coverage and regression

- Add regression coverage for fixed bugs.
- Cover boundary values, empty input, invalid input, missing data, and permission failures when relevant.
- Do not delete or weaken existing tests unless behavior intentionally changed and the new expectation is covered.

## Verification commands

Prefer package scripts and module-scoped commands. Adapt examples to the repository:

- `pnpm test -- <path>`
- `pnpm --filter <package> test -- <path>`
- `npm test -- <path>`
- `yarn test <path>`
- `bun test <path>`
- `pnpm exec vitest run <path>`
- `pnpm exec jest <path>`
- `pnpm exec playwright test <spec>`
- `pnpm exec cypress run --spec <spec>`

Run typecheck, lint, and build when the change touches TypeScript contracts, routing, framework config, public components, or production behavior.

Do not claim checks passed unless commands complete successfully.
