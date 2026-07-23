# Software Quality Technique Research

このディレクトリは、ソフトウェア品質・テスト技法に関する検証前候補を一時的に置く研究領域である。ここにある内容は正典ドキュメントではない。

`docs/_research/` 全体の共通ルールは [../README.md](../README.md) を参照する。

## 位置づけ

- `docs/` の各カテゴリは正典の散文であり、`knowledge/` はそこから抽出した派生物である。
- `_research/` は正典化前の隔離場所であり、一次情報確認・分類設計・重複確認のためだけに使う。
- skills の `knowledge_refs` は `_research` を直接参照しない。スキルが参照してよいのは、検証後に canonical docs へ分配された内容である。
- `knowledge/terminology/term-map.yaml`、`knowledge/index.md`、`knowledge/mappings/` は、canonical docs 側の変更が確定した後にだけ同期する。
- 研究カードの `source_layers[]` は出典カテゴリを表す。URL・版・ライセンス・claim scope は `source-verification-backlog.md` の `source_records` で管理する。

## 現在の研究入力

| ファイル | 位置づけ |
| --- | --- |
| `veriserve-hqw-article-essence-index-v3.md` | HQW記事群から抽出した研究インデックス。原文保存を優先し、本文中の登録先候補や実装候補を採用済みとは扱わない。 |
| `detailed-research-plan.md` | v3を分解・検証・分配するための作業計画。 |
| `knowledge-candidate-register.md` | 研究候補カード。全件skeletonと一部詳細カードを持つ。 |
| `distribution-matrix.md` | 既存docsへの分配表、Phase 2/3判定、PR分割。 |
| `source-verification-backlog.md` | 一次情報・規格・論文・公式実装の確認待ち一覧。 |
| `reference-check-log.md` | この研究領域を作成した時点の参照確認ログ。 |

## 分配先

検証済みの内容は、既存カテゴリへ分配する。

- `quality-models/`
- `test-techniques/`
- `secure-development/`
- `governance-compliance/`
- `operations-quality/`
- `human-centered-quality/`
- `quality-management/`

v3本文をそのまま恒久ドキュメント化しない。特に、v3内の実装候補や外部ギャップ配置案は、一次情報確認と既存docsとの重複確認を通して再分類する。

## 廃止された配置案の扱い

v3本文には `docs/_external-gaps/` という旧配置案が残っている。これは原文由来の未採用案であり、新しいトップレベルカテゴリとして作らない。HQW外の補完候補は、まずこの研究領域内で `origin_layer: external-gap` として隔離する。

## 登録判断

研究カードの `KB登録判断` は次のいずれかに限定する。

- `adopt`: 一次情報確認済みで、既存カテゴリへの登録先も決まっている。
- `merge`: 既存docsや既存技法IDへ補強として統合する。
- `defer`: 有望だが確認・分類・出典整理が不足している。
- `reject`: このrepoのKB対象外、または誤用リスクが高く採用しない。
- `external-gap`: HQW外の補完候補として、HQW由来候補と混ぜずに扱う。
- `existing-additional-candidate`: 既に `test-technique-status-assessment.csv` 等に追加候補として存在する。

## 出典用語

- `source_layers[]`: 研究カード上の出典カテゴリ。`primary-standard` / `paper` / `official-tool-doc` / `official-guidance` / `existing-doc` を使う。
- `source_records`: `source-verification-backlog.md` の行。`official_url`, `version_or_edition`, `license_note`, `claim_scope`, `verification_result` を持つ。
- `source_refs`: 研究カードのフィールド名としては使わない。RAG 等の概念語として残す場合は、field 名ではないことを明確にする。
