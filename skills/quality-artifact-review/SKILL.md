---
name: quality-artifact-review
description: >
  「TRA から TDD までの成果物一式が整合しているかレビューしてほしい」の
  ように、他スキルの成果物一式に対するメタレビューが必要なときに使う。
  各段階の成果物（RISK/HTC/DTC/TAE/COV/TC/保証ステートメント等）と
  ハンドオフエンベロープ群を材料に、文書点・工程一貫性・トレーサビリティ・
  説明責任・技術的妥当性の5観点で `ArtifactReviewFindingList` を生成し、
  所見の severity から3値 gate_status を機械的に導出する。前工程成果物が
  欠けている場合はその欠落自体を最重要所見として報告する。
version: 0.1.0
inputs:
  review_target_summary:
    type: string
    required: true
    description: >
      何の成果物一式を何の目的でレビューするかの1〜3文
      （成果物が1つも無い場合の唯一の必須入力）
  artifact_bundle_ref:
    type: path
    required: false
    description: >
      レビュー対象のハンドオフエンベロープ群・成果物ファイル
      （Markdown/JSON/CSV）へのパス。複数ファイルをまとめて渡してよい
  review_scope_hint:
    type: string
    required: false
    description: >
      優先確認したい観点（例:「工程一貫性を重点的に見てほしい」）。
      未指定なら5観点すべてを対象にする
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  artifact_review_finding:
    schema: ../../schemas/artifact-review-finding.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-management/software-quality-gap-analysis-report.md
  - docs/test-techniques/test-process-research-summary-test-design.md
  - docs/test-techniques/testing-standards-and-assurance-concepts.md
---

# quality-artifact-review

Tester Skillspace 4象限: テスト技法（中）／ドメイン（軽）／ITスキル（軽）／
コミュニケーション（レビュー所見、重）。

## 目的

他スキルの成果物一式（成果物本体＋ハンドオフエンベロープ）を、
[test-process-research-summary-test-design.md §8.5（成果物品質レビュー）](../../docs/test-techniques/test-process-research-summary-test-design.md#85-成果物品質レビュー)
の5観点（文書点・工程一貫性・トレーサビリティ・説明責任・技術的妥当性）で
メタレビューし、所見を `ArtifactReviewFinding` として出力する。
各成果物を生成したスキル自身の自己判定とは独立に、**成果物横断の整合**
（前工程の約束が後工程で実施されたか、エンベロープ間で状態が矛盾して
いないか）を検証することが本スキルの固有の責務である。個々のリンク検査は
traceability-management、リリース可否は quality-gate-release-judgment が
担い、本スキルは代行しない（役割分担は手順2を参照）。

## 手順

1. **成果物収集と分類**: `artifact_bundle_ref` を読み込み、各ファイルを
   工程（routing / risk-analysis / TRA / TAD / TDD-TI / traceability /
   release-judgment）と成果物種別（RiskRegister、DetailedTestConditionList
   等）に分類する。レビュー対象の工程範囲から期待されるのに存在しない
   前工程成果物を列挙し、**欠落1件につき severity=blocker の所見を1件**
   記録する（[ハブ §3 #14](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#14-quality-artifact-review)
   の明文規定: 欠落自体を最重要所見として報告する）。
2. **5観点レビュー**: [references/review-viewpoints.md](references/review-viewpoints.md)
   のチェックリストに従い、観点ごとに所見を `ArtifactReviewFinding`
   （[schemas/artifact-review-finding.schema.json](../../schemas/artifact-review-finding.schema.json)
   準拠）として記録する。特に工程一貫性・説明責任では、**エンベロープ横断の
   突合**（前工程の `assumptions` が約束した下流作業の実施有無、解決済み
   事項が元エンベロープの `open_questions` に未解決のまま残っていないか、
   裁定・決定の記録が散在していないか）を必ず行う。トレーサビリティ観点は、
   バンドル内に traceability-management の `TraceabilityMatrix` があれば
   その結果（切断・未到達・advisory）を引用して評価し、リンク検査自体を
   再実行しない。無ければ「トレーサビリティ検査が未実施」という所見を
   記録する（検査の代行はしない）。
3. **severity 付与**: 各所見に次の判定原則で severity を与える。
   - **blocker**: 前工程成果物の欠落、または進行不能の矛盾
     （どちらの成果物が正か判定できず後工程が進められない状態）
   - **major**: 未解決のまま下流成果物の期待値・妥当性を毀損している事項
     （例: 仕様矛盾が未裁定のままテストケースの期待値が暫定になっている）
   - **minor**: 文書化済みの仮定・緩和策・フォールバック付きの逸脱
     （エンベロープ `assumptions` に理由と手当てが記録されているもの）
   - **info**: 改善提案・記録のみで現時点の妥当性を毀損しないもの
   同じ事実でも「文書化＋緩和策の有無」で major と minor を分ける。
   これは「健全な進行」と「要注意」を gate_status で区別するための
   基準である（[アンチパターン「AI 出力を説明できない」](../../docs/test-techniques/test-process-research-summary-test-design.md#9-アンチパターン)
   の裏返しとして、説明・前提・理由が残っている逸脱は健全とみなす）。
4. **gate_status の導出**: 所見の severity 分布から機械的に導出する。
   - blocker が1件以上 → `blocked`
   - blocker なし・major が1件以上 → `passed-with-risks`
   - major 以上なし（minor・info のみ、または所見なし） → `passed`
   どの所見が gate_status を決めたかをエンベロープの要約に明記し、
   証跡なき主張をしない（[「証跡なき品質は品質なし」](../../docs/quality-management/software-quality-gap-analysis-report.md)）。
5. **エンベロープ出力**: 所見一覧を「出力エンベロープ」節の形式で出力する。
   `trace_ids` には所見が参照した既存 ID 体系のノード ID
   （RISK-/DTC-/TAE-/TC- 等）を列挙する（ARF ID はトレースグラフ非参加の
   ため含めない）。

## 最小入力契約

コールドスタート（レビュー対象成果物が一切ない状態）で本スキルを起動する
ために最低限必要な入力は次の1つのみである。

- **レビュー対象の説明**（`review_target_summary`）: 何の成果物一式を
  何の目的でレビューするかが分かる1〜3文

`artifact_bundle_ref` は0件でも起動可能。0件の場合は「上流成果物なし時の
振る舞い」に従う。

## 上流成果物なし時の振る舞い

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) どの成果物・エンベロープが入手可能か、(b) チェーンのどの工程まで
   進んだ状態か、(c) レビュー結果を何に使うか（ゲート判定か改善か）、
   の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、必ず出力する。
   成果物がゼロの場合は、レビュー対象範囲の全前工程成果物の欠落を
   severity=blocker の所見として列挙し、`gate_status: blocked` を返す
   （成果物なしでのメタレビュー合格判定は出さない）。
3. 一部の成果物だけがある場合は、ある成果物のレビューを実施した上で、
   欠落分を blocker 所見として報告する。判定できなかった観点は
   `assumptions` または `open_questions` に **unknown** として明示する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。

```json
{
  "source_skill": "quality-artifact-review",
  "phase": "artifact-review",
  "artifacts": [
    {
      "type": "ArtifactReviewFindingList",
      "schema_ref": "schemas/artifact-review-finding.schema.json",
      "items": [
        {
          "id": "ARF-001",
          "viewpoint": "process_consistency",
          "severity": "major",
          "target_refs": ["03-tra.json", "04-tad.json", "DTC-026"],
          "statement": "仕様矛盾 G2 の裁定結果が TAD の rationale にのみ存在し、TRA エンベロープの open_questions は未解決のまま。TRA 単独の読者には DTC-026 の期待値が未確定に見える。",
          "recommendation": "裁定を記録した上で元エンベロープの open_questions の解決状態を追跡できるようにする。"
        },
        {
          "id": "ARF-002",
          "viewpoint": "document_quality",
          "severity": "minor",
          "target_refs": ["05-tdd-ti.json"],
          "statement": "trace_ids の列挙規約がエンベロープ間で不整合（全列挙と端点のみが混在）。items 側の ID は完全なため実害は限定的。",
          "recommendation": null
        }
      ]
    }
  ],
  "trace_ids": ["DTC-026"],
  "assumptions": [
    {
      "field": "traceability_source",
      "value": "06-traceability.json",
      "reason": "トレーサビリティ観点は同エンベロープの検査結果（切断0・advisory 2件）を引用し、リンク検査は再実行していない"
    }
  ],
  "open_questions": [
    "G2 裁定の一級記録（決定ログ）をどの成果物として保持するか"
  ],
  "gate_status": "passed-with-risks"
}
```

`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれかを
とり、手順4の導出規則のとおり所見の severity 分布から機械的に決まる。
