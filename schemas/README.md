# リポジトリ内 schema

`schemas/` は、このリポジトリの skill I/O artifacts と local quality-skill outputs のための JSON Schema を置く。

これらの schema は repo-local contracts であり、export candidates でもある。veridia runtime schemas ではない。将来 veridia が import または mapping する場合、その mapping は veridia 側の planning / implementation で扱う。

## Skill I/O schema

- `assurance-statement.schema.json`
- `coverage-item.schema.json`
- `detailed-test-condition.schema.json`
- `handoff-envelope.schema.json`
- `release-decision.schema.json`
- `risk-item.schema.json`
- `test-architecture-element.schema.json`
- `test-case.schema.json`

## ルール

- 各 schema は `description` または関連 documentation で canonical source を示す。
- 新しい構造を導入する前に、既存の canonical docs と established IDs を優先する。
- `docs/_research/` から schema を直接 derive しない。
- veridia 固有の `GatePolicy`、`OracleSpec`、`Evidence`、`ExecutionEvidence`、runtime gate mapping をこのディレクトリに混ぜない。
- export bundles は generated / versioned downstream artifacts として扱い、hand-edited runtime state にしない。

## レビュー観点

- schema は canonical docs または repo-local design document を指しているか。
- ID pattern は existing canonical ID guidance と整合しているか。
- schema はこのリポジトリの skills に必要なものか。veridia runtime concern ではないか。
- product-specific data を避けているか。
- research-only claim を source verification なしに promote していないか。
