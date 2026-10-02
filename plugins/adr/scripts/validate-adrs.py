#!/usr/bin/env python3
"""Structural validation for Architecture Decision Records (ADRs).

Deterministic checks only. No LLM, no network, Python 3.8+ standard library.

Checks:
  1. Every ADR has the required frontmatter fields and an allowed status.
  2. ADR numbers are unique and sequential, and match the filename.
  3. The index (README.md) lists every ADR and links only to existing ones.
  4. supersedes / superseded_by links resolve in both directions.
  5. File paths referenced by ADRs still exist (staleness alarm).
  6. `@decision ADR-NNNN` comments in code point to existing, non-superseded ADRs.

Out of scope: judging whether code complies with a decision.

Exit codes:
  0  no errors (warnings may be present)
  1  one or more errors (or warnings with --strict)
  2  usage or configuration problem (e.g. no ADR directory found)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DEFAULT_ADR_DIRS = (
    "docs/adr",
    "doc/adr",
    "docs/adrs",
    "docs/decisions",
    "docs/architecture/decisions",
    "doc/architecture/decisions",
    "architecture/decisions",
    "adr",
    "adrs",
    ".adr",
)
ALLOWED_STATUSES = ("proposed", "accepted", "superseded", "deprecated", "rejected")
CLOSED_STATUSES = ("superseded", "deprecated", "rejected")
REQUIRED_FIELDS = ("id", "title", "status", "date")
INDEX_NAMES = ("README.md", "index.md", "INDEX.md")
NON_ADR_FILES = {"known-debt.md", "template.md"}

ADR_FILENAME_RE = re.compile(r"^(?P<num>\d{4})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
ADR_ID_RE = re.compile(r"^ADR-(?P<num>\d{4})$")
DECISION_TAG_RE = re.compile(r"@decision\s+ADR-(?P<num>\d{4})\b")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<header>.*?)\r?\n---\r?\n(?P<body>.*)\Z", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INLINE_PATH_RE = re.compile(r"`([A-Za-z0-9_.][A-Za-z0-9_./\-]*/[A-Za-z0-9_./\-]+)`")

SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", "out", "target",
    ".venv", "venv", "env", "__pycache__", ".tox", ".mypy_cache", ".pytest_cache",
    ".next", ".nuxt", ".turbo", ".cache", "coverage", ".idea", ".vscode", "bin", "obj",
    "Pods", "DerivedData", ".gradle", ".terraform", ".dart_tool",
}
MAX_SCAN_BYTES = 1_000_000


class Report:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


# --------------------------------------------------------------------------- parsing

def parse_frontmatter(text: str) -> Tuple[Optional[Dict[str, object]], str]:
    """Minimal YAML subset: scalars, inline lists [a, b], block lists (- item)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    fields: Dict[str, object] = {}
    current_list_key: Optional[str] = None
    for raw in match.group("header").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if current_list_key is not None and line.lstrip().startswith("- "):
            fields[current_list_key].append(_unquote(line.lstrip()[2:].strip()))  # type: ignore[union-attr]
            continue
        current_list_key = None
        if line.startswith((" ", "\t")):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()
        if value == "":
            fields[key] = []
            current_list_key = key
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            fields[key] = [_unquote(v.strip()) for v in inner.split(",") if v.strip()] if inner else []
        else:
            fields[key] = _unquote(value)
    return fields, match.group("body")


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def as_list(value: object) -> List[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


# --------------------------------------------------------------------------- discovery

def find_adr_dir(root: Path, explicit: Optional[str]) -> Optional[Path]:
    if explicit:
        candidate = (root / explicit).resolve()
        return candidate if candidate.is_dir() else None
    for rel in DEFAULT_ADR_DIRS:
        candidate = root / rel
        if candidate.is_dir() and any(ADR_FILENAME_RE.match(p.name) for p in candidate.iterdir()):
            return candidate
    for rel in DEFAULT_ADR_DIRS:
        candidate = root / rel
        if candidate.is_dir():
            return candidate
    return None


def iter_code_files(root: Path, adr_dir: Path):
    adr_dir = adr_dir.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".git"))
        current = Path(dirpath).resolve()
        if current == adr_dir or adr_dir in current.parents:
            dirnames[:] = []
            continue
        for name in sorted(filenames):
            path = Path(dirpath) / name
            try:
                if path.is_symlink() or path.stat().st_size > MAX_SCAN_BYTES:
                    continue
            except OSError:
                continue
            yield path


# --------------------------------------------------------------------------- checks

def validate(root: Path, adr_dir: Path, scan_code: bool, report: Report) -> Dict[str, object]:
    rel = lambda p: str(Path(p).resolve().relative_to(root.resolve())) if _inside(root, p) else str(p)  # noqa: E731

    adrs: Dict[int, Dict[str, object]] = {}
    for path in sorted(adr_dir.iterdir()):
        if not path.is_file() or path.suffix != ".md" or path.name in INDEX_NAMES or path.name in NON_ADR_FILES:
            continue
        match = ADR_FILENAME_RE.match(path.name)
        if not match:
            report.warn(rel(path), "ignored: filename is not NNNN-kebab-slug.md")
            continue
        num = int(match.group("num"))
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            report.error(rel(path), f"cannot read: {exc}")
            continue
        fields, body = parse_frontmatter(text)
        if fields is None:
            report.error(rel(path), "missing YAML frontmatter (--- block at top of file)")
            fields, body = {}, text
        if num in adrs:
            report.error(rel(path), f"duplicate number {num:04d}; already used by {rel(adrs[num]['path'])}")
            continue
        adrs[num] = {"path": path, "fields": fields, "body": body, "num": num}

    if not adrs:
        report.warn(rel(adr_dir), "no ADRs found (expected files named NNNN-slug.md)")

    # 1. frontmatter
    for num, adr in adrs.items():
        where = rel(adr["path"])
        fields = adr["fields"]  # type: ignore[assignment]
        for key in REQUIRED_FIELDS:
            if key not in fields or fields[key] in ("", []):
                report.error(where, f"missing required frontmatter field '{key}'")
        status = str(fields.get("status", "")).lower()
        if status and status not in ALLOWED_STATUSES:
            report.error(where, f"status '{status}' not in {', '.join(ALLOWED_STATUSES)}")
        id_value = str(fields.get("id", ""))
        id_match = ADR_ID_RE.match(id_value)
        if id_value and not id_match:
            report.error(where, f"id '{id_value}' must look like ADR-{num:04d}")
        elif id_match and int(id_match.group("num")) != num:
            report.error(where, f"id '{id_value}' does not match filename number {num:04d}")
        date = str(fields.get("date", ""))
        if date and not DATE_RE.match(date):
            report.error(where, f"date '{date}' must be YYYY-MM-DD")
        if not str(adr["body"]).strip():
            report.error(where, "body is empty")

    # 2. sequential numbering
    numbers = sorted(adrs)
    if numbers:
        start = numbers[0]
        if start not in (0, 1):
            report.error(rel(adr_dir), f"numbering must start at 0001 (or 0000); first ADR is {start:04d}")
        expected = list(range(start, start + len(numbers)))
        missing = sorted(set(expected) - set(numbers))
        if missing:
            report.error(rel(adr_dir), "numbering has gaps: missing " + ", ".join(f"{n:04d}" for n in missing))

    # 3. index
    index_path = next((adr_dir / n for n in INDEX_NAMES if (adr_dir / n).is_file()), None)
    if index_path is None:
        report.error(rel(adr_dir), "index file README.md is missing")
    else:
        index_text = index_path.read_text(encoding="utf-8", errors="replace")
        linked = set()
        for target in LINK_RE.findall(index_text):
            target = target.split("#", 1)[0]
            if target.startswith(("http://", "https://", "mailto:")) or not target:
                continue
            name = Path(target).name
            if ADR_FILENAME_RE.match(name):
                linked.add(name)
                if not (adr_dir / name).is_file():
                    report.error(rel(index_path), f"links to missing ADR {target}")
        for num, adr in adrs.items():
            if adr["path"].name not in linked:  # type: ignore[union-attr]
                report.error(rel(index_path), f"does not list {adr['path'].name}")  # type: ignore[union-attr]

    # 4. supersede links both ways
    by_id = {f"ADR-{num:04d}": adr for num, adr in adrs.items()}
    for num, adr in adrs.items():
        where = rel(adr["path"])
        me = f"ADR-{num:04d}"
        fields = adr["fields"]  # type: ignore[assignment]
        status = str(fields.get("status", "")).lower()
        for target in as_list(fields.get("supersedes")):
            other = by_id.get(target)
            if other is None:
                report.error(where, f"supersedes {target}, which does not exist")
                continue
            back = as_list(other["fields"].get("superseded_by"))  # type: ignore[union-attr]
            if me not in back:
                report.error(rel(other["path"]), f"must declare superseded_by: {me} (because {me} supersedes it)")
            if str(other["fields"].get("status", "")).lower() != "superseded":  # type: ignore[union-attr]
                report.error(rel(other["path"]), f"status must be 'superseded' because {me} supersedes it")
        for target in as_list(fields.get("superseded_by")):
            other = by_id.get(target)
            if other is None:
                report.error(where, f"superseded_by {target}, which does not exist")
                continue
            if me not in as_list(other["fields"].get("supersedes")):  # type: ignore[union-attr]
                report.error(rel(other["path"]), f"must declare supersedes: {me} (because {me} is superseded_by it)")
        if status == "superseded" and not as_list(fields.get("superseded_by")):
            report.error(where, "status is 'superseded' but superseded_by is empty")
        if status != "superseded" and as_list(fields.get("superseded_by")):
            report.error(where, "has superseded_by but status is not 'superseded'")

    # 5. referenced paths still exist
    for num, adr in adrs.items():
        where = rel(adr["path"])
        fields = adr["fields"]  # type: ignore[assignment]
        status = str(fields.get("status", "")).lower()
        if status in CLOSED_STATUSES:
            continue  # closed decisions are allowed to go stale
        for pattern in as_list(fields.get("paths")):
            if not _path_pattern_matches(root, pattern):
                report.warn(where, f"frontmatter path '{pattern}' matches nothing in the repository (stale?)")
        top_level = {p.name for p in root.iterdir() if p.is_dir() and p.name not in SKIP_DIRS}
        seen = set()
        for token in INLINE_PATH_RE.findall(str(adr["body"])):
            first = token.split("/", 1)[0]
            if token in seen or first not in top_level or "://" in token:
                continue
            seen.add(token)
            if not (root / token).exists() and not _path_pattern_matches(root, token):
                report.warn(where, f"mentions `{token}`, which no longer exists (stale?)")

    # 6. @decision tags in code
    tag_count = 0
    if scan_code:
        for path in iter_code_files(root, adr_dir):
            try:
                with open(path, "rb") as handle:
                    raw = handle.read()
            except OSError:
                continue
            if b"@decision" not in raw:
                continue
            text = raw.decode("utf-8", errors="replace")
            for line_no, line in enumerate(text.splitlines(), 1):
                for match in DECISION_TAG_RE.finditer(line):
                    tag_count += 1
                    num = int(match.group("num"))
                    where = f"{rel(path)}:{line_no}"
                    adr = adrs.get(num)
                    if adr is None:
                        report.error(where, f"@decision ADR-{num:04d} points to an ADR that does not exist")
                        continue
                    status = str(adr["fields"].get("status", "")).lower()  # type: ignore[union-attr]
                    if status == "superseded":
                        by = ", ".join(as_list(adr["fields"].get("superseded_by"))) or "?"  # type: ignore[union-attr]
                        report.error(where, f"@decision ADR-{num:04d} is superseded by {by}; update the tag")
                    elif status in ("deprecated", "rejected"):
                        report.warn(where, f"@decision ADR-{num:04d} has status '{status}'")

    return {"adr_dir": rel(adr_dir), "adrs": len(adrs), "decision_tags": tag_count}


def _inside(root: Path, path: Path) -> bool:
    try:
        Path(path).resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _path_pattern_matches(root: Path, pattern: str) -> bool:
    pattern = pattern.strip().lstrip("./")
    if not pattern:
        return False
    if any(ch in pattern for ch in "*?["):
        try:
            return next(root.glob(pattern), None) is not None
        except (ValueError, NotImplementedError):
            return False
    return (root / pattern).exists()


# --------------------------------------------------------------------------- setup snippets

SETUP_TEXT = """\
# Wiring validate-adrs into a repository
#
# The script is standard-library Python; copy it into the repository so CI and
# hooks do not depend on a Claude plugin cache:
#
#   cp "<plugin>/scripts/validate-adrs.py" scripts/validate-adrs.py
#
# --- Option A: pre-commit framework (.pre-commit-config.yaml) --------------
repos:
  - repo: local
    hooks:
      - id: validate-adrs
        name: validate ADRs
        entry: python3 scripts/validate-adrs.py
        language: system
        pass_filenames: false
        files: ^(docs/adr/|.*)$

# --- Option B: plain git hook (.git/hooks/pre-commit, chmod +x) -------------
#!/bin/sh
python3 scripts/validate-adrs.py || exit 1

# --- Option C: GitHub Actions step -----------------------------------------
      - name: Validate ADRs
        run: python3 scripts/validate-adrs.py --strict

# --- Option D: any other CI ------------------------------------------------
# Run `python3 scripts/validate-adrs.py --strict` and fail the job on exit 1.
"""


# --------------------------------------------------------------------------- main

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--adr-dir", help="ADR folder relative to root (default: auto-detect docs/adr and friends)")
    parser.add_argument("--no-code-scan", action="store_true", help="skip scanning code for @decision tags")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--print-setup", action="store_true", help="print pre-commit and CI snippets and exit")
    args = parser.parse_args(argv)

    if args.print_setup:
        print(SETUP_TEXT)
        return 0

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: root {args.root} is not a directory", file=sys.stderr)
        return 2
    adr_dir = find_adr_dir(root, args.adr_dir)
    if adr_dir is None:
        looked = args.adr_dir or ", ".join(DEFAULT_ADR_DIRS)
        print(f"error: no ADR directory found (looked for: {looked}). Run /adr:init or pass --adr-dir.", file=sys.stderr)
        return 2

    report = Report()
    summary = validate(root, adr_dir, not args.no_code_scan, report)
    failed = bool(report.errors) or (args.strict and bool(report.warnings))

    if args.json:
        print(json.dumps({"ok": not failed, "summary": summary, "errors": report.errors, "warnings": report.warnings}, indent=2))
        return 1 if failed else 0

    for item in report.errors:
        print(f"ERROR   {item}")
    for item in report.warnings:
        print(f"WARNING {item}")
    verdict = "FAILED" if failed else "OK"
    print(
        f"{verdict}: {summary['adrs']} ADRs in {summary['adr_dir']}, "
        f"{summary['decision_tags']} @decision tags, "
        f"{len(report.errors)} errors, {len(report.warnings)} warnings"
        + (" (strict)" if args.strict else "")
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
