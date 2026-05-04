#!/usr/bin/env python3
"""Validate prompt skill bundle integrity."""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TEXT_GLOBS = ("*.md", "*.yaml", "*.yml")
CONTROL_ALLOWED = {"\n", "\r", "\t"}
FORBIDDEN_TEXT = {
    "nextjs-app-router-rules.md": "stale Next.js reference filename; use split files under skills/next-change-code/references/",
    "nextjs-rules.md": "stale monolithic Next.js reference filename; use split files under skills/next-change-code/references/",
}


def iter_text_files() -> list[Path]:
    paths: list[Path] = []
    for base in [ROOT / "README.md", ROOT / "skills", ROOT / "scripts", ROOT / ".github"]:
        if base.is_file():
            paths.append(base)
        elif base.exists():
            for pattern in TEXT_GLOBS:
                paths.extend(base.rglob(pattern))
    return sorted(set(paths))


def iter_skill_doc_files() -> list[Path]:
    paths: list[Path] = []
    for base in [ROOT / "README.md", ROOT / "skills", ROOT / ".github"]:
        if base.is_file():
            paths.append(base)
        elif base.exists():
            for pattern in TEXT_GLOBS:
                paths.extend(base.rglob(pattern))
    return sorted(set(paths))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def is_bad_hidden_char(ch: str) -> bool:
    codepoint = ord(ch)
    if ch in CONTROL_ALLOWED:
        return False
    return (
        unicodedata.category(ch) == "Cf"
        or codepoint == 0x7F
        or 0x00 <= codepoint <= 0x1F
        or 0x202A <= codepoint <= 0x202E
        or 0x2066 <= codepoint <= 0x2069
    )


def check_hidden_unicode(errors: list[str]) -> None:
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(keepends=True), start=1):
            for col_no, ch in enumerate(line, start=1):
                if is_bad_hidden_char(ch):
                    name = unicodedata.name(ch, "UNKNOWN")
                    fail(errors, f"{rel(path)}:{line_no}:{col_no}: hidden/control char U+{ord(ch):04X} {name}")


def check_forbidden_text(errors: list[str]) -> None:
    for path in iter_skill_doc_files():
        text = path.read_text(encoding="utf-8")
        for needle, reason in FORBIDDEN_TEXT.items():
            if needle in text:
                fail(errors, f"{rel(path)}: contains forbidden text {needle!r}: {reason}")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def check_skill_frontmatter(errors: list[str]) -> None:
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        try:
            data = parse_frontmatter(text)
        except ValueError as exc:
            fail(errors, f"{rel(path)}: {exc}")
            continue
        if data is None:
            fail(errors, f"{rel(path)}: missing YAML frontmatter")
            continue
        for key in ["name", "description"]:
            if not data.get(key):
                fail(errors, f"{rel(path)}: missing frontmatter key {key!r}")


def load_yaml_if_available(text: str) -> Any:
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    return yaml.safe_load(text)


def parse_simple_agent_yaml(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    in_interface = False
    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        if raw_line == "interface:":
            in_interface = True
            continue
        if not in_interface:
            raise ValueError(f"unexpected top-level line: {raw_line!r}")
        match = re.fullmatch(r"  ([A-Za-z0-9_]+):\s*\"(.*)\"", raw_line)
        if not match:
            raise ValueError(f"invalid interface line: {raw_line!r}")
        result[match.group(1)] = match.group(2)
    return result


def check_agent_yaml(errors: list[str]) -> None:
    for path in sorted((ROOT / "skills").glob("*/agents/openai.yaml")):
        text = path.read_text(encoding="utf-8")
        try:
            parsed = load_yaml_if_available(text)
            if parsed is None:
                interface = parse_simple_agent_yaml(text)
            else:
                if not isinstance(parsed, dict) or not isinstance(parsed.get("interface"), dict):
                    raise ValueError("expected top-level 'interface' mapping")
                interface = parsed["interface"]
            for key in ["display_name", "short_description", "default_prompt"]:
                if not interface.get(key):
                    raise ValueError(f"missing interface.{key}")
        except Exception as exc:
            fail(errors, f"{rel(path)}: invalid YAML metadata: {exc}")


def skill_root_for(path: Path) -> Path | None:
    try:
        relative = path.relative_to(ROOT / "skills")
    except ValueError:
        return None
    return ROOT / "skills" / relative.parts[0] if relative.parts else None


def check_reference_links(errors: list[str]) -> None:
    owning_reference_pattern = re.compile(r"`(references/[A-Za-z0-9._/-]+\.md)`")
    root_relative_skill_path_pattern = re.compile(r"`(skills/[A-Za-z0-9._/-]+\.md)`")
    short_rules_pattern = re.compile(r"`([A-Za-z0-9._-]+-rules\.md)`")

    for path in iter_skill_doc_files():
        text = path.read_text(encoding="utf-8")
        root = skill_root_for(path)

        for match in root_relative_skill_path_pattern.finditer(text):
            target = ROOT / match.group(1)
            if not target.is_file():
                fail(errors, f"{rel(path)}: missing root-relative referenced file {match.group(1)!r}")

        if root is None:
            continue

        for match in owning_reference_pattern.finditer(text):
            target = root / match.group(1)
            if not target.is_file():
                fail(errors, f"{rel(path)}: missing referenced file {match.group(1)!r}")

        for match in short_rules_pattern.finditer(text):
            filename = match.group(1)
            target = root / "references" / filename
            if not target.is_file():
                fail(errors, f"{rel(path)}: missing short rules reference {filename!r}")


def check_readme_numbering(errors: list[str]) -> None:
    path = ROOT / "README.md"
    if not path.exists():
        return
    expected: int | None = None
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = re.match(r"^(\d+)\.\s+", line)
        if match:
            number = int(match.group(1))
            if expected is None:
                expected = number + 1
            elif number != expected:
                fail(errors, f"README.md:{line_no}: ordered list expected {expected}. but found {number}.")
                expected = number + 1
            else:
                expected += 1
        elif line.strip() != "":
            expected = None


def main() -> int:
    errors: list[str] = []
    check_hidden_unicode(errors)
    check_forbidden_text(errors)
    check_skill_frontmatter(errors)
    check_agent_yaml(errors)
    check_reference_links(errors)
    check_readme_numbering(errors)

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
