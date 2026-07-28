# 調査 intake

`docs/_research/` は、外部記事・論文・規格・tool documentation などの source candidates を置く non-canonical intake / staging area である。

このディレクトリの research material は、skills、`knowledge/`、schemas、export bundles の source of truth ではない。source verification、overlap checks、`_research` 外の canonical docs への promotion を経て初めて利用可能になる。

## ルール

- research IDs と canonical IDs を分ける。
- research candidates を adopted knowledge として扱わない。
- skill `knowledge_refs` から `docs/_research/` を直接参照しない。
- research cards から `knowledge/` を直接更新しない。
- research notes に出てくる veridia implementation candidates を、このリポジトリの runtime design にしない。
- 古い配置案や実装案を含む research notes は、必要なら research-only と注記して残す。

## 出典用語

research cards では、大まかな出典カテゴリを `source_layers[]` で表す。

- `primary-standard`
- `paper`
- `official-tool-doc`
- `official-guidance`
- `existing-doc`

source verification backlog は `source_records` を持つ。ここで official URLs、versions / editions、license notes、claim scopes、verification results、next actions を管理する。

旧フィールド名 `source_refs` は research-card field として使わない。RAG などの domain concept として "source refs" が本文に出る場合は、混同を避けるため言い換えるか、research-card field ではないことを明確にする。

## 昇格フロー

1. 候補を `_research` に capture する。
2. research ID、`source_layers[]`、`verification_state`、proposed destination を付けて classify する。
3. URL、edition、license、claim scope を source records で verify する。
4. 既存 canonical docs、technique IDs、terminology、mappings との overlap を確認する。
5. 確認済み claim scope だけを license-safe paraphrase で canonical docs へ promote する。
6. canonical docs が merge された後、`knowledge/` derived artifacts の更新要否を確認する。
7. skills は canonical docs、または source canonical docs が明示された derived artifacts だけを経由して更新する。

## 確認状態

- `not-yet-triaged`: candidate は capture 済みだが未レビュー。
- `needs-official-check`: primary / official source verification が必要。
- `partially-checked`: 一部の overlap または source confirmation はあるが、確認範囲が限定されている。
- `confirmed-for-scope`: `confirmed_scope` に書かれた範囲だけが確認済み。
- `licensed-text-needed`: 詳細確認に licensed source text が必要。public repo では要約に留める。
- `rejected`: 採用しない。

## 現在の調査レーン

- [Software Quality Technique Research](software-quality-technique-research/README.md)
- [ODC 欠陥タクソノミー調査](odc-defect-taxonomy/README.md)
- [日本発テスト設計技法調査](japanese-test-design-methods/README.md)
- [探索的テストの AI 実行境界調査](exploratory-ai-execution/README.md)
- [事業品質メトリクス（VOC・NPS・チャーン・LTV）調査](business-quality-metrics/README.md)
