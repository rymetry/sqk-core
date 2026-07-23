# TDD/TI タスク・完了条件・レビュー観点・技法選択 ポインタ表

## 位置づけ

本ファイルは `test-design-implementation` スキルの手順（[../SKILL.md](../SKILL.md)）
で参照する早見表である。タスクの詳細・完了条件・レビュー観点・技法選択の
解説は docs/ 側の該当節が正典であり、本ファイルはそこへのポインタのみを
提供する。新規の解説は書かない。

## テスト詳細設計（TDD・§4.6）タスク・出力・完了条件

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| タスク1 | テストパラメーターと値候補を仮決めする（入力値、状態、事前条件、環境条件、データ状態、操作回数） | [test-process-research-summary-test-design.md §4.6 タスク1](../../../docs/test-techniques/test-process-research-summary-test-design.md#46-5-テスト詳細設計tdd) |
| タスク2 | リスクと厚みに応じて値候補を追加・削除する | 同上 タスク2 |
| タスク3 | 組合せ爆発を避ける（同値分割、境界値分析、デシジョンテーブル、状態遷移、ペアワイズ／組合せテスト、エラー推測、チェックリスト） | 同上 タスク3 |
| タスク4 | テストカバレッジアイテムを定義する | 同上 タスク4 |
| タスク5 | テストケースを作成する | 同上 タスク5 |
| タスク6 | 期待結果、事後条件、観測点を明示する | 同上 タスク6 |
| タスク7 | テストデータ要件と環境要件を更新する | 同上 タスク7 |
| 出力 | `TestParameterList` / `ValueCandidateList` / `ConstraintList` / `CoverageItemList` / `TestCaseList` / `ExpectedResultList` / `TestDataRequirementList` / `TestEnvironmentRequirementList` | 同上 出力 |
| 完了条件 | 各テストケースの根拠となる詳細テスト条件とカバレッジアイテムが追える／期待結果が判定可能である／ケース数が必要十分に絞られている | 同上 完了条件 |

## テスト実装（TI・§4.7）タスク・出力・完了条件

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| タスク1 | テストケースをテストスイートにまとめる | [test-process-research-summary-test-design.md §4.7 タスク1](../../../docs/test-techniques/test-process-research-summary-test-design.md#47-6-テスト実装ti) |
| タスク2 | テストプロシジャーを作る | 同上 タスク2 |
| タスク3 | 実行順序を決める（前提条件を満たす順序、同じ準備データでまとめられる順序、環境切替が少ない順序、重要ケースを先に実行する順序、異常終了時の影響が小さい順序） | 同上 タスク3 |
| タスク4 | テストデータを作る | 同上 タスク4 |
| タスク5 | テスト環境を構築・確認する | 同上 タスク5 |
| タスク6 | 手動手順または自動化スクリプトを作る | 同上 タスク6 |
| タスク7 | 実行ログ、証跡、判定方法を定義する | 同上 タスク7 |
| 出力 | `TestSuiteList` / `TestProcedureList` / `ExecutionSchedule` / `ManualTestScript` / `AutomatedTestScript` / `PreparedTestData` / `VerifiedTestEnvironment` | 同上 出力 |
| 完了条件 | 実行者が迷わず実行できる／自動化する場合、スクリプトが環境、データ、期待結果と紐づく／実行順序の理由が説明できる | 同上 完了条件 |

## データ契約

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| ID体系 | `COV-nnn`（カバレッジアイテム）／`TC-nnn`（テストケース） | [test-process-research-summary-test-design.md §6.1 基本ID体系](../../../docs/test-techniques/test-process-research-summary-test-design.md#61-基本-id-体系) |
| CoverageItem スキーマ | `id` / `condition_id` / `architecture_element_id` / `parameters` / `expected_result` / `coverage_rationale` | [同 §6.4 CoverageItem](../../../docs/test-techniques/test-process-research-summary-test-design.md#64-coverageitem)、[schemas/coverage-item.schema.json](../../../schemas/coverage-item.schema.json) |
| TestCase スキーマ | `id` / `coverage_item_refs` / `preconditions` / `test_data_refs` / `steps` / `expected_results` / `priority` | [同 §6.5 TestCase](../../../docs/test-techniques/test-process-research-summary-test-design.md#65-testcase)、[schemas/test-case.schema.json](../../../schemas/test-case.schema.json) |

## 技法選択マトリクス（カタログ §7）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| 状況→第一候補／第二候補の対応表 | 入力範囲がある→境界値分析(BB-02)、条件分岐が多い→デシジョンテーブル(BB-03)、状態を持つ→状態遷移テスト(BB-05)、環境・設定が多い→組合せテスト(COM-01〜04)、正解出力が作りにくい→メタモルフィックテスト(META-01) 等、全14状況の対応 | [test-techniques-skill-catalog.md §7 技法選択マトリクス](../../../docs/test-techniques/test-techniques-skill-catalog.md#7-技法選択マトリクス) |

## skills 化を優先すべき技法トップ20（カタログ §4）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| 優先順位付き技法リスト | 同値分割・境界値分析・デシジョンテーブル・状態遷移テスト・リスクベーステスト等、上位20技法とその選定理由 | [test-techniques-skill-catalog.md §4](../../../docs/test-techniques/test-techniques-skill-catalog.md#4-skills-化を優先すべき技法トップ20) |
| 技法ID体系 | BB-xx（仕様ベース）／WB-xx（構造ベース）／COM-xx（組合せ）／EXP-xx（経験ベース）／RISK-xx／ORA-xx／PROP-xx／META-xx／MBT-xx／DIFF-xx／FUZZ-xx／REG-xx／NF-xx／API-xx／SAFE-xx／AI-xx／LLM-xx 等 | [test-techniques-skill-catalog.md §3 テスト技法一覧](../../../docs/test-techniques/test-techniques-skill-catalog.md#3-テスト技法一覧) |
| 個別技法の現況判定・出典URL | 技法ごとの維持・改名・新設等の判定根拠と参考URL一覧 | [test-technique-status-assessment.csv](../../../docs/test-techniques/test-technique-status-assessment.csv) |

## テストオラクル分類（testing-standards §5.1）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| オラクル4分類 | specified（明示仕様オラクル）／derived（導出オラクル）／implicit（暗黙オラクル）／human（人間オラクル） とそれぞれの保証の強さ | [testing-standards-and-assurance-concepts.md §5.1](../../../docs/test-techniques/testing-standards-and-assurance-concepts.md#51-オラクルの分類barr-et-al-2015) |
| オラクル別の保証範囲 | 各オラクル状態が「実際に保証していること」「保証していないこと」の対応表 | [同 §5.2](../../../docs/test-techniques/testing-standards-and-assurance-concepts.md#52-オラクルが無い--弱い場合に何が保証できるか) |

## 保証ステートメントテンプレート（testing-standards §9）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| テンプレート構造 | `target` / `claim` / `test_level` / `test_type` / `technique` / `risk_link` / `oracle` / `coverage` / `fault_detection_evidence` / `assumptions` / `limitations` / `flakiness_controls` / `decay_conditions` | [testing-standards-and-assurance-concepts.md §9](../../../docs/test-techniques/testing-standards-and-assurance-concepts.md#9-このテストは何を保証するか説明テンプレート)、[schemas/assurance-statement.schema.json](../../../schemas/assurance-statement.schema.json) |
| 記入例 | 送料計算モジュールを対象にした記入例（境界値分析＋デシジョンテーブル、specified oracle、ミューテーションスコア付き） | 同上 |

## TDD レビューゲート観点（§8.3）

| 観点 | チェック内容 | 出典 |
| --- | --- | --- |
| パラメーター | 入力、状態、環境、データ、操作が必要十分に識別されているか | [test-process-research-summary-test-design.md §8.3 TDDレビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#83-tdd-レビュー) |
| 値候補 | 正常、異常、境界、代表値が適切か | 同上 |
| 制約 | 実在しない組合せを除外しているか | 同上 |
| カバレッジ | 何をどこまで網羅するかが測定可能か | 同上 |
| 技法 | 目的に合ったテスト設計技法を使っているか | 同上 |
| 期待結果 | 判定可能な期待結果になっているか | 同上 |
| ケース数 | 多すぎず、少なすぎないか | 同上 |

## TI レビューゲート観点（§8.4）

| 観点 | チェック内容 | 出典 |
| --- | --- | --- |
| 実行順序 | 前提条件、データ、環境、重要度を考慮しているか | [test-process-research-summary-test-design.md §8.4 TIレビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#84-ti-レビュー) |
| 手順 | 実行者が迷わないか | 同上 |
| 自動化 | スクリプト、データ、期待結果、環境が紐づいているか | 同上 |
| 証跡 | ログ、スクリーンショット、API応答、DB状態などが残るか | 同上 |
| 再現性 | 失敗時に再現できる情報があるか | 同上 |

## アンチパターン（§9・本スキル関連分のみ抜粋）

| アンチパターン | 対策 | 出典 |
| --- | --- | --- |
| いきなりテストケースを生成する | TRA → TAD → TDD/TI の順で通す | [test-process-research-summary-test-design.md §9 アンチパターン](../../../docs/test-techniques/test-process-research-summary-test-design.md#9-アンチパターン) |
| テスト観点を全部同じ型で扱う | 内部データ型（DTC/TAE/COV/TC等）を分ける | 同上 |
| トレーサビリティを最後に作る | 最初から ID とリンクを付与する | 同上 |
