---
name: create-agents-md
description: Create or update repository AGENTS.md files that give AI coding agents concise, repo-specific operating instructions. Use when the user asks to generate, improve, audit, or align AGENTS.md with project structure, build/test commands, coding conventions, security notes, commit/PR practices, monorepo scoped instructions, or the public agents.md recommendations.
---

# Create AGENTS.md

## Overview

Create a clear English `AGENTS.md` that helps coding agents work safely and efficiently in the current repository. Prefer compact, evidence-based guidance over generic contributor prose.

## Workflow

1. Inspect the repository before writing:
   - Read existing `AGENTS.md`, `README*`, contribution docs, package/build files, CI workflows, formatter/linter configs, test configs, and recent commit messages.
   - When drafting coding or testing guidance, read `references/product-engineering-baseline.md` for the default engineering principles to adapt.
   - Use fast file discovery (`rg --files`) and targeted reads. Do not infer commands when repository files expose them.
   - In a monorepo, create nested `AGENTS.md` files only when subdirectories have independent manifests, toolchains, commands, or conventions that would make one root file ambiguous.
2. Draft or update `AGENTS.md`:
   - If no file exists, create a root `AGENTS.md`; if one exists, edit it in place.
   - Write in English unless the user explicitly requests another language.
   - Keep the root file about 200-400 words when feasible.
   - Use Markdown headings and concise bullets.
   - Make every instruction specific to this repository; omit sections that would be filler.
   - Distinguish repository facts from engineering defaults. Local configs, nearby code, existing architecture, and explicit user instructions override the baseline.
3. Preserve useful existing instructions:
   - Merge existing project-specific rules instead of replacing them blindly.
   - Remove stale commands only when repository evidence shows better current commands.
   - When evidence is missing, omit the claim or state that no convention is documented; do not invent coverage targets, naming rules, or VCS policy.
4. Validate the result:
   - Check that listed commands, paths, and package names match files in the repository.
   - If commands are cheap and safe, run the most relevant verification command or explain why it was not run.

## Recommended Content

Use these sections when applicable:

- `Project Structure & Module Organization`: source, tests, resources, apps/packages, generated files, and important config directories.
- `Build, Test, and Development Commands`: exact commands with one short explanation each.
- `Coding Style & Naming Conventions`: language versions, formatting/linting, naming patterns, framework conventions, and where config lives.
- `Engineering Principles`: concise defaults from `references/product-engineering-baseline.md`, adapted to the repository. Include only rules that help agents make code changes safely; do not paste the full baseline.
- `Testing Guidelines`: test framework, test file naming, focused test commands, coverage expectations when discoverable, edge-case expectations, and when to add tests.
- `Commit & Pull Request Guidelines`: summarize recent commit style from `git log` when available and consistent; describe PR body, issue links, screenshots, migrations, or checklist expectations.
- `Security & Configuration Notes`: secrets handling, env files, credentials, generated artifacts, destructive operations, and local-only data.
- `Agent-Specific Instructions`: repo-specific boundaries such as avoiding vendored files, preserving generated code policy, or running formatters before final response.

## Quality Bar

- Prefer actionable commands and paths: `npm test`, `./gradlew test`, `src/`, `tests/`, `.github/workflows/`.
- Avoid generic statements like "write clean code" unless tied to a local rule.
- Avoid dogmatic rules that are unsafe across repositories. Phrase baseline principles as defaults unless repository evidence makes them strict.
- Include change-hygiene rules when useful: no junk files, temporary debug output, unused code, accidental formatting, duplicate implementations, or weakened tests.
- Avoid duplicating long README content. Point to existing docs when they are the authoritative source.
- Use standard Markdown only; `AGENTS.md` has no required schema or fields.
- Make precedence explicit if multiple `AGENTS.md` files exist: the nearest file to the edited path should contain the most specific instructions.
- Treat `AGENTS.md` as living documentation; update it when commands or conventions change.

## Reference

For a compact checklist and draft template, read `references/agents-md-guide.md` when creating or substantially rewriting a file.
For product-engineering defaults, read `references/product-engineering-baseline.md` and adapt it to repository evidence.
