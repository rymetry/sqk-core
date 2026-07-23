# スキル原本

`skills/` は、ソフトウェア品質 skills の source blueprints を置く。ここにあるファイルは runtime-neutral な SKILL.md units であり、adapters を通じて agent platforms 間で持ち運ぶための原本である。

これらは veridia executable `qa-skills` packages ではない。veridia runtime orchestration、evidence storage、gate execution、product-specific policy も実装しない。

## 原本ルール

- 各 skill は platform-neutral blueprint として保つ。
- `knowledge_refs` は canonical docs、または source canonical docs が明示された derived artifacts だけを指す。
- `knowledge_refs` から `docs/_research/` を直接参照しない。
- canonical docs の長い本文を SKILL.md にコピーしない。必要な箇所への pointer を優先する。
- platform-specific conversion details は `platforms/` に置く。
- veridia runtime mappings をこの source blueprints に混ぜない。

## 許可する知識ソース

| Source | Allowed? | Notes |
| --- | --- | --- |
| `_research` を除く `docs/` | Yes | canonical prose。 |
| `knowledge/` | Yes, with source docs explicit | derived artifact only。 |
| `docs/_research/` | No | non-canonical intake。 |
| product-specific private data | No | この public repo は product specs、quality criteria、defect history を保持しない。 |

## レビュー観点

- frontmatter は portable keys（`name`, `description`, `version`, `inputs`, `outputs`, `capabilities`, `knowledge_refs`）を持つか。
- `capabilities` は必要最小限か。
- すべての `knowledge_refs` は解決できるか。
- すべての `knowledge_refs` は canonical docs、または source-explicit derived artifacts か。
- `knowledge_refs` から `_research` が除外されているか。
- skill は veridia runtime package ではなく blueprint のままか。
