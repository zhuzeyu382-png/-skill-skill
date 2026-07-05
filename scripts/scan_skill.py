#!/usr/bin/env python3
"""Scan a Codex skill directory and summarize its structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RESOURCE_DIRS = ("scripts", "references", "assets")
SKIP_NAMES = {".DS_Store", ".git", "__pycache__"}


def line_count(path: Path) -> int | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return sum(1 for _ in handle)
    except UnicodeDecodeError:
        return None


def iter_entries(root: Path) -> list[Path]:
    entries: list[Path] = []
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_NAMES for part in path.relative_to(root).parts):
            continue
        entries.append(path)
    return entries


def build_tree(root: Path, entries: list[Path]) -> list[str]:
    lines = [f"{root.name}/"]
    for path in entries:
        relative = path.relative_to(root)
        depth = len(relative.parts) - 1
        suffix = "/" if path.is_dir() else ""
        lines.append(f"{'  ' * (depth + 1)}{relative.name}{suffix}")
    return lines


def classify_skill(root: Path, resource_counts: dict[str, int]) -> str:
    has_scripts = resource_counts.get("scripts", 0) > 0
    has_references = resource_counts.get("references", 0) > 0
    has_assets = resource_counts.get("assets", 0) > 0

    if has_scripts and (has_references or has_assets):
        return "混合型"
    if has_scripts:
        return "工具集成型"
    if has_references or has_assets:
        return "流程编排型"
    return "轻量知识型"


def scan(root: Path) -> dict[str, object]:
    entries = iter_entries(root)
    files = [path for path in entries if path.is_file()]
    dirs = [path for path in entries if path.is_dir()]

    resource_counts: dict[str, int] = {}
    resource_bytes: dict[str, int] = {}
    for name in RESOURCE_DIRS:
        directory = root / name
        resource_files = [
            path
            for path in files
            if directory.exists() and directory in path.parents
        ]
        resource_counts[name] = len(resource_files)
        resource_bytes[name] = sum(path.stat().st_size for path in resource_files)

    file_details = []
    total_lines = 0
    text_file_count = 0
    for path in files:
        lines = line_count(path)
        if lines is not None:
            total_lines += lines
            text_file_count += 1
        file_details.append(
            {
                "path": str(path.relative_to(root)),
                "bytes": path.stat().st_size,
                "lines": lines,
            }
        )

    return {
        "path": str(root),
        "has_skill_md": (root / "SKILL.md").is_file(),
        "resource_dirs": {
            name: {
                "exists": (root / name).is_dir(),
                "files": resource_counts[name],
                "bytes": resource_bytes[name],
            }
            for name in RESOURCE_DIRS
        },
        "file_count": len(files),
        "directory_count": len(dirs),
        "total_bytes": sum(path.stat().st_size for path in files),
        "text_file_count": text_file_count,
        "total_text_lines": total_lines,
        "type_guess": classify_skill(root, resource_counts),
        "tree": build_tree(root, entries),
        "files": file_details,
    }


def render_markdown(data: dict[str, object]) -> str:
    resource_dirs = data["resource_dirs"]
    assert isinstance(resource_dirs, dict)

    lines = [
        "## Skill Scan",
        "",
        f"- Path: `{data['path']}`",
        f"- Has SKILL.md: {data['has_skill_md']}",
        f"- Type guess: {data['type_guess']}",
        f"- Files: {data['file_count']}",
        f"- Directories: {data['directory_count']}",
        f"- Total bytes: {data['total_bytes']}",
        f"- Text files: {data['text_file_count']}",
        f"- Total text lines: {data['total_text_lines']}",
        "",
        "### Resource Summary",
        "",
        "| Resource | Exists | Files | Bytes |",
        "|----------|--------|-------|-------|",
    ]
    for name in RESOURCE_DIRS:
        info = resource_dirs[name]
        lines.append(
            f"| {name}/ | {info['exists']} | {info['files']} | {info['bytes']} |"
        )

    lines.extend(["", "### Directory Tree", "", "```text"])
    lines.extend(data["tree"])
    lines.extend(["```", "", "### Files", "", "| File | Lines | Bytes |", "|------|-------|-------|"])
    for item in data["files"]:
        lines.append(f"| `{item['path']}` | {item['lines']} | {item['bytes']} |")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan a Codex skill directory.")
    parser.add_argument("skill_path", help="Path to the skill directory")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format",
    )
    parser.add_argument("--output", help="Optional output file path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.skill_path).expanduser().resolve()

    if not root.exists():
        print(f"error: path does not exist: {root}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"error: path is not a directory: {root}", file=sys.stderr)
        return 2
    if not (root / "SKILL.md").is_file():
        print(f"error: SKILL.md not found in: {root}", file=sys.stderr)
        return 2

    data = scan(root)
    if args.format == "json":
        output = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    else:
        output = render_markdown(data)

    if args.output:
        Path(args.output).expanduser().write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
