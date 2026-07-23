# パイプラインゲート基準（シード）

## 位置づけ

本ファイルは quality-orchestrator が4段階複合フロー（risk-analysis 並行
→ TRA → TAD → TDD/TI）の各段を進めてよいかを判定するためのゲート基準
シードである（[skill-ecosystem-design-plan.md §4「ゲート基準」](../../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#4-オーケストレーション設計)
の表をそのまま採用）。各行の詳細チェックリストは
[test-process-research-summary-test-design.md §8](../../../docs/test-techniques/test-process-research-summary-test-design.md#8-レビューゲート)
の該当節を参照する。

## 変更凍結の注記

[phase1-implementation-guide.md T4](../../../docs/agent-ecosystem/phase1-implementation-guide.md) の
routing-table.md と同様、判断に迷った場合の追加・変更は Phase 1 中は禁止する。
統合試行（T12）の結果を根拠に PR で改訂すること。

## ゲート表

| フェーズ | ゲート観点（要約） | 詳細チェックリスト |
|---|---|---|
| TRAレビュー | 使われ方・仕組み・全体像・リスク・テスト条件・パラメーター・不明点の分離 | [§8.1 TRA レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#81-tra-レビュー) |
| TADレビュー | 構造・関係・厚み・担当・重複漏れ・粒度 | [§8.2 TAD レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#82-tad-レビュー) |
| TDDレビュー | パラメーター・値候補・制約・カバレッジ・技法・期待結果・ケース数 | [§8.3 TDD レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#83-tdd-レビュー) |
| TIレビュー | 実行順序・手順・自動化・証跡・再現性 | [§8.4 TI レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#84-ti-レビュー) |

成果物そのものの文書品質（文書点・工程一貫性・トレーサビリティ・説明責任・
技術的妥当性）まで踏み込んで見たい場合は
[§8.5 成果物品質レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#85-成果物品質レビュー)
も参照する（MVP のオーケストレーターは§8.1〜§8.4を主判定に使い、§8.5は
補助観点とする）。

## `gate_status` 3値と遷移

各段のハンドオフエンベロープの `gate_status` を、対応するフェーズの
チェックリスト（上表）に照らして判定し、次の遷移を適用する。

| `gate_status` | 判定方法 | 遷移 |
|---|---|---|
| `passed` | 該当フェーズの観点をすべて満たし、`assumptions`/`open_questions` が実質空 | 次段へそのまま進める |
| `passed-with-risks` | 観点の大半は満たすが、`assumptions` または残存リスクがある | 残存リスクを利用者・次段の入力に明示した上で次段へ進める |
| `blocked` | 観点の欠落が大きい、または前段スキル自身が `blocked` を返した | 次段へ進めず、利用者に理由を添えて返す |

## 関連ドキュメント

- [routing-table.md](./routing-table.md) — 第2段階ルーティング表（同様に Phase 1 中変更凍結）
- [skill-ecosystem-design-plan.md §4](../../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#4-オーケストレーション設計) — ゲート基準の正典
