# docs

`docs/` は、domain canon、non-canonical な research intake、skill ecosystem の product control docs、移行期間限定文書を区分して置く。各区分の authority は同一ではない。

## 構成

### Domain canon

次の8ディレクトリは、ソフトウェア品質知識の人間可読な source of truth である。

| Path | 主題 |
| --- | --- |
| `exploratory-testing/` | 探索的テスト |
| `governance-compliance/` | ガバナンス・規制・標準 |
| `human-centered-quality/` | アクセシビリティ・UX・人間中心品質 |
| `operations-quality/` | 本番品質・SRE・observability |
| `quality-management/` | 品質保証・品質管理・metrics |
| `quality-models/` | 品質モデルと知識 schema |
| `secure-development/` | セキュア開発と supply chain |
| `test-techniques/` | テスト技法・プロセス・assurance |

### その他

| Path | 位置づけ |
| --- | --- |
| [`_research/`](./_research/) | 外部記事・論文・規格・未検証候補を置く non-canonical staging |
| [`agent-ecosystem/`](./agent-ecosystem/) | skill ecosystem の設計・報告を置く product control docs |
| [`migration/`](./migration/) | v1 から v2 への移行計画など、移行期間限定の文書 |

## agent-ecosystem の位置づけ

`agent-ecosystem/` の7文書は、各文書冒頭の `v2 status` に従って扱う。

| v2 status | 文書 | 扱い |
| --- | --- | --- |
| active | [skill-ecosystem-design-plan.md](./agent-ecosystem/skill-ecosystem-design-plan.md) | skill ecosystem 設計の正典 |
| active | [knowledge-management-design.md](./agent-ecosystem/knowledge-management-design.md) | knowledge management 設計の正典 |
| active | [portability-design.md](./agent-ecosystem/portability-design.md) | portability 設計の正典 |
| historical | [phase1-implementation-guide.md](./agent-ecosystem/phase1-implementation-guide.md) | Phase 1 実装時の手順書。現行手順としては参照しない |
| final report | [phase1-integration-trial-report.md](./agent-ecosystem/phase1-integration-trial-report.md) | Phase 1 統合試行の完了報告・記録 |
| final report | [phase1b-coldstart-trial-report.md](./agent-ecosystem/phase1b-coldstart-trial-report.md) | Phase 1b コールドスタート検証の完了報告・記録 |
| backlog material | [phase2-implementation-guide.md](./agent-ecosystem/phase2-implementation-guide.md) | Phase 2 再評価の素材。作業順序は [ROADMAP.md](../ROADMAP.md) を参照 |

## Authority の違い

domain canon は品質知識そのものの source of truth である。一方、`agent-ecosystem/` は、その知識を利用する skill ecosystem の構造、実装時の記録、将来候補を扱う product control docs であり、domain canon ではない。

active な設計3文書は skill ecosystem 設計に対する authority を持つが、historical、final report、backlog material は現在の手順や確定済み実装範囲を直接規定しない。Phase 2 の着手順序と再評価は [ROADMAP.md](../ROADMAP.md) に従う。
