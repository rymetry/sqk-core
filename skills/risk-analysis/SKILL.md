---
name: risk-analysis
description: >
  プロダクトリスク分析が必要なとき、または「このリリースのリスクを洗い出して」
  「重要度・厚みをどう決めればいいか」という問いに答える必要があるときに使う。
  機能概要、変更差分、既知の障害影響、（あれば）過去の欠陥履歴を材料に、
  FMEA/FTA/STPA/STRIDE の中から状況に応じた手法を選び、影響度×発生確率で
  優先度付けしたリスク一覧を生成する。TRA・TAD・リリース判定への入力となる。
version: 0.1.0
inputs:
  feature_summary:
    type: string
    required: true
    description: 対象機能・変更の概要（何を、なぜ、どこに影響するか）
  change_diff:
    type: string
    required: false
    description: 変更差分（diff、変更点リスト等）。あれば影響範囲の特定精度が上がる
  known_failure_impact:
    type: string
    required: false
    description: 既知の障害シナリオ・過去のインシデントが分かっていればその概要
  defect_history_ref:
    type: path
    required: false
    description: >
      過去の欠陥履歴（動的ナレッジ `knowledge/dynamic/defect-history.yaml`）への
      パス。存在しない場合は業界一般の既知リスクパターンから仮説を提示する
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  risk_register:
    schema: ../../schemas/risk-item.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-models/quality-knowledge-schema.md
  - docs/governance-compliance/domain-specific-quality-and-safety-standards.md
  - docs/secure-development/secure-development-and-supply-chain.md
  - docs/quality-management/software-quality-management-practical-reference.md
---

# risk-analysis

Tester Skillspace 4象限: テスト技法（中）／ドメイン（重）／ITスキル（軽）／コミュニケーション（リスク説明、中）。

## 目的

プロダクトリスク（影響度×発生確率）を分析し、`RiskRegister`（`RISK-nnn`）として
優先度付けの根拠とともに出力する。分析対象の性質（ハードウェア故障起因／
ソフトウェア・自動化・人間の関与／プロセス逸脱／セキュリティ脅威）に応じて
FMEA・FTA・STPA・STRIDE のいずれを使うかを選び、**選定理由を出力に明記する**。
本スキルの出力は test-requirement-analysis（TRA）・test-architecture-design（TAD）・
[quality-gate-release-judgment](../quality-gate-release-judgment/SKILL.md) への
入力になる（[スキル・エコシステム設計プラン](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md)
§3 参照。TRA・TAD は本タスク時点で未実装）。

## 手順

1. **入力の分類**: `feature_summary` / `change_diff` / `known_failure_impact` を
   読み、変更が何に影響するか（コンポーネント、ステークホルダー、規制ドメインの
   有無）を整理する。`defect_history_ref` が与えられ実データが存在すれば読み込み、
   類似の過去欠陥を仮説の裏付けに使う。存在しなければ「上流成果物なし時の
   振る舞い」に従う。
2. **手法選択とその理由の記録（必須）**: 対象の性質を
   [hazard analysis の手法比較表](../../docs/governance-compliance/domain-specific-quality-and-safety-standards.md#2-hazard-analysis-の手法)
   の使い分け目安と照合し、FMEA/FTA/STPA/STRIDE のいずれか（複数可）を選ぶ。
   選定理由（対象がハードウェア故障起因か、ソフトウェア・自動化・人間の関与が
   支配的か、プロセス逸脱か、セキュリティ脅威かの判定根拠）を必ず1〜2文で記録し、
   出力エンベロープの `assumptions` または成果物本体に含める。判断に迷う場合は
   [references/technique-selection.md](references/technique-selection.md) の
   対応表を参照する。
3. **リスク項目の列挙**: 選んだ手法の観点でリスクを列挙し、各項目を
   [RISK ノードのデータ契約](../../docs/quality-models/quality-knowledge-schema.md#risk-riskリスク)
   に従って `id`（`RISK-nnn`）・`statement`・`category`・`likelihood`・`impact`・
   `affected_stakeholder_refs`・`requirement_refs`・`treatment`・`residual_risk`
   のフィールドで記述する。STRIDE を選んだ場合は
   [STRIDE の6分類](../../docs/secure-development/secure-development-and-supply-chain.md#41-stride)
   に沿って脅威種別ごとに洗い出す。
4. **影響度×発生確率の判定**: `likelihood`（low/medium/high）と `impact`
   （low/medium/high/critical）を、`affected_stakeholder_refs` が被る不利益の
   大きさから判定する。規制ドメイン（安全・医療・金融等）に該当する場合は、
   影響度の判定基準自体が規格で定義され得ることに留意し、
   [ドメイン別品質・安全規格](../../docs/governance-compliance/domain-specific-quality-and-safety-standards.md)
   の該当ドメイン節を確認する。セキュリティ・コンプライアンスの一般的な
   リスク評価の枠組み（ISO 31000 等）については
   [品質管理実務リファレンスのリスク・コンプライアンス・セキュリティ品質節](../../docs/quality-management/software-quality-management-practical-reference.md#リスクコンプライアンスセキュリティ品質)
   を参照する。
5. **優先度付けと出所レイヤの明示**: `likelihood × impact` で優先順位を決め、
   最優先で対処すべきリスクから並べる。判断の根拠が静的ナレッジ（`docs/` の
   一般知識）由来か、動的ナレッジ（`defect_history_ref` 等のプロジェクト固有
   データ）由来かを、[ナレッジ参照順序の原則](../../docs/agent-ecosystem/knowledge-management-design.md#14-スキルの参照順序と出所レイヤの明示)
   に従い出力に明示する。動的ナレッジが存在しない場合は業界一般の既知リスク
   パターンからの仮説である旨を `assumption: true` として明記する。

## 最小入力契約

コールドスタート（他スキルの成果物が一切ない状態）で本スキルを起動するために
最低限必要な入力は次の1つのみである。

- **対象機能・変更の概要**（`feature_summary`）: 何を変更し、どこに影響するかを
  1〜3文で記述したもの

`change_diff`・`known_failure_impact`・`defect_history_ref` はいずれも任意であり、
与えられなくても起動・出力可能である。

## 上流成果物なし時の振る舞い

過去の欠陥履歴（動的ナレッジ `knowledge/dynamic/defect-history.yaml`）や
変更差分などの上流成果物が存在しない場合、次の手順で分析を継続する。

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) 変更が既存のどの機能・コンポーネントに影響するか、(b) 対象が安全・医療・
   金融等の規制ドメインに該当するか、(c) 直近で類似の障害・インシデントが
   あったか、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、**業界一般の既知リスク
   パターン**（該当ドメインで典型的な故障モード・脅威パターン）から仮説として
   リスクを提示し、必ず出力する。分析不能を理由に無出力にはしない。
3. 仮説として提示したリスク項目には `assumption: true` を付与し、根拠が
   実データ（動的ナレッジ）ではなく一般的なパターンからの推定であることを
   `open_questions` にも反映する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠、各リスク項目は [schemas/risk-item.schema.json](../../schemas/risk-item.schema.json)
準拠）を必ず出力する。これにより、後から `test-requirement-analysis` や
`quality-orchestrator` に再取り込みできる。

```json
{
  "source_skill": "risk-analysis",
  "phase": "risk-analysis",
  "artifacts": [
    {
      "type": "RiskRegister",
      "schema_ref": "schemas/risk-item.schema.json",
      "items": [
        {
          "id": "RISK-001",
          "statement": "決済APIのタイムアウト値変更により二重課金が発生し、STK-001（決済利用者）が金銭的不利益を受ける",
          "category": "product",
          "likelihood": "medium",
          "impact": "critical",
          "affected_stakeholder_refs": ["STK-001"],
          "requirement_refs": ["REQ-042"],
          "treatment": "mitigate",
          "residual_risk": "冪等性キーが未実装のリトライ経路が残る"
        },
        {
          "id": "RISK-002",
          "statement": "決済APIのエラーメッセージが内部スタック情報を含み、STK-001（決済利用者）の情報が攻撃者に漏えいする",
          "category": "security",
          "likelihood": "low",
          "impact": "medium",
          "affected_stakeholder_refs": ["STK-001"],
          "requirement_refs": [],
          "treatment": "mitigate",
          "residual_risk": null
        }
      ]
    }
  ],
  "trace_ids": ["RISK-001", "RISK-002"],
  "assumptions": [
    "過去の欠陥履歴（knowledge/dynamic/defect-history.yaml）が空のため、決済API一般の既知障害パターン（二重課金・タイムアウト連鎖）から RISK-001 を仮説として提示した（静的ナレッジのみに基づく一般論）",
    "手法選択: 対象はソフトウェア・自動化が支配的なAPI変更のためSTPAの適用も検討したが、変更範囲が単一エンドポイントの故障モードに限定されるため FMEA 的な故障モード列挙で十分と判断し、RISK-001 を抽出した。RISK-002 は外部境界を越えるデータフローが関わるため STRIDE（Information Disclosure）を適用した"
  ],
  "open_questions": [
    "決済APIの冪等性キーは実装済みか",
    "直近3リリースで同種のタイムアウト変更に起因する障害はあったか"
  ],
  "gate_status": "passed-with-risks"
}
```

`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれかを
とる。規制ドメインへの該当有無や過去欠陥の有無が判定できずリスクの見落とし
可能性が高い場合は `blocked` とし、後続スキルに「未確認のまま進めない」ことを
伝える。
