# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jsonschema",
#   "pyyaml",
# ]
# ///
"""Repository verification entry point for sqk-core.

検査は CHECK1〜CHECK5 をここに、CHECK6（エンベロープ内包 payload）を
`check_envelopes.py` に置く。共有部品は `check_common.py`。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from check_common import (
    CheckResult,
    Issue,
    display_path,
    heading_anchors,
    markdown_body,
    read_frontmatter,
    walk_paths,
    without_fenced_code,
    without_inline_code,
)
from check_envelopes import check_envelope_payloads

LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
RESEARCH_PATH_PATTERN = re.compile(r"(?:^|/)_research(?:/|$)")


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
        return (Issue(display_path(source, root), f"invalid link: {error}"),)
    if parsed.scheme or target_text.startswith("//"):
        return ()

    target = _local_link_target(source, root, parsed.path)
    if not target.exists():
        return (
            Issue(
                display_path(source, root),
                f"relative target does not exist: {target_text}",
            ),
        )
    if not parsed.fragment:
        return ()
    if target.suffix.lower() != ".md" or not target.is_file():
        return (
            Issue(
                display_path(source, root),
                f"cannot resolve #{unquote(parsed.fragment)} in non-Markdown target",
            ),
        )
    try:
        anchors = heading_anchors(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        return (
            Issue(
                display_path(source, root),
                f"cannot read anchor target {target_text}: {error}",
            ),
        )
    anchor = unquote(parsed.fragment)
    if anchor in anchors:
        return ()
    return (
        Issue(
            display_path(source, root),
            f"anchor #{anchor} does not exist in {unquote(parsed.path) or source.name}",
        ),
    )


def check_markdown_links(root: Path) -> CheckResult:
    """Check Markdown links; GitHub UI Markdown under .github is excluded."""
    candidates = tuple(
        path
        for path in walk_paths(root)
        if not path.is_symlink()
        and path.is_file()
        and path.relative_to(root).parts[:1] != (".github",)
    )
    issues: list[Issue] = []
    for source in (path for path in candidates if path.suffix.lower() == ".md"):
        try:
            body = markdown_body(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as error:
            issues.append(Issue(display_path(source, root), f"cannot read file: {error}"))
            continue
        for line in without_fenced_code(body):
            for match in LINK_PATTERN.finditer(without_inline_code(line)):
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
                Issue(display_path(path, root), f"invalid Draft 2020-12 schema: {error}")
            )
    return CheckResult(2, len(schema_paths), tuple(issues))


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
        for path in walk_paths(root)
        if path.suffix.lower() == ".md" and path.is_file() and not path.is_symlink()
    )
    issues: list[Issue] = []
    for path in markdown_paths:
        frontmatter, error = read_frontmatter(path)
        if error:
            issues.append(Issue(display_path(path, root), error))
            continue
        if frontmatter is None:
            continue
        for field, value in _string_values(frontmatter):
            if RESEARCH_PATH_PATTERN.search(value):
                issues.append(
                    Issue(
                        display_path(path, root),
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
        return (Issue(display_path(skill_path, root), "outputs must be a mapping"),)
    issues: list[Issue] = []
    for name, output in outputs.items():
        field = f"outputs.{name}.schema"
        schema_reference = output.get("schema") if isinstance(output, Mapping) else None
        if not isinstance(schema_reference, str):
            issues.append(Issue(display_path(skill_path, root), f"{field} must be a string"))
            continue
        if not schema_reference or Path(schema_reference).is_absolute():
            issues.append(
                Issue(
                    display_path(skill_path, root),
                    f"{field} must be a non-empty relative path",
                )
            )
        elif not (skill_path.parent / schema_reference).exists():
            issues.append(
                Issue(
                    display_path(skill_path, root),
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
            Issue(display_path(skill_path, root), "knowledge_refs must be a list"),
        )
    issues: list[Issue] = []
    for index, reference in enumerate(references):
        field = f"knowledge_refs[{index}]"
        if not isinstance(reference, str) or not reference:
            issues.append(
                Issue(display_path(skill_path, root), f"{field} must be a string")
            )
        elif Path(reference).is_absolute():
            issues.append(
                Issue(display_path(skill_path, root), f"{field} must be repo-root relative")
            )
        elif not (root / reference).exists():
            issues.append(
                Issue(
                    display_path(skill_path, root),
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
        frontmatter, error = read_frontmatter(path)
        if error:
            issues.append(Issue(display_path(path, root), error))
            continue
        if frontmatter is None:
            issues.append(Issue(display_path(path, root), "frontmatter is missing"))
            continue
        issues.extend(_output_reference_issues(root, path, frontmatter))
        issues.extend(_knowledge_reference_issues(root, path, frontmatter))
    return CheckResult(4, len(skill_paths), tuple(issues))


def check_symlinks(root: Path) -> CheckResult:
    """Ensure every non-excluded symlink resolves."""
    symlinks = tuple(path for path in walk_paths(root) if path.is_symlink())
    issues: list[Issue] = []
    for path in symlinks:
        try:
            path.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            issues.append(
                Issue(
                    display_path(path, root),
                    f"symlink target does not exist or cannot be resolved: {error}",
                )
            )
    return CheckResult(5, len(symlinks), tuple(issues))


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
