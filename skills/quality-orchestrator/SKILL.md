---
name: quality-orchestrator
description: >
  どの品質スキルを使うべきか分からない品質相談全般の入口として使う。
  例えば「この決済機能のリリース判定をしたいが何から始めればいいか」
  「品質をよくしたい」のように、テスト要求分析・リスク分析・テスト
  アーキテクチャ設計・テストケース作成・トレーサビリティ確認・リリース
  判定のどれに該当するか自分では判断できないときに使う。自然言語の相談文
  のみを入力とし、10ノードチェーン上の分類結果とルーティング先スキル名を
  出力する。複合的な依頼（要求分析からテストケースまで一気に進めたい等）
  では、risk-analysis・test-requirement-analysis・test-architecture-design・
  test-design-implementation を順に呼び出し、各段のゲート判定を
  quality-artifact-review へ委譲しつつ進行管理も担う。
version: 0.7.0
inputs:
  consultation_text:
    type: string
    required: true
    description: >
      ユーザーが発した自然言語の品質相談文（1文でも長文でもよい）。
      「何から始めればいいか分からない」という曖昧な状態も許容する
  known_artifacts_hint:
    type: string
    required: false
    description: >
      既にどの工程まで成果物があるか分かっていれば（例:「仕様書はあるが
      リスク分析はまだ」）その概要。未指定でも起動可能
  desired_scope_hint:
    type: string
    required: false
    description: >
      単一スキルへのルーティングでよいか、複合フロー（TRA→TAD→TDD/TI）
      まで一気通しで進めたいかの希望。未指定なら相談文から推定する
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-models/quality-knowledge-schema.md
  - docs/agent-ecosystem/skill-ecosystem-design-plan.md
  - docs/test-techniques/test-process-research-summary-test-design.md
---

# quality-orchestrator

Tester Skillspace 4象限: テスト技法（軽）／ドメイン（軽）／ITスキル
（ルーティングロジック）／コミュニケーション（明確化質問の設計、重）。

## 目的

ユーザーの自然言語の品質相談を [quality-knowledge-schema.md §3（AI
エージェントの推論手順）](../../docs/quality-models/quality-knowledge-schema.md#3-ai-エージェントの推論手順)
の8ステップ推論で10ノードチェーン上に分類し、
[references/routing-table.md](references/routing-table.md) を用いて適切な
専門スキルへルーティングする。複合的な依頼では risk-analysis と
test-requirement-analysis（TRA）→ test-architecture-design（TAD）→
test-design-implementation（TDD/TI）の4段階複合フローを進行管理し、
各段のゲート判定を行う。本スキルは「どのスキルを使うべきか不明な品質相談
全般」に対するメタな入口であり、ルーティング先の各スキル自体が持つ専門
分析ロジックを代替するものではない。

**最重要ルール（必読）**: 8ステップ推論の途中を飛ばしてテストケース生成
に直行してはならない。相談が「テストケースを作って」のように下流の
ステップから始まっていても、①〜④（要求・ステークホルダー・リスク・
品質特性・受入基準）が不明なら、まず上流を遡って確認するか、不明点を
`assumptions`/`open_questions` に記録した上で最上流フェーズからルーティング
する（[quality-knowledge-schema.md §3 運用ルール1](../../docs/quality-models/quality-knowledge-schema.md#3-ai-エージェントの推論手順)）。

**ゲート判定の位置づけ（必読）**: 複合フロー各段のゲート判定は
`quality-artifact-review` へ委譲する（手順7）。本スキルは判定結果の3値
`gate_status` を受け取って遷移（進行・停止）を管理することに専念し、
ゲート観点の充足判定そのものは行わない。これは
[skill-ecosystem-design-plan.md §4 ゲート基準](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#4-オーケストレーション設計)
の「MVP では内蔵、Phase 2 で quality-artifact-review スキルへ委譲」の
委譲を実装した状態である。

## 手順

1. **8ステップ推論によるチェーンノード分類**: `consultation_text` を
   [quality-knowledge-schema.md §3 の8ステップ](../../docs/quality-models/quality-knowledge-schema.md#3-ai-エージェントの推論手順)
   （①要求・ステークホルダー→②リスク→③品質特性→④受入基準→⑤テスト・
   評価方法→⑥メトリクス・証跡→⑦リリース判断→⑧本番監視）に照らし、
   相談文がどのステップ・ノードに該当するかを分類する。複数ノードに
   またがる場合は該当ノードをすべて記録する。
2. **ルーティング表の適用**: 手順1の分類結果を
   [references/routing-table.md](references/routing-table.md) の
   「チェーンノード×意図（動詞・依頼文）」列と照合し、ルーティング先
   スキルを決定する。1つの相談が複数行に一致する場合は、最も上流の
   フェーズ（8ステップの番号が小さい方）を優先する。
3. **曖昧な場合の明確化質問（1回まで・必須ルール）**: ルーティング表の
   複数行に同程度一致し決定できない場合、明確化質問を**1回だけ**行う。
   質問は「どの工程まで話を進めたいか」「対象機能・変更の概要」のうち
   最も分類に効く1点に絞る。**質問は1回までであり、2回目の質問は行わない**。
   回答が得られない、または利用者が回答不能な場合でも、次の手順4に進み
   必ず出力する（無回答を理由に無出力にはしない）。
4. **フォールバック（それでも定まらない場合）**: 手順3の質問後もルーティング
   先が1つに定まらない場合、入力が揃っている最上流フェーズへルーティング
   する（[skill-ecosystem-design-plan.md §4 の根拠](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#4-オーケストレーション設計)：
   「情報が少ないときほど上流から手当てする」）。`fallback_applied: true`
   をエンベロープに記録する。
   どのスキルの最小入力も満たさない truly-empty の相談時は、フェーズ順最上流の
   `test-requirement-analysis` に着地し、以降は当該スキルのコールドスタート
   分岐に委ねる（[skill-ecosystem-design-plan.md §4「上流から手当てする」](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#4-オーケストレーション設計)）。
5. **P2/P3 スキル宛の案内**: 分類結果が [routing-table.md フォールバック
   規則](references/routing-table.md#フォールバック規則) に従い未実装の
   P2/P3 スキル
   （`code-review`・`defect-analysis-rca`・
   `ai-system-quality-eval`・
   `business-quality-metrics`・
   `exploratory-testing-support`）と判定された場合、「該当スキルは
   未実装。`docs/` の該当文書（ルーティング表の Phase 列
   参照）を手動で参照すること」と案内し、`gate_status: blocked` を返す。
   `quality-artifact-review`・`test-execution-support`・`nfr-review`・
   `sre-quality-ops` は実装済みのため本手順の対象外であり、手順6の単体
   ルーティングとして扱う。
6. **単体ルーティングの実行**: MVP スキル1つへのルーティングと判定した
   場合、ルーティング先スキル名を要素1の順序付き配列として分類根拠とともに
   出力する（本スキル自身はルーティング先スキルの手順を代行実行しない。
   呼び出しは利用者または呼び出し環境が行う）。
7. **複合フローの進行管理とゲート判定の委譲（`desired_scope_hint` が
   複合フローを示す場合）**: risk-analysis を並行起動し、その
   `RiskRegister` を test-requirement-analysis（TRA）のゲート入力として
   渡す。以降 TRA → test-architecture-design（TAD）→
   test-design-implementation（TDD/TI）の順で各スキルを起動する。
   `routed_skill` にはこの実行順でスキル名を並べる。各段のゲート判定は
   本スキルでは行わず、段の完了ごとに `quality-artifact-review` を次の
   呼び出し境界で起動して委譲する。
   - **入力**: `review_target_summary` にどの段のゲート判定かを1〜2文で
     渡し、`artifact_bundle_ref` にその段までのエンベロープ・成果物一式を、
     `review_scope_hint` に [references/pipeline-gates.md](references/pipeline-gates.md)
     の該当フェーズ観点（TRA/TAD/TDD/TI レビュー）を渡す
   - **出力**: quality-artifact-review が所見の severity 分布から機械的に
     導出した3値 `gate_status` を、その段のゲート結果として採用する
   - **短絡則**: 段のスキル自身が `blocked` を返した場合は、委譲呼び出しを
     行わずその段を `blocked` として扱う
   採用した `gate_status` に応じて次の遷移を適用する（遷移の管理は本スキル
   の責務のまま）。
   - `passed`: 次段へそのまま進める
   - `passed-with-risks`: 残存リスクを明示した上で次段へ進める
   - `blocked`: 停止し、利用者にその段までの結果と理由を返す
8. **トレーサビリティの一括付与**: 複合フロー（TRA→TAD→TDD/TI）が末尾まで
   進んだ後に `traceability-management` を**1回**呼び、成果物一式に対して
   チェーンリンクを付与する
   （[skill-ecosystem-design-plan.md §4 の4段階複合フロー図](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#4-オーケストレーション設計)
   の `TRC` の役割）。各段完了ごとに逐次呼ばない——未完成チェーンに対する
   トレースは下流ノード未生成を「切断」として大量に報告してしまい、
   ノイズになるためである（複合フロー内の各段のゲート判定は手順7の
   `gate_status` が担い、トレーサビリティ検査はフロー末尾でまとめて行う）。
   なお、いずれかの段が `blocked` で複合フローが途中停止した場合は、
   その時点までの成果物一式に対して呼ぶ。
9. **統合レポートの出力**: 単体ルーティング・複合フローのいずれでも、
   分類結果・ルーティング先（または各段の結果）・残存する `assumptions`/
   `open_questions` をまとめ、出力エンベロープとして返す。

## 最小入力契約

コールドスタート（他スキルの成果物が一切ない状態）で本スキルを起動する
ために最低限必要な入力は次の1つのみである。

- **自然言語の相談文**（`consultation_text`）: 曖昧な1文（例:「品質を
  よくしたい」）でも起動可能

`known_artifacts_hint`・`desired_scope_hint` はいずれも任意であり、与えられ
なくても起動・出力可能である。本スキルは常にコールドスタート前提であり、
上流成果物（他スキルの出力）を必須入力としない。

## 上流成果物なし時の振る舞い

本スキルはオーケストレーターという性質上、常にコールドスタート
（相談文のみ）から起動される前提である。ルーティング先スキルの成果物が
存在しない場合、次の手順で分類・ルーティングを継続する。

1. **明確化質問は1回まで**とし、それ以上は聞かない（手順3参照）。他の
   MVP スキルの「質問は最大3件まで」より厳格な制約であることに注意する
   （ハブ§4 の規定）。
2. 回答が得られない、または利用者が回答不能な場合でも、**入力が揃って
   いる最上流フェーズへ必ずルーティングして返す**（手順4）。分類不能を
   理由に無出力にはしない。
3. フォールバックを適用した場合は `fallback_applied: true` を、明確化質問
   を行った場合は `clarification_asked: true` を、それぞれエンベロープの
   `RoutingDecision` 成果物に記録する。

## 出力エンベロープ

本スキルは常に下記形式のハンドオフエンベロープ（
[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を出力する。`RoutingDecision` の `schema_ref` には
[schemas/routing-decision.schema.json](../../schemas/routing-decision.schema.json)
を指定し、`content` を同スキーマに準拠させる。`routed_skill` はスキル名の
順序付き配列とし、単体ルーティングでも要素1の配列にする。

例は「決済機能のリリース判定をしたいが何から始めればいいか」という相談文
を分類する例である。この相談は⑦リリース判断（REL/EV ノード）に見えるが、
「何から始めればいいか」という言い回しから証跡・受入基準が未整理な可能性
が高く、ルーティング表の複数行（`quality-gate-release-judgment` と
`test-requirement-analysis`）に一致しうるため、明確化質問を1回行った上で
証跡確認を先にできる `quality-gate-release-judgment` へルーティングした
例とする。

```json
{
  "source_skill": "quality-orchestrator",
  "phase": "routing",
  "artifacts": [
    {
      "type": "RoutingDecision",
      "schema_ref": "schemas/routing-decision.schema.json",
      "content": {
        "chain_nodes": ["EV", "REL"],
        "routed_skill": ["quality-gate-release-judgment"],
        "clarification_asked": true,
        "fallback_applied": false
      }
    }
  ],
  "trace_ids": [],
  "assumptions": [
    "「何から始めればいいか」という言い回しから、証跡が未整理な可能性を想定し、テスト要求分析ではなくリリース判定（証跡収集起点）を優先ルーティング先とした"
  ],
  "open_questions": [
    "決済機能の変更概要と、入手可能な証跡ファイル（テスト結果・カバレッジレポート等）はあるか"
  ],
  "gate_status": "passed"
}
```

複合フローでは、同じ `RoutingDecision` 成果物を次のように出力する。

```json
{
  "type": "RoutingDecision",
  "schema_ref": "schemas/routing-decision.schema.json",
  "content": {
    "chain_nodes": ["RISK", "REQ", "AC", "TEST"],
    "routed_skill": [
      "risk-analysis",
      "test-requirement-analysis",
      "test-architecture-design",
      "test-design-implementation"
    ],
    "clarification_asked": false,
    "fallback_applied": false,
    "flow_label": "要求分析からテストケース設計まで"
  }
}
```

`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれか
をとる。本スキル自身のルーティング処理が完了した場合は `passed` を返す。
複合フローの進行管理中にいずれかの段が `blocked` を返した場合は、本スキル
の `gate_status` も `blocked` とし、それ以降の段へ進めない。

## 関連ドキュメント

- [references/routing-table.md](references/routing-table.md) — 第2段階
  ルーティング表
- [references/pipeline-gates.md](references/pipeline-gates.md) — 複合フロー
  のゲート観点（quality-artifact-review へ渡す入力チェックリスト）
- [quality-artifact-review/SKILL.md](../quality-artifact-review/SKILL.md) —
  各段ゲート判定の委譲先（3値 `gate_status` の導出元）
