---
name: traceability-management
description: >
  要求からテストケースまでのつながりが切れていないか確認してほしいとき、
  または「テスト空間のカバレッジ（レベル×タイプ×プロセス）を可視化して
  ほしい」という問いに答える必要があるときに使う。REQ〜RISK〜HTC〜DTC〜
  TAE〜COV〜TC の ID 参照群（Markdown/JSON/CSVいずれか）を材料に、フォワード
  ／バックワード双方向でリンク切れ・未接続ノードを検出し、`TraceabilityMatrix`
  とテスト空間3軸マトリクス（Markdownヒート表）を生成する。
version: 0.1.0
inputs:
  artifact_bundle_ref:
    type: path
    required: false
    description: >
      これまでの工程（risk-analysis / test-requirement-analysis /
      test-architecture-design / test-design-implementation）が出力した
      ハンドオフエンベロープ群、または成果物ファイル（Markdown/JSON/CSV）
      へのパス。複数ファイルをまとめて渡してよい
  feature_summary:
    type: string
    required: true
    description: >
      対象機能の説明文（成果物一式が無い場合の唯一の必須入力。何のトレース
      チェーンを検査したいかが分かる1〜3文）
  test_space_scope_hint:
    type: string
    required: false
    description: >
      テスト空間3軸マトリクスで優先確認したい軸の値（例:「security特性の
      systemレベルを重点確認したい」）。未指定なら全軸を対象にする
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-models/quality-knowledge-schema.md
  - docs/test-techniques/test-process-research-summary-test-design.md
  - docs/agent-ecosystem/knowledge-management-design.md
  - knowledge/test-space/matrix-template.yaml
---

# traceability-management

Tester Skillspace 4象限: テスト技法（軽）／ドメイン（軽）／
ITスキル（重、可視化・データ処理）／コミュニケーション（軽）。

## 目的

REQ〜RISK〜HTC〜DTC〜TAE〜COV〜TC〜TPR〜RUN〜BUG〜DEC の ID 参照群を材料に、
[quality-knowledge-schema.md §1.4（ノード間関係と双方向トレース）](../../docs/quality-models/quality-knowledge-schema.md#14-ノード間関係と双方向トレース)
のフォワード／バックワード双方向トレースを実施し、リンク切れ・未接続
ノードを検出して `TraceabilityMatrix` として出力する。加えて、
[knowledge-management-design.md §6（テスト空間3軸マトリクスによる品質
カバレッジ可視化）](../../docs/agent-ecosystem/knowledge-management-design.md#6-テスト空間3軸マトリクスによる品質カバレッジ可視化)
のテンプレート（[matrix-template.yaml](../../knowledge/test-space/matrix-template.yaml)）
に基づき、レベル×タイプ×プロセスのカバレッジ状況を `TestSpaceMatrix` として
Markdown ヒート表で描画する。本スキルは
[test-requirement-analysis](../test-requirement-analysis/SKILL.md)・
[test-architecture-design](../test-architecture-design/SKILL.md)・
[test-design-implementation](../test-design-implementation/SKILL.md) の
各段の後に随時起動されるのが標準だが、単体起動も可能である。

**役割境界（必読）**: 本スキルはリンクの有無・整合性を**検査・報告**する
だけであり、欠けているノードの内容（例: 未接続の DTC が本来参照すべき
REQ）を推測して埋めることはしない。埋め戻しは元の工程スキル（TRA/TAD/
TDD-TI）または人間の作業とする。

## 手順

1. **入力の確認と成果物の分類**: `artifact_bundle_ref` が与えられ実データが
   存在すれば読み込み、各ファイルがどのノード種別（REQ/RISK/HTC/DTC/TAE/
   COV/TC 等）に該当するかを、ID プレフィックス（
   [quality-knowledge-schema.md §1.2](../../docs/quality-models/quality-knowledge-schema.md#12-id-体系と既存データ契約との対応)、
   [test-process-research-summary-test-design.md §6.1 基本ID体系](../../docs/test-techniques/test-process-research-summary-test-design.md#61-基本-id-体系)）
   から分類する。存在しなければ「上流成果物なし時の振る舞い」に従う。
2. **ID 体系不明な成果物の切り分け（必須）**: 既知のプレフィックス（`REQ-`/
   `RISK-`/`HTC-`/`DTC-`/`TAE-`/`COV-`/`TC-`/`TPR-`/`RUN-`/`BUG-` 等）に
   一致しない ID・参照を持つ成果物は、内容を推測せず**「未接続」として
   報告する**。無視して読み飛ばしてはならない。
3. **フォワードトレースの実施**: [test-process-research-summary-test-design.md §7.1
   最低限のトレースチェーン](../../docs/test-techniques/test-process-research-summary-test-design.md#71-最低限のトレースチェーン)
   の順（REQ→HTC→DTC→TAE→COV→TC→TPR→RUN→DEC、および RISK→DTC/TAE/COV）
   に従い、各ノードから下流ノードへのリンクが存在するかを検査する。下流
   リンクを持たないノード（例: どの HTC からも参照されない REQ）を
   `unreached_downstream` として一覧化する。
4. **バックワードトレースの実施**: 同チェーンを逆方向にたどり、各ノードが
   上流ノードへのリンク（`source_refs`・`risk_refs`・`condition_id`・
   `architecture_element_id`・`coverage_item_refs` 等、
   [同 §7.2 トレース項目](../../docs/test-techniques/test-process-research-summary-test-design.md#72-トレース項目)
   参照）を持つかを検査する。上流リンクが空・欠落しているノード（例:
   `source_refs` が空の DTC）を `missing_upstream_link` として一覧化し、
   [quality-knowledge-schema.md §1.5（チェーンが切れていると何が言えなく
   なるか）](../../docs/quality-models/quality-knowledge-schema.md#15-チェーンが切れていると何が言えなくなるか)
   の表を用いて、その欠落によって何が言えなくなるか（例: 「なぜこの
   DTC が存在するのか説明できない」）を1文で添える。
5. **未接続ノードの統合報告（必須）**: 手順3・4の結果を統合し、フォワード
   起因・バックワード起因を区別せず「未接続ノード一覧」として
   `TraceabilityMatrix` の `disconnected_nodes` にまとめる。多対多関係
   （[同 §1.4 の関係表](../../docs/quality-models/quality-knowledge-schema.md#14-ノード間関係と双方向トレース)）
   を前提とするため、「1対1で紐づくはず」という仮定で誤検出しないよう、
   1ノードが複数リンクを持つ・複数ノードが1リンクを共有するケースを
   正常とみなす。
6. **テスト空間3軸マトリクスの生成（必須）**: [matrix-template.yaml](../../knowledge/test-space/matrix-template.yaml)
   の `axes`（`test_level`／`test_type`／`test_process`）を軸とし、収集
   できた成果物の `test_level`・`test_type`・`test_process` 相当の属性
   （TAE の `test_level`/`test_type`、成果物の出所フェーズ等）からセルを
   埋める。各セルは `{status: covered|partial|none, evidence: [ID, ...],
   notes}` 形式（[knowledge-management-design.md §6.3](../../docs/agent-ecosystem/knowledge-management-design.md#63-セル形式とマトリクステンプレートyaml)）
   に従う。`test_space_scope_hint` があれば該当軸を優先的に埋める。
   探索的テストのチャーターを証跡に使う場合は `CHT-` プレフィックス
   （例: `CHT-C07`）で参照する。
7. **Markdown ヒート表への描画（必須）**: 手順6のセルデータを、`test_level`
   を行、`test_type` を列とした小さな Markdown 表に描画し、セル内に
   `status` を絵文字や記号ではなく `covered`/`partial`/`none` の文字列
   そのままで表示する（プラットフォーム非依存のため）。1軸に収まりきら
   ない場合は `test_process` ごとに表を分割してよい。CSV エクスポート
   （同じ行×列構造をカンマ区切りで併記したもの）も出力に含める。
8. **レビュー観点での自己点検**: 検出結果を
   [quality-knowledge-schema.md §1.4/§1.5](../../docs/quality-models/quality-knowledge-schema.md#14-ノード間関係と双方向トレース)
   （多対多を誤って1対1と扱っていないか、フォワード・バックワード両方向
   を検査したか）に照らして自己点検する。詳細な参照ポインタは
   [references/trace-checklist.md](references/trace-checklist.md) を用いる。

## 最小入力契約

コールドスタート（他スキルの成果物が一切ない状態）で本スキルを起動するために
最低限必要な入力は次の1つのみである。

- **対象機能の説明文**（`feature_summary`）: 何のトレースチェーンを検査したい
  かが分かる1〜3文

`artifact_bundle_ref`・`test_space_scope_hint` はいずれも任意であり、
与えられなくても起動・出力可能である。

## 上流成果物なし時の振る舞い

検査対象となる成果物（REQ〜TC の ID 参照群）が一切存在しない場合、次の
手順で分析を継続する。

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) どの工程まで成果物が揃っているか（TRA/TAD/TDD-TI のどこまでか）、
   (b) 成果物の形式（Markdown/JSON/CSV のどれか）、(c) 優先確認したいテスト
   空間の軸があるか、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、`feature_summary`
   の記述から「検査対象の成果物が存在しない」こと自体を `TraceabilityMatrix`
   の結論として**必ず出力する**（無出力にはしない）。全ノードを
   `disconnected_nodes` として報告し、テスト空間3軸マトリクスは全セル
   `status: none` の空テンプレートとして出力する。
3. この場合の結果には `assumption: true` を付与し、「成果物が一切提供され
   なかったため、全ノードを未接続として報告した」ことを `assumptions` に
   明記する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。`TraceabilityMatrix` と `TestSpaceMatrix` はいずれも
専用の JSON Schema が Phase 1 時点で存在しないため、`schema_ref` には
出力データの定義箇所へのポインタを指定する（`TraceabilityMatrix` は
[test-process-research-summary-test-design.md §7 トレーサビリティ](../../docs/test-techniques/test-process-research-summary-test-design.md#7-トレーサビリティ)、
`TestSpaceMatrix` は [matrix-template.yaml](../../knowledge/test-space/matrix-template.yaml)）。

例は既存スキル群の題材（REQ-012/REQ-042 → RISK-001/004 → HTC-001/002 →
DTC-001/002 → TAE-001/002 → COV-001/002 → TC-001/002）を引き継ぎ、加えて
`test-requirement-analysis` 側で新規に追加された **`DTC-003`（`source_refs`
が空で、どの REQ からも辿れない）** を未接続の例として含める。

```json
{
  "source_skill": "traceability-management",
  "phase": "traceability",
  "artifacts": [
    {
      "type": "TraceabilityMatrix",
      "schema_ref": "docs/test-techniques/test-process-research-summary-test-design.md#7-トレーサビリティ",
      "content": {
        "chain_links": [
          { "from": "REQ-012", "to": "HTC-001", "direction": "forward" },
          { "from": "HTC-001", "to": "DTC-001", "direction": "forward" },
          { "from": "RISK-004", "to": "DTC-001", "direction": "forward" },
          { "from": "DTC-001", "to": "TAE-001", "direction": "forward" },
          { "from": "TAE-001", "to": "COV-001", "direction": "forward" },
          { "from": "COV-001", "to": "TC-001", "direction": "forward" },
          { "from": "REQ-042", "to": "HTC-002", "direction": "forward" },
          { "from": "HTC-002", "to": "DTC-002", "direction": "forward" },
          { "from": "DTC-002", "to": "TAE-002", "direction": "forward" },
          { "from": "TAE-002", "to": "COV-002", "direction": "forward" },
          { "from": "COV-002", "to": "TC-002", "direction": "forward" }
        ],
        "disconnected_nodes": [
          {
            "id": "DTC-003",
            "node_type": "DTC",
            "reason": "missing_upstream_link",
            "detail": "source_refs が空であり、どの REQ からも辿れない（バックワードトレース失敗）。quality-knowledge-schema.md §1.5 に照らすと、この DTC がなぜ存在するのかを説明できない状態にある",
            "detected_by": "backward"
          }
        ],
        "unreached_downstream": []
      }
    },
    {
      "type": "TestSpaceMatrix",
      "schema_ref": "knowledge/test-space/matrix-template.yaml",
      "content": {
        "heat_table_markdown": "| test_level \\ test_type | functional-suitability | security |\n| --- | --- | --- |\n| component | covered | none |\n| system | partial | covered |\n| acceptance | none | none |\n",
        "cells": [
          {
            "test_level": "component",
            "test_type": "functional-suitability",
            "test_process": "TDD-TI",
            "status": "covered",
            "evidence": ["TC-001", "TC-002"],
            "notes": "カード番号桁数チェックの境界値をコンポーネントレベルで確認済み"
          },
          {
            "test_level": "system",
            "test_type": "functional-suitability",
            "test_process": "TDD-TI",
            "status": "partial",
            "evidence": ["TAE-002"],
            "notes": "タイムアウト時の二重課金防止はTAEレベルまで割当済みだが、TC未生成"
          },
          {
            "test_level": "system",
            "test_type": "security",
            "test_process": "TRA",
            "status": "covered",
            "evidence": ["RISK-004"],
            "notes": "カード番号関連のセキュリティリスクをTRA段階で識別済み"
          },
          {
            "test_level": "component",
            "test_type": "security",
            "test_process": "TDD-TI",
            "status": "none",
            "evidence": [],
            "notes": "コンポーネントレベルのセキュリティテストは未着手"
          },
          {
            "test_level": "acceptance",
            "test_type": "functional-suitability",
            "test_process": "TE",
            "status": "none",
            "evidence": [],
            "notes": "受入レベルの実行結果が未収集"
          },
          {
            "test_level": "acceptance",
            "test_type": "security",
            "test_process": "TE",
            "status": "none",
            "evidence": [],
            "notes": "受入レベルの実行結果が未収集"
          }
        ],
        "csv_export": "test_level,test_type,test_process,status,evidence,notes\ncomponent,functional-suitability,TDD-TI,covered,\"TC-001;TC-002\",カード番号桁数チェックの境界値をコンポーネントレベルで確認済み\nsystem,functional-suitability,TDD-TI,partial,TAE-002,タイムアウト時の二重課金防止はTAEレベルまで割当済みだが、TC未生成\nsystem,security,TRA,covered,RISK-004,カード番号関連のセキュリティリスクをTRA段階で識別済み\ncomponent,security,TDD-TI,none,,コンポーネントレベルのセキュリティテストは未着手\nacceptance,functional-suitability,TE,none,,受入レベルの実行結果が未収集\nacceptance,security,TE,none,,受入レベルの実行結果が未収集\n"
      }
    }
  ],
  "trace_ids": ["REQ-012", "REQ-042", "RISK-001", "RISK-004", "HTC-001", "HTC-002", "DTC-001", "DTC-002", "DTC-003", "TAE-001", "TAE-002", "COV-001", "COV-002", "TC-001", "TC-002"],
  "assumptions": [
    "DTC-003 は test-requirement-analysis 側の成果物に含まれていた項目で、本スキルはその内容を推測せず未接続として報告するに留めた"
  ],
  "open_questions": [
    "DTC-003 は REQ-012/REQ-042 のいずれかの派生条件か、それとも別要求から作られるべきか"
  ],
  "gate_status": "blocked"
}
```

`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれかを
とる。`disconnected_nodes` が1件でも存在する場合は `blocked` とし、後続の
`quality-gate-release-judgment` への引き渡しを保留する。未接続ノードが
ゼロで `unreached_downstream` のみ残る（下流展開が未着手なだけ）場合は
`passed-with-risks` とする。
