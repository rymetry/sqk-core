# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jsonschema",
#   "pyyaml",
# ]
# ///
"""Repository verification entry point for sqk-core."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import unicodedata
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

EXCLUDED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".agent-work",
        ".pytest_cache",
        "__pycache__",
        "node_modules",
    }
)
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")
OPENING_FENCE_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*(\S*)")
ENVELOPE_FIXTURE_GLOB = "schemas/tests/fixtures/handoff-envelope/valid/*.json"
HANDOFF_ENVELOPE_SCHEMA = "schemas/handoff-envelope.schema.json"
MARKDOWN_FENCE_LANGUAGES = frozenset({"markdown", "md"})
SCHEMA_FILE_SUFFIX = ".schema.json"
BACKTICK_RUN_PATTERN = re.compile(r"`+")
RESEARCH_PATH_PATTERN = re.compile(r"(?:^|/)_research(?:/|$)")
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


def _is_excluded(relative_path: Path) -> bool:
    parts = relative_path.parts
    if any(part in EXCLUDED_DIRECTORY_NAMES for part in parts):
        return True
    return any(
        parts[index : index + 2] == ("tests", "fixtures")
        for index in range(len(parts) - 1)
    )


def _walk_paths(root: Path) -> Iterator[Path]:
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


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _markdown_body(text: str) -> str:
    """Remove leading YAML frontmatter before Markdown parsing."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[index + 1 :])
    return text


def _without_fenced_code(text: str) -> tuple[str, ...]:
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


@dataclass(frozen=True, slots=True)
class FencedBlock:
    """One fenced code block with its info string and opening line number."""

    language: str
    line_number: int
    body: str


def _is_closing_fence(line: str, marker: str, marker_length: int) -> bool:
    """A closer repeats the opener's character at least as many times, nothing else.

    Without the length rule, a ``` inside a ````-fenced block would close it and
    desynchronise every later block in the file.
    """
    if len(line) - len(line.lstrip(" ")) > 3:
        return False
    stripped = line.strip()
    return len(stripped) >= marker_length and set(stripped) == {marker}


def _fenced_code_blocks(text: str) -> tuple[FencedBlock, ...]:
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


def _without_inline_code(line: str) -> str:
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


def _heading_anchors(text: str) -> frozenset[str]:
    lines = _without_fenced_code(_markdown_body(text))
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


def _normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return re.split(r"""\s+(?=["'])""", target, maxsplit=1)[0]


def _local_link_target(source: Path, root: Path, path_text: str) -> Path:
    decoded = unquote(path_text)
    if not decoded:
        return source
    if decoded.startswith("/"):
        return root / decoded.lstrip("/")
    return source.parent / decoded


def _validate_markdown_link(
    source: Path, root: Path, raw_target: str
) -> tuple[Issue, ...]:
    target_text = _normalize_link_target(raw_target)
    try:
        parsed = urlsplit(target_text)
    except ValueError as error:
        return (Issue(_display_path(source, root), f"invalid link: {error}"),)
    if parsed.scheme or target_text.startswith("//"):
        return ()

    target = _local_link_target(source, root, parsed.path)
    if not target.exists():
        return (
            Issue(
                _display_path(source, root),
                f"relative target does not exist: {target_text}",
            ),
        )
    if not parsed.fragment:
        return ()
    if target.suffix.lower() != ".md" or not target.is_file():
        return (
            Issue(
                _display_path(source, root),
                f"cannot resolve #{unquote(parsed.fragment)} in non-Markdown target",
            ),
        )
    try:
        anchors = _heading_anchors(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        return (
            Issue(
                _display_path(source, root),
                f"cannot read anchor target {target_text}: {error}",
            ),
        )
    anchor = unquote(parsed.fragment)
    if anchor in anchors:
        return ()
    return (
        Issue(
            _display_path(source, root),
            f"anchor #{anchor} does not exist in {unquote(parsed.path) or source.name}",
        ),
    )


def check_markdown_links(root: Path) -> CheckResult:
    """Check Markdown links; GitHub UI Markdown under .github is excluded."""
    candidates = tuple(
        path
        for path in _walk_paths(root)
        if not path.is_symlink()
        and path.is_file()
        and path.relative_to(root).parts[:1] != (".github",)
    )
    issues: list[Issue] = []
    for source in (path for path in candidates if path.suffix.lower() == ".md"):
        try:
            body = _markdown_body(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as error:
            issues.append(Issue(_display_path(source, root), f"cannot read file: {error}"))
            continue
        for line in _without_fenced_code(body):
            for match in LINK_PATTERN.finditer(_without_inline_code(line)):
                issues.extend(_validate_markdown_link(source, root, match.group(1)))
    return CheckResult(1, len(candidates), tuple(issues))


def check_schemas(root: Path) -> CheckResult:
    """Validate schemas/*.schema.json as Draft 2020-12 schemas."""
    schema_directory = root / "schemas"
    schema_paths = (
        tuple(sorted(schema_directory.glob("*.schema.json")))
        if schema_directory.is_dir()
        else ()
    )
    issues: list[Issue] = []
    for path in schema_paths:
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
        except (OSError, UnicodeError, json.JSONDecodeError, SchemaError) as error:
            issues.append(
                Issue(_display_path(path, root), f"invalid Draft 2020-12 schema: {error}")
            )
    return CheckResult(2, len(schema_paths), tuple(issues))


def _read_frontmatter(path: Path) -> tuple[Mapping[str, object] | None, str | None]:
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


def _string_values(value: object, field: str = "") -> Iterator[tuple[str, str]]:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            nested_field = f"{field}.{key}" if field else str(key)
            yield from _string_values(nested, nested_field)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, nested in enumerate(value):
            yield from _string_values(nested, f"{field}[{index}]")
    elif isinstance(value, str):
        yield field or "<root>", value


def check_research_leaks(root: Path) -> CheckResult:
    """Reject _research references in Markdown YAML frontmatter values."""
    markdown_paths = tuple(
        path
        for path in _walk_paths(root)
        if path.suffix.lower() == ".md" and path.is_file() and not path.is_symlink()
    )
    issues: list[Issue] = []
    for path in markdown_paths:
        frontmatter, error = _read_frontmatter(path)
        if error:
            issues.append(Issue(_display_path(path, root), error))
            continue
        if frontmatter is None:
            continue
        for field, value in _string_values(frontmatter):
            if RESEARCH_PATH_PATTERN.search(value):
                issues.append(
                    Issue(
                        _display_path(path, root),
                        f"{field} contains forbidden research reference: {value}",
                    )
                )
    return CheckResult(3, len(markdown_paths), tuple(issues))


def _output_reference_issues(
    root: Path, skill_path: Path, frontmatter: Mapping[str, object]
) -> tuple[Issue, ...]:
    if "outputs" not in frontmatter:
        return ()
    outputs = frontmatter["outputs"]
    if not isinstance(outputs, Mapping):
        return (Issue(_display_path(skill_path, root), "outputs must be a mapping"),)
    issues: list[Issue] = []
    for name, output in outputs.items():
        field = f"outputs.{name}.schema"
        schema_reference = output.get("schema") if isinstance(output, Mapping) else None
        if not isinstance(schema_reference, str):
            issues.append(Issue(_display_path(skill_path, root), f"{field} must be a string"))
            continue
        if not schema_reference or Path(schema_reference).is_absolute():
            issues.append(
                Issue(
                    _display_path(skill_path, root),
                    f"{field} must be a non-empty relative path",
                )
            )
        elif not (skill_path.parent / schema_reference).exists():
            issues.append(
                Issue(
                    _display_path(skill_path, root),
                    f"{field} target does not exist: {schema_reference}",
                )
            )
    return tuple(issues)


def _knowledge_reference_issues(
    root: Path, skill_path: Path, frontmatter: Mapping[str, object]
) -> tuple[Issue, ...]:
    if "knowledge_refs" not in frontmatter:
        return ()
    references = frontmatter["knowledge_refs"]
    if not isinstance(references, list):
        return (
            Issue(_display_path(skill_path, root), "knowledge_refs must be a list"),
        )
    issues: list[Issue] = []
    for index, reference in enumerate(references):
        field = f"knowledge_refs[{index}]"
        if not isinstance(reference, str) or not reference:
            issues.append(
                Issue(_display_path(skill_path, root), f"{field} must be a string")
            )
        elif Path(reference).is_absolute():
            issues.append(
                Issue(_display_path(skill_path, root), f"{field} must be repo-root relative")
            )
        elif not (root / reference).exists():
            issues.append(
                Issue(
                    _display_path(skill_path, root),
                    f"{field} target does not exist: {reference}",
                )
            )
    return tuple(issues)


def check_skill_references(root: Path) -> CheckResult:
    """Validate schema and knowledge references in skills/*/SKILL.md."""
    skills_directory = root / "skills"
    skill_paths = (
        tuple(sorted(skills_directory.glob("*/SKILL.md")))
        if skills_directory.is_dir()
        else ()
    )
    issues: list[Issue] = []
    for path in skill_paths:
        frontmatter, error = _read_frontmatter(path)
        if error:
            issues.append(Issue(_display_path(path, root), error))
            continue
        if frontmatter is None:
            issues.append(Issue(_display_path(path, root), "frontmatter is missing"))
            continue
        issues.extend(_output_reference_issues(root, path, frontmatter))
        issues.extend(_knowledge_reference_issues(root, path, frontmatter))
    return CheckResult(4, len(skill_paths), tuple(issues))


def check_symlinks(root: Path) -> CheckResult:
    """Ensure every non-excluded symlink resolves."""
    symlinks = tuple(path for path in _walk_paths(root) if path.is_symlink())
    issues: list[Issue] = []
    for path in symlinks:
        try:
            path.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            issues.append(
                Issue(
                    _display_path(path, root),
                    f"symlink target does not exist or cannot be resolved: {error}",
                )
            )
    return CheckResult(5, len(symlinks), tuple(issues))


def _is_handoff_envelope(document: object) -> bool:
    """Detect the envelope shape; conformance itself is the schema's concern."""
    return (
        isinstance(document, Mapping)
        and isinstance(document.get("source_skill"), str)
        and isinstance(document.get("artifacts"), list)
    )


def _payload_validator(schema_path: Path) -> tuple[Draft202012Validator | None, str]:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, UnicodeError, json.JSONDecodeError, SchemaError) as error:
        return None, str(error)
    return Draft202012Validator(schema), ""


def _artifact_payloads(
    artifact: Mapping[str, object], location: str
) -> Iterator[tuple[str, object]]:
    """Yield both payload shapes the envelope allows: items[] and content."""
    items = artifact.get("items")
    if isinstance(items, list):
        for index, item in enumerate(items):
            yield f"{location}.items[{index}]", item
    content = artifact.get("content")
    if isinstance(content, Mapping):
        yield f"{location}.content", content


def _conformance_message(location: str, error: ValidationError, reference: str) -> str:
    pointer = ".".join(str(part) for part in error.absolute_path)
    where = f"{location}.{pointer}" if pointer else location
    return f"{where}: {error.message} (declared schema_ref: {reference})"


def _is_inside(root: Path, target: Path) -> bool:
    """Reject symlinks that leave the tree; is_file() alone follows them out."""
    try:
        target.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, ValueError):
        return False
    return True


def _prose_reference_issues(
    display: str, location: str, reference: str, target: Path, fragment: str
) -> tuple[Issue, ...]:
    """成果物種別に JSON Schema が無い場合、schema_ref は散文の出典を指す。

    payload の構造検証はできないため、参照が解決することだけを保証する。
    """
    if not fragment:
        return ()
    anchor = unquote(fragment)
    if target.suffix.lower() != ".md":
        return (
            Issue(
                display,
                f"{location}.schema_ref cannot resolve anchor #{anchor} "
                f"in non-Markdown target: {reference}",
            ),
        )
    try:
        anchors = _heading_anchors(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        return (
            Issue(display, f"{location}.schema_ref cannot read {reference}: {error}"),
        )
    if anchor in anchors:
        return ()
    return (
        Issue(display, f"{location}.schema_ref anchor #{anchor} does not exist"),
    )


def _payload_conformance_issues(
    validator: Draft202012Validator,
    artifact: Mapping[str, object],
    display: str,
    location: str,
    reference: str,
) -> tuple[Issue, ...]:
    issues: list[Issue] = []
    for payload_location, payload in _artifact_payloads(artifact, location):
        try:
            failures = sorted(
                validator.iter_errors(payload),
                key=lambda failure: list(failure.absolute_path),
            )
        except Exception as error:  # noqa: BLE001
            # 解決できない $ref 等でスキーマ1本が壊れても、検査全体を落とさず報告する。
            issues.append(
                Issue(
                    display,
                    f"{payload_location} cannot be validated against {reference}: {error}",
                )
            )
            continue
        issues.extend(
            Issue(display, _conformance_message(payload_location, failure, reference))
            for failure in failures
        )
    return tuple(issues)


def _artifact_payload_issues(
    root: Path, display: str, location: str, artifact: object
) -> tuple[Issue, ...]:
    if not isinstance(artifact, Mapping):
        return (Issue(display, f"{location} must be an object"),)
    reference = artifact.get("schema_ref")
    if not isinstance(reference, str) or not reference:
        return (Issue(display, f"{location}.schema_ref must be a non-empty string"),)

    path_text, _, fragment = reference.partition("#")
    reference_path = Path(path_text)
    # 絶対パスは root との結合で root 自体が無視され、`..` は root 外へ出る。
    # どちらも検証対象の外を指すため、解決させずに拒否する（CHECK4 と同じ規約）。
    if not path_text or reference_path.is_absolute() or ".." in reference_path.parts:
        return (
            Issue(
                display,
                f"{location}.schema_ref must be a repo-root relative path: {reference}",
            ),
        )

    target = root / reference_path
    if not target.is_file():
        return (
            Issue(display, f"{location}.schema_ref target does not exist: {reference}"),
        )
    if not _is_inside(root, target):
        return (
            Issue(
                display,
                f"{location}.schema_ref resolves outside the tree: {reference}",
            ),
        )
    if not target.name.endswith(SCHEMA_FILE_SUFFIX):
        return _prose_reference_issues(display, location, reference, target, fragment)
    if fragment:
        # fragment を捨ててルートスキーマで検証すると、宣言とは別の契約を検査してしまう。
        return (
            Issue(
                display,
                f"{location}.schema_ref JSON Schema fragments are not supported: {reference}",
            ),
        )

    validator, schema_error = _payload_validator(target)
    if validator is None:
        return (
            Issue(
                display,
                f"{location}.schema_ref is not a usable schema: {reference}: {schema_error}",
            ),
        )
    return _payload_conformance_issues(
        validator, artifact, display, location, reference
    )


def _envelope_payload_issues(
    root: Path,
    display: str,
    document: Mapping[str, object],
    location_prefix: str = "",
) -> tuple[Issue, ...]:
    artifacts = document.get("artifacts")
    if not isinstance(artifacts, list):
        return ()
    return tuple(
        issue
        for index, artifact in enumerate(artifacts)
        for issue in _artifact_payload_issues(
            root, display, f"{location_prefix}artifacts[{index}]", artifact
        )
    )


def _fixture_envelope_issues(root: Path) -> tuple[int, tuple[Issue, ...]]:
    checked = 0
    issues: list[Issue] = []
    for path in sorted(root.glob(ENVELOPE_FIXTURE_GLOB)):
        display = _display_path(path, root)
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            issues.append(Issue(display, f"cannot read envelope fixture: {error}"))
            continue
        if not _is_handoff_envelope(document):
            issues.append(Issue(display, "valid fixture is not a handoff envelope"))
            continue
        checked += 1
        issues.extend(_envelope_payload_issues(root, display, document))
    return checked, tuple(issues)


def _envelope_transport_issues(
    root: Path, display: str, document: Mapping[str, object], location_prefix: str
) -> tuple[Issue, ...]:
    """Markdown のエンベロープ例を transport schema 自体にも当てる。

    fixture は validate-schemas.sh が見るが、Markdown の例は CI で他に見る者がいない。
    """
    schema_path = root / HANDOFF_ENVELOPE_SCHEMA
    if not schema_path.is_file():
        return ()
    validator, schema_error = _payload_validator(schema_path)
    if validator is None:
        return (
            Issue(
                display,
                f"{HANDOFF_ENVELOPE_SCHEMA} is not a usable schema: {schema_error}",
            ),
        )
    return tuple(
        Issue(
            display,
            _conformance_message(
                f"{location_prefix}envelope", failure, HANDOFF_ENVELOPE_SCHEMA
            ),
        )
        for failure in sorted(
            validator.iter_errors(document),
            key=lambda failure: list(failure.absolute_path),
        )
    )


def _envelope_json_blocks(
    text: str, line_offset: int = 0
) -> Iterator[tuple[int, Mapping[str, object]]]:
    """Yield (line number, envelope) for json blocks, descending into quoted Markdown.

    SKILL.md 全体を ````markdown で引用する書き方（portability-design.md の実装例）が
    あり、その内側の出力例も consumer が契約として読む。1段の入れ子まで追う。
    """
    for block in _fenced_code_blocks(text):
        line_number = line_offset + block.line_number
        if block.language in MARKDOWN_FENCE_LANGUAGES:
            yield from _envelope_json_blocks(block.body, line_number)
            continue
        if block.language != "json":
            continue
        try:
            document = json.loads(block.body)
        except json.JSONDecodeError:
            # 省略記法を含む例示ブロックは検証対象にしない。
            continue
        if _is_handoff_envelope(document):
            yield line_number, document


def _markdown_envelope_issues(root: Path) -> tuple[int, tuple[Issue, ...]]:
    checked = 0
    issues: list[Issue] = []
    markdown_paths = (
        path
        for path in _walk_paths(root)
        if path.suffix.lower() == ".md" and path.is_file() and not path.is_symlink()
    )
    for path in markdown_paths:
        display = _display_path(path, root)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            issues.append(Issue(display, f"cannot read file: {error}"))
            continue
        for line_number, document in _envelope_json_blocks(text):
            checked += 1
            location_prefix = f"line {line_number} "
            issues.extend(
                _envelope_transport_issues(root, display, document, location_prefix)
            )
            issues.extend(
                _envelope_payload_issues(root, display, document, location_prefix)
            )
    return checked, tuple(issues)


def check_envelope_payloads(root: Path) -> CheckResult:
    """Validate envelope payloads against the schema each artifact declares.

    transport 構造（handoff-envelope.schema.json）と payload 契約
    （artifacts[].schema_ref が指すスキーマ）の継ぎ目を検証する。
    envelope fixture と、Markdown 内の JSON エンベロープ例の両方を対象にする。
    """
    fixture_checked, fixture_issues = _fixture_envelope_issues(root)
    markdown_checked, markdown_issues = _markdown_envelope_issues(root)
    return CheckResult(
        6, fixture_checked + markdown_checked, fixture_issues + markdown_issues
    )


def run_checks(root: Path) -> tuple[CheckResult, ...]:
    """Run all checks in their documented order."""
    return (
        check_markdown_links(root),
        check_schemas(root),
        check_research_leaks(root),
        check_skill_references(root),
        check_symlinks(root),
        check_envelope_payloads(root),
    )


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository or fixture root (default: repository root)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        print(f"CHECK0: {root}: root is not a directory", file=sys.stderr)
        return 1

    results = run_checks(root)
    for result in results:
        print(
            f"CHECK{result.check_number} summary: "
            f"checked={result.checked} issues={len(result.issues)}"
        )
        for issue in result.issues:
            print(f"CHECK{result.check_number}: {issue.path}: {issue.message}")
    return 1 if any(result.issues for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
