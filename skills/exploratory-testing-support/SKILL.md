---
name: exploratory-testing-support
description: >
  「この機能を探索的にテストするならどのチャーターが向いているか」
  「探索セッションを設計してほしい」「セッションログをまとめてほしい」
  のように、探索的テストのチャーター選定・セッション設計・デブリーフ
  後処理が必要なときに使う。対象機能の説明と（あれば）リスク傾向・
  セッションログを材料に、チャーターカタログ（C01〜C50）からの推奨
  チャーターリスト（`CHT-Cnn`）、SBTM ベースのセッション設計、
  デブリーフ要約を出力する。対象機能の説明のみで起動でき、リスク情報が
  無い場合は汎用チャーター（P0）を優先する。探索の実行そのものは
  行わない（実行主体は AI エージェント＝veridia 等の実行系が担い、
  価値判断・重大度・リリース可否の最終判断は人間が担う）。
version: 0.1.0
inputs:
  target_summary:
    type: string
    required: true
    description: >
      探索対象の機能・領域と、探索の目的（新機能の初期評価か、リスク
      集中領域の深掘りか、セッションログの後処理か）が分かる1〜3文
      （唯一の必須入力）
  risk_info_ref:
    type: path
    required: false
    description: >
      リスク傾向・RiskRegister・上流ハンドオフエンベロープ（risk-analysis
      や test-requirement-analysis の出力）への参照。チャーター選定の
      優先度根拠に使う。無い場合は汎用チャーター（P0）を優先する
  session_log_ref:
    type: path
    required: false
    description: >
      実行済み探索セッションのログ・証跡（セッションノート・操作記録・
      スクリーンショット参照・TBS 記録等）への参照。デブリーフ後処理
      モードに必要。無い場合は選定・設計モードのみ実施する
  time_budget:
    type: string
    required: false
    description: >
      セッション数・時間枠・実行主体の制約（例: 「90分×2セッション、
      実行は veridia エージェント」）。無い場合は 40〜90 分の標準
      時間枠を仮置きし assumptions に記録する
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/exploratory-testing/exploratory-testing-concepts-and-practice.md
  - docs/exploratory-testing/exploratory-testing-charter-catalog-by-tour.md
  - docs/exploratory-testing/exploratory-testing-perspective-library.md
  - docs/exploratory-testing/exploratory-testing-tours-verification-final.md
---

# exploratory-testing-support

Tester Skillspace 4象限: テスト技法（重、ET 固有）／ドメイン（中、対象
機能の文脈理解）／ITスキル（軽）／コミュニケーション（デブリーフ支援、重）。

## 目的

対象機能とリスク傾向を材料に、
[チャーターカタログ](../../docs/exploratory-testing/exploratory-testing-charter-catalog-by-tour.md)
の50チャーター（C01〜C50）から推奨チャーターを選定し、
[SBTM](../../docs/exploratory-testing/exploratory-testing-concepts-and-practice.md#sbtmと運営実務)
に基づくセッション設計（チャーター・時間枠・記録項目）へ具体化する。
実行済みセッションのログが与えられた場合は、デブリーフ後処理（観察
事項・異常候補・次チャーター提案の要約）を行う。

**役割境界（必読）**: 本スキルはチャーター選定・セッション設計・
デブリーフ後処理のブループリントであり、**探索セッションの実行・操作・
証跡収集は行わない**。実行主体は AI エージェント（veridia 等の実行系）
であり、発見の価値判断・重大度判断・リリース可否の最終責任は人間が持つ
（[exploratory-testing-concepts-and-practice.md「実行主体としての AI
エージェント」](../../docs/exploratory-testing/exploratory-testing-concepts-and-practice.md#実行主体としての-ai-エージェント)、
[DECISIONS.md D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)）。
この役割境界は出力エンベロープの `role_boundary` に毎回明記する。

役割分担: リスクの体系的な洗い出しは risk-analysis、テスト条件の導出は
test-requirement-analysis、スクリプトテストのケース設計は
test-design-implementation、実行結果ログの体系的なトリアージ
（RUN-nnn・flaky 判定）は test-execution-support が担う。本スキルの固有の
責務は**探索的アプローチ固有の成果物（チャーター・セッション・
デブリーフ）を、下流が使える契約へ変換すること**である。

## 手順

1. **入力の分類とモード判定**: `target_summary` と `session_log_ref` の
   有無から、(a) 選定・設計モード（実行前）、(b) デブリーフモード
   （実行後）、のいずれか（または両方）を判定する。`risk_info_ref` の
   有無でチャーター優先度の根拠水準（リスク根拠あり／汎用 P0 優先）を
   確認する。
2. **探索アプローチの適合確認**:
   [exploratory-testing-concepts-and-practice.md の適用場面](../../docs/exploratory-testing/exploratory-testing-concepts-and-practice.md#適用しやすい場面)
   に照らし、対象が探索的テストに向くか（要件が曖昧・新機能初期評価・
   複雑連携・リスク集中領域等）を確認する。スクリプトテストや回帰
   スイートが適する対象（精密な反復・網羅保証が主目的）であれば、
   その旨と代替スキル（test-design-implementation 等）を出力に明記した
   うえで、補完としての探索チャーターを提案する。
3. **チャーター選定（CHT-Cnn）**:
   [チャーターカタログの一覧表](../../docs/exploratory-testing/exploratory-testing-charter-catalog-by-tour.md)
   から、対象タイプ・リスク傾向に合致するチャーターを選定する。
   - `risk_info_ref` がある場合: リスク項目（RISK-nnn）とチャーターを
     対応付け、優先度の根拠として引用する。
   - 無い場合: 汎用チャーター（P0）を優先し、`assumptions[]` に汎用
     選定である旨を記録する。
   - AI/LLM 機能が対象に含まれる場合は AI・LLM プロダクト向け
     チャーター（C45〜C50）を必ず検討する。
   - 選定数は時間予算に合わせる（標準: 1セッション1チャーター）。
     観点の細部は
     [観点ライブラリ](../../docs/exploratory-testing/exploratory-testing-perspective-library.md)
     を参照し、ツアーの出典信頼度に言及する場合は
     [ツアー検証](../../docs/exploratory-testing/exploratory-testing-tours-verification-final.md)
     の信頼度区分（A/B/C）を使う。
   - トレース ID は `CHT-` プレフィックス付き表記（例: `CHT-C07`）を
     使う（[ハブ §3 #8](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#3-スキル定義一覧)）。
4. **セッション設計（SBTM）**: 選定チャーターごとに、
   [SBTM の基本プロセス](../../docs/exploratory-testing/exploratory-testing-concepts-and-practice.md#sbtmと運営実務)
   と AI 支援セッション用チャーターテンプレートに従い、次を設計する。
   - チャーター本文（`EXPLORE / WITH / TO DISCOVER` 構文）
   - 時間枠（標準 40〜90 分。`time_budget` があればそれに従う）
   - 実行主体（AI エージェント／人間。既定は AI エージェント）と
     人間の監督者の役割（実行前承認・実行後デブリーフ）
   - 記録項目（セッションノート・TBS・異常候補・証跡参照）。実行系が
     何を証跡として残すべきかを指定するのは本スキルの責務だが、
     収集そのものは実行系が行う
   - チャーターに情報を入れ過ぎない（詰め込みは探索空間を狭める。
     [同文書のチャーター設計の注意](../../docs/exploratory-testing/exploratory-testing-concepts-and-practice.md#探索的テストの基礎)）
5. **デブリーフ後処理**（デブリーフモードの場合）: `session_log_ref` の
   ログを読み、次を要約する。
   - チャーター達成度（何を探索し、何を探索しなかったか）
   - 観察事項と異常候補（再現手順・証跡参照付き。**重大度の確定は
     しない**——候補の提示に留め、確定は人間のデブリーフに委ねる）
   - AI エージェント実行のログでは、エージェントの誤帰属（システム
     欠陥を自身の誤操作として処理した形跡）と異常の未報告（タスク
     完遂優先でスキップした形跡）を重点的に点検する
     （[同「実行主体としての AI エージェント」](../../docs/exploratory-testing/exploratory-testing-concepts-and-practice.md#実行主体としての-ai-エージェント)）
   - 次セッションのチャーター提案（深掘り・隣接領域）
   - 欠陥候補として下流（test-execution-support の
     `DefectCandidateList`・defect-analysis-rca）へ渡すべき項目
6. **エンベロープ出力**: 「出力エンベロープ」節の形式で出力する。
   `gate_status` は、対象機能の説明が読み取れない場合のみ `blocked`、
   リスク情報なしの汎用選定・ログ不完全でデブリーフが部分的な場合は
   `passed-with-risks`、リスク根拠付き選定とセッション設計（デブリーフ
   モードではログ全件の後処理）まで揃った場合は `passed` とする。

## 最小入力契約

コールドスタート（リスク情報・セッションログが一切ない状態）で本スキルを
起動するために最低限必要な入力は次の1つのみである。

- **探索対象の説明**（`target_summary`）: 対象機能・領域と探索の目的が
  分かる1〜3文

`risk_info_ref`・`session_log_ref`・`time_budget` はいずれも任意であり、
与えられなくても起動・出力可能である。リスク情報が無い場合は汎用
チャーター（P0）を優先し、セッションログが無い場合は選定・設計モード
のみを実施する（デブリーフ要約は出力しない）。

## 上流成果物なし時の振る舞い

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき
   質問は (a) 対象のプロダクトタイプ（Web/モバイル/API/AI 機能等。
   チャーターの対象タイプ絞り込みに直結）、(b) リスク傾向・直近の
   障害や不安のある領域はどこか、(c) 時間予算と実行主体の制約
   （セッション数・実行系の指定）、の3つに絞る。既に与えられた入力で
   無意味化した質問枠は、選定に最も効く別の質問へ再配分してよい
   （上限3件は維持する）。「最大3件」は利用者への対話的な確認質問の
   上限であり、`open_questions` に記録する未解決事項の件数には上限を
   設けない。
2. 回答が得られない場合でも、必ず出力する。対象タイプが不明な場合は
   汎用チャーター（P0）のみを提案し、対象タイプ別・AI/LLM 向け
   チャーターの追加検討を `open_questions` に残す。
3. 推定した前提（対象タイプ・時間枠・実行主体等）は `assumptions[]` に
   `{field,value,reason}` 形式で記録する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。

```json
{
  "source_skill": "exploratory-testing-support",
  "phase": "exploratory-testing-support",
  "artifacts": [
    {
      "type": "CharterRecommendationList",
      "schema_ref": "skills/exploratory-testing-support/SKILL.md",
      "content": {
        "role_boundary": "本スキルはチャーター選定・セッション設計・デブリーフ後処理のみを行う。探索セッションの実行・証跡収集は AI エージェント（veridia 等の実行系）が担い、価値判断・重大度・リリース可否の最終判断は人間が担う",
        "recommendations": [
          {
            "charter_id": "CHT-C25",
            "priority": "P0",
            "target_fit": "外部決済 API・通知基盤に依存する返品フロー",
            "rationale": "RISK-021（外部依存の劣化時に返品が滞留する）に直接対応する障害・依存サービス遮断チャーター",
            "risk_refs": ["RISK-021"]
          },
          {
            "charter_id": "CHT-C24",
            "priority": "P0",
            "target_fit": "返品申請の中断・キャンセル・二重送信",
            "rationale": "リスク情報が薄い領域のため、汎用（P0）の中断・キャンセルチャーターで状態遷移の未検証パスを先に広く踏む",
            "risk_refs": []
          }
        ]
      }
    },
    {
      "type": "SessionDesign",
      "schema_ref": "skills/exploratory-testing-support/SKILL.md",
      "content": {
        "sessions": [
          {
            "session_id": "ETS-001",
            "charter_id": "CHT-C25",
            "charter_text": {
              "explore": "返品フローの外部決済 API・通知基盤への依存境界",
              "with": "タイムアウト注入、リトライ再現データ、直近障害 INC-2041 の要約",
              "to_discover": "依存劣化時の滞留・二重処理・利用者への誤通知"
            },
            "timebox_minutes": 90,
            "executor": "ai-agent",
            "human_supervisor_role": "実行前のチャーター承認と実行後デブリーフ・重大度判定",
            "evidence_to_collect": [
              "セッションノート（期待と観察の対比を含む）",
              "操作ログと画面証跡",
              "異常候補ごとの再現手順",
              "TBS（Test/Bug/Setup 時間配分）"
            ]
          }
        ]
      }
    }
  ],
  "trace_ids": ["CHT-C25", "CHT-C24", "RISK-021"],
  "assumptions": [
    {
      "field": "timebox_minutes",
      "value": "90",
      "reason": "time_budget が入力に無いため、SBTM の標準時間枠（40〜90分）の上限を仮置きした"
    },
    {
      "field": "executor",
      "value": "ai-agent",
      "reason": "実行主体の指定が入力に無いため、正典の運用前提（探索実行主体 = AI エージェント）を既定として適用した"
    }
  ],
  "open_questions": [
    "返品フローに AI 機能（自動承認等）が含まれるか。含まれる場合は C45〜C50 の追加検討が必要"
  ],
  "gate_status": "passed-with-risks"
}
```

`CharterRecommendationList`・`SessionDesign`・`DebriefSummary` は ID
体系を持たない助言的成果物のため専用スキーマを設けず `content` に置く
（[schemas/README.md の content/items 使い分け](../../schemas/README.md)）。
デブリーフモードでは `DebriefSummary`（`schema_ref` は本 SKILL.md）を
artifacts に追加し、チャーター達成度・観察事項・異常候補（重大度候補
まで。確定はしない）・次チャーター提案・下流へ渡す欠陥候補を `content`
に記録する。`charter_id` は必ず `CHT-Cnn` 表記とし、
[チャーターカタログ](../../docs/exploratory-testing/exploratory-testing-charter-catalog-by-tour.md)
に実在する C01〜C50 のみを参照する（独自チャーターを追加する場合は
`charter_id` を付けず、カタログ外である旨を明記する）。`trace_ids` には
推奨した CHT- と、入力に含まれる既存 ID（RISK-・REQ- 等）を列挙する。
`role_boundary` は毎回のエンベロープに必須とする（phase2 ガイドの #8
受入観点）。`gate_status` は `passed` / `passed-with-risks` / `blocked`
の3値のいずれかをとる（判定規則は手順6）。

## 関連ドキュメント

- [exploratory-testing-concepts-and-practice.md](../../docs/exploratory-testing/exploratory-testing-concepts-and-practice.md) — ET 理論・SBTM・AI 実行境界の主参照
- [exploratory-testing-charter-catalog-by-tour.md](../../docs/exploratory-testing/exploratory-testing-charter-catalog-by-tour.md) — チャーター50件（C01〜C50）の正典
- [exploratory-testing-perspective-library.md](../../docs/exploratory-testing/exploratory-testing-perspective-library.md) — ツアー観点辞書
- [exploratory-testing-tours-verification-final.md](../../docs/exploratory-testing/exploratory-testing-tours-verification-final.md) — ツアー出典検証（信頼度 A/B/C）
