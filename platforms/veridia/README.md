# veridia（実行系）向け取り込みメモ

品質スキル・エコシステムを runtime consumer である veridia が取り込むための、
sqk-core 側インターフェースの要約。runtime artifacts への mapping・
orchestration・証跡収集の実装は veridia 側の責務であり、本書は扱わない
（[README「veridia との関係」](../../README.md#veridia-との関係)）。

## 取り込み単位

取り込みは**リポジトリ全体の checkout を commit SHA で固定する**ことを単位と
する。ディレクトリ単位の抜き出しは推奨しない。

**根拠**: `knowledge_refs` と SKILL.md 本文のリンクはリポジトリ相対パスで
書かれており、`skills/` 単体のコピーでは解決できない。参照先は domain canon
（`docs/`）に加え、`knowledge/` の derived artifacts、`schemas/`、さらに
`docs/agent-ecosystem/` の設計文書にも及ぶ（例: `quality-orchestrator` の
ルーティング表は
[`docs/agent-ecosystem/skill-ecosystem-design-plan.md`](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md)
にある）。

sqk-core はリリースタグを発行していない（`archive-sqkb-v1` は v1 履歴の
アーカイブ）。固定した SHA の付け替えをもって更新とし、スキル単位の互換性
判断には frontmatter の `version`（semver。authority は SKILL.md 自身 —
[D-010](../../DECISIONS.md#d-010-skillmd-version-の-authority)）を使う。

## 取り込み面（インターフェースとして安定させる範囲）

| 種別 | パス | 内容 |
| --- | --- | --- |
| skill blueprints | `skills/*/SKILL.md`（16ユニット） | portable frontmatter（`name` / `description` / `version` / `inputs` / `outputs` / `capabilities` / `knowledge_refs`）＋ 本文（目的・手順・最小入力契約・上流成果物なし時の振る舞い・出力エンベロープ） |
| skill I/O schemas | `schemas/*.schema.json` | ハンドオフエンベロープ（`handoff-envelope.schema.json`）を含む JSON Schema 群 |
| derived knowledge | `knowledge/` | 索引・用語表・mapping・test-space（derived, not canonical） |
| domain canon | `docs/`（`_research`・`migration` を除く） | `knowledge_refs` の解決先となる品質知識の正典 |

次は実行時の読み込み対象にしなくてよい。

- `docs/_research/` — non-canonical intake。`knowledge_refs` から参照されない
- `docs/migration/`・`MIGRATION.md`・`MIGRATION-SOURCES.sha256` — 移植の経緯
- `scripts/`・`tests/`・`.claude/`・`.github/` — sqk-core ローカルの検証・開発機構
- `.agent-work/` — dry-run 証跡。そもそもコミットされない（D-003）

## 実行境界（取り込み時に守ること）

- sqk-core のスキルは runtime-neutral blueprint であり、テスト実行・探索実行・
  証跡収集は veridia 側が担う（[D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)の実行境界）。
- veridia runtime artifact / evidence / gate mapping をスキルの出力契約へ
  混ぜない。必要な mapping は veridia 側のレイヤーで持つ（[phase2 実装ガイド
  共通受入基準 7・10](../../docs/agent-ecosystem/phase2-implementation-guide.md)）。
- 取り込み時に SKILL.md 原本を veridia 固有に書き換えない。差分が必要なら
  veridia 側の adapter で吸収し、原本への改善はフィードバック経路（後述）で
  sqk-core に還流させる。

## 消費形式

SKILL.md は Claude Code 互換形式である。Claude Code / Cowork 系 runtime なら
[`platforms/claude-code`](../claude-code/README.md) のシンボリックリンク方式で
そのまま発見・発火できる。それ以外の runtime へは
[ポータビリティ設計 §1・§2](../../docs/agent-ecosystem/portability-design.md#1-可搬スキルユニットの定義)
の portable frontmatter と能力→プラットフォーム対応表（`file_read` /
`file_write` / `shell` / `web_search`）から変換する。

## フィードバック経路

実実行ベースのスキル評価は、veridia が取り込んだ後のフィードバックとして
受け取る（[D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)）。
フィードバックは sqk-core の GitHub Issue または PR で受け、最低限次を含める。

- 対象スキルの `name` / `version` と、固定していた commit SHA
- 実行環境の要約（runtime 種別、`capabilities` の解決状況）
- 事象の区分: 出力エンベロープの schema 不整合／SKILL 手順・文言の曖昧さ／
  `knowledge_refs` の不足・誤り／ゲート判定（`gate_status`）の齟齬 等
- 再現材料（エンベロープ抜粋等）。ただし product-specific private data
  （product specs・品質基準・欠陥履歴）は本 public repo に持ち込まない
  （[skills/README「許可する知識ソース」](../../skills/README.md#許可する知識ソース)）

## 詳細

- 可搬スキルユニット仕様・能力対応表:
  [`docs/agent-ecosystem/portability-design.md`](../../docs/agent-ecosystem/portability-design.md)
- skills 原本ルール・レビュー観点: [`skills/README.md`](../../skills/README.md)
- schemas 一覧: [`schemas/README.md`](../../schemas/README.md)
