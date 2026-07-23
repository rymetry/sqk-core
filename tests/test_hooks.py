"""pre-tool-use-policy.sh(push ポリシー hook)の回帰テスト。

Claude 版(.claude/hooks/)と Codex 版(.codex/hooks/)の両方に対して
同一ケースを実行し、判定の一致(= 同一内容)も検証する。
"""

import json
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOKS = {
    "claude": REPO_ROOT / ".claude" / "hooks" / "pre-tool-use-policy.sh",
    "codex": REPO_ROOT / ".codex" / "hooks" / "pre-tool-use-policy.sh",
}

BLOCKED_COMMANDS = [
    "git push origin main",
    "git push origin HEAD:main",
    "git push origin HEAD:refs/heads/main",
    "git push --force origin feature-x",
    "git push --force-with-lease origin feature-x",
    "git push -f origin feature-x",
    "git push origin +feature:main",
    "git push --all origin",
    "git push --mirror origin",
    "git push",
    "git push origin",
    "cd repo && git push origin main",
    # 複数行コマンドでも push 行自体の違反は検出する
    'git commit -m "docs: update\n\n- release + restore" && git push origin main',
    'git commit -m "note\nwith + plus" && git push --force origin feature-x',
]

ALLOWED_COMMANDS = [
    "git push origin feature/task-2",
    "git push -u origin migrate/content-from-v1",
    "git push origin HEAD:feature/x",
    "git push origin v1-final",
    "git status",
    "git add . && git commit -m 'feat: x' && git push -u origin setup/bootstrap",
    # 複数行 commit メッセージ内の記号(+ / ; / -> 等)を refspec と誤検知しない
    'git commit -m "docs: update\n\n- release + restore verification; done\n- Status -> completed" && git push -u origin docs/x',
    # メッセージ本文に "--force" という文字列があっても push 自体が非 force なら許可
    'git commit -m "docs: explain --force blocking\n\ndetails here" && git push origin feature/hook-docs',
]


def run_hook(hook_path: Path, command: str) -> int:
    payload = json.dumps({"tool_input": {"command": command}})
    result = subprocess.run(
        ["bash", str(hook_path)],
        input=payload,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.returncode


@pytest.mark.parametrize("hook_name", HOOKS.keys())
@pytest.mark.parametrize("command", BLOCKED_COMMANDS)
def test_blocked(hook_name: str, command: str) -> None:
    assert run_hook(HOOKS[hook_name], command) == 2, f"should block: {command}"


@pytest.mark.parametrize("hook_name", HOOKS.keys())
@pytest.mark.parametrize("command", ALLOWED_COMMANDS)
def test_allowed(hook_name: str, command: str) -> None:
    assert run_hook(HOOKS[hook_name], command) == 0, f"should allow: {command}"


def test_claude_and_codex_hooks_are_identical() -> None:
    contents = {name: path.read_text() for name, path in HOOKS.items()}
    assert contents["claude"] == contents["codex"]


def test_raw_input_fallback_still_blocks() -> None:
    """JSON でない生入力でも main 宛 push を検出できる(フォールバック経路)。"""
    result = subprocess.run(
        ["bash", str(HOOKS["claude"])],
        input="git push origin main",
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 2
