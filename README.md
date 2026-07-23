# sqk-core

`sqk-core` は、ソフトウェア品質に関する canonical docs、用語・taxonomy・technique IDs、runtime-neutral skill blueprints、machine-readable derived knowledge を管理する knowledge-core repository である。v1 の価値の核を維持しつつ、最小限のガバナンスで再出発する。再構築と移植の経緯は [MIGRATION.md](./MIGRATION.md) を参照する。

## レイヤーモデル

| Layer | Path | 責務 |
| --- | --- | --- |
| Research intake | `docs/_research/` | 外部記事・論文・規格・未検証候補の staging（non-canonical） |
| Domain canon | `docs/`（`_research`・`agent-ecosystem`・`migration` を除く） | 品質知識の人間可読な source of truth |
| Product control docs | `docs/agent-ecosystem/` | skill ecosystem の設計・報告（domain canon とは authority が別） |
| 出典・意思決定の追跡 | 文書内出典 + git 履歴 + [DECISIONS.md](./DECISIONS.md) | v1 の provenance registry 機構に代わり、出典・`derived_from`・authority 区分を維持 |
| Derived knowledge | `knowledge/` | canonical docs から抽出した索引・用語表・mapping（derived, not canonical） |
| Skill blueprints | `skills/` | platform-neutral な `SKILL.md` 原本（7ユニット） |
| Local schemas | `schemas/` | skill I/O 用 JSON Schema 8件（repo-local contract） |
| Platform adapters | `platforms/` | 各実行環境向け導入メモ |
| Runtime consumer | veridia（別リポジトリ・将来） | runtime 実装は out of scope |

## 担うこと

- ソフトウェア品質に関する canonical docs
- 共有する terminology、taxonomy、technique IDs
- platform-neutral な skill blueprints
- canonical docs から導出する索引・用語表・mapping
- skill I/O の repo-local schemas
- 将来の下流 runtime consumer へ提供しうる export candidates（stable knowledge、blueprint、taxonomy、schema。runtime artifacts への mapping は consumer 側）
- source verification 前の候補を隔離する research intake

## 担わないこと

- veridia の runtime 実装と veridia 固有 contracts
- 実行可能な `qa-skills` や product 固有の品質基準
- source verification 前の research candidate の canonical 化
- `docs/_research/` を skill の `knowledge_refs` から直接参照すること

## Research から canonical docs への昇格

research candidate は `docs/_research/` で開始し、`RC-HQW-*` などの research ID を使う。canonical ID と technique ID は canonical docs 側でのみ導入する。

canonical docs へ昇格する前に、次を確認する。

1. claim scope が confirmed である。
2. source record に license note がある。
3. 既存 docs と technique IDs との重複を確認している。
4. canonical destination が確定している。
5. `knowledge/` への影響を確認している。
6. skill の `knowledge_refs` から `docs/_research/` を直接参照していない。

`knowledge/` は canonical docs の更新後に追随する派生物であり、research card から直接更新しない。

## veridia との関係

veridia は将来の runtime consumer である。本リポジトリは、veridia が将来 import しうる stable knowledge、blueprint、taxonomy、schema を提供しうるが、runtime artifacts への mapping は veridia 側で扱う。

## ガードレール

- secrets やローカル環境固有の状態をコミットしない。
- `main` へ直接 push せず、変更は PR 経由で反映し、merge は人間が判断する。
- `main` への force push を禁止する。hook は `main` 宛の push（force を含む）をブロックする。
- conflict marker を残したまま作業を終えない。
- source verification なしに `docs/_research/` の内容を canonical 化しない。
- research card から `knowledge/` を直接更新しない。

## 再発防止原則

v1 ではガバナンス機構が知識本体の約4倍に膨張した。この再発を避けるため、次を原則とする。

1. control file（実行を統制するメタ機構のファイル）は0〜1件に保つ。
2. レビューで同一指摘が2巡残ったら自動続行せず停止し、owner が simplify / defer / abandon を判断する。
3. consumer のいない仕組みを作らない。複数人・外部 consumer・運用事故という実需が現れるまで、多段ゲートを導入しない。
4. governance を追加するときは、何の実害を防ぐかという根拠を明示する。
5. メタ文書量は警告指標として扱い、hard gate にしない。

## 検証

```bash
uv run scripts/check.py
uv run --with pytest --with jsonschema --with pyyaml pytest tests/ -v
```

## ライセンス

[MIT License](./LICENSE)
