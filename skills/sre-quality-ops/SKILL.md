---
name: sre-quality-ops
description: >
  「このサービスの SLO を設計してほしい」「エラーバジェットの運用ルールを
  決めたい」「DORA 指標が悪化しているので解釈してほしい」のように、
  本番運用の品質目標・監視の設計が必要なときに使う。サービス特性と
  （あれば）既存メトリクスを材料に、SLI/SLO 定義（`MON-nnn`）・エラー
  バジェットポリシー・バーンレート警報設計・DORA 5指標の解釈を出力する。
  監視基盤の構築や警報の実装そのものは行わない（実行系・運用基盤が担う）。
  サービス概要のみでも起動でき、既存メトリクスが無い場合は業界標準的な
  水準を仮提案して前提を明記する。
version: 0.1.0
inputs:
  service_context_summary:
    type: string
    required: true
    description: >
      対象サービスの種類・ユーザーが体感する主要動作・設計の目的
      （SLO 新規設計か、既存 SLO の見直しか、DORA 解釈か）の1〜3文
      （既存メトリクスが無い場合の唯一の必須入力）
  metrics_bundle_ref:
    type: path
    required: false
    description: >
      既存のメトリクス・ダッシュボード定義・SLO/警報設定・上流ハンドオフ
      エンベロープ群（QC/AC/RISK 等）への参照
  objectives_hint:
    type: string
    required: false
    description: >
      事業上の目標・制約（SLA 契約の有無、重視する指標、対象期間等）
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  sli_slo_definition:
    schema: ../../schemas/sli-slo-definition.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/operations-quality/production-quality-sre-observability.md
  - docs/quality-management/software-quality-management-practical-reference.md
  - docs/quality-models/quality-knowledge-schema.md
---

# sre-quality-ops

Tester Skillspace 4象限: テスト技法（軽）／ドメイン（中）／ITスキル
（重、可観測性基盤）／コミュニケーション（軽）。

## 目的

対象サービスの本番品質を継続検証するための SLI/SLO・エラーバジェット・
警報を、[production-quality-sre-observability.md](../../docs/operations-quality/production-quality-sre-observability.md)
の実務形（Google SRE 本/Workbook 準拠）に従って設計し、
[quality-knowledge-schema.md §1.3 MON](../../docs/quality-models/quality-knowledge-schema.md#mon-production-monitoring-signal本番監視シグナル)
の契約に準拠した本番監視シグナル（`MON-nnn`）として出力する。MON は
チェーン（REQ→…→REL→MON）の終端であると同時に、検知結果を REQ/RISK へ
還流するループの起点であり、`feedback_target_refs` の明示を重視する
（還流ループがないチェーンは「出荷して終わり」になる）。

**実行境界（必読）**: 本スキルは監視基盤の構築・メトリクス収集・警報の
実装を行わない。それらは実行系・運用基盤が担い、本スキルは定義・設計の
ブループリントを出力する（[DECISIONS.md D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)
の実行境界）。出力する `MON-nnn` は skill-handoff の知識成果物であり、
実行系の runtime evidence 契約ではない。

役割分担: 品質特性の網羅レビューは nfr-review、リスクの洗い出しは
risk-analysis、リリース可否判定は quality-gate-release-judgment が担い、
本スキルは代行しない。本スキルの固有の責務は**本番運用の品質目標
（SLI/SLO）とその運用機構（バジェット・警報・還流）の設計**である。

## 手順

1. **サービス特性の把握と SLI 候補の選定**:
   `service_context_summary`・`metrics_bundle_ref` からサービス種別を
   把握し、[§SLI/SLO/SLA とエラーバジェット](../../docs/operations-quality/production-quality-sre-observability.md#sli--slo--sla-とエラーバジェット)
   の「SLI の選び方」（システム種別×重視 SLI の表。ユーザー向け=可用性・
   レイテンシ・スループット、パイプライン=スループット・E2E レイテンシ、
   全システム=正確性）に従い SLI 候補を選ぶ。計測原則: 平均ではなく
   パーセンタイル（p50/p95/p99）、ユーザー体験に近い位置で測る。
2. **SLO 水準の設定**: 既存メトリクスがあれば実績を参照しつつ、同 §の
   目標値設定5原則（現状追認しない・シンプルに・「絶対」を避ける・数を
   最小限に・最初から完璧を目指さない）で水準を決める。**既存メトリクスが
   無い場合は業界標準的な水準を仮提案し、仮提案である旨と根拠を
   `assumptions[]` に `{field,value,reason}` 形式で記録する**（実測に
   基づかない水準を確定値として出さない）。SLA 契約がある場合は
   SLO を SLA より厳しく設定する（内側の防衛線）。
3. **MON レコードの生成**: 設計した SLI/SLO・警報・還流シグナルを
   [schemas/sli-slo-definition.schema.json](../../schemas/sli-slo-definition.schema.json)
   準拠の `MON-nnn` として記録する。上流成果物（QC/AC ノード）があれば
   `qc_refs`/`ac_refs` で紐付け、無ければ空配列のままレコードをスキーマ
   準拠に保ち、前提を `assumptions[]` に記録する。`feedback_target_refs`
   には検知結果を還流する REQ/RISK を指定し、還流先が特定できない場合は
   `open_questions` に記録する。
4. **エラーバジェットポリシーの明文化**: [§エラーバジェットとエラー
   バジェットポリシー](../../docs/operations-quality/production-quality-sre-observability.md#エラーバジェットとエラーバジェットポリシー)
   に従い、予算消費時の行動（変更凍結の条件・ポストモーテム必須条件・
   エスカレーション先）をポリシーとして明文化する。ポリシーの目的は
   懲罰ではなく「データが信頼性優先を示したとき、チームが信頼性だけに
   集中する許可を与える」ことである点を保つ。
5. **バーンレート警報の設計**: [§SLO ベースのアラート設計（バーンレート
   アラート）](../../docs/operations-quality/production-quality-sre-observability.md#slo-ベースのアラート設計バーンレートアラート)
   に従い、マルチウィンドウ・マルチバーンレート方式（長い窓で有意性、
   短い窓=長い窓の1/12目安で継続性を確認）で警報条件を設計する。単純な
   エラー率閾値アラートの乱発を避ける。
6. **DORA 5指標の解釈（依頼が該当する場合）**: [§DORA メトリクス](../../docs/operations-quality/production-quality-sre-observability.md#dora-メトリクスデリバリーパフォーマンスの結果指標)
   に従い、指標の現状と悪化要因の仮説を解釈する。DORA 指標は結果指標で
   あり、個人・チームの評価やターゲット化に使わない原則を出力に明記する。
7. **エンベロープ出力**: 「出力エンベロープ」節の形式で出力する。
   `gate_status` は、サービス特性が把握できず設計不能な場合のみ
   `blocked`、仮提案水準・未確定の還流先・未検証の警報条件が残る場合は
   `passed-with-risks`、実績に基づき水準・運用・還流が確定している場合は
   `passed` とする。

## 最小入力契約

コールドスタート（既存メトリクス・上流成果物が一切ない状態）で本スキルを
起動するために最低限必要な入力は次の1つのみである。

- **サービス概要**（`service_context_summary`）: 対象サービスの種類・
  主要動作・設計の目的が分かる1〜3文

`metrics_bundle_ref`・`objectives_hint` はいずれも任意であり、与えられ
なくても起動・出力可能である。

## 上流成果物なし時の振る舞い

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) サービスの種類とユーザーが体感する主要動作は何か、
   (b) 既存の監視・メトリクス・SLO はあるか、
   (c) SLO の用途は何か（社内目標か SLA 契約の裏付けか）、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、必ず出力する。
   既存メトリクスが無い場合は、サービス種別に応じた業界標準的な水準の
   仮提案として SLI/SLO・警報を設計し、全仮提案の前提を `assumptions[]`
   に記録して `gate_status: passed-with-risks` を返す。サービスの種類
   すら判別できない場合のみ、確認すべき事項を列挙して
   `gate_status: blocked` を返す。
3. 上流の QC/AC/REQ/RISK ノードが無い場合、`qc_refs`/`ac_refs`/
   `feedback_target_refs` は空配列とし、還流先の特定を `open_questions`
   に **unknown** として明示する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。

```json
{
  "source_skill": "sre-quality-ops",
  "phase": "sre-quality-ops",
  "artifacts": [
    {
      "type": "SliSloDefinitionList",
      "schema_ref": "schemas/sli-slo-definition.schema.json",
      "items": [
        {
          "id": "MON-001",
          "name": "検索 API 可用性 SLO",
          "signal_type": "slo_sli",
          "qc_refs": [],
          "ac_refs": [],
          "threshold": "30日間の成功リクエスト率 99.9% を下回る",
          "owner": "検索チーム（オンコール）",
          "feedback_target_refs": []
        },
        {
          "id": "MON-002",
          "name": "検索 API バーンレート警報",
          "signal_type": "alert",
          "qc_refs": [],
          "ac_refs": [],
          "threshold": "長い窓1時間・短い窓5分でバーンレート 14.4 超（page）",
          "owner": "検索チーム（オンコール）",
          "feedback_target_refs": []
        }
      ]
    },
    {
      "type": "ErrorBudgetPolicy",
      "schema_ref": "skills/sre-quality-ops/SKILL.md",
      "content": {
        "budget": "0.1%（30日、約43.2分の全面停止相当）",
        "actions": [
          "直近4週間でバジェット超過時は P0・セキュリティ修正を除く変更を停止し、SLO 内へ戻るまで信頼性改善に集中する",
          "単一インシデントが4週間分バジェットの20%超を消費した場合はポストモーテム必須・P0 アクション1件以上",
          "ポリシー適用の不一致は経営層へエスカレーションする"
        ]
      }
    }
  ],
  "trace_ids": ["MON-001", "MON-002"],
  "assumptions": [
    {
      "field": "threshold",
      "value": "99.9%/30日",
      "reason": "既存メトリクスが無いため、ユーザー向けサービスの業界標準的な水準を仮提案した。実測1〜2か月後に SLO 目標値設定5原則で見直すこと"
    }
  ],
  "open_questions": [
    "検知結果の還流先となる REQ/RISK ノード（リスク登録簿）は存在するか",
    "SLA 契約の有無（ある場合、SLO は SLA より厳しく再設定する）"
  ],
  "gate_status": "passed-with-risks"
}
```

`ErrorBudgetPolicy`・警報設計・DORA 解釈は ID 体系を持たない助言的
成果物のため専用スキーマを設けず `content` に置く（[schemas/README.md の
content/items 使い分け](../../schemas/README.md)）。`MON-nnn` は
`SliSloDefinitionList` の items として
[sli-slo-definition schema](../../schemas/sli-slo-definition.schema.json)
に個別準拠させる。`gate_status` は `passed` / `passed-with-risks` /
`blocked` の3値のいずれかをとる（判定規則は手順7）。
