---
name: test-requirement-analysis
description: >
  仕様・要求文書からテスト条件を洗い出したいとき、または「このAPI仕様書から
  テスト観点を出してほしい」「この要求から何を確認すべきか整理してほしい」
  という問いに答える必要があるときに使う。仕様書・要求文書・設計書を
  テストベースとして能動的に分析し、3色ボールペン分析（重要箇所・構成要素・
  疑問矛盾のタグ付け）を経て、ユーザー／プロダクト／テスト組織の3視点で
  ハイレベル・詳細テスト条件を導出し、質問リストとともに出力する。
version: 0.1.0
inputs:
  test_basis:
    type: string
    required: true
    description: >
      テストベースとなる仕様・要求・設計文書の本文またはその要約
      （API仕様、画面仕様、業務フロー等）
  risk_register_ref:
    type: path
    required: false
    description: >
      risk-analysis の出力（RiskRegister、`RISK-nnn`）へのパス。
      存在しない場合はリスク欄を `assumption: true` 付きで暫定値とする
  test_overview_hint:
    type: string
    required: false
    description: >
      どのテストレベル・タイプ・サイクルで確認する想定かのヒント
      （分かっている範囲でよい。未指定でも起動可能）
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  detailed_test_condition_list:
    schema: ../../schemas/detailed-test-condition.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/test-techniques/test-process-research-summary-test-design.md
  - docs/test-techniques/testing-standards-and-assurance-concepts.md
  - docs/quality-models/iso25010-product-quality-model.md
---

# test-requirement-analysis

Tester Skillspace 4象限: テスト技法（重）／ドメイン（重、仕様理解）／
ITスキル（軽）／コミュニケーション（質問リスト生成、重）。

## 目的

テストベース（仕様・要求・設計文書）を確認し、テスト要求分析（TRA）として
「何を確認すべきか」と「どこが危ないか」を明らかにする。本スキルは
[test-process-research-summary-test-design.md §4.3（テストベース確認・
静的レビュー）](../../docs/test-techniques/test-process-research-summary-test-design.md#43-2-テストベース確認静的レビュー)
と[同 §4.4（テスト要求分析）](../../docs/test-techniques/test-process-research-summary-test-design.md#44-3-テスト要求分析tra)
の2活動を統合し、ユーザー・プロダクト・テスト組織の3視点で
`HighLevelTestConditionList`（HTC）と `DetailedTestConditionList`（DTC）を
導出する。出力は [test-architecture-design（TAD）](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#3-test-architecture-design-tad)
への入力になる（TAD は本タスク時点で未実装）。

**アンチパターン警告（必読）**: 分析結果から直接テストケースを生成することを
禁止する。本スキルの出力は DTC までであり、次工程は TAD である。段階を
飛ばすと根拠・構造・厚みの正当性が失われた「整理されていないExcelの山」が
量産される（[test-process-research-summary-test-design.md §9 アンチパターン](../../docs/test-techniques/test-process-research-summary-test-design.md#9-アンチパターン)
「いきなりテストケースを生成する」参照）。

## 3色ボールペン分析モード（内蔵）

テストベースを能動的に分析・補完するため、本文中の記述に次の3色でタグを
付け、タグ付け結果をレポートとして出力する。

| タグ | 意味 | 抽出対象の例 |
| --- | --- | --- |
| 赤 | 仕様の重要箇所 | 業務上の制約、金額・数量の境界値、権限、禁止事項 |
| 青 | 構成要素 | 画面・API・データ項目・状態遷移などの構造を示す記述 |
| 緑 | 疑問・矛盾 | 未定義、他箇所と矛盾する記述、曖昧な表現、テスト不能な記述 |

緑タグを付けた箇所は、そのまま「質問リスト」の候補になる（後述の
「出力エンベロープ」で `open_questions` として必須出力する）。

**出典に関する注記（必読）**: 3色ボールペン分析はユーザー提供のプロンプト
由来の手法であり、`docs/` に正典文書が未収録である。[スキル・エコシステム
設計プラン §3 #1](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#1-test-requirement-analysis-tra)
に記載の通り、Phase 2 で `docs/test-techniques/japanese-test-design-methods.md`
として文書化予定であり、現時点は「出典補強待ち」として扱う。本スキルの
分析結果に3色ボールペン由来の判断が含まれる場合、その旨をエンベロープの
`assumptions` に明記する。

## 手順

1. **テストベースの一覧化**: `test_basis` を読み、対象文書の版数・更新日・
   対象範囲・信頼度（分かる範囲で）を記録する。複数文書がある場合は
   それぞれを列挙する。
2. **3色ボールペン分析の実施**: 本文を通読し、赤（重要箇所）・青（構成要素）・
   緑（疑問・矛盾）のタグを付ける。緑タグの箇所は曖昧・矛盾・未定・不足・
   観測不能・制御不能のいずれに該当するかを分類する
   （[test-process-research-summary-test-design.md §4.3 タスク3](../../docs/test-techniques/test-process-research-summary-test-design.md#43-2-テストベース確認静的レビュー)）。
   タグ付き分析結果は Markdown レポートとして出力する（必須）。
3. **3視点での理解整理**:
   - **ユーザー視点**: よく使われる操作、失敗すると困る利用シーン、初心者と
     常連の違い、時間帯・イベントによる使われ方の変化を整理する。
   - **プロダクト視点**: 機能構成、外部連携、データ保持・更新箇所、複雑で
     壊れやすい箇所を整理する（青タグの内容が主な材料になる）。
   - **テスト・組織視点**: どのテストレベル・タイプ・サイクルで確認するか、
     誰がどこまで責任を持つかを `test_overview_hint` があれば踏まえて整理する。
   （3視点の定義は [test-process-research-summary-test-design.md §4.4 タスク1〜3](../../docs/test-techniques/test-process-research-summary-test-design.md#44-3-テスト要求分析tra)）
4. **リスクの取り込み**: `risk_register_ref` が与えられ実データが存在すれば
   読み込み、赤タグの箇所と突き合わせて優先度の根拠にする。存在しなければ
   「上流成果物なし時の振る舞い」に従う。
5. **ハイレベルテスト条件（HTC）の識別**: フィーチャーや品質特性単位の
   確認側面を `HTC-nnn` として識別する。品質特性の切り口が必要な場合は
   [iso25010-product-quality-model.md「要求から品質特性へマッピングする
   方法」](../../docs/quality-models/iso25010-product-quality-model.md#要求から品質特性へマッピングする方法)
   の5ステップ・手がかり語対応表を用いる。
6. **詳細テスト条件（DTC）の識別と根拠付与（必須）**: 各 HTC を、具体的に
   確認したい振る舞いへ `DTC-nnn` として分解する。各 DTC には
   [DetailedTestCondition のデータ契約](../../docs/test-techniques/test-process-research-summary-test-design.md#62-detailedtestcondition)
   に従い、次のフィールドを必ず埋める。
   - `source_refs`: どの仕様記述（赤・青タグ箇所）に基づくか
   - `high_level_condition_id`: 経由した HTC の ID（DTC は必ず HTC 経由で
     導出し、HTC を飛ばして仕様から直接 DTC を作らない）
   - `risk_refs`: 関連するリスク ID（`risk_register_ref` 由来、または
     `assumption: true` の暫定値）
7. **テストパラメーターの識別**: 振る舞いを変化させる要素（入力値、状態、
   環境等）の候補を識別し、DTC の `unknowns` または後続 TAD への申し送りに
   含める。本スキルではパラメーターの値候補までは確定しない（TDD/TI の
   責務）。
8. **不明点・仮定・確認事項の分離（必須）**: 緑タグの箇所、リスク欄の仮定、
   3視点整理で埋まらなかった項目を「質問リスト」としてまとめる。
   出力の質問リスト（`open_questions`）には件数制限を設けず、緑タグ由来の
   疑問・矛盾をすべて記録する（利用者への対話的な確認質問のみ最大3件。
   「上流成果物なし時の振る舞い」参照）。まとめた質問リストは
   [TRAレビューゲートの観点](../../docs/test-techniques/test-process-research-summary-test-design.md#81-tra-レビュー)
   （使われ方・仕組み・全体像・リスク・テスト条件・パラメーター・不明点の
   分離）に照らして自己点検する。

## 最小入力契約

コールドスタート（他スキルの成果物が一切ない状態）で本スキルを起動するために
最低限必要な入力は次の1つのみである。

- **テストベース**（`test_basis`）: 仕様・要求・設計文書の本文またはその要約

`risk_register_ref`・`test_overview_hint` はいずれも任意であり、与えられなくても
起動・出力可能である。

## 上流成果物なし時の振る舞い

risk-analysis の成果物（`RiskRegister`）が存在しない場合、次の手順で分析を
継続する。

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) テストベースに緑タグ（疑問・矛盾）を付けた箇所のうち最も影響が大きい
   もの、(b) どのテストレベル・タイプで確認する想定か、(c) 既知の重大リスクや
   規制ドメインの該当有無、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、赤タグ（重要箇所）の
   内容から一般的なリスク推定を行い、DTC の `risk_refs` に仮の識別子を割り当てて
   **必ず出力する**。分析不能を理由に無出力にはしない。
3. 仮置きしたリスク欄には `assumption: true` を付与し、根拠が
   risk-analysis の実データではなく本スキル内での推定であることを
   `open_questions` にも反映する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠、`DetailedTestConditionList` の各項目は
[schemas/detailed-test-condition.schema.json](../../schemas/detailed-test-condition.schema.json)
準拠）を必ず出力する。これにより、後から `test-architecture-design` や
`quality-orchestrator` に再取り込みできる。

`HighLevelTestConditionList` は Phase 1 時点で専用の JSON Schema が
存在しないため、`schema_ref` には ID 体系の定義箇所（[基本 ID 体系](../../docs/test-techniques/test-process-research-summary-test-design.md#61-基本-id-体系)）
をポインタとして指定し、items は `{id, title}` の最小形とする。

3色ボールペン分析結果は人間可読な Markdown レポートとして本文で提示し、
エンベロープ上は `ThreeColorAnalysisReport` として存在を明記する（専用
スキーマは未定義のため、本スキル定義（ハブ§3 #1）へのポインタを
`schema_ref` とする）。

```json
{
  "source_skill": "test-requirement-analysis",
  "phase": "TRA",
  "artifacts": [
    {
      "type": "HighLevelTestConditionList",
      "schema_ref": "docs/test-techniques/test-process-research-summary-test-design.md#61-基本-id-体系",
      "items": [
        { "id": "HTC-001", "title": "決済API: カード番号入力の妥当性確認" },
        { "id": "HTC-002", "title": "決済API: タイムアウト時の二重課金防止" }
      ]
    },
    {
      "type": "DetailedTestConditionList",
      "schema_ref": "schemas/detailed-test-condition.schema.json",
      "items": [
        {
          "id": "DTC-001",
          "title": "1桁短いカード番号を拒否する",
          "source_refs": ["REQ-012"],
          "high_level_condition_id": "HTC-001",
          "risk_refs": ["RISK-004"],
          "precondition_hint": "支払い画面を表示している",
          "action_hint": "カード番号を入力して支払い確定する",
          "expected_behavior_hint": "カード番号桁数エラーを表示し、決済を実行しない",
          "postcondition_hint": "注文は未確定のまま",
          "unknowns": ["Diners以外の海外ブランドの桁数仕様が仕様書に未記載（緑タグ）"],
          "status": "draft"
        },
        {
          "id": "DTC-002",
          "title": "決済APIタイムアウト時にリトライしても二重課金しない",
          "source_refs": ["REQ-042"],
          "high_level_condition_id": "HTC-002",
          "risk_refs": ["RISK-001"],
          "precondition_hint": "決済APIへのリクエストが送信済みで応答待ちである",
          "action_hint": "タイムアウト後にクライアントが同一注文でリトライする",
          "expected_behavior_hint": "冪等性キーにより二重課金が発生しない",
          "postcondition_hint": "注文の決済状態が一意に確定する",
          "unknowns": [],
          "status": "draft"
        }
      ]
    },
    {
      "type": "ThreeColorAnalysisReport",
      "schema_ref": "docs/agent-ecosystem/skill-ecosystem-design-plan.md#1-test-requirement-analysis-tra",
      "content": {
        "red": ["カード番号は14桁（Diners）〜16桁の範囲で受け付ける", "決済APIのタイムアウトは30秒とする"],
        "blue": ["支払い画面", "決済API", "注文ステータス（未確定/確定）"],
        "green": ["Diners以外の海外ブランドの桁数仕様が明記されていない", "タイムアウト後のリトライ時の冪等性キー仕様が本文中に見当たらない"]
      }
    }
  ],
  "trace_ids": ["REQ-012", "REQ-042", "RISK-001", "RISK-004", "HTC-001", "HTC-002", "DTC-001", "DTC-002"],
  "assumptions": [
    "risk-analysis の RiskRegister が未実行のため、RISK-001（二重課金）・RISK-004（桁数不正の考慮漏れ）は赤タグ箇所からの推定リスクとして仮置きした（assumption: true）",
    "3色ボールペン分析はプロンプト由来・出典補強待ちの手法であり、docs/ に正典文書が未収録である（Phase 2 で japanese-test-design-methods.md として文書化予定）"
  ],
  "open_questions": [
    "Diners以外の海外ブランドのカード番号桁数仕様は確認済みか",
    "決済APIタイムアウト後のリトライにおける冪等性キーの実装状況を確認したい",
    "本機能はどのテストレベル（システム/結合）で主に確認する想定か"
  ],
  "gate_status": "passed-with-risks"
}
```

`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれかを
とる。緑タグの疑問・矛盾が高リスク領域に集中し、DTC の大半が仮定に依存する
場合は `blocked` とし、TAD への引き渡しを保留する。
