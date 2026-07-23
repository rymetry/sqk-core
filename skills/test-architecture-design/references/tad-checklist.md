# TAD タスク・完了条件・レビュー観点 ポインタ表

## 位置づけ

本ファイルは `test-architecture-design` スキルの手順（[../SKILL.md](../SKILL.md)）
で参照する早見表である。タスクの詳細・完了条件・レビュー観点の解説は
docs/ 側の該当節が正典であり、本ファイルはそこへのポインタのみを提供する。
新規の解説は書かない。

## テストアーキテクチャー設計（TAD・§4.5）タスク・出力・完了条件

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| タスク1 | テスト全体を構造化する（機能単位／品質特性・テストタイプ単位／ソフトウェア設計責務単位／テストレベル単位／テストサイクル単位） | [test-process-research-summary-test-design.md §4.5 タスク1](../../../docs/test-techniques/test-process-research-summary-test-design.md#45-4-テストアーキテクチャー設計tad) |
| タスク2 | 要素間の関係を明らかにする（依存、重複、委譲、上位/下位、影響範囲） | 同上 タスク2 |
| タスク3 | リスクや責務分担に応じて厚みを決める（厚く見る、標準的に見る、絞って見る、別レベルへ委譲する） | 同上 タスク3 |
| タスク4 | 詳細なテスト条件の担当グループを決める（重複を避ける、漏れをなくす、トレーサビリティを作れる単位にする） | 同上 タスク4 |
| タスク5 | 割り当てたテスト条件を調整する（顧客影響、他機能影響、利用頻度、コード複雑度、変更量、下位レベルでの担保状況） | 同上 タスク5 |
| 出力 | `TestArchitectureModel` / `TestElementList` / `ElementRelationshipMap` / `TestThicknessPolicy` / `ConditionAssignmentMatrix` / `AdjustedDetailedTestConditionList` | 同上 出力 |
| 完了条件 | テスト全体の「整理棚」がある／各詳細テスト条件をどこで扱うかが決まっている／高リスク領域が厚く低リスク領域が必要十分に絞られている／TDD が迷わずカバレッジアイテムを決められる | 同上 完了条件 |

## データ契約

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| ID体系 | `TAE-nnn`（テストアーキテクチャ要素） | [test-process-research-summary-test-design.md §6.1 基本ID体系](../../../docs/test-techniques/test-process-research-summary-test-design.md#61-基本-id-体系) |
| TAE スキーマ | `id` / `name` / `element_type` / `test_level` / `test_type` / `test_cycle` / `risk_level` / `thickness` / `assigned_conditions` / `delegated_to` / `rationale` | [test-process-research-summary-test-design.md §6.3 TestArchitectureElement](../../../docs/test-techniques/test-process-research-summary-test-design.md#63-testarchitectureelement)、[schemas/test-architecture-element.schema.json](../../../schemas/test-architecture-element.schema.json) |

## テストレベル×テストタイプ×技法の保証マトリクス（§3）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| レベル別の保証範囲 | コンポーネント／コンポーネント統合／システム／システム統合／受け入れの各レベルで「保証できること」「保証できないこと」「代表的な技法」 | [testing-standards-and-assurance-concepts.md §3](../../../docs/test-techniques/testing-standards-and-assurance-concepts.md) |
| タイプ別の保証言明形式 | 機能／非機能／ブラックボックス／ホワイトボックスごとの保証の言明形式と網羅・判定モデル | 同上 |

## リスク→テスト深度の変換手順（§4.2）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| 変換手順 | リスク識別→リスク分析→深度への変換→優先順位への変換→リスクモニタリングの循環 | [testing-standards-and-assurance-concepts.md §4.2](../../../docs/test-techniques/testing-standards-and-assurance-concepts.md) |
| 深度ポリシー表 | リスクレベル（高/中/低）ごとの技法の厚み・カバレッジ目標・実行順序/回帰頻度の対応 | 同上 |

## TAD レビューゲート観点（§8.2）

| 観点 | チェック内容 | 出典 |
| --- | --- | --- |
| 構造 | テスト全体が意味のある単位に分けられているか | [test-process-research-summary-test-design.md §8.2 TADレビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#82-tad-レビュー) |
| 関係 | 要素間の依存、重複、委譲が見えるか | 同上 |
| 厚み | リスクに応じて厚く見る箇所と絞る箇所が説明できるか | 同上 |
| 担当 | 詳細テスト条件をどこで扱うか決まっているか | 同上 |
| 重複・漏れ | 同じ条件を見すぎていないか、誰も見ない条件がないか | 同上 |
| 粒度 | TDD に渡せる粒度へ調整されているか | 同上 |

## アンチパターン（§9・本スキル関連分のみ抜粋）

| アンチパターン | 対策 | 出典 |
| --- | --- | --- |
| いきなりテストケースを生成する | TRA → TAD → TDD の順で通す | [test-process-research-summary-test-design.md §9 アンチパターン](../../../docs/test-techniques/test-process-research-summary-test-design.md#9-アンチパターン) |
| テスト観点を全部同じ型で扱う | 内部データ型（HTC/DTC/TAE等）を分ける | 同上 |
| トレーサビリティを最後に作る | 最初から ID とリンクを付与する | 同上 |
