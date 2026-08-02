"""Shared building blocks for the sqk-core checks.

`scripts/check.py` が入口で、個別の検査はここと `check_envelopes.py` に分かれる。
このモジュールは検査そのものを持たず、結果型・ツリー走査・Markdown 解析だけを提供する。
"""

from __future__ import annotations

import html
import os
import re
import unicodedata
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path

import yaml

EXCLUDED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".agent-work",
        ".pytest_cache",
        "__pycache__",
        "node_modules",
    }
)
FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")
OPENING_FENCE_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*(\S*)")
BACKTICK_RUN_PATTERN = re.compile(r"`+")
ATX_HEADING_PATTERN = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$")
SETEXT_HEADING_PATTERN = re.compile(r"^ {0,3}(?:=+|-+)\s*$")


@dataclass(frozen=True, slots=True)
class Issue:
    """One verification problem."""

    path: str
    message: str


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Result returned by one numbered check."""

    check_number: int
    checked: int
    issues: tuple[Issue, ...]


@dataclass(frozen=True, slots=True)
class FencedBlock:
    """One fenced code block with its info string and opening line number."""

    language: str
    line_number: int
    body: str


def _is_excluded(relative_path: Path) -> bool:
    parts = relative_path.parts
    if any(part in EXCLUDED_DIRECTORY_NAMES for part in parts):
        return True
    return any(
        parts[index : index + 2] == ("tests", "fixtures")
        for index in range(len(parts) - 1)
    )


def walk_paths(root: Path) -> Iterator[Path]:
    """Walk without Git and without following directory symlinks."""
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained_directories: list[str] = []
        for name in sorted(directory_names):
            candidate = current_path / name
            if _is_excluded(candidate.relative_to(root)):
                continue
            if candidate.is_symlink():
                yield candidate
            else:
                retained_directories.append(name)
        directory_names[:] = retained_directories
        for name in sorted(file_names):
            candidate = current_path / name
            if not _is_excluded(candidate.relative_to(root)):
                yield candidate


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def markdown_body(text: str) -> str:
    """Remove leading YAML frontmatter before Markdown parsing."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[index + 1 :])
    return text


def without_fenced_code(text: str) -> tuple[str, ...]:
    visible: list[str] = []
    fence_character: str | None = None
    for line in text.splitlines():
        match = FENCE_PATTERN.match(line)
        if match:
            marker_character = match.group(1)[0]
            if fence_character is None:
                fence_character = marker_character
                continue
            if marker_character == fence_character:
                fence_character = None
                continue
        if fence_character is None:
            visible.append(line)
    return tuple(visible)


def _is_closing_fence(line: str, marker: str, marker_length: int) -> bool:
    """A closer repeats the opener's character at least as many times, nothing else.

    Without the length rule, a ``` inside a ````-fenced block would close it and
    desynchronise every later block in the file.
    """
    if len(line) - len(line.lstrip(" ")) > 3:
        return False
    stripped = line.strip()
    return len(stripped) >= marker_length and set(stripped) == {marker}


def fenced_code_blocks(text: str) -> tuple[FencedBlock, ...]:
    """Collect fenced blocks from raw text so line numbers stay source-accurate."""
    blocks: list[FencedBlock] = []
    marker: str | None = None
    marker_length = 0
    language = ""
    opening_line = 0
    body: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if marker is None:
            match = OPENING_FENCE_PATTERN.match(line)
            if match:
                marker = match.group(1)[0]
                marker_length = len(match.group(1))
                language = match.group(2).lower()
                opening_line = line_number
                body = []
            continue
        if _is_closing_fence(line, marker, marker_length):
            blocks.append(FencedBlock(language, opening_line, "\n".join(body)))
            marker = None
            continue
        body.append(line)
    return tuple(blocks)


def without_inline_code(line: str) -> str:
    """Replace inline code spans while preserving surrounding text positions."""
    visible: list[str] = []
    position = 0
    while opener := BACKTICK_RUN_PATTERN.search(line, position):
        closer = BACKTICK_RUN_PATTERN.search(line, opener.end())
        while closer is not None and len(closer.group()) != len(opener.group()):
            closer = BACKTICK_RUN_PATTERN.search(line, closer.end())
        if closer is None:
            break
        visible.append(line[position : opener.start()])
        visible.append(" " * (closer.end() - opener.start()))
        position = closer.end()
    visible.append(line[position:])
    return "".join(visible)


def _github_slug(heading: str) -> str:
    value = html.unescape(heading)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"[`*_~]", "", value).strip().lower()
    kept = (
        character
        for character in value
        if character.isspace()
        or character in {"-", "_"}
        or unicodedata.category(character)[0] in {"L", "M", "N"}
    )
    return re.sub(r"\s", "-", "".join(kept)).strip("-")


def heading_anchors(text: str) -> frozenset[str]:
    lines = without_fenced_code(markdown_body(text))
    headings: list[str] = []
    index = 0
    while index < len(lines):
        atx_match = ATX_HEADING_PATTERN.match(lines[index])
        if atx_match:
            headings.append(atx_match.group(1))
            index += 1
            continue
        if (
            lines[index].strip()
            and index + 1 < len(lines)
            and SETEXT_HEADING_PATTERN.match(lines[index + 1])
        ):
            headings.append(lines[index].strip())
            index += 2
            continue
        index += 1

    anchors: set[str] = set()
    for heading in headings:
        base = _github_slug(heading)
        if not base:
            continue
        anchor = base
        duplicate_index = 0
        while anchor in anchors:
            duplicate_index += 1
            anchor = f"{base}-{duplicate_index}"
        anchors.add(anchor)
    return frozenset(anchors)


def read_frontmatter(path: Path) -> tuple[Mapping[str, object] | None, str | None]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return None, f"frontmatter cannot be read: {error}"
    if not lines or lines[0].strip() != "---":
        return None, None
    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing_index is None:
        return None, "frontmatter closing delimiter is missing"
    try:
        loaded = yaml.safe_load("\n".join(lines[1:closing_index]))
    except yaml.YAMLError as error:
        return None, f"frontmatter is invalid YAML: {error}"
    if loaded is None:
        return {}, None
    if not isinstance(loaded, Mapping):
        return None, "frontmatter must be a mapping"
    return loaded, None
