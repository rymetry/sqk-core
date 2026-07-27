---
name: defect-analysis-rca
description: >
  「この障害の根本原因を分析してほしい」「ポストモーテムのドラフトを
  作ってほしい」「この欠陥群の傾向を分析してほしい」のように、欠陥・
  障害の分類・根本原因分析・ポストモーテム支援が必要なときに使う。
  欠陥票・インシデント記録を材料に、ODC（直交欠陥分類）による欠陥
  分類、RCA 手法（5 Whys／フィッシュボーン／FTA／STPA）の選定理由
  付きの因果分析、ブレームレスな RCA レポート／ポストモーテム
  ドラフト、および `RiskRegister` 更新提案（`RISK-nnn`）を出力する。
  インシデント記録のテキストのみで起動できる。欠陥 DB の運用・
  修正の適用・再発防止策の実装は行わない（実行系が担う）。
version: 0.1.0
inputs:
  analysis_request_summary:
    type: string
    required: true
    description: >
      何を（単一の障害・欠陥か、欠陥群か）、何の目的で（根本原因分析か
      ポストモーテムか傾向分析か）分析するかの1〜3文（記録が入手
      できない場合の唯一の必須入力）
  incident_records_ref:
    type: path
    required: false
    description: >
      欠陥票・インシデント記録・タイムライン・ポストモーテムドラフト
      への参照（複数件をまとめて渡してよい。欠陥群の傾向分析には
      複数件が必要）
  fix_info_ref:
    type: path
    required: false
    description: >
      修正情報（修正 diff・修正記録・クローズ済み欠陥票）への参照。
      ODC closer 属性（Target/Defect Type/Qualifier/Source/Age）の
      確定に必要。無い場合は opener 属性のみ分類する
  risk_register_ref:
    type: path
    required: false
    description: >
      既存の RiskRegister・上流ハンドオフエンベロープ群への参照
      （更新提案の突合先。無い場合は新規リスク項目として提案する）
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  risk_item:
    schema: ../../schemas/risk-item.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-management/defect-taxonomy-odc.md
  - docs/governance-compliance/domain-specific-quality-and-safety-standards.md
  - docs/operations-quality/production-quality-sre-observability.md
---

# defect-analysis-rca

Tester Skillspace 4象限: テスト技法（中）／ドメイン（重、障害文脈の
理解）／ITスキル（軽）／コミュニケーション（ブレームレスな記述、最重）。

## 目的

欠陥票・インシデント記録を
[defect-taxonomy-odc.md](../../docs/quality-management/defect-taxonomy-odc.md)
の ODC 語彙で分類し、状況に応じて選定した RCA 手法（5 Whys／
フィッシュボーン／FTA／STPA）で因果分析を行い、**ブレームレスな
RCA レポート（またはポストモーテムドラフト）と `RiskRegister` 更新
提案**を返す。単一障害の深掘りと、欠陥群の分布分析
（[同 §5](../../docs/quality-management/defect-taxonomy-odc.md#5-分布分析のパターン)）
の両モードを持ち、ODC と個別 RCA は代替ではなく補完として使う
（[同 §6](../../docs/quality-management/defect-taxonomy-odc.md#6-rca-との関係--代替ではなく補完)）。

役割分担: テスト実行結果からの欠陥候補抽出は test-execution-support
（`DefectCandidateList`）、リスクの体系的な洗い出し・登録簿の所有は
risk-analysis（本スキルは**更新の提案のみ**を返し、採否・採番の確定は
risk-analysis または利用者が行う）、設計段階の hazard analysis の網羅
実施は risk-analysis が担い、本スキルは代行しない。本スキルの固有の
責務は**発生した欠陥・障害からの学習（分類・因果・再発防止）を、
下流が使える契約（RISK 更新提案）へ変換すること**である。

**実行境界（必読）**: 本スキルは欠陥分析の手順・語彙・出力契約の
ブループリントであり、欠陥 DB・インシデント管理システムの運用、
修正の適用、再発防止策の実装・検証実行は実行系（veridia 等）が担う
（[DECISIONS.md D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)
の実行境界）。提案する `RISK-nnn` は skill-handoff の知識成果物で
あり、リスク登録簿そのものの更新ではない。

## 手順

1. **入力の分類とモード判定**: `incident_records_ref` の記録件数と
   `analysis_request_summary` から、(a) 単一障害の RCA／ポストモーテム
   モード、(b) 欠陥群の分布分析モード、のいずれか（または両方）を
   判定する。`fix_info_ref` の有無で ODC closer 属性の確定可否を
   確認する。
2. **ODC 分類**: [defect-taxonomy-odc.md §2〜§4](../../docs/quality-management/defect-taxonomy-odc.md#2-odc-の構造--2時点8属性)
   に従い、記録から opener 属性（Activity/Trigger/Impact）を分類する。
   closer 属性（Target/Defect Type/Qualifier/Source/Age）は
   **修正情報が入力にあるときだけ確定**し、症状からの Type 推定は
   しない（[同 §7](../../docs/quality-management/defect-taxonomy-odc.md#7-運用と-ai-エージェント適用の注意)）。
   各分類に根拠（記録のどの記述から判断したか）を付し、根拠を構成
   できない属性は unknown とする。フィールド欠陥は「本来どの工程
   活動が捕捉すべきだったか」を Activity に割り当てる
   （[同 §3.3](../../docs/quality-management/defect-taxonomy-odc.md#33-フィールド欠陥への適応)）。
3. **RCA 手法の選定（選定理由の出力必須）**: 単一障害モードでは、
   次の規則で手法を選び、**選定理由を必ず出力に含める**。
   - **5 Whys**: 単線的な因果連鎖が想定される欠陥・プロセス逸脱。
     最小コストで開始し、連鎖が分岐したら他手法へ切り替える。
   - **フィッシュボーン（特性要因図）**: 要因が複数カテゴリ（プロセス・
     ツール・環境・情報など）に分散し、構造化した列挙が先に必要な場合。
   - **FTA**: 頂上事象が明確に定義でき、故障の論理的組合せ（AND/OR）
     を追う必要がある場合（[domain-specific-quality-and-safety-standards.md §2](../../docs/governance-compliance/domain-specific-quality-and-safety-standards.md#2-hazard-analysis-の手法)）。
   - **STPA**: 個々のコンポーネント故障では説明できず、相互作用・
     制御構造（フィードバック欠落・制御アクションの不整合）の問題が
     疑われる場合（同 §2）。
   複数手法の併用（例: フィッシュボーンで整理 → 支配的経路を 5 Whys
   で深掘り）を妨げない。併用時は各手法の役割を選定理由に書く。
4. **ブレームレスな因果分析**: 選定手法で因果分析を実施する。
   [production-quality-sre-observability.md](../../docs/operations-quality/production-quality-sre-observability.md)
   のブレームレスポストモーテムの原則に従い、**人を原因に置かない**
   （「誰が誤ったか」ではなく「何がその誤りを可能にし、なぜ防護が
   働かなかったか」）。個人名・非難語彙を使わず、要因はシステム・
   プロセス・情報の欠落として記述する。是正策は「注意する・教育する」
   で終わらせず、ガードレール（プロセス変更・自動化・設計変更・
   検出の追加）として提案し、各是正策に効果の検証方法を付す。
5. **欠陥群の分布分析**（欠陥群モードの場合）:
   [defect-taxonomy-odc.md §5](../../docs/quality-management/defect-taxonomy-odc.md#5-分布分析のパターン)
   の分析パターン（Defect Type の工程シグネチャ・Trigger による
   テスト診断・二元分析・Age/Source・欠陥密度との併用）で分布を
   診断する。**数件規模のデータで分布を断定しない**（同 §5 の
   サンプル規模の注意）。件数が少ない場合は個別分析へ切り替え、
   その判断を出力に明記する。深掘り対象の代表欠陥の選定は分布の
   集中セルに基づいて行う（同 §6 の補完運用）。
6. **RiskRegister 更新提案**: 分析結果（残存する再発リスク・分布が
   示す系統的な弱さ）を
   [schemas/risk-item.schema.json](../../schemas/risk-item.schema.json)
   準拠のリスク項目として提案する。`risk_register_ref` がある場合は
   既存 `RISK-` との重複・更新（likelihood/impact の見直し・
   residual_risk の書き換え）を突合し、新規か更新かを明示する。
   採番は仮採番であることを `assumptions[]` に記録し、確定は
   risk-analysis／利用者に委ねる。
7. **エンベロープ出力**: 「出力エンベロープ」節の形式で出力する。
   `gate_status` は、記録を一切読めなかった場合のみ `blocked`、
   修正情報なしで closer 属性・因果の確定に至らない（原因仮説
   どまり）場合や是正策の検証方法が未定の場合は `passed-with-risks`、
   分類・因果分析・検証方法付き是正策まで揃った場合は `passed` と
   する。

## 最小入力契約

コールドスタート（欠陥票・インシデント記録が一切ない状態）で本スキルを
起動するために最低限必要な入力は次の1つのみである。

- **分析対象の説明**（`analysis_request_summary`）: 何を何の目的で
  分析するかが分かる1〜3文

`incident_records_ref`・`fix_info_ref`・`risk_register_ref` はいずれも
任意であり、与えられなくても起動・出力可能である。インシデント記録の
テキストが1件でもあれば、単一障害モードの分析は完全に実施できる
（修正情報が無い場合は opener 属性のみの分類となり、その旨を明記する）。

## 上流成果物なし時の振る舞い

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき
   質問は (a) 欠陥票・インシデント記録はどこにあるか、(b) 修正情報
   （diff・修正記録）はあるか、(c) 分析結果を何に使うか（再発防止か
   ポストモーテム公開か リスク登録簿の更新か）、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、必ず出力する。
   記録が1件も無い場合は、`analysis_request_summary` から推定できる
   範囲の「分析に必要な記録・情報の一覧」と RCA 手法の候補のみを
   出し、因果・分類の断定はせず `gate_status: blocked` を返す
   （記録を見ずに根本原因を断定しない）。
3. 記録はあるが修正情報・タイムラインが不完全な場合は、読み取れた
   範囲で分析した上で、推定した前提を `assumptions[]` に
   `{field,value,reason}` 形式で記録し、確定できなかった属性・因果は
   unknown として `open_questions` に明示する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。

```json
{
  "source_skill": "defect-analysis-rca",
  "phase": "defect-analysis-rca",
  "artifacts": [
    {
      "type": "DefectClassification",
      "schema_ref": "skills/defect-analysis-rca/SKILL.md",
      "content": {
        "classifications": [
          {
            "defect_ref": "インシデント記録 INC-2041",
            "activity": "system-test",
            "activity_rationale": "本来はシステムテストの回復系シナリオが捕捉すべきフィールド欠陥のため、捕捉責任のある活動を割り当てた",
            "trigger": "recovery-exception",
            "trigger_rationale": "プライマリ DB のフェイルオーバー発生時のみ再現（記録のタイムライン 02:14 の切替イベントが前提条件）",
            "impact": "reliability",
            "closer_attributes": {
              "target": "code",
              "defect_type": "timing-serialization",
              "qualifier": "missing",
              "source": "developed-in-house",
              "age": "base",
              "rationale": "修正 diff が接続プール再取得処理へのロック追加のため Timing/Serialization・Missing と分類。修正対象は今回未変更の既存モジュール（Base）"
            }
          }
        ]
      }
    },
    {
      "type": "RcaReport",
      "schema_ref": "skills/defect-analysis-rca/SKILL.md",
      "content": {
        "mode": "single-incident",
        "method": ["fishbone", "5-whys"],
        "method_selection_rationale": "要因がプロセス・構成・監視の複数カテゴリに分散していたためフィッシュボーンで列挙し、支配的だった構成系の経路のみ 5 Whys で深掘りした。制御構造の不整合は認められず STPA は不要と判断",
        "causal_chain": [
          "フェイルオーバー時に接続プールが旧プライマリへの接続を保持し続けた",
          "再接続処理に排他制御が無く、切替中の並行リクエストが混在した",
          "切替を検出する監視が無く、劣化状態が42分継続した"
        ],
        "contributing_factors": [
          "フェイルオーバー手順の検証がステージングの単発試行のみで、並行負荷下の試験が計画されていなかった"
        ],
        "corrective_actions": [
          {
            "action": "接続プール再取得処理への排他制御追加（適用済み修正の恒久化とレビュー観点への追加）",
            "verification": "フェイルオーバー注入テストを回帰スイートに追加し、並行負荷下で成功することを確認"
          },
          {
            "action": "フェイルオーバー検出アラートの追加",
            "verification": "切替演習で検出までの時間が SLO 内であることを確認"
          }
        ]
      }
    },
    {
      "type": "RiskRegisterUpdateProposal",
      "schema_ref": "schemas/risk-item.schema.json",
      "items": [
        {
          "id": "RISK-101",
          "statement": "フェイルオーバー時の再接続経路に未検証の並行処理が残ることにより、切替時にデータ不整合が発生し、エンドユーザーが処理結果の喪失という不利益を受ける",
          "category": "product",
          "likelihood": "medium",
          "impact": "high",
          "affected_stakeholder_refs": [],
          "requirement_refs": [],
          "treatment": "mitigate",
          "residual_risk": "排他制御追加後も、フェイルオーバー中に受け付けたリクエストの再実行方針が未定義"
        }
      ]
    }
  ],
  "trace_ids": ["RISK-101"],
  "assumptions": [
    {
      "field": "risk_id_numbering",
      "value": "RISK-101 は仮採番",
      "reason": "既存 RiskRegister が入力に無く、確定採番は risk-analysis または利用者が行う"
    },
    {
      "field": "timeline_source",
      "value": "インシデント記録 INC-2041 の記載時刻のみ",
      "reason": "監視システムの生ログは未入手のため、継続時間42分は記録の記載に依拠した"
    }
  ],
  "open_questions": [
    "フェイルオーバー中に受け付けたリクエストの再実行・補償の仕様はどこで定義されるか"
  ],
  "gate_status": "passed-with-risks"
}
```

`DefectClassification`・`RcaReport` は ID 体系を持たない助言的成果物の
ため専用スキーマを設けず `content` に置き、`RiskRegisterUpdateProposal`
の各 item は [risk-item schema](../../schemas/risk-item.schema.json) に
valid でなければならない（[schemas/README.md の content/items
使い分け](../../schemas/README.md)）。ODC 属性値は
[defect-taxonomy-odc.md](../../docs/quality-management/defect-taxonomy-odc.md)
の値集合を使い、確定できない属性は `"unknown"` とする（値集合の
増改築はしない。同 §7）。`trace_ids` には提案した RISK- と、入力に
含まれる既存 ID（RUN-・TC- 等）を列挙する。`gate_status` は
`passed` / `passed-with-risks` / `blocked` の3値のいずれかをとる
（判定規則は手順7）。

## 関連ドキュメント

- [defect-taxonomy-odc.md](../../docs/quality-management/defect-taxonomy-odc.md) — ODC 8属性・分布分析・RCA との補完の主参照
- [domain-specific-quality-and-safety-standards.md](../../docs/governance-compliance/domain-specific-quality-and-safety-standards.md) — FTA・STPA 等の hazard analysis 手法の正典
- [production-quality-sre-observability.md](../../docs/operations-quality/production-quality-sre-observability.md) — ブレームレスポストモーテムの原則と実践
