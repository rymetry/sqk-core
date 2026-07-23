# 派生ナレッジ artifacts

`knowledge/` は、canonical docs から派生した machine-readable / lookup-oriented artifacts を置く。ここにある内容は、それ自体では canonical ではない。

canonical prose は `_research` を除く `docs/` に置く。`knowledge/` と `docs/` が矛盾する場合は、まず canonical docs を更新し、その後に derived artifact を regenerate または手動で整合させる。

## 内容

| Path | Role |
| --- | --- |
| `index.md` | progressive disclosure 用の topic-to-document lookup index。 |
| `terminology/term-map.yaml` | 複数標準の terminology map と canonical term IDs。 |
| `mappings/` | canonical docs から抽出した machine-readable mappings。 |
| `test-space/` | test-space matrix rendering 用 templates。 |
| `dynamic/` | private project-specific knowledge 用 templates。commit する data は non-sensitive に限る。 |

## 派生物ルール

skill `knowledge_refs` で derived artifact を参照できるのは、source canonical docs / section が明示されている場合だけである。受入条件は以下とする。

- canonical docs 由来であり、`_research` 由来ではない。
- source document / section を記録または link している。
- docs-first update rule に従っている。
- independent source of truth として手編集されていない。
- 独自の `verification_state` model を導入していない。

## 更新順序

1. 必要に応じて `docs/_research/` の research candidates を triage する。
2. sources と claim scope を verify する。
3. `_research` 外の `docs/` にある canonical docs を更新する。
4. このディレクトリへの影響を確認する。
5. canonical docs の wording と anchors が安定した後に derived artifacts を更新する。

## レビュー観点

- 新規または変更した entry は canonical docs を指しているか。
- docs anchor の変更により `index.md` 更新が必要になっていないか。
- terminology 変更が `terminology/term-map.yaml` に影響していないか。
- quality taxonomy 変更が `mappings/` に影響していないか。
- `_research` から直接 content をコピーしていないか。該当する場合は、まず canonical docs へ promote する。
- project-specific / confidential content を追加していないか。該当する場合は、この public repository に入れない。
