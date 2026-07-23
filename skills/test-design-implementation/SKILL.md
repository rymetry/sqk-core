---
name: test-design-implementation
description: >
  テスト条件から具体的なテストケースを作ってほしいとき、または「どのテスト
  技法を使ってカバレッジアイテムとテストケースを作ればいいか」という問いに
  答える必要があるときに使う。テストアーキテクチャ要素（TAE）を材料に、
  135技法カタログと状況→技法選択マトリクスから技法を選定し、カバレッジ
  アイテム（COV）とテストケース（TC）を生成し、各テストケースに保証
  ステートメントを必須付与して出力する。
version: 0.1.0
inputs:
  test_architecture_element_ref:
    type: path
    required: false
    description: >
      test-architecture-design の出力（TestArchitectureElementList、`TAE-nnn`）
      へのパス、または本文貼り付け。存在しない場合は対象機能の説明文から
      簡易な TAE 相当をインラインで合成する
  feature_summary:
    type: string
    required: true
    description: >
      対象機能の説明文（TAE が無い場合の唯一の必須入力。何を、どのリスク
      水準でテストケース化したいかが分かる1〜3文）
  technique_constraint_hint:
    type: string
    required: false
    description: >
      使用可能な技法の制約（例:「自動化前提のためモデルベーステストは除外」
      「探索的テストは別スキルに委譲済み」）。未指定でも起動可能
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  coverage_item:
    schema: ../../schemas/coverage-item.schema.json
  test_case:
    schema: ../../schemas/test-case.schema.json
  assurance_statement:
    schema: ../../schemas/assurance-statement.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/test-techniques/test-process-research-summary-test-design.md
  - docs/test-techniques/test-techniques-skill-catalog.md
  - docs/test-techniques/test-technique-status-assessment.csv
  - docs/test-techniques/testing-standards-and-assurance-concepts.md
---

# test-design-implementation

Tester Skillspace 4象限: テスト技法（最重）／ドメイン（中）／
ITスキル（軽）／コミュニケーション（保証ステートメントの説明責任、中）。

## 目的

`TestArchitectureElement`（TAE）を材料に、テスト詳細設計（TDD）とテスト
実装（TI）を実装する。[test-techniques-skill-catalog.md](../../docs/test-techniques/test-techniques-skill-catalog.md)
の135技法カタログと状況→技法選択マトリクスから目的に合う技法を選び、
`CoverageItemList`（COV）と `TestCaseList`（TC）を生成し、**生成した各
テストケースに保証ステートメント（`assurance_statement`）を必須付与**する。
本スキルは [test-process-research-summary-test-design.md §4.6（テスト詳細
設計 TDD）・§4.7（テスト実装 TI）](../../docs/test-techniques/test-process-research-summary-test-design.md#46-5-テスト詳細設計tdd)
の手順を実装し、前工程 [test-architecture-design（TAD）](../test-architecture-design/SKILL.md)
の出力を受けて起動するのが標準だが、単体起動も可能である。出力は
`test-execution-support`（TE、Phase 2 で実装予定）への入力になる。

**アンチパターン警告（必読）**: 分析やアーキテクチャ設計を経ずに直接テスト
ケースを生成することを禁止する。TAE を経由せずにテストケースを作ると、
根拠（どの詳細テスト条件・どのリスク水準に対応するか）と技法選定の妥当性
が失われた「整理されていないExcelの山」が量産される（[test-process-research-summary-test-design.md §9 アンチパターン](../../docs/test-techniques/test-process-research-summary-test-design.md#9-アンチパターン)
「いきなりテストケースを生成する」参照）。TAE が無い場合も、必ず「上流
成果物なし時の振る舞い」に従って簡易 TAE を合成してから先に進むこと。

## 手順

1. **入力の確認**: `test_architecture_element_ref` が与えられ実データが
   存在すれば読み込む。存在しなければ「上流成果物なし時の振る舞い」に従う。
   `technique_constraint_hint` があれば技法選定の制約として保持する。
2. **技法選定（必須・カタログの skill_id で引用する）**: 各 TAE の
   `test_level`・`test_type`・`risk_level` を材料に、
   [test-techniques-skill-catalog.md §7 技法選択マトリクス](../../docs/test-techniques/test-techniques-skill-catalog.md#7-技法選択マトリクス)
   （状況→第一候補／第二候補）と
   [同 §4 skills 化を優先すべき技法トップ20](../../docs/test-techniques/test-techniques-skill-catalog.md#4-skills-化を優先すべき技法トップ20)
   を参照して技法を選ぶ。**選定した技法は必ずカタログの技法 ID（例:
   `BB-01`〜`BB-11`、`WB-01`〜`WB-07`、`COM-01`〜`COM-04` 等、
   [同 §3 テスト技法一覧](../../docs/test-techniques/test-techniques-skill-catalog.md#3-テスト技法一覧)
   の ID 体系）で引用し、技法名のみの記述で済ませない**。カタログに実在
   しない技法名（ゆもつよメソッド等）は使わない。
3. **パラメーターと値候補の仮決め**: [test-process-research-summary-test-design.md §4.6 タスク1〜3](../../docs/test-techniques/test-process-research-summary-test-design.md#46-5-テスト詳細設計tdd)
   に従い、入力値・状態・事前条件・環境条件・データ状態・操作回数を洗い出し、
   リスクと厚み（TAE の `thickness`）に応じて値候補を追加・削除し、組合せ
   爆発を選定技法（同値分割・境界値分析・デシジョンテーブル・状態遷移・
   ペアワイズ／組合せテスト・エラー推測・チェックリスト）で抑える。
4. **カバレッジアイテムの生成（必須）**: [同 タスク4](../../docs/test-techniques/test-process-research-summary-test-design.md#46-5-テスト詳細設計tdd)
   に従い、各パラメーター組合せを `COV-nnn` として定義する（`condition_id`・
   `architecture_element_id`・`parameters`・`expected_result`・
   `coverage_rationale` を含む。詳細は
   [同 §6.4 CoverageItem のデータ契約](../../docs/test-techniques/test-process-research-summary-test-design.md#64-coverageitem)）。
5. **テストケースの生成（必須）**: [同 タスク5〜6](../../docs/test-techniques/test-process-research-summary-test-design.md#46-5-テスト詳細設計tdd)
   に従い、各 COV から `TC-nnn` を作成し、前提条件・手順・期待結果・優先度
   を判定可能な形で明示する（詳細は
   [同 §6.5 TestCase のデータ契約](../../docs/test-techniques/test-process-research-summary-test-design.md#65-testcase)）。
6. **保証ステートメントの付与（必須・全テストケースを漏れなくカバー）**: 生成した
   各テストケースに対し、
   [testing-standards-and-assurance-concepts.md §9「このテストは何を保証
   するか」説明テンプレート](../../docs/test-techniques/testing-standards-and-assurance-concepts.md#9-このテストは何を保証するか説明テンプレート)
   に従って `assurance_statement` を作成する。`technique` にはカタログの
   skill_id を記入し、`oracle.kind` は
   [testing-standards-and-assurance-concepts.md §5.1 オラクルの分類](../../docs/test-techniques/testing-standards-and-assurance-concepts.md#51-オラクルの分類barr-et-al-2015)
   （specified/derived/implicit/human）から選ぶ。1件の保証ステートメントで
   複数テストケースをまとめて説明する場合は、`target` フィールド内に対応
   する TC ID を明記し、どの TC 群に対する主張かを一意に追跡できるように
   する。
7. **テスト実装（TI）観点の記録**: 単体実行では実行環境構築・自動化スクリプト
   の実体化までは行わないが、[同 §4.7 タスク3（実行順序の決定基準）](../../docs/test-techniques/test-process-research-summary-test-design.md#47-6-テスト実装ti)
   の観点（前提条件を満たす順序・同じ準備データでまとめられる順序・環境
   切替が少ない順序・重要ケースを先に実行する順序・異常終了時の影響が
   小さい順序）を `open_questions` または `assumptions` に記録し、TE への
   引き継ぎ材料とする。
8. **レビュー観点での自己点検**: 出力した COV・TC・保証ステートメントを
   [TDDレビュー・TIレビューの観点](../../docs/test-techniques/test-process-research-summary-test-design.md#83-tdd-レビュー)
   （パラメーター・値候補・制約・カバレッジ・技法・期待結果・ケース数、
   および実行順序・手順・自動化・証跡・再現性）に照らして自己点検する。
   詳細な参照ポインタは
   [references/tdd-ti-checklist.md](references/tdd-ti-checklist.md) を用いる。

## 最小入力契約

コールドスタート（他スキルの成果物が一切ない状態）で本スキルを起動するために
最低限必要な入力は次の1つのみである。

- **対象機能の説明文**（`feature_summary`）: 何を、どのリスク水準でテスト
  ケース化したいかが分かる1〜3文

`test_architecture_element_ref`・`technique_constraint_hint` はいずれも任意
であり、与えられなくても起動・出力可能である。

## 上流成果物なし時の振る舞い

test-architecture-design の成果物（`TestArchitectureElement`）が存在しない
場合、次の手順で分析を継続する。

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) 対象機能の範囲（何を、どこまでテストケース化するか）、(b) リスク
   水準（高・中・低のどれに近いか）、(c) 使用可能な技法に制約があるか、
   の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、`feature_summary`
   の記述から想定される TAE 相当を**簡易にインラインで合成し（1グループ）**、
   それを経由してから COV・TC を生成する。**分析結果から直接テストケースを
   生成することはしない**（アンチパターン警告参照）。無出力にはしない。
3. `TAE-900` 番台をインライン合成用に予約し、現行成果物集合で未使用の最初の
   `TAE-9xx` を合成した TAE の `id` に選ぶ（例: `TAE-901`）。合成した旨は
   エンベロープの `assumptions[]` に `{field, value, reason}` 形式で記録する。
   合成した TAE・そこから導出した COV・TC 自体には `assumption` フィールドを
   足さず、それぞれのスキーマ準拠のまま保つ。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。`CoverageItemList` の各項目は
[schemas/coverage-item.schema.json](../../schemas/coverage-item.schema.json)、
`TestCaseList` の各項目は
[schemas/test-case.schema.json](../../schemas/test-case.schema.json)、
`AssuranceStatementList` の各項目は
[schemas/assurance-statement.schema.json](../../schemas/assurance-statement.schema.json)
に個別準拠する。これにより、後から `test-execution-support` や
`quality-orchestrator` に再取り込みできる。

例は [test-architecture-design](../test-architecture-design/SKILL.md) の
`TAE-001`（決済API・カード番号入力の妥当性確認、`DTC-001` を担当）を引き
継ぎ、`COV → TC → assurance_statement` のチェーンを1本通したものである。

```json
{
  "source_skill": "test-design-implementation",
  "phase": "TDD-TI",
  "artifacts": [
    {
      "type": "CoverageItemList",
      "schema_ref": "schemas/coverage-item.schema.json",
      "items": [
        {
          "id": "COV-001",
          "condition_id": "DTC-001",
          "architecture_element_id": "TAE-001",
          "parameters": {
            "card_number_length": 13,
            "expiration_status": "valid",
            "brand": "Diners",
            "submit_count": 1
          },
          "expected_result": "1桁短いカード番号として拒否される",
          "coverage_rationale": "Dinersは14桁が有効値のため、13桁を短すぎる境界として確認する（BB-02 境界値分析）"
        },
        {
          "id": "COV-002",
          "condition_id": "DTC-001",
          "architecture_element_id": "TAE-001",
          "parameters": {
            "card_number_length": 14,
            "expiration_status": "valid",
            "brand": "Diners",
            "submit_count": 1
          },
          "expected_result": "有効な桁数として受理される",
          "coverage_rationale": "Dinersの有効境界（14桁ちょうど）を確認する（BB-02 境界値分析）"
        }
      ]
    },
    {
      "type": "TestCaseList",
      "schema_ref": "schemas/test-case.schema.json",
      "items": [
        {
          "id": "TC-001",
          "coverage_item_refs": ["COV-001"],
          "preconditions": ["支払い画面を表示している", "カートに購入可能商品がある"],
          "test_data_refs": ["TD-001"],
          "steps": [
            "カード番号に13桁のDiners相当番号を入力する",
            "有効期限に有効な年月を入力する",
            "支払い確定ボタンを押下する"
          ],
          "expected_results": [
            "カード番号桁数エラーが表示される",
            "決済APIが呼び出されない",
            "注文状態が未確定のままである"
          ],
          "priority": "high"
        },
        {
          "id": "TC-002",
          "coverage_item_refs": ["COV-002"],
          "preconditions": ["支払い画面を表示している", "カートに購入可能商品がある"],
          "test_data_refs": ["TD-002"],
          "steps": [
            "カード番号に14桁のDiners相当番号を入力する",
            "有効期限に有効な年月を入力する",
            "支払い確定ボタンを押下する"
          ],
          "expected_results": [
            "カード番号桁数エラーが表示されない",
            "決済APIが呼び出される",
            "注文状態が確定処理に進む"
          ],
          "priority": "high"
        }
      ]
    },
    {
      "type": "AssuranceStatementList",
      "schema_ref": "schemas/assurance-statement.schema.json",
      "items": [
        {
          "assurance_statement": {
            "target": "決済API カード番号桁数バリデーション（TC-001, TC-002 対応）",
            "claim": "Dinersブランドのカード番号について、13桁〜14桁の境界の範囲で桁数チェックが仕様通りに動作する。",
            "test_level": "コンポーネント",
            "test_type": "機能",
            "technique": "BB-02",
            "risk_link": {
              "risk_item": "RISK-004",
              "risk_level": "高",
              "depth_policy": "高リスク行（複数技法の重ね掛け）"
            },
            "oracle": {
              "kind": "specified",
              "description": "カードブランド別桁数仕様（REQ-012）の期待値をアサーションとして実装",
              "strength": "完全",
              "known_blind_spots": "仕様自体の誤り、Diners以外のブランドの桁数仕様"
            },
            "coverage": {
              "model": "境界値分析（2点法、BB-02）",
              "achieved": "境界2/2（13桁・14桁）",
              "not_covered": "15桁以上の上限側境界は別カバレッジアイテムで対応予定のため対象外"
            },
            "fault_detection_evidence": "未測定",
            "assumptions": [
              "target フィールドに TC-001/TC-002 のトレース対象を明記して1件に集約した",
              "決済APIはスタブ化して桁数チェックのみを分離して検証する"
            ],
            "limitations": [
              "実APIとの結合時の挙動は保証しない（コンポーネント統合レベルに委譲）",
              "他ブランドの桁数仕様は保証しない"
            ],
            "flakiness_controls": "時刻・乱数非依存、共有状態なし",
            "decay_conditions": "カードブランド別桁数仕様（REQ-012）の改訂"
          }
        }
      ]
    }
  ],
  "trace_ids": ["DTC-001", "TAE-001", "COV-001", "COV-002", "TC-001", "TC-002", "RISK-004"],
  "assumptions": [
    "risk_link.risk_item は test-architecture-design 側の暫定値（RISK-004）をそのまま踏襲した"
  ],
  "open_questions": [
    "15桁以上の上限側境界を別カバレッジアイテムとして追加すべきか、本スキル範囲内で扱うべきか"
  ],
  "gate_status": "passed-with-risks"
}
```

`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれか
をとる。保証ステートメントが付与できないテストケースが残っている、または
選定技法がカタログに実在しない ID を使っている場合は `blocked` とし、
`test-execution-support` への引き渡しを保留する。
