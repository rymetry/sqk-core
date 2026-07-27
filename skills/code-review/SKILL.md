---
name: code-review
description: >
  「この PR をレビューしてほしい」「静的解析の指摘を優先度付けして
  ほしい」のように、コード差分の構造化レビューや静的解析結果の解釈が
  必要なときに使う。差分（diff）と（あれば）静的解析結果を材料に、
  正確性／セキュリティ／保守性の3観点で、重大度
  （blocker/major/minor/info）と根拠付きの所見リストと修正提案を
  生成する。静的解析結果が無い場合は目視レビューのみで実施し、
  その旨を出力に必ず明記する。diff のみで起動できる。レビューボットの
  CI 組み込み・静的解析の実行・修正の適用は行わない（実行系が担う）。
version: 0.1.0
inputs:
  review_target_summary:
    type: string
    required: true
    description: >
      何の変更を、何の目的でレビューするか（マージ判断か指摘の
      優先度付けか）の1〜3文（diff が入手できない場合の唯一の必須入力）
  diff_ref:
    type: path
    required: false
    description: >
      レビュー対象の差分への参照（unified diff・PR のファイル群等。
      複数ファイルをまとめて渡してよい）。変更説明（コミットメッセージ・
      PR 説明）があれば併せて渡すことが望ましい
  static_analysis_ref:
    type: path
    required: false
    description: >
      静的解析・セキュリティスキャンの結果への参照（SAST・SCA・lint
      レポート等）。無い場合は目視レビューのみで実施する
  context_bundle_ref:
    type: path
    required: false
    description: >
      変更周辺のコード・設計文書・コーディング規約・上流ハンドオフ
      エンベロープ群への参照（変更理解の補助材料）
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-management/code-review-techniques.md
  - docs/secure-development/secure-development-and-supply-chain.md
  - docs/quality-management/software-quality-management-practical-reference.md
---

# code-review

Tester Skillspace 4象限: テスト技法（軽）／ドメイン（中）／ITスキル
（重、コード・アーキテクチャ理解）／コミュニケーション（レビュー
コメントの書き方、最重）。

## 目的

コード差分を [code-review-techniques.md](../../docs/quality-management/code-review-techniques.md)
のレビュー体系に従って構造化レビューし、**正確性・セキュリティ・
保守性**の3観点（[同 §3](../../docs/quality-management/code-review-techniques.md#3-レビュー観点の構造化--正確性セキュリティ保守性)）
で重大度・根拠付きの所見リストと修正提案を返す。静的解析結果が
与えられた場合は、生の指摘リストではなくトリアージ
（[同 §4](../../docs/quality-management/code-review-techniques.md#4-静的解析結果の解釈)）
を経た所見として統合する。

役割分担: 仕様・非機能要求のレビューは nfr-review、テスト設計成果物の
メタレビューは quality-artifact-review、リスクの洗い出し・優先度付けは
risk-analysis が担い、本スキルは代行しない。本スキルの固有の責務は
**コード差分を対象とした所見の構造化（観点×重大度×根拠）と、受け手が
行動できるレビューコメントへの変換**である。

**実行境界（必読）**: 本スキルはレビューの手順・観点・出力契約の
ブループリントであり、レビューボットの CI 組み込み・静的解析ツールの
実行・修正の適用・マージ操作は実行系（veridia 等）が担う
（[DECISIONS.md D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)
の実行境界）。静的解析結果は本スキルが生成するものではなく、実行系が
実行した結果を入力として受け取る。

## 手順

1. **入力の分類と確認範囲の宣言**: `diff_ref` の差分、
   `static_analysis_ref` の解析結果、`context_bundle_ref` の周辺
   コンテキストを分類し、**何を入力として何を確認するか（diff のみか・
   周辺コード込みか・静的解析結果の有無）を先に確定する**
   （[code-review-techniques.md §7](../../docs/quality-management/code-review-techniques.md#7-ai-エージェントによるレビューの適用境界)）。
   `static_analysis_ref` が無い場合、本レビューは目視レビューのみであり
   構文パターン系欠陥の網羅性を持たないこと（[同 §4.4](../../docs/quality-management/code-review-techniques.md#44-人間または-aiレビューとの分担)
   の片翼欠如）を、この時点で出力予定の `ReviewScope` に記録する。
2. **変更の理解**: 変更の目的（何を達成する変更か）と影響範囲を、
   変更説明・diff 全体から把握する。変更理解がレビュー品質を律速する
   （[同 §2.2](../../docs/quality-management/code-review-techniques.md#22-何が実際に得られるか--期待と実態)）
   ため、目的が読み取れない場合はレビューを打ち切らず、目的の確認を
   `open_questions` に記録した上で読み取れた範囲でレビューする。
   diff が実証研究の推奨サイズ（400 行）を大きく超える場合は、分割
   提案自体を保守性の所見として出す（[同 §2.3](../../docs/quality-management/code-review-techniques.md#23-サイズと速度のガイドライン)）。
3. **観点別レビュー**: [同 §3](../../docs/quality-management/code-review-techniques.md#3-レビュー観点の構造化--正確性セキュリティ保守性)
   のチェックリストに従い、正確性・セキュリティ・保守性の3観点で
   diff を確認する。観点は変更の性質で重み付けする（認可・入力処理を
   触る変更はセキュリティ優先。セキュリティ観点の詳細は
   [secure-development-and-supply-chain.md](../../docs/secure-development/secure-development-and-supply-chain.md)
   を参照する）。3観点いずれも確認した事実を残し、所見ゼロの観点も
   「確認済み・所見なし」として `ReviewScope` に記録する（未確認と
   区別する）。lint・自動整形で検出できるスタイル指摘は出力しない
   （同 §3 運用原則3）。
4. **静的解析結果のトリアージ**（`static_analysis_ref` がある場合のみ）:
   [同 §4.2](../../docs/quality-management/code-review-techniques.md#42-トリアージの手順)
   の手順（真偽判定 → 該当性判定 → 優先度付け → ベースライン分離）で
   指摘を削減・順位付けし、残った指摘を所見リストへ統合する。
   セキュリティ指摘の優先度は CVSS を基礎に EPSS・KEV・到達可能性で
   補正する。diff 内の抑制コメント・ルール無効化の追加は、それ自体を
   所見対象とする（[同 §4.3](../../docs/quality-management/code-review-techniques.md#43-抑制の監査)）。
5. **重大度付けと根拠の必須化**: 各所見に
   [同 §5.1](../../docs/quality-management/code-review-techniques.md#51-重大度スキーム)
   の基準で blocker / major / minor / info を付す。すべての所見に
   該当箇所（ファイル・行）を付し、blocker / major には「どの入力・
   状態で何が起きるか」の失敗シナリオを必須とする。**該当行と失敗
   シナリオを構成できない指摘は断定せず、question（info）に格下げする
   か出力しない**（[同 §5.2](../../docs/quality-management/code-review-techniques.md#52-判定の軸と根拠の必須化)・
   [§7](../../docs/quality-management/code-review-techniques.md#7-ai-エージェントによるレビューの適用境界)
   の根拠必須の原則。適合率を網羅の演出より優先する）。
6. **修正提案とレビューコメントの生成**: 所見ごとに、
   [同 §6](../../docs/quality-management/code-review-techniques.md#6-レビューコメントの書き方)
   の作法（コードについて述べる・理由を説明する・重要度を明示する）で
   受け手に渡せるコメント文を生成する。ラベルは Conventional Comments
   形式（issue / suggestion / question / nitpick / praise 等＋
   blocking / non-blocking）を使い、重大度との対応（issue (blocking)=
   blocker・major、suggestion (non-blocking)・nitpick=minor、praise /
   thought / question=info）を守る。修正提案は可能な限り具体的な代替
   （コード断片・既存実装への参照）を添え、設計判断が分かれる論点は
   選択肢とトレードオフの提示に留める。よい設計判断への praise も
   所見（info）として含める。
7. **エンベロープ出力**: 「出力エンベロープ」節の形式で出力する。
   `gate_status` は、diff を一切読めなかった場合と blocker 所見が残る
   場合は `blocked`、major 所見が残る（またはリスク受容の記録を条件に
   許容する）場合は `passed-with-risks`、minor / info のみの場合は
   `passed` とする（[同 §5.1](../../docs/quality-management/code-review-techniques.md#51-重大度スキーム)
   のマージ影響、および severity→gate_status 導出の repo 内規約
   （quality-artifact-review と同型）に従う）。

## 最小入力契約

コールドスタート（diff・静的解析結果が一切ない状態）で本スキルを
起動するために最低限必要な入力は次の1つのみである。

- **レビュー対象の説明**（`review_target_summary`）: 何の変更を何の
  目的でレビューするかが分かる1〜3文

`diff_ref`・`static_analysis_ref`・`context_bundle_ref` はいずれも
任意であり、与えられなくても起動・出力可能である。ただしレビュー
所見の生成には diff が必要である（無い場合の振る舞いは次節）。
**diff があれば静的解析結果が無くてもレビューは完全に実施できる**
（その場合は目視レビューのみである旨を必ず明記する）。

## 上流成果物なし時の振る舞い

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき
   質問は (a) レビュー対象の diff・PR はどこにあるか、(b) 静的解析・
   セキュリティスキャンの結果はあるか、(c) レビュー結果を何に使うか
   （マージ判断か、指摘の優先度付けか）、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、必ず出力する。
   diff が1件も無い場合は、`review_target_summary` から推定できる
   範囲の「レビューで確認すべき観点の一覧」のみを出し、所見の断定は
   せず `gate_status: blocked` を返す（コードを見ずにレビュー合格
   判定は出さない）。
3. diff はあるが変更説明・周辺コンテキストが無い場合は、diff 単体で
   レビューを実施した上で、変更目的を推定した旨を `assumptions[]` に
   `{field,value,reason}` 形式で記録し、確認できなかった事項
   （設計意図・影響範囲）を `open_questions` に明示する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。

```json
{
  "source_skill": "code-review",
  "phase": "code-review",
  "artifacts": [
    {
      "type": "ReviewScope",
      "schema_ref": "skills/code-review/SKILL.md",
      "content": {
        "inputs_reviewed": {
          "diff": true,
          "change_description": true,
          "surrounding_code": false,
          "static_analysis": false
        },
        "scope_note": "静的解析結果なし。本レビューは目視レビューのみであり、構文パターン系欠陥（危険 API・既知の脆弱パターン）の網羅性を持たない",
        "viewpoints_examined": [
          { "viewpoint": "correctness", "findings_count": 1 },
          { "viewpoint": "security", "findings_count": 1 },
          { "viewpoint": "maintainability", "findings_count": 1 }
        ]
      }
    },
    {
      "type": "CodeReviewFindingList",
      "schema_ref": "skills/code-review/SKILL.md",
      "content": {
        "findings": [
          {
            "viewpoint": "correctness",
            "severity": "major",
            "location": "src/billing/invoice.py:42",
            "statement": "quantity=0 のとき除算例外が発生する分岐が未処理",
            "failure_scenario": "数量 0 の明細を含む請求書で invoice 生成が例外終了し、バッチ全体が停止する",
            "evidence_ref": "code-review-techniques.md §3（エッジケース: 空・null・境界値）",
            "review_comment": "issue (blocking): この分岐は quantity=0 のとき除算例外になります。入力検証を追加するか、0 を仕様として扱う根拠をコメントで残してください。"
          },
          {
            "viewpoint": "maintainability",
            "severity": "minor",
            "location": "src/billing/invoice.py:88-104",
            "statement": "金額正規化の処理が utils/normalize の既存実装と重複",
            "failure_scenario": null,
            "evidence_ref": "code-review-techniques.md §3（重複: 既存実装の再利用可否）",
            "review_comment": "suggestion (non-blocking): この変換は utils/normalize に既存実装があります。再利用すると差分が小さくなります。"
          }
        ]
      }
    }
  ],
  "trace_ids": [],
  "assumptions": [
    {
      "field": "change_purpose",
      "value": "請求書生成の数量割引対応（PR 説明より）",
      "reason": "設計文書は未入手のため、変更目的は PR 説明の記載範囲でのみ判定した"
    }
  ],
  "open_questions": [
    "数量 0 の明細は仕様上あり得るか（上流バリデーションの有無）"
  ],
  "gate_status": "passed-with-risks"
}
```

`ReviewScope`・`CodeReviewFindingList` は ID 体系を持たない助言的
成果物のため専用スキーマを設けず `content` に置く（[schemas/README.md
の content/items 使い分け](../../schemas/README.md)）。`ReviewScope`
（確認範囲の宣言。静的解析の有無を含む）は**入力構成にかかわらず必須**
で出力する。所見の `severity` は blocker / major / minor / info の
4値（[code-review-techniques.md §5.1](../../docs/quality-management/code-review-techniques.md#51-重大度スキーム)）、
`viewpoint` は correctness / security / maintainability の3値を
とる。blocker / major の所見は `failure_scenario` を null にしない。
`trace_ids` は、上流成果物（TC・RISK 等）との紐付けが入力に含まれる
場合のみ当該 ID を列挙し、diff 単体レビューでは空配列とする。
`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値の
いずれかをとる（判定規則は手順7）。

## 関連ドキュメント

- [code-review-techniques.md](../../docs/quality-management/code-review-techniques.md) — レビュー体系・静的解析結果の解釈・重大度付け・コメント作法の主参照
- [secure-development-and-supply-chain.md](../../docs/secure-development/secure-development-and-supply-chain.md) — セキュリティ観点・SAST/DAST/SCA 特性・セキュリティゲート
- [software-quality-management-practical-reference.md](../../docs/quality-management/software-quality-management-practical-reference.md) — IEEE 1028 系レビュー体系の位置づけ・品質ゲート運用
