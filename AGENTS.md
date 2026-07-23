# Agent Context

sqk-core は、ソフトウェア品質ナレッジベース v2 のリポジトリである。
品質知識、スキル、リポジトリ内契約を、最小限のガバナンスで管理する。

## コマンド

- Check: `uv run scripts/check.py`
- Test: `uv run --with pytest --with jsonschema --with pyyaml pytest tests/ -v`

## ルール

- Secrets やローカル環境固有の状態をコミットしない。
- `main` へ直接 push しない。変更は PR 経由で反映する。
- `main` 宛の push(通常・force とも)、および `--all` / `--mirror` / 宛先を明示しない bare push は禁止(`.claude/hooks/pre-tool-use-policy.sh` でブロックされる。feature branch への明示 push のみ許可)。
- コンフリクトマーカーを残したまま作業を終えない(`.claude/hooks/stop-verify.sh` で検出される)。
