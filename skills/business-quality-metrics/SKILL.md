---
name: business-quality-metrics
description: >
  「品質指標とチャーン率の関係を分析してほしい」「NPS の低下が品質起因か
  切り分けたい」「品質投資を経営指標で説明したい」のように、事業指標
  （VOC・NPS・チャーン・LTV）と品質シグナルの関係の分析設計が必要な
  ときに使う。分析目的と（あれば）品質メトリクス・事業指標のデータ参照を
  材料に、GQM（Goal-Question-Metric）構造、指標選定（`MET-nnn` 提案を
  含む）、ラグ・コホート・交絡を設計した相関分析計画、および相関分析
  所見を出力する。**相関・関連までを主張し、因果は主張しない**（因果を
  確かめたい場合は介入設計の提案に留める）。分析目的の説明のみで起動
  でき、データが無い場合は GQM 構造と必要データ一覧の提示に留める。
  データ収集・分析の実行・ダッシュボード構築は行わない（実行系・分析
  基盤が担う）。
version: 0.1.0
inputs:
  analysis_goal_summary:
    type: string
    required: true
    description: >
      何を（どの品質シグナルとどの事業指標の関係を）、何の目的で
      （品質退行の検知か、品質投資の説明か、解約要因の切り分けか）
      分析するかの1〜3文（データが入手できない場合の唯一の必須入力）
  quality_metrics_ref:
    type: path
    required: false
    description: >
      品質シグナル側のデータ・定義への参照（欠陥密度・SLO 違反時間・
      クラッシュ率・MON-nnn 定義等。系列データでも集計値でもよい）
  business_metrics_ref:
    type: path
    required: false
    description: >
      事業指標側のデータ・定義への参照（NPS 推移・コホート別解約率・
      LTV 推計・VOC 分類等）。無い場合は枠組み提示に留める
  context_events_ref:
    type: path
    required: false
    description: >
      分析期間の交絡イベント記録（リリース履歴・価格改定・営業施策・
      障害・季節性等）への参照。相関所見の交絡併記に使う
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-management/business-quality-metrics-methods.md
  - docs/quality-management/quality-metrics-pitfalls.md
  - docs/quality-management/software-quality-management-practical-reference.md
  - docs/human-centered-quality/accessibility-ux-human-centered-quality.md
---

# business-quality-metrics

Tester Skillspace 4象限: テスト技法（軽）／ドメイン（重、事業指標の
文脈理解）／ITスキル（中、データ分析設計）／コミュニケーション（重、
経営層への説明）。

## 目的

分析目的を
[business-quality-metrics-methods.md](../../docs/quality-management/business-quality-metrics-methods.md)
の手法（VOC §2・NPS §3・チャーン §4・LTV §5）に基づいて GQM
（Goal-Question-Metric）構造へ展開し、**品質シグナルと事業指標の相関
分析の設計と所見**を返す。所見の語彙は「相関」「関連」「時間的先行」
までとし、**因果は主張しない**（[同 §6](../../docs/quality-management/business-quality-metrics-methods.md#6-品質シグナルとの相関分析--gqm-で設計する)
の分析原則5。因果を確かめたい場合は介入設計——A/B テスト・段階的
ロールアウト——の提案として返す）。

役割分担: 品質シグナル側（SLI/SLO・`MON-nnn`）の設計は
sre-quality-ops、メトリクスの目標化・ゲーミング対策の正典は
[quality-metrics-pitfalls.md](../../docs/quality-management/quality-metrics-pitfalls.md)、
UX 質問紙（SUS/CSAT）の運用は
[accessibility-ux-human-centered-quality.md](../../docs/human-centered-quality/accessibility-ux-human-centered-quality.md)
が担う。本スキルの固有の責務は**事業指標と品質シグナルを GQM で接続し、
飛躍（因果の断定・平均値の外挿）のない相関所見へ変換すること**である。

**実行境界（必読）**: 本スキルは分析設計と所見解釈のブループリントで
あり、データ収集・統計処理の実行・ダッシュボード構築・経営判断は
実行系・分析基盤・人間が担う
（[DECISIONS.md D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)
の実行境界）。実データ（自社の NPS 実測値・解約率・顧客データ）は
動的ナレッジであり、本リポジトリにもスキル出力の例にも含めない。
確定的な経営判断（価格・投資・撤退）の根拠には人間の検証を必須とする。

## 手順

1. **入力の分類とモード判定**: `analysis_goal_summary` とデータ参照の
   有無から、(a) 枠組み提示モード（データなし。GQM 構造と必要データ
   一覧まで）、(b) 分析設計モード（定義はあるが系列データが不足）、
   (c) 相関所見モード（品質・事業の両系列あり）、のいずれかを判定する。
2. **GQM 構造の展開**: 分析目的を Goal（目的・対象・視点・環境）→
   Question → Metric の3層に展開する
   （[business-quality-metrics-methods.md §6](../../docs/quality-management/business-quality-metrics-methods.md#6-品質シグナルとの相関分析--gqm-で設計する)
   の構造例に従う）。Metric 層では、品質シグナル側（欠陥密度・SLO
   違反・クラッシュ率等）と事業指標側（VOC 分類・NPS・コホート別
   チャーン・LTV）を対で選定し、不足する指標は `MET-nnn` の新規提案
   （[quality-knowledge-schema.md の MET 属性](../../docs/quality-models/quality-knowledge-schema.md)
   に従い `gaming_risk` を必須記載）として返す。
3. **指標の手法適合の確認**: 選定した事業指標ごとに、
   [同文書 §2〜§5](../../docs/quality-management/business-quality-metrics-methods.md)
   の手法水準と限界を適用する。
   - NPS: 単独 KPI にしない・遅行指標として扱う・測定条件固定
     （§3 の運用原則）。優位性主張には縦断研究の留保を併記する。
   - チャーン: コホートで見る・確率モデル（sBG 等）で射影する・
     契約型/非契約型を区別する（§4）。
   - LTV: 簡易式を使う場合は前提（一定マージン・一定リテンション）を
     明示し、非契約型は BG/NBD 系を指定する（§5）。
   - VOC: 手法水準（インタビュー件数・ニーズ階層化）を満たさない
     データを「VOC」として扱う場合はその旨を明記する（§2）。
4. **相関分析の設計**: 同 §6 の原則1〜4 に従い、(a) ラグ仮説と複数の
   時間窓、(b) コホート・セグメントの固定、(c) 交絡イベントの列挙
   （`context_events_ref` から。無い場合は確認すべき交絡の一覧を
   `open_questions` に出す）、(d) カウンターメトリクス、を設計する。
5. **相関所見の生成**（相関所見モードの場合）: 設計に沿って読み取れる
   関連（方向・強さの程度・時間的先行の有無）を、セル規模・不確かさを
   添えて記述する。**数十件規模のセルで係数を断定しない**（同 §7）。
   所見には必ず (a) 使ったモデル・前提、(b) 交絡の併記、(c) 「相関で
   あり因果ではない」の明示、を含める。因果に踏み込む必要がある場合は
   介入設計（A/B・段階的ロールアウト）の提案として分離する。
6. **エンベロープ出力**: 「出力エンベロープ」節の形式で出力する。
   `gate_status` は、分析目的が読み取れない場合のみ `blocked`、枠組み
   提示モード・分析設計モード（データ不足）または交絡未記録のまま
   所見を出した場合は `passed-with-risks`、両系列データ・交絡記録付きで
   設計と所見まで揃った場合は `passed` とする。

## 最小入力契約

コールドスタート（データ・指標定義が一切ない状態）で本スキルを起動する
ために最低限必要な入力は次の1つのみである。

- **分析目的の説明**（`analysis_goal_summary`）: どの関係を何の目的で
  分析するかが分かる1〜3文

`quality_metrics_ref`・`business_metrics_ref`・`context_events_ref` は
いずれも任意であり、与えられなくても起動・出力可能である。データが
無い場合は GQM 構造・`MET-nnn` 提案・必要データ一覧の提示（枠組み提示
モード）に留め、相関所見は出さない。

## 上流成果物なし時の振る舞い

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき
   質問は (a) ビジネスモデルは契約型（サブスクリプション）か非契約型
   （都度購入）か（チャーン・LTV のモデル選定に直結）、(b) 品質側・
   事業側でいま取れているデータは何か、(c) 分析結果を誰への何の説明に
   使うか（経営層への投資説明か、品質退行の検知運用か）、の3つに絞る。
   既に与えられた入力で無意味化した質問枠は、設計に最も効く別の質問へ
   再配分してよい（上限3件は維持する）。「最大3件」は利用者への対話的な
   確認質問の上限であり、`open_questions` に記録する未解決事項の件数には
   上限を設けない。
2. 回答が得られない場合でも、必ず出力する。ビジネスモデル不明の場合は
   契約型・非契約型の両方の設計を併記し、確定を `open_questions` に
   残す。
3. 推定した前提（ビジネスモデル・時間窓・コホート粒度等）は
   `assumptions[]` に `{field,value,reason}` 形式で記録する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。

```json
{
  "source_skill": "business-quality-metrics",
  "phase": "business-quality-metrics",
  "artifacts": [
    {
      "type": "GqmStructure",
      "schema_ref": "skills/business-quality-metrics/SKILL.md",
      "content": {
        "goal": "リリース品質の劣化が月次コホートの解約率へ与える影響を、SaaS プロダクトの品質責任者の視点で把握する",
        "questions": [
          {
            "question": "障害・SLO 違反に遭遇した顧客コホートは、遭遇しなかったコホートと残存曲線が異なるか",
            "metric_refs": ["MON-002", "MET-101", "MET-102"]
          },
          {
            "question": "解約理由の VOC 分類で、品質起因カテゴリの構成比はリリース品質の推移と連動しているか",
            "metric_refs": ["MET-103"]
          }
        ],
        "proposed_metrics": [
          {
            "id": "MET-101",
            "name": "障害遭遇コホート別 90 日残存率",
            "definition": "月次加入コホートを、加入後 90 日以内の障害遭遇（SLO 違反時間帯のアクティブ利用）有無で層別した残存率。sBG モデルで射影を併記する",
            "unit": "%",
            "target": null,
            "collection_point": "production",
            "qc_refs": [],
            "gaming_risk": "救済オファーによる引き留めが残存率を粉飾しうるため、救済オファー適用顧客を除外した系列を対で集計する"
          }
        ]
      }
    },
    {
      "type": "CorrelationAnalysisPlan",
      "schema_ref": "skills/business-quality-metrics/SKILL.md",
      "content": {
        "lag_windows_days": [30, 60, 90],
        "cohort_definition": "月次加入コホート、プラン別セグメント固定",
        "business_model": "contractual",
        "retention_model": "sBG",
        "confounders_recorded": ["4月の価格改定", "6月の大型競合リリース"],
        "counter_metrics": ["救済オファー除外残存率", "NPS 測定条件の監査ログ"]
      }
    },
    {
      "type": "CorrelationFindings",
      "schema_ref": "skills/business-quality-metrics/SKILL.md",
      "content": {
        "findings": [
          {
            "statement": "障害遭遇コホートは非遭遇コホートに対し 90 日残存率が低い傾向が3コホート連続で観察され、品質イベントが時間的に先行している。これは相関・関連の観察であり因果の主張ではない",
            "model_assumptions": "sBG（契約型・解約確率の Beta 異質性）を適用。コホートあたり数百件規模",
            "confounders_noted": "4月の価格改定が同時期に重なるため、価格改定前のコホートのみでも同方向の差を確認した",
            "causal_claim": false
          }
        ],
        "intervention_proposal": "因果を確かめる場合は、信頼性改善（リトライ導入）の段階的ロールアウトで遭遇率を操作し、残存率の差を比較する介入設計を推奨する"
      }
    }
  ],
  "trace_ids": ["MET-101", "MET-102", "MET-103", "MON-002"],
  "assumptions": [
    {
      "field": "metric_id_numbering",
      "value": "MET-101〜103 は仮採番",
      "reason": "既存の MET 台帳が入力に無く、確定採番は利用者側の指標台帳で行う"
    },
    {
      "field": "business_model",
      "value": "contractual",
      "reason": "月額サブスクリプションである旨が analysis_goal_summary に明記されていたため契約型モデル（sBG）を選定した"
    }
  ],
  "open_questions": [
    "解約理由の自由記述は VOC のニーズカテゴリ水準（階層化済み）か、未分類の生テキストか"
  ],
  "gate_status": "passed-with-risks"
}
```

`GqmStructure`・`CorrelationAnalysisPlan`・`CorrelationFindings` は ID
体系を持たない助言的成果物のため専用スキーマを設けず `content` に置く
（[schemas/README.md の content/items 使い分け](../../schemas/README.md)）。
`proposed_metrics` の各項目は
[quality-knowledge-schema.md の MET ノード属性](../../docs/quality-models/quality-knowledge-schema.md)
（`id`/`name`/`definition`/`unit`/`target`/`collection_point`/`qc_refs`/
`gaming_risk`）に従い、`gaming_risk` を必ず埋める。
`CorrelationFindings.findings[].causal_claim` は常に `false` とし、因果に
関する内容は `intervention_proposal`（介入設計の提案）へ分離する。
数値例・顧客データは出力例に含めない（動的ナレッジの排除。P5）。
`trace_ids` には提案した MET- と、入力に含まれる既存 ID（MON-・RISK-
等）を列挙する。`gate_status` は `passed` / `passed-with-risks` /
`blocked` の3値のいずれかをとる（判定規則は手順6）。

## 関連ドキュメント

- [business-quality-metrics-methods.md](../../docs/quality-management/business-quality-metrics-methods.md) — VOC・NPS・チャーン・LTV の手法と相関分析設計の主参照
- [quality-metrics-pitfalls.md](../../docs/quality-management/quality-metrics-pitfalls.md) — ゲーミング耐性・カウンターメトリクスの正典
- [software-quality-management-practical-reference.md](../../docs/quality-management/software-quality-management-practical-reference.md) — GQM の品質管理文脈・COQ
- [accessibility-ux-human-centered-quality.md](../../docs/human-centered-quality/accessibility-ux-human-centered-quality.md) — SUS/NPS/CSAT の質問紙運用・運用シグナル還流
