---
name: test-architecture-design
description: >
  テスト条件を整理して、どの粒度・順序・厚みでテストするか構造設計してほしい
  とき、または「テストレベル・タイプごとにどう役割分担すればいいか」という
  問いに答える必要があるときに使う。詳細テスト条件（DTC）とリスク優先度を
  材料に、テスト全体を意味のある要素（テストアーキテクチャ要素＝TAE）へ
  分解し、レベル・タイプ・サイクル・厚み・担当を割り当て、割当マトリクスと
  ともに出力する。
version: 0.2.0
inputs:
  detailed_test_condition_list_ref:
    type: path
    required: false
    description: >
      test-requirement-analysis の出力（DetailedTestConditionList、`DTC-nnn`）
      へのパス、または本文貼り付け。存在しない場合は対象機能の説明文から
      簡易アーキテクチャをインラインで合成する
  feature_summary:
    type: string
    required: true
    description: >
      対象機能の説明文（DTC が無い場合の唯一の必須入力。何を、どの範囲で
      テストしたいかが分かる1〜3文）
  risk_priority_hint:
    type: string
    required: false
    description: >
      risk-analysis の出力（RiskRegister）由来のリスク優先度、または
      分かっている範囲でのリスクの高低感。未指定でも起動可能
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  test_architecture_element:
    schema: ../../schemas/test-architecture-element.schema.json
  condition_assignment_matrix:
    schema: ../../schemas/condition-assignment-matrix.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/test-techniques/test-process-research-summary-test-design.md
  - docs/test-techniques/testing-standards-and-assurance-concepts.md
---

# test-architecture-design

Tester Skillspace 4象限: テスト技法（重）／ドメイン（中）／
ITスキル（重、構造設計）／コミュニケーション（軽）。

## 目的

`DetailedTestConditionList`（DTC）とリスク優先度を材料に、テスト全体を
「意味のある整理棚」へ構造化し、テストアーキテクチャ設計（TAD）として
`TestArchitectureElement`（TAE）＋`ConditionAssignmentMatrix` を出力する。
本スキルは [test-process-research-summary-test-design.md §4.5（テスト
アーキテクチャー設計）](../../docs/test-techniques/test-process-research-summary-test-design.md#45-4-テストアーキテクチャー設計tad)
の手順を実装し、前工程 [test-requirement-analysis（TRA）](../test-requirement-analysis/SKILL.md)
の出力を受けて起動するのが標準だが、単体起動も可能である。出力は
[test-design-implementation（TDD/TI）](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#4-test-design-implementation-tddti)
への入力になる（TDD/TI は本タスク時点で未実装）。

**アンチパターン警告（必読）**: DTC やアーキテクチャ設計を経ずに直接テスト
ケースを生成することを禁止する。TAD を省くと、agent はテスト条件から直接
テストケースを生成しがちになる（人間もよくやる）。段階を飛ばすと、根拠・
構造・厚みの正当性が失われた「整理されていないExcelの山」が量産される
（[test-process-research-summary-test-design.md §9 アンチパターン](../../docs/test-techniques/test-process-research-summary-test-design.md#9-アンチパターン)
「いきなりテストケースを生成する」参照）。

## 手順

1. **入力の確認**: `detailed_test_condition_list_ref` が与えられ実データが
   存在すれば読み込む。存在しなければ「上流成果物なし時の振る舞い」に従う。
   `risk_priority_hint` があれば厚み判定の材料として保持する。
2. **テスト全体の構造化（必須）**: DTC 群を
   [test-process-research-summary-test-design.md §4.5 タスク1](../../docs/test-techniques/test-process-research-summary-test-design.md#45-4-テストアーキテクチャー設計tad)
   の5つの切り口（機能単位／品質特性・テストタイプ単位／ソフトウェア設計
   責務単位／テストレベル単位／テストサイクル単位）のいずれかまたは組合せで
   グルーピングし、各グループを `TAE-nnn` として識別する。レベル・タイプの
   切り口を選ぶ際は
   [testing-standards-and-assurance-concepts.md §3（テストレベル×テストタイプ×
   技法の保証マトリクス）](../../docs/test-techniques/testing-standards-and-assurance-concepts.md#3-テストレベル--テストタイプ--技法の保証マトリクス)
   を用い、どのレベルが何を保証し何を保証しないかを踏まえて重複確認を避ける。
3. **要素間の関係の明示**: 依存・重複・委譲・上位/下位・影響範囲を
   [同 §4.5 タスク2](../../docs/test-techniques/test-process-research-summary-test-design.md#45-4-テストアーキテクチャー設計tad)
   に従って整理し、`delegated_to` フィールドに反映する（委譲がなければ
   `null`）。
4. **厚み（thickness）の決定（必須）**: リスクや責務分担に応じて
   `thick`（厚く見る）/`standard`（標準的に見る）/`narrow`（絞って見る）/
   `delegate`（別レベルへ委譲する）のいずれかを各 TAE に割り当てる
   （[同 §4.5 タスク3](../../docs/test-techniques/test-process-research-summary-test-design.md#45-4-テストアーキテクチャー設計tad)）。
   リスクレベルから厚みへの変換は
   [testing-standards-and-assurance-concepts.md §4.2（リスク→テスト深度の
   変換手順）](../../docs/test-techniques/testing-standards-and-assurance-concepts.md#42-リスク--テスト深度の変換手順)
   のリスクレベル別ポリシー表（高＝複数技法の重ね掛け、中＝単一の体系的
   技法、低＝スモーク/探索的で代替）を参照し、どのリスクレベルにどの行を
   適用したかを `rationale` に1文で記録する。
5. **担当グループの決定と調整**: 各 DTC をどの TAE が担当するかを
   [同 §4.5 タスク4〜5](../../docs/test-techniques/test-process-research-summary-test-design.md#45-4-テストアーキテクチャー設計tad)
   に従って決め、`assigned_conditions` に反映する。同じ条件を複数箇所で
   見すぎない・誰も見ない条件をなくす、を顧客影響・他機能影響・利用頻度・
   コード複雑度・変更量・下位レベルでの担保状況の観点で調整する。
6. **割当マトリクスの生成（必須）**: 全 DTC がどの TAE に割り当て済みかを
   `ConditionAssignmentMatrix` として一覧化する（詳細は「出力エンベロープ」
   節参照）。未割当の DTC がある場合はその ID を明示する。
7. **レビュー観点での自己点検**: 出力した TAE 群を
   [TADレビューゲートの観点](../../docs/test-techniques/test-process-research-summary-test-design.md#82-tad-レビュー)
   （構造・関係・厚み・担当・重複漏れ・粒度）に照らして自己点検する。
   詳細な参照ポインタは [references/tad-checklist.md](references/tad-checklist.md)
   を用いる。

**ゆもつよメソッド・Tiramis 8要素について**: 論理的機能構造分析（ゆもつよ
メソッド）と Tiramis 8要素はプロンプト由来・出典補強待ちの手法であり、
`docs/` に正典文書が未収録である（Phase 2 で
`docs/test-techniques/japanese-test-design-methods.md` として文書化予定）。
本スキルの手順5〜6ではこれらの手法を前提とせず、test-process 文書の
5切り口・厚みポリシーのみで構造化を完結させる。

## 最小入力契約

コールドスタート（他スキルの成果物が一切ない状態）で本スキルを起動するために
最低限必要な入力は次の1つのみである。

- **対象機能の説明文**（`feature_summary`）: 何を、どの範囲でテストしたいかが
  分かる1〜3文

`detailed_test_condition_list_ref`・`risk_priority_hint` はいずれも任意であり、
与えられなくても起動・出力可能である。

## 上流成果物なし時の振る舞い

test-requirement-analysis の成果物（`DetailedTestConditionList`）が存在しない
場合、次の手順で分析を継続する。

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) 対象機能のスコープ（どこからどこまでを本アーキテクチャで扱うか）、
   (b) 主要なテストレベル・テストタイプの想定（コンポーネント/結合/システム/
   受け入れのどこが中心か）、(c) 既知の高リスク領域があるか、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、`feature_summary` の
   記述から想定される DTC 相当の項目を仮に列挙し、それらを担当する簡易な
   TAE（1〜2グループ）を**インラインで合成し、必ず出力する**。分析不能を
   理由に無出力にはしない。
3. インラインで合成した TAE・割当マトリクスの前提は、エンベロープの
   `assumptions[]` に `{field, value, reason}` 形式で記録し、根拠が実際の
   DTC ではなく本スキル内での推定であることを `open_questions` にも反映
   する。TAE 自体には `assumption` フィールドを足さず、スキーマ準拠のまま
   保つ。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠、`TestArchitectureElementList` の各項目は
[schemas/test-architecture-element.schema.json](../../schemas/test-architecture-element.schema.json)
準拠）を必ず出力する。これにより、後から `test-design-implementation` や
`quality-orchestrator` に再取り込みできる。

`ConditionAssignmentMatrix` は
[schemas/condition-assignment-matrix.schema.json](../../schemas/condition-assignment-matrix.schema.json)
に準拠し、`schema_ref` に同スキーマを指定する。マトリクスは各 TAE の `assigned_conditions` と
内容が重複するが、**「全 DTC が漏れなくどこかの TAE に割当済みか（重複・
漏れ検査）」を横断的に一覧するための検査ビュー**という位置づけであり、
TAE 自体の `assigned_conditions` を置き換えるものではない。

```json
{
  "source_skill": "test-architecture-design",
  "phase": "TAD",
  "artifacts": [
    {
      "type": "TestArchitectureElementList",
      "schema_ref": "schemas/test-architecture-element.schema.json",
      "items": [
        {
          "id": "TAE-001",
          "name": "決済API - カード番号入力の妥当性確認",
          "element_type": "function_responsibility_group",
          "test_level": "component",
          "test_type": "functional",
          "test_cycle": "new_feature_test",
          "risk_level": "high",
          "thickness": "thick",
          "assigned_conditions": ["DTC-001"],
          "delegated_to": null,
          "rationale": "カード番号桁数不正はコンポーネントレベルで境界値を厚く確認すべき高リスク領域のため、testing-standards §4.2 の『高』行（複数技法の重ね掛け）を適用した"
        },
        {
          "id": "TAE-002",
          "name": "決済API - タイムアウト時の二重課金防止",
          "element_type": "function_responsibility_group",
          "test_level": "system",
          "test_type": "functional",
          "test_cycle": "new_feature_test",
          "risk_level": "high",
          "thickness": "thick",
          "assigned_conditions": ["DTC-002"],
          "delegated_to": null,
          "rationale": "冪等性キーの挙動はコンポーネント間の相互作用が絡むためシステムレベルで確認し、testing-standards §4.2 の『高』行を適用した"
        }
      ]
    },
    {
      "type": "ConditionAssignmentMatrix",
      "schema_ref": "schemas/condition-assignment-matrix.schema.json",
      "content": {
        "assignments": [
          { "architecture_element_id": "TAE-001", "assigned_conditions": ["DTC-001"] },
          { "architecture_element_id": "TAE-002", "assigned_conditions": ["DTC-002"] }
        ],
        "unassigned_conditions": []
      }
    }
  ],
  "trace_ids": ["RISK-001", "RISK-004", "DTC-001", "DTC-002", "TAE-001", "TAE-002"],
  "assumptions": [
    "risk_priority_hint が未指定のため、RISK-001・RISK-004 は test-requirement-analysis 側の暫定値をそのまま高リスクとして扱った"
  ],
  "open_questions": [
    "TAE-002（タイムアウト・二重課金防止）は結合レベルでも重複確認する予定があるか、それともシステムレベルに一本化してよいか"
  ],
  "gate_status": "passed-with-risks"
}
```

`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれかを
とる。未割当の DTC が残っている、または高リスク領域の厚みが `narrow`/
`delegate` のまま説明できない場合は `blocked` とし、TDD/TI への引き渡しを
保留する。
