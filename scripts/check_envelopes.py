"""Envelope payload conformance check (CHECK6) for sqk-core.

transport 構造（handoff-envelope.schema.json）と payload 契約
（artifacts[].schema_ref が指すスキーマ）の継ぎ目を検証する。
"""

from __future__ import annotations

import json
from collections.abc import Iterator, Mapping
from pathlib import Path
from urllib.parse import unquote

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from check_common import (
    CheckResult,
    Issue,
    display_path,
    fenced_code_blocks,
    heading_anchors,
    walk_paths,
)

ENVELOPE_FIXTURE_GLOB = "schemas/tests/fixtures/handoff-envelope/valid/*.json"
HANDOFF_ENVELOPE_SCHEMA = "schemas/handoff-envelope.schema.json"
MARKDOWN_FENCE_LANGUAGES = frozenset({"markdown", "md"})
SCHEMA_FILE_SUFFIX = ".schema.json"


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
        anchors = heading_anchors(target.read_text(encoding="utf-8"))
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
        display = display_path(path, root)
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
    for block in fenced_code_blocks(text):
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
        for path in walk_paths(root)
        if path.suffix.lower() == ".md" and path.is_file() and not path.is_symlink()
    )
    for path in markdown_paths:
        display = display_path(path, root)
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
