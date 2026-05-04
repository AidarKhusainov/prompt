# Skill Authoring Guide

Use this guide when adding or refactoring skills.

## Goal

Keep runtime context small while making the skill tree easy to extend.

Preferred shape:

```text
router skill
  -> language skill
    -> framework skill
      -> narrow reference files
```

Example:

```text
change-code
  -> js-ts-change-code
    -> react-change-code
      -> next-change-code when Next-specific behavior is involved
    -> vue-change-code in the future
      -> nuxt-change-code when Nuxt-specific behavior is involved
```

## Rules

- Keep `SKILL.md` short. It should contain trigger conditions, negative triggers, routing, reference-loading policy, workflow mode, and verification policy.
- Put detailed rules in `references/`.
- Every reference file must have an explicit condition for when to read it.
- Prefer one small reference per concern over one large framework reference.
- Do not copy shared safety, workflow, verification, and final-response rules into every skill unless needed for standalone execution.
- Use compatibility routers when renaming or splitting existing skills.
- Do not route by repository dominant language. Route by the files and behavior that actually change.
- Do not treat file extension alone as framework evidence. For example, `.tsx` alone is not React evidence.
- Add positive and negative routing evals for every new framework skill.
- Add reference-loading evals for token-sensitive skills.

## Token budget guidance

Aim for these rough sizes:

- Router `SKILL.md`: 100-180 lines.
- Language `SKILL.md`: 120-220 lines.
- Framework `SKILL.md`: 80-180 lines.
- Reference file: one concern, ideally under 150 lines.

Do not force these limits when safety or correctness requires more detail, but treat large files as a smell.

## Adding a new JS framework skill

For a new framework such as Vue:

1. Keep generic JS/TS rules in `js-ts-change-code`.
2. Create `vue-change-code` only for Vue-specific components, templates, reactivity, composables, accessibility, and tests.
3. Create `nuxt-change-code` only for Nuxt-specific routing, SSR, server routes, data fetching, middleware, runtime, and deployment behavior.
4. Add negative evals for React, Svelte, Solid, Preact, Astro-only, Node workers, and package tooling.
5. Add reference-loading evals so generic JS/TS tasks do not load Vue/Nuxt rules.

## Compatibility

When splitting an existing skill:

- Keep the old skill name as a router for at least one migration cycle.
- Update README and routing references.
- Prefer adding new skills over deleting old paths immediately.
- Mark old paths as compatibility-only rather than stale.
