# TRA タスク・完了条件・レビュー観点 ポインタ表

## 位置づけ

本ファイルは `test-requirement-analysis` スキルの手順（[../SKILL.md](../SKILL.md)）
で参照する早見表である。タスクの詳細・完了条件・レビュー観点の解説は
docs/ 側の該当節が正典であり、本ファイルはそこへのポインタのみを提供する。
新規の解説は書かない。

## テストベース確認・静的レビュー（§4.3）タスク・出力

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| タスク | テストベースの一覧化、版数・更新日・対象範囲・信頼度の記録、曖昧・矛盾・未定・不足・観測不能・制御不能の抽出、レビュー指摘とテスト影響の紐づけ | [test-process-research-summary-test-design.md §4.3 タスク](../../../docs/test-techniques/test-process-research-summary-test-design.md#43-2-テストベース確認静的レビュー) |
| 出力 | `TestBasisInventory` / `ReviewFindingList` / `TestabilityIssueList` | 同上 |

## テスト要求分析（TRA・§4.4）タスク・出力・完了条件

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| タスク1 | ユーザー視点で使われ方を理解する（よく使われる操作、失敗すると困る利用シーン、初心者と常連の違い、時間帯・イベントによる変化） | [test-process-research-summary-test-design.md §4.4 タスク1](../../../docs/test-techniques/test-process-research-summary-test-design.md#44-3-テスト要求分析tra) |
| タスク2 | プロダクト視点で仕組みを理解する（機能構成、外部連携、データ保持・更新箇所、複雑で壊れやすい箇所） | 同上 タスク2 |
| タスク3 | テスト・組織視点で全体像を整理する（テストレベル・タイプ・サイクル、責任分担） | 同上 タスク3 |
| タスク4 | プロダクトリスクを識別・評価する（影響度、発生しやすさ、必要に応じ検出しにくさ） | 同上 タスク4 |
| タスク5〜6 | ハイレベルテスト条件（HTC）と詳細テスト条件（DTC）を識別する | 同上 タスク5・6 |
| タスク7 | テストパラメーターを識別する | 同上 タスク7 |
| タスク8 | 不明点・仮定・確認事項を分ける | 同上 タスク8 |
| 出力 | `UserUsageModel` / `ProductStructureModel` / `TestOverviewMap` / `RiskRegister` / `HighLevelTestConditionList` / `DetailedTestConditionList` / `TestParameterCandidateList` / `OpenQuestionList` | 同上 出力 |
| 完了条件 | 「何を確認するか」がテスト条件として説明できる／高リスク領域が説明できる／詳細設計へ渡すテスト条件とパラメーターが分離されている | 同上 完了条件 |

## データ契約

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| ID体系 | `HTC-nnn`（ハイレベルテスト条件）／`DTC-nnn`（詳細テスト条件） | [test-process-research-summary-test-design.md §6.1 基本ID体系](../../../docs/test-techniques/test-process-research-summary-test-design.md#61-基本-id-体系) |
| DTC スキーマ | `id` / `title` / `source_refs` / `high_level_condition_id` / `risk_refs` / `precondition_hint` / `action_hint` / `expected_behavior_hint` / `postcondition_hint` / `unknowns` / `status` | [test-process-research-summary-test-design.md §6.2 DetailedTestCondition](../../../docs/test-techniques/test-process-research-summary-test-design.md#62-detailedtestcondition)、[schemas/detailed-test-condition.schema.json](../../../schemas/detailed-test-condition.schema.json) |

## TRA レビューゲート観点（§8.1）

| 観点 | チェック内容 | 出典 |
| --- | --- | --- |
| 使われ方 | 利用者、頻度、重要シーン、失敗時影響を理解しているか | [test-process-research-summary-test-design.md §8.1 TRAレビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#81-tra-レビュー) |
| 仕組み | 機能構成、外部連携、データ更新、複雑箇所を理解しているか | 同上 |
| 全体像 | テストレベル、タイプ、サイクル、責務が整理されているか | 同上 |
| リスク | 影響度と発生しやすさで優先度が説明できるか | 同上 |
| テスト条件 | ハイレベル条件と詳細条件が分離されているか | 同上 |
| パラメーター | 振る舞いを変える要素を識別しているか | 同上 |
| 不明点 | 推測と確認済み事実を分けているか | 同上 |

## アンチパターン（§9・本スキル関連分のみ抜粋）

| アンチパターン | 対策 | 出典 |
| --- | --- | --- |
| いきなりテストケースを生成する | TRA → TAD → TDD の順で通す | [test-process-research-summary-test-design.md §9 アンチパターン](../../../docs/test-techniques/test-process-research-summary-test-design.md#9-アンチパターン) |
| テスト観点を全部同じ型で扱う | 内部データ型（HTC/DTC等）を分ける | 同上 |
| トレーサビリティを最後に作る | 最初から ID とリンクを付与する | 同上 |
