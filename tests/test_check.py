"""scripts/check.py の検査項目と CLI の回帰テスト。"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
CHECK_SCRIPT = REPO_ROOT / "scripts" / "check.py"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "check.yml"


@pytest.fixture(scope="session")
def check_module():
    """未実装時も他モジュールの収集を妨げず、TDD の失敗を明示する。"""
    assert CHECK_SCRIPT.exists(), "scripts/check.py is not implemented yet"
    spec = importlib.util.spec_from_file_location("sqk_check", CHECK_SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def messages(result) -> list[str]:
    return [issue.message for issue in result.issues]


def test_check1_markdown_links_pass(check_module) -> None:
    result = check_module.check_markdown_links(FIXTURES / "check1_links_pass")

    assert result.check_number == 1
    assert result.checked == 3
    assert result.issues == ()


def test_check1_markdown_links_fail(check_module) -> None:
    result = check_module.check_markdown_links(FIXTURES / "check1_links_fail")

    assert result.check_number == 1
    assert len(result.issues) == 2
    assert any("missing.md" in message for message in messages(result))
    assert any("#missing-heading" in message for message in messages(result))


def test_check1_inline_code_links_are_ignored(check_module) -> None:
    result = check_module.check_markdown_links(
        FIXTURES / "check1_inline_code_links_pass"
    )

    assert result.check_number == 1
    assert result.checked == 1
    assert result.issues == ()


def test_check2_schemas_pass(check_module) -> None:
    result = check_module.check_schemas(FIXTURES / "check2_schemas_pass")

    assert result.check_number == 2
    assert result.checked == 1
    assert result.issues == ()


def test_check2_schemas_fail(check_module) -> None:
    result = check_module.check_schemas(FIXTURES / "check2_schemas_fail")

    assert result.check_number == 2
    assert result.checked == 1
    assert len(result.issues) == 1
    assert "invalid.schema.json" in result.issues[0].path


def test_check3_research_prose_mention_is_allowed(check_module) -> None:
    result = check_module.check_research_leaks(
        FIXTURES / "check3_research_mentions_pass"
    )

    assert result.check_number == 3
    assert result.checked == 1
    assert result.issues == ()


def test_check3_structured_research_reference_fails(check_module) -> None:
    result = check_module.check_research_leaks(
        FIXTURES / "check3_research_leak_fail"
    )

    assert result.check_number == 3
    assert len(result.issues) == 1
    assert "source_refs" in result.issues[0].message
    assert "docs/_research/" in result.issues[0].message


def test_check3_research_directory_reference_without_trailing_slash_fails(
    check_module,
) -> None:
    result = check_module.check_research_leaks(
        FIXTURES / "check3_research_root_fail"
    )

    assert result.check_number == 3
    assert len(result.issues) == 1
    assert "source_refs" in result.issues[0].message
    assert "docs/_research" in result.issues[0].message


def test_check4_skill_references_pass(check_module) -> None:
    result = check_module.check_skill_references(
        FIXTURES / "check4_skill_refs_pass"
    )

    assert result.check_number == 4
    assert result.checked == 1
    assert result.issues == ()


def test_check4_skill_references_fail(check_module) -> None:
    result = check_module.check_skill_references(
        FIXTURES / "check4_skill_refs_fail"
    )

    assert result.check_number == 4
    assert result.checked == 3
    assert len(result.issues) == 5
    combined = "\n".join(messages(result))
    assert "frontmatter" in combined
    assert "outputs" in combined
    assert "knowledge_refs" in combined
    assert "does not exist" in combined


def test_check5_symlinks_pass(check_module) -> None:
    result = check_module.check_symlinks(FIXTURES / "check5_symlinks_pass")

    assert result.check_number == 5
    assert result.checked == 1
    assert result.issues == ()


def test_check5_symlinks_fail(check_module) -> None:
    result = check_module.check_symlinks(FIXTURES / "check5_symlinks_fail")

    assert result.check_number == 5
    assert result.checked == 1
    assert len(result.issues) == 1
    assert result.issues[0].path == "broken-link"


def test_repository_check_cli_is_green(check_module) -> None:
    result = subprocess.run(
        [sys.executable, str(CHECK_SCRIPT), "--root", str(REPO_ROOT)],
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    for check_number in range(1, 6):
        assert f"CHECK{check_number} summary:" in result.stdout


def test_ci_workflow_runs_check_and_fixed_pytest() -> None:
    assert WORKFLOW.exists()
    workflow = WORKFLOW.read_text()

    assert "pull_request:" in workflow
    assert "branches: [main]" in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "uses: actions/checkout@v6" in workflow
    assert "uses: astral-sh/setup-uv@v8" in workflow
    assert "uv run scripts/check.py" in workflow
    assert (
        "uv run --with pytest --with jsonschema --with pyyaml pytest tests/ -v"
        in workflow
    )
