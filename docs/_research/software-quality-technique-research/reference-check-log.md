# Reference Check Log

作成日: 2026-07-08

このログは、v3研究インデックス隔離作業の受入確認を記録する。結果はこのPR時点のローカル状態であり、canonical docsへの採用根拠ではない。

## Commands

```sh
rg "veriserve|HQW" knowledge README.md docs/README.md
```

結果: 該当なし。未検証HQW内容は `knowledge/`、ルート `README.md`、`docs/README.md` に混入していない。

```sh
rg "docs/_external-gaps" docs
```

結果: `_research/software-quality-technique-research/` 内のv3原文、または廃止された配置案の説明だけに出現する。ゼロ件条件ではない。

```sh
rg "GatePolicy|OracleSpec|Evidence|veridia" docs/_research/software-quality-technique-research
```

結果: v3原文、または本repoのKB登録対象外であることを示す除外説明に限定される。

```sh
rg "knowledge_refs|_research" skills docs/_research/software-quality-technique-research docs/README.md
```

結果: skills側には既存の `knowledge_refs` 見出しだけがあり、`_research` を直接参照する `knowledge_refs` はない。`_research` への言及は研究領域内の説明と `docs/README.md` の非正典説明に限定される。

```sh
rg --files | rg "veriserve|work/"
```

結果: 移動後のv3ファイルのみ。v3が言及する `work/veriserve_articles.jsonl` は現repoには存在しない。
