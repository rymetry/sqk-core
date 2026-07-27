---
name: nfr-review
description: >
  「この API の非機能要件をレビューしてほしい」「性能とセキュリティの
  バランスを見てほしい」のように、非機能要求（NFR）のレビューや品質特性間
  のトレードオフ整理が必要なときに使う。対象仕様を ISO/IEC 25010:2023 の
  9品質特性にマッピングし、4レンズ（UI/UX+アクセシビリティ／性能／
  セキュリティ／アーキテクチャ）のチェックリストで根拠付き所見を出し、
  特性間トレードオフマトリクスを必ず出力する。レンズ未指定時は全4レンズを
  実施し、対象外レンズは「非該当」と理由付きで明記する。仕様テキストのみ
  でも起動できる。
version: 0.1.1
inputs:
  review_target_summary:
    type: string
    required: true
    description: >
      何を（対象機能・API・システム）何の目的で NFR レビューするかの
      1〜3文（対象仕様が入手できない場合の唯一の必須入力）
  spec_bundle_ref:
    type: path
    required: false
    description: >
      対象仕様・設計文書・上流ハンドオフエンベロープ群への参照
      （複数ファイルをまとめて渡してよい）
  lens_hint:
    type: string
    required: false
    description: >
      優先レンズの指定（例:「性能とセキュリティを重点的に」）。
      未指定なら全4レンズを実施する
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-models/iso25010-product-quality-model.md
  - docs/human-centered-quality/accessibility-ux-human-centered-quality.md
  - docs/secure-development/secure-development-and-supply-chain.md
  - docs/operations-quality/production-quality-sre-observability.md
---

# nfr-review

Tester Skillspace 4象限: テスト技法（軽）／ドメイン（重）／ITスキル
（レンズにより変動）／コミュニケーション（トレードオフ説明、重）。

## 目的

対象仕様を [iso25010-product-quality-model.md](../../docs/quality-models/iso25010-product-quality-model.md)
の9品質特性（2023年版）にマッピングし、4レンズのチェックリストで
非機能要求をレビューして、根拠付き所見と**特性間トレードオフマトリクス
（必須出力）**を返す。4レンズは手順が同一（対象→特性マッピング→
チェックリスト→根拠付き指摘→トレードオフ提示）のため1スキルに統合し、
レンズ固有の知識は [references/](references/) 配下のレンズファイルで
分離する（[ハブ §3 #11](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#11-nfr-review)
の設計根拠）。

役割分担: リスクの洗い出し・優先度付けは risk-analysis、所見のテスト
条件化は test-requirement-analysis、SLI/SLO の詳細設計は sre-quality-ops
（未実装）が担い、本スキルは代行しない。本スキルの固有の責務は
**9特性の網羅チェック（言及されていない特性の発見）と、特性間の衝突の
明文化**である。

## 手順

1. **対象の分解と特性マッピング**: `review_target_summary` と
   `spec_bundle_ref` の仕様を、[iso25010 §「要求から品質特性へマッピング
   する方法」](../../docs/quality-models/iso25010-product-quality-model.md#要求から品質特性へマッピングする方法)
   の5ステップ（分解 → 9特性総当たり → サブ特性で対象・条件・水準を
   具体化 → リスクで重み付け → 測定・証跡の割り当て）と手がかり語対応表
   に従ってマッピングする。総当たりの目的は**言及されていない特性の発見**
   （暗黙要求の抽出）であり、仕様に書いてある特性だけを見ない。水準が
   書けない品質要求は測定不能として `open_questions` に記録する。
2. **レンズの決定**: `lens_hint` があれば優先レンズを解釈し、無ければ
   全4レンズ（UI/UX+アクセシビリティ／性能／セキュリティ／
   アーキテクチャ）を実施する。**対象外と判断したレンズも省略せず、
   「非該当」と判断理由を所見に明記する**（例: バッチ処理のみで UI が
   存在しない → UI/UX レンズは非該当）。
3. **レンズ別チェックリストレビュー**: 各レンズの参照ファイル
   （[references/lens-ui-ux-accessibility.md](references/lens-ui-ux-accessibility.md)・
   [references/lens-performance.md](references/lens-performance.md)・
   [references/lens-security.md](references/lens-security.md)・
   [references/lens-architecture.md](references/lens-architecture.md)）
   のチェック観点に従い、所見を「観点／指摘（何が不足・不明か）／根拠
   （正典の該当節）／推奨」の形で記録する。この4項目は出力エンベロープの
   findings フィールド（観点=`characteristic`／指摘=`statement`／根拠=
   `evidence_ref`／推奨=`recommendation`）にそれぞれ対応する。証跡なき
   主張をせず、仕様のどこを見てそう判断したかを付す。
4. **トレードオフマトリクスの作成（必須）**: [iso25010 §「品質特性間の
   トレードオフと調停」](../../docs/quality-models/iso25010-product-quality-model.md#品質特性間のトレードオフと調停)
   の典型トレードオフ表と調停手順に従い、対象で実際に衝突する（または
   衝突しうる）特性ペアをマトリクスとして必ず出力する。各ペアに「典型
   状況／対象での該当箇所／調停の推奨（優先順位と根拠）」を付す。
   顕在する衝突が無い場合も「検討した結果、顕在トレードオフなし」を
   検討済みペアとともに明示する（未検討と区別する）。全特性を「高」で
   要求している仕様は、優先順位の放棄というアンチパターンとして指摘する
   （同 §調停手順4）。
5. **受入基準・品質ゲートへの接続**: 優先度の高い所見について、
   [iso25010 §「受入基準・品質ゲートへの落とし込みパターン」](../../docs/quality-models/iso25010-product-quality-model.md#受入基準品質ゲートへの落とし込みパターン)
   の基本形（対象・条件・測定可能な水準・検証方法・証跡）で受入基準の
   改善案を提案する。ゲート配置の推奨は同 §のゲート配置パターンに従い、
   優先度上位のサブ特性に絞る（全特性を全ゲートに載せない）。
6. **エンベロープ出力**: 「出力エンベロープ」節の形式で出力する。
   `gate_status` は、対象仕様が一切読めなかった場合のみ `blocked`、
   水準未定義の品質要求・未解決のトレードオフ・重大な特性の欠落が残る
   場合は `passed-with-risks`、全レンズ確認済みで重大所見が無い場合は
   `passed` とする。

## 最小入力契約

コールドスタート（対象仕様・上流成果物が一切ない状態）で本スキルを
起動するために最低限必要な入力は次の1つのみである。

- **レビュー対象の説明**（`review_target_summary`）: 何を何の目的で
  NFR レビューするかが分かる1〜3文

`spec_bundle_ref`・`lens_hint` はいずれも任意であり、与えられなくても
起動・出力可能である。

## 上流成果物なし時の振る舞い

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) 対象仕様・設計文書はどこにあるか、(b) 重点的に見たいレンズは
   どれか、(c) レビュー結果を何に使うか（設計改善か受入基準化か）、
   の3つに絞る。なお「最大3件」は利用者への対話的な確認質問の上限で
   あり、手順1で測定不能要求を `open_questions` に記録する件数には
   上限を設けない（test-requirement-analysis の質問リスト運用と同旨）。
2. 回答が得られない、または利用者が回答不能な場合でも、必ず出力する。
   仕様が1件も無い場合は、`review_target_summary` から推定できる範囲の
   特性マッピングと確認すべき観点の一覧のみを出し、レンズ別所見と
   トレードオフの断定はせず `gate_status: blocked` を返す（仕様なしでの
   レビュー合格判定は出さない）。
3. 仕様の要約だけがある場合は、要約ベースでレビューを実施した上で、
   原典未確認である旨を `assumptions[]` に `{field,value,reason}` 形式で
   記録する。判定できなかったレンズ・観点は `open_questions` に
   **unknown** として明示する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。

```json
{
  "source_skill": "nfr-review",
  "phase": "nfr-review",
  "artifacts": [
    {
      "type": "NfrReviewFindings",
      "schema_ref": "skills/nfr-review/SKILL.md",
      "content": {
        "lens_results": [
          {
            "lens": "performance",
            "applicable": true,
            "findings": [
              {
                "characteristic": "性能効率性/時間効率性",
                "statement": "検索 API の応答時間目標が「十分高速」とのみ記載され、負荷条件と水準が未定義（仕様 §3.2）",
                "evidence_ref": "iso25010 §受入基準の基本形",
                "recommendation": "想定ピーク負荷と p95 水準を定義する（例: 100 req/s で p95 800ms 以下、負荷テストレポートを証跡）"
              }
            ]
          },
          {
            "lens": "ui-ux-accessibility",
            "applicable": false,
            "findings": [],
            "not_applicable_reason": "対象はバッチ連携 API であり、エンドユーザー向け UI を持たない"
          }
        ]
      }
    },
    {
      "type": "TradeoffMatrix",
      "schema_ref": "skills/nfr-review/SKILL.md",
      "content": {
        "conflicts": [
          {
            "pair": ["セキュリティ", "性能効率性"],
            "situation": "全リクエストの暗号化・監査ログ同期書き込みが応答時間目標と衝突しうる（仕様 §3.2 と §5.1）",
            "recommendation": "保護対象データの分類で処理を差別化し、監査ログは非同期化を検討。優先順位はセキュリティ > 性能（個人情報を扱うため）を提案"
          }
        ],
        "examined_without_conflict": [["柔軟性", "性能効率性"]]
      }
    }
  ],
  "trace_ids": [],
  "assumptions": [
    {
      "field": "spec_source",
      "value": "仕様書 v1.2 の §3・§5 のみ",
      "reason": "運用手順書は未入手のため、運用時の特性（信頼性の回復性）は仕様記載範囲でのみ判定した"
    }
  ],
  "open_questions": [
    "検索 API の想定ピーク負荷（req/s・データ件数）の正式値はどこで合意されるか"
  ],
  "gate_status": "passed-with-risks"
}
```

`NfrReviewFindings`・`TradeoffMatrix` は ID 体系を持たない助言的成果物の
ため専用スキーマを設けず `content` に置く（[schemas/README.md の
content/items 使い分け](../../schemas/README.md)）。`TradeoffMatrix` は
レンズ指定の有無にかかわらず**必須**で出力する。`lens` フィールドの
正準値は `ui-ux-accessibility` / `performance` / `security` /
`architecture` の4値であり、表記ゆれ（例: `ui_ux`）をさせない。
findings への `severity` 付与は任意だが、付与する場合は
quality-artifact-review と同じ4値（`blocker` / `major` / `minor` /
`info`）を用いる（ゲート判定の severity→gate_status 導出との整合の
ため）。`gate_status` は
`passed` / `passed-with-risks` / `blocked` の3値のいずれかをとる
（判定規則は手順6）。

## 関連ドキュメント

- [references/lens-ui-ux-accessibility.md](references/lens-ui-ux-accessibility.md) — UI/UX+アクセシビリティレンズ
- [references/lens-performance.md](references/lens-performance.md) — 性能レンズ
- [references/lens-security.md](references/lens-security.md) — セキュリティレンズ
- [references/lens-architecture.md](references/lens-architecture.md) — アーキテクチャレンズ
