# Bash and Shell Quality Rules

Read this file when a change touches Bash, POSIX `sh`, Zsh scripts, Makefile shell snippets, CI shell steps, install scripts, deployment scripts, or code that generates shell commands.

Follow these rules unless the user explicitly asks for something different or the repository has stronger local guidance.

## Shell detection

Before editing, determine the intended shell:

- Read the shebang: `#!/usr/bin/env bash`, `#!/bin/bash`, `#!/bin/sh`, `#!/usr/bin/env zsh`.
- Check how the script is invoked from README, Makefile, package scripts, CI, Dockerfile, or other scripts.
- Inspect ShellCheck directives and existing style.
- If the script is POSIX `sh`, do not introduce Bash-only features.
- If there is no shebang, infer from the caller and nearby scripts before editing.

## Basic style

- Prefer clear, boring shell over clever one-liners.
- Keep scripts small and focused. Extract functions when it improves readability or reuse.
- Use meaningful variable and function names.
- Prefer explicit arguments over hidden global variables.
- Keep output predictable for humans and callers.
- Preserve documented flags, environment variables, stdout/stderr behavior, and exit codes.
- Avoid unrelated formatting churn.

## Safety options

- Use `set -euo pipefail` for Bash scripts when it is compatible with existing control flow.
- For POSIX `sh`, do not use `pipefail` unless the target shell supports it.
- Do not add `set -e` blindly to scripts that intentionally handle non-zero statuses.
- Use explicit error handling where `set -e` behavior would be surprising.
- Use `trap` for cleanup when creating temporary files or modifying external state.
- Preserve existing traps and cleanup behavior.

## Quoting and word splitting

- Quote variable expansions by default: `"$var"`.
- Quote command substitutions by default: `"$(cmd)"`.
- Use arrays in Bash for command arguments and lists that may contain spaces.
- Do not use arrays in POSIX `sh`.
- Avoid relying on word splitting or globbing unless it is intentional and documented by nearby code.
- Handle filenames with spaces, newlines, leading dashes, and glob characters when practical.
- Use `--` before path operands when supported by the command.

## Input and arguments

- Validate required arguments and environment variables early.
- Print a useful usage message for CLI-style scripts.
- Avoid reading from implicit global paths when an explicit argument would be safer.
- Treat user input, env vars, filenames, branch names, URLs, and config values as untrusted.
- Do not pass untrusted input to shell evaluation, glob patterns, regexes, or commands without validation and quoting.

## Command execution

- Avoid `eval`.
- Avoid constructing command strings. In Bash, prefer arrays: `cmd=(tool --flag "$value")`; then `"${cmd[@]}"`.
- Prefer direct command execution over `sh -c`.
- Preserve exit statuses from wrapped commands unless the script intentionally maps them.
- Capture stdout and stderr separately when callers depend on them.
- Avoid hiding failures with `|| true` unless the non-zero status is expected and explained.
- Check tool availability only when the script needs a friendlier error than the shell would provide.

## Filesystem safety

- Use `mktemp` for temporary files and directories.
- Clean up temporary resources with `trap` when appropriate.
- Prevent path traversal when paths can come from user input.
- Avoid broad `rm -rf`, `chmod -R`, `chown -R`, or recursive moves.
- Scope destructive operations tightly and validate target paths before running them.
- Do not follow symlinks unintentionally for sensitive operations.
- Preserve file permissions when the script currently relies on them.
- Avoid writing outside the repository, working directory, or documented output directory unless explicitly required.

## Pipelines and subshells

- Remember that pipeline failures can be hidden without `pipefail`.
- Avoid modifying variables inside pipeline subshells when the value is needed later.
- Prefer process substitution or redirected loops in Bash when state must be preserved.
- In POSIX `sh`, use temporary files or here-docs carefully when needed.
- Be explicit about expected empty results from `grep`, `find`, or similar commands.

## Portability

- Match the portability level of the existing script.
- Do not use GNU-only flags when the script is expected to run on macOS/BSD unless nearby code already requires GNU tools.
- Check existing CI and README for supported platforms.
- Prefer POSIX constructs in `/bin/sh` scripts.
- Use Bash features only in Bash scripts with an appropriate shebang.

## Makefiles and CI shell snippets

- Remember that each Makefile recipe line may run in a separate shell unless configured otherwise.
- Escape `$` as `$$` in Makefile recipes when it should reach the shell.
- Keep CI shell steps readable; move complex logic into versioned scripts when appropriate.
- Preserve CI environment variable names and secret masking behavior.
- Do not print secrets or tokens in debug output.

## Testing and verification

Use the narrowest practical checks:

- `bash -n path/to/script.sh` for Bash syntax.
- `sh -n path/to/script.sh` for POSIX shell syntax.
- `shellcheck path/to/script.sh` when ShellCheck is available or configured.
- `shfmt -w path/to/script.sh` only when the repository uses shfmt or the user asked for formatting.
- Existing script tests, Bats tests, Makefile targets, or CI commands when present.

For behavioral changes, add or update tests when the repository has a shell test framework or an existing script-test pattern. If no test framework exists, verify with a safe dry run, syntax check, or narrowly scoped command and report the limitation.

## Security

- Do not expose secrets through `set -x`, logs, error messages, temporary files, process args, or command history.
- Disable or avoid xtrace around sensitive commands.
- Validate URLs, paths, branch names, container names, and remote names before using them in commands.
- Do not curl-pipe-to-shell or execute downloaded content unless the repository explicitly already does this and the task requires it.
- Use existing signing, checksum, auth, and deployment safeguards.
- Do not weaken permission checks, host verification, TLS validation, or secret handling.

## Final review checklist

Before finishing, check that:

- the shebang still matches the script syntax;
- variables and command substitutions are quoted where needed;
- destructive commands are tightly scoped;
- temporary files are cleaned up;
- expected exit codes are preserved;
- stdout/stderr behavior remains compatible;
- no secrets can be printed;
- syntax and configured shell lint checks were run or honestly reported as not run.
