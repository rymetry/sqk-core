# パイプラインゲート観点

## 位置づけ

本ファイルは、複合フロー（risk-analysis 並行 → TRA → TAD → TDD/TI。
利用者が実行結果の整理まで求める場合は test-execution-support（TE）を
終端段に加えた5段）の各段を進めてよいかを判定するためのゲート観点を
定める
（[skill-ecosystem-design-plan.md §4「ゲート基準」](../../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#4-オーケストレーション設計)
の表を採用）。各行の詳細チェックリストは
[test-process-research-summary-test-design.md §8](../../../docs/test-techniques/test-process-research-summary-test-design.md#8-レビューゲート)
の該当節（TE 行のみ §4.8/§4.9 の実行タスク・完了条件を併用）を参照する。

ゲート判定そのものは quality-orchestrator ではなく
[quality-artifact-review](../../quality-artifact-review/SKILL.md) が行う
（[quality-orchestrator/SKILL.md 手順7](../SKILL.md) の委譲呼び出し）。
本ファイルのゲート表は、その委譲呼び出しで `review_scope_hint` として
渡す**入力チェックリスト**であり、quality-orchestrator は返された
`gate_status` の遷移（進行・停止）管理のみを担う。

## 改訂の注記

Phase 1 中の変更凍結（[phase1-implementation-guide.md T4](../../../docs/agent-ecosystem/phase1-implementation-guide.md)
の規定）は、統合試行（T12）の完了により解除済みである。以降の改訂は
実測・レビュー結果を根拠に通常の PR で行う。

## ゲート表（quality-artifact-review へ渡す段別の重点観点）

| フェーズ | ゲート観点（要約） | 詳細チェックリスト |
|---|---|---|
| TRAレビュー | 使われ方・仕組み・全体像・リスク・テスト条件・パラメーター・不明点の分離 | [§8.1 TRA レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#81-tra-レビュー) |
| TADレビュー | 構造・関係・厚み・担当・重複漏れ・粒度 | [§8.2 TAD レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#82-tad-レビュー) |
| TDDレビュー | パラメーター・値候補・制約・カバレッジ・技法・期待結果・ケース数 | [§8.3 TDD レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#83-tdd-レビュー) |
| TIレビュー | 実行順序・手順・自動化・証跡・再現性 | [§8.4 TI レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#84-ti-レビュー) |
| TEレビュー | 欠陥候補の再現性・flaky と欠陥の区別・再テスト/回帰範囲・証跡参照（`log_ref`） | [§4.8 テスト実行](../../../docs/test-techniques/test-process-research-summary-test-design.md#48-7-テスト実行te)・[§4.9 再テスト・回帰テスト](../../../docs/test-techniques/test-process-research-summary-test-design.md#49-8-再テスト回帰テスト)（実行タスクと完了条件）＋[§8.4 TI レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#84-ti-レビュー) |

quality-artifact-review は上表の段別観点に加えて、常に
[§8.5 成果物品質レビュー](../../../docs/test-techniques/test-process-research-summary-test-design.md#85-成果物品質レビュー)
の5観点（文書点・工程一貫性・トレーサビリティ・説明責任・技術的妥当性）
で所見を記録する（同スキル手順2）。上表は「その段で特に落としてはいけない
観点」を段別に重み付けするためのヒントである。

## `gate_status` 3値の導出と遷移

各段のゲート結果は、quality-artifact-review が所見の severity 分布から
機械的に導出する（[同 SKILL.md 手順3〜4](../../quality-artifact-review/SKILL.md)）。
quality-orchestrator はその結果を受けて遷移のみを適用する。

| `gate_status` | 導出（quality-artifact-review 手順4） | 遷移（quality-orchestrator 手順7） |
|---|---|---|
| `passed` | 所見が minor・info のみ、または所見なし | 次段へそのまま進める |
| `passed-with-risks` | blocker なし・major が1件以上 | 残存リスクを利用者・次段の入力に明示した上で次段へ進める |
| `blocked` | blocker が1件以上（前工程成果物の欠落・進行不能の矛盾） | 次段へ進めず、利用者に理由を添えて返す |

**短絡則**: 段のスキル自身が `blocked` を返した場合は、委譲呼び出しを
行わずその段を `blocked` として扱う（quality-orchestrator 手順7）。

severity の付与原則（文書化済みの仮定＋緩和策つきの逸脱は minor、
未解決のまま下流の期待値・妥当性を毀損する事項は major、前工程成果物の
欠落・進行不能の矛盾は blocker）は
[quality-artifact-review/SKILL.md 手順3](../../quality-artifact-review/SKILL.md)
を正とする。

## 関連ドキュメント

- [quality-artifact-review/SKILL.md](../../quality-artifact-review/SKILL.md) — ゲート判定の委譲先（severity 付与と `gate_status` 導出の正）
- [routing-table.md](./routing-table.md) — 第2段階ルーティング表
- [skill-ecosystem-design-plan.md §4](../../../docs/agent-ecosystem/skill-ecosystem-design-plan.md#4-オーケストレーション設計) — ゲート基準の正典
- [phase2-implementation-guide.md T12・T3b](../../../docs/agent-ecosystem/phase2-implementation-guide.md#t12-ゲート判定の-quality-artifact-review14-への委譲) — 委譲の実施根拠（受入基準を含む）
