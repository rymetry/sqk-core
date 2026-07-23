# v1 から sqk-core への移植

## 経緯

v1（`software-quality-knowledge-base`）では、ガバナンス機構が約57,000行に膨張し、約14,000行の知識本体のおよそ4倍になった。v2 の `sqk-core` では、価値の核となる品質知識、skill、repo-local contract を、最小限のガバナンスで維持するために選択移植した。

## Keep / transform / drop

| 区分 | 対象 | 扱い |
| --- | --- | --- |
| keep（as-is） | `docs/exploratory-testing/`、`docs/governance-compliance/`、`docs/human-centered-quality/`、`docs/operations-quality/`、`docs/quality-management/`、`docs/quality-models/`、`docs/secure-development/`、`docs/test-techniques/` | v1 原文をディレクトリ構造ごと移植 |
| keep（as-is） | `docs/_research/`、`skills/`、`knowledge/`、`platforms/` | v1 原文をディレクトリ構造ごと移植 |
| keep（as-is） | `schemas/` の skill I/O 8件 | `assurance-statement`、`coverage-item`、`detailed-test-condition`、`handoff-envelope`、`release-decision`、`risk-item`、`test-architecture-element`、`test-case` の各 schema のみ移植 |
| transform | `docs/agent-ecosystem/` の7文書 | active / historical / final report / backlog material の v2 status を明示し、v1 の Execution freeze を superseded と記録 |
| transform | `schemas/README.md`、`AGENTS.md`、skill symlink | v2 の8 I/O schema、検証コマンド、単一 skill source に合わせて再構成 |
| drop | governance schema 5件 | `architecture-trace-link`、`artifact-registry`、`dependency-registry`、`g0-activation-config`、`section-registry` を移植しない |
| drop | `docs/agent-ecosystem/` の上記7文書以外、v1 の `docs/README.md` | v2 の最小ガバナンスに不要、または後続 Task で新規作成するため移植しない |
| drop | `provenance/`、v1 由来の `scripts/` と `tests/` | v1 の重いガバナンス実装を移植しない |
| drop | 将来の `research/` 独立 source root への移行構想 | v1 Evolution Plan の migration stage に属する構想であり、Plan と共に移植しない。必要になれば [ROADMAP.md](./ROADMAP.md) で再提案する |

## 移植の完全性

as-is 対象は source commit `ced0ccc495b45a37a446a20319674a6d2468262b` から67パスを列挙し、リポジトリ直下の `MIGRATION-SOURCES.sha256` に repo-relative path と SHA-256 を記録した。コピー直後と最終 tree の双方で `shasum -a 256 -c MIGRATION-SOURCES.sha256` を実行し、67件すべてが一致することを検証した。

## v1 履歴の所在

- Release: `archive-sqkb-v1`（https://github.com/rymetry/sqk-core/releases/tag/archive-sqkb-v1）。Task 5 で作成済み。ダウンロード後の SHA-256 照合・bundle clone・`git fsck --full`・タグ commit 照合による復旧検証も完了している。
- 公開 bundle: `sqk-v1-public.bundle`
  - SHA-256: `6bc2c2e603038fbe1bf90931ba068bbcd002d0e8c9c003d44ceccf014d3b551c`
  - サイズ: 2,022,458 bytes
  - source commit: `ced0ccc495b45a37a446a20319674a6d2468262b`
- bundle 内部タグは `v1-final`、Release タグは `archive-sqkb-v1` で名称が異なる。bundle から復元するときは、bundle 内の `v1-final` を参照する。

## Authority の対応

v1 の provenance 機構で扱っていた出典、`derived_from`、`knowledge_refs`、authority 区分は、v2 では文書内出典、Git 履歴、後続の意思決定記録へ次のように対応させる。

| v1 の仕組み | v2 での維持方法 |
| --- | --- |
| 文書内の出典 | 文書内出典をそのまま保持し、知識主張の根拠を追跡する |
| `derived_from` | Git 履歴と `MIGRATION-SOURCES.sha256` により、移植元 commit とコピー時の同一性を追跡する |
| skill の `knowledge_refs` | repo-root 相対参照を保持し、`scripts/check.py` で実在性を検証する |
| authority 区分 | 文書内出典、Git 履歴、および Task 4 で作成した [DECISIONS.md](./DECISIONS.md) によって判断根拠を維持する |

## Metadata archive

v1 の PR / Issue / review metadata export は `v1-github-metadata.tar.gz` として非公開のローカルバックアップに保管する。

- SHA-256: `3bb0bc3ec51031644216e02da683ff4ebfa292dbf80c271f228d88a855424937`
- サイズ: 84,168 bytes
