# 5観点レビューチェックリスト

本ファイルは quality-artifact-review の手順2で使うチェックリストである。
観点の定義の正典は
[test-process-research-summary-test-design.md §8.5（成果物品質レビュー）](../../../docs/test-techniques/test-process-research-summary-test-design.md#85-成果物品質レビュー)
であり、各チェックはその5観点をハンドオフエンベロープ運用（複合フロー）に
適用するための具体化である。正典の再記述はせず、必要箇所への
ポインタで参照する。

## 1. 文書点（document_quality）

正典チェック: 文書体系、情報量、表現統一、更新性、レビューしやすさ。

- エンベロープ間で同種フィールドの記法・列挙規約が統一されているか
  （例: `trace_ids` が全列挙か端点のみかの混在は不整合として報告する）。
- 各 artifact の `schema_ref` は現存する最も厳密な契約を指しているか
  （repo-local schema が存在するのに docs アンカー参照のままなら、
  再検証未実施として報告する。
  [schemas/README.md の content/items 使い分け](../../../schemas/README.md)
  参照）。
- 成果物単独で読者が文脈を復元できるか（他エンベロープの散在記述に
  依存していないか）。

## 2. 工程一貫性（process_consistency）

正典チェック: 前工程の成果物が次工程で使われていることが分かるか。

- 前工程の出力 ID 群が後工程の参照フィールド（`risk_refs`、
  `assigned_conditions`、`coverage_item_refs` 等）で実際に消費されているか。
- **前工程の約束と後工程の実施の突合**: 前工程エンベロープの
  `assumptions`/`open_questions` が下流工程に委ねた作業
  （例:「requirement_refs はトレーサビリティ付与段階で紐付ける」）が、
  当該下流工程で実施されたか。未実施なら所見として報告する。
- レビュー対象の工程範囲から期待される前工程成果物が欠落していないか
  （欠落は severity=blocker。SKILL.md 手順1）。

## 3. トレーサビリティ（traceability）

正典チェック: ID が一意で、要求から結果まで追えるか。

- バンドル内に traceability-management の `TraceabilityMatrix` があれば、
  その切断・未到達・advisory 所見を引用して評価する（リンク検査の
  再実行はしない。役割分担）。無ければ「検査未実施」を所見として報告する。
- ID の一意性・prefix 規約が
  [quality-knowledge-schema.md §1.2（ID 体系）](../../../docs/quality-models/quality-knowledge-schema.md#12-id-体系と既存データ契約との対応)
  と整合しているか。
- 正式な schema を持たない informal なノード参照（暫定 ID 等）が
  ゲート判定に影響しない位置に留まっているか。

## 4. 説明責任（accountability）

正典チェック: AI agent の出力理由、前提、不明点、採用・不採用理由が
残っているか。

- 暫定性・前提がエンベロープ `assumptions[]` に `{field,value,reason}`
  形式で記録され、reason が根拠（正典・実測・裁定）を指しているか。
- **裁定・決定のライフサイクル**: 人間（owner）の裁定・スコープ決定が
  後から追跡できる形で記録されているか。裁定結果が後工程の rationale に
  散在するだけで、裁定対象を報告した元エンベロープの `open_questions` が
  未解決のまま残っていないか（エンベロープ間の状態矛盾として報告する）。
- 判定に承認者・判断主体が明示されているか（例: release_decision の
  approver。
  [ギャップ分析報告書のアーティファクトチェックリスト](../../../docs/quality-management/software-quality-gap-analysis-report.md#収集すべきアーティファクトチェックリスト)
  の最低条件）。代替記録が明示されていれば minor に留める。

## 5. 技術的妥当性（technical_validity）

正典チェック: モデリング、技法、カバレッジ、リスク反映が適切か。

- リスクレベル→テスト深度（厚み）の変換が
  [testing-standards-and-assurance-concepts.md §4.2](../../../docs/test-techniques/testing-standards-and-assurance-concepts.md#42-リスク--テスト深度の変換手順)
  のポリシーに沿い、逸脱（高リスクの delegate 等）に説明があるか。
- 技法選択がカタログ ID で引用され、カバレッジ主張に対応する
  カウンターメトリクス（not_covered、fault_detection_evidence 等）が
  併記されているか（[quality-metrics-pitfalls の原則3]
  はギャップ分析報告書の
  [推奨メトリクスと暫定閾値](../../../docs/quality-management/software-quality-gap-analysis-report.md#推奨メトリクスと暫定閾値)
  経由で参照）。
- 保証ステートメントが全テストケースをカバーし、オラクルの種類と強度・
  盲点（known_blind_spots）が明示されているか
  （[testing-standards §5 テストオラクル問題](../../../docs/test-techniques/testing-standards-and-assurance-concepts.md#5-テストオラクル問題-合否判定の根拠)）。

## severity 判定の適用メモ

severity の判定原則（blocker / major / minor / info の区分と
gate_status への導出）は [SKILL.md 手順3〜4](../SKILL.md#手順) を正とする。
本チェックリストの各項目は「所見を見つける」ためのものであり、
severity は事実の重さ（文書化＋緩和策の有無、下流への毀損の有無）で
決める。チェック項目に不合格 = 一律 major ではない。
