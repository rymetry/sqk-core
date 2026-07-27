---
name: test-execution-support
description: >
  「このテストスイートを実行した結果をまとめてほしい」「このテスト、
  たまに落ちるので flaky かどうか切り分けたい」のように、テスト実行の
  結果ログを整理・トリアージする必要があるときに使う。実行ログ（CI ログ・
  テストランナー出力等）を材料に、実行単位ごとの結果記録
  `TestExecutionLog`（RUN-nnn）と欠陥候補一覧・flaky 判定結果を生成し、
  再テスト・回帰テストの推奨範囲を出力する。テストの実行そのものは
  行わない（実行系が担う）。テストケース定義が無くても実行ログのみで
  起動できる。
version: 0.1.1
inputs:
  execution_context_summary:
    type: string
    required: true
    description: >
      何のテスト実行結果を、何の目的で扱うか（結果整理か flaky 切り分けか
      再テスト選定か）の1〜3文（実行ログが1件も無い場合の唯一の必須入力）
  execution_log_ref:
    type: path
    required: false
    description: >
      実行ログへの参照（CI ログ、テストランナー出力、JUnit XML 等。
      複数ファイル・複数実行回分をまとめて渡してよい。flaky 切り分けには
      同一テストの複数実行回分があることが望ましい）
  test_case_bundle_ref:
    type: path
    required: false
    description: >
      テストケース定義（TC）・テストプロシジャー・上流ハンドオフ
      エンベロープ群への参照。無い場合はログから実行単位を逆推定する
  environment_info:
    type: string
    required: false
    description: 実行環境・テスト対象ビルド/バージョンの概要
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  test_execution_log:
    schema: ../../schemas/test-execution-log.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/test-techniques/test-process-research-summary-test-design.md
  - docs/test-techniques/testing-standards-and-assurance-concepts.md
---

# test-execution-support

Tester Skillspace 4象限: テスト技法（中）／ドメイン（軽）／ITスキル
（重、CI・ログ解析）／コミュニケーション（軽）。

## 目的

テスト実行の結果ログを [test-process-research-summary-test-design.md §4.8（テスト実行）](../../docs/test-techniques/test-process-research-summary-test-design.md#48-7-テスト実行te)
のタスク定義（実結果の記録、期待結果との比較、不一致・不正・ブロック・
未実行の分類、欠陥候補の分析）に従って整理し、実行単位ごとの
`TestExecutionLog`（RUN-nnn）・欠陥候補一覧・flaky 判定結果を出力する。
あわせて [§4.9（再テスト・回帰テスト）](../../docs/test-techniques/test-process-research-summary-test-design.md#49-8-再テスト回帰テスト)
に従い、修正確認の再テストと回帰テストの推奨範囲を出力する。

**実行境界（必読）**: 本スキルはテストを実行しない。実行と証跡収集は
実行系（veridia 等）が担い、本スキルはその結果ログを入力とする後処理の
ブループリントである（[DECISIONS.md D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)
の実行境界）。出力する `RUN-nnn` は skill-handoff の知識成果物であり、
実行系の runtime evidence 契約ではない。

## 手順

1. **入力の分類とエントリ確認**: `execution_log_ref` のログ、
   `test_case_bundle_ref` の TC 定義・上流エンベロープ、`environment_info`
   を分類する（[§4.8 タスク1](../../docs/test-techniques/test-process-research-summary-test-design.md#48-7-テスト実行te)）。
   ログが複数実行回分あるか（flaky 判定の材料）をここで確認する。
2. **RUN 記録の生成**: ログの実行単位ごとに
   [schemas/test-execution-log.schema.json](../../schemas/test-execution-log.schema.json)
   準拠のレコード（`RUN-nnn`）を生成する。実結果を記録し、期待結果と
   比較し（§4.8 タスク3〜4）、`verdict` を pass / fail / invalid /
   blocked / not-run に分類する（§4.8 タスク5）。blocked / not-run には
   理由を `detail` に残す（§4.8 完了条件）。同一テストの rerun（自動
   再実行を含む）は原則として独立の RUN として記録する（flaky 判定は
   複数 RUN の `verdict` 比較を前提とするため）。個別詳細のない連続
   rerun は1レコードに集約してよく、その場合は集約した旨を
   `assumptions[]` に記録する。期待値が未確定（仕様裁定待ち等）で合否を
   判定できない実行は invalid に分類し、理由と裁定後の再判定条件を
   `detail` に残す。TC 定義がある場合は
   `test_case_refs` で TC-/TPR- に紐付ける。**TC 定義が無い場合は
   ログからケース相当を逆推定し、`test_case_refs` は空配列のまま
   レコードをスキーマ準拠に保ち、逆推定の前提をエンベロープ
   `assumptions[]` に `{field,value,reason}` 形式で記録する**（item に
   assumption フィールドを足さない）。
3. **flaky トリアージ**: 同一テスト（同一 TC または同一テスト名）の
   複数 RUN で `verdict` が合格・不合格の両方を示すものを flaky 候補と
   してマークし、[testing-standards-and-assurance-concepts.md §6](../../docs/test-techniques/testing-standards-and-assurance-concepts.md#6-flaky-test-非決定的テストの管理)
   の原因分類（async wait・並行性・テスト順序依存 等の10カテゴリ）に
   照らして原因仮説を付す。切り分け原則も同 §6 に従う: 再実行は切り分け
   手段であり恒久対策ではない、隔離（quarantine）には修復期限を必ず
   併設する、CI でのみ flaky になるケースがある（ローカル再実行での
   非再現は flaky の否定にならない）。実行単位として復元できないログ内の
   過去実行履歴（コメント行・要約行等）は RUN 化せず、flaky 判定の補助
   証拠として引用し、その信頼性の前提を `assumptions[]` に記録する。
   **単一実行回分のログしか無い場合は
   flaky 判定を行わず、「再実行情報が無く判定不能」を `open_questions`
   に記録する**（単発の fail を flaky と断定しない）。
4. **欠陥候補の抽出**: `verdict` が fail / invalid の RUN から欠陥候補
   一覧（`DefectCandidateList`）を作る（§4.8 タスク6）。各候補には
   再現に必要な情報（対象 RUN、実結果、環境、再現手順の所在）を含める
   （§4.8 完了条件「欠陥票が再現可能な情報を持っている」）。欠陥票の
   起票そのもの（BUG-nnn の採番・登録）は行わず、起票先の判断は利用者・
   実行系に委ねる。flaky 候補と判定したものは欠陥候補と区別して報告する
   （flaky はプロダクト欠陥ではなくテスト資産の欠陥である可能性が高い）。
5. **再テスト・回帰テストの推奨**: [§4.9](../../docs/test-techniques/test-process-research-summary-test-design.md#49-8-再テスト回帰テスト)
   に従い、(a) 欠陥候補ごとの修正確認再テスト（該当 TC の再実行）、
   (b) 変更影響範囲に基づく回帰テストの推奨範囲を `RegressionAdvice`
   として出力する。変更差分・影響範囲の情報が入力に無い場合に出さない
   のは (b) の回帰テスト推奨範囲のみであり、(a) の修正確認再テストは
   欠陥候補から導出して出力する。(b) を出せない場合は必要な情報を
   `open_questions` に記録する。
6. **エンベロープ出力**: 「出力エンベロープ」節の形式で出力する。
   `trace_ids` には参照した TC-/TPR- と生成した RUN- を列挙する。
   `gate_status` は、ログを1件も読めなかった場合のみ `blocked`、
   逆推定・判定不能・欠陥候補が残る場合は `passed-with-risks`、
   全 RUN が pass で残存疑問が無い場合は `passed` とする。

## 最小入力契約

コールドスタート（実行ログ・上流成果物が一切ない状態）で本スキルを
起動するために最低限必要な入力は次の1つのみである。

- **実行結果の説明**（`execution_context_summary`）: 何のテスト実行
  結果を何の目的で扱うかが分かる1〜3文

`execution_log_ref`・`test_case_bundle_ref`・`environment_info` は
いずれも任意であり、与えられなくても起動・出力可能である。

## 上流成果物なし時の振る舞い

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) 実行ログはどこにあるか（CI の URL・ファイルパス等）、
   (b) テストケース定義（TC）はあるか、
   (c) 目的は結果整理・flaky 切り分け・再テスト選定のどれか、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合でも、必ず出力する。
   実行ログが1件も無い場合は「実行ログ欠落」を理由に
   `gate_status: blocked` を返す（ログなしでの結果整理・flaky 判定は
   出さない。実行の代行もしない）。
3. 実行ログのみがある場合（TC 定義なし）は、手順2の逆推定で RUN 記録を
   生成して継続し、逆推定の前提を `assumptions[]` に記録する。
   判定できなかった事項は `open_questions` に **unknown** として明示する。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。

```json
{
  "source_skill": "test-execution-support",
  "phase": "test-execution",
  "artifacts": [
    {
      "type": "TestExecutionLog",
      "schema_ref": "schemas/test-execution-log.schema.json",
      "items": [
        {
          "id": "RUN-001",
          "test_case_refs": ["TC-001"],
          "verdict": "pass",
          "actual_result": "15桁のカード番号が 400 応答で拒否された",
          "executed_at": "2026-07-27T10:00:00+09:00",
          "log_ref": "ci/run-4512/junit.xml"
        },
        {
          "id": "RUN-002",
          "test_case_refs": [],
          "verdict": "fail",
          "actual_result": "timeout_retry_spec がリトライ3回後に 504 で失敗",
          "detail": "TC 定義が無いためログのテスト名から実行単位を逆推定した",
          "executed_at": "2026-07-27T10:05:12+09:00"
        }
      ]
    },
    {
      "type": "DefectCandidateList",
      "schema_ref": "skills/test-execution-support/SKILL.md",
      "content": {
        "candidates": [
          {
            "run_ref": "RUN-002",
            "summary": "タイムアウト後のリトライ回数超過時に 504 が返る（仕様の期待は 503）",
            "reproduction": "ci/run-4512 のログ参照。staging / build 1.4.2"
          }
        ]
      }
    },
    {
      "type": "FlakyTriageReport",
      "schema_ref": "skills/test-execution-support/SKILL.md",
      "content": {
        "flaky_candidates": [],
        "not_assessable": ["単一実行回分のログのみのため flaky 判定は未実施"]
      }
    }
  ],
  "trace_ids": ["TC-001", "RUN-001", "RUN-002"],
  "assumptions": [
    {
      "field": "test_case_refs",
      "value": "[]",
      "reason": "RUN-002 は TC 定義が入手できず、CI ログのテスト名 timeout_retry_spec から実行単位を逆推定した"
    }
  ],
  "open_questions": [
    "timeout_retry_spec に対応する TC 定義・期待結果の正典はどこにあるか",
    "flaky 切り分けに使える複数実行回分のログは入手可能か"
  ],
  "gate_status": "passed-with-risks"
}
```

`DefectCandidateList`・`FlakyTriageReport`・`RegressionAdvice` は ID 体系を
持たない助言的成果物のため専用スキーマを設けず `content` に置く
（[schemas/README.md の content/items 使い分け](../../schemas/README.md)）。
`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれか
をとる（判定規則は手順6）。
