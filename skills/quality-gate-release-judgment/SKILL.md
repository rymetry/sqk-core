---
name: quality-gate-release-judgment
description: >
  リリース判定・CI/CD品質ゲートでの Go/No-Go 判断が必要なとき、
  または「このリリースは出してよいか」「品質ゲートを通すべきか」
  という問いに答える必要があるときに使う。証跡ファイル（テスト結果、
  カバレッジレポート、リスク登録簿、脆弱性台帳等）を根拠として判定し、
  判定不能な項目は assumption として明示する。
version: 0.1.0
inputs:
  release_summary:
    type: string
    required: true
    description: 対象リリースの変更概要（何を、なぜ、影響範囲）
  evidence_files:
    type: array<path>
    required: false
    description: >
      入手可能な証跡ファイルのパス一覧（テスト結果、カバレッジレポート、
      リスク登録簿、脆弱性台帳、SLI/SLO文書等）。空でも起動可能。
  gap_checklist_scope:
    type: array<string>
    required: false
    description: >
      優先確認したいアーティファクト種別（例: "セキュリティ要求表",
      "性能試験計画・結果"）。未指定なら全カテゴリを確認する。
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  release_decision:
    schema: ../../schemas/release-decision.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-management/software-quality-gap-analysis-report.md
  - docs/quality-management/quality-metrics-pitfalls.md
  - docs/quality-models/iso25010-product-quality-model.md
---

# quality-gate-release-judgment

## 目的

リリース対象の変更に対して、収集可能な証跡に基づき Go / No-Go / 条件付き Go
を判定し、判定根拠・残存リスク・判定不能項目を後から監査できる形で出力する。
「証跡なき品質は品質なし」という原則（[ソフトウェア品質ギャップ分析報告書](../../docs/quality-management/software-quality-gap-analysis-report.md)）
に基づき、証跡が存在しない主張を判定の根拠にしない。

## 手順

1. **証跡収集**: `evidence_files` を読み込み、各ファイルがどのアーティファクト
   種別（品質属性一覧、リスク登録簿、カバレッジレポート、脅威分析、SLI/SLO文書等）
   に該当するかを分類する。ファイルが与えられない場合は「上流成果物なし時の
   振る舞い」節の手順に従う。
2. **ギャップチェックリスト照合**: [ギャップ分析報告書の証跡チェックリスト](../../docs/quality-management/software-quality-gap-analysis-report.md#収集すべきアーティファクトチェックリスト)
   の優先度 A 項目を基準に、収集できた証跡と欠落している証跡を仕分ける。
   欠落項目は `open_questions` または `assumptions` に振り分ける（§後述）。
3. **カウンターメトリクス確認**: 提示された指標（カバレッジ率、テスト件数、
   バグクローズ件数等）が単独で使われていないかを確認する。[品質メトリクスの
   誤用と落とし穴の原則3](../../docs/quality-management/quality-metrics-pitfalls.md#原則-3-カウンターメトリクス対になる指標)
   に基づき、主指標に対応するカウンターメトリクス（ミューテーションスコア、
   変更失敗率、再オープン率等）が併記されているかを確認し、なければ
   「この指標は単独では判定に使えない」旨を判定コメントに含める。
4. **Go/No-Go 判定と残存リスク明示**: 収集した証跡・カウンターメトリクス確認
   結果をもとに `gate_status` を決定する。判定理由は証跡の ID・ファイル名を
   引用して記述し、証跡がない主張をしない。残存リスクは
   [ISO/IEC 25010 のトレードオフ](../../docs/quality-models/iso25010-product-quality-model.md)
   の観点も踏まえ、対処せずに出荷した場合に何が起こり得るかを1文で書く。

## 最小入力契約

コールドスタート（他スキルの成果物が一切ない状態）で本スキルを起動するために
最低限必要な入力は次の2つのみである。

- **対象リリースの変更概要**（`release_summary`）: 何を変更し、なぜ変更し、
  影響範囲がどこかを1〜3文で記述したもの
- **入手可能な証跡ファイル群**（`evidence_files`）: 0件でも起動可能。0件の
  場合は「上流成果物なし時の振る舞い」に従う

この2つ以外（トレーサビリティチェーンの ID、DTC、テストアーキテクチャ等）は
一切前提にしない。

## 上流成果物なし時の振る舞い

トレーサビリティチェーンのリンクや DTC（詳細テスト条件）などの上流成果物が
存在しない場合、次の手順で判定を継続する。

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) 変更の影響範囲、(b) 既知の重大リスクの有無、(c) 直近の類似リリースで
   問題が起きたかどうか、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合は、**入手可能な証跡のみで
   判定する**。証跡がゼロの場合でも `gate_status: blocked` を返し、
   「証跡なしでの Go 判定はできない」ことを理由に明記する。
3. 判定できなかった項目（例: セキュリティ要求表が存在せず脆弱性の有無を
   判定できない）は `assumptions` または `open_questions` に **unknown** と
   して明示し、`gate_status` の理由文にも反映する。あいまいな沈黙で
   判定を通さない。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。これにより、後から `quality-orchestrator` や
`quality-artifact-review` に再取り込みできる。

```json
{
  "source_skill": "quality-gate-release-judgment",
  "phase": "release-judgment",
  "artifacts": [
    {
      "type": "release_decision",
      "schema_ref": "schemas/release-decision.schema.json",
      "content": {
        "gate_status": "passed-with-risks",
        "summary": "決済APIのタイムアウト値変更。負荷試験結果とロールバック手順は確認済み。",
        "evidence_used": [
          "loadtest-2026-07-01.md",
          "risk-register.csv"
        ],
        "residual_risks": [
          "セキュリティ要求表が未提出のため、認可まわりの回帰は未確認"
        ]
      }
    }
  ],
  "trace_ids": [],
  "assumptions": [
    "セキュリティ要求表が存在しないため、認可関連の非機能要求は変更前と同等と仮定した"
  ],
  "open_questions": [
    "直近3リリースで同種のタイムアウト変更に起因する障害はあったか"
  ],
  "gate_status": "passed-with-risks"
}
```

`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれかを
とる。証跡が著しく不足する場合は `blocked` とし、Go 判定を出さない。
