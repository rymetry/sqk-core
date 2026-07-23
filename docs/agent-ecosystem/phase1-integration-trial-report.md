> **v2 status**: final report — Phase 1 統合トライアルの完了報告（記録）。

# Phase 1 統合試行（T12）結果レポート

## 位置づけ

本書は [phase1-implementation-guide.md T12](./phase1-implementation-guide.md#t12-統合試行) の実行結果である。
[skill-ecosystem-design-plan.md](./skill-ecosystem-design-plan.md) の TRA→TAD→TDD/TI パイプラインを、
架空の決済 API 仕様書を題材に一気通しで実行した。

## 試行の設定

- **題材**: 架空の決済API仕様書（`payment-api-spec.md`、全10章）。カード番号桁数・決済金額の境界値、
  タイムアウト/リトライ仕様に加え、意図的な曖昧点・矛盾を3種5箇所埋め込んだ
  （曖昧点1: 未記載ブランドの桁数、矛盾1: 金額上限3章vs7章、曖昧点2: 冪等性キー未指定時挙動、
  矛盾2: エラー内部情報非開示vsデバッグヘッダ開示、曖昧点3: 本番でのデバッグ機能無効化方法）。
- **実行日**: 2026-07-07
- **実行形態**: 単一エージェント（本セッション）による、各スキルの SKILL.md 手順に忠実に従った
  ロールプレイ試行である。実際の Claude Code セッションでの `description` 自動発火・複数エージェント
  協調・対話的なユーザー応答は発生していない（「未検証事項」節参照）。
- **成果物出力先**: 本リポジトリ外のスクラッチディレクトリ（`quality-artifacts/` 相当）。本リポジトリには
  本レポートのみコミットする。

## 各段の結果サマリ

| フェーズ | 生成成果物数 | gate_status | スキーマ検証結果 |
|---|---|---|---|
| オーケストレーター（ルーティング） | RoutingDecision 1件 | passed | handoff-envelope: valid |
| risk-analysis | RiskRegister 4件（RISK-001〜004） | passed-with-risks | handoff-envelope: valid / risk-item ×4: valid |
| TRA | HTC 4件・DTC 7件・3色分析1件 | passed-with-risks | handoff-envelope: valid / detailed-test-condition ×7: valid |
| TAD | TAE 4件・割当マトリクス1件 | passed-with-risks | handoff-envelope: valid / test-architecture-element ×4: valid |
| TDD/TI | COV 8件・TC 8件・保証ステートメント6件 | passed-with-risks | handoff-envelope: valid / coverage-item ×8, test-case ×8, assurance-statement ×6: valid |
| traceability-management | TraceabilityMatrix・TestSpaceMatrix 各1件 | **blocked**（DTC-006未接続を検出したため仕様通り） | handoff-envelope: valid |

trace_ids はチェーンとして連続していることを機械確認した（REQ→RISK→HTC→DTC→TAE→COV→TC。
全DTCがいずれかのTAEに割当済み、全COVが実在するDTC/TAEを参照、全TCが実在するCOVを参照）。
未接続の唯一の例外は意図的に作成した DTC-006（`source_refs` 空）であり、これは
`traceability-management` の `disconnected_nodes` として正しく検出された（`missing_upstream_link`）。
追加テストとして DTC-001 の `source_refs` のみを空にしたコピー（`DTC-001-broken-copy`）も作成し、
同様に検出されることを確認した。

## 発見された改善点

1. **複合フロー時の `RoutingDecision.routed_skill` の表現形式が未規定**（quality-orchestrator/SKILL.md）。
   SKILL.md の出力例は単体ルーティングのケースのみを示しており、「risk-analysis→TRA→TAD→TDD/TI」の
   ように複数スキルへの進行管理を行う場合に `routed_skill` へ何を入れるべきか（配列か、フロー名の
   固定文字列か）の規定がない。本試行ではカンマ区切り文字列で代用したが、恣意的である。改訂時に
   複合フロー用の出力形状例を追加すべき。
2. **`TestArchitectureElement.thickness` の語彙が正規出典間で揺れている**。
   test-process-research-summary-test-design.md §6.3 の JSON 例は `"thickness": "deep"` だが、
   test-architecture-design/SKILL.md 手順4本文は `thick`/`standard`/`narrow`/`delegate` の4値を明示する。
   `test-architecture-element.schema.json` は自由文字列（enum制約なし）のため実行時エラーにはならない
   ものの、スキーマの `description` が `deep` を例示しており誤解を招く。スキーマの `description` を
   SKILL.md 側の4値に合わせて修正するか、両語彙の対応を明記すべき。
3. **`assurance-statement.schema.json` の `technique` フィールドが AJV strict mode で警告を出す**。
   `type: ["string", "array"]` のユニオン型を使用しているため、`ajv-cli` 実行時に
   `strict mode: use allowUnionTypes` という警告ログが出力される（バリデーション結果自体は valid）。
   複数技法を1件の保証ステートメントで引用する実例（本試行の TC-003/004 対応ステートメントで
   `["BB-02", "BB-03"]` を使用）が既存のSKILL.md・スキーマのどちらにも存在しなかったため、実行者が
   形式を都度判断する必要があった。スキーマに `strict: false` 相当の配慮を明記するか `oneOf` 形式へ
   の書き換え、または複数技法引用時の実例追加を検討すべき。
4. **ルーティングの誤分類は発生しなかった（確認済み）**。相談文「この決済API仕様書からテストケース
   一式まで作りたい」は8ステップ推論で REQ/RISK/TEST ノードに正しく分類され、「一気通し」の言い回し
   から複合フロー判定に至った。ルーティング表（routing-table.md）の該当4行と整合していた。
5. **質問数超過は発生しなかった（確認済み。ただし発火経路自体は未実行）**。オーケストレーターの
   明確化質問は0回（相談文のスコープが文言上明確だったため手順3をスキップ）で1回以内の制約を
   満たした。ただし本試行は終始「上流成果物あり」のハッピーパスで進んだため、各スキルの「上流成果物
   なし時の振る舞い」の3件質問ロジック、オーケストレーターの曖昧依頼での1回明確化質問、TAD/TDD-TI の
   簡易 TAE インライン合成といった**コールドスタート系の分岐は今回一度も発火していない**。SKILL.md の
   記述上は読み違えが生じなかったが、これは「実行して確認した」ではなく「記述を机上で読んで確認した」
   にとどまる。実行検証は「未検証事項」節に再掲する。
6. **ゲート判定基準（pipeline-gates.md §8.1〜8.4）は迷いなく適用できた（確認済み）**。各段の
   gate_status（passed-with-risks × 4、blocked × 1）は表の観点にそのまま照らして機械的に判定でき、
   曖昧な判断は生じなかった。
7. **未接続検出は仕様通り機能した（確認済み）**。`source_refs` が空の DTC を意図的に混入させたところ、
   traceability-management の手順どおり `missing_upstream_link` として検出され、`gate_status: blocked`
   に正しく遷移した。多対多関係（1つの RISK が複数 DTC にリンクする等）を誤って未接続と判定する
   誤検出も発生しなかった。
8. **ID体系・スキーマの桁数規約は一貫していた（確認済み）**。全スキーマが `^PREFIX-[0-9]+$` の可変桁
   パターンを採用しており、本試行で使用した3桁ID（`RISK-001`等）はすべて問題なくバリデートできた。
9. **`ThreeColorAnalysisReport`・`ConditionAssignmentMatrix`・`TraceabilityMatrix`・`TestSpaceMatrix` は
   専用スキーマが Phase 1 時点で存在せず `schema_ref` がポインタ参照のみだが、SKILL.md の規定通りの
   運用であり実行に迷いは生じなかった（確認済み）**。ただし Phase 2 以降でこれらの成果物が増えた場合、
   `handoff-envelope.schema.json` の `content`（オブジェクト形式）と `items`（配列形式）のどちらを
   使うべきかの判断はスキル実装者の裁量に委ねられており、本試行では出典側の実例形状に合わせて
   使い分けた（HTC/DTC/TAE/COV/TC/RiskItemは`items`、分析レポート・マトリクス類は`content`）。
   この使い分けの原則自体は明文化されていないため、軽微な改善余地として記録する。

## 未検証事項

以下はロールプレイ試行の性質上、本試行では検証できていない。

- **オーケストレーターの代表依頼文10ケースのルーティング整合**（ガイド T12 の #0 追加受入観点）。本試行は
  単一の相談文1件を投入し、ルーティング表14行中4行との整合を確認したにとどまる。10ケース全行の分類は
  T11（#0 スキル作成）時に机上検証済みだが、T12 のパイプライン試行としては再実行していない。
- **コールドスタート系分岐の実行**（各スキルの「上流成果物なし時の3件質問」、オーケストレーターの曖昧
  依頼での1回明確化質問、TAD/TDD-TI の簡易 TAE インライン合成）。本試行はハッピーパス（上流成果物あり）
  で進んだため、これらの分岐は一度も発火していない。SKILL.md の記述レビューによる確認のみで、実行による
  確認は未了（改善点5参照）。
- 実 Claude Code セッションにおける各スキルの `description` による自動発火の精度（本試行はスキル名を
  明示的に指定してSKILL.mdの手順を人手で追跡したものであり、自然言語相談文からの自動トリガーは
  未検証）。
- 明確化質問（1回まで／3件まで）を実際にユーザーに提示し、回答を待って処理を継続する対話的フローの
  実挙動（本試行はすべて「回答が得られない場合」の代替パスを取らずに済むスコープの相談文だったため、
  質問→応答待ち→再開のUXは未検証）。
- 複数スキルが実際に個別のサブエージェント・別プロセスとして起動された場合のハンドオフエンベロープ
  受け渡しの実装（本試行は単一エージェント内でのファイルベースの受け渡しを模擬したのみ）。
- 大規模・実プロダクト規模の仕様書（本試行は1〜2ページ相当のサンプル）における質問数・処理時間の
  スケーラビリティ。

## 受入基準チェック

- [x] パイプライン一気通しで全段のエンベロープが生成され、全て handoff-envelope.schema.json に valid
- [x] 成果物（RISK/HTC/DTC/TAE/COV/TC/保証ステートメント）の個別スキーマ検証も valid
- [x] trace_ids がチェーンとして連続している（REQ→RISK→HTC→DTC→TAE→COV→TC）
- [x] 未接続検出テストが機能する（DTC-006、および追加テストの DTC-001-broken-copy）
- [x] 試行レポートがコミットされている
