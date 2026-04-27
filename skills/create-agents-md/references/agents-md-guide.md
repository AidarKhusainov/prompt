# AGENTS.md Guide

## Checklist

- Place the main file at the repository root as `AGENTS.md`.
- Use nested `AGENTS.md` files for monorepos or subprojects with different commands, languages, or conventions; otherwise keep one root file.
- Use standard Markdown headings and bullets. Do not add custom schema frontmatter unless the user explicitly asks.
- Keep instructions agent-focused: setup, build, test, style, security, VCS workflow, and project-specific boundaries.
- Prefer verified repository evidence over assumptions from common frameworks.
- Keep the document concise enough for frequent context loading.
- Ensure explicit user instructions override `AGENTS.md`, and the nearest nested `AGENTS.md` overrides broader root guidance.

## Discovery Commands

Run only the commands that fit the repository:

```bash
rg --files -g 'AGENTS.md' -g 'README*' -g 'CONTRIBUT*' -g 'package.json' -g 'pom.xml' -g 'build.gradle*' -g 'pyproject.toml' -g 'Cargo.toml' -g 'go.mod' -g 'Makefile' -g '.github/workflows/*'
git log --oneline -n 20
```

Look for scripts in package manifests, Gradle/Maven tasks, Make targets, CI jobs, test directories, linter/formatter configs, env examples, Docker Compose files, and deployment docs. If git history is unavailable or inconsistent, do not claim a commit convention.

## Draft Template

```markdown
# Repository Guidelines

## Project Structure & Module Organization
- Describe where source, tests, resources, config, docs, and generated files live.

## Build, Test, and Development Commands
- `command`: Explain exactly what it does and when to use it.

## Coding Style & Naming Conventions
- State formatter/linter, indentation if explicit, naming conventions, and framework patterns.

## Testing Guidelines
- Name test framework, test locations, naming pattern, focused run commands, and expectations for changed code.

## Commit & Pull Request Guidelines
- Summarize observed commit style and PR requirements.

## Security & Configuration Notes
- Document secrets, env files, credentials, data handling, and dangerous operations.
```

Delete unused sections. Add project-specific sections only when they carry useful instructions.
