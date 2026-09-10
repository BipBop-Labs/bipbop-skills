#!/usr/bin/env python3
"""Validate the public marketplace and its portable skill tree."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(?P<header>.*?)\n---\n(?P<body>.+)\Z", re.DOTALL)
FIELD_RE = re.compile(r'^(?P<key>[A-Za-z][A-Za-z0-9_-]*):\s*(?P<value>.+?)\s*$')
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
UUID_RE = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b")
RUT_RE = re.compile(r"\b\d{1,2}(?:\.\d{3}){2}-[\dkK]\b")
JSON_FILES = (
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
)

errors: list[str] = []


def fail(path: Path | str, message: str) -> None:
    try:
        label = Path(path).relative_to(ROOT)
    except (ValueError, TypeError):
        label = path
    errors.append(f"{label}: {message}")


def load_json(relative: str) -> dict:
    path = ROOT / relative
    if not path.is_file():
        fail(path, "missing required manifest")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(path, f"invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(path, "top-level JSON value must be an object")
        return {}
    return value


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        fail(path, "must start with YAML frontmatter and have a non-empty body")
        return {}

    fields: dict[str, str] = {}
    for line in match.group("header").splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        item = FIELD_RE.match(line)
        if not item:
            continue
        value = item.group("value").strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        fields[item.group("key")] = value
    return fields


def validate_relative_links(path: Path, text: str) -> None:
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        candidate = path.parent / target
        try:
            resolved = candidate.resolve()
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            fail(path, f"link escapes the repository: {raw_target}")
            continue
        if not candidate.exists():
            fail(path, f"broken relative link: {raw_target}")


def validate_public_content(path: Path, text: str) -> None:
    if UUID_RE.search(text):
        fail(path, "contains a UUID; public examples must use invented placeholders")
    if RUT_RE.search(text):
        fail(path, "contains a Chilean RUT; public examples must not contain real identifiers")


def validate_symlinks() -> None:
    root = ROOT.resolve()
    for path in ROOT.rglob("*"):
        if not path.is_symlink():
            continue
        try:
            path.resolve(strict=True).relative_to(root)
        except (FileNotFoundError, ValueError):
            fail(path, "symlink is broken or escapes the repository")


def main() -> int:
    manifests = {name: load_json(name) for name in JSON_FILES}
    portable = manifests["plugin.json"]
    claude = manifests[".claude-plugin/plugin.json"]
    claude_market = manifests[".claude-plugin/marketplace.json"]
    codex_market = manifests[".agents/plugins/marketplace.json"]

    if portable.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        fail("plugin.json", "must declare the Agent Plugins 1.0.0 schema")
    if portable.get("name") != "bipbop-skills":
        fail("plugin.json", "plugin name must be bipbop-skills")
    if claude.get("name") != portable.get("name"):
        fail(".claude-plugin/plugin.json", "name must match plugin.json")
    if claude.get("version") != portable.get("version"):
        fail(".claude-plugin/plugin.json", "version must match plugin.json")
    if claude.get("skills") != "./skills/":
        fail(".claude-plugin/plugin.json", "skills must point to ./skills/")

    claude_plugins = claude_market.get("plugins", [])
    if len(claude_plugins) != 1 or claude_plugins[0].get("name") != "bipbop-skills":
        fail(".claude-plugin/marketplace.json", "must expose exactly bipbop-skills")
    elif claude_plugins[0].get("source") not in {".", "./"}:
        fail(".claude-plugin/marketplace.json", "plugin source must be the repository root")
    elif "version" in claude_plugins[0]:
        fail(".claude-plugin/marketplace.json", "do not duplicate plugin version in the catalog")

    codex_plugins = codex_market.get("plugins", [])
    if len(codex_plugins) != 1 or codex_plugins[0].get("name") != "bipbop-skills":
        fail(".agents/plugins/marketplace.json", "must expose exactly bipbop-skills")
    else:
        source = codex_plugins[0].get("source", {})
        if source.get("source") != "local" or source.get("path") not in {".", "./"}:
            fail(".agents/plugins/marketplace.json", "plugin source must be local repository root")

    skills_root = ROOT / "skills"
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    if not skill_files:
        fail(skills_root, "at least one skill is required")

    names: dict[str, Path] = {}
    for path in skill_files:
        fields = parse_frontmatter(path)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not NAME_RE.fullmatch(name):
            fail(path, "frontmatter name must use kebab-case")
        if name != path.parent.name:
            fail(path, f"frontmatter name {name!r} must match folder {path.parent.name!r}")
        if name in names:
            fail(path, f"duplicate skill name; first declared in {names[name].relative_to(ROOT)}")
        names[name] = path
        if not description:
            fail(path, "frontmatter description is required")
        elif len(description) > 1024:
            fail(path, "frontmatter description exceeds 1024 characters")
        elif not re.search(r"\b(use|usar|úsalo|úsala|cuando|when)\b", description, re.IGNORECASE):
            fail(path, "description must include activation conditions")

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        validate_public_content(path, text)
        if path.suffix.lower() in {".md", ".markdown"}:
            validate_relative_links(path, text)

    validate_symlinks()

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(JSON_FILES)} manifests and {len(skill_files)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
