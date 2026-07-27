---
name: ai-system-quality-eval
description: >
  「この LLM 機能の評価方法を設計してほしい」「LLM-as-a-judge の評価
  バイアスをチェックしたい」のように、AI/LLM 機能の品質評価の設計が
  必要なときに使う。AI 機能の仕様と（あれば）既存評価データを材料に、
  確率的出力に対する統計的合格基準（pass@k / pass^k の選択）・
  LLM-as-a-judge のメタ評価（位置・冗長性・自己選好バイアスの校正）・
  メタモルフィックテスト・ゴールデンセット設計・多段 CI ゲートを含む
  評価設計（`TEST-nnn`、`method_type: llm_eval`）を出力する。評価の
  実行・データ収集は行わない（実行系が担う）。AI 機能の説明のみで
  起動でき、既存評価データが無い場合はゴールデンセット設計指針に留める。
version: 0.2.0
inputs:
  ai_feature_summary:
    type: string
    required: true
    description: >
      対象 AI/LLM 機能の入出力・用途・自動化度合い（人間レビュー併用か
      無人実行か）の1〜3文（既存評価データが無い場合の唯一の必須入力）
  eval_data_bundle_ref:
    type: path
    required: false
    description: >
      既存の評価データ・ゴールデンセット・過去の eval 結果・上流
      ハンドオフエンベロープ群（AC/RISK 等）への参照
  risk_context_hint:
    type: string
    required: false
    description: >
      失敗許容度・規制/監査文脈（EU AI Act 等の適用有無）・重視する
      品質特性のヒント
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  evaluation_design:
    schema: ../../schemas/evaluation-design.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-models/ai-system-quality-model.md
  - docs/governance-compliance/ai-governance-regulation-audit.md
  - docs/test-techniques/test-techniques-skill-catalog.md
---

# ai-system-quality-eval

Tester Skillspace 4象限: テスト技法（重、AI 評価固有）／ドメイン（中）／
ITスキル（中）／コミュニケーション（限界の説明、重）。

## 目的

確率的な出力を持つ AI/LLM 機能に対し、[ai-system-quality-model.md](../../docs/quality-models/ai-system-quality-model.md)
の評価設計体系に従って「1回の実行結果ではなく統計的な評価」を設計し、
[quality-knowledge-schema.md §1.3 TEST](../../docs/quality-models/quality-knowledge-schema.md#test-test--evaluation-methodテスト評価方法)
契約の評価方法ノード（`TEST-nnn`、`method_type: llm_eval`）として出力
する。本スキルの固有の責務は**評価の設計**（何をどう測り、どんな合格
基準と判定機構で品質を主張するか）であり、限界の説明（この評価で何が
言えて何が言えないか）を必ず添える。

**実行境界（必読）**: 本スキルは評価の実行・評価データの収集・CI への
実装を行わない。それらは実行系（veridia 等）が担い、本スキルは評価設計
のブループリントを出力する（[DECISIONS.md D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)
の実行境界）。

役割分担: AI 固有のセキュリティ品質（プロンプトインジェクション等）は
nfr-review のセキュリティレンズと [secure-development §9](../../docs/secure-development/secure-development-and-supply-chain.md#9-llmai-エージェント固有のセキュリティ品質)、
本番監視・還流の設計は sre-quality-ops、リリース可否判定は
quality-gate-release-judgment、決定的テストの設計チェーン（HTC〜TC）は
test-design-implementation が担い、本スキルは代行しない。

## 手順

1. **対象の分解と評価レイヤの特定**: `ai_feature_summary` の機能を
   [ai-system-quality-model §AIシステム品質のレイヤ分解](../../docs/quality-models/ai-system-quality-model.md#aiシステム品質のレイヤ分解)
   に照らし、どのレイヤ（モデル単体／RAG／ツール利用・エージェント行動
   等）の評価が必要かを特定する。エージェント行動品質は終了状態比較・
   軌跡評価・pass^k が対象になる（「1回成功した」を「できる」と報告
   しない）。
2. **統計的合格基準の設計**: [§確率的出力に対する評価設計](../../docs/quality-models/ai-system-quality-model.md#確率的出力に対する評価設計)
   に従い、サンプリングに基づく合格基準を設計する。**pass@k / pass^k の
   選択基準**: 人間がレビューして採用するワークフローなら pass@k
   （能力の上限測定）、無人で実行されるワークフローなら pass^k
   （一貫性・信頼性測定。p=0.9 でも k=8 で約43%に減衰する）。選択の
   根拠を評価設計に明記する。
3. **オラクル設計とメタモルフィックテスト**: 期待値が一意に定まらない
   出力には、ルーブリック評価・ペア比較・メタモルフィック関係（意味を
   変えない変換で出力の一貫性を測る。手順は
   [テスト技法スキルカタログ SKILL-META-01](../../docs/test-techniques/test-techniques-skill-catalog.md#skill-meta-01-メタモルフィックテストを設計する)
   に委譲）から判定方法を選び、TEST レコードの `oracle` に明記する。
4. **LLM-as-a-judge のメタ評価設計**: judge を使う場合は
   [§LLM-as-a-judge の使い方と限界](../../docs/quality-models/ai-system-quality-model.md#llm-as-a-judge-の使い方と限界)
   に従い、位置バイアス・冗長性バイアス・自己選好バイアスを人間判定との
   校正（メタ評価）で確認する手順を評価設計に含める。**校正なしの
   judge スコアを品質数値として採用しない**（[§アンチパターン集](../../docs/quality-models/ai-system-quality-model.md#アンチパターン集)）。
5. **ゴールデンセット設計**: [§golden set 管理](../../docs/quality-models/ai-system-quality-model.md#golden-set-管理)
   と [§データ品質の詳細](../../docs/quality-models/ai-system-quality-model.md#データ品質の詳細)
   （代表性・偏り・鮮度、leakage と分割設計の失敗パターン）に従い、
   評価データの設計指針を出す。**既存評価データが無い場合は、この設計
   指針の提示に留め、評価実測値や品質水準の予測は出さない**。
6. **多段 CI ゲートの設計**: [§eval 駆動開発と CI への組み込み](../../docs/quality-models/ai-system-quality-model.md#eval-駆動開発と-ci-への組み込み)
   に従い、スモーク／フル／深掘り（レッドチーミング・スライス別公平性・
   pass^k 一貫性）の多段構成で CI ゲートを設計する。モデル更新時の回帰
   評価・ドリフト監視・評価セット汚染検出
   （[§モデル更新・運用フェーズの品質](../../docs/quality-models/ai-system-quality-model.md#モデル更新運用フェーズの品質)）
   への接続と、本番監視への還流（sre-quality-ops の `MON-nnn` との接続）
   を明記する。評価コスト・呼び出し予算の制約が与えられた場合は、段階別の
   想定呼び出し数として `EvalCiPlan` に記録し、予算が合格基準（k の選択等）
   に与える制約を明記する。
7. **ガバナンス要求の反映（該当する場合）**: `risk_context_hint` に
   規制・監査文脈がある場合、[ai-governance-regulation-audit.md](../../docs/governance-compliance/ai-governance-regulation-audit.md)
   に従い、評価設計に監査証跡の残し方と
   [human oversight の設計](../../docs/governance-compliance/ai-governance-regulation-audit.md#6-human-oversight-の設計)
   の要求を反映する（詳細な規制対応の設計は同 doc へ委譲し、本スキルは
   評価設計への反映点のみを扱う）。
8. **エンベロープ出力**: 「出力エンベロープ」節の形式で出力する。
   `gate_status` は、AI 機能の内容が判別できない場合のみ `blocked`、
   評価データ無しの設計指針止まり・校正未実施の judge・仮の合格水準が
   残る場合は `passed-with-risks`、既存評価データに基づき設計が確定して
   いる場合は `passed` とする。

## 最小入力契約

コールドスタート（評価データ・上流成果物が一切ない状態）で本スキルを
起動するために最低限必要な入力は次の1つのみである。

- **AI 機能の説明**（`ai_feature_summary`）: 対象機能の入出力・用途・
  自動化度合いが分かる1〜3文

`eval_data_bundle_ref`・`risk_context_hint` はいずれも任意であり、
与えられなくても起動・出力可能である。

## 上流成果物なし時の振る舞い

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) AI 機能の入出力と自動化度合い（人間レビュー併用か無人実行か）、
   (b) 既存の評価データ・ゴールデンセットはあるか、
   (c) 規制・監査文脈（EU AI Act 等）の適用はあるか、の3つに絞る。
   この上限は利用者への対話的な確認質問の件数であり、出力の
   `open_questions` のエントリ数には上限を設けない
   （test-requirement-analysis と同旨。振る舞い3の unknown 明示により
   3件を超えてよい）。
2. 回答が得られない、または利用者が回答不能な場合でも、必ず出力する。
   既存評価データが無い場合は、ゴールデンセット設計指針と評価設計の
   骨子（合格基準の型・オラクル方式・CI 段構成）までを出力し、評価
   実測値の予測をせず `gate_status: passed-with-risks` を返す。
   AI 機能の内容が全く判別できない場合のみ、確認事項を列挙して
   `gate_status: blocked` を返す。
3. 上流の AC/RISK ノードが無い場合、TEST レコードの
   `acceptance_criterion_refs` は空配列とし、検証対象の受入基準が未定義
   である旨を `open_questions` に **unknown** として明示する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。

```json
{
  "source_skill": "ai-system-quality-eval",
  "phase": "ai-quality-eval",
  "artifacts": [
    {
      "type": "EvaluationDesignList",
      "schema_ref": "schemas/evaluation-design.schema.json",
      "items": [
        {
          "id": "TEST-001",
          "name": "問い合わせ要約機能のオフライン eval（ルーブリック+校正済み judge）",
          "method_type": "llm_eval",
          "acceptance_criterion_refs": [],
          "technique_refs": ["SKILL-META-01"],
          "oracle": "5項目ルーブリック（正確性・網羅性・簡潔性・トーン・禁止事項）を人間判定と校正済みの LLM-judge で判定。敬語化・言い換えのメタモルフィック変換ペアで一貫性を併測",
          "design_chain_refs": [],
          "evidence_refs": []
        },
        {
          "id": "TEST-002",
          "name": "無人実行ワークフローの一貫性測定（pass^k）",
          "method_type": "llm_eval",
          "acceptance_criterion_refs": [],
          "technique_refs": [],
          "oracle": "同一入力 k=8 試行の全成功率 pass^k。無人実行のため pass@k ではなく pass^k を主指標とする",
          "design_chain_refs": [],
          "evidence_refs": []
        }
      ]
    },
    {
      "type": "GoldenSetDesignGuide",
      "schema_ref": "skills/ai-system-quality-eval/SKILL.md",
      "content": {
        "principles": [
          "本番入力分布の代表性を層化サンプリングで確保し、鮮度の更新周期を定める",
          "学習・チューニングデータとの leakage を分割設計で防止する",
          "失敗事例・エッジケースを意図的に含める（成功例だけのセットにしない）"
        ],
        "initial_size_hint": "スモーク用 20〜50 件から開始し、本番還流で拡充する"
      }
    },
    {
      "type": "EvalCiPlan",
      "schema_ref": "skills/ai-system-quality-eval/SKILL.md",
      "content": {
        "stages": [
          { "stage": "スモーク", "trigger": "コミット毎", "scope": "ゴールデンセット代表 20 件" },
          { "stage": "フル", "trigger": "マージ前/日次", "scope": "全ゴールデンセット + ルーブリック judge" },
          { "stage": "深掘り", "trigger": "モデル更新時/四半期", "scope": "レッドチーミング・スライス別公平性・pass^k 一貫性" }
        ]
      }
    }
  ],
  "trace_ids": ["TEST-001", "TEST-002"],
  "assumptions": [
    {
      "field": "oracle",
      "value": "ルーブリック+校正済み LLM-judge",
      "reason": "既存評価データが無いため、judge の校正（人間判定とのメタ評価）は初回評価データ作成後に実施する前提の設計とした"
    }
  ],
  "open_questions": [
    "検証対象の受入基準（AC ノード）はどこで定義されるか",
    "評価実行の頻度・コスト上限（CI 段構成の閾値調整に必要）"
  ],
  "gate_status": "passed-with-risks"
}
```

`TEST-nnn` は `EvaluationDesignList` の items として
[evaluation-design schema](../../schemas/evaluation-design.schema.json)
に個別準拠させる（正規出典は
[quality-knowledge-schema.md §1.3 TEST](../../docs/quality-models/quality-knowledge-schema.md#test-test--evaluation-methodテスト評価方法)
の契約）。`GoldenSetDesignGuide`・`EvalCiPlan` は ID 体系を持たない
助言的成果物のため `content` に置く（[schemas/README.md の content/items
使い分け](../../schemas/README.md)）。LLM-as-a-judge のメタ評価（手順4）の
成果物も、必要に応じて `JudgeMetaEvalPlan` 等の任意の content 型成果物
として同様に出力してよい。`gate_status` は `passed` /
`passed-with-risks` / `blocked` の3値のいずれかをとる（判定規則は手順8）。
