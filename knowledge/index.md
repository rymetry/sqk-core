# ナレッジ索引（トピック → 参照先）

出典: [ナレッジマネジメント設計 §5.2](../docs/agent-ecosystem/knowledge-management-design.md#52-knowledgeindexmd-の形式例) の形式例を初期形とする。
本ファイルは `docs/` の派生物であり、正典ではない。参照先が指す `docs/` 側の見出しが変わった場合は、本ファイルの該当行も更新すること（[knowledge-management-design.md §7](../docs/agent-ecosystem/knowledge-management-design.md#7-更新メンテナンスプロセス) の更新プロセス参照）。
`knowledge/` 全体の派生物ルールは [knowledge/README.md](README.md) を参照する。

## §5.2 サンプル（そのまま採用）

トピック文言は [knowledge-management-design.md §5.2](../docs/agent-ecosystem/knowledge-management-design.md#52-knowledgeindexmd-の形式例) のサンプル8行をそのまま採用する。参照先のアンカー部分は、同文書のサンプルが簡略化した見出しテキストを使っているため、`grep -n "^#"` で確認した実在の見出しに合わせて補正している（受入基準「参照先が全行実在すること」を満たすための補正であり、トピック文言・行の意図はサンプルのまま）。

| トピック | 参照先 |
| --- | --- |
| テスト条件の定義（JSTQB/29119差異） | knowledge/terminology/term-map.yaml#test-condition |
| ISO/IEC 25010 新旧特性対応 | docs/quality-models/iso25010-product-quality-model.md#2011-年版からの変更点 |
| リスクベーステスト戦略 | docs/test-techniques/testing-standards-and-assurance-concepts.md#4-リスクベーステスト-リスクをテスト深度に変換する |
| flaky test の実証データ | docs/test-techniques/testing-standards-and-assurance-concepts.md#6-flaky-test-非決定的テストの管理 |
| DORA 5指標 | docs/operations-quality/production-quality-sre-observability.md#dora-メトリクスデリバリーパフォーマンスの結果指標 |
| 探索的テストチャーター一覧（C01–C50） | docs/exploratory-testing/exploratory-testing-charter-catalog-by-tour.md |
| Goodhart の法則とメトリクスゲーミング | docs/quality-management/quality-metrics-pitfalls.md#goodhart-の法則と-campbell-の法則 |
| テスト空間3軸マトリクスの考え方 | knowledge/test-space/matrix-template.yaml |

## MVP 7スキル（#0〜#6）依存ナレッジ索引

出典: [skill-ecosystem-design-plan.md §3](../docs/agent-ecosystem/skill-ecosystem-design-plan.md#3-スキル定義一覧) の #0〜#6 の「依存ナレッジ・技法」欄。各行の参照先は `grep -n "^#"` で見出しの実在を確認済み。

| トピック | 参照先 |
| --- | --- |
| 品質トレーサビリティチェーン8ステップ推論（オーケストレーターの分類ロジック） | docs/quality-models/quality-knowledge-schema.md#3-ai-エージェントの推論手順 |
| ID体系と既存データ契約との対応 | docs/quality-models/quality-knowledge-schema.md#12-id-体系と既存データ契約との対応 |
| ノード間関係と双方向トレース（フォワード/バックワードトレース） | docs/quality-models/quality-knowledge-schema.md#14-ノード間関係と双方向トレース |
| RISKノードのデータ契約定義 | docs/quality-models/quality-knowledge-schema.md#risk-riskリスク |
| テストベース確認・静的レビュー（TRAの前段） | docs/test-techniques/test-process-research-summary-test-design.md#43-2-テストベース確認静的レビュー |
| テスト要求分析（TRA）の目的・入力・タスク・出力 | docs/test-techniques/test-process-research-summary-test-design.md#44-3-テスト要求分析tra |
| テストアーキテクチャー設計（TAD）の目的・入力・タスク・出力 | docs/test-techniques/test-process-research-summary-test-design.md#45-4-テストアーキテクチャー設計tad |
| テスト実行（TE）の目的・入力・タスク・出力 | docs/test-techniques/test-process-research-summary-test-design.md#48-7-テスト実行te |
| 再テスト・回帰テスト（変更関連テスト） | docs/test-techniques/test-process-research-summary-test-design.md#49-8-再テスト回帰テスト |
| フェーズ別レビューゲート（TRA/TAD/TDD/TIレビュー観点） | docs/test-techniques/test-process-research-summary-test-design.md#8-レビューゲート |
| アンチパターン集（分析から直接テストケース生成の禁止） | docs/test-techniques/test-process-research-summary-test-design.md#9-アンチパターン |
| 保証ステートメント説明テンプレート（「このテストは何を保証するか」） | docs/test-techniques/testing-standards-and-assurance-concepts.md#9-このテストは何を保証するか説明テンプレート |
| テストレベル×テストタイプ×技法の保証マトリクス | docs/test-techniques/testing-standards-and-assurance-concepts.md#3-テストレベル--テストタイプ--技法の保証マトリクス |
| flaky test の原因分類・定量管理（非決定的テストの管理） | docs/test-techniques/testing-standards-and-assurance-concepts.md#6-flaky-test-非決定的テストの管理 |
| テスト技法一覧（135技法、BB/WB/経験ベース等の分類） | docs/test-techniques/test-techniques-skill-catalog.md#3-テスト技法一覧 |
| skills化を優先すべき技法トップ20と状況→技法選択マトリクス | docs/test-techniques/test-techniques-skill-catalog.md#4-skills-化を優先すべき技法トップ20 |
| ISO/IEC 25010 2011年版からの変更点（新旧対応表の正典） | docs/quality-models/iso25010-product-quality-model.md#2011-年版からの変更点 |
| 要求から品質特性へマッピングする手順（AIエージェント向け5ステップ） | docs/quality-models/iso25010-product-quality-model.md#要求から品質特性へマッピングする方法 |
| 品質特性間のトレードオフと調停（nfr-reviewの必須出力根拠） | docs/quality-models/iso25010-product-quality-model.md#品質特性間のトレードオフと調停 |
| 証跡ベースのリリース判定チェックリスト（90項目、gap-analysis） | docs/quality-management/software-quality-gap-analysis-report.md#収集すべきアーティファクトチェックリスト |
| カウンターメトリクスの原則（Goodhart対策、release-judgmentが強制） | docs/quality-management/quality-metrics-pitfalls.md#原則-3-カウンターメトリクス対になる指標 |
| Goodhartの法則とCampbellの法則（メトリクスが目標になった瞬間の歪み） | docs/quality-management/quality-metrics-pitfalls.md#goodhart-の法則と-campbell-の法則 |
| hazard analysis の手法（FMEA/FTA/STPA、risk-analysisの技法選択） | docs/governance-compliance/domain-specific-quality-and-safety-standards.md#2-hazard-analysis-の手法 |
| 完全性水準の考え方（SIL・ASIL・DAL、影響度判定の参考） | docs/governance-compliance/domain-specific-quality-and-safety-standards.md#3-完全性水準の考え方silasildal |
| STRIDE（脅威モデリング技法、risk-analysisが参照） | docs/secure-development/secure-development-and-supply-chain.md#41-stride |
| 脅威モデリング全般（何が失敗しうるかを設計段階で列挙する） | docs/secure-development/secure-development-and-supply-chain.md#4-脅威モデリング-何が失敗しうるかを設計段階で列挙する |

## 関連ドキュメント

- [ナレッジマネジメント設計](../docs/agent-ecosystem/knowledge-management-design.md) — 本索引の設計根拠（3段階プログレッシブディスクロージャの第2段階）
- [スキル・エコシステム設計プラン](../docs/agent-ecosystem/skill-ecosystem-design-plan.md) — MVP 7スキルの依存ナレッジ一覧（§3）
